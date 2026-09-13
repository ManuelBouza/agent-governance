# D080 — Orchestrator Execution Shape Control

Status: ACCEPTED  
Date: 2026-09-13  
Authority: Human Owner / ChatGPT Orchestrator  
Scope: source-product ChatGPT Orchestrator task geometry and decomposition

## Context

D067 defines one explicit Human objective per ChatGPT Orchestrator chat, and D069 exposes the recommended `ChatGPT Effort` for the next required ChatGPT intervention. Neither rule determines whether one Human objective should be attempted as one material ChatGPT execution or decomposed into several ordered executions.

Agent Governance therefore needs a separate control for **execution geometry**. This control must not depend on guessed provider timeouts, minute budgets, context-duration folklore, or a fixed mapping from reasoning effort to runtime.

## Decision

For every concrete next ChatGPT Orchestrator task whose geometry is materially relevant, the Orchestrator SHALL classify:

```text
Execution Shape: SINGLE_EXECUTION | MULTI_EXECUTION
```

The two Human-facing controls answer different questions:

```text
ChatGPT Effort: MEDIUM | HIGH
    -> how much reasoning depth the next required ChatGPT intervention warrants

Execution Shape: SINGLE_EXECUTION | MULTI_EXECUTION
    -> whether a concrete material ChatGPT task should be attempted as one bounded execution unit
       or decomposed into several ordered bounded execution units
```

`ChatGPT Effort` is always present in D069 project closure. `Execution Shape` applies when a concrete ChatGPT task exists to classify; it need not be invented for a Human-only gate, Executor-first frontier, or waiting state that has not yet produced a concrete material ChatGPT task.

`Execution Shape` is qualitative task-geometry metadata. It does not specify wall-clock duration and does not claim any OpenAI/provider timeout, session lifetime, token ceiling, or guaranteed completion window.

## Execution-unit semantics

An **execution unit** is a bounded segment of material ChatGPT Orchestrator work inside one D067 Human objective.

A unit has:

- a defined scope;
- known prerequisites;
- a concrete output or durable state transition;
- an observable completion condition;
- a defined gate into the next unit when one exists.

Multiple execution units do **not** create multiple Human objectives merely because the work is split. The parent D067 objective remains one objective until all required units, integration, acceptance, persistence and closure are complete.

`MULTI_EXECUTION` also does not by itself require a new chat, new topic branch, new PR, new Executor session, or merge between every unit. Existing D067, D061/D062, SDD, Task Contract and branching rules continue to decide those boundaries.

## Selection rule

Use `SINGLE_EXECUTION` when the material task can be completed coherently as one bounded unit without an intermediate result that must become a controlling prerequisite for later material work.

Typical indicators are:

- the dependency graph is predominantly linear and shallow;
- the required authority, inputs and acceptance conditions are already stable;
- one coherent artifact set can be authored/reviewed together;
- there is no mandatory intermediate freeze, revalidation, review or convergence gate that changes what later work may safely do;
- failure or correction can be handled locally without invalidating a large independent body of already-completed work.

Use `MULTI_EXECUTION` when the task has material internal geometry that should be made explicit before execution. Strong indicators include one or more of the following:

- downstream work depends on an upstream result that must first be completed, inspected or durably represented;
- the task contains a mandatory intermediate freeze, verification, revalidation, review or convergence gate;
- multiple materially distinct artifact families must be produced and then reconciled under shared invariants;
- the task contains several substantial materialization/review cycles whose failure domains should remain separable;
- later work would be unsafe, ambiguous or wastefully duplicative if begun before an earlier sub-result is accepted;
- a clean durable boundary allows completed work to survive interruption without forcing reconstruction from chat history.

No fixed count of files, lines, tool calls, reasoning steps or subproblems controls the classification. A task touching many files may still be `SINGLE_EXECUTION` if it is one coherent transformation; a smaller task may be `MULTI_EXECUTION` if it has consequential ordered gates.

When classification is genuinely borderline, prefer `SINGLE_EXECUTION` unless a concrete dependency, gate, failure-isolation benefit, or durable resumption boundary justifies the split. Do not manufacture micro-executions merely for ceremony.

## MULTI_EXECUTION planning rule

Before beginning material work classified `MULTI_EXECUTION`, the Orchestrator SHALL define an ordered execution plan:

```text
E1 -> E2 -> ... -> En
```

Each unit SHALL state, at minimum:

```text
Unit
Scope
Prerequisites
Required output / durable boundary
Completion gate
Next-unit condition
```

The plan must preserve one parent objective and one acceptance meaning. A later unit may refine implementation detail inside already-approved semantics, but a material requirement/Design/Plan defect still follows the normal SDD re-entry rule.

