# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O195  
Canonical-Branch: `develop`  
Current-Work-Unit: T053 Codex Persistent Executor Coordinator Pilot is integrated and ready for Phase 1; MG1 remains in Explore/Specify with no V13 authorization  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: ChatGPT Orchestrator

## Durable frontier

- D041, D042, D053, D054, D055 and D056 remain controlling. Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`.
- T050 is `ACCEPTED`; code-health/symbol-map boundary remains active.
- T023/MG1-v12 is closed as valid `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE`; review `docs/reviews/T023-R11.md`; evidence integration PR `#266`, merge `2abc33ad954dbca81975b653bc0a607abdd32f8f`.
- No MG1-v13 is authorized. MG1 remains in Orchestrator Explore/Specify on the near-miss overactivation design problem.
- Persistent-coordinator research: `docs/research/CODEX-PERSISTENT-EXECUTOR-COORDINATOR-RESEARCH.md`; PR `#265`, merge `91f62278e439be8f5eb7e50c3f6aaac9331fa99e`.
- T053 Task Contract: `docs/tasks/T053-codex-persistent-executor-coordinator-pilot.md`.
- T053 planning PR `#268`; merge `a6af47bedc843a6f1d7f834a32894fdc7539181c`.
- D055 is unchanged by T053.

## MG1 boundary

V12 established a valid execution method and a substantive candidate result:

```text
B0 -> FUTILE_QUALIFICATION
B1 -> FUTILE_QUALIFICATION
F2 -> NOT_SCHEDULED_NO_REFERENCE
G3 -> NOT_SCHEDULED_NO_REFERENCE
selected topology -> none
```

Both reference families had one false activation across the fixed `11` negative/near-miss denominator, making the best possible final rate `1/11 = 0.090909... > 0.05`.

Do not rerun V12, relax thresholds, execute challengers outside D050, or create V13 without new upstream MG1 Design/Plan authority and a fresh holdout boundary.

## T053 purpose

T053 is a measured source-product pilot of this execution topology:

```text
one Human-visible persistent Codex coordinator root
        |
        +-- fresh bounded Explorer child(ren)
        +-- one fresh primary Worker writer
        +-- fresh independent Verifier/Reviewer
        |
        +-- concise summaries/evidence references only
```

Git remains authoritative. The root is execution cache only; children are disposable D041 implementation mechanics.

The useful technical deliverable is a behavior-preserving modular refactor of the oversized `repository_context` subsystem:

```text
tools/repository_context.py       1117 LOC grandfathered
tests/test_repository_context.py  1540 LOC grandfathered
```

Final T053 targets include facade/test files `<=500` LOC, focused extracted modules, reduced ratchets, code-health/symbol-map coverage and acyclic dependencies.

## T053 continuity experiment

T053 deliberately keeps current D055 unchanged.

### Phase 1

Human-visible root:

```text
Executor: Codex
Session: NEW
Model: GPT-5.6 Sol
Effort: High
```

Phase 1 must:

1. satisfy D042 and reload current Git authority;
2. start pilot telemetry;
3. use at least two fresh read-only bounded explorations for runtime/dependency and test/compatibility mapping;
4. close explorers after concise summaries;
5. establish/strengthen characterization as needed;
6. use one fresh Worker as sole writer for the tracked-file measurement/report + canonical-identity extraction slice;
7. run focused deterministic verification;
8. use a fresh read-only independent Verifier/Reviewer;
9. close all children;
10. persist/push `handoffs/T053-phase1.json` and `handoffs/T053-pilot-telemetry.json`;
11. return `STATUS: PARTIAL` and stop.

Expected branch: `refactor/t053-repository-context-coordinator-pilot` or collision-safe equivalent.

Phase 1 MUST NOT automatically continue into Phase 2.

### Orchestrator barrier

Orchestrator independently converges the Phase-1 remote state. If accepted, persist `docs/reviews/T053-P1.md` and integrate it to `develop`.

Only that persisted acceptance authorizes Phase 2.

### Phase 2

If Phase 1 is accepted and the original coordinator root is recoverable:

```text
Executor: Codex
Session: CONTINUE
Model/Effort: selected under D055 for remaining risk
```

The same root must repeat D042, reload current `AGENTS.md`, checkpoint, T053 and `T053-P1`, reconcile retained assumptions against Git, and use **fresh** children. Phase-1 children must not be resumed.

If the same root cannot be continued, report `COORDINATOR_RESUME_UNAVAILABLE`; do not silently substitute a fresh root and count the continuity hypothesis as successful.

## T053 child/worktree safety

- maximum `3` concurrently open children in the pilot;
- parallel read-only exploration is allowed when independent;
- maximum one write-capable actor per mutable worktree at any instant;
- normally one Worker is the writer;
- if the root edits technical files, no write-capable child may concurrently mutate the worktree;
- multiple write worktrees are outside Phase-1/Phase-2 pilot scope;
- completed children are closed after concise result transfer;
- child transcripts/private reasoning are not Governance authority and are not required handoff artifacts.

## Pilot telemetry

T053 persists `handoffs/T053-pilot-telemetry.json`, separated by phase.

Required operational evidence includes:

- launch mode and D042 result;
- canonical authority revisions;
- phase timing and time-to-first-useful-action when observable;
- child roles/purposes/read-write status/retries/closed state;
- max child concurrency and simultaneous writer count;
- stale-authority corrections;
- branch/worktree incidents;
- compaction events if observable;
- root-continuation evidence/fingerprint if safely exposed;
- verification/rework outcome;
- concise bootstrap/orientation inventory.

Root/child token/context metrics are best effort. If the supported host does not expose a metric, persist `null` plus reason; do not estimate or mine private reasoning/transcripts.

The post-pilot Orchestrator decision asks whether root persistence reduced repeated orientation or improved context locality at acceptable total compute and equal-or-better quality. Fewer sessions alone is not success.

## T053 phase-1 executable identity

```text
Task: T053
Status: READY / PHASE 1
Task Contract: docs/tasks/T053-codex-persistent-executor-coordinator-pilot.md
Expected handoff: handoffs/T053-phase1.json
Pilot telemetry: handoffs/T053-pilot-telemetry.json
Expected status: PARTIAL
Expected branch: refactor/t053-repository-context-coordinator-pilot
Executor: Codex
Session: NEW
Model: GPT-5.6 Sol
Effort: High
```

Rationale for High: Phase 1 combines a behavior-preserving refactor of a >1k LOC source tool, characterization preservation, native subagent coordination and a new execution-topology pilot. Increased reasoning does not replace persisted Design/Plan authority.

## Next action

1. Refresh canonical `develop` immediately before Human launch.
2. Show D055 exactly: Codex / NEW / GPT-5.6 Sol / High.
3. Launch only `docs/tasks/T053-codex-persistent-executor-coordinator-pilot.md` using pointer-only transport.
4. Executor performs **Phase 1 only** and returns `PARTIAL` with pushed remote evidence.
5. Orchestrator converges Phase 1 independently before any continuation.
6. Do not create or change D055 policy during Phase 1.
7. Do not launch MG1-v13 while T053 is executing.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not treat coordinator memory as authority; do not bypass D042; do not reuse Phase-1 children in Phase 2; do not permit overlapping writers on one worktree; do not build App Server/SDK persistence in T053; do not add a custom `.codex/agents/` catalog solely for the pilot; do not change D055 before measured evidence; do not write directly to `main`/`develop`; do not rerun MG1-v12 or launch V13.
