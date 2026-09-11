"""Frozen T063 v3 experiment configuration and shared types."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

FROZEN_HEAD = "69e910f329a2294c3b40df0f6ee983f9905f4677"
REQUIRED_CODEX_VERSION = "0.153.4"
ROOT_MODEL = "gpt-5.6-sol"
ROOT_REASONING = "medium"
EVIDENCE_BRANCH = "test/t063-adaptive-worker-routing-requalification-v3"
HISTORICAL_BLOCKED_HEADS = (
    "3d8a9460988351383a90adfc6b76e2deff056504",
    "3ff745a8d29e031ca818c1bc618b15a54e0cbf2b",
)

# Version-sensitive upstream revalidation performed by R021:
# 0.154.0 stable and 0.155.0-alpha.2 preserve the same blocking V2
# spawn/message observability semantics, so the D063-qualified 0.153.4
# reference remains pinned for this experiment.
UPSTREAM_REVALIDATED_VERSIONS = ("0.153.4", "0.154.0", "0.155.0-alpha.2")

APP_SERVER_CONFIG_OVERRIDES = (
    "features.multi_agent=true",
    "features.multi_agent_v2.enabled=true",
    "features.multi_agent_v2.expose_spawn_agent_model_overrides=false",
    "features.multi_agent_v2.hide_spawn_agent_metadata=true",
)

EXPECTED_TASK_MESSAGE_DIGESTS = {
    "P1": "9aa60aef807873669690a2ad2b564fed58e0731ff0d6e0162fbef40c621a2164",
    "P2": "031c06d7544f6146901e633d4bceb8af0e15325c0124dc586e10f545aaadfe4a",
    "P3": "9d980424d08517c72911eaacaa9cee36ddf2003d50c21ad6b4d0c25786d9554f",
}

P1_PATHS = (
    ".python-version",
    "agent-governance-source.json",
    "pyproject.toml",
    "code-health.json",
    "src/agent_governance/profile.py",
    "src/agent_governance/source_adapter.py",
)
P2_FILES = (
    "src/agent_governance/__init__.py",
    "src/agent_governance/artifact.py",
    "src/agent_governance/engine.py",
    "src/agent_governance/profile.py",
    "src/agent_governance/source_adapter.py",
)
P2_SYMBOLS = (
    "ArtifactBuildError",
    "build_artifact",
    "Profile",
    "resolve_profile",
    "SourceContext",
    "_bootstrap",
)
P3_SEED_PATH = "src/agent_governance/profile.py"
P3_SEED_BLOB = "1e3ae205b4350adc18a2f3f5d631dd739056ba34"
P3_EXPECTED_FIXTURE_SHA256 = "cd82af740a51e9137eb43903d581e0969e3a8841585c853788bdf4b97c850617"

ARM_ORDER = (
    ("P1", "ADAPTIVE", "gpt-5.6-luna", "medium"),
    ("P1", "CONTROL", "gpt-5.6-sol", "medium"),
    ("P2", "CONTROL", "gpt-5.6-sol", "medium"),
    ("P2", "ADAPTIVE", "gpt-5.6-terra", "medium"),
    ("P3", "ADAPTIVE", "gpt-5.6-terra", "high"),
    ("P3", "CONTROL", "gpt-5.6-sol", "medium"),
)

FORBIDDEN_CHILD_TOOL_FRAGMENTS = (
    "docs/tasks/t063",
    "docs/reviews/t063",
    "docs/decisions/d063",
    "docs/research/r007",
    "docs/research/r018",
    "docs/research/r019",
    "docs/research/r020",
    "docs/research/r021",
    "adaptive_worker_routing",
    "adaptive_worker_routing_v3",
    "t063_harness",
)

P1_TASK = """At frozen Git commit {head}, inspect only the six supplied tracked paths and return, for each path, the exact Git blob SHA, byte size from Git object metadata, and exists_at_frozen_head true/false. Also return the exact frozen HEAD evaluated and concise evidence commands/APIs used. Use Git/object metadata rather than filesystem size or inference. Do not modify repository state and do not inspect T063 task/review/oracle documents.

Paths, in required order:
{paths}

Return only compact JSON with keys frozen_head, files, and evidence. Each files item must contain path, blob_sha, byte_size, and exists_at_frozen_head.
"""

P2_TASK = """At frozen Git commit {head}, analyze only the supplied five Python files. A dependency edge is only an ast.Import or ast.ImportFrom relationship resolving between two files in that exact scope; exclude runtime/package-bootstrap/discovery effects and every external import. Return the sorted exact internal edge set, whether that graph is acyclic, the owning module for each of the six supplied symbols, and concise reproducible evidence. Do not modify repository state and do not inspect T063 task/review/oracle documents.

Files, in required order:
{files}

Symbols, in required order:
{symbols}

