from __future__ import annotations
from pathlib import Path
import tempfile
from typing import Any, Sequence
from .core import ANALYSIS_PATH, ROUTING_PATH, PROVENANCE_PATH, TOPOLOGIES_PATH, MANIFEST_PATH, INSTRUMENTATION_PATH, CORPUS_PATH, ORACLE_PATH, ENVELOPE_PATH, RELIABILITY_PATH, FREEZE_I_REQUIRED, CANDIDATES, HarnessError, Observation, RoutingTruth, ScheduledObservation, append_jsonl, dump_json, load_json, load_jsonl, sha256_file, validate_freeze_i
from .host import codex_version, context_bytes, derive_disposition, execute_codex, materialize_candidate, materialize_fixture
from .scoring import routing_analysis, e2e_analysis

SCIENTIFIC_PHASES={"routing","reliability","e2e"}

class AttemptBudget:

    def __init__(self, plan: dict[str, Any], prior_attempts: Sequence[dict[str, Any]]=()):
        self.spec = plan['attempt_budget']
        self.used = len(prior_attempts)
        self.phase_used = {'preflight': sum((1 for x in prior_attempts if x.get('phase') == 'preflight')), 'canary': sum((1 for x in prior_attempts if x.get('phase') == 'canary'))}

    @property
    def ceiling(self) -> int:
        return int(self.spec['absolute_stage6_provider_model_attempt_ceiling'])

    def remaining_gate_attempts(self, phase: str) -> int:
        field = {'preflight': 'behavioral_preflight_max_attempts', 'canary': 'synthetic_canary_max_attempts'}[phase]
        return int(self.spec[field]) - self.phase_used[phase]

    def consume(self, phase: str) -> None:
        if self.used + 1 > self.ceiling:
            raise HarnessError('absolute provider/model attempt ceiling would be exceeded')
        if phase in self.phase_used:
            if self.remaining_gate_attempts(phase) <= 0:
                raise HarnessError(f'{phase} total attempt ceiling would be exceeded')
            self.phase_used[phase] += 1
        self.used += 1

def routing_first_schedule(corpus: dict[str, Any]) -> list[ScheduledObservation]:
    return [ScheduledObservation('routing', case['id'], candidate, 'r1') for case in corpus['routing_cases'] for candidate in CANDIDATES]

def reliability_schedule(corpus: dict[str, Any], reliability: dict[str, Any]) -> list[ScheduledObservation]:
    subset = reliability.get('case_ids', [])
    allowed = {case['id'] for case in corpus['routing_cases']}
    if len(subset) != 30 or len(set(subset)) != 30 or (not set(subset) <= allowed):
        raise HarnessError('invalid reliability subset')
    return [ScheduledObservation('reliability', case_id, candidate, 'r2') for case_id in subset for candidate in CANDIDATES]

def e2e_schedule(corpus: dict[str, Any], finalists: list[str]) -> list[ScheduledObservation]:
    if not 1 <= len(finalists) <= 2 or len(set(finalists)) != len(finalists):
        raise HarnessError('e2e requires one or two unique finalists')
    if set(finalists) - set(CANDIDATES):
        raise HarnessError('unknown finalist')
    return [ScheduledObservation('e2e', case['id'], candidate, 'r1') for case in corpus['e2e_reserve'] for candidate in finalists]

def truths_from_oracle(oracle: dict[str, Any]) -> dict[str, RoutingTruth]:
    out: dict[str, RoutingTruth] = {}
    for case_id, item in oracle['cases'].items():
        caps = item.get('capability_truth')
        out[case_id] = RoutingTruth(case_id=case_id, disposition=item['routing_disposition'], capabilities=None if caps is None else frozenset(caps), admissible_capability_sets=tuple((frozenset(x) for x in item.get('admissible_capability_sets', []))), critical_permission_boundary=bool(item.get('critical_permission_boundary', False)))
    return out

def observation_from_record(record: dict[str, Any]) -> Observation:
    return Observation(case_id=record['case_id'], candidate_id=record['candidate_id'], repetition=record['repetition'], phase=record['phase'], observed_disposition=record['observed_disposition'], observed_activation_set=frozenset(record['observed_activation_set']), observed_capability_set=frozenset(record['observed_capability_set']), clarification_requested=bool(record['clarification_requested']), bounded_refusal=bool(record['bounded_refusal']), context_bytes=int(record['context_bytes']), latency_seconds=float(record['latency_seconds']), provider_usage=record.get('provider_usage', {}), technical_valid=bool(record['technical_valid']), task_success=record.get('task_success'))

