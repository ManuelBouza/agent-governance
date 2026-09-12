# Orchestrator Checkpoint

Checkpoint-ID: O277  
Date: 2026-09-12  
Current-Objective: T063 — adaptive worker routing requalification  
State: T063_V8_HARDENED_STAGE6_AUTHORIZED_AWAITING_HUMAN_START  
Active-Executor: none — Codex selected for pending Human launch  
Executor-Launch-State: AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Coordinator-ID: `AG | agent-governance | T063 | root-8` — reserved NEW same-work-unit successor root; not yet started  
Task-Contract: `docs/tasks/T063-adaptive-worker-routing-requalification.md`  
Current-Design-Review: `docs/reviews/T063-R16.md`  
Current-Launch-Review: `docs/reviews/T063-R19.md`  
Prior-Readiness-Revocation: `docs/reviews/T063-R18.md`  
Withdrawn-Launch-Review: `docs/reviews/T063-R17.md`  
Current-Research: `docs/research/R025-T063-V8-REATTACH-CLASSIFIER-HARDENING.md`  
T063-V8-Candidate-Branch: `test/t063-adaptive-worker-routing-requalification-v8`  
T063-V8-Candidate-HEAD: `afdae0050226d61a10269f63017e2fac99eef644`  
T063-V8-Candidate-Base: `8b3cc5af3e70367eff6e55ebd416a554c8096763`  
Withdrawn-V8-Candidate-HEAD: `83f38bd9813cfdd107486ad40d39df6335513ce8`  
T063-V7-Evidence-HEAD: `58e396c126e363428544b163cb2aa8c7e1ac8ed6`  
T063-V7-Implementation-HEAD: `5a1769fed3f93d86cbc2e72a6cc89d7a276089d6`  
Held-Work-Unit: T062 / T023 v15 Stage 6  
Held-State: HUMAN_HOLD_R32_UNCONSUMED  
Chat-Closure: KEEP_CURRENT_CHAT

## Canonical transition

O276 revoked the provisional O275 authorization after R025 established that candidate `83f38bd...` did not structurally constrain the represented no-rollout JSON-RPC error tightly enough.

ChatGPT Orchestrator then completed D068 Stage 5 hardening and published a fresh exact candidate from the protected O276 base:

```text
branch: test/t063-adaptive-worker-routing-requalification-v8
HEAD:   afdae0050226d61a10269f63017e2fac99eef644
base:   8b3cc5af3e70367eff6e55ebd416a554c8096763
```

The candidate is exactly one commit above the protected base and adds exactly 28 executable/test files:

```text
24 accepted v3-v7 package/test blobs
+ 4 hardened v8 adapter/test files
```

No historical terminal telemetry/handoff JSON is promoted.

T063-R19 accepts this hardened candidate for Human-mediated Stage 6. The withdrawn candidate `83f38bd...` remains prohibited launch authority.

No v8 provider/model call has been consumed.

## Hardened v8 persistence correction

After exact public child correlation, same-child `thread/resume` may retry only two accepted availability conditions:

```text
EMPTY_ROLLOUT
ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD
```

The no-rollout condition is accepted only when the flattened `AppServerError` safely parses as a mapping and satisfies exactly:

```text
method prefix == "thread/resume failed: "
code type     == int
code          == -32600
message       == "no rollout found for thread id <exact child id>"
```

The published implementation uses `ast.literal_eval`, not `eval`.

Wrong code, `bool`, message drift, malformed/non-mapping payload, wrong method prefix, wrong/missing child ID or unrelated `-32600` error is nonmatching and blocks fail-closed.

Both accepted conditions share one maximum of ten total resume attempts. The budget does not reset across a mixed sequence.

Every retry preserves:

```text
wait 0.2 seconds
-> exact parent loaded-residency recheck
-> identical thread/resume params object
-> same exact child
-> no spawn/parent replay/replacement/provider quality turn
```

