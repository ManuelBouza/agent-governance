"""Conformance checks for repository-backed Skill loading fallback."""

from __future__ import annotations

from pathlib import Path

CANONICAL_SKILL_PATHS = (
    "maintainer-skill/SKILL.md",
    "repository-change-control-skill/SKILL.md",
    "upstream-version-revalidation-skill/SKILL.md",
    "research-evidence-traceability-skill/SKILL.md",
    "durable-work-checkpoint-skill/SKILL.md",
    "executor-launch-handoff-skill/SKILL.md",
)


def test_agents_declares_git_backed_skill_loading_fallback(repo_root: Path) -> None:
    agents = (repo_root / "AGENTS.md").read_text(encoding="utf-8")

    assert "Git-backed fallback" in agents
    assert "same represented Git revision" in agents
    assert "do not claim native host activation" in agents
    assert "maintainer-skill/references/git-backed-skill-loading.md" in agents


def test_maintainer_skill_routes_to_git_backed_loading_reference(repo_root: Path) -> None:
    skill = (repo_root / "maintainer-skill" / "SKILL.md").read_text(encoding="utf-8")

    assert "references/git-backed-skill-loading.md" in skill
    assert "same represented Git revision" in skill
    assert "never describe fallback loading as native host activation" in skill


def test_git_backed_loading_reference_names_all_canonical_skill_sources(
    repo_root: Path,
) -> None:
    reference = (
        repo_root / "maintainer-skill" / "references" / "git-backed-skill-loading.md"
    ).read_text(encoding="utf-8")

    for relative_path in CANONICAL_SKILL_PATHS:
        assert relative_path in reference
        assert (repo_root / relative_path).is_file(), relative_path

    assert "workspace-isolation" in reference
    assert "never promote it to an independent top-level Skill" in reference


def test_git_backed_loading_preserves_git_authority_and_host_neutrality(
    repo_root: Path,
) -> None:
    reference = (
        repo_root / "maintainer-skill" / "references" / "git-backed-skill-loading.md"
    ).read_text(encoding="utf-8")

    assert "Git remains canonical" in reference
    assert "host-specific Skill fork" in reference
    assert "does not" in reference
    assert "ChatGPT/Codex empirical parity" in reference
