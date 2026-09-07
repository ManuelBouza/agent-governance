# D069 — Orchestrator next-task response closure

Status: ACCEPTED  
Date: 2026-09-06  
Scope: ChatGPT Orchestrator Human-facing response closure and next-step visibility

## Context

The canonical repository and Orchestrator checkpoint already persist the current work frontier and the next permitted action. However, a Human-facing completion or status response can still require the Human Owner to infer that next step from the body of the response.

The Human Owner requires the Orchestrator to make the immediate frontier explicit at the end of its project responses.

This is a presentation/navigation requirement. It must not create task authority, silently select a new objective, skip an SDD stage, or substitute chat state for canonical Git authority.

## Decision

For Agent Governance source-product orchestration, every final Human-facing response that reports project work, status, convergence, closure, or a persisted repository change SHALL end with a section titled exactly:

```text
Próxima Tarea
```

The section SHALL contain a short description of the next task or action that follows from the current canonical Git/checkpoint state.

### Source of truth

The Orchestrator SHALL derive `Próxima Tarea` from the current canonical repository state, including the current checkpoint, controlling Task Contract/Decision and applicable SDD stage boundary.

Prior chat or Project Memory MUST NOT be used as authority when it conflicts with Git.

### Authorization boundary

`Próxima Tarea` is navigation metadata only.

It MUST NOT:

- authorize or start the described task by itself;
- imply that a Human-selected objective exists when the checkpoint still says `WAITING_FOR_NEXT_OBJECTIVE`;
- bypass Bootstrap -> explicit validation -> Task execution separation;
- skip SDD ownership/stage gates;
- launch an Executor, call a provider/model, mutate a branch, or enter a dependent task merely because it is named as next.

When the next task is only **permitted** but has not been explicitly selected, the wording SHALL make that distinction clear.

### Blocked and waiting states

If the current frontier is blocked, `Próxima Tarea` SHALL describe the next required unblock, re-entry, review, or Human decision rather than inventing downstream work.

If there is no material next task authorized or inferable from canonical state, the section SHALL state that the Orchestrator is waiting for the Human Owner to select the next objective.

### Brevity

The description SHOULD normally be one concise sentence. Additional detail belongs in the main response or canonical artifacts, not in the closure label.

## Consequences

- Human-facing closure becomes consistent and immediately actionable.
- The next permitted frontier is visible without reading the full checkpoint.
- Canonical Git remains authoritative; the response footer is not a second task registry.
- Existing SDD, branching, ownership, Task Contract, Executor and checkpoint rules are unchanged.

## Current application

At acceptance of this decision, checkpoint O236 remains authoritative for the substantive frontier. No D050/T023 Stage 5 work is selected or started by D069.

The next permitted D050/T023 task, if the Human Owner selects continuation, remains D068 Stage 5 candidate materialization for T061.
