# Orchestrator Checkpoint

Checkpoint-ID: O269  
Date: 2026-09-11  
Current-Objective: T063 — adaptive worker routing requalification  
State: T063_V6_STAGE6_AUTHORIZED_AWAITING_HUMAN_START  
Active-Executor: none — Codex selected for pending Human launch  
Executor-Launch-State: AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Coordinator-ID: `AG | agent-governance | T063 | root-6` — reserved NEW same-work-unit failover root; not yet started  
Task-Contract: `docs/tasks/T063-adaptive-worker-routing-requalification.md`  
Current-Launch-Review: `docs/reviews/T063-R11.md`  
Current-Research: `docs/research/R023-T063-V5-LIVE-SPAWN-RECEIPT-PERSISTENCE-GAP.md`  
T063-V6-Candidate-Branch: `test/t063-adaptive-worker-routing-requalification-v6`  
T063-V6-Candidate-HEAD: `af2de380569285b63e33de3f53628cadcf4052b6`  
T063-V6-Candidate-Base: `d5ff447d3ad162ddfc8afd8baadeac67154d7a6a`  
Historical-T063-V5-Evidence-HEAD: `3f9830a65a152ad595653961205e0ca52b9c5ccc`  
Historical-T063-V4-Evidence-HEAD: `4135a13ce8daa4f6b1fcabe45063364fbbdd16f1`  
Historical-T063-V3-Evidence-HEAD: `746519abc6f159e959120f68d5c9f920d88d5797`  
Historical-T063-V2-Evidence-HEAD: `3ff745a8d29e031ca818c1bc618b15a54e0cbf2b`  
Historical-T063-V1-Evidence-HEAD: `3d8a9460988351383a90adfc6b76e2deff056504`  
Held-Work-Unit: T062 / T023 v15 Stage 6  
Held-State: HUMAN_HOLD_R32_UNCONSUMED  
Chat-Closure: KEEP_CURRENT_CHAT

## Canonical transition

V5 was converged at O268 as `BLOCKED_EXECUTION_INVALID / EXECUTION_VALIDITY` with no model-quality evidence. R023/T063-R10 established that the blocker came from the v5 adapter requiring a public live `subAgentActivity(kind=Started)` receipt to be duplicated in the completed parent-turn snapshot even though the live exact-child correlation had already succeeded.

ChatGPT Orchestrator re-entered Stage 5 and materialized a clean v6 successor from protected-base snapshot `d5ff447d3ad162ddfc8afd8baadeac67154d7a6a`.

Authorized v6 candidate:

```text
branch: test/t063-adaptive-worker-routing-requalification-v6
HEAD:   af2de380569285b63e33de3f53628cadcf4052b6
base:   d5ff447d3ad162ddfc8afd8baadeac67154d7a6a
```

Remote comparison shows the candidate is exactly one commit ahead of its base. It promotes the accepted v3/v4/v5 executable/test package without historical v5 telemetry/handoff evidence and adds only the v6 adapter package plus deterministic v6 parent-surface regression coverage.

## V6 parent-surface correction

V6 preserves the existing public `subAgentActivity` correlation and changes only how parent-surface cardinality/safety are validated.

For the exact parent thread/turn, public live `item/started` and `item/completed` notifications are captured from immediately before parent `turn/start`.

Started `subAgentActivity` representations are deduplicated by public item ID. A valid parent surface requires exactly one unique Started logical item matching the exact correlated child and frozen expected task name, no second/different Started activity, no conflicting duplicate representation, and no forbidden parent tool/item activity.

The completed parent turn still must have the exact turn identity, final `PARENT_SPAWNED` text and no contradictory/forbidden represented activity. It no longer needs to duplicate the already-observed live Started item.

Internal/raw response events remain excluded.

## Preserved scientific semantics

V6 preserves:

- frozen P1/P2/P3 probes and semantic oracles;
- frozen task messages;
- frozen arm order and compute matrix;
- config-authoritative child task/profile;
- D063 exact read-only/identity/usage/duration/reroute receipts;
- v4 exact same-child empty-rollout reattachment barrier;
- first-attempt scoring;
- v5 model-quality/efficiency eligibility taxonomy;
- D076 materialization boundary;
- exclusion of historical v1-v5 evidence from v6 scoring.

