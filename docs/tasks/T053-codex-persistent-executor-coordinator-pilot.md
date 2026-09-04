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
- D055: **unchanged**; Phase 1 `NEW`, accepted Phase 2 `CONTINUE`

## Objective

Test whether one persistent Codex Executor coordinator root can lower repeated bootstrap/context pollution by delegating bounded work to fresh subagents, without weakening Git authority, branch safety, technical quality, or recoverability.

The pilot also delivers useful maintenance: behavior-preserving modularization of the `repository_context` subsystem, currently grandfathered at:

- `tools/repository_context.py`: `1117` LOC;
- `tests/test_repository_context.py`: `1540` LOC.

T053 MUST use one Human-visible Codex root across two governed phases, stop after Phase 1 for Orchestrator review, use fresh disposable child agents in each phase, preserve one-writer-per-worktree safety, reduce the oversized modules, and persist telemetry sufficient for a later D055 decision.

This is a source-product pilot only. It does not change Governance Core semantics and does not authorize App Server/SDK session-management infrastructure.

## Preserved governance

D041, D042, D053, D054, D055 and D056 remain controlling.

The coordinator root is execution cache, never authority. Git, current `AGENTS.md`, checkpoint, Task Contract and Orchestrator reviews win over retained chat assumptions.

Internal Codex children are private Executor mechanics under D041. They receive no Human-facing D055 card and MUST NOT:

- edit committed Markdown;
- redefine scope, Design, Plan/Trace, acceptance, or product semantics;
- create lifecycle authority;
- become a durable correctness dependency.

Before both phases the root MUST satisfy D042. Before Phase 2 it MUST additionally reload the accepted Phase-1 review and discard stale retained assumptions.

## Technical behavior to preserve

The refactor MUST preserve existing observable `repository_context` behavior, including:

- CLI commands/arguments/output/exit behavior and file targets;
- `build_report` physical-context measurement;
- canonical payload/identity versus volatile provenance separation;
- tracked-tree and Markdown-reference measurement;
- RCAB registry parse/canonicalization/validation/digest;
- epoch snapshot versus live-currentness semantics;
- snapshot payload digest;
- registered-content measurements and bootstrap/router ratchet;
- `build_manifest`, `build_live_status`, `check_manifest`, and snapshot-integrity behavior;
- baseline/manifest/context-map schema identities and fail-closed errors;
- module-level callable compatibility relied on by current tests/tooling.

Do not rewrite `docs/CONTEXT-MAP.md`, baselines, Governance Core, schema semantics, or accepted context-management policy to simplify the refactor. A material semantic defect requires Orchestrator re-entry.

## Target architecture

Keep `tools/repository_context.py` as the stable compatibility/CLI facade. Extract cohesive implementation under `tools/_repository_context/` or a mechanically equivalent package.

Approved responsibility boundaries:

1. constants/models — schema/version constants and narrow shared types/errors;
2. git/files — tracked paths and tracked-file reads;
3. measurement/report — file metrics, Markdown references, report construction and canonical identity;
4. registry — context-map registry parse/canonicalization/validation/digest;
5. projection/ratchet — registered-path measurement and bootstrap/router ratchet;
6. snapshot/live — manifest construction, snapshot integrity, live status and explicit currentness comparison;
7. facade/CLI — compatibility exports and command dispatch.

Prefer this acyclic direction:

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
              facade/CLI
