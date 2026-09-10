"""D063 live preflight and one-arm measured execution for T063 v2."""

from __future__ import annotations

import json
import platform
import re
import shutil
import time
from pathlib import Path
from typing import Any

from .app_server import AppServerClient, Notification
from .config import (
    FORBIDDEN_CHILD_TOOL_FRAGMENTS,
    PARENT_INSTRUCTIONS,
    REQUIRED_CODEX_VERSION,
    ROOT_MODEL,
    ROOT_REASONING,
    ArmSpec,
    ExecutionInvalid,
    MeasurementSurfaceBlocked,
    PreparedInputs,
    ProfileResolutionBlocked,
)
from .oracles import (
    parse_child_json,
    run_command,
    score_p1,
    score_p2,
    score_p3,
)


def _codex_version(codex_bin: Path, repo: Path) -> str:
    result = run_command([str(codex_bin), "--version"], cwd=repo)
    match = re.search(r"(\d+\.\d+\.\d+)", result.stdout)
    if match is None:
        raise MeasurementSurfaceBlocked(f"cannot parse Codex version: {result.stdout!r}")
    return match.group(1)


def _active_profile(payload: dict[str, Any]) -> str | None:
    active = payload.get("activePermissionProfile")
    if isinstance(active, dict) and isinstance(active.get("id"), str):
        return active["id"]
    return None


def _legacy_read_only(payload: dict[str, Any]) -> bool:
    sandbox = payload.get("sandbox")
    if isinstance(sandbox, str):
        return sandbox.lower() == "readonly"
    if isinstance(sandbox, dict):
        value = sandbox.get("type")
        return isinstance(value, str) and value.lower() == "readonly"
    return False


def _thread_id(payload: dict[str, Any]) -> str:
    thread = payload.get("thread")
    if not isinstance(thread, dict) or not isinstance(thread.get("id"), str):
        raise MeasurementSurfaceBlocked("thread id unavailable")
    return thread["id"]


def _turn_id(payload: dict[str, Any]) -> str:
    turn = payload.get("turn")
    if not isinstance(turn, dict) or not isinstance(turn.get("id"), str):
        raise MeasurementSurfaceBlocked("turn id unavailable")
    return turn["id"]


def _generate_schema(codex_bin: Path, repo: Path, runtime_root: Path) -> dict[str, Any]:
    schema_dir = runtime_root / "native-schema"
    schema_dir.mkdir()
    run_command(
        [
            str(codex_bin),
            "app-server",
            "generate-json-schema",
            "--experimental",
            "--out",
            str(schema_dir),
        ],
        cwd=repo,
        timeout=60,
    )
    corpus = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in sorted(schema_dir.rglob("*.json"))
    )
    required = (
        "activePermissionProfile",
        "runtimeWorkspaceRoots",
        "thread/loaded/list",
        "thread/tokenUsage/updated",
        "model/rerouted",
        "reasoningEffort",
        "parentThreadId",
    )
    missing = [marker for marker in required if marker not in corpus]
    shutil.rmtree(schema_dir)
    if missing:
        raise MeasurementSurfaceBlocked(f"native schema missing D063 markers: {missing}")
    return {"required_markers": list(required), "missing_markers": []}


def _collect_models(client: AppServerClient) -> dict[str, set[str]]:
    models: dict[str, set[str]] = {}
    cursor: str | None = None
    while True:
        params: dict[str, Any] = {}
        if cursor is not None:
            params["cursor"] = cursor
        response = client.request("model/list", params)
        data = response.get("data")
        if not isinstance(data, list):
            raise MeasurementSurfaceBlocked("model/list data unavailable")
        for item in data:
            if not isinstance(item, dict) or not isinstance(item.get("model"), str):
                continue
            efforts = {
                option["reasoningEffort"]
                for option in item.get("supportedReasoningEfforts", [])
                if isinstance(option, dict) and isinstance(option.get("reasoningEffort"), str)
            }
            models[item["model"]] = efforts
        next_cursor = response.get("nextCursor")
        if not isinstance(next_cursor, str) or not next_cursor:
            return models
        cursor = next_cursor


