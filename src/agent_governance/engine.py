"""Safe bootstrap and structural validation for consumer Governance installs."""

from __future__ import annotations

import argparse
import errno
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import IO

try:
    import fcntl as _fcntl
except ImportError:  # pragma: no cover - exercised on native Windows
    _fcntl = None

if os.name == "nt":  # pragma: no branch - selected once per host
    import ctypes as _ctypes

    _kernel32 = _ctypes.WinDLL("kernel32", use_last_error=True)
    _create_mutex = _kernel32.CreateMutexW
    _create_mutex.argtypes = [_ctypes.c_void_p, _ctypes.c_int, _ctypes.c_wchar_p]
    _create_mutex.restype = _ctypes.c_void_p
    _wait_for_single_object = _kernel32.WaitForSingleObject
    _wait_for_single_object.argtypes = [_ctypes.c_void_p, _ctypes.c_ulong]
    _wait_for_single_object.restype = _ctypes.c_ulong
    _release_mutex = _kernel32.ReleaseMutex
    _release_mutex.argtypes = [_ctypes.c_void_p]
    _release_mutex.restype = _ctypes.c_int
    _close_handle = _kernel32.CloseHandle
    _close_handle.argtypes = [_ctypes.c_void_p]
    _close_handle.restype = _ctypes.c_int
    _windows_lock_api = (
        _create_mutex,
        _wait_for_single_object,
        _release_mutex,
        _close_handle,
    )
else:
    _ctypes = None
    _windows_lock_api = None

CORE_FILES = (
    "ADAPTERS.md",
    "ASSURANCE.md",
    "COEXISTENCE.md",
    "CONTEXT.md",
    "EXECUTION-CONTROL.md",
    "EXECUTION.md",
    "GOVERNANCE.md",
    "HANDOFF.md",
    "INTERACTION.md",
    "LIFECYCLE.md",
    "PROTOCOL.md",
    "QUALITY.md",
    "SECURITY.md",
    "SKILL-DISCOVERY.md",
    "SKILL-SUPPLY-CHAIN.md",
    "SKILLS.md",
)
CORE_VERSION_FIELDS = {
    "ADAPTERS.md": "Adapter-Version",
    "ASSURANCE.md": "Assurance-Audit-Version",
    "COEXISTENCE.md": "Coexistence-Version",
    "CONTEXT.md": "Context-Version",
    "EXECUTION-CONTROL.md": "Execution-Control-Version",
    "EXECUTION.md": "Execution-Version",
    "HANDOFF.md": "Handoff-Version",
    "INTERACTION.md": "Interaction-Module-Version",
    "LIFECYCLE.md": "Lifecycle-Version",
    "PROTOCOL.md": "Protocol-Module-Version",
    "QUALITY.md": "Quality-Module-Version",
    "SECURITY.md": "Security-Verification-Version",
    "SKILL-DISCOVERY.md": "Discovery-Version",
    "SKILL-SUPPLY-CHAIN.md": "Supply-Chain-Version",
    "SKILLS.md": "Skills-Version",
}
ASSET_TARGETS = {
    "MISSION.template.md": "MISSION.md",
    "WORKPLAN.template.md": "WORKPLAN.md",
    "CAPABILITIES.template.json": "CAPABILITIES.json",
    "STATE.template.json": "STATE.json",
    "EXCHANGE.template.jsonl": "EXCHANGE.jsonl",
    "TASK.template.md": "tasks/TASK.template.md",
    "SKILL-APPROVAL.template.json": "skills/SKILL-APPROVAL.template.json",
}
COORDINATION_DIRS = ("tasks", "skills", "decisions")
SOURCE_MARKERS = ("governance-core", "governance-skill", "maintainer-skill")
SEMVER = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)")
ACTORS = {"human", "strategy", "implementation", "gpt", "oc"}
EVENTS = {
    "start",
    "progress",
    "done",
    "blocked",
    "resume",
    "accept",
    "reject",
    "decision",
    "scope_change",
    "cancel",
}
CAPABILITY_CLASSIFICATIONS = {"REUSE", "ADAPT", "COEXIST", "MISSING", "CONFLICT"}
APPROVAL_STATUSES = {"APPROVED", "REVOKED", "SUPERSEDED"}
WORK_STATES = {
    "PLANNED",
    "READY",
    "IN_PROGRESS",
    "BLOCKED",
    "DONE",
    "ACCEPTED",
    "REJECTED",
    "CANCELLED",
}
TERMINAL_STATES = {"DONE", "ACCEPTED", "CANCELLED"}
NEW_ACTORS = {"human", "strategy", "implementation"}
EVENT_FIELDS = {"q", "a", "e", "k", "r", "v", "x", "n", "z", "s", "m"}
TASK_EVENTS = {"start", "progress", "done", "blocked", "resume", "accept", "reject", "cancel"}
TRANSITIONS = {
    "start": ({"READY", "REJECTED"}, "IN_PROGRESS"),
    "progress": ({"IN_PROGRESS"}, "IN_PROGRESS"),
    "blocked": ({"IN_PROGRESS"}, "BLOCKED"),
    "resume": ({"BLOCKED"}, "IN_PROGRESS"),
    "done": ({"IN_PROGRESS"}, "DONE"),
    "accept": ({"DONE"}, "ACCEPTED"),
    "reject": ({"DONE"}, "REJECTED"),
}
EVENT_ACTORS = {
    "start": {"implementation"},
    "progress": {"implementation"},
    "done": {"implementation"},
    "blocked": {"implementation"},
    "resume": {"human", "strategy"},
    "accept": {"human", "strategy"},
    "reject": {"human", "strategy"},
    "decision": {"human", "strategy"},
    "scope_change": {"human", "strategy"},
    "cancel": {"human", "strategy"},
}
MISSION_TEMPLATE = """# Mission

Mission-ID: `<mission-id>`
Status: `<status>`

## Objective

`<human-approved-objective>`

## Scope

- In: `<in-scope>`
- Out: `<out-of-scope>`

## Authority references

- `<project-native-authority-reference>`

## Success criteria

- `<criterion>`
"""
WORKPLAN_TEMPLATE = """# Workplan

Mission-ID: `<mission-id>`
Status: `<status>`

## Tasks

1. `<task-id>` — depends on `<dependency-or-none>` — `<status>`

## Frontier

Current task: `<task-id-or-none>`
Blocker: `<blocker-or-none>`

Task implementation details belong in task records.
"""
EXCHANGE_TEMPLATE = '{"q":1,"a":"human","e":"start","n":"Provide Human-approved mission inputs"}\n'


