"""Strict data models and stable status vocabulary for portable workspaces."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class Status(StrEnum):
    SNAPSHOT_VALID = "SNAPSHOT_VALID"
    ACQUIRE_ALLOWED = "ACQUIRE_ALLOWED"
    BLOCKED_STALE_LOCK_HEAD = "BLOCKED_STALE_LOCK_HEAD"
    BLOCKED_OWNER_EXISTS = "BLOCKED_OWNER_EXISTS"
    BLOCKED_AMBIGUOUS_LOCK = "BLOCKED_AMBIGUOUS_LOCK"
    BLOCKED_IDENTITY_MISMATCH = "BLOCKED_IDENTITY_MISMATCH"
    BLOCKED_STALE_OR_WRONG_SNAPSHOT = "BLOCKED_STALE_OR_WRONG_SNAPSHOT"
    BLOCKED_INVALID_SNAPSHOT = "BLOCKED_INVALID_SNAPSHOT"
    BLOCKED_STALE_BASE = "BLOCKED_STALE_BASE"
    WRITE_ALLOWED = "WRITE_ALLOWED"
    WRITE_BLOCKED = "WRITE_BLOCKED"
    RELEASE_ALLOWED = "RELEASE_ALLOWED"
    RELEASED = "RELEASED"
    GC_ELIGIBLE = "GC_ELIGIBLE"
    RETAIN_ACTIVE = "RETAIN_ACTIVE"
    RETAIN_CLOSED_UNMERGED = "RETAIN_CLOSED_UNMERGED"
    RETAIN_AMBIGUOUS = "RETAIN_AMBIGUOUS"
    RETAIN_INVALID_TARGET_SNAPSHOT = "RETAIN_INVALID_TARGET_SNAPSHOT"
    PUBLICATION_PLAN_READY = "PUBLICATION_PLAN_READY"
    INVALID_INPUT = "INVALID_INPUT"


@dataclass(frozen=True)
class Decision:
    status: Status
    reason: str
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {"status": self.status.value, "reason": self.reason, "details": self.details}


_SHA_RE = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
PROTECTED_BRANCHES = frozenset({"develop", "main"})


def require_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value


def require_sha(value: object, field_name: str) -> str:
    text = require_text(value, field_name)
    if _SHA_RE.fullmatch(text) is None:
        raise ValueError(f"{field_name} must be a lowercase 40- or 64-character Git SHA")
    return text


@dataclass(frozen=True)
class Identity:
    repository: str
    owner: str
    work_unit: str
    topic_branch: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> Identity:
        return cls(
            repository=require_text(value.get("repository"), "repository"),
            owner=require_text(value.get("owner"), "owner"),
            work_unit=require_text(value.get("work_unit"), "work_unit"),
            topic_branch=require_text(value.get("topic_branch"), "topic_branch"),
        )


@dataclass(frozen=True)
class Receipt:
    schema: str
    repository: str
    owner: str
    work_unit: str
    topic_branch: str
    target_branch: str
    remote_head_sha: str
    remote_tree_sha: str
    local_snapshot_head_sha: str
    local_snapshot_tree_sha: str
    working_tree_clean: bool
    lock_branch: str | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> Receipt:
        schema = require_text(value.get("schema"), "schema")
        if schema != "chatgpt-portable-workspace/v1":
            raise ValueError("unsupported receipt schema")
        clean = value.get("working_tree_clean")
        if type(clean) is not bool:
            raise ValueError("working_tree_clean must be a boolean")
        lock_branch = value.get("lock_branch")
        if lock_branch is not None:
            lock_branch = require_text(lock_branch, "lock_branch")
        return cls(
            schema=schema,
            repository=require_text(value.get("repository"), "repository"),
            owner=require_text(value.get("owner"), "owner"),
            work_unit=require_text(value.get("work_unit"), "work_unit"),
            topic_branch=require_text(value.get("topic_branch"), "topic_branch"),
            target_branch=require_text(value.get("target_branch"), "target_branch"),
            remote_head_sha=require_sha(value.get("remote_head_sha"), "remote_head_sha"),
            remote_tree_sha=require_sha(value.get("remote_tree_sha"), "remote_tree_sha"),
            local_snapshot_head_sha=require_sha(
                value.get("local_snapshot_head_sha"), "local_snapshot_head_sha"
            ),
            local_snapshot_tree_sha=require_sha(
                value.get("local_snapshot_tree_sha"), "local_snapshot_tree_sha"
            ),
            working_tree_clean=clean,
            lock_branch=lock_branch,
        )

    def identity(self) -> Identity:
        return Identity(self.repository, self.owner, self.work_unit, self.topic_branch)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LockObservation:
    expected_lock_head: str
    observed_lock_head: str
    sentinel_present: bool
    repository: str | None = None
    owner: str | None = None
    work_unit: str | None = None
    topic_branch: str | None = None
    state: str | None = None
    sentinel_blob_sha: str | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> LockObservation:
        present = value.get("sentinel_present")
        if type(present) is not bool:
            raise ValueError("sentinel_present must be a boolean")

        def optional_text(field_name: str) -> str | None:
            if field_name not in value or value[field_name] is None:
                return None
            return require_text(value[field_name], field_name)

        sentinel_blob_sha = optional_text("sentinel_blob_sha")
        if sentinel_blob_sha is not None:
            sentinel_blob_sha = require_sha(sentinel_blob_sha, "sentinel_blob_sha")
        return cls(
            expected_lock_head=require_sha(value.get("expected_lock_head"), "expected_lock_head"),
            observed_lock_head=require_sha(value.get("observed_lock_head"), "observed_lock_head"),
            sentinel_present=present,
            repository=optional_text("repository"),
            owner=optional_text("owner"),
            work_unit=optional_text("work_unit"),
            topic_branch=optional_text("topic_branch"),
            state=optional_text("state"),
            sentinel_blob_sha=sentinel_blob_sha,
        )

    def sentinel_identity(self) -> Identity | None:
        values = (self.repository, self.owner, self.work_unit, self.topic_branch)
        if not all(isinstance(value, str) and value for value in values):
            return None
        return Identity(*values)  # type: ignore[arg-type]
