"""Provider-free deterministic guard for the T061 v14 holdout freeze."""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "evals" / "skill_activation_topology"
CORPUS = EVAL / "corpus.json"
ORACLE = EVAL / "oracle.json"
HASHES = EVAL / "candidate-hashes-v14.json"
TOPOLOGIES = EVAL / "topologies.json"
MANIFEST = EVAL / "presentations" / "manifest.json"
CAPABILITY_SOURCE = ROOT / "docs" / "AGENT-GOVERNANCE-CAPABILITY-SOURCE.md"

FREEZE_C = "1fc38f979d67ff29649f69ae39b8d46d2523518b"
HISTORICAL_CORPORA = (
    ("v13", "d0ebe46a68c02c66dcfbb21c3dfaee43fb15c27f"),
    ("v12", "3e5bec392d0b8e5804c4efaad74b795b08dc9779"),
)
EXPECTED_COUNTS = {
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
FROZEN_CANDIDATE_PATHS = (
    "docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md",
    "evals/skill_activation_topology/candidate-hashes-v14.json",
    "evals/skill_activation_topology/topologies.json",
    "evals/skill_activation_topology/presentations/manifest.json",
    "evals/skill_activation_topology/presentations-v5/B2/agent-governance/SKILL.md",
    "evals/skill_activation_topology/presentations-v5/F2/consumer-governance/SKILL.md",
    "evals/skill_activation_topology/presentations-v5/F2/source-maintainer/SKILL.md",
    "evals/skill_activation_topology/presentations-v5/G3/consumer-lifecycle/SKILL.md",
    "evals/skill_activation_topology/presentations-v5/G3/source-maintainer/SKILL.md",
    "evals/skill_activation_topology/presentations-v5/G3/external-skill-trust/SKILL.md",
    "evals/skill_activation_topology/presentations-v5/shared/consumer-lifecycle.md",
    "evals/skill_activation_topology/presentations-v5/shared/source-maintainer.md",
    "evals/skill_activation_topology/presentations-v5/shared/external-skill-trust.md",
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_bytes(revision: str, relative: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{revision}:{relative}"], cwd=ROOT, stderr=subprocess.STDOUT
    )


def git_json(revision: str, relative: str) -> dict:
    return json.loads(git_bytes(revision, relative))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def main() -> int:
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", FREEZE_C, "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )

    corpus = load(CORPUS)
    oracle = load(ORACLE)
    hashes = load(HASHES)
    topologies = load(TOPOLOGIES)
    manifest = load(MANIFEST)

    assert corpus["schema_version"] == "8.0.0"
    assert corpus["corpus_id"] == "MG1-T023-CORPUS-v8"
    assert corpus["candidate_freeze_sha"] == FREEZE_C
    assert corpus["presentation_revision"] == "MG1-T023-PRESENTATIONS-v5"
    assert oracle["schema_version"] == "14.0.0"
    assert oracle["oracle_id"] == "MG1-T023-TOPOLOGY-ORACLE-v14"
    assert oracle["execution_epoch"] == "MG1-T023-EXECUTION-v14"
    assert oracle["corpus_id"] == corpus["corpus_id"]
    assert oracle["candidate_freeze_sha"] == FREEZE_C
    assert oracle["candidate_hash_manifest"] == "evals/skill_activation_topology/candidate-hashes-v14.json"
    assert oracle["presentation_revision"] == "MG1-T023-PRESENTATIONS-v5"
    assert oracle["topology_revision"] == "MG1-T023-TOPOLOGIES-v4"
    assert oracle["candidate_ids"] == ["B2", "F2", "G3"]
    assert oracle["historical_unscheduled_candidates"] == ["B0", "B1"]
    assert topologies["topology_revision"] == oracle["topology_revision"]
    assert topologies["presentation_revision"] == oracle["presentation_revision"]
    assert manifest["presentation_revision"] == oracle["presentation_revision"]
    assert hashes["identity"] == "MG1-T061-CANDIDATE-HASHES-v2"

    cases = corpus["cases"]
    assert len(cases) == 70
    assert Counter(case["class"] for case in cases) == Counter(EXPECTED_COUNTS)
    assert Counter(
        case.get("near_miss_axis") for case in cases if case["class"] == "near-miss"
    ) == Counter(EXPECTED_AXES)
    assert sum(case["class"] in {"negative", "near-miss"} for case in cases) == 40
    prompts = [case["prompt"] for case in cases]
    assert len(prompts) == len(set(prompts))
    assert len({case["id"] for case in cases}) == 70

    current_prompts = set(prompts)
    for label, revision in HISTORICAL_CORPORA:
        historical = git_json(revision, "evals/skill_activation_topology/corpus.json")
        reused = current_prompts & {case["prompt"] for case in historical.get("cases", [])}
        assert not reused, f"v14 reuses exact {label} prompts: {sorted(reused)}"

    # Freeze C must predate v14 holdout/oracle identities.
    freeze_c_corpus = git_json(FREEZE_C, "evals/skill_activation_topology/corpus.json")
    freeze_c_oracle = git_json(FREEZE_C, "evals/skill_activation_topology/oracle.json")
    assert freeze_c_corpus.get("corpus_id") != "MG1-T023-CORPUS-v8"
    assert freeze_c_oracle.get("oracle_id") != "MG1-T023-TOPOLOGY-ORACLE-v14"

    # Candidate semantics/provenance must be byte-identical from Freeze C to this holdout freeze.
    for relative in FROZEN_CANDIDATE_PATHS:
        current = (ROOT / relative).read_bytes()
        frozen = git_bytes(FREEZE_C, relative)
        assert current == frozen, f"candidate drift after Freeze C: {relative}"

    # Hash manifest must still describe every candidate/reference byte exactly.
    for relative, expected in hashes["files"].items():
        assert sha256_bytes((ROOT / relative).read_bytes()) == expected
    for target, source in hashes["copy_equivalence"].items():
        assert (ROOT / target).read_bytes() == (ROOT / source).read_bytes()

    method = oracle["trial_method"]
    assert method["reference_stage_candidates"] == ["B2"]
    assert method["challenger_stage_candidates"] == ["F2", "G3"]
    assert method["base_valid_repetitions_per_case_candidate"] == 2
    assert method["max_valid_repetitions_per_case_candidate"] == 3
    assert method["reference_stage_full_completion_base_valid_observations"] == 140
    assert method["challenger_stage_full_completion_base_valid_observations"] == 280
    assert method["overall_full_completion_ceiling_when_challengers_execute"] == 630
    assert oracle["qualifying_thresholds"] == {
        "activation_precision_min": 0.95,
        "activation_recall_min": 0.95,
        "activation_f1_min": 0.95,
        "false_activation_rate_max": 0.05,
        "wrong_specialist_rate_max": 0.05,
        "overactivation_rate_max": 0.05,
        "semantic_outcome_accuracy_overall_min": 0.95,
    }
    assert oracle["stage6_gate"]["provider_model_calls_during_stage5"] == 0

    print(json.dumps({
        "status": "PASS",
        "candidate_freeze_sha": FREEZE_C,
        "corpus_id": corpus["corpus_id"],
        "oracle_id": oracle["oracle_id"],
        "case_count": len(cases),
        "far_denominator": 40,
        "historical_prompt_reuse": 0,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
