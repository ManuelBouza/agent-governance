# T053 — Codex Persistent Executor Coordinator Pilot

## Identity

- Task ID: `T053`
- Status: `PLANNED`
- Type: `behavior-preserving technical refactor + Executor continuity/subagent pilot`
- Base branch: `develop`
- SDD profile: `ASSURED`
- Test-Authorship-Mode: `executor-implementation`
- Research source: `docs/research/CODEX-PERSISTENT-EXECUTOR-COORDINATOR-RESEARCH.md`
- Continuity scope: `T053/repository-context-refactor-pilot-v1`
- D055 status: **unchanged for this pilot**
- First Human-to-Executor launch: `NEW`
- Accepted same-task/same-branch Phase-2 follow-up: `CONTINUE`

## Objective

Validate whether one persistent Codex Executor coordinator root can reduce repeated bootstrap/orientation burden and protect high-value execution context by delegating bounded work to fresh subagents, while preserving Agent Governance authority, Git safety, technical quality, and recoverability.

The pilot MUST simultaneously deliver useful source maintenance: a behavior-preserving modular refactor of the `repository_context` tooling subsystem, which is currently grandfathered by the code-health ratchet at:

- `tools/repository_context.py`: `1117` physical LOC;
- `tests/test_repository_context.py`: `1540` physical LOC.

T053 MUST:

1. keep one Human-visible Codex coordinator root for the full T053 continuity scope;
2. use a `NEW` root for Phase 1 under current D055;
3. stop at an Orchestrator-reviewed `PARTIAL` checkpoint;
4. use the **same root** with `CONTINUE` for Phase 2 only after persisted Orchestrator acceptance;
5. perform D042 Git/current-authority reconciliation before both phases;
6. delegate bounded exploration, implementation, and independent technical review to fresh internal Codex subagents;
7. keep completed child threads disposable and transfer only concise results/evidence references into the root;
8. preserve one-writer-per-mutable-worktree safety;
9. behavior-preservingly decompose `tools/repository_context.py` and its oversized test module into agent-legible focused modules;
10. collect pilot telemetry sufficient to decide whether persistent Executor continuity merits a later D055 refinement.

This task is a **source-product pilot only**. It does not change Governance Core consumer semantics and does not authorize a reusable App Server/SDK session manager.

## Problem statement

Current D055 deliberately defaults the first launch of a new Task Contract/work unit to a fresh Executor session. This protects against stale or contaminated context, but repeated related work can pay substantial bootstrap/orientation cost.

Current Codex supports native subagents and persistent related-work sessions. The research memo recommends retaining one high-level coordinator context per coherent execution dossier while pushing noisy/disposable exploration, implementation slices, logs, and independent review into bounded fresh children.

The hypothesis is:

```text
persistent high-value coordinator context
+ fresh bounded children
+ mandatory Git rehydration
+ concise child summaries
= lower repeated bootstrap/context pollution
  without authority or quality loss
```

The hypothesis is not assumed true. T053 must measure it.

## Governance boundary

### Preserved authority

T053 MUST preserve:

- D041 Executor process autonomy;
- D042 remote freshness and safe local baseline requirements;
- D053 stage ownership;
- D054 Execution Adapter ownership;
- current D055 Human-facing launch semantics;
- D056 progress-note expectations;
- Git as authoritative project state;
- ChatGPT ownership of all committed Markdown;
- existing Task Contract/handoff/review authority;
- the rule that private Executor/subagent reasoning is never Governance authority.

The persistent coordinator root is **execution cache**, not durable authority.

Before Phase 2, any retained coordinator belief that conflicts with current Git, `AGENTS.md`, the current checkpoint, this Task Contract, or the persisted Phase-1 review is stale and MUST be discarded.

### No child Governance lifecycle

Internal Codex children are private Executor mechanics under D041. They do not receive separate Human-facing D055 launch cards and do not create separate Governance lifecycle authority.

Children MUST NOT:

- edit committed Markdown;
- redefine Task Contract scope, Design, Plan/Trace, acceptance criteria, or product semantics;
- create lifecycle/checkpoint authority outside authorized non-Markdown handoff/evidence files;
- become a correctness dependency after their result is summarized and represented in Git/evidence.

## Technical maintenance deliverable

### Preserved behavior

