#!/usr/bin/env python3
import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def load(p): return json.loads((ROOT/p).read_text())
def main():
    f=load('freeze_a.json'); s=load('schedule.json'); idx=load('pairs.json'); o=load('oracles.json')
    pairs=[]
    for p in idx['pair_files']: pairs+=load(p)['pairs']
    assert f['pair_count']==9 and f['arm_ceiling']==18 and len(pairs)==9 and len(s['arms'])==18
    variants=[v['variant_id'] for p in pairs for v in p['variants']]
    assert len(variants)==18 and len(set(variants))==18 and set(variants)==set(o['variants'])
    assert [a['sequence'] for a in s['arms']]==list(range(1,19))
    assert all(a['children_allowed']==0 and a['reasoning']=='medium' and a['speed']=='standard' for a in s['arms'])
    env=load('launch-envelope.json'); assert env['codex_effective_config_requirements']['agents.enabled'] is False
    assert env['instruction_control']['required_effective_project_budget_bytes']>=f['authoritative_refs']['agents_bytes']
    rate=load('receipts/rate-card.json'); assert rate['derivation_authorized'] is False
    manifest=load('manifest.json') if (ROOT/'manifest.json').exists() else None
    if manifest:
        for path,sha in manifest['git_blob_sha1'].items():
            got=subprocess.check_output(['git','hash-object',str(ROOT/path)],text=True).strip(); assert got==sha,(path,got,sha)
    print('T066 Freeze A integrity: PASS'); return 0
if __name__=='__main__': raise SystemExit(main())