def _mode_for_phase(phase: str, case: dict[str, Any]) -> str:
    if phase in {'routing', 'reliability'}:
        return 'routing'
    if phase == 'e2e':
        return 'e2e'
    mode = case.get('mode')
    if mode not in {'routing', 'e2e'}:
        raise HarnessError(f'{phase} gate case must declare mode routing|e2e')
    return mode

def attempt_records_for(attempts: Sequence[dict[str, Any]], spec: ScheduledObservation) -> list[dict[str, Any]]:
    return [
        row for row in attempts
        if row.get('phase') == spec.phase
        and row.get('case_id') == spec.case_id
        and row.get('candidate_id') == spec.candidate_id
        and row.get('repetition') == spec.repetition
    ]

def observation_attempt_limit(spec: ScheduledObservation, inputs: dict[str, Any]) -> int:
    if spec.phase in SCIENTIFIC_PHASES:
        return int(inputs['analysis']['attempt_budget']['max_attempts_per_scientific_observation'])
    return 2

def remaining_observation_attempts(spec: ScheduledObservation, inputs: dict[str, Any], attempts: Sequence[dict[str, Any]]) -> int:
    return max(0, observation_attempt_limit(spec, inputs)-len(attempt_records_for(attempts,spec)))

def run_one(spec: ScheduledObservation, *, inputs: dict[str, Any], case: dict[str, Any], budget: AttemptBudget, args: Any, attempt_log: Path, attempts: list[dict[str, Any]]) -> dict[str, Any]:
    mode = _mode_for_phase(spec.phase, case)
    inst = inputs['instrumentation']['routing_only' if mode == 'routing' else 'e2e']
    suffix = inst['planning_suffix'] if mode == 'routing' else inst['execution_suffix']
    schema = inst['output_schema']
    prompt = case['prompt'].rstrip() + '\n\n' + suffix
    prior = attempt_records_for(attempts,spec)
    max_new = remaining_observation_attempts(spec,inputs,attempts)
    if spec.phase in {'preflight','canary'}:
        max_new=min(max_new,budget.remaining_gate_attempts(spec.phase))
    if max_new <= 0:
        raise HarnessError(f'observation attempt ceiling exhausted: {spec.key}')
    last: dict[str, Any] | None = None
    next_attempt=len(prior)+1
    for offset in range(max_new):
        budget.consume(spec.phase)
        with tempfile.TemporaryDirectory(prefix=f't065-{spec.phase}-') as raw:
            workspace = Path(raw)
            candidate_evidence = materialize_candidate(inputs['manifest'], inputs['provenance'], spec.candidate_id, workspace)
            fixture_evidence = materialize_fixture(case, workspace)
            result = execute_codex(prompt=prompt, output_schema=schema, manifest=inputs['manifest'], candidate_id=spec.candidate_id, workspace=workspace, codex_command=args.codex_command, model=args.model, effort=args.effort, backend=args.backend, sandbox=args.sandbox, timeout_seconds=args.timeout_seconds)
            model = result.get('model_result') or {}
            activation = result.get('observed_activation_set', [])
            capabilities = result.get('observed_capability_set', [])
            clarification = bool(model.get('clarification_requested', False))
            record = {'phase': spec.phase, 'case_id': case['id'], 'candidate_id': spec.candidate_id, 'repetition': spec.repetition, 'attempt': next_attempt+offset, 'technical_valid': bool(result.get('technical_valid')), 'observed_disposition': derive_disposition(activation, capabilities, clarification), 'observed_activation_set': activation, 'observed_capability_set': capabilities, 'clarification_requested': clarification, 'bounded_refusal': bool(model.get('bounded_refusal', False)), 'task_success': model.get('task_success') if mode == 'e2e' else None, 'response_summary': model.get('response_summary'), 'context_bytes': context_bytes(workspace, result.get('read_paths', [])), 'latency_seconds': result.get('latency_seconds', 0.0), 'provider_usage': result.get('provider_usage', {}), 'trace_available': bool(result.get('trace_available')), 'returncode': result.get('returncode'), 'timed_out': bool(result.get('timed_out', False)), 'candidate_materialization': candidate_evidence, 'fixture_materialization': fixture_evidence}
            append_jsonl(attempt_log, record)
            attempts.append(record)
            last = record
            if record['technical_valid']:
                return record
    assert last is not None
    return last

