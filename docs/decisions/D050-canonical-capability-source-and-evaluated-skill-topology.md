# D050 — Canonical capability source and evaluated Skill activation topology

Status: ACCEPTED  
Date: 2026-08-16  
Scope: Agent Governance Skill responsibility, activation topology, generated entrypoints, routing evaluation, product identity and distribution versioning  
Refines: `docs/decisions/D044-unified-governance-skill-architecture.md`  
Preserves: D044 single Core, shared deterministic engine, source independence, profile isolation, generated distribution and rollback invariants

## Context

D044 selected one canonical Governance Skill source with mutually exclusive `consumer` and `source-maintainer` profiles and allowed thin generated entrypoints when packaging or measured activation quality required them.

Subsequent architectural research examined whether Agent Skills should be decomposed according to the Single Responsibility Principle (SRP), component cohesion, progressive disclosure, activation quality, context cost, permission/risk boundaries and host portability.

The research supports two conclusions that must be held together:

1. a Skill does **not** violate SRP merely because it exposes multiple related operations; responsibility is better understood through shared intent, stakeholder, authority, permissions/risk, context and reasons for change;
2. one canonical source/product does **not** imply that one top-level activatable Skill is always the correct routing unit.

Consumer and source-maintainer are especially strong candidates for separate activation units because they differ materially in intent, repository context, mutation surface, permissions, risks and reasons for change even though they should share Core and deterministic semantics.

The Human Owner approved on 2026-08-16 that Agent Governance shall:

- evaluate multiple activation topologies at T023 rather than treating split entrypoints only as a failure fallback;
- pre-register a multidimensional victory criterion before T023 trials;
- retain one Agent Governance product identity/version even if the selected distribution exposes multiple generated Skills.

## Decision

Agent Governance separates five architectural units that D044 previously kept too close conceptually:

```text
normative authority        = governance-core/
runtime semantics          = shared deterministic engine
authoring/capability unit  = one canonical capability source
distribution unit          = one Agent Governance product/version
activation unit            = one or more generated coherent Skills
```

The number of activatable Skills is an **evaluated distribution projection**, not Governance authority and not the number of source products.

### 1. Canonical capability source

Agent Governance SHALL maintain one canonical source for capability semantics, profile definitions, intent/routing metadata and references required to generate the supported Skill entrypoints.

That source may be represented through the existing canonical Markdown/profile contracts plus deterministic structured projections selected by later implementation gates. D050 does not authorize a second editable Governance authority or independently maintained Skill forks.

All generated entrypoints MUST remain subordinate to:

- `governance-core/` as the only normative protocol authority;
- the shared deterministic engine as the only implementation of common deterministic semantics;
- the accepted profile/capability contracts;
- one deterministic build/distribution identity.

### 2. Skill responsibility boundary

For Agent Governance, a Skill responsibility is evaluated as a cohesive group of user intents that normally share:

- stakeholder/actor;
- authority and state surface;
- compatible permission/risk envelope;
- context/load path;
- reasons for change;
- runtime/capability dependencies;
- evaluation and release expectations.

SRP is therefore a cohesion heuristic, not a rule such as one command, one file, one role or one operation per Skill.

The following decompositions are explicitly rejected as defaults:

- one Skill per CLI command;
- one Skill per source file;
- one Skill per agent role merely because roles differ;
- micro-Skills that normally must all activate together.

### 3. T023 topology candidates

T023 SHALL compare at least these activation presentations while keeping Governance Core, deterministic engine, profile semantics and functional capability behavior fixed:

#### B0 — unified dispatcher baseline

One top-level Agent Governance dispatcher with `consumer` and `source-maintainer` routing, as originally preferred by D044.

#### B1 — thin single router

One deliberately small top-level Skill router with focused profile/capability references loaded progressively.

#### F2 — generated profile peers

Two generated peer Skills:

- Consumer Governance;
- Source Maintainer.

They remain projections of one capability source and one distribution, not independently maintained products.

#### G3 — hybrid challenger

Three generated peer Skills:

- Consumer lifecycle, containing the cohesive Consumer bootstrap/state/event/mission/handoff/sequencing/archive/coexistence surface;
- Source Maintainer;
- External Skill Trust, containing external Skill discovery and supply-chain audit.

`External Skill Trust` is only a challenger topology until T023 evidence justifies the split. D050 does not pre-accept that third entrypoint for release.

T023 MAY include additional non-release experimental presentations only when MG1 explicitly defines them without changing Governance semantics. Host-specific experiments MUST be labelled host-specific and cannot become the portable baseline merely because one provider supports them.

### 4. Routing ownership and Skill-to-Skill boundary

Portable Agent Governance MUST NOT require a Skill-to-Skill invocation primitive.

The portable routing model is:

```text
host / current Agent
    -> discovers Skill catalog metadata
    -> selects the appropriate Agent Governance Skill
    -> activated Skill progressively loads its own focused references/tools
```

A top-level Skill may explain routing or expose metadata, but the product contract MUST NOT depend on a nested `Skill -> Skill` call stack with arguments, return semantics or transfer of control unless a later provider-specific adapter explicitly treats that behavior as optional.

If future evidence requires autonomous specialist coordination, that is an Agent/workflow architecture decision and requires a separate accepted gate. D050 does not introduce multi-agent architecture into the current D044 refactor program.

