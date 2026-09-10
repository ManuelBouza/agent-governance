from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from evals.adaptive_worker_routing.app_server import Notification
from evals.adaptive_worker_routing import config as c
from evals.adaptive_worker_routing import measurement as m
from evals.adaptive_worker_routing import oracles as o
from evals.adaptive_worker_routing import runner as r


def test_module_for_path() -> None:
    assert o.module_for_path("src/agent_governance/engine.py") == "agent_governance.engine"
    assert o.module_for_path("src/agent_governance/__init__.py") == "agent_governance"


def test_resolve_import_targets_absolute_and_relative() -> None:
    scope = {
        "agent_governance",
        "agent_governance.engine",
        "agent_governance.profile",
        "agent_governance.source_adapter",
    }
    absolute = ast.parse("from agent_governance.profile import Profile").body[0]
    assert o.resolve_import_targets("agent_governance.engine", absolute, scope) == {
        "agent_governance.profile"
    }
    relative = ast.parse("from .source_adapter import SourceContext").body[0]
    assert o.resolve_import_targets("agent_governance.engine", relative, scope) == {
        "agent_governance.source_adapter"
    }


def test_acyclic() -> None:
    nodes = {"a", "b", "c"}
    assert o.acyclic(nodes, {("a", "b"), ("b", "c")}) is True
    assert o.acyclic(nodes, {("a", "b"), ("b", "a")}) is False


def test_score_p1_exact() -> None:
    oracle = {
        "frozen_head": c.FROZEN_HEAD,
        "files": [
            {
                "path": ".python-version",
                "blob_sha": "abc",
                "byte_size": 5,
                "exists_at_frozen_head": True,
            }
        ],
    }
    passed, _ = o.score_p1(json.loads(json.dumps(oracle)), oracle)
    assert passed is True
    wrong = json.loads(json.dumps(oracle))
    wrong["files"][0]["byte_size"] = 6
    assert o.score_p1(wrong, oracle)[0] is False


def test_score_p2_exact() -> None:
    oracle = {
        "edges": [
            ["agent_governance.engine", "agent_governance.profile"],
            ["agent_governance.engine", "agent_governance.source_adapter"],
        ],
        "acyclic": True,
        "symbol_owners": {
            "ArtifactBuildError": "agent_governance.artifact",
            "build_artifact": "agent_governance.artifact",
            "Profile": "agent_governance.profile",
            "resolve_profile": "agent_governance.profile",
            "SourceContext": "agent_governance.source_adapter",
            "_bootstrap": "agent_governance.engine",
        },
    }
    value = json.loads(json.dumps(oracle))
    value["edges"].reverse()
    assert o.score_p2(value, oracle)[0] is True
    value["symbol_owners"]["_bootstrap"] = "agent_governance.profile"
    assert o.score_p2(value, oracle)[0] is False


def test_score_p3_seeded_defect() -> None:
    value = {
        "status": "finding",
        "findings": [
            {
                "severity": "HIGH",
                "mechanism": "An unsupported profile fails open to source-maintainer.",
                "evidence": "validate_profile(Profile(name='invalid')) returns source-maintainer.",
                "reproduction": "The result grants_source_maintenance instead of raising ProfileError.",
                "fix_direction": "Restore fail-closed ProfileError rejection.",
            }
        ],
    }
    assert o.score_p3(value) == (
        True,
        "seeded fail-open authority escalation detected",
        0,
        0,
    )


def test_score_p3_rejects_invented_material_finding() -> None:
    value = {
        "status": "finding",
        "findings": [
            {
                "severity": "HIGH",
                "mechanism": "Unsupported invalid profile returns source-maintainer.",
                "evidence": "This grants source maintenance authority.",
                "reproduction": "No ProfileError is raised.",
                "fix_direction": "Fail closed.",
            },
            {
                "severity": "HIGH",
                "mechanism": "Unrelated network RCE.",
                "evidence": "invented",
                "reproduction": "invented",
                "fix_direction": "invented",
            },
        ],
    }
    passed, _, false_negative, false_positive = o.score_p3(value)
    assert passed is False
    assert false_negative == 0
    assert false_positive == 1


def test_collab_child_id() -> None:
    notification = Notification(
        method="item/completed",
        params={
            "threadId": "parent",
            "turnId": "turn",
            "item": {
                "type": "collabAgentToolCall",
                "tool": "spawnAgent",
                "receiverThreadIds": ["child"],
            },
        },
    )
    assert m.collab_child_id(notification, "parent", "turn") == "child"
    assert m.collab_child_id(notification, "other", "turn") is None


def test_latest_child_usage_uses_last_breakdown() -> None:
    notification = Notification(
        method="thread/tokenUsage/updated",
        params={
            "threadId": "child",
            "turnId": "turn",
            "tokenUsage": {
                "total": {
                    "inputTokens": 12,
                    "cachedInputTokens": 3,
                    "outputTokens": 4,
                    "reasoningOutputTokens": 2,
                    "totalTokens": 16,
                },
                "last": {
                    "inputTokens": 10,
                    "cachedInputTokens": 3,
                    "outputTokens": 4,
                    "reasoningOutputTokens": 2,
                    "totalTokens": 14,
                },
            },
        },
    )
    assert m.latest_child_usage(
        (notification,), child_id="child", child_turn_id="turn"
    ) == {
        "input_tokens": 10,
        "cached_input_tokens": 3,
        "output_tokens": 4,
        "reasoning_tokens": 2,
        "total_tokens": 14,
    }


