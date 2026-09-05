"""Shared fixtures and loaders for repository-context tests."""

from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

import pytest


def load_measurement_tool(repo_root: Path):
    path = repo_root / "tools" / "repository_context.py"
    spec = importlib.util.spec_from_file_location("repository_context", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(repository: Path, *arguments: str) -> None:
    subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=True,
        capture_output=True,
        timeout=30,
    )


@pytest.fixture
def measured_repository(tmp_path: Path) -> Path:
    repository = tmp_path / "repository"
    (repository / "docs" / "orchestrator").mkdir(parents=True)
    (repository / "baselines").mkdir()
    (repository / "AGENTS.md").write_text(
        "# Agents\n\nSee [guide](docs/guide.md).\n", encoding="utf-8", newline=""
    )
    (repository / "docs" / "orchestrator" / "CHECKPOINT.md").write_text(
        "# Checkpoint\n\nRoute: `docs/guide.md`\n", encoding="utf-8", newline=""
    )
    (repository / "docs" / "guide.md").write_text(
        "# Guide\n\n[checkpoint](orchestrator/CHECKPOINT.md)\n", encoding="utf-8", newline=""
    )
    (repository / "unusual.data").write_text("snowman: \N{SNOWMAN}\n", encoding="utf-8", newline="")
    (repository / "binary.dat").write_bytes(b"\x00\xff\x10")
    (repository / "large.txt").write_text("x" * (1024 * 1024), encoding="utf-8", newline="")
    (repository / "baselines" / "repository-context-source-v1.json").write_text(
        "stale baseline\n", encoding="utf-8", newline=""
    )
    git(repository, "init", "-q")
    git(repository, "add", ".")
    git(
        repository,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-qm",
        "fixture",
    )
    return repository


def _git_fixture(repository: Path) -> None:
    git(repository, "init", "-q")
    git(repository, "add", ".")
    git(
        repository,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-qm",
        "fixture",
    )


def _write_context_map(repository: Path, registry: dict) -> None:
    """Write a minimal CONTEXT-MAP.md with the given registry JSON."""
    json_block = json.dumps(registry, indent=2, sort_keys=True)
    content = (
        "# Source Repository Context Map\n\n"
        "<!-- RCAB-MAP-V1:BEGIN -->\n"
        f"```json\n{json_block}\n```\n"
        "<!-- RCAB-MAP-V1:END -->\n"
    )
    (repository / "docs").mkdir(parents=True, exist_ok=True)
    (repository / "docs" / "CONTEXT-MAP.md").write_text(content, encoding="utf-8", newline="")


def _default_registry(agents_bytes: int, checkpoint_bytes: int) -> dict:
    total_bytes = agents_bytes + checkpoint_bytes
    return {
        "schema_version": "1.0.0",
        "entries": [
            {"path": "AGENTS.md", "class": "bootstrap", "routes": ["cold-start"]},
            {
                "path": "docs/orchestrator/CHECKPOINT.md",
                "class": "router",
                "routes": ["cold-start"],
            },
            {"path": "docs/CONTEXT-MAP.md", "class": "focused", "routes": ["icae-rcab"]},
        ],
        "bootstrap_ratchet": {
            "reference": "T030-R2",
            "file_count": 2,
            "byte_size": total_bytes,
            "line_count": 2,
            "warning_relative_growth": 0.05,
            "blocking": False,
        },
    }


def _make_manifest_repository(
    tmp_path: Path,
    registry: dict | None = None,
    *,
    agents_text: str = "# Agents\n",
    checkpoint_text: str = "# Checkpoint\n",
) -> Path:
    repository = tmp_path / "manifest-repo"
    (repository / "docs" / "orchestrator").mkdir(parents=True)
    (repository / "baselines").mkdir()
    (repository / "AGENTS.md").write_text(agents_text, encoding="utf-8", newline="")
    (repository / "docs" / "orchestrator" / "CHECKPOINT.md").write_text(
        checkpoint_text, encoding="utf-8", newline=""
    )
    if registry is None:
        registry = _default_registry(
            len(agents_text.encode("utf-8")),
            len(checkpoint_text.encode("utf-8")),
        )
    _write_context_map(repository, registry)
    _git_fixture(repository)
    return repository
