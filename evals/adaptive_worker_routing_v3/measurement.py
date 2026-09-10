"""D063 live preflight and one-arm measured execution for T063 v3."""
from __future__ import annotations

import json
import platform
import re
import shutil
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
    build_child_contract,
    build_parent_turn_message,
    per_arm_thread_config,
)
from .oracles import parse_child_json, run_command, score_p1, score_p2, score_p3, sha256_text

SCHEMA_MARKERS = (
    "activePermissionProfile",
    "runtimeWorkspaceRoots",
    "thread/loaded/list",
    "thread/tokenUsage/updated",
    "model/rerouted",
    "reasoningEffort",
    "parentThreadId",
    "subAgentActivity",
    "agentThreadId",
)

STANDARD_AGENT_CONFIG_KEYS = {
    "enabled",
    "max_concurrent_threads_per_session",
    "max_threads",
    "max_depth",
    "default_subagent_model",
    "default_subagent_reasoning_effort",
    "job_max_runtime_seconds",
    "interrupt_message",
}


def _codex_version(codex_bin: Path, repo: Path) -> str:
    result = run_command([str(codex_bin), "--version"], cwd=repo)
    match = re.search(r"(\d+\.\d+\.\d+)", result.stdout)
    if match is None:
        raise MeasurementSurfaceBlocked(f"cannot parse Codex version: {result.stdout!r}")
    return match.group(1)


def app_server_version(initialized: dict[str, Any]) -> str | None:
    server = initialized.get("serverInfo")
    if isinstance(server, dict) and isinstance(server.get("version"), str):
        return server["version"]
    user_agent = initialized.get("userAgent")
    if isinstance(user_agent, str):
        match = re.search(r"\bCodex Desktop/(\d+\.\d+\.\d+)\b", user_agent)
        if match is not None:
            return match.group(1)
    return None


def _active_profile(payload: dict[str, Any]) -> str | None:
    active = payload.get("activePermissionProfile")
    if isinstance(active, dict) and isinstance(active.get("id"), str):
        return active["id"]
    return None


def _legacy_read_only(payload: dict[str, Any]) -> bool:
    sandbox = payload.get("sandbox")
    if isinstance(sandbox, str):
        return sandbox.lower() in {"readonly", "read-only"}
    if isinstance(sandbox, dict):
        value = sandbox.get("type")
        return isinstance(value, str) and value.lower() in {"readonly", "read-only"}
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
        [str(codex_bin), "app-server", "generate-json-schema", "--experimental", "--out", str(schema_dir)],
        cwd=repo,
        timeout=60,
    )
    corpus = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in sorted(schema_dir.rglob("*.json"))
    )
    missing = [marker for marker in SCHEMA_MARKERS if marker not in corpus]
    shutil.rmtree(schema_dir)
    if missing:
        raise MeasurementSurfaceBlocked(f"native schema missing D063/v3 markers: {missing}")
    return {"required_markers": list(SCHEMA_MARKERS), "missing_markers": []}


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


def custom_agent_role_keys(config_read: dict[str, Any]) -> list[str]:
    config = config_read.get("config")
    if not isinstance(config, dict):
        raise MeasurementSurfaceBlocked("config/read effective config unavailable")
    agents = config.get("agents")
    if agents is None:
        return []
    if not isinstance(agents, dict):
        raise MeasurementSurfaceBlocked("config/read agents value is not an object")
    return sorted(key for key in agents if key not in STANDARD_AGENT_CONFIG_KEYS)


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
    app_server = app_server_version(initialized)
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

    config_read = client.request("config/read", {"cwd": str(repo), "includeLayers": False})
    role_keys = custom_agent_role_keys(config_read)
    if role_keys:
        raise MeasurementSurfaceBlocked(
            "custom agent roles would expose agent_type and can override the child contract: "
            + ", ".join(role_keys)
        )

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
    if _active_profile(probe_parent) != ":read-only" or not _legacy_read_only(probe_parent):
        raise MeasurementSurfaceBlocked("provider-free parent read-only receipt failed")
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
        "custom_agent_roles": role_keys,
        "agent_type_override_surface_blocked": True,
        "parent_read_only_preflight": True,
        "result": "PASS",
    }


def _activity_item(
    notification: Notification,
    parent_id: str,
    parent_turn_id: str,
    expected_task_name: str,
) -> dict[str, Any] | None:
    if notification.method not in {"item/started", "item/completed"}:
        return None
    params = notification.params
    if params.get("threadId") != parent_id or params.get("turnId") != parent_turn_id:
        return None
    item = params.get("item")
    if not isinstance(item, dict) or item.get("type") != "subAgentActivity":
        return None
    kind = item.get("kind")
    if not isinstance(kind, str) or kind.lower() != "started":
        return None
    child = item.get("agentThreadId")
    path = item.get("agentPath")
    if not isinstance(child, str) or not isinstance(path, str):
        return None
    normalized = path.rstrip("/").split("/")[-1]
    if normalized != expected_task_name:
        return None
    return item


