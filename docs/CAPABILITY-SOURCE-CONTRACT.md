# Canonical Capability Source Contract

Status: DESIGN-APPROVED  
Controlling decision: `docs/decisions/D050-canonical-capability-source-and-evaluated-skill-topology.md`

## Purpose

Define the canonical **authoring model for Agent Governance capabilities** used to derive routing, profile presentation and future generated Skill entrypoints without creating a second Governance authority or assuming a final activation topology.

D050 separates five different architectural units:

```text
normative authority        = governance-core/
runtime semantics          = shared deterministic engine
authoring/capability unit  = canonical capability source
distribution unit          = one Agent Governance product/version
activation unit            = one or more generated coherent Skills
```

This contract defines the third unit only.

It exists to prevent every future Skill/topology task from reconstructing capability ownership, intent, context, risk and references from many unrelated documents.

## Authority boundary

The canonical capability source is **not** normative protocol authority.

Authority order remains:

```text
Human / repository Governance authority
        -> governance-core/
        -> accepted Decisions / Task Contracts / functional contracts
        -> canonical capability source metadata and references
        -> generated Skill/router/package projections
```

If capability metadata conflicts with the Governance Core or an accepted controlling Decision/Task Contract, the higher authority wins and the capability source must be corrected.

The capability source MUST reference normative behavior rather than copy large protocol rules into routing metadata.

## Capability != Skill

A capability is an authoring/routing unit describing a cohesive set of intents and operational surfaces.

A Skill is an activation/distribution projection selected later.

Therefore:

```text
capability count != Skill count
profile count    != Skill count
command count    != Skill count
file count       != Skill count
```

Several capabilities may be projected into one Skill, and one capability family may be exposed through different generated topology candidates during evaluation.

No capability record may claim that its existence requires a separately installed or independently versioned Skill.

## Canonical capability identity

Every stable capability family SHOULD have a durable, product-neutral identifier.

Identifiers use lowercase dot-separated names scoped by semantic domain, for example:

```text
consumer.lifecycle
consumer.skill-trust
source.maintenance
```

Sub-capability identifiers MAY be introduced when they materially improve routing or context disclosure, for example:

```text
consumer.lifecycle.bootstrap
consumer.lifecycle.state
consumer.lifecycle.execution
source.maintenance.orchestrator
source.maintenance.executor
source.maintenance.testing
```

A sub-capability identifier is a routing/context aid. It does not create an independent product, authority source or top-level Skill.

Identifiers MUST remain stable across generated topology experiments when the underlying capability semantics are unchanged.

## Required capability metadata

A canonical capability definition SHOULD encode or reference the following fields when material.

### Identity

- stable capability ID;
- human-readable name;
- owning profile or profile set;
- lifecycle/status when relevant;
- controlling contract(s) and Core module references.

### Intent boundary

- user/agent intents that SHOULD route to the capability;
- explicit negative or near-miss intent classes that SHOULD NOT route to it;
- expected actor/stakeholder;
- ambiguity/escalation behavior when intent cannot be resolved safely.

### Responsibility/cohesion

- concise responsibility statement;
- main reasons for change;
- capabilities normally co-used with it;
- capabilities that remain intentionally separate because their actor, authority, risk, permissions, context or change drivers differ.

This metadata operationalizes D050's SRP/cohesion rule without equating one responsibility with one command or one file.

### Authority and mutation surface

- authoritative state/documents read;
- project/source surfaces that may be mutated when separately authorized;
- explicit non-authority constraints;
- strategic/judgment boundaries that deterministic code MUST NOT invent.

### Permission and risk envelope

- filesystem scope;
- network/process/secret expectations where material;
- read-only versus mutation default;
- security/supply-chain risk class or controlling policy reference;
- host-specific permission notes clearly separated from portable semantics.

### Context routing

- minimum bootstrap/router context;
- focused references normally required for this capability;
- conditional/on-demand references;
- context that MUST NOT be loaded merely because the capability is active;
- related RCAB/TMC/RFO/ND/CAR evidence when available.

The source should optimize **load paths**, not file counts.

### Deterministic operations

