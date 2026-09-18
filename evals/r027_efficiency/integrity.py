from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def _l(n):return json.loads((ROOT/n).read_text(encoding="utf-8"))
def validate()->list[str]:
 p=[];m=_l("manifest.json");pairs=_l("pairs.json");tasks=_l("tasks.json");s=_l("schedule.json");o=_l("oracles.json")
 if m["pair_count"]!=9 or len(pairs)!=9:p.append("pair count")
 if m["arm_count"]!=18 or len(tasks)!=18:p.append("arm count")
 ids=[t["arm_id"] for t in tasks]
 if len(ids)!=len(set(ids)):p.append("unique ids")
 scheduled=[a for ph in s["phases"] for a in ph["arm_order"]]
 if sorted(scheduled)!=sorted(ids):p.append("schedule coverage")
 if set(o["arms"])!=set(ids):p.append("oracle coverage")
 for pair in pairs:
  ms=[t for t in tasks if t["pair_id"]==pair["pair_id"]]
  if len(ms)!=2 or ms[0]["archetype"]!=ms[1]["archetype"] or ms[0]["expected_changed_paths"]!=ms[1]["expected_changed_paths"]:p.append(pair["pair_id"]+" isomorphism")
 for ph in s["phases"]:
  roles=[]
  for arm in ph["arm_order"][::2]:roles.append(next(t["role"] for t in tasks if t["arm_id"]==arm))
  if len(set(roles))<2:p.append(f'phase {ph["phase"]} counterbalance')
 return p
if __name__=="__main__":
 x=validate()
 if x:raise SystemExit("\n".join(x))
 print("T066 Freeze A integrity: PASS")