When an intermediate output materially controls the next unit, that boundary SHALL be durable enough for cold-start reconstruction. Depending on the active workflow this may be an exact remote topic-branch commit, a persisted authoritative artifact, a checkpoint update, or another already-approved durable Git identity. It does not require merging incomplete work into `develop` merely to create a boundary.

If a unit fails its completion gate, later units SHALL NOT begin until the failure is repaired, the plan is prospectively revised under existing authority, or the objective is explicitly blocked.

## Relationship to ChatGPT Effort

Effort and shape are orthogonal.

Examples:

```text
MEDIUM + SINGLE_EXECUTION
HIGH   + SINGLE_EXECUTION
MEDIUM + MULTI_EXECUTION
HIGH   + MULTI_EXECUTION
```

A task does not become `MULTI_EXECUTION` merely because `HIGH` reasoning is recommended. A task does not become `SINGLE_EXECUTION` merely because its reasoning effort is `MEDIUM`.

The Orchestrator selects the minimum sufficient reasoning effort for the next required ChatGPT intervention and independently selects execution geometry whenever a concrete material ChatGPT task exists.

## Relationship to D055 and Executor configuration

D080 applies only to ChatGPT Orchestrator execution geometry.

It does not configure or infer:

- Executor model;
- Executor reasoning effort;
- Executor speed mode;
- Executor session continuity;
- child/subagent topology;
- provider/model call authorization.

Those remain under D055 and any controlling Task Contract/experimental authority.

## Human-facing representation

D069 requires every qualifying project response to end with `Próxima Tarea` and exactly one `ChatGPT Effort: MEDIUM | HIGH`, regardless of same-chat/cross-chat routing or whether a Human/Executor gate occurs first.

When that frontier also defines a concrete next ChatGPT Orchestrator task, the section SHALL additionally include:

```text
Execution Shape: SINGLE_EXECUTION | MULTI_EXECUTION
```

When `MULTI_EXECUTION` is selected, the Human-facing response SHOULD name the immediate execution unit. It MAY show the compact ordered sequence when doing so materially improves navigation, but the response footer remains navigation metadata rather than a second task registry.

## Checkpoint representation

`docs/orchestrator/CHECKPOINT.md` SHALL carry:

```text
Next-ChatGPT-Effort: MEDIUM | HIGH
```

for the next required ChatGPT intervention, including waiting, Human-gate, Executor-first and cross-chat frontiers.

It SHALL additionally carry:

```text
Next-Execution-Shape: SINGLE_EXECUTION | MULTI_EXECUTION
```

when the checkpoint names a concrete next ChatGPT Orchestrator task.

When `MULTI_EXECUTION` materially controls cold-start resumption, the checkpoint SHALL also identify the ordered execution units or point to the exact authoritative artifact that defines them, and SHALL identify the immediate next unit.

The checkpoint must remain a frontier router, not duplicate the full execution plan when another durable artifact already contains it.

## Reclassification

Execution shape is selected prospectively from the current known task geometry.

A task may be reclassified before or during execution when new authoritative information reveals that the original geometry is wrong. Reclassification requires an explicit updated plan/frontier before continuing material work; it must not be used to disguise an already-failed unit or retroactively rewrite evidence.

Typical reclassification cases:

- `SINGLE_EXECUTION -> MULTI_EXECUTION`: a new mandatory dependency/gate or separable material workstream is discovered;
- `MULTI_EXECUTION -> SINGLE_EXECUTION`: a planned boundary proves artificial because the units are one inseparable coherent transformation and no durable/gating value remains.

A mandatory `ChatGPT Effort` recommendation may also be revalidated when new Human/Executor evidence changes the next ChatGPT intervention. That effort revalidation is not an execution-shape reclassification unless the concrete task geometry also changed.

## Prohibitions

Agent Governance SHALL NOT use `Execution Shape` to:

- publish or enforce minute budgets;
- claim provider timeout or session-duration guarantees;
- infer a maximum safe execution duration from anecdotal runs;
- split tasks solely because an arbitrary elapsed-time threshold was reached;
- bypass D067 objective identity or create hidden new objectives;
- bypass SDD stage ownership, Task Contract authority, branch protection or Human gates;
- launch an Executor or consume provider/model calls.

## Effective rule

```text
project frontier known
-> always expose Próxima Tarea
-> always choose minimum sufficient ChatGPT Effort for the next required ChatGPT intervention
-> if a concrete material ChatGPT task exists, inspect dependency/gate/failure geometry
-> choose SINGLE_EXECUTION or MULTI_EXECUTION
-> if MULTI_EXECUTION, freeze ordered bounded units before material work
-> execute only the immediate authorized unit
-> revalidate effort/shape when new authoritative evidence changes them
-> advance through durable gates until the one Human objective is complete
```
