# Deterministic Governance Tests

This directory contains code-driven tests of the Governance Core and deterministic portions of both Agent Skills.

The normative testing architecture, external references, isolation rules, fixture policy, property-testing guidance, and release thresholds live in `../docs/TESTING-AND-EVALUATION.md`. The concrete language/framework decision is `../docs/decisions/D023-python-testing-stack.md`. Testing Skill/capability boundaries are defined by `../docs/TESTING-SKILL-CAPABILITIES.md` and D024.

## Canonical test stack

Repository-owned deterministic tests use:
- Python `>=3.13`;
- pytest `>=9,<10` as the canonical runner/framework;
- `python -m pytest` as the canonical framework-level invocation;
- Python standard-library facilities first for filesystem, JSON/JSONL, subprocess, digest, and fixture manipulation;
- Hypothesis `>=6,<7` only for tasks that genuinely require property/state-machine coverage.

T001's first deterministic harness should require pytest only unless its approved scope is revised to include stateful/property testing. The local environment manager, dependency installation CLI, and lock strategy are defined separately by the development-toolchain decision.

## Skill boundary

No Agent Skill is required to execute this suite.

When available, the Maintainer Skill may route a source-maintenance task to the relevant testing context, but test correctness, CI execution, and release verification must remain possible from repository contracts plus approved tooling alone.

Do not create or require generic pytest/testing/TDD Skills solely to run these tests. External testing/security Skills are supplemental only after applicable governance approval and cannot replace repository-owned assertions.

## Agent ownership

The `Agente de IA Ejecutor` owns non-Markdown test implementation, synthetic test fixtures, test execution, and verification evidence under `tests/`. The executor role is product agnostic: OpenCode, Codex, Claude Code, Antigravity, or another compatible coding agent may fulfill it.

ChatGPT owns committed Markdown instructions/specifications and defines the product contract that tests must verify. The executor must not weaken or reinterpret tests in a way that contradicts that contract.

For behavior-preserving refactors, characterization tests accepted during RF1 become a frozen baseline for the refactor unit. Changing that baseline after implementation begins requires explicit ChatGPT authorization.

## Test style

- Prefer pytest functions with plain `assert`.
- Use pytest fixtures for reusable setup instead of mutable global state.
- Use `tmp_path` / `tmp_path_factory` plus `pathlib.Path` for disposable repository/filesystem fixtures.
- Use pytest parametrization for input -> expected-decision policy matrices.
- Keep protocol data as data files (for example JSON/JSONL) where that is clearer than embedding it in Python source.
- Use `hypothesis.stateful.RuleBasedStateMachine` only when generated action sequences materially improve coverage.

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

Use Hypothesis only where generated state/action sequences add material coverage.

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
