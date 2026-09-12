from evals.skill_activation_topology.v16._harness.statistics import exact_mcnemar_pvalue, exact_one_sided_rate_upper, exact_one_sided_success_lower, holm_adjust, paired_bootstrap_delta

def test_sixty_zero_failures_crosses_95_5_boundary():
    assert exact_one_sided_success_lower(60, 60) > 0.95
    assert exact_one_sided_rate_upper(0, 60) < 0.05

def test_one_failure_no_longer_supports_95_population_claim():
    assert exact_one_sided_success_lower(59, 60) < 0.95

def test_paired_exact_and_bootstrap_are_deterministic():
    a = [True, True, True, False, True, True]
    b = [True, False, True, False, False, True]
    p = exact_mcnemar_pvalue(a, b)
    assert 0 <= p <= 1
    x = paired_bootstrap_delta([float(v) for v in a], [float(v) for v in b], seed=12, resamples=500)
    y = paired_bootstrap_delta([float(v) for v in a], [float(v) for v in b], seed=12, resamples=500)
    assert x == y and x['delta'] > 0

def test_holm_is_monotone():
    out = holm_adjust({'a': 0.01, 'b': 0.02, 'c': 0.2})
    assert out['a']['adjusted_p'] <= out['b']['adjusted_p'] <= out['c']['adjusted_p']
