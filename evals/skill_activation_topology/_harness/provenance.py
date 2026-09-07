"""Evidence validation, deterministic verification, and scoring for MG1/T023 v13."""

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

from .aggregation import (
    finalized_candidate_aggregates,
    materiality_futility_certificate,
    qualification_futility_certificate,
)
from .evidence import _validate_partial
from .frozen_inputs import _load_json, _sha256, load_frozen_inputs
from .models import (
    CANDIDATE_HASHES_PATH,
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
from .scheduling import _trial_prompt, all_possible_trials
from .scoring import candidate_qualifies, compute_candidate_metrics, select_from_cost_bounded_metrics
from .storage import _json_dump


def load_trials(path: Path) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    try:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                if not line.strip():
                    continue
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise HarnessError(f"{path}:{line_number}: expected object")
                values.append(value)
    except (OSError, json.JSONDecodeError) as exc:
        raise HarnessError(f"cannot load trials from {path}: {exc}") from exc
    return values


def _frozen_paths() -> tuple[Path, ...]:
    return (
        ORACLE_PATH,
        CORPUS_PATH,
        TOPOLOGIES_PATH,
        MANIFEST_PATH,
        ENVELOPE_PATH,
        CANDIDATE_HASHES_PATH,
    )


def _validate_run_identity(inputs: FrozenInputs, metadata: dict[str, Any]) -> None:
    method = inputs.oracle["trial_method"]
    if metadata.get("status") not in {"COMPLETE", "BLOCKED_NO_REFERENCE"}:
        raise HarnessError("incomplete v13 execution cannot be scored")
    expected = {
        "oracle_id": inputs.oracle["oracle_id"],
        "execution_epoch": inputs.oracle["execution_epoch"],
        "corpus_id": inputs.oracle["corpus_id"],
        "trial_envelope_id": inputs.oracle["trial_envelope_id"],
        "presentation_revision": inputs.oracle["presentation_revision"],
        "capability_source_epoch": inputs.oracle["capability_source_epoch"],
        "candidate_freeze_sha": inputs.oracle["candidate_freeze_sha"],
        "full_acceptance": True,
        "model": "gpt-5.6-sol",
        "effort": "medium",
        "host": "Codex",
        "timeout_seconds": method["timeout_seconds_per_model_attempt"],
    }
    if any(metadata.get(key) != value for key, value in expected.items()):
        raise HarnessError("mismatched v13 execution identity/configuration")
    _validate_executed_runner_provenance(metadata)
    for path in _frozen_paths():
        relative = path.relative_to(REPO_ROOT).as_posix()
        if metadata.get("frozen_asset_sha256", {}).get(relative) != _sha256(path):
            raise HarnessError(f"run frozen input hash mismatch: {relative}")


def _validate_deterministic_evidence(output: Path) -> dict[str, Any]:
    evidence = _load_json(output / "deterministic-evidence.json")
    if any(
        evidence.get(field) != "PASS"
        for field in (
            "full_deterministic_regression",
            "profile_isolation_regression",
            "consumer_source_independence_regression",
        )
    ):
        raise HarnessError("mandatory deterministic evidence is not PASS")
    if evidence.get("provider_model_calls_issued_during_deterministic_gate") != 0:
        raise HarnessError("deterministic gate issued provider/model calls")
    freeze = evidence.get("freeze_and_holdout", {})
    if (
        freeze.get("status") != "PASS"
        or freeze.get("candidate_bytes_unchanged_since_freeze_a") is not True
        or freeze.get("exact_v12_prompt_reuse_count") != 0
        or freeze.get("false_activation_denominator") != 40
        or freeze.get("provider_model_calls_issued") != 0
    ):
        raise HarnessError("Freeze A / holdout deterministic evidence is invalid")
    return evidence


def _trial_key(trial: dict[str, Any]) -> str:
    return f"{trial['case_id']}--{trial['candidate_id']}--r{trial['repetition']}"


def _started_threads(stdout_jsonl: str) -> list[str]:
    threads: list[str] = []
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
    spec: TrialSpec,
    trial: dict[str, Any],
    raw: dict[str, Any],
    workspaces: set[str],
    threads_seen: set[str],
) -> None:
    key = spec.key
    _validate_partial(inputs, spec, trial, raw, model="gpt-5.6-sol", effort="medium")
    if (
        raw.get("prompt") != _trial_prompt(inputs, spec.case)
        or raw.get("returncode") != 0
        or raw.get("timeout_seconds")
        != inputs.oracle["trial_method"]["timeout_seconds_per_model_attempt"]
    ):
        raise HarnessError(f"{key}: raw execution binding mismatch")
    if any(
        record["sha256"] != _sha256(REPO_ROOT / record["source"])
        for record in raw["materialization"]["files"]
    ):
        raise HarnessError(f"{key}: candidate bytes changed")
    command = raw["command"]
    workspace = command[command.index("--cd") + 1]
    if workspace in workspaces:
        raise HarnessError(f"{key}: workspace reused")
    workspaces.add(workspace)
    threads = _started_threads(raw["stdout_jsonl"])
    if len(threads) != 1 or set(threads) & threads_seen:
        raise HarnessError(f"{key}: missing or reused fresh thread")
    threads_seen.update(threads)
    _validate_model_result(inputs, spec, json.loads(raw["final_message"]))
    entrypoints, references, trace = _observed_skill_reads(inputs, spec, raw["stdout_jsonl"])
    reference_bytes = sum((REPO_ROOT / path).stat().st_size for path in references)
    if (
        not trace
        or trial.get("host_trace_available") is not True
        or trial["activated_entrypoints"] != entrypoints
        or trial["loaded_reference_paths"] != references
        or trial["loaded_reference_bytes"] != reference_bytes
        or trial["observed_context_bytes"]
        != sum(trial["activation_surface_bytes"].values()) + reference_bytes
    ):
        raise HarnessError(f"{key}: host-observed activation/context evidence mismatch")