The repository-context subsystem's externally observable behavior MUST remain unchanged unless this Task Contract explicitly says otherwise.

Preserve at minimum:

- existing CLI commands, arguments, stdout/stderr shapes, exit semantics, and file targets;
- `build_report` physical-context measurement semantics;
- canonical payload/identity and volatile provenance separation;
- tracked-tree measurement and Markdown-reference behavior;
- RCAB registry parsing, canonicalization, validation, and digest semantics;
- epoch snapshot versus live-currentness separation;
- snapshot payload digest behavior;
- registered-content measurement and bootstrap/router ratchet behavior;
- `build_manifest`, `build_live_status`, `check_manifest`, and snapshot-integrity semantics;
- existing baseline/manifest/context-map schema identities and meanings;
- current deterministic error/fail-closed behavior;
- module-level callable compatibility relied on by existing tests/tooling.

Do not rewrite `docs/CONTEXT-MAP.md`, baselines, schema semantics, Governance Core, or accepted context-management policy merely to simplify the refactor.

If a material semantic defect is discovered, stop for Orchestrator re-entry rather than redesigning it inside T053.

## Target architecture

Keep `tools/repository_context.py` as the stable compatibility/CLI facade.

Extract cohesive implementation under `tools/_repository_context/` (or a mechanically equivalent package if Python import constraints require it). Exact filenames may vary mechanically, but the approved responsibilities are:

1. **constants/models** — schema/version constants, narrow shared types/errors;
2. **git/files** — tracked-path enumeration and tracked-file reads;
3. **measurement/report** — file metrics, Markdown reference projection, report construction, canonical report identity;
4. **registry** — context-map registry parse/canonicalization/validation/digest;
5. **projection/ratchet** — registered-path measurements and bootstrap/router ratchet calculation;
6. **snapshot/live** — epoch manifest construction, snapshot integrity, live status, explicit currentness comparison;
7. **CLI/facade** — backward-compatible public imports and command dispatch.

Prefer an acyclic dependency direction:

```text
constants/models
      ↓
   git/files
      ↓
measurement/report     registry
          \             /
           projection/ratchet
                  ↓
             snapshot/live
                  ↓
            CLI compatibility
```

Equivalent acyclic layering is acceptable. Circular imports are forbidden.

The facade may re-export existing public functions/constants so callers do not need migration in T053.

## Code-health targets

Use `docs/AGENT-LEGIBLE-CODE-HEALTH.md` and the existing deterministic checker.

Final targets:

- `tools/repository_context.py`: `<= 500` physical LOC; target `<= 350`;
- `tests/test_repository_context.py`: `<= 500` physical LOC after focused test extraction;
- each new/refactored implementation/test module: target `<= 500`, hard limit `1000`;
- no new oversized-module grandfathering merely to complete T053;
- update `code-health.json` to ratchet accepted final sizes downward and remove the old `1117`/`1540` permissions when no longer needed;
- add the new implementation package to complexity and symbol-map coverage where mechanically appropriate;
- prove the extracted implementation package is acyclic.

If a module exceeds `600` LOC, the final handoff must justify why it remains cohesive. A new module above `1000` is not acceptable.

## Pilot topology

### Coordinator Root

One Human-visible Codex root owns T053 execution coordination across both phases.

The root should retain only high-value continuity state:

- current T053 objective and phase;
- authoritative Git pointers;
- relevant accepted architectural constraints;
- represented branch/worktree state;
- concise child conclusions;
- unresolved blockers;
- verification/evidence references.

The root SHOULD NOT pull full child transcripts, large file dumps, raw test logs, or abandoned implementation traces back into its context.

### Child roles

Use current stable/native Codex subagent capability. Start with built-in/native roles rather than introducing a project `.codex/agents/` catalog in this pilot.

Required functional roles across each phase:

- **Explorer** — read-only code/test/dependency mapping;
- **Worker** — the single primary writer for the authorized implementation slice;
- **Verifier/Reviewer** — fresh read-only independent technical review of the resulting slice.

A role may use the closest stable built-in Codex agent available. Do not add custom agent files solely to satisfy a role label.

### Concurrency and writer safety

