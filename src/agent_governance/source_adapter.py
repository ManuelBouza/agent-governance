"""Fail-closed adapter for the Agent Governance source repository."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

SOURCE_SIGNAL_FILENAME = "agent-governance-source.json"
SOURCE_SIGNAL_SCHEMA_VERSION = "1.0.0"
SOURCE_PRODUCT_ID = "agent-governance"
SOURCE_PROFILE = "source-maintainer"

SOURCE_RECORDS = {
    "branching_policy": "docs/BRANCHING.md",
    "conformance_oracle_contract": "docs/CONFORMANCE-ORACLE-CONTRACT.md",
    "consumer_skill": "governance-skill",
    "core": "governance-core",
    "decisions": "docs/decisions",
    "development_workflow": "docs/DEVELOPMENT-WORKFLOW.md",
    "evals": "evals",
    "executor_handoff_policy": "docs/EXECUTOR-HANDOFFS.md",
    "executor_handoffs": "handoffs",
    "local_development_toolchain": "docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md",
    "maintainer_skill": "maintainer-skill",
    "orchestrator_checkpoint": "docs/orchestrator/CHECKPOINT.md",
    "refactoring_workflow": "docs/REFACTORING-WORKFLOW.md",
    "release_policy": "docs/RELEASES.md",
    "repository_instructions": "AGENTS.md",
    "task_contract_policy": "docs/TASK-CONTRACTS.md",
    "task_contracts": "docs/tasks",
    "testing_and_evaluation": "docs/TESTING-AND-EVALUATION.md",
    "testing_skill_capabilities": "docs/TESTING-SKILL-CAPABILITIES.md",
    "tests": "tests",
}
SOURCE_RECORD_NAMES = frozenset(SOURCE_RECORDS)
_DIRECTORY_RECORDS = frozenset(
    {
        "consumer_skill",
        "core",
        "decisions",
        "evals",
        "executor_handoffs",
        "maintainer_skill",
        "task_contracts",
        "tests",
    }
)
_CONSUMER_ROOTS = (".agent-governance", ".agent-coordination")
_SIGNAL_FIELDS = {"signal_schema_version", "product_id", "profile"}


class SourceContextError(Exception):
    """Fail-closed source-context routing error."""


@dataclass(frozen=True)
class SourceContext:
    """Validated source-maintainer context over legacy source records."""

    root: Path
    signal_schema_version: str

    def record(self, name: str) -> Path:
        """Resolve a named read-only source record."""

        try:
            relative = SOURCE_RECORDS[name]
        except (KeyError, TypeError) as error:
            raise SourceContextError(f"unsupported source record: {name!r}") from error
        return self.root / relative

    def handoff_write_path(self, relative: str | Path) -> Path:
        """Resolve a non-Markdown handoff target without writing it."""

        candidate_relative = Path(relative)
        if candidate_relative.is_absolute() or any(
            part in {"", ".", ".."} for part in candidate_relative.parts
        ):
            raise SourceContextError(f"unsafe source write path: {relative!r}")
        candidate = (self.root / candidate_relative).resolve()
        try:
            normalized = candidate.relative_to(self.root)
        except ValueError as error:
            raise SourceContextError(f"source write escapes repository: {relative!r}") from error
        if (
            len(normalized.parts) != 2
            or normalized.parts[0] != "handoffs"
            or candidate.suffix.casefold() != ".json"
        ):
            raise SourceContextError(
                "source-maintainer adapter writes are limited to handoffs/*.json"
            )
        return candidate


def _unsafe_link(path: Path) -> bool:
    return path.is_symlink() or path.is_junction()


def _source_root(target: str | Path) -> Path:
    root = Path(target).expanduser()
    if _unsafe_link(root) or not root.is_dir():
        raise SourceContextError(
            f"source target must be an existing, non-symlink directory: {root}"
        )
    return root.resolve()


def _read_signal(root: Path) -> dict[str, object]:
    signal = root / SOURCE_SIGNAL_FILENAME
    if _unsafe_link(signal) or not signal.is_file():
        raise SourceContextError(f"missing or unsafe explicit source-product signal: {signal}")
    try:
        value = json.loads(signal.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeError) as error:
        raise SourceContextError(f"invalid source-product signal {signal}: {error}") from error
    if not isinstance(value, dict) or set(value) != _SIGNAL_FIELDS:
        raise SourceContextError("source-product signal has unexpected or missing fields")
    expected = {
        "signal_schema_version": SOURCE_SIGNAL_SCHEMA_VERSION,
        "product_id": SOURCE_PRODUCT_ID,
        "profile": SOURCE_PROFILE,
    }
    if value != expected:
        raise SourceContextError("source-product signal identity or version is unsupported")
    return value


def resolve_source_context(target: str | Path) -> SourceContext:
    """Resolve source-maintainer context only from the explicit signal."""

    root = _source_root(target)
    signal = _read_signal(root)
    consumer_roots = [
        name for name in _CONSUMER_ROOTS if (root / name).exists() or _unsafe_link(root / name)
    ]
    if consumer_roots:
        raise SourceContextError(
            "ambiguous source/consumer context; found: " + ", ".join(consumer_roots)
        )
    missing_or_unsafe = []
    for name, relative in SOURCE_RECORDS.items():
        record = root / relative
        expected_type_present = record.is_dir() if name in _DIRECTORY_RECORDS else record.is_file()
        if not expected_type_present or _unsafe_link(record):
            missing_or_unsafe.append(relative)
    if missing_or_unsafe:
        raise SourceContextError(
            "source repository is missing required legacy records: "
            + ", ".join(sorted(missing_or_unsafe))
        )
    return SourceContext(
        root=root,
        signal_schema_version=str(signal["signal_schema_version"]),
    )


def source_context_payload(context: SourceContext, record: str | None = None) -> dict[str, object]:
    """Return a deterministic source-context routing description."""

    payload: dict[str, object] = {
        "profile": SOURCE_PROFILE,
        "product_id": SOURCE_PRODUCT_ID,
        "signal_schema_version": context.signal_schema_version,
        "root": str(context.root),
    }
    if record is None:
        payload["records"] = {
            name: str(context.record(name)) for name in sorted(SOURCE_RECORD_NAMES)
        }
    else:
        payload["record"] = record
        payload["path"] = str(context.record(record))
    return payload
