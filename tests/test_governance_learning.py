"""Deterministic EGLL detector and replay regressions."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from _governance_learning import (
    DETECTOR_ID,
    DETECTOR_VERSION,
    DONE_REQUIRES_REWORK,
    FINGERPRINTS,
    detect,
    detect_as_dicts,
)


@pytest.fixture(scope="module")
def cases() -> list[dict[str, object]]:
    path = Path(__file__).parent / "fixtures" / "governance_learning" / "cases.json"
    return json.loads(path.read_text(encoding="utf-8"))["cases"]


def test_replays_emit_only_expected_fingerprints(cases: list[dict[str, object]]) -> None:
    for case in cases:
        actual = [finding.fingerprint for finding in detect(case)]
        assert actual == case["expected_fingerprints"], case["id"]


def test_every_required_fingerprint_has_positive_and_negative_controls(
    cases: list[dict[str, object]],
) -> None:
    emitted = {fingerprint for case in cases for fingerprint in case["expected_fingerprints"]}
    assert emitted == FINGERPRINTS
    for signal in {case["signal"] for case in cases}:
        signal_cases = [case for case in cases if case["signal"] == signal]
        assert any(case["expected_fingerprints"] for case in signal_cases), signal
        assert any(not case["expected_fingerprints"] for case in signal_cases), signal


def test_t007_replays_preserve_freeze_and_safe_deletion_distinctions(
    cases: list[dict[str, object]],
) -> None:
    by_id = {case["id"]: case for case in cases}
    assert detect(by_id["t007-post-merge-branch-advanced"])[0].disposition == "blocking"
    assert detect(by_id["t007-delete-before-classification"])[0].disposition == "blocking"
    assert detect(by_id["t007-delete-after-explicit-resolution"]) == []


def test_identity_mismatch_evidence_is_field_ordered(cases: list[dict[str, object]]) -> None:
    case = next(case for case in cases if case["id"] == "handoff-identity-mismatch")
    finding = detect(case)[0]
    assert [item["field"] for item in finding.evidence["mismatches"]] == [
        "task_id",
        "branch",
        "handoff_path",
    ]


def test_done_rework_is_learning_only_not_blame_or_failure(
    cases: list[dict[str, object]],
) -> None:
    case = next(case for case in cases if case["id"] == "done-followed-by-formal-rework")
    finding = detect(case)[0]
    assert finding.fingerprint == DONE_REQUIRES_REWORK
    assert finding.classification == "review_learning_candidate"
    assert finding.disposition == "learning_candidate_only"
    assert finding.severity == "info"


def test_findings_are_stable_machine_readable_and_agent_neutral(
    cases: list[dict[str, object]],
) -> None:
    bad_cases = [case for case in cases if case["expected_fingerprints"]]
    first = [finding for case in bad_cases for finding in detect_as_dicts(case)]
    second = [finding for case in bad_cases for finding in detect_as_dicts(case)]
    assert first == second
    assert json.loads(json.dumps(first, sort_keys=True)) == first

    required = {
        "fingerprint",
        "detector_id",
        "detector_version",
        "severity",
        "classification",
        "subject",
        "reference",
        "reason",
        "evidence",
        "disposition",
    }
    assert all(finding.keys() == required for finding in first)
    assert all(finding["detector_id"] == DETECTOR_ID for finding in first)
    assert all(finding["detector_version"] == DETECTOR_VERSION for finding in first)
    serialized = json.dumps(first)
    for product_name in ("OpenCode", "Codex", "Claude", "ChatGPT"):
        assert product_name not in serialized


def test_detector_has_no_network_model_or_provider_dependency(repo_root: Path) -> None:
    source = (repo_root / "tests" / "_governance_learning.py").read_text(encoding="utf-8")
    forbidden_imports = (
        "anthropic",
        "httpx",
        "openai",
        "requests",
        "socket",
        "subprocess",
        "urllib",
    )
    assert all(f"import {name}" not in source for name in forbidden_imports)
    assert all(f"from {name}" not in source for name in forbidden_imports)


def test_unknown_signal_fails_closed() -> None:
    with pytest.raises(ValueError, match="unsupported learning signal"):
        detect(
            {
                "signal": "unknown",
                "subject": "synthetic:unknown",
                "reference": "synthetic:unknown",
                "facts": {},
            }
        )
