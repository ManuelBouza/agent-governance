"""Version-parameterized Codex host adapter for v16 routing/e2e execution."""
from __future__ import annotations
import json
import re
import subprocess
import time
from pathlib import Path
from typing import Any
from .models import CAPABILITIES, DISPOSITIONS, HarnessError

def codex_version(command: str) -> str:
    result = subprocess.run([command, '--version'], capture_output=True, text=True, check=False, timeout=30)
    if result.returncode:
        raise HarnessError(f'cannot resolve Codex CLI version: {result.stderr.strip()}')
    return result.stdout.strip()

def output_schema() -> dict[str, Any]:
    return {'$schema': 'https://json-schema.org/draft/2020-12/schema', 'type': 'object', 'additionalProperties': False, 'required': ['routing_disposition', 'selected_capabilities', 'activated_entrypoints', 'clarification_requested', 'permission_broadening', 'task_success', 'semantic_outcome', 'response_summary'], 'properties': {'routing_disposition': {'type': 'string', 'enum': list(DISPOSITIONS)}, 'selected_capabilities': {'type': 'array', 'uniqueItems': True, 'items': {'type': 'string', 'enum': list(CAPABILITIES)}}, 'activated_entrypoints': {'type': 'array', 'uniqueItems': True, 'items': {'type': 'string'}}, 'clarification_requested': {'type': 'boolean'}, 'permission_broadening': {'type': 'boolean'}, 'task_success': {'type': 'boolean'}, 'semantic_outcome': {'type': 'string', 'enum': ['SUCCESS', 'BOUNDED_REJECTION', 'CLARIFICATION', 'NOT_APPLICABLE', 'FAILURE']}, 'response_summary': {'type': 'string'}}}

def build_codex_command(*, codex_command: str, workspace: Path, model: str, effort: str, backend: str, sandbox: str, schema_path: Path, final_path: Path) -> list[str]:
    return [codex_command, 'exec', '--json', '--ignore-user-config', '--ignore-rules', '--strict-config', '--color', 'never', '--sandbox', sandbox, '--ephemeral', '--skip-git-repo-check', '--cd', str(workspace), '--model', model, '--config', f'model_reasoning_effort="{effort}"', '--config', 'web_search="disabled"', '--config', f'windows.sandbox="{backend}"', '--output-schema', str(schema_path), '--output-last-message', str(final_path), '-']

def _trace(stdout_jsonl: str, manifest: dict[str, Any], candidate_id: str) -> dict[str, Any]:
    successful = []
    usage = {}
    trace_available = False
    for line in stdout_jsonl.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get('type') == 'thread.started':
            trace_available = True
        if event.get('type') == 'turn.completed' and isinstance(event.get('usage'), dict):
            usage = event['usage']
        item = event.get('item', {})
        if event.get('type') == 'item.completed' and item.get('type') == 'command_execution' and (item.get('exit_code') == 0):
            command = re.sub('[\\\\/]+', '/', str(item.get('command', ''))).casefold()
            if re.search('\\b(get-content|cat|type|read_text|read_bytes)\\b', command):
                successful.append(command)
    candidate = manifest['candidates'][candidate_id]
    entrypoints = []
    caps = []
    paths = []
    for entrypoint, data in candidate['entrypoints'].items():
        needle = f'.agents/skills/{entrypoint.casefold()}/skill.md'
        if any((needle in c for c in successful)):
            entrypoints.append(entrypoint)
            paths.append(needle)
        for cap in data['capabilities']:
            ref = f'.agents/skills/{entrypoint.casefold()}/references/{cap.casefold()}.md'
            if any((ref in c for c in successful)):
                if cap not in caps:
                    caps.append(cap)
                paths.append(ref)
    return {'trace_available': trace_available, 'observed_activation_set': sorted(entrypoints), 'observed_capability_set': sorted(caps), 'read_paths': sorted(set(paths)), 'provider_usage': usage}

def execute_codex(*, prompt: str, manifest: dict[str, Any], candidate_id: str, workspace: Path, codex_command: str, model: str, effort: str, backend: str, sandbox: str, timeout_seconds: int) -> dict[str, Any]:
    schema_path = workspace / 't064-output-schema.json'
    final_path = workspace / 't064-final.json'
    schema_path.write_text(json.dumps(output_schema(), indent=2, sort_keys=True) + '\n', encoding='utf-8')
    command = build_codex_command(codex_command=codex_command, workspace=workspace, model=model, effort=effort, backend=backend, sandbox=sandbox, schema_path=schema_path, final_path=final_path)
    started = time.monotonic()
    try:
        completed = subprocess.run(command, input=prompt, capture_output=True, text=True, encoding='utf-8', errors='replace', check=False, timeout=timeout_seconds)
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        return {'technical_valid': False, 'timed_out': True, 'returncode': -1, 'stdout_jsonl': exc.stdout or '', 'stderr': exc.stderr or '', 'latency_seconds': time.monotonic() - started, 'provider_usage': {}}
    trace = _trace(completed.stdout, manifest, candidate_id)
    model_result = None
    parse_error = None
    if final_path.exists():
        try:
            model_result = json.loads(final_path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, OSError) as exc:
            parse_error = str(exc)
    valid = completed.returncode == 0 and trace['trace_available'] and isinstance(model_result, dict) and (parse_error is None)
    return {'technical_valid': valid, 'timed_out': timed_out, 'returncode': completed.returncode, 'stdout_jsonl': completed.stdout, 'stderr': completed.stderr, 'latency_seconds': time.monotonic() - started, 'model_result': model_result, 'parse_error': parse_error, **trace}
