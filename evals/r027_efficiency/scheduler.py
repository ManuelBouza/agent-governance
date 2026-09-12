#!/usr/bin/env python3
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def load(): return json.loads((ROOT/'schedule.json').read_text())
def next_arm(completed,phase_gates):
    s=load(); done=set(completed)
    for arm in s['arms']:
        if arm['arm_id'] in done: continue
        p=arm['phase']
        if p>1 and phase_gates.get(str(p-1))!='PASSED': raise RuntimeError(f'phase {p} blocked: prior phase not PASSED')
        earlier=[a['arm_id'] for a in s['arms'] if a['sequence']<arm['sequence']]
        if any(x not in done for x in earlier): raise RuntimeError('earlier scheduled arm missing; fail closed')
        return arm
    return None

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--completed',default=''); ap.add_argument('--phase1'); ap.add_argument('--phase2'); a=ap.parse_args()
    arm=next_arm([x for x in a.completed.split(',') if x],{'1':a.phase1,'2':a.phase2}); print(json.dumps(arm,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
