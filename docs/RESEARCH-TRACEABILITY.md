# Research Traceability Registry

Status: CURRENT  
Owner: ChatGPT Orchestrator  
Controlling decision: `docs/decisions/D057-research-decision-traceability.md`  
Last-Registry-Review: 2026-09-05

## Purpose

This is the canonical ledger for material Agent Governance research. It separates **research completion** from **decision adoption** so a later chat can reconstruct what was learned, what was evaluated, and what actually became normative without relying on prior conversation memory.

Research artifacts remain evidence/analysis until a controlling decision or other explicit normative artifact adopts their conclusions.

## State model

`Research-State`:

- `ACTIVE`
- `COMPLETE`
- `SUPERSEDED`

`Decision-State`:

- `NOT_REQUIRED`
- `EVALUATING`
- `DECIDED`
- `DEFERRED`
- `REJECTED`
- `SUPERSEDED`

See D057 for transition semantics and required metadata for new research.

## Registry

| ID | Research artifact | Research-State | Decision-State | Evaluation / outcome refs | Decision ref | Current disposition |
| --- | --- | --- | --- | --- | --- | --- |
| R001 | `docs/research/MG1-EVAL-EFFICIENCY-RESEARCH.md` | COMPLETE | SUPERSEDED | T023/MG1 v6 method lineage; later v6-v12 research/reviews | none | The fixed-v5 cost question produced a v6 method, but that evaluation method was later replaced through successive MG1 iterations. Findings remain historical evidence. |
| R002 | `docs/research/MG1-V6-CONFOUND-ANALYSIS.md` | COMPLETE | SUPERSEDED | `docs/reviews/T023-R5.md`; T046/MG1-v7 lineage | none | Confounds were incorporated prospectively into the successor method; later MG1 methods supersede the operational disposition, not the historical findings. |
| R003 | `docs/research/MG1-V7-COST-AND-HOST-EXECUTION-ANALYSIS.md` | COMPLETE | SUPERSEDED | T023 successor-method lineage through later MG1 versions | none | Cost/host-execution findings informed subsequent MG1 method revisions; the specific v7 execution path is no longer current. |
| R004 | `docs/research/MG1-V8-WINDOWS-SANDBOX-ROOT-CAUSE.md` | COMPLETE | SUPERSEDED | `docs/reviews/T023-R7.md`; successor MG1 host-preflight work | none | Root-cause analysis informed later host/workspace corrections; v8 restart authority is no longer current. |
| R005 | `docs/research/MG1-V9-WINDOWS-TEMP-ACL-ANALYSIS.md` | COMPLETE | SUPERSEDED | T023 successor-method lineage; current terminal MG1 state `docs/reviews/T023-R11.md` | none | ACL findings remain diagnostic evidence; the v9-specific remediation path has been superseded by later MG1 iterations. |
| R006 | `docs/research/CODEX-PERSISTENT-EXECUTOR-COORDINATOR-RESEARCH.md` | COMPLETE | SUPERSEDED | `docs/tasks/T053-codex-persistent-executor-coordinator-pilot.md`; `docs/reviews/T053-R1.md`; R013 | `docs/decisions/D060-task-scoped-executor-coordinator-continuity.md` | T053's positive same-task continuity/context-locality evidence remains valid, but R006's broader cross-Task-Contract dossier-root recommendation is superseded. D060 adopts a narrower boundary: one Human-visible coordinator root per exact Task/Operational Contract, retired when that work unit closes. |
| R007 | `docs/research/ADAPTIVE-SUBAGENT-COMPUTE-ROUTING-RESEARCH.md` | COMPLETE | DEFERRED | `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md`; `docs/reviews/T054-R1.md`; PR `#277` | none | T054 execution was accepted with pilot decision `NOT_QUALIFIED`: P1 exposed a real `Luna / Low` exactness failure, P2 had a shared task/oracle-semantics confound across both arms, and P3 passed in both arms. No global child-routing policy is adopted. Reconsider only after a successor evaluation removes the P2 confound, uses a first-attempt-qualified mapping, and the measurement substrate is qualified. |
| R008 | `docs/research/CODEX-CHILD-OBSERVABILITY-SURFACE-RESEARCH.md` | COMPLETE | DEFERRED | `docs/tasks/T055-codex-child-observability-qualification.md`; `docs/reviews/T055-R1.md`; PR `#280`; successor R009/T056/T057 | none | T055 execution was accepted with `PARTIAL_OBSERVABILITY`. Model/reasoning, exact child/turn usage and duration were observable, but 0.149.0 did not prove an unambiguous non-write child profile. R009 found a materially stronger 0.153.4+ surface. T056 confirmed the parent `:read-only` profile-ID path but its controller terminated before child reattachment. R008 remains deferred pending T057. |
| R009 | `docs/research/CODEX-CHILD-SANDBOX-INHERITANCE-RESEARCH.md` | COMPLETE | EVALUATING | `docs/tasks/T056-codex-read-only-child-requalification.md`; `docs/reviews/T056-R1.md`; `docs/tasks/T057-codex-read-only-child-requalification-v2.md`; evidence PR `#284` | none | Official source supports parent-derived child permission inheritance and the 0.153.4 parent-owned reload fix. T056 accepted as execution with `PARTIAL_OBSERVABILITY`: version/capability gates, parent `:read-only` receipt, real-child correlation, and requested/resolved `Terra / Low` passed, but a controller misparse of `thread/loaded/list` terminated App Server before child reattachment. R009 remains EVALUATING under T057, which corrects only that harness defect and preserves all material controls. |
| R010 | `docs/research/GPT6-ASTRA-EXECUTOR-LAUNCH-PROFILE-RESEARCH.md` | COMPLETE | DEFERRED | no empirical project evaluation yet | none | GPT-6 Astra is an official quality-first flagship and current Codex source supports it, but availability alone does not justify globally replacing Sol under D055. T056/T057 remain `GPT-5.6 Sol / Medium` to avoid a model-family confound. Global/default Astra adoption is deferred pending task-level or comparative evidence and host/account availability. |
| R011 | `docs/research/CODEX-COORDINATOR-IDENTITY-WORKTREE-HYGIENE-RESEARCH.md` | COMPLETE | DECIDED | current source-maintenance workflow; T056/T057 local-execution lineage | `docs/decisions/D058-executor-coordinator-session-and-worktree-hygiene.md` | Codex supports explicit Human-visible thread naming, while existing branch cleanup did not fully require obsolete-worktree retirement plus primary-checkout convergence. D058 adopts deterministic coordinator chat names, exclusive writable worktrees for concurrent work units, fail-closed local-state classification, post-integration worktree retirement, and a clean/current primary checkout baseline. |
| R012 | `docs/research/CODEX-COORDINATOR-DELEGATION-POLICY-RESEARCH.md` | COMPLETE | DEFERRED | R006; T053; `docs/reviews/T053-R1.md`; R007; current Codex 0.153.4 + official OpenAI multi-agent guidance | none | Pure optional delegation is insufficient if the Human-visible Executor root is intended to act as a real coordinator: current Codex may require an explicit user/`AGENTS.md`/Skill delegation request. Exact global worker choreography is too prescriptive. Recommended direction is a semantic delegation obligation (Agent Governance defines when/bounds; Executor chooses concrete decomposition/worker mechanics). Normative adoption is deferred until T057 converges so no active Task Contract is changed mid-run. |
| R013 | `docs/research/CODEX-TASK-SCOPED-COORDINATOR-CONTINUITY-RESEARCH.md` | COMPLETE | DECIDED | R006; T053; `docs/reviews/T053-R1.md`; R012; current OpenAI long-running/compaction guidance | `docs/decisions/D060-task-scoped-executor-coordinator-continuity.md` | Adopt one Human-visible Executor Coordinator Root per exact Task/Operational Contract. `NEW` at work-unit start, `CONTINUE` through normal same-task phases/rework, retire at closure, and start a new root for the next work unit. `root-2+` is failover only. Root context stays compact through durable Git pointers, concise summaries and supported compaction/fresh child contexts rather than cross-task root reuse. |
| R014 | `docs/research/CHATGPT-GIT-WORKSPACE-AND-GITHUB-TRANSPORT-RESEARCH.md` | COMPLETE | NOT_REQUIRED | workspace/GitHub experiment at `develop` `20ed0e64dd6c98f38be42cd3cc28fcc220d06c5e`; `ManuelBouza/test_biblioteca` round-trip commits `d82750a45f43f45a16c498674391a7a7e15dc319`, `af02345fcfed0ebe7d4b6503af7e89cdf48b84cf`; capability-matrix commits `5d04c16e5705e308457072792e4f3c5204768864`, `dafe8a821e09a09a6200e4c5afed447fcf03320e`; cross-chat Library snapshot round trip; official OpenAI Library storage/retention docs checked 2026-09-05 | none | ChatGPT can combine real temporary-workspace Git semantics, persistent Library working-file/version storage, packaged full-repository snapshots including `.git`, cross-chat Git-history continuation, and explicit GitHub connector transport. Multi-file reconstruction in one remote commit and stale-base rejection via HTTP 409 were verified; connector reconstruction did not preserve the equivalent local commit SHA automatically. Library is persistent storage, not a native Git working tree/remote, and synchronization remains explicit. Official Plus Library limits currently document 20 GB total storage and 512 MB per uploaded file; files are documented as retained until manual deletion, with vendor facts treated as volatile. No workflow/policy adoption is implied. |

