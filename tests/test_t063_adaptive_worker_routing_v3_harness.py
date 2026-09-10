from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from evals.adaptive_worker_routing_v3.app_server import Notification
from evals.adaptive_worker_routing_v3 import config as c
from evals.adaptive_worker_routing_v3 import measurement as m
from evals.adaptive_worker_routing_v3 import oracles as o
from evals.adaptive_worker_routing_v3 import runner as r


def test_frozen_task_message_digests_match() -> None:
    observed = {probe: o.sha256_text(message) for probe, message in c.build_task_messages().items()}
    assert observed == c.EXPECTED_TASK_MESSAGE_DIGESTS


def test_child_contract_is_config_authoritative_and_trigger_secret() -> None:
    spec = c.ArmSpec("P1", "ADAPTIVE", "gpt-5.6-luna", "medium")
    task = c.build_task_messages()["P1"]
    digest = c.EXPECTED_TASK_MESSAGE_DIGESTS["P1"]
    contract = c.build_child_contract(spec, task, digest)
    assert task in contract
    assert spec.contract_nonce in contract
    assert digest in contract
    assert spec.spawn_trigger not in contract
    assert "spawn_trigger_received" in contract


def test_parent_message_contains_no_probe_or_profile_semantics() -> None:
    spec = c.ArmSpec("P3", "ADAPTIVE", "gpt-5.6-terra", "high")
    text = c.build_parent_turn_message(spec)
    assert spec.task_name in text
    assert spec.spawn_trigger in text
    assert 'fork_turns="none"' in text
    assert "gpt-5.6" not in text
    assert "profile_fixture.py" not in text
    assert "source-maintainer" not in text


def test_per_arm_config_fixes_child_profile_and_contract() -> None:
    spec = c.ArmSpec("P2", "CONTROL", "gpt-5.6-sol", "medium")
    cfg = c.per_arm_thread_config(spec, "contract")
    assert cfg["model_reasoning_effort"] == "medium"
    assert cfg["agents.default_subagent_model"] == "gpt-5.6-sol"
    assert cfg["agents.default_subagent_reasoning_effort"] == "medium"
    assert cfg["features.multi_agent_v2.subagent_developer_instructions"] == "contract"
    assert cfg["features.multi_agent_v2.expose_spawn_agent_model_overrides"] is False
    assert cfg["features.multi_agent_v2.hide_spawn_agent_metadata"] is True


def test_v3_app_server_overrides_hide_profile_override_surface() -> None:
    assert c.APP_SERVER_CONFIG_OVERRIDES == (
        "features.multi_agent=true",
        "features.multi_agent_v2.enabled=true",
        "features.multi_agent_v2.expose_spawn_agent_model_overrides=false",
        "features.multi_agent_v2.hide_spawn_agent_metadata=true",
    )


def test_version_sensitive_versions_are_frozen() -> None:
    assert c.UPSTREAM_REVALIDATED_VERSIONS == ("0.153.4", "0.154.0", "0.155.0-alpha.2")


def test_schema_gate_includes_public_v2_child_activity() -> None:
    assert "subAgentActivity" in m.SCHEMA_MARKERS
    assert "agentThreadId" in m.SCHEMA_MARKERS
    assert "activePermissionProfile" in m.SCHEMA_MARKERS


def test_custom_agent_role_detection() -> None:
    assert m.custom_agent_role_keys({"config": {"agents": None}}) == []
    assert m.custom_agent_role_keys({"config": {"agents": {
        "enabled": True,
        "default_subagent_model": "gpt-5.6-luna",
    }}}) == []
    assert m.custom_agent_role_keys({"config": {"agents": {
        "enabled": True,
        "reviewer": {"description": "custom"},
    }}}) == ["reviewer"]


def test_subagent_activity_correlates_child() -> None:
    n = Notification(
        method="item/completed",
        params={
            "threadId": "parent",
            "turnId": "turn",
            "item": {
                "type": "subAgentActivity",
                "id": "call",
                "kind": "started",
                "agentThreadId": "child",
                "agentPath": "/root/t063_p1_adaptive",
            },
        },
    )
    assert m.activity_child_id(n, "parent", "turn", "t063_p1_adaptive") == "child"
    assert m.activity_child_id(n, "parent", "turn", "t063_p1_control") is None


