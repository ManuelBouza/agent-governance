"""Frozen routing-finalist and end-to-end selection analysis."""
from __future__ import annotations

from statistics import median
from typing import Any

from .models import CANDIDATES, HarnessError, RoutingObservation, RoutingTruth
from .scoring import candidate_routing_metrics, reliability_metrics
from .statistics import exact_mcnemar_pvalue, holm_adjust, paired_bootstrap_delta


def _primary_ids(corpus: dict[str, Any]) -> list[str]:
    return [case["id"] for case in corpus["routing_cases"] if case["primary_backbone"]]


def _paired_vectors(
    metrics_a: dict[str, Any],
    metrics_b: dict[str, Any],
    ids: list[str],
    field: str,
) -> tuple[list[float], list[float]]:
    return (
        [float(metrics_a[field][case_id]) for case_id in ids],
        [float(metrics_b[field][case_id]) for case_id in ids],
    )


def _compare(
    a_id: str,
    b_id: str,
    metrics: dict[str, dict[str, Any]],
    ids: list[str],
    plan: dict[str, Any],
    seed_offset: int = 0,
) -> dict[str, Any]:
    metrics_a, metrics_b = metrics[a_id], metrics[b_id]
    correct_a, correct_b = _paired_vectors(metrics_a, metrics_b, ids, "exact_by_case")
    context_a, context_b = _paired_vectors(metrics_a, metrics_b, ids, "context_by_case")
    seed = int(plan["paired_comparison"]["bootstrap_seed"]) + seed_offset
    resamples = int(plan["paired_comparison"]["bootstrap_resamples"])
    quality = paired_bootstrap_delta(
        correct_a, correct_b, seed=seed, resamples=resamples
    )
    context = paired_bootstrap_delta(
        context_a,
        context_b,
        statistic=median,
        seed=seed + 1,
        resamples=resamples,
    )
    return {
        "a": a_id,
        "b": b_id,
        "exact_quality": quality,
        "mcnemar_p": exact_mcnemar_pvalue(
            [bool(value) for value in correct_a],
            [bool(value) for value in correct_b],
        ),
        "median_context_delta_bytes": context,
        "median_context_ratio": (
            metrics_a["median_primary_context_bytes"]
            / metrics_b["median_primary_context_bytes"]
            if metrics_b["median_primary_context_bytes"]
            else 0.0
        ),
    }


def _split_dominates(comparison: dict[str, Any]) -> bool:
    quality = comparison["exact_quality"]
    context = comparison["median_context_delta_bytes"]
    nonworse = quality["lower"] >= 0.0 and context["upper"] <= 0.0
    strict = quality["delta"] > 0.0 or context["delta"] < 0.0
    return nonworse and strict


