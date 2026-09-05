"""Focused repository-context semantic coverage."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from _repository_context_helpers import (
    _default_registry,
    _git_fixture,
    _make_manifest_repository,
    _write_context_map,
    git,
    load_measurement_tool,
)


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
    manifest_path.write_text("placeholder\n", encoding="utf-8", newline="")

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
    (repository / "AGENTS.md").write_text("# A\n", encoding="utf-8", newline="")

    bad_content = (
        "# Map\n\n"
        "<!-- RCAB-MAP-V1:BEGIN -->\n"
        "```json\n{not valid json}\n```\n"
        "<!-- RCAB-MAP-V1:END -->\n"
    )
    (repository / "docs" / "CONTEXT-MAP.md").write_text(bad_content, encoding="utf-8", newline="")
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
    (repository / "AGENTS.md").write_text("# A\n", encoding="utf-8", newline="")

    registry_json = json.dumps(_default_registry(10, 10), sort_keys=True)
    bad_content = (
        "# Map\n\n"
        "<!-- RCAB-MAP-V1:BEGIN -->\n```json\n" + registry_json + "\n```\n"
        "<!-- RCAB-MAP-V1:END -->\n\n"
        "<!-- RCAB-MAP-V1:BEGIN -->\n```json\n" + registry_json + "\n```\n"
        "<!-- RCAB-MAP-V1:END -->\n"
    )
    (repository / "docs" / "CONTEXT-MAP.md").write_text(bad_content, encoding="utf-8", newline="")
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
    (repository / "docs" / "EXTRA-ROUTER.md").write_text(extra, encoding="utf-8", newline="")
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
