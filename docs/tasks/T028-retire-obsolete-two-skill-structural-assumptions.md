# T028 — Retire Obsolete Independently Maintained Skill Product Assumptions

## Identity

- Task ID: `T028`
- Status: `BLOCKED`
- Type: `refactor`
- Base branch: `develop`
- Expected topic branch: `refactor/t028-retire-independent-skill-product-assumptions`
- Expected executor handoff: `handoffs/T028-executor-handoff.json`
- Readiness note: Remains `BLOCKED` until T023 and T024 are ACCEPTED; MG3 occurs after this executable cleanup is accepted.

## Objective

Remove obsolete non-Markdown implementation/test assumptions whose only purpose is enforcing **independently maintained** Consumer and Maintainer Skill source trees/products, while replacing them with invariants that protect profile isolation, source-state exclusion, artifact self-containment, canonical capability provenance and the exact T023-selected generated topology.

T028 does **not** require the release distribution to contain exactly one Skill entrypoint. If T023 selected multiple generated peer Skills under D050, those entrypoints are preserved as projections of one product/source. Markdown retirement remains MG3-owned.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/decisions/D050-canonical-capability-source-and-evaluated-skill-topology.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- accepted T023 topology review/evidence
- accepted T024 distribution/projection review/evidence
- `tests/test_source_consumer_separation.py`
- `docs/TESTING-AND-EVALUATION.md`
- `docs/GOVERNANCE-SKILL-PACKAGE.md`

## Authorized scope

- Non-Markdown tests that currently encode independently maintained two-Skill source/product separation as a physical invariant.
- Non-Markdown packaging/runtime remnants made obsolete by the accepted canonical-capability/selected-topology architecture.
- Replacement non-Markdown tests for source-state exclusion, profile isolation, canonical capability/Core/engine provenance, selected-topology fidelity and artifact boundary.
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Changing the topology selected by T023 or the build projection accepted in T024.
- Collapsing multiple generated entrypoints merely because historical wording used “unified Skill”.
- Creating or retaining independently editable Governance Skill authority/runtime forks.
- Introducing independent per-entrypoint product/version identities.
- Unrelated provider/model routing, host configuration, permissions, Gentle AI/Caveman integration, multi-agent architecture, or release promotion.
- Direct writes to `develop` or `main`.
- Deleting/editing `maintainer-skill/STATUS.md`, D017, package/testing/release Markdown, or any other Markdown; those are MG3.
- Removing an invariant before the replacement test is in place and passing.
- Deleting historical evidence.

## Invariants / constraints

- D017 safety rationale remains protected even though independently maintained two-product layout is retired.
- D050 permits one or multiple **generated** Skill entrypoints, but all remain projections of one canonical capability source/Core/engine/distribution identity.
- Source state must never leak into Consumer-capable distribution surfaces.
- Source-maintainer must never replace live source Core with the bundled Consumer snapshot.
- Consumer must never gain source-maintainer permissions.
- The selected topology must remain reproducible and source-independent according to T024 evidence.

## Acceptance criteria

### AC-T028-1 — obsolete independent-product assumptions retired
Tests/runtime/package logic no longer require separate independently maintained Consumer and Maintainer Skill source products merely as a structural invariant.

### AC-T028-2 — selected topology preserved
The exact T023/T024 accepted one- or multi-entrypoint topology remains intact; no generated peer Skill is removed solely to satisfy old “one Skill” wording.

### AC-T028-3 — canonical provenance protected
Replacement tests mechanically prove that every emitted entrypoint remains derived from the same accepted canonical capability source/Core/engine/distribution identity.

### AC-T028-4 — isolation preserved
Replacement tests protect Consumer/source-maintainer permission, mutation, source-state and live-Core boundaries at least as strongly as the retired structural tests.

### AC-T028-5 — regression
All accepted Consumer/profile/topology/package/upgrade behavior remains green.

## Verification requirements

- Run updated separation/isolation/provenance tests.
- Run T018 characterization, profile, T023 topology, T024 artifact/wrapper, and upgrade regression suites applicable at this stage.
- Run selected-topology reproducibility/fidelity checks.
- Run the full deterministic suite.
- Inspect diff proving no Markdown or unauthorized topology/product/version changes.
- Map every acceptance criterion to exact evidence in the handoff.

## Stop / escalation conditions

- MG3-owned Markdown would have to be edited to make the non-Markdown test change pass.
- A proposed removal eliminates a safety/provenance invariant without an equivalent stronger replacement.
- T023 routing/topology or T024 packaging is not yet accepted.
- Removing an old two-tree assumption would require collapsing an accepted multi-entrypoint topology.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T028-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, follow D048's normal-task publication boundary, commit/push all authorized work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
