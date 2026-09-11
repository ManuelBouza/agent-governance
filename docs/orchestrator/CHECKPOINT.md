# Orchestrator Checkpoint

Checkpoint-ID: O267  
Date: 2026-09-11  
Current-Objective: T063 — adaptive worker routing requalification  
State: T063_V5_STAGE6_AUTHORIZED_AWAITING_HUMAN_START  
Active-Executor: none — Codex selected for pending Human launch  
Executor-Launch-State: AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Coordinator-ID: `AG | agent-governance | T063 | root-5` — reserved NEW same-work-unit failover root; not yet started  
Task-Contract: `docs/tasks/T063-adaptive-worker-routing-requalification.md`  
Current-Launch-Review: `docs/reviews/T063-R9.md`  
T063-V5-Candidate-Branch: `test/t063-adaptive-worker-routing-requalification-v5`  
T063-V5-Candidate-HEAD: `94b5ec6dcf0d094c1a90f84b08e7ce1de483716f`  
T063-V5-Candidate-Base: `b71cc3b23bedb2c3e361207497ebd96f1dc59e49`  
Historical-T063-V4-Evidence-HEAD: `4135a13ce8daa4f6b1fcabe45063364fbbdd16f1`  
Historical-T063-V3-Evidence-HEAD: `746519abc6f159e959120f68d5c9f920d88d5797`  
Historical-T063-V2-Evidence-HEAD: `3ff745a8d29e031ca818c1bc618b15a54e0cbf2b`  
Historical-T063-V1-Evidence-HEAD: `3d8a9460988351383a90adfc6b76e2deff056504`  
Held-Work-Unit: T062 / T023 v15 Stage 6  
Held-State: HUMAN_HOLD_R32_UNCONSUMED  
Chat-Closure: KEEP_CURRENT_CHAT

## Canonical transition

V4 executed from its authorized candidate and consumed one parent turn/one child attempt before blocking on the already-known empty-rollout reattachment race. The live runtime returned `thread-store internal error`; the published adapter incorrectly required the non-contiguous phrase `thread-store error`, so the authorized same-child retry barrier was not entered.

The Executor made a bounded represented Stage 6 repair limited to the v4 adapter and its regression test, changing the classifier marker to `thread-store` while preserving every other empty-rollout marker and the same-child/no-new-provider-turn invariant. Provider-free post-repair verification passed in the v4 environment and no provider call occurred after the repair.

ChatGPT Orchestrator accepted that repair, but the consumed v4 attempt remains historical and unscored. V4 produced no valid scored child and no pilot decision. The block is measurement-adapter evidence, not worker-quality or root-model-quality evidence.

ChatGPT then re-entered Stage 5 and materialized a clean v5 successor that:

1. promotes the repaired v4 adapter/tests byte-for-byte;
2. preserves the frozen v3 probes, oracles, task messages, arm order and compute matrix;
3. adds explicit per-child and run-level model-evidence eligibility semantics;
4. prevents blocked/unscored attempts from being represented as model-quality evidence;
5. treats valid worker-quality FAILs as quality evidence but not quality-preserving efficiency evidence.

## Scientific candidate

Authorized v5 candidate:

```text
branch: test/t063-adaptive-worker-routing-requalification-v5
HEAD:   94b5ec6dcf0d094c1a90f84b08e7ce1de483716f
base:   b71cc3b23bedb2c3e361207497ebd96f1dc59e49
```

The candidate is three commits ahead of its exact base. Its diff is limited to the published v3 evaluation package, repaired v4 adapter/tests and v5 evidence-attribution adapter/tests.

The repaired v4 blobs in v5 exactly match terminal v4:

```text
evals/adaptive_worker_routing_v4/runner.py
  9d1703dbe9c6fc0000112da2c9775f6e3c76b8d8

tests/test_t063_adaptive_worker_routing_v4_adapter.py
  e1cc19f22cddcbf1c73e89c1cb1e85fcc4206cb6
```

