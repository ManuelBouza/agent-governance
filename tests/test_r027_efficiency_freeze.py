from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];EVAL=ROOT/"evals"/"r027_efficiency"
def mod(n,f):
 s=importlib.util.spec_from_file_location(n,EVAL/f);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m
def test_geometry():assert mod("i","integrity.py").validate()==[]
def test_generator(tmp_path):
 fg=mod("fg","fixture_generator.py");created=fg.materialize_all(tmp_path);assert len(created)==18
 for t in json.loads((EVAL/"tasks.json").read_text()):
  d=tmp_path/t["arm_id"];assert (d/"TASK.json").exists();assert (d/"pyproject.toml").exists();assert not (d/"SOLUTION.patch").exists()
def test_pair_isomorphism():
 tasks=json.loads((EVAL/"tasks.json").read_text());pairs=json.loads((EVAL/"pairs.json").read_text())
 for p in pairs:
  ms=[t for t in tasks if t["pair_id"]==p["pair_id"]];assert len(ms)==2;assert ms[0]["archetype"]==ms[1]["archetype"];assert ms[0]["expected_changed_paths"]==ms[1]["expected_changed_paths"];assert ms[0]["variant_token"]!=ms[1]["variant_token"]
def test_scoring():
 s=mod("s","scoring.py");assert s.geometric_mean([.8,.8,.8])<=.80;assert s.geometric_mean([.81,.8,.8])>.80;assert s.derive_credits({"credits":None,"uncached_input_tokens":1_000_000,"cached_input_tokens":0,"output_reasoning_tokens":0},{"uncached_input":100,"cached_input":10,"output_reasoning":500})==100.0
