# Deterministic Governance Tests

This directory contains code-driven tests of the Governance Core and deterministic portions of both Agent Skills.

The normative testing architecture, external references, isolation rules, fixture policy, property-testing guidance, and release thresholds live in `../docs/TESTING-AND-EVALUATION.md`. The concrete language/framework decision is `../docs/decisions/D023-python-testing-stack.md`. Testing Skill/capability boundaries are defined by `../docs/TESTING-SKILL-CAPABILITIES.md` and D024. Source local tooling and locked commands are defined by `../docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md` and D025. Ecosystem/SDD/Skill coexistence is defined by `../governance-core/COEXISTENCE.md` and D026.

## Canonical test stack

Repository-owned deterministic tests use:
- Python `>=3.13`;
- pytest `>=9,<10` as the canonical runner/framework;
- `python -m pytest` as the framework-level invocation;
- uv as the source-repository Python/environment/dependency/lock wrapper;
- Ruff `>=0.16,<0.17` for Python lint/format verification;
- Python standard-library facilities first for filesystem, JSON/JSONL, subprocess, digest, and fixture manipulation;
- Hypothesis `>=6,<7` only for tasks that genuinely require property/state-machine coverage.

T001's first deterministic harness requires pytest and Ruff only unless its approved scope is revised to include stateful/property testing.

After repository configuration/lock files exist, the canonical local verification path is:

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

Ruff configuration MUST exclude committed Markdown so executor tooling cannot mutate ChatGPT-owned `.md` files.

## Skill boundary

No Agent Skill is required to execute this suite.

When available, the Maintainer Skill may route a source-maintenance task to the relevant testing context, but test correctness, CI execution, and release verification must remain possible from repository contracts plus approved tooling alone.

Do not create or require generic pytest/testing/TDD Skills solely to run these tests. External testing/security Skills are supplemental only after applicable governance approval and cannot replace repository-owned assertions.

## Agent ownership

The `Agente de IA Ejecutor` owns non-Markdown test implementation, synthetic test fixtures, test execution, executable test configuration, and verification evidence under the scope authorized by a Task Contract. The executor role is product agnostic: OpenCode, Codex, Claude Code, Antigravity, or another compatible coding agent may fulfill it.

ChatGPT owns committed Markdown instructions/specifications and defines the product contract that tests must verify. The executor must not weaken or reinterpret tests in a way that contradicts that contract.

For behavior-preserving refactors, characterization tests accepted during RF1 become a frozen baseline for the refactor unit. Changing that baseline after implementation begins requires explicit ChatGPT authorization.

## Test style

- Prefer pytest functions with plain `assert`.
- Use pytest fixtures for reusable setup instead of mutable global state.
- Use `tmp_path` / `tmp_path_factory` plus `pathlib.Path` for disposable repository/filesystem fixtures.
- Use pytest parametrization for input -> expected-decision policy matrices.
- Keep protocol data as data files (for example JSON/JSONL) where that is clearer than embedding it in Python source.
- Use `hypothesis.stateful.RuleBasedStateMachine` only when generated action sequences materially improve coverage.
- Do not add undeclared packages to `.venv`; dependency truth lives in `pyproject.toml` and committed `uv.lock`.

## Test layers

### Structural and deterministic policy tests
- repository/layout/reference validation;
- protocol/lifecycle/task transition invariants;
- STATE/EXCHANGE validation and stale-state reconstruction mechanics;
- CAPABILITIES/coexistence inventory shape and non-authority constraints;
- progressive-context budgets/routing metadata;
- sequential-disclosure metadata and blocker/dependency rules;
- agent-neutral adapter contract validation;
- Skill canonical-source/revision/digest/approval/revocation/permission/dependency checks;
- host-selected Skill identity vs exact approved artifact checks;
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
- invalidation of Skill approval after material artifact/dependency/permission drift;
- coexistence entries returning to unresolved state after material provider/selected-artifact drift.

Configured release runs must have zero unresolved counterexamples.

### Consumer Governance Skill
- bootstrap/install and overwrite refusal;
- deterministic state/event/validation commands;
- source-repository independence after installation;
- archive safety;
- installed-footprint generation/validation;
- consumer-only operation boundaries;
- non-destructive coexistence with pre-existing SDD/Skill/instruction fixtures;
- reference/adapt behavior instead of duplicate native specs/plans/tasks;
- `REUSE|ADAPT|COEXIST|MISSING|CONFLICT` inventory validation;
- no-SDD/no-third-party-Skill operation;
- same-name Skill shadowing and exact-approved-artifact matching.

### Maintainer Skill
- source-repository routing/workflow validation where deterministic;
- refusal to initialize a live consumer instance in this source repository;
- branch-policy/release-routing checks where encoded mechanically;
- separation from consumer-only command surfaces.

### Security/supply-chain deterministic checks
- exact canonical source/revision/content identity;
- revoked/superseded artifact rejection;
- permission/dependency envelope drift;
- same-name shadowing selecting an unapproved artifact;
- unsafe/unexpected configuration fields where applicable;
- external-reference pin/drift checks where applicable.

Dynamic/adversarial cases that require running an agent or executable Skill behavior belong in `evals/` or isolated security harnesses, not ordinary unit tests.

## Coexistence fixture families

Synthetic deterministic fixtures SHOULD cover at least:
- no SDD / no third-party Skill ecosystem;
- Gentle-AI-like project assets/registry without requiring Gentle-AI itself;
- Spec Kit-like spec/plan/tasks ownership;
- OpenSpec-like specs/change artifacts;
- generic custom SDD with project-native task ownership;
- same-name project/user Skill collision with deterministic shadowing;
- semantic governance/orchestration Skill overlap;
- shared `AGENTS.md`/agent configuration containing third-party managed sections;
- provider/version/path drift that invalidates a prior capability inventory entry.

Fixtures model public integration shapes only. Tests must not depend on installing or calling the real external product unless a later isolated compatibility task explicitly requires it.

## Network policy

Environment provisioning may need network access to obtain the authorized Python/dependencies on a fresh workstation. Ordinary deterministic test execution itself must not require production/external service access unless a later Task Contract explicitly authorizes such a surface.

## Fixture policy

Synthetic fixtures represent protocol states and ecosystem boundaries, never real business implementations. Minimum families are defined in `../docs/TESTING-AND-EVALUATION.md` and the coexistence requirements above.

No production credentials, production service calls, or real consumer business data may be required by this suite.

## Out of scope

- measuring whether an Agente de IA Ejecutor writes good application code;
- real project feature implementation;
- production/external-service behavior.
