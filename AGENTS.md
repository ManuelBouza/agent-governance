# Agent Governance Product Repository

## Repository role

This repository develops, refactors, and tests the reusable Agent Governance product. It is NOT an installed consumer-project instance.

Only product artifacts belong here:
- canonical governance instructions/protocol structure;
- Governance Skill implementation and supporting code/configuration;
- product-development instructions and decisions;
- deterministic tests and agent-facing evals;
- minimal synthetic fixtures required by those tests/evals.

Real project missions, application task plans, consumer STATE/EXCHANGE history, production credentials, and application implementation MUST live in separate consumer repositories.

Do not create a live `.agent-governance/` / `.agent-coordination/` consumer footprint in this repository. Synthetic installed footprints are allowed only inside disposable test/eval fixtures.

## Canonical product paths

- Canonical protocol source: `governance-core/`.
- Governance Skill implementation: `governance-skill/` when release gates permit it.
- Governance Skill design: `docs/GOVERNANCE-SKILL-CONTRACT.md` and `docs/GOVERNANCE-SKILL-PACKAGE.md`.
- Product decisions and operating instructions: `docs/`.
- Deterministic product tests: `tests/`.
- Agent-facing product evals: `evals/`.

## Agent operating roles

Repository development uses three distinct agent responsibilities plus the Human Owner.

### Human Owner

Final authority over product scope, priorities, risk, public distribution, releases, and overrides.

### ChatGPT — Orchestrator and Markdown Owner

ChatGPT owns product strategy, research synthesis, architectural decisions, work decomposition, acceptance criteria, agent handoffs, and all committed Markdown (`*.md`) authoring/editing.

Only ChatGPT may create, rewrite, or persist Markdown instruction/design/decision files in normal agentic development. This includes `AGENTS.md`, `README.md`, `docs/**/*.md`, `governance-core/*.md`, and Markdown files inside test/eval fixtures.

ChatGPT MUST NOT author or modify test/eval implementation code merely to make an implementation pass. Test ownership belongs to Codex.

### Implementation Executor — OpenCode or another compatible coding agent

The executor owns non-test implementation code/configuration/assets required by an approved task. OpenCode is the default adapter when used, but product task semantics MUST remain executor-neutral.

The executor MUST NOT:
- create or edit committed `*.md` files;
- create or edit `tests/**` or `evals/**` test/eval implementation;
- weaken, delete, skip, rewrite, or reinterpret failing tests to make implementation pass;
- declare test success without Codex verification;
- change product scope or acceptance criteria.

It MAY inspect Markdown and tests/evals as read-only context when the current task requires them.

### Codex — Test and Verification Owner

Codex owns the design, authoring, modification, and execution of deterministic tests and agent-facing evals for this repository.

Codex MAY inspect all product code and Markdown required to derive tests, but during normal verification it MUST NOT modify product implementation code or committed Markdown. A product-code defect discovered by tests is returned to the Implementation Executor; a specification/instruction ambiguity is returned to ChatGPT.

Codex is the authoritative agentic source for test execution evidence. Green status claimed by an implementation executor alone is insufficient for acceptance.

## File ownership invariant

Normal agentic write ownership is exclusive:

- `*.md` -> ChatGPT
- `tests/**`, `evals/**` test/eval code and fixtures -> Codex
- product implementation code/config/assets outside those boundaries -> Implementation Executor

When a file category genuinely crosses responsibilities, ChatGPT defines the exception explicitly before mutation. No agent may silently take over another role's write surface.

## Product boundaries

- Keep the Governance Core agent-product neutral.
- Keep consumer mission/task/state out of this repository except minimal synthetic fixtures under tests/evals.
- The Governance Skill is operational tooling, never authority over the Core.
- Do not author final `governance-skill/SKILL.md` until the documented release gate is satisfied.
- Tests/evals validate Governance/Skill behavior, not application-task implementation quality.
- External Skill research follows `governance-core/SKILL-DISCOVERY.md` and `governance-core/SKILL-SUPPLY-CHAIN.md`.

## Development workflow

Use `docs/DEVELOPMENT-WORKFLOW.md` for normal product changes and `docs/REFACTORING-WORKFLOW.md` for behavior-preserving refactors.

No implementation task begins until ChatGPT has defined an unambiguous objective, scope, invariants/acceptance, and role handoff. No change is accepted until the Codex-owned verification phase is complete when tests/evals apply.

## Change discipline

Prefer one coherent change at a time. Separate behavior-preserving refactors from feature/protocol behavior changes unless ChatGPT explicitly determines that separation is impractical and records why.

When changing protocol behavior, ChatGPT updates the smallest relevant Core Markdown module and applicable product decision/design documentation; Codex updates focused tests/evals; the Implementation Executor changes only implementation artifacts needed by the task.

Preserve progressive context loading and avoid duplicating normative rules.
