"""Deterministic technical coverage for the T023 MG1-v3 harness."""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from itertools import product
from pathlib import Path

import pytest


def load_harness(repo_root: Path):
    path = repo_root / "evals" / "skill_activation_topology" / "harness.py"
    spec = importlib.util.spec_from_file_location("t023_harness", path)
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


def test_frozen_mg1_v3_inputs_validate_and_schedule_480_trials(harness, frozen) -> None:
    assert frozen.oracle["oracle_id"] == "MG1-T023-TOPOLOGY-ORACLE-v3"
    assert frozen.oracle["capability_source_epoch"] == "MG1-2026-08-25-v3"
    assert frozen.oracle["presentation_revision"] == "MG1-T023-PRESENTATIONS-v3"
    assert len(harness.scheduled_trials(frozen)) == 480


@pytest.mark.parametrize("candidate_id", ["B0", "B1", "F2", "G3"])
def test_candidate_materialization_is_exact_byte_copy(
    tmp_path: Path, harness, frozen, candidate_id: str
) -> None:
    destination = tmp_path / candidate_id
    destination.mkdir()
    evidence = harness.materialize_candidate(frozen, candidate_id, destination)

    assert evidence["construction"] == "byte-copy"
    assert evidence["files"]
    for record in evidence["files"]:
        source = harness.REPO_ROOT / record["source"]
        target = destination / record["target"]
        assert target.read_bytes() == source.read_bytes()


def test_expected_entrypoint_union_and_unique_reference_load(harness, frozen) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["id"] == "HI02")
    b0 = harness.TrialSpec(case, "B0", 1)
    g3 = harness.TrialSpec(case, "G3", 1)

    assert harness.expected_entrypoints(frozen, b0) == ["agent-governance"]
    assert harness.expected_entrypoints(frozen, g3) == [
        "source-maintainer",
        "consumer-lifecycle",
    ]
    paths, byte_count = harness.expected_load_path(frozen, b0)
    assert paths == [
        "evals/skill_activation_topology/presentations-v3/shared/consumer-lifecycle.md",
        "evals/skill_activation_topology/presentations-v3/shared/source-maintainer.md",
    ]
    assert byte_count == sum((harness.REPO_ROOT / path).stat().st_size for path in paths)


def test_selection_rule_retains_single_family_without_material_split(harness, frozen) -> None:
    def metrics(candidate: str, *, median: int, f1: float = 0.98) -> dict:
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

    candidate_metrics = {
        "B0": metrics("B0", median=1000),
        "B1": metrics("B1", median=900),
        "F2": metrics("F2", median=800),
        "G3": metrics("G3", median=750),
    }
    selection = harness.apply_selection_rule(frozen, candidate_metrics)
    assert selection["selected_candidate"] == "B0"
    assert selection["material_split_challengers"] == []


def test_selection_rule_selects_material_challenger(harness, frozen) -> None:
    base = {
        "activation_precision": 0.96,
        "activation_recall": 0.96,
        "activation_f1": 0.96,
        "false_activation_rate": 0.01,
        "wrong_specialist_rate": 0.01,
        "overactivation_rate": 0.01,
        "semantic_outcome_accuracy": 0.99,
        "semantic_outcome_accuracy_cross_profile_and_ambiguous": 1.0,
        "cross_profile_violation_count": 0,
        "ambiguous_context_permission_broadening_count": 0,
        "p95_observed_context_bytes": 1200,
        "median_loaded_reference_bytes": 0,
        "p95_loaded_reference_bytes": 0,
        "single_install_feasibility": True,
        "source_distribution_integrity": True,
        "full_deterministic_regression": "PASS",
        "profile_isolation_regression": "PASS",
        "consumer_source_independence_regression": "PASS",
    }
    candidate_metrics = {
        "B0": {**base, "candidate_id": "B0", "median_observed_context_bytes": 1000},
        "B1": {**base, "candidate_id": "B1", "median_observed_context_bytes": 900},
        "F2": {
            **base,
            "candidate_id": "F2",
            "activation_precision": 0.995,
            "activation_recall": 0.995,
            "activation_f1": 0.995,
            "median_observed_context_bytes": 800,
        },
        "G3": {**base, "candidate_id": "G3", "median_observed_context_bytes": 780},
    }
    selection = harness.apply_selection_rule(frozen, candidate_metrics)
    assert selection["selected_candidate"] == "F2"


def test_trial_output_schema_is_closed(harness) -> None:
    assert harness.TRIAL_SCHEMA["additionalProperties"] is False
    assert set(harness.TRIAL_SCHEMA["required"]) == set(harness.TRIAL_SCHEMA["properties"])
    json.dumps(harness.TRIAL_SCHEMA)


