"""Provider-free T063 v3 Git/AST/fixture oracles and graders."""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from .config import (
    EXPECTED_TASK_MESSAGE_DIGESTS,
    FROZEN_HEAD,
    P1_PATHS,
    P2_FILES,
    P2_SYMBOLS,
    P3_EXPECTED_FIXTURE_SHA256,
    P3_SEED_BLOB,
    P3_SEED_PATH,
    HarnessError,
    PreparedInputs,
    build_task_messages,
)


def run_command(args: list[str], *, cwd: Path, timeout: float = 30.0, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=cwd, text=True, encoding="utf-8", capture_output=True, timeout=timeout, check=False)
    if check and result.returncode != 0:
        raise HarnessError(
            f"command failed ({result.returncode}): {args!r}\n"
            f"stdout={result.stdout[-2000:]!r}\nstderr={result.stderr[-2000:]!r}"
        )
    return result


def git(repo: Path, *args: str) -> str:
    return run_command(["git", *args], cwd=repo).stdout.strip()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_text(repo: Path, path: str) -> str:
    return run_command(["git", "show", f"{FROZEN_HEAD}:{path}"], cwd=repo).stdout


def compute_p1_oracle(repo: Path) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    for path in P1_PATHS:
        exists = run_command(["git", "cat-file", "-e", f"{FROZEN_HEAD}:{path}"], cwd=repo, check=False).returncode == 0
        if not exists:
            files.append({"path": path, "blob_sha": None, "byte_size": None, "exists_at_frozen_head": False})
            continue
        blob_sha = git(repo, "rev-parse", f"{FROZEN_HEAD}:{path}")
        files.append({
            "path": path,
            "blob_sha": blob_sha,
            "byte_size": int(git(repo, "cat-file", "-s", blob_sha)),
            "exists_at_frozen_head": True,
        })
    return {"frozen_head": FROZEN_HEAD, "files": files}


def module_for_path(path: str) -> str:
    relative = Path(path).with_suffix("")
    parts = list(relative.parts)
    if parts[:1] == ["src"]:
        parts = parts[1:]
    if parts[-1:] == ["__init__"]:
        parts = parts[:-1]
    return ".".join(parts)


def resolve_import_targets(source_module: str, node: ast.Import | ast.ImportFrom, in_scope_modules: set[str]) -> set[str]:
    if isinstance(node, ast.Import):
        candidates = [alias.name for alias in node.names]
    else:
        if node.level:
            package = source_module.split(".")[:-1]
            ascend = max(node.level - 1, 0)
            base_parts = package[: len(package) - ascend] if ascend else package
            module_parts = node.module.split(".") if node.module else []
            base = ".".join([*base_parts, *module_parts])
        else:
            base = node.module or ""
        candidates = [base]
        if base:
            candidates.extend(f"{base}.{alias.name}" for alias in node.names if alias.name != "*")
    return {candidate for candidate in candidates if candidate in in_scope_modules}


def acyclic(nodes: set[str], edges: set[tuple[str, str]]) -> bool:
    outgoing = {node: set() for node in nodes}
    indegree = {node: 0 for node in nodes}
    for source, target in edges:
        if target not in outgoing[source]:
            outgoing[source].add(target)
            indegree[target] += 1
    pending = sorted(node for node, degree in indegree.items() if degree == 0)
    visited = 0
    while pending:
        node = pending.pop(0)
        visited += 1
        for target in sorted(outgoing[node]):
            indegree[target] -= 1
            if indegree[target] == 0:
                pending.append(target)
                pending.sort()
    return visited == len(nodes)


def compute_p2_oracle(repo: Path) -> dict[str, Any]:
    module_by_path = {path: module_for_path(path) for path in P2_FILES}
    in_scope = set(module_by_path.values())
    edges: set[tuple[str, str]] = set()
    owners: dict[str, str] = {}
    for path in P2_FILES:
        source_module = module_by_path[path]
        tree = ast.parse(frozen_text(repo, path), filename=path)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for target in resolve_import_targets(source_module, node, in_scope):
                    if target != source_module:
                        edges.add((source_module, target))
        for node in tree.body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in P2_SYMBOLS:
                if node.name in owners:
                    raise HarnessError(f"ambiguous P2 symbol owner: {node.name}")
                owners[node.name] = source_module
    missing = [symbol for symbol in P2_SYMBOLS if symbol not in owners]
    if missing:
        raise HarnessError(f"missing P2 symbol owners: {missing}")
    return {
        "edges": [list(edge) for edge in sorted(edges)],
        "acyclic": acyclic(in_scope, edges),
        "symbol_owners": {symbol: owners[symbol] for symbol in P2_SYMBOLS},
    }


