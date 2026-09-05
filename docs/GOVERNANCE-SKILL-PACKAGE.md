# Agent Governance Skill Package Design

Status: DESIGN-APPROVED  
Controlling decisions: D044, D050, D051, D062

## Goal

Define one **Agent Governance Distribution** over one canonical Governance Core, one shared deterministic engine and one canonical capability source.

The distribution may expose one or multiple generated Agent Skill entrypoints after T023 selects the activation topology. Those entrypoints are routing/packaging projections of one product and are not independently maintained Governance products.

For Consumer use, D051 requires **single-install / self-bootstrap** behavior: installing the Agent Governance distribution once must provide every Agent-Governance-owned reusable artifact needed to bootstrap and normally operate a governed repository. The user must not manually assemble additional Agent Governance Core/runtime/template/schema/Skill support packages.

D062 additionally requires the installed Consumer distribution to carry portable long-lived-branch protection bootstrap guidance so an adopting repository does not need to read this source checkout to learn the writable-readiness invariant.

## Architectural units

```text
governance-core/                 canonical normative authority
        |
        v
shared deterministic engine     one implementation of common semantics
        |
        v
canonical capability source     profiles / intents / routing / references
        |
        v
deterministic build
        |
        +--> selected generated Skill entrypoint(s)
        +--> Core snapshot
        +--> runtime
        +--> templates/assets/schemas
        +--> identity/provenance metadata
        |
        v
Agent Governance Distribution vX.Y.Z
```

The current source tree may retain historical `governance-skill/` and `maintainer-skill/` paths until the D044/D050 migration program retires obsolete independently-maintained-product assumptions. Source layout is not final distribution authority.

## Reusable Product Source

Current and prospective product source includes conceptually:

```text
agent-governance/
├── governance-core/                  # canonical protocol authority
├── src/agent_governance/             # shared deterministic engine
├── governance-skill/                 # current Consumer-facing source/legacy entrypoint surface
├── maintainer-skill/                 # current/planned source-maintainer surface until migration
├── tests/
├── evals/
└── deterministic build/projection tooling
```

D050 requires the steady-state authoring model to converge on one canonical capability/source model capable of generating the accepted activation topology. No generated Skill may become a second normative Core or independently maintained runtime fork.

## Distribution boundary

A released Agent Governance distribution must be self-contained for the supported operations of its selected topology.

It contains, as applicable:

- generated Skill entrypoint(s) and focused references;
- the shared deterministic runtime/engine;
- a generated, traceable Consumer Core snapshot;
- bootstrap templates/assets, including portable repository writable-readiness/branch-protection guidance;
- deterministic schemas/configuration required by runtime/package operation;
- product, topology, protocol, installed-footprint compatibility and provenance metadata.

Every generated entrypoint belongs to the same `Agent Governance Distribution vX.Y.Z` and is traceable to the same accepted capability-source/Core/engine/source/build identities.

The distribution MUST NOT require a Consumer to fetch runtime dependencies from the Agent Governance source checkout after installation.

## Single-Install / Self-Bootstrap Rule

For each supported Consumer release-target platform:

```text
install Agent Governance once
        |
        v
bootstrap <consumer-project>
        |
        +--> .agent-governance/
        +--> .agent-coordination/
        |
        v
validate / operate
```

After the Agent Governance distribution is installed, Consumer bootstrap MUST NOT require the user to separately install or copy another Agent Governance Skill, Core archive, runtime package, template bundle, schema bundle or source checkout.

Normal bootstrap from an installed release MUST resolve Agent-Governance-owned reusable material from inside that distribution and MUST NOT require a network fetch of missing Agent Governance payload files.

Repository-provider administration required to protect the adopting repository's own branches is project infrastructure, not a second Agent Governance installation dependency. The distribution must nevertheless carry the guidance needed to perform/verify the invariant without accessing this source repository.

If the selected topology exposes several generated Skills, the supported platform wrapper/bundle must install them as one Agent Governance product unit. Users are not expected to discover and independently install each generated Agent Governance entrypoint.

A platform whose packaging model cannot satisfy this invariant is not silently treated as a supported D051 release target; T024 must stop/escalate for an explicit product decision.

## Installed Consumer Project Footprint

Bootstrap materializes durable project authority/state inside the governed repository:

```text
.agent-governance/
├── GOVERNANCE.md
├── CONTEXT.md
├── ADAPTERS.md
├── LIFECYCLE.md
├── COEXISTENCE.md
├── EXECUTION.md
├── PROTOCOL.md
├── HANDOFF.md
├── SKILLS.md
├── SKILL-DISCOVERY.md
└── SKILL-SUPPLY-CHAIN.md

.agent-coordination/
├── MISSION.md
├── WORKPLAN.md
├── CAPABILITIES.json
├── STATE.json
├── EXCHANGE.jsonl
├── tasks/
├── skills/
└── decisions/
```

The exact current footprint remains controlled by the Governance Core and accepted migration/version policy. The layout above is the design baseline, not permission to bypass those contracts.

