# Native SDD Adoption Plan

Status: ACTIVE  
Date: 2026-08-23  
Authority: accepted `D053`  
Scope: Agent Governance source product and governed consumer projects

## Purpose

Operationalize the accepted native Spec-Driven Development architecture without installing OpenSpec, Spec Kit, Kiro or another external SDD framework, without creating a parallel lifecycle, and without restoring dual ownership inside any SDD stage.

This plan is the first `Plan & Trace` artifact under D053. It intentionally keeps adoption incremental and brownfield-safe.

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

The adoption work treats these accepted/current artifacts as specification carriers rather than duplicating them wholesale:

- `docs/decisions/D053-native-spec-driven-development.md` — native SDD architecture and stage ownership;
- `AGENTS.md` — source-repository role/write/workflow adapter;
- `governance-core/LIFECYCLE.md` — consumer preimplementation lifecycle;
- `governance-core/QUALITY.md` — engineering quality envelope;
- `governance-core/COEXISTENCE.md` — project-native capability/SDD coexistence;
- `docs/DEVELOPMENT-WORKFLOW.md` — source-product PD lifecycle;
- `docs/TASK-CONTRACTS.md` — durable source execution-contract semantics;
- `docs/EXECUTOR-HANDOFFS.md` — Executor evidence boundary;
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
- requirement-to-design-to-plan-to-implementation-to-evidence traceability;
- Executor `Code Review & Verify` as a distinct technical stage;
- Orchestrator `Converge / Accept / Evolve` as the acceptance stage;
- explicit re-entry when implementation evidence exposes an upstream spec/design/plan defect.

### MODIFIED

- source PD0-PD6 wording must map exactly to accepted D053 ownership;
- consumer F0-F6/readiness semantics must make Orchestrator specification/design/plan completeness explicit;
- D041 process autonomy must be clearly bounded inside Executor stages 5-6;
- coexistence must reuse/adapt project-native SDD while preserving Agent Governance stage ownership;
- Task Contracts and handoffs must carry enough trace/evidence for convergence without becoming a second SDD system.

### REMOVED

- `no-SDD` as the normal fallback when no adequate provider exists;
- wording that gives Executor authoritative SDD Design/Plan ownership;
- wording that conflates Executor technical verification with Orchestrator semantic acceptance;
- any need to install a third-party SDD product for native coverage.

### PRESERVED

- Human Owner remains final authority;
- Git remains canonical durable project state;
- existing F0-F6 and PD0-PD6 lifecycles remain the lifecycle skeletons;
- D052 conformance assets remain evidence projections, never authority;
- D041 still allows private Executor tools/plans/sub-agents inside its assigned stages;
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

Native SDD semantics that governed consumer projects need must ultimately live in the reusable Governance Core/product distribution, not only in source-maintenance docs.

### 5. Source/consumer separation

Source-product Task Contracts and Orchestrator checkpoints remain source-only. Consumer projects use their durable Governance/Core and coordination records; source-maintenance artifacts must not leak into consumer bootstrap.

### 6. No mandatory external SDD runtime

OpenSpec, Spec Kit, Kiro and similar systems remain research/coexistence providers only. Native SDD must work from Agent Governance's own distributed artifacts and the governed repository.

### 7. Conformance follows semantic ownership

Where machine-verifiable semantics are required, D052 applies. Orchestrator authors the semantic oracle when appropriate; Executor technical work runs it and supplies evidence; Orchestrator accepts or rejects convergence.

## Adoption sequence

### A1 — Semantic protocol adoption

Owner: **Orchestrator**  
Change class: Markdown/policy  
Executor: **not used**

Update the smallest coherent set of normative Markdown so source and consumer workflows no longer contradict accepted D053.

Expected surfaces include:

- `AGENTS.md`;
- `governance-core/LIFECYCLE.md`;
- `governance-core/QUALITY.md` where specification/design/verification quality semantics need refinement;
- `governance-core/COEXISTENCE.md` for native fallback and provider reuse;
- `docs/DEVELOPMENT-WORKFLOW.md`;
- `docs/TASK-CONTRACTS.md`;
- `docs/EXECUTOR-HANDOFFS.md` where Code Review & Verify evidence/trace is represented;
- D041/D052 cross-reference wording only where needed to remove authority ambiguity;
- reusable Markdown templates that materially encode lifecycle/task/spec semantics.

A1 acceptance requires:

1. one accountable owner per SDD stage everywhere normative;
2. Orchestrator owns Explore, Specify, Design, Plan & Trace and Converge/Accept/Evolve;
3. Executor ownership is limited to technical Implement plus Code Review & Verify for Executor-owned implementation;
4. no normative text requires the Executor to reconstruct missing specification/design/plan authority;
5. native SDD is the fallback when no adequate project-native SDD provider exists;
6. project-native SDD can be reused/adapted without duplicate authority;
7. `ADDED / MODIFIED / REMOVED / PRESERVED`, proportional profiles and re-entry semantics are representable without forcing a new file for each stage;
8. no source-only state is introduced into the consumer footprint;
9. historical Task Contracts are not rewritten solely for SDD labels.

A1 is complete only after its Markdown PR is reviewed and integrated into `develop`.

### A2 — Executable enforcement/materialization decision

Owner: **Orchestrator**  
Change class: design + Task Contract/conformance gate if executable work is required

After A1 is integrated, inspect the resulting protocol against current schemas/runtime/tests/bootstrap/package behavior and decide the minimum executable delta required to make native SDD operational rather than documentation-only.

Possible executable surfaces include:

- deterministic schema/validation for new spec/change/trace fields if such fields are materialized;
- source/consumer conformance tests for stage ownership and native fallback semantics;
- runtime/bootstrap support if durable consumer SDD records require new materialization;
- package/provenance updates if new reusable templates/assets must ship in the single-install distribution;
- eval/security negative controls where deterministic assertions are insufficient.

A2 SHALL NOT assume all of these are required. The Orchestrator must first determine the smallest executable change that satisfies D053 and existing product architecture.

If executable work is required, create a normal source Task Contract under `docs/tasks/` and select D052 `orchestrator-conformance`, `mixed` or `executor-implementation` based on the actual semantic ownership. Required Orchestrator-owned oracle assets must be integrated before Executor launch.

No Executor is launched directly from this adoption plan.

### A3 — Executor implementation and technical review

Owner: **Executor**  
Precondition: an A2 Task Contract and any required D052 conformance assets are integrated and `READY`.

The Executor performs only the authorized non-Markdown implementation and then performs `Code Review & Verify` against the approved D053/A1/A2 specification, design and plan.

Executor `DONE` remains evidence only.

### A4 — Convergence and consumer proof

Owner: **Orchestrator**

Review the remote implementation/evidence and establish:

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

Only after A4 acceptance is native SDD adoption considered operationally complete.

## Transition policy for existing work

D053 is prospective and delta-first.

- Do not retroactively rewrite accepted historical Task Contracts.
- T021/T022 remain paused while the SDD adoption workstream is active.
- Their existing contracts/represented branch history are not silently modified merely to attach SDD terminology.
- When the Human Owner later reopens the pre-existing execution queue, the Orchestrator must decide explicitly whether a current task needs a bounded SDD bridge/revision because of a real semantic gap; absence of new labels alone is not a reason to rewrite represented history.

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

Execute **A1 — Semantic protocol adoption** as an Orchestrator-owned Markdown-only change from current `develop`, then integrate it through the normal Markdown PR before deciding any executable A2 scope.
