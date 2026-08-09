# Deterministic Governance Tests

This directory is for code-driven tests of the Governance Core and deterministic portions of the Governance Skill.

## Agent ownership

Codex is the normal write owner of test implementation and synthetic test fixtures under `tests/`, and is responsible for executing the deterministic test suite and reporting verification evidence.

ChatGPT owns Markdown instructions/specifications in this directory. Implementation Executors may inspect tests read-only but must not create, rewrite, weaken, delete, or skip them to make implementation pass.

A failing test caused by product implementation is returned to the Implementation Executor. A genuine test defect may be corrected by Codex only when the approved product contract or pre-change characterization proves the test is wrong. Specification ambiguity is returned to ChatGPT.

## In scope

- repository/layout/reference validation;
- protocol and lifecycle invariants;
- STATE/EXCHANGE validation and stale-state reconstruction mechanics;
- work-state transitions and blocker semantics;
- progressive-context budgets/routing metadata;
- sequential-disclosure mechanics using synthetic fixtures;
- agent-neutral adapter contract validation;
- Skill discovery canonical-source resolution mechanics;
- Skill approval/digest/permission/dependency validation;
- bootstrap/archive safety;
- characterization/regression coverage required by `docs/REFACTORING-WORKFLOW.md`.

## Out of scope

- measuring whether an Implementation Agent writes good application code;
- real project feature implementation;
- production/external-service behavior.

Synthetic tasks may exist only to exercise governance state/visibility mechanics.
