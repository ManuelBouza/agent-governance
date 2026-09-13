# R029 Incremental Session Sequence

Status: ACTIVE  
Parent-Research: `docs/research/R029-AGENTS-SKILL-ARCHITECTURE-REFACTOR-RESEARCH.md`  
Authority: Human Owner clarified incremental same-chat execution on 2026-09-13  
Lifecycle: one persistent R029 ChatGPT Orchestrator objective with bounded session subtasks  
Decision-State: EVALUATING

## Execution rule

R029 remains one Human objective in this ChatGPT chat. Only one material subtask is executed per work session. Each subtask must be persisted and return to a Human review gate before its successor is selected. No automatic progression is authorized.

The sequence does not authorize a root `AGENTS.md` rewrite, Skill implementation, normative decision, Executor/Codex launch, provider/model evaluation, or T066 work.

```text
R029-S1 -> Human gate -> R029-S2 -> Human gate -> ... -> R029-S10
         -> HUMAN DECISION GATE
```

## Subtask registry

| ID | Status | Subtask | Prerequisites | Durable output | Completion gate | ChatGPT Effort | Execution Shape |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R029-S1 | ACCEPTED | Root preservation-map audit | R029 integrated | `docs/orchestrator/R029-S1-ROOT-PRESERVATION-MAP.md` | Every current root semantic unit has exactly one preservation classification/destination | MEDIUM | SINGLE_EXECUTION |
| R029-S2 | ACCEPTED | Lean-root responsibility contract | S1 accepted | `docs/orchestrator/R029-S2-LEAN-ROOT-RESPONSIBILITY-CONTRACT.md` | Every retained root responsibility is pre-routing justified and omitted detail remains explicitly reachable | MEDIUM | SINGLE_EXECUTION |
| R029-S3 | ACCEPTED | Maintainer Skill domain boundary | S1-S2 accepted | `docs/orchestrator/R029-S3-MAINTAINER-DOMAIN-BOUNDARY.md` | Source-maintenance-specific workflows are separated from transverse candidate seams without splitting the approved Maintainer Skill by role | MEDIUM | SINGLE_EXECUTION |
| R029-S4 | ACCEPTED | `repository-change-control` candidate | S1-S3 accepted | `docs/orchestrator/R029-S4-REPOSITORY-CHANGE-CONTROL-CANDIDATE.md` | Reusable intent and non-overlap are explicit; disposition is `KEEP_CANDIDATE` | MEDIUM | SINGLE_EXECUTION |
| R029-S5 | ACCEPTED | `upstream-version-revalidation` candidate | S1-S3 accepted | `docs/orchestrator/R029-S5-UPSTREAM-VERSION-REVALIDATION-CANDIDATE.md` | Generalizable semantics separated from D077/Agent-Governance policy; disposition is `KEEP_CANDIDATE` | MEDIUM | SINGLE_EXECUTION |
| R029-S6 | ACCEPTED | `research-evidence-traceability` candidate | S1-S3 accepted | `docs/orchestrator/R029-S6-RESEARCH-EVIDENCE-TRACEABILITY-CANDIDATE.md` | Reusable provenance semantics separated from `Rxxx`/`Dxxx` conventions; disposition is `KEEP_CANDIDATE` | MEDIUM | SINGLE_EXECUTION |
| R029-S7 | ACCEPTED | `durable-work-checkpoint` candidate | S1-S3 accepted | `docs/orchestrator/R029-S7-DURABLE-WORK-CHECKPOINT-CANDIDATE.md` | Generic durable-resume semantics separated from D027/D067/checkpoint rules; disposition is `KEEP_CANDIDATE` | MEDIUM | SINGLE_EXECUTION |
| R029-S8 | ACCEPTED | `executor-launch-handoff` candidate | S1-S3 accepted | `docs/orchestrator/R029-S8-EXECUTOR-LAUNCH-HANDOFF-CANDIDATE.md` | Reusable transport/session/handoff separated from repository-specific authority; disposition is `KEEP_CANDIDATE` | MEDIUM | SINGLE_EXECUTION |
| R029-S9 | ACCEPTED | Workspace-isolation placement | S4 and S8 accepted | `docs/orchestrator/R029-S9-WORKSPACE-ISOLATION-PLACEMENT.md` | Workspace isolation classified with explicit parent/dependency and anti-sprawl rationale; disposition is `INTERNAL_ROUTE` | MEDIUM | SINGLE_EXECUTION |
| R029-S10 | NOT_STARTED | Candidate-topology synthesis and evaluation plan | S1-S9 accepted | One bounded candidate topology plus pre-decision evaluation plan | Topology/evaluation plan coherent; no adoption occurs | HIGH | SINGLE_EXECUTION |

