"""Executor-owned branch coverage for native runbook recipe validation."""

from __future__ import annotations

import copy
import importlib.util
import json
from collections.abc import Callable
from pathlib import Path

import pytest


def load_engine(repo_root: Path):
    path = repo_root / "src" / "agent_governance" / "engine.py"
    spec = importlib.util.spec_from_file_location("runbook_recipe_engine", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_template(repo_root: Path) -> dict[str, object]:
    return json.loads(
        (repo_root / "governance-skill" / "assets" / "RUNBOOK-RECIPE.template.json").read_text(
            encoding="utf-8"
        )
    )


def verified_recipe(repo_root: Path) -> dict[str, object]:
    recipe = source_template(repo_root)
    recipe.update(
        {
            "recipe_id": "recipe.observe",
            "status": "VERIFIED",
            "operation_id": "observe",
            "adapter": {
                "family": "cli",
                "tool": "tool",
                "version": "1.0.0",
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
            "invocation": {"kind": "argv", "template": ["tool", "status"]},
            "authoritative_sources": [
                {
                    "source_class": "builtin_help",
                    "reference": "tool help status",
                    "version": "1.0.0",
                }
            ],
            "preconditions": ["repository exists"],
            "postconditions": ["repository was observed"],
            "verification": {
                "verified_at": "2026-08-23T18:00:00Z",
                "evidence": "handoff#observe",
                "result": "pass",
            },
            "stale_triggers": ["adapter_version_drift", "failed_postcondition_or_replay"],
        }
    )
    return recipe


def mutate(recipe: dict[str, object], operation: Callable[[dict[str, object]], None]):
    candidate = copy.deepcopy(recipe)
    operation(candidate)
    return candidate


def test_recipe_record_rejects_every_structural_and_trust_failure_branch(
    repo_root: Path, tmp_path: Path
) -> None:
    engine = load_engine(repo_root)
    recipe = verified_recipe(repo_root)
    source = tmp_path / "recipe.json"
    engine._validate_recipe_record(recipe, source)

    failures = [
        lambda item: item.update({"unknown": True}),
        lambda item: item.update(recipe_id=""),
        lambda item: item.update(operation_id=""),
        lambda item: item.update(status="TRUSTED"),
        lambda item: item.update(adapter={**item["adapter"], "unknown": True}),
        lambda item: item["adapter"].update(family="terminal"),
        lambda item: item["adapter"].update(tool=""),
        lambda item: item["adapter"].update(shell=""),
        lambda item: item.update(binding={**item["binding"], "unknown": True}),
        lambda item: item["binding"].update(target_class=""),
        lambda item: item["binding"].update(network_scope=[1]),
        lambda item: item.update(effect_classes=[]),
        lambda item: item.update(effect_classes=["OBSERVE", "OBSERVE"]),
        lambda item: item.update(effect_classes=["UNKNOWN"]),
        lambda item: item.update(invocation={"kind": "argv"}),
        lambda item: item["invocation"].update(kind="command"),
        lambda item: item["invocation"].update(template=[]),
        lambda item: item.update(invocation={"kind": "shell", "template": ""}),
        lambda item: item.update(invocation={"kind": "api", "template": {}}),
        lambda item: item.update(authoritative_sources=[]),
        lambda item: item.update(authoritative_sources=[{"source_class": "builtin_help"}]),
        lambda item: item["authoritative_sources"][0].update(source_class="community"),
        lambda item: item["authoritative_sources"][0].update(reference=""),
        lambda item: item["authoritative_sources"][0].update(version=""),
        lambda item: item.update(preconditions=[1]),
        lambda item: item.update(effect_classes=["MUTATE_SCOPED"], preconditions=[]),
        lambda item: item.update(postconditions=[""]),
        lambda item: item.update(stale_triggers="adapter_version_drift"),
        lambda item: item.update(preview=[]),
        lambda item: item.update(verification={"result": "pass"}),
        lambda item: item["verification"].update(verified_at="yesterday"),
        lambda item: item["verification"].update(verified_at="20260823T180000+00:00"),
        lambda item: item["verification"].update(evidence=""),
        lambda item: item["verification"].update(result="unknown"),
        lambda item: item.update(runbook_id=""),
        lambda item: item.update(runbook_id="rb", runbook_step=None),
        lambda item: item.update(status="SUPERSEDED", supersedes=None),
        lambda item: item.update(postconditions=[]),
        lambda item: item.update(verification=None),
        lambda item: item["authoritative_sources"][0].update(version="2.0.0"),
        lambda item: item.update(stale_triggers=["failed_postcondition_or_replay"]),
        lambda item: item.update(stale_triggers=["adapter_version_drift"]),
        lambda item: item["invocation"].update(credential_value="secret"),
        lambda item: item["invocation"].update(**{"secret-value": "secret"}),
        lambda item: item["authoritative_sources"][0].update(secret="secret"),
    ]
    for operation in failures:
        with pytest.raises(engine.GovernanceError):
            engine._validate_recipe_record(mutate(recipe, operation), source)


@pytest.mark.parametrize(
    ("kind", "template"),
    [
        ("argv", ["tool", "status"]),
        ("shell", "tool status"),
        ("api", {"operation": "status"}),
        ("sdk", {"operation": "status"}),
        ("remote", {"operation": "status"}),
    ],
)
def test_recipe_record_accepts_each_invocation_kind_and_preview_shape(
    repo_root: Path, tmp_path: Path, kind: str, template: object
) -> None:
    engine = load_engine(repo_root)
    for preview in (None, "tool plan", {"operation": "plan"}, ["tool", "plan"]):
        recipe = verified_recipe(repo_root)
        recipe["invocation"] = {"kind": kind, "template": template}
        recipe["preview"] = preview
        engine._validate_recipe_record(recipe, tmp_path / "recipe.json")


def write_runbook(path: Path, *, runbook_id: str = "rb.one", step: str = "execute") -> None:
    path.write_text(
        f"""# Runbook

Runbook-ID: `{runbook_id}`
Status: `ACTIVE`
Revision: `v1`
Owner: `strategy`

### Step `{step}` — execute
""",
        encoding="utf-8",
    )


def stage_registry(repo_root: Path, tmp_path: Path) -> tuple[Path, Path, Path]:
    coordination = tmp_path / ".agent-coordination"
    runbooks = coordination / "runbooks"
    recipes = runbooks / "recipes"
    recipes.mkdir(parents=True)
    (runbooks / "RUNBOOK.template.md").write_bytes(
        (repo_root / "governance-skill" / "assets" / "RUNBOOK.template.md").read_bytes()
    )
    (recipes / "RUNBOOK-RECIPE.template.json").write_text(
        json.dumps(source_template(repo_root)), encoding="utf-8"
    )
    return coordination, runbooks, recipes


def test_registry_validates_runbook_metadata_steps_and_references(
    repo_root: Path, tmp_path: Path
) -> None:
    engine = load_engine(repo_root)
    coordination, runbooks, recipes = stage_registry(repo_root, tmp_path)
    write_runbook(runbooks / "rb.one.md")
    recipe = verified_recipe(repo_root)
    recipe.update(runbook_id="rb.one", runbook_step="execute")
    (recipes / "observe.json").write_text(json.dumps(recipe), encoding="utf-8")
    engine._validate_runbook_registry(coordination)

    recipe["runbook_step"] = "missing"
    (recipes / "observe.json").write_text(json.dumps(recipe), encoding="utf-8")
    with pytest.raises(engine.GovernanceError, match="unresolved"):
        engine._validate_runbook_registry(coordination)


def test_registry_rejects_invalid_layout_metadata_and_supersession(
    repo_root: Path, tmp_path: Path
) -> None:
    engine = load_engine(repo_root)

    coordination, runbooks, recipes = stage_registry(repo_root, tmp_path / "layout")
    (recipes / "unexpected.txt").write_text("unexpected", encoding="utf-8")
    with pytest.raises(engine.GovernanceError, match="unexpected or unsafe native recipe"):
        engine._validate_runbook_registry(coordination)

    coordination, runbooks, _recipes = stage_registry(repo_root, tmp_path / "runbook-layout")
    (runbooks / "unexpected.txt").write_text("unexpected", encoding="utf-8")
    with pytest.raises(engine.GovernanceError, match="unexpected or unsafe native runbook"):
        engine._validate_runbook_registry(coordination)

    coordination, runbooks, _recipes = stage_registry(repo_root, tmp_path / "metadata")
    (runbooks / "bad.md").write_text(
        "Runbook-ID: `rb.bad`\nStatus: `INVALID`\nRevision: `v1`\nOwner: `strategy`\n",
        encoding="utf-8",
    )
    with pytest.raises(engine.GovernanceError, match="metadata is invalid"):
        engine._validate_runbook_registry(coordination)

    coordination, runbooks, _recipes = stage_registry(repo_root, tmp_path / "duplicates")
    write_runbook(runbooks / "first.md")
    write_runbook(runbooks / "second.md")
    with pytest.raises(engine.GovernanceError, match="duplicate native Runbook-ID"):
        engine._validate_runbook_registry(coordination)

    coordination, runbooks, _recipes = stage_registry(repo_root, tmp_path / "steps")
    path = runbooks / "steps.md"
    write_runbook(path)
    path.write_text(
        path.read_text(encoding="utf-8") + "\n### Step `execute` — again\n", encoding="utf-8"
    )
    with pytest.raises(engine.GovernanceError, match="duplicate native runbook step"):
        engine._validate_runbook_registry(coordination)

    coordination, _runbooks, recipes = stage_registry(repo_root, tmp_path / "supersession")
    superseded = verified_recipe(repo_root)
    superseded.update(status="SUPERSEDED", supersedes="missing")
    (recipes / "superseded.json").write_text(json.dumps(superseded), encoding="utf-8")
    with pytest.raises(engine.GovernanceError, match="invalid recipe supersession"):
        engine._validate_runbook_registry(coordination)

    superseded["supersedes"] = superseded["recipe_id"]
    (recipes / "superseded.json").write_text(json.dumps(superseded), encoding="utf-8")
    with pytest.raises(engine.GovernanceError, match="invalid recipe supersession"):
        engine._validate_runbook_registry(coordination)


def test_validation_never_executes_recipe_content(repo_root: Path, tmp_path: Path) -> None:
    target = tmp_path / "consumer"
    target.mkdir()
    engine = load_engine(repo_root)
    core = repo_root / "governance-core"
    assets = repo_root / "governance-skill" / "assets"
    engine._bootstrap(target, (core, assets))

    sentinel = tmp_path / "must-not-exist"
    recipe = source_template(repo_root)
    recipe["recipe_id"] = "candidate.shell"
    recipe["operation_id"] = "candidate.shell"
    recipe["adapter"] = {
        "family": "powershell",
        "tool": "powershell",
        "version": "7",
        "platform": "windows",
        "shell": "powershell",
    }
    recipe["invocation"] = {
        "kind": "shell",
        "template": f"New-Item -ItemType File -Path {sentinel}",
    }
    path = target / ".agent-coordination" / "runbooks" / "recipes" / "candidate.json"
    path.write_text(json.dumps(recipe), encoding="utf-8")

    engine._validate(target)
    assert not sentinel.exists()
