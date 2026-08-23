# Implementation Execution Rules

Execution-Version: 1.3.0

Load this module for READY implementation work, execution blockers, task transitions or implementation review.

Load `SDD.md` with this module for native Implement and Code Review & Verify stage semantics. Load `EXECUTION-CONTROL.md` additionally when the current task can inspect or mutate material local/remote/system execution state outside ordinary task-local source/test effects.

## Work States

`PLANNED`, `READY`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `ACCEPTED`, `REJECTED`, `CANCELLED`.

Valid transitions:
- PLANNED + sequence eligibility -> READY
- READY + start -> IN_PROGRESS
- IN_PROGRESS + progress -> IN_PROGRESS
- IN_PROGRESS + blocked -> BLOCKED
- BLOCKED + resume -> IN_PROGRESS
- IN_PROGRESS + done -> DONE
- DONE + accept -> ACCEPTED
- DONE + reject -> REJECTED
- REJECTED + start -> IN_PROGRESS
- any non-ACCEPTED active state + cancel -> CANCELLED

ACCEPTED work is immutable as a work unit; later change requires new work or explicit scope change.

`DONE` means the Implementation Agent completed both native SDD stages `Implement` and `Code Review & Verify` for the task and persisted the required evidence. It is not Strategy/Governance acceptance.

## Execution Authorization

F5 validates the complete SDD-anchored plan. F6 persists the execution sequence and makes only the first eligible task READY.

After handoff, the Implementation Agent owns continuous sequential execution of its authorized stages 5-6. It MUST continue task-by-task without asking Strategy/Human permission while eligibility holds.

This autonomous continuation authorizes ordinary task-local technical realization and technical review only. It does not transfer Strategy-owned specification, Design, Plan/Trace, acceptance or current-spec evolution, and it does not turn task readiness into unrestricted local/remote/system authority.

When a task includes material system/remote/privileged/credentialed/network/deployment/persistent-data/destructive effects, `EXECUTION-CONTROL.md` governs the applicable Execution Capability Envelope, approval mode, target identity, runbook/procedure and adapter semantics.

A material operation classified `REQUIRE_HUMAN` is a pre-defined execution gate inside the task. The Implementation Agent stops at that gate until the bounded approval is persisted, then resumes the same task. It MUST NOT reinterpret general task readiness as that approval.

A `DENY`, target mismatch, stale authorization/runbook, unsupported semantic adapter step or failed material precondition/checkpoint is a blocker; it cannot be bypassed by changing command syntax or execution product.

## Sequential Disclosure

Exactly one task record is disclosed at a time during normal execution.

The Implementation Agent MAY read WORKPLAN metadata needed to determine order, dependencies, status and record path, but MUST NOT open the objective/scope/acceptance content of future task records.

Sequence:
1. load only the current READY task record, its referenced specification/Design artifacts and required Skills;
2. load `EXECUTION-CONTROL.md` only when the disclosed task/effect requires it;
3. append `start` and perform the authorized implementation;
4. resolve ordinary implementation defects autonomously inside the approved specification/Design/Plan and capability envelope;
5. perform `Code Review & Verify` under `SDD.md`, including required tests/evals/checks and review for spec/Design fidelity, correctness, maintainability, relevant quality constraints and unauthorized scope;
6. correct review findings that remain implementation defects inside approved authority;
7. if review reveals an upstream specification/Design/Plan/acceptance defect, append `blocked`, stop the affected sequence and return it to Strategy for explicit SDD re-entry;
8. append `done` with implementation/review evidence and requirement-to-verification references when acceptance criteria are satisfied;
9. determine the next eligible task from WORKPLAN metadata and accumulated EXCHANGE state;
10. only after the prior task is DONE, load the next task record;
11. repeat until all authorized tasks are DONE or a valid blocker stops execution.

Do not speculatively inspect future task files.

## Dependency Rule

For autonomous continuation, a dependency is satisfied by `DONE` or `ACCEPTED` unless an F5-approved task/gate explicitly requires external acceptance.

`DONE` means the Implementation Agent implemented the task, technically reviewed it and verified its declared acceptance criteria/evidence obligations. `ACCEPTED` is subsequent Strategy/Human convergence/acceptance and is not, by default, an inter-task execution gate.

Only one task may be READY/IN_PROGRESS in the normal sequence at a time unless the Human Owner explicitly approves parallel execution.

## Eligibility

The Implementation Agent continues when:
- the execution sequence was authorized by F5/F6;
- the next task is the next ordered eligible work unit;
- its dependencies are DONE or ACCEPTED;
- required Skills are approved/available;
- scope, referenced specification delta, controlling Design and acceptance are unambiguous after disclosure;
- any material Execution Capability Envelope/runbook requirements are satisfied for the next operation;
- no strategic/SDD re-entry/safety/execution-control blocker exists.

Routine local coding choices, in-scope refactors, implementation-test fixes and equivalent technical decisions belong to the Implementation Agent when they preserve the approved specification/Design/Plan and MUST NOT stop the sequence.

A choice that would materially alter requirements, architecture/interfaces/state/data flow/trust boundaries, compatibility/migration, acceptance meaning or task decomposition is not a routine implementation choice. It triggers SDD re-entry to Strategy.

## Strategic, SDD and Execution-Control Blockers

Valid blocker reasons include:
`missing_skill`, `conflicting_authority`, `scope_ambiguity`, `specification_ambiguity`, `design_gap`, `plan_gap`, `acceptance_ambiguity`, `production_risk`, `security_risk`, `destructive_change`, `external_dependency`, `human_decision_required`, `execution_authorization`, `target_mismatch`, `runbook_precondition`, `adapter_unsupported`, `recovery_unavailable`.

When a valid blocker occurs:
- append `blocked` for the current task with concise reason/evidence;
- identify the earliest affected Strategy-owned SDD stage when the blocker concerns specification/Design/Plan;
- do not disclose/start later tasks;
- stop the execution sequence and hand off to Strategy/Human as routed by HANDOFF.

Routine adapter/command failures remain Implementation responsibility when they can be corrected without changing target, effect, privilege, credential, runbook semantics, specification/Design/Plan, acceptance or material risk.

## Code Review & Verify evidence

Before `DONE`, the Implementation Agent must make it possible for Strategy to reconstruct:

- which implementation state was reviewed;
- which material requirements/spec-delta items and `PRESERVED` invariants were checked;
- which required tests/evals/checks ran and their results;
- material review findings and how in-authority findings were resolved;
- whether any upstream SDD re-entry issue remains;
- any unresolved technical issue or unauthorized-scope concern.

The exact storage may be the task's normal evidence/handoff/event structure. Do not create a second review authority or mandatory vendor-specific report format when existing project records are sufficient.

## Material Execution Evidence

For a task governed by `EXECUTION-CONTROL.md`, `done` evidence must establish the material runbook/operation postconditions and identify the required sanitized authorization/target/runbook/adapter/checkpoint/recovery evidence. A successful command or client exit code alone is insufficient when the task contract requires verification of actual target state.

Raw terminal transcripts are not required as the canonical evidence record and must not be used as a substitute for semantic postcondition evidence.

## Completion and Review

Task completion does not require an inter-task Strategy handoff. Continue immediately to the next eligible task when all eligibility conditions hold.

When the authorized sequence is exhausted, hand off once for Strategy `Converge / Accept / Evolve` review under `SDD.md`. Strategy MAY accept/reject individual tasks using implementation/review evidence. A rejection may create rework and may invalidate downstream evidence when materially dependent; Strategy determines the affected scope and whether re-entry begins at Specify, Design, Plan or Implementation.
