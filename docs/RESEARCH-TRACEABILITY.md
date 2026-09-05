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
| R007 | `docs/research/ADAPTIVE-SUBAGENT-COMPUTE-ROUTING-RESEARCH.md` | COMPLETE | DEFERRED | `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md`; `docs/reviews/T054-R1.md`; PR `#277` | none | T054 execution was accepted with pilot decision `NOT_QUALIFIED`: P1 exposed a real `Luna / Low` exactness failure, P2 had a shared task/oracle-semantics confound across both arms, and P3 passed in both arms. Effective child profiles and attributable token usage were not observable. No global child-routing policy is adopted. Reconsider only after a successor evaluation removes the P2 confound, uses a first-attempt-qualified mapping, and preferably runs on a surface with effective-profile/usage receipts. |
| R008 | `docs/research/CODEX-CHILD-OBSERVABILITY-SURFACE-RESEARCH.md` | COMPLETE | EVALUATING | `docs/tasks/T055-codex-child-observability-qualification.md` | none | Current Codex 0.153.4 App Server / stable Python SDK provide a materially stronger measurement surface than T054's direct parent-facing tool return: child thread relation/config records, sandbox responses, and thread/turn-attributable token usage are documented. Configured thread model/reasoning are not per-turn provider execution receipts. T055 must qualify the actual installed host before this substrate may support any corrected routing evaluation. R007 remains DEFERRED meanwhile. |

## Live research frontier

The only current `EVALUATING` research item is R008:

```text
R008 — Codex child observability surface
  Research-State: COMPLETE
  Decision-State: EVALUATING
  Evaluation: T055 planned
  Question: can the actual installed host correlate a real child to resolved thread profile, sandbox, attributable token usage and duration through supported App Server/SDK surfaces?
  Global routing decision: none
```

The two routing/persistence research lines remain consciously deferred:

```text
R006 — persistent Executor coordinator
  Research-State: COMPLETE
  Decision-State: DEFERRED
  Evidence: T053 accepted; T054 adds no persistence-causal evidence
  Global policy decision: none
  Reconsideration condition: better persistence observability or separate normative justification

R007 — adaptive subagent compute routing
  Research-State: COMPLETE
  Decision-State: DEFERRED
  Evaluation: T054 accepted; pilot decision NOT_QUALIFIED
  Global policy decision: none
  Reconsideration condition: corrected successor evaluation + first-attempt-qualified mapping after the measurement substrate is qualified
```

R008 does not automatically reactivate R007. R007 can return to `EVALUATING` only through a later persisted transition after T055 demonstrates adequate measurement capability and a corrected routing Task Contract is separately specified.

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
