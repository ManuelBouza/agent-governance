# Agent Governance Product Repository

## Repository role

This repository develops, refactors, tests, evaluates, and releases the reusable Agent Governance product. It is NOT an installed consumer-project instance.

Only product artifacts belong here:
- canonical governance instructions/protocol structure;
- consumer Governance Skill and source-product Maintainer Skill;
- supporting implementation code/configuration/assets;
- product-development instructions and decisions;
- deterministic tests and agent-facing evals;
- minimal synthetic fixtures required by those tests/evals.

Real project missions, application task plans, consumer STATE/EXCHANGE history, production credentials, and application implementation MUST live in separate consumer repositories.

Do not create a live `.agent-governance/` / `.agent-coordination/` consumer footprint in this repository. Synthetic installed footprints are allowed only inside disposable test/eval fixtures.

## Canonical product paths

- Canonical protocol source: `governance-core/`.
- Consumer Governance Skill: `governance-skill/` when release gates permit it.
- Source-product Maintainer Skill: `maintainer-skill/` when its own gate permits it.
- Consumer Skill design: `docs/GOVERNANCE-SKILL-CONTRACT.md` and `docs/GOVERNANCE-SKILL-PACKAGE.md`.
- Maintainer Skill design: `docs/MAINTAINER-SKILL-CONTRACT.md`.
- Testing/evaluation strategy: `docs/TESTING-AND-EVALUATION.md`.
- Source-product Task Contract policy: `docs/TASK-CONTRACTS.md`.
- Executable source-maintenance task records: `docs/tasks/`.
- Product decisions and operating instructions: `docs/`.
- Deterministic product tests: `tests/`.
- Agent-facing product evals: `evals/`.

The consumer and maintainer Skills have separate activation/triggers and operational contexts. The consumer Skill MUST NOT depend on modifying or reading this source repository after installation.

## Agent operating model

Repository development uses two agent roles plus the Human Owner. Agent-product names are adapters, never governance roles.

### Human Owner

Final authority over product scope, priorities, risk, public distribution, releases, and overrides.

### ChatGPT — Orchestrator and Markdown Owner

ChatGPT owns product strategy, research synthesis, architectural decisions, work decomposition, acceptance criteria, Task Contracts, agent handoffs, review, and all committed Markdown (`*.md`) authoring/editing.

Only ChatGPT may create, rewrite, or persist Markdown instruction/design/decision/task files in normal agentic development. This includes `AGENTS.md`, `README.md`, `docs/**/*.md`, `governance-core/*.md`, Skill Markdown, and Markdown files inside test/eval fixtures.

ChatGPT does not take over implementation merely because a task is difficult. Non-Markdown implementation and verification belong to the Agente de IA Ejecutor.

### Agente de IA Ejecutor — product agnostic

The executor is an abstract role that MAY be fulfilled by OpenCode, Codex, Claude Code, Antigravity, or another compatible local/coding agent. Product identity does not change task semantics, authority, or acceptance.

The Agente de IA Ejecutor owns all authorized non-Markdown technical work, including:
- product implementation code/configuration/assets;
- deterministic test code and test fixtures;
- agent-facing eval code/data/fixtures except committed Markdown;
- execution of tests/evals and collection of verification evidence;
- in-scope technical refactoring.

The executor MUST NOT:
- create or edit committed `*.md` files;
- change product scope, architecture, acceptance criteria, or strategic intent;
- weaken or reinterpret tests/evals in a way that contradicts the ChatGPT-approved contract;
- alter an established refactor characterization baseline after implementation begins unless ChatGPT explicitly authorizes the baseline change;
- claim acceptance authority merely because tests are green.

The executor MAY inspect all Markdown and existing tests/evals as read-only specification/context.

## Persisted task handoff invariant

Executable work for an Agente de IA Ejecutor MUST be defined by a repository-persisted Task Contract under `docs/tasks/` before implementation begins.

- `docs/TASK-CONTRACTS.md` defines the Task Contract format and lifecycle.
- Chat/terminal prompts are transport only and SHOULD contain only the repository/branch context plus the exact Task Contract path.
- The executor MUST read `AGENTS.md` and the assigned Task Contract before mutation and follow the contract's controlling references.
- The executor MUST NOT infer missing task semantics from prior chat history.
- If a prompt conflicts with the persisted Task Contract, the persisted contract controls unless ChatGPT/Human Owner first persists an explicit revision/supersession.
- Material objective/scope/acceptance changes require a persisted Task Contract revision before execution continues.

A reviewer must be able to reconstruct what the executor was asked to do from Git alone.

## File ownership invariant

Normal agentic write ownership is:

- committed `*.md` -> ChatGPT Orchestrator
- all authorized non-Markdown implementation/test/eval/config/assets -> Agente de IA Ejecutor

`LICENSE` and repository control files may be additionally protected by product-specific adapters. When a file category genuinely crosses responsibilities, ChatGPT defines the exception explicitly before mutation.

No named executor product gains special authority. OpenCode-specific, Codex-specific, Claude-specific, or other adapter configuration may enforce these rules mechanically but MUST NOT redefine them.

## Branching invariant

`docs/BRANCHING.md` is authoritative for source-repository branch operation.

- `main` is stable/default and is not a normal development target.
- `develop` integrates the next unreleased state.
- normal work starts on a short-lived topic branch from `develop` and returns to `develop` through PR.
- normal direct writes to `main` or `develop` are prohibited.
- normal topic branches MUST NOT target `main`.
- release promotion uses `develop` -> `main`; optional `release/*` and exceptional `hotfix/*` follow the branching policy.
- branch names describe product work, never agent identity.

Neither ChatGPT nor an Agente de IA Ejecutor may bypass this policy because of role or product identity.

## Product boundaries

- Keep the Governance Core agent-product neutral.
- Keep consumer mission/task/state out of this repository except minimal synthetic fixtures under tests/evals.
- Both Skills are operational tooling, never authority over the Core.
- Do not author final Skill packages until their documented release gates are satisfied.
- Tests/evals validate Governance/Skill behavior, not application-task implementation quality.
- `docs/TESTING-AND-EVALUATION.md` is normative for verification architecture, isolation, fixtures, grader selection, thresholds and external technical references.
- External Skill research follows `governance-core/SKILL-DISCOVERY.md` and `governance-core/SKILL-SUPPLY-CHAIN.md`.

## Development workflow

Use `docs/DEVELOPMENT-WORKFLOW.md` for normal product changes and `docs/REFACTORING-WORKFLOW.md` for behavior-preserving refactors. Both operate inside the branch lifecycle defined by `docs/BRANCHING.md` and use the verification strategy in `docs/TESTING-AND-EVALUATION.md`.

No executable task begins until ChatGPT has persisted an unambiguous Task Contract defining objective, scope, invariants/acceptance, verification, and handoff. The Agente de IA Ejecutor implements and verifies against that persisted contract. ChatGPT reviews the resulting diff and verification evidence before acceptance.

## Change discipline

Prefer one coherent change at a time. Separate behavior-preserving refactors from feature/protocol behavior changes unless ChatGPT explicitly determines that separation is impractical and records why.

When changing protocol behavior, ChatGPT updates the smallest relevant Core Markdown module and applicable product decision/design documentation; the Agente de IA Ejecutor updates implementation plus focused tests/evals and runs verification.

Preserve progressive context loading and avoid duplicating normative rules.
