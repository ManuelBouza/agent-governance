"""Focused deterministic tests for T015 Consumer Governance trigger corpus."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def corpus_path(repo_root: Path) -> Path:
    return repo_root / "evals" / "consumer_governance" / "corpus.json"


@pytest.fixture(scope="module")
def corpus(corpus_path: Path) -> dict:
    return json.loads(corpus_path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def grader(repo_root: Path):
    path = repo_root / "evals" / "consumer_governance" / "grader.py"
    spec = importlib.util.spec_from_file_location("consumer_governance_grader", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_authoritative_corpus_passes_with_balanced_fixed_partitions(corpus: dict, grader) -> None:
    report = grader.validate_corpus(corpus)
    assert report == {
        "status": "pass",
        "schema_version": 1,
        "total_cases": 36,
        "counts": {
            "train": {"near_miss": 6, "negative": 6, "positive": 6},
            "validation": {"near_miss": 6, "negative": 6, "positive": 6},
        },
    }


def test_cli_reports_deterministic_json(repo_root: Path, corpus_path: Path) -> None:
    grader_path = repo_root / "evals" / "consumer_governance" / "grader.py"
    result = subprocess.run(
        [sys.executable, str(grader_path), "--corpus", str(corpus_path)],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["total_cases"] == 36
    assert result.stderr == ""


def _drop_validation_negative(data: dict) -> None:
    data["cases"] = [
        case
        for case in data["cases"]
        if not (case["partition"] == "validation" and case["category"] == "negative")
    ]


def _duplicate_id(data: dict) -> None:
    data["cases"][1]["id"] = data["cases"][0]["id"]


def _duplicate_prompt_globally(data: dict) -> None:
    data["cases"][-1]["prompt"] = (
        "  INSTALL agent governance in this disposable application repository, "
        "and initialize its consumer state!  "
    )


def _duplicate_content_globally(data: dict) -> None:
    source = data["cases"][0]
    target = data["cases"][-1]
    target["prompt"] = source["prompt"]
    target["surface_tags"] = source["surface_tags"]
    target["coexistence"] = source["coexistence"]


def _misalign_activation(data: dict) -> None:
    data["cases"][0]["expected_activation"] = False


def _add_unknown_key(data: dict) -> None:
    data["cases"][0]["unexpected"] = "value"


def _remove_required_key(data: dict) -> None:
    del data["cases"][0]["synthetic"]


def _use_non_string_enum(data: dict) -> None:
    data["cases"][0]["category"] = ["positive"]


def _use_vendor_authority(data: dict) -> None:
    data["authority_policy"] = "vendor_defaults"


def _use_malformed_behavior_list(data: dict) -> None:
    coexistence = next(case["coexistence"] for case in data["cases"] if case["coexistence"])
    coexistence["expected_behaviors"] = 3


def _remove_surface(data: dict) -> None:
    for case in data["cases"]:
        case["surface_tags"] = [tag for tag in case["surface_tags"] if tag != "bootstrap_install"]


def _break_source_independence(data: dict) -> None:
    data["cases"][0]["source_independent"] = False


def _add_source_absolute_path(data: dict) -> None:
    data["cases"][0]["prompt"] += " Read /home/owner/agent-governance/governance-core first."


def _add_source_relative_path(data: dict) -> None:
    data["cases"][0]["prompt"] += " Load ../governance-skill/scripts/governance.py first."


def _add_source_docs_tasks_path(data: dict) -> None:
    data["cases"][0]["prompt"] += " Read docs/tasks/T015.md from the source checkout."


def _use_boolean_schema_version(data: dict) -> None:
    data["schema_version"] = True


def _add_unknown_tag(data: dict) -> None:
    data["cases"][0]["surface_tags"].append("invented_surface")


def _misplace_operation_tag(data: dict) -> None:
    data["cases"][0]["surface_tags"].append("generic_coding")


def _misplace_cross_cutting_tag(data: dict) -> None:
    data["cases"][0]["surface_tags"].append("consumer_vs_maintainer")


def _remove_required_cross_cutting_placement(data: dict) -> None:
    data["cases"][0]["surface_tags"].remove("source_independence")


def _remove_coexistence_shape_tag(data: dict) -> None:
    case = next(case for case in data["cases"] if case["coexistence"])
    case["surface_tags"].remove(case["coexistence"]["shape"])


def _remove_coexistence_behavior_tag(data: dict) -> None:
    case = next(
        case
        for case in data["cases"]
        if case["coexistence"]
        and "preserve_managed_surfaces" in case["coexistence"]["expected_behaviors"]
    )
    case["surface_tags"].remove("managed_preservation")


def _delete_one_case(data: dict) -> None:
    data["cases"].pop()


def _drop_conflict_outcome(data: dict) -> None:
    overlap = next(
        case["coexistence"]
        for case in data["cases"]
        if case["coexistence"] and case["coexistence"]["governance_overlap"]
    )
    overlap["expected_behaviors"].remove("fail_closed_conflict")


def _drop_preservation_outcome(data: dict) -> None:
    managed = next(
        case["coexistence"]
        for case in data["cases"]
        if case["coexistence"] and case["coexistence"]["managed_surfaces"]
    )
    managed["expected_behaviors"].remove("preserve_managed_surfaces")


def _remove_native_sdd_fallback(data: dict) -> None:
    no_sdd = next(
        case["coexistence"]
        for case in data["cases"]
        if case["coexistence"] and case["coexistence"]["shape"] == "no_sdd"
    )
    no_sdd["expected_behaviors"].remove("use_native_sdd")


@pytest.mark.parametrize(
    ("mutate", "error"),
    [
        (_drop_validation_negative, "expected 6 cases for validation/negative"),
        (_delete_one_case, "expected 6 cases for validation/near_miss"),
        (_duplicate_id, "duplicate"),
        (_duplicate_prompt_globally, "duplicate normalized prompt"),
        (_duplicate_content_globally, "duplicate normalized"),
        (_misalign_activation, "expected_activation"),
        (_add_unknown_key, "unknown keys"),
        (_remove_required_key, "missing keys"),
        (_use_non_string_enum, "category: invalid value"),
        (_use_vendor_authority, "vendor defaults cannot be authority"),
        (_use_malformed_behavior_list, "expected non-empty list"),
        (_remove_surface, "missing surface tags"),
        (_add_unknown_tag, "unknown tags"),
        (_misplace_operation_tag, "misplaced for positive"),
        (_misplace_cross_cutting_tag, "misplaced for positive"),
        (_remove_required_cross_cutting_placement, "source_independence placements"),
        (_remove_coexistence_shape_tag, "coexistence shape"),
        (_remove_coexistence_behavior_tag, "coexistence behaviors"),
        (_break_source_independence, "synthetic and source_independent must be true"),
        (_add_source_absolute_path, "source checkout path dependency forbidden"),
        (_add_source_relative_path, "source checkout path dependency forbidden"),
        (_add_source_docs_tasks_path, "source checkout path dependency forbidden"),
        (_use_boolean_schema_version, "expected integer 1"),
        (_drop_conflict_outcome, "overlap must fail closed"),
        (_drop_preservation_outcome, "managed surfaces must be preserved"),
        (
            _remove_native_sdd_fallback,
            "no_sdd must use native SDD and refuse unsolicited external SDD",
        ),
    ],
)
def test_mutations_fail_closed(corpus: dict, grader, mutate, error: str) -> None:
    candidate = copy.deepcopy(corpus)
    mutate(candidate)
    with pytest.raises(grader.CorpusError, match=error):
        grader.validate_corpus(candidate)


def test_malformed_json_cli_fails_closed(repo_root: Path, tmp_path: Path) -> None:
    malformed = tmp_path / "malformed.json"
    malformed.write_text("{", encoding="utf-8")
    grader_path = repo_root / "evals" / "consumer_governance" / "grader.py"
    result = subprocess.run(
        [sys.executable, str(grader_path), "--corpus", str(malformed)],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 1
    assert json.loads(result.stdout)["status"] == "fail"


def test_source_checkout_has_no_live_consumer_footprint(repo_root: Path) -> None:
    assert not (repo_root / ".agent-governance").exists()
    assert not (repo_root / ".agent-coordination").exists()
