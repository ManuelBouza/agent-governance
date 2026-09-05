"""Current registered-content measurement, projection, and ratchet."""

from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath

from .common import canonical_json
from .measurement import line_count
from .registry import (
    BOOTSTRAP_CLASSES,
    DEFAULT_CONTEXT_MAP,
    canonical_registry,
    compute_registry_digest,
    parse_registry,
    validate_registry,
)
from .tracked_files import read_tracked_file


def measure_registered_path(root: Path, path: str) -> dict[str, object]:
    data = read_tracked_file(root, path)
    try:
        measured_line_count: int | None = line_count(data.decode("utf-8"))
    except UnicodeDecodeError:
        measured_line_count = None
    return {
        "byte_size": len(data),
        "line_count": measured_line_count,
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def compute_ratchet(
    bootstrap_entries: list[dict[str, object]], reference: dict[str, object]
) -> dict[str, object]:
    current_file_count = len(bootstrap_entries)
    current_byte_size = sum(int(entry["byte_size"]) for entry in bootstrap_entries)
    current_line_count = sum(int(entry["line_count"] or 0) for entry in bootstrap_entries)
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
        "files": sorted(str(entry["path"]) for entry in bootstrap_entries),
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
        "warning": {"active": len(warning_reasons) > 0, "reasons": warning_reasons},
        "ratchet_candidate": ratchet_candidate,
    }


def compute_rcab_projection(
    root: Path,
    *,
    map_path: Path | None = None,
    excluded_paths: set[str] | None = None,
) -> dict[str, object]:
    root = root.resolve()
    map_path = root / DEFAULT_CONTEXT_MAP if map_path is None else Path(map_path).resolve()
    registry = parse_registry(map_path)
    validate_registry(registry, root)
    excluded = set(excluded_paths or set())
    normalized_registry = canonical_registry(registry)
    registry_digest = compute_registry_digest(normalized_registry)
    entries = registry["entries"]
    registry_paths = {PurePosixPath(entry["path"]).as_posix() for entry in entries}
    registered_entries: list[dict[str, object]] = []
    for entry in sorted(entries, key=lambda item: item["path"]):
        posix_path = PurePosixPath(entry["path"]).as_posix()
        if posix_path in excluded:
            continue
        measured = measure_registered_path(root, posix_path)
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
    bootstrap_entries = [e for e in registered_entries if e["class"] in BOOTSTRAP_CLASSES]
    return {
        "registry": normalized_registry,
        "excluded_paths": sorted(excluded & registry_paths),
        "registry_digest": registry_digest,
        "registered_paths": registered_entries,
        "registered_content_digest": hashlib.sha256(canonical_json(content_identity)).hexdigest(),
        "bootstrap_router": compute_ratchet(bootstrap_entries, registry["bootstrap_ratchet"]),
    }