Exhaustion is a persistence/materialization blocker and does not prove that the original no-rollout state was transient.

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

The counterbalanced schedule, v6 public parent surface, P1/P2/P3 oracle semantics, valid-quality-failure continuation, 4/4 per-probe and 12/12 global quality rules, quality-adjusted usage, 10% exact-token materiality floor and four-value pilot taxonomy remain unchanged.

V1-v7 attempts are historical only and cannot enter v8 scoring.

## Stage 5 verification/readiness

Orchestrator verification completed without provider/model calls:

```text
candidate/base ancestry:             VERIFIED REMOTELY
candidate commit count:              1
candidate delta boundary:            VERIFIED — 28 files
accepted v3-v7 blob reuse:           VERIFIED BY EXACT BLOB IDS USED IN TREE
hardened runner blob:                bf5e5dc012b9bf81906b31177ed92c5e319d6858
hardened test blob:                  b9851ca572286dce8d137c1fdf5b8bb0dd7dbfe2
new runner AST parse:                PASS
new test AST parse:                  PASS
structured-classifier smoke matrix:  PASS
GitHub automatic CI statuses:        none
```

The Orchestrator container could not resolve `github.com` for a full local checkout, so this checkpoint does **not** claim repository-native pytest, Ruff or compileall PASS.

Stage 6 on native Windows MUST run all deterministic/provider-free tests, compile, lint, oracle and environment gates before the first provider/model call. Any gate failure blocks with zero new scored provider calls.

## D076 state

The structured classifier and negative conformance suite are material Stage 5 behavior and are now present in the candidate. Stage 6 may not broaden or weaken their semantics.

## D077 state

Post-candidate official release revalidation found:

```text
qualified pin:              0.153.4
latest stable:              0.154.0
latest stable tag:          rust-v0.154.0
latest stable published:    2026-09-09
newer stable than 0.154.0:  none
version disposition:        PIN_RETAINED
```

R025 confirms reviewed later source retains the relevant rollout-resolution architecture. D063 remains qualified specifically on 0.153.4; v8 retains exactly Codex/App Server `0.153.4`.

If a stable release newer than `0.154.0` appears before the first provider call, STOP for D077 relevance classification.

## Coordinator continuity

`AG | agent-governance | T063 | root-8` was reserved under the withdrawn launch but never started. It remains the correct NEW same-work-unit coordinator root for hardened v8.

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

The launch profile is separate from the thin transport prompt.

## Held and frozen work

T062/T023 remains on Human hold exactly as previously recorded. Do not execute its old continuation authority without new Human selection and revalidation.

T058 remains frozen by explicit Human decision. Do not resume, integrate, clean or copy it without new explicit Human authorization.

R007 remains `EVALUATING`; no global adaptive worker-routing policy is adopted.

## Next Chat Minimum Load

After normal bootstrap (`develop`, `AGENTS.md`, this checkpoint):

1. for T063 launch/convergence, load the active Task Contract first;
2. load `docs/reviews/T063-R19.md` for hardened-v8 readiness;
3. load R025/R18 when classifier/revocation provenance is needed;
4. load R16/R024/R022/D063/D076/D077 only when deeper design, receipt, materialization or version interpretation is required;
5. for material Task Contract revision/readiness, load Maintainer Skill v4 template + usage reference;
6. for T062 resumption, load its separate held-line authority;
7. do not reconstruct the frontier from prior chat/Project Memory.

## Next Action

Before Human-mediated hardened-v8 launch:

1. revalidate `develop` and exact candidate HEAD `afdae0050226d61a10269f63017e2fac99eef644`;
2. revalidate that no stable Codex release newer than `0.154.0` has appeared;
3. present the D055 launch card separately;
4. give the Human only the thin transport prompt defined by the canonical T063 Task Contract.

ChatGPT MUST NOT start or directly control Codex.

After the Human returns the Task Contract-defined terminal four-line result, ChatGPT performs remote verification and Stage 7 convergence.
