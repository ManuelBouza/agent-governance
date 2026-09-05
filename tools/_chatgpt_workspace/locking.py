"""Pure lock-acquisition and release classifiers."""

from __future__ import annotations

from .models import Decision, Identity, LockObservation, Status, require_sha


def classify_acquisition(observation: LockObservation) -> Decision:
    if observation.expected_lock_head != observation.observed_lock_head:
        return Decision(Status.BLOCKED_STALE_LOCK_HEAD, "observed lock HEAD is stale")
    if observation.sentinel_present:
        try:
            require_sha(observation.sentinel_blob_sha, "sentinel_blob_sha")
        except ValueError:
            return Decision(Status.BLOCKED_AMBIGUOUS_LOCK, "sentinel blob SHA is invalid")
        if observation.sentinel_identity() is None or not observation.state:
            return Decision(Status.BLOCKED_AMBIGUOUS_LOCK, "sentinel identity is incomplete")
        return Decision(Status.BLOCKED_OWNER_EXISTS, "lock sentinel already exists")
    sentinel_fields = (
        observation.repository,
        observation.owner,
        observation.work_unit,
        observation.topic_branch,
        observation.state,
        observation.sentinel_blob_sha,
    )
    if any(value is not None for value in sentinel_fields):
        return Decision(Status.BLOCKED_AMBIGUOUS_LOCK, "absent sentinel has contradictory data")
    return Decision(Status.ACQUIRE_ALLOWED, "fresh lock HEAD and sentinel is absent")


def classify_release(
    observation: LockObservation,
    expected: Identity,
    expected_sentinel_blob_sha: str,
) -> Decision:
    try:
        expected_blob = require_sha(expected_sentinel_blob_sha, "expected_sentinel_blob_sha")
    except ValueError as error:
        return Decision(Status.BLOCKED_AMBIGUOUS_LOCK, str(error))
    if observation.expected_lock_head != observation.observed_lock_head:
        return Decision(Status.BLOCKED_STALE_LOCK_HEAD, "observed lock HEAD is stale")
    if not observation.sentinel_present:
        return Decision(Status.BLOCKED_AMBIGUOUS_LOCK, "sentinel is absent before release")
    if observation.sentinel_identity() != expected or observation.state != "ACTIVE":
        return Decision(
            Status.BLOCKED_IDENTITY_MISMATCH, "current sentinel ownership does not match"
        )
    try:
        current_blob = require_sha(observation.sentinel_blob_sha, "sentinel_blob_sha")
    except ValueError as error:
        return Decision(Status.BLOCKED_AMBIGUOUS_LOCK, str(error))
    if current_blob != expected_blob:
        return Decision(Status.BLOCKED_STALE_LOCK_HEAD, "current sentinel blob SHA changed")
    return Decision(
        Status.RELEASE_ALLOWED,
        "exact current sentinel may be deleted by the host",
        {"sentinel_blob_sha": current_blob},
    )


def verify_release(observation: LockObservation) -> Decision:
    if observation.expected_lock_head != observation.observed_lock_head:
        return Decision(
            Status.BLOCKED_STALE_LOCK_HEAD, "post-delete lock HEAD observation is stale"
        )
    if observation.sentinel_present:
        return Decision(Status.BLOCKED_OWNER_EXISTS, "sentinel remains present after deletion")
    contradictory = any(
        value is not None
        for value in (
            observation.repository,
            observation.owner,
            observation.work_unit,
            observation.topic_branch,
            observation.state,
            observation.sentinel_blob_sha,
        )
    )
    if contradictory:
        return Decision(Status.BLOCKED_AMBIGUOUS_LOCK, "absence observation is contradictory")
    return Decision(Status.RELEASED, "host-reported sentinel absence verified")
