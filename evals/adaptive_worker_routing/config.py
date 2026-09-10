"""Frozen T063 v2 experiment configuration and shared types."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

FROZEN_HEAD = "69e910f329a2294c3b40df0f6ee983f9905f4677"
REQUIRED_CODEX_VERSION = "0.153.4"
ROOT_MODEL = "gpt-5.6-sol"
ROOT_REASONING = "medium"
EVIDENCE_BRANCH = "test/t063-adaptive-worker-routing-requalification-v2"
HISTORICAL_BLOCKED_HEAD = "3d8a9460988351383a90adfc6b76e2deff056504"

APP_SERVER_CONFIG_OVERRIDES = (
    "features.multi_agent=true",
    "features.multi_agent_v2.enabled=true",
    "features.multi_agent_v2.expose_spawn_agent_model_overrides=true",
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
    "adaptive_worker_routing",
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

PARENT_INSTRUCTIONS = """You are a measurement parent for one frozen Agent Governance probe.
Do not solve the probe yourself and do not inspect repository files for the answer.
Use the collaboration spawn_agent tool exactly once with the exact task_name, child model, and reasoning_effort stated in this turn.
Pass the supplied child task message unchanged as the child message.
Set fork_turns to "none". Multi-Agent V2 does not accept fork_context.
Wait for that exact child to finish, then return only the child's final answer without commentary.
Do not create files or modify repository state.
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
