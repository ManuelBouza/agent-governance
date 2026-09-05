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
import sys
from pathlib import Path

_PACKAGE_DIRECTORY = Path(__file__).resolve().parent / "_repository_context"
_PACKAGE_FINGERPRINT = hashlib.sha256(str(_PACKAGE_DIRECTORY).encode("utf-8")).hexdigest()
_PACKAGE_NAME = f"_repository_context_{_PACKAGE_FINGERPRINT}"


def _load_source_package() -> tuple[object, ...]:
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
    return tuple(
        importlib.import_module(f"{_PACKAGE_NAME}.{name}")
        for name in (
            "common",
            "measurement",
            "tracked_files",
            "registry",
            "projection",
            "snapshot",
        )
    )


_common, _measurement, _tracked_files, _registry, _projection, _snapshot = _load_source_package()

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
write_report = _measurement.write_report
_category = _measurement.category
_line_count = _measurement.line_count
_local_markdown_target = _measurement.local_markdown_target
_file_record = _measurement.file_record
_metric_totals = _measurement.metric_totals
_relative_output = _measurement.relative_output
_git = _tracked_files.git
_tracked_paths = _tracked_files.tracked_paths
_read_tracked_file = _tracked_files.read_tracked_file

DEFAULT_CONTEXT_MAP = _registry.DEFAULT_CONTEXT_MAP
REGISTRY_BEGIN_MARKER = _registry.REGISTRY_BEGIN_MARKER
REGISTRY_END_MARKER = _registry.REGISTRY_END_MARKER
BOOTSTRAP_CLASSES = _registry.BOOTSTRAP_CLASSES
VALID_REGISTRY_CLASSES = _registry.VALID_REGISTRY_CLASSES
REGISTRY_SCHEMA_VERSION = _registry.REGISTRY_SCHEMA_VERSION
parse_registry = _registry.parse_registry
compute_registry_digest = _registry.compute_registry_digest
validate_registry = _registry.validate_registry
_canonical_registry = _registry.canonical_registry
_measure_registered_path = _projection.measure_registered_path
_compute_ratchet = _projection.compute_ratchet
_compute_rcab_projection = _projection.compute_rcab_projection

DEFAULT_MANIFEST = _snapshot.DEFAULT_MANIFEST
MANIFEST_SCHEMA_VERSION = _snapshot.MANIFEST_SCHEMA_VERSION
SUPPORTED_MANIFEST_SCHEMA_VERSIONS = _snapshot.SUPPORTED_MANIFEST_SCHEMA_VERSIONS
SNAPSHOT_PAYLOAD_DIGEST_KEY = _snapshot.SNAPSHOT_PAYLOAD_DIGEST_KEY
SNAPSHOT_TYPE = _snapshot.SNAPSHOT_TYPE
SNAPSHOT_SEMANTICS = _snapshot.SNAPSHOT_SEMANTICS
LIVE_STATUS_TYPE = _snapshot.LIVE_STATUS_TYPE
LIVE_STATUS_SEMANTICS = _snapshot.LIVE_STATUS_SEMANTICS
snapshot_payload = _snapshot.snapshot_payload
compute_snapshot_payload_digest = _snapshot.compute_snapshot_payload_digest
build_manifest = _snapshot.build_manifest
build_live_status = _snapshot.build_live_status
write_manifest = _snapshot.write_manifest
check_manifest = _snapshot.check_manifest
validate_snapshot_integrity = _snapshot.validate_snapshot_integrity
_require_nonnegative_int = _snapshot.require_nonnegative_int
_require_digest = _snapshot.require_digest
_validate_snapshot_entry = _snapshot.validate_snapshot_entry
_validate_snapshot_registry = _snapshot.validate_snapshot_registry


def _resolve_map_path(source_root: Path, map_arg: Path | None) -> Path | None:
    if map_arg is None:
        return None
    if map_arg.is_absolute():
        return map_arg.resolve()
    return (source_root / map_arg).resolve()


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
    if args.output is None:
        print(canonical_json(report).decode("utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
