#!/usr/bin/env python3
"""Safe bootstrap and structural validation for consumer Governance installs."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

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


class GovernanceError(Exception):
    """Expected fail-closed CLI error."""


def _package_paths() -> tuple[Path, Path]:
    skill = Path(__file__).resolve().parents[1]
    return skill.parent / "governance-core", skill / "assets"


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


def _bootstrap(target: Path) -> None:
    core_source, assets = _package_paths()
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
        _validate(target)
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        target = _safe_target(args.target)
        if args.command == "bootstrap":
            _bootstrap(target)
            print(f"bootstrapped and validated Governance at {target}")
        else:
            _validate(target)
            print(f"validated Governance at {target}")
    except (GovernanceError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
