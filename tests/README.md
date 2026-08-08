# Deterministic Governance Tests

This directory is for code-driven tests of the Governance Core and deterministic portions of the Governance Skill.

In scope:
- repository/layout/reference validation;
- protocol and lifecycle invariants;
- STATE/EXCHANGE validation and stale-state reconstruction mechanics;
- work-state transitions and blocker semantics;
- progressive-context budgets/routing metadata;
- sequential-disclosure mechanics using synthetic fixtures;
- agent-neutral adapter contract validation;
- Skill discovery canonical-source resolution mechanics;
- Skill approval/digest/permission/dependency validation;
- bootstrap/archive safety.

Out of scope:
- measuring whether an Implementation Agent writes good application code;
- real project feature implementation;
- production/external-service behavior.

Synthetic tasks may exist only to exercise governance state/visibility mechanics.
