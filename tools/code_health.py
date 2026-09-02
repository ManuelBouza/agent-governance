"""Deterministic Python size, complexity, dependency, and symbol-map checks."""

from __future__ import annotations

import argparse
import ast
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


class ConfigurationError(ValueError):
    """Raised when code-health configuration cannot be trusted."""


def _require(value: Any, expected: type, field: str) -> Any:
    if not isinstance(value, expected):
        raise ConfigurationError(f"{field} must be {expected.__name__}")
    return value


def _validate_string_lists(config: dict[str, Any]) -> None:
    fields = ("governed_roots", "exclude_directories", "complexity_paths", "symbol_map_paths")
    for field in fields:
        values = _require(config.get(field), list, field)
        if not all(isinstance(value, str) and value for value in values):
            raise ConfigurationError(f"{field} must contain non-empty strings")


def _validate_layers(config: dict[str, Any]) -> None:
    layers = _require(config.get("dependency_layers"), list, "dependency_layers")
    if not layers or not all(isinstance(layer, list) and layer for layer in layers):
        raise ConfigurationError("dependency_layers must contain non-empty lists")
    flattened = [name for layer in layers for name in layer]
    if not all(isinstance(name, str) and name for name in flattened):
        raise ConfigurationError("dependency layer names must be non-empty strings")
    if len(flattened) != len(set(flattened)):
        raise ConfigurationError("dependency layer modules must be unique")


def load_config(path: Path) -> dict[str, Any]:
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigurationError(f"cannot load configuration {path}: {exc}") from exc
    _require(config, dict, "configuration")
    if config.get("schema_version") != 1:
        raise ConfigurationError("schema_version must be 1")
    hard_limit = config.get("hard_limit")
    if not isinstance(hard_limit, int) or hard_limit <= 0:
        raise ConfigurationError("hard_limit must be a positive integer")
    _validate_string_lists(config)
    ratchets = _require(config.get("ratchets"), dict, "ratchets")
    if not all(
        isinstance(name, str) and name.endswith(".py") and isinstance(limit, int) and limit > 0
        for name, limit in ratchets.items()
    ):
        raise ConfigurationError("ratchets must map Python paths to positive integer limits")
    _validate_layers(config)
    package = config.get("dependency_package")
    if not isinstance(package, str) or not package:
        raise ConfigurationError("dependency_package must be a non-empty path")
    return config


def physical_loc(path: Path) -> int:
    return len(path.read_bytes().splitlines())


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def governed_modules(root: Path, config: dict[str, Any]) -> list[Path]:
    excluded = set(config["exclude_directories"])
    modules: set[Path] = set()
    for relative_root in config["governed_roots"]:
        directory = root / relative_root
        if not directory.is_dir():
            raise ConfigurationError(f"governed root does not exist: {relative_root}")
        modules.update(
            path
            for path in directory.rglob("*.py")
            if not set(path.relative_to(root).parts) & excluded
        )
    return sorted(modules, key=lambda path: _relative(path, root))


