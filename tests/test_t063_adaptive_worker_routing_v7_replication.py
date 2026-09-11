from __future__ import annotations

from copy import deepcopy

import pytest

from evals.adaptive_worker_routing_v3.config import ExecutionInvalid
from evals.adaptive_worker_routing_v7 import runner as v7


def _child(
    probe: str,
    arm: str,
    *,
    passed: bool = True,
    total_tokens: int = 100,
    duration_seconds: float = 10.0,
    reroute: bool = False,
) -> dict[str, object]:
    model = "gpt-5.6-sol"
    effort = "medium"
    if arm == "ADAPTIVE" and probe == "P1":
        model = "gpt-5.6-luna"
    elif arm == "ADAPTIVE":
        model = "gpt-5.6-terra"
        if probe == "P3":
            effort = "high"
    return {
        "probe": probe,
        "arm": arm,
        "result_status": "PASS" if passed else "FAIL",
        "total_tokens": total_tokens,
        "duration_seconds": duration_seconds,
        "requested_model": model,
        "resolved_model": model,
        "requested_reasoning_effort": effort,
        "resolved_reasoning_effort": effort,
        "reroute_observed": reroute,
        "material_false_negative_count": 0 if passed else 1,
        "material_false_positive_count": 0,
    }


def _complete_scored(
    *,
    adaptive_tokens: int = 90,
    control_tokens: int = 110,
) -> list[dict[str, object]]:
    scored: list[dict[str, object]] = []
    for probe, arm, _, _ in v7.ARM_ORDER:
        tokens = adaptive_tokens if arm == "ADAPTIVE" else control_tokens
        scored.append(_child(probe, arm, total_tokens=tokens))
    return scored


def test_schedule_is_exactly_four_counterbalanced_blocks() -> None:
    assert len(v7.REPLICATE_BLOCKS) == 4
    assert len(v7.ARM_ORDER) == 24
    assert v7.REPLICATE_BLOCKS[0] == v7.BLOCK_1
    assert v7.REPLICATE_BLOCKS[1] == v7.BLOCK_2
    assert v7.REPLICATE_BLOCKS[2] == v7.BLOCK_1
    assert v7.REPLICATE_BLOCKS[3] == v7.BLOCK_2

    for probe in ("P1", "P2", "P3"):
        first = {"ADAPTIVE": 0, "CONTROL": 0}
        for block in v7.REPLICATE_BLOCKS:
            pair = [item for item in block if item[0] == probe]
            first[pair[0][1]] += 1
        assert first == {"ADAPTIVE": 2, "CONTROL": 2}


def test_all_pass_with_material_token_improvement_qualifies_efficiency() -> None:
    scored = _complete_scored(adaptive_tokens=80, control_tokens=100)
    metrics = v7.aggregate(scored)

    assert metrics["adaptive_quality_qualified"] is True
    assert metrics["control_quality_qualified"] is True
    assert metrics["exact_token_improvement"] == pytest.approx(0.2)
    assert (
        v7.pilot_decision(metrics, scored)
        == "QUALIFIED_PROFILE_AND_USAGE_EFFICIENCY"
    )


def test_all_pass_with_small_token_improvement_qualifies_routing_only() -> None:
    scored = _complete_scored(adaptive_tokens=96, control_tokens=100)
    metrics = v7.aggregate(scored)

    assert metrics["exact_token_improvement"] == pytest.approx(0.04)
    assert v7.pilot_decision(metrics, scored) == "QUALIFIED_PROFILE_ROUTING_ONLY"


def test_control_quality_failure_is_defined_complete_outcome() -> None:
    scored = _complete_scored()
    for child in reversed(scored):
        if child["probe"] == "P3" and child["arm"] == "CONTROL":
            child["result_status"] = "FAIL"
            child["material_false_negative_count"] = 1
            break

    metrics = v7.aggregate(scored)

    assert metrics["adaptive_quality_qualified"] is True
    assert metrics["control_quality_qualified"] is False
    assert metrics["per_probe"]["P3"]["pair_outcome"] == "ADAPTIVE_ONLY_QUALIFIED"
    assert (
        v7.pilot_decision(metrics, scored)
        == "ADAPTIVE_QUALITY_QUALIFIED_CONTROL_DEFICIENT"
    )


