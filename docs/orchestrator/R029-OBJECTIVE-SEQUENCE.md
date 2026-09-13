# R029 Incremental Session Sequence

Status: ACTIVE  
Parent-Research: `docs/research/R029-AGENTS-SKILL-ARCHITECTURE-REFACTOR-RESEARCH.md`  
Authority: Human Owner clarified incremental same-chat execution on 2026-09-13  
Lifecycle: one persistent R029 ChatGPT Orchestrator objective with bounded session subtasks  
Decision-State: EVALUATING  

## Execution rule

R029 follow-up is one continuing Human objective executed in this same ChatGPT Orchestrator chat across bounded work sessions. The sequence is decomposed into short subtasks so only one material subtask is executed per session.

This is **not** a sequence of independent D067 objectives and does not require a fresh chat between subtasks. D067 remains satisfied because the parent Human objective remains R029 Skill-architecture evaluation; R029-S1 through R029-S10 are ordered subordinate work units inside that one objective.

There is **no automatic progression** from one subtask to the next. Each subtask must reach its own durable completion gate, be persisted, and return to a Human review gate before the next subtask is selected for a later session of this same chat.

The sequence does not authorize a root `AGENTS.md` rewrite, Skill implementation, normative decision, Executor/Codex launch, provider/model evaluation, or T066 work.

```text
R029 parent objective — same ChatGPT chat remains active

R029-S1 -> Human gate -> R029-S2 -> Human gate -> ... -> R029-S10
         -> HUMAN DECISION GATE
```

Each subtask has its own D080 execution-shape classification. These are bounded material work sessions under one continuing objective, not new D067 objectives.

## Subtask registry

| ID | Status | Subtask | Prerequisites | Durable output | Completion gate | ChatGPT Effort | Execution Shape |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R029-S1 | COMPLETE_AWAITING_HUMAN_REVIEW | Root preservation-map audit | R029 integrated | `docs/orchestrator/R029-S1-ROOT-PRESERVATION-MAP.md` | Every current root semantic unit has exactly one preservation classification/destination, with unresolved conflicts explicitly listed | MEDIUM | SINGLE_EXECUTION |
| R029-S2 | NOT_STARTED | Lean-root responsibility contract | S1 accepted | Candidate always-on root responsibility contract | Every retained root item is justified as pre-routing authority/safety/bootstrap; every omitted detail remains reachable through an explicit destination class | MEDIUM | SINGLE_EXECUTION |
| R029-S3 | NOT_STARTED | Maintainer Skill domain boundary | S1-S2 accepted | Agent-Governance-specific domain-routing map | Source-maintenance-specific workflows are separated from transverse candidates without splitting the approved Maintainer Skill by role | MEDIUM | SINGLE_EXECUTION |
| R029-S4 | NOT_STARTED | `repository-change-control` candidate | S1-S3 accepted | Candidate contract, triggers/anti-triggers, host-adapter boundary, analytical disposition | Reusable intent and non-overlap are explicit; candidate is classified `KEEP_CANDIDATE`, `INTERNAL_ROUTE`, or `REJECT_FOR_TRANSVERSE` as research/evaluation only | MEDIUM | SINGLE_EXECUTION |
| R029-S5 | NOT_STARTED | `upstream-version-revalidation` candidate | S1-S3 accepted | Candidate contract, triggers/anti-triggers, adapter boundary, analytical disposition | Generalizable semantics are separated from D077/Agent-Governance-specific policy and candidate disposition is explicit | MEDIUM | SINGLE_EXECUTION |
| R029-S6 | NOT_STARTED | `research-evidence-traceability` candidate | S1-S3 accepted | Generic capability vs Agent Governance adapter map and disposition | Reusable research/decision provenance semantics are separated from `Rxxx`/`Dxxx` repository conventions | MEDIUM | SINGLE_EXECUTION |
| R029-S7 | NOT_STARTED | `durable-work-checkpoint` candidate | S1-S3 accepted | Generic cold-start/frontier capability vs Agent Governance checkpoint adapter map and disposition | Generic durable-resume semantics are separated from D027/D067/checkpoint-specific rules | MEDIUM | SINGLE_EXECUTION |
| R029-S8 | NOT_STARTED | `executor-launch-handoff` candidate | S1-S3 accepted | Generic launch/handoff capability vs Agent Governance Task Contract/D055 adapter map and disposition | Reusable transport/session/handoff behavior is separated from repository-specific authority and acceptance semantics | MEDIUM | SINGLE_EXECUTION |
| R029-S9 | NOT_STARTED | Workspace-isolation placement | S4 and S8 accepted | Placement analysis and explicit disposition | Workspace isolation is classified as a sub-route/reference or a standalone transverse candidate based on distinct intent/trigger evidence | MEDIUM | SINGLE_EXECUTION |
| R029-S10 | NOT_STARTED | Candidate-topology synthesis and evaluation plan | S1-S9 accepted | One bounded candidate topology plus pre-decision evaluation plan | Candidate skill/root topology, preservation coverage, trigger-eval plan, context-efficiency plan, functional-equivalence plan, cross-host checks and deterministic checks are coherent; no adoption occurs | HIGH | SINGLE_EXECUTION |

