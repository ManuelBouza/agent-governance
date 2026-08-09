# Product Development Workflow

Status: ACTIVE

## Purpose

Define how agents develop the `agent-governance` source product without turning this repository into a consumer instance of its own Governance Core.

This is a repository-maintenance workflow, not an installed `.agent-coordination/` lifecycle. Real consumer-project governance is exercised only in separate repositories or synthetic disposable fixtures.

## Roles

- Human Owner: final authority.
- ChatGPT: Orchestrator, strategy/specification owner, architectural reviewer, and exclusive normal author of committed Markdown.
- Agente de IA Ejecutor: product-agnostic coding-agent role fulfilled by OpenCode, Codex, Claude Code, Antigravity, or another compatible agent; owns authorized non-Markdown implementation, tests/evals, and their execution.

`AGENTS.md` is the normative repository adapter for these responsibilities.

## PD0 — Frame Change

ChatGPT determines:
- requested product outcome;
- whether the change is protocol/instruction, executable tooling, test/eval infrastructure, refactor, release work, or mixed;
- scope and exclusions;
- affected public compatibility surface;
- whether a Decision Record is required.

Do not create consumer mission/workplan/state records for repository development.

## PD1 — Specify Contract

ChatGPT persists the minimum Markdown needed to make the change unambiguous:
- objective/result;
- controlling architecture/invariants;
- compatibility constraints;
- acceptance criteria;
- executor handoff and verification requirements.

For protocol/instruction changes, ChatGPT authors the canonical Markdown change itself. For executable changes, the specification describes required behavior without prescribing unnecessary implementation mechanics.

## PD2 — Establish Verification

The Agente de IA Ejecutor derives the verification strategy from the approved ChatGPT contract before implementing behavior that requires executable verification.

Depending on change type, the executor:
- adds/updates deterministic tests;
- adds/updates agent-facing eval cases;
- establishes a pre-change baseline when required;
- identifies expected failing tests for intentional new behavior;
- records exact commands and relevant evidence.

Tests/evals must test the approved contract, not redefine it. A test/eval change that materially changes required behavior or acceptance meaning requires ChatGPT review before proceeding.

For behavior-preserving refactors, follow `REFACTORING-WORKFLOW.md`; the pre-change characterization baseline must be green before implementation begins.

Tests/evals assess this governance product, not the quality of application tasks in consumer repositories.

## PD3 — Implement

For executable product changes, the Agente de IA Ejecutor receives the approved contract and necessary read-only Markdown context.

The executor:
- edits authorized non-Markdown implementation code/config/assets;
- authors/updates applicable non-Markdown tests/evals;
- does not edit committed Markdown;
- does not change strategic scope or acceptance;
- resolves normal technical implementation and test-design choices autonomously inside the contract.

For Markdown-only product changes, this phase is performed by ChatGPT and no executor implementation is required, although executable verification may still be delegated to the Agente de IA Ejecutor.

For test/eval-only work, the Agente de IA Ejecutor performs the authorized changes and execution.

## PD4 — Verification

The Agente de IA Ejecutor runs the applicable deterministic tests/evals against the resulting implementation and returns reproducible evidence.

If verification fails:
- implementation or test implementation defect -> executor diagnoses and fixes within the approved contract;
- specification/acceptance ambiguity -> stop and return to ChatGPT;
- proposed behavior change discovered during a refactor -> stop refactor and re-enter PD0 as a behavior-changing change.

The executor MUST NOT make tests green by weakening the ChatGPT-approved behavioral contract. If a previously established baseline must change, ChatGPT must explicitly authorize that change.

For higher-risk changes ChatGPT MAY request a fresh executor session or a second compatible executor product to rerun verification, but this remains the same `Agente de IA Ejecutor` role and does not create a new governance role.

## PD5 — Orchestrator Review

ChatGPT reviews:
- implementation/test/eval diff against the approved objective;
- architectural consistency;
- role-boundary compliance;
- executor verification evidence;
- required Markdown/documentation/Decision Records;
- public compatibility and supply-chain implications.

A green suite is necessary when applicable but is not sufficient if the change violates architecture or specification.

## PD6 — Integrate

Integrate only when PD5 accepts the change.

Prefer one coherent, reviewable change/PR at a time. Keep refactors separate from behavior changes where practical. Releases additionally follow `docs/RELEASES.md`.

## Handoff Invariants

- ChatGPT -> Agente de IA Ejecutor only after the contract is sufficiently complete.
- Agente de IA Ejecutor -> ChatGPT with implementation/test/eval diff and reproducible verification evidence.
- ChatGPT -> Agente de IA Ejecutor again when technical rework is required.
- ChatGPT -> Human Owner when product scope/risk/public compatibility requires final authority.

No executor product is privileged. Switching OpenCode -> Codex -> Claude Code -> another compatible executor does not change the role contract.
