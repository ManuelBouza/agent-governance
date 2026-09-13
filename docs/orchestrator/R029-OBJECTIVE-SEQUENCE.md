# R029 Incremental Session Sequence

Status: COMPLETE_AWAITING_HUMAN_DECISION  
Parent-Research: `docs/research/R029-AGENTS-SKILL-ARCHITECTURE-REFACTOR-RESEARCH.md`  
Authority: Human Owner clarified incremental same-chat execution on 2026-09-13  
Lifecycle: one persistent R029 ChatGPT Orchestrator objective with bounded session subtasks  
Decision-State: EVALUATING

## Execution rule

R029 remained one Human objective in this ChatGPT chat. Only one material subtask was executed per work session. Each subtask was persisted and returned to a Human review gate before its successor was selected.

R029 does not authorize a root `AGENTS.md` rewrite, Skill implementation, normative decision, Executor/Codex launch, provider/model evaluation, or T066 work.

```text
R029-S1 -> Human gate -> R029-S2 -> Human gate -> ... -> R029-S10
         -> HUMAN DECISION GATE
```

## Subtask registry

| ID | Status | Subtask | Durable output | Disposition/result | ChatGPT Effort | Execution Shape |
| --- | --- | --- | --- | --- | --- | --- |
| R029-S1 | ACCEPTED | Root preservation-map audit | `docs/orchestrator/R029-S1-ROOT-PRESERVATION-MAP.md` | 79 semantic units preserved/classified | MEDIUM | SINGLE_EXECUTION |
| R029-S2 | ACCEPTED | Lean-root responsibility contract | `docs/orchestrator/R029-S2-LEAN-ROOT-RESPONSIBILITY-CONTRACT.md` | lean pre-routing responsibility contract | MEDIUM | SINGLE_EXECUTION |
| R029-S3 | ACCEPTED | Maintainer Skill domain boundary | `docs/orchestrator/R029-S3-MAINTAINER-DOMAIN-BOUNDARY.md` | Maintainer/domain vs transverse seams | MEDIUM | SINGLE_EXECUTION |
| R029-S4 | ACCEPTED | `repository-change-control` candidate | `docs/orchestrator/R029-S4-REPOSITORY-CHANGE-CONTROL-CANDIDATE.md` | `KEEP_CANDIDATE` | MEDIUM | SINGLE_EXECUTION |
| R029-S5 | ACCEPTED | `upstream-version-revalidation` candidate | `docs/orchestrator/R029-S5-UPSTREAM-VERSION-REVALIDATION-CANDIDATE.md` | `KEEP_CANDIDATE` | MEDIUM | SINGLE_EXECUTION |
| R029-S6 | ACCEPTED | `research-evidence-traceability` candidate | `docs/orchestrator/R029-S6-RESEARCH-EVIDENCE-TRACEABILITY-CANDIDATE.md` | `KEEP_CANDIDATE` | MEDIUM | SINGLE_EXECUTION |
| R029-S7 | ACCEPTED | `durable-work-checkpoint` candidate | `docs/orchestrator/R029-S7-DURABLE-WORK-CHECKPOINT-CANDIDATE.md` | `KEEP_CANDIDATE` | MEDIUM | SINGLE_EXECUTION |
| R029-S8 | ACCEPTED | `executor-launch-handoff` candidate | `docs/orchestrator/R029-S8-EXECUTOR-LAUNCH-HANDOFF-CANDIDATE.md` | `KEEP_CANDIDATE` | MEDIUM | SINGLE_EXECUTION |
| R029-S9 | ACCEPTED | Workspace-isolation placement | `docs/orchestrator/R029-S9-WORKSPACE-ISOLATION-PLACEMENT.md` | `INTERNAL_ROUTE` under `executor-launch-handoff` | MEDIUM | SINGLE_EXECUTION |
| R029-S10 | COMPLETE_AWAITING_HUMAN_DECISION | Candidate-topology synthesis and evaluation plan | `docs/orchestrator/R029-S10-CANDIDATE-TOPOLOGY-AND-EVALUATION-PLAN.md` | `CANDIDATE_TOPOLOGY_READY_FOR_HUMAN_DECISION` | HIGH | SINGLE_EXECUTION |

## Synthesized candidate topology

```text
Lean always-loaded AGENTS.md
│
├── Agent Governance Maintainer Skill
│   ├── Orchestrator route
│   └── Executor route
│
├── repository-change-control
├── upstream-version-revalidation
├── research-evidence-traceability
├── durable-work-checkpoint
└── executor-launch-handoff
    └── workspace-isolation [internal route/reference]
         └── consumes repository-change-control/repository-local policy as needed
```

Supporting deterministic scripts/CI/references and host adapters remain conditional implementation/reference surfaces, not authority sources.

## Human Decision Gate

R029 analytical work is complete. No successor subtask exists inside R029.

The Human Owner now decides among the non-normative options documented by S10:

- `ADOPT_FOR_DESIGN` — accept the candidate direction and separately authorize normative architecture/design work;
- `REVISE_AND_REEVALUATE` — revise one or more assumptions before adoption;
- `REJECT_TOPOLOGY` — retain the current architecture pending a different proposal.

No option is selected automatically.

## Evaluation requirement before implementation

S10 defines the required future evidence categories: semantic preservation, root pre-routing safety, Skill routing precision, authority-leakage/adversarial behavior, progressive-disclosure/context efficiency, cross-host portability, no-Skill degradation, composition/non-overlap and maintainability/change locality.

R029 itself performed no provider/model evaluation and created no scored observations.

## Global prohibitions still active

Until separately authorized: do not change role/stage/Markdown/oracle/execution-mechanics ownership; do not rewrite root `AGENTS.md`; do not create/package/install/release transverse Skills; do not split the Maintainer Skill by role; do not launch an Executor; do not consume provider/model calls; do not treat the candidate topology as accepted policy; do not mutate the unselected T066 scientific branch.