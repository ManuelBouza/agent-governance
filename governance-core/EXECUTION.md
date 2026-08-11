# Implementation Execution Rules

Execution-Version: 1.2.0

Load this module for READY implementation work, execution blockers, task transitions or implementation review.

Load `EXECUTION-CONTROL.md` additionally when the current task can inspect or mutate material local/remote/system execution state outside ordinary task-local source/test effects.

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

## Execution Authorization

F5 validates the complete plan. F6 persists the execution sequence and makes only the first eligible task READY.

After handoff, the Implementation Agent owns continuous sequential execution. It MUST continue task-by-task without asking Strategy/Human permission while eligibility holds.

This autonomous continuation authorizes ordinary task-local technical realization only. It does not turn task readiness into unrestricted local/remote/system authority.

When a task includes material system/remote/privileged/credentialed/network/deployment/persistent-data/destructive effects, `EXECUTION-CONTROL.md` governs the applicable Execution Capability Envelope, approval mode, target identity, runbook/procedure and adapter semantics.

A material operation classified `REQUIRE_HUMAN` is a pre-defined execution gate inside the task. The Implementation Agent stops at that gate until the bounded approval is persisted, then resumes the same task. It MUST NOT reinterpret general task readiness as that approval.

A `DENY`, target mismatch, stale authorization/runbook, unsupported semantic adapter step or failed material precondition/checkpoint is a blocker; it cannot be bypassed by changing command syntax or execution product.

## Sequential Disclosure

Exactly one task record is disclosed at a time during normal execution.

The Implementation Agent MAY read WORKPLAN metadata needed to determine order, dependencies, status and record path, but MUST NOT open the objective/scope/acceptance content of future task records.

Sequence:
1. load only the current READY task record and its required Skills;
2. load `EXECUTION-CONTROL.md` only when the disclosed task/effect requires it;
3. append `start` and execute/verify the task;
4. resolve normal technical problems autonomously inside the authorized task and capability envelope;
5. append `done` with evidence and verification when acceptance criteria are satisfied;
6. determine the next eligible task from WORKPLAN metadata and accumulated EXCHANGE state;
7. only after the prior task is DONE, load the next task record;
8. repeat until all authorized tasks are DONE or a valid blocker stops execution.

Do not speculatively inspect future task files.

## Dependency Rule

For autonomous continuation, a dependency is satisfied by `DONE` or `ACCEPTED` unless an F5-approved task/gate explicitly requires external acceptance.

`DONE` means the Implementation Agent has completed the task and verified its declared acceptance criteria. `ACCEPTED` is subsequent Strategy/Human review and is not, by default, an inter-task execution gate.

Only one task may be READY/IN_PROGRESS in the normal sequence at a time unless the Human Owner explicitly approves parallel execution.

## Eligibility

The Implementation Agent continues when:
- the execution sequence was authorized by F5/F6;
- the next task is the next ordered eligible work unit;
- its dependencies are DONE or ACCEPTED;
- required Skills are approved/available;
- scope and acceptance are unambiguous after disclosure;
- any material Execution Capability Envelope/runbook requirements are satisfied for the next operation;
- no strategic/safety/execution-control blocker exists.

Routine implementation choices, in-scope refactors, test fixes and equivalent technical decisions belong to the Implementation Agent and MUST NOT stop the sequence.

## Strategic and Execution-Control Blockers

Valid blocker reasons include:
`missing_skill`, `conflicting_authority`, `scope_ambiguity`, `acceptance_ambiguity`, `production_risk`, `security_risk`, `destructive_change`, `external_dependency`, `human_decision_required`, `execution_authorization`, `target_mismatch`, `runbook_precondition`, `adapter_unsupported`, `recovery_unavailable`.

When a valid blocker occurs:
- append `blocked` for the current task with concise reason/evidence;
- do not disclose/start later tasks;
- stop the execution sequence and hand off to Strategy/Human as routed by HANDOFF.

Routine adapter/command failures remain Implementation responsibility when they can be corrected without changing target, effect, privilege, credential, runbook semantics, acceptance or material risk.

## Material Execution Evidence

For a task governed by `EXECUTION-CONTROL.md`, `done` evidence must establish the material runbook/operation postconditions and identify the required sanitized authorization/target/runbook/adapter/checkpoint/recovery evidence. A successful command or client exit code alone is insufficient when the task contract requires verification of actual target state.

Raw terminal transcripts are not required as the canonical evidence record and must not be used as a substitute for semantic postcondition evidence.

## Completion and Review

Task completion does not require an inter-task Strategy handoff. Continue immediately to the next eligible task when all eligibility conditions hold.

When the authorized sequence is exhausted, hand off once for Strategy review. Strategy MAY accept/reject individual tasks using evidence. A rejection may create rework and may invalidate downstream evidence when materially dependent; Strategy determines the affected scope.
