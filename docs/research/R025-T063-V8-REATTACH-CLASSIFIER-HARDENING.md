# R025 — T063 V8 Reattach Classifier Hardening

Research-ID: R025  
Research-State: COMPLETE  
Decision-State: NOT_REQUIRED  
Opened: 2026-09-12  
Last-Reviewed: 2026-09-12  
Owner: ChatGPT Orchestrator  
Scope: T063 v8 external revalidation and exact-child no-rollout classifier hardening before Stage 6 readiness  
Question: Is bounded same-child retry for `no rollout found` consistent with official Codex behavior, and what exact fail-closed classifier is required for v8?  
Evaluation-Refs: `docs/reviews/T063-R18.md`; `docs/reviews/T063-R19.md`; hardened candidate `afdae0050226d61a10269f63017e2fac99eef644`  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none  
Task: `docs/tasks/T063-adaptive-worker-routing-requalification.md`  
Prior research: R022, R024  
Measurement authority: D063  
Version authority: D077  
Provider/model calls during this research: `0`

## Question

After v7 exposed `thread/resume failed: {'code': -32600, 'message': 'no rollout found for thread id <exact child id>'}`, is the v8 theory — bounded same-child retry after exact public child correlation — consistent with official Codex behavior, and is the provisional v8 classifier sufficiently narrow for Stage 6 authorization?

## Sources reviewed

Primary official source evidence:

- `openai/codex@rust-v0.153.4` App Server protocol for `ThreadResumeParams` / `ThreadResumeResponse`;
- `openai/codex@rust-v0.153.4` `thread-store/src/local/read_thread.rs`;
- `openai/codex@rust-v0.153.4` `thread-store/src/local/thread_rollout_resolver.rs`;
- `openai/codex@rust-v0.153.4` App Server thread-start/resume tests;
- equivalent relevant paths at `rust-v0.154.0` and current upstream source;
- official `openai/codex` issues #42099, #38613, #33120 and #16872 as field evidence, not normative protocol authority.

Secondary specialized explanatory source reviewed:

- DeepWiki Codex session-resumption/thread-persistence explanation, used only as contextual cross-check and not as normative authority.

## Finding 1 — identity can precede rollout materialization by design

The official `rust-v0.153.4` App Server thread-start test explicitly expects a fresh persistent thread to return a valid thread ID/path while the rollout path does not yet exist before the first user message.

Issue #42099 independently reports the same lifecycle in 0.151.0+: `thread/start` returns and indexes the ID, but a zero-turn thread has no rollout and immediate `thread/resume` returns code `-32600` with `no rollout found for thread id <uuid>`.

Therefore a known thread ID does not imply that rollout-backed resume state is already materialized.

## Finding 2 — `thread/resume` remains the required D063 surface

The official protocol states that when `thread_id` identifies a running thread, App Server rejoins that thread; for non-running threads it may load persisted state by thread ID/path/history.

D063 requires the reattachment response fields used to establish configured model/reasoning and permission provenance. `ThreadReadResponse` carries only the thread object, while `ThreadResumeResponse` carries model, reasoning, sandbox and `activePermissionProfile` fields needed by the qualified receipt set.

Therefore replacing `thread/resume` with `thread/read` would weaken the qualified measurement contract and is not an acceptable v8 workaround.

## Finding 3 — `no rollout found` is produced after supported resolution surfaces fail

At `rust-v0.153.4`, `read_thread()` asks the rollout resolver for the requested thread. The resolver attempts, in order:

1. live-writer rollout path;
2. SQLite selected rollout path;
3. filesystem fallback for eligible threads;
4. archived fallback when requested.

If no current rollout resolves, `read_thread()` emits exactly:

```text
no rollout found for thread id <thread_id>
```

This supports R024's lifecycle model: after exact public child correlation, immediate resume can reach an availability window before rollout visibility is sufficient for the persisted-read path.

## Finding 4 — field evidence supports a real race but not universal transience

Issue #38613 reports the adjacent later phase: a running new thread is resumed roughly tens of milliseconds after start while its rollout file exists but is temporarily empty; later the same rollout becomes valid. This corroborates R022's `EMPTY_ROLLOUT` race.

Issue #33120 reports delegated/subagent placeholders that can remain unmaterialized and surface the same missing-rollout error.

