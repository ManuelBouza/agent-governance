"""Deterministic coverage for the T050 code-health checker and source map."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def code_health(repo_root: Path):
    path = repo_root / "tools" / "code_health.py"
    spec = importlib.util.spec_from_file_location("t050_code_health", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _config() -> dict:
    return {
        "schema_version": 1,
        "hard_limit": 5,
        "governed_roots": ["pkg"],
        "exclude_directories": ["__pycache__"],
        "ratchets": {"pkg/legacy.py": 7},
        "complexity_paths": ["pkg/*.py"],
        "symbol_map_paths": ["pkg/*.py"],
        "dependency_package": "pkg",
        "dependency_layers": [["base"], ["feature"], ["legacy"]],
    }


def _fixture(tmp_path: Path) -> tuple[Path, dict]:
    package = tmp_path / "pkg"
    package.mkdir()
    (package / "base.py").write_text("VALUE = 1\n", encoding="utf-8", newline="\n")
    (package / "feature.py").write_text(
        "from .base import VALUE\n\ndef use():\n    return VALUE\n",
        encoding="utf-8",
        newline="\n",
    )
    (package / "legacy.py").write_text(
        "from .feature import use\n\n\ndef one():\n    return use()\n\n",
        encoding="utf-8",
        newline="\n",
    )
    return tmp_path, _config()


def test_configuration_fails_closed_on_malformed_ratchet(tmp_path: Path, code_health) -> None:
    path = tmp_path / "config.json"
    config = _config()
    config["ratchets"] = {"pkg/legacy.py": "seven"}
    path.write_text(json.dumps(config), encoding="utf-8")
    with pytest.raises(code_health.ConfigurationError, match="ratchets"):
        code_health.load_config(path)


def test_size_checker_enforces_hard_limit_and_no_net_growth(tmp_path: Path, code_health) -> None:
    root, config = _fixture(tmp_path)
    result = code_health.check_sizes(root, config)
    assert result["status"] == "PASS"
    policies = {item["path"]: item["policy"] for item in result["modules"]}
    assert policies["pkg/base.py"] == "new-module-hard-limit"
    assert policies["pkg/legacy.py"] == "no-net-growth"

    (root / "pkg" / "base.py").write_text("\n".join(["VALUE = 1"] * 6), encoding="utf-8")
    (root / "pkg" / "legacy.py").write_text("\n".join(["VALUE = 1"] * 8), encoding="utf-8")
    result = code_health.check_sizes(root, config)
    assert result["status"] == "FAIL"
    assert {
        (item["path"], item["current_loc"], item["allowed_loc"]) for item in result["failures"]
    } == {
        ("pkg/base.py", 6, 5),
        ("pkg/legacy.py", 8, 7),
    }
    assert all(
        "extract a cohesive responsibility" in item["message"] for item in result["failures"]
    )


def test_symbol_map_reports_loc_definitions_ranges_and_imports(tmp_path: Path, code_health) -> None:
    root, config = _fixture(tmp_path)
    result = code_health.build_symbol_map(root, config)
    feature = next(item for item in result["modules"] if item["module_path"] == "pkg/feature.py")
    assert feature["physical_loc"] == 4
    assert feature["direct_imports"] == [".base"]
    assert feature["definitions"] == [
        {"kind": "function", "name": "use", "start_line": 3, "end_line": 4}
    ]
    assert result["generated_from_source"] is True


def test_dependency_check_enforces_direction_and_cycles(tmp_path: Path, code_health) -> None:
    root, config = _fixture(tmp_path)
    assert code_health.check_dependencies(root, config)["status"] == "PASS"
    (root / "pkg" / "base.py").write_text(
        "from .feature import use\nVALUE = use()\n", encoding="utf-8", newline="\n"
    )
    result = code_health.check_dependencies(root, config)
    assert result["status"] == "FAIL"
    assert any(item.get("module") == "base" for item in result["failures"])
    assert any(item.get("cycle") == ["base", "feature", "base"] for item in result["failures"])


def test_repository_configuration_and_dependency_graph_are_green(
    repo_root: Path, code_health
) -> None:
    config = code_health.load_config(repo_root / "code-health.json")
    sizes = code_health.check_sizes(repo_root, config)
    complexity = code_health.check_complexity(repo_root, config)
    dependencies = code_health.check_dependencies(repo_root, config)
    assert sizes["status"] == "PASS", sizes["failures"]
    assert complexity["status"] == "PASS", complexity["failures"]
    assert dependencies["status"] == "PASS", dependencies["failures"]
    harness = next(
        item
        for item in sizes["modules"]
        if item["path"] == "evals/skill_activation_topology/harness.py"
    )
    assert harness == {
        "path": "evals/skill_activation_topology/harness.py",
        "physical_loc": 212,
        "allowed": 212,
        "policy": "no-net-growth",
    }


def test_symbol_map_cli_emits_machine_readable_source_metadata(repo_root: Path) -> None:
    completed = subprocess.run(
        [sys.executable, "tools/code_health.py", "map", "--root", str(repo_root)],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    facade = next(
        item
        for item in result["modules"]
        if item["module_path"] == "evals/skill_activation_topology/harness.py"
    )
    assert facade["physical_loc"] == 212
    assert {item["name"] for item in facade["definitions"]} >= {
        "build_parser",
        "main",
        "run_matrix",
    }
