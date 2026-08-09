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


def is_directory_or_extension_only(target: str) -> bool:
    """Return True when `target` describes a directory or a file
    extension rather than a concrete file path. These are valid
    prose references that cannot be resolved mechanically to a
    single file.
    """

    if target.endswith("/"):
        return True
    return bool(target.startswith("."))


def _resolve(reference: Reference, repo_root: Path) -> tuple[Path, bool]:
    target = reference.target_path
    if not looks_like_path(target):
        return Path(target), False
    return repo_root / target, (repo_root / target).exists()


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
            try:
                resolved.relative_to(repo_root)
            except ValueError:
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
