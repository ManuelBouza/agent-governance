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

    (measured_repository / "unusual.data").write_text("changed\n", encoding="utf-8")
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
    (repository / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
    (repository / "docs" / "orchestrator" / "CHECKPOINT.md").write_text(
        "# Checkpoint\n", encoding="utf-8"
    )
    (repository / "src.txt").write_text("hello\n", encoding="utf-8")

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

    first = subprocess.run(command, check=True, capture_output=True, timeout=30)
    first_bytes = output.read_bytes()
    second = subprocess.run(command, check=True, capture_output=True, timeout=30)

    assert first.stdout == second.stdout == b""
    assert output.read_bytes() == first_bytes
    assert tool_path.parent.name == "tools"
    assert repo_root / "src" / "agent_governance" not in tool_path.parents


# ---------------------------------------------------------------------------
# T031 — RCAB v1 manifest and ratchet tests (AC-RCAB-1 .. AC-RCAB-6)
# ---------------------------------------------------------------------------


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
    (repository / "docs" / "CONTEXT-MAP.md").write_text(content, encoding="utf-8")


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
    (repository / "AGENTS.md").write_text(agents_text, encoding="utf-8")
    (repository / "docs" / "orchestrator" / "CHECKPOINT.md").write_text(
        checkpoint_text, encoding="utf-8"
    )
    if registry is None:
        registry = _default_registry(
            len(agents_text.encode("utf-8")),
            len(checkpoint_text.encode("utf-8")),
        )
    _write_context_map(repository, registry)
    _git_fixture(repository)
    return repository


def test_ac_rcab_1_deterministic_projection_byte_identical(repo_root: Path, tmp_path: Path) -> None:
    """AC-RCAB-1: repeated generation produces byte-identical canonical manifest."""
    tool = load_measurement_tool(repo_root)
    repository = _make_manifest_repository(tmp_path)

    output = repository / tool.DEFAULT_MANIFEST
    tool.write_manifest(repository, output)
    first = output.read_bytes()
    tool.write_manifest(repository, output)
    second = output.read_bytes()

    assert first == second

    manifest = json.loads(first)
    assert manifest["projection_schema_version"] == tool.MANIFEST_SCHEMA_VERSION
    paths = [e["path"] for e in manifest["registered_paths"]]
    assert paths == sorted(paths)
    assert "registry_digest" in manifest
    assert "registered_content_digest" in manifest
    assert tool.DEFAULT_MANIFEST.split("/")[-1] not in paths

    # Manifest does not embed a Git commit SHA
    assert b"source_git_revision" not in first
    rendered = first.decode("utf-8").lower()
    assert "volatile_execution_metadata" not in rendered


def test_ac_rcab_1_no_self_reference(repo_root: Path, tmp_path: Path) -> None:
    """AC-RCAB-1: manifest path excluded from registered_content_digest."""
    tool = load_measurement_tool(repo_root)

    repository = _make_manifest_repository(tmp_path)

    # Create and commit a placeholder manifest so it can be registered
    manifest_path = repository / tool.DEFAULT_MANIFEST
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text("placeholder\n", encoding="utf-8")

    # Register the manifest path in the map to prove self-exclusion
    registry_with_manifest = _default_registry(
        len(b"# Agents\n"),
        len(b"# Checkpoint\n"),
    )
    registry_with_manifest["entries"].append(
        {
            "path": "baselines/repository-context-manifest-v1.json",
            "class": "generated-data",
            "routes": ["epoch-index"],
        }
    )
    _write_context_map(repository, registry_with_manifest)
    git(repository, "add", ".")
    git(
        repository,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-qm",
        "register manifest path",
    )

    tool.write_manifest(repository, manifest_path)
    first = manifest_path.read_bytes()
    tool.write_manifest(repository, manifest_path)
    second = manifest_path.read_bytes()

    assert first == second

    manifest = json.loads(first)
    sha_map = {e["path"]: e["sha256"] for e in manifest["registered_paths"]}
    # The manifest path is registered but excluded from measurement
    assert "baselines/repository-context-manifest-v1.json" not in sha_map


def test_ac_rcab_2_positive_registry(repo_root: Path, tmp_path: Path) -> None:
    """AC-RCAB-2: valid registry parses and validates without semantic inference."""
    tool = load_measurement_tool(repo_root)
    repository = _make_manifest_repository(tmp_path)
    registry = tool.parse_registry(repository / "docs" / "CONTEXT-MAP.md")

    assert registry["schema_version"] == "1.0.0"
    assert len(registry["entries"]) == 3
    tool.validate_registry(registry, repository)

    manifest = tool.build_manifest(repository)
    assert len(manifest["registered_paths"]) == 3


def test_ac_rcab_2_negative_registry_malformed(repo_root: Path, tmp_path: Path) -> None:
    """AC-RCAB-2: malformed JSON in registry fails deterministically."""
    tool = load_measurement_tool(repo_root)
    repository = tmp_path / "bad-registry"
    (repository / "docs").mkdir(parents=True)
    (repository / "AGENTS.md").write_text("# A\n", encoding="utf-8")

    bad_content = (
        "# Map\n\n"
        "<!-- RCAB-MAP-V1:BEGIN -->\n"
        "```json\n{not valid json}\n```\n"
        "<!-- RCAB-MAP-V1:END -->\n"
    )
    (repository / "docs" / "CONTEXT-MAP.md").write_text(bad_content, encoding="utf-8")
    _git_fixture(repository)

    with pytest.raises(tool.MeasurementError, match="invalid JSON"):
        tool.parse_registry(repository / "docs" / "CONTEXT-MAP.md")


def test_ac_rcab_2_negative_duplicate_paths(repo_root: Path, tmp_path: Path) -> None:
    """AC-RCAB-2: duplicate registered paths fail deterministically."""
    tool = load_measurement_tool(repo_root)

    registry = _default_registry(10, 10)
    registry["entries"].append(
        {
            "path": "AGENTS.md",
            "class": "focused",
            "routes": ["other-route"],
        }
    )
    repository = _make_manifest_repository(tmp_path, registry=registry)

    with pytest.raises(tool.MeasurementError, match="duplicate registered path"):
        tool.validate_registry(
            tool.parse_registry(repository / "docs" / "CONTEXT-MAP.md"),
            repository,
        )


def test_ac_rcab_2_negative_invalid_class(repo_root: Path, tmp_path: Path) -> None:
    """AC-RCAB-2: invalid classification fails deterministically."""
    tool = load_measurement_tool(repo_root)

    registry = _default_registry(10, 10)
    registry["entries"][0]["class"] = "nonexistent-class"
    repository = _make_manifest_repository(tmp_path, registry=registry)

    with pytest.raises(tool.MeasurementError, match="invalid class"):
        tool.validate_registry(
            tool.parse_registry(repository / "docs" / "CONTEXT-MAP.md"),
            repository,
        )


def test_ac_rcab_2_negative_missing_target(repo_root: Path, tmp_path: Path) -> None:
    """AC-RCAB-2: registered target not tracked by Git fails deterministically."""
    tool = load_measurement_tool(repo_root)

    registry = _default_registry(10, 10)
    registry["entries"].append(
        {
            "path": "docs/MISSING.md",
            "class": "focused",
            "routes": ["other"],
        }
    )
    repository = _make_manifest_repository(tmp_path, registry=registry)

    with pytest.raises(tool.MeasurementError, match="not tracked by Git"):
        tool.validate_registry(
            tool.parse_registry(repository / "docs" / "CONTEXT-MAP.md"),
            repository,
        )


def test_ac_rcab_2_negative_multiple_markers(repo_root: Path, tmp_path: Path) -> None:
    """AC-RCAB-2: multiple BEGIN/END marker pairs fail deterministically."""
    tool = load_measurement_tool(repo_root)
    repository = tmp_path / "multi-marker"
    (repository / "docs").mkdir(parents=True)
    (repository / "AGENTS.md").write_text("# A\n", encoding="utf-8")

    registry_json = json.dumps(_default_registry(10, 10), sort_keys=True)
    bad_content = (
        "# Map\n\n"
        "<!-- RCAB-MAP-V1:BEGIN -->\n```json\n" + registry_json + "\n```\n"
        "<!-- RCAB-MAP-V1:END -->\n\n"
        "<!-- RCAB-MAP-V1:BEGIN -->\n```json\n" + registry_json + "\n```\n"
        "<!-- RCAB-MAP-V1:END -->\n"
    )
    (repository / "docs" / "CONTEXT-MAP.md").write_text(bad_content, encoding="utf-8")
    _git_fixture(repository)

    with pytest.raises(tool.MeasurementError, match="expected exactly one RCAB-MAP-V1:BEGIN"):
        tool.parse_registry(repository / "docs" / "CONTEXT-MAP.md")


def test_ac_rcab_3_warning_ratchet_below_threshold(repo_root: Path, tmp_path: Path) -> None:
    """AC-RCAB-3: at/below-threshold bootstrap/router does not false-positive."""
    tool = load_measurement_tool(repo_root)

    agents = "# Agents\n" + "a" * 100
    checkpoint = "# Checkpoint\n" + "c" * 100
    agents_bytes = len(agents.encode("utf-8"))
    checkpoint_bytes = len(checkpoint.encode("utf-8"))
    registry = _default_registry(agents_bytes, checkpoint_bytes)
    repository = _make_manifest_repository(
        tmp_path,
        registry=registry,
        agents_text=agents,
        checkpoint_text=checkpoint,
    )

    manifest = tool.build_manifest(repository)
    ratchet = manifest["bootstrap_router"]

    assert ratchet["current"]["file_count"] == 2
    assert ratchet["current"]["byte_size"] == agents_bytes + checkpoint_bytes
    assert ratchet["warning"]["active"] is False
    assert ratchet["warning"]["reasons"] == []
    assert ratchet["delta"]["byte_size_ratio"] == 1.0


def test_ac_rcab_3_warning_ratchet_above_byte_threshold(repo_root: Path, tmp_path: Path) -> None:
    """AC-RCAB-3: >5% byte growth over reference produces a warning."""
    tool = load_measurement_tool(repo_root)

    # Reference: 2 files, 2000 bytes total
    ref_bytes = 2000
    ref_lines = 40
    registry = {
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
            "byte_size": ref_bytes,
            "line_count": ref_lines,
            "warning_relative_growth": 0.05,
            "blocking": False,
        },
    }

    # Current: 2101 bytes (5.05% above reference) → warning
    agents = "A" * 1050
    checkpoint = "C" * 1051
    agents_bytes = len(agents.encode("utf-8"))
    checkpoint_bytes = len(checkpoint.encode("utf-8"))
    assert agents_bytes + checkpoint_bytes > ref_bytes * 1.05

    repository = _make_manifest_repository(
        tmp_path,
        registry=registry,
        agents_text=agents,
        checkpoint_text=checkpoint,
    )

    manifest = tool.build_manifest(repository)
    ratchet = manifest["bootstrap_router"]

    assert ratchet["warning"]["active"] is True
    reasons = [r["reason"] for r in ratchet["warning"]["reasons"]]
    assert "byte_size_exceeds_warning_threshold" in reasons
    assert ratchet["current"]["file_count"] == 2


