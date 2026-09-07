# D070 — Orchestrator visible work narration and compact completion

Status: ACCEPTED  
Date: 2026-09-07  
Scope: ChatGPT Orchestrator Human-facing work visibility and completion reporting

## Context

D069 standardizes the final `Próxima Tarea` closure, but it does not define how much information the Human Owner should receive while a non-trivial source-product task is being carried out.

The Human Owner wants two complementary information layers:

1. a more detailed, expandable view during execution that makes the intended action, important constraints, and observed result understandable; and
2. a compact final report that summarizes what was completed and ends with the canonical next task.

This separation lets the Human Owner inspect the work path when useful without forcing the final answer to become a transcript.

## Decision

For non-trivial Agent Governance source-product orchestration, the Orchestrator SHALL use a two-layer Human-facing reporting model.

### Layer 1 — visible work narration

During Bootstrap and task execution, the Orchestrator SHALL provide concise but substantive progress updates at meaningful boundaries.

A useful update SHOULD explain, as applicable:

- **what is being attempted now** and the immediate purpose;
- **which material authority, invariant, guardrail, or stop condition controls the step**;
- **what result or evidence the step produced** once known;
- **what the next immediate sub-step is** when that improves orientation.

The narration SHOULD contain enough detail for the Human Owner to understand the work path, material decisions, and observed outcomes when inspecting the expanded execution view.

The narration MUST NOT become command-by-command noise, duplicate every tool call, or bury important findings in low-level mechanics. It SHOULD surface material results as soon as they are known.

### Reasoning boundary

Visible work narration is an operational rationale and evidence summary. It is not a requirement to expose private chain-of-thought, hidden scratch work, or internal token-by-token reasoning.

The Human Owner should be able to understand what the Orchestrator tried, why the step was relevant, what constraints applied, and what happened without requiring private internal reasoning.

### Layer 2 — compact completion report

When a project work unit, status check, convergence step, closure, or persisted repository change is reported to the Human Owner, the final answer SHALL remain compact and outcome-oriented.

It SHOULD normally contain:

- the completion or terminal status;
- the most important work completed;
- key remote artifacts, identifiers, branch/PR/commit/checkpoint facts when material;
- important preserved boundaries or deliberately unperformed actions when they affect interpretation;
- any blocker or Human hold that constrains continuation.

The final report SHOULD summarize rather than replay the visible work narration.

### `Próxima Tarea`

D069 remains controlling for response closure.

The final project response SHALL end with the section title exactly:

```text
Próxima Tarea
```

followed by the concise canonical next action derived from current Git/checkpoint state.

Nothing in the work narration or final summary creates authorization merely by describing a possible next action.

### Partial and blocked work

If the objective is partial, blocked, waiting on the Human Owner, or intentionally frozen, both layers SHALL represent that state explicitly.

The narration SHALL explain the material stop condition when it becomes known. The compact final report SHALL state the terminal condition and the `Próxima Tarea` section SHALL describe the required unblock, Human decision, or waiting state rather than inventing downstream work.

## Consequences

- The Human Owner can inspect a more informative execution narrative when desired.
- The final answer remains fast to scan and suitable as a compact project-status report.
- Material constraints and outcomes become visible earlier during long tasks.
- D069 remains the canonical final-closure rule.
- Git/checkpoint authority, Bootstrap separation, SDD ownership, Task Contracts, Executor boundaries, branching rules, and safety gates are unchanged.

## Current application

At acceptance of D070, T061 remains technically `READY_FOR_STAGE6`, but the Human Owner has explicitly frozen continuation at that boundary. The current checkpoint records that Human hold. Stage 6 MUST NOT start until the Human Owner explicitly lifts the hold and selects continuation through a new objective.
