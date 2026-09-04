"""Git-index inventory and worktree-byte access."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path, PurePosixPath

from .common import MeasurementError


def git(root: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=False,
        capture_output=True,
        timeout=30,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise MeasurementError(f"git {' '.join(arguments)} failed: {detail}")
    return result.stdout


def tracked_paths(root: Path, excluded: set[str]) -> list[str]:
    raw = git(root, "ls-files", "--cached", "-z")
    paths = [os.fsdecode(path) for path in raw.split(b"\0") if path]
    return sorted(path for path in paths if PurePosixPath(path).as_posix() not in excluded)


def read_tracked_file(root: Path, relative: str) -> bytes:
    path = root / relative
    if path.is_symlink():
        return os.fsencode(os.readlink(path))
    try:
        return path.read_bytes()
    except OSError as error:
        raise MeasurementError(f"cannot read tracked file {relative}: {error}") from error
