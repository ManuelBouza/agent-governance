# T017 — Consumer Governance remaining CLI v1 surfaces

Task ID: T017
Status: READY_AFTER_PLANNING_MERGE
Type: implementation
Base branch: `develop`
Expected executor handoff: `handoffs/T017-executor-handoff.json`

## Objective

Complete the stable Consumer Governance CLI v1 surface required by the approved package/release contracts by adding the currently missing deterministic subcommands:

- `state`
- `event`
- `skill`
- `ecosystem`
- `archive`

The existing accepted `bootstrap` and `validate` behavior must remain compatible.

## Required outcome

Implement the five missing subcommands in `governance-skill/scripts/governance.py` with deterministic behavior consistent with the current Governance Core and the approved Consumer Governance functional/package contracts.

The implementation must preserve these boundaries:

- scripts do not make strategic, approval, or authority decisions;
- read-only validation remains the default where applicable;
- explicit mutation is bounded and fail-closed;
- source-repository independence remains intact;
- no network/provider/model correctness dependency;
- no live consumer footprint in this source checkout outside disposable fixtures;
- coexistence preserves third-party managed surfaces and does not choose semantic authority winners;
- Skill discovery/audit logic distinguishes discovery source from canonical provenance and exact approval identity;
- state/event handling preserves protocol actor/event semantics, monotonic EXCHANGE history, dependency/transition invariants, and constant-size STATE behavior;
- archive preserves history and refuses unsafe unresolved active state unless the authoritative operation explicitly permits cancellation/closure.

## Ownership and scope

Executor owns implementation process and internal orchestration.

Executor MAY edit non-Markdown implementation/test/handoff files required to complete this Task, including:

- `governance-skill/scripts/governance.py`;
- focused test/eval files under `tests/` or `evals/`;
- non-Markdown package assets only if strictly required by the accepted v1 contracts;
- `handoffs/T017-executor-handoff.json`.

Executor MUST NOT edit committed Markdown, Governance Core semantics, final `governance-skill/SKILL.md`, Maintainer Skill state, unrelated runtime, dependencies/lockfiles/config unless a concrete implementation blocker makes such a change unavoidable. If an unavoidable change would exceed this contract, stop and report BLOCKED rather than expanding scope.

## Acceptance

Remote Git evidence must show only contract-authorized non-Markdown implementation/test/handoff changes.

The completed CLI parser must expose exactly the stable v1 command set:

```text
bootstrap
validate
state
event
skill
ecosystem
archive
```

Focused deterministic tests must cover the new command surfaces, including success and fail-closed cases for malformed/unsafe state, event/history violations, Skill approval/provenance mismatch, coexistence conflict/preservation behavior, and archival safety.

Required repository gates:

```text
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
git diff --check
```

No production/external service, live model/provider judgment, or live consumer source-checkout footprint may be required for correctness.

The handoff must record executor identity, exact base SHA, implementation anchor SHA, changed paths, command surface, focused/full verification, dependency/config changes, limitations, and unresolved issues.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
TASK: T017
BRANCH: <implementation-branch>
BASE_SHA: <exact-base-sha>
HEAD_SHA: <exact-head-sha>
HANDOFF: handoffs/T017-executor-handoff.json
CLI_SURFACE: PASS | FAIL | NOT_RUN
FULL_PYTEST: PASS | FAIL | NOT_RUN
RUFF_CHECK: PASS | FAIL | NOT_RUN
RUFF_FORMAT: PASS | FAIL | NOT_RUN
```
