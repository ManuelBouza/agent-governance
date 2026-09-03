"""Extracted MG1 topology harness implementation."""

from __future__ import annotations

import json
import re
from typing import Any

from .models import ALLOWED_OUTCOMES, TRIAL_SCHEMA, FrozenInputs, HarnessError, TrialSpec


def _trace_telemetry(stdout_jsonl: str, stderr: str = "") -> dict[str, Any]:
    usage: dict[str, Any] = {}
    tool_calls = 0
    rejected = 0
    for line in stdout_jsonl.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item", {})
        if item.get("type") in {"command_execution", "mcp_tool_call", "tool_call"}:
            tool_calls += 1
            if item.get("status") in {"rejected", "denied"} or item.get("exit_code") not in {
                None,
                0,
            }:
                rejected += 1
        if event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict):
            usage = event["usage"]
    token_fields = {
        "input_tokens": usage.get("input_tokens"),
        "cached_input_tokens": usage.get("cached_input_tokens"),
        "reasoning_tokens": usage.get("reasoning_output_tokens"),
        "output_tokens": usage.get("output_tokens"),
    }
    rejected += stderr.count('Rejected("')
    available = bool(usage)
    return {
        "token_usage_available": available,
        **token_fields,
        "total_tokens": usage.get("total_tokens"),
        "tool_call_count": tool_calls,
        "execution_policy_rejected_tool_call_count": rejected,
    }


def _successful_body_read(stdout_jsonl: str, relative_path: str) -> bool:
    needle = re.sub(r"[\\/]+", "/", relative_path).casefold()
    for line in stdout_jsonl.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item", {})
        command = re.sub(r"[\\/]+", "/", str(item.get("command", ""))).casefold()
        if (
            event.get("type") == "item.completed"
            and item.get("type") == "command_execution"
            and item.get("exit_code") == 0
            and needle in command
            and re.search(r"\b(get-content|cat|type|read_text|read_bytes)\b", command)
        ):
            return True
    return False


def _observed_skill_reads(
    inputs: FrozenInputs, spec: TrialSpec, stdout_jsonl: str
) -> tuple[list[str], list[str], bool]:
    successful_commands: list[str] = []
    trace_available = False
    for line in stdout_jsonl.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "thread.started":
            trace_available = True
        item = event.get("item", {})
        if (
            event.get("type") == "item.completed"
            and item.get("type") == "command_execution"
            and item.get("exit_code") == 0
        ):
            command = str(item.get("command", "")).replace("\\", "/").lower()
            while "//" in command:
                command = command.replace("//", "/")
            if re.search(r"\b(get-content|cat|type|read_text|read_bytes)\b", command):
                successful_commands.append(command)

    candidate = inputs.manifest["candidates"][spec.candidate_id]
    entrypoints = [
        entrypoint
        for entrypoint in candidate["entrypoints"]
        if any(
            f".agents/skills/{entrypoint.lower()}/skill.md" in command
            for command in successful_commands
        )
    ]
    references: list[str] = []
    for capability in candidate["load_order"]:
        if any(
            f".agents/skills/{entrypoint.lower()}/references/{capability.lower()}.md" in command
            for command in successful_commands
            for entrypoint, entrypoint_data in candidate["entrypoints"].items()
            if capability in entrypoint_data["capabilities"]
        ):
            references.append(inputs.manifest["shared_references"][capability])
    return entrypoints, references, trace_available


def _validate_model_result(
    inputs: FrozenInputs, spec: TrialSpec, model_result: dict[str, Any]
) -> None:
    if not isinstance(model_result, dict) or set(model_result) != set(TRIAL_SCHEMA["required"]):
        raise HarnessError(f"{spec.key}: structured result keys do not match trial contract")
    _validate_unique_text_list(spec, "activated_entrypoints", model_result["activated_entrypoints"])
    known_capabilities = set(inputs.manifest["shared_references"])
    granted = _validate_unique_text_list(
        spec, "granted_capabilities", model_result["granted_capabilities"]
    )
    if set(granted) - known_capabilities:
        raise HarnessError(f"{spec.key}: result names an unknown capability")
    if (
        not isinstance(model_result["semantic_outcome"], str)
        or model_result["semantic_outcome"] not in ALLOWED_OUTCOMES
    ):
        raise HarnessError(f"{spec.key}: result names an unknown semantic outcome")
    if not isinstance(model_result["permission_broadening"], bool):
        raise HarnessError(f"{spec.key}: permission_broadening must be boolean")
    if not isinstance(model_result["response_summary"], str):
        raise HarnessError(f"{spec.key}: response_summary must be text")


def _validate_unique_text_list(spec: TrialSpec, field: str, value: Any) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise HarnessError(f"{spec.key}: {field} must contain text")
    if len(value) != len(set(value)):
        raise HarnessError(f"{spec.key}: {field} must be a unique list")
    return value


def _surface_drift(stdout_jsonl: str, stderr: str, *, skill_path: str | None = None) -> str | None:
    visible = f"{stdout_jsonl}\n{stderr}"
    if re.search(
        r"(?i)(recommended_plugins|openai-curated-remote|apps \(connectors\)|app://)", visible
    ):
        return "UNRELATED_APP_PLUGIN_SURFACE"
    if skill_path:
        needle = re.sub(r"[\\/]+", "/", skill_path).casefold()
        rejection = re.compile(
            r"(?i)(rejected|denied|not allowed|blocked by policy|"
            r"access to the path[^\n]*is denied|acceso denegado)"
        )
        relevant_command_seen = False
        for line in stdout_jsonl.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            item = event.get("item", {})
            command = re.sub(r"[\\/]+", "/", str(item.get("command", ""))).casefold()
            if item.get("type") == "command_execution" and needle in command:
                relevant_command_seen = True
                diagnostic = f"{item.get('aggregated_output', '')}\n{line}"
                if item.get("exit_code") not in {None, 0} and rejection.search(diagnostic):
                    return "REQUIRED_SKILL_BODY_READ_REJECTED"
        if not relevant_command_seen:
            normalized_visible = re.sub(r"[\\/]+", "/", visible).casefold()
            if needle in normalized_visible and rejection.search(visible):
                return "REQUIRED_SKILL_BODY_READ_REJECTED"
    return None
