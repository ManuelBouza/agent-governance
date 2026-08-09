# Product Development Workflow

Status: ACTIVE

## Purpose

Define how agents develop the `agent-governance` source product without turning this repository into a consumer instance of its own Governance Core.

This is a repository-maintenance workflow, not an installed `.agent-coordination/` lifecycle. Real consumer-project governance is exercised only in separate repositories or synthetic disposable fixtures.

All repository mutation occurs inside the branch lifecycle defined by `docs/BRANCHING.md`.

## Roles

- Human Owner: final authority.
- ChatGPT: Orchestrator, strategy/specification owner, architectural reviewer, exclusive normal author of committed Markdown, and Task Contract owner.
- Agente de IA Ejecutor: product-agnostic coding-agent role fulfilled by OpenCode, Codex, Claude Code, Antigravity, or another compatible agent; owns authorized non-Markdown implementation, tests/evals, their execution, and persisted executor handoffs.

`AGENTS.md` is the normative repository adapter for these responsibilities.

## Persisted task precondition

Executable work MUST have a repository-persisted Task Contract before an Agente de IA Ejecutor begins implementation.

`docs/TASK-CONTRACTS.md` defines the format and lifecycle. Active source-maintenance contracts live under `docs/tasks/`.

The external agent-launch prompt is transport only. It SHOULD contain the minimum repository/branch context plus the exact Task Contract path and MUST NOT become the sole source of objective, scope, acceptance, or verification semantics.

The executor reads `AGENTS.md`, the assigned Task Contract, and only the controlling references required by that contract. It MUST NOT depend on prior chat history to reconstruct missing task intent.

Material changes to objective, scope, acceptance, or required verification require ChatGPT to persist a Task Contract revision before implementation continues.

## Persisted executor-return precondition

Before the executor claims `DONE`, `BLOCKED`, or `PARTIAL`, it MUST persist its technical result under `handoffs/` according to `docs/EXECUTOR-HANDOFFS.md` and the path specified by the Task Contract.

The persisted executor handoff, not chat output, is the authoritative executor-reported result. It must identify the exact branch/HEAD/base, changed files, verification commands/results, environment details, configuration/dependency changes, unresolved issues, and recommended next work required by the contract.

The executor's visible response SHOULD contain only status, handoff path, branch, and HEAD so ChatGPT can fetch and review the durable record.

## Branch precondition

Normal work MUST NOT begin by writing directly to `main` or `develop`.

Before mutation:
1. start from current `develop`;
2. create the appropriate short-lived topic branch defined by `docs/BRANCHING.md`;
3. keep the complete coherent PD change on that branch;
4. integrate by PR back to `develop` after PD5 acceptance.

Release/hotfix exceptions follow `docs/BRANCHING.md` and `docs/RELEASES.md`.

## PD0 — Frame Change

ChatGPT determines:
- requested product outcome;
- whether the change is protocol/instruction, executable tooling, test/eval infrastructure, refactor, release work, or mixed;
- scope and exclusions;
- affected public compatibility surface;
- whether a Decision Record is required;
- appropriate branch class/target.

Do not create consumer mission/workplan/state records for repository development.

## PD1 — Persist Task Contract

For every executable handoff, ChatGPT creates or updates the exact Task Contract under `docs/tasks/` before implementation begins.

The contract defines the minimum durable execution semantics:
- objective/result;
- controlling references;
- authorized scope and explicit exclusions;
- architecture/invariants/compatibility constraints;
- branch/base requirements;
- expected executor handoff path;
- acceptance criteria;
- verification/evidence requirements;
- stop/escalation conditions;
- expected executor handoff.

For protocol/instruction changes, ChatGPT also authors the canonical Markdown changes itself. For executable changes, the contract states required outcomes without prescribing unnecessary implementation mechanics.

The Task Contract is the audit record of what was requested. It is not rewritten after implementation starts merely to match the resulting implementation.

## PD2 — Establish Verification

