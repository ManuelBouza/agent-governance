from __future__ import annotations
import json
from pathlib import Path

from evals.skill_activation_topology.v17 import harness as h


def topo():
    return json.loads((h.V17_ROOT / "topologies.json").read_text(encoding="utf-8"))


def obs(**overrides):
    base = dict(
        case_id="case", candidate_id="F2", repetition="r1", phase="routing",
        observed_disposition="ROUTE",
        observed_activation_set=frozenset({"consumer-governance"}),
        observed_capability_set=frozenset({"consumer-lifecycle"}),
        clarification_requested=False, bounded_refusal=False, context_bytes=10,
        latency_seconds=0.1, provider_usage={}, technical_valid=True, task_success=None,
    )
    base.update(overrides)
    return h.Observation(**base)


def test_freeze_i_guard_passes_without_confirmatory_assets():
    result = h.validate_freeze_i()
    assert result["status"] == "PASS"
    assert result["development_cases"] == 90
    assert result["provider_model_calls"] == 0


def test_routing_schema_is_domain_neutral_and_has_no_task_success():
    inst = h.load_json(h.INSTRUMENTATION_PATH)
    h.validate_model_visible_instrumentation(inst)
    schema = inst["routing_only"]["output_schema"]
    assert set(schema["properties"]) == {
        "clarification_requested", "bounded_refusal", "response_summary"
    }
    assert "task_success" not in json.dumps(schema)


def test_trace_is_only_authority_for_activation_and_capability_identity():
    manifest = h.load_json(h.MANIFEST_PATH)
    stdout = "\n".join([
        json.dumps({"type":"thread.started"}),
        json.dumps({"type":"item.completed","item":{
            "type":"command_execution","exit_code":0,
            "command":"cat .agents/skills/consumer-governance/SKILL.md"
        }}),
        json.dumps({"type":"item.completed","item":{
            "type":"command_execution","exit_code":0,
            "command":"cat .agents/skills/consumer-governance/references/consumer-lifecycle.md"
        }}),
    ])
    trace = h.parse_host_trace(stdout, manifest, "F2")
    assert trace["observed_activation_set"] == ["consumer-governance"]
    assert trace["observed_capability_set"] == ["consumer-lifecycle"]
    assert h.derive_disposition(
        trace["observed_activation_set"], trace["observed_capability_set"], False
    ) == "ROUTE"


def test_shared_entrypoint_requires_exact_capability_reference_set():
    truth = h.RoutingTruth(
        case_id="case", disposition="ROUTE",
        capabilities=frozenset({"external-skill-trust"})
    )
    wrong = obs(observed_capability_set=frozenset({"consumer-lifecycle"}))
    right = obs(observed_capability_set=frozenset({"external-skill-trust"}))
    assert not h.exact_routing_correct(wrong, truth, topo())
    assert h.exact_routing_correct(right, truth, topo())


def test_abstain_is_derived_from_empty_trace_plus_generic_clarification():
    truth = h.RoutingTruth(case_id="case", disposition="ABSTAIN", capabilities=None)
    abstain = obs(
        observed_disposition="ABSTAIN",
        observed_activation_set=frozenset(),
        observed_capability_set=frozenset(),
        clarification_requested=True,
    )
    none = obs(
        observed_disposition="NONE",
        observed_activation_set=frozenset(),
        observed_capability_set=frozenset(),
        clarification_requested=False,
    )
    assert h.exact_routing_correct(abstain, truth, topo())
    assert not h.exact_routing_correct(none, truth, topo())


def test_e2e_conditional_denominator_uses_exact_routing_not_disposition_only():
    t = topo()
    truths = {
        "a": h.RoutingTruth("a","ROUTE",frozenset({"consumer-lifecycle"})),
        "b": h.RoutingTruth("b","ROUTE",frozenset({"consumer-lifecycle"})),
    }
    good = h.Observation(
        "a","B2","r1","e2e","ROUTE",frozenset({"agent-governance"}),
        frozenset({"consumer-lifecycle"}),False,False,10,0.1,{},True,True
    )
    wrong_same_disposition = h.Observation(
        "b","B2","r1","e2e","ROUTE",frozenset({"agent-governance"}),
        frozenset({"source-maintainer"}),False,False,10,0.1,{},True,True
    )
    corpus={"e2e_reserve":[
        {"id":"a","category":"consumer-lifecycle"},
        {"id":"b","category":"consumer-lifecycle"},
    ]}
    plan=h.load_json(h.ANALYSIS_PATH)
    result=h.e2e_analysis(
        [good,wrong_same_disposition],{"finalists":["B2"]},truths,corpus,t,plan
    )
    metrics=result["metrics"]["B2"]
    assert metrics["conditional_exact_routing_n"] == 1
    assert metrics["conditional_execution_success"] == 1.0
    assert metrics["end_to_end_task_success"] == 0.5


