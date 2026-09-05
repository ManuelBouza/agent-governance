"""Focused repository-context semantic coverage."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from _repository_context_helpers import (
    _default_registry,
    _make_manifest_repository,
    git,
    load_measurement_tool,
)


def test_ac_t032_3_tampered_projection_detected_by_integrity(
    repo_root: Path, tmp_path: Path
) -> None:
    """AC-T032-3: tampered projection is deterministically detectable by integrity validation."""
    tool = load_measurement_tool(repo_root)
    repository = _make_manifest_repository(tmp_path)
    manifest_path = repository / tool.DEFAULT_MANIFEST
    tool.write_manifest(repository, manifest_path)

    # Integrity validation passes on clean manifest
    tool.validate_snapshot_integrity(manifest_path)

    # Tamper with registered_content_digest
    tampered = json.loads(manifest_path.read_bytes())
    tampered["registered_content_digest"] = "0" * 64
    manifest_path.write_text(
        json.dumps(tampered, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="",
    )

    with pytest.raises(tool.MeasurementError, match="registered_content_digest mismatch"):
        tool.validate_snapshot_integrity(manifest_path)


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("path", "../AGENTS.md", "invalid registered path"),
        ("class", "unknown", "invalid class"),
        ("routes", ["z-route", "a-route"], "routes must be non-empty, unique, and sorted"),
        ("byte_size", True, "invalid byte_size"),
        ("line_count", -1, "invalid line_count"),
        ("sha256", "A" * 64, "invalid sha256"),
    ],
)
def test_ac_t032_3_entry_type_value_controls_reject_tampering(
    repo_root: Path,
    tmp_path: Path,
    field: str,
    value: object,
    error: str,
) -> None:
    """AC-T032-3: entry fields enforce deterministic type and value constraints."""
    tool = load_measurement_tool(repo_root)
    repository = _make_manifest_repository(tmp_path)
    manifest_path = repository / tool.DEFAULT_MANIFEST
    tool.write_manifest(repository, manifest_path)

    tampered = json.loads(manifest_path.read_bytes())
    tampered["registered_paths"][0][field] = value
    tampered[tool.SNAPSHOT_PAYLOAD_DIGEST_KEY] = tool.compute_snapshot_payload_digest(tampered)
    manifest_path.write_bytes(tool.canonical_json(tampered))

    with pytest.raises(tool.MeasurementError, match=error):
        tool.validate_snapshot_integrity(manifest_path)


def test_ac_t032_3_entry_canonical_order_rejects_tampering(repo_root: Path, tmp_path: Path) -> None:
    """AC-T032-3: registered entries must retain canonical path order."""
    tool = load_measurement_tool(repo_root)
    repository = _make_manifest_repository(tmp_path)
    manifest_path = repository / tool.DEFAULT_MANIFEST
    tool.write_manifest(repository, manifest_path)

    tampered = json.loads(manifest_path.read_bytes())
    tampered["registered_paths"].reverse()
    tampered[tool.SNAPSHOT_PAYLOAD_DIGEST_KEY] = tool.compute_snapshot_payload_digest(tampered)
    manifest_path.write_bytes(tool.canonical_json(tampered))

    with pytest.raises(tool.MeasurementError, match="unique paths in canonical order"):
        tool.validate_snapshot_integrity(manifest_path)


@pytest.mark.parametrize("field", ["class", "routes"])
def test_ac_t032_3_class_and_routes_must_match_registry_semantics(
    repo_root: Path, tmp_path: Path, field: str
) -> None:
    """AC-T032-3 R1 control A1: class/routes tampering fails after digest refresh."""
    tool = load_measurement_tool(repo_root)
    repository = _make_manifest_repository(tmp_path)
    manifest_path = repository / tool.DEFAULT_MANIFEST
    tool.write_manifest(repository, manifest_path)

    tampered = json.loads(manifest_path.read_bytes())
    tampered["registered_paths"][0][field] = "focused" if field == "class" else ["alternate-route"]
    tampered[tool.SNAPSHOT_PAYLOAD_DIGEST_KEY] = tool.compute_snapshot_payload_digest(tampered)
    manifest_path.write_bytes(tool.canonical_json(tampered))

    with pytest.raises(tool.MeasurementError, match="metadata does not match snapshot registry"):
        tool.validate_snapshot_integrity(manifest_path)


def test_ac_t032_3_focused_physical_metrics_bound_by_payload_digest(
    repo_root: Path, tmp_path: Path
) -> None:
    """AC-T032-3 R1 control A2: focused physical metrics are payload-bound."""
    tool = load_measurement_tool(repo_root)
    repository = _make_manifest_repository(tmp_path)
    manifest_path = repository / tool.DEFAULT_MANIFEST
    tool.write_manifest(repository, manifest_path)

    tampered = json.loads(manifest_path.read_bytes())
    focused = next(entry for entry in tampered["registered_paths"] if entry["class"] == "focused")
    focused["byte_size"] += 1
    focused["line_count"] += 1
    manifest_path.write_bytes(tool.canonical_json(tampered))

    with pytest.raises(tool.MeasurementError, match="snapshot_payload_digest mismatch"):
        tool.validate_snapshot_integrity(manifest_path)


def test_ac_t032_3_registry_identity_recomputed_from_snapshot_semantics(
    repo_root: Path, tmp_path: Path
) -> None:
    """AC-T032-3 R1 control B: arbitrary registry identity is rejected."""
    tool = load_measurement_tool(repo_root)
    repository = _make_manifest_repository(tmp_path)
    manifest_path = repository / tool.DEFAULT_MANIFEST
    tool.write_manifest(repository, manifest_path)

    tampered = json.loads(manifest_path.read_bytes())
    tampered["registry_digest"] = "0" * 64
    tampered[tool.SNAPSHOT_PAYLOAD_DIGEST_KEY] = tool.compute_snapshot_payload_digest(tampered)
    manifest_path.write_bytes(tool.canonical_json(tampered))

    with pytest.raises(tool.MeasurementError, match="registry_digest mismatch"):
        tool.validate_snapshot_integrity(manifest_path)


@pytest.mark.parametrize(
    "field",
    [
        "files",
        "current",
        "accepted_reference",
        "delta",
        "warning",
        "warning_reasons",
        "ratchet_candidate",
    ],
)
def test_ac_t032_3_bootstrap_state_recomputed_from_snapshot_entries(
    repo_root: Path, tmp_path: Path, field: str
) -> None:
    """AC-T032-3 R1 control C: derived bootstrap state is exactly recomputed."""
    tool = load_measurement_tool(repo_root)
    repository = _make_manifest_repository(tmp_path)
    manifest_path = repository / tool.DEFAULT_MANIFEST
    tool.write_manifest(repository, manifest_path)

    tampered = json.loads(manifest_path.read_bytes())
    if field == "files":
        tampered["bootstrap_router"][field].reverse()
    elif field in ("current", "accepted_reference"):
        tampered["bootstrap_router"][field]["byte_size"] += 1
    elif field == "delta":
        tampered["bootstrap_router"][field]["byte_size_delta"] += 1
    elif field == "warning":
        tampered["bootstrap_router"][field]["active"] = not tampered["bootstrap_router"][field][
            "active"
        ]
    elif field == "warning_reasons":
        tampered["bootstrap_router"]["warning"]["reasons"].append({"reason": "tampered"})
    else:
        tampered["bootstrap_router"][field] = {"file_count": 0, "byte_size": 0, "line_count": 0}
    tampered[tool.SNAPSHOT_PAYLOAD_DIGEST_KEY] = tool.compute_snapshot_payload_digest(tampered)
    manifest_path.write_bytes(tool.canonical_json(tampered))

    with pytest.raises(tool.MeasurementError, match="bootstrap_router does not match"):
        tool.validate_snapshot_integrity(manifest_path)


def test_ac_t032_3_noncanonical_json_bytes_rejected(repo_root: Path, tmp_path: Path) -> None:
    """AC-T032-3: semantically equivalent noncanonical JSON is rejected."""
    tool = load_measurement_tool(repo_root)
    repository = _make_manifest_repository(tmp_path)
    manifest_path = repository / tool.DEFAULT_MANIFEST
    tool.write_manifest(repository, manifest_path)

    manifest = json.loads(manifest_path.read_bytes())
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="")

    with pytest.raises(tool.MeasurementError, match="JSON bytes are not canonical"):
        tool.validate_snapshot_integrity(manifest_path)


def test_ac_t032_3_tampered_projection_detected_by_currentness(
    repo_root: Path, tmp_path: Path
) -> None:
    """AC-T032-3: tampered projection is also detectable by explicit currentness comparison."""
    tool = load_measurement_tool(repo_root)
    repository = _make_manifest_repository(tmp_path)
    manifest_path = repository / tool.DEFAULT_MANIFEST
    tool.write_manifest(repository, manifest_path)

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


def test_ac_t032_4_historical_snapshot_does_not_poison_regression(
    repo_root: Path, tmp_path: Path
) -> None:
    """AC-T032-4: valid old snapshot + legitimate content change keeps regression green.

    The default regression path validates snapshot integrity (not currentness).
    An internally valid historical snapshot must not make the ordinary suite red
    merely because registered Markdown evolved. Explicit currentness comparison
    correctly reports the snapshot as stale.
    """
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

    # Generate a historical snapshot
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

    # Legitimate registered content evolution
    (repository / "AGENTS.md").write_text("# Agents\n\nnew content\n", encoding="utf-8", newline="")
    git(repository, "add", ".")
    git(
        repository,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-qm",
        "legitimate evolution",
    )

    # Default regression: snapshot internal integrity is still valid
    tool.validate_snapshot_integrity(manifest_path)

    # Explicit currentness: snapshot is stale (deliberate comparison)
    exit_code, message = tool.check_manifest(repository, manifest_path)
    assert exit_code == 1
    assert "stale or tampered" in message

    # Live status: computed from current source, not from snapshot
    live = tool.build_live_status(repository)
    live_agents = next(e for e in live["registered_paths"] if e["path"] == "AGENTS.md")
    assert live_agents["byte_size"] == len(b"# Agents\n\nnew content\n")


def test_ac_t032_5_d047_ratchet_preserved(repo_root: Path) -> None:
    """AC-T032-5: D047 ratchet reference is unchanged in the committed snapshot."""
    tool = load_measurement_tool(repo_root)
    manifest_path = repo_root / tool.DEFAULT_MANIFEST
    committed = tool.validate_snapshot_integrity(manifest_path)

    ratchet = committed["bootstrap_router"]["accepted_reference"]
    assert ratchet["file_count"] == 2
    assert ratchet["byte_size"] == 21471
    assert ratchet["line_count"] == 298
    assert ratchet["warning_relative_growth"] == 0.05
    assert ratchet["blocking"] is False
    assert ratchet["reference"] == "T030-R2"


def test_ac_t032_5_warning_only_live_status_is_success(repo_root: Path, tmp_path: Path) -> None:
    """AC-T032-5: warning-only live status remains non-blocking success."""
    tool = load_measurement_tool(repo_root)

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

    live = tool.build_live_status(repository)
    assert live["bootstrap_router"]["warning"]["active"] is True
    assert live["bootstrap_router"]["accepted_reference"]["blocking"] is False

    # CLI live-status on warning-only state exits 0
    tool_path = repo_root / "tools" / "repository_context.py"
    cmd = [
        sys.executable,
        str(tool_path),
        "--source-root",
        str(repository),
        "--live-status",
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, timeout=30)
    cli_status = json.loads(result.stdout)
    assert cli_status["status_type"] == tool.LIVE_STATUS_TYPE
    assert cli_status["bootstrap_router"]["warning"]["active"] is True


def test_ac_t032_6_source_only_package_isolation(repo_root: Path) -> None:
    """AC-T032-6: RCAB tooling/snapshot remain source-only and outside Consumer artifact."""
    tool_path = repo_root / "tools" / "repository_context.py"
    manifest_path = repo_root / "baselines" / "repository-context-manifest-v1.json"

    assert tool_path.parent.name == "tools"
    assert repo_root / "src" / "agent_governance" not in tool_path.parents

    assert manifest_path.exists()
    consumer_dirs = ("governance-core", "governance-skill", "src/agent_governance")
    for consumer in consumer_dirs:
        assert consumer not in manifest_path.parts

    # Live status tooling also stays outside Consumer package
    load_measurement_tool(repo_root)
    assert tool_path.parent.name == "tools"


def test_live_status_on_real_repository(repo_root: Path) -> None:
    """Live RCAB status on the real repository computes from current source."""
    tool = load_measurement_tool(repo_root)
    live = tool.build_live_status(repo_root)

    assert live["status_type"] == tool.LIVE_STATUS_TYPE
    assert live["status_semantics"] == tool.LIVE_STATUS_SEMANTICS
    assert "registered_paths" in live
    assert len(live["registered_paths"]) >= 2
    assert live["bootstrap_router"]["accepted_reference"]["file_count"] == 2
    assert live["bootstrap_router"]["accepted_reference"]["byte_size"] == 21471


def test_snapshot_v1_0_0_backwards_compatible_integrity(repo_root: Path, tmp_path: Path) -> None:
    """A v1.0.0 snapshot (pre-epoch-fields) passes integrity validation."""
    tool = load_measurement_tool(repo_root)
    repository = _make_manifest_repository(tmp_path)
    manifest_path = repository / tool.DEFAULT_MANIFEST
    tool.write_manifest(repository, manifest_path)

    # Downgrade to v1.0.0 format (remove epoch snapshot fields)
    raw = json.loads(manifest_path.read_bytes())
    raw["projection_schema_version"] = "1.0.0"
    raw.pop("snapshot_type", None)
    raw.pop("snapshot_semantics", None)
    raw.pop("registry", None)
    raw.pop("excluded_paths", None)
    raw.pop("snapshot_payload_digest", None)
    # Recompute digest since we haven't changed registered_paths — it's still valid
    manifest_path.write_text(
        json.dumps(raw, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="",
    )

    committed = tool.validate_snapshot_integrity(manifest_path)
    assert committed["projection_schema_version"] == "1.0.0"
    assert "snapshot_type" not in committed
