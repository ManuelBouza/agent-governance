"""Deterministic repository-context measurement coverage."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
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
        "# Agents\n\nSee [guide](docs/guide.md).\n", encoding="utf-8"
    )
    (repository / "docs" / "orchestrator" / "CHECKPOINT.md").write_text(
        "# Checkpoint\n\nRoute: `docs/guide.md`\n", encoding="utf-8"
    )
    (repository / "docs" / "guide.md").write_text(
        "# Guide\n\n[checkpoint](orchestrator/CHECKPOINT.md)\n", encoding="utf-8"
    )
    (repository / "unusual.data").write_text("snowman: \N{SNOWMAN}\n", encoding="utf-8")
    (repository / "binary.dat").write_bytes(b"\x00\xff\x10")
    (repository / "large.txt").write_text("x" * (1024 * 1024), encoding="utf-8")
    (repository / "baselines" / "repository-context-source-v1.json").write_text(
        "stale baseline\n", encoding="utf-8"
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


def test_inventory_is_canonical_complete_and_honest(
    repo_root: Path, measured_repository: Path
) -> None:
    tool = load_measurement_tool(repo_root)
    report = tool.build_report(measured_repository)
    files = report["files"]
    paths = [record["path"] for record in files]

    assert paths == sorted(paths)
    assert "baselines/repository-context-source-v1.json" not in paths
    assert (
        report["source_git_revision"]
        == subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=measured_repository,
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        ).stdout.strip()
    )
    binary = next(record for record in files if record["path"] == "binary.dat")
    assert binary["category"] == "binary"
    assert binary["character_count"] is None
    assert binary["line_count"] is None
    unusual = next(record for record in files if record["path"] == "unusual.data")
    assert unusual["character_count"] == len("snowman: \N{SNOWMAN}\n")
    assert unusual["line_count"] == 1
    assert report["totals"]["repository"]["file_count"] == len(paths)
    assert report["measurement_scope"]["observed_runtime_context_metrics"] is False
    assert report["structural_markdown_references"]["edges"] == [
        {"occurrences": 1, "source": "AGENTS.md", "target": "docs/guide.md"},
        {
            "occurrences": 1,
            "source": "docs/guide.md",
            "target": "docs/orchestrator/CHECKPOINT.md",
        },
        {
            "occurrences": 1,
            "source": "docs/orchestrator/CHECKPOINT.md",
            "target": "docs/guide.md",
        },
    ]

    (measured_repository / "unusual.data").write_text("changed\n", encoding="utf-8")
    changed = tool.build_report(measured_repository)
    assert changed["source_git_revision"] == report["source_git_revision"]
    assert changed["tracked_content_digest"] != report["tracked_content_digest"]


def test_repeated_runs_are_byte_identical_and_baseline_self_excludes(
    repo_root: Path, measured_repository: Path
) -> None:
    tool = load_measurement_tool(repo_root)
    output = measured_repository / tool.DEFAULT_BASELINE
    before_docs = {
        path.relative_to(measured_repository): path.read_bytes()
        for path in measured_repository.rglob("*.md")
    }

    tool.write_report(measured_repository, output)
    first = output.read_bytes()
    tool.write_report(measured_repository, output)
    second = output.read_bytes()

    assert first == second
    assert json.loads(first)["excluded_paths"] == [tool.DEFAULT_BASELINE]
    assert before_docs == {
        path.relative_to(measured_repository): path.read_bytes()
        for path in measured_repository.rglob("*.md")
    }


def test_bootstrap_footprint_and_largest_files_are_physical_only(
    repo_root: Path, measured_repository: Path
) -> None:
    tool = load_measurement_tool(repo_root)
    report = tool.build_report(measured_repository)
    bootstrap = report["bootstrap_physical_footprint"]

    assert [record["path"] for record in bootstrap["files"]] == list(tool.BOOTSTRAP_PATHS)
    assert bootstrap["totals"]["byte_size"] == sum(
        (measured_repository / path).stat().st_size for path in tool.BOOTSTRAP_PATHS
    )
    assert report["largest_context_relevant_files"]["files"][0]["path"] == "large.txt"
    rendered = tool.canonical_json(report).decode("utf-8").lower()
    assert '"token_count"' not in rendered
    assert '"rfo"' not in rendered
    assert '"tmc"' not in rendered
    assert '"car"' not in rendered


def test_cli_output_is_stable_and_tool_stays_outside_consumer_package(
    repo_root: Path, measured_repository: Path
) -> None:
    tool_path = repo_root / "tools" / "repository_context.py"
    output = measured_repository / "baselines" / "candidate.json"
    command = [
        sys.executable,
        str(tool_path),
        "--source-root",
        str(measured_repository),
        "--output",
        str(output),
    ]

    first = subprocess.run(command, check=True, capture_output=True, timeout=30)
    first_bytes = output.read_bytes()
    second = subprocess.run(command, check=True, capture_output=True, timeout=30)

    assert first.stdout == second.stdout == b""
    assert output.read_bytes() == first_bytes
    assert tool_path.parent.name == "tools"
    assert repo_root / "src" / "agent_governance" not in tool_path.parents
