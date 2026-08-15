# T018 — Consumer V1 Characterization And Package Baseline

## Identity

- Task ID: `T018`
- Status: `READY`
- Type: `test/eval`
- Base branch: `develop`
- Expected topic branch: `test/t018-consumer-v1-characterization`
- Expected executor handoff: `handoffs/T018-executor-handoff.json`
- Readiness note: Execution is allowed only after MG0 is integrated into `develop`; `READY` does not bypass the contract integration gate.

## Objective

Freeze the release-approved Consumer Governance v1 observable behavior and characterize the current package boundary before any structural runtime refactor. The result must provide a durable RF1-compatible baseline for T019 and explicit evidence of the current sibling-Core packaging dependency without intentionally leaving the canonical suite red.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- `docs/REFACTORING-WORKFLOW.md`
- `docs/GOVERNANCE-SKILL-CONTRACT.md`
- `governance-skill/SKILL.md`
- `governance-skill/scripts/governance.py`
- `docs/CONSUMER-GOVERNANCE-SKILL-V1-RELEASE-GATE.md`

## Authorized scope

- Non-Markdown characterization/regression tests under `tests/`.
- Non-Markdown fixtures/helpers required only to freeze current Consumer v1 behavior and package-boundary assumptions.
- The executor handoff JSON for this task.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Unrelated provider/model routing, host configuration, permissions, Gentle AI/Caveman integration, or release promotion.
- Direct writes to `develop` or `main`.
- Any extraction/move of runtime implementation.
- Any new profile behavior, source-maintainer behavior, distribution wrapper, or CLI command.

## Invariants / constraints

- The stable Consumer v1 CLI remains exactly the current seven commands.
- Existing source/consumer behavior is observed, not changed.
- The known sibling `governance-core/` lookup is characterized as current behavior; the task must not silently fix it.
- All pre-existing release-approved tests remain valid.

## Acceptance criteria

- Characterization covers command availability, representative success/failure/exit behavior, bootstrap footprint, validation, state/event/skill/ecosystem/archive behavior, and package path resolution at the level needed to detect structural drift.
- The package-boundary characterization explicitly proves that the current source layout expects a sibling Core or equivalent source-bundle arrangement.
- The full existing deterministic suite remains green.
- T018 evidence is sufficient for ChatGPT to freeze RF1 before T019 starts.

## Verification requirements

- Run the focused T018 characterization tests.
- Run the full deterministic regression suite required by current repository policy.
- Report exact test counts/results and any baseline artifacts/fixtures created.

## Stop / escalation conditions

- A characterization test reveals an already-existing behavior conflict with the accepted Consumer v1 release gate.
- Freezing current behavior would require changing production runtime or protocol semantics.
- The current remote `develop` baseline cannot be established safely.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T018-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push all authorized non-Markdown work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
