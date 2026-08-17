# Unified Governance Skill Refactor Plan

Status: PLANNED
Date: 2026-08-15
Planning baseline: `develop` at `8be1620053d0231c090cabdd7de964fd08dfbe32`
Controlling decisions:
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/decisions/D050-canonical-capability-source-and-evaluated-skill-topology.md`
- `docs/decisions/D051-single-install-self-bootstrap-and-durable-project-footprint.md`

## Purpose

Convert the current Consumer-Skill-plus-planned-Maintainer-Skill architecture into one canonical Agent Governance product over one normative Core, one deterministic engine and one canonical capability source, while preserving consumer behavior, source-product governance, auditability, rollback and release isolation.

The final number of activatable Skill entrypoints is not assumed by the authoring architecture. D050 requires T023 to compare controlled activation topologies and select one or more **generated** coherent entrypoints from the same canonical capability source and distribution identity.

D051 adds the Consumer distribution UX invariant: regardless of the selected topology, a supported release-target platform must expose Agent Governance as one self-contained installation unit capable of bootstrapping a clean Consumer repository without manually installed supplemental Agent Governance payload files or source-checkout access.

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
canonical capability source     intents / routes / profile references
        |
        v
deterministic build/projection
        |
        +--> one selected Skill entrypoint
        |        or
        +--> multiple coherent generated Skill entrypoints
        |
        +--> self-contained platform distribution wrapper(s)
        |
        v
one Agent Governance installation unit per supported platform
        |
        v
bootstrap -> durable consumer project footprint
```

Consumer repositories continue to receive a source-independent installed Core snapshot and durable coordination footprint. The source product uses the same engine/capability semantics but retains source-only policy overlays. Full persistence convergence is separately gated.

Regardless of selected activation topology, the release remains one `Agent Governance Distribution vX.Y.Z` with one Core identity, one engine identity and one canonical capability-source epoch. Generated entrypoints are routing/distribution projections, not independently maintained Governance products.

## Non-goals

This program does not:

- merge the normative Core into `SKILL.md`;
- make distribution artifacts authoritative source;
- require consumer projects to access the Agent Governance source repository after bootstrap;
- require users to manually install a second Agent Governance Core/runtime/template/schema/Skill support payload after installing the distribution;
- classify the durable project footprint created by bootstrap as a second product installation;
- make OpenCode, Codex, Claude Code, Gentle AI, Caveman, or any other provider/runtime an authority source;
- silently migrate governed repositories when the Skill/plugin/distribution updates;
- require immediate source adoption of consumer persistence layout;
- rewrite historical Task Contracts, handoffs, decisions, reviews, or accepted release evidence;
- require portable Skill-to-Skill invocation;
- introduce multi-agent architecture merely to obtain Skill modularity;
- independently version generated Skill entrypoints;
- decompose the product into one Skill per command, file or role;
- bundle arbitrary project-native or third-party capabilities merely because Governance can discover/reuse/audit them.

## Work classes

### Orchestrator-owned Markdown gates

These are authored by ChatGPT on short-lived `docs/*` branches and integrated through PRs. They are not delegated to the executor.

- **MG0 — Architecture and task-plan integration**: D044, this plan, T018–T029, checkpoint refresh.
- **MG1 — Skill activation topology and eval pre-registration gate**: after T022 is accepted, author the smallest canonical dispatcher/profile/capability routing surfaces needed for evaluation and pre-register the T023 topology corpus, variants, host/model matrix, repeated-trial method and victory/non-regression thresholds before comparative results are observed. D051 single-install feasibility is a mandatory non-regression boundary.
- **MG2 — Upgrade contract**: before T027 implementation, explicitly revise the stable CLI/upgrade contract because the current Consumer Skill exposes exactly seven commands, preserving D051 one-product update vs explicit project-footprint migration separation.
- **MG3 — Legacy architecture retirement documentation**: after replacement behavior/topology is accepted, update D017 status/reference, package/testing/release documentation, maintainer-profile documentation, and retire obsolete independently maintained Skill-source assumptions. MG3 MUST NOT equate multiple generated entrypoints with multiple independently maintained products.

Every MG change follows Markdown ownership and branch policy. No executor task may compensate for a missing Markdown gate by editing committed Markdown.

## Executor Task sequence