def activity_child_id(
    notification: Notification,
    parent_id: str,
    parent_turn_id: str,
    expected_task_name: str,
) -> str | None:
    item = _activity_item(notification, parent_id, parent_turn_id, expected_task_name)
    return None if item is None else item["agentThreadId"]


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
    expected_task_name: str,
    start_index: int,
) -> tuple[int, str, dict[str, Any]]:
    index, event = client.wait_for_notification(
        lambda item: activity_child_id(item, parent_id, parent_turn_id, expected_task_name) is not None,
        start_index=start_index,
        timeout=120,
    )
    child_id = activity_child_id(event, parent_id, parent_turn_id, expected_task_name)
    item = _activity_item(event, parent_id, parent_turn_id, expected_task_name)
    if child_id is None or item is None:
        raise ExecutionInvalid("child spawn correlation failed")
    return index, child_id, item


def _wait_turn_completed(
    client: AppServerClient,
    thread_id: str,
    *,
    start_index: int,
    timeout: float = 300.0,
) -> tuple[int, dict[str, Any]]:
    index, event = client.wait_for_notification(
        lambda item: (
            item.method == "turn/completed"
            and item.params.get("threadId") == thread_id
            and isinstance(item.params.get("turn"), dict)
        ),
        start_index=start_index,
        timeout=timeout,
    )
    turn = event.params.get("turn")
    if not isinstance(turn, dict):
        raise ExecutionInvalid("completed turn unavailable")
    return index, turn


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
    notifications: tuple[Notification, ...], *, child_id: str, child_turn_id: str
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


def validate_worker_receipt(
    value: dict[str, Any], *, spec: ArmSpec, task_digest: str
) -> dict[str, str]:
    receipt = value.get("t063_receipt")
    if not isinstance(receipt, dict):
        raise ExecutionInvalid("worker t063_receipt missing")
    observed = {
        "contract_nonce": receipt.get("contract_nonce"),
        "task_message_sha256": receipt.get("task_message_sha256"),
        "spawn_trigger_received": receipt.get("spawn_trigger_received"),
    }
    expected = {
        "contract_nonce": spec.contract_nonce,
        "task_message_sha256": task_digest,
        "spawn_trigger_received": spec.spawn_trigger,
    }
    if observed != expected:
        raise ExecutionInvalid(
            f"worker contract/transport receipt mismatch: observed={observed!r}, expected={expected!r}"
        )
    return expected


def _validate_parent_surface(
    parent_turn: dict[str, Any], *, child_id: str, expected_task_name: str
) -> None:
    items = parent_turn.get("items")
    if not isinstance(items, list):
        raise ExecutionInvalid("parent completed turn items unavailable")
    activities = [
        item
        for item in items
        if isinstance(item, dict)
        and item.get("type") == "subAgentActivity"
        and isinstance(item.get("kind"), str)
        and item["kind"].lower() == "started"
    ]
    matching = [
        item for item in activities
        if item.get("agentThreadId") == child_id
        and isinstance(item.get("agentPath"), str)
        and item["agentPath"].rstrip("/").split("/")[-1] == expected_task_name
    ]
    if len(activities) != 1 or len(matching) != 1:
        raise ExecutionInvalid(
            f"parent spawn activity count mismatch: total={len(activities)}, matching={len(matching)}"
        )
    forbidden_types = {
        "commandExecution",
        "fileChange",
        "mcpToolCall",
        "dynamicToolCall",
        "webSearch",
        "imageView",
        "imageGeneration",
    }
    used = sorted({
        item.get("type")
        for item in items
        if isinstance(item, dict) and item.get("type") in forbidden_types
    })
    if used:
        raise ExecutionInvalid(f"measurement parent used forbidden tool/item types: {used}")
    final = _final_agent_text(parent_turn).strip()
    if final != "PARENT_SPAWNED":
        raise ExecutionInvalid(f"measurement parent final response drift: {final!r}")