- deterministic engine operations/commands used by the capability;
- required inputs/outputs when stable;
- explicit distinction between deterministic verifier/tool behavior and model-mediated judgment.

### Dependencies

- required shared engine/profile facilities;
- prerequisite capability/state relationships;
- optional external/project-native capabilities that may be reused under coexistence rules;
- prohibition on hidden mandatory third-party dependencies unless separately accepted.

### Evaluation ownership

- applicable deterministic acceptance properties;
- routing/behavioral eval classes;
- semantic negative-control families;
- D052 `Test-Authorship-Mode` or controlling test/eval contract when material;
- references to frozen corpora/graders rather than duplicated expected results.

### Distribution/projection metadata

- whether the capability is Consumer-visible, source-maintainer-only, or experimental;
- topology candidates allowed to aggregate/expose it;
- whether separation is only experimental pending T023 evidence;
- one-product/one-version invariants under D050/D051.

Projection metadata MUST NOT select the final topology before the applicable decision/eval gate.

## Current top-level capability families

The following families are the canonical topology-neutral starting point derived from the accepted Consumer and Maintainer functional contracts.

They describe semantic/routing clusters, **not final Skill boundaries**.

### `consumer.lifecycle`

Purpose: initialize, validate, reconstruct and operate Governance lifecycle/state inside a consumer repository while preserving source independence, progressive disclosure and project-native coexistence.

Current functional surface includes:

- bootstrap governance;
- validate installation;
- cold-start reconstruction;
- validate state;
- process handoff;
- validate protocol events;
- refresh checkpoint;
- initialize mission;
- archive completed mission;
- portability verification;
- validate sequential execution;
- inspect ecosystem coexistence.

Primary contract: `docs/GOVERNANCE-SKILL-CONTRACT.md`.

This family may be internally routed into smaller focused references, but those references are not automatically separate Skills.

### `consumer.skill-trust`

Purpose: discover external Skill candidates and evaluate exact artifact provenance/supply-chain suitability without treating discovery sources, directories, registries or host precedence as approval authority.

Current functional surface includes:

- discover Skill candidates;
- audit Skill supply chain;
- exact canonical source/revision/digest verification;
- dependency/permission envelope verification;
- runtime-selected/shadowed artifact identity checks.

Primary contracts/policies:

- `docs/GOVERNANCE-SKILL-CONTRACT.md`;
- `governance-core/SKILL-DISCOVERY.md`;
- `governance-core/SKILL-SUPPLY-CHAIN.md`.

D050 G3 may expose this family as `External Skill Trust` for experiment purposes. That does **not** pre-accept it as a separate release Skill.

### `source.maintenance`

Purpose: develop, refactor, test/evaluate and release the canonical Agent Governance source product while preserving repository role ownership, Task Contracts, branching/release policy and source-only overlays.

Primary contract: `docs/MAINTAINER-SKILL-CONTRACT.md`.

The family contains distinct internal role/context routes:

- `source.maintenance.orchestrator`;
- `source.maintenance.executor`;
- focused testing/eval/toolchain routes when applicable.

Those routes do not create new agent roles and do not imply top-level role Skills.

## Mapping to D050 topology candidates

The capability source must be able to project the same accepted semantics into each MG1/T023 candidate without rewriting capability meaning.

Conceptually:

```text
B0 unified dispatcher
    -> consumer.lifecycle
    -> consumer.skill-trust
    -> source.maintenance

B1 thin router
    -> same capabilities through focused progressive references

F2 generated profile peers
    Consumer Governance
        -> consumer.lifecycle
        -> consumer.skill-trust
    Source Maintainer
        -> source.maintenance

G3 hybrid challenger
    Consumer Lifecycle
        -> consumer.lifecycle
    External Skill Trust
        -> consumer.skill-trust
    Source Maintainer
        -> source.maintenance
```

MG1 may refine presentation metadata and experimental routing descriptions, but it MUST NOT change the underlying capability semantics merely to improve one candidate's score.

## Profile relationship

Profiles are runtime/permission contexts, not activation topology.

Current intended mapping is:

```text
consumer lifecycle / skill trust
    -> consumer profile

source maintenance
    -> source-maintainer profile
```

