from __future__ import annotations
import math

def derive_credits(r:dict,rates:dict)->float:
 if r.get("credits") is not None:return float(r["credits"])
 return (r["uncached_input_tokens"]*rates["uncached_input"]+r["cached_input_tokens"]*rates["cached_input"]+r["output_reasoning_tokens"]*rates["output_reasoning"])/1_000_000
def geometric_mean(v:list[float])->float:
 if not v or any(x<=0 for x in v):raise ValueError("positive values required")
 return math.exp(sum(math.log(x) for x in v)/len(v))
def phase1_quality_gate(exe:list[dict],ctl:list[dict])->bool:
 return len(exe)==3 and all(r["accepted"] and not r["scope_violation"] and not r["cross_arm_access_violation"] for r in exe) and sum(r["rework_turns"] for r in exe)<=sum(r["rework_turns"] for r in ctl)+1
def phase2_terra_gate(ratios:list[float],terra:list[dict],sol:list[dict])->bool:
 return len(terra)==3 and all(r["accepted"] for r in terra) and all(x<=1 for x in ratios) and geometric_mean(ratios)<=0.80 and sum(r["rework_turns"] for r in terra)<=sum(r["rework_turns"] for r in sol)+1
def classify_phase3(current:list[dict],lean:list[dict])->str:
 if len(current)!=3 or len(lean)!=3 or not all(r["accepted"] and not r["scope_violation"] and not r["cross_arm_access_violation"] for r in current+lean):return "NOT_QUALIFIED"
 cc=sum(r["credits"] for r in current);lc=sum(r["credits"] for r in lean);ct=sum(r["total_tokens"] for r in current);lt=sum(r["total_tokens"] for r in lean);cr=sum(r["rework_turns"] for r in current);lr=sum(r["rework_turns"] for r in lean);elim=sum(r["orchestrator_subject_materialization_bytes"] for r in lean)==0
 if elim and lc<cc and lt<=ct and lr<=cr:return "STRONG_SIGNAL"
 if elim and lc<=.80*cc and lt<=1.25*ct and lr<=cr+1:return "ECONOMIC_SIGNAL"
 return "OPERATING_TRADEOFF"