- maximum initial pilot concurrency: `3` open child threads;
- parallel read-heavy children are allowed when their scopes are independent;
- at most **one write-capable actor** may mutate a given worktree at a time;
- normally one Worker child is the implementation writer;
- if the coordinator root itself must edit technical files, no write-capable child may be concurrently active;
- multiple writers on the same mutable worktree/branch are forbidden;
- multiple write worktrees are outside this pilot.

### Child return contract

A child normally returns only:

```text
status
bounded scope completed
concise findings/result
files/symbols affected
verification performed
Git/evidence references when applicable
blocker/follow-up if any
```

Full transcripts are not routine return artifacts.

Completed children MUST be closed after their concise result has been transferred. Phase-1 children MUST NOT be resumed in Phase 2.

## Two-phase execution plan

### Phase 1 — NEW root, characterize + first extraction

Human D055 launch profile MUST be `NEW` because T053 is a new Task Contract.

The root MUST first satisfy D042 and reload current repository authority before delegating.

Required Phase-1 sequence:

1. establish safe current local baseline from canonical Git;
2. read applicable repository instructions and T053 authority;
3. record pilot phase start telemetry;
4. spawn at least two fresh read-only bounded explorations, preferably in parallel:
   - runtime/symbol/dependency map of `tools/repository_context.py`;
   - existing test/CLI/compatibility contract map from `tests/test_repository_context.py` and callers;
5. consolidate only concise explorer summaries into the root;
6. close explorer children;
7. establish/strengthen characterization tests before structural mutation where existing tests do not already fail closed;
8. spawn one fresh Worker as the sole implementation writer for the first extraction slice;
9. Phase 1 implementation slice must extract the **tracked-file measurement/report + canonical identity** responsibilities behind the stable facade without changing semantics;
10. root runs deterministic focused verification;
11. spawn a fresh read-only Verifier/Reviewer to inspect the Phase-1 diff against T053 and characterization authority;
12. resolve in-scope technical defects without changing upstream semantics;
13. close Worker/Verifier children;
14. commit/push the represented branch;
15. persist `handoffs/T053-phase1.json` and `handoffs/T053-pilot-telemetry.json`;
16. return `STATUS: PARTIAL` with branch and pushed HEAD.

Phase 1 MUST stop after the checkpoint. It MUST NOT continue automatically into Phase 2.

The expected branch is:

`refactor/t053-repository-context-coordinator-pilot`

A mechanically equivalent task-specific branch name is acceptable if collision-safe and recorded in the handoff.

### Phase-1 Orchestrator barrier

ChatGPT Orchestrator independently reviews the remote branch and persists `docs/reviews/T053-P1.md` if the checkpoint is accepted.

Phase 2 is unauthorized until that review exists in canonical `develop` and explicitly allows continuation.

### Phase 2 — CONTINUE same root, fresh children, complete refactor

Under unchanged D055, the accepted same-task/same-branch continuation SHOULD use `CONTINUE` in the **same Human-visible Codex root**.

Before using retained context, the root MUST:

1. perform D042 remote freshness reconciliation again;
2. reload current `AGENTS.md`, current checkpoint, T053, and `docs/reviews/T053-P1.md`;
3. reconcile retained root assumptions against Git/current authority;
4. record any stale assumptions corrected by rehydration;
5. prove/record that the intended same coordinator root was continued when the host exposes a stable non-secret identifier or fingerprint.

Phase-1 children are disposable and MUST NOT be resumed.

Required Phase-2 sequence:

1. spawn fresh bounded Explorer child(ren) for remaining registry/snapshot/live/CLI extraction risk;
2. close them after concise summaries;
3. spawn one fresh Worker as sole implementation writer;
4. complete the approved modular decomposition and test-module split;
5. update code-health ratchets/coverage for the accepted new structure;
6. run focused and full deterministic verification;
7. spawn a fresh independent read-only Verifier/Reviewer over the complete T053 delta;
8. correct only in-scope technical defects;
9. close all children;
10. persist final pilot telemetry and `handoffs/T053-executor-handoff.json`;
11. commit/push final branch and return only standard terminal handoff fields.

## Continuity/recovery rules

Thread/session state is an optimization and MUST NOT become correctness authority.

### Root unavailable before Phase 2

If the same coordinator root cannot be resumed/continued:

- do not claim continuity success;
- do not silently substitute a new root and count the pilot as successful;
- preserve Git state;
- return/report `COORDINATOR_RESUME_UNAVAILABLE` for Orchestrator decision.

