"""Extracted MG1 topology harness implementation."""

from __future__ import annotations

import statistics
from collections import Counter
from typing import Any

from .aggregation import _critical_violation, _p95, _safe_ratio, aggregate_candidate_trials
from .models import (
    ACTIVATION_RELEVANT_CLASSES,
    NEGATIVE_CLASSES,
    FrozenInputs,
    HarnessError,
)


def candidate_qualifies(inputs: FrozenInputs, metrics: dict[str, Any]) -> bool:
    thresholds = inputs.oracle["qualifying_thresholds"]
    threshold_checks = (
        metrics["activation_precision"] >= thresholds["activation_precision_min"],
        metrics["activation_recall"] >= thresholds["activation_recall_min"],
        metrics["activation_f1"] >= thresholds["activation_f1_min"],
        metrics["false_activation_rate"] <= thresholds["false_activation_rate_max"],
        metrics["wrong_specialist_rate"] <= thresholds["wrong_specialist_rate_max"],
        metrics["overactivation_rate"] <= thresholds["overactivation_rate_max"],
        metrics["semantic_outcome_accuracy"] >= thresholds["semantic_outcome_accuracy_overall_min"],
    )
    mandatory = inputs.oracle["mandatory_non_regression"]
    mandatory_checks = (
        metrics["full_deterministic_regression"] == mandatory["full_deterministic_regression"],
        metrics["profile_isolation_regression"] == mandatory["profile_isolation_regression"],
        metrics["consumer_source_independence_regression"]
        == mandatory["consumer_source_independence_regression"],
        metrics["source_distribution_integrity"] == mandatory["source_distribution_integrity"],
        metrics["single_install_feasibility"] == mandatory["single_install_feasibility"],
        metrics["cross_profile_violation_count"] == mandatory["cross_profile_violation_count"],
        metrics["ambiguous_context_permission_broadening_count"]
        == mandatory["ambiguous_context_permission_broadening_count"],
        metrics["semantic_outcome_accuracy_cross_profile_and_ambiguous"]
        == mandatory["semantic_outcome_accuracy_cross_profile_and_ambiguous"],
    )
    return all((*threshold_checks, *mandatory_checks))


