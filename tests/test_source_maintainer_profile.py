"""Focused T022 source-maintainer profile and adapter verification."""

from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

import pytest


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_launcher(repo_root: Path):
    return load_module(
        repo_root / "governance-skill" / "scripts" / "governance.py",
        "t022_source_launcher",
    )


def stage_source(repo_root: Path, target: Path) -> Path:
    target.mkdir()
    shutil.copy2(repo_root / "agent-governance-source.json", target)
    for relative in (
        "AGENTS.md",
        "docs/BRANCHING.md",
        "docs/CONFORMANCE-ORACLE-CONTRACT.md",
        "docs/DEVELOPMENT-WORKFLOW.md",
        "docs/EXECUTOR-HANDOFFS.md",
        "docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md",
        "docs/REFACTORING-WORKFLOW.md",
        "docs/RELEASES.md",
        "docs/TASK-CONTRACTS.md",
        "docs/TESTING-AND-EVALUATION.md",
        "docs/TESTING-SKILL-CAPABILITIES.md",
        "docs/orchestrator/CHECKPOINT.md",
    ):
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(repo_root / relative, destination)
    for relative in (
        "docs/decisions",
        "docs/tasks",
        "evals",
        "governance-core",
        "governance-skill",
        "handoffs",
        "maintainer-skill",
        "tests",
    ):
        shutil.copytree(repo_root / relative, target / relative)
    return target


def test_source_maintainer_profile_is_active_and_mutually_exclusive(repo_root: Path) -> None:
    profile_mod = load_module(repo_root / "src" / "agent_governance" / "profile.py", "t022_profile")
    consumer = profile_mod.resolve_profile("consumer")
    source = profile_mod.resolve_profile("source-maintainer")

    assert source.name == "source-maintainer"
    assert source.is_source_maintainer
    assert source.grants_source_maintenance
    assert not source.is_consumer
    assert consumer.is_consumer
    assert not consumer.is_source_maintainer
    assert not consumer.grants_source_maintenance


def test_source_context_resolves_live_legacy_records_from_explicit_signal(
    repo_root: Path,
) -> None:
    launcher = load_launcher(repo_root)
    adapter = launcher._engine.resolve_source_context(repo_root)

    assert adapter.record("core") == repo_root / "governance-core"
    assert adapter.record("task_contracts") == repo_root / "docs" / "tasks"
    assert adapter.record("task_contract_policy") == repo_root / "docs" / "TASK-CONTRACTS.md"
    assert adapter.record("testing_and_evaluation") == (
        repo_root / "docs" / "TESTING-AND-EVALUATION.md"
    )
    assert adapter.record("orchestrator_checkpoint") == (
        repo_root / "docs" / "orchestrator" / "CHECKPOINT.md"
    )
    assert adapter.record("executor_handoffs") == repo_root / "handoffs"
    assert adapter.handoff_write_path("handoffs/T022-executor-handoff.json") == (
        repo_root / "handoffs" / "T022-executor-handoff.json"
    )


@pytest.mark.parametrize(
    "relative",
    [
        "docs/tasks/T022-source-maintainer-profile-over-legacy-adapters.md",
        "AGENTS.md",
        "src/agent_governance/engine.py",
        ".agent-coordination/STATE.json",
        "handoffs/not-json.md",
        "handoffs/nested/result.json",
        "../outside.json",
    ],
)
def test_source_write_adapter_rejects_markdown_consumer_and_out_of_scope_paths(
    repo_root: Path, relative: str
) -> None:
    launcher = load_launcher(repo_root)
    context = launcher._engine.resolve_source_context(repo_root)
    with pytest.raises(launcher._engine.SourceContextError):
        context.handoff_write_path(relative)