def test_adaptive_quality_failure_is_not_qualified() -> None:
    scored = _complete_scored()
    for child in scored:
        if child["probe"] == "P2" and child["arm"] == "ADAPTIVE":
            child["result_status"] = "FAIL"
            child["material_false_negative_count"] = 1
            break

    metrics = v7.aggregate(scored)

    assert metrics["adaptive_quality_qualified"] is False
    assert v7.pilot_decision(metrics, scored) == "NOT_QUALIFIED"


def test_valid_failure_resource_cost_stays_in_per_success_numerator() -> None:
    scored = _complete_scored(adaptive_tokens=100, control_tokens=100)
    first_control = next(child for child in scored if child["arm"] == "CONTROL")
    first_control["result_status"] = "FAIL"

    metrics = v7.aggregate(scored)
    control = metrics["profiles"]["CONTROL"]

    assert control["attempt_count"] == 12
    assert control["pass_count"] == 11
    assert control["total_tokens"] == 1200
    assert control["tokens_per_success"] == pytest.approx(1200 / 11)


def test_adaptive_reroute_disqualifies_absolute_quality() -> None:
    scored = _complete_scored()
    adaptive = next(child for child in scored if child["arm"] == "ADAPTIVE")
    adaptive["reroute_observed"] = True

    metrics = v7.aggregate(scored)

    assert metrics["adaptive_quality_qualified"] is False
    assert v7.pilot_decision(metrics, scored) == "NOT_QUALIFIED"


def test_incomplete_run_cannot_produce_pilot_decision() -> None:
    scored = _complete_scored()[:-1]
    metrics = v7.aggregate(scored)

    with pytest.raises(ExecutionInvalid, match="all 24"):
        v7.pilot_decision(metrics, scored)


def test_trial_metadata_covers_each_schedule_position() -> None:
    metadata = [v7._trial_metadata(index) for index in range(len(v7.ARM_ORDER))]

    assert metadata[0] == {
        "replicate": 1,
        "sequence_index": 1,
        "within_block_index": 1,
        "trial_id": "R1-P1-ADAPTIVE",
    }
    assert metadata[-1]["replicate"] == 4
    assert metadata[-1]["sequence_index"] == 24
    assert len({item["trial_id"] for item in metadata}) == 24


def test_v7_evidence_marks_complete_quality_failure_run_valid(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scored = _complete_scored()
    scored[-1]["result_status"] = "FAIL"

    base_payload = {
        "authority": {},
        "historical_blocked_evidence_heads": [],
        "d076": {},
        "scored_children": deepcopy(scored),
        "model_evidence": {"failure_domain": "EXECUTION_VALIDITY"},
    }
    monkeypatch.setattr(
        v7,
        "_BASE_V6_EVIDENCE_PAYLOAD",
        lambda **_: deepcopy(base_payload),
    )

    payload = v7._v7_evidence_payload(
        started_at="20260911T000000Z",
        status="COMPLETED",
        terminal_classification="COMPLETED_SCORED",
        blocker=None,
        decision="ADAPTIVE_QUALITY_QUALIFIED_CONTROL_DEFICIENT",
    )

    assert payload["model_evidence"]["run_execution_validity"] == "VALID"
    assert payload["model_evidence"]["run_model_comparison_eligible"] is True
    assert payload["model_evidence"]["pilot_eligible"] is True
    assert payload["model_evidence"]["failure_domain"] is None
    assert payload["model_evidence"]["scored_child_quality_eligible_count"] == 24
    assert payload["model_evidence"]["scored_child_efficiency_eligible_count"] == 23