class GovernanceError(Exception):
    """Expected fail-closed CLI error."""


def _protocol_version(governance: Path) -> str:
    try:
        lines = governance.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise GovernanceError(f"cannot read protocol authority {governance}: {error}") from error
    declarations = [
        line.split(":", 1)[1].strip() for line in lines if line.startswith("Protocol-Version:")
    ]
    if len(declarations) != 1 or SEMVER.fullmatch(declarations[0]) is None:
        raise GovernanceError(
            f"{governance} must contain exactly one strict SemVer Protocol-Version declaration"
        )
    return declarations[0]


def _version_declaration(path: Path, field: str) -> None:
    text = _nonempty_text(path)
    declarations = [
        line.split(":", 1)[1].strip() for line in text.splitlines() if line.startswith(f"{field}:")
    ]
    if len(declarations) != 1 or SEMVER.fullmatch(declarations[0]) is None:
        raise GovernanceError(f"{path} must contain exactly one strict SemVer {field} declaration")


def _safe_target(raw_target: str) -> Path:
    target = Path(raw_target).expanduser()
    if target.is_symlink() or not target.is_dir():
        raise GovernanceError(f"target must be an existing, non-symlink directory: {target}")
    target = target.resolve()
    present_markers = [
        name for name in SOURCE_MARKERS if (target / name).exists() or (target / name).is_symlink()
    ]
    if present_markers:
        raise GovernanceError(
            f"source/consumer separation violation; found: {', '.join(present_markers)}"
        )
    return target


def _bootstrap(
    target: Path,
    package_paths: tuple[Path, Path],
    validate: Callable[[Path], None] | None = None,
) -> None:
    core_source, assets = package_paths
    missing_sources = [
        str(core_source / name) for name in CORE_FILES if not (core_source / name).is_file()
    ]
    missing_sources.extend(
        str(assets / name) for name in ASSET_TARGETS if not (assets / name).is_file()
    )
    if missing_sources:
        raise GovernanceError(f"package is incomplete; missing: {', '.join(missing_sources)}")

    version = _validate_core(core_source)
    _validate_assets(assets, version)

    managed = (target / ".agent-governance", target / ".agent-coordination")
    collisions = [str(path) for path in managed if path.exists() or path.is_symlink()]
    if collisions:
        raise GovernanceError(
            f"managed path collision; refusing overwrite: {', '.join(collisions)}"
        )

    governance_target, coordination_target = managed
    owned_roots: list[Path] = []
    try:
        governance_target.mkdir()
        owned_roots.append(governance_target)
        for name in CORE_FILES:
            shutil.copyfile(core_source / name, governance_target / name)
        coordination_target.mkdir()
        owned_roots.append(coordination_target)
        for name in COORDINATION_DIRS:
            (coordination_target / name).mkdir()
        for source_name, relative_target in ASSET_TARGETS.items():
            destination = coordination_target / relative_target
            shutil.copyfile(assets / source_name, destination)
        (validate or _validate)(target)
    except Exception:
        for path in reversed(owned_roots):
            shutil.rmtree(path, ignore_errors=True)
        raise


def _required_file(path: Path) -> None:
    if path.is_symlink() or not path.is_file():
        raise GovernanceError(f"missing or unsafe required file: {path}")


def _required_dir(path: Path) -> None:
    if path.is_symlink() or not path.is_dir():
        raise GovernanceError(f"missing or unsafe required directory: {path}")


def _nonempty_text(path: Path) -> str:
    _required_file(path)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise GovernanceError(f"cannot read required file {path}: {error}") from error
    if not text.strip():
        raise GovernanceError(f"required file must be non-empty: {path}")
    return text


def _read_json(path: Path) -> dict[str, object]:
    _required_file(path)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeError) as error:
        raise GovernanceError(f"malformed JSON in {path}: {error}") from error
    if not isinstance(value, dict):
        raise GovernanceError(f"JSON document must be an object: {path}")
    return value


