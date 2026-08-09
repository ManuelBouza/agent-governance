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
- Testing Skill/capability policy: `docs/TESTING-SKILL-CAPABILITIES.md`.
- Source-product Task Contract policy: `docs/TASK-CONTRACTS.md`.
- Executor handoff policy: `docs/EXECUTOR-HANDOFFS.md`.
- Executable source-maintenance task records: `docs/tasks/`.
- Persisted executor handoffs: `handoffs/`.
- Product decisions and operating instructions: `docs/`.
- Deterministic product tests: `tests/`.
- Agent-facing product evals: `evals/`.

The consumer and maintainer Skills have separate activation/triggers and operational contexts. The consumer Skill MUST NOT depend on modifying or reading this source repository after installation.

## Agent operating model

Repository development uses two agent roles plus the Human Owner. Agent-product names are adapters, never governance roles.

### Human Owner

Final authority over product scope, priorities, risk, public distribution, releases, and overrides.

### ChatGPT — Orchestrator and Markdown Owner

ChatGPT owns product strategy, research synthesis, architectural decisions, work decomposition, acceptance criteria, Task Contracts, agent handoffs, remote review, and all committed Markdown (`*.md`) authoring/editing.

Only ChatGPT may create, rewrite, or persist Markdown instruction/design/decision/task files in normal agentic development. This includes `AGENTS.md`, `README.md`, `docs/**/*.md`, `governance-core/*.md`, Skill Markdown, and Markdown files inside test/eval fixtures.

ChatGPT does not take over implementation merely because a task is difficult. Non-Markdown implementation and verification belong to the Agente de IA Ejecutor.

### Agente de IA Ejecutor — product agnostic

The executor is an abstract role that MAY be fulfilled by OpenCode, Codex, Claude Code, Antigravity, or another compatible local/coding agent. Product identity does not change task semantics, authority, or acceptance.

The Agente de IA Ejecutor owns all authorized non-Markdown technical work, including:
- product implementation code/configuration/assets;
- deterministic test code and test fixtures;
- agent-facing eval code/data/fixtures except committed Markdown;
- execution of tests/evals and collection of verification evidence;
- persisted non-Markdown executor handoffs under `handoffs/`;
- in-scope technical refactoring.

The executor MUST NOT:
- create or edit committed `*.md` files;
- change product scope, architecture, acceptance criteria, or strategic intent;
- weaken or reinterpret tests/evals in a way that contradicts the ChatGPT-approved contract;
- alter an accepted refactor characterization baseline after structural mutation begins unless ChatGPT explicitly authorizes a correction;
- claim acceptance authority merely because tests are green;
- treat local-only/unpushed state as a completed normal handoff.

The executor MAY inspect all Markdown and existing tests/evals as read-only specification/context.

## Source-change procedure invariant

D022, `docs/DEVELOPMENT-WORKFLOW.md`, and `docs/REFACTORING-WORKFLOW.md` define how this source product is changed.

This repository does not install its consumer F0–F6 lifecycle to govern itself.

### Markdown-only changes

ChatGPT performs committed Markdown-only work on a short-lived topic branch from `develop`, reviews the resulting diff, and returns the change to `develop` through PR.

### Executable changes

Executable work uses a contract-first sequence:

1. ChatGPT persists the Task Contract and controlling Markdown/decisions.
2. That planning change is reviewed and integrated into `develop`.
3. Only then may an executor create the implementation topic branch from a `develop` revision containing the exact Task Contract.
4. The executor implements/tests, persists its handoff, commits, and pushes the topic branch.
5. The executor returns only status, handoff path, branch, and pushed HEAD.
6. ChatGPT reviews the remote Task Contract, handoff, base/head identities, complete diff, and evidence through GitHub.
7. Rework uses durable Git/contract revision history rather than chat-only requirements.
8. Only after ChatGPT acceptance does the implementation proceed through PR to `develop`.

The executor does not normally open or merge the implementation PR unless the Task Contract explicitly delegates that mechanical action.

## Persisted task/handoff invariant

- `docs/TASK-CONTRACTS.md` defines the Task Contract format/lifecycle.
- `docs/EXECUTOR-HANDOFFS.md` defines executor return evidence.
- Chat/terminal prompts are transport only and SHOULD contain only repository/branch context plus the exact Task Contract path.
- The executor MUST NOT infer missing task semantics from prior chat history.
- If a prompt conflicts with the persisted Task Contract, the persisted contract controls unless ChatGPT/Human Owner persists an explicit revision/supersession.
- Material objective/scope/acceptance/verification changes require a persisted Task Contract revision before execution continues.
- Before `DONE`, `BLOCKED`, or `PARTIAL`, the executor MUST persist, commit, and push the handoff/current task branch state.

A reviewer must be able to reconstruct what was requested, what the executor reported, and what actually changed from the canonical Git remote alone.

## Testing Skill/capability invariant

D024 and `docs/TESTING-SKILL-CAPABILITIES.md` define the source-product testing Skill boundary.

- the test/eval suite is executable repository code and MUST NOT require model-driven Agent Skill activation;
- the Maintainer Skill, when available, is the only project-owned top-level Skill for source test/eval maintenance;
- it routes progressively to deterministic, property/state-machine, Skill/eval, or security/supply-chain context rather than spawning generic overlapping pytest/testing/TDD Skills;
- a cold executor can bootstrap from `AGENTS.md`, its persisted Task Contract, controlling references, and approved tooling before the Maintainer Skill exists;
- external testing/authoring/security Skills are optional supplemental aids only after applicable supply-chain/coexistence approval and never replace repository-owned verification;
- the Consumer Governance Skill MUST NOT activate for source-product test/eval maintenance.

## File ownership invariant

Normal agentic write ownership is:

- committed `*.md` -> ChatGPT Orchestrator
- all authorized non-Markdown implementation/test/eval/config/assets/handoffs -> Agente de IA Ejecutor

`LICENSE` and repository control files may be additionally protected by product-specific adapters. When a file category genuinely crosses responsibilities, ChatGPT defines the exception explicitly before mutation.

No named executor product gains special authority. Product-specific adapter configuration may enforce these rules mechanically but MUST NOT redefine them.

## Branching invariant

`docs/BRANCHING.md` is authoritative for source-repository branch operation.

- `main` is stable/default and is not a normal development target.
- `develop` integrates the next unreleased state.
- normal work starts on a short-lived topic branch from `develop` and returns to `develop` through PR.
- direct development writes to `main` or `develop` are prohibited.
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
- `docs/TESTING-AND-EVALUATION.md` is normative for verification architecture, isolation, fixtures, grader selection, thresholds, and external technical references.
- External Skill research follows `governance-core/SKILL-DISCOVERY.md` and `governance-core/SKILL-SUPPLY-CHAIN.md`.

## Change discipline

Prefer one coherent, independently reviewable change at a time. Separate behavior-preserving refactors from feature/protocol behavior changes, bug fixes, dependency upgrades, and unrelated cleanup.

For refactors, the RF1 characterization baseline is a remotely auditable checkpoint accepted by ChatGPT before structural mutation.

When changing protocol behavior, ChatGPT updates the smallest relevant Core Markdown module and applicable decisions/design documentation; the Agente de IA Ejecutor updates authorized implementation plus focused tests/evals and runs verification.

Preserve progressive context loading and avoid duplicating normative rules.