## Live research frontier

```text
R009 — Codex child sandbox inheritance / receipt
  Research-State: COMPLETE
  Decision-State: EVALUATING
  T056: accepted execution / PARTIAL_OBSERVABILITY
  T056 positive evidence: Codex 0.153.4; parent :read-only receipt; real child; Terra/Low resolved
  T056 blocker: temporary controller misparsed thread/loaded/list and lost parent residency before child reattachment
  Current evaluation: T057 running from its frozen Task Contract
  T057 scope: correct only loaded-thread parsing/residency and recapture exact child permission/usage/duration/reroute receipts
```

Deferred dependencies remain:

```text
R008 — child observability surface
  COMPLETE / DEFERRED
  Reopens only if T057 qualifies the read-only child receipt

R007 — adaptive subagent compute routing
  COMPLETE / DEFERRED
  Reopens only after the full measurement substrate qualifies and a separate D057 transition is persisted

R012 — coordinator delegation policy
  COMPLETE / DEFERRED
  Research conclusion: semantic delegation obligation is preferred over pure optional delegation or exact global worker choreography
  Reconsider immediately after T057 terminal convergence before the next normal non-experimental implementation task
```

Completed/decided coordinator research:

```text
R006 — persistent Executor coordinator
  COMPLETE / SUPERSEDED
  Same-task continuity evidence retained
  Cross-Task dossier-root recommendation superseded by R013/D060

R011 — coordinator identity / worktree hygiene
  COMPLETE / DECIDED -> D058

R013 — task-scoped coordinator continuity
  COMPLETE / DECIDED -> D060
  One complete Task/Operational Contract = one Human-visible root lifecycle
```

