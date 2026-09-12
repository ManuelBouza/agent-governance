#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def _schedule(): return {a['arm_id']:a for a in json.loads((ROOT/'schedule.json').read_text())['arms']}
def validate_result(r):
    a=_schedule().get(r.get('arm_id'))
    if not a: raise ValueError('unknown arm_id')
    for k in ('variant_id','model','reasoning','speed'):
        if r.get(k)!=a[k]: raise ValueError(f'{k} mismatch')
    if r.get('children_used')!=0: raise ValueError('children forbidden')
    u=r['usage']; total=u['uncached_input_tokens']+u['cached_input_tokens']+u['output_reasoning_tokens']
    if u['total_tokens']!=total: raise ValueError('token aggregate mismatch')
    seg_total=sum(x['uncached_input_tokens']+x['cached_input_tokens']+x['output_reasoning_tokens'] for x in u.get('segments',[]))
    if seg_total!=u['total_tokens']: raise ValueError('usage segments do not reconcile')
    models={x['model'] for x in u.get('segments',[])}
    if a['model']=='gpt-5.6-terra' and models-{'gpt-5.6-terra'}: raise ValueError('Terra arm contaminated by another model')
    if a['model']=='gpt-5.6-sol' and models-{'gpt-5.6-sol'}: raise ValueError('Sol arm contaminated by another model')
    c=r['credits']
    if c['source']=='DERIVED' and not c.get('rate_card_id'): raise ValueError('derived credits require frozen rate_card_id')
    return True

def phase_gate(results):
    for r in results:
        validate_result(r)
        if not r['accepted'] or r.get('protocol_violations'): return 'NOT_QUALIFIED'
    return 'PASSED'

def ecaw(results):
    accepted=sum(1 for r in results if r['accepted'])
    return None if not accepted else sum(r['credits']['total'] for r in results)/accepted
