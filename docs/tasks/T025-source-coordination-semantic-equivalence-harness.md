# T025 — Source Coordination Semantic Equivalence Harness

## Identity

- Task ID: `T025`
- Status: `BLOCKED`
- Type: `test/eval`
- Base branch: `develop`
- Expected topic branch: `test/t025-source-coordination-equivalence`
- Expected executor handoff: `handoffs/T025-executor-handoff.json`
- Readiness note: Remains `BLOCKED` until T022 is ACCEPTED. It may run independently of T023/T024 after that point.

## Objective

Build a deterministic, read-only/synthetic equivalence harness that maps current source-maintenance frontier semantics to the common coordination model. The task must identify both equivalent and non-equivalent semantics, especially Markdown ownership and source Task Contract lifecycle, before any live source persistence migration is authorized.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- `docs/orchestrator/CHECKPOINT.md`
- `docs/TASK-CONTRACTS.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `docs/TESTING-AND-EVALUATION.md`

## Authorized scope

- Non-Markdown equivalence/mapping code.
- Non-Markdown synthetic fixtures and result data; existing Markdown records may be read as fixtures but not edited.
- Tests comparing derived frontier/task/handoff/decision semantics.
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Unrelated provider/model routing, host configuration, permissions, Gentle AI/Caveman integration, or release promotion.
- Direct writes to `develop` or `main`.
- Creating or mutating live `.agent-coordination/` in the source repository.
- Rewriting historical source Task Contracts, checkpoints, handoffs, reviews, operations, or decisions.
- Changing Markdown ownership rules.

## Invariants / constraints

- The harness is observational/synthetic and cannot become a second source of authority.
- Differences are reported rather than normalized away.
- Committed Markdown ownership is treated as a first-class semantic constraint.
- The result must support an explicit later decision on T026 rather than presupposing migration.

## Acceptance criteria

- Defined common frontier semantics can be compared deterministically against representative current source-maintenance records.
- Equivalent mappings and material non-equivalences are enumerated in machine-readable evidence/handoff.
- Ownership/write-path conflicts are explicitly surfaced.
- No live source coordination footprint is created.

## Verification requirements

- Run focused equivalence tests across representative source states.
- Run regression tests ensuring the harness is read-only with respect to source records.
- Report mapping coverage, mismatches, and decision-relevant risks.

## Stop / escalation conditions

- The comparison requires writing/modifying committed Markdown.
- A semantic mismatch would need to be hidden or guessed to obtain equality.
- Representative source states cannot be evaluated without exposing private chat state.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T025-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push all authorized non-Markdown work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
