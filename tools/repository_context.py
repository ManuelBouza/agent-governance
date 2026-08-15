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
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
import subprocess
import tempfile
from pathlib import Path, PurePosixPath

SCHEMA_VERSION = "1.0.0"
DEFAULT_BASELINE = "baselines/repository-context-source-v1.json"
BOOTSTRAP_PATHS = ("AGENTS.md", "docs/orchestrator/CHECKPOINT.md")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
MARKDOWN_CODE_PATH = re.compile(r"`([^`\n]+)`")
MARKDOWN_HEADING = re.compile(r"^#{1,6}(?:[ \t]+|$)", re.MULTILINE)
URI_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")

TRACKED_CONTENT_DIGEST_KEY = "tracked_content_digest"
VOLATILE_EXECUTION_METADATA_KEY = "volatile_execution_metadata"

DEFAULT_CONTEXT_MAP = "docs/CONTEXT-MAP.md"
DEFAULT_MANIFEST = "baselines/repository-context-manifest-v1.json"
MANIFEST_SCHEMA_VERSION = "1.0.0"
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


class MeasurementError(Exception):
    """Raised when a repository cannot be measured deterministically."""


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _git(root: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=False,
        capture_output=True,
        timeout=30,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise MeasurementError(f"git {' '.join(arguments)} failed: {detail}")
    return result.stdout


def _tracked_paths(root: Path, excluded: set[str]) -> list[str]:
    raw = _git(root, "ls-files", "--cached", "-z")
    paths = [os.fsdecode(path) for path in raw.split(b"\0") if path]
    return sorted(path for path in paths if PurePosixPath(path).as_posix() not in excluded)


def _read_tracked_file(root: Path, relative: str) -> bytes:
    path = root / relative
    if path.is_symlink():
        return os.fsencode(os.readlink(path))
    try:
        return path.read_bytes()
    except OSError as error:
        raise MeasurementError(f"cannot read tracked file {relative}: {error}") from error


def _category(path: str, is_text: bool) -> str:
    if not is_text:
        return "binary"
    suffix = PurePosixPath(path).suffix.lower()
    categories = {
        ".json": "json",
        ".jsonl": "jsonl",
        ".md": "markdown",
        ".py": "python",
        ".sh": "shell",
        ".toml": "toml",
        ".yaml": "yaml",
        ".yml": "yaml",
    }
    return categories.get(suffix, "text")


def _line_count(text: str) -> int:
    return len(text.splitlines())


def _local_markdown_target(source: str, raw_target: str, tracked: set[str]) -> str | None:
    target = raw_target.strip("<>").split("#", 1)[0]
    if not target or target.startswith(("#", "//")) or URI_SCHEME.match(target):
        return None
    if target in tracked:
        return target
    if target.startswith("/"):
        candidate = posixpath.normpath(target.lstrip("/"))
    else:
        candidate = posixpath.normpath(posixpath.join(posixpath.dirname(source), target))
    if candidate.startswith("../") or candidate == ".." or candidate not in tracked:
        return None
    return candidate


def _file_record(path: str, data: bytes) -> tuple[dict[str, object], str | None]:
    is_text = b"\0" not in data
    text = None
    if is_text:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            is_text = False
    suffix = PurePosixPath(path).suffix.lower() or None
    record: dict[str, object] = {
        "byte_size": len(data),
        "category": _category(path, is_text),
        "character_count": len(text) if text is not None else None,
        "extension": suffix,
        "line_count": _line_count(text) if text is not None else None,
        "markdown_heading_count": (
            len(MARKDOWN_HEADING.findall(text)) if text is not None and suffix == ".md" else None
        ),
        "path": path,
        "sha256": hashlib.sha256(data).hexdigest(),
        "text_encoding": "utf-8" if text is not None else None,
    }
    return record, text


def _metric_totals(records: list[dict[str, object]]) -> dict[str, object]:
    return {
        "byte_size": sum(int(record["byte_size"]) for record in records),
        "character_count": sum(int(record["character_count"] or 0) for record in records),
        "file_count": len(records),
        "line_count": sum(int(record["line_count"] or 0) for record in records),
        "markdown_heading_count": sum(
            int(record["markdown_heading_count"] or 0) for record in records
        ),
        "text_file_count": sum(record["text_encoding"] == "utf-8" for record in records),
    }


def build_report(
    root: Path,
    *,
    excluded_paths: set[str] | None = None,
    source_git_revision: str | None = None,
) -> dict[str, object]:
    """Build canonical measurement data from files selected by the Git index.

    See the module docstring for the provenance/finalization contract.

    ``source_git_revision`` overrides the implicit ``git rev-parse HEAD``
    derivation; when ``None``, the current HEAD is recorded as volatile
    execution metadata.
    """
    root = root.resolve()
    excluded = {PurePosixPath(DEFAULT_BASELINE).as_posix()}
    excluded.update(PurePosixPath(path).as_posix() for path in (excluded_paths or set()))
    paths = _tracked_paths(root, excluded)
    tracked = set(paths)
    records: list[dict[str, object]] = []
    markdown_text: dict[str, str] = {}
    for path in paths:
        record, text = _file_record(path, _read_tracked_file(root, path))
        records.append(record)
        if text is not None and record["extension"] == ".md":
            markdown_text[path] = text

    edge_counts: dict[tuple[str, str], int] = {}
    reference_counts = {path: 0 for path in markdown_text}
    for source, text in markdown_text.items():
        raw_targets = [match.group(1) for match in MARKDOWN_LINK.finditer(text)]
        raw_targets.extend(match.group(1) for match in MARKDOWN_CODE_PATH.finditer(text))
        for raw_target in raw_targets:
            target = _local_markdown_target(source, raw_target, tracked)
            if target is None:
                continue
            edge = (source, target)
            edge_counts[edge] = edge_counts.get(edge, 0) + 1
            reference_counts[source] += 1
    for record in records:
        record["structural_markdown_reference_count"] = reference_counts.get(str(record["path"]))

    by_category: dict[str, dict[str, object]] = {}
    for category in sorted({str(record["category"]) for record in records}):
        by_category[category] = _metric_totals(
            [record for record in records if record["category"] == category]
        )

    bootstrap = [record for record in records if record["path"] in BOOTSTRAP_PATHS]
    missing_bootstrap = sorted(set(BOOTSTRAP_PATHS) - {str(item["path"]) for item in bootstrap})
    if missing_bootstrap:
        raise MeasurementError(f"missing tracked bootstrap files: {', '.join(missing_bootstrap)}")

    text_records = [record for record in records if record["text_encoding"] == "utf-8"]
    largest = sorted(text_records, key=lambda item: (-int(item["byte_size"]), str(item["path"])))
    content_identity = [{"path": record["path"], "sha256": record["sha256"]} for record in records]
    if source_git_revision is None:
        source_git_revision = _git(root, "rev-parse", "HEAD").decode("ascii").strip()
    return {
        "bootstrap_physical_footprint": {
            "description": "Physical UTF-8 footprint of source cold-start router files; no token or observed-load claim.",
            "files": bootstrap,
            "totals": _metric_totals(bootstrap),
        },
        "excluded_paths": sorted(excluded),
        "files": records,
        "largest_context_relevant_files": {
            "description": "Largest UTF-8 text files by physical byte size; not runtime context fan-out.",
            "limit": 20,
            "files": [
                {
                    "byte_size": record["byte_size"],
                    "category": record["category"],
                    "path": record["path"],
                }
                for record in largest[:20]
            ],
        },
        "measurement_scope": {
            "canonical_size_metric": "raw file bytes; UTF-8 character metrics only for decodable text",
            "inventory": "paths returned by git ls-files --cached, measured from worktree bytes",
            "observed_runtime_context_metrics": False,
        },
        "report_schema_version": SCHEMA_VERSION,
        "structural_markdown_references": {
            "description": "Static resolvable local Markdown links and code-span paths to tracked files; not observed RFO, TMC, CAR, or runtime loads.",
            "edge_count": len(edge_counts),
            "edges": [
                {"occurrences": count, "source": source, "target": target}
                for (source, target), count in sorted(edge_counts.items())
            ],
            "reference_count": sum(edge_counts.values()),
        },
        "totals": {"by_category": by_category, "repository": _metric_totals(records)},
        TRACKED_CONTENT_DIGEST_KEY: hashlib.sha256(canonical_json(content_identity)).hexdigest(),
        VOLATILE_EXECUTION_METADATA_KEY: {
            "description": (
                "Per-execution provenance; NOT part of canonical baseline identity "
                "and MAY legitimately differ across runs even when canonical "
                "baseline identity is identical."
            ),
            "source_git_revision": source_git_revision,
        },
    }


def canonical_payload(report: dict[str, object]) -> dict[str, object]:
    """Return the canonical baseline portion of a report.

    The canonical payload comprises every top-level key except
    :data:`VOLATILE_EXECUTION_METADATA_KEY`. Two reports with equal canonical
    payloads have identical canonical baseline identity and are stable across
    the commit/finalization boundary that persists the baseline/handoff file.
    """
    return {key: value for key, value in report.items() if key != VOLATILE_EXECUTION_METADATA_KEY}


def canonical_identity_digest(report: dict[str, object]) -> str:
    """Return the SHA-256 of :func:`canonical_payload`."""
    return hashlib.sha256(canonical_json(canonical_payload(report))).hexdigest()


def validate_canonical_identity(*reports: dict[str, object]) -> None:
    """Assert that every supplied report shares the same canonical identity.

    Volatile execution metadata is explicitly excluded from the comparison.
    Raises :class:`MeasurementError` if at least one report differs in
    canonical payload or if no reports are supplied.
    """
    if not reports:
        raise MeasurementError("validate_canonical_identity requires at least one report")
    reference = canonical_identity_digest(reports[0])
    for index, report in enumerate(reports[1:], start=1):
        current = canonical_identity_digest(report)
        if current != reference:
            raise MeasurementError(
                f"canonical identity mismatch at report index {index}: {reference} != {current}"
            )


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


def build_manifest(
    root: Path,
    *,
    map_path: Path | None = None,
    excluded_paths: set[str] | None = None,
) -> dict[str, object]:
    """Build the canonical RCAB v1 manifest projection from the registry.

    The manifest is a reproducible, non-authoritative projection of the
    registry embedded in ``docs/CONTEXT-MAP.md`` and the current tracked
    content of each registered path. It does not embed a Git commit SHA
    and its own path does not participate in the computed content identity.
    """
    root = root.resolve()
    map_path = root / DEFAULT_CONTEXT_MAP if map_path is None else Path(map_path).resolve()
    registry = parse_registry(map_path)
    validate_registry(registry, root)

    excluded = set(excluded_paths or set())
    registry_digest = compute_registry_digest(registry)
    entries = registry["entries"]

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
        "projection_schema_version": MANIFEST_SCHEMA_VERSION,
        "registry_digest": registry_digest,
        "registered_paths": registered_entries,
        "registered_content_digest": registered_content_digest,
        "bootstrap_router": ratchet,
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
    """Check a committed manifest against deterministic regeneration.

    Returns ``(exit_code, message)``. Exit code 0 means the manifest is
    fresh and all integrity checks pass (warning state, if any, is
    non-blocking). Exit code 1 means the manifest is stale, tampered,
    or an integrity failure was detected.
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
        help="check a committed manifest against deterministic regeneration",
    )
    args = parser.parse_args(argv)
    map_path = _resolve_map_path(args.source_root, args.map)

    try:
        if args.check_manifest is not None:
            exit_code, message = check_manifest(
                args.source_root, args.check_manifest, map_path=map_path
            )
            print(message)
            return exit_code

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
    if args.output is None and not args.manifest and args.check_manifest is None:
        print(canonical_json(report).decode("utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
