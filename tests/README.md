# Deterministic Governance Tests

This directory contains code-driven tests of the Governance Core and deterministic portions of both Agent Skills.

## Agent ownership

The `Agente de IA Ejecutor` owns non-Markdown test implementation, synthetic test fixtures, test execution, and verification evidence under `tests/`. The executor role is product agnostic: OpenCode, Codex, Claude Code, Antigravity, or another compatible coding agent may fulfill it.

ChatGPT owns committed Markdown instructions/specifications and defines the product contract that tests must verify. The executor must not weaken or reinterpret tests in a way that contradicts that contract.

For behavior-preserving refactors, characterization tests accepted during RF1 become a frozen baseline for the refactor unit. Changing that baseline after implementation begins requires explicit ChatGPT authorization.

## Test surfaces

Tests SHOULD remain distinguishable by the product surface they prove:

### Governance Core
- repository/layout/reference validation;
- protocol and lifecycle invariants;
- STATE/EXCHANGE validation and stale-state reconstruction mechanics;
- work-state transitions and blocker semantics;
- progressive-context budgets/routing metadata;
- sequential-disclosure mechanics using synthetic fixtures;
- agent-neutral adapter contract validation;
- Skill discovery canonical-source resolution mechanics;
- Skill approval/digest/permission/dependency validation.

### Consumer Governance Skill
- bootstrap/install and overwrite refusal;
- deterministic state/event/validation commands;
- source-repository independence after installation;
- archive safety;
- installed-footprint generation/validation;
- consumer-only operation boundaries.

### Maintainer Skill
- source-repository routing and workflow validation where deterministic;
- refusal to initialize a live consumer instance in this source repository;
- branch-policy and release-routing checks where encoded mechanically;
- separation from consumer-only command surfaces.

## Out of scope

- measuring whether an Implementation Agent writes good application code;
- real project feature implementation;
- production/external-service behavior.

Synthetic tasks may exist only to exercise governance state/visibility mechanics.
