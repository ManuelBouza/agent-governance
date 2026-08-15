# Unified Governance Skill Refactor Plan

Status: PLANNED
Date: 2026-08-15
Planning baseline: `develop` at `8be1620053d0231c090cabdd7de964fd08dfbe32`
Controlling decision: `docs/decisions/D044-unified-governance-skill-architecture.md`

## Purpose

Convert the current Consumer-Skill-plus-planned-Maintainer-Skill architecture into one canonical Governance Skill source over one normative Core and one deterministic engine, while preserving consumer behavior, source-product governance, auditability, rollback, and release isolation.

This is not one large refactor. It is a controlled sequence containing both:

- behavior-preserving refactor stages governed by `docs/REFACTORING-WORKFLOW.md`;
- explicit product/behavior changes governed by the normal Task Contract and decision flow.

## End state

```text
governance-core/                 canonical normative authority
        |
        v
shared deterministic engine     one implementation
        |
        +--> consumer profile
        |
        +--> source-maintainer profile
        |
        v
canonical Governance Skill      small dispatcher + progressive references
        |
        v
build/package
        |
        +--> self-contained platform distribution
        +--> optional thin generated routing entrypoint(s)
```

Consumer repositories continue to receive a source-independent installed Core snapshot and durable coordination footprint. The source product uses the same Skill/engine semantics but retains source-only policy overlays. Full persistence convergence is separately gated.

## Non-goals

This program does not:

- merge the normative Core into `SKILL.md`;
- make distribution artifacts authoritative source;
- require consumer projects to access the Agent Governance source repository after bootstrap;
- make OpenCode, Codex, Claude Code, Gentle AI, Caveman, or any other provider/runtime an authority source;
- silently migrate governed repositories when the Skill/plugin updates;
- require immediate source adoption of consumer persistence layout;
- rewrite historical Task Contracts, handoffs, decisions, reviews, or accepted release evidence.

## Work classes

### Orchestrator-owned Markdown gates

These are authored by ChatGPT on short-lived `docs/*` branches and integrated through PRs. They are not delegated to the executor.

- **MG0 — Architecture and task-plan integration**: D044, this plan, T018–T029, checkpoint refresh.
- **MG1 — Unified Skill/profile routing contract**: after T022 is accepted, author the canonical Skill dispatcher/profile reference Markdown and any controlling contract delta required before activation evals.
- **MG2 — Upgrade contract**: before T027 implementation, explicitly revise the stable CLI/upgrade contract because the current Consumer Skill exposes exactly seven commands.
- **MG3 — Legacy architecture retirement documentation**: after replacement behavior is accepted, update D017 status/reference, package/testing/release documentation, maintainer-profile documentation, and retire obsolete `maintainer-skill/` Markdown.

Every MG change follows Markdown ownership and branch policy. No executor task may compensate for a missing Markdown gate by editing committed Markdown.

## Executor Task sequence

| Task | Class | Result | Depends on |
|---|---|---|---|
| T018 | test/eval | Freeze Consumer v1 characterization and package-boundary baseline | MG0 |
| T019 | refactor | Extract shared deterministic engine with zero consumer behavior drift | T018 ACCEPTED |
| T020 | infrastructure | Build self-contained artifact with generated identity metadata | T019 ACCEPTED |
| T021 | refactor | Introduce formal `consumer` profile abstraction with zero behavior drift | T020 ACCEPTED |
| T022 | feature | Add `source-maintainer` profile over current source-maintenance adapters | T021 ACCEPTED |
| T023 | test/eval | Validate unified dispatcher/profile activation and isolation | MG1 + T022 ACCEPTED |
| T024 | infrastructure | Generate and verify platform distribution wrapper(s) from one source | T023 ACCEPTED |
| T025 | test/eval | Prove/characterize semantic equivalence between source legacy state and common coordination semantics | T022 ACCEPTED |
| T026 | mixed | Optional source persistence convergence migration | T025 + separate accepted decision |
| T027 | feature | Add explicit governed-repository upgrade/migration lifecycle | MG2 + T020 + T023 |
| T028 | refactor/test | Remove obsolete non-Markdown two-Skill structural assumptions | T023 + replacement packaging accepted |
| T029 | release/test-eval | Final release-readiness and rollback verification | T024 + T027 + T028 + T026 decision outcome |

T025 may proceed in parallel with T023/T024 once T022 is accepted. T026 is intentionally blocked and is not on the critical path for T024 or T027.

## Phase gates

### Phase A — Freeze and extract

T018 → T019

Goal: protect the release-approved Consumer v1 behavior before moving implementation boundaries.