| Task | Class | Result | Depends on |
|---|---|---|---|
| T018 | test/eval | Freeze Consumer v1 characterization and package-boundary baseline | MG0 |
| T019 | refactor | Extract shared deterministic engine with zero consumer behavior drift | T018 ACCEPTED |
| T020 | infrastructure | Build self-contained artifact with generated identity metadata | T019 ACCEPTED |
| T021 | refactor | Introduce formal `consumer` profile abstraction with zero behavior drift | T020 ACCEPTED |
| T022 | feature | Add `source-maintainer` profile over current source-maintenance adapters | T021 ACCEPTED |
| T023 | test/eval | Compare pre-registered Skill activation topologies and select the accepted projection, preserving D051 installability | MG1 + T022 ACCEPTED |
| T024 | infrastructure | Generate the selected topology as one self-contained installable Agent Governance distribution per supported target | T023 ACCEPTED |
| T025 | test/eval | Prove/characterize semantic equivalence between source legacy state and common coordination semantics | T022 ACCEPTED |
| T026 | mixed | Optional source persistence convergence migration | T025 + separate accepted decision |
| T027 | feature | Add explicit governed-repository upgrade/migration lifecycle preserving one-product distribution identity | MG2 + T020 + T023 |
| T028 | refactor/test | Remove obsolete independently-maintained-two-product structural assumptions | T023 + T024 ACCEPTED |
| T029 | release/test-eval | Final release-readiness, selected-topology identity, D051 clean-install journey and rollback verification | T024 + T027 + T028 + T026 decision outcome |

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

T020 is the accepted technical precursor for D051: the later release pipeline must preserve this self-contained behavior after topology/package refactoring.

### Phase C — Unified profile model and evaluated activation topology

T022 → MG1 → T023

Goal: implement source-maintenance routing on the same engine, then empirically select the activation topology rather than assuming that canonical authoring must equal one activatable Skill.

MG1 freezes the same Core, engine, profile/capability semantics and functional behavior across the topology experiment and pre-registers the comparison criteria before results are observed.

T023 compares at least the D050 candidates:

- **B0** — unified dispatcher baseline;
- **B1** — thin single router with focused references;
- **F2** — generated Consumer + Source Maintainer peer Skills;
- **G3** — generated Consumer lifecycle + Source Maintainer + External Skill Trust challenger.

The experiment measures positive, negative, near-miss and cross-profile routing together with functional non-regression, context/load-path evidence, isolation, overactivation, portability, relevant permission/risk exposure and D051 single-install feasibility.

Exit condition: one topology satisfies the pre-registered multidimensional criteria without weakening deterministic correctness, authority, source independence, profile isolation, security boundaries or one-product/single-install packaging feasibility. If no split topology demonstrates accepted material advantage, a single dispatcher/thin router remains a valid outcome.

### Phase D — Selected topology and self-contained distribution

T024

Goal: reproducibly project the T023-selected topology into one self-contained Agent Governance installation unit per supported release-target platform without turning wrapper/entrypoint metadata into authority.

Exit condition: every emitted entrypoint/wrapper is traceable to the same source/capability epoch, Core identity, engine identity and distribution version; one supported installation action makes the complete Agent Governance product available; a clean Consumer repository bootstraps/validates/operates without source checkout or manually installed supplemental Agent Governance payload; and source-maintainer overlays/history/state do not leak into the Consumer footprint.

### Phase E — Source dogfooding and persistence decision

T025 → decision gate → optional T026

Goal: determine which source-maintenance semantics can safely use the common coordination representation.

Exit condition is one of:

1. accepted evidence supports a controlled source persistence migration, followed by T026; or
2. a decision accepts shared engine/semantics with a source-specific persistence adapter as the steady state, and T026 is CANCELLED.

The second outcome is valid and does not block the selected Skill/distribution architecture.

### Phase F — Explicit upgrade/migration lifecycle

MG2 → T027

Goal: separate distribution updates from governed-repository protocol/footprint migration.

Exit condition: the Agent Governance distribution can update as one product; an update alone does not silently mutate governed project state; a project-footprint migration can be planned, explicitly authorized, applied transactionally, validated and rolled back; and supported migration does not require manually installed supplemental Agent Governance support payload or source checkout.

If the selected topology contains multiple entrypoints, upgrade semantics apply to the atomic Agent Governance distribution rather than independently versioned Skill components.

### Phase G — Legacy retirement and release gate

T028 → MG3 → T029

Goal: remove obsolete assumptions that Consumer and Maintainer must be independently maintained Skill products only after replacement behavior/topology is accepted, then verify the complete release candidate and rollback path.

