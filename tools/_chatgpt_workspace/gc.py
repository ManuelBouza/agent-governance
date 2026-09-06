"""Fail-closed post-merge snapshot retention classifier."""

from __future__ import annotations

from .models import Decision, Status


def classify_gc(
    *,
    merged: bool | None,
    closed: bool | None,
    integration_verified: bool | None,
    target_snapshot_validated: bool | None,
    target_snapshot_promoted: bool | None,
    target_snapshot_revalidated: bool | None,
) -> Decision:
    values = (
        merged,
        closed,
        integration_verified,
        target_snapshot_validated,
        target_snapshot_promoted,
        target_snapshot_revalidated,
    )
    if any(type(value) not in (bool, type(None)) for value in values):
        return Decision(Status.RETAIN_AMBIGUOUS, "GC evidence contains an invalid type")
    if closed is True and merged is False:
        return Decision(Status.RETAIN_CLOSED_UNMERGED, "closed work was not merged")
    target = (
        target_snapshot_validated,
        target_snapshot_promoted,
        target_snapshot_revalidated,
    )
    if merged is True and any(value is False for value in target):
        return Decision(Status.RETAIN_INVALID_TARGET_SNAPSHOT, "target snapshot evidence failed")
    if merged is True and all(
        value is True
        for value in (
            integration_verified,
            target_snapshot_validated,
            target_snapshot_promoted,
            target_snapshot_revalidated,
        )
    ):
        return Decision(Status.GC_ELIGIBLE, "all post-merge evidence is positive")
    if merged is False and closed is False:
        return Decision(Status.RETAIN_ACTIVE, "work remains active or not integrated")
    return Decision(Status.RETAIN_AMBIGUOUS, "GC evidence is incomplete or ambiguous")
