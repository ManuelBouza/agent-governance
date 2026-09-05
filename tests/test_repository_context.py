"""Focused repository-context semantic coverage."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from _repository_context_helpers import git, load_measurement_tool
from _repository_context_helpers import measured_repository as measured_repository


def test_inventory_is_canonical_complete_and_honest(
    repo_root: Path, measured_repository: Path
) -> None:
    tool = load_measurement_tool(repo_root)
    report = tool.build_report(measured_repository)
    files = report["files"]
    paths = [record["path"] for record in files]

    assert paths == sorted(paths)
    assert "baselines/repository-context-source-v1.json" not in paths
    volatile = report[tool.VOLATILE_EXECUTION_METADATA_KEY]
    assert (
        volatile["source_git_revision"]
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
    assert (
        report[tool.TRACKED_CONTENT_DIGEST_KEY]
        == tool.canonical_payload(report)[tool.TRACKED_CONTENT_DIGEST_KEY]
    )

    (measured_repository / "unusual.data").write_text("changed\n", encoding="utf-8", newline="")
    changed = tool.build_report(measured_repository)
    assert (
        changed[tool.VOLATILE_EXECUTION_METADATA_KEY]["source_git_revision"]
        == volatile["source_git_revision"]
    )
    assert changed[tool.TRACKED_CONTENT_DIGEST_KEY] != report[tool.TRACKED_CONTENT_DIGEST_KEY]
    assert tool.canonical_identity_digest(changed) != tool.canonical_identity_digest(report)


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
    parsed = json.loads(first)
    canonical = tool.canonical_payload(parsed)
    assert tool.VOLATILE_EXECUTION_METADATA_KEY not in canonical
    assert tool.TRACKED_CONTENT_DIGEST_KEY in canonical


def test_canonical_identity_survives_finalization_boundary(repo_root: Path, tmp_path: Path) -> None:
    """AC-CTX-1 finalization boundary regression.

    When HEAD advances solely because the canonical baseline/handoff file
    is committed, the canonical baseline identity remains stable while the
    volatile execution metadata legitimately differs.
    """
    tool = load_measurement_tool(repo_root)

    repository = tmp_path / "finalization-fixture"
    (repository / "docs" / "orchestrator").mkdir(parents=True)
    (repository / "AGENTS.md").write_text("# Agents\n", encoding="utf-8", newline="")
    (repository / "docs" / "orchestrator" / "CHECKPOINT.md").write_text(
        "# Checkpoint\n", encoding="utf-8", newline=""
    )
    (repository / "src.txt").write_text("hello\n", encoding="utf-8", newline="")

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
        "fixture content",
    )

    baseline_path = repository / tool.DEFAULT_BASELINE
    tool.write_report(repository, baseline_path)
    before_revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    ).stdout.strip()
    before_report = json.loads(baseline_path.read_bytes())

    git(repository, "add", ".")
    git(
        repository,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-qm",
        "finalize baseline",
    )
    after_revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    ).stdout.strip()

    assert after_revision != before_revision

    after_report = tool.build_report(repository)
    after_persisted = json.loads(baseline_path.read_bytes())

    assert (
        before_report[tool.TRACKED_CONTENT_DIGEST_KEY]
        == after_report[tool.TRACKED_CONTENT_DIGEST_KEY]
    )
    assert tool.canonical_identity_digest(before_report) == tool.canonical_identity_digest(
        after_report
    )
    tool.validate_canonical_identity(before_report, after_report, after_persisted)

    assert (
        before_report[tool.VOLATILE_EXECUTION_METADATA_KEY]["source_git_revision"]
        == before_revision
    )
    assert (
        after_report[tool.VOLATILE_EXECUTION_METADATA_KEY]["source_git_revision"] == after_revision
    )
    assert (
        before_report[tool.VOLATILE_EXECUTION_METADATA_KEY]["source_git_revision"]
        != after_report[tool.VOLATILE_EXECUTION_METADATA_KEY]["source_git_revision"]
    )


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

    first = subprocess.run(
        command, cwd=measured_repository, check=True, capture_output=True, timeout=30
    )
    first_bytes = output.read_bytes()
    second = subprocess.run(
        command, cwd=measured_repository, check=True, capture_output=True, timeout=30
    )

    assert first.stdout == second.stdout == b""
    assert output.read_bytes() == first_bytes
    assert tool_path.parent.name == "tools"
    assert repo_root / "src" / "agent_governance" not in tool_path.parents