def ensure_runtime_root_safe(repo: Path, runtime_root: Path) -> None:
    repo = repo.resolve()
    runtime_root = runtime_root.resolve()
    system_temp = Path(tempfile.gettempdir()).resolve()
    if runtime_root == repo or repo in runtime_root.parents:
        raise HarnessError("P3 runtime root must be outside the repository/worktree")
    if runtime_root.parent != repo.parent:
        raise HarnessError("P3 runtime root must be a sibling of the repository/worktree")
    if runtime_root == system_temp or system_temp in runtime_root.parents:
        raise HarnessError("P3 runtime root must not be inside the system temp directory")
    if runtime_root.exists():
        raise HarnessError(f"P3 runtime root already exists: {runtime_root}")


def seed_p3_fixture(repo: Path, runtime_root: Path) -> tuple[Path, dict[str, Any]]:
    blob = git(repo, "rev-parse", f"{FROZEN_HEAD}:{P3_SEED_PATH}")
    if blob != P3_SEED_BLOB:
        raise HarnessError(f"P3 seed blob drift: expected {P3_SEED_BLOB}, got {blob}")
    source = frozen_text(repo, P3_SEED_PATH)
    pattern = re.compile(
        r'    if not isinstance\(profile\.name, str\) or profile\.name not in ACTIVE_PROFILES:\n'
        r'        raise ProfileError\(\n'
        r'            f"unsupported profile: \{profile\.name!r\}; active profiles: \{sorted\(ACTIVE_PROFILES\)\}"\n'
        r'        \)\n'
        r'    return profile\n'
    )
    replacement = (
        '    if not isinstance(profile.name, str) or profile.name not in ACTIVE_PROFILES:\n'
        '        return Profile(name="source-maintainer")\n'
        '    return profile\n'
    )
    mutated, count = pattern.subn(replacement, source)
    if count != 1:
        raise HarnessError(f"P3 mutation anchor matched {count} times; expected 1")
    runtime_root.mkdir(parents=True, exist_ok=False)
    fixture = runtime_root / "profile_fixture.py"
    fixture.write_text(mutated, encoding="utf-8", newline="\n")
    with fixture.open("rb") as handle:
        handle.read(1)
    digest = sha256_file(fixture)
    if digest != P3_EXPECTED_FIXTURE_SHA256:
        raise HarnessError(f"P3 fixture digest drift: expected {P3_EXPECTED_FIXTURE_SHA256}, got {digest}")
    spec = importlib.util.spec_from_file_location("t063_profile_fixture", fixture)
    if spec is None or spec.loader is None:
        raise HarnessError("cannot load P3 fixture")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
        returned = module.validate_profile(module.Profile(name="invalid"))
    finally:
        sys.modules.pop(spec.name, None)
    reproduction = {
        "input_profile_name": "invalid",
        "returned_profile_name": returned.name,
        "grants_source_maintenance": returned.grants_source_maintenance,
        "expected_original_behavior": "ProfileError",
    }
    if reproduction["returned_profile_name"] != "source-maintainer" or reproduction["grants_source_maintenance"] is not True:
        raise HarnessError("P3 reproduction did not produce expected fail-open authority escalation")
    return fixture, {
        "seed_path": P3_SEED_PATH,
        "seed_blob": P3_SEED_BLOB,
        "fixture_sha256": digest,
        "mutation_count": count,
        "root_reproduction": reproduction,
        "severity": "HIGH",
        "mechanism": "authority/profile escalation through unsupported-name fallback",
        "minimal_fix": "restore fail-closed ProfileError for unsupported names",
    }


