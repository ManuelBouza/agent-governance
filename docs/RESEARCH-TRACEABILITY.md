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
| R007 | `docs/research/ADAPTIVE-SUBAGENT-COMPUTE-ROUTING-RESEARCH.md` | COMPLETE | DEFERRED | `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md`; `docs/reviews/T054-R1.md`; PR `#277`; D063 measurement qualification | none | T054 execution was accepted with pilot decision `NOT_QUALIFIED`: P1 exposed a real `Luna / Low` exactness failure, P2 had a shared task/oracle-semantics confound across both arms, and P3 passed in both arms. D063 clears the measurement-substrate blocker, but no global child-routing policy is adopted. Reconsider only after a corrected successor evaluation removes the P2 confound, uses a first-attempt-qualified mapping, adopts the D063 measurement boundary, and receives its own explicit D057 transition. |
| R008 | `docs/research/CODEX-CHILD-OBSERVABILITY-SURFACE-RESEARCH.md` | COMPLETE | DECIDED | `docs/tasks/T055-codex-child-observability-qualification.md`; `docs/reviews/T055-R1.md`; `docs/tasks/T056-codex-read-only-child-requalification.md`; `docs/reviews/T056-R1.md`; `docs/tasks/T057-codex-read-only-child-requalification-v2.md`; `docs/reviews/T057-R1.md`; evidence PRs `#280`, `#284`, `#296` | `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md` | T055 exposed the non-write receipt gap; R009 identified the stronger 0.153.4+ profile-ID/parent-owned reload path; T056 confirmed the parent path but failed in its temporary controller; T057 then qualified the complete exact-child read-only/identity/usage/duration/reroute surface. D063 adopts that bounded, version-sensitive measurement substrate while preserving the backend-served identity boundary. |
| R009 | `docs/research/CODEX-CHILD-SANDBOX-INHERITANCE-RESEARCH.md` | COMPLETE | DECIDED | `docs/tasks/T056-codex-read-only-child-requalification.md`; `docs/reviews/T056-R1.md`; `docs/tasks/T057-codex-read-only-child-requalification-v2.md`; `docs/reviews/T057-R1.md`; evidence PRs `#284`, `#296` | `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md` | Official source supports parent-derived child permission inheritance and the 0.153.4 parent-owned reload fix. T057 empirically closed the remaining child provenance gate: parent and exact child both returned `activePermissionProfile.id=:read-only`, parent residency was continuous, and exact child usage/duration/reroute evidence was captured. D063 adopts the qualified surface subject to native version/capability revalidation. |
| R010 | `docs/research/GPT6-ASTRA-EXECUTOR-LAUNCH-PROFILE-RESEARCH.md` | COMPLETE | DEFERRED | no empirical project evaluation yet | none | GPT-6 Astra is an official quality-first flagship and current Codex source supports it, but availability alone does not justify globally replacing Sol under D055. T056/T057 remained `GPT-5.6 Sol / Medium` to avoid a model-family confound. Global/default Astra adoption is deferred pending task-level or comparative evidence and host/account availability. |
| R011 | `docs/research/CODEX-COORDINATOR-IDENTITY-WORKTREE-HYGIENE-RESEARCH.md` | COMPLETE | DECIDED | current source-maintenance workflow; T056/T057 local-execution lineage | `docs/decisions/D058-executor-coordinator-session-and-worktree-hygiene.md` | Codex supports explicit Human-visible thread naming, while existing branch cleanup did not fully require obsolete-worktree retirement plus primary-checkout convergence. D058 adopts deterministic coordinator chat names, exclusive writable worktrees for concurrent work units, fail-closed local-state classification, post-integration worktree retirement, and a clean/current primary checkout baseline. |
| R012 | `docs/research/CODEX-COORDINATOR-DELEGATION-POLICY-RESEARCH.md` | COMPLETE | DECIDED | R006; T053; `docs/reviews/T053-R1.md`; R007; T057 terminal convergence; current Codex 0.153.4 + official OpenAI multi-agent guidance | `docs/decisions/D065-semantic-executor-delegation-obligation.md` | D065 adopts the semantic delegation obligation: Agent Governance defines material delegation triggers/anti-triggers plus safety/evidence bounds, while the Executor coordinator retains concrete decomposition, child count/roles, sequencing/parallelism and mechanics. Exact topology remains Task/Operational-Contract-specific only when materially authoritative. No child compute-routing policy is implied. |
| R013 | `docs/research/CODEX-TASK-SCOPED-COORDINATOR-CONTINUITY-RESEARCH.md` | COMPLETE | DECIDED | R006; T053; `docs/reviews/T053-R1.md`; R012; current OpenAI long-running/compaction guidance | `docs/decisions/D060-task-scoped-executor-coordinator-continuity.md` | Adopt one Human-visible Executor Coordinator Root per exact Task/Operational Contract. `NEW` at work-unit start, `CONTINUE` through normal same-task phases/rework, retire at closure, and start a new root for the next work unit. `root-2+` is failover only. Root context stays compact through durable Git pointers, concise summaries and supported compaction/fresh child contexts rather than cross-task root reuse. |
| R014 | `docs/research/CHATGPT-GIT-WORKSPACE-AND-GITHUB-TRANSPORT-RESEARCH.md` | COMPLETE | NOT_REQUIRED | workspace/GitHub experiment; `ManuelBouza/test_biblioteca` Library/GitHub round trips; full `.git` and cross-chat snapshot tests; multi-file/409 capability matrix; Library lifecycle qualification PRs `test_biblioteca#1` and `#2`; official OpenAI Library storage/retention docs checked 2026-09-05 | none | ChatGPT can combine real temporary-workspace Git semantics, persistent Library file/version storage, packaged full-repository snapshots including `.git`, cross-chat Git-history continuation, and explicit GitHub connector transport. The Library GC core is empirically qualified: a real merged branch was retired only after target snapshot round-trip validation and exact Git-tree equivalence; closed-unmerged work was retained; a corrupt candidate left the validated current snapshot untouched. Library deletion moved test artifacts to Trash rather than proving immediate physical erasure. The quota-pressure selector remains unqualified. Library is storage, not a native Git working tree/remote; synchronization and cleanup remain explicit. No workflow/policy adoption is implied. |
| R015 | `docs/research/CHATGPT-LIBRARY-WORKTREE-SIMULATOR-RESEARCH.md` | COMPLETE | NOT_REQUIRED | R014; D058; `ManuelBouza/test_biblioteca` isolated target/topic branches; commits `c1208d6bb5f9e6cc28df7fcc4463d6144750cda9` and `1904904cde94c87bee17ab2e26d757d880f3fb07`; dedicated lock-ref collision test; Library worktree snapshots under `/git-workspaces/ManuelBouza/test_biblioteca/worktree-simulator/` | none | A cross-chat worktree simulator is feasible without treating Library as a native worktree service: one writable work unit maps to one topic branch, one atomically acquired dedicated GitHub lock ref, one portable standalone `.git` snapshot in a unique Library namespace, and an ownership/freshness receipt checked before mutation. Two logical chats changed the same file independently without modifying each other or the target; duplicate lock acquisition failed with HTTP 422; both Library snapshots round-tripped with `git fsck` and exact remote/local tree equality; a wrong-owner restore was blocked before write. Native linked worktree directories are not individually portable because `.git` points back to shared repository metadata. True simultaneous two-chat lock racing, stale-lock recovery/TTL, lock-ref retirement, and post-crash ownership recovery remain unqualified. No policy adoption is implied. |

