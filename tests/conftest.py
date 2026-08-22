"""Pytest configuration for the agent-governance deterministic suite.

Provides a single `repo_root` fixture so each test can reason about
the canonical source repository layout without relying on
``Path.cwd()`` or environment variables.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from _helpers import find_repo_root


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return find_repo_root(Path(__file__).resolve().parent)


@pytest.fixture(scope="session")
def governance_core(repo_root: Path) -> Path:
    return repo_root / "governance-core"


@pytest.fixture
def tmp_consumer_footprint(
    tmp_path: Path,
) -> Iterator[Path]:
    """Yield a synthetic disposable consumer `.agent-coordination/`
    directory. The directory intentionally lives inside a pytest
    temporary path; nothing is created at the repository root.
    """

    footprint = tmp_path / ".agent-coordination"
    footprint.mkdir()
    (footprint / "STATE.json").write_text(
        '{"protocol": "consumer", "is_synthetic": true}\n',
        encoding="utf-8",
        newline="",
    )
    (footprint / "EXCHANGE.jsonl").write_text(
        '{"q": 1, "a": "strategy", "e": "start", "v": "synthetic"}\n',
        encoding="utf-8",
        newline="",
    )
    (footprint / "CAPABILITIES.json").write_text(
        '{"capabilities": [], "is_synthetic": true}\n',
        encoding="utf-8",
        newline="",
    )
    yield footprint