The Agente de IA Ejecutor derives the verification strategy from the persisted Task Contract before implementing behavior that requires executable verification.

Depending on change type, the executor:
- adds/updates deterministic tests;
- adds/updates agent-facing eval cases;
- establishes a pre-change baseline when required;
- identifies expected failing tests for intentional new behavior;
- records exact commands and relevant evidence.

Tests/evals must test the approved contract, not redefine it. A test/eval change that materially changes required behavior or acceptance meaning requires ChatGPT review and, when material, a persisted Task Contract revision before proceeding.

For behavior-preserving refactors, follow `REFACTORING-WORKFLOW.md`; the pre-change characterization baseline must be green before implementation begins.

Tests/evals assess this governance product, not the quality of application tasks in consumer repositories.

## PD3 — Implement

For executable product changes, the Agente de IA Ejecutor receives the Task Contract path and necessary read-only repository context.

The executor:
- edits authorized non-Markdown implementation code/config/assets;
- authors/updates applicable non-Markdown tests/evals;
- does not edit committed Markdown;
- does not change strategic scope or acceptance;
- resolves normal technical implementation and test-design choices autonomously inside the contract.

For Markdown-only product changes, this phase is performed by ChatGPT and no executor implementation is required, although executable verification may still be delegated through a Task Contract.

For test/eval-only work, the Agente de IA Ejecutor performs the authorized changes and execution.

## PD4 — Verify and Persist Handoff

The Agente de IA Ejecutor runs the applicable deterministic tests/evals against the resulting implementation and persists reproducible evidence in the task's executor handoff artifact.

If verification fails:
- implementation or test implementation defect -> executor diagnoses and fixes within the approved contract;
- specification/acceptance ambiguity -> persist a `BLOCKED` handoff and stop for ChatGPT;
- proposed behavior change discovered during a refactor -> persist the situation, stop refactor, and re-enter PD0 as a behavior-changing change.

The executor MUST NOT make tests green by weakening the ChatGPT-approved behavioral contract. If a previously established baseline must change, ChatGPT must explicitly authorize that change and persist any material contract revision first.

For higher-risk changes ChatGPT MAY request a fresh executor session or a second compatible executor product to rerun verification, but this remains the same `Agente de IA Ejecutor` role and does not create a new governance role.

## PD5 — Orchestrator Review

ChatGPT reads and reviews:
- the persisted Task Contract;
- the persisted executor handoff;
- the actual implementation/test/eval diff;
- architectural consistency;
- role-boundary compliance;
- verification evidence;
- required Markdown/documentation/Decision Records;
- public compatibility and supply-chain implications;
- branch/PR target compliance.

A green suite is necessary when applicable but is not sufficient if the change violates architecture or specification. The executor handoff is evidence, not acceptance authority; ChatGPT verifies it against Git and the contract.

## PD6 — Integrate

Integrate only when PD5 accepts the change.

Normal integration is topic branch -> `develop` through PR. Prefer squash merge for one coherent accepted topic change.

Promotion of `develop` to `main` is a separate release/stability action governed by `docs/BRANCHING.md` and `docs/RELEASES.md` and normally uses a merge commit.

## Handoff Invariants

- ChatGPT -> Agente de IA Ejecutor: minimal launch prompt pointing to the persisted Task Contract only after the contract is sufficiently complete.
- Agente de IA Ejecutor -> repository: persist the executor handoff under `handoffs/` after verification and before claiming status.
- Agente de IA Ejecutor -> ChatGPT: minimal status pointer containing handoff path, branch, and HEAD.
- ChatGPT -> Agente de IA Ejecutor again when technical rework is required, with a persisted contract revision first if objective/scope/acceptance materially changes.
- ChatGPT -> Human Owner when product scope/risk/public compatibility requires final authority.

No executor product is privileged. Switching OpenCode -> Codex -> Claude Code -> another compatible executor does not change the role contract or task semantics.
