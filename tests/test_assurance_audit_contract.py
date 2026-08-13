"""Deterministic D036 policy examples; Core Markdown remains authority."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest
from _helpers import ASSURANCE_ROUTE, protocol_version_from, required_core_modules_from

PROFILES = (
    "EVIDENCE_REVIEW",
    "AUTHENTICATED_OBSERVE",
    "SAFE_ACTIVE",
    "INTRUSIVE_AUTHORIZED",
)
FINDING_STATES = frozenset(
    {
        "PASS",
        "FAIL",
        "PARTIAL",
        "NOT_APPLICABLE",
        "NOT_ASSESSED",
        "INCONCLUSIVE",
        "ACCEPTED_EXCEPTION",
    }
)
GAP_STATES = frozenset({"NOT_ASSESSED", "INCONCLUSIVE", "BLOCKED"})
SCOPE_FIELDS = frozenset(
    {"subject", "environment", "resources", "methods", "maximum_profile", "exclusions"}
)


@pytest.fixture(scope="module")
def cases() -> dict[str, object]:
    path = Path(__file__).parent / "fixtures" / "assurance_audit" / "policy_cases.json"
    return json.loads(path.read_text(encoding="utf-8"))


def timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def scope_outcome(case: dict[str, object]) -> str:
    scope = case["scope"]
    requested = case["requested"]
    if scope.keys() < SCOPE_FIELDS or any(
        not scope[field] for field in SCOPE_FIELDS - {"exclusions"}
    ):
        return "BLOCKED"
    if not set(requested["resources"]) <= set(scope["resources"]):
        return "BLOCKED"
    if not set(requested["methods"]) <= set(scope["methods"]):
        return "BLOCKED"
    if PROFILES.index(requested["profile"]) > PROFILES.index(scope["maximum_profile"]):
        return "BLOCKED"
    return "READY"


def profile_allowed(case: dict[str, object]) -> bool:
    return PROFILES.index(case["requested"]) <= PROFILES.index(case["authorized"])


def finding_state(case: dict[str, object]) -> str:
    status = case["status"]
    if status not in FINDING_STATES:
        return "INCONCLUSIVE"
    if status in {"PASS", "FAIL", "PARTIAL"} and not all(
        case.get(field) for field in ("observed_state", "method", "evidence", "source")
    ):
        return "INCONCLUSIVE"
    if case.get("method") == "opinion":
        return "INCONCLUSIVE"
    if status == "ACCEPTED_EXCEPTION":
        exception = case.get("exception", {})
        if not (
            exception.get("human_approved") is True
            and timestamp(exception["evaluate_at"]) < timestamp(exception["expires_at"])
        ):
            return "FAIL"
    return status


def coverage_outcome(case: dict[str, object]) -> tuple[bool, str]:
    complete = not GAP_STATES.intersection(case["cells"])
    bounded = all(
        case.get(field) for field in ("scope", "methods", "source_versions", "assessed_at")
    )
    conclusion = "BOUNDED_NO_MATERIAL_FINDING" if complete and bounded else "GAPS_REMAIN"
    return complete, conclusion


def remediation_authorized(case: dict[str, object]) -> bool:
    return case["remediation_authorized"] is True


def temporal_posture(case: dict[str, object]) -> tuple[str, str]:
    posture = case["current_posture"]
    if case["signal"]["applicable"] is True:
        posture = case["signal"]["result"]
    return case["historical_report"], posture


def composed_outcome(case: dict[str, object]) -> tuple[str, str, bool]:
    method_authorized = case["execution"] in {"ALLOW_TASK", "ALLOW_EXPLICIT"}
    if case["profile"] == "INTRUSIVE_AUTHORIZED":
        method_authorized = case["execution"] == "ALLOW_EXPLICIT"
    return case["audit"], case["security"], method_authorized


def assurance_activation_state(assurance: Path) -> str | None:
    declarations = [
        line.split(":", 1)[1].strip()
        for line in assurance.read_text(encoding="utf-8").splitlines()
        if line.startswith("Activation-State:")
    ]
    if len(declarations) != 1 or declarations[0] not in {"STAGED", "ACTIVE"}:
        return None
    return declarations[0]


def assert_assurance_routing_state(governance: Path, assurance: Path) -> None:
    version = protocol_version_from(governance)
    state = assurance_activation_state(assurance)
    governance_text = governance.read_text(encoding="utf-8")
    required_modules = required_core_modules_from(governance)

    assert version is not None
    assert state is not None
    routed = ASSURANCE_ROUTE in governance_text
    required = "ASSURANCE.md" in required_modules
    if state == "STAGED":
        assert version == "1.12.0"
        assert routed is False
        assert required is False
    else:
        assert tuple(map(int, version.split("."))) >= (1, 13, 0)
        assert routed is True
        assert required is True


def test_scope_is_explicit_complete_and_cannot_expand_from_capability(
    cases: dict[str, object],
) -> None:
    for case in cases["scope_cases"]:
        assert scope_outcome(case) == case["expected"], case["id"]
    bounded = cases["scope_cases"][0]
    assert set(bounded["reachable_resources"]) > set(bounded["scope"]["resources"])
    assert set(bounded["tool_capabilities"]) > set(bounded["scope"]["methods"])
    assert scope_outcome(bounded) == "READY"


def test_profiles_are_monotonic_and_generic_audit_never_implies_intrusion(
    cases: dict[str, object],
) -> None:
    assert tuple(PROFILES) == tuple(dict.fromkeys(PROFILES))
    for case in cases["profile_cases"]:
        assert profile_allowed(case) is case["expected"], case["id"]
    generic = next(case for case in cases["profile_cases"] if case["generic_security_audit"])
    assert generic["capability_available"] is True
    assert profile_allowed(generic) is False


def test_evidence_graph_preserves_all_finding_states_and_fails_closed(
    cases: dict[str, object],
) -> None:
    for case in cases["finding_cases"]:
        assert finding_state(case) == case["expected"], case["id"]
    represented = {case["status"] for case in cases["finding_cases"]}
    assert represented == FINDING_STATES
    for case in cases["finding_cases"]:
        if case["expected"] in {"NOT_ASSESSED", "INCONCLUSIVE"}:
            assert finding_state(case) != "PASS"


def test_severity_and_confidence_remain_independent(cases: dict[str, object]) -> None:
    for case in cases["risk_cases"]:
        assert case["severity"] == case["expected_severity"]
        assert case["confidence"] == case["expected_confidence"]
    high_low = cases["risk_cases"][0]
    assert high_low["severity"] == "HIGH"
    assert high_low["confidence"] == "LOW"
    assert high_low["verification_needed"] is True


def test_coverage_exposes_gaps_and_only_allows_bounded_conclusions(
    cases: dict[str, object],
) -> None:
    for case in cases["coverage_cases"]:
        assert coverage_outcome(case) == (
            case["expected_complete"],
            case["expected_conclusion"],
        )
    assert coverage_outcome(cases["coverage_cases"][1])[1] != "SECURE"
    assert coverage_outcome(cases["coverage_cases"][2])[1] != "COMPLETE"
    assert "NOT_APPLICABLE" not in GAP_STATES


def test_findings_do_not_manufacture_remediation_authority(cases: dict[str, object]) -> None:
    for case in cases["remediation_cases"]:
        assert remediation_authorized(case) is case["expected"], case["id"]
    finding_only = cases["remediation_cases"][0]
    assert finding_only["finding"] == "FAIL"
    assert finding_only["capability_available"] is True
    assert finding_only["recommendation_present"] is True
    assert remediation_authorized(finding_only) is False


def test_temporal_signals_change_posture_without_rewriting_history(
    cases: dict[str, object],
) -> None:
    for case in cases["temporal_cases"]:
        assert temporal_posture(case) == (
            case["expected_historical"],
            case["expected_posture"],
        )
        assert timestamp(case["signal"]["observed_at"]).year == 2026


def test_security_execution_and_audit_planes_do_not_expand_each_other(
    cases: dict[str, object],
) -> None:
    for case in cases["composition_cases"]:
        assert composed_outcome(case) == (
            case["expected_audit"],
            case["expected_security"],
            case["expected_method_authorized"],
        )
    assert {case["id"] for case in cases["composition_cases"]} >= {
        "audit-pass-security-block",
        "security-pass-no-method-authority",
        "execution-cannot-create-pass",
        "intrusive-requires-explicit-execution",
        "exception-does-not-authorize",
    }


def test_assurance_routing_is_state_derived_with_single_protocol_authority(
    repo_root: Path, tmp_path: Path
) -> None:
    governance = repo_root / "governance-core" / "GOVERNANCE.md"
    assurance = repo_root / "governance-core" / "ASSURANCE.md"
    assurance_text = assurance.read_text(encoding="utf-8")
    assert "Assurance-Audit-Version: 1.0.0" in assurance_text
    assert_assurance_routing_state(governance, assurance)

    staged_governance = tmp_path / "staged-governance.md"
    staged_assurance = tmp_path / "staged-assurance.md"
    staged_governance.write_text("Protocol-Version: 1.12.0\n", encoding="utf-8")
    staged_assurance.write_text("Activation-State: STAGED\n", encoding="utf-8")
    assert_assurance_routing_state(staged_governance, staged_assurance)

    active_governance = tmp_path / "active-governance.md"
    active_assurance = tmp_path / "active-assurance.md"
    active_governance.write_text(
        f"Protocol-Version: 1.13.0\n- assurance -> `{ASSURANCE_ROUTE}`\n",
        encoding="utf-8",
    )
    active_assurance.write_text("Activation-State: ACTIVE\n", encoding="utf-8")
    assert_assurance_routing_state(active_governance, active_assurance)

    missing = tmp_path / "missing.md"
    malformed = tmp_path / "malformed.md"
    duplicate = tmp_path / "duplicate.md"
    missing.write_text("# Core\n", encoding="utf-8")
    malformed.write_text("Protocol-Version: next\n", encoding="utf-8")
    duplicate.write_text("Protocol-Version: 1.0.0\nProtocol-Version: 1.0.1\n", encoding="utf-8")
    assert protocol_version_from(missing) is None
    assert protocol_version_from(malformed) is None
    assert protocol_version_from(duplicate) is None


def test_fixture_and_evaluator_are_portable_and_execution_independent(
    cases: dict[str, object],
) -> None:
    combined = f"{Path(__file__).read_text(encoding='utf-8')}\n{json.dumps(cases)}"
    prohibited = (
        "Open" + "Code",
        "Co" + "dex",
        "Power" + "Shell",
        "PO" + "SIX",
        "http" + "://",
        "https" + "://",
        "sub" + "process",
        "sock" + "et",
        "req" + "uests",
        "boto" + "3",
    )
    for dependency in prohibited:
        assert dependency not in combined
