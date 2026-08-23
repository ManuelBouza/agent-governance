"""Orchestrator-owned conformance oracle for D054/T035 runbook readiness.

This file freezes acceptance semantics under D052/T035-D054-v1. Executor
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


def _validate(cli: Path, target: Path, repo_root: Path) -> subprocess.CompletedProcess[str]:
    return _run_cli(cli, "validate", target, cwd=repo_root)


def _verified_recipe(template: dict[str, object], *, recipe_id: str) -> dict[str, object]:
    recipe = copy.deepcopy(template)
    recipe.update(
        {
            "recipe_id": recipe_id,
            "status": "VERIFIED",
            "operation_id": "git.repository.inspect-status",
            "runbook_id": None,
            "runbook_step": None,
            "adapter": {
                "family": "cli",
                "tool": "git",
                "version": "2.53.0.windows.2",
                "platform": "windows",
                "shell": "powershell",
            },
            "binding": {
                "target_class": "repository-worktree",
                "resource_scope": "current governed repository",
                "privilege": "current-user",
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
                    "version": "2.53.0.windows.2",
                },
                {
                    "source_class": "official_docs",
                    "reference": "https://git-scm.com/docs/git-status",
                    "version": "2.53.0",
                },
            ],
            "preconditions": ["working tree path resolves to the intended repository"],
            "preview": None,
            "postconditions": ["repository status is returned without intended mutation"],
            "verification": {
                "verified_at": "2026-08-23T16:00:00Z",
                "evidence": "synthetic-conformance-evidence",
                "result": "pass",
            },
            "stale_triggers": [
                "adapter tool/API version changes",
                "recorded postcondition/replay fails",
            ],
            "supersedes": None,
        }
    )
    return recipe


def test_bootstrap_materializes_native_runbook_recipe_skeleton(
    repo_root: Path, tmp_path: Path
) -> None:
    engine = _load_module(
        repo_root / "src" / "agent_governance" / "engine.py",
        "t035_engine_bootstrap",
    )

    assert "runbooks" in engine.COORDINATION_DIRS
    assert "runbooks/recipes" in engine.COORDINATION_DIRS
    assert engine.ASSET_TARGETS["RUNBOOK.template.md"] == "runbooks/RUNBOOK.template.md"
    assert (
        engine.ASSET_TARGETS["RUNBOOK-RECIPE.template.json"]
        == "runbooks/recipes/RUNBOOK-RECIPE.template.json"
    )

    cli, target = _bootstrap(repo_root, tmp_path)
    runbooks = target / ".agent-coordination" / "runbooks"
    recipes = runbooks / "recipes"
    assert runbooks.is_dir()
    assert recipes.is_dir()

    installed_runbook_template = runbooks / "RUNBOOK.template.md"
    source_runbook_template = repo_root / "governance-skill" / "assets" / "RUNBOOK.template.md"
    assert installed_runbook_template.read_bytes() == source_runbook_template.read_bytes()

    recipe_template_path = recipes / "RUNBOOK-RECIPE.template.json"
    recipe_template = json.loads(recipe_template_path.read_text(encoding="utf-8"))
    assert set(recipe_template) == {
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
    assert recipe_template["status"] == "CANDIDATE"
    assert recipe_template["verification"] is None

    result = _validate(cli, target, repo_root)
    assert result.returncode == 0, result.stderr


def test_verified_recipe_requires_authoritative_provenance_and_postcondition(
    repo_root: Path, tmp_path: Path
) -> None:
    cli, target = _bootstrap(repo_root, tmp_path)
    recipes = target / ".agent-coordination" / "runbooks" / "recipes"
    template = json.loads(
        (recipes / "RUNBOOK-RECIPE.template.json").read_text(encoding="utf-8")
    )

    recipe_path = recipes / "git-status.json"
    valid = _verified_recipe(template, recipe_id="git.status.windows-powershell.v1")
    recipe_path.write_text(json.dumps(valid, indent=2) + "\n", encoding="utf-8", newline="")
    result = _validate(cli, target, repo_root)
    assert result.returncode == 0, result.stderr

    missing_sources = copy.deepcopy(valid)
    missing_sources["authoritative_sources"] = []
    recipe_path.write_text(
        json.dumps(missing_sources, indent=2) + "\n", encoding="utf-8", newline=""
    )
    result = _validate(cli, target, repo_root)
    assert result.returncode != 0
    assert "authoritative" in result.stderr.casefold()

    missing_postcondition = copy.deepcopy(valid)
    missing_postcondition["postconditions"] = []
    recipe_path.write_text(
        json.dumps(missing_postcondition, indent=2) + "\n",
        encoding="utf-8",
        newline="",
    )
    result = _validate(cli, target, repo_root)
    assert result.returncode != 0
    assert "postcondition" in result.stderr.casefold()

    failed_verification = copy.deepcopy(valid)
    failed_verification["verification"] = {
        "verified_at": "2026-08-23T16:00:00Z",
        "evidence": "synthetic-conformance-evidence",
        "result": "fail",
    }
    recipe_path.write_text(
        json.dumps(failed_verification, indent=2) + "\n",
        encoding="utf-8",
        newline="",
    )
    result = _validate(cli, target, repo_root)
    assert result.returncode != 0
    assert "verification" in result.stderr.casefold()


def test_material_recipe_requires_resolvable_semantic_runbook(
    repo_root: Path, tmp_path: Path
) -> None:
    cli, target = _bootstrap(repo_root, tmp_path)
    runbooks = target / ".agent-coordination" / "runbooks"
    recipes = runbooks / "recipes"
    template = json.loads(
        (recipes / "RUNBOOK-RECIPE.template.json").read_text(encoding="utf-8")
    )

    material = _verified_recipe(template, recipe_id="remote.restart.synthetic.v1")
    material["operation_id"] = "remote.service.restart"
    material["runbook_id"] = "service.restart"
    material["runbook_step"] = "restart"
    material["adapter"] = {
        "family": "ssh",
        "tool": "openssh-client",
        "version": "synthetic-verified-version",
        "platform": "synthetic",
        "shell": "bash",
    }
    material["binding"] = {
        "target_class": "remote-development-host",
        "resource_scope": "named development service",
        "privilege": "service-operator",
        "credential_class": "approved-ssh-agent",
        "network_scope": ["named-development-host"],
    }
    material["effect_classes"] = ["NETWORK_CONNECT", "REMOTE_EXECUTE"]
    material["invocation"] = {
        "kind": "remote",
        "template": "<parameterized remote service restart adapter operation>",
    }
    material["authoritative_sources"] = [
        {
            "source_class": "official_docs",
            "reference": "https://man.openbsd.org/ssh_config",
            "version": "synthetic-verified-version",
        }
    ]
    material["preconditions"] = [
        "remote host identity and authenticated principal match the runbook target"
    ]
    material["postconditions"] = ["named development service is healthy after restart"]

    recipe_path = recipes / "remote-restart.json"
    recipe_path.write_text(
        json.dumps(material, indent=2) + "\n", encoding="utf-8", newline=""
    )

    result = _validate(cli, target, repo_root)
    assert result.returncode != 0
    assert "runbook" in result.stderr.casefold()

    semantic_runbook = runbooks / "service.restart.md"
    semantic_runbook.write_text(
        "# Runbook\n\n"
        "Runbook-ID: `service.restart`\n"
        "Status: `ACTIVE`\n"
        "Revision: `synthetic-v1`\n"
        "Owner: `strategy`\n\n"
        "## Semantic steps\n\n"
        "### Step `restart` — restart the named development service\n",
        encoding="utf-8",
        newline="",
    )
    result = _validate(cli, target, repo_root)
    assert result.returncode == 0, result.stderr

    semantic_runbook.write_text(
        semantic_runbook.read_text(encoding="utf-8").replace(
            "Runbook-ID: `service.restart`", "Runbook-ID: `different.runbook`"
        ),
        encoding="utf-8",
        newline="",
    )
    result = _validate(cli, target, repo_root)
    assert result.returncode != 0
    assert "runbook" in result.stderr.casefold()


def test_recipe_registry_rejects_unknown_fields_states_and_duplicate_verified_bindings(
    repo_root: Path, tmp_path: Path
) -> None:
    cli, target = _bootstrap(repo_root, tmp_path)
    recipes = target / ".agent-coordination" / "runbooks" / "recipes"
    template = json.loads(
        (recipes / "RUNBOOK-RECIPE.template.json").read_text(encoding="utf-8")
    )
    first = _verified_recipe(template, recipe_id="git.status.first.v1")
    first_path = recipes / "first.json"
    first_path.write_text(json.dumps(first, indent=2) + "\n", encoding="utf-8", newline="")
    result = _validate(cli, target, repo_root)
    assert result.returncode == 0, result.stderr

    unknown_state = copy.deepcopy(first)
    unknown_state["recipe_id"] = "git.status.unknown-state.v1"
    unknown_state["status"] = "TRUST_ME"
    invalid_path = recipes / "invalid.json"
    invalid_path.write_text(
        json.dumps(unknown_state, indent=2) + "\n", encoding="utf-8", newline=""
    )
    result = _validate(cli, target, repo_root)
    assert result.returncode != 0
    assert "status" in result.stderr.casefold()
    invalid_path.unlink()

    unknown_field = copy.deepcopy(first)
    unknown_field["recipe_id"] = "git.status.unknown-field.v1"
    unknown_field["credential_value"] = "must-never-be-accepted"
    invalid_path.write_text(
        json.dumps(unknown_field, indent=2) + "\n", encoding="utf-8", newline=""
    )
    result = _validate(cli, target, repo_root)
    assert result.returncode != 0
    assert "field" in result.stderr.casefold() or "unexpected" in result.stderr.casefold()
    invalid_path.unlink()

    duplicate_binding = _verified_recipe(template, recipe_id="git.status.second.v1")
    invalid_path.write_text(
        json.dumps(duplicate_binding, indent=2) + "\n",
        encoding="utf-8",
        newline="",
    )
    result = _validate(cli, target, repo_root)
    assert result.returncode != 0
    assert "duplicate" in result.stderr.casefold() or "ambiguous" in result.stderr.casefold()