def check_sizes(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    ratchets = config["ratchets"]
    missing = sorted(path for path in ratchets if not (root / path).is_file())
    if missing:
        raise ConfigurationError(f"ratchet paths do not exist: {missing}")
    modules = []
    failures = []
    for path in governed_modules(root, config):
        relative = _relative(path, root)
        loc = physical_loc(path)
        ratcheted = relative in ratchets
        allowed = ratchets.get(relative, config["hard_limit"])
        policy = "no-net-growth" if ratcheted else "new-module-hard-limit"
        modules.append(
            {"path": relative, "physical_loc": loc, "allowed": allowed, "policy": policy}
        )
        if loc > allowed:
            failures.append(
                {
                    "path": relative,
                    "current_loc": loc,
                    "allowed_loc": allowed,
                    "message": (
                        f"{relative}: {loc} physical lines exceeds allowed {allowed}; "
                        "extract a cohesive responsibility or lower the module size"
                    ),
                }
            )
    return {"status": "PASS" if not failures else "FAIL", "modules": modules, "failures": failures}


def expand_paths(root: Path, patterns: list[str]) -> list[Path]:
    paths = {path for pattern in patterns for path in root.glob(pattern) if path.is_file()}
    missing = [
        pattern for pattern in patterns if not any(path.is_file() for path in root.glob(pattern))
    ]
    if missing:
        raise ConfigurationError(f"configured path patterns matched no files: {missing}")
    return sorted(paths, key=lambda path: _relative(path, root))


def check_complexity(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    paths = expand_paths(root, config["complexity_paths"])
    if not paths:
        return {"status": "PASS", "failures": [], "files": []}
    executable = shutil.which("ruff")
    if executable is None:
        raise ConfigurationError("ruff executable is required for complexity enforcement")
    command = [
        executable,
        "check",
        "--select",
        "C901,PLR0912,PLR0915",
        "--output-format",
        "json",
        *[str(path) for path in paths],
    ]
    completed = subprocess.run(command, cwd=root, check=False, capture_output=True, text=True)
    try:
        diagnostics = json.loads(completed.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise ConfigurationError(f"ruff returned malformed JSON: {completed.stdout}") from exc
    if completed.returncode not in {0, 1}:
        raise ConfigurationError(f"ruff complexity check failed: {completed.stderr.strip()}")
    failures = [
        {
            "path": Path(item["filename"]).resolve().relative_to(root.resolve()).as_posix(),
            "line": item["location"]["row"],
            "code": item["code"],
            "message": item["message"],
        }
        for item in diagnostics
    ]
    return {
        "status": "PASS" if not failures else "FAIL",
        "files": [_relative(path, root) for path in paths],
        "failures": failures,
    }


def _direct_imports(tree: ast.Module) -> list[str]:
    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            prefix = "." * node.level + (node.module or "")
            imports.append(prefix)
    return sorted(set(imports))


def symbol_metadata(path: Path, root: Path) -> dict[str, Any]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError, UnicodeError) as exc:
        raise ConfigurationError(f"cannot parse {_relative(path, root)}: {exc}") from exc
    definitions = [
        {
            "kind": "class" if isinstance(node, ast.ClassDef) else "function",
            "name": node.name,
            "start_line": min([node.lineno, *[item.lineno for item in node.decorator_list]]),
            "end_line": node.end_lineno,
        }
        for node in tree.body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    return {
        "module_path": _relative(path, root),
        "physical_loc": physical_loc(path),
        "definitions": definitions,
        "direct_imports": _direct_imports(tree),
    }


def build_symbol_map(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    modules = [
        symbol_metadata(path, root) for path in expand_paths(root, config["symbol_map_paths"])
    ]
    return {"schema_version": 1, "generated_from_source": True, "modules": modules}


def _package_imports(path: Path, known: set[str]) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports = set()
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom) or node.level != 1:
            continue
        target = node.module.split(".")[0] if node.module else None
        if target in known:
            imports.add(target)
    return imports


def _cycle(edges: dict[str, set[str]]) -> list[str] | None:
    visited: set[str] = set()
    active: list[str] = []

    def visit(node: str) -> list[str] | None:
        if node in active:
            index = active.index(node)
            return [*active[index:], node]
        if node in visited:
            return None
        active.append(node)
        for dependency in sorted(edges[node]):
            found = visit(dependency)
            if found:
                return found
        active.pop()
        visited.add(node)
        return None

    for node in sorted(edges):
        found = visit(node)
        if found:
            return found
    return None


def check_dependencies(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    package = root / config["dependency_package"]
    if not package.is_dir():
        raise ConfigurationError(
            f"dependency package does not exist: {config['dependency_package']}"
        )
    layers = config["dependency_layers"]
    positions = {name: index for index, layer in enumerate(layers) for name in layer}
    missing = sorted(name for name in positions if not (package / f"{name}.py").is_file())
    if missing:
        raise ConfigurationError(f"dependency modules do not exist: {missing}")
    edges = {name: _package_imports(package / f"{name}.py", set(positions)) for name in positions}
    failures = [
        {
            "module": module,
            "dependency": dependency,
            "message": f"{module} imports higher-layer {dependency}; reverse the dependency",
        }
        for module, dependencies in edges.items()
        for dependency in dependencies
        if positions[dependency] > positions[module]
    ]
    cycle = _cycle(edges)
    if cycle:
        failures.append(
            {"cycle": cycle, "message": f"circular imports detected: {' -> '.join(cycle)}"}
        )
    return {
        "status": "PASS" if not failures else "FAIL",
        "layers": layers,
        "edges": {name: sorted(values) for name, values in sorted(edges.items())},
        "failures": failures,
    }


def complete_check(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    sections = {
        "sizes": check_sizes(root, config),
        "complexity": check_complexity(root, config),
        "dependencies": check_dependencies(root, config),
    }
    return {
        "schema_version": 1,
        "status": "PASS"
        if all(value["status"] == "PASS" for value in sections.values())
        else "FAIL",
        **sections,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "map", "sizes", "dependencies"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--config", type=Path, default=Path("code-health.json"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    config_path = args.config if args.config.is_absolute() else root / args.config
    try:
        config = load_config(config_path)
        if args.command == "check":
            result = complete_check(root, config)
        elif args.command == "map":
            result = build_symbol_map(root, config)
        elif args.command == "sizes":
            result = check_sizes(root, config)
        else:
            result = check_dependencies(root, config)
    except ConfigurationError as exc:
        result = {"schema_version": 1, "status": "ERROR", "error": str(exc)}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("status") in {None, "PASS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