## Subtask details

### R029-S1 — Root preservation-map audit

Audit the current `develop` root `AGENTS.md` against R029's semantic inventory. Confirm that every material current rule is represented exactly once in a preservation map as:

- always-on root invariant;
- root trigger plus Agent-Governance domain route;
- root trigger plus transverse candidate;
- domain route;
- reference/deterministic mechanism.

Out of scope: designing the lean root, deciding Skill topology, writing or changing `AGENTS.md`, creating Skills, or provider/model evaluation.

Required durable output: a persisted S1 result containing the complete preservation map, duplicate/ambiguous classifications, and any uncovered current root semantics.

Completion gate: no material root semantic unit remains unclassified. Any disagreement is recorded as an explicit gap rather than silently resolved.

S1 completed on 2026-09-13 and is persisted at `docs/orchestrator/R029-S1-ROOT-PRESERVATION-MAP.md`. The audit refined the coarse R029 inventory into 79 atomic semantic units with zero unclassified units, zero delete-without-replacement units, and zero preservation-classification ambiguities. Two later topology questions remain explicitly deferred rather than silently decided. S1 now awaits Human review/acceptance; S2 is not selected automatically.

### R029-S2 — Lean-root responsibility contract

Define only the responsibility boundary of the future always-loaded root. Do not draft the final root file and do not design individual transverse Skills.

### R029-S3 — Maintainer Skill domain boundary

Define what remains specific to maintaining the Agent Governance source product and therefore belongs in the existing Maintainer Skill or its on-demand references. Preserve the approved single top-level Maintainer Skill with internal Orchestrator/Executor routes.

### R029-S4 — `repository-change-control`

Evaluate reusable semantic intent, positive and negative triggers, output/postcondition contract, authority boundaries, and ChatGPT/Codex host-adapter differences. Analytical disposition only.

### R029-S5 — `upstream-version-revalidation`

Evaluate whether D077's reusable engineering pattern warrants a transverse capability. Separate universal revalidation semantics from Agent Governance decision vocabulary and repository policy.

### R029-S6 — `research-evidence-traceability`

Evaluate reusable evidence/provenance semantics separately from Agent Governance's `Rxxx`, `Dxxx`, registry, and checkpoint conventions.

### R029-S7 — `durable-work-checkpoint`

Evaluate the reusable cold-start/durable-frontier pattern separately from the exact Agent Governance D027/D067 checkpoint schema and lifecycle.

### R029-S8 — `executor-launch-handoff`

Evaluate reusable launch/session/transport/handoff behavior separately from D055 model/effort policy, Task Contract authority, ownership, and acceptance semantics.

### R029-S9 — Workspace-isolation placement

Determine whether workspace isolation has a genuinely separate user intent and trigger boundary or should remain a route/reference inside `repository-change-control` and/or `executor-launch-handoff`.

### R029-S10 — Candidate topology synthesis and evaluation plan

Consume only accepted durable S1-S9 outputs. Produce one coherent pre-decision candidate architecture and the smallest evaluation plan required before any normative adoption.

At minimum cover preserved behavior, routing positives/negatives/near-misses/collisions, wrong-authority activation, context loading, functional equivalence, ChatGPT/Codex cross-host behavior, deterministic checks, and D077 refresh requirements.

S10 does not authorize running provider/model evals, writing a Decision Record, refactoring `AGENTS.md`, or implementing Skills.

## Session and Human gates

After every subtask:

```text
subtask complete
-> persist result and checkpoint
-> stop material work for that session
-> Human Owner reviews/selects next subtask
-> later session resumes this same chat
-> revalidate current develop/checkpoint
-> execute only the selected subtask
```

A later subtask is never implied merely because its prerequisite becomes complete.

After R029-S10, stop at a Human decision gate. Any normative architecture Decision Record, empirical provider/model qualification, root `AGENTS.md` refactor, Skill package creation, or implementation must be separately selected and authorized.

## Global prohibitions

Until separately authorized:

- do not change current role, stage, Markdown, oracle, or execution-mechanics ownership;
- do not rewrite root `AGENTS.md`;
- do not create/package/install/release transverse Skills;
- do not split the Maintainer Skill by ChatGPT/Codex role;
- do not launch Codex/another Executor;
- do not consume provider/model calls or create scored observations;
- do not promote R029 from research/evaluation into normative policy;
- do not start the next subtask automatically;
- do not mutate the unselected T066 scientific branch.