A later fresh root may recover the technical work from Git, but that recovery is a separate pilot outcome.

### Child failure

If a child fails or becomes unusable:

- close/discard it when possible;
- a fresh replacement child may be spawned with the same bounded scope;
- record the retry and reason in telemetry;
- do not depend on recovering the failed child's private reasoning history.

### Authority conflict

If retained coordinator context conflicts with canonical Git/current authority, Git wins. Record the stale assumption and proceed only if the conflict is mechanically reconcilable inside T053; otherwise stop for Orchestrator re-entry.

## Pilot telemetry

Persist non-Markdown telemetry in `handoffs/T053-pilot-telemetry.json`.

The file must separate Phase 1 and Phase 2 and record at minimum:

### Required operational fields

- continuity scope ID;
- phase;
- root launch mode (`NEW` or `CONTINUE`);
- D042 reconciliation result;
- canonical base/authority revisions observed;
- branch/worktree identity;
- phase start/end timestamps and duration;
- time to first useful technical action when deterministically observable;
- child spawn count;
- for each child: functional role, bounded purpose, read/write capability, retry/replacement status, closed status;
- maximum observed concurrent children;
- count of write-capable actors active at one time; MUST never exceed `1` per worktree;
- stale-authority assumptions detected/corrected;
- branch/worktree incidents;
- child failures/retries;
- compaction events if observable;
- root continuation evidence/fingerprint when safely exposable;
- verification/rework outcome.

### Token/context telemetry — best effort but explicit

When Codex exposes these values, record separately for root and children:

- input tokens;
- cached input tokens when available;
- output tokens;
- reasoning tokens;
- total tokens/context occupancy if exposed.

If a metric is not exposed by the supported host surface, persist `null` plus an explicit availability reason rather than estimating it.

Do not parse private chain-of-thought or persist full child transcripts to obtain telemetry.

### Bootstrap comparison

For each phase, record a concise bootstrap/orientation inventory:

- authoritative instruction/task/review files explicitly reloaded by the root;
- repeated repository-orientation reads the root considered necessary before first technical delegation/action;
- whether prior phase summaries avoided rereading large implementation surfaces;
- any deliberate reread required because Git/current authority changed.

This is observational pilot evidence, not correctness authority.

## Pilot success criteria

The pilot evaluates the continuity topology separately from the technical refactor.

A positive continuity recommendation requires all of:

1. same coordinator root successfully continued from accepted Phase 1 to Phase 2;
2. D042/current-authority rehydration passed before both phases;
3. stale-authority/branch/worktree safety incidents = `0`;
4. one-writer invariant held throughout;
5. Phase-1 children were not reused in Phase 2;
6. child results were transferred concisely rather than by full transcript ingestion;
7. root persistence demonstrably avoided at least some repeated architectural/orientation work **or** improved coordinator context locality in a reviewable way;
8. technical quality/acceptance is equal or better than the repository baseline;
9. token/compute amplification, when measurable, remains acceptable relative to saved bootstrap/wall time/quality;
10. loss of any child would not have lost durable project authority.

Failure to prove item 7 does not invalidate the technical refactor; it means the persistence hypothesis is unproven.

The Orchestrator, not the Executor, decides whether evidence justifies a later D055 change.

## Required technical verification

Phase 1 must run at minimum:

1. focused existing repository-context tests;
2. new/strengthened characterization tests for the extracted measurement/report slice;
3. Ruff check/format on changed Python surfaces;
4. code-health check;
5. dependency/import-cycle check for the extracted package slice;
6. `git diff --check`.

Phase 2/final must run at minimum:

1. full `pytest`;
2. focused repository-context tests;
3. Ruff check;
4. Ruff format check;
5. `tools/code_health.py check --root .`;
6. deterministic symbol-map generation/validation covering the new package;
7. dependency/import-cycle check for the complete extracted package;
8. CLI compatibility/characterization tests;
9. deterministic baseline/manifest/live-status behavior tests already present in the repository;
10. `git diff --check`.

No model/provider call is required to test repository-context semantics; model usage in T053 is only the Codex Executor/subagent implementation process itself.

## Acceptance criteria

### AC-T053-1 — Phase-1 D055/D042 discipline
Phase 1 begins in a Human-visible Codex `NEW` root and records successful D042/current-authority reconciliation before child spawning or implementation.