`CAPABILITIES.json` is a compact coexistence/routing inventory, not authority and not a duplicate SDD/Skill catalog. It records only material capability providers/classifications and references under `COEXISTENCE.md`/`PROTOCOL.md`.

Product adapters such as `AGENTS.md`, `opencode.json`, Codex/Claude/other native instructions remain project/tool-specific and are not task semantics. Existing third-party managed files MUST be composed non-destructively or left untouched under `COEXISTENCE.md`.

The installed project footprint is **not** a second package dependency. It is the durable governed-repository authority/state created by bootstrap.

## Progressive Materialization

The distribution may contain reusable templates for many record types, but bootstrap installs only the durable baseline required for a valid governed repository.

Demand-driven records are created only when needed, including concrete:

- task records;
- decisions;
- approved external Skill records;
- capability inventory entries;
- archival records.

Future task detail stays outside WORKPLAN and MUST NOT be pre-materialized merely because templates exist in the distribution.

## Consumer Capability Surface

Purpose: install, bootstrap, validate, operate, recover, hand off, audit, archive and coexist safely with existing project SDD/Skill/tooling capabilities inside an adopting repository.

Controlling contract: `docs/GOVERNANCE-SKILL-CONTRACT.md`.

The final activation presentation is selected by D050/T023. Consumer operations may appear behind one unified router or a generated Consumer-specific entrypoint, but their protocol/runtime semantics remain shared/canonical.

### Consumer routing surface

The Consumer routing surface provides activation, operational routing, non-authority invariant, source-independence, coexistence routing, mutation/read safety and deterministic-tooling routing.

Rules:

- minimal compatible frontmatter/metadata;
- reference/load canonical generated Core content progressively rather than restating all protocol prose in the entrypoint;
- use governance roles, not vendor identities;
- trigger for governance/coordination operations, not generic SDD/planning/testing;
- route to `COEXISTENCE.md` only when existing project capabilities may overlap;
- route to packaged repository branch-protection guidance only during bootstrap/writable-readiness work where branch/PR protection is material;
- never embed source-product maintenance workflow, project state or future task content;
- keep the activation/routing body deliberately small and measured under the applicable T023 context/eval evidence;
- do not require read/write access to the canonical source repository after installation.

### Bootstrap assets

Reusable assets include conceptually:

- `MISSION.template.md` — strategic objective/scope skeleton;
- `WORKPLAN.template.md` — gates, deterministic execution-order metadata and task pointers only;
- `TASK.template.md` — agent-neutral atomic task objective/scope/dependencies/acceptance/Skills/constraints plus references to controlling native project artifacts when required;
- `SKILL-APPROVAL.template.json` — discovery source + exact canonical artifact provenance/revision/digest/risk/permission/dependency approval record;
- `CAPABILITIES.template.json` — compact capability/provider/coexistence classifications and decision references;
- `STATE.template.json` — constant-size frontier;
- `EXCHANGE.template.jsonl` — role-based event seed;
- `REPOSITORY-BRANCH-PROTECTION.md` — portable provider-neutral writable-readiness invariant with a GitHub adapter example and verification/receipt guidance.

Rules:

- placeholders only where the asset is a template; operational guidance may define portable safety invariants and provider-adapter examples;
- future task detail stays outside WORKPLAN;
- native SDD/spec content is referenced instead of copied when it remains the project's source;
- Skill approval records pin immutable audited artifacts;
- bootstrap never silently overwrites existing state or third-party managed files;
- bootstrap must not claim remote branch protection is configured unless effective provider state was actually verified;
- templates/assets are bundled with the Agent Governance distribution and are not separately installed by the user.

### Deterministic Consumer command surface

The current Consumer v1 deterministic surface includes:

- `bootstrap` — safely create Core/instance/task/Skill-record/capability-inventory structure after coexistence preflight;
- `validate` — validate layout, references, context budgets, versions, adapters, STATE, WORKPLAN sequence, coexistence inventory, Skill approval records and EXCHANGE coherence;
- `state` — derive/check/refresh frontier checkpoint;
- `event` — validate role actors, EXCHANGE events/state transitions and DONE dependency semantics;
- `skill` — support candidate source resolution/inventory and validate canonical-source/approval-record/revision/digest/permission/dependency/host-selection matching; MUST NOT decide strategic approval;
- `ecosystem` — inspect mechanically detectable project capability evidence/collisions and maintain compact CAPABILITIES structure; MUST NOT choose semantic authority winners;
- `archive` — validate/prepare mission archival without destroying history.

The exact CLI evolves only through its accepted contract/migration gates.

The current deterministic CLI does not implicitly gain repository-provider administration merely because D062 exists. Remote branch/ruleset administration and effective-state reads require supported provider/project surfaces and Human authority as applicable.

Rules:

- read-only validation by default;
- explicit mutation only;
- no production/external services required for Governance itself;
- no strategic decisions in scripts;
- no blind replacement of third-party managed agent/SDD/Skill files;
- directory/registry install commands are never executed during discovery;
- candidate external Skill acquisition/inspection uses quarantine before active installation.

