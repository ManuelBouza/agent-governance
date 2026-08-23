"""Orchestrator-owned conformance oracle for T035 runbook operation readiness.

This file is the semantic acceptance projection for Oracle-ID
T035-RUNBOOK-OPERATION-READINESS, revision T035-D054-v1. Executor
implementation may satisfy and execute it but must not edit its semantic
assertions.
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

RECIPE_FIELDS = {
    "recipe_id",
    "status",
    "operation_id",
    "runbook_id",
    "runbook_step",
    "adapter",
    "binding",
    "effect_classes",
    "invocation",
    "authoritative_sources",
    "preconditions",
    "preview",
    "postconditions",
    "verification",
    "stale_triggers",
    "supersedes",
}
ADAPTER_FIELDS = {"family", "tool", "version", "platform", "shell"}
BINDING_FIELDS = {
    "target_class",
    "resource_scope",
    "privilege",
    "credential_class",
    "network_scope",
}
RECIPE_STATES = {"CANDIDATE", "VERIFIED", "STALE", "REVOKED", "SUPERSEDED"}
SOURCE_CLASSES = {"project_native", "builtin_help", "official_docs", "official_api_schema"}
MATERIAL_EFFECTS = {
    "REMOTE_EXECUTE",
    "PRIVILEGE_ELEVATE",
    "SECRET_USE",
    "DEPLOY_SERVICE_CHANGE",
    "DATA_MUTATE",
    "DESTRUCTIVE_IRREVERSIBLE",
}
CLI_V1 = {"bootstrap", "validate", "state", "event", "skill", "ecosystem", "archive"}


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


def _bootstrap(repo_root: Path, tmp_path: Path) -> tuple[Path, Path]:
    cli = repo_root / "governance-skill" / "scripts" / "governance.py"
    target = tmp_path / "consumer"
    target.mkdir()
    result = _run_cli(cli, "bootstrap", target, cwd=repo_root)
    assert result.returncode == 0, result.stderr
    return cli, target


def _source_template(repo_root: Path) -> dict[str, object]:
    path = repo_root / "governance-skill" / "assets" / "RUNBOOK-RECIPE.template.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _verified_recipe(template: dict[str, object]) -> dict[str, object]:
    recipe = copy.deepcopy(template)
    recipe.update(
        {
            "recipe_id": "recipe.git.status",
            "status": "VERIFIED",
            "operation_id": "git.status",
            "runbook_id": None,
            "runbook_step": None,
            "adapter": {
                "family": "cli",
                "tool": "git",
                "version": "2.51.0",
                "platform": "any",
                "shell": None,
            },
            "binding": {
                "target_class": "repository",
                "resource_scope": "current_repository",
                "privilege": "current_user",
                "credential_class": "none",
                "network_scope": [],
            },
            "effect_classes": ["OBSERVE"],
            "invocation": {
                "kind": "argv",
                "template": ["git", "status", "--short", "--branch"],
            },
            "authoritative_sources": [
                {
                    "source_class": "builtin_help",
                    "reference": "git help status",
                    "version": "2.51.0",
                }
            ],
            "preconditions": ["repository exists"],
            "preview": None,
            "postconditions": ["working tree status was observed"],
            "verification": {
                "verified_at": "2026-08-23T18:00:00Z",
                "evidence": "handoffs/T035-executor-handoff.json#recipe.git.status",
                "result": "pass",
            },
            "stale_triggers": [
                "adapter_version_drift",
                "failed_postcondition_or_replay",
            ],
            "supersedes": None,
        }
    )
    return recipe


def _write_recipe(target: Path, filename: str, recipe: dict[str, object]) -> Path:
    path = target / ".agent-coordination" / "runbooks" / "recipes" / filename
    path.write_text(json.dumps(recipe, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _assert_validate(cli: Path, target: Path, repo_root: Path, *, succeeds: bool) -> None:
    result = _run_cli(cli, "validate", target, cwd=repo_root)
    if succeeds:
        assert result.returncode == 0, result.stderr
    else:
        assert result.returncode != 0


def test_bootstrap_materializes_only_native_runbook_templates(
    repo_root: Path, tmp_path: Path
) -> None:
    cli, target = _bootstrap(repo_root, tmp_path)
    runbooks = target / ".agent-coordination" / "runbooks"
    recipes = runbooks / "recipes"
    semantic_source = repo_root / "governance-skill" / "assets" / "RUNBOOK.template.md"
    recipe_source = repo_root / "governance-skill" / "assets" / "RUNBOOK-RECIPE.template.json"

    assert runbooks.is_dir()
    assert recipes.is_dir()
    assert (runbooks / "RUNBOOK.template.md").read_bytes() == semantic_source.read_bytes()
    assert (recipes / "RUNBOOK-RECIPE.template.json").read_bytes() == recipe_source.read_bytes()
    assert sorted(
        path.relative_to(runbooks).as_posix() for path in runbooks.rglob("*") if path.is_file()
    ) == ["RUNBOOK.template.md", "recipes/RUNBOOK-RECIPE.template.json"]

    template = _source_template(repo_root)
    assert set(template) == RECIPE_FIELDS
    assert template["status"] == "CANDIDATE"
    assert template["status"] in RECIPE_STATES
    assert isinstance(template["adapter"], dict)
    assert set(template["adapter"]) == ADAPTER_FIELDS
    assert isinstance(template["binding"], dict)
    assert set(template["binding"]) == BINDING_FIELDS
    assert isinstance(template["invocation"], dict)
    assert template["invocation"].get("kind") in {"argv", "shell", "api", "sdk", "remote"}
    assert isinstance(template["authoritative_sources"], list)
    assert template["authoritative_sources"]
    assert all(
        isinstance(item, dict) and item.get("source_class") in SOURCE_CLASSES
        for item in template["authoritative_sources"]
    )

    _assert_validate(cli, target, repo_root, succeeds=True)


def test_verified_recipe_requires_exact_trust_evidence(repo_root: Path, tmp_path: Path) -> None:
    cli, target = _bootstrap(repo_root, tmp_path)
    recipe = _verified_recipe(_source_template(repo_root))
    path = _write_recipe(target, "git-status.json", recipe)
    _assert_validate(cli, target, repo_root, succeeds=True)

    mutations = []

    unknown_field = copy.deepcopy(recipe)
    unknown_field["unexpected"] = True
    mutations.append(unknown_field)

    invalid_state = copy.deepcopy(recipe)
    invalid_state["status"] = "TRUSTED"
    mutations.append(invalid_state)

    invalid_source = copy.deepcopy(recipe)
    invalid_source["authoritative_sources"][0]["source_class"] = "community"
    mutations.append(invalid_source)

    no_postcondition = copy.deepcopy(recipe)
    no_postcondition["postconditions"] = []
    mutations.append(no_postcondition)

    no_verification = copy.deepcopy(recipe)
    no_verification["verification"] = None
    mutations.append(no_verification)

    failed_verification = copy.deepcopy(recipe)
    failed_verification["verification"]["result"] = "fail"
    mutations.append(failed_verification)

    no_stale_triggers = copy.deepcopy(recipe)
    no_stale_triggers["stale_triggers"] = []
    mutations.append(no_stale_triggers)

    for mutation in mutations:
        path.write_text(json.dumps(mutation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        _assert_validate(cli, target, repo_root, succeeds=False)


def test_each_material_effect_requires_resolvable_runbook_step(
    repo_root: Path, tmp_path: Path
) -> None:
    cli, target = _bootstrap(repo_root, tmp_path)
    template = _source_template(repo_root)

    for effect in sorted(MATERIAL_EFFECTS):
        recipe = _verified_recipe(template)
        recipe["recipe_id"] = f"recipe.material.{effect.lower()}"
        recipe["operation_id"] = f"material.{effect.lower()}"
        recipe["effect_classes"] = [effect]
        path = _write_recipe(target, "material.json", recipe)
        _assert_validate(cli, target, repo_root, succeeds=False)
        path.unlink()

    runbook = target / ".agent-coordination" / "runbooks" / "rb.remote.md"
    runbook.write_text(
        """# Remote operation runbook

