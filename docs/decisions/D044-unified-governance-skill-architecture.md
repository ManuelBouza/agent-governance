# D044 — Unified Governance Skill Architecture

Status: ACCEPTED
Date: 2026-08-15
Scope: source product architecture, Skill authoring, deterministic runtime, packaging, source-maintenance profile
Supersedes: D017 only where D017 requires two independently maintained top-level Skills
Preserves: D017 isolation rationale and consumer/source permission boundaries

## Decision

Agent Governance will converge on:

1. one canonical normative authority in `governance-core/`;
2. one shared deterministic implementation engine;
3. one canonical Agent Governance Skill source with mutually exclusive `consumer` and `source-maintainer` profiles;
4. generated, self-contained distribution artifacts whose runtime dependencies are entirely inside the artifact boundary;
5. platform-specific wrappers or multiple thin generated Skill entrypoints only when packaging or measured activation quality requires them.

A generated second entrypoint is a routing/packaging projection of the same canonical source. It is not a second independently maintained Governance product and cannot introduce a second normative authority.

## Context

The current source tree intentionally separates `governance-core/`, `governance-skill/`, and `maintainer-skill/`. D017 chose distinct Consumer and Maintainer Skills because their triggers, context, permissions, mutation surfaces, and risks differ.

The implemented state is asymmetric:

- the Consumer Governance Skill is implemented and release-approved;
- the Maintainer Skill remains design-approved but not released;
- the current consumer runtime resolves the Core from a sibling source-tree directory rather than from inside the Skill payload;
- source-product maintenance and consumer projects use different durable coordination representations for related orchestration concepts.

The isolation concerns behind D017 remain valid. The conclusion that they require two independently maintained top-level Skill products is no longer required.

## Architecture invariants

### Normative authority

`governance-core/` remains the only editable normative protocol source.

Generated Core snapshots inside a distribution artifact are build outputs. They MUST NOT become editable source copies and MUST be traceable to the source revision from which they were built.

### Skill responsibility

The canonical Skill provides discovery, activation, profile routing, bootstrap/recovery guidance, and access to deterministic operations. It MUST NOT redefine Core authority.

`SKILL.md` remains a small routing surface. Detailed profile material is progressively loaded from profile-specific references.

### Profile isolation

`consumer` and `source-maintainer` are mutually exclusive operational contexts.

They MUST preserve the underlying D017 safety properties:

- consumer context does not acquire source-maintenance permissions;
- source-maintainer context does not treat the source repository as a normal consumer installation;
- consumer mutation surfaces remain limited to the governed consumer project;
- source-maintainer mutations remain governed by source-product policy, ownership, branching, Task Contracts, and release rules.

Profile identity MUST be established through an explicit, versioned source-product signal. It MUST NOT rely only on the presence of a directory name such as `governance-core/`.

### Shared deterministic engine

Deterministic operations are implemented once and shared by both profiles. Platform adapters and profile adapters may select paths, capabilities, or persistence representations, but MUST NOT fork protocol semantics.

### Distribution boundary

A released Skill payload MUST be self-contained. Runtime code MUST NOT require files outside the built Skill/package root.

The build may copy the canonical Core into the distribution artifact, bundle runtime modules, assets, templates, profile references, manifests, and generated metadata. `dist/` or equivalent generated output is never hand-maintained authority.

### Version separation

The architecture distinguishes at least:

- product/Skill distribution version;
- Governance protocol version;
- installed-footprint version.

A distribution update does not implicitly authorize a governed repository to migrate its installed protocol or footprint.

### Source independence

Consumer source independence remains mandatory. After bootstrap, a consumer repository must remain governable without access to the Agent Governance source repository.

### Source-product overlays

`AGENTS.md`, source branching/release policy, source Task Contracts, Orchestrator checkpoints, reviews, and source-specific maintenance policy remain source-only overlays. They are not copied into consumer distributions merely because the same Skill engine is used.

## Source-maintenance persistence gate

Unifying the Skill and engine does **not** automatically require the source repository to replace its current checkpoint/Task Contract/handoff persistence with a live consumer-style `.agent-coordination/` tree.

Committed Markdown ownership and source Task Contract semantics are material source-product invariants. Therefore:

1. the first source-maintainer implementation MUST operate through adapters over the current source-maintenance records;
2. a later deterministic semantic-equivalence evaluation must characterize what can be shared safely;
3. full source persistence convergence requires a separate accepted decision after that evidence exists;
4. if identical persistence would weaken Markdown ownership, auditability, or source lifecycle semantics, the accepted steady state may remain shared semantics/engine with a source-specific persistence adapter.

Source self-hosting is therefore a gated migration, not a prerequisite for unified Skill/runtime/package architecture.

## Activation fallback

The preferred authoring model is one canonical Skill dispatcher with profile-specific progressive disclosure.

Activation quality is an empirical release property. Positive, negative, and near-miss evals MUST test consumer routing, source-maintainer routing, and cross-profile contamination.

If a single dispatcher does not meet the accepted activation/isolation threshold, the build may emit two thin platform entrypoints. Both MUST consume the same canonical profiles, Core snapshot, and runtime. This fallback does not restore the D017 two-product architecture.

## Consequences

### Keep

- `governance-core/` as the normative source;
- source independence;
- provider-neutral executor semantics;
- progressive disclosure;
- consumer `.agent-governance/` and `.agent-coordination/` concepts;
- source-product Markdown ownership and Task Contract governance;
- current release-approved Consumer Governance v1 as immutable rollback evidence.

### Refactor

- extract deterministic runtime logic from the monolithic consumer launcher;
- build self-contained Skill artifacts rather than executing against source-tree sibling paths;
- introduce formal profiles over one engine;
- verify built artifacts, not only source layout;
- separate distribution versioning from installed protocol/footprint migration.

### Supersede or retire after evidence

- the requirement that Consumer and Maintainer be independently maintained top-level Skill products;
- the planned separate `maintainer-skill/` implementation;
- tests whose only protected invariant is physical separation of the two Skill source directories;
- release gates that couple public consumer distribution to an unreleased second maintained Skill when that second product no longer exists.

## Migration rule

This decision is implemented incrementally through `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md` and Task Contracts T018–T029.

No task may combine a behavior-changing product decision with an unlabeled pure refactor. Behavior-preserving structural changes must first freeze characterization evidence under the refactoring workflow. Behavior-changing profile, activation, migration, or release-contract changes follow the normal product-development path.

## Rollback

The existing Consumer Governance Skill v1 remains the behavioral rollback baseline until a later release is independently reviewed and accepted. No migration phase may destroy the ability to identify and restore the pre-refactor release-approved behavior.
