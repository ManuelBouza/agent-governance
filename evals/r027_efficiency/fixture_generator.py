from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def _w(p:Path,t:str)->None:
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding="utf-8")

def render_arm(task:dict,d:Path)->None:
 token=task["variant_token"];arch=task["archetype"];_w(d/"pyproject.toml",'[tool.pytest.ini_options]\npythonpath = ["."]\n');_w(d/"src/__init__.py","")
 if arch=="A":
  _w(d/"src/subject.py","def normalize_name(value: str) -> str:\n    return value.lower()\n");_w(d/"tests/test_subject.py",f"from src.subject import normalize_name\n\ndef test_existing_case_behavior():\n    assert normalize_name({token.upper()!r}) == {token!r}\n")
 elif arch=="B":
  old=f"retry_count_{token}";_w(d/"src/settings.py",f"SETTINGS = {{{old!r}: 3}}\n");_w(d/"src/consumer.py",f"from .settings import SETTINGS\n\ndef retry_budget() -> int:\n    return SETTINGS[{old!r}]\n");_w(d/"tests/test_consumer.py","from src.consumer import retry_budget\n\ndef test_existing_retry_budget():\n    assert retry_budget() == 3\n")
 elif arch=="C":
  _w(d/"src/cli.py","def run(argv: list[str]) -> str:\n    if len(argv) == 2 and argv[0] == 'echo':\n        return argv[1]\n    raise ValueError('unsupported command')\n");_w(d/"tests/test_cli.py",f"from src.cli import run\n\ndef test_existing_echo():\n    assert run(['echo', {token!r}]) == {token!r}\n")
 else: raise ValueError(arch)
 _w(d/"TASK.json",json.dumps(task,indent=2,sort_keys=True)+"\n")

def materialize_all(root:Path)->list[Path]:
 tasks=json.loads((ROOT/"tasks.json").read_text(encoding="utf-8"));out=[]
 for task in tasks:
  d=root/task["arm_id"];render_arm(task,d);out.append(d)
 return out

if __name__=="__main__":
 import argparse
 p=argparse.ArgumentParser();p.add_argument("destination",type=Path);a=p.parse_args();materialize_all(a.destination)