def test_subagent_activity_rejects_non_started() -> None:
    n = Notification(
        method="item/completed",
        params={
            "threadId": "parent",
            "turnId": "turn",
            "item": {
                "type": "subAgentActivity",
                "kind": "completed",
                "agentThreadId": "child",
                "agentPath": "/root/t063_p1_adaptive",
            },
        },
    )
    assert m.activity_child_id(n, "parent", "turn", "t063_p1_adaptive") is None


def test_worker_receipt_exact() -> None:
    spec = c.ArmSpec("P1", "ADAPTIVE", "gpt-5.6-luna", "medium")
    digest = c.EXPECTED_TASK_MESSAGE_DIGESTS["P1"]
    value = {"t063_receipt": {
        "contract_nonce": spec.contract_nonce,
        "task_message_sha256": digest,
        "spawn_trigger_received": spec.spawn_trigger,
    }}
    assert m.validate_worker_receipt(value, spec=spec, task_digest=digest)["contract_nonce"] == spec.contract_nonce
    value["t063_receipt"]["spawn_trigger_received"] = "drift"
    with pytest.raises(c.ExecutionInvalid, match="receipt mismatch"):
        m.validate_worker_receipt(value, spec=spec, task_digest=digest)


def test_parent_surface_requires_single_expected_activity() -> None:
    turn = {
        "items": [
            {
                "type": "subAgentActivity",
                "kind": "started",
                "agentThreadId": "child",
                "agentPath": "/root/t063_p1_adaptive",
            },
            {"type": "agentMessage", "text": "PARENT_SPAWNED"},
        ]
    }
    m._validate_parent_surface(turn, child_id="child", expected_task_name="t063_p1_adaptive")
    turn["items"].insert(0, {"type": "commandExecution", "command": "git status"})
    with pytest.raises(c.ExecutionInvalid, match="forbidden"):
        m._validate_parent_surface(turn, child_id="child", expected_task_name="t063_p1_adaptive")


def test_latest_child_usage_uses_last_breakdown() -> None:
    n = Notification(
        method="thread/tokenUsage/updated",
        params={
            "threadId": "child",
            "turnId": "turn",
            "tokenUsage": {
                "last": {
                    "inputTokens": 10,
                    "cachedInputTokens": 3,
                    "outputTokens": 4,
                    "reasoningOutputTokens": 2,
                    "totalTokens": 14,
                }
            },
        },
    )
    assert m.latest_child_usage((n,), child_id="child", child_turn_id="turn")["total_tokens"] == 14


def test_tool_trace_detects_oracle_path() -> None:
    turn = {"items": [{"type": "commandExecution", "command": "Get-Content docs/reviews/T063-R6.md"}]}
    assert m.tool_trace_oracle_leak(turn) is True
    turn["items"][0]["command"] = "git cat-file -s abc"
    assert m.tool_trace_oracle_leak(turn) is False


def test_module_for_path_and_relative_import() -> None:
    assert o.module_for_path("src/agent_governance/__init__.py") == "agent_governance"
    scope = {"agent_governance.engine", "agent_governance.profile", "agent_governance.source_adapter"}
    node = ast.parse("from .source_adapter import SourceContext").body[0]
    assert o.resolve_import_targets("agent_governance.engine", node, scope) == {"agent_governance.source_adapter"}


def test_acyclic() -> None:
    assert o.acyclic({"a", "b", "c"}, {("a", "b"), ("b", "c")}) is True
    assert o.acyclic({"a", "b"}, {("a", "b"), ("b", "a")}) is False


def test_score_p1_exact_ignores_receipt_extra_key() -> None:
    oracle = {"frozen_head": c.FROZEN_HEAD, "files": [{
        "path": ".python-version", "blob_sha": "abc", "byte_size": 5, "exists_at_frozen_head": True
    }]}
    value = json.loads(json.dumps(oracle))
    value["t063_receipt"] = {}
    assert o.score_p1(value, oracle)[0] is True


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