def compute_candidate_metrics(
    inputs: FrozenInputs,
    candidate_id: str,
    trials: list[dict[str, Any]],
    deterministic_evidence: dict[str, Any],
) -> dict[str, Any]:
    selected = [trial for trial in trials if trial["candidate_id"] == candidate_id]
    aggregates = aggregate_candidate_trials(inputs, candidate_id, selected)

    tp = fp = fn = 0
    false_activation = wrong_specialist = overactivation = semantic_correct = 0
    negative_trials = 0
    cross_profile_violations = ambiguous_broadenings = 0
    cross_ambiguous_correct = cross_ambiguous_total = 0
    observed_context_bytes: list[int] = []
    loaded_reference_bytes: list[int] = []
    for trial in aggregates:
        actual = set(trial["activated_entrypoints"])
        expected = set(trial["expected_entrypoints"])
        tp += len(actual & expected)
        fp += len(actual - expected)
        fn += len(expected - actual)
        if trial["case_class"] in NEGATIVE_CLASSES:
            negative_trials += 1
            false_activation += bool(actual)
        if expected and actual - expected:
            wrong_specialist += 1
        if actual > expected:
            overactivation += 1
        correct = trial["semantic_outcome"] == trial["expected_semantic_outcome"]
        semantic_correct += correct
        if trial["case_class"] in ACTIVATION_RELEVANT_CLASSES:
            observed_context_bytes.append(trial["observed_context_bytes"])
            loaded_reference_bytes.append(trial["loaded_reference_bytes"])

    critical_trials = [
        trial for trial in selected if trial["case_class"] in {"cross-profile", "ambiguous"}
    ]
    cross_ambiguous_total = len(critical_trials)
    cross_ambiguous_correct = sum(
        trial["semantic_outcome"] == trial["expected_semantic_outcome"] for trial in critical_trials
    )
    cross_profile_violations = sum(
        trial["case_class"] == "cross-profile" and _critical_violation(trial) for trial in selected
    )
    ambiguous_broadenings = sum(
        trial["case_class"] == "ambiguous" and _critical_violation(trial) for trial in selected
    )

    precision = _safe_ratio(tp, tp + fp)
    recall = _safe_ratio(tp, tp + fn)
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    mandatory = inputs.oracle["mandatory_non_regression"]
    return {
        "candidate_id": candidate_id,
        "case_count": len(aggregates),
        "valid_repetition_count": len(selected),
        "activation_precision": precision,
        "activation_recall": recall,
        "activation_f1": f1,
        "false_activation_rate": _safe_ratio(false_activation, negative_trials),
        "wrong_specialist_rate": wrong_specialist / len(aggregates),
        "overactivation_rate": overactivation / len(aggregates),
        "semantic_outcome_accuracy": semantic_correct / len(aggregates),
        "semantic_outcome_accuracy_cross_profile_and_ambiguous": _safe_ratio(
            cross_ambiguous_correct, cross_ambiguous_total
        ),
        "cross_profile_violation_count": cross_profile_violations,
        "ambiguous_context_permission_broadening_count": ambiguous_broadenings,
        "median_observed_context_bytes": statistics.median(observed_context_bytes),
        "p95_observed_context_bytes": _p95(observed_context_bytes),
        "median_loaded_reference_bytes": statistics.median(loaded_reference_bytes),
        "p95_loaded_reference_bytes": _p95(loaded_reference_bytes),
        "first_two_disagreement_count": sum(
            bool(item["first_two_disagreement_fields"]) for item in aggregates
        ),
        "first_two_disagreement_rate": sum(
            bool(item["first_two_disagreement_fields"]) for item in aggregates
        )
        / len(aggregates),
        "conditional_third_repetition_count": sum(
            item["valid_repetitions"] == 3 for item in aggregates
        ),
        "valid_repetitions_per_case": dict(
            sorted(
                (str(count), frequency)
                for count, frequency in Counter(
                    item["valid_repetitions"] for item in aggregates
                ).items()
            )
        ),
        "single_install_feasibility": deterministic_evidence["candidates"][candidate_id][
            "single_install_feasibility"
        ],
        "source_distribution_integrity": deterministic_evidence["candidates"][candidate_id][
            "source_distribution_integrity"
        ],
        "full_deterministic_regression": deterministic_evidence["full_deterministic_regression"],
        "profile_isolation_regression": deterministic_evidence["profile_isolation_regression"],
        "consumer_source_independence_regression": deterministic_evidence[
            "consumer_source_independence_regression"
        ],
        "mandatory_expected": mandatory,
    }


