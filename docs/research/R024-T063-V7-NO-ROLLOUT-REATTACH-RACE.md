# R024 — T063 V7 No-Rollout Reattach Race

Research-ID: R024  
Research-State: COMPLETE  
Decision-State: NOT_REQUIRED  
Opened: 2026-09-12  
Last-Reviewed: 2026-09-12  
Owner: ChatGPT Orchestrator  
Scope: T063 v7 exact-child `thread/resume` no-rollout blocker and successor persistence-barrier semantics  
Question: Does the v7 exact-child `no rollout found` blocker represent worker quality, invalid child identity, or a persistence-visibility phase suitable for bounded same-child retry?  
Evaluation-Refs: `docs/reviews/T063-R15.md`; `docs/reviews/T063-R16.md`; v7 terminal HEAD `58e396c126e363428544b163cb2aa8c7e1ac8ed6`  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none  
Task: `docs/tasks/T063-adaptive-worker-routing-requalification.md`  
Prior adapter research: `docs/research/R022-T063-V3-EMPTY-ROLLOUT-REATTACH-RACE.md`  
Prior parent-surface research: `docs/research/R023-T063-V5-LIVE-SPAWN-RECEIPT-PERSISTENCE-GAP.md`  
Measurement authority: `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md`  
Version authority: `docs/decisions/D077-version-sensitive-upstream-revalidation.md`  
Provider/model calls during this research: `0`

## Question

T063 v7 blocked on scheduled arm 6 after a public exact-child spawn correlation because the first public App Server `thread/resume` for that child returned:

```text
thread/resume failed: {'code': -32600, 'message': 'no rollout found for thread id <exact child id>'}
```

The question is whether this represents worker/profile quality, a distinct invalid child, or an earlier persistence-visibility phase of the same public same-child reattachment race already characterized by R022.

## Evidence examined

V7 terminal evidence:

```text
branch: test/t063-adaptive-worker-routing-requalification-v7
initial candidate: 9fb55e8f36570f6b91d0a23720ccc6a62a9d0b90
implementation head before scoring: 5a1769fed3f93d86cbc2e72a6cc89d7a276089d6
terminal evidence head: 58e396c126e363428544b163cb2aa8c7e1ac8ed6
handoff: handoffs/T063-executor-handoff-v7.json
telemetry: handoffs/T063-adaptive-worker-routing-telemetry-v7.json
```

The run completed five fully measured children, all PASS, then consumed the sixth parent/child attempt and blocked before a fully measured sixth child snapshot existed.

Observed complete quality evidence before the block:

```text
P1 ADAPTIVE PASS
P1 CONTROL  PASS
P2 CONTROL  PASS
P2 ADAPTIVE PASS
P3 ADAPTIVE PASS
```

The blocked sixth scheduled arm was P3 CONTROL. The partial five-child evidence is historical only and is not a complete v7 model comparison or pilot decision.

## Finding 1 — the Executor stopped at the correct contract boundary

V7 authorized same-child reattachment retries only for the exact R022 empty-rollout marker family. `no rollout found for thread id ...` did not match that family.

The Executor therefore:

- made no replacement spawn;
- made no parent-turn replay;
- made no compensating scored call;
- emitted `BLOCKED_EXECUTION_INVALID`;
- left `pilot_decision=null`;
- identified Stage 2 Specify as the earliest required re-entry stage.

This is compliant fail-closed behavior, not a v7 quality result.

## Finding 2 — `no rollout found` is emitted by the same persisted-read path

At the exact qualified runtime `openai/codex@rust-v0.153.4`, thread-store `read_thread()` first tries persisted SQLite-backed metadata when usable, then calls the thread-rollout resolver. If no rollout can be resolved, it returns:

```text
no rollout found for thread id <thread_id>
```

The resolver attempts, in order:

1. the live writer rollout path, when present and visible;
2. SQLite's selected rollout path;
3. filesystem fallback for eligible threads;
4. archived fallback only when requested.

Therefore the v7 error means that the same exact child ID was publicly known to the parent/App Server surface, but the resume-side persisted-read machinery could not yet resolve a rollout through any of its supported visibility paths.

## Finding 3 — this is earlier than R022 empty-rollout, not contradictory to it

R022 established that a correlated/running child can race persistence on immediate `thread/resume`, producing an empty rollout before session metadata is durable.

V7 exposes an earlier phase of that lifecycle:

```text
phase A: rollout path not yet resolvable -> "no rollout found for thread id ..."
phase B: rollout path resolvable but metadata not yet readable -> "rollout at ... is empty"
phase C: persisted read succeeds -> reattachment succeeds
```

