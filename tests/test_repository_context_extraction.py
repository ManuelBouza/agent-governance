"""Characterization for the repository-context Phase-1 module boundary."""

from __future__ import annotations

import ast
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path


def test_dynamic_file_loading_works_from_unrelated_cwd(repo_root: Path, tmp_path: Path) -> None:
    """The stable facade resolves its source-local package without cwd assumptions."""
    tool_path = repo_root / "tools" / "repository_context.py"
    loader = """
import importlib.util
import json
import pathlib
import sys

spec = importlib.util.spec_from_file_location("isolated_repository_context", sys.argv[1])
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
report = module.build_report(pathlib.Path(sys.argv[2]))
print(json.dumps({"schema": report["report_schema_version"]}, sort_keys=True))
"""
    result = subprocess.run(
        [sys.executable, "-c", loader, str(tool_path), str(repo_root)],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert json.loads(result.stdout) == {"schema": "1.0.0"}


def test_dynamic_loading_is_isolated_between_source_roots(repo_root: Path, tmp_path: Path) -> None:
    """Each facade binds to its own source package without changing sys.path."""
    loaded = []
    original_sys_path = list(sys.path)
    for label, schema_version in (("first", "root-a"), ("second", "root-b")):
        tools = tmp_path / label / "tools"
        shutil.copytree(repo_root / "tools" / "_repository_context", tools / "_repository_context")
        shutil.copy2(repo_root / "tools" / "repository_context.py", tools / "repository_context.py")
        measurement = tools / "_repository_context" / "measurement.py"
        measurement.write_text(
            measurement.read_text(encoding="utf-8").replace(
                'SCHEMA_VERSION = "1.0.0"', f'SCHEMA_VERSION = "{schema_version}"'
            ),
            encoding="utf-8",
        )

        spec = importlib.util.spec_from_file_location(
            f"repository_context_{label}", tools / "repository_context.py"
        )
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        loaded.append(module)

    assert [module.SCHEMA_VERSION for module in loaded] == ["root-a", "root-b"]
    assert loaded[0]._measurement is not loaded[1]._measurement
    assert sys.path == original_sys_path


def test_repository_context_package_dependency_graph_is_acyclic(repo_root: Path) -> None:
    """The complete extracted package has the characterized one-way dependency graph."""
    tools = repo_root / "tools"
    modules = {
        "repository_context": tools / "repository_context.py",
        "_repository_context": tools / "_repository_context" / "__init__.py",
        **{
            f"_repository_context.{path.stem}": path
            for path in (tools / "_repository_context").glob("*.py")
            if path.name != "__init__.py"
        },
    }
    edges: set[tuple[str, str]] = set()
    for source, path in modules.items():
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module is not None:
                target = f"_repository_context.{node.module}" if node.level else node.module
                if target in modules:
                    edges.add((source, target))
            elif source == "repository_context" and isinstance(node, ast.Assign):
                names = {
                    target.id
                    for assignment_target in node.targets
                    for target in ast.walk(assignment_target)
                    if isinstance(target, ast.Name)
                }
                loaded = {
                    f"_repository_context.{name.removeprefix('_')}"
                    for name in names
                    if name.startswith("_")
                    and f"_repository_context.{name.removeprefix('_')}" in modules
                }
                edges.update((source, target) for target in loaded)

    assert edges == {
        ("repository_context", "_repository_context.common"),
        ("repository_context", "_repository_context.measurement"),
        ("repository_context", "_repository_context.projection"),
        ("repository_context", "_repository_context.registry"),
        ("repository_context", "_repository_context.snapshot"),
        ("repository_context", "_repository_context.tracked_files"),
        ("_repository_context.measurement", "_repository_context.common"),
        ("_repository_context.measurement", "_repository_context.tracked_files"),
        ("_repository_context.projection", "_repository_context.common"),
        ("_repository_context.projection", "_repository_context.measurement"),
        ("_repository_context.projection", "_repository_context.registry"),
        ("_repository_context.projection", "_repository_context.tracked_files"),
        ("_repository_context.registry", "_repository_context.common"),
        ("_repository_context.registry", "_repository_context.tracked_files"),
        ("_repository_context.snapshot", "_repository_context.common"),
        ("_repository_context.snapshot", "_repository_context.projection"),
        ("_repository_context.snapshot", "_repository_context.registry"),
        ("_repository_context.tracked_files", "_repository_context.common"),
    }
    assert all(target != "repository_context" for _, target in edges)

    remaining = set(modules)
    while remaining:
        leaves = {
            module
            for module in remaining
            if not any(source == module and target in remaining for source, target in edges)
        }
        assert leaves, f"import cycle among: {sorted(remaining)}"
        remaining.difference_update(leaves)
