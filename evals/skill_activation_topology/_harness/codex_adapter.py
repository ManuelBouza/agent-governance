"""Extracted MG1 topology harness implementation."""

from __future__ import annotations

import os
import re
import subprocess
import time
from pathlib import Path
from typing import Any

from .materialization import _inherited_acl_workspace
from .models import BACKEND_PROBE_NONCE, MINIMAL_DISABLED_FEATURES, HarnessError


def _is_explicit_capacity_event(raw: dict[str, Any]) -> bool:
    visible = "\n".join(
        str(raw.get(field, "")) for field in ("stdout_jsonl", "stderr", "final_message")
    )
    return bool(
        re.search(
            r"(?i)(usage[- _]?limit|quota[^\n]{0,80}(exceed|exhaust|limit|capacity)|"
            r"(account|service)[^\n]{0,80}capacity[^\n]{0,80}(exceed|exhaust|unavailable))",
            visible,
        )
    )


def _codex_version(codex_command: str) -> str:
    result = subprocess.run(
        [codex_command, "--version"],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise HarnessError(f"cannot resolve Codex CLI version: {result.stderr.strip()}")
    return result.stdout.strip()


def _backend_probe(
    codex_command: str,
    *,
    backend: str,
    workspace_parent: Path,
    timeout_seconds: int = 20,
) -> dict[str, Any]:
    """Verify a native Windows backend without issuing a provider/model call."""
    started = time.monotonic()
    with _inherited_acl_workspace(workspace_parent, prefix=f"mx-backend-{backend}-") as (
        root,
        workspace_diagnostic,
    ):
        codex_home = root / "codex-home"
        codex_home.mkdir()
        command = [
            codex_command,
            "--config",
            f'windows.sandbox="{backend}"',
            "sandbox",
            "cmd.exe",
            "/d",
            "/c",
            f"echo {BACKEND_PROBE_NONCE}",
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
        passed = (
            not timed_out and completed.returncode == 0 and BACKEND_PROBE_NONCE in completed.stdout
        )
        record = {
            "backend": backend,
            "passed": passed,
            "returncode": completed.returncode,
            "timed_out": timed_out,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "duration_seconds": round(time.monotonic() - started, 6),
            "command": command,
            "provider_model_call_issued": False,
            "user_config_isolation": "temporary empty CODEX_HOME",
            "config_override": f'windows.sandbox="{backend}"',
            "official_config_key": "windows.sandbox",
            "official_allowed_values": ["unelevated", "elevated"],
            "workspace": workspace_diagnostic,
        }
    return record


def _host_command(
    codex_command: str,
    *,
    root: Path,
    model: str,
    effort: str,
    backend: str,
    sandbox: str,
    schema_path: Path,
    final_path: Path,
) -> list[str]:
    command = [
        codex_command,
        "exec",
        "--json",
        "--ignore-user-config",
        "--ignore-rules",
        "--strict-config",
        "--color",
        "never",
        "--sandbox",
        sandbox,
        "--ephemeral",
        "--skip-git-repo-check",
        "--cd",
        str(root),
        "--model",
        model,
        "--config",
        f'model_reasoning_effort="{effort}"',
        "--config",
        'web_search="disabled"',
        "--config",
        f'windows.sandbox="{backend}"',
    ]
    for feature in MINIMAL_DISABLED_FEATURES:
        command.extend(("--disable", feature))
    command.extend(
        (
            "--output-schema",
            str(schema_path),
            "--output-last-message",
            str(final_path),
            "-",
        )
    )
    return command
