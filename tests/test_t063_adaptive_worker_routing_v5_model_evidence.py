from __future__ import annotations

from evals.adaptive_worker_routing_v5 import runner as v5


def _payload(scored: list[dict[str, object]]) -> dict[str, object]:
    return {"scored_children": scored}


def test_adapter_block_is_not_model_quality_evidence() -> None:
    payload = _payload([])
    v5._annotate_model_evidence(
        payload=payload,
        status="BLOCKED",
        terminal_classification="BLOCKED_EXECUTION_INVALID",
        blocker={
            "message": "thread/resume failed: thread-store internal error: rollout at x is empty"
        },
        decision=None,
    )
    evidence = payload["model_evidence"]
    assert evidence["run_execution_validity"] == "INVALID"
    assert evidence["failure_domain"] == "MEASUREMENT_ADAPTER"
    assert evidence["run_model_comparison_eligible"] is False
    assert evidence["pilot_eligible"] is False
    assert evidence["scored_child_quality_eligible_count"] == 0
    assert evidence["unscored_child_attempts_count_as_model_quality"] is False
    assert evidence["root_model_failure_attributed"] is False


def test_profile_resolution_block_is_not_model_quality_evidence() -> None:
    payload = _payload([])
    v5._annotate_model_evidence(
        payload=payload,
        status="BLOCKED",
        terminal_classification="BLOCKED_PROFILE_RESOLUTION",
        blocker={"message": "profile unavailable"},
        decision=None,
    )
    assert payload["model_evidence"]["failure_domain"] == "PROFILE_RESOLUTION"
    assert payload["model_evidence"]["run_model_comparison_eligible"] is False


def test_valid_scored_child_remains_quality_eligible_in_partial_run() -> None:
    payload = _payload(
        [
            {
                "result_status": "FAIL",
                "arm": "ADAPTIVE",
                "total_tokens": 10,
                "duration_seconds": 1.0,
            }
        ]
    )
    v5._annotate_model_evidence(
        payload=payload,
        status="BLOCKED",
        terminal_classification="BLOCKED_MEASUREMENT_SURFACE",
        blocker={"message": "later arm lacked receipt"},
        decision=None,
    )
    child = payload["scored_children"][0]
    evidence = payload["model_evidence"]
    assert child["execution_validity"] == "VALID"
    assert child["failure_domain"] == "WORKER_QUALITY"
    assert child["model_quality_eligible"] is True
    assert child["model_efficiency_eligible"] is True
    assert evidence["scored_child_quality_eligible_count"] == 1
    assert evidence["run_model_comparison_eligible"] is False
    assert evidence["pilot_eligible"] is False


def test_only_clean_six_arm_completion_is_run_comparison_eligible() -> None:
    scored = [
        {
            "result_status": "PASS",
            "arm": "CONTROL" if index % 2 else "ADAPTIVE",
            "total_tokens": 10,
            "duration_seconds": 1.0,
        }
        for index in range(6)
    ]
    payload = _payload(scored)
    v5._annotate_model_evidence(
        payload=payload,
        status="COMPLETED",
        terminal_classification="COMPLETED_SCORED",
        blocker=None,
        decision="QUALIFIED",
    )
    evidence = payload["model_evidence"]
    assert evidence["run_execution_validity"] == "VALID"
    assert evidence["failure_domain"] is None
    assert evidence["run_model_comparison_eligible"] is True
    assert evidence["pilot_eligible"] is True
    assert evidence["scored_child_quality_eligible_count"] == 6


def test_v5_identity_excludes_v4_from_scoring() -> None:
    assert v5.EVIDENCE_BRANCH.endswith("requalification-v5")
    assert v5.TELEMETRY_DEFAULT.as_posix().endswith("telemetry-v5.json")
    assert v5.HANDOFF_DEFAULT.as_posix().endswith("handoff-v5.json")
    assert v5.HISTORICAL_BLOCKED_HEADS[-1] == v5.V4_TERMINAL_HEAD
