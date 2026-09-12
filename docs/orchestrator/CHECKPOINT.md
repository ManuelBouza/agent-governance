# Orchestrator Checkpoint

Checkpoint-ID: O275  
Date: 2026-09-12  
Current-Objective: T063 — adaptive worker routing requalification  
State: T063_V8_STAGE6_AUTHORIZED_AWAITING_HUMAN_START  
Active-Executor: none — Codex selected for pending Human launch  
Executor-Launch-State: AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Coordinator-ID: `AG | agent-governance | T063 | root-8` — reserved NEW same-work-unit successor root; not yet started  
Task-Contract: `docs/tasks/T063-adaptive-worker-routing-requalification.md`  
Current-Design-Review: `docs/reviews/T063-R16.md`  
Current-Launch-Review: `docs/reviews/T063-R17.md`  
Prior-Convergence-Review: `docs/reviews/T063-R15.md`  
Current-Blocker-Research: `docs/research/R024-T063-V7-NO-ROLLOUT-REATTACH-RACE.md`  
T063-V8-Candidate-Branch: `test/t063-adaptive-worker-routing-requalification-v8`  
T063-V8-Candidate-HEAD: `83f38bd9813cfdd107486ad40d39df6335513ce8`  
T063-V8-Candidate-Base: `621e9ae0d73378b1013699e8726b315128c95891`  
T063-V7-Evidence-HEAD: `58e396c126e363428544b163cb2aa8c7e1ac8ed6`  
T063-V7-Implementation-HEAD: `5a1769fed3f93d86cbc2e72a6cc89d7a276089d6`  
Held-Work-Unit: T062 / T023 v15 Stage 6  
Held-State: HUMAN_HOLD_R32_UNCONSUMED  
Chat-Closure: KEEP_CURRENT_CHAT

## Canonical transition

O274 completed v8 Specify / Design / Plan & Trace and required D068 Stage 5 materialization.

ChatGPT Orchestrator then materialized and remotely reviewed the exact v8 candidate:

```text
branch: test/t063-adaptive-worker-routing-requalification-v8
HEAD:   83f38bd9813cfdd107486ad40d39df6335513ce8
base:   621e9ae0d73378b1013699e8726b315128c95891
```

The candidate is exactly one commit above its protected-base snapshot and adds exactly 28 executable/test files:

```text
24 accepted v3-v7 package/test blobs
+ 4 new v8 adapter/test files
```

The accepted v3-v7 blobs come from v7 implementation HEAD `5a1769fed3f93d86cbc2e72a6cc89d7a276089d6`. V7 terminal telemetry/handoff JSON is not promoted.

T063-R17 accepted Stage 5 readiness and authorized this exact candidate for Human-mediated Stage 6.

No provider/model call was consumed during v8 Stage 2–5/readiness.

## V8 experiment semantics

V8 preserves the v7 fixed-n replicated qualification calibration:

```text
4 replicate blocks
3 frozen probes per block
2 profiles per probe
= 24 scored first-attempt children
```

Frozen root:

```text
gpt-5.6-sol / medium
```

Frozen child profiles:

```text
P1 ADAPTIVE  gpt-5.6-luna  / medium
P1 CONTROL   gpt-5.6-sol   / medium
P2 ADAPTIVE  gpt-5.6-terra / medium
P2 CONTROL   gpt-5.6-sol   / medium
P3 ADAPTIVE  gpt-5.6-terra / high
P3 CONTROL   gpt-5.6-sol   / medium
```

The 24-arm counterbalanced schedule, v6-qualified public parent surface, P1/P2/P3 oracle semantics, valid-quality-failure continuation, 4/4 per-probe and 12/12 global quality rules, quality-adjusted usage, 10% exact-token materiality floor and four-value pilot taxonomy remain unchanged.

V1-v7 attempts are historical only and cannot enter v8 scoring.

## V8 persistence correction

After exact public child correlation, same-child `thread/resume` may retry only two exact transient classes:

