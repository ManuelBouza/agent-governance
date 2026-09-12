"""CLI entrypoint for the T023 v16 selective-routing harness."""
from __future__ import annotations
import argparse
from pathlib import Path
from ._harness.runner import run_full

def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run-full")
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--codex-command", default="codex")
    run.add_argument("--required-codex-version", required=True)
    run.add_argument("--model", required=True)
    run.add_argument("--effort", required=True)
    run.add_argument("--backend", required=True)
    run.add_argument("--sandbox", default="read-only")
    run.add_argument("--timeout-seconds", type=int, default=180)
    return p

def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "run-full":
        return run_full(args)
    raise AssertionError(args.command)

if __name__ == "__main__":
    raise SystemExit(main())
