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

## Role-aware progressive routing

The Maintainer Skill is one source-maintenance Skill with two internal role routes. It MUST NOT be split into separate top-level `ChatGPT Orchestrator Skill` and `Executor Skill` merely because the repository has two agent roles.

The Skill selects the smallest route required by the active source-maintenance role and task:

```text
maintainer-skill
  -> Orchestrator route
  -> Executor route
```

The routes are context/routing surfaces only. They do not create new authority, change D016 role ownership, or replace repository policy.

### Orchestrator route

Use when the active role is ChatGPT Orchestrator and the work concerns strategy, research synthesis, architecture, Decision Records, Task Contracts, committed Markdown, acceptance/review, executor launch/handoff control, or Orchestrator checkpointing.

The route SHOULD progressively disclose only the required source-maintenance context, such as:

- `AGENTS.md`;
- `docs/orchestrator/CHECKPOINT.md` and `docs/ORCHESTRATOR-CHECKPOINTS.md`;
- `docs/TASK-CONTRACTS.md` and `docs/EXECUTOR-HANDOFFS.md`;
- applicable development/refactoring/branch/release policy;
- the smallest relevant Decision Records and Core modules;
- current Task Contract/review artifacts when the frontier requires them.

The Orchestrator route MUST NOT grant ChatGPT ownership of executor-authorized non-Markdown implementation merely because the Skill can describe that work.

### Executor route

Use when the active role is the product-agnostic Agente de IA Ejecutor and executable source work has been authorized by a persisted Task Contract.

The route SHOULD progressively disclose only the execution context required by that contract, such as:

- `AGENTS.md`;
- exactly the assigned Task Contract and its controlling references;
- `docs/EXECUTOR-HANDOFFS.md`;
- applicable local toolchain/test/eval guidance;
- relevant implementation/test surfaces and synthetic fixtures.

The Executor route MUST NOT expose a parallel strategy layer or allow the executor to edit committed Markdown, expand task scope, redefine acceptance, or infer task semantics from prior chat history.

### Role-routing invariants

```text
role != Skill
Skill routing != authority
Orchestrator route != implementation ownership
Executor route != strategy/acceptance ownership
```

A single session MUST NOT blend the two routes in a way that changes ownership semantics. If the operating role changes, the caller must establish the new role explicitly and reload only the context appropriate to that role.

Standing rules remain canonical in Git. The Skill SHOULD reference repository policy rather than duplicate it in role-local instructions.

A future separate top-level source-maintenance Skill for either role requires new evidence of a distinct non-overlapping intent, measurable routing benefit, acceptable trigger separation, and an explicit Human/Orchestrator architecture decision.

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

The Maintainer Skill is operational assistance, not canonical authority and not a prerequisite for source maintenance or test correctness.

A cold ChatGPT Orchestrator MUST be able to resume source-product orchestration from:
- current `develop`;
- `AGENTS.md`;
- `docs/orchestrator/CHECKPOINT.md`;
- only the additional repository context required by that checkpoint or a concrete conflict.

A cold Agente de IA Ejecutor MUST be able to implement/run an authorized source task from:
- `AGENTS.md`;
- the persisted Task Contract;
- the Task Contract's controlling repository references;
- the approved local development/test tooling.

These bootstrap paths are required so the repository can test and develop the Maintainer Skill before that Skill itself is released. CI and deterministic release checks MUST NOT depend on model-driven Skill activation.

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
- split into role-named top-level Skills without a separately approved architecture change;
- bypass release, branch, supply-chain, toolchain, or role ownership rules.

## Acceptance

The Maintainer Skill is acceptable only if:
1. it activates for source-product maintenance and not ordinary consumer governance;
2. it respects ChatGPT Orchestrator vs Agente de IA Ejecutor ownership;
3. it uses distinct internal Orchestrator and Executor routing without creating additional governance roles or top-level role Skills;
4. each route progressively loads only the context needed by its active role/task and never blends ownership semantics;
5. it follows PD/RF and branch policy correctly;
6. it can guide a cold maintainer session without requiring chat history;
7. both Orchestrator and Executor retain documented no-Skill bootstrap paths;
8. it routes testing/evaluation work to the smallest relevant capability/context without requiring generic overlapping testing Skills;
9. it routes executable source work to the repository-declared local toolchain without making the Skill itself a tool installer;
10. source-product deterministic tests remain executable when the Maintainer Skill is absent/disabled;
11. it never creates a live consumer instance in the source repository;
12. removing the Maintainer Skill does not alter the canonical product itself.
