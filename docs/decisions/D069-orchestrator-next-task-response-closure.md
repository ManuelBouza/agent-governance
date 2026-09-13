# D069 — Orchestrator next-task response closure

Status: ACCEPTED  
Date: 2026-09-06  
Last-Refined: 2026-09-13  
Scope: ChatGPT Orchestrator Human-facing response closure and next-step visibility

## Context

The canonical repository and Orchestrator checkpoint already persist the current work frontier and the next permitted action. However, a Human-facing completion or status response can still require the Human Owner to infer that next step from the body of the response.

The Human Owner requires the Orchestrator to make the immediate frontier explicit at the end of its project responses and to make the recommended ChatGPT reasoning effort for the next required ChatGPT intervention visible on every such closure, regardless of whether that intervention continues in the current chat, follows a Human/Executor gate, or starts in a successor chat. When the frontier also defines a concrete next ChatGPT Orchestrator task, the selected execution geometry is shown as well, without introducing a runtime-duration contract.

This is a presentation/navigation requirement. It must not create task authority, silently select a new objective, skip an SDD stage, or substitute chat state for canonical Git authority.

## Decision

For Agent Governance source-product orchestration, every final Human-facing response that reports project work, status, convergence, closure, or a persisted repository change SHALL end with a section titled exactly:

```text
Próxima Tarea
```

The section SHALL contain a short description of the next task or action that follows from the current canonical Git/checkpoint state and SHALL always contain exactly one ChatGPT effort recommendation:

```text
ChatGPT Effort: MEDIUM | HIGH
```

The emitted value uses one member of the allowed set; the pipe notation above defines choices and is not emitted literally.

When the next concrete ChatGPT Orchestrator task is known, the same section SHALL also contain exactly one execution-shape classification:

```text
Execution Shape: SINGLE_EXECUTION | MULTI_EXECUTION
```

### ChatGPT effort selection

`ChatGPT Effort` configures the recommended reasoning effort for the **next ChatGPT Orchestrator intervention required to advance the canonical frontier**.

That intervention may be:

- the next material step in the current chat while the current D067 objective remains active;
- the ChatGPT continuation after an intervening Human decision/gate;
- the ChatGPT review/convergence step after an intervening Executor action;
- the first substantive intervention in a successor chat after D067 handoff; or
- a bounded status/bootstrap/reconciliation intervention when no broader material objective is yet authorized.

Use the minimum sufficient effort for the expected intervention:

- `MEDIUM` — normal default for bounded, direct orchestration with limited exploration, synthesis or cross-checking;
- `HIGH` — when the next ChatGPT intervention is expected to require materially deeper or longer reasoning, substantial research/synthesis, broad cross-file or cross-authority reconciliation, or multiple consequential verification steps.

If an intervening Human/Executor result may materially alter the required effort, emit the minimum sufficient recommendation supported by the current canonical envelope and revalidate it before material ChatGPT work begins. Do not omit the field merely because another actor acts first or because a new chat is required.

This recommendation is qualitative. Agent Governance SHALL NOT infer, publish or enforce a wall-clock duration, timeout, minute budget, or fixed mapping from `MEDIUM`/`HIGH` to execution time. Runtime behavior remains provider-controlled and may vary.

`ChatGPT Effort` is distinct from D055. D055 configures the concrete **Executor** launch profile; this field configures only the Human-facing recommendation for ChatGPT. One MUST NOT be inferred from the other.

### Execution-shape selection

`Execution Shape` configures only the decomposition geometry of a **concrete next ChatGPT Orchestrator task** under D080.

- `SINGLE_EXECUTION` — attempt the material task as one bounded coherent execution unit because no consequential intermediate dependency/gate requires a durable split;
- `MULTI_EXECUTION` — decompose the task into ordered bounded execution units because its dependency, gate, failure-isolation or durable-resumption geometry makes the split materially useful.

Execution shape is qualitative and orthogonal to `ChatGPT Effort`. `HIGH` does not imply `MULTI_EXECUTION`, and `MEDIUM` does not imply `SINGLE_EXECUTION`.

D080 defines the controlling selection criteria, ordered-unit requirements, reclassification rule and prohibition on minute budgets/provider timeout assumptions.

`Execution Shape` is also distinct from D055. It does not configure Executor model, reasoning, speed, session continuity, child topology or provider/model-call authorization.

When `MULTI_EXECUTION` is selected and the immediate unit is known, `Próxima Tarea` SHOULD identify that immediate unit. The compact ordered sequence MAY also be shown when it materially improves navigation.

