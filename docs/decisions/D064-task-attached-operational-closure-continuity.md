# D064 — Task-Attached Operational Closure Continuity

Status: ACCEPTED  
Date: 2026-09-05  
Authority: Human Owner / ChatGPT Orchestrator  
Refines: `docs/decisions/D060-task-scoped-executor-coordinator-continuity.md`  
Related: `docs/OPERATION-CONTRACTS.md`, `docs/BRANCH-CLEANUP.md`, `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`

## Problem

D060 correctly established one Human-visible Executor Coordinator Root per governed work unit. Separately, source-product branch-cleanup policy requires delegated post-integration retirement to be controlled by a persisted Operational Contract.

Taken literally, those two rules created an unintended seam:

```text
Txxx implementation/review -> one Txxx coordinator
accepted Txxx still needs branch/worktree closure
cleanup requires new OPxxx
D060 says new OPxxx -> NEW coordinator
```

That would discard useful task context precisely during the final closure step even though the Human-visible activity is still completion of the same task.

The Human Owner requires one coordinator to remain responsible for a complete task through its actual termination, while still keeping cleanup authority durable and auditable.

## Decision

Agent Governance introduces a narrow **task-attached operational closure** relation.

An Operational Contract may declare:

```text
Parent-Work-Unit: Txxx
Coordinator-Continuity: ATTACHED_CLOSURE
```

when, and only when, the operation is solely the post-acceptance closure of that exact Task Contract.

A valid attached closure does **not** start a new Human-visible coordinator work unit. If the parent task root remains safe and recoverable, the Executor MUST `CONTINUE` the parent task coordinator.

Example:

```text
T057 root-1 executes T057
T057 accepted by Orchestrator
OP069 is persisted solely to retire T057 branches/worktree
OP069 declares Parent-Work-Unit: T057 / ATTACHED_CLOSURE
=> CONTINUE AG | agent-governance | T057 | root-1
=> retire root only after OP069 closure is accepted
```

## Eligibility gate

An Operational Contract may use `ATTACHED_CLOSURE` only if all of the following are true:

1. the parent `Txxx` exists and has completed its implementation/evidence phase;
2. the Orchestrator has accepted or otherwise durably resolved the task outcome sufficiently for closure;
3. the operation creates no new implementation scope and does not reopen task acceptance;
4. the operation is limited to lifecycle closure such as branch/worktree retirement, remote/local pruning, receipt publication and restoration/verification of the normal primary checkout baseline;
5. every mutation target is deterministically derived from the parent task's integrated PR/evidence/review lineage or from the attached Operational Contract's own authoring PR;
6. the operation does not add unrelated backlog cleanup merely for convenience;
7. the parent root is still safely recoverable; otherwise normal D060 failover rules apply.

If any condition fails, the operation is a normal independent `OPxxx` and uses `NEW / AG | <repo> | OPxxx | root-1`.

## Coordinator identity

For an attached closure:

```text
Session: CONTINUE
Coordinator-Chat: parent task coordinator name
```

The OP identity remains persisted execution authority, but the Human-visible coordinator name remains the parent Txxx identity.

The durable Operational Contract and receipt MUST record both:

```text
Operation-ID: OPxxx
Parent-Work-Unit: Txxx
Coordinator-Continuity: ATTACHED_CLOSURE
Coordinator-Chat: AG | <repo> | Txxx | root-n
```

This makes the relationship reconstructible without relying on chat history.

## Context semantics

Attached closure exists specifically to preserve useful same-task context while keeping Git authoritative.

On continuation the coordinator still performs D042/RB001 freshness, loads the newly integrated Operational Contract and current repository policy, and treats remembered task state only as navigation/context.

The root should retain concise knowledge of:

- accepted task outcome;
- task branch/worktree identity;
- integrated PR/review identities;
- known retained/review local-state facts relevant to safe cleanup;
- exact next closure action.

It should not retain raw logs merely because the session continues.

## Compute/profile rule

D064 changes coordinator lifetime, not D055 compute selection.

A continuation still receives a D055 launch card. However, an attached closure MUST NOT violate a model/effort profile that the parent Task Contract explicitly froze for the complete task lifecycle.

If the parent contract froze a Human-visible profile through completion, keep that profile for the attached closure. Otherwise D055 may select the minimum sufficient profile compatible with safe continuation on the same coordinator host.

## Scope isolation

An attached closure MUST NOT absorb cleanup belonging to another Task Contract, unrelated Operational Contract, documentation change, research change or historical backlog item.

For example, T057 attached closure may retire:

- the T057 evidence/execution branch/worktree;
- T057-specific Orchestrator convergence branch when explicitly authorized by the closure contract;
- the closure contract's own authoring branch when the normal self-retirement pattern is used.

It may not retire an unrelated D062 documentation branch merely because that branch is also stale.

Unrelated cleanup requires its own operational authority and, under D060, normally its own coordinator lifecycle.

## Relationship to D060

D060 remains the default:

```text
new Txxx -> NEW
new standalone OPxxx -> NEW
same Txxx -> CONTINUE
same standalone OPxxx -> CONTINUE
```

D064 adds exactly one composition rule:

```text
OPxxx declares valid Parent-Work-Unit: Txxx
AND Coordinator-Continuity: ATTACHED_CLOSURE
=> OPxxx is closure authority inside the existing Txxx coordinator lifecycle
```

The attached OP is still a separate persisted authority artifact for operational safety; it is not a separate Human-visible coordinator lifecycle.

## Relationship to Operational Contracts

`docs/OPERATION-CONTRACTS.md` is refined so attached closures must include the two additional required fields and must make the eligibility/scope boundary explicit.

The standard compact Operational Contract terminal response remains unchanged:

```text
STATUS: DONE | BLOCKED | PARTIAL
RECEIPT: <durable GitHub receipt URL>
COORDINATOR: <Human-visible coordinator name>
```

For an attached closure, `COORDINATOR` is the parent Txxx coordinator.

## Root retirement invariant

A Task coordinator is retired only after all Executor-owned final actions in the task lifecycle are closed, including an authorized task-attached operational closure when one is required.

```text
implementation complete != root retired
Orchestrator acceptance + required attached closure accepted = task lifecycle closed -> retire root
```

## Effective rule

```text
post-acceptance operation is solely closure of Txxx
AND persisted OP declares ATTACHED_CLOSURE to Txxx
AND parent root is recoverable
=> CONTINUE parent Txxx root

otherwise
=> normal D060 work-unit boundary applies
```