def execute_arm(
    client: AppServerClient,
    *,
    repo: Path,
    runtime_root: Path,
    prepared: PreparedInputs,
    spec: ArmSpec,
) -> dict[str, Any]:
    task_message = prepared.task_messages[spec.probe]
    task_digest = prepared.task_message_digests[spec.probe]
    child_contract = build_child_contract(spec, task_message, task_digest)
    child_cwd = runtime_root if spec.probe == "P3" else repo
    request_config = per_arm_thread_config(spec, child_contract)

    parent = client.request(
        "thread/start",
        {
            "model": ROOT_MODEL,
            "cwd": str(child_cwd),
            "permissions": ":read-only",
            "approvalPolicy": "never",
            "runtimeWorkspaceRoots": [str(child_cwd)],
            "developerInstructions": PARENT_INSTRUCTIONS,
            "config": request_config,
        },
    )
    parent_id = _thread_id(parent)
    if parent.get("model") != ROOT_MODEL:
        raise ProfileResolutionBlocked(
            f"parent resolved model {parent.get('model')!r}; expected {ROOT_MODEL}"
        )
    if parent.get("reasoningEffort") not in {None, ROOT_REASONING}:
        raise ProfileResolutionBlocked(
            f"parent thread reasoning {parent.get('reasoningEffort')!r}; expected unset or {ROOT_REASONING}"
        )
    if _active_profile(parent) != ":read-only" or not _legacy_read_only(parent):
        raise MeasurementSurfaceBlocked("scored parent read-only receipt failed")

    start_index = len(client.notifications())
    parent_turn = client.request(
        "turn/start",
        {
            "threadId": parent_id,
            "input": [{"type": "text", "text": build_parent_turn_message(spec)}],
            "effort": ROOT_REASONING,
        },
    )
    parent_turn_id = _turn_id(parent_turn)
    index, child_id, activity = _wait_for_spawn(
        client, parent_id, parent_turn_id, spec.task_name, start_index
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
            f"{spec.probe} {spec.arm} resolved {resolved_model} / {resolved_reasoning}; expected {spec.requested_profile}"
        )
    if _active_profile(child_resume) != ":read-only" or not _legacy_read_only(child_resume):
        raise MeasurementSurfaceBlocked("child read-only receipt failed")

    _parent_index, parent_done = _wait_turn_completed(
        client, parent_id, start_index=index, timeout=300
    )
    if parent_done.get("id") != parent_turn_id:
        raise ExecutionInvalid("parent completed turn identity mismatch")
    _validate_parent_surface(
        parent_done, child_id=child_id, expected_task_name=spec.task_name
    )

    _child_index, child_done = _wait_turn_completed(
        client, child_id, start_index=start_index, timeout=300
    )
    child_turn_id = child_done.get("id")
    if not isinstance(child_turn_id, str) or child_done.get("status") != "completed":
        raise ExecutionInvalid("child turn did not complete with stable identity")

    child_read = client.request("thread/read", {"threadId": child_id, "includeTurns": True})
    child_turn = _one_child_turn(child_read)
    if child_turn.get("id") != child_turn_id or child_turn.get("status") != "completed":
        raise ExecutionInvalid("child thread/read turn identity/status mismatch")
    duration_ms = child_turn.get("durationMs")
    if not isinstance(duration_ms, int) or duration_ms < 0:
        raise MeasurementSurfaceBlocked("exact child duration unavailable")
    notifications = client.notifications()
    usage = latest_child_usage(notifications, child_id=child_id, child_turn_id=child_turn_id)
    reroutes = _reroutes(notifications, child_id)
    if tool_trace_oracle_leak(child_turn):
        raise ExecutionInvalid(f"oracle/authority tool access observed in {spec.probe} {spec.arm}")

    value = parse_child_json(_final_agent_text(child_turn))
    receipt = validate_worker_receipt(value, spec=spec, task_digest=task_digest)
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
        "parent_turn_id": parent_turn_id,
        "turn_id": child_turn_id,
        "probe": spec.probe,
        "arm": spec.arm,
        "role": spec.task_name,
        "task_class": {
            "P1": "narrow_deterministic_evidence_retrieval",
            "P2": "broader_code_dependency_exploration",
            "P3": "adversarial_independent_review",
        }[spec.probe],
        "task_message_sha256": task_digest,
        "child_contract_sha256": sha256_text(child_contract),
        "contract_receipt": receipt,
        "spawn_correlation_receipt": {
            "type": "subAgentActivity",
            "kind": activity.get("kind"),
            "agent_thread_id": child_id,
            "agent_path": activity.get("agentPath"),
        },
        "requested_profile": spec.requested_profile,
        "requested_model": spec.model,
        "requested_reasoning_effort": spec.reasoning,
        "request_profile_source": "thread/start.config agents defaults",
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
        "child_single_turn_no_parent_history": True,
        "closed": True,
    }
    client.request("thread/archive", {"threadId": child_id})
    client.request("thread/archive", {"threadId": parent_id})
    return snapshot
