# R029-S10 — Candidate Topology and Pre-Decision Evaluation Plan

Status: COMPLETE  
Parent: `R029 — AGENTS.md / Skill Architecture Refactor Research`  
Subtask: `R029-S10 — Candidate-topology synthesis and evaluation plan`  
Baseline-Develop: `097a15a41326d914a07f3eb6122df8caa5194f4e`  
Inputs: accepted R029-S1 through R029-S9 artifacts  
Decision-State: EVALUATING  
Normative-Effect: none  
Analytical-Result: `CANDIDATE_TOPOLOGY_READY_FOR_HUMAN_DECISION`

## Purpose

Synthesize the accepted R029 analytical results into one bounded candidate instruction/Skill topology and define the evaluation plan that would be required before any normative adoption or implementation.

This artifact does **not** adopt the topology, rewrite `AGENTS.md`, create/package/install Skills, launch an Executor, consume provider/model calls, create scored observations, or authorize T066 work.

## Candidate topology

```text
Lean always-loaded AGENTS.md
│
├── Agent Governance Maintainer Skill
│   ├── Orchestrator route
│   └── Executor route
│
├── repository-change-control
│
├── upstream-version-revalidation
│
├── research-evidence-traceability
│
├── durable-work-checkpoint
│
└── executor-launch-handoff
    └── workspace-isolation   [internal route/reference]
         └── consumes repository-change-control / repository-local policy
             for branch/base/integration/retirement constraints

Supporting deterministic/reference layer
└── scripts / CI / local references / host adapters loaded only when needed
```

This is a candidate topology only. A later Human decision is required before any element becomes normative.

## Layer 1 — lean always-loaded root

The future root should retain only responsibilities that must be known **before** optional routing can occur safely.

The root responsibility surface remains the S2 twelve-family contract:

1. repository identity and contamination boundary;
2. authority model and host neutrality;
3. write/file ownership boundary;
4. SDD stage and re-entry safety boundary;
5. semantic-vs-execution boundary and Human gate;
6. durable authority over ephemeral/private context;
7. bootstrap and routing anchors;
8. repository mutation/branch safety;
9. durable handoff/completion boundary;
10. research/evidence non-authority and freshness triggers;
11. Skill independence/coexistence boundary;
12. instruction architecture/change-discipline guardrail.

The root is therefore not a pointer-only file. It must preserve pre-routing identity, authority, safety, bootstrap and concise dispatch triggers while moving conditional procedure out of the always-loaded surface.

S1 coverage remains mandatory: all 79 audited semantic units must remain represented as `ROOT`, `ROOT+ROUTE`, or reachable routed detail. No semantic unit is authorized for deletion merely because the topology is leaner.

## Layer 2 — Agent Governance Maintainer Skill

The existing approved source-maintenance architecture remains:

```text
Maintainer Skill
  -> Orchestrator route
  -> Executor route
```

The Maintainer Skill remains the project-owned source-maintenance domain entry point. R029 does not split it into separate role-named top-level Skills.

Agent-Governance-specific material stays here or in its references/adapters, including:

- product/source-vs-consumer identity and canonical paths;
- D052/D053/D068/D076 ownership and SDD lifecycle;
- Task Contracts, Stage 5 candidate publication, Stage 6 handoff and Stage 7 acceptance semantics;
- exact checkpoint schema/lifecycle;
- `Rxxx`/`Dxxx`, Research-State/Decision-State and research-to-decision promotion rules;
- `main`/`develop`, release/hotfix and source-specific branch policy;
- testing/evaluation/supply-chain architecture;
- local source-maintainer toolchain policy;
- all Agent Governance adapters for transverse capabilities.

A transverse capability can structure a reusable workflow, but never supersedes repository policy, Task Contract authority, stage ownership, write ownership, semantic-oracle ownership or acceptance authority.

## Layer 3 — retained transverse candidates

### `repository-change-control`

Intent: control an authorized repository mutation path while preserving protected-target safety, reviewability, durable provenance and repository-local policy.

It is not generic Git help. Agent Governance continues to provide exact branch names, D061/D062 freshness, D068 publication semantics, L007, release flow and role/write ownership.

### `upstream-version-revalidation`

Intent: before consequential reliance on version-sensitive external behavior, compare the exact relied-on version against current/higher relevant upstream state and classify whether the historical assumption remains valid.

It supplies evidence/disposition structure, not upgrade or qualification authority. D077/D063/project pins and launch consequences stay domain-side.

### `research-evidence-traceability`

Intent: preserve consequential evidence with reconstructable provenance, freshness, uncertainty and separation between evidence, inference/recommendation and accepted authority.

It does not own Agent Governance `Rxxx`, `Dxxx`, ledger schema or Decision-State transitions.

### `durable-work-checkpoint`

Intent: persist the minimum authoritative frontier required for cold-start-safe resumption without private conversational memory.

It is not a transcript. Agent Governance retains exact `CHECKPOINT.md`, `Oxxx`, D027/D067, Human gates, effort/shape fields and source-maintenance bootstrap semantics.

### `executor-launch-handoff`

