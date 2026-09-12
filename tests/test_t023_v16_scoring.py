from evals.skill_activation_topology.v16._harness.models import RoutingObservation, RoutingTruth
from evals.skill_activation_topology.v16._harness.scoring import exact_routing_correct
TOPO = {'topology_revision': 'MG1-T023-TOPOLOGIES-v4', 'candidates': {'B2': {'capability_to_entrypoints': {'consumer-lifecycle': ['agent-governance'], 'source-maintainer': ['agent-governance'], 'external-skill-trust': ['agent-governance']}}, 'F2': {'capability_to_entrypoints': {'consumer-lifecycle': ['consumer-governance'], 'source-maintainer': ['source-maintainer'], 'external-skill-trust': ['consumer-governance']}}, 'G3': {'capability_to_entrypoints': {'consumer-lifecycle': ['consumer-lifecycle'], 'source-maintainer': ['source-maintainer'], 'external-skill-trust': ['external-skill-trust']}}}}

def obs(**kw):
    base = dict(case_id='x', candidate_id='B2', repetition='r1', observed_disposition='ROUTE', observed_activation_set=frozenset({'agent-governance'}), observed_capability_set=frozenset({'consumer-lifecycle'}), clarification_requested=False, critical_permission_violation=False, context_bytes=10, latency_seconds=1.0, provider_usage={}, technical_valid=True)
    base.update(kw)
    return RoutingObservation(**base)

def test_shared_entrypoint_does_not_hide_wrong_capability():
    truth = RoutingTruth('x', 'ROUTE', frozenset({'source-maintainer'}))
    assert not exact_routing_correct(obs(), truth, TOPO)

def test_none_and_abstain_are_distinct():
    none = RoutingTruth('x', 'NONE', frozenset())
    abstain = RoutingTruth('x', 'ABSTAIN', None)
    empty = obs(observed_disposition='NONE', observed_activation_set=frozenset(), observed_capability_set=frozenset())
    assert exact_routing_correct(empty, none, TOPO)
    assert not exact_routing_correct(empty, abstain, TOPO)
    ask = obs(observed_disposition='ABSTAIN', observed_activation_set=frozenset(), observed_capability_set=frozenset(), clarification_requested=True)
    assert exact_routing_correct(ask, abstain, TOPO)
