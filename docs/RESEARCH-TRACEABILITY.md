# Research Traceability Registry

Status: CURRENT  
Owner: ChatGPT Orchestrator  
Controlling decision: `docs/decisions/D057-research-decision-traceability.md`  
Last-Registry-Review: 2026-09-11

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
| R007 | `docs/research/ADAPTIVE-SUBAGENT-COMPUTE-ROUTING-RESEARCH.md` | COMPLETE | EVALUATING | `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md`; `docs/reviews/T054-R1.md`; D063; `docs/tasks/T063-adaptive-worker-routing-requalification.md`; R018; R019; R020; R021; R022; `docs/reviews/T063-R7.md` | none | T054 was accepted but `NOT_QUALIFIED`. T063 v1, v2 and v3 each blocked without a pilot decision. R022/R7 classify v3 as a same-child rollout-persistence visibility race and authorize a clean v4 run with a bounded same-child reattachment barrier while retaining the D063 measurement set and deliberate Codex `0.153.4` pin. No global adaptive worker-routing policy is adopted. |
| R008 | `docs/research/CODEX-CHILD-OBSERVABILITY-SURFACE-RESEARCH.md` | COMPLETE | DECIDED | T055/T056/T057; `docs/reviews/T057-R1.md`; evidence PRs `#280`, `#284`, `#296` | `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md` | T057 qualified the exact-child read-only/identity/usage/duration/reroute measurement surface. D063 adopts that bounded, version-sensitive substrate while preserving the backend-served identity boundary. |
| R009 | `docs/research/CODEX-CHILD-SANDBOX-INHERITANCE-RESEARCH.md` | COMPLETE | DECIDED | T056/T057; `docs/reviews/T057-R1.md`; evidence PRs `#284`, `#296` | `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md` | T057 empirically closed the exact-child `:read-only` provenance and continuous-parent-residency gate. D063 adopts the qualified surface subject to native version/capability revalidation. |
| R010 | `docs/research/GPT6-ASTRA-EXECUTOR-LAUNCH-PROFILE-RESEARCH.md` | COMPLETE | DEFERRED | no empirical project evaluation yet | none | GPT-6 Astra is an official quality-first flagship and current Codex source supports it, but availability alone does not justify globally replacing Sol under D055. Global/default adoption remains deferred pending task-level/comparative evidence and host/account availability. |
| R011 | `docs/research/CODEX-COORDINATOR-IDENTITY-WORKTREE-HYGIENE-RESEARCH.md` | COMPLETE | DECIDED | current source-maintenance workflow; T056/T057 lineage | `docs/decisions/D058-executor-coordinator-session-and-worktree-hygiene.md` | D058 adopts deterministic coordinator chat names, exclusive writable worktrees, fail-closed local-state classification and post-integration worktree retirement/primary-checkout convergence. |
| R012 | `docs/research/CODEX-COORDINATOR-DELEGATION-POLICY-RESEARCH.md` | COMPLETE | DECIDED | R006; T053; R007; T057; official OpenAI multi-agent guidance | `docs/decisions/D065-semantic-executor-delegation-obligation.md` | D065 adopts the semantic delegation obligation: Agent Governance defines material triggers/anti-triggers plus safety/evidence bounds, while the Executor coordinator retains concrete decomposition, child count/roles, sequencing/parallelism and mechanics. D075 later makes the pre-worker direct-execution gate explicit without replacing D065. |
| R013 | `docs/research/CODEX-TASK-SCOPED-COORDINATOR-CONTINUITY-RESEARCH.md` | COMPLETE | DECIDED | R006; T053; R012; current OpenAI long-running/compaction guidance | `docs/decisions/D060-task-scoped-executor-coordinator-continuity.md` | Adopt one Human-visible Executor Coordinator Root per exact Task/Operational Contract: NEW at work-unit start, CONTINUE through clean same-task phases/rework, retire at closure, root-2+ failover only. |
| R014 | `docs/research/CHATGPT-GIT-WORKSPACE-AND-GITHUB-TRANSPORT-RESEARCH.md` | COMPLETE | DECIDED | workspace/GitHub experiments; test_biblioteca qualification; source research PR `#291`; T058 path | `docs/decisions/D066-chatgpt-portable-git-workspace-transport.md` | D066 adopts the qualified local-Git + Library snapshot + explicit GitHub transport/lifecycle subset for ChatGPT Orchestrator source maintenance. Unqualified recovery/GC/ruleset gaps remain explicit. |
| R015 | `docs/research/CHATGPT-LIBRARY-WORKTREE-SIMULATOR-RESEARCH.md` | COMPLETE | DECIDED | R014; D058; test_biblioteca isolation/lifecycle/race qualification; PR `#291`; T058 path | `docs/decisions/D066-chatgpt-portable-git-workspace-transport.md` | D066 adopts the qualified portable workspace isolation subset using unique topic branch + coordination-only lock branch + expected-HEAD CAS + owner sentinel + standalone Library Git snapshot; unresolved recovery/transfer/automatic-retirement gaps remain explicit. |
| R016 | `docs/research/R016-MG1-V12-REFERENCE-FAMILY-REENTRY.md` | COMPLETE | EVALUATING | T061 successor lineage; D074/T062 v15 RIQ-NBC; T023-R30/R31/R32/R33 | none | The original reference-family re-entry has evolved into T062 RIQ-NBC. T062 Stage 5 is complete, the first Stage 6 attempt blocked before provider process creation with zero provider/model calls, R32 continuation authority exists but is unconsumed, and T023-R33 places the scientific line in Human Hold. No topology is selected; the research/evaluation disposition remains open. |
| R017 | `docs/research/R017-COORDINATOR-DIRECT-EXECUTION-GATE.md` | COMPLETE | DECIDED | R012/D065; R007/T054/T054-R1; D063; fresh official revalidation by R018 | `docs/decisions/D075-coordinator-direct-execution-gate.md` | D075 makes the first routing gate explicit: low-elaboration auxiliary microactions may remain coordinator-direct when delegation overhead dominates, while materially elaborated isolatable units remain subject to D065 mandatory delegation. R018 subsequently performs the fresh external revalidation that was not actually executed before D075 integration and confirms the decision without normative change. |
| R018 | `docs/research/R018-CODEX-SUBAGENT-RUNTIME-REVALIDATION.md` | COMPLETE | NOT_REQUIRED | D075; T063; `docs/reviews/T063-R1.md`; exact official Codex `rust-v0.153.4` source and current OpenAI docs | none | Fresh official revalidation supported D075/D065 and the T063 hypotheses. Its volatile statement that `0.153.4` was current stable was true at review time; R019 records that `0.154.0` later became stable while `0.153.4` remains deliberately pinned as the D063-qualified T063 experimental baseline. |
| R019 | `docs/research/R019-T063-MULTI-AGENT-V2-HARNESS-REENTRY.md` | COMPLETE | NOT_REQUIRED | `docs/reviews/T063-R3.md`; D076; `docs/reviews/T063-R4.md`; R020 | none | R019 correctly froze the runtime pin, V2 `task_name`/`fork_turns`, explicit feature configuration, P3 placement, clean-rerun rule and D076 boundary. R020 prospectively supersedes only R019 Finding 4 and its live V2 spawn/message receipt assumptions: `subAgentActivity` is the public spawn correlation item and `thread/read` cannot attest the inter-agent task as a child `userMessage`. |
| R020 | `docs/research/R020-T063-V2-LIVE-RECEIPT-CORRECTION.md` | COMPLETE | NOT_REQUIRED | v2 terminal HEAD `3ff745a8d29e031ca818c1bc618b15a54e0cbf2b`; `docs/reviews/T063-R5.md`; exact official Codex `rust-v0.153.4` source | none | Live evidence plus exact source establish that T063 v2 blocked on incorrect Stage 5 receipt assumptions, not worker quality. One P1 ADAPTIVE call was consumed but is invalid/unscored. `experimentalRawEvents` could expose exact function-call arguments but is internal-only and not D063-qualified. R021 changes the future repair architecture rather than rewriting this historical diagnosis. |
| R021 | `docs/research/R021-T063-V3-CONFIG-AUTHORITATIVE-WORKER-RECEIPTS.md` | COMPLETE | DECIDED | v3 candidate `9b8a8d96b7586c25e808e93c3cec02d1f2fa3467`; `docs/reviews/T063-R6.md`; official Codex `0.153.4`, `0.154.0`, `0.155.0-alpha.2` source/release evidence | `docs/decisions/D077-version-sensitive-upstream-revalidation.md` | V3 removes the unsupported exact spawned-task-message receipt by moving substantive task/profile authority into Stage 5 App Server configuration, retaining public `subAgentActivity` child correlation and D063 measurement receipts. Higher relevant Codex versions do not remove the blocker, so `0.153.4` remains deliberately pinned. D077 adopts the general version-sensitive upstream-revalidation rule. |
| R022 | `docs/research/R022-T063-V3-EMPTY-ROLLOUT-REATTACH-RACE.md` | COMPLETE | NOT_REQUIRED | v3 terminal HEAD `746519abc6f159e959120f68d5c9f920d88d5797`; v4 candidate `f06c8f48f7b1d59dff9fc117cca5b42453ad23e8`; `docs/reviews/T063-R7.md`; official Codex `0.153.4`, `0.154.0` and current-main source | none | V3 blocked because immediate exact-child `thread/resume` raced rollout metadata persistence. The live-thread reattach path still reads persisted thread state, and current stable retains the same dependency/error class. V4 adds a bounded same-child retry barrier with parent-residency recheck immediately before each retry, no new provider turn, and fail-closed handling; the 0.153.4 qualified pin remains deliberate. |

