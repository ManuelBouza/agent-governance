import pytest
from evals.skill_activation_topology.v16._harness.models import HarnessError
from evals.skill_activation_topology.v16._harness.scheduler import AttemptBudget, e2e_schedule, reliability_schedule, routing_first_schedule
PLAN = {'attempt_budget': {'absolute_stage6_provider_model_attempt_ceiling': 1264, 'max_attempts_per_scientific_observation': 2, 'behavioral_preflight_max_attempts': 4, 'synthetic_canary_max_attempts': 4}}

def test_geometry_and_budget_fail_closed():
    corpus = {'routing_cases': [{'id': f'r{i}'} for i in range(270)], 'e2e_reserve': [{'id': f'e{i}'} for i in range(60)]}
    oracle = {'reliability_subset_case_ids': [f'r{i}' for i in range(30)]}
    assert len(routing_first_schedule(corpus)) == 810
    assert len(reliability_schedule(corpus, oracle)) == 90
    assert len(e2e_schedule(corpus, ['B2', 'F2'])) == 120
    budget = AttemptBudget(PLAN, 1264)
    with pytest.raises(HarnessError):
        budget.consume()