Exit condition: the shared engine exists, while the seven-command CLI, outputs, exit behavior, consumer footprint, and protocol semantics remain characterization-equivalent to the baseline.

### Phase B — Self-contained distribution foundation

T020 → T021

Goal: make the built Skill payload autonomous and introduce a profile abstraction without changing consumer semantics.

Exit condition: artifact-only bootstrap/validate/normal operations pass with the source checkout unavailable, and `profile=consumer` remains behaviorally equivalent to Consumer v1.

### Phase C — Unified profile model

T022 → MG1 → T023

Goal: implement source-maintenance routing on the same engine, then measure whether a single Skill dispatcher can isolate both contexts reliably.

Exit condition: profile isolation tests and activation evals pass. If dispatcher quality fails the accepted threshold, the architecture remains one source/product but the build switches to thin generated entrypoints.

### Phase D — Distribution wrappers

T024

Goal: turn the self-contained payload into reproducible platform distribution artifacts without turning wrapper metadata into authority.

Exit condition: clean built artifacts have traceable source identity, contain no source-maintenance state, and bootstrap a clean unrelated repository without source-tree access.

### Phase E — Source dogfooding and persistence decision

T025 → decision gate → optional T026

Goal: determine which source-maintenance semantics can safely use the common coordination representation.

Exit condition is one of:

1. accepted evidence supports a controlled source persistence migration, followed by T026; or
2. a decision accepts shared engine/semantics with a source-specific persistence adapter as the steady state, and T026 is CANCELLED.

The second outcome is valid and does not block unified Skill/distribution architecture.

### Phase F — Explicit upgrade/migration lifecycle

MG2 → T027

Goal: separate distribution updates from governed-repository protocol/footprint migration.

Exit condition: an update can be planned, explicitly authorized, applied transactionally, validated, and rolled back; a distribution auto-update cannot silently mutate governed repository state.

### Phase G — Legacy retirement and release gate

T028 → MG3 → T029

Goal: remove obsolete structural assumptions only after replacement behavior is accepted, then verify the complete release candidate and rollback path.

Exit condition: final deterministic tests, artifact isolation tests, profile activation evals, supported-adapter verification, migration tests, and rollback checks pass under the repository release policy.

## Cross-cutting invariants

All tasks preserve these properties unless an explicit accepted decision changes one:

- `governance-core/` remains the normative source;
- Skills and runtime remain subordinate to Core authority;
- consumer source independence remains mandatory;
- source-product Markdown remains ChatGPT-owned;
- executor work remains non-Markdown unless repository policy is explicitly changed first;
- `develop` remains the normal integration branch and `main` remains stable/release;
- Task Contracts are integrated into `develop` before executor launch;
- generated distribution output is reproducible and non-authoritative;
- prior Consumer Governance v1 accepted behavior remains an identifiable rollback reference;
- no task may broaden into provider/model routing, host permission changes, Gentle/Caveman dependency, or unrelated protocol work.

## Version model

The build/release system must be able to distinguish:

```text
product / Skill distribution version
protocol version
installed-footprint version
source commit identity
build schema version
Core/runtime digests
```

Generated identity metadata is evidence and compatibility metadata, not Governance authority.

## Verification model

The program progressively establishes four independent test planes:

1. **Core contract tests** — normative protocol behavior.
2. **Deterministic runtime tests** — state/operation behavior and compatibility.
3. **Profile/isolation tests** — consumer versus source-maintainer routing and mutation boundaries.
4. **Skill activation evals** — positive, negative, near-miss, and cross-profile routing quality.

Release verification additionally runs against the **built artifact**, not only the source layout.

## Rollback strategy

Each task has its own rollback boundary. The program does not rely on one end-of-project rollback.

- T018 freezes the pre-refactor behavioral reference.
- T019 keeps a thin compatible launcher and can revert to the monolithic implementation.
- T020 introduces build output without changing installed consumer semantics.
- T021 adds a consumer profile without source-maintainer behavior.
- T022 adds source-maintainer through adapters without changing source persistence.
- T023 does not authorize retiring separate-layout protections until routing evidence passes.
- T025 prevents speculative live source-state migration.
- T027 requires transactional migration/rollback behavior.
- T028/MG3 retire legacy structure only after replacement acceptance.
- T029 verifies the immutable pre-refactor Consumer v1 rollback reference remains identifiable.

## Program completion

This refactor program is complete only when T029 is ACCEPTED and all required Markdown retirement/release records are integrated. Release promotion/tagging remains a separate Human-authorized release action under `docs/RELEASES.md`.