def test_tool_trace_detects_oracle_path() -> None:
    turn = {
        "items": [
            {"type": "commandExecution", "command": "Get-Content docs/reviews/T063-R4.md"}
        ]
    }
    assert m.tool_trace_oracle_leak(turn) is True
    turn["items"][0]["command"] = "git cat-file -s abc"
    assert m.tool_trace_oracle_leak(turn) is False


def test_pilot_decision() -> None:
    scored = [
        {"arm": "CONTROL", "reroute_observed": False},
        {"arm": "ADAPTIVE", "reroute_observed": False},
    ]
    metrics = {
        "adaptive_first_attempt_failures": 0,
        "material_false_negative_count": 0,
        "material_false_positive_count": 0,
        "control_pass_count": 3,
        "adaptive_pass_count": 3,
        "adaptive_exact_tokens_total": 90,
        "control_exact_tokens_total": 100,
    }
    assert r.pilot_decision(metrics, scored) == "QUALIFIED"
    metrics["adaptive_exact_tokens_total"] = 110
    assert r.pilot_decision(metrics, scored) == "QUALIFIED_QUALITY_ONLY"
    metrics["adaptive_first_attempt_failures"] = 1
    assert r.pilot_decision(metrics, scored) == "NOT_QUALIFIED"


def test_control_failure_blocks_baseline() -> None:
    metrics = {
        "adaptive_first_attempt_failures": 0,
        "material_false_negative_count": 0,
        "material_false_positive_count": 0,
        "control_pass_count": 2,
        "adaptive_pass_count": 3,
        "adaptive_exact_tokens_total": 90,
        "control_exact_tokens_total": 100,
    }
    with pytest.raises(c.ExecutionInvalid, match="baseline invalid"):
        r.pilot_decision(metrics, [])


def test_runtime_root_rejects_repo_child(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    with pytest.raises(c.HarnessError, match="outside the repository"):
        o.ensure_runtime_root_safe(repo, repo / "runtime")


def test_seed_p3_fixture_exact_digest(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    source = """\"\"\"Runtime profile abstraction for Agent Governance.

``consumer`` and ``source-maintainer`` are mutually exclusive active
profiles. Unsupported or ambiguous profile values are rejected rather than
routed with broader permissions.

Profiles are implementation context, not normative authority.  No profile
default grants source-maintenance permissions.
\"\"\"

from dataclasses import dataclass


class ProfileError(Exception):
    \"\"\"Fail-closed profile-routing error.\"\"\"


ACTIVE_PROFILES = frozenset({"consumer", "source-maintainer"})
DEFAULT_PROFILE = "consumer"


@dataclass(frozen=True)
class Profile:
    \"\"\"Resolved operational profile.

    Profile identity selects an adapter boundary. Source-maintainer context
    still requires the explicit source-product signal validated by that
    adapter.
    \"\"\"

    name: str

    @property
    def is_consumer(self) -> bool:
        return self.name == "consumer"

    @property
    def is_source_maintainer(self) -> bool:
        return self.name == "source-maintainer"

    @property
    def grants_source_maintenance(self) -> bool:
        return self.is_source_maintainer


def validate_profile(profile: object) -> Profile:
    \"\"\"Validate a resolved profile against the active runtime identities.\"\"\"

    if not isinstance(profile, Profile):
        raise ProfileError(f"profile must be a Profile instance, got {type(profile).__name__}")
    if not isinstance(profile.name, str) or profile.name not in ACTIVE_PROFILES:
        raise ProfileError(
            f"unsupported profile: {profile.name!r}; active profiles: {sorted(ACTIVE_PROFILES)}"
        )
    return profile


def resolve_profile(name: str | None = None) -> Profile:
    \"\"\"Resolve a runtime profile by name.

    * ``None`` resolves to the default ``consumer`` profile.
    * Active profile names resolve to their :class:`Profile`.
    * Unsupported or ambiguous values raise :class:`ProfileError`.

    Fail-closed routing means rejected profiles never acquire broader
    permissions.
    \"\"\"

    if name is None:
        name = DEFAULT_PROFILE
    if not isinstance(name, str) or not name:
        raise ProfileError(
            f"profile must be a non-empty string, got {name!r}; "
            f"active profiles: {sorted(ACTIVE_PROFILES)}"
        )
    return validate_profile(Profile(name=name))
"""
    monkeypatch.setattr(o, "git", lambda repo, *args: c.P3_SEED_BLOB)
    monkeypatch.setattr(o, "frozen_text", lambda repo, path: source)
    fixture, oracle = o.seed_p3_fixture(tmp_path, tmp_path / "runtime")
    assert fixture.exists()
    assert oracle["mutation_count"] == 1
    assert oracle["fixture_sha256"] == c.P3_EXPECTED_FIXTURE_SHA256
    assert oracle["root_reproduction"]["returned_profile_name"] == "source-maintainer"
    assert oracle["root_reproduction"]["grants_source_maintenance"] is True


def test_task_messages_do_not_contain_p3_oracle() -> None:
    messages = c.build_task_messages()
    assert "source-maintainer" not in messages["P3"]
    assert "ProfileError" not in messages["P3"]
    assert c.FROZEN_HEAD in messages["P1"]
    assert c.FROZEN_HEAD in messages["P2"]
