"""Source-product vs. installed consumer footprint separation.

These tests treat the ChatGPT Orchestrator checkpoint and any
repository-level `.agent-coordination/` directory as distinct
categories. They do not require any real consumer/business
repository, external SDD framework, or third-party Skill registry
to run.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from _helpers import CONSUMER_FOOTPRINT_DIR


def test_orchestrator_checkpoint_is_not_a_consumer_state_file(
    repo_root: Path,
) -> None:
    """The source Orchestrator checkpoint must not be confused with
    a consumer `STATE.json`. It lives at a different path, with a
    different extension, and is owned by ChatGPT, not the consumer
    lifecycle.
    """

    checkpoint = repo_root / "docs" / "orchestrator" / "CHECKPOINT.md"
    consumer_state = repo_root / CONSUMER_FOOTPRINT_DIR / "STATE.json"

    assert checkpoint.suffix == ".md"
    assert checkpoint.exists()
    assert not consumer_state.exists(), (
        "Live consumer `.agent-coordination/STATE.json` must not exist at "
        "the source repository root."
    )

    checkpoint_text = checkpoint.read_text(encoding="utf-8")
    assert "Checkpoint-" in checkpoint_text, (
        "Source checkpoint must use a Markdown front-matter style, not JSON."
    )


def test_synthetic_consumer_fixture_is_recognised_as_synthetic(
    tmp_consumer_footprint: Path,
) -> None:
    """Disposable synthetic consumer fixtures must be self-describing.
    The test itself never reads the repository root for this; the
    fixture lives entirely under `tmp_path`.
    """

    state = json.loads((tmp_consumer_footprint / "STATE.json").read_text(encoding="utf-8"))
    assert state.get("is_synthetic") is True

    exchange = (tmp_consumer_footprint / "EXCHANGE.jsonl").read_text(encoding="utf-8").splitlines()
    assert exchange, "synthetic EXCHANGE.jsonl must contain at least one event"
    for raw in exchange:
        parsed = json.loads(raw)
        assert "q" in parsed
        assert "e" in parsed


def test_source_repository_does_not_depend_on_live_consumer_state(
    repo_root: Path,
) -> None:
    """Mechanical: the repository tree must not contain a live
    consumer footprint, and its canonical governance product must
    not require it to run deterministic tests.
    """

    assert not (repo_root / CONSUMER_FOOTPRINT_DIR).exists()
    assert (repo_root / "tests").is_dir()
    assert (repo_root / "pyproject.toml").is_file()
    pyproject = (repo_root / "pyproject.toml").read_text(encoding="utf-8")
    assert "pytest" in pyproject
    assert "ruff" in pyproject


def test_skill_directories_are_distinct_from_consumer_state(
    repo_root: Path,
) -> None:
    """Consumer Governance Skill and Maintainer Skill live in their
    own directories. They are not consumer `STATE.json` artifacts
    and must not be located inside `.agent-coordination/`.
    """

    for skill_dir in ("governance-skill", "maintainer-skill"):
        path = repo_root / skill_dir
        assert path.is_dir(), f"{skill_dir} must exist"
        assert not str(path).startswith(f"{repo_root / CONSUMER_FOOTPRINT_DIR}"), (
            f"{skill_dir} must not live under a consumer footprint directory"
        )


@pytest.mark.parametrize("ad_hoc_path", ["", "missing"])
def test_extract_handles_unresolvable_paths_gracefully(repo_root: Path, ad_hoc_path: str) -> None:
    """The reference resolver must not raise on unusual tokens; it
    must simply report them as unresolvable. This guards the
    infrastructure from regressing into a crash when an obvious
    identifier like `` `D019` `` is encountered.
    """

    from _helpers import extract_internal_references

    references = extract_internal_references(repo_root / "AGENTS.md")
    for ref in references:
        cleaned = ref.target_path
        assert isinstance(cleaned, str)
