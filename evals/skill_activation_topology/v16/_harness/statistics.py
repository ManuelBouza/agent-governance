"""Dependency-free exact/binomial and paired resampling statistics for v16."""
from __future__ import annotations
from collections.abc import Callable, Sequence
import math
import random
from .models import HarnessError

def _binom_cdf(k: int, n: int, p: float) -> float:
    return sum(math.comb(n, i) * p**i * (1.0 - p) ** (n - i) for i in range(k + 1))

def _binom_sf(k_minus_one: int, n: int, p: float) -> float:
    return 1.0 - _binom_cdf(k_minus_one, n, p)

def exact_one_sided_success_lower(successes: int, n: int, confidence: float = 0.95) -> float:
    """Clopper-Pearson one-sided lower confidence bound for a success probability."""
    if not 0 <= successes <= n or n <= 0:
        raise HarnessError("invalid binomial counts")
    if successes == 0:
        return 0.0
    alpha = 1.0 - confidence
    lo, hi = (0.0, 1.0)
    for _ in range(90):
        mid = (lo + hi) / 2.0
        tail = _binom_sf(successes - 1, n, mid)
        if tail < alpha:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0

def exact_one_sided_rate_upper(events: int, n: int, confidence: float = 0.95) -> float:
    """Clopper-Pearson one-sided upper confidence bound for an event probability."""
    if not 0 <= events <= n or n <= 0:
        raise HarnessError("invalid binomial counts")
    if events == n:
        return 1.0
    alpha = 1.0 - confidence
    lo, hi = (0.0, 1.0)
    for _ in range(90):
        mid = (lo + hi) / 2.0
        cdf = _binom_cdf(events, n, mid)
        if cdf > alpha:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0

def exact_mcnemar_pvalue(a_correct: Sequence[bool], b_correct: Sequence[bool]) -> float:
    if len(a_correct) != len(b_correct) or not a_correct:
        raise HarnessError("paired vectors must have equal non-zero length")
    b = sum((x and not y for x, y in zip(a_correct, b_correct, strict=True)))
    c = sum((y and not x for x, y in zip(a_correct, b_correct, strict=True)))
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum((math.comb(n, i) for i in range(k + 1))) / 2**n
    return min(1.0, 2.0 * tail)

def paired_bootstrap_delta(a: Sequence[float], b: Sequence[float], *, statistic: Callable[[Sequence[float]], float] | None = None, seed: int, resamples: int, confidence: float = 0.95) -> dict[str, float]:
    if len(a) != len(b) or not a:
        raise HarnessError("paired bootstrap requires equal non-zero vectors")
    if resamples < 100:
        raise HarnessError("bootstrap resamples must be >= 100")
    stat = statistic or (lambda xs: sum(xs) / len(xs))
    observed = stat(a) - stat(b)
    rng = random.Random(seed)
    deltas: list[float] = []
    n = len(a)
    for _ in range(resamples):
        idx = [rng.randrange(n) for _ in range(n)]
        deltas.append(stat([a[i] for i in idx]) - stat([b[i] for i in idx]))
    deltas.sort()
    alpha = 1.0 - confidence
    low_i = max(0, min(resamples - 1, int(alpha / 2.0 * resamples)))
    high_i = max(0, min(resamples - 1, int((1.0 - alpha / 2.0) * resamples) - 1))
    return {"delta": observed, "lower": deltas[low_i], "upper": deltas[high_i]}

def holm_adjust(pvalues: dict[str, float], alpha: float = 0.05) -> dict[str, dict[str, float | bool]]:
    ordered = sorted(pvalues.items(), key=lambda item: item[1])
    m = len(ordered)
    running = 0.0
    adjusted: dict[str, dict[str, float | bool]] = {}
    for rank, (name, pvalue) in enumerate(ordered, start=1):
        raw_adjusted = min(1.0, (m - rank + 1) * pvalue)
        running = max(running, raw_adjusted)
        adjusted[name] = {"raw_p": pvalue, "adjusted_p": running, "reject": running <= alpha}
    return adjusted
