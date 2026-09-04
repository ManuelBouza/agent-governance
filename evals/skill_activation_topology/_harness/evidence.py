"""Extracted MG1 topology harness implementation."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .frozen_inputs import _load_json, _sha256
from .materialization import _is_relative_to, _validate_fixture_evidence, materialize_candidate
from .models import (
    CORPUS_PATH,
    ENVELOPE_PATH,
    MANIFEST_PATH,
    MINIMAL_DISABLED_FEATURES,
    ORACLE_PATH,
    REPO_ROOT,
    TOPOLOGIES_PATH,
    WINDOWS_BACKEND_ORDER,
    WORKSPACE_FACTORY_ID,
    AttemptFailure,
    CapacityPause,
    FrozenInputs,
    HarnessError,
    HostSurfaceDrift,
    TrialSpec,
)
from .scheduling import validate_repetition
from .storage import _json_dump
from .trial_execution import run_trial


def _holdout_rotation_evidence(inputs: FrozenInputs) -> dict[str, Any]:
    relative = CORPUS_PATH.relative_to(REPO_ROOT).as_posix()
    try:
        change = subprocess.check_output(
            ["git", "log", "-1", "--format=%H", "--", relative],
            cwd=REPO_ROOT,
            text=True,
        ).strip()
        prior_bytes = subprocess.check_output(
            ["git", "show", f"{change}^:{relative}"], cwd=REPO_ROOT
        )
        prior = json.loads(prior_bytes)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        raise HarnessError("cannot resolve the frozen corpus v5 predecessor") from exc
    current_cases = {case["id"]: case for case in inputs.corpus["cases"]}
    prior_cases = {case["id"]: case for case in prior.get("cases", [])}
    shared_ids = set(current_cases) & set(prior_cases)
    rotated = {
        key: value
        for key, value in current_cases.get("WX00R", {}).items()
        if key not in {"id", "prompt"}
    }
    exposed = {
        key: value
        for key, value in prior_cases.get("WX00", {}).items()
        if key not in {"id", "prompt"}
    }
    valid = (
        len(current_cases) == len(prior_cases) == 40
        and set(current_cases) - set(prior_cases) == {"WX00R"}
        and set(prior_cases) - set(current_cases) == {"WX00"}
        and all(current_cases[case_id] == prior_cases[case_id] for case_id in shared_ids)
        and rotated == exposed
        and current_cases["WX00R"]["prompt"] != prior_cases["WX00"]["prompt"]
    )
    if not valid:
        raise HarnessError("corpus v6 is not the frozen WX00-to-WX00R rotation of corpus v5")
    return {
        "status": "PASS",
        "corpus_change_commit": change,
        "prior_corpus_id": prior.get("corpus_id"),
        "prior_sha256": hashlib.sha256(prior_bytes).hexdigest(),
        "current_corpus_id": inputs.corpus["corpus_id"],
        "current_sha256": _sha256(CORPUS_PATH),
        "unchanged_case_count": len(shared_ids),
        "retired_case_id": "WX00",
        "replacement_case_id": "WX00R",
        "semantic_fields_equal": True,
        "prompt_changed": True,
    }


def build_deterministic_evidence(inputs: FrozenInputs) -> dict[str, Any]:
    candidates: dict[str, Any] = {}
    with tempfile.TemporaryDirectory(prefix="t023-provenance-") as temporary:
        root = Path(temporary)
        for candidate_id in inputs.oracle["candidate_ids"]:
            destination = root / candidate_id
            destination.mkdir()
            materialization = materialize_candidate(inputs, candidate_id, destination)
            topology = inputs.topologies["candidates"][candidate_id]
            candidates[candidate_id] = {
                "materialization": materialization,
                "source_distribution_integrity": (
                    inputs.topologies["product_id"] == "agent-governance"
                    and inputs.topologies["distribution_identity"] == "single-product"
                    and not topology["portable_skill_to_skill_required"]
                ),
                "single_install_feasibility": (
                    not topology["portable_skill_to_skill_required"]
                    and all(
                        (destination / ".agents" / "skills" / entrypoint / "SKILL.md").is_file()
                        for entrypoint in topology["entrypoints"]
                    )
                ),
                "entrypoint_count": len(topology["entrypoints"]),
                "one_distribution_root": True,
                "manual_support_install_required": False,
            }
    return {
        "oracle_id": inputs.oracle["oracle_id"],
        "capability_source_epoch": inputs.oracle["capability_source_epoch"],
        "presentation_revision": inputs.oracle["presentation_revision"],
        "corpus_id": inputs.oracle["corpus_id"],
        "trial_envelope_id": inputs.oracle["trial_envelope_id"],
        "execution_epoch": inputs.oracle["execution_epoch"],
        "prior_acceptance_observations_imported": 0,
        "provider_model_calls_issued_during_deterministic_gate": 0,
        "holdout_rotation": _holdout_rotation_evidence(inputs),
        "frozen_asset_sha256": {
            path.relative_to(REPO_ROOT).as_posix(): _sha256(path)
            for path in (ORACLE_PATH, CORPUS_PATH, TOPOLOGIES_PATH, MANIFEST_PATH, ENVELOPE_PATH)
        },
        "full_deterministic_regression": "NOT_RUN",
        "profile_isolation_regression": "NOT_RUN",
        "consumer_source_independence_regression": "NOT_RUN",
        "candidates": candidates,
    }


def _validated_prior_attempts(output: Path, spec: TrialSpec) -> list[dict[str, Any]]:
    prior = [
        _load_json(path) for path in sorted((output / "attempts").glob(f"{spec.key}--a*.json"))
    ]
    if [item["attempt"] for item in prior] != list(range(1, len(prior) + 1)):
        raise HarnessError(f"{spec.key}: invalid persisted attempt sequence")
    valid = [item for item in prior if item["status"] == "VALID"]
    if len(valid) > 1 or (valid and valid[-1] is not prior[-1]):
        raise HarnessError(f"{spec.key}: retry after valid observation")
    return prior


def _new_attempt_record(
    inputs: FrozenInputs, spec: TrialSpec, output: Path, attempt: int
) -> tuple[Path, dict[str, Any]]:
    journal = output / "attempts" / f"{spec.key}--a{attempt}.json"
    if journal.exists():
        raise HarnessError(f"refusing to overwrite attempt journal: {journal.name}")
    return journal, {
        "trial_key": spec.key,
        "candidate_id": spec.candidate_id,
        "attempt": attempt,
        "execution_epoch": inputs.oracle["execution_epoch"],
        "status": "STARTED",
        "started_at": datetime.now(UTC).isoformat(),
    }


def execute_logical_observation(
    inputs: FrozenInputs, spec: TrialSpec, *, output: Path, **kwargs: Any
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    """Persist model attempts; explicit capacity events consume no attempt ordinal."""
    method = inputs.oracle["trial_method"]
    validate_repetition(inputs, spec)
    limit = method["max_model_attempts_per_scheduled_observation"]
    prior = _validated_prior_attempts(output, spec)
    valid = [item for item in prior if item["status"] == "VALID"]
    if valid:
        return valid[0]["structured"], valid[0]["raw"]
    for attempt in range(len(prior) + 1, limit + 1):
        journal, record = _new_attempt_record(inputs, spec, output, attempt)
        terminal_drift: HostSurfaceDrift | None = None
        try:
            structured, raw = run_trial(inputs, spec, attempt=attempt, **kwargs)
        except CapacityPause as exc:
            capacity_dir = output / "capacity-events"
            ordinal = len(list(capacity_dir.glob(f"{spec.key}--c*.json"))) + 1
            _json_dump(
                capacity_dir / f"{spec.key}--c{ordinal}.json",
                {
                    "trial_key": spec.key,
                    "candidate_id": spec.candidate_id,
                    "pending_attempt": attempt,
                    "execution_epoch": inputs.oracle["execution_epoch"],
                    "status": "EXTERNAL_CAPACITY",
                    "recorded_at": datetime.now(UTC).isoformat(),
                    "raw": exc.raw,
                },
            )
            raise
        except AttemptFailure as exc:
            record.update(
                status="FAILED", failure_class=exc.failure_class, error=str(exc), raw=exc.raw
            )
            if exc.failure_class == "HOST_SURFACE_DRIFT":
                terminal_drift = HostSurfaceDrift(str(exc), exc.raw)
        except HarnessError as exc:
            # Setup failed before the model invocation; there is no observation to score.
            record.update(status="FAILED", failure_class="ATTEMPT_SETUP_ERROR", error=str(exc))
        else:
            record.update(status="VALID", structured=structured, raw=raw)
        record["completed_at"] = datetime.now(UTC).isoformat()
        _json_dump(journal, record)
        if terminal_drift is not None:
            raise terminal_drift
        if record["status"] == "VALID":
            return structured, raw
        print(f"failed attempt {attempt}/{limit} {spec.key}: {record['failure_class']}", flush=True)
    return None


def _validate_resumed_command(spec: TrialSpec, command: Any, model: str, effort: str) -> list[str]:
    if not isinstance(command, list):
        raise HarnessError(f"{spec.key}: resumed command evidence is malformed")
    try:
        recorded_model = command[command.index("--model") + 1]
    except (ValueError, IndexError) as exc:
        raise HarnessError(f"{spec.key}: resumed model evidence is missing") from exc
    if recorded_model != model or f'model_reasoning_effort="{effort}"' not in command:
        raise HarnessError(f"{spec.key}: resumed model/effort differs from this run")
    if "--sandbox" not in command or command[command.index("--sandbox") + 1] not in {
        "read-only",
        "workspace-write",
    }:
        raise HarnessError(f"{spec.key}: resumed execution used an invalid frozen sandbox")
    if not any(
        command[index : index + 2] == ["--config", f'windows.sandbox="{backend}"']
        for index in range(len(command) - 1)
        for backend in WINDOWS_BACKEND_ORDER
    ):
        raise HarnessError(f"{spec.key}: resumed execution lacked an explicit Windows backend")
    if "--ignore-user-config" not in command or "--ignore-rules" not in command:
        raise HarnessError(f"{spec.key}: resumed execution did not isolate host configuration")
    for feature in MINIMAL_DISABLED_FEATURES:
        if not any(
            command[index : index + 2] == ["--disable", feature]
            for index in range(len(command) - 1)
        ):
            raise HarnessError(f"{spec.key}: resumed execution enabled forbidden host surface")
    if "--ephemeral" not in command:
        raise HarnessError(f"{spec.key}: resumed execution was not ephemeral")
    return command


def _validate_resumed_isolation(
    inputs: FrozenInputs, spec: TrialSpec, isolation: dict[str, Any], workspace: Path
) -> None:
    canonical = REPO_ROOT.resolve(strict=True)
    root_folded = str(workspace).casefold()
    invalid = (
        isolation.get("outside_canonical_repository") is not True
        or isolation.get("forbidden_root_substring_matches") != []
        or isolation.get("canonical_git_metadata_present") is not False
        or isolation.get("linked_components") != []
        or isolation.get("initially_empty") is not True
        or isolation.get("absolute_root") != str(workspace)
        or _is_relative_to(workspace, canonical)
        or any(
            term in root_folded
            for term in inputs.envelope["workspace_root_policy"][
                "forbidden_root_substrings_casefold"
            ]
        )
    )
    if invalid:
        raise HarnessError(f"{spec.key}: resumed workspace isolation evidence mismatch")


def _validate_resumed_workspace(
    spec: TrialSpec, workspace_evidence: dict[str, Any], workspace: Path
) -> None:
    invalid = (
        workspace_evidence.get("absolute_workspace_root") != str(workspace)
        or workspace_evidence.get("workspace_creation_method") != WORKSPACE_FACTORY_ID
        or workspace_evidence.get("workspace_acl_profile_identity") != WORKSPACE_FACTORY_ID
        or workspace_evidence.get("private_temp_creation_avoided") is not True
        or workspace_evidence.get("cleanup_result") != "REMOVED"
    )
    if invalid:
        raise HarnessError(f"{spec.key}: resumed v12 workspace factory evidence mismatch")


def _validate_partial(
    inputs: FrozenInputs,
    spec: TrialSpec,
    structured: dict[str, Any],
    raw: dict[str, Any],
    *,
    model: str,
    effort: str,
) -> None:
    identity = (
        structured.get("case_id"),
        structured.get("candidate_id"),
        structured.get("repetition"),
    )
    if identity != (spec.case["id"], spec.candidate_id, spec.repetition):
        raise HarnessError(f"{spec.key}: resumed structured trial identity mismatch")
    if raw.get("trial_key") != spec.key:
        raise HarnessError(f"{spec.key}: resumed raw trial identity mismatch")
    materialization = raw.get("materialization", {})
    if (
        materialization.get("candidate_id") != spec.candidate_id
        or materialization.get("presentation_revision") != inputs.oracle["presentation_revision"]
        or materialization.get("capability_source_epoch")
        != inputs.oracle["capability_source_epoch"]
    ):
        raise HarnessError(f"{spec.key}: resumed materialization identity mismatch")
    command = _validate_resumed_command(spec, raw.get("command"), model, effort)
    fixture = raw.get("fixture_materialization", {})
    _validate_fixture_evidence(inputs, spec.case, fixture)
    isolation = raw.get("workspace_isolation", {})
    workspace = Path(command[command.index("--cd") + 1])
    _validate_resumed_isolation(inputs, spec, isolation, workspace)
    _validate_resumed_workspace(spec, raw.get("workspace", {}), workspace)
