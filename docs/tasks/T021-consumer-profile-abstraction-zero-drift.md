# T021 — Consumer Profile Abstraction Zero Drift

## Identity

- Task ID: `T021`
- Status: `BLOCKED`
- Type: `refactor`
- Base branch: `develop`
- Expected topic branch: `refactor/t021-consumer-profile-abstraction`
- Expected executor handoff: `handoffs/T021-executor-handoff.json`
- Readiness note: Remains `BLOCKED` until T020 is ACCEPTED.

## Objective

Introduce an explicit runtime profile abstraction with `consumer` as the only active profile, without changing Consumer v1 behavior. This creates the profile boundary required for later source-maintainer support while remaining a behavior-preserving refactor.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- `docs/REFACTORING-WORKFLOW.md`
- `docs/GOVERNANCE-SKILL-CONTRACT.md`

## Authorized scope

- Non-Markdown profile/runtime modules and routing code.
- Non-Markdown tests proving `consumer` profile behavior and isolation defaults.
- The thin launcher/build plumbing necessary to pass an explicit or resolved consumer profile.
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Unrelated provider/model routing, host configuration, permissions, Gentle AI/Caveman integration, or release promotion.
- Direct writes to `develop` or `main`.
- Source-maintainer profile implementation.
- Changes to Skill Markdown activation/description.
- Changes to consumer CLI commands or repository footprint.

## Invariants / constraints

- The T018 Consumer v1 characterization remains the behavioral baseline.
- `consumer` is an implementation profile, not a new normative authority.
- No profile default may grant source-maintenance permissions.
- The built artifact remains self-contained.

## Acceptance criteria

- Consumer behavior is identical with the profile abstraction enabled.
- Profile routing has a fail-closed default for unsupported/ambiguous profile values.
- All Consumer v1, artifact-isolation, and regression tests pass.

## Verification requirements

- Run T018 characterization unchanged.
- Run focused profile routing/isolation tests.
- Run T020 artifact-isolation tests and the full deterministic suite.

## Stop / escalation conditions

- Profile abstraction requires changing the Consumer Skill contract or activation semantics.
- An ambiguous context would be routed with broader permissions rather than fail closed.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T021-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push all authorized non-Markdown work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
