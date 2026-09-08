"""Deterministic technical coverage for the T061 MG1-v14 topology harness."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


def load_harness(repo_root: Path):
    path = repo_root / "evals" / "skill_activation_topology" / "harness.py"
    spec = importlib.util.spec_from_file_location("t023_v14_harness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def harness(repo_root: Path):
    return load_harness(repo_root)


@pytest.fixture(scope="module")
def frozen(harness):
    return harness.load_frozen_inputs()


def test_frozen_v14_inputs_validate_and_schedule_expected_ceilings(harness, frozen) -> None:
    assert frozen.oracle["oracle_id"] == "MG1-T023-TOPOLOGY-ORACLE-v14"
    assert frozen.oracle["execution_epoch"] == "MG1-T023-EXECUTION-v14"
    assert frozen.oracle["candidate_freeze_sha"] == "1fc38f979d67ff29649f69ae39b8d46d2523518b"
    assert frozen.oracle["candidate_ids"] == ["B2", "F2", "G3"]
    assert frozen.oracle["presentation_revision"] == "MG1-T023-PRESENTATIONS-v5"
    assert frozen.corpus["corpus_id"] == "MG1-T023-CORPUS-v8"
    assert len(frozen.corpus["cases"]) == 70
    assert len(harness.stage_schedule(frozen, "R")) == 140
    assert len(harness.stage_schedule(frozen, "C")) == 280
    assert len(harness.scheduled_trials(frozen)) == 420
    assert len(harness.all_possible_trials(frozen)) == 630


@pytest.mark.parametrize("candidate_id", ["B2", "F2", "G3"])
def test_candidate_materialization_is_exact_byte_copy(
    tmp_path: Path, harness, frozen, candidate_id: str
) -> None:
    destination = tmp_path / candidate_id
    destination.mkdir()
    evidence = harness.materialize_candidate(frozen, candidate_id, destination)
    assert evidence["construction"] == "byte-copy"
    assert evidence["presentation_revision"] == "MG1-T023-PRESENTATIONS-v5"
    for record in evidence["files"]:
        source = harness.REPO_ROOT / record["source"]
        target = destination / record["target"]
        assert target.read_bytes() == source.read_bytes()


def test_v14_expected_entrypoint_union_and_progressive_reference_path(harness, frozen) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["id"] == "C14I02")
    b2 = harness.TrialSpec(case, "B2", 1)
    g3 = harness.TrialSpec(case, "G3", 1)
    assert harness.expected_entrypoints(frozen, b2) == ["agent-governance"]
    assert harness.expected_entrypoints(frozen, g3) == [
        "source-maintainer",
        "consumer-lifecycle",
    ]
    paths, byte_count = harness.expected_load_path(frozen, b2)
    assert paths == [
        "evals/skill_activation_topology/presentations-v5/shared/consumer-lifecycle.md",
        "evals/skill_activation_topology/presentations-v5/shared/source-maintainer.md",
    ]
    assert byte_count == sum((harness.REPO_ROOT / path).stat().st_size for path in paths)


def test_ambiguous_positive_applicability_activates_only_b2_router(harness, frozen) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["id"] == "C14A01")
    assert harness.expected_entrypoints(frozen, harness.TrialSpec(case, "B2", 1)) == [
        "agent-governance"
    ]
    assert harness.expected_entrypoints(frozen, harness.TrialSpec(case, "F2", 1)) == []
    assert harness.expected_entrypoints(frozen, harness.TrialSpec(case, "G3", 1)) == []


def test_negative_and_near_miss_cases_have_no_expected_entrypoint(harness, frozen) -> None:
    for case in frozen.corpus["cases"]:
        if case["class"] not in {"negative", "near-miss"}:
            continue
        for candidate in frozen.oracle["candidate_ids"]:
            assert harness.expected_entrypoints(frozen, harness.TrialSpec(case, candidate, 1)) == []


def _metrics(candidate: str, *, median: int, f1: float = 0.98) -> dict:
    return {
        "candidate_id": candidate,
        "activation_precision": f1,
        "activation_recall": f1,
        "activation_f1": f1,
        "false_activation_rate": 0.0,
        "wrong_specialist_rate": 0.0,
        "overactivation_rate": 0.0,
        "semantic_outcome_accuracy": 1.0,
        "semantic_outcome_accuracy_cross_profile_and_ambiguous": 1.0,
        "cross_profile_violation_count": 0,
        "ambiguous_context_permission_broadening_count": 0,
        "median_observed_context_bytes": median,
        "p95_observed_context_bytes": median,
        "median_loaded_reference_bytes": 0,
        "p95_loaded_reference_bytes": 0,
        "single_install_feasibility": True,
        "source_distribution_integrity": True,
        "full_deterministic_regression": "PASS",
        "profile_isolation_regression": "PASS",
        "consumer_source_independence_regression": "PASS",
    }


def test_v14_reference_selection_requires_qualifying_b2(harness, frozen) -> None:
    good = _metrics("B2", median=1000)
    selected = harness.select_single_family_reference(frozen, {"B2": good})
    assert selected["single_family_reference"] == "B2"
    bad = {**good, "false_activation_rate": 0.075}
    blocked = harness.select_single_family_reference(frozen, {"B2": bad})
    assert blocked["status"] == "BLOCKED"
    assert blocked["single_family_reference"] is None


def test_v14_selection_retains_b2_without_material_split(harness, frozen) -> None:
    metrics = {
        "B2": _metrics("B2", median=1000, f1=0.98),
        "F2": _metrics("F2", median=800, f1=0.99),
        "G3": _metrics("G3", median=780, f1=0.99),
    }
    selection = harness.apply_selection_rule(frozen, metrics)
    assert selection["selected_candidate"] == "B2"
    assert selection["material_split_challengers"] == []


def test_v14_selection_accepts_material_f2(harness, frozen) -> None:
    metrics = {
        "B2": _metrics("B2", median=1000, f1=0.96),
        "F2": _metrics("F2", median=800, f1=0.995),
        "G3": _metrics("G3", median=900, f1=0.96),
    }
    selection = harness.apply_selection_rule(frozen, metrics)
    assert selection["selected_candidate"] == "F2"
    assert selection["material_split_challengers"] == ["F2"]


def test_trial_output_schema_is_closed(harness) -> None:
    assert harness.TRIAL_SCHEMA["additionalProperties"] is False
    assert set(harness.TRIAL_SCHEMA["required"]) == set(harness.TRIAL_SCHEMA["properties"])
    json.dumps(harness.TRIAL_SCHEMA)


def test_model_visible_turn_is_exact_prompt_plus_preserved_neutral_suffix(harness, frozen) -> None:
    suffix = frozen.envelope["user_suffix"]
    forbidden = frozen.envelope["forbidden_added_terms_casefold"]
    for case in frozen.corpus["cases"]:
        visible = harness._trial_prompt(frozen, case)
        assert visible == f"{case['prompt']}\n\n{suffix}"
        added = visible.removeprefix(case["prompt"]).casefold()
        assert not [term for term in forbidden if term in added]


@pytest.mark.parametrize("role", ["neutral", "source", "consumer"])
def test_fixture_materialization_remains_role_bounded(
    tmp_path: Path, harness, frozen, role: str
) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["fixture_role"] == role)
    evidence = harness.materialize_fixture(frozen, case, tmp_path)
    assert evidence["fixture_role"] == role
    expected = frozen.envelope["fixtures"][role]
    expected_files = {item["path"]: item["json"] for item in expected.get("files", [])}
    actual_files = {
        path.relative_to(tmp_path).as_posix(): json.loads(path.read_text(encoding="utf-8"))
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    assert actual_files == expected_files


def test_v14_historical_prompt_exclusions_are_frozen(frozen) -> None:
    assert frozen.corpus["historical_prompt_exclusion"] == [
        {
            "revision": "MG1-v13",
            "commit": "d0ebe46a68c02c66dcfbb21c3dfaee43fb15c27f",
            "path": "evals/skill_activation_topology/corpus.json",
        },
        {
            "revision": "MG1-v12",
            "commit": "3e5bec392d0b8e5804c4efaad74b795b08dc9779",
            "path": "evals/skill_activation_topology/corpus.json",
        },
    ]


def test_freeze_c_evidence_is_provider_free(harness, frozen) -> None:
    evidence = harness.build_deterministic_evidence(frozen)
    freeze = evidence["freeze_and_holdout"]
    assert freeze["status"] == "PASS"
    assert freeze["candidate_bytes_unchanged_since_freeze_a"] is True
    assert freeze["exact_v12_prompt_reuse_count"] == 0
    assert freeze["false_activation_denominator"] == 40
    assert freeze["provider_model_calls_issued"] == 0
    assert evidence["provider_model_calls_issued_during_deterministic_gate"] == 0


def test_v14_host_and_scheduling_contract_remains_frozen(frozen) -> None:
    method = frozen.oracle["trial_method"]
    assert method["reference_stage_candidates"] == ["B2"]
    assert method["challenger_stage_candidates"] == ["F2", "G3"]
    assert method["base_valid_repetitions_per_case_candidate"] == 2
    assert method["max_valid_repetitions_per_case_candidate"] == 3
    assert frozen.oracle["windows_backend_resolution"]["codex_cli_baseline"] == "0.149.0"
    assert frozen.oracle["stage6_gate"]["required_live_cell"] == (
        "Codex / native Windows / GPT-5.6 Sol / Medium"
    )
