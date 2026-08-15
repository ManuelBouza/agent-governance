#!/usr/bin/env python3
"""Compatibility launcher for the shared deterministic Governance engine."""

from __future__ import annotations

import sys
from pathlib import Path


def _source_root() -> Path:
    candidates = (Path(__file__).resolve().parents[2], Path.cwd().resolve())
    for root in candidates:
        source = root / "src"
        if (source / "agent_governance" / "engine.py").is_file():
            return source
    raise RuntimeError("shared Agent Governance engine is unavailable from source layout")


sys.path.insert(0, str(_source_root()))

from agent_governance import engine as _engine  # noqa: E402

GovernanceError = _engine.GovernanceError
shutil = _engine.shutil
_validate = _engine._validate


def _package_paths() -> tuple[Path, Path]:
    skill = Path(__file__).resolve().parents[1]
    return skill.parent / "governance-core", skill / "assets"


def _bootstrap(target: Path) -> None:
    _engine._bootstrap(target, _package_paths(), validate=_validate)


def main(argv: list[str] | None = None) -> int:
    return _engine.main(argv, package_paths=_package_paths())


if __name__ == "__main__":
    raise SystemExit(main())
