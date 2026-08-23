# Native SDD Adoption Plan

Status: ACTIVE  
Date: 2026-08-23  
Authority: accepted `D053`  
Scope: Agent Governance source product and governed consumer projects

## Purpose

Operationalize the accepted native Spec-Driven Development architecture without installing OpenSpec, Spec Kit, Kiro or another external SDD framework, without creating a parallel lifecycle, and without restoring dual ownership inside any SDD stage.

This plan is the first `Plan & Trace` artifact under D053. Adoption is incremental and brownfield-safe.

## SDD profile

Adoption is `ASSURED` because it changes Governance protocol, source-development authority, consumer-project workflow and potentially durable bootstrap/package semantics.

The profile increases specification, trace and conformance depth; it does not transfer stage ownership.

## Accepted stage ownership

```text
1 Explore / Frame           -> Orchestrator
2 Specify                   -> Orchestrator
3 Design                    -> Orchestrator
4 Plan & Trace              -> Orchestrator
5 Implement                 -> Executor, only when Executor-owned technical implementation exists
6 Code Review & Verify      -> Executor, only for that technical implementation
7 Converge/Accept/Evolve    -> Orchestrator
```

No adoption work may create a second Design, Plan or acceptance authority inside Executor tooling or host-native SDD state.

## Current specification carriers

The adoption work treats accepted/current artifacts as specification carriers rather than duplicating them wholesale:

- `docs/decisions/D053-native-spec-driven-development.md` — accepted native SDD architecture and stage ownership;
- `governance-core/SDD.md` — reusable consumer-native SDD semantics added by A1;
- `AGENTS.md` — source-repository role/write/workflow adapter;
- `governance-core/GOVERNANCE.md` — reusable Core router/authority entry point;
- `governance-core/LIFECYCLE.md` — consumer preimplementation lifecycle;
- `governance-core/QUALITY.md` — engineering quality envelope;
- `governance-core/COEXISTENCE.md` — project-native capability/SDD coexistence;
- `governance-core/EXECUTION.md` and `governance-core/HANDOFF.md` — consumer implementation/review/convergence routing;
- `governance-core/PROTOCOL.md` and `governance-core/CONTEXT.md` — durable state/event/context semantics;
- `docs/DEVELOPMENT-WORKFLOW.md` — source-product PD lifecycle;
- `docs/TASK-CONTRACTS.md` — durable source execution-contract/trace semantics;
- `docs/EXECUTOR-HANDOFFS.md` — Executor implementation/review evidence boundary;
- `docs/decisions/D041-executor-process-autonomy.md` — Executor private-process autonomy;
- `docs/decisions/D052-specification-owned-conformance-test-authorship.md` — semantic conformance ownership.

D053 supersedes conflicting earlier wording prospectively. Existing historical records are not rewritten merely to attach SDD terminology.

## Adoption delta

### ADDED

- native SDD is a built-in Agent Governance capability when no adequate project-native SDD provider is primary;
- every applicable development change receives proportionate SDD coverage;
- explicit single-owner stages;
- current-spec carrier identification;
- `ADDED / MODIFIED / REMOVED / PRESERVED` change-delta semantics;
- requirement-to-Design-to-plan-to-implementation-to-evidence traceability;
- Executor `Code Review & Verify` as a distinct technical stage;
- Orchestrator `Converge / Accept / Evolve` as the acceptance stage;
- explicit re-entry when implementation/review evidence exposes an upstream specification/Design/Plan defect.

### MODIFIED

- source PD0-PD6 maps exactly to accepted D053 ownership;
- consumer F0-F6/readiness makes Orchestrator specification/Design/Plan completeness explicit;
- D041 process autonomy is bounded inside Executor stages 5-6;
- coexistence reuses/adapts project-native SDD while preserving Agent Governance stage ownership;
- Task Contracts and handoffs carry enough trace/review evidence for convergence without becoming a second SDD system.

### REMOVED

- `no-SDD` as the normal fallback when no adequate external/project-native provider exists;
- wording that gives Executor authoritative SDD Design/Plan ownership;
- wording that conflates Executor technical verification/review with Orchestrator semantic acceptance;
- any need to install a third-party SDD product for native coverage.

### PRESERVED

- Human Owner remains final authority;
- Git remains canonical durable project state;
- existing F0-F6 and PD0-PD6 lifecycles remain the lifecycle skeletons;
- D052 conformance assets remain evidence projections, never authority;
- D041 still allows private Executor tools/plans/sub-agents inside stages 5-6;
- committed Markdown ownership remains Orchestrator-controlled under repository policy;
- external/project-native SDD is reused/adapted instead of duplicated when adequate;
- brownfield adoption remains delta-first with no full historical backfill;
- Agent Governance remains executor-product neutral and single-install/self-bootstrap compatible.