Runbook-ID: `rb.remote`
Status: `ACTIVE`
Revision: `v1`
Owner: `strategy`

## Purpose

Perform one bounded remote action.

## Applicability and exclusions

- Applies when: the approved remote target is bound.
- Excludes: any unapproved target.

## Authorization binding

- Required effect classes: `REMOTE_EXECUTE`
- Target constraints: approved target only
- Privilege ceiling: approved identity only
- Credential class: reference only
- Network scope: approved destination only
- Approval/Human gates: as governed by D033

## Inputs

- target — approved remote target

## Preconditions

- target identity is verified

## Semantic steps

### Step `execute` — perform bounded remote action

- Required effect: `REMOTE_EXECUTE`
- Resource scope: approved target
- Pre-step assertion: target identity matches
- Required state transition/effect: approved remote action occurs
- Post-step assertion: expected remote state is observed
- Evidence: sanitized execution reference
- Retry/idempotency: no blind retry
- Failure route: stop
- Recovery/compensation: strategy-defined recovery

## Checkpoints and Human gates

- honor D033 approval mode

## Postconditions

- expected remote state is established

## Recovery

- Rollback/compensation: strategy-defined recovery
- Unsafe/impossible rollback stop condition: stop when recovery is not safe
- Escalation: strategy

## Evidence