```text
EMPTY_ROLLOUT
ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD
```

The no-rollout class is accepted only when the represented thread id equals the exact resumed child id.

Both classes share one maximum of ten total resume attempts. The budget does not reset across a mixed sequence.

Every retry must preserve:

```text
wait 0.2 seconds
-> exact parent loaded-residency recheck
-> identical thread/resume params for same child
-> no spawn/parent replay/new provider turn
```

Wrong/missing child id, unrelated error, parent loss or exhaustion blocks fail-closed.

## Stage 5 verification/readiness

Orchestrator verification completed without provider/model calls:

```text
candidate/base ancestry:          VERIFIED REMOTELY
candidate commit count:           1
candidate delta boundary:         VERIFIED — 28 files
accepted v3-v7 blob reuse:        VERIFIED BY EXACT BLOB IDS
v7 terminal JSON excluded:        VERIFIED
v8 source/conformance inspection: PASS against R16/R024
GitHub automatic CI statuses:     none
```

The Orchestrator does not claim repository-native pytest, Ruff or compileall PASS for v8. Stage 6 on native Windows MUST run all required deterministic tests, compile, lint, oracle and environment gates before the first provider/model call. A gate failure blocks with zero scored provider calls.

## D077 state

Post-candidate official release revalidation found:

```text
qualified pin:              0.153.4
latest stable:              0.154.0
latest stable tag:          rust-v0.154.0
newer stable than 0.154.0:  none
disposition:                PIN_RETAINED
```

R024 established that 0.154.0 retains the relevant no-rollout persisted-read path. D063 remains qualified specifically on `0.153.4`; v8 therefore retains exactly Codex/App Server `0.153.4`.

If a stable release newer than `0.154.0` appears before the first provider call, STOP for D077 relevance classification.

## Coordinator continuity

V7 `root-7` is retired after its consumed blocked run and material successor revision.

V8 uses NEW same-work-unit successor root:

```text
AG | agent-governance | T063 | root-8
```

This is not a concurrent second root.

## Launch profile

Current D055 Human-facing launch card:

```text
Executor:        Codex
Surface:         Codex Desktop / native Windows
Session:         NEW
Coordinator-ID:  AG | agent-governance | T063 | root-8
Root model:      gpt-5.6-sol
Root reasoning:  medium
Codex runtime:   exactly 0.153.4
App Server:      exactly 0.153.4
Auth category:   chatgpt
```

The launch profile is separate from the Task Contract semantics and separate from the thin transport prompt.

## Held and frozen work

T062/T023 remains on Human hold exactly as previously recorded. Do not execute its old continuation authority without new Human selection and revalidation.

T058 remains frozen by explicit Human decision. Do not resume, integrate, clean or copy it without new explicit Human authorization.

R007 remains `EVALUATING`; no global adaptive worker-routing policy is adopted.

## Next Chat Minimum Load

After normal bootstrap (`develop`, `AGENTS.md`, this checkpoint):

1. for T063 launch/convergence, load the active Task Contract first;
2. load `docs/reviews/T063-R17.md` for v8 readiness rationale;
3. load R16/R024 when persistence design needs deeper interpretation;
4. load R15/R021/R022/R023/D063/D076/D077 only when provenance, implementation detail or a concrete conflict requires them;
5. for material Task Contract revision/readiness review, load Maintainer Skill v4 template + usage reference;
6. for T062 resumption, load its separate held-line authority;
7. do not reconstruct the frontier from prior chat/Project Memory.

## Next Action

Before Human-mediated v8 launch:

1. revalidate `develop` and exact v8 candidate HEAD;
2. revalidate that no stable Codex release newer than `0.154.0` has appeared;
3. present the D055 launch card separately;
4. give the Human only the thin transport prompt defined by the canonical T063 Task Contract.

ChatGPT MUST NOT start or directly control Codex.

After the Human returns the Task Contract-defined terminal four-line result, ChatGPT performs remote verification and Stage 7 convergence.