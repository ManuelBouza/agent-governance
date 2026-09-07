"""Load and validate the frozen MG1/T023 v14 semantic inputs."""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from .models import (
    ALLOWED_OUTCOMES,
    CANDIDATE_HASHES_PATH,
    CORPUS_PATH,
    ENVELOPE_PATH,
    MANIFEST_PATH,
    ORACLE_PATH,
    REPO_ROOT,
    TOPOLOGIES_PATH,
    FrozenInputs,
    HarnessError,
)

EXPECTED_CANDIDATES = ["B2", "F2", "G3"]
EXPECTED_CLASS_COUNTS = {
    "positive-consumer": 6,
    "positive-source-maintainer": 6,
    "positive-external-skill-trust": 6,
    "negative": 10,
    "near-miss": 30,
    "ambiguous": 4,
    "cross-profile": 4,
    "multi-intent": 4,
}
EXPECTED_NEAR_MISS_AXES = {
    "unrelated-source-maintenance": 6,
    "generic-skill-tooling": 6,
    "explicit-non-applicability": 6,
    "incidental-mention": 6,
    "homonym-outside-product": 6,
}
EXPECTED_HISTORICAL_CORPORA = {
    "MG1-v13": "d0ebe46a68c02c66dcfbb21c3dfaee43fb15c27f",
    "MG1-v12": "3e5bec392d0b8e5804c4efaad74b795b08dc9779",
}


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HarnessError(f"cannot load {path.relative_to(REPO_ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise HarnessError(f"{path.relative_to(REPO_ROOT)} must contain a JSON object")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_bytes(revision: str, relative: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", "show", f"{revision}:{relative}"],
            cwd=REPO_ROOT,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as exc:
        raise HarnessError(f"cannot resolve Git object {revision}:{relative}") from exc


def _validate_oracle_method(oracle: dict[str, Any]) -> None:
    if (
        oracle.get("schema_version") != "14.0.0"
        or oracle.get("oracle_id") != "MG1-T023-TOPOLOGY-ORACLE-v14"
        or oracle.get("execution_epoch") != "MG1-T023-EXECUTION-v14"
    ):
        raise HarnessError("harness requires the frozen MG1 v14 oracle")
    method = oracle.get("trial_method", {})
    if (
        method.get("reference_stage_candidates") != ["B2"]
        or method.get("challenger_stage_candidates") != ["F2", "G3"]
        or method.get("base_valid_repetitions_per_case_candidate") != 2
        or method.get("max_valid_repetitions_per_case_candidate") != 3
        or method.get("max_model_attempts_per_scheduled_observation") != 2
        or method.get("timeout_seconds_per_model_attempt") != 180
        or method.get("reference_stage_full_completion_base_valid_observations") != 140
        or method.get("reference_stage_full_completion_max_valid_observations") != 210
        or method.get("challenger_stage_full_completion_base_valid_observations") != 280
        or method.get("challenger_stage_full_completion_max_valid_observations") != 420
        or method.get("overall_full_completion_ceiling_when_challengers_execute") != 630
    ):
        raise HarnessError("oracle v14 trial/scheduling method is not the frozen T061 method")
    workspace_acl = oracle.get("windows_workspace_acl", {})
    if (
        workspace_acl.get("required_before_synthetic_model_calls") is not True
        or workspace_acl.get("python_private_temp_root_forbidden") is not True
        or workspace_acl.get("workspace_probe_provider_model_call_allowed") is not False
    ):
        raise HarnessError("oracle v14 Windows workspace gate is incomplete")


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
    candidates = inputs.oracle.get("candidate_ids")
    if candidates != EXPECTED_CANDIDATES:
        raise HarnessError("oracle candidate order/identity is not the frozen v14 set")
    for name, document in (("topologies", inputs.topologies), ("manifest", inputs.manifest)):
        if list(document.get("candidates", {})) != EXPECTED_CANDIDATES:
            raise HarnessError(f"{name} candidate identities/order do not match oracle v14")
    return candidates