- runbook revision, target, completed step and postcondition
""",
        encoding="utf-8",
    )

    recipe = _verified_recipe(template)
    recipe["recipe_id"] = "recipe.remote.execute"
    recipe["operation_id"] = "remote.execute"
    recipe["effect_classes"] = ["REMOTE_EXECUTE"]
    recipe["runbook_id"] = "rb.remote"
    recipe["runbook_step"] = "execute"
    path = _write_recipe(target, "remote.json", recipe)
    _assert_validate(cli, target, repo_root, succeeds=True)

    recipe["runbook_step"] = "missing-step"
    path.write_text(json.dumps(recipe, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _assert_validate(cli, target, repo_root, succeeds=False)


def test_duplicate_supersession_and_secret_value_controls(repo_root: Path, tmp_path: Path) -> None:
    cli, target = _bootstrap(repo_root, tmp_path)
    template = _source_template(repo_root)
    first = _verified_recipe(template)
    second = copy.deepcopy(first)

    _write_recipe(target, "first.json", first)
    second_path = _write_recipe(target, "second.json", second)
    _assert_validate(cli, target, repo_root, succeeds=False)

    second["recipe_id"] = "recipe.git.status.second"
    second_path.write_text(json.dumps(second, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _assert_validate(cli, target, repo_root, succeeds=False)

    second["status"] = "SUPERSEDED"
    second["supersedes"] = None
    second_path.write_text(json.dumps(second, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _assert_validate(cli, target, repo_root, succeeds=False)

    second["supersedes"] = "recipe.git.status"
    second_path.write_text(json.dumps(second, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _assert_validate(cli, target, repo_root, succeeds=True)

    second["binding"]["credential_value"] = "must-not-be-stored"
    second_path.write_text(json.dumps(second, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _assert_validate(cli, target, repo_root, succeeds=False)


def test_unsafe_recipe_path_fails_closed_without_platform_skip(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cli, target = _bootstrap(repo_root, tmp_path)
    recipes = target / ".agent-coordination" / "runbooks" / "recipes"
    template = recipes / "RUNBOOK-RECIPE.template.json"
    unsafe = recipes / "unsafe-link.json"

    try:
        unsafe.symlink_to(template)
    except OSError:
        engine = _load_module(
            repo_root / "src" / "agent_governance" / "engine.py",
            "t035_engine_unsafe_path",
        )
        original = engine._is_unsafe_link

        def _simulated_unsafe(path: Path) -> bool:
            return path == recipes or original(path)

        monkeypatch.setattr(engine, "_is_unsafe_link", _simulated_unsafe)
        with pytest.raises(engine.GovernanceError):
            engine._validate(target)
    else:
        _assert_validate(cli, target, repo_root, succeeds=False)


def test_t035_does_not_expand_routed_protocol_or_cli(repo_root: Path) -> None:
    engine = _load_module(
        repo_root / "src" / "agent_governance" / "engine.py",
        "t035_engine_preserved_surface",
    )
    assert engine._protocol_version(repo_root / "governance-core" / "GOVERNANCE.md") == "1.14.0"

    parser = engine._parser()
    subparsers = next(
        action for action in parser._actions if isinstance(action, argparse._SubParsersAction)
    )
    assert set(subparsers.choices) == CLI_V1
