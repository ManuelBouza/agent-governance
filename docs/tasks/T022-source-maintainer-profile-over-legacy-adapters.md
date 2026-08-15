# T022 — Source Maintainer Profile Over Legacy Adapters

## Identity

- Task ID: `T022`
- Status: `BLOCKED`
- Type: `feature`
- Base branch: `develop`
- Expected topic branch: `feat/t022-source-maintainer-profile`
- Expected executor handoff: `handoffs/T022-executor-handoff.json`
- Readiness note: Remains `BLOCKED` until T021 is ACCEPTED.

## Objective

Implement a `source-maintainer` runtime profile on the shared engine that operates over the source repository's existing maintenance records and policies through explicit adapters. It must enable shared engine semantics without creating a consumer installation or changing source persistence yet.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- `docs/MAINTAINER-SKILL-CONTRACT.md`
- `docs/DEVELOPMENT-WORKFLOW.md`
- `docs/REFACTORING-WORKFLOW.md`
- `docs/BRANCHING.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `docs/orchestrator/CHECKPOINT.md`

## Authorized scope

- Non-Markdown source-profile runtime/adapters.
- A non-Markdown explicit, versioned source-product identification mechanism and tests for it.
- Non-Markdown tests/fixtures for source profile routing, read/write boundaries, and legacy source-record adaptation.
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Unrelated provider/model routing, host configuration, permissions, Gentle AI/Caveman integration, or release promotion.
- Direct writes to `develop` or `main`.
- Creating live `.agent-governance/` or `.agent-coordination/` consumer state at the source repository root.
- Editing source Task Contract/checkpoint/review/release Markdown.
- Implementing a separate `maintainer-skill/SKILL.md`.
- Inferring source-product identity solely from directory names.

## Invariants / constraints

- Live source `governance-core/` remains the normative Core for the source-maintainer profile.
- Source Task Contracts, Markdown ownership, branching, release policy, and checkpoint semantics remain controlling overlays.
- Consumer and source-maintainer permission/mutation surfaces remain mutually isolated.
- The source profile must not overwrite live Core with a bundled consumer snapshot.

## Acceptance criteria

- The shared engine can resolve source-maintainer context only from the explicit source-product signal.
- Source-maintainer operations needed by the accepted maintainer contract can route to current source records/adapters without consumer-state initialization.
- Consumer profile tests remain unchanged and green.
- Cross-profile mutation-isolation tests pass.

## Verification requirements

- Run focused source-profile adapter tests.
- Run consumer/profile regression and artifact tests.
- Run the full deterministic regression suite.
- Provide evidence that no live consumer state was created in the source repository.

## Stop / escalation conditions

- Required source behavior cannot be represented without changing Markdown ownership or Task Contract semantics.
- Source/consumer context is ambiguous or profile identification cannot fail closed.
- Implementation would require a second independently maintained Skill runtime.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T022-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push all authorized non-Markdown work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
