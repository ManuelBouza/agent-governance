"""Extracted MG1 topology harness implementation."""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any

from .codex_adapter import _host_command, _is_explicit_capacity_event
from .materialization import (
    _inherited_acl_workspace,
    _validate_workspace_root,
    materialize_candidate,
    materialize_fixture,
)
from .models import (
    MINIMAL_DISABLED_FEATURES,
    REPO_ROOT,
    REQUIRED_CODEX_VERSION,
    TRIAL_SCHEMA,
    WORKSPACE_FACTORY_ID,
    AttemptFailure,
    CapacityPause,
    FrozenInputs,
    HarnessError,
    TrialSpec,
)
from .observability import (
    _observed_skill_reads,
    _surface_drift,
    _trace_telemetry,
    _validate_model_result,
)
from .scheduling import _trial_prompt, expected_entrypoints


def _raw_record(
    inputs: FrozenInputs,
    spec: TrialSpec,
    attempt: int,
    timeout_seconds: int,
    command: list[str],
    completed: subprocess.CompletedProcess,
    final_raw: str,
    duration: float,
    backend: str,
    sandbox: str,
    model: str,
    effort: str,
    provenance: dict[str, Any],
    fixture: dict[str, Any],
    isolation: dict[str, Any],
    workspace: dict[str, Any],
) -> dict[str, Any]:
    return {
        "trial_key": spec.key,
        "attempt": attempt,
        "oracle_id": inputs.oracle["oracle_id"],
        "execution_epoch": inputs.oracle["execution_epoch"],
        "timeout_seconds": timeout_seconds,
        "command": command,
        "prompt": _trial_prompt(inputs, spec.case),
        "returncode": completed.returncode,
        "stdout_jsonl": completed.stdout,
        "stderr": completed.stderr,
        "final_message": final_raw,
        "duration_seconds": round(duration, 6),
        "effective_host_profile": {
            "codex_cli_version": REQUIRED_CODEX_VERSION,
            "native_windows_backend": backend,
            "logical_sandbox": sandbox,
            "workspace_acl_profile_identity": WORKSPACE_FACTORY_ID,
            "model": model,
            "effort": effort,
            "ignore_user_config": True,
            "ignore_rules": True,
            "disabled_features": list(MINIMAL_DISABLED_FEATURES),
        },
        "telemetry": _trace_telemetry(completed.stdout, completed.stderr),
        "materialization": provenance,
        "fixture_materialization": fixture,
        "workspace_isolation": isolation,
        "workspace": workspace,
    }


def _structured_record(
    inputs: FrozenInputs,
    spec: TrialSpec,
    attempt: int,
    model_result: dict[str, Any],
    stdout_jsonl: str,
    duration: float,
) -> dict[str, Any]:
    observed_entrypoints, observed_references, trace_available = _observed_skill_reads(
        inputs, spec, stdout_jsonl
    )
    entrypoint_manifest = inputs.manifest["candidates"][spec.candidate_id]["entrypoints"]
    reported_invalid_entrypoints = [
        name for name in model_result["activated_entrypoints"] if name not in entrypoint_manifest
    ]
    activation_surface = {
        name: (REPO_ROOT / entrypoint_manifest[name]["skill_source"]).stat().st_size
        for name in observed_entrypoints
    }
    loaded_bytes = sum((REPO_ROOT / path).stat().st_size for path in observed_references)
    return {
        "attempt": attempt,
        "execution_epoch": inputs.oracle["execution_epoch"],
        "case_id": spec.case["id"],
        "case_class": spec.case["class"],
        "candidate_id": spec.candidate_id,
        "repetition": spec.repetition,
        "activated_entrypoints": observed_entrypoints,
        "reported_activated_entrypoints": model_result["activated_entrypoints"],
        "reported_invalid_entrypoints": reported_invalid_entrypoints,
        "expected_entrypoints": expected_entrypoints(inputs, spec),
        "semantic_outcome": model_result["semantic_outcome"],
        "expected_semantic_outcome": spec.case["expected_semantic_outcome"],
        "granted_capabilities": model_result["granted_capabilities"],
        "forbidden_capabilities": spec.case.get("forbidden_capabilities", []),
        "permission_broadening": model_result["permission_broadening"],
        "response_summary": model_result["response_summary"],
        "activation_surface_bytes": activation_surface,
        "loaded_reference_paths": observed_references,
        "loaded_reference_bytes": loaded_bytes,
        "observed_reference_paths": observed_references,
        "observed_reference_bytes": loaded_bytes,
        "observed_context_bytes": sum(activation_surface.values()) + loaded_bytes,
        "host_trace_available": trace_available,
        "duration_seconds": round(duration, 6),
    }


