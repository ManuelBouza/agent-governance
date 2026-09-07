"""Provider-free integrity guard for the T061 v13 holdout/oracle freeze."""

from __future__ import annotations

import collections
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "evals" / "skill_activation_topology"
CORPUS = EVAL / "corpus.json"
ORACLE = EVAL / "oracle.json"
HASHES = EVAL / "candidate-hashes-v13.json"

EXPECTED_CLASSES = {
    "positive-consumer": 6,
    "positive-source-maintainer": 6,
    "positive-external-skill-trust": 6,
    "negative": 10,
    "near-miss": 30,
    "ambiguous": 4,
    "cross-profile": 4,
    "multi-intent": 4,
}
EXPECTED_AXES = {
    "unrelated-source-maintenance": 6,
    "generic-skill-tooling": 6,
    "explicit-non-applicability": 6,
    "incidental-mention": 6,
    "homonym-outside-product": 6,
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_bytes(revision: str, relative: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{revision}:{relative}"], cwd=ROOT, stderr=subprocess.STDOUT
    )


def main() -> int:
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
    hashes = json.loads(HASHES.read_text(encoding="utf-8"))
    freeze = oracle["candidate_freeze_sha"]

    assert oracle["schema_version"] == "13.0.0"
    assert oracle["oracle_id"] == "MG1-T023-TOPOLOGY-ORACLE-v13"
    assert oracle["execution_epoch"] == "MG1-T023-EXECUTION-v13"
    assert oracle["candidate_ids"] == ["B2", "F2", "G3"]
    assert oracle["trial_method"]["reference_stage_candidates"] == ["B2"]
    assert oracle["trial_method"]["challenger_stage_candidates"] == ["F2", "G3"]
    assert oracle["trial_method"]["reference_stage_full_completion_base_valid_observations"] == 140
    assert oracle["trial_method"]["challenger_stage_full_completion_base_valid_observations"] == 280
    assert oracle["trial_method"]["overall_full_completion_ceiling_when_challengers_execute"] == 630

    assert corpus["schema_version"] == "7.0.0"
    assert corpus["corpus_id"] == "MG1-T023-CORPUS-v7"
    assert corpus["candidate_freeze_sha"] == freeze
    cases = corpus["cases"]
    assert len(cases) == 70
    assert collections.Counter(case["class"] for case in cases) == collections.Counter(EXPECTED_CLASSES)
    assert sum(case["class"] in {"negative", "near-miss"} for case in cases) == 40
    axes = collections.Counter(
        case.get("near_miss_axis") for case in cases if case["class"] == "near-miss"
    )
    assert axes == collections.Counter(EXPECTED_AXES)
    contrasts: set[str] = set()
    for case in cases:
        if case["class"].startswith("positive-"):
            contrasts.update(case.get("contrast_axes", []))
    assert contrasts == set(EXPECTED_AXES)

    current_prompts = [case["prompt"] for case in cases]
    assert len(current_prompts) == len(set(current_prompts))
    prior_corpus = json.loads(
        git_bytes(f"{freeze}^", "evals/skill_activation_topology/corpus.json")
    )
    prior_prompts = {case["prompt"] for case in prior_corpus["cases"]}
    assert not (set(current_prompts) & prior_prompts)

    subprocess.run(
        ["git", "merge-base", "--is-ancestor", freeze, "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    for relative, expected in hashes["files"].items():
        current = (ROOT / relative).read_bytes()
        frozen = git_bytes(freeze, relative)
        assert current == frozen
        assert sha256_bytes(current) == expected
    for current, historical in hashes["copy_equivalence"].items():
        assert (ROOT / current).read_bytes() == (ROOT / historical).read_bytes()

    thresholds = oracle["qualifying_thresholds"]
    assert thresholds == {
        "activation_precision_min": 0.95,
        "activation_recall_min": 0.95,
        "activation_f1_min": 0.95,
        "false_activation_rate_max": 0.05,
        "wrong_specialist_rate_max": 0.05,
        "overactivation_rate_max": 0.05,
        "semantic_outcome_accuracy_overall_min": 0.95,
    }
    mandatory = oracle["mandatory_non_regression"]
    assert mandatory["cross_profile_violation_count"] == 0
    assert mandatory["ambiguous_context_permission_broadening_count"] == 0
    assert mandatory["semantic_outcome_accuracy_cross_profile_and_ambiguous"] == 1.0

    print(json.dumps({
        "status": "PASS",
        "oracle_id": oracle["oracle_id"],
        "corpus_id": corpus["corpus_id"],
        "candidate_freeze_sha": freeze,
        "case_count": len(cases),
        "false_activation_denominator": 40,
        "exact_v12_prompt_reuse_count": 0,
        "candidate_hash_count": len(hashes["files"]),
        "provider_model_calls_issued": 0,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
