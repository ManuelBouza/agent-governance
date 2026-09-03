"""Extracted MG1 topology harness implementation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .models import (
    ALLOWED_OUTCOMES,
    CORPUS_PATH,
    ENVELOPE_PATH,
    MANIFEST_PATH,
    ORACLE_PATH,
    REPO_ROOT,
    TOPOLOGIES_PATH,
    FrozenInputs,
    HarnessError,
)


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HarnessError(f"cannot load {path.relative_to(REPO_ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise HarnessError(f"{path.relative_to(REPO_ROOT)} must contain a JSON object")
    return value


def _validate_oracle_method(oracle: dict[str, Any]) -> None:
    if oracle.get("schema_version") != "11.0.0" or oracle.get("oracle_id") != (
        "MG1-T023-TOPOLOGY-ORACLE-v11"
    ):
        raise HarnessError("harness requires the frozen MG1 V11 oracle")
    method = oracle.get("trial_method", {})
    if (
        method.get("base_valid_repetitions_per_case_candidate") != 2
        or method.get("max_valid_repetitions_per_case_candidate") != 3
        or method.get("max_model_attempts_per_scheduled_observation") != 2
        or method.get("timeout_seconds_per_model_attempt") != 180
    ):
        raise HarnessError("oracle paired repetition/attempt method is not frozen V11")
    workspace_acl = oracle.get("windows_workspace_acl", {})
    if (
        workspace_acl.get("required_before_synthetic_model_calls") is not True
        or workspace_acl.get("python_private_temp_root_forbidden") is not True
        or workspace_acl.get("workspace_probe_provider_model_call_allowed") is not False
    ):
        raise HarnessError("oracle v11 Windows workspace gate is incomplete")


def _validate_envelope(oracle: dict[str, Any], envelope: dict[str, Any]) -> None:
    if (
        envelope.get("schema_version") != "1.0.0"
        or envelope.get("envelope_id") != oracle.get("trial_envelope_id")
        or oracle.get("trial_envelope_path") != ENVELOPE_PATH.relative_to(REPO_ROOT).as_posix()
        or envelope.get("user_suffix") != "Return only the required structured record."
    ):
        raise HarnessError("oracle/trial-envelope identity or neutral suffix mismatch")
    if any(
        term in envelope["user_suffix"].casefold()
        for term in envelope.get("forbidden_added_terms_casefold", [])
    ):
        raise HarnessError("trial-envelope neutral suffix contains a forbidden added term")
    boundary = envelope.get("execution_boundary", {})
    if not all(
        boundary.get(field) is True
        for field in (
            "read_only_enforced_out_of_band",
            "no_domain_bearing_safety_wrapper",
            "output_schema_must_be_domain_neutral",
            "model_self_report_is_not_activation_authority",
        )
    ):
        raise HarnessError("trial-envelope execution boundary is incomplete")


def _validate_candidate_identities(inputs: FrozenInputs) -> list[str]:
    oracle = inputs.oracle
    candidates = oracle.get("candidate_ids")
    if candidates != ["B0", "B1", "F2", "G3"]:
        raise HarnessError("oracle candidate order/identity is not the frozen MG1 set")
    for name, document in (("topologies", inputs.topologies), ("manifest", inputs.manifest)):
        if set(document.get("candidates", {})) != set(candidates):
            raise HarnessError(f"{name} candidate identities do not match the oracle")
    return candidates


def _validate_document_identities(inputs: FrozenInputs) -> None:
    if inputs.oracle.get("corpus_id") != inputs.corpus.get("corpus_id"):
        raise HarnessError("oracle/corpus identity mismatch")
    for document_name, document in (
        ("topologies", inputs.topologies),
        ("manifest", inputs.manifest),
    ):
        if document.get("capability_source_epoch") != inputs.oracle.get("capability_source_epoch"):
            raise HarnessError(f"oracle/{document_name} capability-source epoch mismatch")
        if document.get("presentation_revision") != inputs.oracle.get("presentation_revision"):
            raise HarnessError(f"oracle/{document_name} presentation revision mismatch")


def _validate_cases(inputs: FrozenInputs, known_capabilities: set[str]) -> None:
    cases = inputs.corpus.get("cases")
    if (
        inputs.corpus.get("schema_version") != "5.0.0"
        or not isinstance(cases, list)
        or len(cases) != 40
    ):
        raise HarnessError("harness requires the frozen 40-case MG1 V11 corpus")
    ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if len(ids) != len(cases) or len(ids) != len(set(ids)):
        raise HarnessError("corpus case identities must be unique objects")
    fixtures = inputs.envelope.get("fixtures", {})
    if set(fixtures) != {"neutral", "source", "consumer"}:
        raise HarnessError("trial-envelope fixture roles are not the frozen V11 set")
    for case in cases:
        if set(case.get("expected_capabilities", [])) - known_capabilities:
            raise HarnessError(f"{case['id']}: unknown expected capability")
        if set(case.get("forbidden_capabilities", [])) - known_capabilities:
            raise HarnessError(f"{case['id']}: unknown forbidden capability")
        if case.get("expected_semantic_outcome") not in ALLOWED_OUTCOMES:
            raise HarnessError(f"{case['id']}: invalid semantic outcome")
        fixture_role = case.get("fixture_role")
        if fixture_role not in fixtures:
            raise HarnessError(f"{case['id']}: invalid fixture role")
        if case.get("class") in {"ambiguous", "negative", "near-miss"} and fixture_role != (
            "neutral"
        ):
            raise HarnessError(f"{case['id']}: class requires a neutral fixture")


def _validate_presentations(
    inputs: FrozenInputs, candidates: list[str], known_capabilities: set[str]
) -> None:
    for candidate_id in candidates:
        topology = inputs.topologies["candidates"][candidate_id]
        presentation = inputs.manifest["candidates"][candidate_id]
        if list(presentation.get("entrypoints", {})) != topology.get("entrypoints"):
            raise HarnessError(f"{candidate_id}: topology/manifest entrypoint mismatch")
        for entrypoint, entrypoint_data in presentation["entrypoints"].items():
            source = REPO_ROOT / entrypoint_data["skill_source"]
            if not source.is_file() or source.name != "SKILL.md":
                raise HarnessError(f"{candidate_id}/{entrypoint}: missing frozen SKILL.md")
            if set(entrypoint_data.get("capabilities", [])) - known_capabilities:
                raise HarnessError(f"{candidate_id}/{entrypoint}: unknown capability")
        for capability in presentation.get("load_order", []):
            if capability not in known_capabilities:
                raise HarnessError(f"{candidate_id}: invalid load-order capability")

    for relative in inputs.manifest["shared_references"].values():
        path = REPO_ROOT / relative
        if not path.is_file():
            raise HarnessError(f"missing frozen shared reference: {relative}")


def validate_frozen_inputs(inputs: FrozenInputs) -> None:
    _validate_oracle_method(inputs.oracle)
    _validate_envelope(inputs.oracle, inputs.envelope)
    candidates = _validate_candidate_identities(inputs)
    _validate_document_identities(inputs)
    known_capabilities = set(inputs.manifest.get("shared_references", {}))
    _validate_cases(inputs, known_capabilities)
    _validate_presentations(inputs, candidates, known_capabilities)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_frozen_inputs() -> FrozenInputs:
    inputs = FrozenInputs(
        oracle=_load_json(ORACLE_PATH),
        corpus=_load_json(CORPUS_PATH),
        topologies=_load_json(TOPOLOGIES_PATH),
        manifest=_load_json(MANIFEST_PATH),
        envelope=_load_json(ENVELOPE_PATH),
    )
    validate_frozen_inputs(inputs)
    return inputs
