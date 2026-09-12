"""T023 v17 provider-gated routing/e2e controller.

Stage 5 materializes this package but never invokes provider/model execution.
The ``run`` command is Stage-6-only and requires separate authorization.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Sequence
from .core import *
from .host import *
from .statistics import *
from .scoring import *
from .controller import *

def build_parser()->argparse.ArgumentParser:
    parser=argparse.ArgumentParser(description="T023 v17 frozen evaluation controller")
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("verify-freeze-i")
    run=sub.add_parser("run")
    run.add_argument("--output",type=Path,required=True)
    run.add_argument("--codex-command",default="codex")
    run.add_argument("--required-codex-version",required=True)
    run.add_argument("--model",required=True)
    run.add_argument("--effort",required=True)
    run.add_argument("--backend",required=True)
    run.add_argument("--sandbox",default="read-only")
    run.add_argument("--timeout-seconds",type=int,default=180)
    return parser

def main(argv:Sequence[str]|None=None)->int:
    args=build_parser().parse_args(argv)
    if args.command=="verify-freeze-i":
        print(json.dumps(validate_freeze_i(),indent=2,sort_keys=True)); return 0
    return run_full(args)

if __name__=="__main__": raise SystemExit(main())
