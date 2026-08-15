"""Focused deterministic tests for the T021 consumer profile abstraction.

AC-T021-1 — zero Consumer drift: ``consumer`` resolves to a Profile whose
properties preserve the frozen T018 behavioral baseline.

AC-T021-2 — fail-closed profile routing: unsupported or ambiguous profile
values are rejected with ``ProfileError`` rather than routed with broader
permissions.

AC-T021-3 — artifact compatibility: the built artifact bundles
``profile.py`` in its runtime and the launcher resolves ``consumer`` from
inside the artifact boundary.
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_profile(repo_root: Path):
    return load_module(
        repo_root / "src" / "agent_governance" / "profile.py", "t021_profile_under_test"
    )


def load_builder(repo_root: Path):
    return load_module(
        repo_root / "src" / "agent_governance" / "artifact.py", "t021_builder_under_test"
    )


# -- AC-T021-1: zero Consumer drift --------------------------------------------


def test_default_profile_resolves_to_consumer(repo_root: Path) -> None:
    profile_mod = load_profile(repo_root)
    profile = profile_mod.resolve_profile()
    assert profile.name == "consumer"
    assert profile.is_consumer
    assert not profile.is_source_maintainer
    assert not profile.grants_source_maintenance


def test_explicit_consumer_matches_default(repo_root: Path) -> None:
    profile_mod = load_profile(repo_root)
    assert profile_mod.resolve_profile("consumer") == profile_mod.resolve_profile(None)


def test_engine_exports_profile_symbols(repo_root: Path) -> None:
    launcher = repo_root / "governance-skill" / "scripts" / "governance.py"
    module = load_module(launcher, "t021_engine_via_launcher")
    engine = module._engine
    assert hasattr(engine, "resolve_profile")
    assert hasattr(engine, "Profile")
    assert hasattr(engine, "ProfileError")
    assert callable(engine.resolve_profile)


def test_engine_main_accepts_consumer_profile_without_behavior_change(
    tmp_path: Path, repo_root: Path
) -> None:
    launcher = repo_root / "governance-skill" / "scripts" / "governance.py"
    target = tmp_path / "consumer"
    target.mkdir()
    result = subprocess.run(
        [sys.executable, str(launcher), "bootstrap", str(target)],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert (target / ".agent-governance" / "GOVERNANCE.md").is_file()
    assert (target / ".agent-coordination" / "STATE.json").is_file()


# -- AC-T021-2: fail-closed profile routing -----------------------------------


@pytest.mark.parametrize(
    "bad_name",
    [
        "source-maintainer",
        "maintainer",
        "admin",
        "",
        "CONSUMER",
        "Consumer",
        " consumer ",
        "consumer,source-maintainer",
        123,
        True,
        [],
    ],
)
def test_resolve_profile_rejects_unsupported_or_ambiguous_values(
    repo_root: Path, bad_name: object
) -> None:
    profile_mod = load_profile(repo_root)
    with pytest.raises(profile_mod.ProfileError):
        profile_mod.resolve_profile(bad_name)  # type: ignore[arg-type]


def test_no_active_profile_grants_source_maintenance(repo_root: Path) -> None:
    profile_mod = load_profile(repo_root)
    for name in profile_mod.ACTIVE_PROFILES:
        profile = profile_mod.resolve_profile(name)
        assert not profile.grants_source_maintenance, name


def test_source_maintainer_is_not_active(repo_root: Path) -> None:
    profile_mod = load_profile(repo_root)
    assert "source-maintainer" not in profile_mod.ACTIVE_PROFILES
    with pytest.raises(profile_mod.ProfileError):
        profile_mod.resolve_profile("source-maintainer")


# -- AC-T021-3: artifact compatibility ----------------------------------------


def stage_build_source(repo_root: Path, destination: Path) -> Path:
    for relative in ("governance-core", "governance-skill", "src/agent_governance", "schemas"):
        shutil.copytree(repo_root / relative, destination / relative)
    return destination


def test_artifact_bundles_profile_module_in_runtime(repo_root: Path, tmp_path: Path) -> None:
    builder = load_builder(repo_root)
    source = stage_build_source(repo_root, tmp_path / "disposable-source")
    artifact = tmp_path / "governance-skill"
    builder.build_artifact(
        source,
        artifact,
        skill_version="0.1.0",
        installed_footprint_version="1.0.0",
        source_commit="b" * 40,
    )

    profile_in_artifact = artifact / "runtime" / "agent_governance" / "profile.py"
    assert profile_in_artifact.is_file()
    assert (
        profile_in_artifact.read_bytes()
        == (repo_root / "src" / "agent_governance" / "profile.py").read_bytes()
    )


def test_launcher_resolves_consumer_profile_inside_artifact(
    repo_root: Path, tmp_path: Path
) -> None:
    builder = load_builder(repo_root)
    source = stage_build_source(repo_root, tmp_path / "disposable-source")
    artifact = tmp_path / "governance-skill"
    builder.build_artifact(
        source,
        artifact,
        skill_version="0.1.0",
        installed_footprint_version="1.0.0",
        source_commit="c" * 40,
    )
    shutil.rmtree(source)
    assert not source.exists()

    cli = artifact / "scripts" / "governance.py"
    isolated = tmp_path / "isolated"
    isolated.mkdir()

    probe = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import importlib.util, pathlib; "
                f"p=pathlib.Path({str(cli)!r}); "
                "s=importlib.util.spec_from_file_location('t021_artifact_probe', p); "
                "m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "
                "prof=m._engine.resolve_profile(); "
                "print(prof.name, prof.is_consumer, prof.grants_source_maintenance)"
            ),
        ],
        cwd=isolated,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert probe.returncode == 0, probe.stderr
    assert probe.stdout.strip() == "consumer True False"