## Live research frontier

### T063 — adaptive worker routing requalification

```text
R017 — coordinator direct-execution gate
  COMPLETE / DECIDED -> D075
  Stage A: COORDINATOR_DIRECT | DELEGATED | CONTRACT_FIXED

R018 — Codex subagent/runtime revalidation
  COMPLETE / NOT_REQUIRED
  D075 conclusion supported
  0.153.4 was stable at R018 review time

R019 — T063 Multi-Agent V2 harness re-entry
  COMPLETE / NOT_REQUIRED
  runtime pin / V2 task_name + fork_turns / P3 / D076 corrections remain historical inputs
  spawn/message receipt assumption partially superseded by R020

R020 — T063 v2 live receipt correction
  COMPLETE / NOT_REQUIRED
  v2 terminal HEAD: 3ff745a8d29e031ca818c1bc618b15a54e0cbf2b
  one P1 ADAPTIVE attempt consumed; invalid/unscored
  worker answer diagnostic PASS only
  public V2 child correlation: subAgentActivity
  child spawn task: InterAgentCommunication, not userMessage
  raw response event route: internal-only / not D063-qualified

R021 — T063 v3 config-authoritative receipt repair
  COMPLETE / DECIDED -> D077 for the general version-sensitive rule
  original v3 candidate HEAD: 9b8a8d96b7586c25e808e93c3cec02d1f2fa3467
  substantive child task/profile authority: Stage 5 thread config
  public child correlation: subAgentActivity
  D063 measurement set: preserved
  raw response events: not used
  version disposition: PIN_RETAINED on 0.153.4

R022 — T063 v3 empty-rollout reattach race
  COMPLETE / NOT_REQUIRED
  v3 terminal HEAD: 746519abc6f159e959120f68d5c9f920d88d5797
  one P1 ADAPTIVE attempt consumed; invalid/unscored
  blocker: same-child rollout-persistence visibility race during thread/resume
  v4 candidate HEAD: f06c8f48f7b1d59dff9fc117cca5b42453ad23e8
  retry invariant: same child / no provider replay / parent residency immediately before retry
  current stable reviewed: 0.154.0; same persistence dependency remains
  version disposition: PIN_RETAINED on 0.153.4

R007 — adaptive subagent compute routing
  COMPLETE / EVALUATING
  T054: accepted execution / NOT_QUALIFIED
  D063: measurement substrate qualified on 0.153.4
  T063 v1: blocked / no pilot decision
  T063 v2: blocked / no pilot decision
  T063 v3: blocked / no pilot decision
  T063 v4: Stage 5 complete / Stage 6 authorized awaiting Human Codex start
  scored execution_target: CONTRACT_FIXED
  underlying probe delegation eligibility: DELEGATED
  next T063 step: NEW root-4 clean six-arm v4 execution, then Orchestrator convergence
```