When the immediate frontier is not itself a ChatGPT Orchestrator task — for example, a Human decision or an Executor action — `Próxima Tarea` SHALL still emit `ChatGPT Effort` for the next ChatGPT intervention that follows or handles that frontier. `Execution Shape` MAY be omitted until a concrete material ChatGPT task exists; if the canonical checkpoint already defines that task, it SHALL be emitted normally.

### Same-chat and cross-chat invariance

The closure rule is invariant to chat turnover.

- `KEEP_CURRENT_CHAT`: emit `Próxima Tarea` plus `ChatGPT Effort`; emit `Execution Shape` when the next concrete ChatGPT task is known.
- `ELIGIBLE`: same requirement; eligibility for a new chat does not suppress effort.
- `NEW_CHAT_RECOMMENDED`: same requirement, and the successor bootstrap SHOULD carry the recommended ChatGPT effort explicitly in addition to pointing to the canonical checkpoint.
- `WAITING_FOR_NEXT_OBJECTIVE`: emit the immediate Human-selection action in `Próxima Tarea` and still emit the effort recommended for ChatGPT's next bounded intervention after/around that selection. Do not infer or authorize an unselected material objective.
- Human gate / Executor-first frontier: describe that actor's immediate action, then emit the effort for the next ChatGPT intervention needed to consume/review/advance the result.

### Source of truth

The Orchestrator SHALL derive `Próxima Tarea`, `ChatGPT Effort` and, when applicable, `Execution Shape` from the current canonical repository state, including the current checkpoint, controlling Task Contract/Decision and applicable SDD stage boundary.

Prior chat or Project Memory MUST NOT be used as authority when it conflicts with Git.

### Authorization boundary

`Próxima Tarea`, `ChatGPT Effort` and `Execution Shape` are navigation/configuration metadata only.

They MUST NOT:

- authorize or start the described task by themselves;
- imply that a Human-selected objective exists when the checkpoint still says `WAITING_FOR_NEXT_OBJECTIVE`;
- bypass Bootstrap -> explicit validation -> Task execution separation;
- skip SDD ownership/stage gates;
- launch an Executor, call a provider/model, mutate a branch, or enter a dependent task merely because it is named as next;
- convert a ChatGPT effort recommendation or execution shape into an Executor/Codex launch profile;
- convert a `MULTI_EXECUTION` plan into authority to run later units before their preceding gates pass.

When the next task is only **permitted** but has not been explicitly selected, the wording SHALL make that distinction clear. The mandatory effort recommendation configures the next ChatGPT intervention only; it is not evidence that a material objective has been selected.

### Blocked and waiting states

If the current frontier is blocked, `Próxima Tarea` SHALL describe the next required unblock, re-entry, review, or Human decision rather than inventing downstream work, and SHALL still emit `ChatGPT Effort` for the next ChatGPT intervention needed to advance or process that frontier.

If there is no material next task authorized or inferable from canonical state, the section SHALL state that the Orchestrator is waiting for the Human Owner to select the next objective and SHALL still emit `ChatGPT Effort` for the next bounded ChatGPT selection/bootstrap/status intervention. `Execution Shape` is omitted unless the checkpoint already defines a concrete next ChatGPT task whose execution is merely waiting for Human selection.

### Brevity

The task description SHOULD normally be one concise sentence. `ChatGPT Effort` SHOULD occupy one additional compact line. `Execution Shape`, when applicable, SHOULD occupy one additional compact line. When `MULTI_EXECUTION` is selected, one additional compact immediate-unit or sequence line is acceptable. Additional detail belongs in the main response or canonical artifacts, not in the closure label.

## Consequences

- Human-facing closure becomes consistent and immediately actionable.
- Every project closure exposes the recommended ChatGPT reasoning effort, independent of same-chat/cross-chat routing or intervening Human/Executor gates.
- A concrete next ChatGPT task additionally exposes its execution geometry without requiring geometry to be invented for actor-first/waiting states.
- No unstable estimate of ChatGPT execution duration becomes governance policy.
- ChatGPT effort and execution shape remain independent controls and both remain separate from D055 Executor launch configuration.
- Canonical Git remains authoritative; the response footer is not a second task registry.
- Existing SDD, branching, ownership, Task Contract, Executor and checkpoint rules are otherwise unchanged.

## Current application

This refinement does not by itself change substantive task authority. The current checkpoint remains authoritative for the frontier and shall carry `Next-ChatGPT-Effort` unconditionally for the next required ChatGPT intervention, plus `Next-Execution-Shape` whenever it names a concrete next ChatGPT task.
