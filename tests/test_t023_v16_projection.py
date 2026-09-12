from evals.skill_activation_topology.v16._harness.projection import project_capabilities, validate_topologies
TOPO = {'topology_revision': 'MG1-T023-TOPOLOGIES-v4', 'candidates': {'B2': {'capability_to_entrypoints': {'consumer-lifecycle': ['agent-governance'], 'source-maintainer': ['agent-governance'], 'external-skill-trust': ['agent-governance']}}, 'F2': {'capability_to_entrypoints': {'consumer-lifecycle': ['consumer-governance'], 'source-maintainer': ['source-maintainer'], 'external-skill-trust': ['consumer-governance']}}, 'G3': {'capability_to_entrypoints': {'consumer-lifecycle': ['consumer-lifecycle'], 'source-maintainer': ['source-maintainer'], 'external-skill-trust': ['external-skill-trust']}}}}

def test_projection_collapses_duplicate_f2_multi_label():
    validate_topologies(TOPO)
    assert project_capabilities(TOPO, 'F2', ['consumer-lifecycle', 'external-skill-trust']) == frozenset({'consumer-governance'})

def test_projection_b2_union_is_single_router():
    assert project_capabilities(TOPO, 'B2', ['source-maintainer', 'external-skill-trust']) == frozenset({'agent-governance'})

def test_projection_g3_preserves_multi_label():
    assert project_capabilities(TOPO, 'G3', ['source-maintainer', 'external-skill-trust']) == frozenset({'source-maintainer', 'external-skill-trust'})