T028/MG3 MUST preserve any multiple generated entrypoints selected by T023; what is retired is independent authoring/product authority, not necessarily the physical count of Skill entrypoints.

Exit condition: final deterministic tests, selected-topology activation evals, artifact isolation tests, supported-adapter verification, migration tests, atomic distribution identity checks, D051 one-install/self-bootstrap clean-environment tests, and rollback checks pass under the repository release policy.

## Cross-cutting invariants

All tasks preserve these properties unless an explicit accepted decision changes one:

- `governance-core/` remains the normative source;
- Skills and runtime remain subordinate to Core authority;
- one canonical capability/source model feeds every generated entrypoint;
- the shared deterministic engine remains the single implementation of common semantics;
- consumer source independence remains mandatory;
- every supported Consumer release-target platform exposes one self-contained Agent Governance installation unit/bundle for the accepted topology;
- bootstrap materializes durable repository-owned Governance/state and does not require manually installed supplemental Agent Governance payload after product installation;
- source-maintenance overlays/history/state remain outside ordinary Consumer footprints;
- source-product Markdown remains ChatGPT-owned;
- executor work remains non-Markdown unless repository policy is explicitly changed first;
- `develop` remains the normal integration branch and `main` remains stable/release;
- Task Contracts are integrated into `develop` before executor launch;
- generated distribution output is reproducible and non-authoritative;
- generated entrypoints belong to one Agent Governance distribution version and are not independently versioned by default;
- portable operation does not depend on Skill-to-Skill invocation;
- distribution updates do not silently migrate governed project footprint;
- prior Consumer Governance v1 accepted behavior remains an identifiable rollback reference;
- no task may broaden into provider/model authority, unapproved host permission changes, Gentle/Caveman dependency, multi-agent product architecture, or unrelated protocol work.

## Version model

The build/release system must be able to distinguish at least:

```text
Agent Governance distribution version
selected activation-topology identity/schema
protocol version
installed-footprint version
source commit identity
canonical capability-source epoch/identity
build schema version
Core/runtime digests
```

If multiple Skill entrypoints are emitted, they share the same distribution version and must be traceable to the same accepted capability/Core/runtime identities.

Generated identity metadata is evidence and compatibility metadata, not Governance authority.

## Verification model

The program progressively establishes independent test/evidence planes:

1. **Core contract tests** — normative protocol behavior.
2. **Deterministic runtime tests** — state/operation behavior and compatibility.
3. **Profile/isolation tests** — consumer versus source-maintainer routing and mutation boundaries.
4. **Skill activation topology evals** — positive, negative, near-miss, cross-profile, wrong-specialist and overactivation quality across the pre-registered topology candidates.
5. **Context/routing evidence** — TMC/RFO/ND/CAR-compatible or host-observed load-path evidence where practical, without relabelling byte heuristics as exact tokens.
6. **Distribution identity/isolation evidence** — reproducibility, one-product identity, shared Core/engine/capability provenance and source independence across every emitted entrypoint/wrapper.
7. **D051 installation evidence** — clean one-install -> self-bootstrap -> durable-operation paths with source checkout unavailable and no out-of-band Agent Governance support payload.
8. **Upgrade/migration evidence** — distribution update and project-footprint migration remain separate, explicit and rollback-safe.

Release verification runs against the **built artifact/distribution topology**, not only the source layout.

## Rollback strategy

Each task has its own rollback boundary. The program does not rely on one end-of-project rollback.

- T018 freezes the pre-refactor behavioral reference.
- T019 keeps a thin compatible launcher and can revert to the monolithic implementation.
- T020 introduces self-contained build output without changing installed consumer semantics.
- T021 adds a consumer profile without source-maintainer behavior.
- T022 adds source-maintainer through adapters without changing source persistence.
- T023 is evaluative: a challenger topology cannot replace the current presentation unless it meets pre-registered criteria including D051 feasibility.
- T024 projects only the T023-selected topology and must preserve one-install self-bootstrap.
- T025 prevents speculative live source-state migration.
- T027 requires transactional migration/rollback behavior for the atomic distribution while preserving distribution-update/project-migration separation.
- T028/MG3 retire only obsolete independent-product/source assumptions after replacement acceptance.
- T029 verifies the immutable pre-refactor Consumer v1 rollback reference remains identifiable and the D051 user journey remains release-green.

## Program completion

This refactor program is complete only when T029 is ACCEPTED and all required Markdown retirement/release records are integrated. Release promotion/tagging remains a separate Human-authorized release action under `docs/RELEASES.md`.