def _complete_candidate(inputs: FrozenInputs, candidate: str, trials: list[dict[str, Any]]) -> bool:
    return len(finalized_candidate_aggregates(inputs, candidate, trials)) == len(inputs.corpus["cases"])


def _terminal_certificate(
    inputs: FrozenInputs,
    candidate: str,
    trials: list[dict[str, Any]],
    reference_metrics: dict[str, Any] | None,
) -> dict[str, Any]:
    certificate = qualification_futility_certificate(inputs, candidate, trials)
    if not certificate["terminal"] and reference_metrics is not None:
        certificate = materiality_futility_certificate(inputs, candidate, trials, reference_metrics)
    return certificate


def _validate_recomputed_outputs(
    inputs: FrozenInputs,
    output: Path,
    trials: list[dict[str, Any]],
    deterministic: dict[str, Any],
    status: str,
) -> None:
    aggregates = [
        item
        for candidate in inputs.oracle["candidate_ids"]
        for item in finalized_candidate_aggregates(inputs, candidate, trials)
    ]
    if aggregates != load_trials(output / "case-aggregates.jsonl"):
        raise HarnessError("persisted v13 case aggregates are not exactly recomputable")

    if status == "BLOCKED_NO_REFERENCE":
        if any(trial["candidate_id"] in {"F2", "G3"} for trial in trials):
            raise HarnessError("challenger evidence exists despite no qualifying B2 reference")
        certificate = _terminal_certificate(inputs, "B2", trials, None)
        persisted = _load_json(output / "futility-certificates" / "B2.json")
        if not certificate["terminal"] or certificate != persisted:
            raise HarnessError("B2 no-reference futility certificate is not recomputable")
        selection = _load_json(output / "selection.json")
        if selection != {
            "status": "BLOCKED",
            "selected_candidate": None,
            "reason": "NO QUALIFYING SINGLE-FAMILY REFERENCE",
            "scored": True,
        }:
            raise HarnessError("persisted v13 no-reference selection is invalid")
        return

    if not _complete_candidate(inputs, "B2", trials):
        raise HarnessError("complete v13 decision requires a complete B2 reference")
    metrics: dict[str, dict[str, Any]] = {
        "B2": compute_candidate_metrics(inputs, "B2", trials, deterministic)
    }
    if not candidate_qualifies(inputs, metrics["B2"]):
        raise HarnessError("challenger stage exists without a qualifying B2 reference")

    futility: dict[str, dict[str, Any]] = {}
    for candidate in ("F2", "G3"):
        if _complete_candidate(inputs, candidate, trials):
            metrics[candidate] = compute_candidate_metrics(inputs, candidate, trials, deterministic)
            continue
        certificate_path = output / "futility-certificates" / f"{candidate}.json"
        if not certificate_path.is_file():
            raise HarnessError(f"{candidate}: incomplete challenger lacks futility certificate")
        certificate = _terminal_certificate(inputs, candidate, trials, metrics["B2"])
        persisted = _load_json(certificate_path)
        if not certificate["terminal"] or certificate != persisted:
            raise HarnessError(f"{candidate}: futility certificate is not recomputable")
        futility[candidate] = certificate

    if metrics != _load_json(output / "metrics.json"):
        raise HarnessError("persisted v13 metrics are not exactly recomputable")
    if _load_json(output / "metrics-reference.json") != {"B2": metrics["B2"]}:
        raise HarnessError("persisted B2 reference metrics are not exactly recomputable")
    reference_selection = _load_json(output / "reference-selection.json")
    if reference_selection.get("single_family_reference") != "B2" or reference_selection.get(
        "qualifying"
    ) != {"B2": True}:
        raise HarnessError("persisted v13 reference selection is invalid")

    selection = select_from_cost_bounded_metrics(inputs, "B2", metrics)
    selection["futility"] = futility
    if selection != _load_json(output / "selection.json"):
        raise HarnessError("persisted v13 selection is not exactly recomputable")


