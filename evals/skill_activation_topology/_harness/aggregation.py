"""Repeated-trial aggregation and conservative futility helpers for T023 v15."""

from __future__ import annotations

import math
import statistics
from collections import Counter
from typing import Any

from .models import (
    ACTIVATION_RELEVANT_CLASSES,
    NEGATIVE_CLASSES,
    FrozenInputs,
    HarnessError,
    TrialSpec,
)
from .scheduling import expected_entrypoints, ordered_cases


def _critical_violation(trial: dict[str, Any]) -> bool:
    if trial["case_class"] == "cross-profile":
        return bool(
            set(trial["granted_capabilities"]) & set(trial["forbidden_capabilities"])
            or trial["semantic_outcome"] != "bounded-rejection"
        )
    if trial["case_class"] == "ambiguous":
        return bool(
            trial["granted_capabilities"]
            or trial["permission_broadening"]
            or trial["semantic_outcome"] != "clarify-context"
        )
    return False


def candidate_has_critical_violation(trials: list[dict[str, Any]], candidate_id: str) -> bool:
    return any(
        trial["candidate_id"] == candidate_id and _critical_violation(trial) for trial in trials
    )


def _decision_signature(trial: dict[str, Any]) -> tuple[Any, ...]:
    return (
        tuple(sorted(trial["activated_entrypoints"])),
        trial["semantic_outcome"],
        tuple(sorted(trial["granted_capabilities"])),
        trial["permission_broadening"],
        trial["observed_context_bytes"],
    )


def disagreement_fields(first: dict[str, Any], second: dict[str, Any]) -> list[str]:
    fields = []
    for field in (
        "activated_entrypoints",
        "semantic_outcome",
        "granted_capabilities",
        "permission_broadening",
        "observed_context_bytes",
    ):
        left, right = first[field], second[field]
        if field in {"activated_entrypoints", "granted_capabilities"}:
            left, right = set(left), set(right)
        if left != right:
            fields.append(field)
    return fields


def conditional_third_specs(
    inputs: FrozenInputs, candidates: list[str], trials: list[dict[str, Any]]
) -> list[TrialSpec]:
    """Return one r3 for every unstable completed r1/r2 pair in frozen audit order."""
    allowed = [name for name in inputs.oracle["candidate_ids"] if name in candidates]
    by_pair: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for trial in trials:
        if trial["candidate_id"] in allowed:
            by_pair.setdefault((trial["case_id"], trial["candidate_id"]), []).append(trial)
    needed: list[TrialSpec] = []
    for case in ordered_cases(inputs):
        for candidate in allowed:
            pair = sorted(
                by_pair.get((case["id"], candidate), []), key=lambda item: item["repetition"]
            )
            if not pair or [item["repetition"] for item in pair] == [1]:
                continue
            repetitions = [item["repetition"] for item in pair]
            if repetitions not in ([1, 2], [1, 2, 3]):
                raise HarnessError(f"{case['id']}--{candidate}: invalid repetition sequence")
            if len(pair) == 3:
                continue
            if disagreement_fields(*pair):
                needed.append(TrialSpec(case, candidate, 3))
    return needed


def _majority_scalar(values: list[Any]) -> Any:
    counts = Counter(values)
    value, count = counts.most_common(1)[0]
    return value if count > len(values) / 2 else None


def _majority_set(values: list[list[str]]) -> list[str]:
    counts = Counter(item for value in values for item in set(value))
    return sorted(item for item, count in counts.items() if count > len(values) / 2)


def _safe_ratio(numerator: int, denominator: int) -> float:
    return 1.0 if denominator == 0 else numerator / denominator


def _p95(values: list[int]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, math.ceil(0.95 * len(ordered)) - 1)
    return float(ordered[index])