```

The facade may re-export existing public functions/constants. Circular imports are forbidden.

## Code-health targets

Use `docs/AGENT-LEGIBLE-CODE-HEALTH.md` and existing deterministic tooling.

Final targets:

- `tools/repository_context.py <=500` LOC; target `<=350`;
- `tests/test_repository_context.py <=500` LOC after focused test extraction;
- new/refactored modules target `<=500`, hard limit `1000`;
- remove or lower the old `1117`/`1540` code-health ratchets to accepted final sizes;
- cover the new implementation package with complexity/symbol-map checks where mechanically appropriate;
- deterministically prove the extracted package is acyclic.

Any module above `600` LOC requires a cohesion justification in the final handoff. No new module above `1000` is acceptable.

## Pilot topology

### Coordinator root

One Human-visible Codex root owns T053 coordination across both phases. Retain only objective/phase, Git pointers, relevant architectural constraints, branch/worktree state, concise child conclusions, blockers and evidence references.

Do not routinely ingest full child transcripts, large file dumps, raw test logs, or abandoned implementation traces into the root.

### Children

Use stable/native Codex subagents; do not add a project `.codex/agents/` catalog solely for this pilot.

Each phase must exercise these functions with fresh children:

- Explorer — read-only code/test/dependency mapping;
- Worker — primary implementation writer;
- Verifier/Reviewer — fresh read-only independent technical review.

Use the closest stable built-in role available.

### Safety

- maximum `3` concurrently open child threads;
- parallel read-only exploration is allowed when independent;
- only one write-capable actor may mutate one worktree at a time;
- normally the Worker is that writer;
- if the root edits technical files, no write-capable child may be active concurrently;
- multiple write worktrees are outside this pilot.

Completed children must be closed after concise result transfer. Phase-1 children MUST NOT be resumed in Phase 2.

Child return shape should normally be limited to:

```text
status
bounded result/findings
files/symbols affected
verification performed
Git/evidence references
blocker/follow-up
```

## Phase 1 — NEW root

D055 launch mode: `NEW`.

Required sequence:

1. D042 safe baseline + current authority reload;
2. start Phase-1 telemetry;
3. spawn at least two fresh read-only explorations, preferably parallel:
   - runtime/symbol/dependency map of `tools/repository_context.py`;
   - tests/CLI/compatibility map from `tests/test_repository_context.py` and callers;
4. retain concise summaries only, then close explorers;
5. establish/strengthen characterization tests before structural mutation where needed;
6. spawn one fresh Worker as sole writer;
7. extract the **tracked-file measurement/report + canonical-identity** responsibilities behind the stable facade;
8. run focused deterministic verification;
9. spawn a fresh read-only Verifier/Reviewer over the Phase-1 diff;
10. resolve only in-scope technical defects;
11. close all children;
12. commit/push branch;
13. persist `handoffs/T053-phase1.json` and `handoffs/T053-pilot-telemetry.json`;
14. return `PARTIAL` and stop.

Expected branch: `refactor/t053-repository-context-coordinator-pilot` or a collision-safe equivalent recorded in the handoff.

Phase 1 MUST NOT continue automatically into Phase 2.

## Orchestrator barrier

ChatGPT independently reviews the remote Phase-1 branch. Phase 2 is unauthorized until `docs/reviews/T053-P1.md` is integrated into canonical `develop` and explicitly permits continuation.

## Phase 2 — CONTINUE same root

Under unchanged D055, accepted same-task/same-branch follow-up uses `CONTINUE` in the same Human-visible Codex root.

Before relying on retained context, the root MUST:

1. repeat D042;
2. reload current `AGENTS.md`, checkpoint, T053 and `docs/reviews/T053-P1.md`;
3. reconcile retained assumptions against Git/current authority;
4. record stale assumptions corrected;
5. record same-root continuation evidence/fingerprint when safely exposed by the host.

Phase-1 children remain closed/disposable.

Required Phase-2 sequence:

1. spawn fresh Explorer child(ren) for remaining registry/snapshot/live/CLI extraction risk;
2. close explorers after concise summaries;
3. spawn one fresh Worker as sole writer;
4. complete modular decomposition and test-module split;
5. update code-health ratchets/coverage;
6. run focused and full deterministic verification;
7. spawn fresh independent read-only Verifier/Reviewer over complete T053 delta;
8. correct only in-scope technical defects;
9. close all children;
10. persist final telemetry and `handoffs/T053-executor-handoff.json`;
11. commit/push and return the standard terminal handoff fields.

## Recovery rules

### Root unavailable before Phase 2

Do not silently substitute a fresh root and call the continuity pilot successful. Preserve Git state and report `COORDINATOR_RESUME_UNAVAILABLE` for Orchestrator decision. A later fresh root may recover the technical work, but that is a different pilot outcome.

### Child failure

Discard/close the failed child when possible. A fresh replacement may retry the same bounded scope. Record retry/reason. Durable correctness must not depend on the failed child's private history.

### Authority conflict

Git/current authority wins over retained coordinator state. Record mechanically corrected stale assumptions; stop for Orchestrator re-entry if the conflict is material.

## Telemetry

Persist `handoffs/T053-pilot-telemetry.json`, separated by phase.

Required operational fields:

- continuity scope and phase;
- root launch mode (`NEW`/`CONTINUE`);
- D042 result and canonical authority revisions;
- branch/worktree identity;
- phase timestamps/duration;
- time to first useful technical action when observable;
- child spawn count and, per child: role, bounded purpose, read/write capability, retry/replacement and closed status;
- maximum concurrent children;
- maximum simultaneous write-capable actors per worktree; MUST be `<=1`;
- stale-authority assumptions corrected;
- branch/worktree incidents;
- child failures/retries;
- compaction events if observable;
- root continuation evidence/fingerprint when safely exposable;
- verification/rework outcome.

When Codex exposes token/context data, record separately for root and children: input, cached input, output, reasoning and total/context occupancy. If unavailable, store `null` plus an explicit availability reason. Do not estimate and do not persist private chain-of-thought/full child transcripts to obtain telemetry.

For each phase also record a concise bootstrap inventory: authority files reloaded, repeated orientation reads before first technical action, deliberate rereads caused by Git changes, and whether retained Phase-1 summaries avoided rereading large implementation surfaces.

## Continuity pilot decision criteria

A positive later recommendation requires:

1. same root continued Phase 1 -> Phase 2;
2. D042/current authority reload passed both phases;
3. stale-authority/branch/worktree safety incidents = `0`;
4. one-writer invariant held;
5. Phase-1 children were not reused;
6. child results returned concisely rather than via transcript ingestion;
7. persistence demonstrably avoided some repeated orientation or improved root context locality;
8. technical quality is equal-or-better than baseline;
9. measurable compute amplification is acceptable relative to bootstrap/time/quality benefit;
10. child loss would not lose durable authority.

Failure to prove item 7 does not invalidate the refactor; it leaves the persistence hypothesis unproven. Only the Orchestrator decides whether evidence warrants a later D055 change.

## Verification

Phase 1 minimum:

- focused repository-context tests;
- characterization tests for the extracted slice;
- Ruff check + format check on changed Python;
- code-health check;
- dependency/import-cycle check for extracted slice;
- `git diff --check`.

Final minimum:

- full pytest;
- focused repository-context tests;
- Ruff check + format check;
- `tools/code_health.py check --root .`;
- deterministic symbol-map generation/validation covering new package;
- dependency/import-cycle check;
- CLI compatibility/characterization tests;
- existing baseline/manifest/live-status deterministic tests;
- `git diff --check`.

No provider/model call is required for repository-context correctness; model usage is only the Codex Executor/subagent implementation process.

## Acceptance criteria

- **AC-T053-1:** Phase 1 begins `NEW`; D042 passes before delegation/implementation.
- **AC-T053-2:** Phase 1 uses bounded fresh Explorer, Worker and independent Verifier functions; concurrency/writer limits hold.
- **AC-T053-3:** Phase-1 measurement/report/canonical-identity extraction is behavior-preserving and characterized.
- **AC-T053-4:** Phase 1 persists telemetry/handoff, closes children, returns `PARTIAL`, and honors the Orchestrator barrier.
- **AC-T053-5:** Phase 2 uses `CONTINUE` in the same root when recoverable; resume failure is reported, not disguised.
- **AC-T053-6:** Phase 2 repeats D042 and reloads current authority including `T053-P1` before using retained context.
- **AC-T053-7:** Phase 2 uses fresh children; Phase-1 children remain closed.
- **AC-T053-8:** final runtime/test facades are each `<=500` LOC; extracted modules are cohesive, bounded and acyclic; compatibility is preserved.
- **AC-T053-9:** old `1117`/`1540` ratchets are removed/lowered and relevant new modules are covered by code-health/symbol-map checks.
- **AC-T053-10:** required operational telemetry exists for both phases; unavailable token metrics are explicit, not invented.
- **AC-T053-11:** no authority leakage or Executor-authored Markdown; Git/handoffs/tests suffice for independent convergence.
- **AC-T053-12:** final deterministic verification and independent technical review are green with no unresolved in-scope finding.

## Non-goals

T053 does not authorize changing D055, Governance Core semantics, MG1/T023, building App Server/SDK persistence, adding a custom `.codex/agents/` catalog solely for the pilot, requiring subagents globally, maximizing parallelism, or persisting child trees as correctness state.

## Ownership and handoffs

ChatGPT Orchestrator owns this Task Contract, Design, Phase-1 acceptance, final convergence and any later D055/portability decision.

Executor owns authorized non-Markdown implementation/tests/config, internal Codex orchestration, technical review, telemetry/handoff JSON, and Git mechanics.

### Phase 1 handoff

Persist `handoffs/T053-phase1.json` with status `PARTIAL`, branch/base/HEAD, technical delta, characterization/verification, before/after LOC, child-role/closed-state summary, one-writer evidence, telemetry pointer and blockers.

Return only:

```text
STATUS: PARTIAL
HANDOFF: handoffs/T053-phase1.json
BRANCH: <branch>
HEAD: <pushed-head>
```

### Final handoff

Persist `handoffs/T053-executor-handoff.json` with standard evidence plus same-root/recovery result, D042 evidence for both phases, before/after LOC/module map, code-health/symbol-map/dependency results, bootstrap comparison, child spawn/close/retry summary, available root/child token/context telemetry, and final verification.

Return only standard terminal status, handoff path, branch and pushed HEAD.
