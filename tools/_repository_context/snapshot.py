"""RCAB epoch snapshots, live status, integrity, currentness, and writes."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path, PurePosixPath

from .common import MeasurementError, canonical_json, relative_output
from .projection import compute_ratchet, compute_rcab_projection
from .registry import (
    BOOTSTRAP_CLASSES,
    REGISTRY_SCHEMA_VERSION,
    VALID_REGISTRY_CLASSES,
    compute_registry_digest,
)

DEFAULT_MANIFEST = "baselines/repository-context-manifest-v1.json"
MANIFEST_SCHEMA_VERSION = "1.2.0"
SUPPORTED_MANIFEST_SCHEMA_VERSIONS = frozenset({"1.0.0", "1.1.0", "1.2.0"})
SNAPSHOT_PAYLOAD_DIGEST_KEY = "snapshot_payload_digest"
SNAPSHOT_TYPE = "epoch"
SNAPSHOT_SEMANTICS = "evidence_snapshot_not_live_authority"
LIVE_STATUS_TYPE = "live"
LIVE_STATUS_SEMANTICS = "computed_from_current_source_not_snapshot"


def snapshot_payload(manifest: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in manifest.items() if key != SNAPSHOT_PAYLOAD_DIGEST_KEY}


def compute_snapshot_payload_digest(manifest: dict[str, object]) -> str:
    return hashlib.sha256(canonical_json(snapshot_payload(manifest))).hexdigest()


def build_manifest(
    root: Path,
    *,
    map_path: Path | None = None,
    excluded_paths: set[str] | None = None,
) -> dict[str, object]:
    projection = compute_rcab_projection(root, map_path=map_path, excluded_paths=excluded_paths)
    manifest = {
        "projection_schema_version": MANIFEST_SCHEMA_VERSION,
        "snapshot_type": SNAPSHOT_TYPE,
        "snapshot_semantics": SNAPSHOT_SEMANTICS,
        "registry": projection["registry"],
        "excluded_paths": projection["excluded_paths"],
        "registry_digest": projection["registry_digest"],
        "registered_paths": projection["registered_paths"],
        "registered_content_digest": projection["registered_content_digest"],
        "bootstrap_router": projection["bootstrap_router"],
    }
    manifest[SNAPSHOT_PAYLOAD_DIGEST_KEY] = compute_snapshot_payload_digest(manifest)
    return manifest


def build_live_status(
    root: Path,
    *,
    map_path: Path | None = None,
    excluded_paths: set[str] | None = None,
) -> dict[str, object]:
    projection = compute_rcab_projection(root, map_path=map_path, excluded_paths=excluded_paths)
    return {
        "status_type": LIVE_STATUS_TYPE,
        "status_semantics": LIVE_STATUS_SEMANTICS,
        "registry_digest": projection["registry_digest"],
        "registered_paths": projection["registered_paths"],
        "registered_content_digest": projection["registered_content_digest"],
        "bootstrap_router": projection["bootstrap_router"],
    }


def write_manifest(root: Path, output: Path, *, map_path: Path | None = None) -> dict[str, object]:
    root = root.resolve()
    relative = relative_output(root, output)
    manifest = build_manifest(
        root,
        map_path=map_path,
        excluded_paths={relative} if relative is not None else set(),
    )
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(canonical_json(manifest))
    temporary.replace(output)
    return manifest


def check_manifest(
    root: Path, manifest_path: Path, *, map_path: Path | None = None
) -> tuple[int, str]:
    root = root.resolve()
    relative = relative_output(root, manifest_path)
    current = build_manifest(
        root,
        map_path=map_path,
        excluded_paths={relative} if relative is not None else set(),
    )
    if manifest_path.read_bytes() != canonical_json(current):
        return 1, (
            "manifest is stale or tampered: committed projection does not match "
            "deterministic regeneration from current registry and registered content"
        )
    warning = current["bootstrap_router"]["warning"]
    if warning["active"]:
        parts = [
            f"{reason['reason']}"
            f" (current={reason.get('current')}, reference={reason.get('reference')})"
            for reason in warning["reasons"]
        ]
        return 0, "manifest OK (warning: " + "; ".join(parts) + ")"
    return 0, "manifest OK"


def require_nonnegative_int(value: object, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise MeasurementError(f"invalid {field}: {value!r}")
    return value


def require_digest(value: object, field: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or value != value.lower():
        raise MeasurementError(f"invalid {field}: {value!r}")
    try:
        int(value, 16)
    except ValueError as error:
        raise MeasurementError(f"{field} is not a lowercase hex string: {value!r}") from error
    return value


def validate_snapshot_entry(entry: object) -> dict[str, object]:
    required = {"path", "class", "routes", "byte_size", "line_count", "sha256"}
    if not isinstance(entry, dict) or set(entry) != required:
        raise MeasurementError("registered path entry must contain exactly canonical entry fields")
    path = entry["path"]
    if (
        not isinstance(path, str)
        or not path
        or PurePosixPath(path).is_absolute()
        or PurePosixPath(path).as_posix() != path
        or ".." in PurePosixPath(path).parts
    ):
        raise MeasurementError(f"invalid registered path: {path!r}")
    if entry["class"] not in VALID_REGISTRY_CLASSES:
        raise MeasurementError(f"invalid class for path {path!r}: {entry['class']!r}")
    routes = entry["routes"]
    if (
        not isinstance(routes, list)
        or not routes
        or not all(isinstance(route, str) and route for route in routes)
        or routes != sorted(set(routes))
    ):
        raise MeasurementError(f"routes must be non-empty, unique, and sorted for path {path!r}")
    require_nonnegative_int(entry["byte_size"], f"byte_size for path {path!r}")
    if entry["line_count"] is not None:
        require_nonnegative_int(entry["line_count"], f"line_count for path {path!r}")
    require_digest(entry["sha256"], f"sha256 for path {path!r}")
    return entry


def validate_snapshot_registry_entry(entry: object) -> dict[str, object]:
    if not isinstance(entry, dict) or set(entry) != {"path", "class", "routes"}:
        raise MeasurementError("snapshot registry entry must contain exactly path, class, routes")
    path = entry["path"]
    if (
        not isinstance(path, str)
        or not path
        or PurePosixPath(path).is_absolute()
        or PurePosixPath(path).as_posix() != path
        or ".." in PurePosixPath(path).parts
    ):
        raise MeasurementError(f"invalid snapshot registry path: {path!r}")
    if entry["class"] not in VALID_REGISTRY_CLASSES:
        raise MeasurementError(f"invalid snapshot registry class for {path!r}")
    routes = entry["routes"]
    if (
        not isinstance(routes, list)
        or not routes
        or not all(isinstance(route, str) and route for route in routes)
        or routes != sorted(set(routes))
    ):
        raise MeasurementError(f"invalid snapshot registry routes for {path!r}")
    return entry


def validate_snapshot_reference(reference: object) -> None:
    required_reference = {
        "reference",
        "file_count",
        "byte_size",
        "line_count",
        "warning_relative_growth",
        "blocking",
    }
    if not isinstance(reference, dict) or set(reference) != required_reference:
        raise MeasurementError("snapshot registry bootstrap_ratchet has invalid fields")
    if not isinstance(reference["reference"], str) or not reference["reference"]:
        raise MeasurementError("snapshot registry bootstrap_ratchet.reference must be non-empty")
    for field in ("file_count", "byte_size", "line_count"):
        require_nonnegative_int(reference[field], f"bootstrap_ratchet.{field}")
    growth = reference["warning_relative_growth"]
    if isinstance(growth, bool) or not isinstance(growth, (int, float)) or not 0 <= growth <= 1:
        raise MeasurementError(f"invalid bootstrap_ratchet.warning_relative_growth: {growth!r}")
    if not isinstance(reference["blocking"], bool):
        raise MeasurementError(f"invalid bootstrap_ratchet.blocking: {reference['blocking']!r}")


def validate_snapshot_registry(registry: object) -> dict[str, object]:
    if not isinstance(registry, dict) or set(registry) != {
        "schema_version",
        "entries",
        "bootstrap_ratchet",
    }:
        raise MeasurementError("snapshot registry must contain exactly canonical registry fields")
    if registry["schema_version"] != REGISTRY_SCHEMA_VERSION:
        raise MeasurementError(
            f"unsupported snapshot registry schema: {registry['schema_version']!r}"
        )
    entries = registry["entries"]
    if not isinstance(entries, list) or not entries:
        raise MeasurementError("snapshot registry entries must be a non-empty list")
    for entry in entries:
        validate_snapshot_registry_entry(entry)
    registry_paths = [entry["path"] for entry in entries]
    if registry_paths != sorted(set(registry_paths)):
        raise MeasurementError(
            "snapshot registry entries must have unique paths in canonical order"
        )
    validate_snapshot_reference(registry["bootstrap_ratchet"])
    return registry


def load_canonical_manifest(manifest_path: Path) -> dict[str, object]:
    raw = manifest_path.read_bytes()
    try:
        committed = json.loads(raw)
    except json.JSONDecodeError as error:
        raise MeasurementError(f"manifest is not valid JSON: {error}") from error
    if not isinstance(committed, dict):
        raise MeasurementError("manifest must be a JSON object")
    if raw != canonical_json(committed):
        raise MeasurementError("manifest JSON bytes are not canonical")
    return committed


def validate_snapshot_envelope(
    committed: dict[str, object],
) -> tuple[str, str]:
    schema = committed.get("projection_schema_version")
    if schema not in SUPPORTED_MANIFEST_SCHEMA_VERSIONS:
        raise MeasurementError(
            f"unsupported projection_schema_version: {schema!r}; "
            f"supported: {sorted(SUPPORTED_MANIFEST_SCHEMA_VERSIONS)}"
        )
    if schema != "1.0.0":
        if committed.get("snapshot_type") != SNAPSHOT_TYPE:
            raise MeasurementError(
                f"missing or invalid snapshot_type: {committed.get('snapshot_type')!r}; "
                f"expected {SNAPSHOT_TYPE!r}"
            )
        if committed.get("snapshot_semantics") != SNAPSHOT_SEMANTICS:
            raise MeasurementError(
                f"missing or invalid snapshot_semantics: {committed.get('snapshot_semantics')!r}; "
                f"expected {SNAPSHOT_SEMANTICS!r}"
            )
    registry_digest = require_digest(committed.get("registry_digest"), "registry_digest")
    return schema, registry_digest


def validate_bootstrap_router(committed: dict[str, object]) -> dict[str, object]:
    bootstrap_router = committed.get("bootstrap_router")
    if not isinstance(bootstrap_router, dict):
        raise MeasurementError("manifest must contain a 'bootstrap_router' object")
    for field in (
        "files",
        "current",
        "accepted_reference",
        "delta",
        "warning",
        "ratchet_candidate",
    ):
        if field not in bootstrap_router:
            raise MeasurementError(f"bootstrap_router missing required field: {field}")
    return bootstrap_router


def validate_registered_content(
    committed: dict[str, object],
) -> tuple[list[dict[str, object]], list[str]]:
    registered_paths = committed.get("registered_paths")
    if not isinstance(registered_paths, list) or not registered_paths:
        raise MeasurementError("manifest must contain a non-empty 'registered_paths' list")
    paths = [validate_snapshot_entry(entry)["path"] for entry in registered_paths]
    if paths != sorted(set(paths)):
        raise MeasurementError("registered_paths must have unique paths in canonical order")
    content_identity = [{"path": e["path"], "sha256": e["sha256"]} for e in registered_paths]
    expected_digest = hashlib.sha256(canonical_json(content_identity)).hexdigest()
    actual_digest = require_digest(
        committed.get("registered_content_digest"), "registered_content_digest"
    )
    if actual_digest != expected_digest:
        raise MeasurementError(
            f"registered_content_digest mismatch: manifest claims {actual_digest!r} "
            f"but registered_paths compute to {expected_digest!r}"
        )
    return registered_paths, paths


def validate_current_snapshot_integrity(
    committed: dict[str, object],
    registry_digest: str,
    registered_paths: list[dict[str, object]],
    paths: list[str],
    bootstrap_router: dict[str, object],
) -> None:
    required_fields = {
        "projection_schema_version",
        "snapshot_type",
        "snapshot_semantics",
        "registry",
        "excluded_paths",
        "registry_digest",
        "registered_paths",
        "registered_content_digest",
        "bootstrap_router",
        SNAPSHOT_PAYLOAD_DIGEST_KEY,
    }
    if set(committed) != required_fields:
        raise MeasurementError("manifest must contain exactly canonical snapshot fields")
    registry = validate_snapshot_registry(committed["registry"])
    expected_registry_digest = compute_registry_digest(registry)
    if registry_digest != expected_registry_digest:
        raise MeasurementError(
            f"registry_digest mismatch: manifest claims {registry_digest!r} "
            f"but snapshot registry computes to {expected_registry_digest!r}"
        )
    excluded_paths = committed["excluded_paths"]
    registry_entries = registry["entries"]
    registry_paths = [entry["path"] for entry in registry_entries]
    if (
        not isinstance(excluded_paths, list)
        or not all(isinstance(path, str) and path in registry_paths for path in excluded_paths)
        or excluded_paths != sorted(set(excluded_paths))
    ):
        raise MeasurementError("excluded_paths must be unique registered paths in canonical order")
    expected_paths = [path for path in registry_paths if path not in excluded_paths]
    if paths != expected_paths:
        raise MeasurementError("registered_paths do not match snapshot registry and exclusions")
    projected_metadata = [
        {"path": entry["path"], "class": entry["class"], "routes": entry["routes"]}
        for entry in registered_paths
    ]
    expected_metadata = [entry for entry in registry_entries if entry["path"] not in excluded_paths]
    if projected_metadata != expected_metadata:
        raise MeasurementError("registered path metadata does not match snapshot registry")
    expected_ratchet = compute_ratchet(
        [entry for entry in registered_paths if entry["class"] in BOOTSTRAP_CLASSES],
        registry["bootstrap_ratchet"],
    )
    if bootstrap_router != expected_ratchet:
        raise MeasurementError("bootstrap_router does not match registered entries and reference")
    payload_digest = require_digest(
        committed.get(SNAPSHOT_PAYLOAD_DIGEST_KEY), SNAPSHOT_PAYLOAD_DIGEST_KEY
    )
    expected_payload_digest = compute_snapshot_payload_digest(committed)
    if payload_digest != expected_payload_digest:
        raise MeasurementError(
            f"snapshot_payload_digest mismatch: manifest claims {payload_digest!r} "
            f"but canonical payload computes to {expected_payload_digest!r}"
        )


def validate_snapshot_integrity(manifest_path: Path) -> dict[str, object]:
    """Validate canonical snapshot evidence without consulting live source."""
    committed = load_canonical_manifest(manifest_path)
    schema, registry_digest = validate_snapshot_envelope(committed)
    registered_paths, paths = validate_registered_content(committed)
    bootstrap_router = validate_bootstrap_router(committed)
    if schema != MANIFEST_SCHEMA_VERSION:
        return committed
    validate_current_snapshot_integrity(
        committed, registry_digest, registered_paths, paths, bootstrap_router
    )
    return committed
