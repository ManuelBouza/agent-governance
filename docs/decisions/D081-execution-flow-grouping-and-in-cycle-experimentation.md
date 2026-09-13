# D081 — Execution-Flow Grouping and In-Cycle Experimentation

Status: ACCEPTED  
Date: 2026-09-13  
Authority: Human Owner / ChatGPT Orchestrator  
Scope: source-product ChatGPT Orchestrator execution grouping, in-cycle adaptation and normative-promotion boundary

## Context

D067 scopes a ChatGPT Orchestrator chat to one explicit Human objective. D080 independently classifies the geometry of a concrete ChatGPT task as `SINGLE_EXECUTION` or `MULTI_EXECUTION`.

Those rules do not by themselves make a trace/decomposition subtask an execution unit, nor do they define how an in-scope Human adjustment during an active execution is handled without either silently turning it into policy or unnecessarily breaking the active objective.

D081 refines D067 and D080 prospectively. It preserves their objective identity, closure, bootstrap, effort/shape separation and fail-closed boundaries.

## Decision

Agent Governance distinguishes three different layers:

```text
subtask / trace unit
    != execution unit
    != normative decision
```

A trace unit exists to decompose, name or evidence work. An execution unit exists only when task geometry justifies a bounded material execution boundary. A normative decision exists only when the applicable authority explicitly adopts durable policy or product semantics.

No identifier, checklist item, file family, analytical subproblem or trace node creates an execution boundary merely by existing.

## Execution grouping rule

Related consecutive subtasks SHALL normally remain in the same execution when all of the following remain true:

- they operate under the same Human objective and authority envelope;
- they share the same controlling context, specification/Design, invariants and acceptance meaning;
- they form one coherent flow whose later work can safely proceed from the same active state;
- no earlier result must first be frozen, independently verified, revalidated or Human-accepted before later material work is safe;
- no materially distinct failure domain requires isolation; and
- no durable-resumption boundary is needed to make completed work independently authoritative before continuation.

This is the default grouping rule even when the execution contains many trace IDs, files, artifacts or internal subtasks.

### Real split conditions

Use separate ordered execution units only when at least one concrete material boundary exists, such as:

- a downstream unit depends on an upstream result that must become a controlling prerequisite before continuation;
- a mandatory freeze, verification, revalidation, review, convergence or Human-acceptance gate intervenes;
- authority, ownership, specification/Design, safety envelope or acceptance meaning changes;
- failure isolation is materially valuable because one workstream can fail without invalidating another already-complete workstream;
- a durable checkpoint is required so completed material work can survive interruption without reconstruction or ambiguity; or
- the current unit cannot safely determine the next unit until its own result is represented and evaluated.

When classification is borderline, preserve D080's default: prefer `SINGLE_EXECUTION` unless a concrete dependency, gate, failure-domain or durable-resumption benefit justifies `MULTI_EXECUTION`.

Do not manufacture micro-executions merely because the plan contains multiple subtasks or trace identifiers.

## In-cycle Human adaptation

A Human Owner request arriving while an execution/cycle is active does not automatically complete the D067 objective, require a new chat, create a new execution, or become product policy.

When the requested change remains inside the current objective and the existing authority, ownership, specification/Design, safety and acceptance envelope, the Orchestrator MAY apply it locally as:

```text
EXPERIMENTAL_IN_CYCLE
```

The adaptation is an explicitly local experimental variation of the active execution/cycle. It is evidence-generating behavior, not normative authority.

### Required trace

Every `EXPERIMENTAL_IN_CYCLE` adaptation SHALL durably identify, at the level appropriate to the active workflow:

- what changed;
- why it changed;
- which execution/cycle it affects;
- which prior assumptions, invariants and authority remain unchanged;
- what evidence will determine whether the adaptation helped, harmed or remained inconclusive; and
- that the adaptation is not yet normative policy or product authority.

The trace may live in an existing Task Contract, evaluation record, experiment artifact, checkpoint or another already-authoritative project artifact. A new artifact is not required solely for ceremony.

## Stop / re-entry boundary

`EXPERIMENTAL_IN_CYCLE` MUST NOT be used to bypass a material change to:

