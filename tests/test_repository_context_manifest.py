"""Focused repository-context semantic coverage."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from _repository_context_helpers import (
    _default_registry,
    _make_manifest_repository,
    git,
    load_measurement_tool,
)


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
        newline="",
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
    (repository / "AGENTS.md").write_text("# Agents\n\nchanged\n", encoding="utf-8", newline="")
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

    implementation_paths = [repo_root / "tools" / "repository_context.py"]
    implementation_paths.extend(sorted((repo_root / "tools" / "_repository_context").glob("*.py")))
    for implementation_path in implementation_paths:
        tree = _ast.parse(implementation_path.read_text())
        for node in _ast.walk(tree):
            if not isinstance(node, (_ast.Import, _ast.ImportFrom)):
                continue
            if isinstance(node, _ast.ImportFrom) and node.level:
                continue
            imported = node.names[0].name if isinstance(node, _ast.Import) else node.module
            assert imported is not None
            top = imported.split(".")[0]
            assert top in sys.stdlib_module_names or top == "_repository_context", (
                f"unexpected import in {implementation_path.relative_to(repo_root)}: {top}"
            )


def test_manifest_snapshot_integrity_on_real_repository(repo_root: Path) -> None:
    """Validate committed snapshot internal integrity without requiring currentness.

    The ordinary default regression suite validates snapshot canonical/internal
    integrity. A historical snapshot that predates legitimate registered-file
    evolution remains internally valid and MUST NOT make the regression red.
    Explicit currentness comparison is a separate deliberate operation.
    """
    tool = load_measurement_tool(repo_root)
    manifest_path = repo_root / tool.DEFAULT_MANIFEST
    assert manifest_path.exists()

    committed = tool.validate_snapshot_integrity(manifest_path)
    assert committed["projection_schema_version"] == tool.MANIFEST_SCHEMA_VERSION
    assert committed["snapshot_type"] == tool.SNAPSHOT_TYPE
    assert committed["snapshot_semantics"] == tool.SNAPSHOT_SEMANTICS


def test_manifest_does_not_embed_git_sha(repo_root: Path) -> None:
    """The committed manifest must not require or embed a Git commit SHA."""
    manifest_path = repo_root / "baselines" / "repository-context-manifest-v1.json"
    raw = manifest_path.read_bytes()
    manifest = json.loads(raw)

    for key in manifest:
        assert "git" not in key.lower()
        assert "sha" not in key.lower() or key in (
            "registry_digest",
            "registered_content_digest",
            "snapshot_payload_digest",
        )
        assert "commit" not in key.lower()

    for entry in manifest["registered_paths"]:
        assert entry["sha256"] != ""
        assert "source_git_revision" not in entry
        assert "commit_sha" not in entry

    assert b"volatile_execution_metadata" not in raw
    assert b"source_git_revision" not in raw


# ---------------------------------------------------------------------------
# T032 — RCAB snapshot/live separation (AC-T032-1 .. AC-T032-6)
# ---------------------------------------------------------------------------


def test_ac_t032_1_epoch_snapshot_semantics_machine_visible(
    repo_root: Path, tmp_path: Path
) -> None:
    """AC-T032-1: snapshot has machine-visible epoch semantics and is byte-identical on repeat.

    Repeated generation from identical registry/content inputs produces
    byte-identical canonical output with explicit epoch/snapshot semantics,
    canonical ordering, stable registered-content identity and no
    self-reference or Git-commit self-reference requirement.
    """
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
    assert manifest["snapshot_type"] == tool.SNAPSHOT_TYPE
    assert manifest["snapshot_semantics"] == tool.SNAPSHOT_SEMANTICS

    # Machine-visible: snapshot fields clearly distinguish from live authority
    assert "epoch" in manifest["snapshot_type"]
    assert "not_live" in manifest["snapshot_semantics"]

    # Canonical ordering preserved
    paths = [e["path"] for e in manifest["registered_paths"]]
    assert paths == sorted(paths)

    # No Git self-reference
    assert b"source_git_revision" not in first
    assert b"volatile_execution_metadata" not in first


def test_ac_t032_1_snapshot_integrity_validates_without_currentness(
    repo_root: Path, tmp_path: Path
) -> None:
    """AC-T032-1: snapshot internal integrity is self-contained and validatable."""
    tool = load_measurement_tool(repo_root)
    repository = _make_manifest_repository(tmp_path)
    manifest_path = repository / tool.DEFAULT_MANIFEST
    tool.write_manifest(repository, manifest_path)

    # Integrity validation does not require current source to match
    committed = tool.validate_snapshot_integrity(manifest_path)
    assert committed["snapshot_type"] == tool.SNAPSHOT_TYPE
    assert committed["registered_content_digest"] != ""


def test_ac_t032_2_live_status_from_current_source(repo_root: Path, tmp_path: Path) -> None:
    """AC-T032-2: live status is computed from current files, not from snapshot."""
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

    # Generate and commit a snapshot
    manifest_path = repository / tool.DEFAULT_MANIFEST
    tool.write_manifest(repository, manifest_path)
    git(repository, "add", ".")
    git(
        repository,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-qm",
        "snapshot epoch",
    )

    # Modify a registered file AFTER the snapshot
    new_agents = "# Agents\n\nupdated\n"
    (repository / "AGENTS.md").write_text(new_agents, encoding="utf-8", newline="")
    git(repository, "add", ".")
    git(
        repository,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-qm",
        "content evolution",
    )

    # Live status computed from CURRENT files
    live = tool.build_live_status(repository)
    assert live["status_type"] == tool.LIVE_STATUS_TYPE
    assert live["status_semantics"] == tool.LIVE_STATUS_SEMANTICS

    # Live status reflects the updated file, not the snapshot
    agents_entry = next(e for e in live["registered_paths"] if e["path"] == "AGENTS.md")
    assert agents_entry["byte_size"] == len(new_agents.encode("utf-8"))

    # Snapshot still has old value (it was not trusted)
    snapshot = json.loads(manifest_path.read_bytes())
    snapshot_agents = next(e for e in snapshot["registered_paths"] if e["path"] == "AGENTS.md")
    assert snapshot_agents["byte_size"] == len(agents.encode("utf-8"))

    # Live content digest differs from snapshot content digest
    assert live["registered_content_digest"] != snapshot["registered_content_digest"]


def test_ac_t032_2_live_status_recomputes_ratchet_from_current(
    repo_root: Path, tmp_path: Path
) -> None:
    """AC-T032-2: live ratchet/warning is recomputed from current files."""
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

    live = tool.build_live_status(repository)
    ratchet = live["bootstrap_router"]
    assert ratchet["current"]["file_count"] == 2
    assert ratchet["current"]["byte_size"] == len(agents.encode()) + len(checkpoint.encode())
    assert ratchet["warning"]["active"] is False
    assert ratchet["accepted_reference"]["file_count"] == 2
    assert ratchet["accepted_reference"]["warning_relative_growth"] == 0.05
    assert ratchet["accepted_reference"]["blocking"] is False


def test_ac_t032_3_explicit_currentness_fresh_and_stale(repo_root: Path, tmp_path: Path) -> None:
    """AC-T032-3: explicit currentness comparison accepts fresh, rejects stale."""
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

    # Fresh: snapshot matches current content
    tool.write_manifest(repository, manifest_path)
    exit_code, message = tool.check_manifest(repository, manifest_path)
    assert exit_code == 0
    assert "OK" in message

    # Legitimate content change makes snapshot stale
    (repository / "AGENTS.md").write_text("# Agents\n\nchanged\n", encoding="utf-8", newline="")
    git(repository, "add", ".")
    git(
        repository,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-qm",
        "content evolution",
    )

    exit_code, message = tool.check_manifest(repository, manifest_path)
    assert exit_code == 1
    assert "stale or tampered" in message
