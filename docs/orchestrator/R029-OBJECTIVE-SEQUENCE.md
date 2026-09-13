# R029 Incremental Objective Sequence

Status: ACTIVE  
Parent-Research: `docs/research/R029-AGENTS-SKILL-ARCHITECTURE-REFACTOR-RESEARCH.md`  
Authority: Human Owner selected incremental objective execution on 2026-09-13  
Lifecycle: D067 — one Human objective per ChatGPT Orchestrator chat  
Decision-State: EVALUATING  

## Execution rule

R029 follow-up is decomposed into independent Human objectives. Each objective is executed in a fresh ChatGPT Orchestrator chat, reaches its own durable completion gate, and returns to a Human gate before any successor objective starts.

There is **no automatic progression** from one objective to the next. Completion of one objective establishes only eligibility for the Human Owner to select its successor. This sequence does not authorize a root `AGENTS.md` rewrite, Skill implementation, normative decision, Executor/Codex launch, provider/model evaluation, or T066 work.

The objective sequence is:

```text
R029-O1 -> R029-O2 -> R029-O3 -> R029-O4 -> R029-O5
         -> R029-O6 -> R029-O7 -> R029-O8 -> R029-O9 -> R029-O10
         -> HUMAN DECISION GATE
```

Each objective has its own D080 execution-shape classification. These are separate D067 objectives, not D080 execution units of one oversized objective.

## Objective registry

| ID | Status | Objective | Prerequisites | Durable output | Completion gate | ChatGPT Effort | Execution Shape |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R029-O1 | SELECTED_NEXT | Root preservation-map audit | R029 integrated | Verified root semantic preservation map with gaps/conflicts | Every current root semantic unit has exactly one preservation classification/destination, with unresolved conflicts explicitly listed | MEDIUM | SINGLE_EXECUTION |
| R029-O2 | NOT_STARTED | Lean-root responsibility contract | O1 accepted | Candidate always-on root responsibility contract | Every retained root item is justified as pre-routing authority/safety/bootstrap; every omitted detail remains reachable through an explicit destination class | MEDIUM | SINGLE_EXECUTION |
| R029-O3 | NOT_STARTED | Maintainer Skill domain boundary | O1-O2 accepted | Agent-Governance-specific domain-routing map | Source-maintenance-specific workflows are separated from transverse candidates without splitting the approved Maintainer Skill by role | MEDIUM | SINGLE_EXECUTION |
| R029-O4 | NOT_STARTED | `repository-change-control` candidate | O1-O3 accepted | Candidate contract, triggers/anti-triggers, host-adapter boundary, analytical disposition | Reusable intent and non-overlap are explicit; candidate is classified `KEEP_CANDIDATE`, `INTERNAL_ROUTE`, or `REJECT_FOR_TRANSVERSE` as research/evaluation only | MEDIUM | SINGLE_EXECUTION |
| R029-O5 | NOT_STARTED | `upstream-version-revalidation` candidate | O1-O3 accepted | Candidate contract, triggers/anti-triggers, adapter boundary, analytical disposition | Generalizable semantics are separated from D077/Agent-Governance-specific policy and candidate disposition is explicit | MEDIUM | SINGLE_EXECUTION |
| R029-O6 | NOT_STARTED | `research-evidence-traceability` candidate | O1-O3 accepted | Generic capability vs Agent Governance adapter map and disposition | Reusable research/decision provenance semantics are separated from `Rxxx`/`Dxxx` repository conventions | MEDIUM | SINGLE_EXECUTION |
| R029-O7 | NOT_STARTED | `durable-work-checkpoint` candidate | O1-O3 accepted | Generic cold-start/frontier capability vs Agent Governance checkpoint adapter map and disposition | Generic durable-resume semantics are separated from D027/D067/checkpoint-specific rules | MEDIUM | SINGLE_EXECUTION |
| R029-O8 | NOT_STARTED | `executor-launch-handoff` candidate | O1-O3 accepted | Generic launch/handoff capability vs Agent Governance Task Contract/D055 adapter map and disposition | Reusable transport/session/handoff behavior is separated from repository-specific authority and acceptance semantics | MEDIUM | SINGLE_EXECUTION |
| R029-O9 | NOT_STARTED | Workspace-isolation placement | O4 and O8 accepted | Placement analysis and explicit disposition | Workspace isolation is classified as a sub-route/reference or a standalone transverse candidate based on distinct intent/trigger evidence | MEDIUM | SINGLE_EXECUTION |
| R029-O10 | NOT_STARTED | Candidate-topology synthesis and evaluation plan | O1-O9 accepted | One bounded candidate topology plus pre-decision evaluation plan | Candidate skill/root topology, preservation coverage, trigger-eval plan, context-efficiency plan, functional-equivalence plan, cross-host checks and deterministic checks are coherent; no adoption occurs | HIGH | SINGLE_EXECUTION |

