from __future__ import annotations
from dataclasses import dataclass
import hashlib, json
from pathlib import Path
from typing import Any, Sequence

V17_ROOT=Path(__file__).resolve().parent
REPO_ROOT=V17_ROOT.parents[2]
CAPABILITIES=("consumer-lifecycle","source-maintainer","external-skill-trust")
CANDIDATES=("B2","F2","G3")
ANALYSIS_PATH=V17_ROOT/"analysis-plan.json"
ROUTING_PATH=V17_ROOT/"capability-routing.json"
PROVENANCE_PATH=V17_ROOT/"candidate-provenance.json"
TOPOLOGIES_PATH=V17_ROOT/"topologies.json"
MANIFEST_PATH=V17_ROOT/"presentation-manifest.json"
DEVELOPMENT_PATH=V17_ROOT/"development.json"
INSTRUMENTATION_PATH=V17_ROOT/"instrumentation.json"
CORPUS_PATH=V17_ROOT/"corpus.json"
ORACLE_PATH=V17_ROOT/"oracle.json"
ENVELOPE_PATH=V17_ROOT/"trial-envelope.json"
RELIABILITY_PATH=V17_ROOT/"reliability-subset.json"
FREEZE_I_REQUIRED=(ANALYSIS_PATH,ROUTING_PATH,PROVENANCE_PATH,TOPOLOGIES_PATH,MANIFEST_PATH,DEVELOPMENT_PATH,INSTRUMENTATION_PATH)
FREEZE_I_FORBIDDEN=(CORPUS_PATH,ORACLE_PATH,ENVELOPE_PATH,RELIABILITY_PATH)

class HarnessError(RuntimeError): pass

def load_json(path:Path)->dict[str,Any]:
    try: value=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: raise HarnessError(f"cannot load JSON {path}: {exc}") from exc
    if not isinstance(value,dict): raise HarnessError(f"{path} must contain a JSON object")
    return value

def dump_json(path:Path,value:Any)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def append_jsonl(path:Path,value:dict[str,Any])->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("a",encoding="utf-8",newline="\n") as h: h.write(json.dumps(value,sort_keys=True)+"\n")

def load_jsonl(path:Path)->list[dict[str,Any]]:
    if not path.exists(): return []
    out=[]
    for n,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        try: v=json.loads(line)
        except json.JSONDecodeError as exc: raise HarnessError(f"{path}:{n}: invalid JSONL") from exc
        if not isinstance(v,dict): raise HarnessError(f"{path}:{n}: expected object")
        out.append(v)
    return out

