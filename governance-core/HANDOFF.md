# Handoff and Recovery

Handoff-Version: 1.2.0

Load this module for agent handoff, cold-start recovery, implementation review, SDD re-entry, stale checkpoint repair or human intervention persistence.

Load `SDD.md` when the handoff follows Implementation `Code Review & Verify`, when Strategy performs `Converge / Accept / Evolve`, or when an upstream specification/Design/Plan defect requires re-entry.

## Cold Start

Start with STATE + GOVERNANCE only. Use GOVERNANCE routing to identify additional context. Never assume prior chat history exists or that a particular agent product is active.

## Strategy -> Implementation

1. Ensure F5 passed and F6 persisted an authorized SDD-anchored execution sequence.
2. STATE identifies the current frontier; WORKPLAN exposes only execution metadata/index.
3. The Implementation Agent loads EXECUTION + SDD + the first READY task + exact referenced specification/Design artifacts + required Skills.
4. It then continues sequentially without Strategy/Human handoff between tasks while eligibility remains valid.
5. Future task content remains undisclosed until the current task reaches DONE.

Strategy's handoff must not require Implementation to reconstruct missing requirements, controlling Design, Plan/Trace or acceptance meaning.

## Implementation -> Strategy

A normal handoff occurs only when:
- the authorized task sequence is exhausted after the applicable tasks completed Implement + Code Review & Verify; or
- the current task reaches a valid cross-responsibility/SDD re-entry blocker; or
- the Human Owner intervenes; or
- an explicit F5-approved external gate requires it.

At handoff, Implementation evidence for each relevant DONE task must make the applicable subset reconstructable:

- implementation state/identity;
- material requirement/spec-delta and `PRESERVED` coverage;
- required verification commands/methods/results;
- technical code-review findings and resolution of in-authority defects;
- unresolved issues;
- any suspected upstream specification/Design/Plan defect and the earliest affected SDD stage.

At Strategy handoff processing:
1. read EXCHANGE events with `q > STATE.exchange_q`;
2. inspect only evidence referenced by those events that is required for convergence/blocker resolution;
3. load SDD plus EXECUTION/current or completed task records only as needed;
4. perform `Converge / Accept / Evolve`: compare specification/Design/Plan, implementation and review/verification evidence for completeness, correctness, coherence, containment and persistence;
5. emit accept/reject/decision/scope_change/resume as required;
6. if an upstream defect exists, re-enter the earliest affected Strategy-owned SDD stage and persist revised authority before resume;
7. evolve the accepted current specification carrier when acceptance changes its living state;
8. update strategic records only if strategy/specification/Design/Plan changed;
9. refresh STATE after authoritative changes;
10. report concise project status to the Human Owner.

Implementation `DONE` remains evidence only. Strategy/Human acceptance is the authority transition to `ACCEPTED`.

## Blocker Resume

When Strategy/Human resolves a valid blocker, persist the resolution and `resume` event. For an SDD blocker, the revised specification/Design/Plan authority must be durable before resume. The Implementation Agent reloads only the blocked/current task context plus the exact changed controlling artifact and continues the existing sequence. Do not reveal later task content merely to resolve the blocker.

## Stale STATE

If STATE conflicts with later EXCHANGE or authority sources, do not trust it silently. Load PROTOCOL and the minimum disputed authority records, reconstruct the frontier, persist the repair and then continue.

## Human Intervention

Human instructions take effect immediately. Persist their operational effect when it affects future work. Persist the effect, not the conversation transcript. If the intervention changes material specification/Design/Plan/acceptance semantics, route through the corresponding Strategy-owned SDD stage before implementation continues.

## Handoff Invariant

No handoff is complete while future action depends on unavailable chat context, a specific product identity, an external SDD product, an unpersisted controlling decision, or an unpersisted material specification/Design/Plan change.
