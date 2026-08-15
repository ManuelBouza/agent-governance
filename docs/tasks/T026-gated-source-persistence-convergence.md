# T026 — Gated Source Persistence Convergence

## Identity

- Task ID: `T026`
- Status: `BLOCKED`
- Type: `mixed`
- Base branch: `develop`
- Expected topic branch: `feat/t026-source-persistence-convergence`
- Expected executor handoff: `handoffs/T026-executor-handoff.json`
- Readiness note: Intentionally `BLOCKED`; if the later decision selects the adapter steady state, ChatGPT changes this task to `CANCELLED`.

## Objective

Reserved migration task for live source persistence convergence only if T025 evidence and a subsequent accepted architecture/ownership decision authorize it. The task is intentionally not execution-ready; its final authorized scope must be revised and frozen after that decision.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- `docs/TASK-CONTRACTS.md`
- `docs/orchestrator/CHECKPOINT.md`
- `docs/TESTING-AND-EVALUATION.md`

## Authorized scope

- No executable mutation scope is authorized while this contract remains `BLOCKED`.
- If later authorized by a separate accepted decision, ChatGPT must revise this contract with exact non-Markdown executor scope after resolving any Markdown ownership changes through a prior Markdown policy gate.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Unrelated provider/model routing, host configuration, permissions, Gentle AI/Caveman integration, or release promotion.
- Direct writes to `develop` or `main`.
- Any live `.agent-coordination/` source migration before the required decision gate.
- Executor creation/editing of committed Markdown under current ownership policy.
- Treating identical persistence as mandatory for unified Skill/engine/distribution architecture.

## Invariants / constraints

- T026 is not on the critical path for unified Skill packaging.
- A valid decision outcome is to CANCEL T026 and retain the source-specific persistence adapter.
- Live source `governance-core/` must remain authoritative if migration is later approved.
- Historical audit records must remain preserved.

## Acceptance criteria

- No implementation is accepted under this draft scope.
- Before status can change to `READY`, T025 must be ACCEPTED and a separate decision must resolve persistence/ownership semantics.
- Any future READY revision must define transactional migration, dual-read/equivalence period, rollback, and exact write ownership.

## Verification requirements

- No executor launch while status is `BLOCKED`.
- Future verification requirements must be supplied in the post-decision contract revision.

## Stop / escalation conditions

- Any attempt to launch this task before the decision gate.
- The required ownership model remains unresolved.
- Migration would weaken auditability, Markdown ownership, or source lifecycle semantics.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T026-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push all authorized non-Markdown work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
