from __future__ import annotations
import math,random
from typing import Any,Callable,Sequence
from .core import HarnessError

def _binom_cdf(k:int,n:int,p:float)->float:
    return sum(math.comb(n,i)*p**i*(1-p)**(n-i) for i in range(k+1))

def exact_one_sided_success_lower(successes:int,n:int,confidence:float=.95)->float:
    if not 0<=successes<=n or n<=0: raise HarnessError("invalid binomial counts")
    if successes==0: return 0.
    alpha=1-confidence; lo,hi=0.,1.
    for _ in range(90):
        mid=(lo+hi)/2; tail=1-_binom_cdf(successes-1,n,mid)
        if tail<alpha: lo=mid
        else: hi=mid
    return (lo+hi)/2

def exact_one_sided_rate_upper(events:int,n:int,confidence:float=.95)->float:
    if not 0<=events<=n or n<=0: raise HarnessError("invalid binomial counts")
    if events==n: return 1.
    alpha=1-confidence; lo,hi=0.,1.
    for _ in range(90):
        mid=(lo+hi)/2; cdf=_binom_cdf(events,n,mid)
        if cdf>alpha: lo=mid
        else: hi=mid
    return (lo+hi)/2

def exact_mcnemar_pvalue(a:Sequence[bool],b:Sequence[bool])->float:
    if len(a)!=len(b) or not a: raise HarnessError("paired vectors must have equal non-zero length")
    x=sum(left and not right for left,right in zip(a,b,strict=True))
    y=sum(right and not left for left,right in zip(a,b,strict=True)); n=x+y
    if n==0: return 1.
    k=min(x,y); return min(1.,2*sum(math.comb(n,i) for i in range(k+1))/2**n)

def paired_bootstrap_delta(a:Sequence[float],b:Sequence[float],*,seed:int,resamples:int,statistic:Callable[[Sequence[float]],float]|None=None,confidence:float=.95)->dict[str,float]:
    if len(a)!=len(b) or not a: raise HarnessError("paired bootstrap requires equal non-zero vectors")
    if resamples<100: raise HarnessError("bootstrap resamples must be >=100")
    stat=statistic or (lambda xs:sum(xs)/len(xs)); rng=random.Random(seed); n=len(a)
    observed=stat(a)-stat(b); values=[]
    for _ in range(resamples):
        idx=[rng.randrange(n) for _ in range(n)]
        values.append(stat([a[i] for i in idx])-stat([b[i] for i in idx]))
    values.sort(); alpha=1-confidence
    lo=max(0,min(resamples-1,int(alpha/2*resamples)))
    hi=max(0,min(resamples-1,int((1-alpha/2)*resamples)-1))
    return {"delta":observed,"lower":values[lo],"upper":values[hi]}

def holm_adjust(pvalues:dict[str,float],alpha:float=.05)->dict[str,dict[str,Any]]:
    ordered=sorted(pvalues.items(),key=lambda p:p[1]); m=len(ordered); running=0.; out={}
    for rank,(name,pvalue) in enumerate(ordered,1):
        running=max(running,min(1.,(m-rank+1)*pvalue))
        out[name]={"raw_p":pvalue,"adjusted_p":running,"reject":running<=alpha}
    return out