def _validate_document_identities(inputs: FrozenInputs) -> None:
    if inputs.oracle.get("corpus_id") != inputs.corpus.get("corpus_id"):
        raise HarnessError("oracle/corpus identity mismatch")
    if inputs.oracle.get("candidate_freeze_sha") != inputs.corpus.get("candidate_freeze_sha"):
        raise HarnessError("oracle/corpus Freeze C identity mismatch")
    if inputs.oracle.get("topology_revision") != inputs.topologies.get("topology_revision"):
        raise HarnessError("oracle/topologies revision mismatch")
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
        inputs.corpus.get("schema_version") != "8.0.0"
        or inputs.corpus.get("corpus_id") != "MG1-T023-CORPUS-v8"
        or not isinstance(cases, list)
        or len(cases) != 70
    ):
        raise HarnessError("harness requires the frozen 70-case MG1 v14 corpus")
    ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if len(ids) != len(cases) or len(ids) != len(set(ids)):
        raise HarnessError("corpus case identities must be unique objects")
    if Counter(case.get("class") for case in cases) != Counter(EXPECTED_CLASS_COUNTS):
        raise HarnessError("corpus v8 class counts differ from the frozen T061 design")
    near_miss_axes = Counter(
        case.get("near_miss_axis") for case in cases if case.get("class") == "near-miss"
    )
    if near_miss_axes != Counter(EXPECTED_NEAR_MISS_AXES):
        raise HarnessError("corpus v8 near-miss axes are not exactly six-per-axis")
    contrast_axes: set[str] = set()
    for case in cases:
        if str(case.get("class", "")).startswith("positive-"):
            contrast_axes.update(case.get("contrast_axes", []))
    if contrast_axes != set(EXPECTED_NEAR_MISS_AXES):
        raise HarnessError("positive cases do not contrast every frozen near-miss axis")
    fixtures = inputs.envelope.get("fixtures", {})
    if set(fixtures) != {"neutral", "source", "consumer"}:
        raise HarnessError("trial-envelope fixture roles are not the frozen set")
    for case in cases:
        if set(case.get("expected_capabilities", [])) - known_capabilities:
            raise HarnessError(f"{case['id']}: unknown expected capability")
        if set(case.get("forbidden_capabilities", [])) - known_capabilities:
            raise HarnessError(f"{case['id']}: unknown forbidden capability")
        if case.get("expected_semantic_outcome") not in ALLOWED_OUTCOMES:
            raise HarnessError(f"{case['id']}: invalid semantic outcome")
        role = case.get("fixture_role")
        if role not in fixtures:
            raise HarnessError(f"{case['id']}: invalid fixture role")
        if case.get("class") in {"ambiguous", "negative", "near-miss"} and role != "neutral":
            raise HarnessError(f"{case['id']}: class requires a neutral fixture")
    if sum(case["class"] in {"negative", "near-miss"} for case in cases) != 40:
        raise HarnessError("corpus v8 false-activation denominator must be exactly 40")


def _validate_presentations(
    inputs: FrozenInputs, candidates: list[str], known_capabilities: set[str]
) -> None:
    for candidate_id in candidates:
        topology = inputs.topologies["candidates"][candidate_id]
        presentation = inputs.manifest["candidates"][candidate_id]
        if list(presentation.get("entrypoints", {})) != topology.get("entrypoints"):
            raise HarnessError(f"{candidate_id}: topology/manifest entrypoint mismatch")
        for entrypoint, data in presentation["entrypoints"].items():
            source = REPO_ROOT / data["skill_source"]
            if not source.is_file() or source.name != "SKILL.md":
                raise HarnessError(f"{candidate_id}/{entrypoint}: missing frozen SKILL.md")
            if set(data.get("capabilities", [])) - known_capabilities:
                raise HarnessError(f"{candidate_id}/{entrypoint}: unknown capability")
        for capability in presentation.get("load_order", []):
            if capability not in known_capabilities:
                raise HarnessError(f"{candidate_id}: invalid load-order capability")
    for relative in inputs.manifest["shared_references"].values():
        if not (REPO_ROOT / relative).is_file():
            raise HarnessError(f"missing frozen shared reference: {relative}")


