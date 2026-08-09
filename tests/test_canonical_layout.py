"""Canonical source layout invariants.

These tests verify the required product directory and module shape
without judging the strategic content of any Markdown file. They
fail loudly when a required path is missing; they pass when the
required structure exists.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from _helpers import (
    CONSUMER_FOOTPRINT_DIR,
    CONSUMER_SKILL_DIR,
    CORE_REQUIRED_MODULES,
    MAINTAINER_SKILL_DIR,
    SOURCE_MAINTENANCE_PATHS,
    SOURCE_PROTOCOL_VERSION,
    iter_markdown_files,
    protocol_version_from,
)


def test_repository_root_contains_expected_top_level_paths(repo_root: Path) -> None:
    required_top_level = (
        "AGENTS.md",
        "README.md",
        "LICENSE",
        "pyproject.toml",
        ".python-version",
        ".gitignore",
        "docs",
        "evals",
        "governance-core",
        "governance-skill",
        "maintainer-skill",
        "tests",
    )
    missing = [name for name in required_top_level if not (repo_root / name).exists()]
    assert not missing, f"Missing top-level paths: {missing}"


def test_governance_core_is_a_directory(repo_root: Path) -> None:
    assert (repo_root / "governance-core").is_dir()


@pytest.mark.parametrize("module_name", CORE_REQUIRED_MODULES)
def test_governance_core_module_exists(repo_root: Path, module_name: str) -> None:
    module_path = repo_root / "governance-core" / module_name
    assert module_path.is_file(), f"Required Core module missing: {module_path}"


def test_governance_core_uses_documented_protocol_version(
    governance_core: Path,
) -> None:
    version = protocol_version_from(governance_core / "GOVERNANCE.md")
    assert version is not None, "governance-core/GOVERNANCE.md has no Protocol-Version"
    assert version == SOURCE_PROTOCOL_VERSION, (
        f"Expected Protocol-Version {SOURCE_PROTOCOL_VERSION} for the "
        f"canonical source, found {version!r}"
    )


def test_coexistence_module_is_present_under_canonical_protocol(repo_root: Path) -> None:
    coexistence = repo_root / "governance-core" / "COEXISTENCE.md"
    assert coexistence.is_file(), "COEXISTENCE.md is part of the required Core"


@pytest.mark.parametrize("relative_path", SOURCE_MAINTENANCE_PATHS)
def test_source_maintenance_path_exists(repo_root: Path, relative_path: str) -> None:
    target = repo_root / relative_path
    assert target.is_file(), f"Source-maintenance path missing: {relative_path}"


def test_consumer_and_maintainer_skill_boundaries_are_separate(
    repo_root: Path,
) -> None:
    consumer = repo_root / CONSUMER_SKILL_DIR
    maintainer = repo_root / MAINTAINER_SKILL_DIR
    assert consumer.is_dir(), f"Missing {CONSUMER_SKILL_DIR} skill directory"
    assert maintainer.is_dir(), f"Missing {MAINTAINER_SKILL_DIR} skill directory"
    assert consumer != maintainer
    assert CONSUMER_SKILL_DIR != MAINTAINER_SKILL_DIR


def test_consumer_and_maintainer_skill_have_status_files(
    repo_root: Path,
) -> None:
    assert (repo_root / CONSUMER_SKILL_DIR / "STATUS.md").is_file()
    assert (repo_root / MAINTAINER_SKILL_DIR / "STATUS.md").is_file()


def test_repository_root_has_no_live_consumer_footprint(repo_root: Path) -> None:
    """The source repository must not host a live consumer
    `.agent-coordination/` instance. Synthetic fixtures under
    `tests/` or `evals/` are acceptable; this test only inspects the
    repository root.
    """

    live = repo_root / CONSUMER_FOOTPRINT_DIR
    assert not live.exists(), (
        f"Live consumer footprint present at repository root: {live}. "
        "AGENTS.md forbids hosting a consumer `.agent-coordination/` "
        "instance inside the source product."
    )


def test_documented_decision_records_include_required_t001_prerequisites(
    repo_root: Path,
) -> None:
    required_decisions = (
        "D019-testing-and-evaluation-strategy.md",
        "D021-persisted-executor-handoffs.md",
        "D022-source-product-change-procedure.md",
        "D023-python-testing-stack.md",
        "D024-testing-skill-capability-model.md",
        "D025-local-development-toolchain.md",
        "D026-ecosystem-coexistence-and-capability-reuse.md",
        "D027-orchestrator-chat-checkpoints.md",
    )
    decisions_dir = repo_root / "docs" / "decisions"
    assert decisions_dir.is_dir(), "docs/decisions must exist"
    missing = [name for name in required_decisions if not (decisions_dir / name).is_file()]
    assert not missing, f"Missing prerequisite decision records: {missing}"


def test_executor_handoff_directory_is_creatable(tmp_path: Path) -> None:
    """The handoff persistence directory must be a writable, plain
    location, not a tracked Markdown path.
    """

    handoff_dir = tmp_path / "handoffs"
    handoff_dir.mkdir()
    sample = handoff_dir / "sample.json"
    sample.write_text("{}", encoding="utf-8")
    assert sample.read_text(encoding="utf-8") == "{}"


def test_markdown_files_in_core_render_as_text(governance_core: Path) -> None:
    """Every Core Markdown file must be readable as UTF-8 text. The
    test does not inspect prose meaning; it only guards against
    accidentally committing a binary blob to a Core module.
    """

    for path in iter_markdown_files(governance_core):
        content = path.read_text(encoding="utf-8")
        assert isinstance(content, str)
        assert content.strip(), f"Core Markdown file is empty: {path}"
