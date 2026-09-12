# Orchestrator Checkpoint

Checkpoint-ID: O276  
Date: 2026-09-12  
Current-Objective: T063 — adaptive worker routing requalification  
State: T063_V8_READINESS_REVOKED_STAGE5_HARDENING_REQUIRED  
Active-Executor: none  
Executor-Launch-State: NOT_AUTHORIZED  
Coordinator-ID: `AG | agent-governance | T063 | root-8` — reserved NEW same-work-unit successor root; not started or consumed  
Task-Contract: `docs/tasks/T063-adaptive-worker-routing-requalification.md`  
Current-Design-Review: `docs/reviews/T063-R16.md`  
Current-Readiness-Revocation: `docs/reviews/T063-R18.md`  
Withdrawn-Launch-Review: `docs/reviews/T063-R17.md`  
Current-Research: `docs/research/R025-T063-V8-REATTACH-CLASSIFIER-HARDENING.md`  
Prior-Research: `docs/research/R024-T063-V7-NO-ROLLOUT-REATTACH-RACE.md`  
Withdrawn-V8-Candidate-HEAD: `83f38bd9813cfdd107486ad40d39df6335513ce8`  
Withdrawn-V8-Candidate-Base: `621e9ae0d73378b1013699e8726b315128c95891`  
T063-V7-Evidence-HEAD: `58e396c126e363428544b163cb2aa8c7e1ac8ed6`  
T063-V7-Implementation-HEAD: `5a1769fed3f93d86cbc2e72a6cc89d7a276089d6`  
Held-Work-Unit: T062 / T023 v15 Stage 6  
Held-State: HUMAN_HOLD_R32_UNCONSUMED  
Chat-Closure: KEEP_CURRENT_CHAT

## Canonical transition

O275 had authorized v8 candidate `83f38bd...` for Human-mediated Stage 6. Before launch, the Human requested external validation of the v8 persistence theory against official Codex source/documentation and specialized field evidence.

R025 confirmed the conceptual bounded same-child retry but found the provisional `ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD` classifier too permissive for readiness. The withdrawn adapter matched the resume prefix plus exact child ID but did not structurally require the represented JSON-RPC mapping to have exactly code `-32600` and exactly the canonical no-rollout message.

T063-R18 therefore revokes R17/O275 authorization before any Human Codex launch or v8 provider/model call.

```text
withdrawn candidate: test/t063-adaptive-worker-routing-requalification-v8@83f38bd9813cfdd107486ad40d39df6335513ce8
provider/model calls under v8: 0
Stage 6 authority: none
```

## R025 external revalidation result

Official Codex `rust-v0.153.4` source/tests establish:

- a fresh persistent thread may expose a valid thread ID/path before rollout materialization;
- `thread/resume` remains required for the D063 permission/profile receipt surface;
- no-rollout is emitted after live-writer/SQLite/filesystem rollout resolution fails.

Official issue evidence shows both short-lived startup races and persistent/unmaterialized cases with the same message family. Therefore `no rollout found` is not intrinsically transient.

The supported interpretation is:

```text
exact public child correlation
+ exact same-child thread/resume
+ safely parsed error mapping
+ code == -32600
+ message == "no rollout found for thread id <exact child id>"
=> bounded retryable availability condition inside the existing persistence barrier

otherwise
=> fail closed
```

The accepted R022 `EMPTY_ROLLOUT` class remains unchanged.

## Required Stage 5 hardening

Materialize a clean v8 candidate that:

1. safely parses the represented JSON-RPC mapping from the flattened `AppServerError` without `eval`;
2. requires integer code `-32600` exactly;
3. requires exact message equality for the exact resumed child ID;
4. rejects wrong code, message drift, malformed payload and wrong/missing child;
5. preserves the R022 empty-rollout classifier;
6. preserves one shared ten-attempt budget across both availability conditions;
7. preserves `0.2s wait -> exact parent residency check -> identical same-child resume` for every retry;
8. creates no respawn, parent replay, replacement child or provider/model quality turn;
9. preserves v7 24-arm schedule, profiles, probes/oracles, quality/usage/pilot semantics;
10. promotes no historical terminal telemetry/handoff JSON.

A new exact candidate HEAD and fresh readiness review are required before Stage 6 can be authorized again.

## Scientific continuity

V8 remains one clean 24-arm fixed-n replicated qualification calibration:

```text
4 replicate blocks
3 probes
2 profiles
= 24 first-attempt scored children on a complete valid run
```

Frozen profiles/schedule/oracles/quality taxonomy remain unchanged from R16. V1-v7 evidence remains historical only and cannot enter v8 scoring.

## D076 state

The structured two-class persistence controller and its regression suite are material Stage 5 behavior. Stage 6 must not invent or broaden this classifier.

## D077 state

```text
qualified pin:              0.153.4
latest stable reviewed:     0.154.0
latest stable tag:          rust-v0.154.0
version disposition:        PIN_RETAINED
```

No reviewed stable release proves removal of the relevant persistence architecture. D063 remains qualified specifically on 0.153.4.

## Coordinator continuity

`AG | agent-governance | T063 | root-8` was reserved under O275 but never launched. It remains unconsumed and may be retained if a hardened v8 candidate is later authorized.

## Held and frozen work

T062/T023 remains on Human hold exactly as previously recorded. Do not execute its old continuation authority without new Human selection and revalidation.

T058 remains frozen by explicit Human decision. Do not resume, integrate, clean or copy it without new explicit Human authorization.

R007 remains `EVALUATING`; no global adaptive worker-routing policy is adopted.

## Next Chat Minimum Load

After normal bootstrap (`develop`, `AGENTS.md`, this checkpoint):

1. load the active T063 Task Contract first;
2. load R18 and R025 for current Stage 5 hardening authority;
3. load R16/R024/R022 when deeper persistence/design provenance is required;
4. load D063/D076/D077 when receipt, materialization or version constraints are at issue;
5. for Task Contract material revision/readiness, load the Maintainer Skill v4 template + usage reference;
6. do not reconstruct the frontier from prior chat/Project Memory.

## Next Action

ChatGPT Orchestrator must complete D068 Stage 5:

1. materialize a fresh hardened v8 candidate from current protected `develop` authority;
2. replace the withdrawn textual/regex no-rollout classifier with safe structural parsing and exact code/message/child equality;
3. add the R025 negative conformance cases;
4. verify remote candidate ancestry/delta and any provider-free checks available without claiming unavailable pytest/Ruff results;
5. perform D077 release revalidation;
6. persist a new readiness review, exact candidate freeze and checkpoint before any Human launch.

No provider/model call and no Codex Stage 6 launch is authorized at O276.
