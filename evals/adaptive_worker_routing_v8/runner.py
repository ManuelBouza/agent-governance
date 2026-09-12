"""T063 v8 adapter: v7 replication plus hardened exact-child persistence barrier."""

from __future__ import annotations

import ast
import json
import sys
import time
from pathlib import Path
from typing import Any

from evals.adaptive_worker_routing_v3 import config as base_config
from evals.adaptive_worker_routing_v3 import runner as base_runner
from evals.adaptive_worker_routing_v3.app_server import AppServerError
from evals.adaptive_worker_routing_v3.config import MeasurementSurfaceBlocked
from evals.adaptive_worker_routing_v4 import runner as v4
from evals.adaptive_worker_routing_v7 import runner as v7

EVIDENCE_BRANCH = "test/t063-adaptive-worker-routing-requalification-v8"
TELEMETRY_DEFAULT = Path("handoffs/T063-adaptive-worker-routing-telemetry-v8.json")
HANDOFF_DEFAULT = Path("handoffs/T063-executor-handoff-v8.json")
V7_TERMINAL_HEAD = "58e396c126e363428544b163cb2aa8c7e1ac8ed6"
HISTORICAL_EVIDENCE_HEADS = (*v7.HISTORICAL_EVIDENCE_HEADS, V7_TERMINAL_HEAD)
_BASE_V7_EVIDENCE_PAYLOAD = v7._v7_evidence_payload
_RESUME_ERROR_PREFIX = "thread/resume failed: "


def _represented_resume_error(exc: BaseException) -> dict[str, Any] | None:
    """Recover the represented JSON-RPC error mapping from the v3 flattened exception."""
    text = str(exc)
    if not text.startswith(_RESUME_ERROR_PREFIX):
        return None
    represented = text[len(_RESUME_ERROR_PREFIX) :]
    try:
        payload = ast.literal_eval(represented)
    except (SyntaxError, ValueError):
        return None
    if not isinstance(payload, dict):
        return None
    return payload


def _transient_resume_error_class(exc: BaseException, child_id: str) -> str | None:
    if v4._is_empty_rollout_resume_error(exc):
        return "EMPTY_ROLLOUT"

    payload = _represented_resume_error(exc)
    if payload is None:
        return None

    code = payload.get("code")
    message = payload.get("message")
    expected = f"no rollout found for thread id {child_id}"
    if type(code) is not int or code != -32600:
        return None
    if not isinstance(message, str) or message != expected:
        return None
    return "ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD"


class V8AppServerClient(v4.V4AppServerClient):
    """V4-compatible client with one shared budget for two persistence phases."""

    def request(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        *,
        timeout: float = 30.0,
    ) -> dict[str, Any]:
        if method != "thread/resume":
            return super().request(method, params, timeout=timeout)

        child_id = params.get("threadId") if isinstance(params, dict) else None
        if not isinstance(child_id, str):
            return v4.BaseAppServerClient.request(self, method, params, timeout=timeout)

        parent_id = self._v4_parent_thread_id
        if parent_id is None:
            raise MeasurementSurfaceBlocked(
                "child reattachment has no exact explicitly-started parent identity"
            )
        v4._CHILD_ATTEMPT_IDS.add(child_id)
        parent_residency_rechecks = 0
        transient_classes: list[str] = []

        for attempt in range(1, v4.RESUME_MAX_ATTEMPTS + 1):
            if attempt > 1:
                time.sleep(v4.RESUME_RETRY_DELAY_SECONDS)
                parent_residency_rechecks += 1
                if parent_id not in self._loaded_ids_via_base_request():
                    audit = {
                        "child_id": child_id,
                        "parent_id": parent_id,
                        "status": "PARENT_LOST",
                        "attempt_count": attempt - 1,
                        "retry_count": attempt - 2,
                        "transient_error_class": (
                            transient_classes[-1] if transient_classes else None
                        ),
                        "transient_error_classes": list(transient_classes),
                        "shared_attempt_budget_max": v4.RESUME_MAX_ATTEMPTS,
                        "retry_delay_seconds": v4.RESUME_RETRY_DELAY_SECONDS,
                        "parent_residency_rechecks": parent_residency_rechecks,
                        "same_child_reused": True,
                        "new_provider_turn_created": False,
                    }
                    v4._REATTACHMENT_AUDIT.append(audit)
                    raise MeasurementSurfaceBlocked(
                        "parent lost residency immediately before same-child reattach retry"
                    )

            try:
                result = v4.BaseAppServerClient.request(
                    self, method, params, timeout=timeout
                )
            except AppServerError as exc:
                transient_class = _transient_resume_error_class(exc, child_id)
                if transient_class is None:
                    raise
                transient_classes.append(transient_class)
                if attempt >= v4.RESUME_MAX_ATTEMPTS:
                    audit = {
                        "child_id": child_id,
                        "parent_id": parent_id,
                        "status": "EXHAUSTED",
                        "attempt_count": attempt,
                        "retry_count": attempt - 1,
                        "transient_error_class": transient_classes[-1],
                        "transient_error_classes": list(transient_classes),
                        "shared_attempt_budget_max": v4.RESUME_MAX_ATTEMPTS,
                        "retry_delay_seconds": v4.RESUME_RETRY_DELAY_SECONDS,
                        "parent_residency_rechecks": parent_residency_rechecks,
                        "same_child_reused": True,
                        "new_provider_turn_created": False,
                    }
                    v4._REATTACHMENT_AUDIT.append(audit)
                    raise MeasurementSurfaceBlocked(
                        "same-child thread/resume persistence barrier exhausted after "
                        f"{v4.RESUME_MAX_ATTEMPTS} total attempts"
                    ) from exc
                continue

            receipt = {
                "child_id": child_id,
                "parent_id": parent_id,
                "status": "PASS",
                "attempt_count": attempt,
                "retry_count": attempt - 1,
                "transient_error_class": (
                    transient_classes[-1] if transient_classes else None
                ),
                "transient_error_classes": list(transient_classes),
                "shared_attempt_budget_max": v4.RESUME_MAX_ATTEMPTS,
                "retry_delay_seconds": v4.RESUME_RETRY_DELAY_SECONDS,
                "total_retry_wait_seconds": round(
                    (attempt - 1) * v4.RESUME_RETRY_DELAY_SECONDS, 3
                ),
                "parent_residency_rechecks": parent_residency_rechecks,
                "same_child_reused": True,
                "new_provider_turn_created": False,
            }
            self._v4_reattachment_receipts[child_id] = receipt
            v4._REATTACHMENT_AUDIT.append(dict(receipt))
            return result

        raise AssertionError("unreachable child reattachment loop")


