# D051 — Single-install self-bootstrap and durable project footprint

Status: ACCEPTED  
Date: 2026-08-17  
Scope: Consumer installation UX, distribution self-containment, bootstrap materialization, durable project independence and upgrade/package verification  
Refines: D044 and D050 distribution semantics  
Preserves: T020 self-contained artifact boundary, Consumer source independence, non-authority, profile isolation, coexistence, explicit migration and rollback invariants

## Context

Agent Governance already has two complementary architectural properties:

1. T020 proves that a built Consumer-capable artifact can contain the Core snapshot, deterministic runtime, assets and identity metadata needed to bootstrap and operate without reading the Agent Governance source checkout;
2. the Consumer contract requires a governed project to persist its own Governance authority/state so that the Skill is not the only copy of the rules or project coordination records.

The Human Owner clarified and approved the product UX consequence on 2026-08-17:

> A consumer should install Agent Governance once. The user must not then manually locate, download, copy or install separate Agent Governance support files in order to bootstrap or normally operate a governed project.

This does **not** mean that Agent Governance keeps all project state inside the installed Skill. Bootstrap must still materialize the durable project-specific Governance footprint inside the governed repository.

## Decision

Agent Governance adopts a **single-install / self-bootstrap** Consumer product invariant.

```text
one Agent Governance distribution install
        |
        v
self-contained product payload
        |
        +-- selected generated Skill entrypoint(s)
        +-- shared deterministic runtime
        +-- Governance Core snapshot
        +-- templates/assets/schemas
        +-- identity/provenance metadata
        |
        v
bootstrap <consumer repository>
        |
        +-- .agent-governance/     installed project Governance
        +-- .agent-coordination/   project-specific durable state
```

The distribution carries all **Agent-Governance-owned reusable material** required for supported Consumer bootstrap and normal operations. Bootstrap creates the **project-owned durable material** required by the governed repository.

These are different lifecycle boundaries and MUST NOT be conflated.

## 1. Single installation unit

For each supported release-target host/platform, the normal Consumer installation experience SHALL require one Agent Governance distribution installation action or one platform-native atomic bundle installation representing the same product.

After that installation, Consumer bootstrap MUST NOT require the user to separately install or copy:

- another Agent Governance Skill package;
- a separate Governance Core archive/repository checkout;
- standalone Agent Governance templates/assets;
- a second Agent Governance runtime/helper package;
- product-owned schemas/configuration downloaded out of band;
- source-product Markdown/history;
- another independently versioned Agent Governance component.

A platform prerequisite intrinsic to the supported host/runtime is not a second Agent Governance product component. Any such prerequisite must be explicit platform compatibility metadata, not an undeclared post-install support download.

## 2. Self-contained distribution boundary

The installed distribution MUST contain, directly or through deterministic generated packaging, every Agent-Governance-owned reusable artifact required by the selected topology and supported Consumer operations, including as applicable:

- generated Skill entrypoint(s) and focused references;
- the shared deterministic runtime/engine required by those entrypoints;
- a traceable generated snapshot of `governance-core/` sufficient for Consumer bootstrap;
- bootstrap templates/assets;
- deterministic schemas or package metadata required at runtime;
- product/distribution/topology/Core/runtime/capability provenance and version identity.

Normal bootstrap from an already installed release MUST NOT require access to the canonical source checkout or a network fetch of missing Agent Governance payload files.

Acquiring/installing the released distribution itself may of course use the host/platform's normal package delivery mechanism. The invariant applies after the product has been installed.

## 3. Durable project footprint

Bootstrap SHALL materialize the reusable Governance protocol snapshot and project-specific coordination state inside the consumer repository.

The current intended footprint remains conceptually:

```text
.agent-governance/
    installed Governance/Core snapshot and applicable project adapters

.agent-coordination/
    mission/workplan/state/exchange/task/decision/Skill records
```

This footprint is not a "supplemental installation dependency". It is the governed repository's durable installed authority/state, generated from the installed distribution plus Human/Strategy/project inputs.

The exact footprint remains governed by the canonical Consumer/Core contracts and migration/versioning policy.

## 4. Minimal and progressive materialization

Self-bootstrap does not authorize dumping all possible future state or all product/source material into every consumer repository.

Bootstrap MUST materialize only the durable baseline required for a valid installation. Records that are naturally demand-driven SHOULD be created when required, for example:

- concrete task records;
- project decisions;
- approved external Skill records;
- mission-specific capability inventory entries;
- archival records.

Future task content MUST NOT be preloaded merely because templates are available inside the distribution.

Source-maintenance policy/history, source Task Contracts, Orchestrator checkpoints, source reviews and source-only tooling MUST NOT leak into the consumer footprint.

## 5. Skill availability is not project authority

The installed Skill/distribution is operational tooling, not the sole repository authority.

After successful bootstrap:

- the governed project's installed Governance rules and state remain in the repository;
- loss/unavailability of the Skill MUST NOT erase or invalidate those records merely because tooling is absent;
- a compatible stateless agent must be able to reconstruct the governed frontier from repository authority/state under the Consumer contract;
- normal project authority MUST NOT require read/write access to the Agent Governance source repository.