Return only compact JSON with keys edges, acyclic, symbol_owners, and evidence. Represent each edge as a two-element [source_module, target_module] array.
"""

P3_TASK = """Review only the supplied Python fixture for one material correctness or security defect. Return status; material findings with severity; mechanism/evidence; minimal reproduction or proof direction; and minimal fix direction. Do not modify the fixture or repository. Do not inspect repository task, review, research, decision or oracle documents; use only the supplied fixture as substantive input.

Fixture:
profile_fixture.py

Return only compact JSON with keys status and findings. Each material finding must contain severity, mechanism, evidence, reproduction, and fix_direction.
"""

PARENT_INSTRUCTIONS = """You are a transport-only measurement parent for one frozen Agent Governance probe.
Do not solve or inspect the probe.
Use spawn_agent exactly once.
Use exactly the task_name, message and fork_turns supplied in the user turn.
Set fork_turns to "none".
Do not provide agent_type, model, reasoning_effort, fork_context or any extra spawn argument.
Do not use repository/file/shell/network tools.
After spawn_agent succeeds, return only the exact text PARENT_SPAWNED.
"""


class HarnessError(RuntimeError):
    """Base fail-closed harness error."""


class MeasurementSurfaceBlocked(HarnessError):
    """D063 mandatory measurement surface is unavailable."""


class ProfileResolutionBlocked(HarnessError):
    """Requested child model/reasoning did not resolve exactly."""


class ExecutionInvalid(HarnessError):
    """Scored execution became invalid without a quality result."""


@dataclass(frozen=True)
class ArmSpec:
    probe: str
    arm: str
    model: str
    reasoning: str

    @property
    def requested_profile(self) -> str:
        return f"{self.model} / {self.reasoning}"

    @property
    def task_name(self) -> str:
        return f"t063_{self.probe.lower()}_{self.arm.lower()}"

    @property
    def contract_nonce(self) -> str:
        seed = f"T063-v3-contract|{self.probe}|{self.arm}|{self.model}|{self.reasoning}"
        return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:32]

    @property
    def spawn_trigger(self) -> str:
        seed = f"T063-v3-trigger|{self.probe}|{self.arm}|{self.model}|{self.reasoning}"
        return "T063_TRIGGER_" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:32]


@dataclass(frozen=True)
class PreparedInputs:
    p1_oracle: dict[str, Any]
    p2_oracle: dict[str, Any]
    p3_oracle: dict[str, Any]
    p3_fixture: Path
    task_messages: dict[str, str]
    task_message_digests: dict[str, str]


def build_task_messages() -> dict[str, str]:
    return {
        "P1": P1_TASK.format(head=FROZEN_HEAD, paths="\n".join(P1_PATHS)),
        "P2": P2_TASK.format(
            head=FROZEN_HEAD,
            files="\n".join(P2_FILES),
            symbols="\n".join(P2_SYMBOLS),
        ),
        "P3": P3_TASK,
    }


def build_child_contract(spec: ArmSpec, task_message: str, task_digest: str) -> str:
    """Build the harness-controlled child developer contract.

    The substantive frozen task is unchanged. The wrapper adds only measurement
    attestation fields, and intentionally omits the expected spawn trigger so
    the child must report the inter-agent transport it actually received.
    """
    return f"""You are the scored worker for one T063 v3 arm.

Authority and isolation:
- Execute only the frozen task below.
- Treat the inter-agent spawn message that initiated this turn as transport only.
- Do not use inherited parent history as task authority.
- Do not inspect T063 task/review/research/decision/oracle material.
- Do not modify any file.

Measurement receipt:
Your final JSON MUST preserve every top-level key required by the frozen task and MUST additionally contain:
"t063_receipt": {{
  "contract_nonce": "{spec.contract_nonce}",
  "task_message_sha256": "{task_digest}",
  "spawn_trigger_received": "<exact inter-agent spawn message text that initiated this turn>"
}}

The expected spawn-trigger text is intentionally not repeated in this developer contract. Report what you actually received; do not infer or substitute it.

--- FROZEN TASK BEGIN ---
{task_message}
--- FROZEN TASK END ---
"""


def build_parent_turn_message(spec: ArmSpec) -> str:
    return (
        f"task_name={spec.task_name}\n"
        f"message={spec.spawn_trigger}\n"
        'fork_turns="none"\n'
        "Spawn exactly one child with those exact values, then return PARENT_SPAWNED."
    )


def per_arm_thread_config(spec: ArmSpec, child_contract: str) -> dict[str, Any]:
    return {
        "model_reasoning_effort": ROOT_REASONING,
        "agents.default_subagent_model": spec.model,
        "agents.default_subagent_reasoning_effort": spec.reasoning,
        "features.multi_agent_v2.subagent_developer_instructions": child_contract,
        "features.multi_agent_v2.expose_spawn_agent_model_overrides": False,
        "features.multi_agent_v2.hide_spawn_agent_metadata": True,
    }
