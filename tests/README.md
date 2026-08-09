# Deterministic Governance Tests

This directory contains code-driven tests of the Governance Core and deterministic portions of both Agent Skills.

The normative testing architecture, external references, isolation rules, fixture policy, property-testing guidance, and release thresholds live in `../docs/TESTING-AND-EVALUATION.md`.

## Agent ownership

The `Agente de IA Ejecutor` owns non-Markdown test implementation, synthetic test fixtures, test execution, and verification evidence under `tests/`. The executor role is product agnostic: OpenCode, Codex, Claude Code, Antigravity, or another compatible coding agent may fulfill it.

ChatGPT owns committed Markdown instructions/specifications and defines the product contract that tests must verify. The executor must not weaken or reinterpret tests in a way that contradicts that contract.

For behavior-preserving refactors, characterization tests accepted during RF1 become a frozen baseline for the refactor unit. Changing that baseline after implementation begins requires explicit ChatGPT authorization.

## Test layers

### Structural and deterministic policy tests
- repository/layout/reference validation;
- protocol/lifecycle/task transition invariants;
- STATE/EXCHANGE validation and stale-state reconstruction mechanics;
- progressive-context budgets/routing metadata;
- sequential-disclosure metadata and blocker/dependency rules;
- agent-neutral adapter contract validation;
- Skill canonical-source/revision/digest/approval/revocation/permission/dependency checks;
- bootstrap/archive overwrite and safety behavior.

Release-blocking deterministic regression tests must pass 100%.

### Property/state-machine tests

Use Hypothesis or an equivalent property-based engine only where generated state/action sequences add material coverage.

Candidate invariant families include:
- monotonic sequence/event identifiers;
- legal terminal-state behavior;
- BLOCKED stopping later disclosure;
- dependency-constrained READY;
- STATE deriving but never inventing strategy;
- rejection of invalid generated event sequences;
- invalidation of Skill approval after material artifact/dependency/permission drift.

Configured release runs must have zero unresolved counterexamples.

### Consumer Governance Skill
- bootstrap/install and overwrite refusal;
- deterministic state/event/validation commands;
- source-repository independence after installation;
- archive safety;
- installed-footprint generation/validation;
- consumer-only operation boundaries.

### Maintainer Skill
- source-repository routing/workflow validation where deterministic;
- refusal to initialize a live consumer instance in this source repository;
- branch-policy/release-routing checks where encoded mechanically;
- separation from consumer-only command surfaces.

### Security/supply-chain deterministic checks
- exact canonical source/revision/content identity;
- revoked/superseded artifact rejection;
- permission/dependency envelope drift;
- unsafe/unexpected configuration fields where applicable;
- external-reference pin/drift checks where applicable.

Dynamic/adversarial cases that require running an agent or executable Skill behavior belong in `evals/` or isolated security harnesses, not ordinary unit tests.

## Fixture policy

Synthetic fixtures represent protocol states, never real business implementations. Minimum families are defined in `../docs/TESTING-AND-EVALUATION.md`.

No production credentials, production service calls, or real consumer business data may be required by this suite.

## Out of scope

- measuring whether an Agente de IA Ejecutor writes good application code;
- real project feature implementation;
- production/external-service behavior.
