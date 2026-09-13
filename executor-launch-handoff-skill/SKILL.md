---
name: executor-launch-handoff
description: Prepare and close a bounded delegated executor/session boundary by binding persisted execution authority to a concrete executor/session, establishing a safe fresh baseline, keeping transport minimal, requiring durable return evidence, and failing closed on ambiguous authority or writable-session collision. Do not use for local helper calls, direct non-delegated execution, generic model advice, task specification/Design, command syntax selection, or already-complete results with no new delegation.
---

# Executor Launch and Handoff

Use for an actual bounded delegation boundary, not generic prompting.

## Trigger

Activate when one role/agent delegates a persisted work unit to an executor/worker and safe launch/continuation requires exact authority, fresh represented state, session identity, minimal transport, and durable return evidence.

Do not activate for local helper tools inside the same execution context, ordinary direct execution, model-selection advice without a delegated task, specification/Design/acceptance work, shell/Git/API syntax selection, or a final result already durably represented with no new launch/handoff.

## Workflow

1. Resolve the persisted delegated authority and resource/repository context.
2. Bind the concrete executor/adapter and NEW/CONTINUE/session context supplied by domain policy.
3. Establish the required safe fresh baseline and fail closed on authority/transport conflicts.
4. When writable collision/continuation safety is material, load `references/workspace-isolation.md`.
5. Transport only the minimum routing/bootstrap information needed to reach canonical authority.
6. Let the executor act inside delegated authority using its own mechanics.
7. Require the domain-defined durable terminal/partial/blocked return artifact/state.
8. Verify returned durable identity/evidence before delegating authority proceeds to its own review/acceptance.

## Postcondition

The caller can reconstruct which executor/session acted, which persisted authority controlled, which represented baseline was used, where the durable result is stored, which durable state identifies it, and whether review may proceed.

## Authority boundary

This Skill cannot create task scope/specification/Design/acceptance/Human approval, prescribe executor-private methodology absent a material requirement, convert model/session settings into correctness semantics, override repository ownership/freshness rules, or treat chat transport as stronger than persisted authority.

Agent Governance Task Contract format, D055 launch profile, D060 coordinator lifecycle, D054 mechanics, D058/D061/D068/D076 semantics, and exact handoff schema remain in the Maintainer domain.
