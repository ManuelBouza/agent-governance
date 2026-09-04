"""Extracted MG1 topology harness implementation."""

from __future__ import annotations

import argparse
import platform
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .aggregation import (
    finalized_candidate_aggregates,
)
from .codex_adapter import _codex_version
from .evidence import build_deterministic_evidence, execute_logical_observation
from .frozen_inputs import _load_json, _sha256, load_frozen_inputs
from .host_preflight import run_host_preflight
from .models import (
    CORPUS_PATH,
    ENVELOPE_PATH,
    HARNESS_PATH,
    MANIFEST_PATH,
    ORACLE_PATH,
    REPO_ROOT,
    REQUIRED_CODEX_VERSION,
    TOPOLOGIES_PATH,
    WINDOWS_BACKEND_ORDER,
    WORKSPACE_FACTORY_ID,
    FrozenInputs,
    HarnessError,
    TrialSpec,
)
from .provenance import verify_deterministic
from .run_support import RunContext
from .scheduler_simulation import run_provider_free_scheduler_simulation
from .scheduling import scheduled_trials, stage_schedule
from .scoring import (
    candidate_qualifies,
    compute_candidate_metrics,
    select_from_cost_bounded_metrics,
    select_single_family_reference,
)
from .storage import _json_dump, _jsonl_dump


def validate_execution_config(inputs: FrozenInputs, args: argparse.Namespace) -> None:
    method = inputs.oracle["trial_method"]
    if args.model != "gpt-5.6-sol" or args.effort != "medium" or platform.system() != "Windows":
        raise HarnessError("required live cell is native Windows / GPT-5.6 Sol / Medium")
    if _codex_version(args.codex_command) != REQUIRED_CODEX_VERSION:
        raise HarnessError(f"required Codex CLI baseline is {REQUIRED_CODEX_VERSION}")
    if args.timeout_seconds != method["timeout_seconds_per_model_attempt"]:
        raise HarnessError("per-attempt timeout must match the frozen oracle")
    if args.full_acceptance and (args.case or args.candidate or args.repetition):
        raise HarnessError("full acceptance cannot use trial filters")
    if (
        len(stage_schedule(inputs, "R"))
        != method["reference_stage_full_completion_base_valid_observations"]
    ):
        raise HarnessError("reference-stage base schedule does not match the frozen oracle")
    if (
        len(stage_schedule(inputs, "C"))
        != method["challenger_stage_full_completion_base_valid_observations"]
    ):
        raise HarnessError("challenger-stage base schedule does not match the frozen oracle")


def _frozen_hashes() -> dict[str, str]:
    return {
        path.relative_to(REPO_ROOT).as_posix(): _sha256(path)
        for path in (ORACLE_PATH, CORPUS_PATH, TOPOLOGIES_PATH, MANIFEST_PATH, ENVELOPE_PATH)
    }


def _resume_metadata(
    inputs: FrozenInputs, args: argparse.Namespace, output: Path
) -> dict[str, Any]:
    if not output.is_dir():
        raise HarnessError("resume requires an existing evidence root")
    metadata = _load_json(output / "run-metadata.json")
    expected_identity = {
        "oracle_id": inputs.oracle["oracle_id"],
        "execution_epoch": inputs.oracle["execution_epoch"],
        "corpus_id": inputs.oracle["corpus_id"],
        "trial_envelope_id": inputs.oracle["trial_envelope_id"],
        "presentation_revision": inputs.oracle["presentation_revision"],
        "capability_source_epoch": inputs.oracle["capability_source_epoch"],
        "model": args.model,
        "effort": args.effort,
        "timeout_seconds": args.timeout_seconds,
    }
    if any(metadata.get(key) != value for key, value in expected_identity.items()):
        raise HarnessError("resume execution identity differs from frozen V12 run")
    if metadata.get("runner_sha256") != _sha256(HARNESS_PATH):
        raise HarnessError("resume runner identity changed")
    for relative, digest in _frozen_hashes().items():
        if metadata["frozen_asset_sha256"].get(relative) != digest:
            raise HarnessError(f"resume frozen asset changed: {relative}")
    metadata.setdefault("resume_records", []).append(
        {"resumed_at": datetime.now(UTC).isoformat(), "prior_status": metadata["status"]}
    )
    preflight = _load_json(output / "host-preflight.json")
    identity_mismatch = (
        preflight.get("status") != "PASS"
        or metadata.get("selected_sandbox") != preflight.get("selected_sandbox")
        or metadata.get("selected_backend") != preflight.get("selected_backend")
        or metadata.get("selected_workspace_acl_profile")
        != preflight.get("selected_workspace_acl_profile")
    )
    if identity_mismatch:
        raise HarnessError("resume host preflight/profile identity mismatch")
    return metadata


