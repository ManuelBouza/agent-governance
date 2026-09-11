# R022 — T063 V3 Empty-Rollout Reattach Race

Research-ID: R022  
Research-State: COMPLETE  
Decision-State: NOT_REQUIRED  
Opened: 2026-09-11  
Last-Reviewed: 2026-09-11  
Owner: ChatGPT Orchestrator  
Task: `docs/tasks/T063-adaptive-worker-routing-requalification.md`  
Prior authority: `docs/reviews/T063-R6.md`  
Prior receipt research: `docs/research/R021-T063-V3-CONFIG-AUTHORITATIVE-WORKER-RECEIPTS.md`  
Measurement authority: `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md`  
Version authority: `docs/decisions/D077-version-sensitive-upstream-revalidation.md`  
Provider/model calls during this research: `0`

## Question

T063 v3 blocked after the exact child had already started because the harness immediately attempted public App Server `thread/resume` reattachment and received a thread-store error ending in:

```text
rollout at <path> is empty
```

The question is whether this is evidence of an invalid child, a profile/quality failure, or a transient persistence-visibility race on the public reattach path, and what bounded Stage 5 adapter behavior can preserve D063 semantics without creating another scored child/provider attempt.

## Evidence examined

The v3 terminal evidence is preserved at:

```text
branch: test/t063-adaptive-worker-routing-requalification-v3
HEAD:   746519abc6f159e959120f68d5c9f920d88d5797
handoff:   handoffs/T063-executor-handoff-v3.json
telemetry: handoffs/T063-adaptive-worker-routing-telemetry-v3.json
```

The run consumed one P1 ADAPTIVE parent/child first attempt and then blocked during measurement reattachment. That consumed result remains historical and is excluded from any successor clean-run score.

The bounded Stage 6 repair represented before the terminal v3 return is:

```text
4a1bc28b83bffecc706df0f2e42aafe29456c54e
```

It is mechanical/lint-level and does not alter the diagnosis below.

## Finding 1 — live-thread resume still reads persisted thread state

At exact qualified runtime `openai/codex@rust-v0.153.4`, App Server's running-thread resume path does not rejoin an already loaded thread using only its in-memory `thread_manager` entry.

When the requested thread id resolves to an existing live thread, `thread_resume` still calls:

```text
read_stored_thread_for_resume(
    <exact thread id>,
    path = None,
    include_history = false,
)
```

before proceeding with running-thread rejoin semantics.

Therefore a child may already exist and be running while an immediate public `thread/resume` remains dependent on the rollout/session metadata becoming readable from persistent storage.

This is the exact layer at which the v3 terminal error occurred.

## Finding 2 — empty rollout is a real persisted-read failure class

At `rust-v0.153.4`, the rollout parser emits an I/O error when it reaches the end of a rollout without finding usable session metadata:

```text
rollout at <path> is empty
```

The v3 App Server error wrapped this persisted-read failure as a `thread-store error` / `failed to read session metadata` error during `thread/resume`.

The error therefore does not imply that the public child-correlation receipt was false, that the worker profile failed to resolve, or that the worker produced a bad answer. It establishes that the immediate reattachment read raced persistence visibility.

## Finding 3 — current stable does not remove the relevant path

D077 was revalidated on 2026-09-11 against the official upstream release state.

Current stable remains:

```text
openai/codex 0.154.0
release tag: rust-v0.154.0
published: 2026-09-09
```

No newer stable release appeared after R021/R6.

At `rust-v0.154.0`:

- the running-thread resume path still calls `read_stored_thread_for_resume(... include_history=false)` for an already live thread;
- the rollout parser still contains the same `rollout at <path> is empty` error class.

A fresh review of upstream `main` on 2026-09-11 also found the same live-thread persisted-read call on the reattach path.

This evidence does not extend D063 qualification to `0.154.0` or `main`; it only shows that upgrading would not remove the specific persistence dependency that blocked v3.

D077 disposition remains:

```text
PIN_RETAINED
qualified runtime: 0.153.4
upgrade fixes this blocker: false based on current stable review
```

If a newer stable appears before successor launch, D077 requires another relevance classification before provider-backed execution.

## Finding 4 — retrying reattachment is not a new child attempt

The blocked operation is the App Server measurement client's public `thread/resume` RPC for the **same already-created child id**.