Intent: bind a concrete delegated executor/session to persisted authority, establish a fresh safe baseline, transport only minimal routing context, and require a durable return identity/evidence channel.

It is not a Task Contract generator, model router, command runbook, executor methodology or acceptance authority. Agent Governance retains D055/D060/D054/D068/D076 and exact handoff schemas.

#### Internal `workspace-isolation` route/reference

S9 places workspace isolation inside `executor-launch-handoff`, not as another top-level Skill.

Its reusable concern is delegated writable-work attribution and collision prevention. It consumes `repository-change-control`/repository-local policy when branch/base/integration/retirement semantics are needed.

This placement intentionally avoids Skill proliferation and duplicate routing.

## Progressive-disclosure model

The topology should use progressive disclosure in this order:

```text
always-loaded root
    -> select Agent Governance domain and/or transverse intent
    -> load only the selected Skill metadata/instructions
    -> load domain adapter/reference only when repository-specific semantics are required
    -> load deterministic script/reference/tool detail only when mechanics require it
```

The same semantic capability should normally serve ChatGPT and Codex/other Executors. Host-specific UI, API, Git, session, browser or CLI mechanics belong in adapters/references rather than separate top-level Skills unless later evidence demonstrates genuinely different intent or permission boundaries.

## Cross-capability dispatch rules

### Volatile external fact

```text
version-specific external behavior materially controls decision
    -> upstream-version-revalidation

non-version-specific consequential evidence/fact freshness
    -> research-evidence-traceability
```

When both apply, version revalidation owns exact release/behavior comparison while evidence traceability owns broader provenance/persistence. Neither acquires normative decision authority.

### Repository mutation plus delegated Executor

```text
repository mutation path
    -> repository-change-control

delegated execution transport/session/return
    -> executor-launch-handoff

writable workspace collision/attribution
    -> executor-launch-handoff / workspace-isolation internal route

branch/base/integration/retirement policy needed inside that route
    -> consume repository-change-control or repository-local adapter
```

### Resumption versus executor return

`durable-work-checkpoint` owns the orchestrator/resumer frontier. `executor-launch-handoff` owns the delegation boundary and result pointer. They may reference each other but should not duplicate state ownership.

## Anti-sprawl rules

A future Skill should not be created merely because a topic is reusable-looking. A top-level transverse Skill should require all of:

1. a distinct semantic intent;
2. clear positive and negative triggers;
3. a concrete postcondition;
4. reusable value after removing Agent Governance names/IDs/stages/paths;
5. an authority-safe boundary;
6. sufficient distinction from existing candidates to justify routing/context overhead.

The candidate topology explicitly rejects top-level generic Skills such as `coding`, `testing`, `pytest`, `TDD`, `git-commands`, `Markdown-editing`, generic `branching`, separate `Orchestrator`/`Executor` Skills, and standalone workspace-isolation.

## Candidate architecture invariants

Any later adopted form must preserve all of the following:

- Git/persisted repository state remains canonical authority;
- Skills are routing/context mechanisms, never authority sources;
- root pre-routing safety cannot depend on successful Skill activation;
- the Maintainer Skill remains one project-owned source-maintenance Skill with internal role routes unless a separate explicit decision changes that contract;
- host identity never grants governance authority;
- no capability may silently invent task/spec/design/acceptance/ownership authority;
- no-Skill bootstrap and deterministic repository operation must remain possible;
- repository-local policy overrides generic defaults;
- ambiguous authority/state fails closed;
- source-product and consumer-project activation domains remain separated.

## Pre-decision evaluation plan

No evaluation is executed by R029-S10. This section defines the future evidence required before the Human should adopt the topology.

### E1 — semantic preservation audit

**Goal:** prove root slimming does not lose current semantics.

Method:
- map every S1 semantic unit to its proposed future carrier;
- require exactly one authoritative destination plus explicit trigger/reference edges where necessary;
- verify all 79 units remain covered;
- reject any topology with an uncovered unit or duplicated competing authority.

Must-pass:
- `79/79` covered;
- `0` delete-without-replacement;
- `0` ambiguous authority destinations.

### E2 — root pre-routing safety audit

**Goal:** verify the lean root alone is sufficient to avoid unsafe routing/mutation before any Skill loads.

Test cases should cover:
- repository identity/source-vs-consumer confusion;
- Human/Orchestrator/Executor authority;
- write ownership;
- SDD re-entry/stop conditions;
- protected/direct-write restrictions;
- durable authority over chat/private context;
- Skill-is-not-authority rule;
- missing/failed Skill availability.

Must-pass: every unsafe case stops or routes safely without requiring hidden conditional context first.

### E3 — Skill routing evaluation

Build explicit, implicit/contextual and negative prompts for each retained transverse candidate plus Maintainer routing.

Required classes:
- clear positive trigger;
- paraphrased/implicit positive trigger;
- contextual trigger where relevant intent is inferred from current work;
- near-neighbor negative trigger;
- generic-topic negative trigger;
- overlapping multi-capability case requiring bounded composition.

Measure later:
- correct Skill selection;
- false-positive activation;
- false-negative non-activation;
- unnecessary multi-Skill activation;
- route stability across host adapters.

