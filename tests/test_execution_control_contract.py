"""Deterministic D033/D034 policy examples; Core Markdown remains authority."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from _helpers import CORE_REQUIRED_MODULES, SOURCE_PROTOCOL_VERSION, protocol_version_from

OUTCOME_RANK = {"ALLOW_TASK": 0, "ALLOW_EXPLICIT": 1, "REQUIRE_HUMAN": 2, "DENY": 3}
DENY_VIOLATIONS = frozenset(
    {
        "target_unknown",
        "target_mismatch",
        "identity_verification_bypass",
        "credential_exfiltration",
        "security_control_bypass",
    }
)
RUNBOOK_TRAITS = frozenset(
    {
        "production_mutation",
        "privileged",
        "remote_persistent",
        "security_control",
        "credential_lifecycle",
        "persistent_migration",
        "destructive",
        "multi_system_sequence",
        "recovery",
        "recurring_failure_modes",
    }
)
ENVELOPE_EXACT_FIELDS = ("actor", "target", "credential", "network", "context")
EVIDENCE_FIELDS = frozenset(
    {
        "task_authorization",
        "target",
        "runbook",
        "adapter",
        "checkpoints",
        "postconditions",
        "recovery",
    }
)


@pytest.fixture(scope="module")
def cases() -> dict[str, object]:
    path = Path(__file__).parent / "fixtures" / "execution_control" / "policy_cases.json"
    return json.loads(path.read_text(encoding="utf-8"))


def authorization_outcome(case: dict[str, object]) -> str:
    """Evaluate normalized facts only; no command text participates."""

    if DENY_VIOLATIONS.intersection(case.get("violations", [])):
        return "DENY"
    return max(case["effect_outcomes"], key=OUTCOME_RANK.__getitem__)


def envelope_valid(approved: dict[str, object], requested: dict[str, object]) -> bool:
    if not requested.get("target"):
        return False
    if any(requested.get(field) != approved.get(field) for field in ENVELOPE_EXACT_FIELDS):
        return False
    if int(requested["privilege"]) > int(approved["privilege"]):
        return False
    return set(requested["effects"]) <= set(approved["effects"]) and set(
        requested["resources"]
    ) <= set(approved["resources"])


def authority_is_subset(parent: list[str], child: list[str]) -> bool:
    return set(child) <= set(parent)


def runbook_required(traits: list[str]) -> bool:
    return bool(RUNBOOK_TRAITS.intersection(traits))


def invocation_executable(runbook: dict[str, object], invocation: dict[str, object]) -> bool:
    return (
        runbook["procedurally_valid"] is True
        and invocation["target_valid"] is True
        and invocation["authorization"] in {"ALLOW_TASK", "ALLOW_EXPLICIT"}
    )


def valid_lifecycle(states: list[str]) -> bool:
    normal_prefix = ["SELECT", "BIND_INPUTS", "PREFLIGHT"]
    if states[:3] != normal_prefix:
        return False
    if states == [*normal_prefix, "BLOCKED"]:
        return True
    if states == [*normal_prefix, "AUTHORIZE", "BLOCKED"]:
        return True
    expected = ["AUTHORIZE", "READY"]
    if states[3:5] != expected:
        return False
    if states == [*normal_prefix, *expected, "STALE"]:
        return True
    if states[-4:] in (
        ["VERIFY_CHECKPOINT", "STOP", "RECOVER", "BLOCKED"],
        ["VERIFY_CHECKPOINT", "STOP", "ROLLBACK", "BLOCKED"],
    ):
        attempted_steps = states[5:-4]
        return not attempted_steps or attempted_steps == ["EXECUTE_STEP"]
    body = states[5:-2]
    if (
        not body
        or len(body) % 2
        or any(
            pair != ["EXECUTE_STEP", "VERIFY_CHECKPOINT"]
            for pair in (body[index : index + 2] for index in range(0, len(body), 2))
        )
    ):
        return False
    return states[-2:] == ["VERIFY_POSTCONDITIONS", "DONE"]


def adapter_path_outcome(case: dict[str, object]) -> str:
    if case["native_denial"]:
        return "BLOCKED_NATIVE_DENIAL"
    if not case["supports_steps"]:
        return "BLOCKED_UNSUPPORTED"
    if case["semantic_drift"]:
        return "STALE_REVALIDATE"
    return "READY"


def evidence_valid(case: dict[str, object]) -> bool:
    facts = case["facts"]
    return facts.keys() >= EVIDENCE_FIELDS and not case["secret_value"]


def test_all_approval_outcomes_and_strictest_effect_are_enforced(
    cases: dict[str, object],
) -> None:
    approval_cases = cases["approval_cases"]
    assert {case["expected"] for case in approval_cases} == OUTCOME_RANK.keys()
    for case in approval_cases:
        assert len(case["effects"]) == len(case["effect_outcomes"])
        assert authorization_outcome(case) == case["expected"]
    strictest = next(case for case in approval_cases if case["id"] == "strictest-effect-wins")
    assert strictest["effect_outcomes"][0] == "ALLOW_TASK"
    assert authorization_outcome(strictest) == "REQUIRE_HUMAN"


def test_envelope_target_and_context_mismatches_fail_closed(cases: dict[str, object]) -> None:
    envelope_cases = cases["envelope_cases"]
    baseline = envelope_cases[0]
    for case in envelope_cases:
        approved = case.get("approved", baseline["approved"])
        requested = dict(case.get("requested", baseline["requested"]))
        if mutation := case.get("mutation"):
            requested[mutation["field"]] = mutation["value"]
        assert envelope_valid(approved, requested) is case["expected_valid"], case["id"]
    assert {case["id"] for case in envelope_cases} >= {
        "missing-target",
        "target-mismatch",
        "resource-outside-scope",
        "privilege-above-ceiling",
        "credential-binding-mismatch",
        "network-binding-mismatch",
        "context-drift",
    }


def test_child_adapter_and_indirection_authority_never_expand(cases: dict[str, object]) -> None:
    for case in cases["authority_cases"]:
        assert authority_is_subset(case["parent"], case["child"]) is case["expected_valid"]
    assert sum(not case["expected_valid"] for case in cases["authority_cases"]) == 3


def test_runbook_routing_covers_all_material_operation_families(
    cases: dict[str, object],
) -> None:
    routing_cases = cases["runbook_routing_cases"]
    for case in routing_cases:
        assert runbook_required(case["traits"]) is case["expected"]
    covered_traits = {trait for case in routing_cases for trait in case["traits"]}
    assert covered_traits >= RUNBOOK_TRAITS


def test_approved_runbook_does_not_authorize_invocation(cases: dict[str, object]) -> None:
    fixture = cases["runbook_invocations"]
    assert fixture["runbook"]["procedurally_valid"] is True
    for invocation in fixture["cases"]:
        assert (
            invocation_executable(fixture["runbook"], invocation)
            is invocation["expected_executable"]
        )
    assert sum(invocation["expected_executable"] for invocation in fixture["cases"]) == 1


def test_runbook_lifecycle_checkpoints_recovery_and_staleness(cases: dict[str, object]) -> None:
    for case in cases["lifecycle_cases"]:
        assert valid_lifecycle(case["states"]) is case["expected_valid"], case["id"]
        assert case["states"][-1] == case["expected_terminal"]
        if case.get("human_approved") is False:
            assert "EXECUTE_STEP" not in case["states"]
    no_postconditions = next(
        case for case in cases["lifecycle_cases"] if case["id"] == "exit-without-postconditions"
    )
    assert no_postconditions["states"][-1] == "DONE"
    assert valid_lifecycle(no_postconditions["states"]) is False


def test_adapter_equivalence_uses_semantics_not_syntax(cases: dict[str, object]) -> None:
    for pair in cases["adapter_pairs"]:
        assert pair["left"]["family"] != pair["right"]["family"]
        equivalent = pair["left"]["semantic"] == pair["right"]["semantic"]
        assert equivalent is pair["expected_equivalent"]
    syntax_pair = cases["adapter_pairs"][0]
    assert syntax_pair["left"]["inert_syntax"] != syntax_pair["right"]["inert_syntax"]
    assert syntax_pair["left"]["semantic"] == syntax_pair["right"]["semantic"]


def test_unsupported_stale_and_native_denied_adapter_paths_block(
    cases: dict[str, object],
) -> None:
    for case in cases["adapter_path_cases"]:
        assert adapter_path_outcome(case) == case["expected"]
    assert {case["expected"] for case in cases["adapter_path_cases"]} == {
        "READY",
        "BLOCKED_UNSUPPORTED",
        "STALE_REVALIDATE",
        "BLOCKED_NATIVE_DENIAL",
    }


def test_material_evidence_is_semantic_sanitized_and_transcript_independent(
    cases: dict[str, object],
) -> None:
    for case in cases["evidence_cases"]:
        assert evidence_valid(case) is case["expected_valid"]
    transcript_free = next(
        case for case in cases["evidence_cases"] if case["id"] == "raw-transcript-not-required"
    )
    assert transcript_free["raw_terminal_transcript"] is False
    assert evidence_valid(transcript_free)


def test_core_protocol_and_execution_control_module_alignment(repo_root: Path) -> None:
    governance = repo_root / "governance-core" / "GOVERNANCE.md"
    execution = (repo_root / "governance-core" / "EXECUTION.md").read_text(encoding="utf-8")
    governance_text = governance.read_text(encoding="utf-8")
    assert SOURCE_PROTOCOL_VERSION == "1.11.0"
    assert "EXECUTION-CONTROL.md" in CORE_REQUIRED_MODULES
    assert protocol_version_from(governance) == SOURCE_PROTOCOL_VERSION
    assert ".agent-governance/EXECUTION-CONTROL.md" in governance_text
    assert "EXECUTION-CONTROL.md" in execution


def test_fixture_is_platform_terminal_cli_api_and_executor_host_neutral(
    cases: dict[str, object],
) -> None:
    families = {
        adapter[side]["family"] for adapter in cases["adapter_pairs"] for side in ("left", "right")
    }
    assert families == {"command-environment", "native-api-automation"}
    fixture_text = json.dumps(cases)
    for product_dependency in ("PowerShell", "POSIX", "Windows", "Linux", "OpenCode", "Codex"):
        assert product_dependency not in fixture_text
