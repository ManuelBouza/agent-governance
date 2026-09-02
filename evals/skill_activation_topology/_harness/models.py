"""Extracted MG1 topology harness implementation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent.parent


REPO_ROOT = HERE.parents[1]


HARNESS_PATH = HERE / "harness.py"


ORACLE_PATH = HERE / "oracle.json"


CORPUS_PATH = HERE / "corpus.json"


TOPOLOGIES_PATH = HERE / "topologies.json"


MANIFEST_PATH = HERE / "presentations" / "manifest.json"


ENVELOPE_PATH = HERE / "trial-envelope.json"


ALLOWED_OUTCOMES = {"activate", "no-activation", "bounded-rejection", "clarify-context"}


ACTIVATION_RELEVANT_CLASSES = {
    "positive-consumer",
    "positive-source-maintainer",
    "positive-external-skill-trust",
    "cross-profile",
    "ambiguous",
    "multi-intent",
}


NEGATIVE_CLASSES = {"negative", "near-miss"}


V10_CLASS_ORDER = (
    "cross-profile",
    "ambiguous",
    "negative",
    "near-miss",
    "positive-consumer",
    "positive-source-maintainer",
    "positive-external-skill-trust",
    "multi-intent",
)


MINIMAL_DISABLED_FEATURES = (
    "apps",
    "remote_plugin",
    "multi_agent",
    "skill_mcp_dependency_install",
    "shell_snapshot",
    "standalone_web_search",
)


CANARY_NONCE = "The quartz heron carries seven indigo pebbles at noon."


BACKEND_PROBE_NONCE = "T023_WINDOWS_SANDBOX_BACKEND_READY"


WORKSPACE_PROBE_FILENAME = "workspace-probe.txt"


WORKSPACE_PROBE_NONCE = "T023_V10_WORKSPACE_READABLE"


WORKSPACE_FACTORY_ID = "windows-inherited-acl-mkdir-v1"


REQUIRED_CODEX_VERSION = "codex-cli 0.149.0"


WINDOWS_BACKEND_ORDER = ("elevated", "unelevated")


TRIAL_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "activated_entrypoints": {"type": "array", "items": {"type": "string"}},
        "semantic_outcome": {"type": "string", "enum": sorted(ALLOWED_OUTCOMES)},
        "granted_capabilities": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ["consumer-lifecycle", "source-maintainer", "external-skill-trust"],
            },
        },
        "permission_broadening": {"type": "boolean"},
        "response_summary": {"type": "string"},
    },
    "required": [
        "activated_entrypoints",
        "semantic_outcome",
        "granted_capabilities",
        "permission_broadening",
        "response_summary",
    ],
}


CANARY_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "properties": {"body_nonce": {"type": "string"}},
    "required": ["body_nonce"],
}


class HarnessError(RuntimeError):
    """Fail-closed error for malformed frozen inputs or unusable live evidence."""


class AttemptFailure(HarnessError):
    """An unscored attempt, including its visible execution evidence."""

    def __init__(self, failure_class: str, message: str, raw: dict[str, Any]):
        super().__init__(message)
        self.failure_class = failure_class
        self.raw = raw


class CapacityPause(HarnessError):
    """An explicit provider/account capacity event that consumes no model attempt."""

    def __init__(self, message: str, raw: dict[str, Any]):
        super().__init__(message)
        self.raw = raw


class HostSurfaceDrift(HarnessError):
    """An unscored host-profile drift that forbids retry and new scheduling."""

    def __init__(self, message: str, raw: dict[str, Any]):
        super().__init__(message)
        self.raw = raw


@dataclass(frozen=True)
class FrozenInputs:
    oracle: dict[str, Any]
    corpus: dict[str, Any]
    topologies: dict[str, Any]
    manifest: dict[str, Any]
    envelope: dict[str, Any]


@dataclass(frozen=True)
class TrialSpec:
    case: dict[str, Any]
    candidate_id: str
    repetition: int

    @property
    def key(self) -> str:
        return f"{self.case['id']}--{self.candidate_id}--r{self.repetition}"
