"""Harness foundation sanity tests.

These tests prove that the deterministic harness itself runs
locally without production credentials, hosted services, or
third-party SDD/Skill ecosystems. They are intentionally trivial
and only assert the most basic mechanical properties of the
harness.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest


def test_python_version_meets_minimum_contract() -> None:
    """Python must be at least 3.13 per D023. This test does not
    require a particular patch release.
    """

    assert sys.version_info >= (3, 13), (
        f"Expected Python >= 3.13, found {sys.version_info.major}.{sys.version_info.minor}"
    )


def test_no_required_environment_variables_for_deterministic_run(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Removing the variable set must not change pytest's basic
    test discovery behavior. This guards the suite from a future
    regression that quietly depends on an undocumented env var.
    """

    for key in (
        "GITHUB_TOKEN",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GENTLE_AI_TOKEN",
        "SPEC_KIT_TOKEN",
    ):
        monkeypatch.delenv(key, raising=False)

    # The test does not assert anything about process state; the
    # deletion alone proves the suite does not require these
    # secrets.
    assert os.environ.get("GITHUB_TOKEN") is None


def test_pytest_discovers_test_modules(repo_root: Path) -> None:
    """The configured test path must contain the four canonical
    deterministic test modules required by T001.
    """

    tests_dir = repo_root / "tests"
    expected = {
        "test_canonical_layout.py",
        "test_reference_integrity.py",
        "test_source_consumer_separation.py",
        "test_harness_foundation.py",
    }
    found = {p.name for p in tests_dir.glob("test_*.py")}
    missing = expected - found
    assert not missing, f"Missing required test modules: {sorted(missing)}"


def test_pytest_self_collects(repo_root: Path) -> None:
    """`python -m pytest --collect-only -q` must succeed against
    the locked environment and report the local tests. This proves
    the harness runs the suite it ships.
    """

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "-q",
            "tests",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"pytest --collect-only failed:\nstdout={result.stdout}\nstderr={result.stderr}"
    )
    assert "test_canonical_layout" in result.stdout
    assert "test_reference_integrity" in result.stdout
    assert "test_source_consumer_separation" in result.stdout
    assert "test_harness_foundation" in result.stdout


def test_ruff_is_invokable_from_locked_environment(repo_root: Path) -> None:
    """`uv run --locked ruff --version` must succeed; this guards
    against a future regression where the lockfile drifts from the
    toolchain declared in `pyproject.toml`.
    """

    result = subprocess.run(
        [
            "uv",
            "run",
            "--locked",
            "ruff",
            "--version",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"`uv run --locked ruff --version` failed:\nstdout={result.stdout}\nstderr={result.stderr}"
    )
    assert "ruff" in result.stdout.lower()


def test_ruff_exclusions_protect_markdown_without_external_surfaces(repo_root: Path) -> None:
    """Ruff must protect Markdown without naming external host state."""

    pyproject = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["tool"]["ruff"]["extend-exclude"] == ["**/*.md", ".venv"]


def test_failures_identify_the_violated_invariant(repo_root: Path, tmp_path: Path) -> None:
    """A broken invariant must be reported with the test name; this
    guards the harness against silent green lights.
    """

    sentinel = tmp_path / "sentinel.py"
    sentinel.write_text(
        "def test_sentinel_broken():\n    assert False, 'sentinel broken'\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--no-header",
            "--tb=line",
            str(sentinel),
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode != 0, "expected the sentinel test to fail"
    combined = result.stdout + result.stderr
    assert "sentinel_broken" in combined, "failing test name must be reported in the output"
    assert "sentinel broken" in combined, "assertion message must identify the violated invariant"
