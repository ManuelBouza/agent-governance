# Product Development Workflow

Status: ACTIVE

## Purpose

Define how agents develop the `agent-governance` source product without turning this repository into a consumer instance of its own Governance Core.

This is a repository-maintenance workflow, not an installed `.agent-coordination/` lifecycle. Real consumer-project governance is exercised only in separate repositories or synthetic disposable fixtures.

## Roles

- Human Owner: final authority.
- ChatGPT: Orchestrator, specification owner, architectural reviewer, and exclusive normal author of committed Markdown.
- Implementation Executor: OpenCode or another compatible coding agent; owns non-test product implementation code/config/assets.
- Codex: exclusive normal author/maintainer of tests/evals and owner of test/eval execution evidence.

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
- role ownership and handoff order.

For protocol/instruction changes, ChatGPT authors the canonical Markdown change itself. For executable changes, the specification must describe behavior without prescribing unnecessary implementation mechanics.

## PD2 — Establish Verification

Codex derives the verification strategy from the approved specification.

Depending on change type, Codex:
- adds/updates deterministic tests;
- adds/updates agent-facing eval cases;
- establishes a baseline result;
- identifies expected failing tests for intentional new behavior;
- records the exact commands and relevant evidence.

For behavior-preserving refactors, follow `REFACTORING-WORKFLOW.md`; the pre-change characterization baseline must be green before implementation begins.

Tests/evals assess this governance product, not the quality of application tasks in consumer repositories.

## PD3 — Implement

For executable product changes, the Implementation Executor receives only the approved implementation contract and necessary read-only specification/test context.

The executor:
- edits implementation code/config/assets only;
- does not edit committed Markdown;
- does not edit tests/evals;
- does not weaken verification;
- returns implementation evidence/diff to the Orchestrator.

For Markdown-only product changes, this phase is performed by ChatGPT and no implementation executor is required.

For test/eval-only work, Codex performs the authorized test/eval changes and no implementation executor is required.

## PD4 — Independent Verification

Codex runs the applicable deterministic tests/evals against the implementation produced in PD3.

If verification fails:
- implementation defect -> return to Implementation Executor;
- test/eval defect demonstrably inconsistent with the approved contract -> Codex may correct the test/eval;
- specification/acceptance ambiguity -> stop and return to ChatGPT;
- proposed behavior change discovered during a refactor -> stop refactor and re-enter PD0 as a behavior-changing change.

The Implementation Executor must never resolve a failure by modifying tests/evals. Codex must never resolve a product implementation failure by modifying implementation code.

## PD5 — Orchestrator Review

ChatGPT reviews:
- diff against the approved objective;
- architectural consistency;
- role-boundary compliance;
- Codex verification evidence;
- required Markdown/documentation/Decision Records;
- public compatibility and supply-chain implications.

A green suite is necessary when applicable but not sufficient if the change violates architecture or specification.

## PD6 — Integrate

Integrate only when PD5 accepts the change.

Prefer one coherent, reviewable change/PR at a time. Keep refactors separate from behavior changes where practical. Releases additionally follow `docs/RELEASES.md`.

## Handoff Invariants

- ChatGPT -> Codex before executable implementation when verification must be established first.
- ChatGPT -> Implementation Executor only after the contract is sufficiently complete.
- Implementation Executor -> Codex for independent verification.
- Codex -> ChatGPT with verification evidence, not acceptance authority.
- ChatGPT -> Human Owner when product scope/risk/public compatibility requires final authority.

No agent silently assumes another role's write ownership.
