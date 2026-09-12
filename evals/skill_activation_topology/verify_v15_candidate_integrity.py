"""Provider-free deterministic guard for the T023 v15 Candidate Freeze E."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "evals" / "skill_activation_topology"
HASHES = EVAL / "candidate-hashes-v15.json"
TOPOLOGIES = EVAL / "topologies.json"
MANIFEST = EVAL / "presentations" / "manifest.json"

FREEZE_E = "5b025087bc7b6996f683a34fdd1ce441d3d6dd82"
SOURCE_STAGE5_HEAD = "aea43441a424fe18003176cb05b5594b8b561a68"
SOURCE_MANIFEST_PATH = "evals/skill_activation_topology/candidate-hashes-v14.json"
SOURCE_MANIFEST_BLOB = "f78b587b76ef0c06669b15fa4d0e85b393cab5b0"
EXPECTED_CANDIDATES = ["B2", "F2", "G3"]
EXPECTED_EPOCH = "MG1-2026-09-06-v4"
EXPECTED_TOPOLOGY = "MG1-T023-TOPOLOGIES-v4"
EXPECTED_PRESENTATION = "MG1-T023-PRESENTATIONS-v5"
EXPECTED_HASH_IDENTITY = "MG1-T023-CANDIDATE-HASHES-v3"
FORBIDDEN_AT_FREEZE_E = (
    "evals/skill_activation_topology/corpus.json",
    "evals/skill_activation_topology/oracle.json",
    "evals/skill_activation_topology/trial-envelope.json",
    "evals/skill_activation_topology/verify_v15_holdout_integrity.py",
)


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_show(revision: str, relative: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{revision}:{relative}"],
        cwd=ROOT,
        stderr=subprocess.STDOUT,
    )


def _git_blob_for_path(relative: str) -> str:
    return subprocess.check_output(
        ["git", "hash-object", relative],
        cwd=ROOT,
        text=True,
    ).strip()


def _path_exists_at(revision: str, relative: str) -> bool:
    completed = subprocess.run(
        ["git", "cat-file", "-e", f"{revision}:{relative}"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return completed.returncode == 0


def _assert_freeze_e_ancestor() -> None:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", FREEZE_E, "HEAD"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    assert completed.returncode == 0, "Candidate Freeze E is not an ancestor of HEAD"


def main() -> int:
    _assert_freeze_e_ancestor()
    spec = _load_json(HASHES)
    topologies = _load_json(TOPOLOGIES)
    manifest = _load_json(MANIFEST)
    source_spec = json.loads(_git_show(SOURCE_STAGE5_HEAD, SOURCE_MANIFEST_PATH))
    assert isinstance(source_spec, dict)

    assert spec["schema_version"] == "2.0.0"
    assert spec["identity"] == EXPECTED_HASH_IDENTITY
    assert spec["algorithm"] == "sha256"
    assert spec["topology_revision"] == EXPECTED_TOPOLOGY
    assert spec["presentation_revision"] == EXPECTED_PRESENTATION
    assert spec["capability_source_epoch"] == EXPECTED_EPOCH
    assert spec["source_stage5_head"] == SOURCE_STAGE5_HEAD
    assert spec["source_manifest_path"] == SOURCE_MANIFEST_PATH
    assert spec["source_manifest_blob"] == SOURCE_MANIFEST_BLOB
    assert spec["files"] == source_spec["files"]
    assert spec["copy_equivalence"] == source_spec["copy_equivalence"]
    assert set(spec["source_git_blobs"]) == set(spec["files"])
    assert "candidate_freeze" not in spec
    assert "candidate_freeze_sha" not in spec

    assert topologies["topology_revision"] == EXPECTED_TOPOLOGY
    assert topologies["capability_source_epoch"] == EXPECTED_EPOCH
    assert topologies["presentation_revision"] == EXPECTED_PRESENTATION
    assert topologies["presentation_manifest"] == (
        "evals/skill_activation_topology/presentations/manifest.json"
    )
    assert manifest["capability_source_epoch"] == EXPECTED_EPOCH
    assert manifest["presentation_revision"] == EXPECTED_PRESENTATION
    assert list(topologies["candidates"]) == EXPECTED_CANDIDATES
    assert list(manifest["candidates"]) == EXPECTED_CANDIDATES
    assert topologies["historical_unscheduled_candidates"] == ["B0", "B1"]

    frozen_identity_paths = (
        "evals/skill_activation_topology/candidate-hashes-v15.json",
        "evals/skill_activation_topology/topologies.json",
        "evals/skill_activation_topology/presentations/manifest.json",
    )
    for relative in frozen_identity_paths:
        assert (ROOT / relative).read_bytes() == _git_show(FREEZE_E, relative), (
            f"Candidate Freeze E identity drift: {relative}"
        )

    assert TOPOLOGIES.read_bytes() == _git_show(
        SOURCE_STAGE5_HEAD, "evals/skill_activation_topology/topologies.json"
    )
    assert MANIFEST.read_bytes() == _git_show(
        SOURCE_STAGE5_HEAD,
        "evals/skill_activation_topology/presentations/manifest.json",
    )

    for relative, expected_sha256 in spec["files"].items():
        path = ROOT / relative
        assert path.is_file(), f"missing candidate/reference payload: {relative}"
        actual_sha256 = _sha256(path)
        assert actual_sha256 == expected_sha256, (
            f"hash mismatch: {relative}: {actual_sha256} != {expected_sha256}"
        )
        actual_blob = _git_blob_for_path(relative)
        expected_blob = spec["source_git_blobs"][relative]
        assert actual_blob == expected_blob, (
            f"Git blob mismatch: {relative}: {actual_blob} != {expected_blob}"
        )
        assert path.read_bytes() == _git_show(SOURCE_STAGE5_HEAD, relative), (
            f"clean-source byte mismatch: {relative}"
        )
        assert path.read_bytes() == _git_show(FREEZE_E, relative), (
            f"Candidate Freeze E payload drift: {relative}"
        )

    for target, historical_v3_source in spec["copy_equivalence"].items():
        assert (ROOT / target).read_bytes() == _git_show(
            SOURCE_STAGE5_HEAD, historical_v3_source
        ), f"v5/v3 copy drift: {target} != {historical_v3_source}"

    for forbidden in FORBIDDEN_AT_FREEZE_E:
        assert not _path_exists_at(FREEZE_E, forbidden), (
            f"holdout identity existed at Candidate Freeze E: {forbidden}"
        )

    print(
        json.dumps(
            {
                "status": "PASS",
                "freeze_e": FREEZE_E,
                "identity": spec["identity"],
                "candidate_count": len(EXPECTED_CANDIDATES),
                "hashed_file_count": len(spec["files"]),
                "source_blob_count": len(spec["source_git_blobs"]),
                "copy_equivalence_count": len(spec["copy_equivalence"]),
                "provider_model_calls": 0,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