Both phase A and phase B occur after exact public child correlation and before the measurement client can reattach through the public persisted-read path.

This classification does not claim that every generic `no rollout found` error is transient. It is safe to treat it as a retryable persistence-visibility state only inside the already-correlated same-child barrier and only when the represented error names the exact requested child ID.

## Finding 4 — bounded same-child retry remains semantically safe

A successor may extend the existing persistence barrier to two exact transient classes without creating a second worker-quality attempt:

```text
EMPTY_ROLLOUT
ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD
```

The extended barrier must preserve all existing R022 invariants:

```text
same exact correlated child id
same thread/resume params
same exact parent
sleep before retry
parent residency rechecked immediately before every retry
no spawn replay
no parent turn replay
no new provider/model turn
one common maximum of 10 total resume attempts
fail closed on any other error
```

For `ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD`, the represented error must contain the exact child ID being resumed. A different/missing ID or generic thread-not-found condition is nonmatching and blocks immediately.

A mixed sequence such as:

```text
no rollout found -> empty rollout -> success
```

uses the same single ten-attempt budget. The budget must not reset when the transient class changes.

## Finding 5 — v7 partial observations do not qualify the routing mapping

V7 model-evidence accounting is correct:

```text
run_execution_validity: INVALID
run_model_comparison_eligible: false
pilot_eligible: false
scored_child_quality_eligible_count: 5
scored_child_efficiency_eligible_count: 5
pilot_decision: null
root_model_failure_attributed: false
```

The five valid PASS children remain historical quality observations. They cannot be combined with a successor run because v7 was prospectively defined as one homogeneous 24-child calibration.

A successor must start a fresh 24-arm schedule and exclude all v7 attempts from scoring.

## Finding 6 — Stage 6 repairs were bounded and acceptable

Before provider-backed scoring, Stage 6 committed exactly two changes to the v7 adapter:

1. rewrote `_TRIAL_CURSOR >= len(ARM_ORDER)` as the equivalent `len(ARM_ORDER) <= _TRIAL_CURSOR` to satisfy lint;
2. changed the schedule guard from nonexistent `ArmSpec.reasoning_effort` to the represented v3 field `ArmSpec.reasoning`.

Remote diff shows exactly two added/two removed lines across the two commits, only in `evals/adaptive_worker_routing_v7/runner.py`. Neither change modifies schedule, profile matrix, oracle, retry semantics, quality semantics, thresholds or decision taxonomy.

The terminal commit after scoring adds only the v7 telemetry and handoff JSON files.

Disposition:

```text
D076 bounded repair: ACCEPTED
semantic redesign by Executor: no
```

## Finding 7 — current stable still does not remove the blocker class

Official Codex release state revalidated on 2026-09-12:

```text
qualified runtime: 0.153.4
current stable:     0.154.0
```

At `rust-v0.154.0`, `read_thread()` still returns the same `no rollout found for thread id ...` error when the resolver yields no rollout. Therefore the current stable does not remove this persistence dependency.

D077 remains:

```text
PIN_RETAINED
upgrade fixes blocker: false based on current stable review
```

This does not extend D063 qualification beyond `0.153.4`.

## Successor specification impact

Earliest affected SDD stage:

```text
Stage 2 — Specify
```

A clean successor should modify only the same-child persistence barrier semantics and corresponding tests/evidence labels while preserving the v7 24-arm replicated design, probe/oracle definitions, profile matrix, schedule, quality taxonomy, efficiency threshold and pilot-decision taxonomy.

Required successor conformance coverage should include:

- exact-child `no rollout found` classification;
- rejection when the represented thread ID differs from the correlated child;
- mixed `ROLLOUT_NOT_FOUND -> EMPTY_ROLLOUT -> success` under one attempt budget;
- common ten-attempt exhaustion across mixed transient classes;
- sleep then parent-residency check before every retry;
- same-child/same-params reuse and no new provider turn;
- immediate failure for every other error.

## Conclusion

V7 is classified as:

```text
terminal: BLOCKED_EXECUTION_INVALID
cause: SAME_CHILD_ROLLOUT_DISCOVERY_VISIBILITY_RACE
worker-quality failure: no
profile-resolution failure: no
measurement-adapter/specification gap: yes
v7 pilot decision: null
successor required: clean 24-arm run
```

The supported correction is a prospectively specified extension of the existing same-child persistence barrier to the exact-child `no rollout found` phase, with one shared bounded retry budget and all existing fail-closed residency/provider-call invariants preserved.