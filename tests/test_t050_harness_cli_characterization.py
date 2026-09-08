"""Characterization for the stable T050 harness CLI facade under T023 v15."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def harness(repo_root: Path):
    path = repo_root / "evals" / "skill_activation_topology" / "harness.py"
    spec = importlib.util.spec_from_file_location("t050_v15_harness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _actions(parser: argparse.ArgumentParser) -> dict[str, argparse.Action]:
    return {action.dest: action for action in parser._actions}


def test_cli_subcommands_and_argument_contract(harness) -> None:
    parser = harness.build_parser()
    subparsers = next(
        action for action in parser._actions if isinstance(action, argparse._SubParsersAction)
    )
    assert list(subparsers.choices) == ["validate", "materialize", "run", "score", "verify"]

    validate = parser.parse_args(["validate"])
    assert validate.func is harness.command_validate

    materialize = parser.parse_args(
        ["materialize", "--candidate", "G3", "--destination", "destination"]
    )
    assert materialize.func is harness.command_materialize
    assert materialize.candidate == "G3"
    assert materialize.destination == Path("destination")

    run_parser = subparsers.choices["run"]
    run_actions = _actions(run_parser)
    assert set(run_actions) == {
        "help",
        "output",
        "codex_command",
        "model",
        "effort",
        "workers",
        "timeout_seconds",
        "case",
        "candidate",
        "repetition",
        "resume",
        "full_acceptance",
    }
    assert run_actions["output"].required is True
    assert run_actions["candidate"].choices == ("B2", "F2", "G3")
    assert run_actions["repetition"].choices == (1, 2, 3)
    run = parser.parse_args(["run", "--output", "evidence"])
    assert run.func is harness.run_matrix
    assert vars(run) == {
        "command": "run",
        "output": Path("evidence"),
        "codex_command": "codex",
        "model": "gpt-5.6-sol",
        "effort": "medium",
        "workers": 1,
        "timeout_seconds": 180,
        "case": None,
        "candidate": None,
        "repetition": None,
        "resume": False,
        "full_acceptance": False,
        "func": harness.run_matrix,
    }

    score = parser.parse_args(["score", "--output", "evidence"])
    assert score.func is harness.score_matrix
    assert score.output == Path("evidence")

    verify = parser.parse_args(["verify", "--output", "evidence"])
    assert verify.func is harness.verify_deterministic
    assert verify.output == Path("evidence")
    assert verify.timeout_seconds == 900


def test_validate_cli_success_output_and_exit(harness, capsys) -> None:
    assert harness.main(["validate"]) == 0
    assert json.loads(capsys.readouterr().out) == {
        "status": "PASS",
        "oracle_id": "MG1-T023-TOPOLOGY-ORACLE-v15",
        "strategy": "RIQ-NBC",
        "cases": 70,
        "candidates": ["B2", "F2", "G3"],
        "base_scheduled_trials": 420,
        "maximum_trial_identities": 630,
    }


def test_cli_maps_harness_error_to_json_and_exit_one(harness, monkeypatch, capsys) -> None:
    def fail():
        raise harness.HarnessError("characterized failure")

    monkeypatch.setattr(harness, "load_frozen_inputs", fail)
    assert harness.main(["validate"]) == 1
    assert json.loads(capsys.readouterr().out) == {
        "status": "ERROR",
        "error": "characterized failure",
    }


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["materialize", "--candidate", "unknown", "--destination", "target"],
        ["run", "--output", "evidence", "--workers", "0"],
    ],
)
def test_cli_usage_errors_exit_two(harness, argv) -> None:
    with pytest.raises(SystemExit) as exc_info:
        harness.main(argv)
    assert exc_info.value.code == 2