A capability definition MUST NOT bypass profile resolution or broaden a profile's permission envelope.

T021/T022 remain responsible for the engine/profile implementation sequence; this contract does not alter their executable scope.

## Progressive disclosure rule

The canonical capability source should make future generated routing surfaces smaller, not become another document that every task must preload.

Rules:

1. top-level Skill/host metadata identifies intent and routes to a capability family;
2. capability metadata points to the smallest focused reference set;
3. normative Core modules are loaded only when their rule surface is actually needed;
4. deterministic tooling replaces repeated mechanical validation prose;
5. source-maintainer policy stays out of normal Consumer context;
6. external Skill trust material stays out of normal Consumer lifecycle work unless a Skill discovery/audit concern exists;
7. generated projections MUST NOT duplicate the entire capability source into every entrypoint.

## D051 distribution relationship

Capability decomposition never changes the single-install product invariant.

Regardless of how many generated entrypoints expose the capability source:

```text
one Agent Governance Distribution vX.Y.Z
    -> one supported installation unit/bundle per target platform
    -> all selected generated entrypoints + shared engine/Core payload
```

A capability may be separately activated without becoming separately installed or independently versioned.

## D052 conformance relationship

For Skill/governance/documentation-managed semantic work, capability acceptance semantics may be projected into Orchestrator-owned conformance assets under D052.

The capability source SHOULD make those assets cheaper to author by providing a focused place to obtain:

- intent positives/negatives/near misses;
- profile/authority boundary;
- semantic negative-control families;
- expected routing ownership;
- controlling normative references.

However, conformance tests remain evidence. They are not capability authority.

## Authoring and change discipline

Capability-source changes are ChatGPT Orchestrator-owned source-product design work and follow normal Markdown branch/PR policy unless a later accepted decision introduces a deterministic structured source maintained under D052 or another explicit ownership rule.

A capability change MUST be classified before mutation.

### Metadata/routing clarification

No behavior change. Examples:

- improving intent wording;
- correcting a reference;
- making a context route more focused;
- documenting an already-accepted permission boundary.

### Capability semantic change

Potential behavior/product change. Examples:

- adding/removing a supported operation;
- broadening mutation authority;
- changing profile ownership;
- changing security/permission expectations;
- changing what constitutes a valid outcome.

These require the applicable Decision/Task Contract/Core changes before the capability source is updated.

### Projection/topology change

Changing which generated Skill exposes a capability is a topology/distribution concern. It does not alter capability semantics and follows D050/T023/T024 authority.

## Structured projection boundary

This Markdown contract establishes the canonical authoring model; it does **not** select a final machine-readable schema or require immediate duplication into JSON/YAML.

A later deterministic implementation may project capability metadata into structured build/eval inputs if that reduces ambiguity or context cost.

Any structured representation must satisfy:

- deterministic generation or one clearly designated editable source;
- no conflicting dual-edit authority;
- stable capability IDs;
- references back to controlling Core/contracts;
- reproducible identity/epoch metadata;
- no topology-specific mutation of capability semantics;
- generated copies are non-authoritative.

Until such a gate is accepted, this contract plus the referenced functional/Core contracts are the source-product authoring surface.

## Acceptance invariants

The capability-source architecture is acceptable only while all of these remain true:

1. `governance-core/` remains the only normative protocol authority;
2. capability metadata does not duplicate large normative rule bodies;
3. one capability source can feed B0/B1/F2/G3 without semantic forks;
4. capability IDs remain stable across equivalent projections;
5. Consumer and source-maintainer profile isolation is preserved;
6. `consumer.skill-trust` can be evaluated separately without being pre-accepted as a separate release Skill;
7. internal Maintainer role routes remain context routes, not new governance roles/top-level Skills;
8. D051 one-product/single-install semantics hold regardless of activation count;
9. D052 conformance ownership can reference capabilities without making tests authority;
10. progressive disclosure is improved or preserved rather than replaced by a mandatory monolithic capability document load;
11. no capability source introduces hidden network/provider/model/third-party dependencies;
12. final activation topology remains an MG1/T023 empirical decision.
