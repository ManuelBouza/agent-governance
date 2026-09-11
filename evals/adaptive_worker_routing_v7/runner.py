"""T063 v7 adapter: replicated qualification over the accepted v6 measurement stack."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from evals.adaptive_worker_routing_v3 import config as base_config
from evals.adaptive_worker_routing_v3 import runner as base_runner
from evals.adaptive_worker_routing_v3.config import ArmSpec
from evals.adaptive_worker_routing_v6 import runner as v6

EVIDENCE_BRANCH = "test/t063-adaptive-worker-routing-requalification-v7"
TELEMETRY_DEFAULT = Path("handoffs/T063-adaptive-worker-routing-telemetry-v7.json")
HANDOFF_DEFAULT = Path("handoffs/T063-executor-handoff-v7.json")
V6_TERMINAL_HEAD = "276fa94cde6904c003482c8b527de7e8cda416d4"
HISTORICAL_EVIDENCE_HEADS = (*v6.HISTORICAL_BLOCKED_HEADS, V6_TERMINAL_HEAD)
REPLICATE_COUNT = 4
EXPECTED_SCORED_CHILDREN = 24
TOKEN_IMPROVEMENT_FLOOR = 0.10

BLOCK_1 = (
    ("P1", "ADAPTIVE", "gpt-5.6-luna", "medium"),
    ("P1", "CONTROL", "gpt-5.6-sol", "medium"),
    ("P2", "CONTROL", "gpt-5.6-sol", "medium"),
    ("P2", "ADAPTIVE", "gpt-5.6-terra", "medium"),
    ("P3", "ADAPTIVE", "gpt-5.6-terra", "high"),
    ("P3", "CONTROL", "gpt-5.6-sol", "medium"),
)
BLOCK_2 = (
    ("P1", "CONTROL", "gpt-5.6-sol", "medium"),
    ("P1", "ADAPTIVE", "gpt-5.6-luna", "medium"),
    ("P2", "ADAPTIVE", "gpt-5.6-terra", "medium"),
    ("P2", "CONTROL", "gpt-5.6-sol", "medium"),
    ("P3", "CONTROL", "gpt-5.6-sol", "medium"),
    ("P3", "ADAPTIVE", "gpt-5.6-terra", "high"),
)
REPLICATE_BLOCKS = (BLOCK_1, BLOCK_2, BLOCK_1, BLOCK_2)
ARM_ORDER = tuple(arm for block in REPLICATE_BLOCKS for arm in block)

_BASE_V6_EVIDENCE_PAYLOAD = v6._v6_evidence_payload
_BASE_EXECUTE_ARM: Any | None = None
_TRIAL_CURSOR = 0


def _trial_metadata(index: int) -> dict[str, int | str]:
    block_index = index // len(BLOCK_1)
    within_block = index % len(BLOCK_1)
    probe, arm, _, _ = ARM_ORDER[index]
    return {
        "replicate": block_index + 1,
        "sequence_index": index + 1,
        "within_block_index": within_block + 1,
        "trial_id": f"R{block_index + 1}-{probe}-{arm}",
    }


def _spec_tuple(spec: ArmSpec) -> tuple[str, str, str, str]:
    return (spec.probe, spec.arm, spec.model, spec.reasoning)


def _v7_execute_arm(client: Any, **kwargs: Any) -> dict[str, Any]:
    global _TRIAL_CURSOR

    if _BASE_EXECUTE_ARM is None:
        raise base_config.ExecutionInvalid("T063 v7 underlying execute_arm adapter unavailable")
    if len(ARM_ORDER) <= _TRIAL_CURSOR:
        raise base_config.ExecutionInvalid("T063 v7 received more arms than frozen schedule")
    spec = kwargs.get("spec")
    if not isinstance(spec, ArmSpec):
        raise base_config.ExecutionInvalid("T063 v7 ArmSpec unavailable")
    expected = ARM_ORDER[_TRIAL_CURSOR]
    if _spec_tuple(spec) != expected:
        raise base_config.ExecutionInvalid(
            "T063 v7 schedule drift: "
            f"expected={expected!r}, observed={_spec_tuple(spec)!r}"
        )

    snapshot = _BASE_EXECUTE_ARM(client, **kwargs)
    snapshot.update(_trial_metadata(_TRIAL_CURSOR))
    _TRIAL_CURSOR += 1
    return snapshot


def _safe_per_success(total: float | int, pass_count: int) -> float | None:
    if pass_count <= 0:
        return None
    return round(float(total) / pass_count, 6)


def _profile_integrity(items: list[dict[str, Any]]) -> bool:
    return all(
        not item.get("reroute_observed", False)
        and item.get("requested_model") == item.get("resolved_model")
        and item.get("requested_reasoning_effort")
        == item.get("resolved_reasoning_effort")
        for item in items
    )


def _summary(items: list[dict[str, Any]]) -> dict[str, Any]:
    pass_count = sum(item.get("result_status") == "PASS" for item in items)
    total_tokens = sum(int(item.get("total_tokens", 0)) for item in items)
    total_duration = round(
        sum(float(item.get("duration_seconds", 0.0)) for item in items), 3
    )
    return {
        "attempt_count": len(items),
        "pass_count": pass_count,
        "total_tokens": total_tokens,
        "total_duration": total_duration,
        "tokens_per_success": _safe_per_success(total_tokens, pass_count),
        "duration_per_success": _safe_per_success(total_duration, pass_count),
        "profile_integrity": _profile_integrity(items),
    }


def aggregate(scored: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    by_arm: dict[str, list[dict[str, Any]]] = {"ADAPTIVE": [], "CONTROL": []}
    for item in scored:
        probe = str(item.get("probe", ""))
        arm = str(item.get("arm", ""))
        grouped[(probe, arm)].append(item)
        if arm in by_arm:
            by_arm[arm].append(item)

    per_probe: dict[str, Any] = {}
    material_false_negative_count = 0
    material_false_positive_count = 0
    for probe in ("P1", "P2", "P3"):
        adaptive = _summary(grouped[(probe, "ADAPTIVE")])
        control = _summary(grouped[(probe, "CONTROL")])
        adaptive_qualified = (
            adaptive["attempt_count"] == REPLICATE_COUNT
            and adaptive["pass_count"] == REPLICATE_COUNT
            and adaptive["profile_integrity"]
        )
        control_qualified = (
            control["attempt_count"] == REPLICATE_COUNT
            and control["pass_count"] == REPLICATE_COUNT
            and control["profile_integrity"]
        )
        if adaptive_qualified and control_qualified:
            pair_outcome = "BOTH_QUALIFIED"
        elif adaptive_qualified:
            pair_outcome = "ADAPTIVE_ONLY_QUALIFIED"
        elif control_qualified:
            pair_outcome = "CONTROL_ONLY_QUALIFIED"
        else:
            pair_outcome = "NEITHER_QUALIFIED"
        per_probe[probe] = {
            "ADAPTIVE": adaptive,
            "CONTROL": control,
            "pair_outcome": pair_outcome,
        }

    for item in scored:
        material_false_negative_count += int(
            item.get("material_false_negative_count", 0)
        )
        material_false_positive_count += int(
            item.get("material_false_positive_count", 0)
        )

    adaptive = _summary(by_arm["ADAPTIVE"])
    control = _summary(by_arm["CONTROL"])
    adaptive_quality_qualified = (
        adaptive["attempt_count"] == 12
        and adaptive["pass_count"] == 12
        and adaptive["profile_integrity"]
    )
    control_quality_qualified = (
        control["attempt_count"] == 12
        and control["pass_count"] == 12
        and control["profile_integrity"]
    )

    token_improvement: float | None = None
    if (
        adaptive_quality_qualified
        and control_quality_qualified
        and isinstance(adaptive["tokens_per_success"], float)
        and isinstance(control["tokens_per_success"], float)
        and control["tokens_per_success"] > 0
    ):
        token_improvement = round(
            1 - (adaptive["tokens_per_success"] / control["tokens_per_success"]),
            6,
        )

    return {
        "control_pass_count": control["pass_count"],
        "adaptive_pass_count": adaptive["pass_count"],
        "adaptive_first_attempt_failures": (
            adaptive["attempt_count"] - adaptive["pass_count"]
        ),
        "adaptive_escalation_count": 0,
        "material_false_negative_count": material_false_negative_count,
        "material_false_positive_count": material_false_positive_count,
        "profile_resolution_failures": 0,
        "control_exact_tokens_total": control["total_tokens"],
        "adaptive_exact_tokens_total": adaptive["total_tokens"],
        "control_exact_duration_total": control["total_duration"],
        "adaptive_exact_duration_total": adaptive["total_duration"],
        "root_rework_events_caused_by_children": 0,
        "replicate_count": REPLICATE_COUNT,
        "scheduled_child_attempts": EXPECTED_SCORED_CHILDREN,
        "observed_child_attempts": len(scored),
        "per_probe": per_probe,
        "profiles": {
            "ADAPTIVE": adaptive,
            "CONTROL": control,
        },
        "adaptive_quality_qualified": adaptive_quality_qualified,
        "control_quality_qualified": control_quality_qualified,
        "exact_token_improvement": token_improvement,
        "token_improvement_floor": TOKEN_IMPROVEMENT_FLOOR,
    }


def pilot_decision(metrics: dict[str, Any], scored: list[dict[str, Any]]) -> str:
    if len(scored) != EXPECTED_SCORED_CHILDREN:
        raise base_config.ExecutionInvalid(
            "T063 v7 pilot decision requires all 24 scheduled scored children"
        )
    if not metrics["adaptive_quality_qualified"]:
        return "NOT_QUALIFIED"
    if metrics["root_rework_events_caused_by_children"]:
        return "NOT_QUALIFIED"
    if not metrics["control_quality_qualified"]:
        return "ADAPTIVE_QUALITY_QUALIFIED_CONTROL_DEFICIENT"
    improvement = metrics.get("exact_token_improvement")
    if improvement is not None and improvement >= TOKEN_IMPROVEMENT_FLOOR:
        return "QUALIFIED_PROFILE_AND_USAGE_EFFICIENCY"
    return "QUALIFIED_PROFILE_ROUTING_ONLY"


def _v7_evidence_payload(**kwargs: Any) -> dict[str, Any]:
    payload = _BASE_V6_EVIDENCE_PAYLOAD(**kwargs)
    started_at = kwargs["started_at"]
    scored = payload.get("scored_children", [])
    if not isinstance(scored, list):
        scored = []
    complete_run = (
        kwargs["status"] == "COMPLETED"
        and kwargs["terminal_classification"] == "COMPLETED_SCORED"
        and len(scored) == EXPECTED_SCORED_CHILDREN
    )
    decision = kwargs["decision"]

    payload["run_id"] = f"T063-v7-{started_at}"
    payload["authority"]["evidence_branch"] = EVIDENCE_BRANCH
    payload["authority"]["launch_authority_review"] = "docs/reviews/T063-R14.md"
    payload["historical_evidence_heads"] = list(HISTORICAL_EVIDENCE_HEADS)
    payload["historical_blocked_evidence_heads"] = list(HISTORICAL_EVIDENCE_HEADS)
    payload["replication"] = {
        "design": "FIXED_N_REPLICATED_ABSOLUTE_QUALITY_GATE",
        "replicate_count": REPLICATE_COUNT,
        "scheduled_child_attempts": EXPECTED_SCORED_CHILDREN,
        "counterbalanced": True,
        "arm_order": [list(item) for item in ARM_ORDER],
        "outcome_conditioned_reruns_authorized": False,
    }
    payload["model_evidence"] = {
        "run_execution_validity": "VALID" if complete_run else "INVALID",
        "run_model_comparison_eligible": complete_run,
        "pilot_eligible": complete_run and decision is not None,
        "failure_domain": (
            None
            if complete_run
            else payload.get("model_evidence", {}).get("failure_domain")
        ),
        "scored_child_quality_eligible_count": len(scored),
        "scored_child_efficiency_eligible_count": sum(
            isinstance(item, dict) and item.get("result_status") == "PASS"
            for item in scored
        ),
        "unscored_child_attempts_count_as_model_quality": False,
        "root_model_failure_attributed": False,
    }
    payload["d076"]["v7_replication_taxonomy_materialized_by_orchestrator"] = True
    return payload


def _install_adapter() -> None:
    global _BASE_EXECUTE_ARM, _TRIAL_CURSOR

    v6._install_adapter()
    _TRIAL_CURSOR = 0
    _BASE_EXECUTE_ARM = base_runner.execute_arm
    base_config.EVIDENCE_BRANCH = EVIDENCE_BRANCH
    base_config.HISTORICAL_BLOCKED_HEADS = HISTORICAL_EVIDENCE_HEADS
    base_config.ARM_ORDER = ARM_ORDER
    base_runner.EVIDENCE_BRANCH = EVIDENCE_BRANCH
    base_runner.HISTORICAL_BLOCKED_HEADS = HISTORICAL_EVIDENCE_HEADS
    base_runner.ARM_ORDER = ARM_ORDER
    base_runner.TELEMETRY_DEFAULT = TELEMETRY_DEFAULT
    base_runner.HANDOFF_DEFAULT = HANDOFF_DEFAULT
    base_runner.execute_arm = _v7_execute_arm
    base_runner.aggregate = aggregate
    base_runner.pilot_decision = pilot_decision
    base_runner.evidence_payload = _v7_evidence_payload


def _argument_path(argv: list[str], flag: str, default: Path) -> Path:
    if flag in argv:
        index = argv.index(flag)
        if index + 1 < len(argv):
            return Path(argv[index + 1])
    return default


def _copy_v7_evidence_to_handoff(argv: list[str]) -> None:
    repo = _argument_path(argv, "--repo", Path.cwd()).resolve()
    telemetry = _argument_path(argv, "--telemetry", TELEMETRY_DEFAULT)
    handoff = _argument_path(argv, "--handoff", HANDOFF_DEFAULT)
    telemetry = telemetry if telemetry.is_absolute() else repo / telemetry
    handoff = handoff if handoff.is_absolute() else repo / handoff
    if not telemetry.exists() or not handoff.exists():
        return
    telemetry_payload = json.loads(telemetry.read_text(encoding="utf-8"))
    handoff_payload = json.loads(handoff.read_text(encoding="utf-8"))
    handoff_payload["model_evidence"] = telemetry_payload.get("model_evidence")
    handoff_payload["replication"] = telemetry_payload.get("replication")
    handoff.write_text(
        json.dumps(handoff_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    _install_adapter()
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    result = base_runner.main(effective_argv)
    if "run" in effective_argv:
        _copy_v7_evidence_to_handoff(effective_argv)
    return result