def _initial_metadata(
    inputs: FrozenInputs, args: argparse.Namespace, workspace_parent: Path
) -> dict[str, Any]:
    return {
        "oracle_id": inputs.oracle["oracle_id"],
        "execution_epoch": inputs.oracle["execution_epoch"],
        "corpus_id": inputs.oracle["corpus_id"],
        "trial_envelope_id": inputs.oracle["trial_envelope_id"],
        "presentation_revision": inputs.oracle["presentation_revision"],
        "capability_source_epoch": inputs.oracle["capability_source_epoch"],
        "host": "Codex",
        "platform": f"native Windows ({platform.platform()})",
        "model": args.model,
        "effort": args.effort,
        "codex_cli": _codex_version(args.codex_command),
        "runner_sha256": _sha256(HARNESS_PATH),
        "frozen_asset_sha256": _frozen_hashes(),
        "workers": args.workers,
        "timeout_seconds": args.timeout_seconds,
        "max_model_attempts_per_scheduled_observation": inputs.oracle["trial_method"][
            "max_model_attempts_per_scheduled_observation"
        ],
        "full_acceptance": args.full_acceptance,
        "clean_context": "one new codex exec thread and disposable workspace per attempt",
        "workspace_parent": str(workspace_parent),
        "workspace_factory": WORKSPACE_FACTORY_ID,
        "sandbox_selection_order": ["read-only", "workspace-write"],
        "windows_backend_selection_order": list(WINDOWS_BACKEND_ORDER),
        "stimulus_rule": "exact corpus prompt, two newlines, frozen neutral suffix",
        "stage_state": "REFERENCE_BASE_PENDING" if args.full_acceptance else "FILTERED_PENDING",
        "status": "RUNNING",
        "started_at": datetime.now(UTC).isoformat(),
    }


def _block_deterministic_gate(output: Path, metadata: dict[str, Any]) -> int:
    metadata.update(status="BLOCKED", stage_state="DETERMINISTIC_GATE_FAILED")
    _json_dump(output / "run-metadata.json", metadata)
    _json_dump(
        output / "selection.json",
        {
            "status": "BLOCKED",
            "selected_candidate": None,
            "reason": "mandatory deterministic verification failed before live execution",
        },
    )
    return 1


def _block_preflight(
    inputs: FrozenInputs, output: Path, metadata: dict[str, Any], preflight: dict[str, Any]
) -> int:
    reason = preflight["reason"]
    metadata.update(
        status="BLOCKED",
        stage_state=f"{reason}_FAILED",
        selected_backend=None,
        selected_sandbox=None,
        selected_workspace_acl_profile=None,
        synthetic_canary_prompts_issued=len(preflight.get("records", [])),
        completed_valid_observations=0,
        acceptance_prompts_issued=0,
    )
    _json_dump(output / "run-metadata.json", metadata)
    _json_dump(
        output / "selection.json",
        {"status": "BLOCKED", "selected_candidate": None, "reason": reason, "scored": False},
    )
    _json_dump(
        output / "completeness.json",
        {
            "execution_epoch": inputs.oracle["execution_epoch"],
            "stage_state": f"{reason}_FAILED",
            "completed_valid_observations": 0,
            "acceptance_prompts_issued": 0,
            "acceptance_complete": False,
            "partial_scoring_permitted": False,
        },
    )
    return 1


def _start_new_run(
    inputs: FrozenInputs,
    args: argparse.Namespace,
    output: Path,
    workspace_parent: Path,
) -> tuple[dict[str, Any], int | None]:
    if output.exists() and any(output.iterdir()):
        raise HarnessError("refusing to overwrite existing run evidence")
    output.mkdir(parents=True, exist_ok=True)
    metadata = _initial_metadata(inputs, args, workspace_parent)
    _json_dump(output / "run-metadata.json", metadata)
    if not args.full_acceptance:
        return metadata, None
    deterministic = build_deterministic_evidence(inputs)
    deterministic["adaptive_scheduler_preflight"] = run_provider_free_scheduler_simulation(inputs)
    _json_dump(output / "deterministic-evidence.json", deterministic)
    verify_args = argparse.Namespace(output=output, timeout_seconds=900)
    if verify_deterministic(verify_args) != 0:
        return metadata, _block_deterministic_gate(output, metadata)
    preflight = run_host_preflight(inputs, args, output, workspace_parent)
    if preflight["status"] != "PASS":
        return metadata, _block_preflight(inputs, output, metadata, preflight)
    metadata["selected_backend"] = preflight["selected_backend"]
    metadata["selected_sandbox"] = preflight["selected_sandbox"]
    metadata["selected_workspace_acl_profile"] = preflight["selected_workspace_acl_profile"]
    metadata["effective_host_profile"] = _load_json(output / "host-preflight.json")["records"][-1][
        "effective_host_profile"
    ]
    return metadata, None


def _filtered_schedule(inputs: FrozenInputs, args: argparse.Namespace) -> list[TrialSpec]:
    schedule = scheduled_trials(inputs)
    if args.case:
        schedule = [spec for spec in schedule if spec.case["id"] in set(args.case)]
    if args.candidate:
        schedule = [spec for spec in schedule if spec.candidate_id in set(args.candidate)]
    if args.repetition:
        schedule = [spec for spec in schedule if spec.repetition in set(args.repetition)]
    if not schedule:
        raise HarnessError("trial filters selected no trials")
    return schedule