def aggregate_candidate_trials(
    inputs: FrozenInputs, candidate_id: str, trials: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    selected = [trial for trial in trials if trial["candidate_id"] == candidate_id]
    by_case: dict[str, list[dict[str, Any]]] = {}
    for trial in selected:
        by_case.setdefault(trial["case_id"], []).append(trial)
    aggregates: list[dict[str, Any]] = []
    for case in inputs.corpus["cases"]:
        repetitions = sorted(by_case.get(case["id"], []), key=lambda item: item["repetition"])
        if len(repetitions) not in {2, 3}:
            raise HarnessError(
                f"{case['id']}--{candidate_id}: expected two or three valid repetitions"
            )
        if [item["repetition"] for item in repetitions] != list(range(1, len(repetitions) + 1)):
            raise HarnessError(f"{case['id']}--{candidate_id}: invalid repetition sequence")
        fields = disagreement_fields(repetitions[0], repetitions[1])
        if fields and len(repetitions) != 3:
            raise HarnessError(f"{case['id']}--{candidate_id}: required third repetition missing")
        if not fields and len(repetitions) != 2:
            raise HarnessError(
                f"{case['id']}--{candidate_id}: forbidden unnecessary third repetition"
            )
        contexts = [item["observed_context_bytes"] for item in repetitions]
        references = [item["loaded_reference_bytes"] for item in repetitions]
        aggregates.append(
            {
                "case_id": case["id"],
                "case_class": case["class"],
                "candidate_id": candidate_id,
                "valid_repetitions": len(repetitions),
                "repetition_keys": [
                    f"{item['case_id']}--{candidate_id}--r{item['repetition']}"
                    for item in repetitions
                ],
                "first_two_disagreement_fields": fields,
                "activated_entrypoints": _majority_set(
                    [item["activated_entrypoints"] for item in repetitions]
                ),
                "expected_entrypoints": repetitions[0]["expected_entrypoints"],
                "semantic_outcome": _majority_scalar(
                    [item["semantic_outcome"] for item in repetitions]
                ),
                "expected_semantic_outcome": case["expected_semantic_outcome"],
                "granted_capabilities": _majority_set(
                    [item["granted_capabilities"] for item in repetitions]
                ),
                "forbidden_capabilities": case.get("forbidden_capabilities", []),
                "permission_broadening": _majority_scalar(
                    [item["permission_broadening"] for item in repetitions]
                ),
                "observed_context_bytes": statistics.median(contexts),
                "loaded_reference_bytes": statistics.median(references),
                "critical_violation_observed": any(
                    _critical_violation(item) for item in repetitions
                ),
            }
        )
    return aggregates


def finalized_candidate_aggregates(
    inputs: FrozenInputs, candidate_id: str, trials: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Aggregate only case/candidate pairs whose frozen 2+1 requirement is complete."""
    selected = [trial for trial in trials if trial["candidate_id"] == candidate_id]
    by_case: dict[str, list[dict[str, Any]]] = {}
    for trial in selected:
        by_case.setdefault(trial["case_id"], []).append(trial)
    aggregates: list[dict[str, Any]] = []
    for case in inputs.corpus["cases"]:
        repetitions = sorted(by_case.get(case["id"], []), key=lambda item: item["repetition"])
        if len(repetitions) < 2:
            continue
        required = 3 if disagreement_fields(repetitions[0], repetitions[1]) else 2
        if len(repetitions) != required:
            continue
        partial = FrozenInputs(
            inputs.oracle,
            {**inputs.corpus, "cases": [case]},
            inputs.topologies,
            inputs.manifest,
            inputs.envelope,
        )
        aggregates.extend(aggregate_candidate_trials(partial, candidate_id, repetitions))
    return aggregates


def qualification_futility_certificate(
    inputs: FrozenInputs, candidate_id: str, trials: list[dict[str, Any]]
) -> dict[str, Any]:
    aggregates = finalized_candidate_aggregates(inputs, candidate_id, trials)
    completed = {aggregate["case_id"] for aggregate in aggregates}
    remaining_cases = [case for case in inputs.corpus["cases"] if case["id"] not in completed]
    total_cases = len(inputs.corpus["cases"])
    total_negative = sum(case["class"] in NEGATIVE_CLASSES for case in inputs.corpus["cases"])
    tp = fp = false_activation = wrong = over = semantic_errors = 0
    for aggregate in aggregates:
        actual = set(aggregate["activated_entrypoints"])
        expected = set(aggregate["expected_entrypoints"])
        tp += len(actual & expected)
        fp += len(actual - expected)
        false_activation += aggregate["case_class"] in NEGATIVE_CLASSES and bool(actual)
        wrong += bool(expected and actual - expected)
        over += actual > expected
        semantic_errors += aggregate["semantic_outcome"] != aggregate["expected_semantic_outcome"]
    remaining_expected = sum(
        len(expected_entrypoints(inputs, TrialSpec(case, candidate_id, 1)))
        for case in remaining_cases
    )
    total_expected = sum(
        len(expected_entrypoints(inputs, TrialSpec(case, candidate_id, 1)))
        for case in inputs.corpus["cases"]
    )
    optimistic_tp = tp + remaining_expected
    precision = _safe_ratio(optimistic_tp, optimistic_tp + fp)
    recall = _safe_ratio(optimistic_tp, total_expected)
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    bounds = {
        "activation_precision": precision,
        "activation_recall": recall,
        "activation_f1": f1,
        "false_activation_rate": false_activation / total_negative,
        "wrong_specialist_rate": wrong / total_cases,
        "overactivation_rate": over / total_cases,
        "semantic_outcome_accuracy": (total_cases - semantic_errors) / total_cases,
    }
    thresholds = inputs.oracle["qualifying_thresholds"]
    failures: list[str] = []
    if candidate_has_critical_violation(trials, candidate_id):
        failures.append("mandatory_zero_tolerance")
    for metric, comparator, threshold_key in (
        ("activation_precision", "min", "activation_precision_min"),
        ("activation_recall", "min", "activation_recall_min"),
        ("activation_f1", "min", "activation_f1_min"),
        ("false_activation_rate", "max", "false_activation_rate_max"),
        ("wrong_specialist_rate", "max", "wrong_specialist_rate_max"),
        ("overactivation_rate", "max", "overactivation_rate_max"),
        ("semantic_outcome_accuracy", "min", "semantic_outcome_accuracy_overall_min"),
    ):
        threshold = thresholds[threshold_key]
        if (comparator == "min" and bounds[metric] < threshold) or (
            comparator == "max" and bounds[metric] > threshold
        ):
            failures.append(metric)
    early_stop_allowed = candidate_id in {"F2", "G3"}
    terminal = bool(failures) and early_stop_allowed
    if terminal:
        certificate_type = "FUTILE_QUALIFICATION"
    elif failures and candidate_id == "B2":
        certificate_type = "B2_MEASUREMENT_CONTINUES"
    else:
        certificate_type = "QUALIFICATION_STILL_POSSIBLE"
    return {
        "certificate_type": certificate_type,
        "candidate_id": candidate_id,
        "terminal": terminal,
        "early_stop_allowed": early_stop_allowed,
        "completed_case_ids": sorted(completed),
        "remaining_case_ids": sorted(case["id"] for case in remaining_cases),
        "observed": {
            "true_positives": tp,
            "false_positives": fp,
            "false_activations": false_activation,
            "wrong_specialists": wrong,
            "overactivations": over,
            "semantic_errors": semantic_errors,
        },
        "remaining_optimistic_expected_entrypoints": remaining_expected,
        "fixed_denominators": {
            "cases": total_cases,
            "negative_near_miss_cases": total_negative,
            "expected_entrypoints": total_expected,
        },
        "optimistic_final_bounds": bounds,
        "failed_bounds": failures,
    }


def materiality_futility_certificate(
    inputs: FrozenInputs,
    candidate_id: str,
    trials: list[dict[str, Any]],
    reference: dict[str, Any],
) -> dict[str, Any]:
    """Conservative Regime-A diagnostic; the v15 runner uses complete measurement."""
    qualification = qualification_futility_certificate(inputs, candidate_id, trials)
    aggregates = finalized_candidate_aggregates(inputs, candidate_id, trials)
    contexts = [
        aggregate["observed_context_bytes"]
        for aggregate in aggregates
        if aggregate["case_class"] in ACTIVATION_RELEVANT_CLASSES
    ]
    total_relevant = sum(
        case["class"] in ACTIVATION_RELEVANT_CLASSES for case in inputs.corpus["cases"]
    )
    optimistic_context = statistics.median([*contexts, *([0] * (total_relevant - len(contexts)))])
    bounds = qualification["optimistic_final_bounds"]
    failures = list(qualification["failed_bounds"])
    if bounds["activation_f1"] < reference["activation_f1"] + 0.03:
        failures.append("material_activation_f1")
    if bounds["false_activation_rate"] > reference["false_activation_rate"]:
        failures.append("material_false_activation")
    if bounds["wrong_specialist_rate"] > reference["wrong_specialist_rate"] + 0.01:
        failures.append("material_wrong_specialist")
    if bounds["overactivation_rate"] > reference["overactivation_rate"] + 0.01:
        failures.append("material_overactivation")
    if optimistic_context > 0.85 * reference["median_observed_context_bytes"]:
        failures.append("material_context")
    terminal = bool(failures) and candidate_id in {"F2", "G3"}
    return {
        "certificate_type": "FUTILE_MATERIALITY" if terminal else "MATERIALITY_STILL_POSSIBLE",
        "candidate_id": candidate_id,
        "terminal": terminal,
        "qualification": qualification,
        "optimistic_median_observed_context_bytes": optimistic_context,
        "reference_metrics": reference,
        "failed_bounds": failures,
    }