## Controlling design

### 1. Semantic overlay, not a third lifecycle

Native SDD is expressed through existing lifecycle stages and durable artifacts. Agent Governance SHALL NOT create a second independent workflow queue, separate authority graph or mandatory vendor-style directory tree merely to resemble OpenSpec or Spec Kit.

### 2. Existing artifacts first

An existing normative artifact may be the current specification carrier. A separate spec file is created only when it adds durable value and does not duplicate current truth.

### 3. Proportional materialization

`COMPACT`, `STANDARD` and `ASSURED` control how much durable SDD material is required. They never change stage ownership.

### 4. Consumer portability

Native SDD semantics that governed consumer projects need live in reusable Governance Core/product distribution, not only in source-maintenance docs. A1 therefore adds `governance-core/SDD.md` and routes it from the existing Core rather than creating source-only SDD authority.

### 5. Source/consumer separation

Source-product Task Contracts and Orchestrator checkpoints remain source-only. Consumer projects use their installed Governance Core and coordination records; source-maintenance artifacts must not leak into consumer bootstrap.

### 6. No mandatory external SDD runtime

OpenSpec, Spec Kit, Kiro and similar systems remain research/coexistence providers only. Native SDD works from Agent Governance's own distributed artifacts and the governed repository.

### 7. Conformance follows semantic ownership

Where machine-verifiable semantics are required, D052 applies. Orchestrator authors the semantic oracle when appropriate; Executor technical work runs it and supplies evidence; Orchestrator accepts or rejects convergence.

## Adoption sequence

### A1 — Semantic protocol adoption

Owner: **Orchestrator**  
Change class: Markdown/policy  
Executor: **not used**  
State: **AUTHORED — pending PR integration**

A1 was authored on `docs/sdd-a1-semantic-protocol` from the accepted D053 baseline. It updates the smallest coherent normative surface needed to remove known contradictions and introduces one focused reusable SDD Core module.

A1 changed:

- `governance-core/SDD.md` — new reusable native SDD method;
- `AGENTS.md` — source role/workflow adapter;
- `governance-core/GOVERNANCE.md` — router/authority and mandatory-lifecycle integration;
- `governance-core/LIFECYCLE.md` — F0-F6 specification/Design/Plan ownership and readiness;
- `governance-core/COEXISTENCE.md` — native SDD fallback and external-provider reuse;
- `governance-core/EXECUTION.md` — Executor Implement + Code Review & Verify semantics;
- `governance-core/HANDOFF.md` — review evidence and Strategy convergence/re-entry;
- `governance-core/CONTEXT.md` — focused/lazy SDD loading and no duplicate spec truth;
- `governance-core/ADAPTERS.md` — product-neutral single-owner stage mapping;
- `governance-core/PROTOCOL.md` — DONE vs ACCEPTED and SDD blocker/event semantics;
- `docs/DEVELOPMENT-WORKFLOW.md` — exact PD0-PD6 SDD mapping;
- `docs/TASK-CONTRACTS.md` — source SDD profile/carrier/delta/Design/trace contract;
- `docs/EXECUTOR-HANDOFFS.md` — Code Review & Verify/requirement-trace evidence;
- `docs/decisions/D041-executor-process-autonomy.md` — private autonomy bounded inside stages 5-6;
- `docs/decisions/D052-specification-owned-conformance-test-authorship.md` — test authorship aligned with single-owner Design/acceptance;
- `governance-skill/SKILL.md` — consumer governance routing for installed native SDD;
- `governance-skill/assets/TASK.template.md` — proportionate SDD task fields.

`governance-core/QUALITY.md`, `governance-core/ASSURANCE.md` and `governance-core/EXECUTION-CONTROL.md` were inspected and do not require A1 edits: their existing Strategy-owned quality/design/authorization semantics already compose with D053.

A1 acceptance requires:

1. one accountable owner per SDD stage everywhere normative;
2. Orchestrator owns Explore, Specify, Design, Plan & Trace and Converge/Accept/Evolve;
3. Executor ownership is limited to technical Implement plus Code Review & Verify for Executor-owned implementation;
4. no normative text requires the Executor to reconstruct missing specification/Design/Plan authority;
5. native SDD is the fallback when no adequate project-native SDD provider exists;
6. project-native SDD can be reused/adapted without duplicate authority;
7. `ADDED / MODIFIED / REMOVED / PRESERVED`, proportional profiles and re-entry semantics are representable without forcing a new file for each stage;
8. no source-only state is introduced into the consumer footprint;
9. historical Task Contracts are not rewritten solely for SDD labels.

