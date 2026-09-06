"""Direct local reference integrity.

These tests extract path-style references from selected Markdown
files and verify that each referenced path resolves to an existing
file in the source repository. They do not interpret the prose
meaning of any sentence; they only check that a quoted/linked path
points to something real.

The tests deliberately ignore identifier-style references (for
example `D019`, `T001`) and external URLs. References that begin
with a documented consumer-side prefix (``.agent-coordination/``)
are recognised as consumer-installation documentation and are
expected to be absent from the source repository root.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import pytest
from _helpers import (
    CONSUMER_FOOTPRINT_ALIAS_DIR,
    CONSUMER_FOOTPRINT_DIR,
    Reference,
    extract_internal_references,
    iter_markdown_files,
    looks_like_path,
)

CONSUMER_SIDE_PREFIXES: tuple[str, ...] = (
    f"{CONSUMER_FOOTPRINT_DIR}/",
    f"./{CONSUMER_FOOTPRINT_DIR}/",
    f"{CONSUMER_FOOTPRINT_ALIAS_DIR}/",
    f"./{CONSUMER_FOOTPRINT_ALIAS_DIR}/",
)


def is_consumer_side_reference(target: str) -> bool:
    """Return True when `target` describes a consumer-installation
    artifact that intentionally does not live inside the source
    repository.
    """

    return any(target.startswith(prefix) for prefix in CONSUMER_SIDE_PREFIXES)


GLOB_TOKENS: tuple[str, ...] = ("*", "**")


def is_glob_or_branch_pattern(target: str) -> bool:
    """Return True when `target` contains a glob character or
    otherwise looks like a branch / naming pattern rather than a
    repository file path.
    """

    return any(token in target for token in GLOB_TOKENS)


EXTENSION_ONLY_PROSE_TOKENS: frozenset[str] = frozenset(
    {".md", ".py", ".toml", ".json", ".lock", ".yaml", ".yml"}
)


def is_directory_or_extension_only(target: str) -> bool:
    """Return True when `target` describes a directory or a file
    extension rather than a concrete file path. These are valid
    prose references that cannot be resolved mechanically to a
    single file.

    Extension-only prose tokens are explicitly allowlisted. Other
    dot-prefixed tokens are concrete path candidates so repository
    dotfiles remain eligible for mechanical resolution.
    """

    if target.endswith("/"):
        return True
    return target in EXTENSION_ONLY_PROSE_TOKENS


def _resolve(reference: Reference, repo_root: Path) -> tuple[Path, bool]:
    target = reference.target_path
    if not looks_like_path(target):
        return Path(target), False
    resolved = (repo_root / target).resolve(strict=False)
    return resolved, resolved.exists()


def is_inside_repository(candidate: Path, repo_root: Path) -> bool:
    """Return whether a canonical candidate remains below repository root."""

    try:
        candidate.resolve(strict=False).relative_to(repo_root.resolve(strict=False))
    except ValueError:
        return False
    return True


def _references_to_paths(
    references: Iterable[Reference], repo_root: Path
) -> list[tuple[Reference, Path, bool]]:
    return [(ref, *_resolve(ref, repo_root)) for ref in references]


@pytest.mark.parametrize(
    "markdown_relative_path",
    [
        "AGENTS.md",
        "governance-core/GOVERNANCE.md",
        "governance-core/PROTOCOL.md",
        "governance-core/COEXISTENCE.md",
        "governance-core/SKILLS.md",
        "governance-core/SKILL-DISCOVERY.md",
        "governance-core/SKILL-SUPPLY-CHAIN.md",
        "governance-core/EXECUTION.md",
        "governance-core/LIFECYCLE.md",
        "governance-core/HANDOFF.md",
        "governance-core/CONTEXT.md",
        "governance-core/ADAPTERS.md",
    ],
)
def test_canonical_markdown_references_resolve(
    repo_root: Path, markdown_relative_path: str
) -> None:
    """Every internal path reference inside canonical Core and
    repository Markdown must resolve to an existing file.
    """

    markdown = repo_root / markdown_relative_path
    references = extract_internal_references(markdown)
    assert references, f"No path references extracted from {markdown_relative_path}"

    failures: list[str] = []
    for ref, resolved, exists in _references_to_paths(references, repo_root):
        if not looks_like_path(ref.target_path):
            continue
        if is_consumer_side_reference(ref.target_path):
            continue
        if is_glob_or_branch_pattern(ref.target_path):
            continue
        if is_directory_or_extension_only(ref.target_path):
            continue
        if not exists:
            failures.append(
                f"{markdown_relative_path}:{ref.line_no} -> {resolved.relative_to(repo_root)}"
            )
    assert not failures, "Unresolved internal references:\n" + "\n".join(failures)


def test_orchestrator_checkpoint_paths_referenced_by_agents_md_resolve(
    repo_root: Path,
) -> None:
    """AGENTS.md must point at the documented source-maintenance
    Orchestrator checkpoint files; this test only verifies that the
    references exist on disk, not whether the prose is strategically
    correct.
    """

    agents_md = repo_root / "AGENTS.md"
    text = agents_md.read_text(encoding="utf-8")

    required_phrases = (
        "docs/ORCHESTRATOR-CHECKPOINTS.md",
        "docs/orchestrator/CHECKPOINT.md",
    )
    for phrase in required_phrases:
        assert phrase in text, f"AGENTS.md does not mention required checkpoint path: {phrase}"
        assert (repo_root / phrase).is_file(), (
            f"Required checkpoint path is referenced but missing: {phrase}"
        )


def test_no_internal_reference_inside_core_points_outside_repo(
    governance_core: Path, repo_root: Path
) -> None:
    """Core Markdown files must only reference paths inside the
    repository. This guards against accidental external coupling via
    the Core's normative Markdown.
    """

    for path in iter_markdown_files(governance_core):
        references = extract_internal_references(path)
        for ref, resolved, _ in _references_to_paths(references, repo_root):
            if not looks_like_path(ref.target_path):
                continue
            if is_glob_or_branch_pattern(ref.target_path):
                continue
            if not is_inside_repository(resolved, repo_root):
                pytest.fail(
                    f"{path.relative_to(repo_root)}:{ref.line_no} "
                    f"references path outside repository: {ref.target_path}"
                )


def test_consumer_side_references_are_explicitly_documented(
    governance_core: Path, repo_root: Path
) -> None:
    """Every `.agent-coordination/...` reference inside the Core
    must be intentional consumer-installation documentation, not a
    typo for a source-side path. This guards the source product
    from a future regression that re-points a consumer artifact to
    a source path.
    """

    consumer_count = 0
    for path in iter_markdown_files(governance_core):
        for ref, resolved, exists in _references_to_paths(
            extract_internal_references(path), repo_root
        ):
            if is_consumer_side_reference(ref.target_path):
                assert not exists, (
                    f"{path.relative_to(repo_root)}:{ref.line_no} "
                    f"references a consumer artifact that unexpectedly "
                    f"exists at the source repository root: "
                    f"{resolved.relative_to(repo_root)}"
                )
                consumer_count += 1
    assert consumer_count > 0, (
        "Expected at least one documented consumer-side reference; "
        "the Core must continue to document consumer installation paths."
    )


def test_checkpoint_files_are_markdown_not_json(
    repo_root: Path,
) -> None:
    """The source Orchestrator checkpoint files must remain Markdown
    so the executor cannot accidentally treat them as a consumer
    `STATE.json` equivalent.
    """

    for relative in (
        "docs/ORCHESTRATOR-CHECKPOINTS.md",
        "docs/orchestrator/CHECKPOINT.md",
    ):
        path = repo_root / relative
        assert path.suffix == ".md", f"{relative} must remain Markdown"
        text = path.read_text(encoding="utf-8")
        assert text.startswith("#"), f"{relative} must be a Markdown file"


# --- R1-REF regression coverage -----------------------------------------
#
# R2 keeps only known extension prose tokens exempted. Dotfiles must
# remain concrete candidates, and canonical resolution must reject `..` escapes.


@pytest.mark.parametrize(
    "extension_token",
    [".md", ".py", ".toml", ".json", ".lock", ".yaml", ".yml"],
)
def test_extension_only_token_is_treated_as_prose(extension_token: str) -> None:
    """Genuine extension-only tokens are valid prose that cannot be
    resolved to a single file and must remain exempted from
    mechanical reference resolution.
    """

    assert is_directory_or_extension_only(extension_token) is True


@pytest.mark.parametrize(
    "concrete_path",
    [
        "./docs/ORCHESTRATOR-CHECKPOINTS.md",
        ".github/workflows/check.yml",
        "./tests/test_reference_integrity.py",
        ".python-version",
        "./pyproject.toml",
    ],
)
def test_concrete_dot_prefixed_path_is_not_exempted(concrete_path: str) -> None:
    """Concrete dot-prefixed paths must remain eligible for
    mechanical resolution. They contain a path separator or a
    bare filename component and are not extension-only tokens.
    """

    assert is_directory_or_extension_only(concrete_path) is False, (
        f"Concrete path {concrete_path!r} must not be exempted from mechanical reference resolution"
    )


def test_dotfile_is_treated_as_a_concrete_path() -> None:
    """A root dotfile is not extension-only prose."""

    assert is_directory_or_extension_only(".gitignore") is False


def test_directory_only_token_is_treated_as_prose() -> None:
    """A trailing-slash target is a directory reference, not a
    concrete file path, and must remain exempted.
    """

    assert is_directory_or_extension_only("handoffs/") is True
    assert is_directory_or_extension_only("./handoffs/") is True


def test_concrete_dot_prefixed_path_resolves_when_present(
    repo_root: Path,
) -> None:
    """A concrete dot-prefixed reference that points at an existing
    file must resolve through the same machinery as any other
    concrete path.
    """

    target = "./docs/ORCHESTRATOR-CHECKPOINTS.md"
    assert is_directory_or_extension_only(target) is False
    assert looks_like_path(target)
    resolved = repo_root / target.lstrip("./")
    assert resolved.is_file(), f"Expected {target} to resolve to an existing file"


def test_missing_concrete_dot_prefixed_path_is_classified_as_unresolved(
    tmp_path: Path,
) -> None:
    """A concrete dot-prefixed reference that points at a file the
    repository does not contain must be classified as unresolved by
    the resolution helper, not silently ignored as 'extension only'.
    """

    target = "./does-not-exist/check.yml"
    assert is_directory_or_extension_only(target) is False
    assert looks_like_path(target)
    resolved = tmp_path / target.lstrip("./")
    assert not resolved.exists()
    assert is_glob_or_branch_pattern(target) is False
    assert is_consumer_side_reference(target) is False


def test_existing_dotfile_resolves(repo_root: Path) -> None:
    """Existing root dotfiles resolve as concrete paths."""

    reference = Reference(
        source=repo_root / "AGENTS.md",
        line_no=1,
        raw=".gitignore",
        target=".gitignore",
    )
    resolved, exists = _resolve(reference, repo_root)
    assert exists
    assert resolved == repo_root / ".gitignore"


def test_missing_dotfile_is_unresolved(repo_root: Path) -> None:
    """Missing dotfiles are not exempted as extension-only prose."""

    reference = Reference(
        source=repo_root / "AGENTS.md",
        line_no=1,
        raw=".missingconfig",
        target=".missingconfig",
    )
    resolved, exists = _resolve(reference, repo_root)
    assert is_directory_or_extension_only(reference.target_path) is False
    assert not exists
    assert resolved == repo_root / ".missingconfig"


def test_reference_resolution_flags_concrete_dot_prefixed_paths(
    repo_root: Path,
) -> None:
    """The per-reference resolution helper must report ``exists=False``
    for a missing concrete dot-prefixed path rather than classifying
    it as an exempt extension token.
    """

    fake_reference = Reference(
        source=repo_root / "AGENTS.md",
        line_no=1,
        raw="./does-not-exist/check.yml",
        target="./does-not-exist/check.yml",
    )
    resolved, exists = _resolve(fake_reference, repo_root)
    assert not exists
    assert resolved == repo_root / "does-not-exist" / "check.yml"


def test_parent_traversal_reference_is_outside_repository(tmp_path: Path) -> None:
    """Canonical resolution rejects lexical parent traversal outside root."""

    repo_root = tmp_path / "repository"
    repo_root.mkdir()
    reference = Reference(
        source=repo_root / "governance-core" / "GOVERNANCE.md",
        line_no=1,
        raw="../outside.md",
        target="../outside.md",
    )
    resolved, _ = _resolve(reference, repo_root)
    assert is_inside_repository(resolved, repo_root) is False


@pytest.mark.parametrize(
    "taxonomy",
    [
        "ADDED / MODIFIED / REMOVED / PRESERVED",
        "ADDED/MODIFIED/REMOVED/PRESERVED",
        "Converge / Accept",
        "Converge/Accept",
        "Converge / Accept / Evolve",
        "Converge/Accept/Evolve",
    ],
)
def test_sdd_taxonomy_is_not_classified_as_a_repository_path(taxonomy: str) -> None:
    """Accepted slash-separated SDD terms are prose, not repository paths."""

    assert looks_like_path(taxonomy) is False


def test_inline_branch_alignment_comparison_is_not_classified_as_path() -> None:
    """A complete inline equivalence expression is prose, not a path."""

    assert looks_like_path("develop == origin/develop") is False


def test_unspaced_comparison_like_token_remains_a_path_candidate() -> None:
    """The comparison exemption requires a structurally delimited operator."""

    assert looks_like_path("docs/tasks==archive.md") is True


@pytest.mark.parametrize(
    "concrete_path",
    [
        "docs/tasks/T034-native-sdd-executable-materialization.md",
        "governance-core/SDD.md",
        "src/agent_governance/artifact.py",
        ".github/workflows/check.yml",
        "../outside.md",
    ],
)
def test_concrete_slash_paths_remain_path_candidates(concrete_path: str) -> None:
    """The taxonomy correction must not weaken concrete path classification."""

    assert looks_like_path(concrete_path) is True
