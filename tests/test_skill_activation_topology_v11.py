"""Historical V12 immutability and V13 freshness checks for T061."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

FREEZE_A = "a454091aff7bb932372a6057e2d9804f94e66320"
CORPUS_PATH = "evals/skill_activation_topology/corpus.json"
ORACLE_PATH = "evals/skill_activation_topology/oracle.json"


def _git_bytes(repo_root: Path, revision: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{revision}:{relative}"], cwd=repo_root)


def test_v12_remains_historical_at_pre_freeze_a_parent(repo_root: Path) -> None:
    oracle = json.loads(_git_bytes(repo_root, f"{FREEZE_A}^", ORACLE_PATH))
    corpus = json.loads(_git_bytes(repo_root, f"{FREEZE_A}^", CORPUS_PATH))
    assert oracle["schema_version"] == "12.0.0"
    assert oracle["oracle_id"] == "MG1-T023-TOPOLOGY-ORACLE-v12"
    assert oracle["candidate_ids"] == ["B0", "B1", "F2", "G3"]
    assert corpus["schema_version"] == "6.0.0"
    assert corpus["corpus_id"] == "MG1-T023-CORPUS-v6"
    assert len(corpus["cases"]) == 40


def test_v13_has_zero_exact_v12_prompt_reuse(repo_root: Path) -> None:
    prior = json.loads(_git_bytes(repo_root, f"{FREEZE_A}^", CORPUS_PATH))
    current = json.loads((repo_root / CORPUS_PATH).read_text(encoding="utf-8"))
    prior_prompts = {case["prompt"] for case in prior["cases"]}
    current_prompts = {case["prompt"] for case in current["cases"]}
    assert len(current_prompts) == 70
    assert prior_prompts.isdisjoint(current_prompts)


def test_v3_historical_presentations_are_unchanged_by_v13(repo_root: Path) -> None:
    paths = [
        "evals/skill_activation_topology/presentations-v3/B0/agent-governance/SKILL.md",
        "evals/skill_activation_topology/presentations-v3/B1/agent-governance-router/SKILL.md",
        "evals/skill_activation_topology/presentations-v3/F2/consumer-governance/SKILL.md",
        "evals/skill_activation_topology/presentations-v3/F2/source-maintainer/SKILL.md",
        "evals/skill_activation_topology/presentations-v3/G3/consumer-lifecycle/SKILL.md",
        "evals/skill_activation_topology/presentations-v3/G3/source-maintainer/SKILL.md",
        "evals/skill_activation_topology/presentations-v3/G3/external-skill-trust/SKILL.md",
    ]
    for relative in paths:
        assert (repo_root / relative).read_bytes() == _git_bytes(
            repo_root, f"{FREEZE_A}^", relative
        )
