"""Self-contained Governance Skill artifact and identity coverage."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

from test_consumer_governance_cli_v1 import approval_record, configure_mission, ecosystem_facts


def load_builder(repo_root: Path):
    path = repo_root / "src" / "agent_governance" / "artifact.py"
    spec = importlib.util.spec_from_file_location("governance_artifact_builder", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_cli(cli: Path, *arguments: object, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(cli), *(str(argument) for argument in arguments)],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def stage_build_source(repo_root: Path, destination: Path) -> Path:
    for relative in ("governance-core", "governance-skill", "src/agent_governance", "schemas"):
        shutil.copytree(repo_root / relative, destination / relative)
    return destination


def test_builder_cli_derives_source_commit(tmp_path: Path, repo_root: Path) -> None:
    builder_path = repo_root / "src" / "agent_governance" / "artifact.py"
    artifact = tmp_path / "artifact"
    result = subprocess.run(
        [
            sys.executable,
            str(builder_path),
            str(artifact),
            "--skill-version",
            "0.1.0",
            "--installed-footprint-version",
            "1.0.0",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    identity = json.loads(result.stdout)
    expected_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    ).stdout.strip()
    assert identity["source_commit"] == expected_commit
    assert json.loads((artifact / "artifact-identity.json").read_text(encoding="utf-8")) == identity


def test_repeated_builds_have_identical_verified_identity(tmp_path: Path, repo_root: Path) -> None:
    builder = load_builder(repo_root)
    commit = "a" * 40
    artifacts = [tmp_path / "first", tmp_path / "second"]

    identities = [
        builder.build_artifact(
            repo_root,
            artifact,
            skill_version="0.1.0",
            installed_footprint_version="1.0.0",
            source_commit=commit,
        )
        for artifact in artifacts
    ]

    assert identities[0] == identities[1]
    assert (artifacts[0] / builder.IDENTITY_FILENAME).read_bytes() == (
        artifacts[1] / builder.IDENTITY_FILENAME
    ).read_bytes()
    identity = identities[0]
    assert identity["build_schema_version"] == "1.0.0"
    assert identity["skill_version"] == "0.1.0"
    assert identity["protocol_version"] == builder._protocol_version(
        repo_root / "governance-core" / "GOVERNANCE.md"
    )
    assert identity["installed_footprint_version"] == "1.0.0"
    assert identity["source_commit"] == commit

    files = identity["files"]
    assert [entry["path"] for entry in files] == sorted(entry["path"] for entry in files)
    assert identity["payload_digest"] == hashlib.sha256(canonical_json(files)).hexdigest()
    unsigned = {key: value for key, value in identity.items() if key != "identity_digest"}
    assert identity["identity_digest"] == hashlib.sha256(canonical_json(unsigned)).hexdigest()
    expected_skill_files = {
        "SKILL.md",
        "assets/CAPABILITIES.template.json",
        "assets/EXCHANGE.template.jsonl",
        "assets/MISSION.template.md",
        "assets/REPOSITORY-BRANCH-PROTECTION.md",
        "assets/RUNBOOK-RECIPE.template.json",
        "assets/RUNBOOK.template.md",
        "assets/SKILL-APPROVAL.template.json",
        "assets/STATE.template.json",
        "assets/TASK.template.md",
        "assets/WORKPLAN.template.md",
        "scripts/governance.py",
    }
    generated_skill_files = {
        path.relative_to(artifacts[0]).as_posix()
        for path in artifacts[0].rglob("*")
        if path.is_file()
        and path.parts[-1] != "artifact-identity.json"
        and "core" not in path.relative_to(artifacts[0]).parts
        and "runtime" not in path.relative_to(artifacts[0]).parts
        and path.name != "governance-artifact-identity.schema.json"
    }
    assert generated_skill_files == expected_skill_files
    assert (artifacts[0] / "assets" / "REPOSITORY-BRANCH-PROTECTION.md").read_bytes() == (
        repo_root / "governance-skill" / "assets" / "REPOSITORY-BRANCH-PROTECTION.md"
    ).read_bytes()
    assert not (artifacts[0] / "STATUS.md").exists()
    for entry in files:
        path = artifacts[0] / entry["path"]
        assert path.stat().st_size == entry["size"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
    for source, destination in (
        (repo_root / "governance-core", artifacts[0] / "core"),
        (repo_root / "governance-skill" / "assets", artifacts[0] / "assets"),
        (
            repo_root / "src" / "agent_governance",
            artifacts[0] / "runtime" / "agent_governance",
        ),
    ):
        source_files = sorted(
            path.relative_to(source) for path in source.rglob("*") if path.is_file()
        )
        generated_files = sorted(
            path.relative_to(destination)
            for path in destination.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
        )
        expected_files = [
            path
            for path in source_files
            if "__pycache__" not in path.parts and path.suffix != ".pyc"
        ]
        assert generated_files == expected_files
        for relative in expected_files:
            assert (destination / relative).read_bytes() == (source / relative).read_bytes()
    assert (artifacts[0] / "governance-artifact-identity.schema.json").read_bytes() == (
        repo_root / "schemas" / "governance-artifact-identity.schema.json"
    ).read_bytes()


def test_inventory_uses_canonical_relative_path_string_order(
    tmp_path: Path, repo_root: Path
) -> None:
    builder = load_builder(repo_root)
    artifact = tmp_path / "artifact"
    for relative in ("a/file.txt", "Z/file.txt"):
        path = artifact / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(relative.encode())

    assert [entry["path"] for entry in builder._inventory(artifact)] == [
        "Z/file.txt",
        "a/file.txt",
    ]


def test_artifact_runs_without_source_or_sibling_dependencies(
    tmp_path: Path, repo_root: Path
) -> None:
    builder = load_builder(repo_root)
    isolated = tmp_path / "isolated"
    isolated.mkdir()
    source = stage_build_source(repo_root, tmp_path / "disposable-source")
    artifact = isolated / "governance-skill"
    builder.build_artifact(
        source,
        artifact,
        skill_version="0.1.0",
        installed_footprint_version="1.0.0",
        source_commit="b" * 40,
    )
    shutil.rmtree(source)
    assert not source.exists()
    cli = artifact / "scripts" / "governance.py"
    consumer = isolated / "unrelated-repository"
    consumer.mkdir()

    probe = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import importlib.util, pathlib; "
                f"p=pathlib.Path({str(cli)!r}); "
                "s=importlib.util.spec_from_file_location('artifact_cli', p); "
                "m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "
                "print(m._engine.__file__); print(*m._package_paths(), sep='\\n')"
            ),
        ],
        cwd=isolated,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert probe.returncode == 0, probe.stderr
    assert probe.stdout.splitlines() == [
        str(artifact / "runtime" / "agent_governance" / "engine.py"),
        str(artifact / "core"),
        str(artifact / "assets"),
    ]
    assert sorted(path.name for path in isolated.iterdir()) == [
        "governance-skill",
        "unrelated-repository",
    ]

    bootstrap = run_cli(cli, "bootstrap", consumer, cwd=isolated)
    assert bootstrap.returncode == 0, bootstrap.stderr
    validate = run_cli(cli, "validate", consumer, cwd=isolated)
    assert validate.returncode == 0, validate.stderr
    configure_mission(consumer)
    state = run_cli(cli, "state", consumer, cwd=isolated)
    assert state.returncode == 1
    assert "STATE is stale" in state.stderr
    state = run_cli(cli, "state", consumer, "--refresh", cwd=isolated)
    assert state.returncode == 0, state.stderr
    assert json.loads(state.stdout)["protocol_version"] == builder._protocol_version(
        artifact / "core" / "GOVERNANCE.md"
    )

    for event, arguments in (
        ("start", ("--next-action", "Execute T1")),
        ("progress", ("--reference", "commit:abc")),
        ("done", ("--reference", "commit:def", "--verification", "passed")),
    ):
        result = run_cli(
            cli,
            "event",
            consumer,
            "--actor",
            "implementation",
            "--event",
            event,
            "--task",
            "T1",
            *arguments,
            cwd=isolated,
        )
        assert result.returncode == 0, result.stderr

    approval, candidate, _facts = approval_record(consumer)
    skill = run_cli(
        cli,
        "skill",
        consumer,
        "--approval",
        approval.relative_to(consumer),
        "--candidate",
        candidate.relative_to(consumer),
        cwd=isolated,
    )
    assert skill.returncode == 0, skill.stderr
    assert json.loads(skill.stdout) == {"skill_id": "S1", "status": "VALID"}

    facts = ecosystem_facts(consumer)
    ecosystem = run_cli(
        cli,
        "ecosystem",
        consumer,
        "--facts",
        facts.relative_to(consumer),
        "--update",
        cwd=isolated,
    )
    assert ecosystem.returncode == 0, ecosystem.stderr
    capabilities = json.loads(
        (consumer / ".agent-coordination" / "CAPABILITIES.json").read_text(encoding="utf-8")
    )
    assert [item["classification"] for item in capabilities["capabilities"]] == [
        "REUSE",
        "CONFLICT",
        "MISSING",
    ]

    events = [
        json.loads(line)
        for line in (consumer / ".agent-coordination" / "EXCHANGE.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    configure_mission(
        consumer,
        mission_status="COMPLETED",
        tasks=(("T1", "none", "DONE"),),
        current="none",
        exchange=events,
    )
    refreshed = run_cli(cli, "state", consumer, "--refresh", cwd=isolated)
    assert refreshed.returncode == 0, refreshed.stderr
    archive = run_cli(cli, "archive", consumer, "--prepare", cwd=isolated)
    assert archive.returncode == 0, archive.stderr
    assert (consumer / ".agent-coordination" / "archive" / "M1" / "EXCHANGE.jsonl").is_file()

    help_result = run_cli(cli, "--help", cwd=isolated)
    assert help_result.returncode == 0
    assert "{bootstrap,validate,state,event,skill,ecosystem,archive}" in help_result.stdout
