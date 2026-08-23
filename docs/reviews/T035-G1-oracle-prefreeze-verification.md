# T035-G1 — Oracle pre-freeze technical verification

Status: `READY_FOR_EXECUTOR_VERIFICATION`  
Task: `T035`  
Gate type: `D052 oracle pre-freeze verification`  
Authority: ChatGPT Orchestrator  
Oracle branch: `test/t035-runbook-conformance-oracle`  
Canonical baseline: `develop@219904a352785d49dabe4f688d5cc65bde3dd547`  
Oracle authoring commit: `9ddf7afde88663677ee1f3b6d5258b07e00c92ba`  
Oracle asset: `tests/test_t035_runbook_operation_resolution_conformance.py`

## Purpose

Verify the Orchestrator-owned T035 conformance oracle mechanically before it is frozen and integrated. This gate does not authorize T035 implementation or any repository mutation by the Executor.

The expected state is intentionally RED against the pre-T035 runtime. PASS for this gate means that the oracle itself is mechanically valid and that its failures are attributable only to the T035 capabilities that have not yet been implemented.

## Controlling references

- `AGENTS.md`
- `docs/tasks/T035-runbook-operation-resolution-readiness.md`
- `docs/CONFORMANCE-ORACLE-CONTRACT.md`
- `docs/RUNBOOK-OPERATION-RESOLUTION.md`
- `docs/runbooks/RB001-source-executor-checkout-bootstrap.md`

## Authorized Executor activity

Read-only technical verification only.

The Executor SHALL:

1. establish the exact oracle branch safely under D054/RB001;
2. verify that the branch is based on the stated canonical baseline and contains no unrelated drift;
3. verify that the oracle file is syntactically collectible by pytest;
4. run repository Ruff lint against the oracle/current branch;
5. run repository Ruff format-check against the oracle/current branch;
6. execute only the T035 oracle against the pre-T035 runtime;
7. classify the resulting RED state as expected only when failures arise from absent T035 capabilities;
8. verify that the worktree remains clean after verification.

The Executor SHALL NOT:

- implement T035;
- edit, fix, reformat or otherwise mutate the oracle;
- edit any tracked repository file;
- create the T035 implementation branch;
- create an Executor handoff for T035 implementation;
- change Markdown;
- weaken, reinterpret or modify oracle semantics;
- repair an unexpected oracle defect.

## Expected preimplementation semantic absences

Failures are expected when they are caused by capabilities T035 has not yet implemented, including:

- native `.agent-coordination/runbooks/` and `runbooks/recipes/` bootstrap footprint;
- `RUNBOOK-RECIPE.template.json` materialization;
- deterministic recipe schema/trust validation;
- VERIFIED provenance/postcondition/staleness requirements;
- material-effect runbook binding validation;
- duplicate/supersession/unsafe-path recipe controls.

These expected absences are not oracle defects.

## Unexpected defect classes

Return `BLOCKED` without repair if failure is instead caused by any oracle-side mechanical defect, including:

- Python syntax/import error;
- pytest collection/fixture defect;
- incorrect path/reference in the oracle;
- timeout caused by oracle mechanics rather than product behavior;
- accidental host/platform dependency contrary to the Task Contract;
- Ruff lint/format failure in the oracle itself;
- unrelated branch drift;
- any other defect that prevents the oracle from expressing the approved semantics mechanically.

Do not reinterpret semantic assertions. A suspected semantic contradiction is an `ORACLE_DEFECT`-equivalent and returns to the Orchestrator.

## Execution mechanics

All Git, uv, PowerShell and equivalent command/API mechanics belong to the Executor under D054. Use RB001 and authoritative installed/version-specific help or official vendor documentation as required. Do not delegate routine command execution to the Human Owner.

## Acceptance

Gate PASS requires all of the following:

```text
branch identity/drift      = PASS
Ruff lint                  = PASS
Ruff format-check          = PASS
pytest collection          = PASS
oracle execution           = RED only for expected missing T035 behavior
worktree after verification = CLEAN
```

This gate does not freeze the oracle. Only the Orchestrator may mark `T035-D054-v1` FROZEN after reviewing this evidence.

## Required Executor return

Return only:

```text
STATUS: PASS | BLOCKED
BRANCH: <verified branch>
HEAD: <verified HEAD>
DIFF-SCOPE: <PASS or concise deviation>
RUFF-CHECK: <PASS or concise failure>
RUFF-FORMAT: <PASS or concise failure>
PYTEST-COLLECTION: <PASS or concise failure>
ORACLE-RED: <EXPECTED or concise unexpected defect>
WORKTREE: <CLEAN or concise status>
```
