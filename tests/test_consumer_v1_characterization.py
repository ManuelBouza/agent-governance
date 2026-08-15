"""Pre-refactor characterization for the Consumer Governance v1 package boundary."""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path


def load_cli(cli: Path):
    spec = importlib.util.spec_from_file_location("consumer_v1_characterization", cli)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_bootstrap(cli: Path, target: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(cli), "bootstrap", str(target)],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_source_package_paths_resolve_sibling_core_and_skill_assets(repo_root: Path) -> None:
    cli = repo_root / "governance-skill" / "scripts" / "governance.py"
    core, assets = load_cli(cli)._package_paths()

    assert core == repo_root / "governance-core"
    assert assets == repo_root / "governance-skill" / "assets"


def test_bootstrap_requires_sibling_core_source_bundle(tmp_path: Path, repo_root: Path) -> None:
    package = tmp_path / "package"
    shutil.copytree(repo_root / "governance-skill", package / "governance-skill")
    cli = package / "governance-skill" / "scripts" / "governance.py"
    target = tmp_path / "consumer"
    target.mkdir()

    missing_core = run_bootstrap(cli, target)
    assert missing_core.returncode == 1
    assert str(package / "governance-core" / "GOVERNANCE.md") in missing_core.stderr
    assert not (target / ".agent-governance").exists()
    assert not (target / ".agent-coordination").exists()

    shutil.copytree(repo_root / "governance-core", package / "governance-core")
    bundled = run_bootstrap(cli, target)
    assert bundled.returncode == 0, bundled.stderr
    assert (target / ".agent-governance" / "GOVERNANCE.md").is_file()
    assert (target / ".agent-coordination" / "STATE.json").is_file()
