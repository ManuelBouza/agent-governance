"""Provider-free Freeze-G integrity guard for T023 v16."""
from __future__ import annotations
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any
ROOT = Path(__file__).resolve().parents[3]
V16 = Path(__file__).resolve().parent
FREEZE_E = '5b025087bc7b6996f683a34fdd1ce441d3d6dd82'
G_PATHS = {'evals/skill_activation_topology/v16/candidate-hashes.json', 'evals/skill_activation_topology/v16/capability-routing.json', 'evals/skill_activation_topology/v16/analysis-plan.json', 'evals/skill_activation_topology/v16/development.json', 'evals/skill_activation_topology/v16/topologies.json', 'evals/skill_activation_topology/v16/presentation-manifest.json', 'evals/skill_activation_topology/v16/harness.py', 'evals/skill_activation_topology/v16/_harness/models.py', 'evals/skill_activation_topology/v16/_harness/projection.py', 'evals/skill_activation_topology/v16/_harness/statistics.py', 'evals/skill_activation_topology/v16/_harness/scoring.py', 'evals/skill_activation_topology/v16/_harness/analysis.py', 'evals/skill_activation_topology/v16/_harness/scheduler.py', 'evals/skill_activation_topology/v16/_harness/storage.py', 'evals/skill_activation_topology/v16/_harness/materialization.py', 'evals/skill_activation_topology/v16/_harness/codex_adapter.py', 'evals/skill_activation_topology/v16/_harness/runner.py', 'evals/skill_activation_topology/v16/__init__.py', 'evals/skill_activation_topology/v16/_harness/__init__.py', 'tests/test_t023_v16_projection.py', 'tests/test_t023_v16_statistics.py', 'tests/test_t023_v16_scoring.py', 'tests/test_t023_v16_scheduler.py'}
CONFIRMATORY = {'evals/skill_activation_topology/v16/corpus.json', 'evals/skill_activation_topology/v16/oracle.json', 'evals/skill_activation_topology/v16/trial-envelope.json'}

def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=ROOT, stderr=subprocess.STDOUT, text=True)

def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding='utf-8'))
    assert isinstance(value, dict)
    return value

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    hashes = load(V16 / 'candidate-hashes.json')
    routing = load(V16 / 'capability-routing.json')
    plan = load(V16 / 'analysis-plan.json')
    dev = load(V16 / 'development.json')
    topo = load(V16 / 'topologies.json')
    assert hashes['identity'] == 'MG1-T023-CANDIDATE-HASHES-v4' and hashes['candidate_freeze_source'] == FREEZE_E
    assert hashes['candidate_ids'] == ['B2', 'F2', 'G3']
    for rel, item in hashes['files'].items():
        assert sha(ROOT / rel) == item['sha256'], rel
    assert routing['identity'] == 'MG1-T023-CAPABILITY-ROUTING-v1' and routing['capabilities'] == ['consumer-lifecycle', 'source-maintainer', 'external-skill-trust']
    assert set(routing['dispositions']) == {'ROUTE', 'NONE', 'ABSTAIN'} and routing['multi_label'] is True
    assert topo['topology_revision'] == 'MG1-T023-TOPOLOGIES-v4' and list(topo['candidates']) == ['B2', 'F2', 'G3']
    assert plan['geometry'] == {'development_cases': 90, 'routing_confirmatory_cases': 270, 'primary_backbone_cases': 240, 'challenge_cases': 30, 'reliability_subset_cases': 30, 'e2e_reserve_cases': 60, 'candidates': 3, 'max_e2e_finalists': 2}
    assert plan['attempt_budget']['absolute_stage6_provider_model_attempt_ceiling'] == 1264
    assert sum((int(family['count']) for family in dev['case_families'])) == 90 and dev['case_count'] == 90 and (dev['confirmatory'] is False)
    freeze_g = git('log', '-1', '--format=%H', '--', *sorted(G_PATHS)).strip()
    assert freeze_g
    for rel in CONFIRMATORY:
        probe = subprocess.run(['git', 'cat-file', '-e', f'{freeze_g}:{rel}'], cwd=ROOT, capture_output=True, text=True)
        assert probe.returncode != 0, f'confirmatory asset existed at Freeze G: {rel}'
    drift = set(filter(None, git('diff', '--name-only', freeze_g, 'HEAD').splitlines())) & G_PATHS
    assert not drift, f'Freeze G semantic drift: {sorted(drift)}'
    print(json.dumps({'status': 'PASS', 'freeze_g': freeze_g, 'candidate_files': len(hashes['files']), 'development_cases': 90, 'provider_model_calls': 0}, sort_keys=True))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