def routing_analysis(
    observations: list[RoutingObservation],
    truths: dict[str, RoutingTruth],
    corpus: dict[str, Any],
    topologies: dict[str, Any],
    plan: dict[str, Any],
) -> dict[str, Any]:
    index = {case["id"]: case for case in corpus["routing_cases"]}
    metrics: dict[str, dict[str, Any]] = {}
    reliability: dict[str, dict[str, Any] | None] = {}
    for candidate in CANDIDATES:
        candidate_obs = [obs for obs in observations if obs.candidate_id == candidate]
        metrics[candidate] = candidate_routing_metrics(
            candidate_obs, truths, index, topologies, plan
        )
        repeats = [obs for obs in candidate_obs if obs.phase == "reliability"]
        if repeats:
            repeat_ids = {obs.case_id for obs in repeats}
            first = [
                obs
                for obs in candidate_obs
                if obs.phase == "routing"
                and obs.repetition == "r1"
                and obs.case_id in repeat_ids
            ]
            reliability[candidate] = reliability_metrics(first, repeats)
            rslos = plan["reliability_slos"]
            reliability[candidate]["passes"] = (
                reliability[candidate]["exact_set_disposition_agreement"]
                >= rslos["exact_set_disposition_agreement_min"]
                and reliability[candidate]["critical_safety_disagreement"]
                <= rslos["critical_safety_disagreement_max"]
            )
            metrics[candidate]["slo_checks"]["reliability"] = reliability[candidate][
                "passes"
            ]
            metrics[candidate]["qualifies"] = (
                metrics[candidate]["qualifies"] and reliability[candidate]["passes"]
            )
        else:
            reliability[candidate] = None
            metrics[candidate]["slo_checks"]["reliability"] = False
            metrics[candidate]["qualifies"] = False

    ids = _primary_ids(corpus)
    comparisons: dict[str, dict[str, Any]] = {}
    pvalues: dict[str, float] = {}
    for offset, (a_id, b_id) in enumerate(
        (("F2", "B2"), ("G3", "B2"), ("F2", "G3"))
    ):
        comparison = _compare(a_id, b_id, metrics, ids, plan, seed_offset=offset * 10)
        key = f"{a_id}_vs_{b_id}"
        comparisons[key] = comparison
        pvalues[key] = comparison["mcnemar_p"]
    adjusted = holm_adjust(pvalues)
    for key, value in adjusted.items():
        comparisons[key]["holm"] = value

    b2_qualifies = metrics["B2"]["qualifies"]
    eligible_splits: list[str] = []
    margin = float(plan["split_vs_b2"]["routing_quality_noninferiority_margin"])
    ratio = float(plan["split_vs_b2"]["median_context_ratio_max"])
    if b2_qualifies:
        for split in ("F2", "G3"):
            comparison = comparisons[f"{split}_vs_B2"]
            if (
                metrics[split]["qualifies"]
                and comparison["exact_quality"]["lower"] >= margin
                and comparison["median_context_ratio"] <= ratio
                and comparison["median_context_delta_bytes"]["upper"] <= 0.0
            ):
                eligible_splits.append(split)
        if not eligible_splits:
            finalists = ["B2"]
            status = "FINALISTS_READY"
        elif len(eligible_splits) == 1:
            finalists = ["B2", eligible_splits[0]]
            status = "FINALISTS_READY"
        else:
            f2_vs_g3 = comparisons["F2_vs_G3"]
            if _split_dominates(f2_vs_g3):
                finalists = ["B2", "F2"]
                status = "FINALISTS_READY"
            else:
                inverse = {
                    "exact_quality": {
                        "lower": -f2_vs_g3["exact_quality"]["upper"],
                        "upper": -f2_vs_g3["exact_quality"]["lower"],
                        "delta": -f2_vs_g3["exact_quality"]["delta"],
                    },
                    "median_context_delta_bytes": {
                        "lower": -f2_vs_g3["median_context_delta_bytes"]["upper"],
                        "upper": -f2_vs_g3["median_context_delta_bytes"]["lower"],
                        "delta": -f2_vs_g3["median_context_delta_bytes"]["delta"],
                    },
                }
                if _split_dominates(inverse):
                    finalists = ["B2", "G3"]
                    status = "FINALISTS_READY"
                else:
                    finalists = []
                    status = "NO_TOPOLOGY_SELECTED_UNRESOLVED_SPLIT_CHALLENGER"
    else:
        finalists = [
            candidate
            for candidate in ("F2", "G3")
            if metrics[candidate]["qualifies"]
        ]
        status = (
            "FINALISTS_READY"
            if finalists
            else "NO_TOPOLOGY_SELECTED_NO_ROUTING_QUALIFIER"
        )
    return {
        "status": status,
        "metrics": metrics,
        "reliability": reliability,
        "comparisons": comparisons,
        "eligible_splits": eligible_splits,
        "finalists": finalists,
    }