def test_ac_rcab_3_warning_ratchet_file_count_growth(repo_root: Path, tmp_path: Path) -> None:
    """AC-RCAB-3: bootstrap/router cohort > 2 files produces a warning."""
    tool = load_measurement_tool(repo_root)

    registry = {
        "schema_version": "1.0.0",
        "entries": [
            {"path": "AGENTS.md", "class": "bootstrap", "routes": ["cold-start"]},
            {
                "path": "docs/orchestrator/CHECKPOINT.md",
                "class": "router",
                "routes": ["cold-start"],
            },
            {"path": "docs/EXTRA-ROUTER.md", "class": "bootstrap", "routes": ["cold-start"]},
            {"path": "docs/CONTEXT-MAP.md", "class": "focused", "routes": ["icae-rcab"]},
        ],
        "bootstrap_ratchet": {
            "reference": "T030-R2",
            "file_count": 2,
            "byte_size": 200,
            "line_count": 10,
            "warning_relative_growth": 0.05,
            "blocking": False,
        },
    }

    agents = "# Agents\n"
    checkpoint = "# Checkpoint\n"
    extra = "# Extra\n"
    repository = _make_manifest_repository(
        tmp_path,
        registry=registry,
        agents_text=agents,
        checkpoint_text=checkpoint,
    )
    (repository / "docs" / "EXTRA-ROUTER.md").write_text(extra, encoding="utf-8")
    git(repository, "add", ".")
    git(
        repository,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-qm",
        "add extra router",
    )

    manifest = tool.build_manifest(repository)
    ratchet = manifest["bootstrap_router"]

    assert ratchet["current"]["file_count"] == 3
    assert ratchet["warning"]["active"] is True
    reasons = [r["reason"] for r in ratchet["warning"]["reasons"]]
    assert "file_count_exceeds_reference" in reasons


