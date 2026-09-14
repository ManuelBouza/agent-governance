from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "evals" / "t068_chatgpt_skill_host" / "qualification-corpus.json"
EXPECTED_SKILLS = {
    "source-maintainer",
    "repository-change-control",
    "upstream-version-revalidation",
    "research-evidence-traceability",
    "durable-work-checkpoint",
    "executor-launch-handoff",
}


def load_corpus() -> dict[str, object]:
    return json.loads(CORPUS.read_text(encoding="utf-8"))


def test_corpus_freezes_exact_d082_top_level_skill_set() -> None:
    corpus = load_corpus()
    assert set(corpus["expected_top_level_skills"]) == EXPECTED_SKILLS
    assert corpus["forbidden_top_level_skills"] == ["workspace-isolation"]
    assert "workspace-isolation" not in corpus["expected_top_level_skills"]


def test_corpus_has_unique_observable_scenarios() -> None:
    corpus = load_corpus()
    scenarios = corpus["scenarios"]
    assert isinstance(scenarios, list)
    ids = [scenario["id"] for scenario in scenarios]
    assert len(ids) == len(set(ids)) == 22
    assert corpus["scoring_boundary"] == {
        "observable_only": True,
        "hidden_chain_of_thought_required": False,
        "automatic_routing_claim_requires_auto_mode": True,
        "explicit_invocation_alone_does_not_prove_auto_routing": True,
    }
    for scenario in scenarios:
        assert scenario["prompt"].strip()
        assert scenario["expected_visible_behavior"]
        assert scenario["forbidden_visible_behavior"]


def test_every_skill_has_explicit_positive_and_negative_coverage() -> None:
    corpus = load_corpus()
    scenarios = corpus["scenarios"]
    assert isinstance(scenarios, list)

    explicit = Counter()
    positive = Counter()
    negative = Counter()
    for scenario in scenarios:
        scenario_id = scenario["id"]
        if scenario_id.startswith("T068-EXPLICIT-"):
            for skill in scenario["target_skills"]:
                explicit[skill] += 1
        elif scenario_id.startswith("T068-AUTO-POS-"):
            for skill in scenario["target_skills"]:
                positive[skill] += 1
        elif scenario_id.startswith("T068-AUTO-NEG-"):
            negative[scenario["anti_target_skill"]] += 1

    assert set(explicit) == EXPECTED_SKILLS
    assert set(positive) == EXPECTED_SKILLS
    assert set(negative) == EXPECTED_SKILLS
    assert all(explicit[skill] == 1 for skill in EXPECTED_SKILLS)
    assert all(positive[skill] == 1 for skill in EXPECTED_SKILLS)
    assert all(negative[skill] == 1 for skill in EXPECTED_SKILLS)


def test_auto_routing_scenarios_never_target_workspace_isolation() -> None:
    corpus = load_corpus()
    scenarios = corpus["scenarios"]
    assert isinstance(scenarios, list)
    for scenario in scenarios:
        assert "workspace-isolation" not in scenario.get("target_skills", [])
        assert scenario.get("anti_target_skill") != "workspace-isolation"


def test_role_and_composition_cases_cover_d082_boundaries() -> None:
    corpus = load_corpus()
    scenarios = {scenario["id"]: scenario for scenario in corpus["scenarios"]}

    role = scenarios["T068-ROLE-01"]
    assert role["target_skills"] == ["source-maintainer"]
    assert any("Orchestrator route" in item for item in role["expected_visible_behavior"])
    assert any("Executor route" in item for item in role["forbidden_visible_behavior"])

    composition = scenarios["T068-COMPOSE-03"]
    assert set(composition["target_skills"]) == {
        "source-maintainer",
        "repository-change-control",
        "executor-launch-handoff",
    }
    assert any("workspace isolation" in item for item in composition["expected_visible_behavior"])
    assert any("seventh top-level Skill" in item for item in composition["forbidden_visible_behavior"])
