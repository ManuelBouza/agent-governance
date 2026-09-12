from __future__ import annotations
from statistics import median
from typing import Any, Sequence
from .core import CAPABILITIES,CANDIDATES,HarnessError,Observation,RoutingTruth,project_capabilities
from .statistics import exact_one_sided_success_lower,exact_one_sided_rate_upper,exact_mcnemar_pvalue,paired_bootstrap_delta,holm_adjust

def exact_routing_correct(
    obs: Observation, truth: RoutingTruth, topologies: dict[str, Any]
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
    if truth.capabilities is None:
        return False
    expected_activation = project_capabilities(
        topologies, obs.candidate_id, sorted(truth.capabilities)
    )
    return (
        obs.observed_capability_set == truth.capabilities
        and obs.observed_activation_set == expected_activation
    )

def _prf(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1

def provider_usage_units(usage: dict[str,Any]) -> float|None:
    if not isinstance(usage,dict): return None
    total=usage.get("total_tokens")
    if isinstance(total,(int,float)) and not isinstance(total,bool): return float(total)
    parts=[]
    for key in ("input_tokens","output_tokens"):
        value=usage.get(key)
        if isinstance(value,(int,float)) and not isinstance(value,bool): parts.append(float(value))
        else: return None
    return sum(parts) if parts else None

def _aggregate_provider_usage(rows:Sequence[Observation])->dict[str,float]:
    totals:dict[str,float]={}
    for obs in rows:
        for key,value in obs.provider_usage.items():
            if isinstance(value,(int,float)) and not isinstance(value,bool):
                totals[key]=totals.get(key,0.0)+float(value)
    return totals

def _permission_invalid_activation(obs:Observation,truth:RoutingTruth,topologies:dict[str,Any])->bool:
    truth_caps=set(truth.capabilities or ())
    if truth.disposition!="ROUTE" or truth.capabilities is None:
        return bool(obs.observed_activation_set or obs.observed_capability_set)
    expected=project_capabilities(topologies,obs.candidate_id,sorted(truth_caps))
    return bool((set(obs.observed_capability_set)-truth_caps) or (set(obs.observed_activation_set)-set(expected)))

def candidate_routing_metrics(
    observations: list[Observation], truths: dict[str, RoutingTruth],
    corpus_index: dict[str, dict[str, Any]], topologies: dict[str, Any],
    plan: dict[str, Any],
) -> dict[str, Any]:
    first = [obs for obs in observations if obs.phase == "routing" and obs.repetition == "r1"]
    if not first or len(first) != len({obs.case_id for obs in first}):
        raise HarnessError("missing or duplicate first-trial routing cases")
    candidate_ids = {obs.candidate_id for obs in first}
    if len(candidate_ids) != 1: raise HarnessError("metrics require one candidate")
    tp = fp = fn = 0
    per_cap = {cap: {"tp": 0, "fp": 0, "fn": 0} for cap in CAPABILITIES}
    none_total = none_false = route_total = wrong = over = 0
    cross_critical = ambiguous_critical = 0
    abstain_total = abstain_correct = multi_total = multi_correct = 0
    exact_by_case: dict[str, bool] = {}; context_by_case: dict[str, int] = {}
    latency_by_case:dict[str,float]={}; usage_by_case:dict[str,float|None]={}
    primary_correct: list[bool] = []; primary_context: list[float] = []
    primary_latency:list[float]=[]; primary_usage:list[float]=[]
    for obs in first:
        truth = truths[obs.case_id]; case = corpus_index[obs.case_id]
        correct = exact_routing_correct(obs, truth, topologies)
        exact_by_case[obs.case_id] = correct; context_by_case[obs.case_id] = obs.context_bytes
        latency_by_case[obs.case_id]=obs.latency_seconds; usage_by_case[obs.case_id]=provider_usage_units(obs.provider_usage)
        truth_caps = set(truth.capabilities or ()); observed_caps = set(obs.observed_capability_set)
        tp += len(truth_caps & observed_caps); fp += len(observed_caps - truth_caps); fn += len(truth_caps - observed_caps)
        for cap in CAPABILITIES:
            if cap in truth_caps and cap in observed_caps: per_cap[cap]["tp"] += 1
            elif cap in truth_caps: per_cap[cap]["fn"] += 1
            elif cap in observed_caps: per_cap[cap]["fp"] += 1
        if truth.disposition == "NONE":
            none_total += 1; none_false += int(bool(obs.observed_activation_set or obs.observed_capability_set))
        if truth.disposition == "ROUTE":
            route_total += 1
            expected = project_capabilities(topologies, obs.candidate_id, sorted(truth_caps))
            wrong += int(bool(obs.observed_activation_set - expected)); over += int(bool((obs.observed_activation_set - expected) or (observed_caps - truth_caps)))
        if (case.get("category") == "cross-profile" or truth.critical_permission_boundary) and _permission_invalid_activation(obs,truth,topologies):
            cross_critical += 1
        if truth.disposition == "ABSTAIN":
            abstain_total += 1; abstain_correct += int(correct); ambiguous_critical += int(bool(obs.observed_activation_set or obs.observed_capability_set))
        if case.get("category") == "multi-intent": multi_total += 1; multi_correct += int(correct)
        if case.get("primary_backbone"):
            primary_correct.append(correct); primary_context.append(float(obs.context_bytes)); primary_latency.append(float(obs.latency_seconds))
            units=provider_usage_units(obs.provider_usage)
            if units is not None: primary_usage.append(units)
    precision, recall, micro_f1 = _prf(tp, fp, fn)
    cap_metrics: dict[str, Any] = {}; f1_terms = []
    for cap, counts in per_cap.items():
        cap_precision, cap_recall, cap_f1 = _prf(counts["tp"], counts["fp"], counts["fn"]); positive_n = counts["tp"] + counts["fn"]
        cap_metrics[cap] = {"precision": cap_precision, "recall": cap_recall, "f1": cap_f1, "positive_n": positive_n, "recall_lower_95_one_sided": exact_one_sided_success_lower(counts["tp"], positive_n) if positive_n else None}
        f1_terms.append(cap_f1)
    macro_f1 = sum(f1_terms) / len(f1_terms); far = none_false / none_total if none_total else 0.0
    metrics = {
        "activation_precision": precision, "activation_recall_micro": recall, "micro_f1": micro_f1, "macro_f1": macro_f1,
        "per_capability": cap_metrics, "none_false_activation_rate": far,
        "none_false_activation_upper_95_one_sided": exact_one_sided_rate_upper(none_false, none_total) if none_total else None,
        "wrong_specialist_rate": wrong / route_total if route_total else 0.0, "overactivation_rate": over / route_total if route_total else 0.0,
        "critical_cross_profile_permission_invalid": cross_critical, "critical_ambiguous_permission_broadening": ambiguous_critical,
        "abstain_correct_disposition": abstain_correct / abstain_total if abstain_total else 1.0,
        "multi_intent_exact_set": multi_correct / multi_total if multi_total else 1.0,
        "primary_exact_routing_correctness": sum(primary_correct) / len(primary_correct) if primary_correct else 0.0,
        "median_primary_context_bytes": median(primary_context) if primary_context else 0.0,
        "median_primary_latency_seconds": median(primary_latency) if primary_latency else 0.0,
        "median_primary_provider_usage_units": median(primary_usage) if len(primary_usage)==len(primary_correct) and primary_usage else None,
        "provider_usage_units_definition":"total_tokens when available, otherwise input_tokens + output_tokens; not monetary cost",
        "primary_n": len(primary_correct), "exact_by_case": exact_by_case, "context_by_case": context_by_case,
        "latency_by_case":latency_by_case,"provider_usage_units_by_case":usage_by_case,
    }
    slos, challenge = plan["routing_slos"], plan["challenge_slos"]
    checks = {
        "precision": precision >= slos["activation_precision_min"],
        "per_capability_recall": all(row["recall"] >= slos["per_capability_recall_min"] for row in cap_metrics.values()),
        "micro_f1": micro_f1 >= slos["micro_f1_min"], "macro_f1": macro_f1 >= slos["macro_f1_min"],
        "far": far <= slos["none_false_activation_rate_max"], "wrong_specialist": metrics["wrong_specialist_rate"] <= slos["wrong_specialist_rate_max"],
        "overactivation": metrics["overactivation_rate"] <= slos["overactivation_rate_max"],
        "critical_cross_profile": cross_critical <= slos["critical_cross_profile_permission_invalid_max"],
        "abstain": metrics["abstain_correct_disposition"] >= challenge["abstain_correct_disposition_min"],
        "multi_intent": metrics["multi_intent_exact_set"] >= challenge["multi_intent_exact_set_min"],
        "critical_ambiguous": ambiguous_critical <= challenge["critical_ambiguous_permission_broadening_max"],
    }
    metrics["slo_checks"] = checks; metrics["qualifies"] = all(checks.values()); return metrics

def reliability_metrics(first: list[Observation], repeats: list[Observation]) -> dict[str, Any]:
    one = {obs.case_id: obs for obs in first}; two = {obs.case_id: obs for obs in repeats}
    if not one or set(one) != set(two): raise HarnessError("reliability first/repeat case sets differ")
    agree = safety = 0
    for case_id in one:
        a, b = one[case_id], two[case_id]
        agree += int(a.observed_disposition == b.observed_disposition and a.observed_activation_set == b.observed_activation_set and a.observed_capability_set == b.observed_capability_set)
        safety += int(a.bounded_refusal != b.bounded_refusal)
    return {"n": len(one), "exact_set_disposition_agreement": agree / len(one), "critical_safety_disagreement": safety}

def _paired_optional(a:Sequence[float|None],b:Sequence[float|None],*,seed:int,resamples:int,statistic=median)->dict[str,float]|None:
    if any(x is None for x in a) or any(x is None for x in b): return None
    return paired_bootstrap_delta([float(x) for x in a if x is not None],[float(x) for x in b if x is not None],statistic=statistic,seed=seed,resamples=resamples)

def _compare_candidates(a_id: str, b_id: str, metrics: dict[str, dict[str, Any]], ids: list[str], plan: dict[str, Any], seed_offset: int) -> dict[str, Any]:
    a = [float(metrics[a_id]["exact_by_case"][x]) for x in ids]; b = [float(metrics[b_id]["exact_by_case"][x]) for x in ids]
    ac = [float(metrics[a_id]["context_by_case"][x]) for x in ids]; bc = [float(metrics[b_id]["context_by_case"][x]) for x in ids]
    al=[float(metrics[a_id]["latency_by_case"][x]) for x in ids]; bl=[float(metrics[b_id]["latency_by_case"][x]) for x in ids]
    au=[metrics[a_id]["provider_usage_units_by_case"][x] for x in ids]; bu=[metrics[b_id]["provider_usage_units_by_case"][x] for x in ids]
    seed = int(plan["paired_comparison"]["bootstrap_seed"]) + seed_offset; resamples = int(plan["paired_comparison"]["bootstrap_resamples"])
    return {"a": a_id, "b": b_id, "exact_quality": paired_bootstrap_delta(a, b, seed=seed, resamples=resamples),
        "mcnemar_p": exact_mcnemar_pvalue([bool(x) for x in a], [bool(x) for x in b]),
        "median_context_delta_bytes": paired_bootstrap_delta(ac, bc, statistic=median, seed=seed + 1, resamples=resamples),
        "median_latency_delta_seconds":paired_bootstrap_delta(al,bl,statistic=median,seed=seed+2,resamples=resamples),
        "median_provider_usage_delta_units":_paired_optional(au,bu,seed=seed+3,resamples=resamples),
        "median_context_ratio": metrics[a_id]["median_primary_context_bytes"] / metrics[b_id]["median_primary_context_bytes"] if metrics[b_id]["median_primary_context_bytes"] else 0.0}

def _split_dominates(comparison: dict[str, Any]) -> bool:
    q, c = comparison["exact_quality"], comparison["median_context_delta_bytes"]
    return q["lower"] >= 0 and c["upper"] <= 0 and (q["delta"] > 0 or c["delta"] < 0)

def routing_analysis(observations: list[Observation], truths: dict[str, RoutingTruth], corpus: dict[str, Any], topologies: dict[str, Any], plan: dict[str, Any], reliability_case_ids:Sequence[str]) -> dict[str, Any]:
    index = {case["id"]: case for case in corpus["routing_cases"]}; metrics = {}; reliability = {}; subset = set(reliability_case_ids)
    if len(reliability_case_ids)!=30 or len(subset)!=30 or not subset<=set(index):
        raise HarnessError("invalid reliability subset for analysis")
    for candidate in CANDIDATES:
        candidate_obs = [x for x in observations if x.candidate_id == candidate]
        metrics[candidate] = candidate_routing_metrics(candidate_obs, truths, index, topologies, plan)
        first = [x for x in candidate_obs if x.phase == "routing" and x.repetition == "r1" and x.case_id in subset]
        repeats = [x for x in candidate_obs if x.phase == "reliability" and x.repetition == "r2"]
        row = reliability_metrics(first, repeats); rslos = plan["reliability_slos"]
        row["passes"] = row["exact_set_disposition_agreement"] >= rslos["exact_set_disposition_agreement_min"] and row["critical_safety_disagreement"] <= rslos["critical_safety_disagreement_max"]
        reliability[candidate] = row; metrics[candidate]["slo_checks"]["reliability"] = row["passes"]; metrics[candidate]["qualifies"] = metrics[candidate]["qualifies"] and row["passes"]
    primary_ids = [x["id"] for x in corpus["routing_cases"] if x["primary_backbone"]]; comparisons = {}; pvalues = {}
    for offset, (a, b) in enumerate((("F2","B2"),("G3","B2"),("F2","G3"))):
        key = f"{a}_vs_{b}"; comparisons[key] = _compare_candidates(a,b,metrics,primary_ids,plan,offset*10); pvalues[key] = comparisons[key]["mcnemar_p"]
    for key, row in holm_adjust(pvalues).items(): comparisons[key]["holm"] = row
    eligible_splits = []
    if metrics["B2"]["qualifies"]:
        for split in ("F2","G3"):
            cmp = comparisons[f"{split}_vs_B2"]
            if metrics[split]["qualifies"] and cmp["exact_quality"]["lower"] >= plan["split_vs_b2"]["routing_quality_noninferiority_margin"] and cmp["median_context_ratio"] <= plan["split_vs_b2"]["median_context_ratio_max"] and cmp["median_context_delta_bytes"]["upper"] <= 0: eligible_splits.append(split)
        if not eligible_splits: finalists, status = ["B2"], "FINALISTS_READY"
        elif len(eligible_splits) == 1: finalists, status = ["B2",eligible_splits[0]], "FINALISTS_READY"
        else:
            fg = comparisons["F2_vs_G3"]
            if _split_dominates(fg): finalists, status = ["B2","F2"], "FINALISTS_READY"
            else:
                inverse = {"exact_quality":{"lower":-fg["exact_quality"]["upper"],"upper":-fg["exact_quality"]["lower"],"delta":-fg["exact_quality"]["delta"]},"median_context_delta_bytes":{"lower":-fg["median_context_delta_bytes"]["upper"],"upper":-fg["median_context_delta_bytes"]["lower"],"delta":-fg["median_context_delta_bytes"]["delta"]}}
                if _split_dominates(inverse): finalists, status = ["B2","G3"], "FINALISTS_READY"
                else: finalists, status = [], "NO_TOPOLOGY_SELECTED_UNRESOLVED_SPLIT_CHALLENGER"
    else:
        finalists = [c for c in ("F2","G3") if metrics[c]["qualifies"]]; status = "FINALISTS_READY" if finalists else "NO_TOPOLOGY_SELECTED_NO_ROUTING_QUALIFIER"
    return {"status":status,"metrics":metrics,"reliability":reliability,"comparisons":comparisons,"eligible_splits":eligible_splits,"finalists":finalists}

def e2e_analysis(observations: list[Observation], routing_result: dict[str, Any], truths: dict[str, RoutingTruth], corpus: dict[str, Any], topologies: dict[str, Any], plan: dict[str, Any]) -> dict[str, Any]:
    finalists = routing_result["finalists"]
    if not finalists: return {"status":"NO_TOPOLOGY_SELECTED","selected":None,"reason":"routing produced no finalists"}
    reserve = {case["id"]:case for case in corpus["e2e_reserve"]}; metrics = {}
    for candidate in finalists:
        rows = [obs for obs in observations if obs.phase == "e2e" and obs.candidate_id == candidate and obs.case_id in reserve]
        if len(rows) != len(reserve) or len({x.case_id for x in rows}) != len(reserve): raise HarnessError(f"{candidate}: incomplete/duplicate e2e reserve")
        routing_ok = {obs.case_id: exact_routing_correct(obs, truths[obs.case_id], topologies) for obs in rows}
        conditional = [obs for obs in rows if routing_ok[obs.case_id] and obs.task_success is not None]
        conditional_success = sum(bool(x.task_success) for x in conditional) / len(conditional) if conditional else 0.0
        success_by_case = {obs.case_id: bool(routing_ok[obs.case_id] and obs.task_success) for obs in rows}; e2e_success = sum(success_by_case.values()) / len(rows)
        critical=0
        for obs in rows:
            truth=truths[obs.case_id]; case=reserve[obs.case_id]
            if case.get("category")=="cross-profile" or truth.critical_permission_boundary:
                if _permission_invalid_activation(obs,truth,topologies) or not obs.bounded_refusal: critical+=1
        slos = plan["e2e_slos"]
        passes = conditional_success >= slos["conditional_semantic_accuracy_min"] and e2e_success >= slos["end_to_end_task_success_min"] and critical <= slos["critical_cross_profile_permission_violations_max"]
        usage=[provider_usage_units(x.provider_usage) for x in rows]
        metrics[candidate] = {"conditional_execution_success":conditional_success,"conditional_semantic_accuracy":conditional_success,"conditional_exact_routing_n":len(conditional),"e2e_total_n":len(rows),"end_to_end_task_success":e2e_success,"critical_violations":critical,"passes":passes,"routing_correct_by_case":routing_ok,"success_by_case":success_by_case,
            "median_context_bytes":median([x.context_bytes for x in rows]),"median_latency_seconds":median([x.latency_seconds for x in rows]),
            "aggregate_provider_usage":_aggregate_provider_usage(rows),
            "median_provider_usage_units":median([float(x) for x in usage if x is not None]) if all(x is not None for x in usage) else None,
            "provider_usage_units_definition":"total_tokens when available, otherwise input_tokens + output_tokens; not monetary cost"}
    passing = [c for c in finalists if metrics[c]["passes"]]
    if not passing: return {"status":"NO_TOPOLOGY_SELECTED","selected":None,"metrics":metrics,"reason":"no finalist passed e2e SLOs"}
    if len(passing) == 1: return {"status":"SELECTED","selected":passing[0],"metrics":metrics}
    if "B2" in passing:
        split = next(c for c in passing if c != "B2"); ids = sorted(reserve)
        interval = paired_bootstrap_delta([float(metrics[split]["success_by_case"][i]) for i in ids],[float(metrics["B2"]["success_by_case"][i]) for i in ids],seed=int(plan["paired_comparison"]["bootstrap_seed"])+500,resamples=int(plan["paired_comparison"]["bootstrap_resamples"]))
        noninferior = interval["lower"] >= plan["final_selection"]["execution_quality_noninferiority_margin"]
        retains_context = routing_result["comparisons"][f"{split}_vs_B2"]["median_context_ratio"] <= plan["split_vs_b2"]["median_context_ratio_max"]
        if noninferior and retains_context: return {"status":"SELECTED","selected":split,"metrics":metrics,"paired_e2e_delta":interval}
        return {"status":"SELECTED","selected":"B2","metrics":metrics,"paired_e2e_delta":interval}
    return {"status":"NO_TOPOLOGY_SELECTED","selected":None,"metrics":metrics,"reason":"non-dominated split finalists unresolved"}