def test_score_p3_seeded_defect() -> None:
    value = {"status": "finding", "findings": [{
        "severity": "HIGH",
        "mechanism": "Unsupported invalid profile fails open to source-maintainer authority.",
        "evidence": "validate_profile returns source-maintainer and grants_source_maintenance.",
        "reproduction": "Invalid name receives source maintenance instead of ProfileError.",
        "fix_direction": "Restore fail-closed ProfileError rejection.",
    }]}
    assert o.score_p3(value) == (True, "seeded fail-open authority escalation detected", 0, 0)


def test_runtime_root_requires_worktree_sibling(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(o.tempfile, "gettempdir", lambda: str(tmp_path / "system-temp"))
    parent = tmp_path / "worktrees"
    parent.mkdir()
    repo = parent / "t063"
    repo.mkdir()
    o.ensure_runtime_root_safe(repo, parent / "t063-runtime")
    with pytest.raises(c.HarnessError, match="sibling"):
        o.ensure_runtime_root_safe(repo, tmp_path / "other" / "t063-runtime")


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


def test_app_server_version_01534() -> None:
    initialized = {"userAgent": "Codex Desktop/0.153.4 (Windows 10; x86_64)"}
    assert m.app_server_version(initialized) == "0.153.4"


def test_seed_p3_fixture_exact_digest(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    source = '''"""Runtime profile abstraction for Agent Governance.

``consumer`` and ``source-maintainer`` are mutually exclusive active
profiles. Unsupported or ambiguous profile values are rejected rather than
routed with broader permissions.

Profiles are implementation context, not normative authority.  No profile
default grants source-maintenance permissions.
"""

from dataclasses import dataclass


class ProfileError(Exception):
    """Fail-closed profile-routing error."""


ACTIVE_PROFILES = frozenset({"consumer", "source-maintainer"})
DEFAULT_PROFILE = "consumer"


@dataclass(frozen=True)
class Profile:
    """Resolved operational profile.

    Profile identity selects an adapter boundary. Source-maintainer context
    still requires the explicit source-product signal validated by that
    adapter.
    """

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
    """Validate a resolved profile against the active runtime identities."""

    if not isinstance(profile, Profile):
        raise ProfileError(f"profile must be a Profile instance, got {type(profile).__name__}")
    if not isinstance(profile.name, str) or profile.name not in ACTIVE_PROFILES:
        raise ProfileError(
            f"unsupported profile: {profile.name!r}; active profiles: {sorted(ACTIVE_PROFILES)}"
        )
    return profile


def resolve_profile(name: str | None = None) -> Profile:
    """Resolve a runtime profile by name.

    * ``None`` resolves to the default ``consumer`` profile.
    * Active profile names resolve to their :class:`Profile`.
    * Unsupported or ambiguous values raise :class:`ProfileError`.

    Fail-closed routing means rejected profiles never acquire broader
    permissions.
    """

    if name is None:
        name = DEFAULT_PROFILE
    if not isinstance(name, str) or not name:
        raise ProfileError(
            f"profile must be a non-empty string, got {name!r}; "
            f"active profiles: {sorted(ACTIVE_PROFILES)}"
        )
    return validate_profile(Profile(name=name))
'''
    monkeypatch.setattr(o, "git", lambda repo, *args: c.P3_SEED_BLOB)
    monkeypatch.setattr(o, "frozen_text", lambda repo, path: source)
    fixture, oracle = o.seed_p3_fixture(tmp_path, tmp_path.parent / "runtime-sibling")
    assert fixture.exists()
    assert oracle["mutation_count"] == 1
    assert oracle["fixture_sha256"] == c.P3_EXPECTED_FIXTURE_SHA256
    assert oracle["root_reproduction"]["returned_profile_name"] == "source-maintainer"
    assert oracle["root_reproduction"]["grants_source_maintenance"] is True
