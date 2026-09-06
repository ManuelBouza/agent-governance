"""Provider-free deterministic guard for the T061 v13 candidate freeze."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "evals" / "skill_activation_topology"
HASHES = EVAL / "candidate-hashes-v13.json"
TOPOLOGIES = EVAL / "topologies.json"
MANIFEST = EVAL / "presentations" / "manifest.json"

EXPECTED_CANDIDATES = ["B2", "F2", "G3"]
EXPECTED_EPOCH = "MG1-2026-09-06-v4"
EXPECTED_PRESENTATION = "MG1-T023-PRESENTATIONS-v4"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    spec = json.loads(HASHES.read_text(encoding="utf-8"))
    topologies = json.loads(TOPOLOGIES.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert spec["algorithm"] == "sha256"
    assert topologies["capability_source_epoch"] == EXPECTED_EPOCH
    assert manifest["capability_source_epoch"] == EXPECTED_EPOCH
    assert topologies["presentation_revision"] == EXPECTED_PRESENTATION
    assert manifest["presentation_revision"] == EXPECTED_PRESENTATION
    assert list(topologies["candidates"]) == EXPECTED_CANDIDATES
    assert list(manifest["candidates"]) == EXPECTED_CANDIDATES
    assert topologies["historical_unscheduled_candidates"] == ["B0", "B1"]

    for relative, expected in spec["files"].items():
        actual = sha256(ROOT / relative)
        assert actual == expected, f"hash mismatch: {relative}: {actual} != {expected}"

    for target, source in spec["copy_equivalence"].items():
        assert (ROOT / target).read_bytes() == (ROOT / source).read_bytes(), (
            f"v4 copy drift: {target} != {source}"
        )

    print(json.dumps({
        "status": "PASS",
        "identity": spec["identity"],
        "candidate_count": len(EXPECTED_CANDIDATES),
        "hashed_file_count": len(spec["files"]),
        "copy_equivalence_count": len(spec["copy_equivalence"]),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