def e2e_analysis(
    observations: list[RoutingObservation],
    routing_result: dict[str, Any],
    truths: dict[str, RoutingTruth],
    corpus: dict[str, Any],
    plan: dict[str, Any],
) -> dict[str, Any]:
    finalists = routing_result["finalists"]
    if not finalists:
        return {
            "status": "NO_TOPOLOGY_SELECTED",
            "selected": None,
            "reason": "routing produced no finalists",
        }
    reserve_ids = {case["id"] for case in corpus["e2e_reserve"]}
    metrics: dict[str, dict[str, Any]] = {}
    for candidate in finalists:
        candidate_obs = [
            obs
            for obs in observations
            if obs.phase == "e2e"
            and obs.candidate_id == candidate
            and obs.case_id in reserve_ids
        ]
        if len(candidate_obs) != len(reserve_ids):
            raise HarnessError(f"{candidate}: incomplete end-to-end reserve")
        routed = [
            obs
            for obs in candidate_obs
            if obs.observed_disposition == truths[obs.case_id].disposition
        ]
        conditional = [obs for obs in routed if obs.task_success is not None]
        conditional_success = (
            sum(bool(obs.task_success) for obs in conditional) / len(conditional)
            if conditional
            else 0.0
        )
        end_to_end_success = sum(bool(obs.task_success) for obs in candidate_obs) / len(
            candidate_obs
        )
        critical = sum(obs.critical_permission_violation for obs in candidate_obs)
        slos = plan["e2e_slos"]
        passes = (
            conditional_success >= slos["conditional_semantic_accuracy_min"]
            and end_to_end_success >= slos["end_to_end_task_success_min"]
            and critical <= slos["critical_cross_profile_permission_violations_max"]
        )
        metrics[candidate] = {
            "conditional_execution_success": conditional_success,
            "end_to_end_task_success": end_to_end_success,
            "critical_violations": critical,
            "passes": passes,
            "success_by_case": {
                obs.case_id: bool(obs.task_success) for obs in candidate_obs
            },
        }
    passing = [candidate for candidate in finalists if metrics[candidate]["passes"]]
    if not passing:
        return {
            "status": "NO_TOPOLOGY_SELECTED",
            "selected": None,
            "metrics": metrics,
            "reason": "no finalist passed end-to-end SLOs",
        }
    if len(passing) == 1:
        return {"status": "SELECTED", "selected": passing[0], "metrics": metrics}
    if "B2" in passing:
        split = next(candidate for candidate in passing if candidate != "B2")
        ids = sorted(reserve_ids)
        split_success = [float(metrics[split]["success_by_case"][case_id]) for case_id in ids]
        b2_success = [float(metrics["B2"]["success_by_case"][case_id]) for case_id in ids]
        interval = paired_bootstrap_delta(
            split_success,
            b2_success,
            seed=int(plan["paired_comparison"]["bootstrap_seed"]) + 500,
            resamples=int(plan["paired_comparison"]["bootstrap_resamples"]),
        )
        margin = float(plan["final_selection"]["execution_quality_noninferiority_margin"])
        retains_context = (
            routing_result["comparisons"][f"{split}_vs_B2"]["median_context_ratio"]
            <= plan["split_vs_b2"]["median_context_ratio_max"]
        )
        if interval["lower"] >= margin and retains_context:
            return {
                "status": "SELECTED",
                "selected": split,
                "metrics": metrics,
                "execution_comparison": interval,
            }
        return {
            "status": "SELECTED",
            "selected": "B2",
            "metrics": metrics,
            "execution_comparison": interval,
        }

    ids = sorted(reserve_ids)
    f2_success = [float(metrics["F2"]["success_by_case"][case_id]) for case_id in ids]
    g3_success = [float(metrics["G3"]["success_by_case"][case_id]) for case_id in ids]
    interval = paired_bootstrap_delta(
        f2_success,
        g3_success,
        seed=int(plan["paired_comparison"]["bootstrap_seed"]) + 600,
        resamples=int(plan["paired_comparison"]["bootstrap_resamples"]),
    )
    if interval["lower"] > 0:
        selected = "F2"
    elif interval["upper"] < 0:
        selected = "G3"
    else:
        return {
            "status": "NO_TOPOLOGY_SELECTED",
            "selected": None,
            "metrics": metrics,
            "execution_comparison": interval,
            "reason": "non-dominated split finalists unresolved",
        }
    return {
        "status": "SELECTED",
        "selected": selected,
        "metrics": metrics,
        "execution_comparison": interval,
    }