def sha256_file(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()

@dataclass(frozen=True)
class RoutingTruth:
    case_id:str
    disposition:str
    capabilities:frozenset[str]|None
    admissible_capability_sets:tuple[frozenset[str],...]=()
    critical_permission_boundary:bool=False

@dataclass(frozen=True)
class Observation:
    case_id:str
    candidate_id:str
    repetition:str
    phase:str
    observed_disposition:str
    observed_activation_set:frozenset[str]
    observed_capability_set:frozenset[str]
    clarification_requested:bool
    bounded_refusal:bool
    context_bytes:int
    latency_seconds:float
    provider_usage:dict[str,Any]
    technical_valid:bool
    task_success:bool|None=None

@dataclass(frozen=True)
class ScheduledObservation:
    phase:str
    case_id:str
    candidate_id:str
    repetition:str
    @property
    def key(self)->str: return f"{self.phase}:{self.case_id}:{self.candidate_id}:{self.repetition}"

def project_capabilities(topologies:dict[str,Any],candidate_id:str,capabilities:Sequence[str])->frozenset[str]:
    candidate=topologies.get("candidates",{}).get(candidate_id)
    if not candidate: raise HarnessError(f"unknown candidate: {candidate_id}")
    mapping=candidate.get("capability_to_entrypoints",{})
    result=set()
    for cap in capabilities:
        if cap not in CAPABILITIES or cap not in mapping: raise HarnessError(f"unknown/unmapped capability: {cap}")
        result.update(mapping[cap])
    return frozenset(result)

def validate_topologies(topologies:dict[str,Any])->None:
    if topologies.get("topology_revision")!="MG1-T023-TOPOLOGIES-v4": raise HarnessError("unexpected topology revision")
    if tuple(topologies.get("candidates",{}).keys())!=CANDIDATES: raise HarnessError("candidate topology set/order drift")
    for candidate in CANDIDATES:
        if set(topologies["candidates"][candidate].get("capability_to_entrypoints",{}))!=set(CAPABILITIES):
            raise HarnessError(f"{candidate}: incomplete capability projection")

def validate_model_visible_instrumentation(instrumentation:dict[str,Any])->None:
    routing=instrumentation["routing_only"]
    visible=json.dumps({"suffix":routing["planning_suffix"],"schema":routing["output_schema"]},sort_keys=True).casefold()
    forbidden={"agent governance","agent-governance","consumer-lifecycle","source-maintainer","external-skill-trust","consumer-governance",'"b2"','"f2"','"g3"',"routing_disposition","selected_capabilities","activated_entrypoints","task_success","semantic_outcome"}
    hits=sorted(x for x in forbidden if x in visible)
    if hits: raise HarnessError(f"routing-only model-visible leakage: {hits}")
    required={"clarification_requested","bounded_refusal","response_summary"}
    schema=routing["output_schema"]
    if set(schema.get("required",[]))!=required or set(schema.get("properties",{}))!=required:
        raise HarnessError("routing-only schema field drift")
    e2e_required={"clarification_requested","bounded_refusal","task_success","response_summary"}
    e2e=instrumentation["e2e"]["output_schema"]
    if set(e2e.get("required",[]))!=e2e_required or set(e2e.get("properties",{}))!=e2e_required:
        raise HarnessError("e2e schema field drift")

def validate_frozen_baseline()->dict[str,Any]:
    missing=[p.relative_to(REPO_ROOT).as_posix() for p in FREEZE_I_REQUIRED if not p.is_file()]
    if missing: raise HarnessError(f"Freeze I required files missing: {missing}")
    plan,routing,prov,topo,dev,inst=(load_json(p) for p in (ANALYSIS_PATH,ROUTING_PATH,PROVENANCE_PATH,TOPOLOGIES_PATH,DEVELOPMENT_PATH,INSTRUMENTATION_PATH))
    validate_topologies(topo); validate_model_visible_instrumentation(inst)
    if prov.get("candidate_freeze_source")!="5b025087bc7b6996f683a34fdd1ce441d3d6dd82": raise HarnessError("candidate Freeze E provenance drift")
    if prov.get("presentations_tree_source")!="bdbcf3eb4b1b3acf74e8ec9c36d58400e60efda3": raise HarnessError("candidate presentation tree provenance drift")
    if prov.get("topologies_blob_source")!="1adb4c156bb03e39dd9bf8c2443c501c82f31f5f": raise HarnessError("topology blob provenance drift")
    if sum(int(f["count"]) for f in dev.get("case_families",[]))!=90 or dev.get("confirmatory") is not False: raise HarnessError("development boundary drift")
    geometry={"candidates":3,"development_cases":90,"routing_confirmatory_cases":270,"primary_backbone_cases":240,"challenge_cases":30,"reliability_subset_cases":30,"e2e_reserve_cases":60,"max_e2e_finalists":2}
    if plan["geometry"]!=geometry: raise HarnessError("analysis geometry drift")
    b=plan["attempt_budget"]
    if b["scientific_base_max"]+b["behavioral_preflight_max_attempts"]+b["synthetic_canary_max_attempts"]+b["retry_reserve_after_nominal_and_preflight_canary"]!=b["absolute_stage6_provider_model_attempt_ceiling"]: raise HarnessError("attempt budget arithmetic drift")
    if plan["e2e_estimand"]["conditional_denominator"]!="same-observation exact_routing_correct == true": raise HarnessError("e2e denominator drift")
    gate=plan["behavioral_gates"]["synthetic_canary"]
    if gate["logical_cases"]!=2 or gate["required_logical_passes"]!=2: raise HarnessError("synthetic canary must require 2/2 logical PASS")
    if "authoritative" in routing["observation_authority"]["model_self_report"].casefold() and not routing["observation_authority"]["model_self_report"].casefold().startswith("diagnostic"):
        raise HarnessError("model self-report cannot be routing authority")
    return {"status":"PASS","evaluation_id":plan["evaluation_id"],"development_cases":90,"provider_model_calls":0}

def validate_freeze_i()->dict[str,Any]:
    result=validate_frozen_baseline()
    leaked=[p.relative_to(REPO_ROOT).as_posix() for p in FREEZE_I_FORBIDDEN if p.exists()]
    if leaked and len(leaked)!=len(FREEZE_I_FORBIDDEN):
        raise HarnessError(f"incomplete confirmatory Freeze J boundary: {leaked}")
    return {**result,"confirmatory_assets_present":bool(leaked)}

def validate_preconfirmatory_freeze_i()->dict[str,Any]:
    result=validate_frozen_baseline()
    leaked=[p.relative_to(REPO_ROOT).as_posix() for p in FREEZE_I_FORBIDDEN if p.exists()]
    if leaked: raise HarnessError(f"confirmatory assets exist before Freeze I: {leaked}")
    return {**result,"confirmatory_assets_present":False}