def test_wrong_routing_is_end_to_end_failure_even_if_model_claims_success():
    t = topo()
    truth = h.RoutingTruth("a","ROUTE",frozenset({"consumer-lifecycle"}))
    wrong = h.Observation(
        "a","B2","r1","e2e","ROUTE",frozenset({"agent-governance"}),
        frozenset({"source-maintainer"}),False,False,10,0.1,{},True,True
    )
    corpus={"e2e_reserve":[{"id":"a","category":"consumer-lifecycle"}]}
    result=h.e2e_analysis(
        [wrong],{"finalists":["B2"]},{"a":truth},corpus,t,h.load_json(h.ANALYSIS_PATH)
    )
    assert result["metrics"]["B2"]["end_to_end_task_success"] == 0.0
    assert result["metrics"]["B2"]["conditional_exact_routing_n"] == 0


def test_canary_requires_two_of_two_behavioral_passes():
    plan=h.load_json(h.ANALYSIS_PATH)
    cases=[
        {"id":"c1","expected_generic_evidence":{"clarification_requested":False}},
        {"id":"c2","expected_generic_evidence":{"clarification_requested":False}},
    ]
    records=[
        {"phase":"canary","case_id":"c1","technical_valid":True,
         "clarification_requested":False,"observed_activation_set":[],"observed_capability_set":[]},
        {"phase":"canary","case_id":"c2","technical_valid":True,
         "clarification_requested":True,"observed_activation_set":[],"observed_capability_set":[]},
    ]
    assert not h.evaluate_behavioral_gate("canary",records,cases,plan)["passed"]
    records[1]["clarification_requested"]=False
    assert h.evaluate_behavioral_gate("canary",records,cases,plan)["passed"]


def test_gate_attempt_budgets_are_total_not_per_observation():
    plan=h.load_json(h.ANALYSIS_PATH)
    budget=h.AttemptBudget(plan)
    for _ in range(4):
        budget.consume("canary")
    try:
        budget.consume("canary")
    except h.HarnessError:
        pass
    else:
        raise AssertionError("canary phase exceeded four total attempts")


def test_exact_one_sided_bounds_support_planned_95_5_claim_at_n60_zero_failures():
    assert h.exact_one_sided_success_lower(60,60) > 0.95
    assert h.exact_one_sided_rate_upper(0,60) < 0.05


def test_freeze_e_candidate_git_blob_receipt_matches_actual_bytes():
    prov=h.load_json(h.PROVENANCE_PATH)
    h.validate_candidate_integrity(prov,h.load_json(h.MANIFEST_PATH),topo())
    b2=h.REPO_ROOT/"evals/skill_activation_topology/v17/presentations/B2/agent-governance/SKILL.md"
    assert h.git_blob_sha_file(b2)=="1558c74a524b399b100b05dd6f1041011b8e1949"
    assert h.git_blob_sha_file(h.TOPOLOGIES_PATH)=="1adb4c156bb03e39dd9bf8c2443c501c82f31f5f"


def test_scientific_attempt_limit_survives_resume():
    plan=h.load_json(h.ANALYSIS_PATH)
    inputs={"analysis":plan}
    spec=h.ScheduledObservation("routing","r-001","B2","r1")
    attempts=[
        {"phase":"routing","case_id":"r-001","candidate_id":"B2","repetition":"r1","technical_valid":False},
    ]
    assert h.remaining_observation_attempts(spec,inputs,attempts)==1
    attempts.append(
        {"phase":"routing","case_id":"r-001","candidate_id":"B2","repetition":"r1","technical_valid":False}
    )
    assert h.remaining_observation_attempts(spec,inputs,attempts)==0


def test_reliability_schedule_uses_separate_frozen_subset():
    corpus={"routing_cases":[{"id":f"r-{i:03d}"} for i in range(40)]}
    reliability={"case_ids":[f"r-{i:03d}" for i in range(30)]}
    schedule=h.reliability_schedule(corpus,reliability)
    assert len(schedule)==90
    assert {x.case_id for x in schedule}==set(reliability["case_ids"])


def test_cross_profile_critical_gate_uses_trace_not_bounded_refusal_self_report():
    plan=h.load_json(h.ANALYSIS_PATH); t=topo()
    truth=h.RoutingTruth("x","ROUTE",frozenset({"consumer-lifecycle"}),critical_permission_boundary=True)
    case={"id":"x","category":"cross-profile","primary_backbone":False}
    correct=obs(case_id="x",bounded_refusal=False)
    wrong=obs(
        case_id="x",bounded_refusal=True,
        observed_activation_set=frozenset({"source-maintainer"}),
        observed_capability_set=frozenset({"source-maintainer"}),
    )
    good=h.candidate_routing_metrics([correct],{"x":truth},{"x":case},t,plan)
    bad=h.candidate_routing_metrics([wrong],{"x":truth},{"x":case},t,plan)
    assert good["critical_cross_profile_permission_invalid"]==0
    assert bad["critical_cross_profile_permission_invalid"]==1


def test_provider_usage_and_latency_reporting_are_host_observation_dimensions():
    assert h.provider_usage_units({"total_tokens":7})==7.0
    assert h.provider_usage_units({"input_tokens":3,"output_tokens":2})==5.0
    assert h.provider_usage_units({"input_tokens":3}) is None
