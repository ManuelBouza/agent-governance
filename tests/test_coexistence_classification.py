"""Synthetic capability/ownership coexistence classification tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

OUTCOMES = frozenset({"REUSE", "ADAPT", "COEXIST", "MISSING", "CONFLICT"})


def _surfaces(providers: list[dict[str, object]]) -> list[str]:
    return [
        surface
        for provider in providers
        for key in ("write_surfaces", "authority_surfaces")
        for surface in provider.get(key, [])
    ]


def classify(case: dict[str, object]) -> str:
    """Classify explicit fixture facts; labels never determine routing."""

    providers = case["providers"]
    surfaces = _surfaces(providers)
    skill = case.get("selected_skill")
    managed = case.get("managed_collision")
    if len(surfaces) != len(set(surfaces)):
        return "CONFLICT"
    if skill and skill["approved"] and skill["selected"] != skill["approved"]:
        return "CONFLICT"
    if managed and not managed["safe_composition"]:
        return "CONFLICT"
    if not providers:
        return "MISSING"
    if case.get("adapter_needed") or managed:
        return "ADAPT"
    if len(providers) > 1:
        return "COEXIST"
    if any(case["required"] in provider["capabilities"] for provider in providers):
        return "REUSE"
    return "COEXIST"


@pytest.fixture(scope="module")
def cases() -> list[dict[str, object]]:
    path = Path(__file__).parent / "fixtures" / "coexistence" / "cases.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "case_id",
    [
        case["id"]
        for case in json.loads(
            (Path(__file__).parent / "fixtures" / "coexistence" / "cases.json").read_text()
        )
    ],
)
def test_each_fixture_matches_explicit_expected_classification(
    cases: list[dict[str, object]], case_id: str
) -> None:
    case = next(case for case in cases if case["id"] == case_id)
    assert case["expected"] in OUTCOMES
    assert classify(case) == case["expected"]


def test_required_outcomes_are_covered(cases: list[dict[str, object]]) -> None:
    assert {case["expected"] for case in cases} == OUTCOMES


def test_reuse_and_adapt_preserve_native_ownership(cases: list[dict[str, object]]) -> None:
    reuse = next(case for case in cases if case["expected"] == "REUSE")
    adapt = next(case for case in cases if case["id"] == "openspec-like-adapt")
    assert reuse["outcome"]["duplicate_artifacts"] == []
    assert adapt["outcome"]["native_owner"] == "openspec-like"
    assert adapt["outcome"]["governance_reference"] == "change-plan"


def test_coexistence_needs_separate_surfaces_and_conflicts_fail_closed(
    cases: list[dict[str, object]],
) -> None:
    coexist = next(case for case in cases if case["expected"] == "COEXIST")
    conflict = next(case for case in cases if case["id"] == "custom-sdd-overlap")
    assert len(_surfaces(coexist["providers"])) == len(set(_surfaces(coexist["providers"])))
    assert classify(conflict) == "CONFLICT"
    renamed = {
        **conflict,
        "providers": [{**provider, "label": "winner"} for provider in conflict["providers"]],
    }
    assert classify(renamed) == "CONFLICT"


def test_no_sdd_and_skill_precedence_remain_non_authoritative(
    cases: list[dict[str, object]],
) -> None:
    no_sdd = next(case for case in cases if case["id"] == "no-sdd-missing")
    shadow = next(case for case in cases if case["id"] == "same-name-skill-precedence")
    rejected = next(case for case in cases if case["id"] == "same-name-skill-unapproved")
    assert no_sdd["no_sdd_valid"] is True
    assert shadow["selected_skill"]["selected"] == "project/review-v2"
    assert shadow["selected_skill"]["trusted"] is False
    assert classify(rejected) == "CONFLICT"


def test_managed_surfaces_preserve_owner_or_fail_closed(cases: list[dict[str, object]]) -> None:
    composed = next(case for case in cases if case["id"] == "managed-surface-composed")
    blocked = next(case for case in cases if case["id"] == "managed-surface-blocked")
    assert composed["outcome"]["preserved_owner"] == composed["managed_collision"]["owner"]
    assert classify(composed) == "ADAPT"
    assert classify(blocked) == "CONFLICT"


def test_product_labels_do_not_control_classification(cases: list[dict[str, object]]) -> None:
    named = next(case for case in cases if case["id"] == "spec-kit-like-reuse")
    generic = next(case for case in cases if case["id"] == "generic-label-control")
    assert classify(named) == classify(generic) == "REUSE"
