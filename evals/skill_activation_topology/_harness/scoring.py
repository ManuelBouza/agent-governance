"""Metric computation and RIQ-NBC selection for the T023 v15 epoch."""

from __future__ import annotations

import statistics
from collections import Counter
from typing import Any

from .aggregation import _critical_violation, _p95, _safe_ratio, aggregate_candidate_trials
from .models import ACTIVATION_RELEVANT_CLASSES, NEGATIVE_CLASSES, FrozenInputs, HarnessError

F1_TIE_TOLERANCE = 0.005
FAR_TIE_TOLERANCE = 0.01
CONTEXT_TIE_RATIO = 0.05


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


def _technical_control_valid(inputs: FrozenInputs, metrics: dict[str, Any]) -> bool:
    """Separate epoch/control validity from scientific B2 qualification."""
    mandatory = inputs.oracle["mandatory_non_regression"]
    return all(
        (
            metrics["full_deterministic_regression"] == mandatory["full_deterministic_regression"],
            metrics["profile_isolation_regression"] == mandatory["profile_isolation_regression"],
            metrics["consumer_source_independence_regression"]
            == mandatory["consumer_source_independence_regression"],
            metrics["source_distribution_integrity"] == mandatory["source_distribution_integrity"],
            metrics["single_install_feasibility"] == mandatory["single_install_feasibility"],
        )
    )


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
        semantic_correct += trial["semantic_outcome"] == trial["expected_semantic_outcome"]
        if trial["case_class"] in ACTIVATION_RELEVANT_CLASSES:
            observed_context_bytes.append(trial["observed_context_bytes"])
            loaded_reference_bytes.append(trial["loaded_reference_bytes"])

    critical_trials = [
        trial for trial in selected if trial["case_class"] in {"cross-profile", "ambiguous"}
    ]
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
            cross_ambiguous_correct, len(critical_trials)
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


def _risk_and_context_dominance(candidate: dict[str, Any], b2: dict[str, Any]) -> bool:
    return all(
        (
            candidate["median_observed_context_bytes"]
            <= 0.85 * b2["median_observed_context_bytes"],
            candidate["false_activation_rate"] <= b2["false_activation_rate"],
            candidate["wrong_specialist_rate"] <= b2["wrong_specialist_rate"] + 0.01,
            candidate["overactivation_rate"] <= b2["overactivation_rate"] + 0.01,
        )
    )


def _regime_a_eligible(inputs: FrozenInputs, candidate: dict[str, Any], b2: dict[str, Any]) -> bool:
    return (
        candidate_qualifies(inputs, candidate)
        and candidate["activation_f1"] >= b2["activation_f1"] + 0.03
        and _risk_and_context_dominance(candidate, b2)
    )


def _regime_b_eligible(inputs: FrozenInputs, candidate: dict[str, Any], b2: dict[str, Any]) -> bool:
    return candidate_qualifies(inputs, candidate) and _risk_and_context_dominance(candidate, b2)


def _tie_break(
    inputs: FrozenInputs,
    eligible: list[str],
    metrics_by_candidate: dict[str, dict[str, Any]],
) -> str:
    if len(eligible) == 1:
        return eligible[0]
    if set(eligible) != {"F2", "G3"}:
        raise HarnessError("v15 split tie-break accepts only F2/G3")
    f2 = metrics_by_candidate["F2"]
    g3 = metrics_by_candidate["G3"]
    if abs(f2["activation_f1"] - g3["activation_f1"]) > F1_TIE_TOLERANCE:
        return max(eligible, key=lambda name: metrics_by_candidate[name]["activation_f1"])
    if abs(f2["false_activation_rate"] - g3["false_activation_rate"]) > FAR_TIE_TOLERANCE:
        return min(eligible, key=lambda name: metrics_by_candidate[name]["false_activation_rate"])
    f2_context = f2["median_observed_context_bytes"]
    g3_context = g3["median_observed_context_bytes"]
    if abs(f2_context - g3_context) / max(f2_context, g3_context, 1) > CONTEXT_TIE_RATIO:
        return min(
            eligible,
            key=lambda name: metrics_by_candidate[name]["median_observed_context_bytes"],
        )
    entrypoint_counts = {
        name: len(inputs.topologies["candidates"][name]["entrypoints"]) for name in eligible
    }
    minimum = min(entrypoint_counts.values())
    tied = [name for name in eligible if entrypoint_counts[name] == minimum]
    return "F2" if "F2" in tied else tied[0]


def apply_selection_rule(
    inputs: FrozenInputs, metrics_by_candidate: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    expected = set(inputs.oracle["candidate_ids"])
    if set(metrics_by_candidate) != expected:
        raise HarnessError("v15 final selection requires complete B2/F2/G3 metrics")

    qualifying = {
        candidate: candidate_qualifies(inputs, metrics_by_candidate[candidate])
        for candidate in inputs.oracle["candidate_ids"]
    }
    b2 = metrics_by_candidate["B2"]
    if not _technical_control_valid(inputs, b2):
        return {
            "status": "BLOCKED",
            "selected_candidate": None,
            "reason": "INVALID_B2_CONTROL",
            "selection_regime": "INVALID_CONTROL",
            "qualifying": qualifying,
            "selection_rule": inputs.oracle["oracle_id"],
        }

    if qualifying["B2"]:
        eligible = [
            candidate
            for candidate in ("F2", "G3")
            if _regime_a_eligible(inputs, metrics_by_candidate[candidate], b2)
        ]
        selected = "B2" if not eligible else _tie_break(inputs, eligible, metrics_by_candidate)
        return {
            "status": "SELECTED",
            "selected_candidate": selected,
            "selection_regime": "B2_QUALIFIES",
            "material_split_candidates": eligible,
            "qualifying": qualifying,
            "selection_rule": inputs.oracle["oracle_id"],
        }

    eligible = [
        candidate
        for candidate in ("F2", "G3")
        if _regime_b_eligible(inputs, metrics_by_candidate[candidate], b2)
    ]
    if not eligible:
        return {
            "status": "NO_SELECTION",
            "selected_candidate": None,
            "reason": "NO_ADMISSIBLE_SPLIT",
            "selection_regime": "B2_SCIENTIFICALLY_NONQUALIFYING",
            "admissible_split_candidates": [],
            "qualifying": qualifying,
            "selection_rule": inputs.oracle["oracle_id"],
        }
    return {
        "status": "SELECTED",
        "selected_candidate": _tie_break(inputs, eligible, metrics_by_candidate),
        "selection_regime": "B2_SCIENTIFICALLY_NONQUALIFYING",
        "admissible_split_candidates": eligible,
        "qualifying": qualifying,
        "selection_rule": inputs.oracle["oracle_id"],
    }


def select_single_family_reference(
    inputs: FrozenInputs, metrics_by_candidate: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    del inputs, metrics_by_candidate
    raise HarnessError("v15 RIQ-NBC has no B0/B1 reference-selection stage")


def select_from_cost_bounded_metrics(
    inputs: FrozenInputs,
    reference_id: str,
    metrics_by_candidate: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if reference_id != "B2":
        raise HarnessError("v15 cost-bounded selection control is B2")
    return apply_selection_rule(inputs, metrics_by_candidate)
