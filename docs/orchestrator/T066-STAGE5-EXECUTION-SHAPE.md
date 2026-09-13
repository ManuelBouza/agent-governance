# T066 Stage 5 — Prospective Orchestrator Execution Shape

Status: PROSPECTIVE_BLOCKED  
Date: 2026-09-13  
Parent-Task-Contract: `docs/tasks/T066-r027-chatgpt-codex-efficiency-evaluation.md`  
Policy: `docs/decisions/D080-orchestrator-execution-shape-control.md`  
ChatGPT-Effort: HIGH  
Execution-Shape: MULTI_EXECUTION  
Sequence: `T066-S5-E1 -> T066-S5-E2 -> T066-S5-E3 -> T066-S5-E4`

## Authority boundary

This file is Orchestrator routing metadata for the prospective ChatGPT execution geometry of T066 Stage 5. It does **not** define or modify scientific requirements, scored-arm topology, Task Contract semantics, Executor configuration, provider/model authorization or acceptance meaning.

If this routing artifact conflicts with T066, T066 controls and material work stops for reconciliation.

The plan is currently blocked because remote Git contains a pre-existing divergent `test/r027-chatgpt-codex-efficiency-v1` Freeze A surface that contradicts the later canonical checkpoint which stated Stage 5 was deferred and the branch was not created. No unit below may start until that branch conflict receives an explicit Human disposition and the resulting T066 readiness/branch authority is revalidated.

## Geometry rationale

T066 Stage 5 is `MULTI_EXECUTION` because downstream materialization depends on consequential upstream results and gates:

```text
frozen experiment/control skeleton
-> complete benchmark/spec/oracle surface
-> harness/accounting/provider-free preflight surface
-> whole-candidate Freeze A convergence
```

The split isolates failure domains and provides durable resumption boundaries. It is not based on elapsed-time estimates, minute budgets, provider timeouts, token ceilings or a fixed relationship to `ChatGPT Effort: HIGH`.

## T066-S5-E1 — Freeze architecture and experiment-control skeleton

**Scope**  
Once the branch conflict is explicitly resolved and T066 Stage 5 is selected, establish/verify the authorized scientific branch from the then-current canonical baseline and materialize the static experiment-control skeleton: exact phase/pair topology, opaque arm identities, frozen constants, deterministic randomization seed/order, common verification contract, isolation/contamination rules and terminal/scoring schema contracts.

**Prerequisites**  
Fresh-chat bootstrap; explicit Human Stage 5 selection; pre-existing branch conflict resolved; T066 remains `READY_FOR_STAGE5`; D080/D079/T066 authority revalidated.

**Required output / durable boundary**  
An exact remotely represented scientific-branch checkpoint containing the frozen control skeleton and enough identities for E2 to consume without reconstructing intent from chat.

**Completion gate**  
All nine pair slots and phase/gate relationships are represented consistently; randomization/order and shared constants are frozen; no scored output/provider/model call exists; no material T066 semantic conflict is found.

**Next-unit condition**  
E1 remote state is reviewed against T066 and accepted as the controlling Stage 5 skeleton.

## T066-S5-E2 — Benchmark fixtures, specifications and semantic oracles

**Scope**  
Materialize the three archetype fixture families and all nine isomorphic matched-pair variants, deterministic task specifications and Design/Plan envelopes, D052 acceptance oracles, cross-arm contamination guards and provider-free geometry/integrity checks.

**Prerequisites**  
Accepted E1 exact remote state.

**Required output / durable boundary**  
An exact remotely represented scientific-branch checkpoint containing complete benchmark/fixture/spec/oracle assets bound to E1 identities and constraints.

**Completion gate**  
Isomorphism and isolation are deterministically checkable; all variant acceptance meanings are complete; no control-solution leakage or scored model output exists; any semantic/design defect causes re-entry rather than progression.

**Next-unit condition**  
E2 benchmark/oracle surface is internally coherent and preserves the frozen E1 topology.

## T066-S5-E3 — Harness, accounting and provider-free launch-preflight assets

**Scope**  
Materialize the arm scheduler/isolation enforcement, scoring implementation, usage/credit normalization, terminal-result representation, instruction-loading proof mechanism/exact envelope, prospective run-ceiling controls, applicable version/model/accounting receipts and D077 revalidation evidence required by T066 before live launch.

**Prerequisites**  
Accepted E1 + E2 exact remote state; still no live scored execution.

**Required output / durable boundary**  
An exact remotely represented scientific-branch checkpoint containing the complete provider-free harness/preflight surface and current volatile-fact receipts needed for Freeze A.

**Completion gate**  
Deterministic/provider-free checks pass; measurement/accounting logic is prospectively frozen; complete instruction loading can be proved by the designed preflight surface; D077 disposition is explicit for launch-sensitive facts; no provider/model call or scored output has been consumed.

**Next-unit condition**  
E3 adds no conflict with E1/E2 and leaves only whole-candidate Freeze A convergence/publication.

## T066-S5-E4 — Freeze A convergence and remote publication

**Scope**  
Reconcile E1-E3 as one coherent candidate, review the complete remote diff/state against the T066 Stage 5 deliverable checklist, repair only in-scope Stage 5 inconsistencies, run all provider-free integrity checks, and publish the exact Freeze A branch checkpoint.

**Prerequisites**  
Accepted E1 + E2 + E3 exact remote states.

**Required output / durable boundary**  
One exact remotely verified Freeze A scientific-branch HEAD containing the complete T066 Stage 5 candidate and zero scored model outputs.

**Completion gate**  
Every T066 Freeze A deliverable is represented; provider-free checks/integrity evidence are green; branch/head and authority identities are exact; provider/model-call count remains `0`; scored observations remain `0`; readiness or a precise blocker is durably represented.

**Next-unit condition**  
There is no automatic E5. Stop. Any live measurement/Executor launch requires a later explicit Human selection plus applicable D055/D071/D077 gates.

## Execution rules

- The four units are bounded execution units inside one prospective D067 Human objective, not four backlog tasks.
- Do not enter a later unit until the preceding completion gate is durably satisfied.
- Intermediate unit boundaries do not require separate merges to `develop`; exact remote scientific-branch state is sufficient when the active workflow permits it.
- A material requirement/Design/Plan defect triggers normal SDD re-entry rather than local semantic invention.
- No unit in this Stage 5 plan authorizes Codex/Executor/provider/model calls or scored observations.
- The plan must be revalidated after the pre-existing branch conflict is resolved and before E1 starts.