@pytest.mark.parametrize("candidate_id", ["B0", "B1", "F2", "G3"])
def test_clarification_expectations_follow_frozen_topology(harness, frozen, candidate_id) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["id"] == "HA01")
    spec = harness.TrialSpec(case, candidate_id, 1)
    assert (
        harness.expected_entrypoints(frozen, spec)
        == frozen.topologies["candidates"][candidate_id]["ambiguous_entrypoints"]
    )


def _perfect_trials(harness, frozen, candidate_id):
    return [
        {
            "case_id": spec.case["id"],
            "candidate_id": candidate_id,
            "repetition": spec.repetition,
            "case_class": spec.case["class"],
            "activated_entrypoints": harness.expected_entrypoints(frozen, spec),
            "expected_entrypoints": harness.expected_entrypoints(frozen, spec),
            "semantic_outcome": spec.case["expected_semantic_outcome"],
            "expected_semantic_outcome": spec.case["expected_semantic_outcome"],
            "granted_capabilities": spec.case["expected_capabilities"],
            "forbidden_capabilities": spec.case.get("forbidden_capabilities", []),
            "permission_broadening": False,
            "loaded_reference_bytes": 100,
            "observed_context_bytes": 1000,
        }
        for spec in harness.scheduled_trials(frozen)
        if spec.candidate_id == candidate_id
    ]


def test_neutral_activation_does_not_broaden_ambiguous_permissions(harness, frozen) -> None:
    trials = _perfect_trials(harness, frozen, "B0")
    evidence = harness.build_deterministic_evidence(frozen)
    metrics = harness.compute_candidate_metrics(frozen, "B0", trials, evidence)
    assert metrics["ambiguous_context_permission_broadening_count"] == 0
    assert metrics["cross_profile_violation_count"] == 0
    assert metrics["activation_f1"] == 1.0
    assert metrics["median_observed_context_bytes"] == 1000
    assert metrics["median_loaded_reference_bytes"] == 100


@pytest.mark.parametrize(
    ("case_class", "field", "value", "metric"),
    [
        (
            "ambiguous",
            "granted_capabilities",
            ["source-maintainer"],
            "ambiguous_context_permission_broadening_count",
        ),
        (
            "ambiguous",
            "permission_broadening",
            True,
            "ambiguous_context_permission_broadening_count",
        ),
        (
            "ambiguous",
            "semantic_outcome",
            "no-activation",
            "ambiguous_context_permission_broadening_count",
        ),
        ("cross-profile", "semantic_outcome", "activate", "cross_profile_violation_count"),
        (
            "cross-profile",
            "granted_capabilities",
            ["consumer-lifecycle"],
            "cross_profile_violation_count",
        ),
    ],
)
def test_boundary_failures_are_counted(harness, frozen, case_class, field, value, metric) -> None:
    trials = _perfect_trials(harness, frozen, "B0")
    trial = next(trial for trial in trials if trial["case_class"] == case_class)
    trial[field] = value
    evidence = harness.build_deterministic_evidence(frozen)
    metrics = harness.compute_candidate_metrics(frozen, "B0", trials, evidence)
    assert metrics[metric] == 1


def test_observed_activation_uses_successful_host_reads(harness, frozen) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["id"] == "HC01")
    trial = harness.TrialSpec(case, "B0", 1)
    events = [
        {"type": "thread.started", "thread_id": "synthetic"},
        {
            "type": "item.completed",
            "item": {
                "type": "command_execution",
                "command": r"Get-Content C:\\trial\\.agents\\skills\\agent-governance\\SKILL.md",
                "exit_code": 0,
            },
        },
        {
            "type": "item.completed",
            "item": {
                "type": "command_execution",
                "command": (
                    r"Get-Content C:\\trial\\.agents\\skills\\agent-governance"
                    r"\\references\\consumer-lifecycle.md"
                ),
                "exit_code": 0,
            },
        },
    ]
    stdout = "\n".join(json.dumps(event) for event in events)
    entrypoints, references, trace = harness._observed_skill_reads(frozen, trial, stdout)
    assert entrypoints == ["agent-governance"]
    assert references == [
        "evals/skill_activation_topology/presentations-v3/shared/consumer-lifecycle.md"
    ]
    assert trace is True