def preflight(
    client: AppServerClient,
    *,
    codex_bin: Path,
    repo: Path,
    runtime_root: Path,
    required_profiles: set[tuple[str, str]],
) -> dict[str, Any]:
    if platform.system().lower() != "windows":
        raise MeasurementSurfaceBlocked("T063 requires native Windows")
    cli_version = _codex_version(codex_bin, repo)
    if cli_version != REQUIRED_CODEX_VERSION:
        raise MeasurementSurfaceBlocked(
            f"Codex CLI mismatch: expected {REQUIRED_CODEX_VERSION}, got {cli_version}"
        )
    schema = _generate_schema(codex_bin, repo, runtime_root)
    initialized = client.initialize()
    server = initialized.get("serverInfo")
    app_server = server.get("version") if isinstance(server, dict) else None
    if app_server != REQUIRED_CODEX_VERSION:
        raise MeasurementSurfaceBlocked(
            f"App Server mismatch: expected {REQUIRED_CODEX_VERSION}, got {app_server!r}"
        )
    account = client.request("account/read", {"refreshToken": False}).get("account")
    if not isinstance(account, dict) or account.get("type") != "chatgpt":
        raise MeasurementSurfaceBlocked("auth category is not chatgpt")
    models = _collect_models(client)
    for model, effort in required_profiles:
        if model not in models:
            raise ProfileResolutionBlocked(f"required model absent from model/list: {model}")
        if models[model] and effort not in models[model]:
            raise ProfileResolutionBlocked(f"{model} does not expose reasoning effort {effort}")

    probe_parent = client.request(
        "thread/start",
        {
            "model": ROOT_MODEL,
            "cwd": str(repo),
            "permissions": ":read-only",
            "approvalPolicy": "never",
            "runtimeWorkspaceRoots": [str(repo)],
        },
    )
    parent_id = _thread_id(probe_parent)
    if _active_profile(probe_parent) != ":read-only" or not _legacy_read_only(probe_parent):
        raise MeasurementSurfaceBlocked("provider-free parent read-only receipt failed")
    client.request("thread/archive", {"threadId": parent_id})
    return {
        "platform": "native Windows",
        "codex_cli": cli_version,
        "app_server": app_server,
        "auth_category": "chatgpt",
        "schema": schema,
        "required_profiles": [
            {"model": model, "reasoning_effort": effort}
            for model, effort in sorted(required_profiles)
        ],
        "parent_read_only_preflight": True,
        "result": "PASS",
    }


def _spawn_item(
    notification: Notification,
    parent_id: str,
    parent_turn_id: str,
) -> dict[str, Any] | None:
    if notification.method not in {"item/started", "item/completed"}:
        return None
    params = notification.params
    if params.get("threadId") != parent_id or params.get("turnId") != parent_turn_id:
        return None
    item = params.get("item")
    if not isinstance(item, dict) or item.get("type") != "collabAgentToolCall":
        return None
    if item.get("tool") not in {"spawnAgent", "spawn_agent"}:
        return None
    receivers = item.get("receiverThreadIds")
    if isinstance(receivers, list) and len(receivers) == 1 and isinstance(receivers[0], str):
        return item
    return None


def collab_child_id(
    notification: Notification, parent_id: str, parent_turn_id: str
) -> str | None:
    item = _spawn_item(notification, parent_id, parent_turn_id)
    return None if item is None else item["receiverThreadIds"][0]


def _loaded_thread_ids(client: AppServerClient) -> set[str]:
    ids: set[str] = set()
    cursor: str | None = None
    while True:
        params: dict[str, Any] = {}
        if cursor is not None:
            params["cursor"] = cursor
        response = client.request("thread/loaded/list", params)
        data = response.get("data")
        if not isinstance(data, list):
            raise MeasurementSurfaceBlocked("thread/loaded/list data unavailable")
        ids.update(item for item in data if isinstance(item, str))
        next_cursor = response.get("nextCursor")
        if not isinstance(next_cursor, str) or not next_cursor:
            return ids
        cursor = next_cursor


