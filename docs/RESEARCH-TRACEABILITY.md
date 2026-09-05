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
| R006 | `docs/research/CODEX-PERSISTENT-EXECUTOR-COORDINATOR-RESEARCH.md` | COMPLETE | DEFERRED | `docs/tasks/T053-codex-persistent-executor-coordinator-pilot.md`; `docs/reviews/T053-R1.md`; `docs/reviews/T054-R1.md` | none | T053 produced positive qualitative persistence/context-locality evidence, but no attributable token/context metrics. T054 did not add causal persistence evidence. No global D055 persistence-policy change is adopted. Reconsider only with materially better persistence observability or a separate normative justification that does not depend on an unverified efficiency claim. |
| R007 | `docs/research/ADAPTIVE-SUBAGENT-COMPUTE-ROUTING-RESEARCH.md` | COMPLETE | DEFERRED | `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md`; `docs/reviews/T054-R1.md`; PR `#277` | none | T054 execution was accepted with pilot decision `NOT_QUALIFIED`: P1 exposed a real `Luna / Low` exactness failure, P2 had a shared task/oracle-semantics confound across both arms, and P3 passed in both arms. No global child-routing policy is adopted. Reconsider only after a successor evaluation removes the P2 confound, uses a first-attempt-qualified mapping, and the measurement substrate is qualified. |
| R008 | `docs/research/CODEX-CHILD-OBSERVABILITY-SURFACE-RESEARCH.md` | COMPLETE | DEFERRED | `docs/tasks/T055-codex-child-observability-qualification.md`; `docs/reviews/T055-R1.md`; PR `#280`; successor R009/T056 | none | T055 execution was accepted with `PARTIAL_OBSERVABILITY`. Model/reasoning, exact child/turn usage and duration were observable, but the 0.149.0 post-run child lifecycle receipt did not prove an unambiguous non-write permission profile. R009 found a material post-0.149 parent-owned child reload fix and a stronger profile-ID receipt path. R008 remains deferred until T056 qualifies that surface. |
| R009 | `docs/research/CODEX-CHILD-SANDBOX-INHERITANCE-RESEARCH.md` | COMPLETE | EVALUATING | `docs/tasks/T056-codex-read-only-child-requalification.md` | none | Official source shows spawned children inherit the parent permission snapshot; profile-ID selection `:read-only` plus `activePermissionProfile` is the preferred provenance path; and commit `d21794d6` / PR #40477 (2026-08-24), included in Codex 0.153.4, fixed parent-owned V2 child reload so unloaded children reattach through the actual parent and inherit its execution policy. T056 is a new version-gated requalification. The last observed installed host was 0.149.0, so execution must not start until the installed host naturally/explicitly reaches a qualifying version outside the Executor task. |
| R010 | `docs/research/GPT6-ASTRA-EXECUTOR-LAUNCH-PROFILE-RESEARCH.md` | COMPLETE | DEFERRED | no empirical project evaluation yet | none | GPT-6 Astra is an official quality-first flagship and current Codex source supports it, but availability alone does not justify changing the frozen T056 root or globally replacing Sol under D055. T056 remains `GPT-5.6 Sol / Medium` to avoid adding a model-family confound. Global/default Astra adoption is deferred pending task-level or comparative evidence and host/account availability. |

## Live research frontier

```text
R009 — Codex child sandbox inheritance / receipt
  Research-State: COMPLETE
  Decision-State: EVALUATING
  Evaluation: T056 planned
  Current gate: installed Codex/App Server must be >= 0.153.4 and preserve the native required schema
  Last observed host: 0.149.0 during T055; reconfirmed by Human on 2026-09-05 after the desktop app update
  Executor may not globally upgrade Codex to satisfy the gate
```

Deferred dependencies remain:

```text
R008 — child observability surface
  COMPLETE / DEFERRED
  Reopens only if T056 qualifies the read-only child receipt on the corrected surface

R007 — adaptive subagent compute routing
  COMPLETE / DEFERRED
  Reopens only after the full measurement substrate qualifies and a separate D057 transition is persisted

R006 — persistent Executor coordinator
  COMPLETE / DEFERRED
  No global D055 persistence-session policy change
```

Completed vendor/model research not adopted as policy:

```text
R010 — GPT-6 Astra Executor launch profile
  COMPLETE / DEFERRED
  T056 remains Sol / Medium
  No global D055 Astra migration adopted
```

T056 is not a routing pilot. Even a passing T056 result requires Orchestrator convergence and explicit D057 transitions before R007 may return to `EVALUATING`.

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

Do not rewrite a completed research artifact merely to align it with a later conclusion. Preserve the original analysis, create a successor/revision when material evidence changes, and use the registry to express supersession and current disposition.

For volatile vendor/model/pricing/regulatory facts, revalidate the source before a later decision and update the research `Last-Reviewed` metadata or create a successor research item.