def _atomic_write(path: Path, content: str) -> None:
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def _atomic_json(path: Path, value: dict[str, object]) -> None:
    _atomic_write(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def _validate_jsonl(path: Path) -> int:
    _required_file(path)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise GovernanceError(f"cannot read JSONL {path}: {error}") from error
    if not lines:
        raise GovernanceError(f"EXCHANGE must contain at least one event: {path}")
    previous = 0
    for line_number, line in enumerate(lines, 1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise GovernanceError(f"malformed JSONL at {path}:{line_number}: {error}") from error
        if not isinstance(event, dict):
            raise GovernanceError(f"JSONL event must be an object at {path}:{line_number}")
        q = event.get("q")
        if not isinstance(q, int) or isinstance(q, bool) or q <= previous:
            raise GovernanceError(f"EXCHANGE q must increase at {path}:{line_number}")
        if event.get("a") not in ACTORS or event.get("e") not in EVENTS:
            raise GovernanceError(f"invalid EXCHANGE actor/event at {path}:{line_number}")
        previous = q
    return previous


def _events_from_text(content: str, path: Path) -> list[dict[str, object]]:
    lines = content.splitlines()
    if not lines:
        raise GovernanceError(f"EXCHANGE must contain at least one event: {path}")
    events: list[dict[str, object]] = []
    superseded: set[int] = set()
    previous = 0
    for line_number, line in enumerate(lines, 1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise GovernanceError(f"malformed JSONL at {path}:{line_number}: {error}") from error
        if not isinstance(event, dict) or not set(event) <= EVENT_FIELDS:
            raise GovernanceError(f"EXCHANGE event has unexpected fields at {path}:{line_number}")
        q = event.get("q")
        if not isinstance(q, int) or isinstance(q, bool) or q <= previous:
            raise GovernanceError(f"EXCHANGE q must increase at {path}:{line_number}")
        if event.get("a") not in ACTORS or event.get("e") not in EVENTS:
            raise GovernanceError(f"invalid EXCHANGE actor/event at {path}:{line_number}")
        for field in set(event) - {"q", "s"}:
            if not isinstance(event[field], str) or not event[field]:
                raise GovernanceError(
                    f"EXCHANGE {field} must be a non-empty string at {path}:{line_number}"
                )
        supersedes = event.get("s")
        if supersedes is not None:
            if (
                not isinstance(supersedes, int)
                or isinstance(supersedes, bool)
                or supersedes >= event["q"]
                or supersedes not in {item["q"] for item in events}
                or supersedes in superseded
            ):
                raise GovernanceError(
                    f"invalid EXCHANGE superseded sequence at {path}:{line_number}"
                )
            superseded.add(supersedes)
        events.append(event)
        previous = q
    return events


def _read_events(path: Path) -> list[dict[str, object]]:
    _required_file(path)
    try:
        return _events_from_text(path.read_text(encoding="utf-8"), path)
    except (OSError, UnicodeError) as error:
        raise GovernanceError(f"cannot read JSONL {path}: {error}") from error


@contextmanager
def _locked_exchange(path: Path, *, exclusive: bool) -> Iterator[IO[str]]:
    _required_file(path)
    try:
        with path.open("r+", encoding="utf-8", newline="") as stream:
            lock_token = _acquire_file_lock(stream, exclusive=exclusive)
            try:
                yield stream
            finally:
                _release_file_lock(stream, lock_token)
    except (OSError, UnicodeError) as error:
        raise GovernanceError(f"cannot lock EXCHANGE {path}: {error}") from error


def _acquire_file_lock(stream: IO[str], *, exclusive: bool) -> object | None:
    if _fcntl is not None:
        mode = _fcntl.LOCK_EX if exclusive else _fcntl.LOCK_SH
        _fcntl.flock(stream.fileno(), mode)
        return None
    if _windows_lock_api is not None and _ctypes is not None:
        create_mutex, wait_for_single_object, _release_mutex, close_handle = _windows_lock_api
        canonical_path = os.path.normcase(os.path.abspath(os.fspath(stream.name)))
        lock_name = (
            "Local\\AgentGovernanceExchange-"
            + hashlib.sha256(canonical_path.encode("utf-8")).hexdigest()
        )
        handle = create_mutex(None, False, lock_name)
        if not handle:
            raise OSError(_ctypes.get_last_error(), "cannot create Windows EXCHANGE mutex")
        wait_result = wait_for_single_object(handle, 0xFFFFFFFF)
        if wait_result != 0:
            close_handle(handle)
            if wait_result == 0x80:
                raise OSError(errno.EOWNERDEAD, "Windows EXCHANGE mutex was abandoned")
            raise OSError(_ctypes.get_last_error(), "cannot acquire Windows EXCHANGE mutex")
        return handle
    raise OSError(errno.ENOSYS, "no supported file-locking backend")


def _release_file_lock(stream: IO[str], lock_token: object | None) -> None:
    if _fcntl is not None:
        _fcntl.flock(stream.fileno(), _fcntl.LOCK_UN)
        return
    if _windows_lock_api is not None and _ctypes is not None and lock_token is not None:
        _create_mutex, _wait_for_single_object, release_mutex, close_handle = _windows_lock_api
        if not release_mutex(lock_token):
            error = _ctypes.get_last_error()
            close_handle(lock_token)
            raise OSError(error, "cannot release Windows EXCHANGE mutex")
        if not close_handle(lock_token):
            raise OSError(_ctypes.get_last_error(), "cannot close Windows EXCHANGE mutex")
        return
    raise OSError(errno.ENOSYS, "no supported file-locking backend")


def _metadata(text: str, field: str, source: Path) -> str:
    values = [
        line.split(":", 1)[1].strip() for line in text.splitlines() if line.startswith(f"{field}:")
    ]
    if len(values) != 1 or not values[0] or "<" in values[0]:
        raise GovernanceError(f"{source} must contain exactly one resolved {field}")
    value = values[0]
    if value.startswith("`") and value.endswith("`"):
        value = value[1:-1]
    return value


def _parse_workplan(coordination: Path) -> dict[str, object]:
    mission_path = coordination / "MISSION.md"
    workplan_path = coordination / "WORKPLAN.md"
    mission_text = _nonempty_text(mission_path)
    workplan_text = _nonempty_text(workplan_path)
    mission_id = _metadata(mission_text, "Mission-ID", mission_path)
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", mission_id) is None:
        raise GovernanceError("MISSION Mission-ID is unsafe")
    mission_status = _metadata(mission_text, "Status", mission_path).upper()
    if _metadata(workplan_text, "Mission-ID", workplan_path) != mission_id:
        raise GovernanceError("MISSION and WORKPLAN Mission-ID mismatch")
    phase = _metadata(workplan_text, "Status", workplan_path).upper()
    if re.fullmatch(r"F[0-6]", phase) is None:
        raise GovernanceError("WORKPLAN Status must be a lifecycle phase F0-F6")
    try:
        gate_lines = [line for line in workplan_text.splitlines() if line.startswith("Gates:")]
        record_lines = [
            line for line in workplan_text.splitlines() if line.startswith("Controlling records:")
        ]
        gates = json.loads(gate_lines[0].split(":", 1)[1].strip()) if gate_lines else {}
        controlling_records = (
            json.loads(record_lines[0].split(":", 1)[1].strip())
            if record_lines
            else ["MISSION.md", "WORKPLAN.md"]
        )
    except json.JSONDecodeError as error:
        raise GovernanceError(f"WORKPLAN state metadata must be valid JSON: {error}") from error
    if len(gate_lines) > 1 or len(record_lines) > 1:
        raise GovernanceError("WORKPLAN state metadata must not be duplicated")
    if not isinstance(gates, dict) or not all(
        isinstance(key, str) and isinstance(value, bool) for key, value in gates.items()
    ):
        raise GovernanceError("WORKPLAN Gates must be a JSON object of booleans")
    if not _string_array(controlling_records):
        raise GovernanceError("WORKPLAN Controlling records must be a JSON string array")
    if len(gates) > 7 or len(controlling_records) > 16:
        raise GovernanceError("WORKPLAN STATE metadata exceeds constant-size bounds")
    for reference in controlling_records:
        relative = Path(reference)
        if relative.is_absolute() or ".." in relative.parts:
            raise GovernanceError(f"invalid controlling record reference: {reference}")
        record = coordination / relative
        _required_file(record)

    tasks: dict[str, dict[str, object]] = {}
    task_pattern = re.compile(r"^\d+\. `([^`]+)` \u2014 depends on `([^`]+)` \u2014 `([A-Z_]+)`$")
    for line in workplan_text.splitlines():
        match = task_pattern.fullmatch(line)
        if match is None:
            continue
        task_id, dependency_text, status = match.groups()
        if (
            task_id in tasks
            or status not in WORK_STATES
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", task_id)
        ):
            raise GovernanceError(f"invalid or duplicate WORKPLAN task metadata: {task_id}")
        dependencies = [] if dependency_text.lower() == "none" else dependency_text.split(",")
        if any(not dependency or dependency.strip() != dependency for dependency in dependencies):
            raise GovernanceError(f"invalid dependencies for task {task_id}")
        tasks[task_id] = {"status": status, "dependencies": dependencies}
    if not tasks:
        raise GovernanceError("WORKPLAN must contain resolved task metadata")
    for task_id, task in tasks.items():
        for dependency in task["dependencies"]:
            if dependency == task_id or dependency not in tasks:
                raise GovernanceError(f"task {task_id} has invalid dependency {dependency}")
    current = _metadata(workplan_text, "Current task", workplan_path)
    current_task = None if current.lower() == "none" else current
    if current_task is not None and current_task not in tasks:
        raise GovernanceError("WORKPLAN Current task has invalid reference")
    blocker = _metadata(workplan_text, "Blocker", workplan_path)
    blocker_value = None if blocker.lower() == "none" else blocker
    active = [
        task_id
        for task_id, task in tasks.items()
        if task["status"] in {"READY", "IN_PROGRESS", "BLOCKED"}
    ]
    if (
        len(active) > 1
        or (active and current_task != active[0])
        or (not active and current_task is not None)
    ):
        raise GovernanceError("WORKPLAN has ambiguous active task frontier")
    if blocker_value is not None and (
        current_task is None or tasks[current_task]["status"] != "BLOCKED"
    ):
        raise GovernanceError("WORKPLAN blocker does not reference a BLOCKED current task")
    if current_task is not None:
        task_record = coordination / "tasks" / f"{current_task}.md"
        _required_file(task_record)
        if _metadata(_nonempty_text(task_record), "Task-ID", task_record) != current_task:
            raise GovernanceError(f"task record ID mismatch for {current_task}")
    return {
        "mission_id": mission_id,
        "mission_status": mission_status,
        "phase": phase,
        "gates": gates,
        "controlling_records": controlling_records,
        "tasks": tasks,
        "active_task": current_task,
        "blocker": blocker_value,
    }


def _effective_events(events: list[dict[str, object]]) -> list[dict[str, object]]:
    superseded = {event["s"] for event in events if "s" in event}
    return [event for event in events if event["q"] not in superseded]


def _validate_event_history(
    events: list[dict[str, object]], plan: dict[str, object]
) -> dict[str, str]:
    tasks = plan["tasks"]
    states = {task_id: "PLANNED" for task_id in tasks}
    seen_task_event: set[str] = set()
    for event in _effective_events(events):
        event_name = event["e"]
        actor = event["a"]
        task_id = event.get("k")
        if task_id is None:
            if event_name == "start" and actor == "human":
                continue
            if event_name not in {"decision", "scope_change", "cancel"}:
                raise GovernanceError(f"event {event_name} requires a task ID")
        elif task_id not in tasks:
            raise GovernanceError(f"event references unknown task {task_id}")
        if actor in {"gpt", "oc"}:
            actor = {"gpt": "strategy", "oc": "implementation"}[actor]
        if event_name in EVENT_ACTORS and actor not in EVENT_ACTORS[event_name]:
            raise GovernanceError(f"actor {event['a']} cannot emit {event_name}")
        if task_id is None or event_name not in TASK_EVENTS:
            continue
        current = states[task_id]
        if task_id not in seen_task_event:
            declared = tasks[task_id]["status"]
            if event_name == "start":
                current = "READY"
            elif event_name == "cancel":
                current = declared if declared != "CANCELLED" else "PLANNED"
            else:
                raise GovernanceError(f"first event for task {task_id} must be start or cancel")
            seen_task_event.add(task_id)
        if event_name == "cancel":
            if current == "ACCEPTED":
                raise GovernanceError(f"cannot cancel ACCEPTED task {task_id}")
            states[task_id] = "CANCELLED"
            continue
        if event_name == "done" and not all(event.get(field) for field in ("r", "v")):
            raise GovernanceError("done event requires evidence reference and verification")
        if event_name == "blocked" and not all(event.get(field) for field in ("r", "x")):
            raise GovernanceError("blocked event requires evidence reference and reason")
        allowed, destination = TRANSITIONS[event_name]
        if current not in allowed:
            raise GovernanceError(
                f"invalid {event_name} transition for task {task_id} from {current}"
            )
        if event_name == "start":
            unmet = [
                dependency
                for dependency in tasks[task_id]["dependencies"]
                if states[dependency] not in {"DONE", "ACCEPTED"}
            ]
            if unmet:
                raise GovernanceError(f"task {task_id} has unmet dependencies: {', '.join(unmet)}")
            other_active = [
                other
                for other, state in states.items()
                if other != task_id and state in {"IN_PROGRESS", "BLOCKED"}
            ]
            if other_active:
                raise GovernanceError("event history has parallel active tasks")
        states[task_id] = destination
    for task_id, task in tasks.items():
        declared = task["status"]
        if task_id not in seen_task_event:
            if declared not in {"PLANNED", "READY"}:
                raise GovernanceError(
                    f"task {task_id} has status {declared} without transition history"
                )
            states[task_id] = declared
    return states


def _nullable_string(value: object) -> bool:
    return value is None or isinstance(value, str)


def _string_array(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _validate_capabilities(data: dict[str, object]) -> None:
    if set(data) != {"protocol_version", "capabilities"}:
        raise GovernanceError("CAPABILITIES has unexpected or missing fields")
    capabilities = data["capabilities"]
    if not isinstance(capabilities, list):
        raise GovernanceError("CAPABILITIES capabilities must be an array")
    for index, capability in enumerate(capabilities):
        if not isinstance(capability, dict):
            raise GovernanceError(f"CAPABILITIES entry {index} must be an object")
        if capability.get("classification") not in CAPABILITY_CLASSIFICATIONS:
            raise GovernanceError(f"CAPABILITIES entry {index} has invalid classification")


def _validate_state(data: dict[str, object]) -> None:
    expected = {
        "protocol_version",
        "mission_id",
        "phase",
        "gates",
        "active_task",
        "ready_tasks",
        "next_action",
        "controlling_records",
        "exchange_q",
    }
    if set(data) != expected:
        raise GovernanceError("STATE has unexpected or missing fields")
    if not _nullable_string(data["mission_id"]) or not _nullable_string(data["active_task"]):
        raise GovernanceError("STATE mission_id/active_task must be strings or null")
    if not isinstance(data["phase"], str) or not isinstance(data["next_action"], str):
        raise GovernanceError("STATE phase/next_action must be strings")
    if not isinstance(data["gates"], dict) or not all(
        isinstance(key, str) and isinstance(value, bool) for key, value in data["gates"].items()
    ):
        raise GovernanceError("STATE gates must map strings to booleans")
    if not _string_array(data["ready_tasks"]) or not _string_array(data["controlling_records"]):
        raise GovernanceError("STATE ready_tasks/controlling_records must be string arrays")
    exchange_q = data["exchange_q"]
    if not isinstance(exchange_q, int) or isinstance(exchange_q, bool) or exchange_q < 0:
        raise GovernanceError("STATE exchange_q must be a non-negative integer")


def _validate_approval(data: dict[str, object]) -> None:
    expected = {
        "skill_id",
        "name",
        "capability",
        "discovery_source",
        "provenance_tier",
        "canonical_source",
        "revision",
        "digest",
        "version",
        "license",
        "risk",
        "required_tools",
        "permissions",
        "dependencies",
        "audit",
        "approval",
        "status",
    }
    if set(data) != expected:
        raise GovernanceError("Skill approval template has unexpected or missing fields")
    nullable_fields = expected - {
        "canonical_source",
        "required_tools",
        "permissions",
        "dependencies",
        "audit",
        "approval",
    }
    if not all(_nullable_string(data[field]) for field in nullable_fields):
        raise GovernanceError("Skill approval scalar fields must be strings or null")
    if data["risk"] not in {None, "LOW", "MEDIUM", "HIGH"}:
        raise GovernanceError("Skill approval risk is invalid")
    if data["status"] is not None and data["status"] not in APPROVAL_STATUSES:
        raise GovernanceError("Skill approval status is invalid")
    for field in ("required_tools", "permissions", "dependencies"):
        if not _string_array(data[field]):
            raise GovernanceError(f"Skill approval {field} must be a string array")
    source = data["canonical_source"]
    if (
        not isinstance(source, dict)
        or set(source) != {"owner", "repository", "path"}
        or not all(_nullable_string(value) for value in source.values())
    ):
        raise GovernanceError("Skill approval canonical_source has invalid structure")
    audit = data["audit"]
    if not isinstance(audit, dict) or set(audit) != {"result", "exceptions"}:
        raise GovernanceError("Skill approval audit has invalid structure")
    if not _nullable_string(audit["result"]) or not _string_array(audit["exceptions"]):
        raise GovernanceError("Skill approval audit has invalid types")
    approval = data["approval"]
    if (
        not isinstance(approval, dict)
        or set(approval) != {"authority", "date"}
        or not all(_nullable_string(value) for value in approval.values())
    ):
        raise GovernanceError("Skill approval approval has invalid structure")


def _derived_state(
    target: Path, events: list[dict[str, object]] | None = None
) -> dict[str, object]:
    coordination = target / ".agent-coordination"
    plan = _parse_workplan(coordination)
    events = events if events is not None else _read_events(coordination / "EXCHANGE.jsonl")
    task_states = _validate_event_history(events, plan)
    effective = _effective_events(events)
    latest = effective[-1]
    active_tasks = [
        task_id
        for task_id, status in task_states.items()
        if status in {"READY", "IN_PROGRESS", "BLOCKED"}
    ]
    active_task = active_tasks[0] if active_tasks else None
    if len(active_tasks) > 1:
        raise GovernanceError("effective event frontier has parallel active tasks")
    if "n" in latest:
        next_action = latest["n"]
    elif active_task is not None:
        status = task_states[active_task]
        verb = {"READY": "Start", "IN_PROGRESS": "Continue", "BLOCKED": "Resolve blocker for"}[
            status
        ]
        next_action = f"{verb} {active_task}"
    elif all(status in TERMINAL_STATES for status in task_states.values()):
        next_action = "Close or archive mission"
    else:
        next_action = "Determine next eligible task"
    return {
        "protocol_version": _protocol_version(target / ".agent-governance" / "GOVERNANCE.md"),
        "mission_id": plan["mission_id"],
        "phase": plan["phase"],
        "gates": plan["gates"],
        "active_task": active_task,
        "ready_tasks": [task_id for task_id, status in task_states.items() if status == "READY"],
        "next_action": next_action,
        "controlling_records": plan["controlling_records"],
        "exchange_q": events[-1]["q"],
    }


def _state(target: Path, refresh: bool) -> None:
    _validate(target)
    coordination = target / ".agent-coordination"
    path = coordination / "STATE.json"
    current = _read_json(path)
    exchange = coordination / "EXCHANGE.jsonl"
    with _locked_exchange(exchange, exclusive=refresh) as stream:
        derived = _derived_state(target, _events_from_text(stream.read(), exchange))
        _validate_state(derived)
        if current != derived:
            if not refresh:
                raise GovernanceError(
                    "STATE is stale; rerun with --refresh after reviewing derived frontier"
                )
            _atomic_json(path, derived)
    print(json.dumps(derived, sort_keys=True))


def _event(target: Path, args: argparse.Namespace) -> None:
    _validate(target)
    coordination = target / ".agent-coordination"
    plan = _parse_workplan(coordination)
    path = coordination / "EXCHANGE.jsonl"
    with _locked_exchange(path, exclusive=True) as stream:
        content = stream.read()
        events = _events_from_text(content, path)
        _validate_event_history(events, plan)
        event: dict[str, object] = {
            "q": events[-1]["q"] + 1,
            "a": args.actor,
            "e": args.event,
        }
        for argument, field in (
            ("task", "k"),
            ("reference", "r"),
            ("verification", "v"),
            ("reason", "x"),
            ("next_action", "n"),
            ("risk", "z"),
            ("note", "m"),
            ("supersedes", "s"),
        ):
            value = getattr(args, argument)
            if value is not None:
                event[field] = value
        if event["a"] not in NEW_ACTORS:
            raise GovernanceError("new EXCHANGE events require a role actor")
        _validate_event_history([*events, event], plan)
        if content and not content.endswith("\n"):
            raise GovernanceError("EXCHANGE must end with a newline before append")
        stream.seek(0, os.SEEK_END)
        stream.write(json.dumps(event, separators=(",", ":"), sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps(event, sort_keys=True))


def _bounded_path(target: Path, raw_path: str, label: str) -> Path:
    path = Path(raw_path)
    path = path if path.is_absolute() else target / path
    resolved = path.resolve()
    if target != resolved and target not in resolved.parents:
        raise GovernanceError(f"{label} must be inside target repository")
    _required_file(path)
    return path


def _bounded_artifact(target: Path, raw_path: object, label: str) -> Path:
    if not isinstance(raw_path, str) or not raw_path or raw_path == ".":
        raise GovernanceError(f"{label} must be a non-empty repository-relative path")
    path = Path(raw_path)
    if path.is_absolute() or ".." in path.parts:
        raise GovernanceError(f"{label} must be inside target repository")
    resolved = (target / path).resolve()
    if target not in resolved.parents or not resolved.exists() or resolved.is_symlink():
        raise GovernanceError(f"{label} is missing or unsafe")
    return resolved


def _artifact_digest(path: Path) -> str:
    digest = hashlib.sha256()
    descendants = list(path.rglob("*")) if path.is_dir() else []
    symlinks = [item for item in descendants if item.is_symlink()]
    if symlinks:
        raise GovernanceError(f"Skill artifact contains unsafe symlink: {symlinks[0]}")
    files = [path] if path.is_file() else sorted(item for item in descendants if item.is_file())
    if not files:
        raise GovernanceError(f"Skill artifact has no files: {path}")
    for item in files:
        relative = item.name if path.is_file() else item.relative_to(path).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        try:
            digest.update(item.read_bytes())
        except OSError as error:
            raise GovernanceError(f"cannot hash Skill artifact {item}: {error}") from error
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def _identity(value: object, label: str) -> dict[str, object]:
    expected = {"canonical_source", "revision", "digest"}
    if not isinstance(value, dict) or set(value) != expected:
        raise GovernanceError(f"{label} has invalid identity structure")
    source = value["canonical_source"]
    if (
        not isinstance(source, dict)
        or set(source) != {"owner", "repository", "path"}
        or not all(isinstance(item, str) and item for item in source.values())
    ):
        raise GovernanceError(f"{label} has unresolved canonical source")
    if not all(isinstance(value[field], str) and value[field] for field in ("revision", "digest")):
        raise GovernanceError(f"{label} requires exact revision and digest")
    if value["revision"].lower() in {"main", "master", "develop", "latest", "head"}:
        raise GovernanceError(f"{label} revision must be immutable")
    return value


def _skill(target: Path, approval_raw: str, candidate_raw: str) -> None:
    _validate(target)
    approval_path = _bounded_path(target, approval_raw, "approval record")
    approval = _read_json(approval_path)
    candidate = _read_json(_bounded_path(target, candidate_raw, "candidate facts"))
    _validate_approval(approval)
    expected = {
        "skill_id",
        "name",
        "discovery_source",
        "provenance_tier",
        "canonical_source",
        "revision",
        "digest",
        "required_tools",
        "permissions",
        "dependencies",
        "selected_host_identity",
        "candidate_artifact",
        "selected_host_artifact",
    }
    if set(candidate) != expected:
        raise GovernanceError("candidate facts have unexpected or missing fields")
    candidate_identity = _identity(
        {
            "canonical_source": candidate["canonical_source"],
            "revision": candidate["revision"],
            "digest": candidate["digest"],
        },
        "candidate",
    )
    selected_identity = _identity(candidate["selected_host_identity"], "selected host")
    if approval["status"] != "APPROVED":
        raise GovernanceError("Skill approval record is not APPROVED")
    if (
        not isinstance(approval["skill_id"], str)
        or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", approval["skill_id"]) is None
    ):
        raise GovernanceError("Skill approval has unsafe skill_id")
    canonical_approval = target / ".agent-coordination" / "skills" / f"{approval['skill_id']}.json"
    if approval_path.resolve() != canonical_approval.resolve():
        raise GovernanceError("Skill approval must use canonical current record")
    audit = approval["audit"]
    authority = approval["approval"]
    if audit["result"] != "PASS" or not authority["authority"] or not authority["date"]:
        raise GovernanceError("Skill approval lacks passing audit and explicit authority")
    for field in ("skill_id", "name", "discovery_source", "provenance_tier"):
        if (
            not isinstance(candidate[field], str)
            or not candidate[field]
            or candidate[field] != approval[field]
        ):
            raise GovernanceError(f"candidate {field} does not match approval")
    approval_identity = {
        "canonical_source": approval["canonical_source"],
        "revision": approval["revision"],
        "digest": approval["digest"],
    }
    _identity(approval_identity, "approval")
    if candidate_identity != approval_identity or selected_identity != approval_identity:
        raise GovernanceError("candidate or selected host identity does not match exact approval")
    candidate_artifact = _bounded_artifact(
        target, candidate["candidate_artifact"], "candidate artifact"
    )
    selected_artifact = _bounded_artifact(
        target, candidate["selected_host_artifact"], "selected host artifact"
    )
    for label, artifact in (
        ("candidate", candidate_artifact),
        ("selected host", selected_artifact),
    ):
        if _artifact_digest(artifact) != approval["digest"]:
            raise GovernanceError(f"{label} artifact digest does not match exact approval")
    for field in ("required_tools", "permissions", "dependencies"):
        if not _string_array(candidate[field]) or not set(candidate[field]) <= set(approval[field]):
            raise GovernanceError(f"candidate {field} exceeds approved envelope")
    print(json.dumps({"skill_id": approval["skill_id"], "status": "VALID"}, sort_keys=True))


def _classify_capabilities(
    target: Path, facts: dict[str, object], version: str
) -> dict[str, object]:
    if set(facts) != {"capabilities"} or not isinstance(facts["capabilities"], list):
        raise GovernanceError("ecosystem facts must contain only a capabilities array")
    classified: list[dict[str, object]] = []
    seen: set[str] = set()
    expected = {
        "id",
        "category",
        "provider",
        "scope",
        "evidence",
        "provider_present",
        "need_covered",
        "adapter_required",
        "responsibilities_distinct",
        "authority_overlap",
        "managed_surfaces",
        "control_reference",
    }
    coordination = target / ".agent-coordination"
    events = _read_events(coordination / "EXCHANGE.jsonl")
    _validate_event_history(events, _parse_workplan(coordination))
    for index, fact in enumerate(facts["capabilities"]):
        if not isinstance(fact, dict) or set(fact) != expected:
            raise GovernanceError(f"ecosystem fact {index} has unexpected or missing fields")
        capability_id = fact["id"]
        if not isinstance(capability_id, str) or not capability_id or capability_id in seen:
            raise GovernanceError(f"ecosystem fact {index} has invalid or duplicate id")
        seen.add(capability_id)
        if not all(isinstance(fact[field], str) and fact[field] for field in ("category", "scope")):
            raise GovernanceError(f"ecosystem fact {capability_id} has invalid metadata")
        if not all(
            isinstance(fact[field], bool)
            for field in (
                "provider_present",
                "need_covered",
                "adapter_required",
                "responsibilities_distinct",
                "authority_overlap",
            )
        ):
            raise GovernanceError(f"ecosystem fact {capability_id} has non-boolean signals")
        if not _string_array(fact["managed_surfaces"]):
            raise GovernanceError(f"ecosystem fact {capability_id} has invalid managed surfaces")
        for surface in fact["managed_surfaces"]:
            _bounded_artifact(target, surface, f"ecosystem fact {capability_id} managed surface")
        present = fact["provider_present"]
        covered = fact["need_covered"]
        adapter = fact["adapter_required"]
        distinct = fact["responsibilities_distinct"]
        overlap = fact["authority_overlap"]
        if not present:
            if any((covered, adapter, distinct, overlap)) or fact["provider"] is not None:
                raise GovernanceError(f"ecosystem fact {capability_id} is contradictory")
            classification = "MISSING"
        elif (
            not isinstance(fact["provider"], str)
            or not fact["provider"]
            or not isinstance(fact["evidence"], str)
            or not fact["evidence"]
        ):
            raise GovernanceError(f"ecosystem fact {capability_id} lacks provider evidence")
        elif overlap:
            classification = "CONFLICT"
        elif distinct and not adapter:
            classification = "COEXIST"
        elif covered and adapter and not distinct:
            classification = "ADAPT"
        elif covered and not adapter and not distinct:
            classification = "REUSE"
        else:
            raise GovernanceError(f"ecosystem fact {capability_id} is mechanically ambiguous")
        if present:
            _bounded_artifact(target, fact["evidence"], f"ecosystem fact {capability_id} evidence")
            control_reference = fact["control_reference"]
            if isinstance(control_reference, str) and control_reference.startswith("exchange:"):
                sequence = control_reference.removeprefix("exchange:")
                controlling_events = {
                    event["q"]
                    for event in _effective_events(events)
                    if event["e"] in {"decision", "scope_change"}
                }
                if not sequence.isdigit() or int(sequence) not in controlling_events:
                    raise GovernanceError(
                        f"ecosystem fact {capability_id} has invalid EXCHANGE control reference"
                    )
            else:
                _bounded_artifact(
                    target,
                    control_reference,
                    f"ecosystem fact {capability_id} control reference",
                )
        elif fact["evidence"] is not None or fact["control_reference"] is not None:
            raise GovernanceError(f"ecosystem fact {capability_id} is contradictory")
        classified.append(
            {
                "id": capability_id,
                "category": fact["category"],
                "provider": fact["provider"],
                "scope": fact["scope"],
                "evidence": fact["evidence"],
                "classification": classification,
                "managed_surfaces": fact["managed_surfaces"],
                "control_reference": fact["control_reference"],
            }
        )
    return {"protocol_version": version, "capabilities": classified}


def _ecosystem(target: Path, facts_raw: str, update: bool) -> None:
    _validate(target)
    facts = _read_json(_bounded_path(target, facts_raw, "ecosystem facts"))
    path = target / ".agent-coordination" / "CAPABILITIES.json"
    classified = _classify_capabilities(
        target,
        facts,
        _protocol_version(target / ".agent-governance" / "GOVERNANCE.md"),
    )
    current = _read_json(path)
    if current != classified:
        if not update:
            raise GovernanceError(
                "CAPABILITIES is stale; rerun with --update after reviewing output"
            )
        _atomic_json(path, classified)
    print(json.dumps(classified, sort_keys=True))


def _archive(target: Path, prepare: bool) -> None:
    _validate(target)
    coordination = target / ".agent-coordination"
    exchange = coordination / "EXCHANGE.jsonl"
    with _locked_exchange(exchange, exclusive=prepare) as stream:
        plan = _parse_workplan(coordination)
        exchange_content = stream.read()
        events = _events_from_text(exchange_content, exchange)
        if plan["mission_status"] not in {"COMPLETED", "CANCELLED"}:
            raise GovernanceError("mission is not authoritatively completed or cancelled")
        task_states = _validate_event_history(events, plan)
        active_tasks = [
            task_id
            for task_id, status in task_states.items()
            if status in {"READY", "IN_PROGRESS", "BLOCKED"}
        ]
        if active_tasks:
            raise GovernanceError("mission has active task or blocker")
        unresolved = [
            task_id for task_id, status in task_states.items() if status not in TERMINAL_STATES
        ]
        if unresolved:
            raise GovernanceError(f"mission has unresolved tasks: {', '.join(unresolved)}")
        for task_id in plan["tasks"]:
            task_record = coordination / "tasks" / f"{task_id}.md"
            _required_file(task_record)
            if _metadata(_nonempty_text(task_record), "Task-ID", task_record) != task_id:
                raise GovernanceError(f"task record ID mismatch for {task_id}")
        current_state = _read_json(coordination / "STATE.json")
        derived_state = _derived_state(target, events)
        if current_state != derived_state:
            raise GovernanceError("STATE is stale; refresh it before archival")
        destination = coordination / "archive" / plan["mission_id"]
        if destination.exists() or destination.is_symlink():
            raise GovernanceError("mission archive already exists")
        if not prepare:
            print(json.dumps({"mission_id": plan["mission_id"], "archive": "SAFE"}, sort_keys=True))
            return
        archive_root = coordination / "archive"
        created_archive_root = not archive_root.exists()
        archive_root.mkdir(exist_ok=True)
        temporary = Path(tempfile.mkdtemp(prefix=f".{plan['mission_id']}.", dir=archive_root))
        try:
            for name in (
                "MISSION.md",
                "WORKPLAN.md",
                "STATE.json",
                "CAPABILITIES.json",
            ):
                shutil.copyfile(coordination / name, temporary / name)
            _atomic_write(temporary / "EXCHANGE.jsonl", exchange_content)
            for name in COORDINATION_DIRS:
                shutil.copytree(coordination / name, temporary / name)
            temporary.replace(destination)
            if os.name != "nt":
                directory_fd = os.open(archive_root, os.O_RDONLY)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
        except Exception:
            shutil.rmtree(temporary, ignore_errors=True)
            if created_archive_root:
                archive_root.rmdir()
            raise
        _atomic_write(coordination / "MISSION.md", MISSION_TEMPLATE)
        _atomic_write(coordination / "WORKPLAN.md", WORKPLAN_TEMPLATE)
        _atomic_json(
            coordination / "STATE.json",
            {
                "protocol_version": current_state["protocol_version"],
                "mission_id": None,
                "phase": "F0",
                "gates": {},
                "active_task": None,
                "ready_tasks": [],
                "next_action": "Obtain Human-approved mission inputs",
                "controlling_records": [],
                "exchange_q": 1,
            },
        )
        _atomic_json(
            coordination / "CAPABILITIES.json",
            {"protocol_version": current_state["protocol_version"], "capabilities": []},
        )
        for path in (coordination / "tasks").iterdir():
            if path.name != "TASK.template.md":
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
        for path in (coordination / "decisions").iterdir():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
        stream.seek(0)
        stream.truncate()
        stream.write(EXCHANGE_TEMPLATE)
        stream.flush()
        os.fsync(stream.fileno())
    print(
        json.dumps({"mission_id": plan["mission_id"], "archive": str(destination)}, sort_keys=True)
    )


def _validate_core(core: Path) -> str:
    for name in CORE_FILES:
        _nonempty_text(core / name)
    version = _protocol_version(core / "GOVERNANCE.md")
    governance_text = _nonempty_text(core / "GOVERNANCE.md")
    references = set(re.findall(r"`\.agent-governance/([A-Z][A-Z-]*\.md)`", governance_text))
    if references != set(CORE_FILES):
        raise GovernanceError("GOVERNANCE routed Core references do not match required Core files")
    for name, field in CORE_VERSION_FIELDS.items():
        _version_declaration(core / name, field)
    return version


def _validate_assets(assets: Path, version: str) -> None:
    for name in ("MISSION.template.md", "WORKPLAN.template.md", "TASK.template.md"):
        _nonempty_text(assets / name)
    capabilities = _read_json(assets / "CAPABILITIES.template.json")
    state = _read_json(assets / "STATE.template.json")
    approval = _read_json(assets / "SKILL-APPROVAL.template.json")
    _validate_capabilities(capabilities)
    _validate_state(state)
    _validate_approval(approval)
    if capabilities["protocol_version"] != version or state["protocol_version"] != version:
        raise GovernanceError(
            f"package asset protocol_version does not match Governance Core {version}"
        )
    _validate_jsonl(assets / "EXCHANGE.template.jsonl")


def _validate(target: Path) -> None:
    present_markers = [
        name for name in SOURCE_MARKERS if (target / name).exists() or (target / name).is_symlink()
    ]
    if present_markers:
        raise GovernanceError(
            f"source/consumer separation violation; found: {', '.join(present_markers)}"
        )

    core = target / ".agent-governance"
    coordination = target / ".agent-coordination"
    _required_dir(core)
    _required_dir(coordination)
    for name in CORE_FILES:
        _required_file(core / name)
    unexpected_core = sorted(path.name for path in core.iterdir() if path.name not in CORE_FILES)
    if unexpected_core:
        raise GovernanceError(f"ambiguous Governance Core contents: {', '.join(unexpected_core)}")

    for name in COORDINATION_DIRS:
        _required_dir(coordination / name)
    for relative_target in ASSET_TARGETS.values():
        _required_file(coordination / relative_target)

    expected_coordination = {
        "MISSION.md",
        "WORKPLAN.md",
        "CAPABILITIES.json",
        "STATE.json",
        "EXCHANGE.jsonl",
        *COORDINATION_DIRS,
    }
    if (coordination / "archive").is_dir() and not (coordination / "archive").is_symlink():
        expected_coordination.add("archive")
    unexpected_coordination = sorted(
        path.name for path in coordination.iterdir() if path.name not in expected_coordination
    )
    if unexpected_coordination:
        raise GovernanceError(
            f"ambiguous coordination root contents: {', '.join(unexpected_coordination)}"
        )
    unsafe_symlinks = sorted(
        str(path.relative_to(target))
        for root in (core, coordination)
        for path in root.rglob("*")
        if path.is_symlink()
    )
    if unsafe_symlinks:
        raise GovernanceError(f"unsafe managed symlinks: {', '.join(unsafe_symlinks)}")

    version = _validate_core(core)

    capabilities = _read_json(coordination / "CAPABILITIES.json")
    state = _read_json(coordination / "STATE.json")
    approval = _read_json(coordination / "skills" / "SKILL-APPROVAL.template.json")
    _validate_capabilities(capabilities)
    _validate_state(state)
    _validate_approval(approval)
    if capabilities.get("protocol_version") != version or state.get("protocol_version") != version:
        raise GovernanceError(
            f"Core/reference/version inconsistency; expected protocol_version {version}"
        )
    exchange_q = state["exchange_q"]
    latest_q = _validate_jsonl(coordination / "EXCHANGE.jsonl")
    if exchange_q > latest_q:
        raise GovernanceError("STATE exchange_q is ahead of EXCHANGE history")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="governance.py")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("bootstrap", "validate"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("target", help="existing consumer repository directory")
    state = subparsers.add_parser("state")
    state.add_argument("target")
    state.add_argument("--refresh", action="store_true")
    event = subparsers.add_parser("event")
    event.add_argument("target")
    event.add_argument("--actor", required=True, choices=sorted(NEW_ACTORS))
    event.add_argument("--event", required=True, choices=sorted(EVENTS))
    event.add_argument("--task")
    event.add_argument("--reference")
    event.add_argument("--verification")
    event.add_argument("--reason")
    event.add_argument("--next-action")
    event.add_argument("--risk")
    event.add_argument("--supersedes", type=int)
    event.add_argument("--note")
    skill = subparsers.add_parser("skill")
    skill.add_argument("target")
    skill.add_argument("--approval", required=True)
    skill.add_argument("--candidate", required=True)
    ecosystem = subparsers.add_parser("ecosystem")
    ecosystem.add_argument("target")
    ecosystem.add_argument("--facts", required=True)
    ecosystem.add_argument("--update", action="store_true")
    archive = subparsers.add_parser("archive")
    archive.add_argument("target")
    archive.add_argument("--prepare", action="store_true")
    return parser


def main(argv: list[str] | None = None, *, package_paths: tuple[Path, Path]) -> int:
    args = _parser().parse_args(argv)
    try:
        target = _safe_target(args.target)
        if args.command == "bootstrap":
            _bootstrap(target, package_paths)
            print(f"bootstrapped and validated Governance at {target}")
        elif args.command == "validate":
            _validate(target)
            print(f"validated Governance at {target}")
        elif args.command == "state":
            _state(target, args.refresh)
        elif args.command == "event":
            _event(target, args)
        elif args.command == "skill":
            _skill(target, args.approval, args.candidate)
        elif args.command == "ecosystem":
            _ecosystem(target, args.facts, args.update)
        else:
            _archive(target, args.prepare)
    except (GovernanceError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0