def select_single_family_reference(
    inputs: FrozenInputs, metrics_by_candidate: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    if set(metrics_by_candidate) != {"B0", "B1"}:
        raise HarnessError("reference selection requires exactly B0 and B1 metrics")
    qualifying = {
        candidate: candidate_qualifies(inputs, metrics_by_candidate[candidate])
        for candidate in ("B0", "B1")
    }
    if not any(qualifying.values()):
        return {
            "status": "BLOCKED",
            "single_family_reference": None,
            "reason": "neither B0 nor B1 qualifies",
            "qualifying": qualifying,
        }
    if all(qualifying.values()):
        b0, b1 = metrics_by_candidate["B0"], metrics_by_candidate["B1"]
        b1_reference = (
            b1["activation_f1"] >= b0["activation_f1"] - 0.01
            and b1["false_activation_rate"] <= b0["false_activation_rate"] + 0.01
            and b1["median_observed_context_bytes"] <= 0.80 * b0["median_observed_context_bytes"]
        )
        reference_id = "B1" if b1_reference else "B0"
    else:
        reference_id = "B0" if qualifying["B0"] else "B1"
    return {
        "status": "REFERENCE_SELECTED",
        "single_family_reference": reference_id,
        "qualifying": qualifying,
    }


def select_from_cost_bounded_metrics(
    inputs: FrozenInputs,
    reference_id: str,
    metrics_by_candidate: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Apply unchanged challenger materiality/tie-breaks to completed survivors."""
    reference = metrics_by_candidate[reference_id]
    material = []
    for candidate in ("F2", "G3"):
        metrics = metrics_by_candidate.get(candidate)
        if metrics and (
            candidate_qualifies(inputs, metrics)
            and metrics["activation_f1"] >= reference["activation_f1"] + 0.03
            and metrics["median_observed_context_bytes"]
            <= 0.85 * reference["median_observed_context_bytes"]
            and metrics["false_activation_rate"] <= reference["false_activation_rate"]
            and metrics["wrong_specialist_rate"] <= reference["wrong_specialist_rate"] + 0.01
            and metrics["overactivation_rate"] <= reference["overactivation_rate"] + 0.01
        ):
            material.append(candidate)
    if not material:
        selected = reference_id
    elif len(material) == 1:
        selected = material[0]
    else:
        f2, g3 = metrics_by_candidate["F2"], metrics_by_candidate["G3"]
        if abs(f2["activation_f1"] - g3["activation_f1"]) > 0.005:
            selected = max(material, key=lambda name: metrics_by_candidate[name]["activation_f1"])
        elif abs(f2["false_activation_rate"] - g3["false_activation_rate"]) > 0.01:
            selected = min(
                material, key=lambda name: metrics_by_candidate[name]["false_activation_rate"]
            )
        else:
            f2_load, g3_load = (
                f2["median_observed_context_bytes"],
                g3["median_observed_context_bytes"],
            )
            if abs(f2_load - g3_load) / max(f2_load, g3_load, 1) > 0.05:
                selected = min(
                    material,
                    key=lambda name: metrics_by_candidate[name]["median_observed_context_bytes"],
                )
            else:
                selected = min(
                    material,
                    key=lambda name: (
                        len(inputs.topologies["candidates"][name]["entrypoints"]),
                        name != "F2",
                    ),
                )
    return {
        "status": "SELECTED",
        "selected_candidate": selected,
        "single_family_reference": reference_id,
        "material_split_candidates": material,
        "qualifying": {
            candidate: candidate_qualifies(inputs, metrics)
            for candidate, metrics in metrics_by_candidate.items()
        },
    }


def apply_selection_rule(
    inputs: FrozenInputs, metrics_by_candidate: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    if set(metrics_by_candidate) != set(inputs.oracle["candidate_ids"]):
        raise HarnessError("final selection requires complete B0/B1/F2/G3 metrics")
    qualifying = {
        candidate: candidate_qualifies(inputs, metrics)
        for candidate, metrics in metrics_by_candidate.items()
    }
    reference_result = select_single_family_reference(
        inputs, {candidate: metrics_by_candidate[candidate] for candidate in ("B0", "B1")}
    )
    if reference_result["status"] == "BLOCKED":
        return {
            "status": "BLOCKED",
            "selected_candidate": None,
            "reason": reference_result["reason"],
            "qualifying": qualifying,
        }
    reference_id = reference_result["single_family_reference"]

    reference = metrics_by_candidate[reference_id]
    material: list[str] = []
    for candidate in ("F2", "G3"):
        metrics = metrics_by_candidate[candidate]
        if (
            qualifying[candidate]
            and metrics["activation_f1"] >= reference["activation_f1"] + 0.03
            and metrics["median_observed_context_bytes"]
            <= 0.85 * reference["median_observed_context_bytes"]
            and metrics["false_activation_rate"] <= reference["false_activation_rate"]
            and metrics["wrong_specialist_rate"] <= reference["wrong_specialist_rate"] + 0.01
            and metrics["overactivation_rate"] <= reference["overactivation_rate"] + 0.01
        ):
            material.append(candidate)

    if not material:
        selected = reference_id
    elif len(material) == 1:
        selected = material[0]
    else:
        f2 = metrics_by_candidate["F2"]
        g3 = metrics_by_candidate["G3"]
        if abs(f2["activation_f1"] - g3["activation_f1"]) > 0.005:
            selected = max(material, key=lambda name: metrics_by_candidate[name]["activation_f1"])
        elif abs(f2["false_activation_rate"] - g3["false_activation_rate"]) > 0.01:
            selected = min(
                material, key=lambda name: metrics_by_candidate[name]["false_activation_rate"]
            )
        else:
            f2_load = f2["median_observed_context_bytes"]
            g3_load = g3["median_observed_context_bytes"]
            denominator = max(f2_load, g3_load, 1)
            if abs(f2_load - g3_load) / denominator > 0.05:
                selected = min(
                    material,
                    key=lambda name: metrics_by_candidate[name]["median_observed_context_bytes"],
                )
            else:
                entrypoint_counts = {
                    name: len(inputs.topologies["candidates"][name]["entrypoints"])
                    for name in material
                }
                minimum = min(entrypoint_counts.values())
                tied = [name for name in material if entrypoint_counts[name] == minimum]
                selected = "F2" if "F2" in tied else tied[0]

    return {
        "status": "SELECTED",
        "selected_candidate": selected,
        "single_family_reference": reference_id,
        "material_split_challengers": material,
        "qualifying": qualifying,
        "selection_rule": inputs.oracle["oracle_id"],
    }
