# Handoff and Recovery

Handoff-Version: 1.1.0

Load this module for agent handoff, cold-start recovery, implementation review, stale checkpoint repair or human intervention persistence.

## Cold Start

Start with STATE + GOVERNANCE only. Use GOVERNANCE routing to identify additional context. Never assume prior chat history exists or that a particular agent product is active.

## Strategy -> Implementation

1. Ensure F5 passed and F6 persisted an authorized execution sequence.
2. STATE identifies the current frontier; WORKPLAN exposes only execution metadata/index.
3. The Implementation Agent loads EXECUTION + the first READY task + required Skills.
4. It then continues sequentially without Strategy/Human handoff between tasks.
5. Future task content remains undisclosed until the current task reaches DONE.

## Implementation -> Strategy

A normal handoff occurs only when:
- the authorized task sequence is exhausted; or
- the current task reaches a valid cross-responsibility blocker; or
- the Human Owner intervenes; or
- an explicit F5-approved external gate requires it.

At handoff:
1. read EXCHANGE events with `q > STATE.exchange_q`;
2. inspect only evidence referenced by those events that is required for review/blocker resolution;
3. load EXECUTION/current or completed task records only as needed;
4. emit accept/reject/decision/scope_change/resume as required;
5. update strategic records only if strategy changed;
6. refresh STATE after authoritative changes;
7. report concise project status to the Human Owner.

## Blocker Resume

When Strategy/Human resolves a valid blocker, persist the resolution and `resume` event. The Implementation Agent reloads only the blocked/current task context and continues the existing sequence. Do not reveal later task content merely to resolve the blocker.

## Stale STATE

If STATE conflicts with later EXCHANGE or authority sources, do not trust it silently. Load PROTOCOL and the minimum disputed authority records, reconstruct the frontier, persist the repair and then continue.

## Human Intervention

Human instructions take effect immediately. Persist their operational effect when it affects future work. Persist the effect, not the conversation transcript.

## Handoff Invariant

No handoff is complete while future action depends on unavailable chat context, a specific product identity, or an unpersisted controlling decision.
