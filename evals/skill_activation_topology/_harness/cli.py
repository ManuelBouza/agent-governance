"""Extracted MG1 topology harness implementation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .frozen_inputs import load_frozen_inputs
from .materialization import materialize_candidate
from .models import HarnessError
from .provenance import score_matrix, verify_deterministic
from .runner import run_matrix
from .scheduling import scheduled_trials


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "workers", 1) < 1:
        parser.error("--workers must be positive")
    try:
        return args.func(args)
    except HarnessError as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}))
        return 1


def command_validate(_: argparse.Namespace) -> int:
    inputs = load_frozen_inputs()
    print(
        json.dumps(
            {
                "status": "PASS",
                "oracle_id": inputs.oracle["oracle_id"],
                "cases": len(inputs.corpus["cases"]),
                "candidates": inputs.oracle["candidate_ids"],
                "scheduled_trials": len(scheduled_trials(inputs)),
            },
            sort_keys=True,
        )
    )
    return 0


def command_materialize(args: argparse.Namespace) -> int:
    inputs = load_frozen_inputs()
    args.destination.mkdir(parents=True, exist_ok=False)
    provenance = materialize_candidate(inputs, args.candidate, args.destination)
    print(json.dumps(provenance, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate")
    validate.set_defaults(func=command_validate)

    materialize = subparsers.add_parser("materialize")
    materialize.add_argument("--candidate", required=True, choices=("B0", "B1", "F2", "G3"))
    materialize.add_argument("--destination", required=True, type=Path)
    materialize.set_defaults(func=command_materialize)

    run = subparsers.add_parser("run")
    run.add_argument("--output", required=True, type=Path)
    run.add_argument("--codex-command", default="codex")
    run.add_argument("--model", default="gpt-5.6-sol")
    run.add_argument("--effort", default="medium")
    run.add_argument("--workers", type=int, default=4)
    run.add_argument("--timeout-seconds", type=int, default=180)
    run.add_argument("--case", action="append")
    run.add_argument("--candidate", action="append", choices=("B0", "B1", "F2", "G3"))
    run.add_argument("--repetition", action="append", type=int, choices=(1, 2, 3))
    run.add_argument("--resume", action="store_true")
    run.add_argument("--full-acceptance", action="store_true")
    run.set_defaults(func=run_matrix)

    score = subparsers.add_parser("score")
    score.add_argument("--output", required=True, type=Path)
    score.set_defaults(func=score_matrix)

    verify = subparsers.add_parser("verify")
    verify.add_argument("--output", required=True, type=Path)
    verify.add_argument("--timeout-seconds", type=int, default=900)
    verify.set_defaults(func=verify_deterministic)
    return parser
