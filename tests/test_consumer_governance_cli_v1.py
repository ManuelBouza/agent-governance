"""Subprocess coverage for remaining Consumer Governance CLI v1 commands."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


def run_cli(cli: Path, *arguments: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(cli), *(str(argument) for argument in arguments)],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )


@pytest.fixture
def governance_cli(repo_root: Path) -> Path:
    return repo_root / "governance-skill" / "scripts" / "governance.py"


@pytest.fixture
def consumer(tmp_path: Path, governance_cli: Path) -> Path:
    target = tmp_path / "consumer"
    target.mkdir()
    result = run_cli(governance_cli, "bootstrap", target)
    assert result.returncode == 0, result.stderr
    configure_mission(target)
    return target


def task_line(task_id: str, dependency: str, status: str, position: int) -> str:
    return f"{position}. `{task_id}` \N{EM DASH} depends on `{dependency}` \N{EM DASH} `{status}`"


def configure_mission(
    target: Path,
    *,
    mission_id: str = "M1",
    mission_status: str = "ACTIVE",
    phase: str = "F6",
    tasks: tuple[tuple[str, str, str], ...] = (("T1", "none", "READY"),),
    current: str = "T1",
    blocker: str = "none",
    exchange: list[dict[str, object]] | None = None,
    controlling_records: list[str] | None = None,
) -> None:
    coordination = target / ".agent-coordination"
    (coordination / "MISSION.md").write_text(
        f"# Mission\n\nMission-ID: `{mission_id}`\nStatus: `{mission_status}`\n",
        encoding="utf-8",
    )
    lines = "\n".join(
        task_line(task_id, dependency, status, position)
        for position, (task_id, dependency, status) in enumerate(tasks, 1)
    )
    records = controlling_records or ["MISSION.md", "WORKPLAN.md"]
    (coordination / "WORKPLAN.md").write_text(
        "# Workplan\n\n"
        f"Mission-ID: `{mission_id}`\n"
        f"Status: `{phase}`\n"
        'Gates: {"F5": true, "F6": true}\n'
        f"Controlling records: {json.dumps(records)}\n\n"
        f"## Tasks\n\n{lines}\n\n"
        "## Frontier\n\n"
        f"Current task: `{current}`\n"
        f"Blocker: `{blocker}`\n",
        encoding="utf-8",
    )
    for task_id, _dependency, status in tasks:
        (coordination / "tasks" / f"{task_id}.md").write_text(
            f"# Task\n\nTask-ID: `{task_id}`\nStatus: `{status}`\n",
            encoding="utf-8",
        )
    events = exchange or [{"q": 1, "a": "human", "e": "start", "n": "Start T1"}]
    (coordination / "EXCHANGE.jsonl").write_text(
        "".join(json.dumps(event, separators=(",", ":")) + "\n" for event in events),
        encoding="utf-8",
    )


def approval_record(target: Path) -> tuple[Path, Path, dict[str, object]]:
    skills = target / ".agent-coordination" / "skills"
    candidate_artifact = target / "quarantine" / "safe-skill"
    selected_artifact = target / "installed" / "safe-skill"
    candidate_artifact.mkdir(parents=True, exist_ok=True)
    selected_artifact.mkdir(parents=True, exist_ok=True)
    content = b"safe skill\n"
    for artifact in (candidate_artifact, selected_artifact):
        (artifact / "SKILL.md").write_bytes(content)
    digest = hashlib.sha256(b"SKILL.md\0" + content + b"\0").hexdigest()
    approval = {
        "skill_id": "S1",
        "name": "safe-skill",
        "capability": "linting",
        "discovery_source": "internal-registry",
        "provenance_tier": "PROJECT_OWNED",
        "canonical_source": {
            "owner": "example",
            "repository": "skills",
            "path": "safe-skill",
        },
        "revision": "0123456789abcdef",
        "digest": f"sha256:{digest}",
        "version": "1.0.0",
        "license": "MIT",
        "risk": "LOW",
        "required_tools": ["python"],
        "permissions": ["read-project"],
        "dependencies": ["stdlib"],
        "audit": {"result": "PASS", "exceptions": []},
        "approval": {"authority": "Human Owner", "date": "2026-08-14"},
        "status": "APPROVED",
    }
    identity = {
        "canonical_source": approval["canonical_source"],
        "revision": approval["revision"],
        "digest": approval["digest"],
    }
    candidate = {
        "skill_id": "S1",
        "name": "safe-skill",
        "discovery_source": "internal-registry",
        "provenance_tier": "PROJECT_OWNED",
        **identity,
        "required_tools": ["python"],
        "permissions": ["read-project"],
        "dependencies": ["stdlib"],
        "selected_host_identity": identity,
        "candidate_artifact": str(candidate_artifact.relative_to(target)),
        "selected_host_artifact": str(selected_artifact.relative_to(target)),
    }
    approval_path = skills / "S1.json"
    candidate_path = skills / "S1-candidate.json"
    approval_path.write_text(json.dumps(approval), encoding="utf-8")
    candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
    return approval_path, candidate_path, candidate


def ecosystem_facts(target: Path) -> Path:
    (target / "managed.txt").write_text("third-party managed\n", encoding="utf-8")
    (target / "specs").mkdir(exist_ok=True)
    facts = {
        "capabilities": [
            {
                "id": "native-sdd",
                "category": "sdd",
                "provider": "project-specs",
                "scope": "project",
                "evidence": "specs/",
                "provider_present": True,
                "need_covered": True,
                "adapter_required": False,
                "responsibilities_distinct": False,
                "authority_overlap": False,
                "managed_surfaces": ["managed.txt"],
                "control_reference": ".agent-coordination/MISSION.md",
            },
            {
                "id": "governance-overlap",
                "category": "orchestration",
                "provider": "other-governance",
                "scope": "project",
                "evidence": "managed.txt",
                "provider_present": True,
                "need_covered": True,
                "adapter_required": False,
                "responsibilities_distinct": False,
                "authority_overlap": True,
                "managed_surfaces": ["managed.txt"],
                "control_reference": ".agent-coordination/MISSION.md",
            },
            {
                "id": "optional-sdd",
                "category": "sdd",
                "provider": None,
                "scope": "project",
                "evidence": None,
                "provider_present": False,
                "need_covered": False,
                "adapter_required": False,
                "responsibilities_distinct": False,
                "authority_overlap": False,
                "managed_surfaces": [],
                "control_reference": None,
            },
        ]
    }
    path = target / "ecosystem-facts.json"
    path.write_text(json.dumps(facts), encoding="utf-8")
    return path


def test_parser_exposes_exact_stable_commands(governance_cli: Path) -> None:
    result = run_cli(governance_cli, "--help")
    assert result.returncode == 0
    match = re.search(r"\{([^}]+)\}", result.stdout)
    assert match is not None
    assert match.group(1).split(",") == [
        "bootstrap",
        "validate",
        "state",
        "event",
        "skill",
        "ecosystem",
        "archive",
    ]


def test_state_is_read_only_by_default_and_refreshes_explicitly(
    consumer: Path, governance_cli: Path
) -> None:
    state_path = consumer / ".agent-coordination" / "STATE.json"
    before = state_path.read_bytes()
    stale = run_cli(governance_cli, "state", consumer)
    assert stale.returncode == 1
    assert "STATE is stale" in stale.stderr
    assert state_path.read_bytes() == before

    refreshed = run_cli(governance_cli, "state", consumer, "--refresh")
    assert refreshed.returncode == 0, refreshed.stderr
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state == json.loads(refreshed.stdout)
    assert state["mission_id"] == "M1"
    assert state["active_task"] == "T1"
    assert state["ready_tasks"] == ["T1"]
    assert state["exchange_q"] == 1
    assert run_cli(governance_cli, "state", consumer).returncode == 0


@pytest.mark.parametrize(
    ("mutation", "error"),
    [
        ("missing-reference", "missing or unsafe required file"),
        ("unknown-task", "unknown task"),
        ("malformed-event", "malformed JSONL"),
    ],
)
def test_state_refuses_invalid_authority_or_history(
    consumer: Path, governance_cli: Path, mutation: str, error: str
) -> None:
    if mutation == "missing-reference":
        configure_mission(consumer, controlling_records=["missing.md"])
    elif mutation == "unknown-task":
        configure_mission(
            consumer,
            exchange=[
                {"q": 1, "a": "human", "e": "start", "n": "Start"},
                {"q": 2, "a": "implementation", "e": "start", "k": "UNKNOWN"},
            ],
        )
    else:
        (consumer / ".agent-coordination" / "EXCHANGE.jsonl").write_text(
            "{broken\n", encoding="utf-8"
        )
    result = run_cli(governance_cli, "state", consumer)
    assert result.returncode == 1
    assert error in result.stderr


def test_state_operates_from_standalone_script_without_source_checkout(
    consumer: Path, governance_cli: Path, tmp_path: Path
) -> None:
    standalone = tmp_path / "governance.py"
    shutil.copyfile(governance_cli, standalone)
    result = run_cli(standalone, "state", consumer, "--refresh")
    assert result.returncode == 0, result.stderr


def test_event_appends_one_atomic_transition_after_full_preflight(
    consumer: Path, governance_cli: Path
) -> None:
    configure_mission(consumer, tasks=(("T1", "none", "READY"),), current="T1")
    exchange = consumer / ".agent-coordination" / "EXCHANGE.jsonl"
    result = run_cli(
        governance_cli,
        "event",
        consumer,
        "--actor",
        "implementation",
        "--event",
        "start",
        "--task",
        "T1",
        "--next-action",
        "Execute T1",
    )
    assert result.returncode == 0, result.stderr
    lines = exchange.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[-1]) == json.loads(result.stdout)
    assert json.loads(lines[-1])["q"] == 2


def test_event_serializes_concurrent_appenders_without_lost_updates(
    consumer: Path, governance_cli: Path
) -> None:
    processes = [
        subprocess.Popen(
            [
                sys.executable,
                str(governance_cli),
                "event",
                str(consumer),
                "--actor",
                "strategy",
                "--event",
                "decision",
                "--reference",
                f"D{index}",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for index in range(8)
    ]
    results = [(*process.communicate(timeout=30), process.returncode) for process in processes]
    assert all(returncode == 0 for _stdout, _stderr, returncode in results), results
    events = [
        json.loads(line)
        for line in (consumer / ".agent-coordination" / "EXCHANGE.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert [event["q"] for event in events] == list(range(1, 10))
    assert {event.get("r") for event in events[1:]} == {f"D{index}" for index in range(8)}


@pytest.mark.parametrize(
    ("event", "arguments", "error"),
    [
        ("done", (), "requires evidence reference and verification"),
        ("blocked", (), "requires evidence reference and reason"),
    ],
)
def test_event_requires_transition_evidence(
    consumer: Path,
    governance_cli: Path,
    event: str,
    arguments: tuple[str, ...],
    error: str,
) -> None:
    configure_mission(
        consumer,
        tasks=(("T1", "none", "IN_PROGRESS"),),
        current="T1",
        exchange=[
            {"q": 1, "a": "human", "e": "start", "n": "Start T1"},
            {"q": 2, "a": "implementation", "e": "start", "k": "T1"},
        ],
    )
    path = consumer / ".agent-coordination" / "EXCHANGE.jsonl"
    before = path.read_bytes()
    result = run_cli(
        governance_cli,
        "event",
        consumer,
        "--actor",
        "implementation",
        "--event",
        event,
        "--task",
        "T1",
        *arguments,
    )
    assert result.returncode == 1
    assert error in result.stderr
    assert path.read_bytes() == before


def test_event_replays_continuous_sequence_without_workplan_status_rewrites(
    consumer: Path, governance_cli: Path
) -> None:
    for event, arguments in (
        ("start", ("--next-action", "Execute T1")),
        ("progress", ("--reference", "commit:abc")),
        ("done", ("--reference", "commit:def", "--verification", "passed")),
    ):
        result = run_cli(
            governance_cli,
            "event",
            consumer,
            "--actor",
            "implementation",
            "--event",
            event,
            "--task",
            "T1",
            *arguments,
        )
        assert result.returncode == 0, result.stderr
    state = run_cli(governance_cli, "state", consumer, "--refresh")
    assert state.returncode == 0, state.stderr
    frontier = json.loads(state.stdout)
    assert frontier["active_task"] is None
    assert frontier["ready_tasks"] == []
    assert frontier["next_action"] == "Close or archive mission"


@pytest.mark.parametrize(
    ("actor", "event", "task", "error"),
    [
        ("strategy", "start", "T1", "cannot emit"),
        ("implementation", "done", "T1", "first event"),
        ("implementation", "start", "UNKNOWN", "unknown task"),
    ],
)
def test_event_rejects_actor_transition_and_task_violations_without_append(
    consumer: Path,
    governance_cli: Path,
    actor: str,
    event: str,
    task: str,
    error: str,
) -> None:
    configure_mission(consumer, tasks=(("T1", "none", "READY"),), current="T1")
    path = consumer / ".agent-coordination" / "EXCHANGE.jsonl"
    before = path.read_bytes()
    result = run_cli(
        governance_cli,
        "event",
        consumer,
        "--actor",
        actor,
        "--event",
        event,
        "--task",
        task,
    )
    assert result.returncode == 1
    assert error in result.stderr
    assert path.read_bytes() == before


def test_event_requires_done_or_accepted_dependencies(consumer: Path, governance_cli: Path) -> None:
    configure_mission(
        consumer,
        tasks=(("T1", "none", "PLANNED"), ("T2", "T1", "READY")),
        current="T2",
    )
    result = run_cli(
        governance_cli,
        "event",
        consumer,
        "--actor",
        "implementation",
        "--event",
        "start",
        "--task",
        "T2",
    )
    assert result.returncode == 1
    assert "unmet dependencies: T1" in result.stderr


def test_skill_validates_exact_approval_candidate_and_selected_host(
    consumer: Path, governance_cli: Path
) -> None:
    approval, candidate, _facts = approval_record(consumer)
    result = run_cli(
        governance_cli,
        "skill",
        consumer,
        "--approval",
        approval.relative_to(consumer),
        "--candidate",
        candidate.relative_to(consumer),
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {"skill_id": "S1", "status": "VALID"}


@pytest.mark.parametrize(
    ("mutation", "error"),
    [
        ("discovery", "discovery_source does not match"),
        ("digest", "identity does not match"),
        ("permission", "permissions exceeds"),
        ("host", "identity does not match"),
        ("artifact", "artifact digest does not match"),
    ],
)
def test_skill_refuses_provenance_envelope_and_host_mismatch(
    consumer: Path, governance_cli: Path, mutation: str, error: str
) -> None:
    approval, candidate_path, candidate = approval_record(consumer)
    if mutation == "discovery":
        candidate["discovery_source"] = "marketplace"
    elif mutation == "digest":
        candidate["digest"] = "sha256:changed"
    elif mutation == "permission":
        candidate["permissions"] = ["read-project", "network"]
    else:
        if mutation == "host":
            candidate["selected_host_identity"]["revision"] = "different-revision"
        else:
            artifact = consumer / candidate["candidate_artifact"] / "SKILL.md"
            artifact.write_text("tampered\n", encoding="utf-8")
    candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
    result = run_cli(
        governance_cli,
        "skill",
        consumer,
        "--approval",
        approval.relative_to(consumer),
        "--candidate",
        candidate_path.relative_to(consumer),
    )
    assert result.returncode == 1
    assert error in result.stderr


def test_skill_refuses_noncanonical_approval_copy(consumer: Path, governance_cli: Path) -> None:
    approval, candidate, _facts = approval_record(consumer)
    stale = consumer / "stale-approval.json"
    shutil.copyfile(approval, stale)
    result = run_cli(
        governance_cli,
        "skill",
        consumer,
        "--approval",
        stale.relative_to(consumer),
        "--candidate",
        candidate.relative_to(consumer),
    )
    assert result.returncode == 1
    assert "canonical current record" in result.stderr


def test_skill_refuses_unsafe_id_and_symlinked_artifact(
    consumer: Path, governance_cli: Path
) -> None:
    approval, candidate_path, candidate = approval_record(consumer)
    approval_value = json.loads(approval.read_text(encoding="utf-8"))
    approval_value["skill_id"] = "../decisions/rogue"
    candidate["skill_id"] = "../decisions/rogue"
    rogue = consumer / ".agent-coordination" / "decisions" / "rogue.json"
    rogue.write_text(json.dumps(approval_value), encoding="utf-8")
    candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
    unsafe = run_cli(
        governance_cli,
        "skill",
        consumer,
        "--approval",
        rogue.relative_to(consumer),
        "--candidate",
        candidate_path.relative_to(consumer),
    )
    assert unsafe.returncode == 1
    assert "unsafe skill_id" in unsafe.stderr

    approval, candidate_path, candidate = approval_record(consumer)
    candidate_artifact = consumer / candidate["candidate_artifact"]
    (candidate_artifact / "linked").symlink_to(consumer / "managed.txt")
    linked = run_cli(
        governance_cli,
        "skill",
        consumer,
        "--approval",
        approval.relative_to(consumer),
        "--candidate",
        candidate_path.relative_to(consumer),
    )
    assert linked.returncode == 1
    assert "unsafe symlink" in linked.stderr


def test_ecosystem_is_read_only_then_updates_compact_inventory_without_managed_writes(
    consumer: Path, governance_cli: Path
) -> None:
    managed = consumer / "managed.txt"
    facts = ecosystem_facts(consumer)
    capabilities = consumer / ".agent-coordination" / "CAPABILITIES.json"
    before = capabilities.read_bytes()
    inspect = run_cli(governance_cli, "ecosystem", consumer, "--facts", facts.relative_to(consumer))
    assert inspect.returncode == 1
    assert "CAPABILITIES is stale" in inspect.stderr
    assert capabilities.read_bytes() == before

    update = run_cli(
        governance_cli,
        "ecosystem",
        consumer,
        "--facts",
        facts.relative_to(consumer),
        "--update",
    )
    assert update.returncode == 0, update.stderr
    inventory = json.loads(capabilities.read_text(encoding="utf-8"))
    assert [item["classification"] for item in inventory["capabilities"]] == [
        "REUSE",
        "CONFLICT",
        "MISSING",
    ]
    assert managed.read_text(encoding="utf-8") == "third-party managed\n"
    assert (
        run_cli(
            governance_cli, "ecosystem", consumer, "--facts", facts.relative_to(consumer)
        ).returncode
        == 0
    )


def test_ecosystem_refuses_ambiguous_facts(consumer: Path, governance_cli: Path) -> None:
    facts = ecosystem_facts(consumer)
    value = json.loads(facts.read_text(encoding="utf-8"))
    value["capabilities"][2]["need_covered"] = True
    facts.write_text(json.dumps(value), encoding="utf-8")
    result = run_cli(governance_cli, "ecosystem", consumer, "--facts", facts.relative_to(consumer))
    assert result.returncode == 1
    assert "contradictory" in result.stderr


def test_ecosystem_refuses_unverifiable_or_unsafe_paths(
    consumer: Path, governance_cli: Path
) -> None:
    facts = ecosystem_facts(consumer)
    value = json.loads(facts.read_text(encoding="utf-8"))
    value["capabilities"][0]["evidence"] = "does-not-exist"
    facts.write_text(json.dumps(value), encoding="utf-8")
    result = run_cli(governance_cli, "ecosystem", consumer, "--facts", facts.relative_to(consumer))
    assert result.returncode == 1
    assert "evidence is missing or unsafe" in result.stderr


def test_ecosystem_accepts_effective_exchange_control_reference(
    consumer: Path, governance_cli: Path
) -> None:
    facts = ecosystem_facts(consumer)
    value = json.loads(facts.read_text(encoding="utf-8"))
    event = run_cli(
        governance_cli,
        "event",
        consumer,
        "--actor",
        "strategy",
        "--event",
        "decision",
        "--reference",
        "D1",
    )
    assert event.returncode == 0, event.stderr
    value["capabilities"][0]["control_reference"] = "exchange:2"
    facts.write_text(json.dumps(value), encoding="utf-8")
    result = run_cli(
        governance_cli, "ecosystem", consumer, "--facts", facts.relative_to(consumer), "--update"
    )
    assert result.returncode == 0, result.stderr


def test_state_does_not_load_future_task_records(consumer: Path, governance_cli: Path) -> None:
    configure_mission(
        consumer,
        tasks=(("T1", "none", "READY"), ("T2", "T1", "PLANNED")),
        current="T1",
    )
    (consumer / ".agent-coordination" / "tasks" / "T2.md").unlink()
    result = run_cli(governance_cli, "state", consumer, "--refresh")
    assert result.returncode == 0, result.stderr


def test_state_uses_current_frontier_instead_of_historical_next_action(
    consumer: Path, governance_cli: Path
) -> None:
    configure_mission(
        consumer,
        mission_status="COMPLETED",
        tasks=(("T1", "none", "DONE"),),
        current="none",
        exchange=[
            {"q": 1, "a": "human", "e": "start", "n": "Execute T1"},
            {"q": 2, "a": "implementation", "e": "start", "k": "T1"},
            {
                "q": 3,
                "a": "implementation",
                "e": "done",
                "k": "T1",
                "r": "commit:abc",
                "v": "passed",
            },
        ],
    )
    result = run_cli(governance_cli, "state", consumer, "--refresh")
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["next_action"] == "Close or archive mission"


def test_archive_checks_then_atomically_preserves_completed_mission(
    consumer: Path, governance_cli: Path
) -> None:
    events = [
        {"q": 1, "a": "human", "e": "start", "n": "Start T1"},
        {"q": 2, "a": "implementation", "e": "start", "k": "T1"},
        {
            "q": 3,
            "a": "implementation",
            "e": "done",
            "k": "T1",
            "r": "commit:abc",
            "v": "passed",
        },
    ]
    configure_mission(
        consumer,
        mission_status="COMPLETED",
        tasks=(("T1", "none", "DONE"),),
        current="none",
        exchange=events,
    )
    coordination = consumer / ".agent-coordination"
    refreshed = run_cli(governance_cli, "state", consumer, "--refresh")
    assert refreshed.returncode == 0, refreshed.stderr
    before = (coordination / "EXCHANGE.jsonl").read_bytes()
    check = run_cli(governance_cli, "archive", consumer)
    assert check.returncode == 0, check.stderr
    assert not (coordination / "archive").exists()

    prepared = run_cli(governance_cli, "archive", consumer, "--prepare")
    assert prepared.returncode == 0, prepared.stderr
    archive = coordination / "archive" / "M1"
    assert (archive / "EXCHANGE.jsonl").read_bytes() == before
    active_events = (coordination / "EXCHANGE.jsonl").read_text(encoding="utf-8").splitlines()
    assert [json.loads(line) for line in active_events] == [
        {"q": 1, "a": "human", "e": "start", "n": "Provide Human-approved mission inputs"}
    ]
    assert (archive / "tasks" / "T1.md").is_file()
    assert not (coordination / "tasks" / "T1.md").exists()
    assert "<mission-id>" in (coordination / "MISSION.md").read_text(encoding="utf-8")
    assert run_cli(governance_cli, "validate", consumer).returncode == 0


def test_archive_refuses_terminal_status_without_transition_history(
    consumer: Path, governance_cli: Path
) -> None:
    configure_mission(
        consumer,
        mission_status="COMPLETED",
        tasks=(("T1", "none", "DONE"),),
        current="none",
    )
    result = run_cli(governance_cli, "archive", consumer, "--prepare")
    assert result.returncode == 1
    assert "without transition history" in result.stderr


@pytest.mark.parametrize(
    ("mission_status", "task_status", "current", "blocker", "error"),
    [
        ("ACTIVE", "DONE", "none", "none", "not authoritatively completed"),
        ("COMPLETED", "BLOCKED", "T1", "security_risk", "without transition history"),
        ("COMPLETED", "PLANNED", "none", "none", "unresolved tasks"),
    ],
)
def test_archive_refuses_unsafe_mission_state(
    consumer: Path,
    governance_cli: Path,
    mission_status: str,
    task_status: str,
    current: str,
    blocker: str,
    error: str,
) -> None:
    configure_mission(
        consumer,
        mission_status=mission_status,
        tasks=(("T1", "none", task_status),),
        current=current,
        blocker=blocker,
    )
    result = run_cli(governance_cli, "archive", consumer, "--prepare")
    assert result.returncode == 1
    assert error in result.stderr
    assert not (consumer / ".agent-coordination" / "archive").exists()


def test_archive_refuses_unsafe_mission_id(consumer: Path, governance_cli: Path) -> None:
    configure_mission(consumer, mission_id="../escape", mission_status="COMPLETED")
    result = run_cli(governance_cli, "archive", consumer, "--prepare")
    assert result.returncode == 1
    assert "Mission-ID is unsafe" in result.stderr
    assert not (consumer.parent / "escape").exists()
