"""T063 v4 adapter for the v3 harness.

V4 preserves the v3 experiment, oracles, task messages, profile matrix and
scoring. It adds one bounded persistence barrier around reattaching the exact
child after ``subAgentActivity(kind=Started)``. Codex 0.153.4 can emit that
public activity before the first rollout JSONL metadata line is durable; an
immediate ``thread/resume`` can therefore fail with an empty-rollout error even
though the same child is already running.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from evals.adaptive_worker_routing_v3 import config as base_config
from evals.adaptive_worker_routing_v3 import measurement as base_measurement
from evals.adaptive_worker_routing_v3 import runner as base_runner
from evals.adaptive_worker_routing_v3.app_server import (
    AppServerClient as BaseAppServerClient,
)
from evals.adaptive_worker_routing_v3.app_server import AppServerError
from evals.adaptive_worker_routing_v3.config import MeasurementSurfaceBlocked

EVIDENCE_BRANCH = "test/t063-adaptive-worker-routing-requalification-v4"
TELEMETRY_DEFAULT = Path("handoffs/T063-adaptive-worker-routing-telemetry-v4.json")
HANDOFF_DEFAULT = Path("handoffs/T063-executor-handoff-v4.json")
V3_TERMINAL_HEAD = "746519abc6f159e959120f68d5c9f920d88d5797"
HISTORICAL_BLOCKED_HEADS = (
    *base_config.HISTORICAL_BLOCKED_HEADS,
    V3_TERMINAL_HEAD,
)
RESUME_MAX_ATTEMPTS = 10
RESUME_RETRY_DELAY_SECONDS = 0.2

_EMPTY_ROLLOUT_MARKERS = (
    "thread/resume failed:",
    "thread-store error",
    "failed to read session metadata",
    "rollout at",
    "is empty",
)

_BASE_EXECUTE_ARM = base_measurement.execute_arm
_BASE_EVIDENCE_PAYLOAD = base_runner.evidence_payload
_PARENT_TURN_IDS: set[str] = set()
_CHILD_ATTEMPT_IDS: set[str] = set()
_REATTACHMENT_AUDIT: list[dict[str, Any]] = []


def _is_empty_rollout_resume_error(exc: BaseException) -> bool:
    text = str(exc).lower()
    return all(marker in text for marker in _EMPTY_ROLLOUT_MARKERS)


class V4AppServerClient(BaseAppServerClient):
    """App Server client with a narrow same-child empty-rollout retry barrier."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._v4_parent_thread_id: str | None = None
        self._v4_reattachment_receipts: dict[str, dict[str, Any]] = {}

    def _loaded_ids_via_base_request(self) -> set[str]:
        ids: set[str] = set()
        cursor: str | None = None
        while True:
            params: dict[str, Any] = {}
            if cursor is not None:
                params["cursor"] = cursor
            response = super().request("thread/loaded/list", params)
            data = response.get("data")
            if not isinstance(data, list):
                raise MeasurementSurfaceBlocked(
                    "thread/loaded/list unavailable during child reattach retry"
                )
            ids.update(item for item in data if isinstance(item, str))
            next_cursor = response.get("nextCursor")
            if not isinstance(next_cursor, str) or not next_cursor:
                return ids
            cursor = next_cursor

    def request(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        *,
        timeout: float = 30.0,
    ) -> dict[str, Any]:
        if method != "thread/resume":
            result = super().request(method, params, timeout=timeout)
            if method == "thread/start":
                thread = result.get("thread")
                if isinstance(thread, dict) and isinstance(thread.get("id"), str):
                    self._v4_parent_thread_id = thread["id"]
            elif method == "turn/start":
                turn = result.get("turn")
                if isinstance(turn, dict) and isinstance(turn.get("id"), str):
                    _PARENT_TURN_IDS.add(turn["id"])
            return result

        child_id = params.get("threadId") if isinstance(params, dict) else None
        if not isinstance(child_id, str):
            return super().request(method, params, timeout=timeout)
        parent_id = self._v4_parent_thread_id
        if parent_id is None:
            raise MeasurementSurfaceBlocked(
                "child reattachment has no exact explicitly-started parent identity"
            )
        _CHILD_ATTEMPT_IDS.add(child_id)
        parent_residency_rechecks = 0

        for attempt in range(1, RESUME_MAX_ATTEMPTS + 1):
            if attempt > 1:
                time.sleep(RESUME_RETRY_DELAY_SECONDS)
                parent_residency_rechecks += 1
                if parent_id not in self._loaded_ids_via_base_request():
                    audit = {
                        "child_id": child_id,
                        "parent_id": parent_id,
                        "status": "PARENT_LOST",
                        "attempt_count": attempt - 1,
                        "retry_count": attempt - 2,
                        "transient_error_class": "EMPTY_ROLLOUT",
                        "retry_delay_seconds": RESUME_RETRY_DELAY_SECONDS,
                        "parent_residency_rechecks": parent_residency_rechecks,
                        "same_child_reused": True,
                        "new_provider_turn_created": False,
                    }
                    _REATTACHMENT_AUDIT.append(audit)
                    raise MeasurementSurfaceBlocked(
                        "parent lost residency immediately before same-child reattach retry"
                    )

            try:
                result = super().request(method, params, timeout=timeout)
            except AppServerError as exc:
                if not _is_empty_rollout_resume_error(exc):
                    raise
                if attempt >= RESUME_MAX_ATTEMPTS:
                    audit = {
                        "child_id": child_id,
                        "parent_id": parent_id,
                        "status": "EXHAUSTED",
                        "attempt_count": attempt,
                        "retry_count": attempt - 1,
                        "transient_error_class": "EMPTY_ROLLOUT",
                        "retry_delay_seconds": RESUME_RETRY_DELAY_SECONDS,
                        "parent_residency_rechecks": parent_residency_rechecks,
                        "same_child_reused": True,
                        "new_provider_turn_created": False,
                    }
                    _REATTACHMENT_AUDIT.append(audit)
                    raise MeasurementSurfaceBlocked(
                        "same-child thread/resume persistence barrier exhausted after "
                        f"{RESUME_MAX_ATTEMPTS} attempts"
                    ) from exc
                continue

            receipt = {
                "child_id": child_id,
                "parent_id": parent_id,
                "status": "PASS",
                "attempt_count": attempt,
                "retry_count": attempt - 1,
                "transient_error_class": "EMPTY_ROLLOUT" if attempt > 1 else None,
                "retry_delay_seconds": RESUME_RETRY_DELAY_SECONDS,
                "total_retry_wait_seconds": round(
                    (attempt - 1) * RESUME_RETRY_DELAY_SECONDS, 3
                ),
                "parent_residency_rechecks": parent_residency_rechecks,
                "same_child_reused": True,
                "new_provider_turn_created": False,
            }
            self._v4_reattachment_receipts[child_id] = receipt
            _REATTACHMENT_AUDIT.append(dict(receipt))
            return result

        raise AssertionError("unreachable child reattachment loop")

    def reattachment_receipt(self, child_id: str) -> dict[str, Any] | None:
        receipt = self._v4_reattachment_receipts.get(child_id)
        return None if receipt is None else dict(receipt)