def prepare_inputs(repo: Path, runtime_root: Path) -> PreparedInputs:
    ensure_runtime_root_safe(repo, runtime_root)
    if run_command(["git", "cat-file", "-e", f"{FROZEN_HEAD}^{{commit}}"], cwd=repo, check=False).returncode != 0:
        raise HarnessError(f"frozen commit unavailable: {FROZEN_HEAD}")
    p1 = compute_p1_oracle(repo)
    p2 = compute_p2_oracle(repo)
    fixture, p3 = seed_p3_fixture(repo, runtime_root)
    messages = build_task_messages()
    digests = {probe: sha256_text(message) for probe, message in messages.items()}
    if digests != EXPECTED_TASK_MESSAGE_DIGESTS:
        raise HarnessError(f"frozen task-message digest drift: expected {EXPECTED_TASK_MESSAGE_DIGESTS}, got {digests}")
    return PreparedInputs(p1, p2, p3, fixture, messages, digests)


def parse_child_json(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            lines = lines[1:-1]
            if lines and lines[0].strip().lower() == "json":
                lines = lines[1:]
            stripped = "\n".join(lines).strip()
    try:
        value = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise HarnessError(f"child response is not valid JSON: {text[:500]!r}") from exc
    if not isinstance(value, dict):
        raise HarnessError("child response JSON is not an object")
    return value


def score_p1(value: dict[str, Any], oracle: dict[str, Any]) -> tuple[bool, str]:
    files = value.get("files")
    if not isinstance(files, list):
        raise HarnessError("P1 result files is not a list")
    normalized = []
    for item in files:
        if not isinstance(item, dict):
            raise HarnessError("P1 files item is not an object")
        normalized.append({
            "path": item.get("path"),
            "blob_sha": item.get("blob_sha"),
            "byte_size": item.get("byte_size"),
            "exists_at_frozen_head": item.get("exists_at_frozen_head"),
        })
    passed = {"frozen_head": value.get("frozen_head"), "files": normalized} == oracle
    return passed, "exact Git inventory match" if passed else "P1 exact Git inventory mismatch"


def _normalize_edges(value: Any) -> list[list[str]]:
    if not isinstance(value, list):
        raise HarnessError("P2 edges is not a list")
    edges: list[list[str]] = []
    for edge in value:
        if not (isinstance(edge, list) and len(edge) == 2 and all(isinstance(part, str) for part in edge)):
            raise HarnessError("P2 edge is not [source, target]")
        edges.append([edge[0], edge[1]])
    return sorted(edges)


def score_p2(value: dict[str, Any], oracle: dict[str, Any]) -> tuple[bool, str]:
    owners = value.get("symbol_owners")
    if not isinstance(owners, dict):
        raise HarnessError("P2 symbol_owners is not an object")
    normalized = {
        "edges": _normalize_edges(value.get("edges")),
        "acyclic": value.get("acyclic"),
        "symbol_owners": {symbol: owners.get(symbol) for symbol in P2_SYMBOLS},
    }
    passed = normalized == oracle
    return passed, "exact static AST map match" if passed else "P2 static AST map mismatch"


def score_p3(value: dict[str, Any]) -> tuple[bool, str, int, int]:
    findings = value.get("findings")
    if not isinstance(findings, list) or not findings:
        return False, "P3 material defect not reported", 1, 0
    material = [item for item in findings if isinstance(item, dict)]
    if not material:
        return False, "P3 findings malformed", 1, 0
    matching = 0
    invented = 0
    for finding in material:
        severity = str(finding.get("severity", "")).upper()
        combined = " ".join(str(finding.get(key, "")) for key in ("mechanism", "evidence", "reproduction", "fix_direction")).lower()
        has_invalid = "invalid" in combined or "unsupported" in combined
        has_broader = "source-maintainer" in combined or "source maintainer" in combined
        has_fail_closed = "profileerror" in combined or "fail-closed" in combined or "fail closed" in combined
        has_authority = any(token in combined for token in ("authority", "permission", "grants_source_maintenance", "source maintenance"))
        if severity == "HIGH" and has_invalid and has_broader and has_fail_closed and has_authority:
            matching += 1
        else:
            invented += 1
    passed = matching >= 1 and invented == 0
    return passed, "seeded fail-open authority escalation detected" if passed else "P3 oracle mismatch", 0 if matching else 1, invented


def cleanup_runtime_root(runtime_root: Path, prepared: PreparedInputs | None) -> None:
    if prepared is not None and prepared.p3_fixture.exists():
        expected = prepared.p3_oracle["fixture_sha256"]
        if sha256_file(prepared.p3_fixture) != expected:
            raise HarnessError("P3 fixture changed during execution")
    if runtime_root.exists():
        shutil.rmtree(runtime_root, ignore_errors=False)
