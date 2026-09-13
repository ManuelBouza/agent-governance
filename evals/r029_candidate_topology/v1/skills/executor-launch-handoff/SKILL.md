---
name: executor-launch-handoff
description: Use when bounded work is actually delegated to a separate executor or worker session and must be bound to persisted authority, a fresh safe baseline and durable return evidence. Do not use for same-context helpers, generic model advice, task specification or ordinary direct execution without a delegation boundary.
---

# Executor launch handoff — evaluation fixture

Intent: bind a concrete delegated executor/session to persisted execution authority, establish a safe fresh baseline, transport only minimum routing context and require durable return identity/evidence.

Required behavior:
- require identifiable persisted delegated authority;
- bind the concrete executor/session and continuation state;
- establish/verify the required fresh baseline without destructive guessing;
- transport routing context rather than invent missing specification/Design/acceptance semantics;
- require the configured durable result/handoff surface;
- leave semantic acceptance with the governing authority.

Internal route: when delegated work is writable and workspace ownership can collide, use `workspace-isolation` to require one exclusive attributable writable surface, preserve ambiguous/unrepresented state and reuse only coherent same-work-unit state. For repository-backed work, consume `repository-change-control` or repository-local policy for branch/base/integration/retirement facts.

Anti-triggers: local helpers within the same execution context, model-selection questions without an actual delegated unit, shell/Git syntax, task specification, or already-finished work with no new launch/handoff boundary.

Postcondition: executor/session, persisted authority, baseline and durable return identity are reconstructable, or the launch/handoff is explicitly blocked. This Skill grants no execution or acceptance authority.
