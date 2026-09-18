from __future__ import annotations
import importlib,importlib.util,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];EVAL=ROOT/"evals"/"r027_efficiency"

def mod(n,f):
 s=importlib.util.spec_from_file_location(n,EVAL/f);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m

def _clear_src_modules():
 for name in list(sys.modules):
  if name=="src" or name.startswith("src."):sys.modules.pop(name,None)

def _workspace_import(workspace:Path,module_name:str):
 _clear_src_modules();sys.path.insert(0,str(workspace))
 try:return importlib.import_module(module_name)
 finally:sys.path.pop(0)

def test_geometry():assert mod("i","integrity.py").validate()==[]

def test_generator_materializes_all_arms(tmp_path):
 fg=mod("fg","fixture_generator.py");created=fg.materialize_all(tmp_path);assert len(created)==18
 for t in json.loads((EVAL/"tasks.json").read_text()):
  d=tmp_path/t["arm_id"];assert (d/"TASK.json").exists();assert (d/"pyproject.toml").exists();assert (d/"tests/test_acceptance.py").exists();assert not (d/"SOLUTION.patch").exists()
  for source in d.rglob("*.py"):compile(source.read_text(encoding="utf-8"),str(source),"exec")

def test_every_pair_is_isomorphic_on_declared_geometry():
 tasks=json.loads((EVAL/"tasks.json").read_text());pairs=json.loads((EVAL/"pairs.json").read_text())
 for p in pairs:
  ms=[t for t in tasks if t["pair_id"]==p["pair_id"]];assert len(ms)==2;assert ms[0]["archetype"]==ms[1]["archetype"];assert ms[0]["expected_changed_paths"]==ms[1]["expected_changed_paths"];assert ms[0]["variant_token"]!=ms[1]["variant_token"]

def test_clean_fixtures_preserve_baseline_but_require_target_delta(tmp_path):
 fg=mod("fg_baseline","fixture_generator.py");fg.materialize_all(tmp_path)
 for t in json.loads((EVAL/"tasks.json").read_text()):
  d=tmp_path/t["arm_id"];acc=t["acceptance"]
  if t["archetype"]=="A":
   subject=_workspace_import(d,"src.subject")
   assert subject.normalize_name(acc["preserved_input"])==acc["preserved_expected"]
   assert subject.normalize_name(acc["input"])!=acc["expected"]
  elif t["archetype"]=="B":
   settings=_workspace_import(d,"src.settings");consumer=importlib.import_module("src.consumer")
   assert consumer.retry_budget()==acc["retry_budget"];assert acc["old_key"] in settings.SETTINGS;assert acc["new_key"] not in settings.SETTINGS
  else:
   cli=_workspace_import(d,"src.cli")
   assert cli.run(acc["preserved_argv"])==acc["preserved_expected"]
   try:cli.run(acc["argv"])
   except ValueError:pass
   else:raise AssertionError(f'{t["arm_id"]}: clean fixture unexpectedly satisfies target delta')
 _clear_src_modules()

def test_scoring_thresholds_and_credit_derivation():
 s=mod("s","scoring.py");assert s.geometric_mean([.8,.8,.8])<=.80;assert s.geometric_mean([.81,.8,.8])>.80
 assert s.derive_credits({"credits":None,"uncached_input_tokens":1_000_000,"cached_input_tokens":0,"output_reasoning_tokens":0},{"uncached_input":100,"cached_input":10,"output_reasoning":500})==100.0