- the Human objective;
- authority or ownership;
- accepted specification or controlling Design;
- safety/security envelope;
- acceptance criteria or acceptance meaning; or
- another mandatory Human or normative gate.

A change in any of those categories follows the existing stop/re-entry, objective, SDD, Human-approval and/or execution-shape rules. Local experimental labeling does not make an otherwise unauthorized change permissible.

## End-of-cycle evaluation

At the close of the relevant cycle, every `EXPERIMENTAL_IN_CYCLE` adaptation SHALL be evaluated against the controlling objective, acceptance meaning and observed evidence.

Allowed dispositions are:

```text
RETAIN
REVISE
REJECT
RECOMMEND_PROMOTION
```

`RETAIN` means the adaptation may remain as local experimental practice/evidence inside the still-authorized experimental context; it does not become general policy. `REVISE` and `REJECT` preserve the evidence and record the resulting adjustment or abandonment. `RECOMMEND_PROMOTION` means the evidence is sufficient to propose a later normative decision.

The promotion path is:

```text
EXPERIMENTAL_IN_CYCLE
    -> evidence at cycle close
    -> retain / revise / reject / recommend promotion
    -> explicit normative decision when promotion is desired
    -> materialization only after that decision authorizes it
```

Successful local experimentation never self-promotes.

## Relationship to D067

D067's one-objective-per-chat rule remains unchanged.

An in-scope Human adjustment during `ACTIVE` work remains part of the same objective when it preserves the active objective and controlling authority envelope. It therefore does not require chat retirement or successor bootstrap merely because it was requested after execution began.

A materially new objective still requires normal D067 completion and successor routing.

## Relationship to D080

D080 remains the execution-geometry control. D081 refines what counts as a legitimate execution boundary.

The controlling rule is:

```text
trace decomposition
    -> does not imply execution decomposition

shared authority + shared context/invariants + coherent flow + no material gate
    -> group in one execution

real controlling dependency / gate / failure boundary / durable-resumption boundary
    -> split into ordered executions
```

`ChatGPT Effort: MEDIUM | HIGH` remains orthogonal to `Execution Shape: SINGLE_EXECUTION | MULTI_EXECUTION`.

Execution Shape SHALL continue to depend on task geometry and dependencies, not on minute budgets, token budgets, provider/session folklore or assumed OpenAI limits.

## Prospective application to T066 Stage 5

The future Stage 5 of `docs/tasks/T066-r027-chatgpt-codex-efficiency-evaluation.md` is prospectively classified:

```text
ChatGPT Effort: HIGH
Execution Shape: SINGLE_EXECUTION
```

Reason: the Stage 5 fixture/oracle/scheduler/scoring/receipt/instruction-control items are trace/decomposition units under one T066 authority envelope, share the same experimental constants and acceptance meaning, and converge into one coherent provider-free `Freeze A` before any scored Codex execution. The current Task Contract does not require an intermediate Human acceptance, independent freeze, controlling revalidation gate, failure-domain handoff or durable-resumption boundary between those Stage 5 materialization subtasks.

Therefore they should be materialized as one coherent Stage 5 execution when separately authorized. Internal ordering remains valid and necessary, but internal order alone does not create multiple executions.

This prospective classification SHALL be re-evaluated before or during Stage 5 if new authoritative information creates a real gate. In particular, if a required revalidation or other prerequisite yields a result that must be frozen/accepted before later materialization can safely continue, D080 permits reclassification to `MULTI_EXECUTION` with an explicit ordered plan.

This decision does **not** start T066 Stage 5, create its scientific branch, consume the preexisting `test/r027-chatgpt-codex-efficiency-v1` branch, authorize Executor/Codex, or authorize any provider/model call.

## Effective rule

```text
identify one Human objective
-> decompose for reasoning/traceability as needed
-> do not map trace units mechanically to executions
-> group related work while authority/context/invariants remain shared and no real gate exists
-> split only at a justified material boundary
-> allow in-scope Human adjustments as EXPERIMENTAL_IN_CYCLE with durable trace
-> evaluate adaptations at cycle close
-> require an explicit later normative decision before promotion/materialization
```