Completed research dispositions outside the live evaluation frontier:

```text
R010 — GPT-6 Astra Executor launch profile
  COMPLETE / DEFERRED
  T057 remains Sol / Medium
  No global D055 Astra migration adopted

R014 — ChatGPT Git workspace / Library / GitHub transport
  COMPLETE / NOT_REQUIRED
  Temporary-workspace Git, Library persistence, and GitHub canonical transport remain separate layers
  Full Git repository snapshots including .git were recovered across chats with Git history intact and advanced
  Multi-file one-commit transport and stale-base conflict detection were verified; Library remains storage rather than a Git remote
  Current official Library quotas/retention are recorded as volatile product facts, not governance policy
```

T057 is not a routing or normal delegation pilot. D060 does not alter T057's frozen one-child topology; T057 already uses one task-scoped root. Even a passing T057 result requires Orchestrator convergence and explicit D057 transitions before R007 may return to `EVALUATING`. R012 remains separately deferred until post-T057 convergence.

## Required workflow for new research

For each new material investigation:

1. allocate the next stable `Rxxx` identifier;
2. create the research artifact under `docs/research/` with D057 metadata;
3. add/update its registry row in the same Markdown change set;
4. record sources/evidence and distinguish volatile facts from durable analysis;
5. if empirical validation is required, set `Decision-State: EVALUATING` and link the exact Task Contract/eval/review;
6. if a decision is accepted, update the registry to `DECIDED` and link the exact `Dxxx` authority;
7. if deferred/rejected/superseded, persist that disposition and reason/reference;
8. update `docs/orchestrator/CHECKPOINT.md` only when the item is part of the live frontier.

No material research may be relied on for a downstream Task Contract or normative change while existing only in chat.

## Provenance rule

Do not rewrite a completed research artifact merely to align with a later conclusion. Preserve the original analysis, create a successor/revision when material evidence changes, and use the registry to express supersession and current disposition.

For volatile vendor/model/pricing/regulatory facts, revalidate the source before a later decision and update the research `Last-Reviewed` metadata or create a successor research item.