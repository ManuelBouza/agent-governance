"""Orchestrator-owned conformance oracle for T034 native SDD materialization.

This file is frozen acceptance semantics under D052/T034-A2-v1. Executor
implementation may satisfy and execute it but must not edit its semantic
assertions.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_cli(cli: Path, *arguments: object, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(cli), *(str(argument) for argument in arguments)],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_native_sdd_is_required_installed_core(
    repo_root: Path, tmp_path: Path
) -> None:
    engine = _load_module(
        repo_root / "src" / "agent_governance" / "engine.py",
        "t034_engine",
    )

    assert "SDD.md" in engine.CORE_FILES
    assert engine.CORE_VERSION_FIELDS["SDD.md"] == "SDD-Version"

    cli = repo_root / "governance-skill" / "scripts" / "governance.py"
    target = tmp_path / "consumer"
    target.mkdir()

    bootstrap = _run_cli(cli, "bootstrap", target, cwd=repo_root)
    assert bootstrap.returncode == 0, bootstrap.stderr

    installed_sdd = target / ".agent-governance" / "SDD.md"
    assert installed_sdd.read_bytes() == (repo_root / "governance-core" / "SDD.md").read_bytes()

    validate = _run_cli(cli, "validate", target, cwd=repo_root)
    assert validate.returncode == 0, validate.stderr

    installed_sdd.unlink()
    missing = _run_cli(cli, "validate", target, cwd=repo_root)
    assert missing.returncode != 0
    assert "missing" in missing.stderr.lower()


def test_core_and_artifact_expect_protocol_1_14_with_sdd(
    repo_root: Path, tmp_path: Path
) -> None:
    helpers = _load_module(repo_root / "tests" / "_helpers.py", "t034_helpers")
    assert "SDD.md" in helpers.CORE_REQUIRED_MODULES

    builder = _load_module(
        repo_root / "src" / "agent_governance" / "artifact.py",
        "t034_artifact_builder",
    )
    artifact = tmp_path / "governance-skill"
    identity = builder.build_artifact(
        repo_root,
        artifact,
        skill_version="0.1.0",
        installed_footprint_version="1.0.0",
        source_commit="d" * 40,
    )

    assert identity["protocol_version"] == "1.14.0"
    assert "core/SDD.md" in {entry["path"] for entry in identity["files"]}
    assert (artifact / "core" / "SDD.md").read_bytes() == (
        repo_root / "governance-core" / "SDD.md"
    ).read_bytes()


def test_missing_external_sdd_uses_native_sdd_without_external_install(
    repo_root: Path,
) -> None:
    corpus_path = repo_root / "evals" / "consumer_governance" / "corpus.json"
    grader_path = repo_root / "evals" / "consumer_governance" / "grader.py"
    corpus = json.loads(corpus_path.read_text(encoding="utf-8"))
    grader = _load_module(grader_path, "t034_consumer_governance_grader")

    case = next(item for item in corpus["cases"] if item["id"] == "cg-pos-validation-001")
    assert case["coexistence"]["shape"] == "no_sdd"
    assert case["coexistence"]["expected_behaviors"] == [
        "use_native_sdd",
        "refuse_unsolicited_external_sdd",
    ]
    assert {
        "native_sdd_fallback",
        "no_unsolicited_external_sdd",
    } <= set(case["surface_tags"])
    assert "native sdd" in case["prompt"].casefold()
    assert "external sdd" in case["prompt"].casefold()

    assert "use_native_sdd" in grader.BEHAVIORS
    assert "refuse_unsolicited_external_sdd" in grader.BEHAVIORS
    assert "refuse_unsolicited_sdd" not in grader.BEHAVIORS
    assert "native_sdd_fallback" in grader.COEXISTENCE_TAGS
    assert "no_unsolicited_external_sdd" in grader.COEXISTENCE_TAGS
    assert "no_unsolicited_sdd" not in grader.COEXISTENCE_TAGS

    report = grader.validate_corpus(corpus)
    assert report["status"] == "pass"

    for required_behavior in (
        "use_native_sdd",
        "refuse_unsolicited_external_sdd",
    ):
        mutated = copy.deepcopy(corpus)
        mutated_case = next(
            item for item in mutated["cases"] if item["id"] == "cg-pos-validation-001"
        )
        mutated_case["coexistence"]["expected_behaviors"].remove(required_behavior)
        with pytest.raises(
            grader.CorpusError,
            match="no_sdd must use native SDD and refuse unsolicited external SDD",
        ):
            grader.validate_corpus(mutated)
