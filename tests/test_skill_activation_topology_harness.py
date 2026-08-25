"""Deterministic technical coverage for the T023 MG1-v2 harness."""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from itertools import product
from pathlib import Path

import pytest


def load_harness(repo_root: Path):
    path = repo_root / "evals" / "skill_activation_topology" / "harness.py"
    spec = importlib.util.spec_from_file_location("t023_harness", path)
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


def test_frozen_mg1_v2_inputs_validate_and_schedule_360_trials(harness, frozen) -> None:
    assert frozen.oracle["oracle_id"] == "MG1-T023-TOPOLOGY-ORACLE-v2"
    assert frozen.oracle["capability_source_epoch"] == "MG1-2026-08-25-v2"
    assert frozen.oracle["presentation_revision"] == "MG1-T023-PRESENTATIONS-v2"
    assert len(harness.scheduled_trials(frozen)) == 360


@pytest.mark.parametrize("candidate_id", ["B0", "B1", "F2", "G3"])
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


def test_expected_entrypoint_union_and_unique_reference_load(harness, frozen) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["id"] == "I02")
    b0 = harness.TrialSpec(case, "B0", 1)
    g3 = harness.TrialSpec(case, "G3", 1)

    assert harness.expected_entrypoints(frozen, b0) == ["agent-governance"]
    assert harness.expected_entrypoints(frozen, g3) == [
        "source-maintainer",
        "consumer-lifecycle",
    ]
    paths, byte_count = harness.expected_load_path(frozen, b0)
    assert paths == [
        "evals/skill_activation_topology/presentations/shared/consumer-lifecycle.md",
        "evals/skill_activation_topology/presentations/shared/source-maintainer.md",
    ]
    assert byte_count == sum((harness.REPO_ROOT / path).stat().st_size for path in paths)


def test_selection_rule_retains_single_family_without_material_split(harness, frozen) -> None:
    def metrics(candidate: str, *, median: int, f1: float = 0.98) -> dict:
        return {
            "candidate_id": candidate,
            "activation_precision": f1,
            "activation_recall": f1,
            "activation_f1": f1,
            "false_activation_rate": 0.0,
            "wrong_specialist_rate": 0.0,
            "overactivation_rate": 0.0,
            "semantic_outcome_accuracy": 1.0,
            "semantic_outcome_accuracy_cross_profile_and_ambiguous": 1.0,
            "cross_profile_violation_count": 0,
            "ambiguous_context_permission_broadening_count": 0,
            "median_loaded_reference_bytes": median,
            "p95_loaded_reference_bytes": median,
            "single_install_feasibility": True,
            "source_distribution_integrity": True,
            "full_deterministic_regression": "PASS",
            "profile_isolation_regression": "PASS",
            "consumer_source_independence_regression": "PASS",
        }

    candidate_metrics = {
        "B0": metrics("B0", median=1000),
        "B1": metrics("B1", median=900),
        "F2": metrics("F2", median=800),
        "G3": metrics("G3", median=750),
    }
    selection = harness.apply_selection_rule(frozen, candidate_metrics)
    assert selection["selected_candidate"] == "B0"
    assert selection["material_split_challengers"] == []


def test_selection_rule_selects_material_challenger(harness, frozen) -> None:
    base = {
        "activation_precision": 0.96,
        "activation_recall": 0.96,
        "activation_f1": 0.96,
        "false_activation_rate": 0.01,
        "wrong_specialist_rate": 0.01,
        "overactivation_rate": 0.01,
        "semantic_outcome_accuracy": 0.99,
        "semantic_outcome_accuracy_cross_profile_and_ambiguous": 1.0,
        "cross_profile_violation_count": 0,
        "ambiguous_context_permission_broadening_count": 0,
        "p95_loaded_reference_bytes": 1200,
        "single_install_feasibility": True,
        "source_distribution_integrity": True,
        "full_deterministic_regression": "PASS",
        "profile_isolation_regression": "PASS",
        "consumer_source_independence_regression": "PASS",
    }
    candidate_metrics = {
        "B0": {**base, "candidate_id": "B0", "median_loaded_reference_bytes": 1000},
        "B1": {**base, "candidate_id": "B1", "median_loaded_reference_bytes": 900},
        "F2": {
            **base,
            "candidate_id": "F2",
            "activation_precision": 0.995,
            "activation_recall": 0.995,
            "activation_f1": 0.995,
            "median_loaded_reference_bytes": 800,
        },
        "G3": {**base, "candidate_id": "G3", "median_loaded_reference_bytes": 780},
    }
    selection = harness.apply_selection_rule(frozen, candidate_metrics)
    assert selection["selected_candidate"] == "F2"


