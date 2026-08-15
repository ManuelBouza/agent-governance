# T024 — Generated Platform Distribution Wrappers

## Identity

- Task ID: `T024`
- Status: `BLOCKED`
- Type: `infrastructure`
- Base branch: `develop`
- Expected topic branch: `feat/t024-governance-distribution-wrappers`
- Expected executor handoff: `handoffs/T024-executor-handoff.json`
- Readiness note: Remains `BLOCKED` until T023 is ACCEPTED.

## Objective

Generate and verify platform distribution wrapper(s) from the accepted self-contained canonical Skill payload. Wrappers must add packaging metadata only and must not fork Governance behavior, Core authority, profile contracts, or runtime implementation.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- `docs/RELEASES.md`
- `docs/GOVERNANCE-SKILL-PACKAGE.md`

## Authorized scope

- Non-Markdown platform manifest/config generation.
- Non-Markdown packaging/validation code and tests.
- Generated wrapper artifacts in ignored/temporary build output as appropriate.
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Unrelated provider/model routing, host configuration, permissions, Gentle AI/Caveman integration, or release promotion.
- Direct writes to `develop` or `main`.
- Manual maintenance of generated distribution copies.
- Publishing/tagging/releasing to `main` or an external directory/store.
- Platform-specific forks of protocol or deterministic engine behavior.

## Invariants / constraints

- One canonical Skill payload remains the source for every wrapper.
- Wrapper-specific metadata is subordinate packaging evidence, not Governance authority.
- The emitted payload remains self-contained and contains no source-maintenance state/history.
- If T023 selected thin entrypoint fallback, both entrypoints are generated from the same profiles/runtime/Core snapshot.

## Acceptance criteria

- At least the current target platform wrapper and standalone Skill payload can be generated reproducibly from canonical source.
- Structural/package validation passes for each supported wrapper.
- Artifact-only bootstrap/validate remains green after wrapping.
- No wrapper contains unexpected source-only files or references outside its package root.

## Verification requirements

- Run focused wrapper/package validation tests.
- Run artifact isolation tests for each release-target wrapper.
- Verify manifest/release identity agrees with T020 generated metadata.

## Stop / escalation conditions

- Platform packaging requirements would force behavior/protocol duplication.
- Required wrapper metadata cannot be generated without making a platform file an authority source.
- T023 routing outcome is unresolved.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T024-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push all authorized non-Markdown work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
