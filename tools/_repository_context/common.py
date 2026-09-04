"""Shared repository-context primitives."""

from __future__ import annotations

import json


class MeasurementError(Exception):
    """Raised when a repository cannot be measured deterministically."""


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
