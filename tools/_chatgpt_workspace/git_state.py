"""Side-effect-bounded local Git inspection."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path


class GitInspectionError(RuntimeError):
    pass


@dataclass(frozen=True)
class GitState:
    head: str
    tree: str
    branch: str
    clean: bool


def _git(repository: Path, *args: str) -> str:
    env = os.environ.copy()
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0"})
    command = [
        "git",
        "-c",
        "core.fsmonitor=false",
        "-c",
        "core.hooksPath=NUL" if os.name == "nt" else "core.hooksPath=/dev/null",
        "-C",
        str(repository),
        *args,
    ]
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            env=env,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired, UnicodeError) as error:
        raise GitInspectionError(f"Git inspection failed: {error}") from error
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "unknown Git error"
        raise GitInspectionError(f"git {' '.join(args)} failed: {message}")
    return result.stdout.strip()


def inspect_repository(repository: Path) -> GitState:
    if not repository.is_dir() or not (repository / ".git").is_dir():
        raise GitInspectionError("snapshot is not a standalone Git repository")
    _git(repository, "fsck", "--full")
    status = _git(repository, "status", "--porcelain", "--untracked-files=all")
    head = _git(repository, "rev-parse", "--verify", "HEAD")
    tree = _git(repository, "rev-parse", "--verify", "HEAD^{tree}")
    branch = _git(repository, "symbolic-ref", "--quiet", "--short", "HEAD")
    return GitState(head=head, tree=tree, branch=branch, clean=not status)
