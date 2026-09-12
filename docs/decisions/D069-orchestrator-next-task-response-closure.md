# D069 — Orchestrator next-task response closure

Status: ACCEPTED  
Date: 2026-09-06  
Last-Refined: 2026-09-12  
Scope: ChatGPT Orchestrator Human-facing response closure and next-step visibility

## Context

The canonical repository and Orchestrator checkpoint already persist the current work frontier and the next permitted action. However, a Human-facing completion or status response can still require the Human Owner to infer that next step from the body of the response.

The Human Owner requires the Orchestrator to make the immediate frontier explicit at the end of its project responses and, when that frontier is a next ChatGPT Orchestrator task, to make the recommended ChatGPT reasoning effort visible without introducing a runtime-duration contract.

This is a presentation/navigation requirement. It must not create task authority, silently select a new objective, skip an SDD stage, or substitute chat state for canonical Git authority.

## Decision

For Agent Governance source-product orchestration, every final Human-facing response that reports project work, status, convergence, closure, or a persisted repository change SHALL end with a section titled exactly:

```text
Próxima Tarea
```

The section SHALL contain a short description of the next task or action that follows from the current canonical Git/checkpoint state.

When the next task is a ChatGPT Orchestrator task, the same section SHALL also contain exactly one ChatGPT effort recommendation:

```text
ChatGPT Effort: MEDIUM | HIGH
```

The emitted value is one of `MEDIUM` or `HIGH`; the pipe notation above defines the allowed choices and is not emitted literally.

### ChatGPT effort selection

`ChatGPT Effort` configures only the recommended reasoning effort for the **next ChatGPT Orchestrator task**.

Use the minimum sufficient effort for the expected task geometry:

- `MEDIUM` — normal default for bounded, direct orchestration with limited exploration, synthesis or cross-checking;
- `HIGH` — when the next task is expected to require materially deeper or longer reasoning, substantial research/synthesis, broad cross-file or cross-authority reconciliation, or multiple consequential verification steps.

This recommendation is qualitative. Agent Governance SHALL NOT infer, publish or enforce a wall-clock duration, timeout, minute budget, or fixed mapping from `MEDIUM`/`HIGH` to execution time. Runtime behavior remains provider-controlled and may vary.

`ChatGPT Effort` is distinct from D055. D055 configures the concrete **Executor** launch profile; this field configures only the Human-facing recommendation for the next **ChatGPT Orchestrator** task. One MUST NOT be inferred from the other.

When the next frontier is not a ChatGPT Orchestrator task — for example, the Orchestrator is waiting for a Human decision or an already-configured Executor action — no synthetic ChatGPT effort recommendation is required.

### Source of truth

The Orchestrator SHALL derive `Próxima Tarea` and any associated `ChatGPT Effort` recommendation from the current canonical repository state, including the current checkpoint, controlling Task Contract/Decision and applicable SDD stage boundary.

Prior chat or Project Memory MUST NOT be used as authority when it conflicts with Git.

### Authorization boundary

`Próxima Tarea` and `ChatGPT Effort` are navigation/configuration metadata only.

They MUST NOT:

- authorize or start the described task by themselves;
- imply that a Human-selected objective exists when the checkpoint still says `WAITING_FOR_NEXT_OBJECTIVE`;
- bypass Bootstrap -> explicit validation -> Task execution separation;
- skip SDD ownership/stage gates;
- launch an Executor, call a provider/model, mutate a branch, or enter a dependent task merely because it is named as next;
- convert a ChatGPT effort recommendation into an Executor/Codex effort selection.

When the next task is only **permitted** but has not been explicitly selected, the wording SHALL make that distinction clear.

### Blocked and waiting states

If the current frontier is blocked, `Próxima Tarea` SHALL describe the next required unblock, re-entry, review, or Human decision rather than inventing downstream work.

If there is no material next task authorized or inferable from canonical state, the section SHALL state that the Orchestrator is waiting for the Human Owner to select the next objective. A `ChatGPT Effort` value is then omitted unless the checkpoint already defines a concrete next ChatGPT task whose execution is merely waiting for that Human selection.

### Brevity

The task description SHOULD normally be one concise sentence. `ChatGPT Effort` SHOULD be one additional compact line. Additional detail belongs in the main response or canonical artifacts, not in the closure label.

## Consequences

- Human-facing closure becomes consistent and immediately actionable.
- The next permitted frontier and its recommended ChatGPT reasoning effort are visible without reading the full checkpoint.
- No unstable estimate of ChatGPT execution duration becomes governance policy.
- ChatGPT effort selection remains separate from D055 Executor launch configuration.
- Canonical Git remains authoritative; the response footer is not a second task registry.
- Existing SDD, branching, ownership, Task Contract, Executor and checkpoint rules are otherwise unchanged.

## Current application

This refinement does not change the substantive work-unit frontier. The current checkpoint remains authoritative for the active task and shall carry the recommended ChatGPT effort for its next ChatGPT action when the checkpoint is refreshed.