def test_ac_rcab_3_warning_ratchet_ratchet_candidate(repo_root: Path, tmp_path: Path) -> None:
    """AC-RCAB-3: footprint below reference reports a ratchet_candidate."""
    tool = load_measurement_tool(repo_root)

    registry = {
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
            "byte_size": 10000,
            "line_count": 200,
            "warning_relative_growth": 0.05,
            "blocking": False,
        },
    }

    agents = "A" * 100
    checkpoint = "C" * 100
    repository = _make_manifest_repository(
        tmp_path,
        registry=registry,
        agents_text=agents,
        checkpoint_text=checkpoint,
    )

    manifest = tool.build_manifest(repository)
    ratchet = manifest["bootstrap_router"]

    assert ratchet["current"]["byte_size"] == 200
    assert ratchet["ratchet_candidate"] is not None
    assert ratchet["ratchet_candidate"]["byte_size"] == 200
    assert ratchet["warning"]["active"] is False


def test_ac_rcab_3_warning_only_exit_success(repo_root: Path, tmp_path: Path) -> None:
    """AC-RCAB-3: warning-only run exits success (no integrity failure)."""
    tool_path = repo_root / "tools" / "repository_context.py"
    ref_bytes = 100
    registry = {
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
            "byte_size": ref_bytes,
            "line_count": 5,
            "warning_relative_growth": 0.05,
            "blocking": False,
        },
    }

    agents = "A" * 200
    checkpoint = "C" * 200
    repository = _make_manifest_repository(
        tmp_path,
        registry=registry,
        agents_text=agents,
        checkpoint_text=checkpoint,
    )
    manifest_path = repository / "baselines" / "manifest-v1.json"
    cmd_gen = [
        sys.executable,
        str(tool_path),
        "--source-root",
        str(repository),
        "--manifest",
        "--output",
        str(manifest_path),
    ]
    subprocess.run(cmd_gen, check=True, capture_output=True, timeout=30)

    cmd_check = [
        sys.executable,
        str(tool_path),
        "--source-root",
        str(repository),
        "--check-manifest",
        str(manifest_path),
    ]
    result = subprocess.run(cmd_check, check=False, capture_output=True, text=True, timeout=30)

    assert result.returncode == 0
    assert "warning" in result.stdout.lower()