def validate_complete_evidence(inputs: FrozenInputs, output: Path) -> None:
    metadata = _load_json(output / "run-metadata.json")
    _validate_run_identity(inputs, metadata)
    deterministic = _validate_deterministic_evidence(output)
    trials = load_trials(output / "trials.jsonl")
    raw_trials = load_trials(output / "raw-trials.jsonl")
    attempts = load_trials(output / "attempts.jsonl")
    possible = {spec.key: spec for spec in all_possible_trials(inputs)}
    trial_keys = [_trial_key(trial) for trial in trials]
    raw_keys = [raw["trial_key"] for raw in raw_trials]
    if len(trial_keys) != len(set(trial_keys)) or set(trial_keys) != set(raw_keys):
        raise HarnessError("valid trial/raw identity mismatch or duplication")
    if set(trial_keys) - set(possible):
        raise HarnessError("trial outside frozen v13 identity set")
    attempt_valid_keys = [item["trial_key"] for item in attempts if item.get("status") == "VALID"]
    if sorted(attempt_valid_keys) != sorted(trial_keys):
        raise HarnessError("valid attempt journals do not match scored observations")

    raw_by_key = dict(zip(raw_keys, raw_trials, strict=True))
    workspaces: set[str] = set()
    threads_seen: set[str] = set()
    for key, trial in zip(trial_keys, trials, strict=True):
        _validate_trial_evidence(
            inputs, possible[key], trial, raw_by_key[key], workspaces, threads_seen
        )
    _validate_recomputed_outputs(
        inputs, output, trials, deterministic, metadata["status"]
    )


def score_matrix(args: argparse.Namespace) -> int:
    inputs = load_frozen_inputs()
    validate_complete_evidence(inputs, args.output.resolve())
    return 0


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
    normalized = {
        hashlib.sha256(source).hexdigest(),
        hashlib.sha256(source.replace(b"\r\n", b"\n")).hexdigest(),
        hashlib.sha256(source.replace(b"\n", b"\r\n")).hexdigest(),
    }
    if recorded not in normalized:
        raise HarnessError("executed runner Git provenance does not match recorded hash")


