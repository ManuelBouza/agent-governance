# T028 — Retire Obsolete Two Skill Structural Assumptions

## Identity

- Task ID: `T028`
- Status: `BLOCKED`
- Type: `refactor`
- Base branch: `develop`
- Expected topic branch: `refactor/t028-retire-two-skill-assumptions`
- Expected executor handoff: `handoffs/T028-executor-handoff.json`
- Readiness note: Remains `BLOCKED` until T023 and T024 are ACCEPTED; MG3 occurs after this executable cleanup is accepted.

## Objective

Remove obsolete non-Markdown implementation/test assumptions whose only purpose is enforcing independently maintained Consumer and Maintainer Skill source trees, while replacing them with invariants that protect profile isolation, source-state exclusion, and artifact self-containment. Markdown retirement remains MG3-owned.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- `tests/test_source_consumer_separation.py`
- `docs/TESTING-AND-EVALUATION.md`
- `docs/GOVERNANCE-SKILL-PACKAGE.md`

## Authorized scope

- Non-Markdown tests that currently encode physical two-Skill directory separation.
- Non-Markdown packaging/runtime remnants made obsolete by accepted unified profile architecture.
- Replacement non-Markdown tests for source-state exclusion, profile isolation, live-Core protection, and artifact boundary.
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Unrelated provider/model routing, host configuration, permissions, Gentle AI/Caveman integration, or release promotion.
- Direct writes to `develop` or `main`.
- Deleting/editing `maintainer-skill/STATUS.md`, D017, package/testing/release Markdown, or any other Markdown; those are MG3.
- Removing an invariant before the replacement test is in place and passing.
- Deleting historical evidence.

## Invariants / constraints

- D017 safety rationale remains protected even though physical two-product layout is retired.
- Source state must never leak into consumer distribution.
- Source-maintainer must never replace live source Core with the bundled consumer snapshot.
- Consumer must never gain source-maintainer permissions.

## Acceptance criteria

- Tests no longer require two independently maintained Skill source directories merely as a structural invariant.
- Replacement tests mechanically protect the D044 isolation and distribution invariants.
- All accepted consumer/profile/package/upgrade behavior remains green.

## Verification requirements

- Run updated separation/isolation tests.
- Run T018 characterization, profile, artifact, wrapper, and upgrade regression suites.
- Run the full deterministic suite.

## Stop / escalation conditions

- MG3-owned Markdown would have to be edited to make the non-Markdown test change pass.
- A proposed removal eliminates a safety invariant without an equivalent stronger replacement.
- T023 routing or T024 packaging is not yet accepted.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T028-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push all authorized non-Markdown work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