A retry can preserve experiment semantics only when it does all of the following:

```text
same exact child thread id
same thread/resume params
no spawn_agent replay
no parent turn replay
no new child/provider turn
no task/profile/oracle mutation
no fallback to another receipt surface
```

Such a retry is a measurement-adapter transport operation, not a scored worker retry.

It must therefore be accounted separately from:

```text
scored_parent_turns
scored_child_attempts
```

## Finding 5 — bounded same-child persistence barrier

The supported Stage 5 repair is a narrow fail-closed persistence barrier around exact-child `thread/resume`:

```text
initial thread/resume
    -> success: continue D063 measurement
    -> exact empty-rollout thread-store error only:
         wait 0.2 seconds
         re-check exact parent loaded residency
         if parent absent: BLOCK
         retry thread/resume for the same child id
    -> any other error: fail immediately
    -> maximum 10 total resume attempts
    -> exhaustion: BLOCK
```

The parent residency check must occur **after the delay and immediately before each retry**. Checking before the delay leaves an unobserved residency window and is not sufficient for the D063 continuous-parent-residency requirement.

The adapter must record at least:

```text
child_id
parent_id
attempt_count
retry_count
parent_residency_rechecks
transient_error_class
same_child_reused = true
new_provider_turn_created = false
```

## Stage 5 candidate

ChatGPT Orchestrator materialized the successor adapter on:

```text
branch: test/t063-adaptive-worker-routing-requalification-v4
base:   9da2b6fed64ded9af8d38f67cd53cd066abef838
HEAD:   f06c8f48f7b1d59dff9fc117cca5b42453ad23e8
```

The branch includes the repaired v3 executable package byte-for-byte plus the v4 adapter and adapter tests. All nine copied v3 code/test blobs were verified byte-identical to the repaired v3 state represented by `4a1bc28b83bffecc706df0f2e42aafe29456c54e`.

The v4-specific adapter:

```text
evals/adaptive_worker_routing_v4/runner.py
```

retries only when all observed empty-rollout markers match, sleeps first, rechecks parent residency immediately before the retry, and calls base `thread/resume` with the same child id/params. It does not respawn or create another provider turn.

## Provider-free verification

Provider-free verification was executed against byte-exact copies of the current remote v4 runner/test blobs:

```text
v4 adapter tests:    6 passed
Python compileall:   PASS
provider/model calls: 0
Codex/App Server launches: 0
```

The tested local Git blob hashes matched the remote candidate blobs:

```text
evals/adaptive_worker_routing_v4/runner.py
  3996ad60619d8f4822707389e13878b5a134f7fe

tests/test_t063_adaptive_worker_routing_v4_adapter.py
  4c50e3a47c41d9cb42d1f709356ba89f924656ff
```

The tests cover:

- exact empty-rollout classification;
- same-child reuse across retries;
- ordering `sleep -> parent residency check -> retry resume`;
- immediate failure for nonmatching errors;
- stop before retry if parent residency is lost;
- bounded exhaustion.

## D063 and D076 interpretation

The v4 persistence barrier does not weaken D063. All mandatory parent/child identity, read-only permission, configured model/reasoning, exact usage/duration, reroute and mutation receipts remain required after successful reattachment.

`backend_served_profile_verified = false` remains unchanged.

The barrier is substantial executable measurement-adapter material, so it was materialized by ChatGPT Orchestrator in Stage 5. Executor Stage 6 may execute/diagnose/verify and make only bounded technical repairs that preserve this exact semantic boundary. D076 does not permit the Executor to invent a different reattachment controller or receipt strategy privately.

## Conclusion

The v3 blocker is classified as:

```text
BLOCKED_MEASUREMENT_SURFACE
cause: SAME_CHILD_ROLLOUT_PERSISTENCE_VISIBILITY_RACE
worker-quality failure: no
profile-resolution failure: no
new child required: no
D076 violation: no
```

A bounded same-child `thread/resume` persistence barrier is a valid Stage 5 correction when it retries only the exact empty-rollout failure, rechecks parent residency immediately before each retry, never respawns/replays a provider turn, and fails closed on every other condition.

The v3 consumed P1 attempt remains historical and unscored. Any successor pilot must again be one homogeneous clean six-arm run.