def _v8_evidence_payload(**kwargs: Any) -> dict[str, Any]:
    payload = _BASE_V7_EVIDENCE_PAYLOAD(**kwargs)
    started_at = kwargs["started_at"]
    payload["run_id"] = f"T063-v8-{started_at}"
    payload["authority"]["evidence_branch"] = EVIDENCE_BRANCH
    payload["authority"]["launch_authority_review"] = "docs/reviews/T063-R19.md"
    payload["authority"]["persistence_adapter_research"] = (
        "docs/research/R025-T063-V8-REATTACH-CLASSIFIER-HARDENING.md"
    )
    payload["historical_evidence_heads"] = list(HISTORICAL_EVIDENCE_HEADS)
    payload["historical_blocked_evidence_heads"] = list(HISTORICAL_EVIDENCE_HEADS)
    payload["receipt_strategy"]["child_reattachment"] = {
        "method": "same-child bounded two-condition thread/resume persistence barrier",
        "retry_conditions": [
            "EMPTY_ROLLOUT",
            "ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD",
        ],
        "rollout_not_found_structural_requirements": {
            "json_rpc_code": -32600,
            "message": "no rollout found for thread id <exact child id>",
            "exact_child_id_required": True,
            "safe_literal_parse_required": True,
        },
        "max_total_attempts_shared_across_conditions": v4.RESUME_MAX_ATTEMPTS,
        "retry_delay_seconds": v4.RESUME_RETRY_DELAY_SECONDS,
        "parent_residency_rechecked_immediately_before_each_retry": True,
        "new_child_or_provider_turn_on_retry": False,
    }
    payload["d076"]["v8_persistence_adapter_materialized_by_orchestrator"] = True
    payload["d076"]["v8_structured_classifier_hardening_materialized_by_orchestrator"] = True
    return payload


def _install_adapter() -> None:
    v7._install_adapter()
    base_config.EVIDENCE_BRANCH = EVIDENCE_BRANCH
    base_config.HISTORICAL_BLOCKED_HEADS = HISTORICAL_EVIDENCE_HEADS
    base_runner.EVIDENCE_BRANCH = EVIDENCE_BRANCH
    base_runner.HISTORICAL_BLOCKED_HEADS = HISTORICAL_EVIDENCE_HEADS
    base_runner.TELEMETRY_DEFAULT = TELEMETRY_DEFAULT
    base_runner.HANDOFF_DEFAULT = HANDOFF_DEFAULT
    base_runner.AppServerClient = V8AppServerClient
    base_runner.evidence_payload = _v8_evidence_payload


def _argument_path(argv: list[str], flag: str, default: Path) -> Path:
    if flag in argv:
        index = argv.index(flag)
        if index + 1 < len(argv):
            return Path(argv[index + 1])
    return default


def _copy_v8_evidence_to_handoff(argv: list[str]) -> None:
    repo = _argument_path(argv, "--repo", Path.cwd()).resolve()
    telemetry = _argument_path(argv, "--telemetry", TELEMETRY_DEFAULT)
    handoff = _argument_path(argv, "--handoff", HANDOFF_DEFAULT)
    telemetry = telemetry if telemetry.is_absolute() else repo / telemetry
    handoff = handoff if handoff.is_absolute() else repo / handoff
    if not telemetry.exists() or not handoff.exists():
        return
    telemetry_payload = json.loads(telemetry.read_text(encoding="utf-8"))
    handoff_payload = json.loads(handoff.read_text(encoding="utf-8"))
    for key in (
        "model_evidence",
        "replication",
        "adapter_reattachment_audit",
        "receipt_strategy",
        "historical_evidence_heads",
    ):
        handoff_payload[key] = telemetry_payload.get(key)
    handoff.write_text(
        json.dumps(handoff_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    _install_adapter()
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    result = base_runner.main(effective_argv)
    if "run" in effective_argv:
        _copy_v8_evidence_to_handoff(effective_argv)
    return result
