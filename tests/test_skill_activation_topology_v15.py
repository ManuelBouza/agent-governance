"""Mechanical identity and holdout-shape checks for the T023 v15 epoch."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

CORPUS_PATH = "evals/skill_activation_topology/corpus.json"
ORACLE_PATH = "evals/skill_activation_topology/oracle.json"
HASHES_PATH = "evals/skill_activation_topology/candidate-hashes-v15.json"


def test_v15_identity_and_zero_prior_observation_policy(repo_root: Path) -> None:
    oracle = json.loads((repo_root / ORACLE_PATH).read_text(encoding="utf-8"))
    corpus = json.loads((repo_root / CORPUS_PATH).read_text(encoding="utf-8"))
    prior = oracle["prior_experiment_policy"]

    assert oracle["schema_version"] == "15.0.0"
    assert oracle["oracle_id"] == "MG1-T023-TOPOLOGY-ORACLE-v15"
    assert oracle["execution_epoch"] == "MG1-T023-EXECUTION-v15"
    assert oracle["strategy"] == "RIQ-NBC"
    assert oracle["candidate_ids"] == ["B2", "F2", "G3"]
    assert corpus["schema_version"] == "9.0.0"
    assert corpus["corpus_id"] == "MG1-T023-CORPUS-v9"
    assert prior["prior_observations_may_enter_v15_score"] is False
    assert prior["exact_prior_prompts_may_not_be_reused_as_v15_acceptance_stimuli"] is True


def test_v15_corpus_geometry_and_far_denominator(repo_root: Path) -> None:
    corpus = json.loads((repo_root / CORPUS_PATH).read_text(encoding="utf-8"))
    cases = corpus["cases"]
    assert len(cases) == 70
    assert len({case["id"] for case in cases}) == 70
    assert len({case["prompt"] for case in cases}) == 70
    assert Counter(case["class"] for case in cases) == {
        "positive-consumer": 6,
        "positive-source-maintainer": 6,
        "positive-external-skill-trust": 6,
        "negative": 10,
        "near-miss": 30,
        "ambiguous": 4,
        "cross-profile": 4,
        "multi-intent": 4,
    }
    assert sum(case["class"] in {"negative", "near-miss"} for case in cases) == 40
    assert Counter(case["near_miss_axis"] for case in cases if case["class"] == "near-miss") == {
        "unrelated-source-maintenance": 6,
        "generic-skill-tooling": 6,
        "explicit-non-applicability": 6,
        "incidental-mention": 6,
        "homonym-outside-product": 6,
    }


def test_v15_historical_prompt_exclusion_refs_are_frozen(repo_root: Path) -> None:
    corpus = json.loads((repo_root / CORPUS_PATH).read_text(encoding="utf-8"))
    assert corpus["historical_prompt_exclusion"] == [
        {
            "revision": "MG1-v14",
            "commit": "aea43441a424fe18003176cb05b5594b8b561a68",
            "path": CORPUS_PATH,
        },
        {
            "revision": "MG1-v13",
            "commit": "d0ebe46a68c02c66dcfbb21c3dfaee43fb15c27f",
            "path": CORPUS_PATH,
        },
        {
            "revision": "MG1-v12",
            "commit": "3e5bec392d0b8e5804c4efaad74b795b08dc9779",
            "path": CORPUS_PATH,
        },
    ]


def test_v15_candidate_hash_manifest_matches_current_payloads(repo_root: Path) -> None:
    manifest = json.loads((repo_root / HASHES_PATH).read_text(encoding="utf-8"))
    assert manifest["identity"] == "MG1-T023-CANDIDATE-HASHES-v3"
    assert manifest["presentation_revision"] == "MG1-T023-PRESENTATIONS-v5"
    assert len(manifest["files"]) == 9
    for relative, expected in manifest["files"].items():
        actual = hashlib.sha256((repo_root / relative).read_bytes()).hexdigest()
        assert actual == expected


def test_v15_oracle_freezes_nonblocking_scheduler_and_budgets(repo_root: Path) -> None:
    oracle = json.loads((repo_root / ORACLE_PATH).read_text(encoding="utf-8"))
    schedule = oracle["scheduling"]
    method = oracle["trial_method"]
    assert schedule["base_repetition_order"] == ["r1", "r2"]
    assert schedule["candidate_round_robin_order"] == ["B2", "F2", "G3"]
    assert schedule["reference_scientific_qualification_gates_challengers"] is False
    assert schedule["b2_scientific_nonqualification_is_nonblocking"] is True
    assert schedule["r4_allowed"] is False
    assert method["per_candidate_base_valid_observations"] == 140
    assert method["per_candidate_max_valid_observations"] == 210
    assert method["global_base_valid_observations"] == 420
    assert method["global_max_valid_observations"] == 630
    assert method["maximum_acceptance_model_attempts"] == 1260
    assert method["absolute_stage6_provider_model_attempt_ceiling"] == 1264
