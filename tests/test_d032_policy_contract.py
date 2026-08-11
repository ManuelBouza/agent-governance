"""Mechanical D032 examples; Core Markdown remains semantic authority."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

QUALITY_OUTCOMES = frozenset({"BASELINE", "MATERIAL", "NOT_APPLICABLE"})
DIAGRAMS = {
    "system-boundary": "C4 System Context",
    "service-data-store-boundary": "C4 Container",
    "component-dependency-boundary": "C4 Component",
    "temporal-collaboration": "dynamic/sequence",
    "lifecycle-transition": "state diagram",
    "trust-boundary-data-flow": "DFD with trust boundaries",
    "persistent-relationship": "ER/data model",
    "local-workflow-dependency": "compact flow/dependency diagram",
}
MATERIAL_CHANGE_BOUNDARIES = frozenset({"architecture", "data-flow", "state", "responsibility"})


@pytest.fixture(scope="module")
def cases() -> dict[str, list[dict[str, object]]]:
    path = Path(__file__).parent / "fixtures" / "d032" / "policy_cases.json"
    return json.loads(path.read_text(encoding="utf-8"))


def engineering_contract(case: dict[str, object]) -> tuple[object, object, object]:
    """Presentation metadata deliberately does not enter engineering identity."""

    return case["engineering_id"], tuple(case["controls"]), case["acceptance"]


def user_visible(concern: dict[str, object]) -> bool:
    return concern["outcome"] == "MATERIAL" and concern["human_impact"] is True


def selected_diagram(case: dict[str, object]) -> str:
    return DIAGRAMS[case["dominant_question"]]


def refresh_required(case: dict[str, object]) -> bool:
    return bool(MATERIAL_CHANGE_BOUNDARIES.intersection(case["changes"]))


def test_register_variants_preserve_engineering_contract(
    cases: dict[str, list[dict[str, object]]],
) -> None:
    variants = cases["register_cases"]
    contracts = {engineering_contract(case) for case in variants}
    assert {case["register"] for case in variants} == {
        "plain/domain",
        "expert/architecture",
        "code-native",
    }
    assert len(contracts) == 1
    changed_presentation = {**variants[0], "register": "practitioner/technical"}
    assert engineering_contract(changed_presentation) == engineering_contract(variants[0])


def test_code_native_fixture_preserves_supplied_tokens(
    cases: dict[str, list[dict[str, object]]],
) -> None:
    code_native = next(
        case for case in cases["register_cases"] if case["register"] == "code-native"
    )
    assert code_native["supplied_tokens"] == code_native["preserved_tokens"]


def test_quality_routing_is_material_and_security_is_always_triaged(
    cases: dict[str, list[dict[str, object]]],
) -> None:
    for case in cases["quality_cases"]:
        concerns = case["concerns"]
        assert any(concern["dimension"] == "security" for concern in concerns)
        for concern in concerns:
            assert concern["outcome"] in QUALITY_OUTCOMES
            if concern["outcome"] == "MATERIAL":
                assert concern["control"] in case["controls"]
            assert user_visible(concern) == (concern["dimension"] in case["visible"])


def test_privacy_routes_independently_from_security(
    cases: dict[str, list[dict[str, object]]],
) -> None:
    sensitive_export = next(
        case for case in cases["quality_cases"] if case["id"] == "sensitive-export"
    )
    outcomes = {
        concern["dimension"]: concern["outcome"] for concern in sensitive_export["concerns"]
    }
    assert outcomes["privacy"] == "MATERIAL"
    assert outcomes["security"] == "BASELINE"


@pytest.mark.parametrize("dominant_question, expected", DIAGRAMS.items())
def test_primary_diagram_follows_dominant_question(
    cases: dict[str, list[dict[str, object]]], dominant_question: str, expected: str
) -> None:
    case = next(
        case for case in cases["diagram_cases"] if case["dominant_question"] == dominant_question
    )
    assert case["expected"] == expected
    assert selected_diagram(case) == expected
    assert selected_diagram({**case, "product_label": "unrelated-label"}) == expected


def test_diagram_refresh_tracks_material_solution_boundary(
    cases: dict[str, list[dict[str, object]]],
) -> None:
    for case in cases["refresh_cases"]:
        assert refresh_required(case) is case["refresh_required"]
