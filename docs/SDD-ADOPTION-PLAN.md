# Native SDD Adoption Plan

Status: ACTIVE  
Date: 2026-08-23  
Authority: accepted `D053`  
Scope: Agent Governance source product and governed consumer projects

## Purpose

Operationalize the accepted native Spec-Driven Development architecture without installing OpenSpec, Spec Kit, Kiro or another external SDD framework, without creating a parallel lifecycle, and without restoring dual ownership inside any SDD stage.

This plan is the first `Plan & Trace` artifact under D053. Adoption is incremental and brownfield-safe.

## SDD profile

Adoption is `ASSURED` because it changes Governance protocol, source-development authority, consumer-project workflow and durable bootstrap/package semantics.

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

Native SDD semantics that governed consumer projects need live in reusable Governance Core/product distribution, not only in source-maintenance docs. A1 therefore added `governance-core/SDD.md`; A2/T034 materializes that module through the existing deterministic install/validation/package architecture.

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
State: **INTEGRATED**

A1 was authored on `docs/sdd-a1-semantic-protocol` from accepted D053 baseline `0c0ecdcc8d19492bed9a0fbaa1751f845e7ddfa4`, reviewed through PR #185, and squash-integrated into `develop` as `6d5c24d9641177a6556c7b475e53c4716fb024b4`.

A1 established the reusable semantic surface across:

- new `governance-core/SDD.md`;
- source `AGENTS.md` and PD workflow;
- Core router/lifecycle/coexistence/execution/handoff/context/protocol/adapters;
- source Task Contracts and executor handoffs;
- D041/D052 ownership alignment;
- Consumer Governance Skill routing and task template.

A1 established one owner per stage, native fallback when no adequate project-native SDD exists, proportional profiles, change-delta semantics, bidirectional traceability and explicit re-entry. It did not change runtime/package/test code.

A1 acceptance criteria were satisfied at semantic/Markdown convergence. Executable materialization was deliberately deferred to A2.

### A2 — Executable enforcement/materialization decision

Owner: **Orchestrator**  
Change class: Design + Task Contract + D052 conformance gate  
State: **DECIDED — T034 GATE AUTHORED**

A2 inspected integrated A1 against current runtime/package/bootstrap/schema/test behavior and selected the **minimum coherent executable delta**.

#### Required executable delta

1. **Required Core inventory** — `src/agent_governance/engine.py` uses a closed `CORE_FILES` and `CORE_VERSION_FIELDS` inventory. It does not yet contain `SDD.md`, while integrated `GOVERNANCE.md` routes that module and `_validate_core()` requires routed references to equal the closed inventory. T034 must add `SDD.md`/`SDD-Version` through the existing fail-closed model.
2. **Protocol/Core deterministic expectations** — test helpers still enumerate the pre-A1 Core set and artifact tests contain pre-A1 protocol expectations. The generic artifact builder already copies all `governance-core/*.md`; T034 aligns executable expectations rather than creating special SDD packaging.
3. **Missing-provider behavioral conformance** — the existing Consumer Governance corpus/grader still encodes the obsolete `no_sdd -> refuse_unsolicited_sdd` meaning. T034 freezes the accepted replacement: `use_native_sdd` plus `refuse_unsolicited_external_sdd`.

#### Explicitly not required by current architecture

- no parser/schema for the expanded Markdown `TASK.template.md`; current deterministic task mechanics need only existing task identity/state metadata while D053 semantics remain agent/Governance-readable Markdown;
- no new handoff JSON schema/validator; A1 review/trace obligations are protocol/Task-Contract semantics and no consumer runtime handoff schema exists today;
- no new SDD command family, state tree, lifecycle queue or external SDD dependency.

If implementation proves one of these excluded mechanisms genuinely necessary, T034 requires SDD Design re-entry rather than scope expansion.

A2 created:

- `docs/tasks/T034-native-sdd-executable-materialization.md` — complete ASSURED Design/Plan & Trace;
- `tests/test_t034_native_sdd_conformance.py` — D052 Orchestrator-owned frozen acceptance projection (`T034-A2-v1`).

T034 uses `Test-Authorship-Mode: mixed`. The Executor owns implementation, technical review, supplementary tests and execution evidence; it may only synchronize legacy T015 semantic files to the exact frozen T034 meaning and may not edit the T034 oracle.

A2 is complete when this Task Contract/conformance gate is reviewed and integrated into `develop`.

### A3 — Executor implementation and technical review

Owner: **Executor**  
Precondition: T034 and `T034-A2-v1` are integrated/reachable from canonical `develop`.

The Executor performs only the authorized non-Markdown implementation from:

`docs/tasks/T034-native-sdd-executable-materialization.md`

It then performs D053 `Code Review & Verify`, runs the frozen T034 conformance oracle plus required existing/supplementary verification, persists `handoffs/T034-executor-handoff.json`, commits and performs the one planned final push.

Because A1 changed `AGENTS.md`, the first T034 Executor launch MUST include the D043 conditional current-`AGENTS.md` reload after synchronizing the integrated `develop` baseline.

T034 execution must use a safe fresh/rematerialized native-Windows checkout; the stale pre-T033 CRLF checkout is not acceptance evidence.

Executor `DONE` remains evidence only.

### A4 — Convergence and consumer proof

Owner: **Orchestrator**

Review remote T034 implementation/evidence and establish:

- source workflow convergence with D053;
- installed Consumer Core includes/routs/validates native `SDD.md`;
- no dual-stage ownership or second lifecycle;
- no hidden dependency on external SDD tooling;
- no duplicate current-truth/spec authority;
- coexistence with adequate project-native SDD remains unchanged;
- missing-provider fallback uses native SDD and does not install an external SDD merely for methodology coverage;
- single-install/self-bootstrap compatibility and Protocol 1.14.0 package identity are green;
- frozen T034 oracle plus applicable deterministic/eval/package verification are green;
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
        -> A1 semantic protocol adoption (integrated)
        -> A2 executable decision + T034/frozen conformance gate
        -> A3 T034 Executor implementation + Code Review & Verify
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
- rewriting represented T021/T022 history merely to retrofit labels;
- adding task/handoff schemas or new SDD runtime machinery merely because they are possible rather than required by accepted behavior.

## Current next action

1. Review the A2/T034 planning + conformance-gate diff against D053, D052 and this plan.
2. Integrate the gate through a normal topic PR to `develop` only if the frozen oracle and Task Contract are coherent.
3. Reverify `develop` after integration and confirm `T034-A2-v1` is frozen/reachable there.
4. Establish a safe fresh/rematerialized native-Windows Executor checkout current with that `develop` revision.
5. Launch T034 using the canonical minimal executor prompt plus the required D043 current-`AGENTS.md` reload line.
6. Do not resume T021/T022 automatically.
