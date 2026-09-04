"""Measure deterministic physical context properties of a tracked Git tree.

Provenance/finalization contract
--------------------------------

The canonical baseline produced by :func:`build_report` separates
**deterministic canonical payload** from **volatile execution metadata**:

* The canonical payload comprises every top-level key of the report except
  :data:`VOLATILE_EXECUTION_METADATA_KEY`. It is fully deterministic given an
  unchanged tracked Git tree and remains stable across the
  commit/finalization boundary that persists the baseline/handoff file
  itself. :data:`TRACKED_CONTENT_DIGEST_KEY` is the deterministic content
  identity derived from the measured tracked files only.

* :data:`VOLATILE_EXECUTION_METADATA_KEY` records per-execution provenance
  such as the Git revision observed at measurement time. It is explicitly
  documented as NOT part of canonical baseline identity and MAY legitimately
  differ across runs even when canonical identity is identical.

This separation is what makes AC-CTX-1 satisfiable: the committed canonical
baseline can be regenerated or deterministically validated without byte
drift caused solely by the commit that persists the baseline/handoff, while
the required source Git revision is still preserved as explicitly volatile
execution metadata.

RCAB snapshot/live separation (D049)
------------------------------------

The RCAB manifest separates **committed epoch snapshot evidence** from
**live repository currentness**.

* :func:`build_manifest` generates a deterministic epoch snapshot for the
  registered content measured at generation time. The snapshot is
  non-authoritative evidence. Its machine-visible fields
  (:data:`SNAPSHOT_TYPE`, :data:`SNAPSHOT_SEMANTICS`) make it impossible to
  honestly mistake the committed JSON for live authority.

* :func:`build_live_status` computes current registry integrity, registered
  content measurements and bootstrap/router warning state directly from
  current :data:`DEFAULT_CONTEXT_MAP` plus current tracked registered files.
  It MUST NOT trust the committed snapshot's stored measurements.

* :func:`check_manifest` is a **deliberate explicit currentness comparison**
  of a committed snapshot against current registered content. It MAY report
  stale/tampered when invoked intentionally. If an explicit currentness
  comparison returns failure for stale state, that is not the default
  invariant of the ordinary full deterministic regression suite. The
  ordy regression suite validates snapshot canonical/internal integrity
  via :func:`validate_snapshot_integrity` without requiring a historical
  snapshot to equal mutable live source state.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path, PurePosixPath

# The facade is intentionally loadable both as a directly invoked script and
# through spec_from_file_location from a process whose cwd is unrelated.  A
# source-path-derived package name prevents a long-lived process from reusing
# implementation modules previously loaded from another checkout/worktree.
_PACKAGE_DIRECTORY = Path(__file__).resolve().parent / "_repository_context"
_PACKAGE_FINGERPRINT = hashlib.sha256(str(_PACKAGE_DIRECTORY).encode("utf-8")).hexdigest()
_PACKAGE_NAME = f"_repository_context_{_PACKAGE_FINGERPRINT}"


def _load_source_package() -> tuple[object, object, object]:
    if _PACKAGE_NAME not in sys.modules:
        package_spec = importlib.util.spec_from_file_location(
            _PACKAGE_NAME,
            _PACKAGE_DIRECTORY / "__init__.py",
            submodule_search_locations=[str(_PACKAGE_DIRECTORY)],
        )
        if package_spec is None or package_spec.loader is None:
            raise ImportError(f"cannot load repository-context package from {_PACKAGE_DIRECTORY}")
        package = importlib.util.module_from_spec(package_spec)
        sys.modules[_PACKAGE_NAME] = package
        try:
            package_spec.loader.exec_module(package)
        except BaseException:
            sys.modules.pop(_PACKAGE_NAME, None)
            raise

    return (
        importlib.import_module(f"{_PACKAGE_NAME}.common"),
        importlib.import_module(f"{_PACKAGE_NAME}.measurement"),
        importlib.import_module(f"{_PACKAGE_NAME}.tracked_files"),
    )


_common, _measurement, _tracked_files = _load_source_package()

MeasurementError = _common.MeasurementError
canonical_json = _common.canonical_json

SCHEMA_VERSION = _measurement.SCHEMA_VERSION
DEFAULT_BASELINE = _measurement.DEFAULT_BASELINE
BOOTSTRAP_PATHS = _measurement.BOOTSTRAP_PATHS
MARKDOWN_LINK = _measurement.MARKDOWN_LINK
MARKDOWN_CODE_PATH = _measurement.MARKDOWN_CODE_PATH
MARKDOWN_HEADING = _measurement.MARKDOWN_HEADING
URI_SCHEME = _measurement.URI_SCHEME
TRACKED_CONTENT_DIGEST_KEY = _measurement.TRACKED_CONTENT_DIGEST_KEY
VOLATILE_EXECUTION_METADATA_KEY = _measurement.VOLATILE_EXECUTION_METADATA_KEY
build_report = _measurement.build_report
canonical_payload = _measurement.canonical_payload
canonical_identity_digest = _measurement.canonical_identity_digest
validate_canonical_identity = _measurement.validate_canonical_identity
_category = _measurement.category
_line_count = _measurement.line_count
_local_markdown_target = _measurement.local_markdown_target
_file_record = _measurement.file_record
_metric_totals = _measurement.metric_totals

_git = _tracked_files.git
_tracked_paths = _tracked_files.tracked_paths
_read_tracked_file = _tracked_files.read_tracked_file

DEFAULT_CONTEXT_MAP = "docs/CONTEXT-MAP.md"
DEFAULT_MANIFEST = "baselines/repository-context-manifest-v1.json"
MANIFEST_SCHEMA_VERSION = "1.2.0"
SUPPORTED_MANIFEST_SCHEMA_VERSIONS = frozenset({"1.0.0", "1.1.0", "1.2.0"})
SNAPSHOT_PAYLOAD_DIGEST_KEY = "snapshot_payload_digest"
SNAPSHOT_TYPE = "epoch"
SNAPSHOT_SEMANTICS = "evidence_snapshot_not_live_authority"
LIVE_STATUS_TYPE = "live"
LIVE_STATUS_SEMANTICS = "computed_from_current_source_not_snapshot"
REGISTRY_BEGIN_MARKER = "<!-- RCAB-MAP-V1:BEGIN -->"
REGISTRY_END_MARKER = "<!-- RCAB-MAP-V1:END -->"
BOOTSTRAP_CLASSES = frozenset({"bootstrap", "router"})
VALID_REGISTRY_CLASSES = frozenset(
    {
        "bootstrap",
        "router",
        "focused",
        "task",
        "evidence",
        "generated-index",
        "generated-data",
        "exempt-on-demand",
    }
)
REGISTRY_SCHEMA_VERSION = "1.0.0"


def parse_registry(map_path: Path) -> dict[str, object]:
    """Extract and parse the RCAB-MAP-V1 registry JSON from a context map file.

    Requires exactly one BEGIN/END marker pair and valid JSON inside the
    fenced code block between them.
    """
    text = map_path.read_text(encoding="utf-8")
    begin_offsets = [m.start() for m in re.finditer(re.escape(REGISTRY_BEGIN_MARKER), text)]
    end_offsets = [m.start() for m in re.finditer(re.escape(REGISTRY_END_MARKER), text)]
    if len(begin_offsets) != 1:
        raise MeasurementError(
            f"expected exactly one RCAB-MAP-V1:BEGIN marker, found {len(begin_offsets)}"
        )
    if len(end_offsets) != 1:
        raise MeasurementError(
            f"expected exactly one RCAB-MAP-V1:END marker, found {len(end_offsets)}"
        )
    if end_offsets[0] <= begin_offsets[0]:
        raise MeasurementError("RCAB-MAP-V1:END marker appears before BEGIN marker")
    block = text[begin_offsets[0] + len(REGISTRY_BEGIN_MARKER) : end_offsets[0]]
    fence = re.search(r"```(?:json)?\s*\n(.*?)\n```", block, re.DOTALL)
    json_text = fence.group(1) if fence else block.strip()
    try:
        registry = json.loads(json_text)
    except json.JSONDecodeError as error:
        raise MeasurementError(f"invalid JSON in RCAB-MAP-V1 registry: {error}") from error
    if not isinstance(registry, dict):
        raise MeasurementError("RCAB-MAP-V1 registry must be a JSON object")
    return registry


def compute_registry_digest(registry: dict[str, object]) -> str:
    """Return the SHA-256 of the canonical JSON serialization of the registry."""
    return hashlib.sha256(canonical_json(registry)).hexdigest()


def _canonical_registry(registry: dict[str, object]) -> dict[str, object]:
    return {
        "schema_version": registry["schema_version"],
        "entries": sorted(
            [
                {
                    "path": PurePosixPath(entry["path"]).as_posix(),
                    "class": entry["class"],
                    "routes": sorted(entry["routes"]),
                }
                for entry in registry["entries"]
            ],
            key=lambda entry: entry["path"],
        ),
        "bootstrap_ratchet": {
            field: registry["bootstrap_ratchet"][field]
            for field in (
                "reference",
                "file_count",
                "byte_size",
                "line_count",
                "warning_relative_growth",
                "blocking",
            )
        },
    }


def snapshot_payload(manifest: dict[str, object]) -> dict[str, object]:
    """Return snapshot evidence fields without the self-referential digest."""
    return {key: value for key, value in manifest.items() if key != SNAPSHOT_PAYLOAD_DIGEST_KEY}


def compute_snapshot_payload_digest(manifest: dict[str, object]) -> str:
    """Return the SHA-256 identity of the complete canonical snapshot payload."""
    return hashlib.sha256(canonical_json(snapshot_payload(manifest))).hexdigest()


def validate_registry(registry: dict[str, object], root: Path) -> None:
    """Validate the RCAB-MAP-V1 registry for mechanically decidable integrity.

    Raises :class:`MeasurementError` on malformed data, duplicate paths,
    invalid classifications, or registered targets not tracked by Git.
    """
    schema_version = registry.get("schema_version")
    if schema_version != REGISTRY_SCHEMA_VERSION:
        raise MeasurementError(f"unsupported registry schema_version: {schema_version!r}")
    entries = registry.get("entries")
    if not isinstance(entries, list) or not entries:
        raise MeasurementError("registry must contain a non-empty 'entries' list")
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise MeasurementError(f"registry entry must be an object, got {type(entry).__name__}")
        path = entry.get("path")
        if not isinstance(path, str) or not path:
            raise MeasurementError(f"invalid registered path: {path!r}")
        posix_path = PurePosixPath(path).as_posix()
        if posix_path in seen:
            raise MeasurementError(f"duplicate registered path: {posix_path}")
        seen.add(posix_path)
        cls = entry.get("class")
        if cls not in VALID_REGISTRY_CLASSES:
            raise MeasurementError(f"invalid class {cls!r} for path {posix_path}")
        routes = entry.get("routes")
        if not isinstance(routes, list) or not routes:
            raise MeasurementError(f"invalid routes for path {posix_path}: {routes!r}")
        if not all(isinstance(r, str) and r for r in routes):
            raise MeasurementError(f"invalid route entry for path {posix_path}: {routes!r}")
    ratchet = registry.get("bootstrap_ratchet")
    if not isinstance(ratchet, dict):
        raise MeasurementError("registry must contain a 'bootstrap_ratchet' object")
    for field in (
        "reference",
        "file_count",
        "byte_size",
        "line_count",
        "warning_relative_growth",
        "blocking",
    ):
        if field not in ratchet:
            raise MeasurementError(f"bootstrap_ratchet missing required field: {field}")
    if not isinstance(ratchet["file_count"], int) or ratchet["file_count"] < 0:
        raise MeasurementError(f"invalid bootstrap_ratchet.file_count: {ratchet['file_count']!r}")
    if not isinstance(ratchet["byte_size"], int) or ratchet["byte_size"] < 0:
        raise MeasurementError(f"invalid bootstrap_ratchet.byte_size: {ratchet['byte_size']!r}")
    if not isinstance(ratchet["line_count"], int) or ratchet["line_count"] < 0:
        raise MeasurementError(f"invalid bootstrap_ratchet.line_count: {ratchet['line_count']!r}")
    growth = ratchet["warning_relative_growth"]
    if not isinstance(growth, (int, float)) or not 0 <= growth <= 1:
        raise MeasurementError(f"invalid bootstrap_ratchet.warning_relative_growth: {growth!r}")
    if not isinstance(ratchet["blocking"], bool):
        raise MeasurementError(f"invalid bootstrap_ratchet.blocking: {ratchet['blocking']!r}")
    tracked = set(_tracked_paths(root, set()))
    for entry in entries:
        posix_path = PurePosixPath(entry["path"]).as_posix()
        if posix_path not in tracked:
            raise MeasurementError(f"registered path not tracked by Git: {posix_path}")


def _measure_registered_path(root: Path, path: str) -> dict[str, object]:
    data = _read_tracked_file(root, path)
    line_count: int | None
    try:
        text = data.decode("utf-8")
        line_count = _line_count(text)
    except UnicodeDecodeError:
        line_count = None
    return {
        "byte_size": len(data),
        "line_count": line_count,
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def _compute_ratchet(
    bootstrap_entries: list[dict[str, object]],
    reference: dict[str, object],
) -> dict[str, object]:
    current_file_count = len(bootstrap_entries)
    current_byte_size = sum(int(e["byte_size"]) for e in bootstrap_entries)
    current_line_count = sum(int(e["line_count"] or 0) for e in bootstrap_entries)

    ref_file_count = int(reference["file_count"])
    ref_byte_size = int(reference["byte_size"])
    ref_line_count = int(reference["line_count"])
    growth_threshold = reference["warning_relative_growth"]

    byte_ratio: float | None = current_byte_size / ref_byte_size if ref_byte_size > 0 else None

    warning_reasons: list[dict[str, object]] = []
    if current_file_count > ref_file_count:
        warning_reasons.append(
            {
                "reason": "file_count_exceeds_reference",
                "current": current_file_count,
                "reference": ref_file_count,
            }
        )
    if ref_byte_size > 0 and current_byte_size > ref_byte_size * (1 + growth_threshold):
        warning_reasons.append(
            {
                "reason": "byte_size_exceeds_warning_threshold",
                "current": current_byte_size,
                "reference": ref_byte_size,
                "threshold": ref_byte_size * (1 + growth_threshold),
            }
        )

    ratchet_candidate: dict[str, object] | None = None
    if current_byte_size < ref_byte_size or current_file_count < ref_file_count:
        ratchet_candidate = {
            "file_count": current_file_count,
            "byte_size": current_byte_size,
            "line_count": current_line_count,
        }

    return {
        "files": sorted(
            [str(e["path"]) for e in bootstrap_entries],
        ),
        "current": {
            "file_count": current_file_count,
            "byte_size": current_byte_size,
            "line_count": current_line_count,
        },
        "accepted_reference": {
            "reference": reference["reference"],
            "file_count": ref_file_count,
            "byte_size": ref_byte_size,
            "line_count": ref_line_count,
            "warning_relative_growth": growth_threshold,
            "blocking": reference["blocking"],
        },
        "delta": {
            "file_count_delta": current_file_count - ref_file_count,
            "byte_size_delta": current_byte_size - ref_byte_size,
            "line_count_delta": current_line_count - ref_line_count,
            "byte_size_ratio": byte_ratio,
        },
        "warning": {
            "active": len(warning_reasons) > 0,
            "reasons": warning_reasons,
        },
        "ratchet_candidate": ratchet_candidate,
    }


def _compute_rcab_projection(
    root: Path,
    *,
    map_path: Path | None = None,
    excluded_paths: set[str] | None = None,
) -> dict[str, object]:
    """Compute the shared RCAB projection from current registry and registered files.

    This is the common computation used by both :func:`build_manifest` (epoch
    snapshot) and :func:`build_live_status` (live state). It parses the
    current registry from the context map, validates it, measures each
    registered path, and computes the bootstrap/router ratchet.

    The computation never reads a committed manifest. It derives everything
    from current source authority.
    """
    root = root.resolve()
    map_path = root / DEFAULT_CONTEXT_MAP if map_path is None else Path(map_path).resolve()
    registry = parse_registry(map_path)
    validate_registry(registry, root)

    excluded = set(excluded_paths or set())
    canonical_registry = _canonical_registry(registry)
    registry_digest = compute_registry_digest(canonical_registry)
    entries = registry["entries"]
    registry_paths = {PurePosixPath(entry["path"]).as_posix() for entry in entries}
    projected_exclusions = sorted(excluded & registry_paths)

    registered_entries: list[dict[str, object]] = []
    for entry in sorted(entries, key=lambda e: e["path"]):
        posix_path = PurePosixPath(entry["path"]).as_posix()
        if posix_path in excluded:
            continue
        measured = _measure_registered_path(root, posix_path)
        registered_entries.append(
            {
                "path": posix_path,
                "class": entry["class"],
                "routes": sorted(entry["routes"]),
                "byte_size": measured["byte_size"],
                "line_count": measured["line_count"],
                "sha256": measured["sha256"],
            }
        )

    content_identity = [{"path": e["path"], "sha256": e["sha256"]} for e in registered_entries]
    registered_content_digest = hashlib.sha256(canonical_json(content_identity)).hexdigest()

    bootstrap_entries = [e for e in registered_entries if e["class"] in BOOTSTRAP_CLASSES]
    ratchet = _compute_ratchet(bootstrap_entries, registry["bootstrap_ratchet"])

    return {
        "registry": canonical_registry,
        "excluded_paths": projected_exclusions,
        "registry_digest": registry_digest,
        "registered_paths": registered_entries,
        "registered_content_digest": registered_content_digest,
        "bootstrap_router": ratchet,
    }


def build_manifest(
    root: Path,
    *,
    map_path: Path | None = None,
    excluded_paths: set[str] | None = None,
) -> dict[str, object]:
    """Build the canonical RCAB v1 epoch snapshot manifest from current source.

    The manifest is a reproducible, non-authoritative projection of the
    registry embedded in ``docs/CONTEXT-MAP.md`` and the current tracked
    content of each registered path. It does not embed a Git commit SHA
    and its own path does not participate in the computed content identity.

    The output carries machine-visible epoch snapshot semantics
    (:data:`SNAPSHOT_TYPE`, :data:`SNAPSHOT_SEMANTICS`) so a consumer of
    the JSON cannot honestly mistake it for live authority.
    """
    projection = _compute_rcab_projection(root, map_path=map_path, excluded_paths=excluded_paths)
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
    """Compute live RCAB status directly from current registry and registered files.

    Live status is derived entirely from the current
    ``docs/CONTEXT-MAP.md`` registry and the current tracked content of
    each registered path. It MUST NOT trust the committed snapshot's stored
    measurements.

    The output carries machine-visible live semantics
    (:data:`LIVE_STATUS_TYPE`, :data:`LIVE_STATUS_SEMANTICS`) so a consumer
    can distinguish it from a committed epoch snapshot.
    """
    projection = _compute_rcab_projection(root, map_path=map_path, excluded_paths=excluded_paths)
    return {
        "status_type": LIVE_STATUS_TYPE,
        "status_semantics": LIVE_STATUS_SEMANTICS,
        "registry_digest": projection["registry_digest"],
        "registered_paths": projection["registered_paths"],
        "registered_content_digest": projection["registered_content_digest"],
        "bootstrap_router": projection["bootstrap_router"],
    }


def write_manifest(
    root: Path,
    output: Path,
    *,
    map_path: Path | None = None,
) -> dict[str, object]:
    """Generate the manifest and atomically write it to ``output``."""
    root = root.resolve()
    relative = _relative_output(root, output)
    excluded = {relative} if relative is not None else set()
    manifest = build_manifest(root, map_path=map_path, excluded_paths=excluded)
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(canonical_json(manifest))
    temporary.replace(output)
    return manifest


def check_manifest(
    root: Path,
    manifest_path: Path,
    *,
    map_path: Path | None = None,
) -> tuple[int, str]:
    """Explicitly compare a committed snapshot against current registered content.

    Returns ``(exit_code, message)``. Exit code 0 means the committed
    snapshot matches deterministic regeneration from the current registry
    and registered content (fresh, all integrity checks pass; warning state,
    if any, is non-blocking). Exit code 1 means the committed snapshot is
    stale, tampered, or an integrity failure was detected.

    This is a **deliberate explicit currentness comparison** — not the
    default invariant of the ordinary full deterministic regression suite.
    A historical committed snapshot that predates legitimate registered-file
    evolution will correctly report stale here, but that does not make the
    ordinary regression suite red. Snapshot canonical/internal integrity is
    validated by :func:`validate_snapshot_integrity`.
    """
    root = root.resolve()
    relative = _relative_output(root, manifest_path)
    excluded = {relative} if relative is not None else set()
    current = build_manifest(root, map_path=map_path, excluded_paths=excluded)
    committed = manifest_path.read_bytes()
    regenerated = canonical_json(current)
    if committed != regenerated:
        return 1, (
            "manifest is stale or tampered: committed projection does not match "
            "deterministic regeneration from current registry and registered content"
        )
    warning = current["bootstrap_router"]["warning"]
    if warning["active"]:
        parts = []
        for reason in warning["reasons"]:
            parts.append(
                f"{reason['reason']}"
                f" (current={reason.get('current')}, reference={reason.get('reference')})"
            )
        return 0, "manifest OK (warning: " + "; ".join(parts) + ")"
    return 0, "manifest OK"


def _require_nonnegative_int(value: object, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise MeasurementError(f"invalid {field}: {value!r}")
    return value


def _require_digest(value: object, field: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or value != value.lower():
        raise MeasurementError(f"invalid {field}: {value!r}")
    try:
        int(value, 16)
    except ValueError as error:
        raise MeasurementError(f"{field} is not a lowercase hex string: {value!r}") from error
    return value


def _validate_snapshot_entry(entry: object) -> dict[str, object]:
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
    _require_nonnegative_int(entry["byte_size"], f"byte_size for path {path!r}")
    line_count = entry["line_count"]
    if line_count is not None:
        _require_nonnegative_int(line_count, f"line_count for path {path!r}")
    _require_digest(entry["sha256"], f"sha256 for path {path!r}")
    return entry


def _validate_snapshot_registry(registry: object) -> dict[str, object]:
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
    canonical_entries: list[dict[str, object]] = []
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"path", "class", "routes"}:
            raise MeasurementError(
                "snapshot registry entry must contain exactly path, class, routes"
            )
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
        canonical_entries.append(entry)
    registry_paths = [entry["path"] for entry in canonical_entries]
    if registry_paths != sorted(set(registry_paths)):
        raise MeasurementError(
            "snapshot registry entries must have unique paths in canonical order"
        )

    reference = registry["bootstrap_ratchet"]
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
        _require_nonnegative_int(reference[field], f"bootstrap_ratchet.{field}")
    growth = reference["warning_relative_growth"]
    if isinstance(growth, bool) or not isinstance(growth, (int, float)) or not 0 <= growth <= 1:
        raise MeasurementError(f"invalid bootstrap_ratchet.warning_relative_growth: {growth!r}")
    if not isinstance(reference["blocking"], bool):
        raise MeasurementError(f"invalid bootstrap_ratchet.blocking: {reference['blocking']!r}")
    return registry


def validate_snapshot_integrity(manifest_path: Path) -> dict[str, object]:
    """Validate canonical snapshot evidence without consulting live source."""
    raw = manifest_path.read_bytes()
    try:
        committed = json.loads(raw)
    except json.JSONDecodeError as error:
        raise MeasurementError(f"manifest is not valid JSON: {error}") from error
    if not isinstance(committed, dict):
        raise MeasurementError("manifest must be a JSON object")
    if raw != canonical_json(committed):
        raise MeasurementError("manifest JSON bytes are not canonical")

    schema = committed.get("projection_schema_version")
    if schema not in SUPPORTED_MANIFEST_SCHEMA_VERSIONS:
        raise MeasurementError(
            f"unsupported projection_schema_version: {schema!r}; "
            f"supported: {sorted(SUPPORTED_MANIFEST_SCHEMA_VERSIONS)}"
        )

    if schema != "1.0.0":
        snapshot_type = committed.get("snapshot_type")
        if snapshot_type != SNAPSHOT_TYPE:
            raise MeasurementError(
                f"missing or invalid snapshot_type: {snapshot_type!r}; expected {SNAPSHOT_TYPE!r}"
            )
        snapshot_semantics = committed.get("snapshot_semantics")
        if snapshot_semantics != SNAPSHOT_SEMANTICS:
            raise MeasurementError(
                f"missing or invalid snapshot_semantics: {snapshot_semantics!r}; "
                f"expected {SNAPSHOT_SEMANTICS!r}"
            )

    registry_digest = _require_digest(committed.get("registry_digest"), "registry_digest")

    registered_paths = committed.get("registered_paths")
    if not isinstance(registered_paths, list) or not registered_paths:
        raise MeasurementError("manifest must contain a non-empty 'registered_paths' list")

    paths = [_validate_snapshot_entry(entry)["path"] for entry in registered_paths]

    if paths != sorted(set(paths)):
        raise MeasurementError("registered_paths must have unique paths in canonical order")

    content_identity = [{"path": e["path"], "sha256": e["sha256"]} for e in registered_paths]
    expected_digest = hashlib.sha256(canonical_json(content_identity)).hexdigest()
    actual_digest = _require_digest(
        committed.get("registered_content_digest"), "registered_content_digest"
    )
    if actual_digest != expected_digest:
        raise MeasurementError(
            f"registered_content_digest mismatch: manifest claims {actual_digest!r} "
            f"but registered_paths compute to {expected_digest!r}"
        )

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
    if schema != MANIFEST_SCHEMA_VERSION:
        return committed

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

    registry = _validate_snapshot_registry(committed["registry"])
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

    expected_ratchet = _compute_ratchet(
        [entry for entry in registered_paths if entry["class"] in BOOTSTRAP_CLASSES],
        registry["bootstrap_ratchet"],
    )
    if bootstrap_router != expected_ratchet:
        raise MeasurementError("bootstrap_router does not match registered entries and reference")

    payload_digest = _require_digest(
        committed.get(SNAPSHOT_PAYLOAD_DIGEST_KEY), SNAPSHOT_PAYLOAD_DIGEST_KEY
    )
    expected_payload_digest = compute_snapshot_payload_digest(committed)
    if payload_digest != expected_payload_digest:
        raise MeasurementError(
            f"snapshot_payload_digest mismatch: manifest claims {payload_digest!r} "
            f"but canonical payload computes to {expected_payload_digest!r}"
        )

    return committed


def _resolve_map_path(source_root: Path, map_arg: Path | None) -> Path | None:
    if map_arg is None:
        return None
    if map_arg.is_absolute():
        return map_arg.resolve()
    return (source_root / map_arg).resolve()


def _relative_output(root: Path, output: Path) -> str | None:
    try:
        return output.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def write_report(root: Path, output: Path) -> dict[str, object]:
    excluded = {_relative} if (_relative := _relative_output(root, output)) else set()
    report = build_report(root, excluded_paths=excluded)
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(canonical_json(report))
    temporary.replace(output)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--map", type=Path, help="path to the context map Markdown file")
    parser.add_argument(
        "--manifest",
        action="store_true",
        help="generate the RCAB v1 manifest projection instead of the full report",
    )
    parser.add_argument(
        "--check-manifest",
        type=Path,
        metavar="PATH",
        help="explicit currentness comparison of a committed snapshot against current registered content",
    )
    parser.add_argument(
        "--validate-snapshot",
        type=Path,
        metavar="PATH",
        help="validate internal integrity of a committed snapshot without comparing to current source",
    )
    parser.add_argument(
        "--live-status",
        action="store_true",
        help="compute live RCAB status from current registry and registered files",
    )
    args = parser.parse_args(argv)
    map_path = _resolve_map_path(args.source_root, args.map)

    try:
        if args.validate_snapshot is not None:
            validate_snapshot_integrity(args.validate_snapshot)
            print("snapshot integrity OK")
            return 0

        if args.check_manifest is not None:
            exit_code, message = check_manifest(
                args.source_root, args.check_manifest, map_path=map_path
            )
            print(message)
            return exit_code

        if args.live_status:
            status = build_live_status(args.source_root, map_path=map_path)
            print(canonical_json(status).decode("utf-8"), end="")
            return 0

        if args.manifest:
            if args.output is not None:
                write_manifest(args.source_root, args.output, map_path=map_path)
            else:
                manifest = build_manifest(args.source_root, map_path=map_path)
                print(canonical_json(manifest).decode("utf-8"), end="")
            return 0

        report = (
            write_report(args.source_root, args.output)
            if args.output is not None
            else build_report(args.source_root)
        )
    except (MeasurementError, OSError, UnicodeError) as error:
        parser.exit(1, f"error: {error}\n")
    if (
        args.output is None
        and not args.manifest
        and args.check_manifest is None
        and args.validate_snapshot is None
        and not args.live_status
    ):
        print(canonical_json(report).decode("utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
