# Orchestrator Checkpoint

Checkpoint-ID: O274  
Date: 2026-09-12  
Current-Objective: T063 — adaptive worker routing requalification  
State: T063_V8_STAGE2_4_COMPLETE_STAGE5_REQUIRED  
Active-Executor: none  
Executor-Launch-State: NOT_AUTHORIZED  
Coordinator-ID: none active — prospective successor will use `AG | agent-governance | T063 | root-8` only after readiness  
Task-Contract: `docs/tasks/T063-adaptive-worker-routing-requalification.md` — v8 specification/design active; Stage 6 not authorized  
Current-Design-Review: `docs/reviews/T063-R16.md`  
Prior-Convergence-Review: `docs/reviews/T063-R15.md`  
Current-Blocker-Research: `docs/research/R024-T063-V7-NO-ROLLOUT-REATTACH-RACE.md`  
T063-V7-Evidence-HEAD: `58e396c126e363428544b163cb2aa8c7e1ac8ed6`  
T063-V7-Implementation-HEAD: `5a1769fed3f93d86cbc2e72a6cc89d7a276089d6`  
Held-Work-Unit: T062 / T023 v15 Stage 6  
Held-State: HUMAN_HOLD_R32_UNCONSUMED  
Chat-Closure: KEEP_CURRENT_CHAT

## Canonical transition

O273 accepted T063 v7 only as correctly blocked historical execution and required Stage 2 successor re-entry.

ChatGPT Orchestrator completed v8 Specify / Design / Plan & Trace in T063-R16 and materially revised the active Task Contract using the Maintainer Skill v4 template/checklist.

No provider/model call was made during this work.

## V8 specification delta

V8 preserves the complete v7 replicated calibration and changes only the same-child persistence barrier.

After exact public child correlation, the same `thread/resume` may retry for exactly two transient classes:

```text
EMPTY_ROLLOUT
ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD
```

The no-rollout class matches only when the represented thread id equals the exact correlated child being resumed.

Both classes share one ten-attempt total budget. A class transition does not reset the budget.

Every retry preserves:

```text
wait 0.2 seconds
-> exact parent loaded-residency recheck
-> identical thread/resume for same child
-> no spawn/parent replay/new provider turn
```

Wrong/missing child id, unrelated error, parent loss or exhaustion blocks fail-closed.

## Preserved v7 scientific design

V8 remains one clean homogeneous 24-arm fixed-n calibration:

```text
4 replicate blocks
3 probes per block
2 profiles per probe
= 24 scored first-attempt children
```

The v7 frozen schedule, profiles, P1/P2/P3 oracles, public parent surface, first-attempt quality semantics, 4/4 per-probe and 12/12 global quality qualification, quality-adjusted usage, 10% exact-token materiality floor and four-value pilot taxonomy are unchanged.

V1-v7 attempts are historical only and cannot enter v8 scoring.

## Stage ownership

```text
Stages 2-4 -> COMPLETE by ChatGPT Orchestrator / T063-R16
Stage 5    -> REQUIRED next / ChatGPT Orchestrator
Stage 6    -> NOT AUTHORIZED
Stage 7    -> future ChatGPT Orchestrator convergence
```

## Stage 5 requirements

Materialize a fresh v8 candidate from the post-O274 `develop` HEAD.

The candidate must:

1. promote the accepted v7 implementation substrate from `5a1769fed3f93d86cbc2e72a6cc89d7a276089d6` without v7 terminal telemetry/handoff JSON;
2. preserve inherited v3-v7 executable/test blobs except where the new v8 layer deliberately supersedes behavior;
3. add `evals/adaptive_worker_routing_v8/*` plus a v8 persistence-barrier conformance test;
4. cover exact-child no-rollout, wrong/missing id rejection, mixed no-rollout/empty-rollout success, one shared ten-attempt exhaustion, retry ordering, same-child/same-params/no-new-provider-turn and immediate nonmatching failure;
5. consume zero provider/model calls during Stage 5/readiness.

After candidate publication, perform remote delta/blob verification and provider-free static/smoke checks available to the Orchestrator.

## D077 state

R024 last verified:

```text
qualified pin:   0.153.4
stable reviewed: 0.154.0
disposition:     PIN_RETAINED
```

Readiness MUST revalidate the official stable release again after candidate publication and before any Stage 6 authorization.

## Held and frozen work

T062/T023 remains on Human hold; do not consume its old continuation authority.

T058 remains frozen by explicit Human decision; do not resume, integrate, clean or copy it without new explicit Human authorization.

R007 remains `EVALUATING`; no global adaptive worker-routing policy is adopted.

## Next Chat Minimum Load

After normal bootstrap (`develop`, `AGENTS.md`, this checkpoint):

1. for T063 Stage 5/readiness, load the active Task Contract first;
2. load T063-R16 and R024 for v8 persistence semantics;
3. load T063-R15 only when v7 execution provenance is needed;
4. load R021/R022/R023/D063/D076/D077 only for deeper implementation/provenance conflict;
5. for any material Task Contract revision/readiness review, load Maintainer Skill `TASK-CONTRACT-V4-TEMPLATE.md` and its usage reference;
6. for T062 resumption, load its separate held-line authority;
7. do not reconstruct the frontier from chat memory.

## Next Action

ChatGPT Orchestrator must complete D068 Stage 5:

1. integrate this Stage 2–4 authority into `develop` through PR;
2. create a fresh v8 candidate branch from the resulting `develop` HEAD;
3. materialize accepted v7 implementation blobs plus the new v8 adapter/tests;
4. verify candidate boundary and required conformance provider-free;
5. revalidate D077 current stable state;
6. persist a separate readiness review and exact candidate branch/HEAD/base;
7. only if readiness passes, advance to `AUTHORIZED_AWAITING_HUMAN_START` and present D055 launch information separately from thin transport.

No provider/model execution and no Codex Human launch is authorized at O274.