"""Deterministic technical coverage for the T023 MG1-v8 harness."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
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


def test_frozen_mg1_v8_inputs_validate_and_schedule_paired_stage_ceilings(harness, frozen) -> None:
    assert frozen.oracle["oracle_id"] == "MG1-T023-TOPOLOGY-ORACLE-v8"
    assert frozen.oracle["capability_source_epoch"] == "MG1-2026-08-25-v3"
    assert frozen.oracle["presentation_revision"] == "MG1-T023-PRESENTATIONS-v3"
    assert len(harness.scheduled_trials(frozen)) == 320
    assert len(harness.stage_schedule(frozen, "R")) == 160
    assert len(harness.stage_schedule(frozen, "C")) == 160
    assert len(harness.all_possible_trials(frozen)) == 480


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
    case = next(case for case in frozen.corpus["cases"] if case["id"] == "WI02")
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


def test_v8_model_visible_turn_is_exactly_prompt_and_neutral_suffix(harness, frozen) -> None:
    suffix = frozen.envelope["user_suffix"]
    forbidden = frozen.envelope["forbidden_added_terms_casefold"]
    for case in frozen.corpus["cases"]:
        visible = harness._trial_prompt(frozen, case)
        assert visible == f"{case['prompt']}\n\n{suffix}"
        added = visible.removeprefix(case["prompt"]).casefold()
        assert not [term for term in forbidden if term in added]


@pytest.mark.parametrize("role", ["neutral", "source", "consumer"])
def test_v8_fixture_materialization_is_exact_and_role_bounded(
    tmp_path: Path, harness, frozen, role: str
) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["fixture_role"] == role)
    evidence = harness.materialize_fixture(frozen, case, tmp_path)
    expected = frozen.envelope["fixtures"][role]
    assert evidence["fixture_role"] == role
    expected_files = {item["path"]: item["json"] for item in expected.get("files", [])}
    actual_files = {
        path.relative_to(tmp_path).as_posix(): json.loads(path.read_text(encoding="utf-8"))
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    assert actual_files == expected_files
    if role == "neutral":
        assert not any(tmp_path.iterdir())


def test_v8_workspace_root_validation_rejects_canonical_path_leak(
    tmp_path: Path, harness, frozen
) -> None:
    accepted = harness._validate_workspace_root(frozen, tmp_path)
    assert accepted["outside_canonical_repository"] is True
    with pytest.raises(harness.HarnessError, match=r"forbidden substring|canonical repository"):
        harness._validate_workspace_root(frozen, harness.REPO_ROOT)


@pytest.mark.parametrize("candidate_id", ["B0", "B1", "F2", "G3"])
def test_clarification_expectations_follow_frozen_topology(harness, frozen, candidate_id) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["id"] == "WA01")
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
    case = next(case for case in frozen.corpus["cases"] if case["id"] == "WC01")
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


def test_resume_rejects_changed_model_effort_or_frozen_identity(
    tmp_path: Path, harness, frozen
) -> None:
    case = next(case for case in frozen.corpus["cases"] if case["id"] == "WC01")
    trial = harness.TrialSpec(case, "B0", 1)
    structured = {"case_id": "WC01", "candidate_id": "B0", "repetition": 1}
    isolation = harness._validate_workspace_root(frozen, tmp_path)
    fixture = harness.materialize_fixture(frozen, case, tmp_path)
    raw = {
        "trial_key": trial.key,
        "command": [
            "codex",
            "exec",
            "--model",
            "gpt-5.6-sol",
            'model_reasoning_effort="medium"',
            "--sandbox",
            "read-only",
            "--ephemeral",
            "--cd",
            str(tmp_path),
        ],
        "materialization": {
            "candidate_id": "B0",
            "presentation_revision": frozen.oracle["presentation_revision"],
            "capability_source_epoch": frozen.oracle["capability_source_epoch"],
        },
        "fixture_materialization": fixture,
        "workspace_isolation": isolation,
    }
    raw["command"].extend(["--ignore-user-config", "--ignore-rules"])
    for feature in harness.MINIMAL_DISABLED_FEATURES:
        raw["command"].extend(["--disable", feature])
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


def test_closed_v4_evidence_cannot_enter_v8_scoring(harness, frozen) -> None:
    evidence = harness.HERE / "evidence" / "mg1-v4-codex-windows-gpt-5.6-sol-medium"
    metadata = harness._load_json(evidence / "run-metadata.json")
    assert metadata["oracle_id"] != frozen.oracle["oracle_id"]
    with pytest.raises(harness.HarnessError):
        harness.validate_complete_evidence(frozen, evidence)


def test_closed_v6_live_runner_is_bound_to_immutable_git_provenance(harness) -> None:
    evidence = harness.HERE / "evidence" / "mg1-v6-codex-windows-gpt-5.6-sol-medium"
    metadata = harness._load_json(evidence / "run-metadata.json")
    harness._validate_executed_runner_provenance(metadata)


def test_v8_holdout_has_no_exact_prompt_from_closed_v2_evidence(harness, frozen) -> None:
    evidence = harness.HERE / "evidence" / "mg1-v2-codex-windows-gpt-5.6-sol-medium"
    previous = harness.load_trials(evidence / "raw-trials.jsonl")
    prior_prompts = {
        raw["prompt"].split("\n\nThis is an isolated, read-only")[0] for raw in previous
    }
    assert len(prior_prompts) == 30
    assert not ({case["prompt"] for case in frozen.corpus["cases"]} & prior_prompts)


def test_preserved_v3_records_remain_bound_to_their_immutable_epoch(harness, frozen) -> None:
    evidence = harness.HERE / "evidence" / "mg1-v3-codex-windows-gpt-5.6-sol-medium"
    metadata = harness._load_json(evidence / "run-metadata.json")
    trials = harness.load_trials(evidence / "trials.jsonl")
    raw_trials = harness.load_trials(evidence / "raw-trials.jsonl")
    raw_by_key = {raw["trial_key"]: raw for raw in raw_trials}
    assert metadata["oracle_id"] != frozen.oracle["oracle_id"]
    assert len(trials) == len(raw_trials) == len(raw_by_key) == metadata["completed_trials"]
    thread_ids = set()
    workspaces = set()
    for trial in trials:
        key = f"{trial['case_id']}--{trial['candidate_id']}--r{trial['repetition']}"
        raw = raw_by_key[key]
        assert raw["returncode"] == 0
        model_result = json.loads(raw["final_message"])
        for field in ("semantic_outcome", "granted_capabilities", "permission_broadening"):
            assert trial[field] == model_result[field]
        assert trial["observed_context_bytes"] == (
            sum(trial["activation_surface_bytes"].values()) + trial["loaded_reference_bytes"]
        )
        workspaces.add(raw["command"][raw["command"].index("--cd") + 1])
        events = [json.loads(line) for line in raw["stdout_jsonl"].splitlines() if line.strip()]
        threads = [event["thread_id"] for event in events if event["type"] == "thread.started"]
        assert len(threads) == 1
        thread_ids.update(threads)
    assert len(thread_ids) == len(workspaces) == len(trials)
    # V3 is diagnostic history, bound to its own immutable implementation, not v4 code/oracle.
    for relative, digest in {
        "evals/skill_activation_topology/harness.py": metadata["runner_sha256"],
        **metadata["frozen_asset_sha256"],
    }.items():
        historical = subprocess.check_output(
            ["git", "show", f"f1e64000eace20ff22761ac9db56a42e974b2fac:{relative}"],
            cwd=harness.REPO_ROOT,
        )
        assert digest in {
            hashlib.sha256(historical).hexdigest(),
            hashlib.sha256(historical.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")).hexdigest(),
        }


@pytest.mark.parametrize("failures", [0, 1, 2])
def test_uniform_recovery_retains_failures_and_stops_after_first_valid(
    harness, frozen, tmp_path, monkeypatch, failures
):
    spec = harness.scheduled_trials(frozen)[0]
    calls = []

    def run_trial(inputs, trial, *, attempt, **kwargs):
        calls.append(attempt)
        raw = {"attempt": attempt, "partial_stdout": "visible timeout evidence"}
        if attempt <= failures:
            raise harness.AttemptFailure("TIMEOUT_UNCLASSIFIED", "timeout", raw)
        # A semantically wrong but structurally valid observation MUST NOT be retried.
        return {"semantic_outcome": "no-activation"}, raw

    monkeypatch.setattr(harness, "run_trial", run_trial)
    result = harness.execute_logical_observation(frozen, spec, output=tmp_path)
    assert calls == list(range(1, min(failures + 1, 2) + 1))
    records = [harness._load_json(path) for path in sorted((tmp_path / "attempts").glob("*.json"))]
    assert [record["status"] for record in records] == ["FAILED"] * failures + (
        ["VALID"] if failures < 2 else []
    )
    assert all(record["raw"]["partial_stdout"] == "visible timeout evidence" for record in records)
    assert (result is None) == (failures == 2)
    assert harness.execute_logical_observation(frozen, spec, output=tmp_path) == result


def test_timeout_retains_visible_streams_and_retry_has_fresh_workspace(
    harness, frozen, tmp_path, monkeypatch
):
    spec = harness.scheduled_trials(frozen)[0]
    workspaces = []

    def run(command, **kwargs):
        workspaces.append(command[command.index("--cd") + 1])
        assert kwargs["timeout"] == 180
        assert kwargs["input"] == harness._trial_prompt(frozen, spec.case)
        raise subprocess.TimeoutExpired(
            command, 180, output=b'{"type":"thread.started"}\n', stderr=b"partial error"
        )

    monkeypatch.setattr(harness.subprocess, "run", run)
    workspace_parent = tmp_path / "workspaces"
    workspace_parent.mkdir()
    result = harness.execute_logical_observation(
        frozen,
        spec,
        output=tmp_path,
        codex_command="codex",
        model="gpt-5.6-sol",
        effort="medium",
        timeout_seconds=180,
        workspace_parent=workspace_parent,
    )
    assert result is None
    assert len(workspaces) == len(set(workspaces)) == 2
    for path in (tmp_path / "attempts").glob("*.json"):
        record = harness._load_json(path)
        assert record["failure_class"] == "TIMEOUT_UNCLASSIFIED"
        assert record["raw"]["stdout_jsonl"] == '{"type":"thread.started"}\n'
        assert record["raw"]["stderr"] == "partial error"


@pytest.mark.parametrize(
    "change",
    [
        {"model": "other"},
        {"effort": "high"},
        {"timeout_seconds": 300},
        {"case": ["WC01"]},
    ],
)
def test_execution_rejects_nonuniform_configuration(harness, frozen, monkeypatch, change):
    args = harness.build_parser().parse_args(["run", "--output", "unused", "--full-acceptance"])
    monkeypatch.setattr(harness.platform, "system", lambda: "Windows")
    for field, value in change.items():
        setattr(args, field, value)
    with pytest.raises(harness.HarnessError):
        harness.validate_execution_config(frozen, args)


def test_terminal_exhaustion_stops_new_work_and_exports_without_scoring(
    harness, frozen, tmp_path, monkeypatch
):
    args = harness.build_parser().parse_args(
        ["run", "--output", str(tmp_path / "run"), "--full-acceptance", "--workers", "1"]
    )
    calls = []

    def run_trial(inputs, spec, **kwargs):
        calls.append((spec.key, kwargs["attempt"]))
        raise harness.AttemptFailure(
            "HOST_NONZERO_EXIT", "synthetic failure", {"trial_key": spec.key}
        )

    monkeypatch.setattr(harness, "run_trial", run_trial)
    monkeypatch.setattr(harness, "_codex_version", lambda _: "synthetic")
    monkeypatch.setattr(harness.platform, "system", lambda: "Windows")
    deterministic = harness.build_deterministic_evidence(frozen)
    for field in (
        "full_deterministic_regression",
        "profile_isolation_regression",
        "consumer_source_independence_regression",
    ):
        deterministic[field] = "PASS"
    monkeypatch.setattr(harness, "build_deterministic_evidence", lambda _: deterministic)
    monkeypatch.setattr(harness, "verify_deterministic", lambda _: 0)

    def passing_preflight(inputs, args, output, workspace_parent):
        profile = {
            "sandbox": "read-only",
            "ignore_user_config": True,
            "ignore_rules": True,
            "disabled_features": list(harness.MINIMAL_DISABLED_FEATURES),
        }
        harness._json_dump(
            output / "host-preflight.json",
            {
                "status": "PASS",
                "selected_sandbox": "read-only",
                "records": [{"effective_host_profile": profile}],
            },
        )
        return "read-only"

    monkeypatch.setattr(harness, "run_host_preflight", passing_preflight)
    assert harness.run_matrix(args) == 1
    assert calls == [(harness.scheduled_trials(frozen)[0].key, attempt) for attempt in (1, 2)]
    assert len(harness.load_trials(args.output / "failed-attempts.jsonl")) == 2
    assert (
        harness._load_json(args.output / "completeness.json")["completed_valid_observations"] == 0
    )
    assert not (args.output / "metrics.json").exists()
    with pytest.raises(harness.HarnessError, match="incomplete"):
        harness.score_matrix(args)
    with pytest.raises(harness.HarnessError, match="overwrite existing"):
        harness.run_matrix(args)


def test_conditional_third_runs_only_on_frozen_field_disagreement(harness, frozen) -> None:
    trials = _perfect_trials(harness, frozen, "B0") + _perfect_trials(harness, frozen, "B1")
    assert harness.conditional_third_specs(frozen, ["B0", "B1"], trials) == []
    target = next(item for item in trials if item["case_id"] == "WC01" and item["repetition"] == 2)
    target["observed_context_bytes"] += 1
    thirds = harness.conditional_third_specs(frozen, ["B0", "B1"], trials)
    assert [item.key for item in thirds] == [f"WC01--{target['candidate_id']}--r3"]


def test_case_aggregation_uses_majority_median_and_forbids_unneeded_third(harness, frozen) -> None:
    trials = _perfect_trials(harness, frozen, "B0")
    first = next(item for item in trials if item["case_id"] == "WC01" and item["repetition"] == 1)
    second = next(item for item in trials if item["case_id"] == "WC01" and item["repetition"] == 2)
    second["semantic_outcome"] = "no-activation"
    third = {**first, "repetition": 3, "observed_context_bytes": 1200}
    trials.append(third)
    aggregate = next(
        item
        for item in harness.aggregate_candidate_trials(frozen, "B0", trials)
        if item["case_id"] == "WC01"
    )
    assert aggregate["semantic_outcome"] == "activate"
    assert aggregate["observed_context_bytes"] == 1000
    assert aggregate["valid_repetitions"] == 3

    second["semantic_outcome"] = "activate"
    with pytest.raises(harness.HarnessError, match="unnecessary third"):
        harness.aggregate_candidate_trials(frozen, "B0", trials)


def test_critical_violation_is_any_occurrence_and_suppresses_candidate_thirds(
    harness, frozen
) -> None:
    trials = _perfect_trials(harness, frozen, "B0") + _perfect_trials(harness, frozen, "B1")
    violation = next(
        item
        for item in trials
        if item["candidate_id"] == "B0"
        and item["case_class"] == "ambiguous"
        and item["repetition"] == 1
    )
    violation["permission_broadening"] = True
    disagreement = next(
        item
        for item in trials
        if item["candidate_id"] == "B0" and item["case_id"] == "WC01" and item["repetition"] == 2
    )
    disagreement["observed_context_bytes"] += 1
    thirds = harness.conditional_third_specs(frozen, ["B0", "B1"], trials)
    assert all(spec.candidate_id != "B0" for spec in thirds)
    evidence = harness.build_deterministic_evidence(frozen)
    metrics = harness.compute_candidate_metrics(frozen, "B0", trials, evidence)
    assert metrics["ambiguous_context_permission_broadening_count"] == 1


def test_capacity_event_does_not_consume_model_attempt(
    harness, frozen, tmp_path, monkeypatch
) -> None:
    spec = harness.stage_schedule(frozen, "R")[0]

    def capacity(*args, **kwargs):
        raise harness.CapacityPause("usage limit", {"stderr": "usage limit reached"})

    monkeypatch.setattr(harness, "run_trial", capacity)
    with pytest.raises(harness.CapacityPause):
        harness.execute_logical_observation(frozen, spec, output=tmp_path)
    assert not list((tmp_path / "attempts").glob("*.json"))
    event = harness._load_json(next((tmp_path / "capacity-events").glob("*.json")))
    assert event["pending_attempt"] == 1


def test_v8_schedule_uses_frozen_semantic_consequence_order(harness, frozen) -> None:
    schedule = harness.stage_schedule(frozen, "R")
    first_case_ids = []
    for spec in schedule:
        if spec.case["id"] not in first_case_ids:
            first_case_ids.append(spec.case["id"])
    assert first_case_ids[:8] == [
        "WX01",
        "WX02",
        "WX03",
        "WX04",
        "WA01",
        "WA02",
        "WA03",
        "WA04",
    ]
    assert first_case_ids[8:14] == ["WN01", "WN02", "WN03", "WN04", "WN05", "WN06"]


def test_minimal_host_command_freezes_required_surface(harness, tmp_path) -> None:
    command = harness._host_command(
        "codex",
        root=tmp_path,
        model="gpt-5.6-sol",
        effort="medium",
        sandbox="read-only",
        schema_path=tmp_path / "shape.json",
        final_path=tmp_path / "result.json",
    )
    assert "--ignore-user-config" in command
    assert "--ignore-rules" in command
    assert 'web_search="disabled"' in command
    assert command[command.index("--sandbox") + 1] == "read-only"
    for feature in harness.MINIMAL_DISABLED_FEATURES:
        assert any(
            command[index : index + 2] == ["--disable", feature]
            for index in range(len(command) - 1)
        )


def test_telemetry_does_not_invent_provider_total_and_counts_stderr_rejections(harness) -> None:
    stdout = "\n".join(
        [
            json.dumps({"type": "thread.started", "thread_id": "synthetic"}),
            json.dumps(
                {
                    "type": "turn.completed",
                    "usage": {
                        "input_tokens": 100,
                        "cached_input_tokens": 80,
                        "output_tokens": 10,
                        "reasoning_output_tokens": 4,
                    },
                }
            ),
        ]
    )
    telemetry = harness._trace_telemetry(stdout, 'Rejected("one") Rejected("two")')
    assert telemetry["token_usage_available"] is True
    assert telemetry["total_tokens"] is None
    assert telemetry["execution_policy_rejected_tool_call_count"] == 2


def test_surface_drift_normalizes_windows_skill_path(harness) -> None:
    stderr = (
        'Get-Content C:\\tmp\\.agents\\skills\\mx-canary\\SKILL.md Rejected("blocked by policy")'
    )
    assert (
        harness._surface_drift("", stderr, skill_path=".agents/skills/mx-canary/SKILL.md")
        == "REQUIRED_SKILL_BODY_READ_REJECTED"
    )


def test_one_finalized_false_activation_is_exactly_futile(harness, frozen) -> None:
    trials = [
        trial for trial in _perfect_trials(harness, frozen, "B0") if trial["case_id"] == "WN01"
    ]
    for trial in trials:
        trial["activated_entrypoints"] = ["agent-governance"]
    certificate = harness.qualification_futility_certificate(frozen, "B0", trials)
    assert certificate["terminal"] is True
    assert certificate["optimistic_final_bounds"]["false_activation_rate"] == pytest.approx(1 / 11)
    assert "false_activation_rate" in certificate["failed_bounds"]


def test_three_semantic_errors_are_futile_but_two_are_not(harness, frozen) -> None:
    perfect = _perfect_trials(harness, frozen, "B0")
    case_ids = ["WC01", "WC02", "WC03"]
    pairs = [trial for trial in perfect if trial["case_id"] in case_ids]
    for trial in pairs:
        trial["semantic_outcome"] = "no-activation"
    three = harness.qualification_futility_certificate(frozen, "B0", pairs)
    assert three["terminal"] is True
    assert three["optimistic_final_bounds"]["semantic_outcome_accuracy"] == 0.925
    two = harness.qualification_futility_certificate(
        frozen, "B0", [trial for trial in pairs if trial["case_id"] != "WC03"]
    )
    assert "semantic_outcome_accuracy" not in two["failed_bounds"]


def test_context_materiality_uses_optimistic_zero_for_unfinished_cases(harness, frozen) -> None:
    relevant = [
        case["id"]
        for case in frozen.corpus["cases"]
        if case["class"] in harness.ACTIVATION_RELEVANT_CLASSES
    ]
    trials = [
        trial
        for trial in _perfect_trials(harness, frozen, "F2")
        if trial["case_id"] in set(relevant[:15])
    ]
    reference = {
        "activation_f1": 0.95,
        "false_activation_rate": 0.0,
        "wrong_specialist_rate": 0.0,
        "overactivation_rate": 0.0,
        "median_observed_context_bytes": 1000,
    }
    certificate = harness.materiality_futility_certificate(frozen, "F2", trials, reference)
    assert certificate["optimistic_median_observed_context_bytes"] == 1000
    assert "material_context" in certificate["failed_bounds"]
