"""Provider-free characterization for the MG1 v12 pair-scoped scheduler."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


def load_harness(repo_root: Path):
    path = repo_root / "evals" / "skill_activation_topology" / "harness.py"
    spec = importlib.util.spec_from_file_location("t023_v12_scheduler_harness", path)
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


def _pair_record(harness, frozen, spec):
    expected = harness.expected_entrypoints(frozen, spec)
    return {
        "case_id": spec.case["id"],
        "case_class": spec.case["class"],
        "candidate_id": spec.candidate_id,
        "repetition": spec.repetition,
        "activated_entrypoints": expected,
        "expected_entrypoints": expected,
        "semantic_outcome": spec.case["expected_semantic_outcome"],
        "expected_semantic_outcome": spec.case["expected_semantic_outcome"],
        "granted_capabilities": spec.case["expected_capabilities"],
        "forbidden_capabilities": spec.case.get("forbidden_capabilities", []),
        "permission_broadening": False,
        "observed_context_bytes": 1000,
        "loaded_reference_bytes": 0,
    }


def test_conditional_third_is_pair_scoped_with_unrelated_pairs_unscheduled(harness, frozen) -> None:
    schedule = harness.stage_schedule(frozen, "R")
    first_case = schedule[0].case
    next_case = next(spec.case for spec in schedule if spec.case["id"] != first_case["id"])
    partial = [
        _pair_record(harness, frozen, harness.TrialSpec(first_case, "B0", repetition))
        for repetition in (1, 2)
    ]
    partial.append(_pair_record(harness, frozen, harness.TrialSpec(next_case, "B0", 1)))
    assert harness.conditional_third_specs(frozen, ["B0"], partial) == []
    partial[1]["observed_context_bytes"] += 1
    assert [spec.key for spec in harness.conditional_third_specs(frozen, ["B0"], partial)] == [
        f"{first_case['id']}--B0--r3"
    ]


def test_provider_free_scheduler_simulation_covers_v12_gate(harness, frozen) -> None:
    evidence = harness.run_provider_free_scheduler_simulation(frozen)
    assert evidence["status"] == "PASS"
    assert evidence["provider_model_calls_issued"] == 0
    assert evidence["scenarios"]["no_fourth_repetition"]["status"] == "PASS"
    assert evidence["scenarios"]["full_reference_adaptive_dry_run"] == {
        "status": "PASS",
        "scheduled_observations": 160,
    }