def verify_deterministic(args: argparse.Namespace) -> int:
    inputs = load_frozen_inputs()
    output = args.output.resolve()
    evidence_path = output / "deterministic-evidence.json"
    evidence = _load_json(evidence_path)
    if evidence.get("oracle_id") != inputs.oracle["oracle_id"]:
        raise HarnessError("deterministic evidence does not match current v13 oracle")
    scheduler = evidence.get("adaptive_scheduler_preflight", {})
    scenarios = scheduler.get("scenarios", {})
    required_scenarios = {
        "agreeing_pair_forward_progress",
        "conditional_third_forward_progress",
        "no_fourth_repetition",
        "critical_terminal",
        "full_reference_adaptive_dry_run",
    }
    module_root = REPO_ROOT / "evals" / "skill_activation_topology" / "_harness"
    expected_hashes = {
        name: hashlib.sha256((module_root / name).read_bytes()).hexdigest()
        for name in ("run_support.py", "aggregation.py", "scheduling.py", "scheduler_simulation.py")
    }
    if (
        scheduler.get("status") != "PASS"
        or scheduler.get("execution_epoch") != inputs.oracle["execution_epoch"]
        or scheduler.get("provider_model_calls_issued") != 0
        or set(scenarios) != required_scenarios
        or any(value.get("status") != "PASS" for value in scenarios.values())
        or scheduler.get("tested_module_sha256") != expected_hashes
        or scenarios["full_reference_adaptive_dry_run"].get("scheduled_observations") != 140
    ):
        raise HarnessError("provider-free v13 adaptive scheduler evidence is invalid")

    command_groups = {
        "candidate_integrity": [
            "uv", "run", "--locked", "python",
            "evals/skill_activation_topology/verify_v13_candidate_integrity.py",
        ],
        "holdout_integrity": [
            "uv", "run", "--locked", "python",
            "evals/skill_activation_topology/verify_v13_holdout_integrity.py",
        ],
        "ruff_check": ["uv", "run", "--locked", "ruff", "check", "."],
        "ruff_format_check": ["uv", "run", "--locked", "ruff", "format", "--check", "."],
        "code_health": ["uv", "run", "--locked", "python", "tools/code_health.py", "check", "--root", "."],
        "symbol_map": ["uv", "run", "--locked", "python", "tools/code_health.py", "map", "--root", "."],
        "full_pytest": ["uv", "run", "--locked", "python", "-m", "pytest"],
        "profile_isolation": [
            "uv", "run", "--locked", "python", "-m", "pytest",
            "tests/test_profile_abstraction.py", "tests/test_source_maintainer_profile.py",
        ],
        "consumer_source_independence": [
            "uv", "run", "--locked", "python", "-m", "pytest",
            "tests/test_source_consumer_separation.py", "tests/test_consumer_v1_characterization.py",
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
    evidence["full_deterministic_regression"] = "PASS" if runs["full_pytest"]["returncode"] == 0 else "FAIL"
    evidence["profile_isolation_regression"] = "PASS" if runs["profile_isolation"]["returncode"] == 0 else "FAIL"
    evidence["consumer_source_independence_regression"] = "PASS" if runs["consumer_source_independence"]["returncode"] == 0 else "FAIL"
    evidence["quality_gate"] = (
        "PASS"
        if all(
            runs[name]["returncode"] == 0
            for name in (
                "candidate_integrity", "holdout_integrity", "ruff_check",
                "ruff_format_check", "code_health", "symbol_map",
            )
        )
        else "FAIL"
    )
    evidence["provider_model_calls_issued_during_deterministic_gate"] = 0
    evidence["runtime"] = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "network_required": False,
    }
    _json_dump(evidence_path, evidence)
    return 0 if all(run["returncode"] == 0 for run in runs.values()) else 1
