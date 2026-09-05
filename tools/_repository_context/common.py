"""Shared repository-context primitives."""

from __future__ import annotations

import json
from pathlib import Path


class MeasurementError(Exception):
    """Raised when a repository cannot be measured deterministically."""


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def relative_output(root: Path, output: Path) -> str | None:
    try:
        return output.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None