def _run_filtered(context: RunContext) -> int:
    terminal = context.stop_for_execution_state(
        *context.execute_schedule(_filtered_schedule(context.inputs, context.args)), "FILTERED"
    )
    if terminal is not None:
        return terminal
    context.export_evidence("FILTERED_COMPLETE", "COMPLETE")
    return 0


def _block_no_reference(
    context: RunContext, candidates: list[str], trials: list[dict[str, Any]]
) -> int:
    _json_dump(context.output / "metrics-reference.json", {})
    _json_dump(
        context.output / "reference-selection.json",
        {
            "status": "BLOCKED",
            "single_family_reference": None,
            "reason": "both single-family candidates are FUTILE_QUALIFICATION",
            "futility": context.terminal_candidates,
        },
    )
    _json_dump(
        context.output / "selection.json",
        {
            "status": "BLOCKED",
            "selected_candidate": None,
            "reason": "NO QUALIFYING SINGLE-FAMILY REFERENCE",
            "scored": True,
        },
    )
    _jsonl_dump(
        context.output / "case-aggregates.jsonl",
        [
            item
            for candidate in candidates
            for item in finalized_candidate_aggregates(context.inputs, candidate, trials)
        ],
    )
    context.export_evidence("REFERENCE_FUTILE_NO_QUALIFIER", "BLOCKED_NO_REFERENCE")
    return 1


def _select_reference(
    context: RunContext,
    candidates: list[str],
    survivors: list[str],
    metrics: dict[str, dict[str, Any]],
) -> tuple[str | None, int | None]:
    if not survivors:
        return None, _block_no_reference(context, candidates, context.trials())
    if len(survivors) == 1:
        reference_id = survivors[0]
        reference = {
            "status": "REFERENCE_SELECTED",
            "single_family_reference": reference_id,
            "qualifying": {
                reference_id: candidate_qualifies(context.inputs, metrics[reference_id])
            },
            "futility": context.terminal_candidates,
        }
    else:
        reference = select_single_family_reference(context.inputs, metrics)
        reference_id = reference["single_family_reference"]
    if reference_id is None:
        raise HarnessError("completed reference stage produced no valid reference")
    context.metadata["single_family_reference"] = reference_id
    _json_dump(context.output / "reference-selection.json", reference)
    _json_dump(context.output / "metrics-reference.json", metrics)
    return reference_id, None


def _complete_decision(
    context: RunContext,
    reference_id: str,
    reference_metrics: dict[str, dict[str, Any]],
    deterministic: dict[str, Any],
) -> int:
    candidates = context.inputs.oracle["trial_method"]["challenger_stage_candidates"]
    stopped = context.adaptive_stage("C", candidates, reference_metrics[reference_id])
    if stopped is not None:
        return stopped
    trials = context.trials()
    survivors = [
        candidate for candidate in candidates if candidate not in context.terminal_candidates
    ]
    metrics = dict(reference_metrics)
    metrics.update(
        {
            candidate: compute_candidate_metrics(context.inputs, candidate, trials, deterministic)
            for candidate in survivors
        }
    )
    selection = select_from_cost_bounded_metrics(context.inputs, reference_id, metrics)
    selection["futility"] = context.terminal_candidates
    _json_dump(context.output / "metrics.json", metrics)
    _json_dump(context.output / "selection.json", selection)
    _jsonl_dump(
        context.output / "case-aggregates.jsonl",
        [
            item
            for candidate in context.inputs.oracle["candidate_ids"]
            for item in finalized_candidate_aggregates(context.inputs, candidate, trials)
        ],
    )
    context.export_evidence("COST_BOUNDED_DECISION_COMPLETE", "COMPLETE")
    return 0


def _run_full(context: RunContext) -> int:
    deterministic = _load_json(context.output / "deterministic-evidence.json")
    candidates = context.inputs.oracle["trial_method"]["reference_stage_candidates"]
    stopped = context.adaptive_stage("R", candidates)
    if stopped is not None:
        return stopped
    trials = context.trials()
    survivors = [
        candidate for candidate in candidates if candidate not in context.terminal_candidates
    ]
    metrics = {
        candidate: compute_candidate_metrics(context.inputs, candidate, trials, deterministic)
        for candidate in survivors
    }
    reference_id, terminal = _select_reference(context, candidates, survivors, metrics)
    if terminal is not None:
        return terminal
    return _complete_decision(context, reference_id, metrics, deterministic)


def run_matrix(args: argparse.Namespace) -> int:
    inputs = load_frozen_inputs()
    validate_execution_config(inputs, args)
    output = args.output.resolve()
    workspace_parent = Path(tempfile.gettempdir()).resolve()
    if args.resume:
        metadata = _resume_metadata(inputs, args, output)
        terminal = None
    else:
        metadata, terminal = _start_new_run(inputs, args, output, workspace_parent)
    if terminal is not None:
        return terminal
    _json_dump(output / "run-metadata.json", metadata)
    context = RunContext(
        inputs, args, output, workspace_parent, metadata, execute_logical_observation
    )
    return _run_full(context) if args.full_acceptance else _run_filtered(context)
