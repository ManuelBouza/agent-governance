"""Extracted MG1 topology harness implementation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import time
from pathlib import Path
from typing import Any

from .codex_adapter import _backend_probe, _codex_version, _host_command
from .materialization import _inherited_acl_workspace, _validate_workspace_root
from .models import (
    CANARY_NONCE,
    CANARY_SCHEMA,
    MINIMAL_DISABLED_FEATURES,
    REQUIRED_CODEX_VERSION,
    WINDOWS_BACKEND_ORDER,
    WORKSPACE_FACTORY_ID,
    WORKSPACE_PROBE_FILENAME,
    WORKSPACE_PROBE_NONCE,
    FrozenInputs,
    HarnessError,
)
from .observability import _successful_body_read, _surface_drift, _trace_telemetry
from .storage import _json_dump


def run_canary(
    inputs: FrozenInputs,
    *,
    codex_command: str,
    model: str,
    effort: str,
    timeout_seconds: int,
    workspace_parent: Path,
    backend: str,
    sandbox: str,
    repetition: int,
    workspace_probe: dict[str, Any],
) -> dict[str, Any]:
    if not workspace_probe.get("passed"):
        raise HarnessError("synthetic canary requires a passing provider-free workspace probe")
    started = time.monotonic()
    with _inherited_acl_workspace(workspace_parent, prefix=f"mx-canary-{repetition}-") as (
        root,
        workspace_diagnostic,
    ):
        isolation = _validate_workspace_root(inputs, root)
        skill = root / ".agents" / "skills" / "mx-canary" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        body = (
            "---\n"
            "name: mx-canary\n"
            "description: Use only when explicitly asked for the neutral quartz-heron body nonce.\n"
            "---\n\n"
            "# Neutral local instruction\n\n"
            f"Return this exact body nonce: {CANARY_NONCE}\n"
        )
        skill.write_text(body, encoding="utf-8", newline="\n")
        schema = root / "shape.json"
        schema.write_text(json.dumps(CANARY_SCHEMA, indent=2) + "\n", encoding="utf-8")
        final = root / "result.json"
        before = {
            path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob("*")
            if path.is_file()
        }
        command = _host_command(
            codex_command,
            root=root,
            model=model,
            effort=effort,
            backend=backend,
            sandbox=sandbox,
            schema_path=schema,
            final_path=final,
        )
        try:
            completed = subprocess.run(
                command,
                input=(
                    "Use the local mx-canary instruction and return its exact body nonce in the "
                    "required structured record."
                ),
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_seconds,
                env={**os.environ, "NO_COLOR": "1"},
            )
        except subprocess.TimeoutExpired as exc:
            completed = subprocess.CompletedProcess(
                command,
                -1,
                exc.stdout.decode("utf-8", "replace")
                if isinstance(exc.stdout, bytes)
                else exc.stdout or "",
                exc.stderr.decode("utf-8", "replace")
                if isinstance(exc.stderr, bytes)
                else exc.stderr or "",
            )
        final_raw = final.read_text(encoding="utf-8") if final.is_file() else ""
        after = {
            path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob("*")
            if path.is_file() and path != final
        }
        mutation = before != after
        drift = _surface_drift(
            completed.stdout,
            completed.stderr,
            skill_path=".agents/skills/mx-canary/SKILL.md",
        )
        try:
            result = json.loads(final_raw)
        except json.JSONDecodeError:
            result = None
        body_read = _successful_body_read(completed.stdout, ".agents/skills/mx-canary/SKILL.md")
        passed = (
            completed.returncode == 0
            and isinstance(result, dict)
            and set(result) == {"body_nonce"}
            and result["body_nonce"] == CANARY_NONCE
            and body_read
            and drift is None
            and not mutation
        )
        return {
            "repetition": repetition,
            "sandbox": sandbox,
            "passed": passed,
            "returncode": completed.returncode,
            "metadata_discovery_proved": body_read,
            "body_read_use_proved": body_read and result == {"body_nonce": CANARY_NONCE},
            "body_nonce_correct": result == {"body_nonce": CANARY_NONCE},
            "structured_output_valid": isinstance(result, dict) and set(result) == {"body_nonce"},
            "host_surface_drift": drift,
            "unexpected_model_workspace_mutation": mutation,
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
            "workspace_isolation": isolation,
            "workspace": workspace_diagnostic,
            "provider_free_workspace_probe_passed": True,
            "duration_seconds": round(time.monotonic() - started, 6),
            "telemetry": _trace_telemetry(completed.stdout, completed.stderr),
            "command": command,
            "stdout_jsonl": completed.stdout,
            "stderr": completed.stderr,
            "final_message": final_raw,
        }


def _run_canary_pair(
    inputs: FrozenInputs,
    args: argparse.Namespace,
    output: Path,
    workspace_parent: Path,
    backend: str,
    sandbox: str,
    workspace_record: dict[str, Any],
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    pair = []
    for repetition in (1, 2):
        record = run_canary(
            inputs,
            codex_command=args.codex_command,
            model=args.model,
            effort=args.effort,
            timeout_seconds=args.timeout_seconds,
            workspace_parent=workspace_parent,
            backend=backend,
            sandbox=sandbox,
            repetition=repetition,
            workspace_probe=workspace_record,
        )
        records.append(record)
        pair.append(record)
        _json_dump(output / "canary" / f"{backend}-{sandbox}-r{repetition}.json", record)
        if not record["passed"]:
            break
    return pair


def _passing_preflight(
    output: Path,
    backend: str,
    sandbox: str,
    backend_records: list[dict[str, Any]],
    workspace_records: list[dict[str, Any]],
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    result = {
        "status": "PASS",
        "reason": None,
        "selected_backend": backend,
        "selected_sandbox": sandbox,
        "selected_workspace_acl_profile": WORKSPACE_FACTORY_ID,
        "backend_records": backend_records,
        "workspace_records": workspace_records,
        "records": records,
    }
    _json_dump(output / "host-preflight.json", result)
    return result


def _probe_sandbox(
    inputs: FrozenInputs,
    args: argparse.Namespace,
    output: Path,
    workspace_parent: Path,
    backend: str,
    sandbox: str,
    backend_records: list[dict[str, Any]],
    workspace_records: list[dict[str, Any]],
    records: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, bool]:
    workspace_record = _workspace_access_probe(
        args.codex_command,
        backend=backend,
        sandbox=sandbox,
        workspace_parent=workspace_parent,
    )
    workspace_records.append(workspace_record)
    _json_dump(output / "workspace-probes" / f"{backend}-{sandbox}.json", workspace_record)
    if not workspace_record["passed"]:
        return None, False
    pair = _run_canary_pair(
        inputs, args, output, workspace_parent, backend, sandbox, workspace_record, records
    )
    if len(pair) == 2 and all(record["passed"] for record in pair):
        return (
            _passing_preflight(
                output, backend, sandbox, backend_records, workspace_records, records
            ),
            False,
        )
    body_rejected = any(
        record.get("host_surface_drift") == "REQUIRED_SKILL_BODY_READ_REJECTED" for record in pair
    )
    return None, body_rejected


def _probe_backend(
    inputs: FrozenInputs,
    args: argparse.Namespace,
    output: Path,
    workspace_parent: Path,
    backend: str,
    backend_records: list[dict[str, Any]],
    workspace_records: list[dict[str, Any]],
    records: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, bool]:
    backend_record = _backend_probe(
        args.codex_command, backend=backend, workspace_parent=workspace_parent
    )
    backend_records.append(backend_record)
    _json_dump(
        output / "backend-resolution.json",
        {
            "status": "AVAILABLE" if backend_record["passed"] else "PROBING",
            "codex_cli_version": _codex_version(args.codex_command),
            "platform": platform.platform(),
            "backend_selection_order": list(WINDOWS_BACKEND_ORDER),
            "records": backend_records,
            "provider_model_calls_issued": 0,
            "dangerous_bypass_used": False,
        },
    )
    if not backend_record["passed"]:
        return None, False
    for sandbox in ("read-only", "workspace-write"):
        result, body_rejected = _probe_sandbox(
            inputs,
            args,
            output,
            workspace_parent,
            backend,
            sandbox,
            backend_records,
            workspace_records,
            records,
        )
        if result is not None:
            return result, False
        if sandbox == "read-only" and not body_rejected:
            break
    workspace_passed = any(
        record["passed"] for record in workspace_records if record["backend"] == backend
    )
    if not workspace_passed:
        return None, False
    backend_canaries = [
        record
        for record in records
        if record["effective_host_profile"]["native_windows_backend"] == backend
    ]
    retry_other_backend = any(
        record.get("host_surface_drift") == "REQUIRED_SKILL_BODY_READ_REJECTED"
        or record.get("returncode") not in {0, None}
        for record in backend_canaries
    )
    return None, not retry_other_backend


def run_host_preflight(
    inputs: FrozenInputs, args: argparse.Namespace, output: Path, workspace_parent: Path
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    backend_records: list[dict[str, Any]] = []
    workspace_records: list[dict[str, Any]] = []
    for backend in WINDOWS_BACKEND_ORDER:
        result, stop = _probe_backend(
            inputs,
            args,
            output,
            workspace_parent,
            backend,
            backend_records,
            workspace_records,
            records,
        )
        if result is not None:
            return result
        if stop:
            break
    backend_available = any(record["passed"] for record in backend_records)
    workspace_available = any(record["passed"] for record in workspace_records)
    if not backend_available:
        reason = "WINDOWS_SANDBOX_BACKEND_UNAVAILABLE"
    elif not workspace_available:
        reason = "WINDOWS_WORKSPACE_ACL_UNAVAILABLE"
    else:
        reason = "HOST_CAPABILITY_PREFLIGHT"
    result = {
        "status": "BLOCKED",
        "reason": reason,
        "selected_backend": None,
        "selected_sandbox": None,
        "selected_workspace_acl_profile": None,
        "backend_records": backend_records,
        "workspace_records": workspace_records,
        "records": records,
    }
    _json_dump(output / "host-preflight.json", result)
    _json_dump(
        output / "backend-resolution.json",
        {
            "status": "BLOCKED" if not backend_available else "AVAILABLE",
            "reason": reason if not backend_available else None,
            "codex_cli_version": _codex_version(args.codex_command),
            "platform": platform.platform(),
            "backend_selection_order": list(WINDOWS_BACKEND_ORDER),
            "records": backend_records,
            "provider_model_calls_issued": 0,
            "dangerous_bypass_used": False,
        },
    )
    return result


def _workspace_access_probe(
    codex_command: str,
    *,
    backend: str,
    sandbox: str,
    workspace_parent: Path,
    timeout_seconds: int = 20,
) -> dict[str, Any]:
    """Prove exact-root readability through the native sandbox without a model call."""
    started = time.monotonic()
    with _inherited_acl_workspace(
        workspace_parent, prefix=f"mx-workspace-{backend}-{sandbox}-"
    ) as (root, workspace_diagnostic):
        probe = root / WORKSPACE_PROBE_FILENAME
        probe.write_text(WORKSPACE_PROBE_NONCE + "\n", encoding="utf-8", newline="\n")
        codex_home = root / "codex-home"
        codex_home.mkdir()
        command = [
            codex_command,
            "--config",
            f'windows.sandbox="{backend}"',
            "sandbox",
            "--permission-profile",
            ":read-only" if sandbox == "read-only" else ":workspace",
            "--cd",
            str(root),
            "cmd.exe",
            "/d",
            "/c",
            f"cd & dir /b & type {WORKSPACE_PROBE_FILENAME}",
        ]
        environment = os.environ.copy()
        environment["CODEX_HOME"] = str(codex_home)
        timed_out = False
        try:
            completed = subprocess.run(
                command,
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_seconds,
                env=environment,
            )
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            completed = subprocess.CompletedProcess(
                command,
                -1,
                exc.stdout.decode("utf-8", "replace")
                if isinstance(exc.stdout, bytes)
                else exc.stdout or "",
                exc.stderr.decode("utf-8", "replace")
                if isinstance(exc.stderr, bytes)
                else exc.stderr or "",
            )
        root_observed = str(root).casefold() in completed.stdout.casefold()
        file_observed = WORKSPACE_PROBE_FILENAME.casefold() in completed.stdout.casefold()
        nonce_observed = WORKSPACE_PROBE_NONCE in completed.stdout
        record = {
            "backend": backend,
            "logical_sandbox": sandbox,
            "passed": (
                not timed_out
                and completed.returncode == 0
                and root_observed
                and file_observed
                and nonce_observed
            ),
            "returncode": completed.returncode,
            "timed_out": timed_out,
            "workspace_root_enumerated": root_observed and file_observed,
            "probe_file_read_exactly": nonce_observed,
            "probe_nonce": WORKSPACE_PROBE_NONCE,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "duration_seconds": round(time.monotonic() - started, 6),
            "command": command,
            "provider_model_call_issued": False,
            "dangerous_bypass_used": False,
            "interactive_approval_used": False,
            "network_access_requested": False,
            "workspace": workspace_diagnostic,
        }
    return record