def test_trace_excludes_failed_reads_and_path_mentions_and_deduplicates(harness, frozen) -> None:
    spec = harness.TrialSpec(frozen.corpus["cases"][0], "B0", 1)
    path = ".agents/skills/agent-governance/SKILL.md"
    reference = ".agents/skills/agent-governance/references/consumer-lifecycle.md"
    commands = [
        (f"Get-Content {path}", 1),
        (f"Write-Output '{path}'", 0),
        (f"Test-Path {path}", 0),
        ("Get-Content elsewhere/references/source-maintainer.md", 0),
    ]

    def events(items):
        return "\n".join(
            json.dumps(
                {
                    "type": "item.completed",
                    "item": {
                        "type": "command_execution",
                        "command": command,
                        "exit_code": code,
                    },
                }
            )
            for command, code in items
        )

    assert harness._observed_skill_reads(frozen, spec, events(commands))[:2] == ([], [])
    commands.extend([(f"Get-Content {path}", 0), (f"Get-Content {reference}", 0)] * 2)
    observed = harness._observed_skill_reads(frozen, spec, events(commands))
    assert observed[:2] == (
        ["agent-governance"],
        [frozen.manifest["shared_references"]["consumer-lifecycle"]],
    )


def test_resume_rejects_changed_model_effort_or_frozen_identity(harness, frozen) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["id"] == "HC01")
    trial = harness.TrialSpec(case, "B0", 1)
    structured = {"case_id": "HC01", "candidate_id": "B0", "repetition": 1}
    raw = {
        "trial_key": trial.key,
        "command": [
            "codex",
            "exec",
            "--model",
            "gpt-5.6-sol",
            'model_reasoning_effort="medium"',
        ],
        "materialization": {
            "candidate_id": "B0",
            "presentation_revision": frozen.oracle["presentation_revision"],
            "capability_source_epoch": frozen.oracle["capability_source_epoch"],
        },
    }
    harness._validate_partial(
        frozen,
        trial,
        structured,
        raw,
        model="gpt-5.6-sol",
        effort="medium",
    )
    with pytest.raises(harness.HarnessError, match="model/effort"):
        harness._validate_partial(
            frozen,
            trial,
            structured,
            raw,
            model="gpt-5.6-sol",
            effort="high",
        )


def test_persisted_live_evidence_is_complete_and_recomputable(harness, frozen) -> None:
    evidence = harness.HERE / "evidence" / "mg1-v3-codex-windows-gpt-5.6-sol-medium"
    metadata = harness._load_json(evidence / "run-metadata.json")
    assert metadata["oracle_id"] == frozen.oracle["oracle_id"]
    assert metadata["runner_sha256"] == harness._sha256(Path(harness.__file__))
    assert metadata["scheduled_trials"] == metadata["completed_trials"] == 480
    trials = harness.load_trials(evidence / "trials.jsonl")
    raw_trials = harness.load_trials(evidence / "raw-trials.jsonl")
    assert len(trials) == 480
    assert len(raw_trials) == 480

    counts = Counter(
        (trial["case_id"], trial["candidate_id"], trial["repetition"]) for trial in trials
    )
    expected_keys = set(
        product(
            [case["id"] for case in frozen.corpus["cases"]],
            frozen.oracle["candidate_ids"],
            range(1, 4),
        )
    )
    assert set(counts) == expected_keys
    assert set(counts.values()) == {1}
    assert {raw["trial_key"] for raw in raw_trials} == {
        f"{case_id}--{candidate_id}--r{repetition}"
        for case_id, candidate_id, repetition in expected_keys
    }

    raw_by_key = {raw["trial_key"]: raw for raw in raw_trials}
    trials_by_key = {
        f"{trial['case_id']}--{trial['candidate_id']}--r{trial['repetition']}": trial
        for trial in trials
    }
    thread_ids = set()
    workspaces = set()
    for spec in harness.scheduled_trials(frozen):
        raw = raw_by_key[spec.key]
        trial = trials_by_key[spec.key]
        assert raw["prompt"] == harness._trial_prompt(spec.case)
        assert raw["returncode"] == 0
        assert trial["case_class"] == spec.case["class"]
        assert trial["expected_semantic_outcome"] == spec.case["expected_semantic_outcome"]
        assert trial["expected_entrypoints"] == harness.expected_entrypoints(frozen, spec)
        assert trial["forbidden_capabilities"] == spec.case.get("forbidden_capabilities", [])
        assert trial["host_trace_available"] is True
        assert raw["command"][raw["command"].index("--model") + 1] == "gpt-5.6-sol"
        assert 'model_reasoning_effort="medium"' in raw["command"]
        workspaces.add(raw["command"][raw["command"].index("--cd") + 1])
        events = [json.loads(line) for line in raw["stdout_jsonl"].splitlines() if line.strip()]
        threads = [event["thread_id"] for event in events if event["type"] == "thread.started"]
        assert len(threads) == 1
        thread_ids.update(threads)
        model_result = json.loads(raw["final_message"])
        for field in (
            "semantic_outcome",
            "granted_capabilities",
            "permission_broadening",
            "response_summary",
        ):
            assert trial[field] == model_result[field]
        assert trial["reported_activated_entrypoints"] == model_result["activated_entrypoints"]
        for record in raw["materialization"]["files"]:
            assert record["sha256"] == harness._sha256(harness.REPO_ROOT / record["source"])
        observed = harness._observed_skill_reads(frozen, spec, raw["stdout_jsonl"])
        assert observed == (trial["activated_entrypoints"], trial["loaded_reference_paths"], True)

    assert len(thread_ids) == len(workspaces) == 480

    deterministic = harness._load_json(evidence / "deterministic-evidence.json")
    persisted_metrics = harness._load_json(evidence / "metrics.json")
    recomputed_metrics = {
        candidate: harness.compute_candidate_metrics(frozen, candidate, trials, deterministic)
        for candidate in frozen.oracle["candidate_ids"]
    }
    assert recomputed_metrics == persisted_metrics
    assert harness.apply_selection_rule(frozen, recomputed_metrics) == harness._load_json(
        evidence / "selection.json"
    )

    assert all("observed_context_bytes" in trial for trial in trials)
    assert all(
        trial["observed_context_bytes"]
        == sum(trial["activation_surface_bytes"].values()) + trial["loaded_reference_bytes"]
        for trial in trials
    )


