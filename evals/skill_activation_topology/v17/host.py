from __future__ import annotations
import hashlib,json,re,shutil,subprocess,time
from pathlib import Path
from typing import Any,Sequence
from .core import REPO_ROOT,HarnessError,sha256_file

def _copy_verified(source:Path,target:Path)->dict[str,Any]:
    target.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(source,target)
    before,after=source.read_bytes(),target.read_bytes()
    if before!=after: raise HarnessError(f"copy verification failed: {source}")
    return {"source":source.relative_to(REPO_ROOT).as_posix(),"target":target.as_posix(),"bytes":len(before),"sha256":hashlib.sha256(before).hexdigest()}

def materialize_candidate(manifest:dict[str,Any],provenance:dict[str,Any],candidate_id:str,workspace:Path)->dict[str,Any]:
    candidate=manifest.get("candidates",{}).get(candidate_id)
    if not candidate: raise HarnessError(f"unknown candidate: {candidate_id}")
    expected=provenance["target_files"]; records=[]; root=workspace/".agents"/"skills"
    for entrypoint,data in candidate["entrypoints"].items():
        source=REPO_ROOT/data["skill_source"]; row=expected.get(data["skill_source"])
        if not row or sha256_file(source)!=row["sha256"]: raise HarnessError(f"candidate byte drift: {data['skill_source']}")
        records.append(_copy_verified(source,root/entrypoint/"SKILL.md"))
        for cap in data["capabilities"]:
            rel=manifest["shared_references"][cap]; refrow=expected.get(rel)
            if not refrow or sha256_file(REPO_ROOT/rel)!=refrow["sha256"]: raise HarnessError(f"reference byte drift: {rel}")
            records.append(_copy_verified(REPO_ROOT/rel,root/entrypoint/"references"/f"{cap}.md"))
    return {"candidate_id":candidate_id,"records":records}

def materialize_fixture(case:dict[str,Any],workspace:Path)->dict[str,Any]:
    fixture=case.get("fixture",{}); records=[]
    for rel in fixture.get("directories",[]): (workspace/rel).mkdir(parents=True,exist_ok=True); records.append({"path":rel,"kind":"directory"})
    for spec in fixture.get("files",[]):
        target=workspace/spec["path"]; target.parent.mkdir(parents=True,exist_ok=True)
        payload=json.dumps(spec["json"],indent=2,sort_keys=True)+"\n" if "json" in spec else str(spec.get("text",""))
        target.write_text(payload,encoding="utf-8",newline="\n")
        records.append({"path":spec["path"],"kind":"file","sha256":hashlib.sha256(payload.encode()).hexdigest()})
    return {"records":records}

def codex_version(command:str)->str:
    r=subprocess.run([command,"--version"],capture_output=True,text=True,check=False,timeout=30)
    if r.returncode: raise HarnessError(f"cannot resolve Codex CLI version: {r.stderr.strip()}")
    return r.stdout.strip()

def build_codex_command(*,codex_command:str,workspace:Path,model:str,effort:str,backend:str,sandbox:str,schema_path:Path,final_path:Path)->list[str]:
    return [codex_command,"exec","--json","--ignore-user-config","--ignore-rules","--strict-config","--color","never","--sandbox",sandbox,"--ephemeral","--skip-git-repo-check","--cd",str(workspace),"--model",model,"--config",f'model_reasoning_effort="{effort}"',"--config",'web_search="disabled"',"--config",f'windows.sandbox="{backend}"',"--output-schema",str(schema_path),"--output-last-message",str(final_path),"-"]

_READ_VERBS=re.compile(r"\b(get-content|cat|type|read_text|read_bytes|sed|head|tail)\b",re.I)

def parse_host_trace(stdout_jsonl:str,manifest:dict[str,Any],candidate_id:str)->dict[str,Any]:
    successful=[]; usage={}; trace_available=False
    for line in stdout_jsonl.splitlines():
        try: event=json.loads(line)
        except json.JSONDecodeError: continue
        if event.get("type")=="thread.started": trace_available=True
        if event.get("type")=="turn.completed" and isinstance(event.get("usage"),dict): usage=event["usage"]
        item=event.get("item") or {}
        if event.get("type")=="item.completed" and item.get("type")=="command_execution" and item.get("exit_code")==0:
            raw=item.get("command",""); command=raw if isinstance(raw,str) else json.dumps(raw,sort_keys=True)
            command=re.sub(r"[\\/]+","/",command).casefold()
            if _READ_VERBS.search(command): successful.append(command)
    candidate=manifest["candidates"][candidate_id]; activation=set(); caps=set(); paths=set()
    for entrypoint,data in candidate["entrypoints"].items():
        skill=f".agents/skills/{entrypoint.casefold()}/skill.md"
        if any(skill in c for c in successful): activation.add(entrypoint); paths.add(skill)
        for cap in data["capabilities"]:
            ref=f".agents/skills/{entrypoint.casefold()}/references/{cap.casefold()}.md"
            if any(ref in c for c in successful): caps.add(cap); paths.add(ref)
    return {"trace_available":trace_available,"observed_activation_set":sorted(activation),"observed_capability_set":sorted(caps),"read_paths":sorted(paths),"provider_usage":usage}

def derive_disposition(activation:Sequence[str],capabilities:Sequence[str],clarification_requested:bool)->str:
    if activation or capabilities: return "ROUTE"
    return "ABSTAIN" if clarification_requested else "NONE"

def context_bytes(workspace:Path,read_paths:Sequence[str])->int:
    return sum((workspace/rel).stat().st_size for rel in set(read_paths) if (workspace/rel).is_file())

def execute_codex(*,prompt:str,output_schema:dict[str,Any],manifest:dict[str,Any],candidate_id:str,workspace:Path,codex_command:str,model:str,effort:str,backend:str,sandbox:str,timeout_seconds:int)->dict[str,Any]:
    schema_path=workspace/"t065-output-schema.json"; final_path=workspace/"t065-final.json"
    schema_path.write_text(json.dumps(output_schema,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    command=build_codex_command(codex_command=codex_command,workspace=workspace,model=model,effort=effort,backend=backend,sandbox=sandbox,schema_path=schema_path,final_path=final_path)
    started=time.monotonic()
    try:
        completed=subprocess.run(command,input=prompt,capture_output=True,text=True,encoding="utf-8",errors="replace",check=False,timeout=timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        return {"technical_valid":False,"timed_out":True,"returncode":-1,"stdout_jsonl":exc.stdout or "","stderr":exc.stderr or "","latency_seconds":time.monotonic()-started,"provider_usage":{},"trace_available":False}
    trace=parse_host_trace(completed.stdout,manifest,candidate_id); model_result=None; parse_error=None
    if final_path.exists():
        try: model_result=json.loads(final_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError,OSError) as exc: parse_error=str(exc)
    valid=completed.returncode==0 and trace["trace_available"] and isinstance(model_result,dict) and parse_error is None
    return {"technical_valid":valid,"timed_out":False,"returncode":completed.returncode,"stdout_jsonl":completed.stdout,"stderr":completed.stderr,"latency_seconds":time.monotonic()-started,"model_result":model_result,"parse_error":parse_error,**trace}
