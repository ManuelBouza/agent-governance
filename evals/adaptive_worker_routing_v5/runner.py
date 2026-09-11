"""T063 v5 adapter: repaired v4 reattach barrier plus model-evidence attribution."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from evals.adaptive_worker_routing_v3 import config as base_config
from evals.adaptive_worker_routing_v3 import runner as base_runner
from evals.adaptive_worker_routing_v4 import runner as v4

EVIDENCE_BRANCH = "test/t063-adaptive-worker-routing-requalification-v5"
TELEMETRY_DEFAULT = Path("handoffs/T063-adaptive-worker-routing-telemetry-v5.json")
HANDOFF_DEFAULT = Path("handoffs/T063-executor-handoff-v5.json")
V4_TERMINAL_HEAD = "4135a13ce8daa4f6b1fcabe45063364fbbdd16f1"
HISTORICAL_BLOCKED_HEADS = (*v4.HISTORICAL_BLOCKED_HEADS, V4_TERMINAL_HEAD)
_BASE_V4_EVIDENCE_PAYLOAD = v4._v4_evidence_payload


def _failure_domain(
    terminal_classification: str, blocker: dict[str, Any] | None
) -> str | None:
    if terminal_classification == "COMPLETED_SCORED":
        return None
    if terminal_classification == "BLOCKED_PROFILE_RESOLUTION":
        return "PROFILE_RESOLUTION"
    if terminal_classification == "BLOCKED_MEASUREMENT_SURFACE":
        return "MEASUREMENT_SURFACE"
    if terminal_classification == "BLOCKED_EXECUTION_INVALID":
        message = str((blocker or {}).get("message", "")).lower()
        if all(
            marker in message
            for marker in ("thread/resume failed:", "thread-store", "rollout at", "is empty")
        ):
            return "MEASUREMENT_ADAPTER"
        return "EXECUTION_VALIDITY"
    return "UNCLASSIFIED_EXECUTION"


def _annotate_model_evidence(
    *,
    payload: dict[str, Any],
    status: str,
    terminal_classification: str,
    blocker: dict[str, Any] | None,
    decision: str | None,
) -> dict[str, Any]:
    scored = payload.get("scored_children", [])
    if not isinstance(scored, list):
        scored = []
    quality_eligible = 0
    efficiency_eligible = 0
    for child in scored:
        if not isinstance(child, dict):
            continue
        passed = child.get("result_status") == "PASS"
        child["execution_validity"] = "VALID"
        child["failure_domain"] = None if passed else "WORKER_QUALITY"
        child["model_quality_eligible"] = True
        child["model_efficiency_eligible"] = passed
        quality_eligible += 1
        efficiency_eligible += int(passed)

    complete_clean_run = status == "COMPLETED" and len(scored) == 6
    payload["model_evidence"] = {
        "run_execution_validity": "VALID" if complete_clean_run else "INVALID",
        "run_model_comparison_eligible": complete_clean_run,
        "pilot_eligible": complete_clean_run and decision is not None,
        "failure_domain": _failure_domain(terminal_classification, blocker),
        "scored_child_quality_eligible_count": quality_eligible,
        "scored_child_efficiency_eligible_count": efficiency_eligible,
        "unscored_child_attempts_count_as_model_quality": False,
        "root_model_failure_attributed": False,
    }
    return payload


def _v5_evidence_payload(**kwargs: Any) -> dict[str, Any]:
    payload = _BASE_V4_EVIDENCE_PAYLOAD(**kwargs)
    started_at = kwargs["started_at"]
    payload["run_id"] = f"T063-v5-{started_at}"
    payload["authority"]["evidence_branch"] = EVIDENCE_BRANCH
    payload["authority"]["launch_authority_review"] = "docs/reviews/T063-R9.md"
    payload["historical_blocked_evidence_heads"] = list(HISTORICAL_BLOCKED_HEADS)
    payload["d076"]["v5_model_evidence_taxonomy_materialized_by_orchestrator"] = True
    return _annotate_model_evidence(
        payload=payload,
        status=kwargs["status"],
        terminal_classification=kwargs["terminal_classification"],
        blocker=kwargs["blocker"],
        decision=kwargs["decision"],
    )


def _argument_path(argv: list[str], flag: str, default: Path) -> Path:
    if flag in argv:
        index = argv.index(flag)
        if index + 1 < len(argv):
            return Path(argv[index + 1])
    return default


def _copy_model_evidence_to_handoff(argv: list[str]) -> None:
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
    handoff.write_text(
        json.dumps(handoff_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _install_adapter() -> None:
    v4._install_adapter()
    base_config.EVIDENCE_BRANCH = EVIDENCE_BRANCH
    base_config.HISTORICAL_BLOCKED_HEADS = HISTORICAL_BLOCKED_HEADS
    base_runner.EVIDENCE_BRANCH = EVIDENCE_BRANCH
    base_runner.HISTORICAL_BLOCKED_HEADS = HISTORICAL_BLOCKED_HEADS
    base_runner.TELEMETRY_DEFAULT = TELEMETRY_DEFAULT
    base_runner.HANDOFF_DEFAULT = HANDOFF_DEFAULT
    base_runner.evidence_payload = _v5_evidence_payload


def main(argv: list[str] | None = None) -> int:
    _install_adapter()
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    result = base_runner.main(effective_argv)
    if "run" in effective_argv:
        _copy_model_evidence_to_handoff(effective_argv)
    return result
