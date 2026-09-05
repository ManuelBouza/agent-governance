"""Deterministic publication manifest generation without network mutation."""

from __future__ import annotations

from pathlib import Path, PurePosixPath

from .git_state import inspect_repository
from .models import Decision, Status, require_sha, require_text


def _normalize_changed_path(value: object) -> str:
    text = require_text(value, "changed_paths entry").replace("\\", "/")
    path = PurePosixPath(text)
    if path.is_absolute() or ".." in path.parts or ":" in path.parts[0]:
        raise ValueError(f"unsafe changed path: {text}")
    normalized = path.as_posix()
    if normalized in ("", "."):
        raise ValueError("changed path must identify a repository file")
    return normalized


def build_publication_plan(
    repository_path: Path,
    *,
    repository: str,
    work_unit: str,
    topic_branch: str,
    expected_remote_head: str,
    changed_paths: list[object],
) -> Decision:
    repository = require_text(repository, "repository")
    work_unit = require_text(work_unit, "work_unit")
    topic_branch = require_text(topic_branch, "topic_branch")
    expected_remote_head = require_sha(expected_remote_head, "expected_remote_head")
    state = inspect_repository(repository_path)
    if state.branch != topic_branch:
        return Decision(Status.BLOCKED_IDENTITY_MISMATCH, "local topic branch does not match")
    paths = sorted({_normalize_changed_path(path) for path in changed_paths})
    if not paths:
        raise ValueError("changed_paths must contain at least one path")
    return Decision(
        Status.PUBLICATION_PLAN_READY,
        "local publication plan created; no publication was performed",
        {
            "repository": repository,
            "work_unit": work_unit,
            "topic_branch": topic_branch,
            "expected_remote_head": expected_remote_head,
            "local_head": state.head,
            "local_tree": state.tree,
            "changed_paths": paths,
        },
    )