def _wait_for_spawn(
    client: AppServerClient,
    parent_id: str,
    parent_turn_id: str,
    start_index: int,
) -> tuple[int, str, dict[str, Any]]:
    index, event = client.wait_for_notification(
        lambda item: collab_child_id(item, parent_id, parent_turn_id) is not None,
        start_index=start_index,
        timeout=120,
    )
    child_id = collab_child_id(event, parent_id, parent_turn_id)
    item = _spawn_item(event, parent_id, parent_turn_id)
    if child_id is None or item is None:
        raise ExecutionInvalid("child spawn correlation failed")
    return index, child_id, item


def _wait_parent_completed(
    client: AppServerClient,
    parent_id: str,
    parent_turn_id: str,
    start_index: int,
) -> Notification:
    _index, event = client.wait_for_notification(
        lambda item: (
            item.method == "turn/completed"
            and item.params.get("threadId") == parent_id
            and isinstance(item.params.get("turn"), dict)
            and item.params["turn"].get("id") == parent_turn_id
        ),
        start_index=start_index,
        timeout=300,
    )
    return event


def _one_child_turn(thread_read: dict[str, Any]) -> dict[str, Any]:
    thread = thread_read.get("thread")
    turns = thread.get("turns") if isinstance(thread, dict) else None
    if not isinstance(turns, list):
        raise MeasurementSurfaceBlocked("child turns unavailable")
    turns = [turn for turn in turns if isinstance(turn, dict)]
    if len(turns) != 1:
        raise ExecutionInvalid(f"expected one child turn, got {len(turns)}")
    return turns[0]


def _final_agent_text(turn: dict[str, Any]) -> str:
    items = turn.get("items")
    if not isinstance(items, list):
        raise ExecutionInvalid("child turn items unavailable")
    texts = [
        item["text"]
        for item in items
        if isinstance(item, dict)
        and item.get("type") == "agentMessage"
        and isinstance(item.get("text"), str)
    ]
    if not texts:
        raise ExecutionInvalid("child final agent message unavailable")
    return texts[-1]


def latest_child_usage(
    notifications: tuple[Notification, ...],
    *,
    child_id: str,
    child_turn_id: str,
) -> dict[str, int]:
    snapshots = [
        item.params.get("tokenUsage")
        for item in notifications
        if item.method == "thread/tokenUsage/updated"
        and item.params.get("threadId") == child_id
        and item.params.get("turnId") == child_turn_id
    ]
    snapshots = [item for item in snapshots if isinstance(item, dict)]
    if not snapshots:
        raise MeasurementSurfaceBlocked("exact child token usage unavailable")
    last = snapshots[-1].get("last")
    if not isinstance(last, dict):
        raise MeasurementSurfaceBlocked("child token usage last breakdown unavailable")
    fields = {
        "input_tokens": last.get("inputTokens"),
        "cached_input_tokens": last.get("cachedInputTokens"),
        "output_tokens": last.get("outputTokens"),
        "reasoning_tokens": last.get("reasoningOutputTokens"),
        "total_tokens": last.get("totalTokens"),
    }
    if not all(isinstance(value, int) for value in fields.values()):
        raise MeasurementSurfaceBlocked(f"child token usage has non-integer fields: {fields}")
    return fields  # type: ignore[return-value]


def _reroutes(notifications: tuple[Notification, ...], child_id: str) -> list[dict[str, Any]]:
    return [
        dict(item.params)
        for item in notifications
        if item.method == "model/rerouted" and item.params.get("threadId") == child_id
    ]


def tool_trace_oracle_leak(turn: dict[str, Any]) -> bool:
    items = turn.get("items")
    if not isinstance(items, list):
        return False
    for item in items:
        if not isinstance(item, dict):
            continue
        payload: str | None = None
        if item.get("type") == "commandExecution" and isinstance(item.get("command"), str):
            payload = item["command"]
        elif item.get("type") in {"mcpToolCall", "dynamicToolCall"}:
            payload = json.dumps(item.get("arguments"), sort_keys=True)
        if payload is None:
            continue
        lowered = payload.lower().replace("\\", "/")
        if any(fragment in lowered for fragment in FORBIDDEN_CHILD_TOOL_FRAGMENTS):
            return True
    return False


def _task_name(spec: ArmSpec) -> str:
    return f"t063_{spec.probe.lower()}_{spec.arm.lower()}"


