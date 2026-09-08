"""Provider-free characterization of the T023 v15 RIQ-NBC scheduler."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .aggregation import conditional_third_specs, qualification_futility_certificate
from .models import FrozenInputs, HarnessError, TrialSpec
from .scheduling import ordered_cases, scheduled_trials, validate_repetition


def _record(inputs: FrozenInputs, spec: TrialSpec, *, context_bytes: int = 1000) -> dict[str, Any]:
    expected = spec.case["expected_semantic_outcome"]
    return {
        "case_id": spec.case["id"],
        "case_class": spec.case["class"],
        "candidate_id": spec.candidate_id,
        "repetition": spec.repetition,
        "activated_entrypoints": [],
        "expected_entrypoints": [],
        "semantic_outcome": expected,
        "expected_semantic_outcome": expected,
        "granted_capabilities": [],
        "forbidden_capabilities": spec.case.get("forbidden_capabilities", []),
        "permission_broadening": False,
        "observed_context_bytes": context_bytes,
        "loaded_reference_bytes": 0,
    }


def _base_order_scenario(inputs: FrozenInputs) -> dict[str, Any]:
    schedule = scheduled_trials(inputs)
    cases = ordered_cases(inputs)
    candidates = inputs.oracle["candidate_ids"]
    expected = [
        TrialSpec(case, candidate, repetition).key
        for repetition in (1, 2)
        for case in cases
        for candidate in candidates
    ]
    actual = [spec.key for spec in schedule]
    if actual != expected or len(actual) != 420:
        raise HarnessError("provider-free v15 base schedule does not match frozen order")
    return {
        "status": "PASS",
        "scheduled_observations": len(actual),
        "first_six": actual[:6],
        "last_six": actual[-6:],
    }


def _conditional_third_scenario(inputs: FrozenInputs) -> dict[str, Any]:
    case = ordered_cases(inputs)[0]
    trials: list[dict[str, Any]] = []
    for candidate in inputs.oracle["candidate_ids"]:
        for repetition in (1, 2):
            context = 1001 if candidate == "F2" and repetition == 2 else 1000
            trials.append(_record(inputs, TrialSpec(case, candidate, repetition), context_bytes=context))
    thirds = conditional_third_specs(inputs, inputs.oracle["candidate_ids"], trials)
    expected = [TrialSpec(case, "F2", 3).key]
    actual = [spec.key for spec in thirds]
    if actual != expected:
        raise HarnessError("provider-free v15 conditional third is not pair-scoped")
    return {"status": "PASS", "scheduled": actual}


def _critical_instability_third_scenario(inputs: FrozenInputs) -> dict[str, Any]:
    case = next(case for case in inputs.corpus["cases"] if case["class"] == "cross-profile")
    first = _record(inputs, TrialSpec(case, "F2", 1))
    first["semantic_outcome"] = "activate"
    second = _record(inputs, TrialSpec(case, "F2", 2))
    trials = [first, second]
    certificate = qualification_futility_certificate(inputs, "F2", trials)
    thirds = conditional_third_specs(inputs, ["F2"], trials)
    expected = [TrialSpec(case, "F2", 3).key]
    actual = [spec.key for spec in thirds]
    if not certificate["terminal"] or actual != expected:
        raise HarnessError(
            "provider-free v15 critical instability did not retain required pair-scoped r3"
        )
    return {
        "status": "PASS",
        "futility_terminal": certificate["terminal"],
        "scheduled": actual,
    }


def _no_fourth_scenario(inputs: FrozenInputs) -> dict[str, Any]:
    spec = TrialSpec(ordered_cases(inputs)[0], "B2", 4)
    try:
        validate_repetition(inputs, spec)
    except HarnessError:
        return {"status": "PASS"}
    raise HarnessError("provider-free v15 scheduler accepted forbidden repetition r4")


def _nonblocking_futility_scenario(inputs: FrozenInputs) -> dict[str, Any]:
    case = next(case for case in inputs.corpus["cases"] if case["class"] == "cross-profile")
    b2 = _record(inputs, TrialSpec(case, "B2", 1))
    b2["semantic_outcome"] = "activate"
    f2 = {**b2, "candidate_id": "F2"}
    b2_certificate = qualification_futility_certificate(inputs, "B2", [b2])
    f2_certificate = qualification_futility_certificate(inputs, "F2", [f2])
    if b2_certificate["terminal"] or not f2_certificate["terminal"]:
        raise HarnessError("provider-free v15 futility is not B2-nonblocking/candidate-local")
    return {
        "status": "PASS",
        "b2_terminal": b2_certificate["terminal"],
        "f2_terminal": f2_certificate["terminal"],
    }


def _tested_module_hashes() -> dict[str, str]:
    modules = (
        Path(__file__).with_name(name)
        for name in (
            "run_support.py",
            "aggregation.py",
            "scheduling.py",
            "scheduler_simulation.py",
        )
    )
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in modules}


def run_provider_free_scheduler_simulation(inputs: FrozenInputs) -> dict[str, Any]:
    """Exercise frozen v15 scheduling invariants without issuing provider/model calls."""
    return {
        "status": "PASS",
        "execution_epoch": inputs.oracle["execution_epoch"],
        "provider_model_calls_issued": 0,
        "tested_module_sha256": _tested_module_hashes(),
        "scenarios": {
            "base_round_robin": _base_order_scenario(inputs),
            "conditional_third_pair_scoped": _conditional_third_scenario(inputs),
            "critical_instability_still_gets_r3": _critical_instability_third_scenario(inputs),
            "no_fourth_repetition": _no_fourth_scenario(inputs),
            "b2_nonblocking_split_local_futility": _nonblocking_futility_scenario(inputs),
        },
    }