def behavioral_record_pass(record: dict[str, Any], case: dict[str, Any]) -> bool:
    if not record.get('technical_valid'):
        return False
    expected = case.get('expected_generic_evidence', {})
    for key, value in expected.items():
        if key not in {'clarification_requested', 'bounded_refusal', 'task_success'}:
            raise HarnessError(f'non-generic gate expectation: {key}')
        if record.get(key) != value:
            return False
    trace = case.get('expected_trace', {})
    if 'activation_empty' in trace:
        if bool(record.get('observed_activation_set')) == bool(trace['activation_empty']):
            return False
    if 'capability_reads_empty' in trace:
        if bool(record.get('observed_capability_set')) == bool(trace['capability_reads_empty']):
            return False
    return True

def evaluate_behavioral_gate(phase: str, records: list[dict[str, Any]], cases: list[dict[str, Any]], plan: dict[str, Any]) -> dict[str, Any]:
    by_id = {row['case_id']: row for row in records if row['phase'] == phase}
    passes = {case['id']: behavioral_record_pass(by_id[case['id']], case) if case['id'] in by_id else False for case in cases}
    if phase == 'canary':
        gate = plan['behavioral_gates']['synthetic_canary']
        required = gate['required_logical_passes']
        if len(cases) != gate['logical_cases']:
            raise HarnessError('canary logical-case geometry drift')
        passed = sum(passes.values()) == required == len(cases)
    else:
        passed = bool(cases) and all(passes.values())
    return {'phase': phase, 'logical_results': passes, 'passed': passed}

def load_runtime_inputs() -> dict[str, Any]:
    validate_freeze_i()
    required = (CORPUS_PATH, ORACLE_PATH, ENVELOPE_PATH, RELIABILITY_PATH)
    missing = [p.name for p in required if not p.is_file()]
    if missing:
        raise HarnessError(f'Freeze J runtime inputs missing: {missing}')
    inputs = {'analysis': load_json(ANALYSIS_PATH), 'routing': load_json(ROUTING_PATH), 'provenance': load_json(PROVENANCE_PATH), 'topologies': load_json(TOPOLOGIES_PATH), 'manifest': load_json(MANIFEST_PATH), 'instrumentation': load_json(INSTRUMENTATION_PATH), 'corpus': load_json(CORPUS_PATH), 'oracle': load_json(ORACLE_PATH), 'envelope': load_json(ENVELOPE_PATH), 'reliability': load_json(RELIABILITY_PATH)}
    inputs['hashes'] = {p.name: sha256_file(p) for p in (*FREEZE_I_REQUIRED, CORPUS_PATH, ORACLE_PATH, ENVELOPE_PATH, RELIABILITY_PATH)}
    return inputs

def validate_live_cell(args: Any) -> None:
    if codex_version(args.codex_command) != args.required_codex_version:
        raise HarnessError('Codex CLI version mismatch')
    if args.timeout_seconds <= 0:
        raise HarnessError('timeout must be positive')