## Objective details

### R029-O1 — Root preservation-map audit

**Scope**

Audit the current `develop` root `AGENTS.md` against R029's semantic inventory. Confirm that every material current rule is represented exactly once in a preservation map as:

- always-on root invariant;
- root trigger plus Agent-Governance domain route;
- root trigger plus transverse candidate;
- domain route;
- reference/deterministic mechanism.

**Out of scope**

- designing the lean root;
- deciding Skill topology;
- writing or changing `AGENTS.md`;
- creating Skills;
- provider/model evaluation.

**Required durable output**

A persisted O1 result containing the complete preservation map, any duplicate/ambiguous classifications, and any uncovered current root semantics.

**Completion gate**

No material root semantic unit remains unclassified. Any disagreement is recorded as an explicit gap rather than silently resolved.

### R029-O2 — Lean-root responsibility contract

Define only the responsibility boundary of the future always-loaded root. Do not draft the final root file and do not design individual transverse Skills.

Completion requires a compact set of always-on responsibilities justified by the need to establish authority, safety, mutation boundaries, cold-start behavior, and routing constraints before optional Skill activation.

### R029-O3 — Maintainer Skill domain boundary

Define what remains specific to maintaining the Agent Governance source product and therefore belongs in the existing Maintainer Skill or its on-demand references.

Preserve the approved single top-level Maintainer Skill with internal Orchestrator/Executor routes. Do not create role-named top-level Skills.

### R029-O4 — `repository-change-control`

Evaluate this candidate independently. Define reusable semantic intent, positive and negative triggers, output/postcondition contract, authority boundaries, and ChatGPT/Codex host-adapter differences.

The result is an analytical candidate disposition only, not adoption or implementation.

### R029-O5 — `upstream-version-revalidation`

Evaluate whether D077's reusable engineering pattern warrants a transverse capability. Separate universal revalidation semantics from Agent Governance decision vocabulary and repository policy.

### R029-O6 — `research-evidence-traceability`

Evaluate reusable evidence/provenance semantics separately from Agent Governance's `Rxxx`, `Dxxx`, registry, and checkpoint conventions.

### R029-O7 — `durable-work-checkpoint`

Evaluate the reusable cold-start/durable-frontier pattern separately from the exact Agent Governance D027/D067 checkpoint schema and lifecycle.

### R029-O8 — `executor-launch-handoff`

Evaluate reusable launch/session/transport/handoff behavior separately from D055 model/effort policy, Task Contract authority, ownership, and acceptance semantics.

### R029-O9 — Workspace-isolation placement

Determine whether workspace isolation has a genuinely separate user intent and trigger boundary or should remain a route/reference inside `repository-change-control` and/or `executor-launch-handoff`.

Standalone Skill status requires positive evidence; it is not the default.

### R029-O10 — Candidate topology synthesis and evaluation plan

Consume only accepted durable O1-O9 outputs. Produce one coherent pre-decision candidate architecture and the smallest evaluation plan required before any normative adoption.

At minimum, cover:

- preserved-behavior/root coverage;
- explicit/implicit/negative/near-miss/collision Skill routing cases;
- wrong-authority activation cases;
- baseline-vs-candidate context loading;
- functional-equivalence source-maintenance workflows;
- ChatGPT/Codex cross-host behavior;
- deterministic structural/package checks;
- D077 refresh requirements before consequential reliance.

O10 does not authorize running provider/model evals, writing a Decision Record, refactoring `AGENTS.md`, or implementing Skills.

## Human gates

After every objective:

```text
objective complete
-> persist result and checkpoint
-> Human Owner reviews/selects next objective
-> fresh ChatGPT chat bootstraps from current develop
-> only then execute the selected successor
```

A later objective is never implied merely because its prerequisite becomes complete.

After R029-O10, stop at a Human decision gate. Any normative architecture Decision Record, empirical provider/model qualification, root `AGENTS.md` refactor, Skill package creation, or implementation must be separately selected and authorized.

## Global prohibitions

Until separately authorized:

- do not change current role, stage, Markdown, oracle, or execution-mechanics ownership;
- do not rewrite root `AGENTS.md`;
- do not create/package/install/release transverse Skills;
- do not split the Maintainer Skill by ChatGPT/Codex role;
- do not launch Codex/another Executor;
- do not consume provider/model calls or create scored observations;
- do not promote R029 from research/evaluation into normative policy;
- do not start the successor objective automatically;
- do not mutate the unselected T066 scientific branch.