def _parent_message(spec: ArmSpec, child_task: str) -> str:
    return (
        f"Required task_name: {_task_name(spec)}\n"
        f"Requested child model: {spec.model}\n"
        f"Requested child reasoning_effort: {spec.reasoning}\n"
        'Required fork_turns: "none"\n\n'
        "Child task message begins after the delimiter and must be passed unchanged.\n"
        "--- CHILD TASK ---\n"
        f"{child_task}"
    )


def _child_user_message_text(turn: dict[str, Any]) -> str:
    items = turn.get("items")
    if not isinstance(items, list):
        raise ExecutionInvalid("child turn items unavailable")
    user_messages = [
        item
        for item in items
        if isinstance(item, dict) and item.get("type") == "userMessage"
    ]
    if len(user_messages) != 1:
        raise ExecutionInvalid(
            f"expected one child userMessage item, got {len(user_messages)}"
        )
    content = user_messages[0].get("content")
    if not isinstance(content, list):
        raise ExecutionInvalid("child userMessage content unavailable")
    texts = [
        part.get("text")
        for part in content
        if isinstance(part, dict) and part.get("type") == "text" and isinstance(part.get("text"), str)
    ]
    if len(texts) != 1:
        raise ExecutionInvalid(
            f"expected one text part in child userMessage, got {len(texts)}"
        )
    return texts[0]


def _validate_parent_surface(parent_turn: dict[str, Any]) -> dict[str, Any]:
    items = parent_turn.get("items")
    if not isinstance(items, list):
        raise ExecutionInvalid("parent completed turn items unavailable")
    spawn_calls = [
        item
        for item in items
        if isinstance(item, dict)
        and item.get("type") == "collabAgentToolCall"
        and item.get("tool") in {"spawnAgent", "spawn_agent"}
    ]
    if len(spawn_calls) != 1:
        raise ExecutionInvalid(f"parent created {len(spawn_calls)} child spawns; expected 1")
    forbidden_types = {
        "commandExecution",
        "fileChange",
        "mcpToolCall",
        "dynamicToolCall",
        "webSearch",
        "imageView",
        "imageGeneration",
    }
    used = sorted(
        {item.get("type") for item in items if isinstance(item, dict) and item.get("type") in forbidden_types}
    )
    if used:
        raise ExecutionInvalid(f"measurement parent used forbidden tool/item types: {used}")
    return spawn_calls[0]