def _validate_candidate_hashes(inputs: FrozenInputs) -> None:
    manifest = _load_json(CANDIDATE_HASHES_PATH)
    if (
        manifest.get("schema_version") != "1.0.0"
        or manifest.get("identity") != "MG1-T061-CANDIDATE-HASHES-v2"
        or manifest.get("topology_revision") != inputs.oracle["topology_revision"]
        or manifest.get("presentation_revision") != inputs.oracle["presentation_revision"]
        or manifest.get("capability_source_epoch") != inputs.oracle["capability_source_epoch"]
    ):
        raise HarnessError("candidate hash manifest identity mismatch")
    freeze = inputs.oracle["candidate_freeze_sha"]
    try:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", freeze, "HEAD"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:
        raise HarnessError("Freeze C is not an ancestor of the executing v14 branch") from exc
    for relative, expected in manifest.get("files", {}).items():
        path = REPO_ROOT / relative
        if _sha256(path) != expected:
            raise HarnessError(f"candidate/reference hash changed after Freeze C: {relative}")
        frozen_bytes = _git_bytes(freeze, relative)
        if hashlib.sha256(frozen_bytes).hexdigest() != expected or path.read_bytes() != frozen_bytes:
            raise HarnessError(f"candidate/reference bytes differ from Freeze C: {relative}")
    for current, historical in manifest.get("copy_equivalence", {}).items():
        if (REPO_ROOT / current).read_bytes() != (REPO_ROOT / historical).read_bytes():
            raise HarnessError(f"v5 challenger/reference copy differs from v3 source: {current}")


def _validate_holdout_freshness(inputs: FrozenInputs) -> None:
    current_prompts = [case["prompt"] for case in inputs.corpus["cases"]]
    if len(current_prompts) != len(set(current_prompts)):
        raise HarnessError("corpus v8 prompts must be unique")
    exclusions = inputs.corpus.get("historical_prompt_exclusion")
    if not isinstance(exclusions, list) or len(exclusions) != 2:
        raise HarnessError("corpus v8 historical prompt exclusion set is incomplete")
    observed: dict[str, str] = {}
    current = set(current_prompts)
    for item in exclusions:
        if not isinstance(item, dict):
            raise HarnessError("corpus v8 historical prompt exclusion entry is malformed")
        revision = item.get("revision")
        commit = item.get("commit")
        relative = item.get("path")
        if (
            revision not in EXPECTED_HISTORICAL_CORPORA
            or commit != EXPECTED_HISTORICAL_CORPORA[revision]
            or relative != CORPUS_PATH.relative_to(REPO_ROOT).as_posix()
        ):
            raise HarnessError("corpus v8 historical prompt exclusion identity mismatch")
        try:
            historical = json.loads(_git_bytes(commit, relative))
        except json.JSONDecodeError as exc:
            raise HarnessError(f"cannot decode historical corpus {revision}") from exc
        reused = sorted(current & {case.get("prompt") for case in historical.get("cases", [])})
        if reused:
            raise HarnessError(f"corpus v8 reuses exact {revision} acceptance prompts")
        observed[revision] = commit
    if observed != EXPECTED_HISTORICAL_CORPORA:
        raise HarnessError("corpus v8 historical prompt exclusions are incomplete")


def validate_frozen_inputs(inputs: FrozenInputs) -> None:
    _validate_oracle_method(inputs.oracle)
    _validate_envelope(inputs.oracle, inputs.envelope)
    candidates = _validate_candidate_identities(inputs)
    _validate_document_identities(inputs)
    known_capabilities = set(inputs.manifest.get("shared_references", {}))
    _validate_cases(inputs, known_capabilities)
    _validate_presentations(inputs, candidates, known_capabilities)
    _validate_candidate_hashes(inputs)
    _validate_holdout_freshness(inputs)


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