def _v4_execute_arm(client: BaseAppServerClient, **kwargs: Any) -> dict[str, Any]:
    snapshot = _BASE_EXECUTE_ARM(client, **kwargs)
    if not isinstance(client, V4AppServerClient):
        raise MeasurementSurfaceBlocked("T063 v4 scored arm did not use V4AppServerClient")
    child_id = snapshot.get("child_id")
    if not isinstance(child_id, str):
        raise MeasurementSurfaceBlocked("T063 v4 child identity unavailable after arm")
    receipt = client.reattachment_receipt(child_id)
    if receipt is None:
        raise MeasurementSurfaceBlocked("T063 v4 child reattachment receipt unavailable")
    snapshot["child_reattachment_receipt"] = receipt
    snapshot["measurement_adapter_retry_count"] = receipt["retry_count"]
    return snapshot


def _v4_evidence_payload(**kwargs: Any) -> dict[str, Any]:
    payload = _BASE_EVIDENCE_PAYLOAD(**kwargs)
    started_at = kwargs["started_at"]
    payload["run_id"] = f"T063-v4-{started_at}"
    authority = payload["authority"]
    authority["evidence_branch"] = EVIDENCE_BRANCH
    authority["launch_authority_review"] = "docs/reviews/T063-R7.md"
    authority["adapter_research"] = (
        "docs/research/R022-T063-V3-EMPTY-ROLLOUT-REATTACH-RACE.md"
    )
    version = payload["version_sensitive_revalidation"]
    version["disposition"] = "PIN_RETAINED"
    version["current_main_same_resume_path_reviewed"] = True
    payload["receipt_strategy"]["child_reattachment"] = {
        "method": "same-child bounded thread/resume persistence barrier",
        "retry_only_on": "exact empty-rollout thread-store error",
        "max_attempts": RESUME_MAX_ATTEMPTS,
        "retry_delay_seconds": RESUME_RETRY_DELAY_SECONDS,
        "parent_residency_rechecked_immediately_before_each_retry": True,
        "new_child_or_provider_turn_on_retry": False,
    }
    payload["historical_blocked_evidence_heads"] = list(HISTORICAL_BLOCKED_HEADS)
    payload["provider_execution"]["scored_parent_turns"] = len(_PARENT_TURN_IDS)
    payload["provider_execution"]["scored_child_attempts"] = len(_CHILD_ATTEMPT_IDS)
    payload["provider_execution"]["reattachment_rpc_retries"] = sum(
        max(int(item.get("retry_count", 0)), 0) for item in _REATTACHMENT_AUDIT
    )
    payload["adapter_reattachment_audit"] = [dict(item) for item in _REATTACHMENT_AUDIT]
    payload["d076"]["v4_adapter_materialized_by_orchestrator"] = True
    payload["d076"]["v3_repaired_harness_reused_byte_for_byte"] = True
    for item in payload["d076"].get("candidate_runtime_artifacts", []):
        if isinstance(item, dict) and item.get("label") == "P3 profile fixture":
            item["created_by"] = "published T063 v3 harness reused by v4 adapter"
    return payload


def _install_adapter() -> None:
    _PARENT_TURN_IDS.clear()
    _CHILD_ATTEMPT_IDS.clear()
    _REATTACHMENT_AUDIT.clear()
    base_config.EVIDENCE_BRANCH = EVIDENCE_BRANCH
    base_config.HISTORICAL_BLOCKED_HEADS = HISTORICAL_BLOCKED_HEADS
    base_runner.EVIDENCE_BRANCH = EVIDENCE_BRANCH
    base_runner.HISTORICAL_BLOCKED_HEADS = HISTORICAL_BLOCKED_HEADS
    base_runner.TELEMETRY_DEFAULT = TELEMETRY_DEFAULT
    base_runner.HANDOFF_DEFAULT = HANDOFF_DEFAULT
    base_runner.AppServerClient = V4AppServerClient
    base_runner.execute_arm = _v4_execute_arm
    base_runner.evidence_payload = _v4_evidence_payload


def main(argv: list[str] | None = None) -> int:
    _install_adapter()
    return base_runner.main(argv)
