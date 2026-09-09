# Research Traceability Registry

Status: CURRENT  
Owner: ChatGPT Orchestrator  
Controlling decision: `docs/decisions/D057-research-decision-traceability.md`  
Last-Registry-Review: 2026-09-09

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
| R005 | `docs/research/MG1-V9-WINDOWS-TEMP-ACL-ANALYSIS.md` | COMPLETE | SUPERSEDED | T023 successor-method lineage; later MG1 reviews | none | ACL findings remain diagnostic evidence; the v9-specific remediation path has been superseded by later MG1 iterations. |
| R006 | `docs/research/CODEX-PERSISTENT-EXECUTOR-COORDINATOR-RESEARCH.md` | COMPLETE | SUPERSEDED | `docs/tasks/T053-codex-persistent-executor-coordinator-pilot.md`; `docs/reviews/T053-R1.md`; R013 | `docs/decisions/D060-task-scoped-executor-coordinator-continuity.md` | T053's positive same-task continuity/context-locality evidence remains valid, but R006's broader cross-Task-Contract dossier-root recommendation is superseded. D060 adopts one Human-visible coordinator root per exact Task/Operational Contract. |
| R007 | `docs/research/ADAPTIVE-SUBAGENT-COMPUTE-ROUTING-RESEARCH.md` | COMPLETE | EVALUATING | `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md`; `docs/reviews/T054-R1.md`; D063; `docs/tasks/T063-adaptive-worker-routing-requalification.md` | none | T054 was accepted but `NOT_QUALIFIED`: P1 exposed a real Luna/Low exactness failure, P2 had a shared task/oracle confound, and P3 passed. D063 later qualified the read-only child measurement substrate. T063 is now the explicitly specified corrected successor evaluation: P1 uses a less aggressive first-attempt economy mapping and unambiguous Git evidence, P2 statically defines AST dependency semantics, and all scored children require D063 receipts. No global adaptive worker-routing policy is adopted unless T063 later converges with sufficient evidence and receives a separate D057 decision transition. |
| R008 | `docs/research/CODEX-CHILD-OBSERVABILITY-SURFACE-RESEARCH.md` | COMPLETE | DECIDED | T055/T056/T057; `docs/reviews/T057-R1.md`; evidence PRs `#280`, `#284`, `#296` | `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md` | T057 qualified the exact-child read-only/identity/usage/duration/reroute measurement surface. D063 adopts that bounded, version-sensitive substrate while preserving the backend-served identity boundary. |
| R009 | `docs/research/CODEX-CHILD-SANDBOX-INHERITANCE-RESEARCH.md` | COMPLETE | DECIDED | T056/T057; `docs/reviews/T057-R1.md`; evidence PRs `#284`, `#296` | `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md` | T057 empirically closed the exact-child `:read-only` provenance and continuous-parent-residency gate. D063 adopts the qualified surface subject to native version/capability revalidation. |
| R010 | `docs/research/GPT6-ASTRA-EXECUTOR-LAUNCH-PROFILE-RESEARCH.md` | COMPLETE | DEFERRED | no empirical project evaluation yet | none | GPT-6 Astra is an official quality-first flagship and current Codex source supports it, but availability alone does not justify globally replacing Sol under D055. Global/default adoption remains deferred pending task-level/comparative evidence and host/account availability. |
| R011 | `docs/research/CODEX-COORDINATOR-IDENTITY-WORKTREE-HYGIENE-RESEARCH.md` | COMPLETE | DECIDED | current source-maintenance workflow; T056/T057 lineage | `docs/decisions/D058-executor-coordinator-session-and-worktree-hygiene.md` | D058 adopts deterministic coordinator chat names, exclusive writable worktrees, fail-closed local-state classification and post-integration worktree retirement/primary-checkout convergence. |
| R012 | `docs/research/CODEX-COORDINATOR-DELEGATION-POLICY-RESEARCH.md` | COMPLETE | DECIDED | R006; T053; R007; T057; official OpenAI multi-agent guidance | `docs/decisions/D065-semantic-executor-delegation-obligation.md` | D065 adopts the semantic delegation obligation: Agent Governance defines material triggers/anti-triggers plus safety/evidence bounds, while the Executor coordinator retains concrete decomposition, child count/roles, sequencing/parallelism and mechanics. D075 later makes the pre-worker direct-execution gate explicit without replacing D065. |
| R013 | `docs/research/CODEX-TASK-SCOPED-COORDINATOR-CONTINUITY-RESEARCH.md` | COMPLETE | DECIDED | R006; T053; R012; current OpenAI long-running/compaction guidance | `docs/decisions/D060-task-scoped-executor-coordinator-continuity.md` | Adopt one Human-visible Executor Coordinator Root per exact Task/Operational Contract: NEW at work-unit start, CONTINUE through clean same-task phases/rework, retire at closure, root-2+ failover only. |
| R014 | `docs/research/CHATGPT-GIT-WORKSPACE-AND-GITHUB-TRANSPORT-RESEARCH.md` | COMPLETE | DECIDED | workspace/GitHub experiments; test_biblioteca qualification; source research PR `#291`; T058 path | `docs/decisions/D066-chatgpt-portable-git-workspace-transport.md` | D066 adopts the qualified local-Git + Library snapshot + explicit GitHub transport/lifecycle subset for ChatGPT Orchestrator source maintenance. Unqualified recovery/GC/ruleset gaps remain explicit. |
| R015 | `docs/research/CHATGPT-LIBRARY-WORKTREE-SIMULATOR-RESEARCH.md` | COMPLETE | DECIDED | R014; D058; test_biblioteca isolation/lifecycle/race qualification; PR `#291`; T058 path | `docs/decisions/D066-chatgpt-portable-git-workspace-transport.md` | D066 adopts the qualified portable workspace isolation subset using unique topic branch + coordination-only lock branch + expected-HEAD CAS + owner sentinel + standalone Library Git snapshot; unresolved recovery/transfer/automatic-retirement gaps remain explicit. |
| R016 | `docs/research/R016-MG1-V12-REFERENCE-FAMILY-REENTRY.md` | COMPLETE | EVALUATING | T061 successor lineage; D074/T062 v15 RIQ-NBC; T023-R30/R31/R32/R33 | none | The original reference-family re-entry has evolved into T062 RIQ-NBC. T062 Stage 5 is complete, the first Stage 6 attempt blocked before provider process creation with zero provider/model calls, R32 continuation authority exists but is unconsumed, and T023-R33 places the scientific line in Human Hold. No topology is selected; the research/evaluation disposition remains open. |
| R017 | `docs/research/R017-COORDINATOR-DIRECT-EXECUTION-GATE.md` | COMPLETE | DECIDED | R012/D065; R007/T054/T054-R1; D063; official OpenAI Subagents/model guidance revalidated 2026-09-09 | `docs/decisions/D075-coordinator-direct-execution-gate.md` | D075 makes the first routing gate explicit: low-elaboration auxiliary microactions may remain coordinator-direct when delegation overhead dominates, while materially elaborated isolatable units remain subject to D065 mandatory delegation. It adds a microaction-chaining anti-evasion rule and explicitly keeps adaptive child model/effort routing as separate R007/T063 evidence-gated Stage-B policy. |