def test_trial_output_schema_is_closed(harness) -> None:
    assert harness.TRIAL_SCHEMA["additionalProperties"] is False
    assert set(harness.TRIAL_SCHEMA["required"]) == set(harness.TRIAL_SCHEMA["properties"])
    json.dumps(harness.TRIAL_SCHEMA)


def test_observed_activation_uses_successful_host_reads(harness, frozen) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["id"] == "C01")
    trial = harness.TrialSpec(case, "B0", 1)
    events = [
        {"type": "thread.started", "thread_id": "synthetic"},
        {
            "type": "item.completed",
            "item": {
                "type": "command_execution",
                "command": r"Get-Content C:\\trial\\.agents\\skills\\agent-governance\\SKILL.md",
                "exit_code": 0,
            },
        },
        {
            "type": "item.completed",
            "item": {
                "type": "command_execution",
                "command": (
                    r"Get-Content C:\\trial\\.agents\\skills\\agent-governance"
                    r"\\references\\consumer-lifecycle.md"
                ),
                "exit_code": 0,
            },
        },
    ]
    stdout = "\n".join(json.dumps(event) for event in events)
    entrypoints, references, trace = harness._observed_skill_reads(frozen, trial, stdout)
    assert entrypoints == ["agent-governance"]
    assert references == [
        "evals/skill_activation_topology/presentations/shared/consumer-lifecycle.md"
    ]
    assert trace is True


def test_resume_rejects_changed_model_effort_or_frozen_identity(harness, frozen) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["id"] == "C01")
    trial = harness.TrialSpec(case, "B0", 1)
    structured = {"case_id": "C01", "candidate_id": "B0", "repetition": 1}
    raw = {
        "trial_key": trial.key,
        "command": [
            "codex",
            "exec",
            "--model",
            "gpt-5.6-sol",
            'model_reasoning_effort="medium"',
        ],
        "materialization": {
            "candidate_id": "B0",
            "presentation_revision": frozen.oracle["presentation_revision"],
            "capability_source_epoch": frozen.oracle["capability_source_epoch"],
        },
    }
    harness._validate_partial(
        frozen,
        trial,
        structured,
        raw,
        model="gpt-5.6-sol",
        effort="medium",
    )
    with pytest.raises(harness.HarnessError, match="model/effort"):
        harness._validate_partial(
            frozen,
            trial,
            structured,
            raw,
            model="gpt-5.6-sol",
            effort="high",
        )


def test_persisted_live_evidence_is_complete_and_recomputable(harness, frozen) -> None:
    evidence = harness.HERE / "evidence" / "mg1-v2-codex-windows-gpt-5.6-sol-medium"
    trials = harness.load_trials(evidence / "trials.jsonl")
    raw_trials = harness.load_trials(evidence / "raw-trials.jsonl")
    assert len(trials) == 360
    assert len(raw_trials) == 360

    counts = Counter(
        (trial["case_id"], trial["candidate_id"], trial["repetition"]) for trial in trials
    )
    expected_keys = set(
        product(
            [case["id"] for case in frozen.corpus["cases"]],
            frozen.oracle["candidate_ids"],
            range(1, 4),
        )
    )
    assert set(counts) == expected_keys
    assert set(counts.values()) == {1}
    assert {raw["trial_key"] for raw in raw_trials} == {
        f"{case_id}--{candidate_id}--r{repetition}"
        for case_id, candidate_id, repetition in expected_keys
    }

    deterministic = harness._load_json(evidence / "deterministic-evidence.json")
    persisted_metrics = harness._load_json(evidence / "metrics.json")
    recomputed_metrics = {
        candidate: harness.compute_candidate_metrics(frozen, candidate, trials, deterministic)
        for candidate in frozen.oracle["candidate_ids"]
    }
    assert recomputed_metrics == persisted_metrics
    assert harness.apply_selection_rule(frozen, recomputed_metrics) == harness._load_json(
        evidence / "selection.json"
    )

    diagnostic = harness._load_json(evidence / "oracle-diagnostics.json")
    assert diagnostic["status"] == "ORACLE_DEFECT_SUSPECTED"
    for case_id in {trial["case_id"] for trial in trials}:
        candidate_loads = {
            trial["loaded_reference_bytes"] for trial in trials if trial["case_id"] == case_id
        }
        assert len(candidate_loads) == 1
