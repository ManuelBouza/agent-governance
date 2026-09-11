"""T063 v6 adapter: v5 evidence semantics plus live parent-surface validation."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from evals.adaptive_worker_routing_v3 import config as base_config
from evals.adaptive_worker_routing_v3 import measurement as base_measurement
from evals.adaptive_worker_routing_v3 import runner as base_runner
from evals.adaptive_worker_routing_v3.app_server import AppServerClient
from evals.adaptive_worker_routing_v5 import runner as v5

EVIDENCE_BRANCH = "test/t063-adaptive-worker-routing-requalification-v6"
TELEMETRY_DEFAULT = Path("handoffs/T063-adaptive-worker-routing-telemetry-v6.json")
HANDOFF_DEFAULT = Path("handoffs/T063-executor-handoff-v6.json")
V5_TERMINAL_HEAD = "3f9830a65a152ad595653961205e0ca52b9c5ccc"
HISTORICAL_BLOCKED_HEADS = (*v5.HISTORICAL_BLOCKED_HEADS, V5_TERMINAL_HEAD)

_BASE_WAIT_FOR_SPAWN = base_measurement._wait_for_spawn
_BASE_V5_EVIDENCE_PAYLOAD = v5._v5_evidence_payload

_FORBIDDEN_PARENT_ITEM_TYPES = {
    "commandExecution",
    "fileChange",
    "mcpToolCall",
    "dynamicToolCall",
    "webSearch",
    "imageView",
    "imageGeneration",
}


@dataclass(frozen=True)
class _ParentSurfaceContext:
    client: AppServerClient
    parent_id: str
    parent_turn_id: str
    start_index: int
    spawn_item_id: str


_PARENT_CONTEXT_BY_CHILD: dict[str, _ParentSurfaceContext] = {}


def _normalized_agent_path(item: dict[str, Any]) -> str | None:
    path = item.get("agentPath")
    if not isinstance(path, str):
        return None
    return path.rstrip("/").split("/")[-1]


def _wait_for_spawn_v6(
    client: AppServerClient,
    parent_id: str,
    parent_turn_id: str,
    expected_task_name: str,
    start_index: int,
) -> tuple[int, str, dict[str, Any]]:
    index, child_id, item = _BASE_WAIT_FOR_SPAWN(
        client,
        parent_id,
        parent_turn_id,
        expected_task_name,
        start_index,
    )
    item_id = item.get("id")
    if not isinstance(item_id, str) or not item_id:
        raise base_config.ExecutionInvalid("public spawn activity item id unavailable")
    _PARENT_CONTEXT_BY_CHILD[child_id] = _ParentSurfaceContext(
        client=client,
        parent_id=parent_id,
        parent_turn_id=parent_turn_id,
        start_index=start_index,
        spawn_item_id=item_id,
    )
    return index, child_id, item


def _live_parent_items(context: _ParentSurfaceContext) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for notification in context.client.notifications()[context.start_index :]:
        if notification.method not in {"item/started", "item/completed"}:
            continue
        params = notification.params
        if (
            params.get("threadId") != context.parent_id
            or params.get("turnId") != context.parent_turn_id
        ):
            continue
        item = params.get("item")
        if isinstance(item, dict):
            items.append(item)
    return items


def _validate_started_activities(
    items: list[dict[str, Any]],
    *,
    context: _ParentSurfaceContext,
    child_id: str,
    expected_task_name: str,
) -> None:
    unique: dict[str, dict[str, Any]] = {}
    for item in items:
        if (
            item.get("type") != "subAgentActivity"
            or not isinstance(item.get("kind"), str)
            or item["kind"].lower() != "started"
        ):
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            raise base_config.ExecutionInvalid("public Started subAgentActivity item id unavailable")
        prior = unique.get(item_id)
        if prior is not None:
            fields = ("agentThreadId", "agentPath", "kind")
            if any(prior.get(field) != item.get(field) for field in fields):
                raise base_config.ExecutionInvalid(
                    f"public Started subAgentActivity changed across notifications: {item_id}"
                )
            continue
        unique[item_id] = item

    matching = [
        item
        for item in unique.values()
        if item.get("agentThreadId") == child_id
        and _normalized_agent_path(item) == expected_task_name
    ]
    if len(unique) != 1 or len(matching) != 1:
        raise base_config.ExecutionInvalid(
            "live parent spawn activity count mismatch: "
            f"unique_total={len(unique)}, matching={len(matching)}"
        )
    if context.spawn_item_id not in unique:
        raise base_config.ExecutionInvalid("correlated spawn activity missing from live parent window")


def _forbidden_parent_item_types(items: list[dict[str, Any]]) -> list[str]:
    return sorted(
        {
            item_type
            for item in items
            if isinstance((item_type := item.get("type")), str)
            and item_type in _FORBIDDEN_PARENT_ITEM_TYPES
        }
    )


def _validate_parent_surface_v6(
    parent_turn: dict[str, Any], *, child_id: str, expected_task_name: str
) -> None:
    context = _PARENT_CONTEXT_BY_CHILD.pop(child_id, None)
    if context is None:
        raise base_config.ExecutionInvalid("live parent surface context unavailable")

    live_items = _live_parent_items(context)
    _validate_started_activities(
        live_items,
        context=context,
        child_id=child_id,
        expected_task_name=expected_task_name,
    )
    live_forbidden = _forbidden_parent_item_types(live_items)
    if live_forbidden:
        raise base_config.ExecutionInvalid(
            f"measurement parent used forbidden live item types: {live_forbidden}"
        )

    completed_items = parent_turn.get("items")
    if not isinstance(completed_items, list):
        raise base_config.ExecutionInvalid("parent completed turn items unavailable")
    completed_dict_items = [item for item in completed_items if isinstance(item, dict)]
    completed_forbidden = _forbidden_parent_item_types(completed_dict_items)
    if completed_forbidden:
        raise base_config.ExecutionInvalid(
            f"measurement parent used forbidden completed item types: {completed_forbidden}"
        )

    completed_started = [
        item
        for item in completed_dict_items
        if item.get("type") == "subAgentActivity"
        and isinstance(item.get("kind"), str)
        and item["kind"].lower() == "started"
    ]
    contradictory = [
        item
        for item in completed_started
        if item.get("agentThreadId") != child_id
        or _normalized_agent_path(item) != expected_task_name
    ]
    if contradictory:
        raise base_config.ExecutionInvalid(
            "completed parent snapshot contradicts live spawn correlation"
        )

    final = base_measurement._final_agent_text(parent_turn).strip()
    if final != "PARENT_SPAWNED":
        raise base_config.ExecutionInvalid(f"measurement parent final response drift: {final!r}")


def _v6_evidence_payload(**kwargs: Any) -> dict[str, Any]:
    payload = _BASE_V5_EVIDENCE_PAYLOAD(**kwargs)
    started_at = kwargs["started_at"]
    payload["run_id"] = f"T063-v6-{started_at}"
    payload["authority"]["evidence_branch"] = EVIDENCE_BRANCH
    payload["authority"]["launch_authority_review"] = "docs/reviews/T063-R11.md"
    payload["historical_blocked_evidence_heads"] = list(HISTORICAL_BLOCKED_HEADS)
    payload["d076"]["v6_live_parent_surface_materialized_by_orchestrator"] = True
    return payload


def _install_adapter() -> None:
    v5._install_adapter()
    _PARENT_CONTEXT_BY_CHILD.clear()
    base_config.EVIDENCE_BRANCH = EVIDENCE_BRANCH
    base_config.HISTORICAL_BLOCKED_HEADS = HISTORICAL_BLOCKED_HEADS
    base_runner.EVIDENCE_BRANCH = EVIDENCE_BRANCH
    base_runner.HISTORICAL_BLOCKED_HEADS = HISTORICAL_BLOCKED_HEADS
    base_runner.TELEMETRY_DEFAULT = TELEMETRY_DEFAULT
    base_runner.HANDOFF_DEFAULT = HANDOFF_DEFAULT
    base_runner.evidence_payload = _v6_evidence_payload
    base_measurement._wait_for_spawn = _wait_for_spawn_v6
    base_measurement._validate_parent_surface = _validate_parent_surface_v6


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
        json.dumps(handoff_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    _install_adapter()
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    result = base_runner.main(effective_argv)
    if "run" in effective_argv:
        _copy_model_evidence_to_handoff(effective_argv)
    return result