## Live research frontier

### T063 — adaptive worker routing requalification

```text
R017 — coordinator direct-execution gate
  COMPLETE / DECIDED -> D075
  Stage A fixed: COORDINATOR_DIRECT | DELEGATED | CONTRACT_FIXED

R007 — adaptive subagent compute routing
  COMPLETE / EVALUATING
  T054: accepted execution / NOT_QUALIFIED
  D063: measurement substrate qualified
  T063: corrected successor evaluation fully specified
  Stage B remains experimental: delegated worker role/model/reasoning/context
  Executor launch: NOT_AUTHORIZED pending separate Human launch
```

T063 deliberately does not vary the D075 Stage-A delegation-worthiness decision. Its probes are already delegated material units; only the child execution profile is the experimental variable.

### Held T023/T062 scientific frontier

```text
T062 / T023 v15 RIQ-NBC
  Stage 5: complete
  blocked Stage 6 evidence HEAD: b9034e450f04fbc9736543425e531159d4b79d49
  provider/model calls: 0
  R32 provider continuation authority: valid but unconsumed
  T023-R33: HUMAN_HOLD / CONTINUATION_NOT_LAUNCHED
  topology selected: no
```

T062 may not resume from the held state without a new explicit Human instruction followed by remote revalidation.

## Completed/decided coordinator research

```text
R006 — persistent Executor coordinator
  COMPLETE / SUPERSEDED -> R013/D060 narrower task-scoped continuity

R011 — coordinator identity / worktree hygiene
  COMPLETE / DECIDED -> D058

R012 — coordinator delegation policy
  COMPLETE / DECIDED -> D065

R013 — task-scoped coordinator continuity
  COMPLETE / DECIDED -> D060

R017 — coordinator direct-execution gate
  COMPLETE / DECIDED -> D075
```

## Deferred/qualified dependencies

```text
R008/R009 -> D063
  qualified version-sensitive exact read-only child measurement substrate

R010
  COMPLETE / DEFERRED
  no global D055 Astra migration

R014/R015 -> D066
  qualified ChatGPT Orchestrator portable Git workspace/transport subset
  explicit unresolved recovery/automatic-lifecycle gaps remain
```

D063 qualifies the child measurement substrate only. D065 establishes delegation obligation. D075 establishes only the coordinator-direct versus delegated first gate. None of them adopts adaptive child compute routing, changes D055, establishes provider-signed backend identity, or authorizes a global savings claim. R007 remains EVALUATING through T063.

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

Do not rewrite a completed research artifact merely to align with a later conclusion. Preserve the original analysis, create or reference a successor when material evidence changes, and use the registry to express supersession/current disposition.

For volatile vendor/model/pricing/regulatory facts, revalidate the source before a later decision and update `Last-Reviewed` metadata or create a successor research item.