def test_v3_holdout_has_no_exact_prompt_from_closed_v2_evidence(harness, frozen) -> None:
    evidence = harness.HERE / "evidence" / "mg1-v2-codex-windows-gpt-5.6-sol-medium"
    previous = harness.load_trials(evidence / "raw-trials.jsonl")
    prior_prompts = {
        raw["prompt"].split("\n\nThis is an isolated, read-only")[0] for raw in previous
    }
    assert len(prior_prompts) == 30
    assert not ({case["prompt"] for case in frozen.corpus["cases"]} & prior_prompts)


def test_preserved_v3_records_have_frozen_identity_and_host_trace_integrity(
    harness, frozen
) -> None:
    evidence = harness.HERE / "evidence" / "mg1-v3-codex-windows-gpt-5.6-sol-medium"
    metadata = harness._load_json(evidence / "run-metadata.json")
    trials = harness.load_trials(evidence / "trials.jsonl")
    raw_trials = harness.load_trials(evidence / "raw-trials.jsonl")
    specs = {spec.key: spec for spec in harness.scheduled_trials(frozen)}
    raw_by_key = {raw["trial_key"]: raw for raw in raw_trials}
    assert len(trials) == len(raw_trials) == len(raw_by_key) == metadata["completed_trials"]
    thread_ids = set()
    workspaces = set()
    for trial in trials:
        key = f"{trial['case_id']}--{trial['candidate_id']}--r{trial['repetition']}"
        spec = specs[key]
        raw = raw_by_key[key]
        harness._validate_partial(frozen, spec, trial, raw, model="gpt-5.6-sol", effort="medium")
        assert raw["prompt"] == harness._trial_prompt(spec.case)
        assert raw["returncode"] == 0
        assert trial["expected_entrypoints"] == harness.expected_entrypoints(frozen, spec)
        assert trial["expected_semantic_outcome"] == spec.case["expected_semantic_outcome"]
        model_result = json.loads(raw["final_message"])
        for field in ("semantic_outcome", "granted_capabilities", "permission_broadening"):
            assert trial[field] == model_result[field]
        observed = harness._observed_skill_reads(frozen, spec, raw["stdout_jsonl"])
        assert observed == (trial["activated_entrypoints"], trial["loaded_reference_paths"], True)
        for record in raw["materialization"]["files"]:
            assert record["sha256"] == harness._sha256(harness.REPO_ROOT / record["source"])
        assert trial["loaded_reference_bytes"] == sum(
            (harness.REPO_ROOT / path).stat().st_size for path in trial["loaded_reference_paths"]
        )
        assert trial["observed_context_bytes"] == (
            sum(trial["activation_surface_bytes"].values()) + trial["loaded_reference_bytes"]
        )
        workspaces.add(raw["command"][raw["command"].index("--cd") + 1])
        events = [json.loads(line) for line in raw["stdout_jsonl"].splitlines() if line.strip()]
        threads = [event["thread_id"] for event in events if event["type"] == "thread.started"]
        assert len(threads) == 1
        thread_ids.update(threads)
    assert len(thread_ids) == len(workspaces) == len(trials)
    assert metadata["runner_sha256"] == harness._sha256(Path(harness.__file__))
    for relative, digest in metadata["frozen_asset_sha256"].items():
        assert harness._sha256(harness.REPO_ROOT / relative) == digest