### E4 — authority-leakage / adversarial evaluation

Construct prompts attempting to make a transverse capability:
- invent task scope or acceptance criteria;
- override repository-local branch policy;
- upgrade a dependency merely because newer exists;
- convert research evidence into accepted Decision authority;
- accept Executor results from chat-only evidence;
- bypass Human gates;
- reinterpret Agent Governance stage ownership;
- use host/model/session identity as authority.

Must-pass: capability refuses/escalates/routes to controlling domain authority.

### E5 — progressive-disclosure and context-efficiency evaluation

Compare the current root baseline with a later candidate implementation using the same representative task set.

Measure:
- always-loaded root size;
- Skill catalog/description footprint;
- conditional context loaded per task;
- irrelevant instruction exposure;
- duplicate instruction exposure;
- number of routing hops;
- whether required context can be reached without broad history loading.

The target is not a fixed token quota in R029. Success means materially lower irrelevant always-loaded context without loss of correctness, safety or reconstructability.

### E6 — cross-host portability evaluation

Run equivalent semantic cases through ChatGPT and at least one Executor adapter when later authorized.

Verify:
- same intent/postcondition classification;
- host-specific mechanics remain adapter-only;
- no separate role/host Skill becomes necessary merely because tooling differs;
- repository authority and fail-closed behavior remain identical.

Provider/model selection is not part of the semantic topology score and requires separate authorization/qualification if studied.

### E7 — no-Skill bootstrap/degradation evaluation

Verify repository operation remains safe when:
- no optional transverse Skill is installed/available;
- Skill metadata fails to load;
- host does not support a convenience feature;
- deterministic scripts/CI execute without model Skill activation.

Expected result: reduced convenience/context efficiency is acceptable; authority or safety degradation is not.

### E8 — composition/non-overlap evaluation

Exercise the main seam cases:
- repository change + executor launch + workspace isolation;
- version revalidation + research traceability;
- executor return + durable checkpoint;
- Maintainer domain adapter + transverse workflow.

Must-pass:
- one clear owner per semantic concern;
- references rather than duplicated authority;
- no routing loops;
- no unnecessary standalone activation of workspace isolation;
- final acceptance remains domain/Human-owned.

### E9 — maintainability / change-locality evaluation

Simulate representative policy changes and determine where edits would be required:
- Agent Governance branch naming change;
- provider model-name change;
- D077 disposition wording change;
- checkpoint schema change;
- generic upstream revalidation improvement.

Desired property:
- domain-specific changes remain localized to Maintainer/adapters;
- generic workflow improvements remain localized to transverse capability;
- root changes occur only when a pre-routing invariant/trigger changes.

## Evaluation corpus structure

A later evaluation suite should include at minimum:

```text
maintainer-domain positives and negatives
repository-change-control positives / near-neighbor Git negatives
upstream-version-revalidation positives / generic-update negatives
research-evidence-traceability positives / simple-search negatives
durable-work-checkpoint positives / summarization-note negatives
executor-launch-handoff positives / local-helper negatives
workspace-isolation contextual positives / standalone-routing negatives
cross-capability composition cases
authority-adversarial cases
no-Skill degradation cases
```

Each case should define expected route(s), prohibited route(s), required authority source, required postcondition and any fail-closed expectation. Trace evaluation should inspect routing decisions and loaded context, not only final prose.

## Decision criteria after evaluation

A later Human adoption decision should require evidence that the candidate topology:

1. preserves all current required semantics;
2. materially reduces irrelevant always-loaded context;
3. improves or preserves routing precision;
4. does not create authority leakage or new ambiguous ownership;
5. keeps Agent Governance-specific policy localized;
6. avoids top-level Skill proliferation;
7. remains host-neutral at semantic level;
8. preserves no-Skill safe operation;
9. has a maintainable change-locality profile;
10. has no unresolved must-pass failures in preservation/safety/authority tests.

If those conditions are not met, the Human should reject or revise the topology rather than implementing it merely because individual candidates looked reusable.

## Recommended decision options

At the Human Decision Gate, R029 supports three legitimate next dispositions:

- `ADOPT_FOR_DESIGN` — accept the candidate topology as the architecture direction and authorize a separate normative Decision/design/implementation objective;
- `REVISE_AND_REEVALUATE` — keep R029 evidence but change one or more topology assumptions before adoption;
- `REJECT_TOPOLOGY` — retain current architecture until a different proposal is justified.

R029 itself does not select among these options.

## R029 completion assessment

S10 satisfies its analytical gate:

- S1-S9 results are reconciled into one bounded candidate topology;
- lean-root, Maintainer/domain, five transverse candidates and S9 internal workspace route have explicit relationships;
- progressive disclosure and host-adapter boundaries are explicit;
- anti-sprawl/non-overlap rules are explicit;
- a pre-decision evaluation plan covers preservation, routing, authority, context efficiency, portability, degradation, composition and maintainability;
- no architecture adoption, root rewrite, Skill implementation, Executor/provider/model call, scored observation or T066 mutation occurred.

R029 research/evaluation is therefore complete and must stop at the Human Decision Gate.