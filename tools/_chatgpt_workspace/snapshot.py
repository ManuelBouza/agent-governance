"""Deterministic portable snapshot creation and fail-closed validation."""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import re
import tarfile
from collections.abc import Mapping
from pathlib import Path, PurePosixPath

from .git_state import GitInspectionError, inspect_repository
from .models import Decision, Identity, Receipt, Status, require_sha


def archive_sha256(archive: Path) -> str:
    digest = hashlib.sha256()
    with archive.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tar_info(name: str, *, directory: bool, size: int = 0) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.type = tarfile.DIRTYPE if directory else tarfile.REGTYPE
    info.mode = 0o755 if directory else 0o644
    info.size = size
    info.uid = info.gid = 0
    info.uname = info.gname = ""
    info.mtime = 0
    return info


def create_snapshot(repository: Path, receipt: Receipt, archive: Path) -> str:
    """Create a deterministic tar.gz containing ``repository/`` and ``receipt.json``."""
    repository = repository.resolve()
    if not repository.is_dir() or not (repository / ".git").is_dir():
        raise ValueError("source must be a standalone repository with a real .git directory")
    entries = sorted(
        repository.rglob("*"), key=lambda path: path.relative_to(repository).as_posix()
    )
    for entry in entries:
        if entry.is_symlink() or not (entry.is_dir() or entry.is_file()):
            raise ValueError(f"unsupported snapshot source entry: {entry}")
    archive.parent.mkdir(parents=True, exist_ok=True)
    receipt_bytes = (
        json.dumps(receipt.as_dict(), sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()
    with (
        archive.open("wb") as raw,
        gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as compressed,
        tarfile.open(fileobj=compressed, mode="w") as bundle,
    ):
        bundle.addfile(_tar_info("repository", directory=True))
        for entry in entries:
            relative = entry.relative_to(repository).as_posix()
            name = f"repository/{relative}"
            if entry.is_dir():
                bundle.addfile(_tar_info(name, directory=True))
            else:
                data = entry.read_bytes()
                bundle.addfile(_tar_info(name, directory=False, size=len(data)), io.BytesIO(data))
        bundle.addfile(
            _tar_info("receipt.json", directory=False, size=len(receipt_bytes)),
            io.BytesIO(receipt_bytes),
        )
    return archive_sha256(archive)


_DRIVE = re.compile(r"^[A-Za-z]:")


def _safe_name(member: tarfile.TarInfo) -> tuple[str, bool]:
    raw = member.name
    normalized_input = raw.replace("\\", "/")
    path = PurePosixPath(normalized_input)
    if (
        not raw
        or raw.startswith(("/", "\\"))
        or _DRIVE.match(normalized_input)
        or path.is_absolute()
        or any(part in ("", ".", "..") for part in path.parts)
    ):
        raise ValueError(f"unsafe archive member path: {raw!r}")
    if member.issym() or member.islnk():
        raise ValueError(f"archive links are prohibited: {raw!r}")
    if not (member.isdir() or member.isfile()):
        raise ValueError(f"unsupported archive member type: {raw!r}")
    return path.as_posix(), member.isdir()


def _validate_members(members: list[tarfile.TarInfo]) -> None:
    seen: dict[str, bool] = {}
    for member in members:
        name, is_directory = _safe_name(member)
        if name in seen:
            raise ValueError(f"duplicate archive member: {name}")
        parts = PurePosixPath(name).parts
        if parts[0] not in ("repository", "receipt.json"):
            raise ValueError(f"unexpected archive root: {parts[0]}")
        if parts[0] == "receipt.json" and (len(parts) != 1 or is_directory):
            raise ValueError("receipt.json must be one regular root file")
        for index in range(1, len(parts)):
            prefix = PurePosixPath(*parts[:index]).as_posix()
            if prefix in seen and not seen[prefix]:
                raise ValueError(f"archive file/directory prefix collision: {prefix}")
        if not is_directory:
            prefix = f"{name}/"
            if any(previous.startswith(prefix) for previous in seen):
                raise ValueError(f"archive file/directory prefix collision: {name}")
        seen[name] = is_directory
    if seen.get("repository") is not True or seen.get("receipt.json") is not False:
        raise ValueError("archive must contain repository/ and receipt.json")


def safe_extract(archive: Path, destination: Path) -> None:
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("extraction destination must be empty")
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, mode="r:gz") as bundle:
        members = bundle.getmembers()
        _validate_members(members)
        bundle.extractall(destination, members=members, filter="data")
    root = destination.resolve()
    for entry in destination.rglob("*"):
        if not entry.resolve().is_relative_to(root):
            raise ValueError("archive extraction escaped destination")


def _identity_mismatch(receipt: Receipt, expected: Identity) -> bool:
    return receipt.identity() != expected


def validate_snapshot(
    archive: Path,
    destination: Path,
    *,
    expected_archive_sha256: str,
    expected_identity: Identity,
    expected_remote_head: str,
    expected_remote_tree: str,
    require_clean: bool = True,
    require_remote_tree_equivalence: bool = False,
) -> Decision:
    """Validate one candidate without repairing or promoting any external state."""
    try:
        checksum = require_sha(expected_archive_sha256, "expected_archive_sha256")
        if len(checksum) != 64:
            raise ValueError("expected_archive_sha256 must be a 64-character SHA-256 digest")
        remote_head = require_sha(expected_remote_head, "expected_remote_head")
        remote_tree = require_sha(expected_remote_tree, "expected_remote_tree")
        actual_checksum = archive_sha256(archive)
        if actual_checksum != checksum:
            return Decision(Status.BLOCKED_INVALID_SNAPSHOT, "archive checksum mismatch")
        safe_extract(archive, destination)
        receipt_value = json.loads((destination / "receipt.json").read_text(encoding="utf-8"))
        if not isinstance(receipt_value, Mapping):
            raise ValueError("receipt must be a JSON object")
        receipt = Receipt.from_mapping(receipt_value)
        if _identity_mismatch(receipt, expected_identity):
            return Decision(Status.BLOCKED_IDENTITY_MISMATCH, "receipt identity does not match")
        if receipt.remote_head_sha != remote_head or receipt.remote_tree_sha != remote_tree:
            return Decision(
                Status.BLOCKED_STALE_OR_WRONG_SNAPSHOT,
                "receipt remote identity is stale or wrong",
            )
        state = inspect_repository(destination / "repository")
        if state.branch != receipt.topic_branch:
            return Decision(
                Status.BLOCKED_IDENTITY_MISMATCH, "snapshot branch does not match receipt"
            )
        if (
            state.head != receipt.local_snapshot_head_sha
            or state.tree != receipt.local_snapshot_tree_sha
        ):
            return Decision(
                Status.BLOCKED_STALE_OR_WRONG_SNAPSHOT,
                "snapshot Git identity does not match receipt",
            )
        if require_clean and (not receipt.working_tree_clean or not state.clean):
            return Decision(Status.BLOCKED_INVALID_SNAPSHOT, "snapshot worktree is not clean")
        if require_remote_tree_equivalence and state.tree != remote_tree:
            return Decision(
                Status.BLOCKED_STALE_OR_WRONG_SNAPSHOT,
                "snapshot tree differs from expected remote tree",
            )
        return Decision(
            Status.SNAPSHOT_VALID,
            "checksum, archive, receipt, Git and freshness validation passed",
            {
                "archive_sha256": actual_checksum,
                "repository_path": str(destination / "repository"),
                "receipt": receipt.as_dict(),
                "local_head": state.head,
                "local_tree": state.tree,
                "working_tree_clean": state.clean,
            },
        )
    except (
        OSError,
        tarfile.TarError,
        json.JSONDecodeError,
        ValueError,
        GitInspectionError,
    ) as error:
        return Decision(Status.BLOCKED_INVALID_SNAPSHOT, str(error))
