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
- product Decision Records;
- `governance-core/`;
- `governance-skill/`;
- `maintainer-skill/`;
- `tests/` and `evals/`.

It MUST preserve progressive context loading rather than preloading the whole repository.

## Agent roles

The Skill follows the repository operating model:
- ChatGPT Orchestrator owns strategy, architecture, task contracts, review, handoffs, and committed Markdown;
- the product-agnostic Agente de IA Ejecutor owns authorized non-Markdown implementation, tests/evals, fixtures, and verification execution;
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
- bypass release, branch, supply-chain, or role ownership rules.

## Acceptance

The Maintainer Skill is acceptable only if:
1. it activates for source-product maintenance and not ordinary consumer governance;
2. it respects ChatGPT Orchestrator vs Agente de IA Ejecutor ownership;
3. it follows PD/RF and branch policy correctly;
4. it can guide a cold maintainer session without requiring chat history;
5. it never creates a live consumer instance in the source repository;
6. removing the Maintainer Skill does not alter the canonical product itself.