### AC-T053-2 — bounded native subagent use
Phase 1 uses fresh bounded Explorer, Worker, and independent Verifier/Reviewer functions; no more than three children are concurrently open and only one write-capable actor mutates the worktree at a time.

### AC-T053-3 — meaningful Phase-1 technical slice
The measurement/report/canonical-identity responsibilities are extracted behind the stable facade with characterization evidence green and no semantic drift.

### AC-T053-4 — hard PARTIAL barrier
Phase 1 persists/pushes its branch, phase handoff and telemetry, closes completed children, returns `PARTIAL`, and does not execute Phase 2 before Orchestrator acceptance.

### AC-T053-5 — same-root continuation
After persisted Phase-1 acceptance, Phase 2 uses `CONTINUE` in the same coordinator root when the root is recoverable. Failure to recover is reported, not disguised by a fresh root.

### AC-T053-6 — Phase-2 Git rehydration
Before relying on retained context, the continued root repeats D042 and reloads current authority including `docs/reviews/T053-P1.md`, with stale retained assumptions resolved in favor of Git.

### AC-T053-7 — fresh Phase-2 children
Phase-2 exploration, implementation, and review use fresh bounded children. Phase-1 child threads are not resumed.

### AC-T053-8 — final modular architecture
`tools/repository_context.py <=500` LOC, `tests/test_repository_context.py <=500` LOC, new modules obey hard limits, responsibilities are cohesive/acyclic, and compatibility is preserved.

### AC-T053-9 — ratchet and navigation improvement
The old `1117`/`1540` grandfathered permissions are removed or lowered to accepted final sizes; relevant new implementation modules are covered by deterministic code-health/symbol-map checks.

### AC-T053-10 — telemetry completeness
Required operational telemetry exists for both phases; unavailable token/context metrics are explicitly null with reasons rather than invented.

### AC-T053-11 — no authority leakage
No child transcript/private reasoning becomes Governance authority; no Executor-authored Markdown is committed; Git/handoffs/tests remain sufficient for independent Orchestrator convergence.

### AC-T053-12 — verification green
All required final deterministic verification passes and independent technical review has no unresolved in-scope findings.

## Non-goals

T053 does **not** authorize:

- changing D055;
- changing Governance Core consumer semantics;
- building an App Server/SDK thread registry/session manager;
- adding `.codex/agents/*.toml` custom agent catalog solely for this pilot;
- requiring Codex subagents in every future task;
- maximizing parallelism;
- multiple writers on one worktree;
- persisting child trees as correctness state;
- changing MG1/T023 candidate/eval semantics;
- launching MG1-v13.

## Ownership

ChatGPT Orchestrator owns this Task Contract, technical Design boundaries, Phase-1 checkpoint acceptance, final convergence, and the post-pilot decision about D055/portability.

Agente de IA Ejecutor owns authorized non-Markdown implementation, tests, code-health config changes, internal Codex child orchestration, technical Code Review & Verify, telemetry/handoff JSON, Git mechanics, and branch/worktree mechanics inside the approved boundary.

## Handoffs

### Phase 1

Persist `handoffs/T053-phase1.json` and include:

- status `PARTIAL`;
- base/current HEADs and branch;
- Phase-1 technical delta summary;
- characterization/verification results;
- before/after LOC for affected runtime/test files;
- child-role summary with closed-state confirmation;
- one-writer invariant evidence;
- pointer to `handoffs/T053-pilot-telemetry.json`;
- blockers/re-entry needs if any.

Return only:

```text
STATUS: PARTIAL
HANDOFF: handoffs/T053-phase1.json
BRANCH: <branch>
HEAD: <pushed-head>
```

### Final

Persist `handoffs/T053-executor-handoff.json` and include the standard Executor evidence plus:

- proof Phase 2 used the accepted continuation path or explicit resume failure;
- D042 rehydration evidence for both phases;
- before/after LOC and final module map;
- code-health/symbol-map/dependency results;
- Phase-1 versus Phase-2 bootstrap inventory;
- child spawn/close/retry summary;
- root/child token telemetry when available;
- context/compaction telemetry when available;
- final technical verification;
- pilot observations relevant to continuity efficiency, without making the normative D055 decision.

Return only the standard terminal status, handoff path, branch, and pushed HEAD.