A1 is complete only after its full Markdown diff is reviewed and integrated into `develop`.

### A2 — Executable enforcement/materialization decision

Owner: **Orchestrator**  
Change class: design + Task Contract/conformance gate if executable work is required

After A1 integration, inspect the resulting protocol against current schemas/runtime/tests/bootstrap/package behavior and decide the **minimum** executable delta required to make native SDD operational rather than documentation-only.

A1 intentionally creates likely executable questions without answering them ad hoc, including:

- whether bootstrap/package inventory must ship the new `governance-core/SDD.md`;
- whether Core/protocol version manifests or deterministic inventory expectations require updates;
- whether the expanded consumer `TASK.template.md` requires parser/validator/schema changes;
- whether `docs/EXECUTOR-HANDOFFS.md` review/trace evidence requires a handoff schema/validator update;
- whether deterministic/eval conformance must prove stage ownership, native fallback and package self-bootstrap semantics.

A2 SHALL NOT assume all of these are required. The Orchestrator must inspect current implementation/tests and select only the smallest coherent executable delta.

If executable work is required, create a normal source Task Contract under `docs/tasks/` and select D052 `orchestrator-conformance`, `mixed` or `executor-implementation` based on actual semantic ownership. Required Orchestrator-owned oracle assets must be integrated before Executor launch.

No Executor is launched directly from this adoption plan.

### A3 — Executor implementation and technical review

Owner: **Executor**  
Precondition: an A2 Task Contract and any required D052 conformance assets are integrated and `READY`.

The Executor performs only authorized non-Markdown implementation and then `Code Review & Verify` against the approved D053/A1/A2 specification, Design and Plan.

Executor `DONE` remains evidence only.

### A4 — Convergence and consumer proof

Owner: **Orchestrator**

Review remote implementation/evidence and establish:

- source workflow convergence with D053;
- consumer Core convergence with D053;
- no dual-stage ownership;
- no hidden dependency on external SDD tooling;
- no duplicate current-truth/spec authority;
- coexistence with an adequate project-native SDD provider;
- native fallback behavior when no provider exists;
- single-install/self-bootstrap compatibility where new distributed assets/state exist;
- applicable deterministic/eval/security verification is green;
- accepted current specification carriers and implementation agree.

Only after A4 acceptance is native SDD adoption operationally complete.

## Transition policy for existing work

D053 is prospective and delta-first.

- Do not retroactively rewrite accepted historical Task Contracts.
- T021/T022 remain paused while the SDD adoption workstream is active.
- Their existing contracts/represented branch history are not silently modified merely to attach SDD terminology.
- When the Human Owner later reopens the pre-existing execution queue, the Orchestrator decides explicitly whether a current task needs a bounded SDD bridge/revision because of a real semantic gap; absence of new labels alone is not a reason to rewrite represented history.

## Trace for this adoption program

```text
Human request for project-wide native SDD
        -> SDD research
        -> D053 accepted architecture
        -> this adoption Plan & Trace
        -> A1 semantic protocol adoption
        -> A2 executable delta/Task Contract if required
        -> A3 Executor implementation + Code Review & Verify
        -> A4 Orchestrator convergence/acceptance
        -> accepted native SDD current state
```

## Stop / escalation conditions

Stop and return to Orchestrator Design/Plan if adoption would require any of the following without explicit persisted authority:

- dual Orchestrator/Executor ownership of one SDD stage;
- an external SDD product becoming a mandatory Agent Governance dependency;
- a parallel lifecycle that competes with F0-F6/PD0-PD6;
- a full retrospective specification backfill;
- source-maintenance records copied into ordinary consumer repositories;
- silent migration of existing consumer project state;
- weakening D052, security, provenance, coexistence or single-install invariants;
- rewriting represented T021/T022 history merely to retrofit labels.

## Current next action

1. Review the complete A1 Markdown diff on `docs/sdd-a1-semantic-protocol` against accepted D053 and this plan.
2. Integrate A1 through the normal Markdown PR to `develop`.
3. Reverify `develop` after integration.
4. Execute **A2 — executable enforcement/materialization decision** by inspecting current runtime/package/bootstrap/schema/test behavior.
5. Do not launch an Executor until A2 produces an integrated `READY` Task Contract and any required D052 conformance gate.