## Live research frontier

The child-observability research line is decided:

```text
R008 — Codex child observability surface
  COMPLETE / DECIDED -> D063
  T057: ACCEPTED / QUALIFIED_READ_ONLY_CHILD_SURFACE

R009 — Codex child sandbox inheritance / receipt
  COMPLETE / DECIDED -> D063
  T057 closed the exact-child :read-only provenance and continuous-parent-residency gate
```

Deferred dependency:

```text
R007 — adaptive subagent compute routing
  COMPLETE / DEFERRED
  measurement-substrate blocker: CLEARED by D063
  remaining gate: corrected successor evaluation with T054 P2 confound removed,
                  first-attempt-qualified mapping, D063 measurement boundary,
                  and explicit D057 transition before execution
```

Completed/decided coordinator research:

```text
R006 — persistent Executor coordinator
  COMPLETE / SUPERSEDED
  same-task continuity evidence retained
  cross-Task dossier-root recommendation superseded by R013/D060

R011 — coordinator identity / worktree hygiene
  COMPLETE / DECIDED -> D058

R012 — coordinator delegation policy
  COMPLETE / DECIDED -> D065
  semantic delegation obligation adopted; concrete orchestration remains Executor-owned

R013 — task-scoped coordinator continuity
  COMPLETE / DECIDED -> D060
  one complete Task/Operational Contract = one Human-visible root lifecycle
```

Completed research dispositions outside the live evaluation frontier:

```text
R010 — GPT-6 Astra Executor launch profile
  COMPLETE / DEFERRED
  no global D055 Astra migration adopted

R014 — ChatGPT Git workspace / Library / GitHub transport
  COMPLETE / NOT_REQUIRED
  full Git snapshots including .git persist across chats and can continue Git history
  explicit GitHub transport, multi-file one-commit reconstruction, and stale-base rejection are verified
  Library lifecycle/GC core: QUALIFIED / NON_NORMATIVE
  merged snapshot retirement after target validation: VERIFIED
  closed-unmerged retention: VERIFIED
  invalid candidate preserves current: VERIFIED
  remaining GC gap: quota-pressure automatic selector

R015 — ChatGPT Library worktree simulator
  COMPLETE / NOT_REQUIRED
  D058-style exclusive writable workspaces can be emulated across transient chat runtimes
  dedicated GitHub lock ref per logical worktree: VERIFIED
  distinct topic branches + portable standalone Library Git snapshots: VERIFIED
  same-file concurrent-work isolation across logical chats: VERIFIED
  wrong-owner write gate: VERIFIED
  native linked worktree directory portability: NOT SUPPORTED
  remaining gaps: true simultaneous two-chat race, stale-lock recovery/TTL, lock-ref retirement
```

D063 qualifies the measurement substrate only. D065 establishes delegation posture only. Neither adopts child compute routing, alters D055, establishes backend-served per-turn model identity, or authorizes savings claims. R007 remains separately deferred until a corrected evaluation is specified and explicitly transitioned.

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
