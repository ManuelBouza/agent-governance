from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
QUALIFIER = REPO / "tools" / "r029_materialization_qualify.py"


def run_qualifier() -> dict:
    completed = subprocess.run(
        [sys.executable, str(QUALIFIER), "--root", str(REPO)],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    return json.loads(completed.stdout)


def test_r029_materialization_qualifier_passes() -> None:
    result = run_qualifier()
    assert result["status"] == "PASS"
    assert result["measurements"]["root_bytes"] < result["measurements"]["baseline_root_bytes"]
    assert result["measurements"]["reference_hop_depth_max"] >= 1


def test_r029_residuals_remain_explicit() -> None:
    result = run_qualifier()
    residuals = result["residuals"]
    assert residuals["chatgpt_codex_empirical_parity"] == "NOT_ESTABLISHED"
    assert residuals["chatgpt_empirical_trials"] == "0/36"
    assert "informational/unscored" in residuals["maintainer_historical_observation"]


def test_r029_no_workspace_isolation_top_level_skill() -> None:
    result = run_qualifier()
    named_check = next(
        check for check in result["checks"] if check["name"] == "workspace-isolation-not-top-level"
    )
    assert named_check["ok"] is True