Issue #16872 demonstrates an important counterexample: a thread may complete activity while a rollout never materializes, so `no rollout found` can persist rather than resolve with time.

Therefore `no rollout found` is **not intrinsically a transient error class**. It is only safe to retry as an availability condition inside an already-correlated exact-child barrier with strict identity and bounded-attempt invariants.

## Finding 5 — the provisional v8 classifier is too permissive

The provisional candidate `83f38bd9813cfdd107486ad40d39df6335513ce8` classifies `ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD` by checking:

- that the flattened exception contains `thread/resume failed:`;
- exactly one `no rollout found for thread id <id>` regex match;
- matched ID equals the requested child.

That is narrower than a generic substring match but still does not prove the represented JSON-RPC error is the exact supported shape. App Server uses `-32600` for multiple invalid-request conditions, and additional text/data could be flattened into the exception representation.

Readiness therefore should not rely on this classifier.

## Finding 6 — hardened classifier requirement

Because the v3 client currently flattens JSON-RPC errors into `AppServerError` text, v8 must parse the represented error payload structurally rather than expand the transport client in Stage 6.

For `ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD`, retry is allowed only when all are true:

```text
method == thread/resume
error payload parses as one mapping
error.code == -32600 exactly
error.message == "no rollout found for thread id <exact child id>" exactly
no alternate/missing/different child id
```

A robust Stage 5 implementation may parse the suffix after the exact `thread/resume failed: ` prefix with a safe literal parser and then compare typed fields exactly. Any parse failure, extra/changed message text, wrong code or wrong child ID is nonmatching and fails closed.

The accepted R022 `EMPTY_ROLLOUT` classifier remains unchanged.

## Finding 7 — retry semantics remain bounded and non-provider

The conceptual v8 barrier remains supported with these invariants:

```text
exact publicly correlated child only
same thread/resume params object
same parent
one shared maximum of 10 total resume attempts across both availability conditions
0.2 s wait before each retry
parent loaded-residency check immediately before each retry
no spawn replay
no parent-turn replay
no child replacement
no provider/model quality turn created by retry
```

A sequence such as:

```text
NO_ROLLOUT -> EMPTY_ROLLOUT -> success
```

may succeed within one common budget.

If the budget exhausts, the evidence must be classified as a persistence/materialization blocker. Exhaustion does **not** prove that the original no-rollout condition was transient.

The 10-attempt/0.2-second policy is a project fail-closed bound inherited from the qualified successor design, not an upstream guarantee that Codex must materialize within two seconds.

## Finding 8 — D077 remains PIN_RETAINED

`0.154.0` remains the current stable reviewed during this research and retains the relevant rollout-resolution/persisted-read architecture. No reviewed stable release establishes removal of this blocker family, while D063 remains qualified specifically on 0.153.4.

Disposition:

```text
qualified runtime: 0.153.4
current stable reviewed: 0.154.0
upgrade proven to fix blocker: no
D077: PIN_RETAINED
```

## Readiness impact

Earliest affected stage:

```text
Stage 5 — candidate materialization/readiness
```

R024's conceptual successor direction remains valid. The external revalidation narrows the classifier and changes the interpretation from an inherently transient error class to a bounded retryable availability condition under exact correlated-child evidence.

The previous Stage 6 authorization for candidate `83f38bd...` must therefore be revoked before Human launch. A new exact candidate HEAD must materialize the hardened classifier and negative conformance tests, then receive a fresh readiness review.

## Required regression additions

At minimum the hardened v8 suite must prove:

- exact `-32600` + exact message + exact child => classified;
- wrong code + otherwise exact message => not classified;
- exact code + message prefix/suffix drift => not classified;
- exact code + wrong/missing child => not classified;
- malformed/unparseable error payload => not classified;
- unrelated `-32600` condition => not classified;
- accepted `EMPTY_ROLLOUT` behavior unchanged;
- mixed no-rollout/empty-rollout success uses one shared budget;
- common-budget exhaustion remains fail-closed;
- same-child/same-params/residency/no-new-provider invariants remain intact.

## Conclusion

```text
v8 conceptual same-child bounded retry: SUPPORTED
no-rollout intrinsically transient: NO
provisional candidate 83f38bd readiness: REVOKE
required repair: Stage 5 structured exact classifier hardening
provider/model calls consumed by revalidation: 0
```