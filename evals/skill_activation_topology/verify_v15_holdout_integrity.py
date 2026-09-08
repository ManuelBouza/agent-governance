"""Provider-free deterministic guard for the T023 v15 Holdout/Oracle Freeze F."""

from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "evals" / "skill_activation_topology"
FREEZE_E = "5b025087bc7b6996f683a34fdd1ce441d3d6dd82"
CORPUS = EVAL / "corpus.json"
ORACLE = EVAL / "oracle.json"
TRIAL = EVAL / "trial-envelope.json"
CANDIDATE_HASHES = EVAL / "candidate-hashes-v15.json"
FROZEN_PATHS = {
    "evals/skill_activation_topology/corpus.json",
    "evals/skill_activation_topology/oracle.json",
    "evals/skill_activation_topology/trial-envelope.json",
    "evals/skill_activation_topology/verify_v15_holdout_integrity.py",
}
HISTORICAL = (
    ("v12", "3e5bec392d0b8e5804c4efaad74b795b08dc9779"),
    ("v13", "d0ebe46a68c02c66dcfbb21c3dfaee43fb15c27f"),
    ("v14", "aea43441a424fe18003176cb05b5594b8b561a68"),
)
EXPECTED_CLASS_COUNTS = {
    "positive-consumer": 6,
    "positive-source-maintainer": 6,
    "positive-external-skill-trust": 6,
    "negative": 10,
    "near-miss": 30,
    "ambiguous": 4,
    "cross-profile": 4,
    "multi-intent": 4,
}
EXPECTED_NEAR_MISS = {
    "unrelated-source-maintenance": 6,
    "generic-skill-tooling": 6,
    "explicit-non-applicability": 6,
    "incidental-mention": 6,
    "homonym-outside-product": 6,
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def _git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, stderr=subprocess.STDOUT, text=True
    )


def _historical_prompts(revision: str) -> set[str]:
    raw = _git("show", f"{revision}:evals/skill_activation_topology/corpus.json")
    data = json.loads(raw)
    assert isinstance(data, dict) and isinstance(data.get("cases"), list)
    prompts = [case["prompt"] for case in data["cases"]]
    assert all(isinstance(prompt, str) for prompt in prompts)
    return set(prompts)


def _freeze_f() -> str:
    latest = _git("log", "-1", "--format=%H", "--", *sorted(FROZEN_PATHS)).strip()
    assert latest, "cannot resolve Freeze F from frozen paths"
    assert _git("merge-base", "--is-ancestor", FREEZE_E, latest) == ""
    changed = set(filter(None, _git("diff", "--name-only", FREEZE_E, latest).splitlines()))
    assert changed == FROZEN_PATHS, f"Freeze E -> F path boundary drift: {sorted(changed)}"
    post_freeze = set(filter(None, _git("diff", "--name-only", latest, "HEAD").splitlines()))
    assert not (post_freeze & FROZEN_PATHS), f"frozen asset drift after Freeze F: {sorted(post_freeze & FROZEN_PATHS)}"
    return latest


def main() -> int:
    freeze_f = _freeze_f()
    corpus = _load(CORPUS)
    oracle = _load(ORACLE)
    trial = _load(TRIAL)
    hashes = _load(CANDIDATE_HASHES)

    assert corpus["schema_version"] == "9.0.0"
    assert corpus["corpus_id"] == "MG1-T023-CORPUS-v9"
    assert corpus["candidate_freeze_sha"] == FREEZE_E
    cases = corpus["cases"]
    assert isinstance(cases, list) and len(cases) == 70
    ids = [case["id"] for case in cases]
    prompts = [case["prompt"] for case in cases]
    assert len(ids) == len(set(ids)) == 70
    assert len(prompts) == len(set(prompts)) == 70
    assert Counter(case["class"] for case in cases) == EXPECTED_CLASS_COUNTS
    assert Counter(case["near_miss_axis"] for case in cases if case["class"] == "near-miss") == EXPECTED_NEAR_MISS
    far_denominator = sum(case["class"] in {"negative", "near-miss"} for case in cases)
    assert far_denominator == 40

    overlaps: dict[str, int] = {}
    v15_prompts = set(prompts)
    for name, revision in HISTORICAL:
        overlap = v15_prompts & _historical_prompts(revision)
        overlaps[name] = len(overlap)
        assert not overlap, f"historical prompt reuse against {name}: {sorted(overlap)}"

    assert oracle["schema_version"] == "15.0.0"
    assert oracle["oracle_id"] == "MG1-T023-TOPOLOGY-ORACLE-v15"
    assert oracle["execution_epoch"] == "MG1-T023-EXECUTION-v15"
    assert oracle["strategy"] == "RIQ-NBC"
    assert oracle["corpus_id"] == corpus["corpus_id"]
    assert oracle["trial_envelope_id"] == trial["envelope_id"]
    assert oracle["candidate_freeze_sha"] == FREEZE_E
    assert oracle["candidate_ids"] == ["B2", "F2", "G3"]
    assert hashes["identity"] == "MG1-T023-CANDIDATE-HASHES-v3"

    schedule = oracle["scheduling"]
    assert schedule["base_repetition_order"] == ["r1", "r2"]
    assert schedule["candidate_round_robin_order"] == ["B2", "F2", "G3"]
    assert schedule["reference_scientific_qualification_gates_challengers"] is False
    assert schedule["b2_scientific_nonqualification_is_nonblocking"] is True
    assert schedule["r4_allowed"] is False

    method = oracle["trial_method"]
    assert method["per_candidate_base_valid_observations"] == 140
    assert method["per_candidate_max_valid_observations"] == 210
    assert method["global_base_valid_observations"] == 420
    assert method["global_max_valid_observations"] == 630
    assert method["max_model_attempts_per_scheduled_observation"] == 2
    assert method["maximum_acceptance_model_attempts"] == 1260
    assert method["synthetic_canary_max_model_attempts"] == 4
    assert method["absolute_stage6_provider_model_attempt_ceiling"] == 1264
    assert method["timeout_seconds_per_model_attempt"] == 180

    assert oracle["qualifying_thresholds"] == {
        "activation_precision_min": 0.95,
        "activation_recall_min": 0.95,
        "activation_f1_min": 0.95,
        "false_activation_rate_max": 0.05,
        "wrong_specialist_rate_max": 0.05,
        "overactivation_rate_max": 0.05,
        "semantic_outcome_accuracy_overall_min": 0.95,
    }
    selection = oracle["selection"]
    assert selection["regime_a_b2_qualifies"]["activation_f1_delta_min_vs_b2"] == 0.03
    assert selection["regime_a_b2_qualifies"]["median_observed_context_ratio_max_vs_b2"] == 0.85
    assert selection["regime_b_b2_scientifically_nonqualifying"]["b2_eligible"] is False
    assert selection["regime_b_b2_scientifically_nonqualifying"]["relative_f1_delta_required"] is False
    assert selection["regime_b_b2_scientifically_nonqualifying"]["admissibility_dominance_required"] is True
    assert oracle["stage6_gate"]["provider_model_calls_during_stage5"] == 0
    assert oracle["stage6_gate"]["executor_launch_requires_separate_human_authorization"] is True
    assert trial["schema_version"] == "3.0.0"
    assert trial["envelope_id"] == "MG1-T023-TRIAL-ENVELOPE-v3"

    print(json.dumps({
        "status": "PASS",
        "freeze_e": FREEZE_E,
        "freeze_f": freeze_f,
        "case_count": len(cases),
        "far_denominator": far_denominator,
        "historical_prompt_overlap": overlaps,
        "provider_model_calls": 0,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
