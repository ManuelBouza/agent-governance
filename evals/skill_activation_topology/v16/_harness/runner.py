"""Materialized Stage-6 controller for T023 v16.

This controller does not authorize provider use. It executes only after a separate
Human launch supplies the exact live cell and provider envelope.
"""
from __future__ import annotations
import hashlib
import tempfile
from pathlib import Path
from typing import Any
from .analysis import e2e_analysis, routing_analysis
from .codex_adapter import codex_version, execute_codex
from .materialization import materialize_candidate, materialize_fixture
from .models import ANALYSIS_PATH, CORPUS_PATH, ENVELOPE_PATH, ORACLE_PATH, PRESENTATION_MANIFEST_PATH, ROUTING_PATH, TOPOLOGIES_PATH, HarnessError, RoutingObservation, RoutingTruth, load_json
from .scheduler import AttemptBudget, e2e_schedule, reliability_schedule, routing_first_schedule
from .storage import append_jsonl, dump_json, load_jsonl

def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_inputs() -> dict[str, Any]:
    required = (ANALYSIS_PATH, ROUTING_PATH, TOPOLOGIES_PATH, PRESENTATION_MANIFEST_PATH, CORPUS_PATH, ORACLE_PATH, ENVELOPE_PATH)
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise HarnessError(f'missing frozen v16 inputs: {missing}')
    return {'analysis': load_json(ANALYSIS_PATH), 'routing': load_json(ROUTING_PATH), 'topologies': load_json(TOPOLOGIES_PATH), 'manifest': load_json(PRESENTATION_MANIFEST_PATH), 'corpus': load_json(CORPUS_PATH), 'oracle': load_json(ORACLE_PATH), 'envelope': load_json(ENVELOPE_PATH), 'hashes': {p.name: _sha(p) for p in required}}

def truths_from_oracle(oracle: dict[str, Any]) -> dict[str, RoutingTruth]:
    out = {}
    for case_id, item in oracle['cases'].items():
        caps = item.get('capability_truth')
        out[case_id] = RoutingTruth(case_id=case_id, disposition=item['routing_disposition'], capabilities=None if caps is None else frozenset(caps), admissible_capability_sets=tuple((frozenset(x) for x in item.get('admissible_capability_sets', []))), critical_permission_boundary=bool(item.get('critical_permission_boundary', False)), expected_semantic_outcome=item.get('expected_semantic_outcome'))
    return out

def _case_map(corpus: dict[str, Any]) -> dict[str, dict[str, Any]]:
    cases = [*corpus['routing_cases'], *corpus['e2e_reserve']]
    return {case['id']: case for case in cases}

def _observation_from_record(record: dict[str, Any]) -> RoutingObservation:
    return RoutingObservation(case_id=record['case_id'], candidate_id=record['candidate_id'], repetition=record['repetition'], phase=record['phase'], observed_disposition=record['observed_disposition'], observed_activation_set=frozenset(record['observed_activation_set']), observed_capability_set=frozenset(record['observed_capability_set']), clarification_requested=bool(record['clarification_requested']), critical_permission_violation=bool(record['critical_permission_violation']), context_bytes=int(record['context_bytes']), latency_seconds=float(record['latency_seconds']), provider_usage=record.get('provider_usage', {}), technical_valid=bool(record['technical_valid']), task_success=record.get('task_success'), semantic_outcome=record.get('semantic_outcome'))

def _context_bytes(workspace: Path, read_paths: list[str]) -> int:
    total = 0
    for rel in set(read_paths):
        path = workspace / rel
        if path.is_file():
            total += path.stat().st_size
    return total

def _run_one(spec, *, inputs: dict[str, Any], case: dict[str, Any], budget: AttemptBudget, args: Any, attempt_log: Path) -> dict[str, Any]:
    envelope = inputs['envelope']
    phase = spec.phase
    suffix = envelope['routing_suffix'] if phase in {'routing', 'reliability', 'preflight', 'canary'} else envelope['e2e_suffix']
    prompt = case['prompt'].rstrip() + '\n\n' + suffix
    max_attempts = inputs['analysis']['attempt_budget']['max_attempts_per_scientific_observation'] if phase in {'routing', 'reliability', 'e2e'} else 2
    last = None
    for attempt in range(1, int(max_attempts) + 1):
        budget.consume()
        with tempfile.TemporaryDirectory(prefix=f't064-{phase}-') as raw:
            workspace = Path(raw)
            candidate_evidence = materialize_candidate(inputs['manifest'], spec.candidate_id, workspace)
            fixture_evidence = materialize_fixture(envelope, case['fixture_role'], workspace)
            result = execute_codex(prompt=prompt, manifest=inputs['manifest'], candidate_id=spec.candidate_id, workspace=workspace, codex_command=args.codex_command, model=args.model, effort=args.effort, backend=args.backend, sandbox=args.sandbox, timeout_seconds=args.timeout_seconds)
            model = result.get('model_result') or {}
            record = {'phase': phase, 'case_id': case['id'], 'candidate_id': spec.candidate_id, 'repetition': spec.repetition, 'attempt': attempt, 'technical_valid': bool(result.get('technical_valid')), 'observed_disposition': model.get('routing_disposition', 'INVALID'), 'observed_activation_set': result.get('observed_activation_set', []), 'observed_capability_set': result.get('observed_capability_set', []), 'clarification_requested': bool(model.get('clarification_requested', False)), 'critical_permission_violation': bool(model.get('permission_broadening', False)), 'task_success': model.get('task_success'), 'semantic_outcome': model.get('semantic_outcome'), 'response_summary': model.get('response_summary'), 'context_bytes': _context_bytes(workspace, result.get('read_paths', [])), 'latency_seconds': result.get('latency_seconds', 0.0), 'provider_usage': result.get('provider_usage', {}), 'returncode': result.get('returncode'), 'timed_out': result.get('timed_out', False), 'candidate_materialization': candidate_evidence, 'fixture_materialization': fixture_evidence}
            append_jsonl(attempt_log, record)
            last = record
            if record['technical_valid']:
                return record
    assert last is not None
    return last

