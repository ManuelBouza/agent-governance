# T035-G1 — Oracle pre-freeze technical verification

Status: `REWORK_READY_FOR_EXECUTOR_VERIFICATION`  
Task: `T035`  
Gate type: `D052 oracle pre-freeze verification`  
Authority: ChatGPT Orchestrator  
Oracle branch: `test/t035-runbook-conformance-oracle`  
Canonical baseline: current remote `develop` at execution time  
Initial oracle authoring commit: `9ddf7afde88663677ee1f3b6d5258b07e00c92ba`  
First verification HEAD: `bdfae9967394e8de9888d9e84e2be02513ba0f78`  
Oracle asset: `tests/test_t035_runbook_operation_resolution_conformance.py`

## Purpose

Mechanically verify and, only where explicitly authorized below, mechanically normalize the Orchestrator-owned T035 conformance oracle before it is frozen and integrated.

The expected state is intentionally RED against the pre-T035 runtime. PASS for this gate means that the oracle itself is mechanically valid and that its failures are attributable only to T035 capabilities that have not yet been implemented.

The first verification returned `BLOCKED` solely because Ruff reported import ordering and formatting drift. Pytest collection passed, the oracle RED state was expected, and tracked content remained clean. This rework authorizes only the bounded mechanical correction required to clear that defect.

## Controlling references

- `AGENTS.md`
- `docs/tasks/T035-runbook-operation-resolution-readiness.md`
- `docs/CONFORMANCE-ORACLE-CONTRACT.md`
- `docs/RUNBOOK-OPERATION-RESOLUTION.md`
- `docs/decisions/D042-remote-baseline-freshness-before-contract-load.md`
- `docs/runbooks/RB001-source-executor-checkout-bootstrap.md`

## Required remote freshness

Before loading repository instructions or this gate for execution, synchronize with GitHub and establish the current canonical remote `develop` identity under D042/RB001.

Continue on the represented oracle branch and reconcile current `develop` into it safely. Preserve represented branch history and any unrepresented local work. Do not reset, clean, recreate, force-push or discard work merely to make reconciliation convenient. If safe reconciliation is not possible, return `BLOCKED`.

## Authorized Executor activity

The Executor SHALL:

1. synchronize the canonical GitHub remote and establish current remote `develop`;
2. safely reconcile current `develop` into `test/t035-runbook-conformance-oracle` without represented-history rewrite;
3. reload current repository instructions from the reconciled state when required by D043;
4. apply only repository-native Ruff mechanical corrections to `tests/test_t035_runbook_operation_resolution_conformance.py` necessary to clear import ordering and formatter checks;
5. verify that the semantic oracle delta is unchanged: no assertion meaning, contractual constants, case membership, expected outcome, negative-control intent, fixture semantics or acceptance boundary may change;
6. verify pytest collection;
7. run repository Ruff lint and Ruff format-check;
8. execute only the T035 oracle against the pre-T035 runtime;
9. classify RED as expected only when failures arise from absent T035 capabilities;
10. commit and push the bounded authorized mechanical correction/reconciliation to the represented oracle branch;
11. verify the resulting tracked worktree is clean.

## Mechanical correction boundary

Authorized changes to the oracle are limited to semantics-preserving transformations produced or required by the repository's configured Ruff tooling, such as:

- import ordering;
- whitespace/blank-line normalization;
- line wrapping;
- parenthesization or equivalent formatter-only syntax normalization;
- other Ruff autofix/format transformations that provably preserve Python behavior and oracle acceptance meaning.

The Executor MUST NOT change:

- assertion expressions or expected values except formatter-only syntactic normalization;
- `RECIPE_FIELDS`, `ADAPTER_FIELDS`, `BINDING_FIELDS`, `RECIPE_STATES`, `SOURCE_CLASSES`, `MATERIAL_EFFECTS` or `CLI_V1` membership/values;
- required test functions/case membership;
- recipe/runbook fixtures in a way that changes the condition being tested;
- expected PASS/FAIL classification;
- negative-control intent;
- semantic comments/docstrings in a way that reinterprets authority;
- any other tracked source/test/Markdown file except the unavoidable branch reconciliation of already-canonical `develop` commits.

If Ruff cannot be satisfied within this boundary, return `BLOCKED` and identify the exact mechanical/semantic conflict.

## Expected preimplementation semantic absences

Failures are expected when caused by capabilities T035 has not yet implemented, including:

- native `.agent-coordination/runbooks/` and `runbooks/recipes/` bootstrap footprint;
- `RUNBOOK-RECIPE.template.json` materialization;
- deterministic recipe schema/trust validation;
- VERIFIED provenance/postcondition/staleness requirements;
- material-effect runbook binding validation;
- duplicate/supersession/unsafe-path recipe controls.

These expected absences are not oracle defects.

## Unexpected defect classes

Return `BLOCKED` without semantic repair if failure is caused by:

- Python syntax/import or pytest collection/fixture defect not mechanically repairable within the Ruff boundary;
- incorrect semantic path/reference in the oracle;
- timeout caused by oracle mechanics rather than product behavior;
- accidental host/platform dependency contrary to the Task Contract;
- unrelated branch drift;
- any required semantic change to make the oracle pass tooling;
- any contradiction between the oracle and controlling specification.

A suspected semantic contradiction is an `ORACLE_DEFECT`-equivalent and returns to the Orchestrator.

## Execution mechanics

All Git, uv, PowerShell and equivalent command/API mechanics belong to the Executor under D054. Use RB001 and authoritative installed/version-specific help or official vendor documentation as required. Do not delegate routine command execution to the Human Owner.

The untracked `.worktrees/` administrative directory observed during the first verification is not itself a semantic oracle defect. It must not be committed. Preserve it unless the Executor can prove it is invocation-owned disposable state and cleanup is authorized; otherwise simply report its presence separately from tracked cleanliness.

## Acceptance

Gate PASS requires:

```text
current remote freshness       = PASS
represented branch reconcile   = PASS
semantic oracle delta          = UNCHANGED
Ruff lint                      = PASS
Ruff format-check              = PASS
pytest collection              = PASS
oracle execution               = RED only for expected missing T035 behavior
tracked worktree after push    = CLEAN
```

This gate does not freeze the oracle. Only the Orchestrator may mark `T035-D054-v1` FROZEN after reviewing this evidence.

## Required Executor return

Return only:

```text
STATUS: PASS | BLOCKED
BRANCH: <verified branch>
HEAD: <pushed HEAD>
REMOTE-DEVELOP: <current verified origin/develop SHA>
RECONCILE: <PASS or concise blocker>
SEMANTIC-DELTA: UNCHANGED | <concise blocker>
RUFF-CHECK: <PASS or concise failure>
RUFF-FORMAT: <PASS or concise failure>
PYTEST-COLLECTION: <PASS or concise failure>
ORACLE-RED: <EXPECTED or concise unexpected defect>
WORKTREE: <TRACKED-CLEAN plus concise untracked status>
```