This preserves the existing non-authority and source-independence invariants.

## 6. D050 multi-entrypoint compatibility

D050 permits T023 to select one or multiple generated Skill entrypoints, but all selected entrypoints remain one Agent Governance product/distribution.

Therefore a multi-entrypoint outcome such as:

```text
Agent Governance Distribution vX.Y.Z
    +-- Consumer Governance
    +-- Source Maintainer
    +-- optional accepted specialist entrypoint(s)
```

MUST still be installable as one product unit for a supported release-target platform.

The user MUST NOT be required to discover and manually install each Agent Governance entrypoint independently as if they were unrelated products.

Consumer bootstrap MUST copy/materialize only Consumer-applicable protocol/project material. Source-maintainer overlays/history/state MUST NOT be copied into an ordinary consumer repository merely because their generated entrypoint ships in the same product distribution.

## 7. T023 topology selection constraint

Single-install feasibility is a mandatory non-regression property for the topology experiment.

A candidate topology MAY contain several generated Skills, but it cannot become the portable release topology if its architecture intrinsically requires users to perform multiple independent Agent Governance installations or to manually assemble product-owned support files.

T023 does not need to finalize platform packaging, which belongs to T024, but it MUST reject or clearly mark non-portable any candidate whose decomposition cannot reasonably be projected into the D051 one-product installation model on the intended release-target host set.

## 8. T024 packaging responsibility

T024 SHALL produce the accepted topology as one self-contained Agent Governance distribution installation unit per supported release-target platform.

For Consumer-capable release artifacts, T024 must prove from a clean environment that:

1. the Agent Governance distribution is installed once;
2. no separate Agent Governance support payload is manually installed;
3. bootstrap of a clean unrelated repository succeeds without source-checkout access;
4. required Core/runtime/assets/templates are resolved from inside the installed distribution;
5. the resulting durable project footprint validates;
6. applicable normal Consumer operations run from the installed distribution/project footprint.

If a target platform fundamentally cannot package the selected topology into one supported installation unit, T024 MUST stop/escalate rather than silently weakening D051. A later Human-approved platform exception may narrow support, but cannot be inferred by the executor.

## 9. Distribution update vs project migration

Single-install does not authorize silent project mutation when the installed Agent Governance distribution changes.

The version boundaries remain separate:

```text
Agent Governance distribution version
Governance protocol version
installed project-footprint version
```

Updating/replacing the host-installed distribution may be atomic as one product, but changing an already governed repository's `.agent-governance/` or `.agent-coordination/` footprint remains an explicit planned/authorized migration under MG2/T027.

A multi-entrypoint distribution is upgraded as one Agent Governance product; entrypoints are not independently updated by default.

## 10. T029 release proof

Final release readiness MUST demonstrate the complete user journey from a clean supported environment:

```text
install Agent Governance once
        -> bootstrap clean unrelated repository
        -> validate durable footprint
        -> perform applicable normal operation(s)
        -> operate without source checkout
```

The release gate must fail if success requires undeclared/manual Agent Governance support installation outside the released distribution.

## External and project-native capabilities

D051 governs **Agent-Governance-owned product dependencies**.

It does not mean Agent Governance bundles every possible external capability a governed project may use. In particular:

- project-native SDD/testing/tooling remains owned by the project and is reused/adapted under coexistence rules;
- third-party Skills discovered/audited for a project remain separately approved external artifacts;
- optional external capabilities are not reclassified as hidden Agent Governance product dependencies merely because Governance can discover or audit them.

Agent Governance itself must remain usable without requiring such optional third-party capabilities unless a later explicit product decision changes the supported baseline.

## Consequences

### Required

- one product installation experience;
- self-contained reusable Agent Governance payload;
- deterministic self-bootstrap;
- durable repository-owned Governance/state footprint;
- no source-checkout dependency after installation;
- no manual second Agent Governance support package;
- atomic product identity across all generated entrypoints;
- explicit migration for already-installed project footprint changes.

### Not required

- keeping project state inside the Skill;
- pre-materializing future task/mission details;
- bundling arbitrary third-party Skills or project-native tooling;
- copying source-maintenance overlays into consumer repositories;
- one physical `SKILL.md` when D050 evidence selects multiple generated entrypoints.

## Program impact

- T020 remains accepted evidence for the underlying self-contained artifact capability.
- T021 and T022 executable scope are unchanged.
- MG1/T023 must treat single-install feasibility as a mandatory topology non-regression boundary.
- T024 owns deterministic projection into one installable self-contained distribution unit per supported release-target platform.
- MG2/T027 must preserve the distinction between distribution update and explicit project-footprint migration.
- T029 must verify the clean single-install -> self-bootstrap -> durable-operation journey.
- T026 remains separately gated and is not authorized by D051.

## Rollback

D051 is prospective and does not rewrite accepted Consumer v1 history. Consumer Governance v1 remains the behavioral rollback baseline until a later release is independently accepted.