def run_trial(
    inputs: FrozenInputs,
    spec: TrialSpec,
    *,
    codex_command: str,
    model: str,
    effort: str,
    timeout_seconds: int,
    workspace_parent: Path,
    backend: str = "elevated",
    sandbox: str = "read-only",
    attempt: int = 1,
) -> tuple[dict[str, Any], dict[str, Any]]:
    started = time.monotonic()
    with _inherited_acl_workspace(workspace_parent, prefix=f"mx-{spec.key}-") as (
        root,
        workspace_diagnostic,
    ):
        isolation = _validate_workspace_root(inputs, root)
        fixture = materialize_fixture(inputs, spec.case, root)
        provenance = materialize_candidate(inputs, spec.candidate_id, root)
        schema_path = root / "shape.json"
        schema_path.write_text(json.dumps(TRIAL_SCHEMA, indent=2) + "\n", encoding="utf-8")
        final_path = root / "result.json"
        command = _host_command(
            codex_command,
            root=root,
            model=model,
            effort=effort,
            backend=backend,
            sandbox=sandbox,
            schema_path=schema_path,
            final_path=final_path,
        )
        environment = os.environ.copy()
        environment["NO_COLOR"] = "1"
        failure_class = None
        failure_message = None
        try:
            completed = subprocess.run(
                command,
                input=_trial_prompt(inputs, spec.case),
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_seconds,
                env=environment,
            )
        except subprocess.TimeoutExpired as exc:
            # TimeoutExpired carries bytes even with text=True on some Python versions.
            def decode(value: str | bytes | None) -> str:
                return (
                    value.decode("utf-8", errors="replace")
                    if isinstance(value, bytes)
                    else value or ""
                )

            completed = subprocess.CompletedProcess(
                command, -1, decode(exc.stdout), decode(exc.stderr)
            )
            failure_class = "TIMEOUT_UNCLASSIFIED"
            failure_message = f"{spec.key}: exceeded {timeout_seconds}-second attempt timeout"
        except OSError as exc:
            completed = subprocess.CompletedProcess(command, -1, "", str(exc))
            failure_class = "HOST_LAUNCH_ERROR"
            failure_message = f"{spec.key}: cannot launch Codex: {exc}"
        duration = time.monotonic() - started
        final_raw = final_path.read_text(encoding="utf-8") if final_path.is_file() else ""
        raw_record = _raw_record(
            inputs,
            spec,
            attempt,
            timeout_seconds,
            command,
            completed,
            final_raw,
            duration,
            backend,
            sandbox,
            model,
            effort,
            provenance,
            fixture,
            isolation,
            workspace_diagnostic,
        )
        if _is_explicit_capacity_event(raw_record) and not final_raw:
            raise CapacityPause(f"{spec.key}: explicit external capacity event", raw_record)
        if failure_class:
            raise AttemptFailure(failure_class, failure_message, raw_record)
        if completed.returncode != 0:
            raise AttemptFailure(
                "HOST_NONZERO_EXIT", f"{spec.key}: Codex exited {completed.returncode}", raw_record
            )
        entrypoints = inputs.manifest["candidates"][spec.candidate_id]["entrypoints"]
        candidate_skill_paths = [
            f".agents/skills/{entrypoint}/SKILL.md" for entrypoint in entrypoints
        ]
        drift = next(
            (
                value
                for path in candidate_skill_paths
                if (value := _surface_drift(completed.stdout, completed.stderr, skill_path=path))
            ),
            _surface_drift(completed.stdout, completed.stderr),
        )
        if drift:
            raw_record["host_surface_drift"] = drift
            raise AttemptFailure("HOST_SURFACE_DRIFT", f"{spec.key}: {drift}", raw_record)
        try:
            model_result = json.loads(final_raw)
            _validate_model_result(inputs, spec, model_result)
        except (json.JSONDecodeError, HarnessError) as exc:
            raise AttemptFailure(
                "INVALID_STRUCTURED_RESULT",
                f"{spec.key}: invalid structured response: {exc}",
                raw_record,
            ) from exc

        structured = _structured_record(
            inputs, spec, attempt, model_result, completed.stdout, duration
        )
        return structured, raw_record
