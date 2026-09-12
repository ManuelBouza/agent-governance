"""Provider-free characterization of the T023 v15 independent scheduler."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


def _load_harness(repo_root: Path):
    path = repo_root / "evals" / "skill_activation_topology" / "harness.py"
    spec = importlib.util.spec_from_file_location("t023_v15_scheduler_harness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def harness(repo_root: Path):
    return _load_harness(repo_root)


@pytest.fixture(scope="module")
def frozen(harness):
    return harness.load_frozen_inputs()


def _record(harness, frozen, spec, *, context: int = 1000):
    return {
        "case_id": spec.case["id"],
        "case_class": spec.case["class"],
        "candidate_id": spec.candidate_id,
        "repetition": spec.repetition,
        "activated_entrypoints": harness.expected_entrypoints(frozen, spec),
        "expected_entrypoints": harness.expected_entrypoints(frozen, spec),
        "semantic_outcome": spec.case["expected_semantic_outcome"],
        "expected_semantic_outcome": spec.case["expected_semantic_outcome"],
        "granted_capabilities": spec.case["expected_capabilities"],
        "forbidden_capabilities": spec.case.get("forbidden_capabilities", []),
        "permission_broadening": False,
        "observed_context_bytes": context,
        "loaded_reference_bytes": 0,
    }


def test_provider_free_scheduler_simulation_passes_with_zero_provider_calls(
    harness, frozen
) -> None:
    evidence = harness.run_provider_free_scheduler_simulation(frozen)
    assert evidence["status"] == "PASS"
    assert evidence["execution_epoch"] == "MG1-T023-EXECUTION-v15"
    assert evidence["provider_model_calls_issued"] == 0
    assert set(evidence["scenarios"]) == {
        "base_round_robin",
        "conditional_third_pair_scoped",
        "critical_instability_still_gets_r3",
        "no_fourth_repetition",
        "b2_nonblocking_split_local_futility",
    }
    assert all(item["status"] == "PASS" for item in evidence["scenarios"].values())


def test_conditional_thirds_are_pair_scoped_and_candidate_ordered(harness, frozen) -> None:
    case = harness.scheduled_trials(frozen)[0].case
    trials = []
    for candidate in frozen.oracle["candidate_ids"]:
        for repetition in (1, 2):
            context = 1001 if candidate in {"F2", "G3"} and repetition == 2 else 1000
            spec = harness.TrialSpec(case, candidate, repetition)
            trials.append(_record(harness, frozen, spec, context=context))
    thirds = harness.conditional_third_specs(frozen, frozen.oracle["candidate_ids"], trials)
    assert [spec.key for spec in thirds] == [
        f"{case['id']}--F2--r3",
        f"{case['id']}--G3--r3",
    ]


def test_b2_scientific_failure_never_becomes_terminal_futility(harness, frozen) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["class"] == "cross-profile")
    spec = harness.TrialSpec(case, "B2", 1)
    trial = _record(harness, frozen, spec)
    trial["semantic_outcome"] = "activate"
    certificate = harness.qualification_futility_certificate(frozen, "B2", [trial])
    assert certificate["failed_bounds"]
    assert certificate["early_stop_allowed"] is False
    assert certificate["terminal"] is False
    assert certificate["certificate_type"] == "B2_MEASUREMENT_CONTINUES"


def test_split_scientific_futility_is_candidate_local(harness, frozen) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["class"] == "cross-profile")
    spec = harness.TrialSpec(case, "F2", 1)
    trial = _record(harness, frozen, spec)
    trial["semantic_outcome"] = "activate"
    certificate = harness.qualification_futility_certificate(frozen, "F2", [trial])
    assert certificate["early_stop_allowed"] is True
    assert certificate["terminal"] is True
    assert certificate["certificate_type"] == "FUTILE_QUALIFICATION"


def test_no_fourth_repetition_is_accepted(harness, frozen) -> None:
    spec = harness.TrialSpec(frozen.corpus["cases"][0], "B2", 4)
    with pytest.raises(harness.HarnessError, match="outside the frozen v15 identity set"):
        harness.validate_repetition(frozen, spec)


def test_critical_split_instability_still_requires_r3(harness, frozen) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["class"] == "cross-profile")
    first = _record(harness, frozen, harness.TrialSpec(case, "F2", 1))
    first["semantic_outcome"] = "activate"
    second = _record(harness, frozen, harness.TrialSpec(case, "F2", 2))
    trials = [first, second]
    certificate = harness.qualification_futility_certificate(frozen, "F2", trials)
    assert certificate["terminal"] is True
    thirds = harness.conditional_third_specs(frozen, ["F2"], trials)
    assert [spec.key for spec in thirds] == [f"{case['id']}--F2--r3"]