## Completed subtasks

### R029-S1 — Root preservation-map audit
Accepted 2026-09-13. Durable output: `docs/orchestrator/R029-S1-ROOT-PRESERVATION-MAP.md`.

### R029-S2 — Lean-root responsibility contract
Accepted 2026-09-13. Durable output: `docs/orchestrator/R029-S2-LEAN-ROOT-RESPONSIBILITY-CONTRACT.md`.

### R029-S3 — Maintainer Skill domain boundary
Accepted 2026-09-13. Durable output: `docs/orchestrator/R029-S3-MAINTAINER-DOMAIN-BOUNDARY.md`.

### R029-S4 — `repository-change-control` candidate
Accepted 2026-09-13. Durable output: `docs/orchestrator/R029-S4-REPOSITORY-CHANGE-CONTROL-CANDIDATE.md`. Disposition: `KEEP_CANDIDATE`.

### R029-S5 — `upstream-version-revalidation` candidate
Accepted 2026-09-13. Durable output: `docs/orchestrator/R029-S5-UPSTREAM-VERSION-REVALIDATION-CANDIDATE.md`. Disposition: `KEEP_CANDIDATE`.

### R029-S6 — `research-evidence-traceability` candidate
Accepted 2026-09-13. Durable output: `docs/orchestrator/R029-S6-RESEARCH-EVIDENCE-TRACEABILITY-CANDIDATE.md`. Disposition: `KEEP_CANDIDATE`.

### R029-S7 — `durable-work-checkpoint` candidate
Accepted 2026-09-13. Durable output: `docs/orchestrator/R029-S7-DURABLE-WORK-CHECKPOINT-CANDIDATE.md`. Disposition: `KEEP_CANDIDATE`.

### R029-S8 — `executor-launch-handoff` candidate
Accepted 2026-09-13. Durable output: `docs/orchestrator/R029-S8-EXECUTOR-LAUNCH-HANDOFF-CANDIDATE.md`. Disposition: `KEEP_CANDIDATE`.

### R029-S9 — Workspace-isolation placement
Accepted 2026-09-13. Durable output: `docs/orchestrator/R029-S9-WORKSPACE-ISOLATION-PLACEMENT.md`.

S9 classifies workspace isolation as `INTERNAL_ROUTE` under `executor-launch-handoff`, with `repository-change-control`/repository-local policy as the dependency for branch/base/integration/retirement semantics. Workspace isolation is reusable but normally subordinate to delegated writable-execution attribution and continuation safety, so a standalone top-level Skill would add routing/context overhead without a sufficiently distinct independent intent.

## Remaining subtask intent

- S10 synthesizes accepted results and the pre-decision evaluation plan.

## Session and Human gates

```text
subtask complete
-> persist result and checkpoint
-> stop material work for that session
-> Human Owner reviews/selects next subtask
-> later session resumes this same chat
-> revalidate current develop/checkpoint
-> execute only the selected subtask
```

After R029-S10, stop at a Human decision gate. Any normative architecture Decision Record, provider/model qualification, root refactor, Skill creation, or implementation requires separate authorization.

## Global prohibitions

Until separately authorized: do not change role/stage/Markdown/oracle/execution-mechanics ownership; do not rewrite root `AGENTS.md`; do not create/package/install/release transverse Skills; do not split the Maintainer Skill by role; do not launch an Executor; do not consume provider/model calls; do not promote R029 into normative policy; do not start the next subtask automatically; do not mutate the unselected T066 scientific branch.