def _run_schedule(schedule, *, inputs, case_map, budget, args, output, completed):
    valid_path = output / 'observations.jsonl'
    attempts = output / 'attempts.jsonl'
    for spec in schedule:
        if spec.key in completed:
            continue
        record = _run_one(spec, inputs=inputs, case=case_map[spec.case_id], budget=budget, args=args, attempt_log=attempts)
        if not record['technical_valid']:
            raise HarnessError(f'technical observation failure after retry allowance: {spec.key}')
        record['logical_key'] = spec.key
        append_jsonl(valid_path, record)
        completed.add(spec.key)
        dump_json(output / 'budget.json', {'attempts_used': budget.used, 'attempt_ceiling': budget.ceiling})

def validate_live_cell(args: Any, inputs: dict[str, Any]) -> None:
    actual = codex_version(args.codex_command)
    if actual != args.required_codex_version:
        raise HarnessError(f'Codex CLI mismatch: expected {args.required_codex_version}, got {actual}')
    if args.timeout_seconds <= 0:
        raise HarnessError('timeout must be positive')

def run_full(args: Any) -> int:
    inputs = load_inputs()
    validate_live_cell(args, inputs)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    metadata_path = output / 'run-metadata.json'
    if metadata_path.exists():
        metadata = load_json(metadata_path)
        if metadata['frozen_asset_sha256'] != inputs['hashes']:
            raise HarnessError('resume frozen-asset drift')
        if metadata['live_cell'] != {'model': args.model, 'effort': args.effort, 'codex_cli': args.required_codex_version, 'backend': args.backend, 'sandbox': args.sandbox}:
            raise HarnessError('resume live-cell drift')
    else:
        metadata = {'status': 'RUNNING', 'evaluation_id': 'MG1-T023-EVALUATION-v16', 'frozen_asset_sha256': inputs['hashes'], 'live_cell': {'model': args.model, 'effort': args.effort, 'codex_cli': args.required_codex_version, 'backend': args.backend, 'sandbox': args.sandbox}}
        dump_json(metadata_path, metadata)
    valid = load_jsonl(output / 'observations.jsonl')
    completed = {r['logical_key'] for r in valid if r.get('technical_valid') and r.get('logical_key')}
    attempts_used = len(load_jsonl(output / 'attempts.jsonl'))
    budget = AttemptBudget(inputs['analysis'], attempts_used)
    cases = _case_map(inputs['corpus'])
    truths = truths_from_oracle(inputs['oracle'])
    from .scheduler import ScheduledObservation
    preflight = [ScheduledObservation('preflight', c['id'], c['candidate_id'], 'p1') for c in inputs['envelope']['behavioral_preflight_cases']]
    canary = [ScheduledObservation('canary', c['id'], c['candidate_id'], 'c1') for c in inputs['envelope']['synthetic_canary_cases']]
    extra_cases = {c['id']: c for c in [*inputs['envelope']['behavioral_preflight_cases'], *inputs['envelope']['synthetic_canary_cases']]}
    _run_schedule(preflight, inputs=inputs, case_map=extra_cases, budget=budget, args=args, output=output, completed=completed)
    _run_schedule(canary, inputs=inputs, case_map=extra_cases, budget=budget, args=args, output=output, completed=completed)
    _run_schedule(routing_first_schedule(inputs['corpus']), inputs=inputs, case_map=cases, budget=budget, args=args, output=output, completed=completed)
    _run_schedule(reliability_schedule(inputs['corpus'], inputs['oracle']), inputs=inputs, case_map=cases, budget=budget, args=args, output=output, completed=completed)
    observations = [_observation_from_record(r) for r in load_jsonl(output / 'observations.jsonl') if r['phase'] in {'routing', 'reliability', 'e2e'}]
    routing_result = routing_analysis(observations, truths, inputs['corpus'], inputs['topologies'], inputs['analysis'])
    dump_json(output / 'routing-analysis.json', routing_result)
    dump_json(output / 'finalists.json', {'status': routing_result['status'], 'finalists': routing_result['finalists']})
    if not routing_result['finalists']:
        metadata.update(status='COMPLETE_NO_TOPOLOGY_SELECTED', attempts_used=budget.used)
        dump_json(metadata_path, metadata)
        return 0
    _run_schedule(e2e_schedule(inputs['corpus'], routing_result['finalists']), inputs=inputs, case_map=cases, budget=budget, args=args, output=output, completed=completed)
    observations = [_observation_from_record(r) for r in load_jsonl(output / 'observations.jsonl') if r['phase'] in {'routing', 'reliability', 'e2e'}]
    final = e2e_analysis(observations, routing_result, truths, inputs['corpus'], inputs['analysis'])
    dump_json(output / 'selection.json', final)
    metadata.update(status='COMPLETE', attempts_used=budget.used, selected_candidate=final.get('selected'))
    dump_json(metadata_path, metadata)
    return 0
