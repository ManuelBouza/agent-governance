"""Focused deterministic tests for safe consumer bootstrap and validation."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


def symlink_or_skip(link: Path, target: str | Path, *, target_is_directory: bool = False) -> None:
    try:
        link.symlink_to(target, target_is_directory=target_is_directory)
    except OSError as error:
        if getattr(error, "winerror", None) == 1314:
            pytest.skip("native Windows host does not grant symbolic-link creation privilege")
        raise


@pytest.fixture
def governance_cli(repo_root: Path) -> Path:
    return repo_root / "governance-skill" / "scripts" / "governance.py"


def run_cli(cli: Path, command: str, target: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(cli), command, str(target)],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )


def load_cli(cli: Path):
    spec = importlib.util.spec_from_file_location("governance_cli_under_test", cli)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def installed_repo(tmp_path: Path, governance_cli: Path) -> Path:
    target = tmp_path / "unrelated-repository"
    target.mkdir()
    (target / "application.txt").write_text("unrelated\n", encoding="utf-8")
    result = run_cli(governance_cli, "bootstrap", target)
    assert result.returncode == 0, result.stderr
    return target


def test_bootstrap_creates_canonical_footprint_without_touching_project(
    installed_repo: Path, repo_root: Path
) -> None:
    assert (installed_repo / "application.txt").read_text(encoding="utf-8") == "unrelated\n"
    core_names = {path.name for path in (repo_root / "governance-core").glob("*.md")}
    assert {path.name for path in (installed_repo / ".agent-governance").iterdir()} == core_names
    coordination = installed_repo / ".agent-coordination"
    assert {"MISSION.md", "WORKPLAN.md", "CAPABILITIES.json", "STATE.json", "EXCHANGE.jsonl"} <= {
        path.name for path in coordination.iterdir()
    }
    assert all((coordination / name).is_dir() for name in ("tasks", "skills", "decisions"))


@pytest.mark.parametrize("collision", [".agent-governance", ".agent-coordination"])
@pytest.mark.parametrize("collision_kind", ["directory", "file", "symlink"])
def test_bootstrap_refuses_managed_collision_without_partial_writes(
    tmp_path: Path, governance_cli: Path, collision: str, collision_kind: str
) -> None:
    target = tmp_path / "consumer"
    target.mkdir()
    existing = target / collision
    if collision_kind == "directory":
        existing.mkdir()
        sentinel = existing / "sentinel"
    elif collision_kind == "file":
        sentinel = existing
    else:
        symlink_target = tmp_path / "managed-symlink-target"
        symlink_target.mkdir(exist_ok=True)
        symlink_or_skip(existing, symlink_target, target_is_directory=True)
        sentinel = symlink_target / "sentinel"
    sentinel.write_text("keep", encoding="utf-8")
    result = run_cli(governance_cli, "bootstrap", target)
    assert result.returncode != 0
    assert "collision" in result.stderr
    assert sentinel.read_text(encoding="utf-8") == "keep"
    other = ".agent-coordination" if collision == ".agent-governance" else ".agent-governance"
    assert not (target / other).exists()


@pytest.mark.parametrize("unsafe_kind", ["missing", "file", "symlink", "source"])
def test_bootstrap_refuses_unsafe_target_without_writes(
    tmp_path: Path, governance_cli: Path, unsafe_kind: str
) -> None:
    target = tmp_path / unsafe_kind
    if unsafe_kind == "file":
        target.write_text("not a directory", encoding="utf-8")
    elif unsafe_kind == "symlink":
        real = tmp_path / "real"
        real.mkdir()
        symlink_or_skip(target, real, target_is_directory=True)
    elif unsafe_kind == "source":
        target.mkdir()
        (target / "governance-core").mkdir()
    result = run_cli(governance_cli, "bootstrap", target)
    assert result.returncode != 0
    if target.is_dir():
        assert not (target / ".agent-governance").exists()
        assert not (target / ".agent-coordination").exists()


def test_bootstrap_consumes_markdown_templates_without_modifying_them(
    tmp_path: Path, repo_root: Path
) -> None:
    package = tmp_path / "package"
    shutil.copytree(repo_root / "governance-core", package / "governance-core")
    shutil.copytree(repo_root / "governance-skill", package / "governance-skill")
    assets = package / "governance-skill" / "assets"
    before = {
        name: (assets / name).read_bytes()
        for name in ("MISSION.template.md", "WORKPLAN.template.md", "TASK.template.md")
    }
    target = tmp_path / "consumer"
    target.mkdir()
    cli = package / "governance-skill" / "scripts" / "governance.py"
    result = run_cli(cli, "bootstrap", target)
    assert result.returncode == 0, result.stderr
    assert (target / ".agent-coordination" / "MISSION.md").read_bytes() == before[
        "MISSION.template.md"
    ]
    assert (target / ".agent-coordination" / "WORKPLAN.md").read_bytes() == before[
        "WORKPLAN.template.md"
    ]
    assert (target / ".agent-coordination" / "tasks" / "TASK.template.md").read_bytes() == before[
        "TASK.template.md"
    ]
    assert {name: (assets / name).read_bytes() for name in before} == before


def test_bootstrap_race_does_not_remove_unowned_root(
    tmp_path: Path, governance_cli: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "consumer"
    target.mkdir()
    module = load_cli(governance_cli)
    original_mkdir = Path.mkdir
    raced = target / ".agent-coordination"

    def racing_mkdir(path: Path, *args, **kwargs) -> None:
        if path == raced:
            original_mkdir(path, *args, **kwargs)
            (path / "other-process").write_text("owned elsewhere", encoding="utf-8")
            raise FileExistsError(path)
        original_mkdir(path, *args, **kwargs)

    monkeypatch.setattr(Path, "mkdir", racing_mkdir)
    with pytest.raises(FileExistsError):
        module._bootstrap(target)
    assert not (target / ".agent-governance").exists()
    assert (raced / "other-process").read_text(encoding="utf-8") == "owned elsewhere"


def test_bootstrap_prevalidates_package_before_mutation(tmp_path: Path, repo_root: Path) -> None:
    package = tmp_path / "package"
    shutil.copytree(repo_root / "governance-core", package / "governance-core")
    shutil.copytree(repo_root / "governance-skill", package / "governance-skill")
    (package / "governance-skill" / "assets" / "STATE.template.json").write_text(
        "{}", encoding="utf-8"
    )
    target = tmp_path / "consumer"
    target.mkdir()
    result = run_cli(
        package / "governance-skill" / "scripts" / "governance.py", "bootstrap", target
    )
    assert result.returncode != 0
    assert not (target / ".agent-governance").exists()
    assert not (target / ".agent-coordination").exists()


@pytest.mark.parametrize("failure", ["copy", "post_validation"])
def test_bootstrap_rolls_back_owned_roots_after_mutation_failure(
    tmp_path: Path,
    governance_cli: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    target = tmp_path / "consumer"
    target.mkdir()
    module = load_cli(governance_cli)
    if failure == "copy":
        original_copyfile = module.shutil.copyfile
        calls = 0

        def failing_copyfile(source: Path, destination: Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected copy failure")
            original_copyfile(source, destination)

        monkeypatch.setattr(module.shutil, "copyfile", failing_copyfile)
    else:
        monkeypatch.setattr(
            module,
            "_validate",
            lambda _target: (_ for _ in ()).throw(
                module.GovernanceError("injected validation failure")
            ),
        )
    with pytest.raises((OSError, module.GovernanceError)):
        module._bootstrap(target)
    assert not (target / ".agent-governance").exists()
    assert not (target / ".agent-coordination").exists()


def test_validation_is_source_independent_and_read_only(tmp_path: Path, repo_root: Path) -> None:
    package = tmp_path / "package"
    shutil.copytree(repo_root / "governance-core", package / "governance-core")
    shutil.copytree(repo_root / "governance-skill", package / "governance-skill")
    cli = package / "governance-skill" / "scripts" / "governance.py"
    target = tmp_path / "consumer"
    target.mkdir()
    assert run_cli(cli, "bootstrap", target).returncode == 0
    standalone_cli = tmp_path / "standalone-governance.py"
    shutil.copyfile(cli, standalone_cli)
    shutil.rmtree(package)
    before = {
        path.relative_to(target): path.read_bytes() for path in target.rglob("*") if path.is_file()
    }
    result = run_cli(standalone_cli, "validate", target)
    after = {
        path.relative_to(target): path.read_bytes() for path in target.rglob("*") if path.is_file()
    }
    assert result.returncode == 0, result.stderr
    assert after == before


@pytest.mark.parametrize(
    ("relative_path", "content", "error_text"),
    [
        (".agent-governance/GOVERNANCE.md", "# no authority\n", "Protocol-Version"),
        (
            ".agent-governance/GOVERNANCE.md",
            "Protocol-Version: 1.13.0\nProtocol-Version: 1.13.0\n",
            "exactly one",
        ),
        (".agent-coordination/STATE.json", "{broken", "malformed JSON"),
        (".agent-coordination/EXCHANGE.jsonl", "{broken\n", "malformed JSONL"),
        (
            ".agent-coordination/EXCHANGE.jsonl",
            '{"q":1,"a":"human","e":"start"}\n{"q":1,"a":"strategy","e":"progress"}\n',
            "must increase",
        ),
    ],
)
def test_validate_fails_closed_for_malformed_installation(
    installed_repo: Path,
    governance_cli: Path,
    relative_path: str,
    content: str,
    error_text: str,
) -> None:
    (installed_repo / relative_path).write_text(content, encoding="utf-8")
    result = run_cli(governance_cli, "validate", installed_repo)
    assert result.returncode != 0
    assert error_text in result.stderr


def test_validate_rejects_missing_file(installed_repo: Path, governance_cli: Path) -> None:
    (installed_repo / ".agent-governance" / "PROTOCOL.md").unlink()
    result = run_cli(governance_cli, "validate", installed_repo)
    assert result.returncode != 0
    assert "missing" in result.stderr


def test_validate_rejects_core_reference_version_inconsistency(
    installed_repo: Path, governance_cli: Path
) -> None:
    state_path = installed_repo / ".agent-coordination" / "STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["protocol_version"] = "9.0.0"
    state_path.write_text(json.dumps(state), encoding="utf-8")
    result = run_cli(governance_cli, "validate", installed_repo)
    assert result.returncode != 0
    assert "version inconsistency" in result.stderr


def test_validate_rejects_unresolved_core_reference(
    installed_repo: Path, governance_cli: Path
) -> None:
    governance_path = installed_repo / ".agent-governance" / "GOVERNANCE.md"
    governance_path.write_text(
        governance_path.read_text(encoding="utf-8")
        + "\n- invalid route -> `.agent-governance/UNKNOWN.md`\n",
        encoding="utf-8",
    )
    result = run_cli(governance_cli, "validate", installed_repo)
    assert result.returncode != 0
    assert "routed Core references" in result.stderr


@pytest.mark.parametrize(
    ("relative_path", "replacement", "error_text"),
    [
        (".agent-governance/QUALITY.md", "\n", "non-empty"),
        (".agent-governance/QUALITY.md", "# Quality\n", "Quality-Module-Version"),
        (
            ".agent-governance/GOVERNANCE.md",
            "Protocol-Version: 1.13.0\n` .agent-governance/GOVERNANCE.md`\n",
            "routed Core references",
        ),
    ],
)
def test_validate_rejects_stripped_or_structurally_tampered_core(
    installed_repo: Path,
    governance_cli: Path,
    relative_path: str,
    replacement: str,
    error_text: str,
) -> None:
    (installed_repo / relative_path).write_text(replacement, encoding="utf-8")
    result = run_cli(governance_cli, "validate", installed_repo)
    assert result.returncode != 0
    assert error_text in result.stderr


@pytest.mark.parametrize(
    ("relative_path", "mutate", "error_text"),
    [
        (
            ".agent-coordination/CAPABILITIES.json",
            lambda value: value.update({"capabilities": [{"classification": "INSTALL"}]}),
            "invalid classification",
        ),
        (
            ".agent-coordination/STATE.json",
            lambda value: value.update({"ready_tasks": [1]}),
            "string arrays",
        ),
        (
            ".agent-coordination/STATE.json",
            lambda value: value.update({"gates": {"F0": "passed"}}),
            "map strings to booleans",
        ),
        (
            ".agent-coordination/skills/SKILL-APPROVAL.template.json",
            lambda value: value.update({"status": "INSTALLED"}),
            "status is invalid",
        ),
        (
            ".agent-coordination/skills/SKILL-APPROVAL.template.json",
            lambda value: value.update({"approval": {"authority": []}}),
            "approval has invalid structure",
        ),
    ],
)
def test_validate_rejects_invalid_json_schema(
    installed_repo: Path,
    governance_cli: Path,
    relative_path: str,
    mutate,
    error_text: str,
) -> None:
    path = installed_repo / relative_path
    value = json.loads(path.read_text(encoding="utf-8"))
    mutate(value)
    path.write_text(json.dumps(value), encoding="utf-8")
    result = run_cli(governance_cli, "validate", installed_repo)
    assert result.returncode != 0
    assert error_text in result.stderr


@pytest.mark.parametrize("entry_kind", ["file", "directory", "symlink"])
def test_validate_rejects_unexpected_coordination_root_entry(
    installed_repo: Path, governance_cli: Path, entry_kind: str
) -> None:
    entry = installed_repo / ".agent-coordination" / "unexpected"
    if entry_kind == "file":
        entry.write_text("unexpected", encoding="utf-8")
    elif entry_kind == "directory":
        entry.mkdir()
    else:
        symlink_or_skip(entry, "missing")
    result = run_cli(governance_cli, "validate", installed_repo)
    assert result.returncode != 0
    assert "ambiguous coordination root" in result.stderr


def test_validate_rejects_managed_symlink(installed_repo: Path, governance_cli: Path) -> None:
    symlink_or_skip(installed_repo / ".agent-coordination" / "tasks" / "linked-task", "missing")
    result = run_cli(governance_cli, "validate", installed_repo)
    assert result.returncode != 0
    assert "unsafe managed symlinks" in result.stderr


def test_validate_rejects_source_consumer_mixing(
    installed_repo: Path, governance_cli: Path
) -> None:
    (installed_repo / "maintainer-skill").mkdir()
    result = run_cli(governance_cli, "validate", installed_repo)
    assert result.returncode != 0
    assert "source/consumer separation" in result.stderr


def test_validate_rejects_dangling_source_marker(
    installed_repo: Path, governance_cli: Path
) -> None:
    symlink_or_skip(installed_repo / "governance-core", "missing")
    result = run_cli(governance_cli, "validate", installed_repo)
    assert result.returncode != 0
    assert "source/consumer separation" in result.stderr


def test_source_root_has_no_live_consumer_footprint(repo_root: Path) -> None:
    assert not (repo_root / ".agent-governance").exists()
    assert not (repo_root / ".agent-coordination").exists()