def run_schedule(schedule: Sequence[ScheduledObservation], *, inputs: dict[str, Any], cases: dict[str, dict[str, Any]], budget: AttemptBudget, args: Any, output: Path, completed: set[str], attempts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    valid_path, attempt_path = (output / 'observations.jsonl', output / 'attempts.jsonl')
    emitted: list[dict[str, Any]] = []
    for spec in schedule:
        if spec.key in completed:
            continue
        prior=attempt_records_for(attempts,spec)
        recovered=next((row for row in reversed(prior) if row.get('technical_valid')),None)
        if recovered is not None:
            record=dict(recovered)
        else:
            record = run_one(spec, inputs=inputs, case=cases[spec.case_id], budget=budget, args=args, attempt_log=attempt_path, attempts=attempts)
        if not record['technical_valid']:
            raise HarnessError(f'technical observation failure after allowed attempts: {spec.key}')
        record['logical_key'] = spec.key
        append_jsonl(valid_path, record)
        emitted.append(record)
        completed.add(spec.key)
        dump_json(output / 'budget.json', {'attempts_used': budget.used, 'attempt_ceiling': budget.ceiling, 'preflight_attempts': budget.phase_used['preflight'], 'canary_attempts': budget.phase_used['canary']})
    return emitted

def _case_map(corpus: dict[str, Any]) -> dict[str, dict[str, Any]]:
    all_cases = [*corpus['routing_cases'], *corpus['e2e_reserve']]
    return {case['id']: case for case in all_cases}

def run_full(args: Any) -> int:
    inputs = load_runtime_inputs()
    validate_live_cell(args)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    metadata_path = output / 'run-metadata.json'
    live_cell = {'model': args.model, 'effort': args.effort, 'codex_cli': args.required_codex_version, 'backend': args.backend, 'sandbox': args.sandbox}
    if metadata_path.exists():
        metadata = load_json(metadata_path)
        if metadata['frozen_asset_sha256'] != inputs['hashes']:
            raise HarnessError('resume frozen-asset drift')
        if metadata['live_cell'] != live_cell:
            raise HarnessError('resume live-cell drift')
    else:
        metadata = {'status': 'RUNNING', 'evaluation_id': 'MG1-T023-EVALUATION-v17', 'frozen_asset_sha256': inputs['hashes'], 'live_cell': live_cell}
        dump_json(metadata_path, metadata)
    valid = load_jsonl(output / 'observations.jsonl')
    attempts = load_jsonl(output / 'attempts.jsonl')
    completed = {r['logical_key'] for r in valid if r.get('technical_valid') and r.get('logical_key')}
    budget = AttemptBudget(inputs['analysis'], attempts)
    envelope = inputs['envelope']
    gate_cases = {case['id']: case for case in [*envelope['behavioral_preflight_cases'], *envelope['synthetic_canary_cases']]}
    preflight_schedule = [ScheduledObservation('preflight', case['id'], case['candidate_id'], 'p1') for case in envelope['behavioral_preflight_cases']]
    canary_schedule = [ScheduledObservation('canary', case['id'], case['candidate_id'], 'c1') for case in envelope['synthetic_canary_cases']]
    run_schedule(preflight_schedule, inputs=inputs, cases=gate_cases, budget=budget, args=args, output=output, completed=completed, attempts=attempts)
    valid = load_jsonl(output / 'observations.jsonl')
    preflight = evaluate_behavioral_gate('preflight', valid, envelope['behavioral_preflight_cases'], inputs['analysis'])
    dump_json(output / 'preflight.json', preflight)
    if not preflight['passed']:
        raise HarnessError('behavioral preflight did not PASS')
    run_schedule(canary_schedule, inputs=inputs, cases=gate_cases, budget=budget, args=args, output=output, completed=completed, attempts=attempts)
    valid = load_jsonl(output / 'observations.jsonl')
    canary = evaluate_behavioral_gate('canary', valid, envelope['synthetic_canary_cases'], inputs['analysis'])
    dump_json(output / 'canary.json', canary)
    if not canary['passed']:
        raise HarnessError('synthetic canary did not achieve 2/2 logical PASS')
    cases = _case_map(inputs['corpus'])
    run_schedule(routing_first_schedule(inputs['corpus']), inputs=inputs, cases=cases, budget=budget, args=args, output=output, completed=completed, attempts=attempts)
    run_schedule(reliability_schedule(inputs['corpus'], inputs['reliability']), inputs=inputs, cases=cases, budget=budget, args=args, output=output, completed=completed, attempts=attempts)
    observations = [observation_from_record(r) for r in load_jsonl(output / 'observations.jsonl') if r['phase'] in SCIENTIFIC_PHASES]
    truths = truths_from_oracle(inputs['oracle'])
    routing_result = routing_analysis(observations, truths, inputs['corpus'], inputs['topologies'], inputs['analysis'], inputs['reliability']['case_ids'])
    dump_json(output / 'routing-analysis.json', routing_result)
    dump_json(output / 'finalists.json', {'status': routing_result['status'], 'finalists': routing_result['finalists']})
    if not routing_result['finalists']:
        metadata.update(status='COMPLETE_NO_TOPOLOGY_SELECTED', attempts_used=budget.used)
        dump_json(metadata_path, metadata)
        return 0
    run_schedule(e2e_schedule(inputs['corpus'], routing_result['finalists']), inputs=inputs, cases=cases, budget=budget, args=args, output=output, completed=completed, attempts=attempts)
    observations = [observation_from_record(r) for r in load_jsonl(output / 'observations.jsonl') if r['phase'] in SCIENTIFIC_PHASES]
    final = e2e_analysis(observations, routing_result, truths, inputs['corpus'], inputs['topologies'], inputs['analysis'])
    dump_json(output / 'selection.json', final)
    metadata.update(status='COMPLETE', attempts_used=budget.used, selected_candidate=final.get('selected'))
    dump_json(metadata_path, metadata)
    return 0