Historical v1/v2/v3/v4 results are excluded from v5 scoring.

## Verification status

The Orchestrator attempted to create an exact local checkout for provider-free execution, but the sandbox could not resolve `github.com`. No local deterministic execution result is claimed.

Stage 6 therefore MUST run the candidate's deterministic/provider-free test, compile and lint gates before its first provider/model call. Any failure blocks with zero new scored calls.

Remote structural review completed:

```text
v5 branch identity:          VERIFIED
v5 base ancestry:            VERIFIED
candidate diff boundary:     VERIFIED
repaired v4 blob identity:   VERIFIED
v5 evidence tests present:   VERIFIED
```

## Model-evidence invariant

Only fully measured entries in `scored_children` are valid model-quality evidence. A valid FAIL remains first-attempt worker-quality evidence. Only PASS children are eligible as quality-preserving efficiency observations.

A partial or blocked run is not a matched CONTROL/ADAPTIVE comparison and cannot yield a pilot decision. An unscored provider attempt is not converted into model-quality evidence merely because it consumed provider work.

Run-level blockers are classified separately as profile resolution, measurement surface, measurement adapter, execution validity or unclassified execution. Unknown execution-invalid states are not overclaimed as infrastructure failures.

## D077 state

Launch-time upstream revalidation on 2026-09-11 found:

```text
qualified pin:              0.153.4
latest stable:              0.154.0
newest observed prerelease: 0.155.0-alpha.3.9
newer stable than 0.154.0:  none
D077 disposition:           PIN_RETAINED
```

If a stable release newer than `0.154.0` appears before the first v5 provider call, STOP and return to Orchestrator for relevance classification.

## Coordinator continuity

V4 `root-4` is retired after a consumed blocked run plus material adapter/Task Contract revision. V5 uses NEW failover root:

```text
AG | agent-governance | T063 | root-5
```

This is a D060 failover due contaminated execution context/adapter migration, not a concurrent second root.

## Launch profile

Current D055 Human-facing launch card:

```text
Executor:        Codex
Surface:         Codex Desktop / native Windows
Session:         NEW
Coordinator-ID:  AG | agent-governance | T063 | root-5
Root model:      gpt-5.6-sol
Root reasoning:  medium
Codex runtime:   exactly 0.153.4
App Server:      exactly 0.153.4
Auth category:   chatgpt
```

The launch profile is not Task semantics and remains separate from the thin transport prompt.

## Held and frozen work

T062/T023 remains on Human hold exactly as previously recorded. Do not execute its old continuation authority without new Human selection and revalidation.

T058 remains frozen by explicit Human decision. Do not resume, integrate, clean or copy it without new explicit Human authorization.

R007 remains `EVALUATING`; no global adaptive worker-routing policy is adopted.

## Next Chat Minimum Load

After normal bootstrap (`develop`, `AGENTS.md`, this checkpoint):

1. for T063 launch/convergence, load `docs/tasks/T063-adaptive-worker-routing-requalification.md` first;
2. load `docs/reviews/T063-R9.md` only for v4 convergence/v5 authorization rationale;
3. load R022/R021/D063/D076/D077 only when the Task Contract references require deeper interpretation or a concrete conflict arises;
4. for creation/material revision/readiness review of any source-product Task Contract, load the Maintainer Skill v4 template + usage reference;
5. for T062 resumption, load its separate held-line authority instead;
6. do not reconstruct frontiers from prior chat/Project Memory.

## Next Action

Before Human-mediated v5 launch:

1. revalidate `develop` and exact v5 candidate HEAD;
2. revalidate that no stable Codex release newer than `0.154.0` has appeared;
3. present the D055 launch card separately;
4. give the Human only the thin transport prompt defined by the canonical T063 Task Contract.

ChatGPT MUST NOT start or directly control Codex under D071.

After the Human returns the Task Contract-defined terminal four-line result, ChatGPT performs remote verification and Stage 7 convergence.
