"""Frozen-input loading and fail-closed validation for the T023 v15 epoch."""

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
    V15_CLASS_ORDER,
    FrozenInputs,
    HarnessError,
)

EXPECTED_CANDIDATES = ["B2", "F2", "G3"]
EXPECTED_EPOCH = "MG1-2026-09-06-v4"
EXPECTED_PRESENTATION = "MG1-T023-PRESENTATIONS-v5"
EXPECTED_TOPOLOGY = "MG1-T023-TOPOLOGIES-v4"


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HarnessError(f"cannot load {path.relative_to(REPO_ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise HarnessError(f"{path.relative_to(REPO_ROOT)} must contain a JSON object")
    return value


def _validate_oracle_method(oracle: dict[str, Any]) -> None:
    if (
        oracle.get("schema_version") != "15.0.0"
        or oracle.get("oracle_id") != "MG1-T023-TOPOLOGY-ORACLE-v15"
        or oracle.get("execution_epoch") != "MG1-T023-EXECUTION-v15"
        or oracle.get("strategy") != "RIQ-NBC"
    ):
        raise HarnessError("harness requires the frozen MG1 v15 RIQ-NBC oracle")
    if oracle.get("candidate_ids") != EXPECTED_CANDIDATES:
        raise HarnessError("oracle candidate order must be B2/F2/G3")
    method = oracle.get("trial_method", {})
    required = {
        "base_valid_repetitions_per_case_candidate": 2,
        "max_valid_repetitions_per_case_candidate": 3,
        "per_candidate_base_valid_observations": 140,
        "per_candidate_max_valid_observations": 210,
        "global_base_valid_observations": 420,
        "global_max_valid_observations": 630,
        "max_model_attempts_per_scheduled_observation": 2,
        "maximum_acceptance_model_attempts": 1260,
        "synthetic_canary_max_model_attempts": 4,
        "absolute_stage6_provider_model_attempt_ceiling": 1264,
        "timeout_seconds_per_model_attempt": 180,
    }
    if any(method.get(key) != value for key, value in required.items()):
        raise HarnessError("oracle v15 repetition or budget method is not frozen")
    schedule = oracle.get("scheduling", {})
    if (
        schedule.get("case_group_order") != list(V15_CLASS_ORDER)
        or schedule.get("base_repetition_order") != ["r1", "r2"]
        or schedule.get("candidate_round_robin_order") != EXPECTED_CANDIDATES
        or schedule.get("reference_scientific_qualification_gates_challengers") is not False
        or schedule.get("b2_scientific_nonqualification_is_nonblocking") is not True
        or schedule.get("r4_allowed") is not False
    ):
        raise HarnessError("oracle v15 independent scheduler contract is incomplete")


def _validate_envelope(oracle: dict[str, Any], envelope: dict[str, Any]) -> None:
    if (
        envelope.get("schema_version") != "3.0.0"
        or envelope.get("envelope_id") != "MG1-T023-TRIAL-ENVELOPE-v3"
        or envelope.get("envelope_id") != oracle.get("trial_envelope_id")
        or oracle.get("trial_envelope_path") != ENVELOPE_PATH.relative_to(REPO_ROOT).as_posix()
        or envelope.get("user_suffix") != "Return only the required structured record."
    ):
        raise HarnessError("oracle/trial-envelope v15 identity mismatch")
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


def _validate_document_identities(inputs: FrozenInputs) -> None:
    oracle = inputs.oracle
    if oracle.get("corpus_id") != inputs.corpus.get("corpus_id"):
        raise HarnessError("oracle/corpus identity mismatch")
    if oracle.get("capability_source_epoch") != EXPECTED_EPOCH:
        raise HarnessError("oracle capability-source epoch mismatch")
    if oracle.get("presentation_revision") != EXPECTED_PRESENTATION:
        raise HarnessError("oracle presentation revision mismatch")
    if oracle.get("topology_revision") != EXPECTED_TOPOLOGY:
        raise HarnessError("oracle topology revision mismatch")
    for name, document in (("topologies", inputs.topologies), ("manifest", inputs.manifest)):
        if document.get("capability_source_epoch") != EXPECTED_EPOCH:
            raise HarnessError(f"{name} capability-source epoch mismatch")
        if document.get("presentation_revision") != EXPECTED_PRESENTATION:
            raise HarnessError(f"{name} presentation revision mismatch")
        if set(document.get("candidates", {})) != set(EXPECTED_CANDIDATES):
            raise HarnessError(f"{name} candidate identities do not match v15")
    if inputs.topologies.get("topology_revision") != EXPECTED_TOPOLOGY:
        raise HarnessError("topology revision mismatch")


def _validate_cases(inputs: FrozenInputs, known_capabilities: set[str]) -> None:
    cases = inputs.corpus.get("cases")
    if (
        inputs.corpus.get("schema_version") != "9.0.0"
        or inputs.corpus.get("corpus_id") != "MG1-T023-CORPUS-v9"
        or not isinstance(cases, list)
        or len(cases) != 70
    ):
        raise HarnessError("harness requires the frozen 70-case MG1 v15 corpus")
    ids = [case.get("id") for case in cases if isinstance(case, dict)]
    prompts = [case.get("prompt") for case in cases if isinstance(case, dict)]
    if len(ids) != 70 or len(ids) != len(set(ids)) or len(prompts) != len(set(prompts)):
        raise HarnessError("corpus case ids and prompts must be unique")
    fixtures = inputs.envelope.get("fixtures", {})
    if set(fixtures) != {"neutral", "source", "consumer"}:
        raise HarnessError("trial-envelope fixture roles are not the frozen v15 set")
    for case in cases:
        if case.get("class") not in V15_CLASS_ORDER:
            raise HarnessError(f"{case.get('id')}: unknown case class")
        if set(case.get("expected_capabilities", [])) - known_capabilities:
            raise HarnessError(f"{case['id']}: unknown expected capability")
        if set(case.get("forbidden_capabilities", [])) - known_capabilities:
            raise HarnessError(f"{case['id']}: unknown forbidden capability")
        if case.get("expected_semantic_outcome") not in ALLOWED_OUTCOMES:
            raise HarnessError(f"{case['id']}: invalid semantic outcome")
        fixture_role = case.get("fixture_role")
        if fixture_role not in fixtures:
            raise HarnessError(f"{case['id']}: invalid fixture role")
        if case.get("class") in {"ambiguous", "negative", "near-miss"} and fixture_role != "neutral":
            raise HarnessError(f"{case['id']}: class requires a neutral fixture")


def _validate_presentations(inputs: FrozenInputs, known_capabilities: set[str]) -> None:
    for candidate_id in EXPECTED_CANDIDATES:
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
        if not (REPO_ROOT / relative).is_file():
            raise HarnessError(f"missing frozen shared reference: {relative}")


def validate_frozen_inputs(inputs: FrozenInputs) -> None:
    _validate_oracle_method(inputs.oracle)
    _validate_envelope(inputs.oracle, inputs.envelope)
    _validate_document_identities(inputs)
    known_capabilities = set(inputs.manifest.get("shared_references", {}))
    _validate_cases(inputs, known_capabilities)
    _validate_presentations(inputs, known_capabilities)


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
