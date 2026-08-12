"""Deterministic source-maintenance learning-signal detectors."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

DETECTOR_ID: Final = "agent-governance.learning-signals"
DETECTOR_VERSION: Final = "1"

POST_MERGE_ADVANCE: Final = "git.branch.post_merge_advance"
DELETE_BEFORE_RESOLUTION: Final = "git.branch.delete_before_review_resolution"
HANDOFF_IDENTITY_MISMATCH: Final = "task.handoff.identity_mismatch"
DONE_REQUIRES_REWORK: Final = "task.done_requires_rework"
PROCEDURAL_NONCONFORMANCE: Final = "workflow.procedural_nonconformance"

FINGERPRINTS: Final = frozenset(
    {
        POST_MERGE_ADVANCE,
        DELETE_BEFORE_RESOLUTION,
        HANDOFF_IDENTITY_MISMATCH,
        DONE_REQUIRES_REWORK,
        PROCEDURAL_NONCONFORMANCE,
    }
)


@dataclass(frozen=True, slots=True)
class Finding:
    fingerprint: str
    detector_id: str
    detector_version: str
    severity: str
    classification: str
    subject: str
    reference: str
    reason: str
    evidence: dict[str, Any]
    disposition: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _finding(
    fingerprint: str,
    case: dict[str, Any],
    *,
    severity: str,
    classification: str,
    reason: str,
    evidence: dict[str, Any],
    disposition: str,
) -> Finding:
    return Finding(
        fingerprint=fingerprint,
        detector_id=DETECTOR_ID,
        detector_version=DETECTOR_VERSION,
        severity=severity,
        classification=classification,
        subject=case["subject"],
        reference=case["reference"],
        reason=reason,
        evidence=evidence,
        disposition=disposition,
    )


def detect(case: dict[str, Any]) -> list[Finding]:
    """Interpret normalized facts without inferring cause, intent, or remediation."""

    kind = case["signal"]
    if kind == "branch_post_merge_state":
        return _detect_post_merge_advance(case)
    if kind == "branch_deletion_attempt":
        return _detect_delete_before_resolution(case)
    if kind == "task_handoff_identity":
        return _detect_handoff_identity(case)
    if kind == "task_review_outcome":
        return _detect_done_requires_rework(case)
    if kind == "procedural_nonconformance":
        return _detect_procedural_nonconformance(case)
    raise ValueError(f"unsupported learning signal: {kind}")


def detect_as_dicts(case: dict[str, Any]) -> list[dict[str, Any]]:
    """Return stable machine-readable output for checks and future aggregation."""

    return [finding.to_dict() for finding in detect(case)]


def _detect_post_merge_advance(case: dict[str, Any]) -> list[Finding]:
    facts = case["facts"]
    if not facts["source_branch_present"]:
        return []
    if facts["reviewed_head_sha"] == facts["current_source_head_sha"]:
        return []
    return [
        _finding(
            POST_MERGE_ADVANCE,
            case,
            severity="error",
            classification="repository_state_nonconformance",
            reason="surviving merged source branch differs from reviewed head",
            evidence={
                "current_source_head_sha": facts["current_source_head_sha"],
                "reviewed_head_sha": facts["reviewed_head_sha"],
                "source_branch": facts["source_branch"],
            },
            disposition="blocking",
        )
    ]


def _detect_delete_before_resolution(case: dict[str, Any]) -> list[Finding]:
    facts = case["facts"]
    identity_complete = bool(
        facts.get("reviewed_head_sha")
        and facts.get("observed_head_sha")
        and facts["reviewed_head_sha"] == facts["observed_head_sha"]
    )
    authorized = facts["disposition"] in {"DELETE", "RESOLVED_ABANDON"}
    if facts["action"] != "DELETE" or (authorized and identity_complete):
        return []
    missing = []
    if not authorized:
        missing.append("resolved_disposition")
    if not identity_complete:
        missing.append("matching_head_identity")
    return [
        _finding(
            DELETE_BEFORE_RESOLUTION,
            case,
            severity="error",
            classification="unsafe_destructive_action",
            reason="branch deletion attempted without resolved disposition and exact identity evidence",
            evidence={
                "action": facts["action"],
                "disposition": facts["disposition"],
                "missing": missing,
                "observed_head_sha": facts.get("observed_head_sha"),
                "reviewed_head_sha": facts.get("reviewed_head_sha"),
            },
            disposition="blocking",
        )
    ]


def _detect_handoff_identity(case: dict[str, Any]) -> list[Finding]:
    facts = case["facts"]
    fields = ("task_id", "branch", "handoff_path")
    mismatches = [
        {
            "actual": facts["actual"].get(field),
            "expected": facts["expected"].get(field),
            "field": field,
        }
        for field in fields
        if facts["actual"].get(field) != facts["expected"].get(field)
    ]
    if not mismatches:
        return []
    return [
        _finding(
            HANDOFF_IDENTITY_MISMATCH,
            case,
            severity="error",
            classification="evidence_identity_nonconformance",
            reason="persisted or returned task identity differs from expected identity",
            evidence={"mismatches": mismatches},
            disposition="blocking",
        )
    ]


def _detect_done_requires_rework(case: dict[str, Any]) -> list[Finding]:
    facts = case["facts"]
    if facts["executor_status"] != "DONE" or facts["review_disposition"] != "REWORK_REQUIRED":
        return []
    return [
        _finding(
            DONE_REQUIRES_REWORK,
            case,
            severity="info",
            classification="review_learning_candidate",
            reason="formal review required rework after executor reported DONE",
            evidence={
                "executor_status": facts["executor_status"],
                "review_disposition": facts["review_disposition"],
                "review_reference": facts["review_reference"],
            },
            disposition="learning_candidate_only",
        )
    ]


def _detect_procedural_nonconformance(case: dict[str, Any]) -> list[Finding]:
    facts = case["facts"]
    if facts.get("procedural_nonconformance") is not True:
        return []
    return [
        _finding(
            PROCEDURAL_NONCONFORMANCE,
            case,
            severity="warning",
            classification="persisted_procedural_nonconformance",
            reason="structured evidence explicitly records procedural nonconformance",
            evidence={
                "code": facts["code"],
                "evidence_reference": facts["evidence_reference"],
            },
            disposition="advisory",
        )
    ]
