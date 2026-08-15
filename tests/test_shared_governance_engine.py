"""Structural coverage for the shared deterministic engine extraction."""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path


def load_launcher(path: Path):
    spec = importlib.util.spec_from_file_location("shared_engine_launcher", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def function_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {
        node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def test_launcher_is_thin_and_delegates_to_single_shared_engine(repo_root: Path) -> None:
    launcher = repo_root / "governance-skill" / "scripts" / "governance.py"
    engine = repo_root / "src" / "agent_governance" / "engine.py"
    implementation_functions = {
        "_archive",
        "_ecosystem",
        "_event",
        "_parser",
        "_skill",
        "_state",
        "_validate",
    }

    assert function_names(launcher) == {"_bootstrap", "_package_paths", "_source_root", "main"}
    assert implementation_functions.isdisjoint(function_names(launcher))
    assert implementation_functions | {"_bootstrap"} <= function_names(engine)

    module = load_launcher(launcher)
    assert module._engine.__file__ == str(engine)
    assert callable(module.main)
