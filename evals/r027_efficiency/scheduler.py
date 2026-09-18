from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def load_schedule()->dict:return json.loads((ROOT/"schedule.json").read_text(encoding="utf-8"))
def phase_arms(phase:int)->list[str]:
 for item in load_schedule()["phases"]:
  if item["phase"]==phase:return list(item["arm_order"])
 raise ValueError(phase)
def assert_phase_allowed(phase:int,prior_passed:bool)->None:
 if phase>1 and not prior_passed:raise RuntimeError(f"phase {phase} blocked until prior gate passes")
