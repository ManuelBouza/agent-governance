"""Structural coverage for the shared deterministic engine extraction."""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

import pytest


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


def test_exchange_lock_backend_acquires_and_releases_on_current_platform(
    repo_root: Path, tmp_path: Path
) -> None:
    launcher = load_launcher(repo_root / "governance-skill" / "scripts" / "governance.py")
    exchange = tmp_path / "EXCHANGE.jsonl"
    exchange.write_text('{"q":1}\n', encoding="utf-8", newline="")

    with launcher._engine._locked_exchange(exchange, exclusive=True) as stream:
        assert stream.read() == '{"q":1}\n'

    with launcher._engine._locked_exchange(exchange, exclusive=False) as stream:
        assert stream.read() == '{"q":1}\n'


def test_exchange_lock_failure_is_controlled_and_never_enters_critical_section(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    launcher = load_launcher(repo_root / "governance-skill" / "scripts" / "governance.py")
    engine = launcher._engine
    exchange = tmp_path / "EXCHANGE.jsonl"
    exchange.write_text('{"q":1}\n', encoding="utf-8", newline="")

    def refuse_lock(_stream, *, exclusive: bool) -> None:
        assert exclusive
        raise OSError("lock refused")

    monkeypatch.setattr(engine, "_acquire_file_lock", refuse_lock)
    entered = False
    with (
        pytest.raises(engine.GovernanceError, match=r"cannot lock EXCHANGE.*lock refused"),
        engine._locked_exchange(exchange, exclusive=True),
    ):
        entered = True
    assert not entered


def test_exchange_lock_fails_closed_without_supported_backend(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    launcher = load_launcher(repo_root / "governance-skill" / "scripts" / "governance.py")
    engine = launcher._engine
    exchange = tmp_path / "EXCHANGE.jsonl"
    exchange.write_text('{"q":1}\n', encoding="utf-8", newline="")
    monkeypatch.setattr(engine, "_fcntl", None)
    monkeypatch.setattr(engine, "_windows_lock_api", None)

    with (
        pytest.raises(engine.GovernanceError, match="no supported file-locking backend"),
        engine._locked_exchange(exchange, exclusive=True),
    ):
        pytest.fail("critical section must not run without a lock")
