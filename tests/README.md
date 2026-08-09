# Deterministic Governance Tests

This directory contains code-driven tests of the Governance Core and deterministic portions of the Governance Skill.

## Agent ownership

The `Agente de IA Ejecutor` owns non-Markdown test implementation, synthetic test fixtures, test execution, and verification evidence under `tests/`. The executor role is product agnostic: OpenCode, Codex, Claude Code, Antigravity, or another compatible coding agent may fulfill it.

ChatGPT owns committed Markdown instructions/specifications and defines the product contract that tests must verify. The executor must not weaken or reinterpret tests in a way that contradicts that contract.

For behavior-preserving refactors, characterization tests accepted during RF1 become a frozen baseline for the refactor unit. Changing that baseline after implementation begins requires explicit ChatGPT authorization.

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