def execute_arm(
    client: AppServerClient,
    *,
    repo: Path,
    runtime_root: Path,
    prepared: PreparedInputs,
    spec: ArmSpec,
) -> dict[str, Any]:
    child_task = prepared.task_messages[spec.probe]
    child_cwd = runtime_root if spec.probe == "P3" else repo
    parent = client.request(
        "thread/start",
        {
            "model": ROOT_MODEL,
            "cwd": str(child_cwd),
            "permissions": ":read-only",
            "approvalPolicy": "never",
            "runtimeWorkspaceRoots": [str(child_cwd)],
            "developerInstructions": PARENT_INSTRUCTIONS,
        },
    )
    parent_id = _thread_id(parent)
    if _active_profile(parent) != ":read-only" or not _legacy_read_only(parent):
        raise MeasurementSurfaceBlocked("scored parent read-only receipt failed")

    start_index = len(client.notifications())
    parent_turn = client.request(
        "turn/start",
        {
            "threadId": parent_id,
            "input": [{"type": "text", "text": _parent_message(spec, child_task)}],
            "effort": ROOT_REASONING,
        },
    )
    parent_turn_id = _turn_id(parent_turn)
    index, child_id, spawn = _wait_for_spawn(client, parent_id, parent_turn_id, start_index)
    requested_model = spawn.get("model")
    requested_reasoning = spawn.get("reasoningEffort")
    if requested_model != spec.model or requested_reasoning != spec.reasoning:
        raise ProfileResolutionBlocked(
            f"{spec.probe} {spec.arm} spawn receipt {requested_model} / "
            f"{requested_reasoning}; expected {spec.requested_profile}"
        )

    if parent_id not in _loaded_thread_ids(client):
        raise MeasurementSurfaceBlocked("parent lost residency before child reattachment")
    child_resume = client.request("thread/resume", {"threadId": child_id})
    child_thread = child_resume.get("thread")
    if not isinstance(child_thread, dict) or child_thread.get("parentThreadId") != parent_id:
        raise MeasurementSurfaceBlocked("child parentThreadId mismatch")
    resolved_model = child_resume.get("model")
    resolved_reasoning = child_resume.get("reasoningEffort")
    if resolved_model != spec.model or resolved_reasoning != spec.reasoning:
        raise ProfileResolutionBlocked(
            f"{spec.probe} {spec.arm} resolved {resolved_model} / "
            f"{resolved_reasoning}; expected {spec.requested_profile}"
        )
    if _active_profile(child_resume) != ":read-only" or not _legacy_read_only(child_resume):
        raise MeasurementSurfaceBlocked("child read-only receipt failed")

    parent_done = _wait_parent_completed(client, parent_id, parent_turn_id, index)
    parent_turn_payload = parent_done.params.get("turn")
    if not isinstance(parent_turn_payload, dict):
        raise ExecutionInvalid("parent completed turn unavailable")
    _validate_parent_surface(parent_turn_payload)

    child_read = client.request("thread/read", {"threadId": child_id, "includeTurns": True})
    child_turn = _one_child_turn(child_read)
    child_turn_id = child_turn.get("id")
    if not isinstance(child_turn_id, str) or child_turn.get("status") != "completed":
        raise ExecutionInvalid("child turn did not complete with stable identity")
    observed_child_message = _child_user_message_text(child_turn)
    if observed_child_message != child_task:
        raise ExecutionInvalid(
            f"child task message drift in {spec.probe} {spec.arm}; exact equality required"
        )
    duration_ms = child_turn.get("durationMs")
    if not isinstance(duration_ms, int) or duration_ms < 0:
        raise MeasurementSurfaceBlocked("exact child duration unavailable")
    notifications = client.notifications()
    usage = latest_child_usage(
        notifications,
        child_id=child_id,
        child_turn_id=child_turn_id,
    )
    reroutes = _reroutes(notifications, child_id)
    if tool_trace_oracle_leak(child_turn):
        raise ExecutionInvalid(f"oracle/authority tool access observed in {spec.probe} {spec.arm}")

    value = parse_child_json(_final_agent_text(child_turn))
    if spec.probe == "P1":
        passed, verification = score_p1(value, prepared.p1_oracle)
        false_negative = false_positive = 0
    elif spec.probe == "P2":
        passed, verification = score_p2(value, prepared.p2_oracle)
        false_negative = false_positive = 0
    else:
        passed, verification, false_negative, false_positive = score_p3(value)

    snapshot = {
        "child_id": child_id,
        "parent_id": parent_id,
        "turn_id": child_turn_id,
        "probe": spec.probe,
        "arm": spec.arm,
        "role": _task_name(spec),
        "task_class": {
            "P1": "narrow_deterministic_evidence_retrieval",
            "P2": "broader_code_dependency_exploration",
            "P3": "adversarial_independent_review",
        }[spec.probe],
        "task_message_sha256": prepared.task_message_digests[spec.probe],
        "child_message_exact_match": True,
        "requested_profile": spec.requested_profile,
        "requested_model": requested_model,
        "requested_reasoning_effort": requested_reasoning,
        "resolved_model": resolved_model,
        "resolved_reasoning_effort": resolved_reasoning,
        "permission_profile": ":read-only",
        "legacy_sandbox_projection": "readOnly",
        "reroute_observed": bool(reroutes),
        "reroute_events": reroutes,
        "backend_served_profile_verified": False,
        **usage,
        "duration_seconds": duration_ms / 1000.0,
        "result_status": "PASS" if passed else "FAIL",
        "oracle_score": 1 if passed else 0,
        "verification_result": verification,
        "material_false_negative_count": false_negative,
        "material_false_positive_count": false_positive,
        "retry_or_escalation_reason": None,
        "oracle_leak_observed": False,
        "parent_residency_passed": True,
        "usage_exact_and_non_estimated": True,
        "closed": True,
    }
    client.request("thread/archive", {"threadId": child_id})
    client.request("thread/archive", {"threadId": parent_id})
    return snapshot
