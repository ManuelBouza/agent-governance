# R023 — T063 V5 Live Spawn Receipt Persistence Gap

Research-ID: R023  
Research-State: COMPLETE  
Decision-State: NOT_REQUIRED  
Opened: 2026-09-11  
Last-Reviewed: 2026-09-11  
Owner: ChatGPT Orchestrator  
Task: `docs/tasks/T063-adaptive-worker-routing-requalification.md`  
Prior receipt research: `docs/research/R021-T063-V3-CONFIG-AUTHORITATIVE-WORKER-RECEIPTS.md`  
Prior adapter research: `docs/research/R022-T063-V3-EMPTY-ROLLOUT-REATTACH-RACE.md`  
Measurement authority: `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md`  
Version authority: `docs/decisions/D077-version-sensitive-upstream-revalidation.md`  
Provider/model calls during this research: `0`

## Question

T063 v5 obtained a public live `subAgentActivity(kind=Started)` receipt for the exact P1 ADAPTIVE child and successfully reattached that same child after one bounded empty-rollout retry. The run then blocked because the completed parent-turn snapshot contained zero `subAgentActivity(kind=Started)` items.

The question is whether the missing duplicate in `turn/completed` invalidates the already-observed public parent/child correlation, or whether the v5 adapter imposed an unsupported persistence assumption on a live notification.

## Evidence examined

Terminal v5 evidence:

```text
branch:    test/t063-adaptive-worker-routing-requalification-v5
candidate: 94b5ec6dcf0d094c1a90f84b08e7ce1de483716f
terminal:  3f9830a65a152ad595653961205e0ca52b9c5ccc
handoff:   handoffs/T063-executor-handoff-v5.json
telemetry: handoffs/T063-adaptive-worker-routing-telemetry-v5.json
```

Observed execution accounting:

```text
scored_parent_turns:         1
scored_child_attempts:       1
reattach_resume_attempts:    2
reattach_resume_retries:     1
scored_children:             0
pilot_decision:              null
run_model_comparison_eligible: false
```

No compensating or diagnostic provider call followed the block.

## Finding 1 — the exact child correlation succeeded before the block

The live App Server stream exposed a public `subAgentActivity` item with:

```text
kind = Started
agentThreadId = exact child id
agentPath = expected task name
```

The adapter used that exact child id for reattachment. The first `thread/resume` hit the already-known empty-rollout race; the bounded v4 barrier then retried the same child after the required delay and parent-residency recheck, and the second resume succeeded.

Therefore the run did not fail because child identity was unknown, because another child was substituted, or because the v4 retry classifier failed.

## Finding 2 — D063 requires real correlation, not duplicate persistence in the final parent snapshot

D063 requires a real exact parent/child correlation plus the remaining permission, residency, profile, usage, duration, reroute and mutation receipts. It does not require the public live correlation item to be duplicated inside the final `turn/completed` snapshot.

The v5 candidate nevertheless called `_validate_parent_surface()` after the parent completed and required exactly one `subAgentActivity(kind=Started)` inside `parent_done.items`.

That additional persistence requirement is adapter Design, not D063 authority.

## Finding 3 — Codex 0.153.4 distinguishes live item events from persisted history

At the qualified `openai/codex@rust-v0.153.4` runtime, Multi-Agent V2 emits a `SubAgentActivity` turn item through both live item-started and item-completed emission helpers.

The rollout persistence policy separately controls what becomes durable/replayable history. In particular:

- `EventMsg::ItemStarted` is transient and is not persisted;
- paginated history persists `ItemCompleted` turn items;
- legacy `EventMsg::SubAgentActivity` persistence follows different rules;
- live App Server item notifications can therefore expose a spawn receipt that is not required to reappear as the same `Started` item in the parent turn snapshot returned at completion.

The v5 observation is consistent with this architecture: the live public receipt existed and was usable for exact-child reattachment, while the completed parent-turn item list did not duplicate it.

## Finding 4 — Codex 0.154.0 retains the relevant persistence policy

The official `rust-v0.154.0` rollout policy retains the same material distinction: `ItemStarted` remains transient and paginated history persists completed turn items.

No newer stable release than `0.154.0` was present at review time.

Therefore upgrading does not remove this blocker. D063 qualification is not extended to `0.154.0`; the version conclusion is only that the specific v5 persistence assumption is not repaired by the current stable release.

D077 disposition remains:

```text
qualified runtime: 0.153.4
current stable:     0.154.0
disposition:        PIN_RETAINED
upgrade fixes blocker: false
```

## Finding 5 — successor parent-surface validation should use the live public event window

A successor adapter can preserve the v5 safety intent without requiring unsupported duplicate persistence.

For the exact parent turn, after receiving the first matching public spawn receipt and before accepting the parent turn as valid, the adapter should inspect the captured public notification window and require:

```text
exactly one subAgentActivity(kind=Started) for the parent turn
that item matches the exact child id and expected task name
no second/different Started child activity for the same parent turn
no forbidden parent tool/item activity in the same public window
parent turn completes with the exact expected turn id
parent final agent text == PARENT_SPAWNED
```

The completed parent-turn snapshot may still be used for stable final text/status and any durable item checks that are actually represented there, but absence of the already-observed live `Started` item must not invalidate correlation by itself.

Internal/raw response events remain excluded. The canonical spawn correlation remains the public App Server `subAgentActivity` item.

## Finding 6 — v5 remains execution-invalid and model-neutral

Because the adapter blocked before a fully measured child snapshot existed:

```text
terminal_classification: BLOCKED_EXECUTION_INVALID
failure_domain:          EXECUTION_VALIDITY
run_execution_validity:  INVALID
scored_child_quality_eligible_count: 0
scored_child_efficiency_eligible_count: 0
root_model_failure_attributed: false
pilot_decision: null
```

The consumed attempt is historical only. It is not worker-quality evidence for Luna, Terra or Sol and must not enter any matched CONTROL/ADAPTIVE comparison.

## Conclusion

T063 v5 exposed a measurement-adapter Design defect:

```text
cause: COMPLETED_PARENT_SNAPSHOT_DUPLICATION_ASSUMPTION
live public exact-child correlation: succeeded
same-child v4 reattachment barrier: succeeded
model-quality evidence: none
profile-resolution failure: no
runtime upgrade required: no
```

The supported successor correction is to make the public live notification window authoritative for spawn cardinality/correlation and parent-tool activity, while using the completed parent turn only for properties that are actually stable in that snapshot. A clean successor run is required; the consumed v5 attempt remains excluded from scoring.
