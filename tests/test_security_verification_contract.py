"""Deterministic D035 policy examples; Core Markdown remains authority."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest
from _helpers import CORE_REQUIRED_MODULES, protocol_version_from

CURRENT_SOURCE_STATES = frozenset({"CURRENT"})
BLOCKING_SOURCE_STATES = frozenset({"STALE", "UNKNOWN", "CONFLICT"})


@pytest.fixture(scope="module")
def cases() -> dict[str, object]:
    path = Path(__file__).parent / "fixtures" / "security_verification" / "policy_cases.json"
    return json.loads(path.read_text(encoding="utf-8"))


def timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def authority_state(sources: list[dict[str, object]]) -> str:
    controls = {
        source["control"]
        for source in sources
        if source["authoritative"] is True and source["applicable"] is True
    }
    if not controls:
        return "UNKNOWN"
    return "CURRENT" if len(controls) == 1 else "CONFLICT"


def freshness_state(case: dict[str, object]) -> str:
    if case.get("source_known", True) is False:
        return "UNKNOWN"
    if case.get("source_conflict", False) is True:
        return "CONFLICT"
    if case.get("superseded", False) is True:
        return "SUPERSEDED"
    freshness_class = case["class"]
    if freshness_class == "THREAT_LIVE":
        return (
            "CURRENT"
            if timestamp(case["evaluate_at"]) <= timestamp(case["recheck_by"])
            else "STALE"
        )
    if freshness_class == "PRODUCT_VERSION":
        return "CURRENT" if case["bound_context"] == case["evaluation_context"] else "STALE"
    if freshness_class == "STANDARD_PINNED":
        return "CURRENT" if case["selected_revision"] == case["active_revision"] else "STALE"
    if case.get("is_exception", False):
        return (
            "CURRENT" if timestamp(case["evaluate_at"]) < timestamp(case["expires_at"]) else "STALE"
        )
    return "CURRENT"


def known_bad_blocks(record: dict[str, object]) -> bool:
    return record["state"] == "ACTIVE" and record["applicable"] is True


def exception_valid(
    exception: dict[str, object],
    *,
    control: str,
    target: str,
    version: str,
    evaluate_at: str,
) -> bool:
    return (
        exception["human_approved"] is True
        and exception["control"] == control
        and exception["target"] == target
        and exception["version"] == version
        and exception["compensating_evidence_passes"] is True
        and timestamp(evaluate_at) < timestamp(exception["expires_at"])
    )


def security_outcome(case: dict[str, object]) -> str:
    controls = [control for control in case["controls"] if control["active"] is True]
    blocking_control = any(
        control["freshness"] in BLOCKING_SOURCE_STATES
        or control["actual_matches"] is not True
        or (control["evidence_required"] is True and control["evidence_passes"] is not True)
        for control in controls
    )
    blocking_known_bad = any(known_bad_blocks(record) for record in case["known_bad"])
    if not blocking_control and not blocking_known_bad:
        return "PASS"
    exception = case.get("exception")
    if exception and len(controls) == 1:
        control = controls[0]
        if exception_valid(
            exception,
            control=control["id"],
            target=case["target"],
            version=case["version"],
            evaluate_at=case["evaluate_at"],
        ):
            return "HUMAN_EXCEPTION"
    return "BLOCK"


def invalidate_posture(case: dict[str, object]) -> tuple[str, str]:
    posture = case["current_posture"]
    if case["signal"]["applicable"] is True:
        posture = case["signal"]["result"]
    return case["historical_acceptance"], posture


def compose_planes(case: dict[str, object]) -> tuple[str, str]:
    security = case["security"]
    if case["security_evidence_current"] is not True or case["target_context_matches"] is not True:
        security = "BLOCK"
    return security, case["execution"]


def test_explicit_authoritative_sources_resolve_without_model_authority(
    cases: dict[str, object],
) -> None:
    authority_cases = cases["authority_cases"]
    for case in authority_cases:
        assert authority_state(case["sources"]) == case["expected"], case["id"]
    compatible = authority_cases[0]
    assert {source["class"] for source in compatible["sources"]} == {
        "PROJECT",
        "PRODUCT_VENDOR",
        "THREAT_INTELLIGENCE",
        "VERSIONED_BASELINE",
    }
    model_only = next(case for case in authority_cases if case["id"] == "unsupported-model-only")
    assert authority_state(model_only["sources"]) == "UNKNOWN"


def test_freshness_is_class_aware_explicit_and_fail_closed(cases: dict[str, object]) -> None:
    freshness_cases = cases["freshness_cases"]
    for case in freshness_cases:
        assert freshness_state(case) == case["expected"], case["id"]
    assert {case["class"] for case in freshness_cases} == {
        "THREAT_LIVE",
        "PRODUCT_VERSION",
        "STANDARD_PINNED",
        "PROJECT_DECISION",
    }
    assert {case["expected"] for case in freshness_cases} >= {
        "CURRENT",
        "STALE",
        "UNKNOWN",
        "CONFLICT",
        "SUPERSEDED",
    }


def test_active_known_bad_blocks_despite_probabilistic_prior_metadata(
    cases: dict[str, object],
) -> None:
    known_bad_cases = cases["known_bad_cases"]
    for case in known_bad_cases:
        assert known_bad_blocks(case) is case["expected_block"], case["id"]
    active = next(
        case for case in known_bad_cases if case["id"] == "active-common-model-recommended"
    )
    assert active["model_recommends"] is True
    assert active["historically_common"] is True
    assert active["synthetic_prevalence"] == 99
    assert known_bad_blocks(active)


def test_security_acceptance_requires_current_independent_evidence(
    cases: dict[str, object],
) -> None:
    acceptance_cases = cases["acceptance_cases"]
    assert {case["expected"] for case in acceptance_cases} == {
        "PASS",
        "BLOCK",
        "HUMAN_EXCEPTION",
    }
    for case in acceptance_cases:
        assert security_outcome(case) == case["expected"], case["id"]
    asserted_secure = [
        case
        for case in acceptance_cases
        if case.get("model_claims_secure") or case.get("reviewer_claims_secure")
    ]
    assert asserted_secure
    assert all(security_outcome(case) == "BLOCK" for case in asserted_secure)


def test_human_exception_is_exact_scope_verified_non_transitive_and_unexpired(
    cases: dict[str, object],
) -> None:
    exception_cases = cases["exception_cases"]
    for case in exception_cases:
        valid = exception_valid(
            case["exception"],
            control=case["control"],
            target=case["target"],
            version=case["version"],
            evaluate_at=case["evaluate_at"],
        )
        assert valid is case["expected_valid"], case["id"]
    assert sum(case["expected_valid"] for case in exception_cases) == 1


def test_temporal_invalidation_preserves_historical_acceptance(
    cases: dict[str, object],
) -> None:
    invalidation_cases = cases["invalidation_cases"]
    for case in invalidation_cases:
        historical, posture = invalidate_posture(case)
        assert historical == case["expected_historical"] == "ACCEPTED"
        assert posture == case["expected_posture"]
    assert {case["signal"]["kind"] for case in invalidation_cases} >= {
        "ADVISORY",
        "VULNERABILITY",
        "DRIFT",
    }


def test_security_and_execution_control_planes_do_not_expand_each_other(
    cases: dict[str, object],
) -> None:
    composition_cases = cases["composition_cases"]
    for case in composition_cases:
        assert compose_planes(case) == (case["expected_security"], case["expected_execution"])
    assert {case["id"] for case in composition_cases} >= {
        "security-pass-execution-deny",
        "security-pass-human-gate",
        "security-block-execution-allow-task",
        "security-block-execution-allow-explicit",
        "exception-does-not-authorize",
        "adapter-success-no-security-evidence",
        "target-context-drift",
    }


def test_core_protocol_security_module_and_router_alignment(repo_root: Path) -> None:
    governance = repo_root / "governance-core" / "GOVERNANCE.md"
    security = repo_root / "governance-core" / "SECURITY.md"
    governance_text = governance.read_text(encoding="utf-8")
    security_text = security.read_text(encoding="utf-8")
    assert "SECURITY.md" in CORE_REQUIRED_MODULES
    assert protocol_version_from(governance) is not None
    assert ".agent-governance/SECURITY.md" in governance_text
    assert "add SECURITY" in governance_text
    assert security.is_file()
    assert "Security-Verification-Version: 1.0.0" in security_text


def test_fixture_and_evaluator_are_provider_platform_network_and_model_execution_neutral(
    cases: dict[str, object],
) -> None:
    module_text = Path(__file__).read_text(encoding="utf-8")
    fixture_text = json.dumps(cases)
    combined = f"{module_text}\n{fixture_text}"
    prohibited_dependencies = (
        "Open" + "Code",
        "Co" + "dex",
        "Power" + "Shell",
        "PO" + "SIX",
        "http" + "://",
        "https" + "://",
        "sub" + "process",
        "sock" + "et",
        "req" + "uests",
    )
    for prohibited_dependency in prohibited_dependencies:
        assert prohibited_dependency not in combined
