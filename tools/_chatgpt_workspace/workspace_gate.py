"""Portable writable-entry classification."""

from __future__ import annotations

from .models import Decision, Identity, LockObservation, Receipt, Status


def classify_write_entry(
    snapshot: Decision,
    *,
    expected_identity: Identity,
    lock_observation: LockObservation,
    observed_remote_head: str | None,
    observed_remote_tree: str | None = None,
    require_tree_equivalence: bool = False,
) -> Decision:
    if snapshot.status is not Status.SNAPSHOT_VALID:
        reasons = {
            Status.BLOCKED_IDENTITY_MISMATCH: Status.BLOCKED_IDENTITY_MISMATCH,
            Status.BLOCKED_STALE_OR_WRONG_SNAPSHOT: Status.BLOCKED_STALE_OR_WRONG_SNAPSHOT,
            Status.BLOCKED_STALE_BASE: Status.BLOCKED_STALE_BASE,
        }
        reason = reasons.get(snapshot.status, Status.BLOCKED_INVALID_SNAPSHOT).value
        return Decision(Status.WRITE_BLOCKED, reason, {"snapshot_status": snapshot.status.value})
    try:
        receipt_value = snapshot.details["receipt"]
        receipt = Receipt.from_mapping(receipt_value)
    except (KeyError, TypeError, ValueError) as error:
        return Decision(
            Status.WRITE_BLOCKED, Status.BLOCKED_INVALID_SNAPSHOT.value, {"error": str(error)}
        )
    if receipt.identity() != expected_identity:
        return Decision(Status.WRITE_BLOCKED, Status.BLOCKED_IDENTITY_MISMATCH.value)
    if lock_observation.expected_lock_head != lock_observation.observed_lock_head:
        return Decision(Status.WRITE_BLOCKED, Status.BLOCKED_STALE_LOCK_HEAD.value)
    if (
        not lock_observation.sentinel_present
        or lock_observation.sentinel_identity() != expected_identity
        or lock_observation.state != "ACTIVE"
    ):
        return Decision(Status.WRITE_BLOCKED, Status.BLOCKED_IDENTITY_MISMATCH.value)
    if not observed_remote_head or observed_remote_head != receipt.remote_head_sha:
        return Decision(Status.WRITE_BLOCKED, Status.BLOCKED_STALE_BASE.value)
    if require_tree_equivalence and (
        not observed_remote_tree or observed_remote_tree != receipt.local_snapshot_tree_sha
    ):
        return Decision(Status.WRITE_BLOCKED, Status.BLOCKED_STALE_OR_WRONG_SNAPSHOT.value)
    return Decision(Status.WRITE_ALLOWED, "all snapshot, ownership and freshness gates passed")
