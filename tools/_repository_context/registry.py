"""RCAB context-map registry parsing, validation, and canonical identity."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath

from .common import MeasurementError, canonical_json
from .tracked_files import tracked_paths

DEFAULT_CONTEXT_MAP = "docs/CONTEXT-MAP.md"
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
    """Extract and parse the sole RCAB-MAP-V1 registry from a context map."""
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
    return hashlib.sha256(canonical_json(registry)).hexdigest()


def canonical_registry(registry: dict[str, object]) -> dict[str, object]:
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


def validate_registry_entry(entry: object, seen: set[str]) -> str:
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
    if not all(isinstance(route, str) and route for route in routes):
        raise MeasurementError(f"invalid route entry for path {posix_path}: {routes!r}")
    return posix_path


def validate_bootstrap_ratchet(ratchet: object) -> None:
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
    for field in ("file_count", "byte_size", "line_count"):
        if not isinstance(ratchet[field], int) or ratchet[field] < 0:
            raise MeasurementError(f"invalid bootstrap_ratchet.{field}: {ratchet[field]!r}")
    growth = ratchet["warning_relative_growth"]
    if not isinstance(growth, (int, float)) or not 0 <= growth <= 1:
        raise MeasurementError(f"invalid bootstrap_ratchet.warning_relative_growth: {growth!r}")
    if not isinstance(ratchet["blocking"], bool):
        raise MeasurementError(f"invalid bootstrap_ratchet.blocking: {ratchet['blocking']!r}")


def validate_registry(registry: dict[str, object], root: Path) -> None:
    schema_version = registry.get("schema_version")
    if schema_version != REGISTRY_SCHEMA_VERSION:
        raise MeasurementError(f"unsupported registry schema_version: {schema_version!r}")
    entries = registry.get("entries")
    if not isinstance(entries, list) or not entries:
        raise MeasurementError("registry must contain a non-empty 'entries' list")
    seen: set[str] = set()
    paths = [validate_registry_entry(entry, seen) for entry in entries]
    validate_bootstrap_ratchet(registry.get("bootstrap_ratchet"))
    tracked = set(tracked_paths(root, set()))
    for posix_path in paths:
        if posix_path not in tracked:
            raise MeasurementError(f"registered path not tracked by Git: {posix_path}")