### 5. Pre-registered multidimensional selection

MG1 SHALL pre-register the T023 corpus, comparison method, host/model matrix that is practically testable, repeated-trial policy and numeric/qualitative victory thresholds **before** T023 observes comparative results.

T023 selection MUST consider, where observable and applicable:

- functional task success and deterministic regression;
- activation precision, recall and F1 or equivalent routing measures;
- false activation on negative and near-miss cases;
- cross-profile contamination;
- wrong-specialist selection;
- unnecessary multi-activation/overactivation;
- actual or explicitly modelled context load, including TMC/RFO/ND/CAR-compatible evidence;
- permission/risk exposure where the host makes it observable;
- source independence and package isolation;
- portability across supported hosts, with vendor-specific behavior separated from portable claims;
- maintenance/source duplication and version-skew risk.

A candidate MUST NOT win by improving one routing metric while weakening deterministic correctness, profile isolation, source independence, authority integrity or required security boundaries.

The exact material-improvement and non-regression thresholds are an MG1 pre-registration concern. They MUST NOT be weakened after results are observed merely to select a preferred topology.

If no split topology demonstrates an accepted material advantage, the single-dispatcher/thin-router family remains a valid result.

### 6. One product and one version

Regardless of the number of selected generated Skill entrypoints, the public product identity remains:

```text
Agent Governance Distribution vX.Y.Z
```

A release SHALL use one atomic distribution identity for the generated topology.

Initial architecture MUST NOT independently version Consumer, Source Maintainer or External Skill Trust entrypoints. Every emitted entrypoint must be traceable to the same accepted source/capability epoch, Core identity, engine identity and distribution version.

A later decision may introduce independently versioned components only with explicit compatibility/version-skew evidence and Human Owner approval.

### 7. T024 projection responsibility

T024 SHALL generate and verify the topology selected by T023 from canonical source. It is no longer limited conceptually to wrapping one physical Skill payload.

The build may emit one or several coherent Skill entrypoints plus platform wrappers, but all outputs must remain reproducible projections of one capability source/Core/engine/distribution identity.

### 8. T028 retirement meaning

T028 retires assumptions that Consumer and Maintainer must be **independently maintained Skill products/source trees**.

T028 MUST NOT interpret its name or D044 legacy wording as requiring the final distribution to expose exactly one Skill entrypoint. Multiple generated entrypoints remain compatible with the unified product when selected by T023.

### 9. T029 release proof

If the selected topology contains multiple entrypoints, T029 MUST prove at least:

- one distribution version/identity;
- common canonical capability-source epoch;
- common Core identity;
- common engine identity;
- atomic build/install/update semantics for the supported distribution;
- no independently editable normative authority in any entrypoint;
- profile/activation/isolation thresholds for the selected topology;
- rollback to the immutable Consumer v1 baseline remains identifiable.

## Program impact

### T021

No scope change. T021 remains a zero-behavior-drift `consumer` profile abstraction. Profile identity and Skill activation topology are separate architectural layers.

### T022

No scope change. T022 still implements the `source-maintainer` profile on the shared engine through current source-maintenance adapters.

### MG1

MG1 becomes the **Skill activation topology and eval pre-registration gate**. It authors the smallest canonical dispatcher/profile/capability routing surfaces needed for the experiment and pre-registers the comparison criteria before T023 trials.

### T023

T023 changes from a binary "single dispatcher or fallback" test into a controlled comparative topology evaluation over B0, B1, F2 and G3.

### T024 / T028 / T029

Their future contracts are refined by this decision as described above.

### T026

Unchanged. Source persistence convergence remains separately gated and MUST NOT be launched by D050.

## RCAB relationship

D050 does not change D047 source-repository bootstrap thresholds or authorize splitting source Markdown because of size.

T023 may use RCAB-compatible measurements to compare Skill activation load paths, but source-repository RCAB and distributed-Skill activation context are distinct measured surfaces.

The governing rule remains:

> Budget the load path, not just the file or Skill count.

More Skills are not presumed to reduce context. A split is justified only by observed routing/context/risk/maintenance benefit under the pre-registered evaluation.

## Consequences

### Keep

- one Agent Governance product;
- one `governance-core/` authority;
- one deterministic engine;
- one canonical capability/source model;
- profile isolation;
- progressive disclosure;
- source independence;
- reproducible generated distribution;
- Consumer v1 rollback baseline.

### Refine

- "one canonical Skill source" now means one canonical capability/authoring source that may project to multiple coherent generated Skill entrypoints;
- activation topology becomes an empirical T023 decision rather than an authoring assumption;
- multiple generated entrypoints no longer imply return to the D017 two-product architecture.

### Do not introduce

- independently maintained Governance Skill products;
- duplicated Core or profile authority;
- mandatory Skill-to-Skill invocation;
- multi-agent architecture without a new decision;
- independent per-entrypoint versioning;
- micro-Skill decomposition by command/file/role;
- post-hoc eval thresholds.

## Rollback

D050 is prospective and does not rewrite accepted implementation history.

Until T023 and subsequent packaging/release gates accept a replacement topology, the existing Consumer Governance v1 remains the behavioral rollback baseline and current accepted source/runtime states remain authoritative for their completed tasks.