Historical evidence remains:

```text
v1  3d8a9460988351383a90adfc6b76e2deff056504
v2  3ff745a8d29e031ca818c1bc618b15a54e0cbf2b
v3  746519abc6f159e959120f68d5c9f920d88d5797
v4  4135a13ce8daa4f6b1fcabe45063364fbbdd16f1
v5  3f9830a65a152ad595653961205e0ca52b9c5ccc
```

No historical attempt may enter v6 scoring.

## Verification status

Remote structural review completed:

```text
v6 branch identity:                    VERIFIED
v6 exact base ancestry:                VERIFIED
candidate diff boundary:               VERIFIED
v3/v4/v5 promoted blob reuse:          VERIFIED BY CONSTRUCTION/REMOTE BLOB IDS
v6 parent-surface adapter present:      VERIFIED
v6 deterministic regression test:      VERIFIED
new v6 Python AST parse:                PASS
```

The Orchestrator attempted a fresh local clone of the v6 branch, but the sandbox again could not resolve `github.com`. Therefore no local pytest, Ruff or compileall PASS is claimed.

Stage 6 MUST execute every deterministic/provider-free test/compile/lint/preflight gate successfully before the first provider/model call. Any failure blocks with zero new scored calls.

No provider/model call was consumed during v6 Stage 5/readiness work.

## D077 state

Launch-readiness upstream revalidation on 2026-09-11 found:

```text
qualified pin:              0.153.4
latest stable:              0.154.0
newest observed prerelease: 0.155.0-alpha.3.9
newer stable than 0.154.0:  none
D077 disposition:           PIN_RETAINED
```

R023 established that 0.154.0 retains the relevant live-item/history persistence distinction and does not remove the v5 blocker. D063 qualification is not extended to 0.154.0.

If a stable release newer than `0.154.0` appears before the first v6 provider call, STOP and return to Orchestrator for relevance classification.

## Coordinator continuity

V5 `root-5` is retired after the consumed blocked run and material adapter/Task Contract revision.

V6 uses NEW failover root:

```text
AG | agent-governance | T063 | root-6
```

This is a D060 same-work-unit failover, not a concurrent second root.

## Launch profile

Current D055 Human-facing launch card:

```text
Executor:        Codex
Surface:         Codex Desktop / native Windows
Session:         NEW
Coordinator-ID:  AG | agent-governance | T063 | root-6
Root model:      gpt-5.6-sol
Root reasoning:  medium
Codex runtime:   exactly 0.153.4
App Server:      exactly 0.153.4
Auth category:   chatgpt
```

The launch profile is separate from Task semantics and remains separate from the thin transport prompt.

## Held and frozen work

T062/T023 remains on Human hold exactly as previously recorded. Do not execute its old continuation authority without new Human selection and revalidation.

T058 remains frozen by explicit Human decision. Do not resume, integrate, clean or copy it without new explicit Human authorization.

R007 remains `EVALUATING`; no global adaptive worker-routing policy is adopted.

## Next Chat Minimum Load

After normal bootstrap (`develop`, `AGENTS.md`, this checkpoint):

1. for T063 launch/convergence, load `docs/tasks/T063-adaptive-worker-routing-requalification.md` first;
2. load `docs/reviews/T063-R11.md` for v6 readiness rationale;
3. load R023/R022/R021/D063/D076/D077 only when the Task Contract references require deeper interpretation or a concrete conflict arises;
4. for creation/material revision/readiness review of any source-product Task Contract, load the Maintainer Skill v4 template + usage reference;
5. for T062 resumption, load its separate held-line authority instead;
6. do not reconstruct frontiers from prior chat/Project Memory.

## Next Action

Before Human-mediated v6 launch:

1. revalidate `develop` and exact v6 candidate HEAD;
2. revalidate that no stable Codex release newer than `0.154.0` has appeared;
3. present the D055 launch card separately;
4. give the Human only the thin transport prompt defined by the canonical T063 Task Contract.

ChatGPT MUST NOT start or directly control Codex under D071.

After the Human returns the Task Contract-defined terminal four-line result, ChatGPT performs remote verification and Stage 7 convergence.