## Source-Maintainer Capability Surface

Purpose: develop, refactor, test/evaluate and release the canonical source repository only.

Controlling contract: `docs/MAINTAINER-SKILL-CONTRACT.md`.

A selected topology may expose Source Maintainer as a generated peer Skill or route it through a shared dispatcher. In either case it remains part of the same Agent Governance product/capability source/engine identity.

Source-maintainer routing MAY use source-specific paths/workflows such as `AGENTS.md`, `docs/DEVELOPMENT-WORKFLOW.md`, `docs/REFACTORING-WORKFLOW.md`, `docs/BRANCHING.md`, `docs/RELEASES.md`, Decision Records, product source, tests and evals.

It MUST NOT:

- install a live Consumer `.agent-coordination/` instance in the Agent Governance source repository;
- broaden into ordinary Consumer governance;
- duplicate Consumer operation instructions as a second authority;
- redefine ChatGPT Orchestrator / Agente de IA Ejecutor authority;
- bypass topic-branch/PR or release rules.

Shipping a source-maintainer entrypoint in the same product distribution does not authorize copying source-maintenance overlays/history/state into an ordinary Consumer project footprint.

## Shared Implementation Rule

If multiple generated Skills require the same deterministic implementation, use the shared engine rather than duplicated code.

Shared code does not require identical activation descriptions, contexts or permission envelopes.

Generated entrypoint separation does not create separately versioned product components.

## External Skill / Project-Native Boundary

D051 covers Agent-Governance-owned product payload.

Agent Governance does not bundle arbitrary project-native SDD/testing/memory/tooling or third-party Skills merely to avoid all external dependencies in the abstract.

Instead:

- existing project-native capabilities are reused/adapted/coexisted with under `COEXISTENCE.md`;
- external Skills are separately discovered, audited and approved under `SKILL-DISCOVERY.md` / `SKILL-SUPPLY-CHAIN.md`;
- optional external capabilities are not hidden prerequisites for basic Agent Governance operation.

Repository-provider branch protection is a project infrastructure control and is handled through the provider/project's own administration surface. Agent Governance packages the required invariant/guidance, not the provider itself.

## Test/Eval Separation

At minimum maintain distinguishable coverage for:

### Core

- deterministic protocol/layout/reference/state/capability-inventory invariants;
- coexistence classifications and conflict fail-closed behavior.

### Consumer

- single-install/self-bootstrap from installed distribution only;
- bootstrap/install/overwrite refusal;
- cold-start/recovery;
- state/event validation;
- context budgets;
- sequential disclosure;
- Skill discovery/supply-chain controls;
- existing Skill host-selection/shadowing checks;
- SDD/Skill/tool coexistence and managed-file preservation;
- repository long-lived-branch writable-readiness protection detection/gating without assuming one provider;
- source-repository independence;
- source-maintainer overlay exclusion;
- positive/negative/near-miss Consumer activation.

### Source Maintainer

- source-product activation vs Consumer near misses;
- ChatGPT Orchestrator / Agente de IA Ejecutor role routing;
- PD/RF workflow routing;
- branch-policy routing;
- release preparation;
- refusal to create a live Consumer instance in the source repository.

### Distribution

- selected topology reproducibility;
- one Agent Governance distribution identity/version across all entrypoints;
- clean one-install bootstrap on every supported release-target packaging path;
- packaged repository branch-protection guidance available without source-checkout access;
- no out-of-band Agent Governance support files after installation;
- artifact/source isolation;
- explicit update-vs-project-migration separation.

No production/external services are required for release-only tests.

## Deliberately Excluded

Do not add without evidence/decision:

- independently maintained Consumer/Maintainer Governance products;
- independently versioned generated entrypoints;
- a replacement SDD methodology bundled into Governance;
- a generic Skill registry/memory/testing ecosystem bundled merely for convenience;
- duplicate prose reference layers;
- multiple overlapping deterministic runtimes;
- mandatory Skill-to-Skill invocation;
- MCP/network dependencies for Governance itself;
- destructive rewrite of project-native/third-party managed instruction files;
- decorative assets;
- domain-specific sample projects;
- Consumer dependence on a floating source checkout;
- post-install manual download/copy of Agent-Governance-owned support payload.

## Release Gate

Before releasing the selected topology, define and validate:

1. exact trigger corpus and activation descriptions;
2. context-routing contract and progressive disclosure;
3. mutation/read and permission boundaries;
4. focused tests/evals and near-miss separation;
5. deterministic topology/package generation;
6. one Agent Governance product/version/provenance identity;
7. D051 one-install/self-bootstrap journey for every supported Consumer release-target packaging path;
8. source-independence, packaged repository-protection bootstrap guidance and source-maintainer-overlay exclusion;
9. explicit upgrade/project-migration lifecycle;
10. Consumer v1 rollback evidence.

Final release promotion remains Human-authorized under `docs/RELEASES.md`.