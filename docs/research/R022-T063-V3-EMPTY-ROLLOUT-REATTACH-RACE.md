# R022 — T063 V3 Empty-Rollout Reattach Race

Research-ID: R022  
Research-State: COMPLETE  
Decision-State: NOT_REQUIRED  
Opened: 2026-09-11  
Last-Reviewed: 2026-09-11  
Owner: ChatGPT Orchestrator  
Task: `T063 — Adaptive Worker Routing Requalification`  
Terminal V3 evidence: `test/t063-adaptive-worker-routing-requalification-v3@746519abc6f159e959120f68d5c9f920d88d5797`  
Pre-provider repaired V3 candidate: `4a1bc28b83bffecc706df0f2e42aafe29456c54e`  
Measurement authority: `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md`  
Version authority: `docs/decisions/D077-version-sensitive-upstream-revalidation.md`

## Question

Why did the clean T063 v3 run block on the first P1 ADAPTIVE child at `thread/resume`, and can that defect be repaired without changing the scientific experiment or creating another provider-backed attempt inside the already-consumed v3 run?

## Verified terminal evidence

The Human returned:

```text
STATUS: BLOCKED
HANDOFF: handoffs/T063-executor-handoff-v3.json
BRANCH: test/t063-adaptive-worker-routing-requalification-v3
HEAD: 746519abc6f159e959120f68d5c9f920d88d5797
```

Remote Git verification established that the returned HEAD exactly matched the branch. The delta from the frozen v3 Stage 5 candidate contained only:

- one represented pre-provider Ruff/formatting repair to the published harness/tests at `4a1bc28b83bffecc706df0f2e42aafe29456c54e`;
- terminal non-Markdown v3 telemetry/handoff evidence.

No committed Markdown, product source, T062/T023 work, or T058 work changed.

The represented formatting repair preserved experiment semantics and is accepted as bounded D068/D076 Stage 6 repair.

Terminal provider accounting is:

```text
scored parent turns:       1
scored child attempts:     1
valid scored children:     0
diagnostic child attempts: 0
compensating attempts:     0
invalid attempt:            P1 ADAPTIVE
pilot_decision:             null
```

The failed attempt is historical invalid execution evidence. It is neither a quality PASS nor FAIL and may not be reused in a future scored set.

## Desktop runtime result

The v3 native preflight resolved the runtime used from the Human's Codex Desktop installation and proved:

```text
Codex CLI / effective bundled codex.exe: 0.153.4
App Server:                               0.153.4
auth category:                            chatgpt
```

Therefore the v3 block was not caused by using the wrong Desktop/CLI/App Server version and did not require a separate standalone CLI installation.

## Exact failure

The child was publicly correlated by the expected V2 activity item, but immediate reattachment failed:

```text
thread/resume
  -> thread-store error
  -> failed to read session metadata from rollout-....jsonl
  -> rollout ... is empty
```

The public `subAgentActivity(kind=Started, agentThreadId=<child>)` had already established the real child identity. The failure occurred before the harness could capture the D063 child reattachment receipts required for scoring.

## Exact-source diagnosis

The official Codex App Server implementation for the reviewed runtime performs the running-thread resume path in this order:

1. `thread/resume` resolves stored thread/session metadata from the rollout;
2. only after that persisted metadata read succeeds does the App Server rejoin/get the in-memory running thread.

The relevant implementation is in:

```text
codex-rs/app-server/src/request_processors/thread_processor.rs
```

and routes through the running-thread resume / stored-thread-for-resume path before returning the active thread.

This creates a narrow startup race:

```text
spawn child
  -> child identity exists and Started activity is emitted
  -> rollout JSONL path exists
  -> first metadata line is not yet durable
  -> harness immediately calls thread/resume
  -> stored metadata reader sees an empty rollout
  -> resume fails although the same child is already running
```

This is an adapter persistence race, not a worker-quality or profile-resolution result.

## D077 higher-version revalidation

The same relevant `thread/resume` ordering was reviewed in:

```text
0.153.4
0.154.0          current stable during this review
0.155.0-alpha.2  later relevant prerelease
current upstream main
```

The higher reviewed versions retain the same material resume path; none provides an upstream fix that removes the empty-rollout race for T063.

Disposition:

```text
PIN_RETAINED
retained runtime:       0.153.4
upgrade fixes blocker:  false
requalification needed: no version-driven change for this repair
```

D063 qualification therefore remains pinned to 0.153.4. This research does not generalize D063 to newer versions.

## Qualified repair

The minimum repair is a bounded persistence barrier around the **same** child reattachment operation.

A future clean run may retry `thread/resume` only when all of the following hold:

- the error is specifically the `thread-store` / `failed to read session metadata` / `rollout ... is empty` condition;
- the child ID is unchanged;
- the parent ID is unchanged;
- the exact parent remains present in `thread/loaded/list` before every retry;
- no new child is spawned;
- no new parent/model turn is started;
- no task/profile/oracle/scoring value changes;
- retries are deterministically bounded and exhaustion fails closed;
- the retry count and result are persisted as measurement-adapter evidence.

Any other `thread/resume` error fails immediately rather than being hidden by the barrier.

A `thread/resume` RPC retry under those constraints is reattachment mechanics for an already-created child, not a compensating provider/model attempt.

## V4 Stage 5 materialization

ChatGPT Orchestrator materialized the repair on:

```text
branch: test/t063-adaptive-worker-routing-requalification-v4
base:   9da2b6fed64ded9af8d38f67cd53cd066abef838
HEAD:   89da4d5b5fbeeb32e6dcf4dd4fde7839f043dfa5
```

The candidate reuses the represented pre-provider v3 harness/test blobs byte-for-byte and adds a narrow v4 adapter plus provider-free adapter tests.

The v4 adapter freezes:

```text
max thread/resume attempts: 10
retry delay:                0.2 seconds
maximum retry wait:         1.8 seconds
retry target:               same exact child
parent residency:           rechecked before each retry
new provider/model turn:    forbidden
```

No v4 provider/model calls occurred during Orchestrator materialization.

## Scientific restart consequence

The consumed v3 P1 ADAPTIVE attempt cannot be rerun and mixed with new arms. A future accepted pilot must again be one homogeneous clean six-arm run under the repaired adapter.

Historical excluded heads are now:

```text
v1  3d8a9460988351383a90adfc6b76e2deff056504
v2  3ff745a8d29e031ca818c1bc618b15a54e0cbf2b
v3  746519abc6f159e959120f68d5c9f920d88d5797
```

R007 remains `EVALUATING`. No adaptive routing policy or pilot decision is adopted by this research.
