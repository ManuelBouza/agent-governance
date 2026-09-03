"""Extracted MG1 topology harness implementation."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import subprocess
import time
from pathlib import Path
from typing import Any

from .aggregation import aggregate_candidate_trials
from .evidence import _validate_partial
from .frozen_inputs import _load_json, _sha256, load_frozen_inputs
from .models import (
    CORPUS_PATH,
    ENVELOPE_PATH,
    HARNESS_PATH,
    MANIFEST_PATH,
    ORACLE_PATH,
    REPO_ROOT,
    TOPOLOGIES_PATH,
    FrozenInputs,
    HarnessError,
    TrialSpec,
)
from .observability import _observed_skill_reads, _validate_model_result
from .scheduling import _trial_prompt, all_possible_trials, stage_schedule
from .scoring import apply_selection_rule, compute_candidate_metrics, select_single_family_reference
from .storage import _json_dump


def load_trials(path: Path) -> list[dict[str, Any]]:
    trials: list[dict[str, Any]] = []
    try:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                if line.strip():
                    value = json.loads(line)
                    if not isinstance(value, dict):
                        raise HarnessError(f"{path}:{line_number}: expected object")
                    trials.append(value)
    except (OSError, json.JSONDecodeError) as exc:
        raise HarnessError(f"cannot load trials from {path}: {exc}") from exc
    return trials


def score_matrix(args: argparse.Namespace) -> int:
    inputs = load_frozen_inputs()
    output = args.output.resolve()
    validate_complete_evidence(inputs, output)
    metadata = _load_json(output / "run-metadata.json")
    trials = load_trials(output / "trials.jsonl")
    deterministic = _load_json(output / "deterministic-evidence.json")
    candidates = (
        ["B0", "B1"]
        if metadata["status"] == "BLOCKED_NO_REFERENCE"
        else inputs.oracle["candidate_ids"]
    )
    metrics = {
        candidate: compute_candidate_metrics(inputs, candidate, trials, deterministic)
        for candidate in candidates
    }
    selection = (
        _load_json(output / "selection.json")
        if len(candidates) == 2
        else apply_selection_rule(inputs, metrics)
    )
    _json_dump(output / "metrics.json", metrics)
    _json_dump(output / "selection.json", selection)
    return 0


def _validate_run_identity(inputs: FrozenInputs, metadata: dict[str, Any]) -> None:
    method = inputs.oracle["trial_method"]
    if metadata.get("status") not in {"COMPLETE", "BLOCKED_NO_REFERENCE"}:
        raise HarnessError("incomplete V10 execution cannot be scored")
    if (
        metadata.get("oracle_id") != inputs.oracle["oracle_id"]
        or metadata.get("execution_epoch") != inputs.oracle["execution_epoch"]
        or metadata.get("trial_envelope_id") != inputs.oracle["trial_envelope_id"]
        or metadata.get("full_acceptance") is not True
        or metadata.get("model") != "gpt-5.6-sol"
        or metadata.get("effort") != "medium"
        or metadata.get("host") != "Codex"
        or metadata.get("timeout_seconds") != method["timeout_seconds_per_model_attempt"]
    ):
        raise HarnessError("mismatched V10 execution identity/configuration")
    _validate_executed_runner_provenance(metadata)
    for path in (ORACLE_PATH, CORPUS_PATH, TOPOLOGIES_PATH, MANIFEST_PATH, ENVELOPE_PATH):
        relative = path.relative_to(REPO_ROOT).as_posix()
        if metadata["frozen_asset_sha256"].get(relative) != _sha256(path):
            raise HarnessError(f"run frozen input hash mismatch: {relative}")


def _validate_deterministic_evidence(output: Path) -> dict[str, Any]:
    deterministic = _load_json(output / "deterministic-evidence.json")
    if any(
        deterministic.get(field) != "PASS"
        for field in (
            "full_deterministic_regression",
            "profile_isolation_regression",
            "consumer_source_independence_regression",
        )
    ):
        raise HarnessError("mandatory deterministic evidence is not PASS")
    return deterministic


def _validate_schedule_records(
    inputs: FrozenInputs, output: Path, metadata: dict[str, Any]
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, TrialSpec],
    list[str],
    list[str],
    list[str],
]:
    method = inputs.oracle["trial_method"]
    trials = load_trials(output / "trials.jsonl")
    raw_trials = load_trials(output / "raw-trials.jsonl")
    attempts = load_trials(output / "attempts.jsonl")
    possible = {spec.key: spec for spec in all_possible_trials(inputs)}
    trial_keys = [
        f"{trial['case_id']}--{trial['candidate_id']}--r{trial['repetition']}" for trial in trials
    ]
    raw_keys = [raw["trial_key"] for raw in raw_trials]
    if len(set(trial_keys)) != len(trial_keys) or set(trial_keys) != set(raw_keys):
        raise HarnessError("valid trial/raw identity mismatch or duplication")
    if set(trial_keys) - set(possible):
        raise HarnessError("trial outside frozen V10 identity set")
    evaluated = (
        ["B0", "B1"]
        if metadata["status"] == "BLOCKED_NO_REFERENCE"
        else inputs.oracle["candidate_ids"]
    )
    expected_base = {
        spec.key
        for stage in (("R",) if len(evaluated) == 2 else ("R", "C"))
        for spec in stage_schedule(inputs, stage)
    }
    if not expected_base <= set(trial_keys):
        raise HarnessError("mandatory paired base schedule is incomplete")
    if metadata["status"] == "BLOCKED_NO_REFERENCE" and any(
        trial["candidate_id"] in {"F2", "G3"} for trial in trials
    ):
        raise HarnessError("challenger evidence exists despite no qualifying reference")
    lower = method["reference_stage_base_valid_observations"]
    upper = method["reference_stage_max_valid_observations"]
    if len(evaluated) == 4:
        lower, upper = method["overall_valid_observation_range_when_challengers_execute"]
    if not lower <= len(trials) <= upper:
        raise HarnessError("V10 valid observation count is outside the frozen stage range")
    return trials, raw_trials, attempts, possible, trial_keys, raw_keys, evaluated


def _started_threads(stdout_jsonl: str) -> list[str]:
    threads = []
    for line in stdout_jsonl.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "thread.started":
            threads.append(event["thread_id"])
    return threads


def _validate_trial_evidence(
    inputs: FrozenInputs,
    key: str,
    trial: dict[str, Any],
    raw: dict[str, Any],
    attempts: list[dict[str, Any]],
    spec: TrialSpec,
    workspaces: set[str],
    thread_ids: set[str],
) -> None:
    method = inputs.oracle["trial_method"]
    history = sorted(
        (item for item in attempts if item["trial_key"] == key),
        key=lambda item: item["attempt"],
    )
    invalid_history = (
        not 1 <= len(history) <= method["max_model_attempts_per_scheduled_observation"]
        or [item["attempt"] for item in history] != list(range(1, len(history) + 1))
        or [item["status"] for item in history] != ["FAILED"] * (len(history) - 1) + ["VALID"]
    )
    if invalid_history:
        raise HarnessError(f"{key}: invalid attempt count/order")
    if history[-1]["structured"] != trial or history[-1]["raw"] != raw:
        raise HarnessError(f"{key}: scored result differs from first valid attempt")
    if any(item["execution_epoch"] != inputs.oracle["execution_epoch"] for item in history):
        raise HarnessError(f"{key}: prior epoch attempt")
    _validate_partial(inputs, spec, trial, raw, model="gpt-5.6-sol", effort="medium")
    if (
        raw.get("prompt") != _trial_prompt(inputs, spec.case)
        or raw.get("returncode") != 0
        or raw.get("timeout_seconds") != method["timeout_seconds_per_model_attempt"]
    ):
        raise HarnessError(f"{key}: raw execution binding mismatch")
    if any(
        record["sha256"] != _sha256(REPO_ROOT / record["source"])
        for record in raw["materialization"]["files"]
    ):
        raise HarnessError(f"{key}: candidate bytes changed")
    workspace = raw["command"][raw["command"].index("--cd") + 1]
    if workspace in workspaces:
        raise HarnessError(f"{key}: workspace reused")
    workspaces.add(workspace)
    threads = _started_threads(raw["stdout_jsonl"])
    if len(threads) != 1 or set(threads) & thread_ids:
        raise HarnessError(f"{key}: missing or reused fresh thread")
    thread_ids.update(threads)
    _validate_model_result(inputs, spec, json.loads(raw["final_message"]))
    entrypoints, references, trace = _observed_skill_reads(inputs, spec, raw["stdout_jsonl"])
    reference_bytes = sum((REPO_ROOT / path).stat().st_size for path in references)
    observability_mismatch = (
        not trace
        or trial.get("host_trace_available") is not True
        or trial["activated_entrypoints"] != entrypoints
        or trial["loaded_reference_paths"] != references
        or trial["loaded_reference_bytes"] != reference_bytes
        or trial["observed_context_bytes"]
        != sum(trial["activation_surface_bytes"].values()) + reference_bytes
    )
    if observability_mismatch:
        raise HarnessError(f"{key}: observed host-read evidence mismatch")


def _validate_recomputed_outputs(
    inputs: FrozenInputs,
    output: Path,
    trials: list[dict[str, Any]],
    evaluated: list[str],
    deterministic: dict[str, Any],
) -> None:
    aggregates = [
        item
        for candidate in evaluated
        for item in aggregate_candidate_trials(inputs, candidate, trials)
    ]
    if aggregates != load_trials(output / "case-aggregates.jsonl"):
        raise HarnessError("persisted V10 case aggregates are not exactly recomputable")
    recomputed_metrics = {
        candidate: compute_candidate_metrics(inputs, candidate, trials, deterministic)
        for candidate in evaluated
    }
    if recomputed_metrics != _load_json(output / "metrics.json"):
        raise HarnessError("persisted V10 metrics are not exactly recomputable")
    expected_selection = (
        {
            "status": "BLOCKED",
            "selected_candidate": None,
            "reason": "neither B0 nor B1 qualifies; challenger stage not executed",
            "qualifying": select_single_family_reference(inputs, recomputed_metrics)["qualifying"],
            "scored": True,
        }
        if len(evaluated) == 2
        else apply_selection_rule(inputs, recomputed_metrics)
    )
    if expected_selection != _load_json(output / "selection.json"):
        raise HarnessError("persisted V10 selection is not exactly recomputable")


def validate_complete_evidence(inputs: FrozenInputs, output: Path) -> None:
    """Fail closed on V10 epoch, adaptive schedule, attempts, traces and aggregates."""
    metadata = _load_json(output / "run-metadata.json")
    _validate_run_identity(inputs, metadata)
    deterministic = _validate_deterministic_evidence(output)
    trials, raw_trials, attempts, possible, trial_keys, raw_keys, evaluated = (
        _validate_schedule_records(inputs, output, metadata)
    )
    raw_by_key = dict(zip(raw_keys, raw_trials, strict=True))
    workspaces: set[str] = set()
    thread_ids: set[str] = set()
    for key, trial in zip(trial_keys, trials, strict=True):
        _validate_trial_evidence(
            inputs,
            key,
            trial,
            raw_by_key[key],
            attempts,
            possible[key],
            workspaces,
            thread_ids,
        )
    _validate_recomputed_outputs(inputs, output, trials, evaluated, deterministic)


def _validate_executed_runner_provenance(metadata: dict[str, Any]) -> None:
    recorded = metadata.get("runner_sha256")
    if recorded == _sha256(HARNESS_PATH):
        return
    commit = metadata.get("executed_runner_git_commit")
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise HarnessError("executed runner changed without immutable Git provenance")
    relative = HARNESS_PATH.relative_to(REPO_ROOT).as_posix()
    try:
        source = subprocess.check_output(
            ["git", "show", f"{commit}:{relative}"], cwd=REPO_ROOT, stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as exc:
        raise HarnessError("cannot resolve executed runner Git provenance") from exc
    normalized_digests = {
        hashlib.sha256(source).hexdigest(),
        hashlib.sha256(source.replace(b"\r\n", b"\n")).hexdigest(),
        hashlib.sha256(source.replace(b"\n", b"\r\n")).hexdigest(),
    }
    if recorded not in normalized_digests:
        raise HarnessError("executed runner Git provenance does not match recorded hash")


def verify_deterministic(args: argparse.Namespace) -> int:
    inputs = load_frozen_inputs()
    output = args.output.resolve()
    evidence_path = output / "deterministic-evidence.json"
    evidence = _load_json(evidence_path)
    if evidence.get("oracle_id") != inputs.oracle["oracle_id"]:
        raise HarnessError("deterministic evidence does not match the current frozen oracle")

    command_groups = {
        "ruff_check": ["uv", "run", "--locked", "ruff", "check", "."],
        "ruff_format_check": ["uv", "run", "--locked", "ruff", "format", "--check", "."],
        "full_pytest": ["uv", "run", "--locked", "python", "-m", "pytest"],
        "profile_isolation": [
            "uv",
            "run",
            "--locked",
            "python",
            "-m",
            "pytest",
            "tests/test_profile_abstraction.py",
            "tests/test_source_maintainer_profile.py",
        ],
        "consumer_source_independence": [
            "uv",
            "run",
            "--locked",
            "python",
            "-m",
            "pytest",
            "tests/test_source_consumer_separation.py",
            "tests/test_consumer_v1_characterization.py",
        ],
    }
    runs: dict[str, Any] = {}
    for name, command in command_groups.items():
        started = time.monotonic()
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=args.timeout_seconds,
        )
        runs[name] = {
            "command": command,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "duration_seconds": round(time.monotonic() - started, 6),
        }
        print(f"{name}: {'PASS' if completed.returncode == 0 else 'FAIL'}", flush=True)

    evidence["verification_runs"] = runs
    evidence["full_deterministic_regression"] = (
        "PASS" if runs["full_pytest"]["returncode"] == 0 else "FAIL"
    )
    evidence["profile_isolation_regression"] = (
        "PASS" if runs["profile_isolation"]["returncode"] == 0 else "FAIL"
    )
    evidence["consumer_source_independence_regression"] = (
        "PASS" if runs["consumer_source_independence"]["returncode"] == 0 else "FAIL"
    )
    evidence["quality_gate"] = (
        "PASS"
        if all(runs[name]["returncode"] == 0 for name in ("ruff_check", "ruff_format_check"))
        else "FAIL"
    )
    evidence["runtime"] = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "network_required": False,
    }
    _json_dump(evidence_path, evidence)
    return 0 if all(run["returncode"] == 0 for run in runs.values()) else 1
