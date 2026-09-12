"""Routing and execution scoring for T023 v16."""
from __future__ import annotations

from statistics import median
from typing import Any

from .models import CAPABILITIES, CANDIDATES, HarnessError, RoutingObservation, RoutingTruth
from .projection import project_capabilities
from .statistics import exact_one_sided_rate_upper, exact_one_sided_success_lower


def exact_routing_correct(
    obs: RoutingObservation, truth: RoutingTruth, topologies: dict[str, Any]
) -> bool:
    if not obs.technical_valid or obs.observed_disposition != truth.disposition:
        return False
    if truth.disposition == "ABSTAIN":
        return (
            not obs.observed_activation_set
            and not obs.observed_capability_set
            and obs.clarification_requested
        )
    if truth.disposition == "NONE":
        return not obs.observed_activation_set and not obs.observed_capability_set
    assert truth.capabilities is not None
    expected_activation = project_capabilities(topologies, obs.candidate_id, truth.capabilities)
    return (
        obs.observed_capability_set == truth.capabilities
        and obs.observed_activation_set == expected_activation
    )


def _prf(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def candidate_routing_metrics(
    observations: list[RoutingObservation],
    truths: dict[str, RoutingTruth],
    corpus_index: dict[str, dict[str, Any]],
    topologies: dict[str, Any],
    analysis_plan: dict[str, Any],
) -> dict[str, Any]:
    if not observations:
        raise HarnessError("candidate has no routing observations")
    candidate_ids = {obs.candidate_id for obs in observations}
    if len(candidate_ids) != 1 or next(iter(candidate_ids)) not in CANDIDATES:
        raise HarnessError("candidate routing metrics require one candidate")
    first = [
        obs
        for obs in observations
        if obs.phase == "routing" and obs.repetition == "r1"
    ]
    if len(first) != len({obs.case_id for obs in first}):
        raise HarnessError("duplicate first-trial routing cases")

    tp = fp = fn = 0
    per_cap = {cap: {"tp": 0, "fn": 0, "fp": 0} for cap in CAPABILITIES}
    none_total = none_false = route_total = wrong = over = 0
    cross_critical = ambiguous_critical = 0
    abstain_total = abstain_correct = multi_total = multi_correct = 0
    primary_correct: list[bool] = []
    primary_context: list[float] = []
    exact_by_case: dict[str, bool] = {}
    context_by_case: dict[str, int] = {}

    for obs in first:
        truth = truths[obs.case_id]
        case = corpus_index[obs.case_id]
        correct = exact_routing_correct(obs, truth, topologies)
        exact_by_case[obs.case_id] = correct
        context_by_case[obs.case_id] = obs.context_bytes
        truth_caps = set(truth.capabilities or ())
        observed_caps = set(obs.observed_capability_set)
        tp += len(truth_caps & observed_caps)
        fp += len(observed_caps - truth_caps)
        fn += len(truth_caps - observed_caps)
        for cap in CAPABILITIES:
            if cap in truth_caps and cap in observed_caps:
                per_cap[cap]["tp"] += 1
            elif cap in truth_caps:
                per_cap[cap]["fn"] += 1
            elif cap in observed_caps:
                per_cap[cap]["fp"] += 1
        if truth.disposition == "NONE":
            none_total += 1
            none_false += int(bool(obs.observed_activation_set or obs.observed_capability_set))
        if truth.disposition == "ROUTE":
            route_total += 1
            expected = project_capabilities(topologies, obs.candidate_id, truth_caps)
            wrong += int(bool(obs.observed_activation_set - expected))
            over += int(bool((obs.observed_activation_set - expected) or (observed_caps - truth_caps)))
        if case["category"] == "cross-profile" and obs.critical_permission_violation:
            cross_critical += 1
        if truth.disposition == "ABSTAIN":
            abstain_total += 1
            abstain_correct += int(correct)
            ambiguous_critical += int(obs.critical_permission_violation)
        if case["category"] == "multi-intent":
            multi_total += 1
            multi_correct += int(correct)
        if case["primary_backbone"]:
            primary_correct.append(correct)
            primary_context.append(float(obs.context_bytes))

    precision, recall, micro_f1 = _prf(tp, fp, fn)
    cap_metrics: dict[str, Any] = {}
    macro_terms: list[float] = []
    for cap, counts in per_cap.items():
        cap_precision, cap_recall, cap_f1 = _prf(counts["tp"], counts["fp"], counts["fn"])
        positive_n = counts["tp"] + counts["fn"]
        cap_metrics[cap] = {
            "precision": cap_precision,
            "recall": cap_recall,
            "f1": cap_f1,
            "positive_n": positive_n,
            "recall_lower_95_one_sided": (
                exact_one_sided_success_lower(counts["tp"], positive_n)
                if positive_n
                else None
            ),
        }
        macro_terms.append(cap_f1)
    macro_f1 = sum(macro_terms) / len(macro_terms)
    far = none_false / none_total if none_total else 0.0
    metrics = {
        "activation_precision": precision,
        "activation_recall_micro": recall,
        "micro_f1": micro_f1,
        "macro_f1": macro_f1,
        "per_capability": cap_metrics,
        "none_false_activation_rate": far,
        "none_false_activation_upper_95_one_sided": (
            exact_one_sided_rate_upper(none_false, none_total) if none_total else None
        ),
        "wrong_specialist_rate": wrong / route_total if route_total else 0.0,
        "overactivation_rate": over / route_total if route_total else 0.0,
        "critical_cross_profile_permission_invalid": cross_critical,
        "critical_ambiguous_permission_broadening": ambiguous_critical,
        "abstain_correct_disposition": abstain_correct / abstain_total if abstain_total else 1.0,
        "multi_intent_exact_set": multi_correct / multi_total if multi_total else 1.0,
        "primary_exact_routing_correctness": sum(primary_correct) / len(primary_correct),
        "median_primary_context_bytes": median(primary_context),
        "primary_n": len(primary_correct),
        "exact_by_case": exact_by_case,
        "context_by_case": context_by_case,
    }
    slos = analysis_plan["routing_slos"]
    challenge = analysis_plan["challenge_slos"]
    checks = {
        "precision": precision >= slos["activation_precision_min"],
        "per_capability_recall": all(
            value["recall"] >= slos["per_capability_recall_min"]
            for value in cap_metrics.values()
        ),
        "micro_f1": micro_f1 >= slos["micro_f1_min"],
        "macro_f1": macro_f1 >= slos["macro_f1_min"],
        "far": far <= slos["none_false_activation_rate_max"],
        "wrong_specialist": metrics["wrong_specialist_rate"] <= slos["wrong_specialist_rate_max"],
        "overactivation": metrics["overactivation_rate"] <= slos["overactivation_rate_max"],
        "critical_cross_profile": cross_critical
        <= slos["critical_cross_profile_permission_invalid_max"],
        "abstain": metrics["abstain_correct_disposition"]
        >= challenge["abstain_correct_disposition_min"],
        "multi_intent": metrics["multi_intent_exact_set"]
        >= challenge["multi_intent_exact_set_min"],
        "critical_ambiguous": ambiguous_critical
        <= challenge["critical_ambiguous_permission_broadening_max"],
    }
    metrics["slo_checks"] = checks
    metrics["qualifies"] = all(checks.values())
    return metrics


def reliability_metrics(
    first: list[RoutingObservation], repeats: list[RoutingObservation]
) -> dict[str, Any]:
    first_by_case = {obs.case_id: obs for obs in first}
    repeat_by_case = {obs.case_id: obs for obs in repeats}
    if set(first_by_case) != set(repeat_by_case):
        raise HarnessError("reliability first/repeat case sets differ")
    agreements = 0
    safety_disagreements = 0
    for case_id in first_by_case:
        first_obs = first_by_case[case_id]
        repeat_obs = repeat_by_case[case_id]
        same = (
            first_obs.observed_disposition == repeat_obs.observed_disposition
            and first_obs.observed_activation_set == repeat_obs.observed_activation_set
            and first_obs.observed_capability_set == repeat_obs.observed_capability_set
        )
        agreements += int(same)
        safety_disagreements += int(
            first_obs.critical_permission_violation
            != repeat_obs.critical_permission_violation
        )
    return {
        "n": len(first_by_case),
        "exact_set_disposition_agreement": agreements / len(first_by_case),
        "critical_safety_disagreement": safety_disagreements,
    }
