import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evals" / "r027_efficiency"


def load(name: str):
    return json.loads((EVAL / name).read_text(encoding="utf-8"))


def test_freeze_geometry_and_controls() -> None:
    freeze = load("freeze_a.json")
    schedule = load("schedule.json")
    oracle = load("oracles.json")
    assert freeze["pair_count"] == 9
    assert freeze["arm_ceiling"] == 18
    assert len(schedule["arms"]) == 18
    assert {a["phase"] for a in schedule["arms"]} == {1, 2, 3}
    assert all(a["children_allowed"] == 0 for a in schedule["arms"])
    assert all(a["reasoning"] == "medium" and a["speed"] == "standard" for a in schedule["arms"])
    assert len(oracle["variants"]) == 18


def test_live_measurement_is_fail_closed() -> None:
    rate = load("receipts/rate-card.json")
    runtime = load("receipts/runtime.json")
    readiness = load("receipts/stage5-readiness.json")
    assert rate["derivation_authorized"] is False
    assert runtime["launch_authorized"] is False
    assert readiness["live_launch_authorized"] is False


def test_integrity_script() -> None:
    proc = subprocess.run([sys.executable, str(EVAL / "integrity.py")], cwd=ROOT, capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PASS" in proc.stdout