T063 deliberately does not vary the D075 Stage-A delegation-worthiness decision. Its exact matched-arm topology is contract-fixed because topology is material to the experiment, while the selected probe units independently satisfy D065/D075 material-delegation eligibility. Only the child execution profile is the scored experimental variable.

All three blocked T063 evidence heads remain historical and excluded from v4 scoring:

```text
v1  3d8a9460988351383a90adfc6b76e2deff056504
v2  3ff745a8d29e031ca818c1bc618b15a54e0cbf2b
v3  746519abc6f159e959120f68d5c9f920d88d5797
```

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

R018 — Codex subagent/runtime revalidation
  COMPLETE / NOT_REQUIRED
  supporting evidence for D075/T063 prelaunch

R019/R020 — T063 historical runtime/harness receipt research
  COMPLETE / NOT_REQUIRED
  R020 partially supersedes R019's V2 message-receipt mechanics

R021 — T063 v3 config-authoritative receipt/version revalidation
  COMPLETE / DECIDED -> D077

R022 — T063 v3 empty-rollout reattach race
  COMPLETE / NOT_REQUIRED
  supports R7 v4 measurement-adapter repair without normative decision change
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
  explicit unresolved recovery/automatic-retirement gaps remain
```

D063 qualifies the child measurement substrate only. D065 establishes delegation obligation. D075 establishes only the coordinator-direct versus delegated/contract-fixed first gate. D077 governs upstream version-range revalidation. None of them adopts adaptive child compute routing, changes D055, establishes provider-signed backend identity, or authorizes a global savings claim. R007 remains EVALUATING through T063.

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

Version-sensitive external/vendor research is additionally subject to D077: compare the pinned/reference version, current stable, and higher relevant versions before promoting a version-dependent conclusion into consequential authority.

## Provenance rule

Do not rewrite a completed research artifact merely to align with a later conclusion. Preserve the original analysis, create or reference a successor when material evidence changes, and use the registry to express supersession/current disposition.

For volatile vendor/model/pricing/regulatory facts, revalidate the source before a later decision and update `Last-Reviewed` metadata or create a successor research item.