def test_engine_routes_source_context_without_consumer_initialization(
    repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    launcher = load_launcher(repo_root)
    result = launcher._engine.main(
        ["context", str(repo_root), "--record", "core"],
        package_paths=launcher._package_paths(),
        profile=launcher._engine.resolve_profile("source-maintainer"),
    )

    assert result == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["profile"] == "source-maintainer"
    assert payload["signal_schema_version"] == "1.0.0"
    assert payload["record"] == "core"
    assert Path(payload["path"]) == repo_root / "governance-core"
    assert not (repo_root / ".agent-governance").exists()
    assert not (repo_root / ".agent-coordination").exists()


def test_engine_validates_source_context_without_consumer_initialization(
    repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    launcher = load_launcher(repo_root)
    result = launcher._engine.main(
        ["validate", str(repo_root)],
        package_paths=launcher._package_paths(),
        profile=launcher._engine.resolve_profile("source-maintainer"),
    )

    assert result == 0
    assert "validated source-maintainer context" in capsys.readouterr().out
    assert not (repo_root / ".agent-governance").exists()
    assert not (repo_root / ".agent-coordination").exists()


@pytest.mark.parametrize(
    "command", ["bootstrap", "state", "event", "skill", "ecosystem", "archive"]
)
def test_source_profile_rejects_consumer_operations_before_mutation(
    tmp_path: Path,
    repo_root: Path,
    capsys: pytest.CaptureFixture[str],
    command: str,
) -> None:
    launcher = load_launcher(repo_root)
    target = stage_source(repo_root, tmp_path / command)
    argv = {
        "bootstrap": ["bootstrap", str(target)],
        "state": ["state", str(target)],
        "event": ["event", str(target), "--actor", "implementation", "--event", "start"],
        "skill": ["skill", str(target), "--approval", "x", "--candidate", "y"],
        "ecosystem": ["ecosystem", str(target), "--facts", "{}"],
        "archive": ["archive", str(target)],
    }[command]

    result = launcher._engine.main(
        argv,
        package_paths=launcher._package_paths(),
        profile=launcher._engine.resolve_profile("source-maintainer"),
    )

    assert result == 1
    assert "unavailable for source-maintainer profile" in capsys.readouterr().err
    assert not (target / ".agent-governance").exists()
    assert not (target / ".agent-coordination").exists()


@pytest.mark.parametrize(
    ("signal", "expected"),
    [
        (None, "missing or unsafe explicit source-product signal"),
        ({"signal_schema_version": "1.0.0"}, "unexpected or missing fields"),
        (
            {
                "signal_schema_version": "2.0.0",
                "product_id": "agent-governance",
                "profile": "source-maintainer",
            },
            "identity or version is unsupported",
        ),
        (
            {
                "signal_schema_version": "1.0.0",
                "product_id": "other-product",
                "profile": "source-maintainer",
            },
            "identity or version is unsupported",
        ),
        (
            {
                "signal_schema_version": "1.0.0",
                "product_id": "agent-governance",
                "profile": "consumer",
            },
            "identity or version is unsupported",
        ),
    ],
)
def test_source_context_fails_closed_without_exact_versioned_signal(
    tmp_path: Path,
    repo_root: Path,
    signal: dict[str, str] | None,
    expected: str,
) -> None:
    launcher = load_launcher(repo_root)
    target = stage_source(repo_root, tmp_path / "source")
    signal_path = target / "agent-governance-source.json"
    if signal is None:
        signal_path.unlink()
    else:
        signal_path.write_text(json.dumps(signal), encoding="utf-8")

    with pytest.raises(launcher._engine.SourceContextError, match=expected):
        launcher._engine.resolve_source_context(target)
    assert not (target / ".agent-governance").exists()
    assert not (target / ".agent-coordination").exists()


def test_source_context_rejects_directory_name_inference_and_ambiguous_consumer_state(
    tmp_path: Path, repo_root: Path
) -> None:
    launcher = load_launcher(repo_root)
    unsigned = tmp_path / "unsigned"
    unsigned.mkdir()
    (unsigned / "governance-core").mkdir()
    with pytest.raises(launcher._engine.SourceContextError, match="explicit source-product signal"):
        launcher._engine.resolve_source_context(unsigned)

    ambiguous = stage_source(repo_root, tmp_path / "ambiguous")
    (ambiguous / ".agent-coordination").mkdir()
    with pytest.raises(launcher._engine.SourceContextError, match="ambiguous source/consumer"):
        launcher._engine.resolve_source_context(ambiguous)


def test_source_context_rejects_legacy_record_with_wrong_type(
    tmp_path: Path, repo_root: Path
) -> None:
    launcher = load_launcher(repo_root)
    target = stage_source(repo_root, tmp_path / "wrong-type")
    shutil.rmtree(target / "governance-core")
    (target / "governance-core").write_text("not a Core directory", encoding="utf-8")

    with pytest.raises(launcher._engine.SourceContextError, match="governance-core"):
        launcher._engine.resolve_source_context(target)


def test_consumer_profile_cannot_route_source_context(
    repo_root: Path,
) -> None:
    launcher = load_launcher(repo_root)
    parser = launcher._engine._parser(launcher._engine.resolve_profile("consumer"))
    assert "context" not in parser._subparsers._group_actions[0].choices
    assert not (repo_root / ".agent-governance").exists()
    assert not (repo_root / ".agent-coordination").exists()
