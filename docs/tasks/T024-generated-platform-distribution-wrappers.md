# T024 — Generated Platform Distribution Wrappers

## Identity

- Task ID: `T024`
- Status: `BLOCKED`
- Type: `infrastructure`
- Base branch: `develop`
- Expected topic branch: `feat/t024-governance-distribution-wrappers`
- Expected executor handoff: `handoffs/T024-executor-handoff.json`
- Readiness note: Remains `BLOCKED` until T023 is ACCEPTED with one selected activation topology.

## Objective

Generate and verify the T023-selected Agent Governance Skill topology plus supported platform distribution wrapper(s) from one canonical capability source/Core/engine/distribution identity.

The selected topology may contain one or multiple generated Skill entrypoints. Wrappers and entrypoints must add routing/packaging projection only and must not fork Governance behavior, Core authority, profile contracts, deterministic engine implementation or product versioning.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/decisions/D050-canonical-capability-source-and-evaluated-skill-topology.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- accepted T023 review/evidence selecting the exact topology
- `docs/RELEASES.md`
- `docs/GOVERNANCE-SKILL-PACKAGE.md`

## Authorized scope

- Non-Markdown deterministic projection/build logic required to emit the accepted topology.
- Non-Markdown platform manifest/config generation.
- Non-Markdown packaging/validation code and tests.
- Generated wrapper/Skill artifacts in ignored/temporary build output as appropriate.
- Non-Markdown artifact identity/provenance evidence.
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Changes to the topology selected by accepted T023 evidence.
- Creating independently maintained Governance Skill sources/products.
- Independent per-entrypoint version numbers or release cycles.
- Making portable operation depend on Skill-to-Skill invocation.
- Unrelated provider/model routing, host configuration, permissions, Gentle AI/Caveman integration, multi-agent architecture, or release promotion.
- Direct writes to `develop` or `main`.
- Manual maintenance of generated distribution copies.
- Publishing/tagging/releasing to `main` or an external directory/store.
- Platform-specific forks of protocol or deterministic engine behavior.

## Invariants / constraints

- One canonical capability/source model remains the source for every emitted entrypoint/wrapper.
- `governance-core/` remains the only normative protocol authority.
- One shared deterministic engine implements common runtime semantics.
- Every emitted entrypoint belongs to the same `Agent Governance Distribution vX.Y.Z` identity/version.
- Entry-point/wrapper-specific metadata is subordinate packaging/routing evidence, not Governance authority.
- The emitted Consumer-capable payload remains self-contained and contains no forbidden source-maintenance state/history.
- The final topology must match the exact T023-selected outcome; T024 is projection/packaging, not another topology decision.

## Acceptance criteria

### AC-T024-1 — selected topology reproducibility
The exact T023-selected Skill topology and supported platform wrapper(s) can be generated reproducibly from canonical source.

### AC-T024-2 — shared identity and provenance
Every generated entrypoint/wrapper is traceable to the same canonical capability-source epoch, Core identity, engine identity, source revision/build schema and Agent Governance distribution version.

### AC-T024-3 — no independent product forks
No emitted Skill contains independently editable normative/runtime source or independent product/version metadata that could evolve separately from the atomic distribution.

### AC-T024-4 — package and source isolation
Structural/package validation passes for every supported emitted artifact; Consumer-capable artifacts contain no unexpected source-only files and require no source checkout outside the artifact boundary.

### AC-T024-5 — artifact operation
Artifact-only bootstrap/validate and the applicable accepted normal operations remain green after topology projection/wrapping.

### AC-T024-6 — topology fidelity
The generated number/names/routing metadata and capability partition match the T023-selected topology without unreviewed widening, merging or decomposition.

## Verification requirements

- Run focused topology-projection/wrapper/package validation tests.
- Run reproducibility/byte- or identity-equivalence checks appropriate to the build format.
- Run artifact isolation tests for every release-target entrypoint/wrapper.
- Verify manifest/release identity agrees with T020 generated metadata and later accepted identity schema.
- Verify all emitted entrypoints share the same distribution/Core/engine/capability provenance.
- Run artifact-only Consumer bootstrap/validate/normal-operation regression where applicable.
- Map every acceptance criterion to exact evidence in the handoff.

## Stop / escalation conditions

- Platform packaging requirements would force behavior/protocol duplication.
- Required wrapper metadata cannot be generated without making a platform file an authority source.
- T023 topology outcome is unresolved or cannot be reproduced from canonical source.
- A selected multi-entrypoint topology would require independent versions or Skill-to-Skill invocation to function.
- The build cannot provide one atomic distribution identity across all emitted entrypoints.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T024-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, follow D048's normal-task publication boundary, commit/push all authorized work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
