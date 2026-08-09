# Maintainer Skill Functional Contract

Status: DESIGN-APPROVED

## Purpose

Define the Agent Skill used only for developing, refactoring, testing, evaluating, and releasing the canonical `agent-governance` source product.

This Skill is NOT the consumer Governance Skill and MUST NOT install or operate a live consumer-project governance instance in this repository.

## Activation boundary

Trigger for work such as:
- changing Governance Core architecture or instructions;
- implementing/refactoring source-product tooling;
- creating or modifying deterministic tests/evals;
- running product verification;
- applying `docs/DEVELOPMENT-WORKFLOW.md` or `docs/REFACTORING-WORKFLOW.md`;
- preparing releases or migration artifacts;
- validating source-product structure and public distribution readiness.

Do not trigger merely because another repository uses Agent Governance.

## Repository context

The Skill MAY route to source-specific context including:
- `AGENTS.md`;
- `docs/DEVELOPMENT-WORKFLOW.md`;
- `docs/REFACTORING-WORKFLOW.md`;
- `docs/BRANCHING.md`;
- `docs/RELEASES.md`;
- `docs/TESTING-AND-EVALUATION.md`;
- `docs/TESTING-SKILL-CAPABILITIES.md`;
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`;
- `docs/decisions/D023-python-testing-stack.md`;
- `docs/decisions/D024-testing-skill-capability-model.md`;
- `docs/decisions/D025-local-development-toolchain.md`;
- assigned `docs/tasks/` Task Contracts and `handoffs/` policy;
- product Decision Records;
- `governance-core/`;
- `governance-skill/`;
- `maintainer-skill/`;
- `tests/` and `evals/`.

It MUST preserve progressive context loading rather than preloading the whole repository.

## Testing/evaluation capability routing

The Maintainer Skill is the single project-owned top-level Skill for source-product testing/evaluation work. It does not replace the test runner and source tests MUST remain runnable without the Skill.

When test/eval maintenance is in scope, the Skill SHOULD route progressively to the smallest relevant capability area:

1. **Deterministic test maintenance** — Python/pytest source-product invariants, synthetic fixtures, local deterministic verification and persisted evidence.
2. **Property/state-machine testing** — Hypothesis stateful/property work only when D019 Layer 2 applies.
3. **Skill/eval maintenance** — trigger corpora, near misses, repeated clean-context trials, baseline comparison and grader selection.
4. **Security/supply-chain testing** — identity/digest/envelope checks plus adversarial Skill fixtures and isolated dynamic checks when separately authorized.

These capability areas SHOULD be represented through on-demand references/resources inside the eventual Maintainer Skill package rather than separate broad top-level testing Skills unless future trigger/eval evidence demonstrates a distinct, non-overlapping need.

The Maintainer Skill MUST NOT require an external generic pytest/testing/TDD Skill to perform normal source-product testing. External Skills may be supplemental only after approval under the applicable discovery/supply-chain and coexistence policies.

## Local toolchain routing

When executable source work requires local setup/verification, the Maintainer Skill SHOULD route to `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md` instead of embedding product-specific installation recipes in its top-level activation instructions.

The Maintainer Skill must preserve these boundaries:
- Git/uv/Python/pytest/Ruff are source-maintainer tooling defined by D023/D025;
- the executor host itself remains product-neutral and external to the repository dependency graph;
- GitHub CLI is optional when normal Git authentication already works;
- Ruff must not be allowed to rewrite ChatGPT-owned Markdown;
- source-maintainer tool choices must not be projected automatically into consumer repositories.

Detailed tool commands should be loaded only for tasks that actually execute/verify code.

## Bootstrap / no-Skill operation

The Maintainer Skill is operational assistance, not canonical authority and not a prerequisite for test correctness.

A cold Agente de IA Ejecutor MUST be able to implement/run an authorized source test task from:
- `AGENTS.md`;
- the persisted Task Contract;
- the Task Contract's controlling repository references;
- the approved local development/test tooling.

This bootstrap path is required so the repository can test and develop the Maintainer Skill before that Skill itself is released. CI and deterministic release checks MUST NOT depend on model-driven Skill activation.

## Agent roles

The Skill follows the repository operating model:
- ChatGPT Orchestrator owns strategy, architecture, task contracts, review, handoffs, and committed Markdown;
- the product-agnostic Agente de IA Ejecutor owns authorized non-Markdown implementation, tests/evals, fixtures, executable configuration, and verification execution;
- Human Owner retains final authority.

No executor product receives special governance status.

## Branch discipline

All normal product changes follow `docs/BRANCHING.md`:
- `main` stable;
- `develop` integration;
- work on short-lived topic branches;
- no normal direct writes to `main` or `develop`;
- normal PR target is `develop`;
- promotion to `main` occurs only through release/stability review.

## Explicitly out of scope

The Maintainer Skill MUST NOT:
- initialize consumer `MISSION`, `WORKPLAN`, `STATE`, or `EXCHANGE` in this source repository;
- treat this source repository as a real consumer instance;
- implement application/business features for unrelated consumer projects;
- redefine Governance Core authority inside Skill-local instructions;
- become a mandatory runtime dependency for deterministic source tests;
- duplicate generic pytest/Hypothesis/uv/Ruff documentation when task-specific repository guidance is sufficient;
- impose the source repository's uv/Python/Ruff stack on consumer projects;
- bypass release, branch, supply-chain, toolchain, or role ownership rules.

## Acceptance

The Maintainer Skill is acceptable only if:
1. it activates for source-product maintenance and not ordinary consumer governance;
2. it respects ChatGPT Orchestrator vs Agente de IA Ejecutor ownership;
3. it follows PD/RF and branch policy correctly;
4. it can guide a cold maintainer session without requiring chat history;
5. it routes testing/evaluation work to the smallest relevant capability/context without requiring generic overlapping testing Skills;
6. it routes executable source work to the repository-declared local toolchain without making the Skill itself a tool installer;
7. source-product deterministic tests remain executable when the Maintainer Skill is absent/disabled;
8. it never creates a live consumer instance in the source repository;
9. removing the Maintainer Skill does not alter the canonical product itself.
