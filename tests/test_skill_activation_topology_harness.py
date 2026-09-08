"""Deterministic characterization for the T023 MG1-v15 RIQ-NBC harness."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


def load_harness(repo_root: Path):
    path = repo_root / "evals" / "skill_activation_topology" / "harness.py"
    spec = importlib.util.spec_from_file_location("t023_v15_harness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def harness(repo_root: Path):
    return load_harness(repo_root)


@pytest.fixture(scope="module")
def frozen(harness):
    return harness.load_frozen_inputs()


def test_frozen_v15_inputs_validate_and_schedule_exact_budgets(harness, frozen) -> None:
    assert frozen.oracle["oracle_id"] == "MG1-T023-TOPOLOGY-ORACLE-v15"
    assert frozen.oracle["execution_epoch"] == "MG1-T023-EXECUTION-v15"
    assert frozen.oracle["strategy"] == "RIQ-NBC"
    assert frozen.oracle["candidate_ids"] == ["B2", "F2", "G3"]
    assert frozen.oracle["capability_source_epoch"] == "MG1-2026-09-06-v4"
    assert frozen.oracle["presentation_revision"] == "MG1-T023-PRESENTATIONS-v5"
    assert len(frozen.corpus["cases"]) == 70
    assert len(harness.scheduled_trials(frozen)) == 420
    assert len(harness.all_possible_trials(frozen)) == 630


def test_base_schedule_is_all_r1_then_r2_with_b2_f2_g3_round_robin(harness, frozen) -> None:
    schedule = harness.scheduled_trials(frozen)
    first_case = schedule[0].case["id"]
    assert [spec.key for spec in schedule[:3]] == [
        f"{first_case}--B2--r1",
        f"{first_case}--F2--r1",
        f"{first_case}--G3--r1",
    ]
    assert all(spec.repetition == 1 for spec in schedule[:210])
    assert all(spec.repetition == 2 for spec in schedule[210:])
    assert [spec.candidate_id for spec in schedule[210:213]] == ["B2", "F2", "G3"]


@pytest.mark.parametrize("candidate_id", ["B2", "F2", "G3"])
def test_candidate_materialization_is_exact_byte_copy(
    tmp_path: Path, harness, frozen, candidate_id: str
) -> None:
    destination = tmp_path / candidate_id
    destination.mkdir()
    evidence = harness.materialize_candidate(frozen, candidate_id, destination)
    assert evidence["construction"] == "byte-copy"
    assert evidence["files"]
    for record in evidence["files"]:
        source = harness.REPO_ROOT / record["source"]
        target = destination / record["target"]
        assert target.read_bytes() == source.read_bytes()


def test_expected_entrypoints_follow_frozen_topology(harness, frozen) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["class"] == "multi-intent")
    for candidate_id in frozen.oracle["candidate_ids"]:
        spec = harness.TrialSpec(case, candidate_id, 1)
        mapping = frozen.topologies["candidates"][candidate_id]["capability_to_entrypoints"]
        expected: list[str] = []
        for capability in case["expected_capabilities"]:
            for entrypoint in mapping[capability]:
                if entrypoint not in expected:
                    expected.append(entrypoint)
        assert harness.expected_entrypoints(frozen, spec) == expected


def _metrics(
    candidate: str,
    *,
    f1: float,
    median: int,
    far: float = 0.0,
    wrong: float = 0.0,
    over: float = 0.0,
    deterministic: str = "PASS",
) -> dict:
    return {
        "candidate_id": candidate,
        "activation_precision": f1,
        "activation_recall": f1,
        "activation_f1": f1,
        "false_activation_rate": far,
        "wrong_specialist_rate": wrong,
        "overactivation_rate": over,
        "semantic_outcome_accuracy": 1.0,
        "semantic_outcome_accuracy_cross_profile_and_ambiguous": 1.0,
        "cross_profile_violation_count": 0,
        "ambiguous_context_permission_broadening_count": 0,
        "median_observed_context_bytes": median,
        "p95_observed_context_bytes": median,
        "median_loaded_reference_bytes": 0,
        "p95_loaded_reference_bytes": 0,
        "single_install_feasibility": True,
        "source_distribution_integrity": True,
        "full_deterministic_regression": deterministic,
        "profile_isolation_regression": "PASS",
        "consumer_source_independence_regression": "PASS",
    }


def test_regime_a_keeps_b2_without_material_split(harness, frozen) -> None:
    metrics = {
        "B2": _metrics("B2", f1=0.97, median=1000),
        "F2": _metrics("F2", f1=0.98, median=800),
        "G3": _metrics("G3", f1=0.98, median=750),
    }
    selection = harness.apply_selection_rule(frozen, metrics)
    assert selection["status"] == "SELECTED"
    assert selection["selection_regime"] == "B2_QUALIFIES"
    assert selection["selected_candidate"] == "B2"
    assert selection["material_split_candidates"] == []


def test_regime_a_selects_material_split(harness, frozen) -> None:
    metrics = {
        "B2": _metrics("B2", f1=0.96, median=1000, far=0.01, wrong=0.01, over=0.01),
        "F2": _metrics("F2", f1=0.995, median=800, far=0.01, wrong=0.01, over=0.01),
        "G3": _metrics("G3", f1=0.97, median=700, far=0.01, wrong=0.01, over=0.01),
    }
    selection = harness.apply_selection_rule(frozen, metrics)
    assert selection["selected_candidate"] == "F2"
    assert selection["material_split_candidates"] == ["F2"]


def test_regime_b_uses_admissibility_without_relative_f1_uplift(harness, frozen) -> None:
    metrics = {
        "B2": _metrics("B2", f1=0.90, median=1000, far=0.04, wrong=0.04, over=0.04),
        "F2": _metrics("F2", f1=0.96, median=800, far=0.04, wrong=0.04, over=0.04),
        "G3": _metrics("G3", f1=0.96, median=900, far=0.04, wrong=0.04, over=0.04),
    }
    selection = harness.apply_selection_rule(frozen, metrics)
    assert selection["status"] == "SELECTED"
    assert selection["selection_regime"] == "B2_SCIENTIFICALLY_NONQUALIFYING"
    assert selection["selected_candidate"] == "F2"
    assert selection["admissible_split_candidates"] == ["F2"]


def test_regime_b_can_validly_select_no_topology(harness, frozen) -> None:
    metrics = {
        "B2": _metrics("B2", f1=0.90, median=1000),
        "F2": _metrics("F2", f1=0.96, median=900),
        "G3": _metrics("G3", f1=0.96, median=950),
    }
    selection = harness.apply_selection_rule(frozen, metrics)
    assert selection["status"] == "NO_SELECTION"
    assert selection["selected_candidate"] is None
    assert selection["reason"] == "NO_ADMISSIBLE_SPLIT"


def test_technical_b2_invalidity_fails_closed(harness, frozen) -> None:
    metrics = {
        "B2": _metrics("B2", f1=0.90, median=1000, deterministic="FAIL"),
        "F2": _metrics("F2", f1=0.99, median=700),
        "G3": _metrics("G3", f1=0.99, median=650),
    }
    selection = harness.apply_selection_rule(frozen, metrics)
    assert selection["status"] == "BLOCKED"
    assert selection["selected_candidate"] is None
    assert selection["reason"] == "INVALID_B2_CONTROL"


def test_exact_split_tie_falls_to_f2(harness, frozen) -> None:
    metrics = {
        "B2": _metrics("B2", f1=0.90, median=1000),
        "F2": _metrics("F2", f1=0.96, median=800),
        "G3": _metrics("G3", f1=0.96, median=800),
    }
    selection = harness.apply_selection_rule(frozen, metrics)
    assert selection["selected_candidate"] == "F2"


def test_trial_output_schema_is_closed(harness) -> None:
    assert harness.TRIAL_SCHEMA["additionalProperties"] is False
    assert set(harness.TRIAL_SCHEMA["required"]) == set(harness.TRIAL_SCHEMA["properties"])
    json.dumps(harness.TRIAL_SCHEMA)


def test_model_visible_turn_is_exact_prompt_and_neutral_suffix(harness, frozen) -> None:
    suffix = frozen.envelope["user_suffix"]
    forbidden = frozen.envelope["forbidden_added_terms_casefold"]
    for case in frozen.corpus["cases"]:
        visible = harness._trial_prompt(frozen, case)
        assert visible == f"{case['prompt']}\n\n{suffix}"
        added = visible.removeprefix(case["prompt"]).casefold()
        assert not [term for term in forbidden if term in added]


@pytest.mark.parametrize("role", ["neutral", "source", "consumer"])
def test_fixture_materialization_is_exact_and_role_bounded(
    tmp_path: Path, harness, frozen, role: str
) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["fixture_role"] == role)
    destination = tmp_path / role
    destination.mkdir()
    evidence = harness.materialize_fixture(frozen, case, destination)
    expected = frozen.envelope["fixtures"][role]
    expected_files = {item["path"]: item["json"] for item in expected.get("files", [])}
    actual_files = {
        path.relative_to(destination).as_posix(): json.loads(path.read_text(encoding="utf-8"))
        for path in destination.rglob("*")
        if path.is_file()
    }
    assert evidence["fixture_role"] == role
    assert actual_files == expected_files


def test_clarification_expectations_follow_frozen_topology(harness, frozen) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["class"] == "ambiguous")
    for candidate_id in frozen.oracle["candidate_ids"]:
        spec = harness.TrialSpec(case, candidate_id, 1)
        assert (
            harness.expected_entrypoints(frozen, spec)
            == frozen.topologies["candidates"][candidate_id]["ambiguous_entrypoints"]
        )


def _perfect_trials(harness, frozen, candidate_id: str) -> list[dict]:
    return [
        {
            "case_id": spec.case["id"],
            "candidate_id": candidate_id,
            "repetition": spec.repetition,
            "case_class": spec.case["class"],
            "activated_entrypoints": harness.expected_entrypoints(frozen, spec),
            "expected_entrypoints": harness.expected_entrypoints(frozen, spec),
            "semantic_outcome": spec.case["expected_semantic_outcome"],
            "expected_semantic_outcome": spec.case["expected_semantic_outcome"],
            "granted_capabilities": spec.case["expected_capabilities"],
            "forbidden_capabilities": spec.case.get("forbidden_capabilities", []),
            "permission_broadening": False,
            "loaded_reference_bytes": 100,
            "observed_context_bytes": 1000,
        }
        for spec in harness.scheduled_trials(frozen)
        if spec.candidate_id == candidate_id
    ]


def test_perfect_b2_metrics_qualify(harness, frozen) -> None:
    trials = _perfect_trials(harness, frozen, "B2")
    deterministic = harness.build_deterministic_evidence(frozen)
    deterministic.update(
        full_deterministic_regression="PASS",
        profile_isolation_regression="PASS",
        consumer_source_independence_regression="PASS",
    )
    metrics = harness.compute_candidate_metrics(frozen, "B2", trials, deterministic)
    assert metrics["case_count"] == 70
    assert metrics["valid_repetition_count"] == 140
    assert metrics["activation_f1"] == 1.0
    assert metrics["false_activation_rate"] == 0.0
    assert harness.candidate_qualifies(frozen, metrics) is True


def test_observed_activation_uses_successful_host_reads(harness, frozen) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["class"] == "positive-consumer")
    trial = harness.TrialSpec(case, "B2", 1)
    skill = ".agents/skills/agent-governance/SKILL.md"
    reference = ".agents/skills/agent-governance/references/consumer-lifecycle.md"
    events = [
        {"type": "thread.started", "thread_id": "synthetic"},
        {
            "type": "item.completed",
            "item": {"type": "command_execution", "command": f"Get-Content {skill}", "exit_code": 0},
        },
        {
            "type": "item.completed",
            "item": {
                "type": "command_execution",
                "command": f"Get-Content {reference}",
                "exit_code": 0,
            },
        },
    ]
    stdout = "\n".join(json.dumps(event) for event in events)
    entrypoints, references, trace = harness._observed_skill_reads(frozen, trial, stdout)
    assert entrypoints == ["agent-governance"]
    assert references == [frozen.manifest["shared_references"]["consumer-lifecycle"]]
    assert trace is True