def test_ac_rcab_4_stale_manifest_rejected(repo_root: Path, tmp_path: Path) -> None:
    """AC-RCAB-4: stale/tampered manifest is deterministically rejected."""
    tool = load_measurement_tool(repo_root)
    repository = _make_manifest_repository(tmp_path)
    manifest_path = repository / tool.DEFAULT_MANIFEST

    tool.write_manifest(repository, manifest_path)
    exit_code, message = tool.check_manifest(repository, manifest_path)
    assert exit_code == 0
    assert "OK" in message

    # Tamper with manifest content
    tampered = json.loads(manifest_path.read_bytes())
    tampered["registered_content_digest"] = "0" * 64
    manifest_path.write_text(
        json.dumps(tampered, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    exit_code, message = tool.check_manifest(repository, manifest_path)
    assert exit_code == 1
    assert "stale or tampered" in message

    # Regenerate fresh — check passes again
    tool.write_manifest(repository, manifest_path)
    exit_code, message = tool.check_manifest(repository, manifest_path)
    assert exit_code == 0


def test_ac_rcab_4_stale_manifest_after_content_change(repo_root: Path, tmp_path: Path) -> None:
    """AC-RCAB-4: manifest becomes stale when registered content changes."""
    tool = load_measurement_tool(repo_root)
    agents = "# Agents\n"
    checkpoint = "# Checkpoint\n"
    registry = _default_registry(len(agents.encode()), len(checkpoint.encode()))
    repository = _make_manifest_repository(
        tmp_path,
        registry=registry,
        agents_text=agents,
        checkpoint_text=checkpoint,
    )
    manifest_path = repository / tool.DEFAULT_MANIFEST
    tool.write_manifest(repository, manifest_path)
    assert tool.check_manifest(repository, manifest_path)[0] == 0

    # Modify registered content
    (repository / "AGENTS.md").write_text("# Agents\n\nchanged\n", encoding="utf-8")
    git(repository, "add", ".")
    git(
        repository,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-qm",
        "change content",
    )

    exit_code, message = tool.check_manifest(repository, manifest_path)
    assert exit_code == 1
    assert "stale or tampered" in message


def test_ac_rcab_5_manifest_stays_outside_consumer_package(repo_root: Path) -> None:
    """AC-RCAB-5: manifest and tooling remain outside the T020 Consumer package."""
    manifest_path = repo_root / "baselines" / "repository-context-manifest-v1.json"
    tool_path = repo_root / "tools" / "repository_context.py"

    assert manifest_path.exists()
    assert tool_path.parent.name == "tools"
    assert repo_root / "src" / "agent_governance" not in tool_path.parents

    # Manifest is not inside any Consumer artifact source dir
    consumer_dirs = ("governance-core", "governance-skill", "src/agent_governance")
    for consumer in consumer_dirs:
        assert consumer not in manifest_path.parts


def test_ac_rcab_6_no_mutation_drift(repo_root: Path, tmp_path: Path) -> None:
    """AC-RCAB-6: generation/check does not rewrite Markdown or introduce deps."""
    tool = load_measurement_tool(repo_root)
    repository = _make_manifest_repository(tmp_path)
    manifest_path = repository / tool.DEFAULT_MANIFEST

    before_docs = {path: path.read_bytes() for path in repository.rglob("*.md")}

    tool.write_manifest(repository, manifest_path)
    tool.check_manifest(repository, manifest_path)

    after_docs = {path: path.read_bytes() for path in repository.rglob("*.md")}
    assert before_docs == after_docs

    # No network or dependency changes — manifest uses only stdlib
    import ast as _ast

    source = (repo_root / "tools" / "repository_context.py").read_text()
    tree = _ast.parse(source)
    imports = [
        node.names[0].name if isinstance(node, _ast.Import) else node.module
        for node in _ast.walk(tree)
        if isinstance(node, (_ast.Import, _ast.ImportFrom))
    ]
    for imp in imports:
        if imp is None:
            continue
        top = imp.split(".")[0]
        assert top in (
            "argparse",
            "hashlib",
            "json",
            "os",
            "posixpath",
            "re",
            "subprocess",
            "tempfile",
            "pathlib",
            "__future__",
        ), f"unexpected import: {top}"


def test_manifest_cli_check_on_real_repository(repo_root: Path) -> None:
    """The committed manifest on the real repository passes check_manifest."""
    tool = load_measurement_tool(repo_root)
    manifest_path = repo_root / tool.DEFAULT_MANIFEST
    assert manifest_path.exists()

    exit_code, message = tool.check_manifest(repo_root, manifest_path)
    assert exit_code == 0
    assert "OK" in message


def test_manifest_does_not_embed_git_sha(repo_root: Path) -> None:
    """The committed manifest must not require or embed a Git commit SHA."""
    manifest_path = repo_root / "baselines" / "repository-context-manifest-v1.json"
    raw = manifest_path.read_bytes()
    manifest = json.loads(raw)

    for key in manifest:
        assert "git" not in key.lower()
        assert "sha" not in key.lower() or key in ("registry_digest", "registered_content_digest")
        assert "commit" not in key.lower()

    for entry in manifest["registered_paths"]:
        assert entry["sha256"] != ""
        assert "source_git_revision" not in entry
        assert "commit_sha" not in entry

    assert b"volatile_execution_metadata" not in raw
    assert b"source_git_revision" not in raw
