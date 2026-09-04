"""Mechanical identity and holdout-rotation checks for the T023 v12 epoch."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

CORPUS_PATH = "evals/skill_activation_topology/corpus.json"
ORACLE_PATH = "evals/skill_activation_topology/oracle.json"


def _git_bytes(repo_root: Path, revision: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{revision}:{relative}"], cwd=repo_root)


def _corpus_change(repo_root: Path) -> str:
    return subprocess.check_output(
        ["git", "log", "-1", "--format=%H", "--", CORPUS_PATH],
        cwd=repo_root,
        text=True,
    ).strip()


def test_v12_identity_and_zero_prior_observation_policy(repo_root: Path) -> None:
    oracle = json.loads((repo_root / ORACLE_PATH).read_text(encoding="utf-8"))
    corpus = json.loads((repo_root / CORPUS_PATH).read_text(encoding="utf-8"))
    prior = oracle["prior_experiment_policy"]

    assert oracle["schema_version"] == "12.0.0"
    assert oracle["oracle_id"] == "MG1-T023-TOPOLOGY-ORACLE-v12"
    assert oracle["execution_epoch"] == "MG1-T023-EXECUTION-v12"
    assert corpus["schema_version"] == "6.0.0"
    assert corpus["corpus_id"] == "MG1-T023-CORPUS-v6"
    assert prior["mg1_v10_scored_observations"] == 0
    assert prior["mg1_v11_scored_observations"] == 0
    assert prior["prior_v2_v3_v4_v6_v7_v8_v9_v10_v11_observations_may_enter_v12_score"] is False


def test_v6_differs_from_v5_only_by_wx00_to_wx00r_rotation(repo_root: Path) -> None:
    change = _corpus_change(repo_root)
    current = json.loads(_git_bytes(repo_root, change, CORPUS_PATH))
    previous = json.loads(_git_bytes(repo_root, f"{change}^", CORPUS_PATH))
    current_cases = {case["id"]: case for case in current["cases"]}
    previous_cases = {case["id"]: case for case in previous["cases"]}

    assert len(current_cases) == len(previous_cases) == 40
    assert set(current_cases) - set(previous_cases) == {"WX00R"}
    assert set(previous_cases) - set(current_cases) == {"WX00"}
    for case_id in set(current_cases) & set(previous_cases):
        assert current_cases[case_id] == previous_cases[case_id]
    rotated = {
        key: value for key, value in current_cases["WX00R"].items() if key not in {"id", "prompt"}
    }
    exposed = {
        key: value for key, value in previous_cases["WX00"].items() if key not in {"id", "prompt"}
    }
    assert rotated == exposed
    assert current_cases["WX00R"]["prompt"] != previous_cases["WX00"]["prompt"]


def test_v11_exposed_prompt_is_absent_from_v12(repo_root: Path) -> None:
    corpus = json.loads((repo_root / CORPUS_PATH).read_text(encoding="utf-8"))
    attempt_path = repo_root / (
        "evals/skill_activation_topology/evidence/"
        "mg1-v11-codex-windows-gpt-5.6-sol-medium/attempts/WX00--B0--r1--a1.json"
    )
    attempt = json.loads(attempt_path.read_text(encoding="utf-8"))
    assert attempt["raw"]["prompt"] not in {case["prompt"] for case in corpus["cases"]}


def test_v12_preserves_frozen_presentations_topologies_and_envelope(repo_root: Path) -> None:
    change = _corpus_change(repo_root)
    manifest_path = "evals/skill_activation_topology/presentations/manifest.json"
    manifest = json.loads(_git_bytes(repo_root, change, manifest_path))
    preserved = {
        "evals/skill_activation_topology/topologies.json",
        "evals/skill_activation_topology/trial-envelope.json",
        manifest_path,
        *manifest["shared_references"].values(),
    }
    for candidate in manifest["candidates"].values():
        preserved.update(item["skill_source"] for item in candidate["entrypoints"].values())
    for relative in preserved:
        assert _git_bytes(repo_root, change, relative) == _git_bytes(
            repo_root, f"{change}^", relative
        )
