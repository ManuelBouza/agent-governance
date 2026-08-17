# D016 — Binary agent role model

Status: ACCEPTED
Authority: Human Owner

## Context

The source-repository workflow previously distinguished OpenCode/other implementation executors from Codex as a separate test/eval owner. That distinction was based on product names rather than stable governance responsibilities.

OpenCode, Codex, Claude Code, Antigravity, and similar local/coding agents belong to the same operational category: an AI executor capable of modifying repository artifacts and running technical verification.

D052 later refined test authorship without adding another agent role. Test ownership is now split by semantic authority: designated acceptance/conformance oracle assets may be authored by ChatGPT, while implementation/exploratory tests and verification execution remain executor responsibilities.

## Decision

Repository development uses only two agent roles plus the Human Owner:

1. **ChatGPT Orchestrator**
   - owns strategy, research synthesis, architecture, task contracts, scope, acceptance criteria, handoffs, review, and all committed Markdown (`*.md`);
   - decides what must be built or changed and what evidence is sufficient;
   - under D052 `orchestrator-conformance` or `mixed`, owns the narrow committed non-Markdown conformance/oracle assets that directly encode ChatGPT-owned acceptance semantics;
   - does not depend on a specific executor product.

2. **Agente de IA Ejecutor**
   - is an abstract, product-agnostic role that may be fulfilled by OpenCode, Codex, Claude Code, Antigravity, or another compatible coding agent;
   - owns authorized non-Markdown implementation, implementation-focused tests/evals/fixtures, technical harness/adapters, execution of all required tests/evals, and verification evidence, except D052-designated Orchestrator conformance/oracle assets;
   - makes technical implementation/test decisions inside the ChatGPT-approved contract while remaining free to add supplementary unit/integration/property/fuzz/adversarial coverage;
   - has no authority to edit committed Markdown, change strategic scope, redefine acceptance, weaken verification contrary to the approved contract, or semantically modify an Orchestrator-owned conformance oracle without persisted ChatGPT authorization.

The **Human Owner** retains final authority over product scope, priorities, risk, public distribution, releases, and overrides.

No executor product has special governance status. Product-specific configuration files are adapters only and may enforce the same executor contract mechanically.

## Refactoring consequence

Refactor safety does not require a third agent role.

ChatGPT defines behavior-preservation invariants. Depending on the D052 mode, ChatGPT may also persist the accepted characterization/conformance oracle before structural mutation. The Agente de IA Ejecutor executes that baseline, performs authorized non-Markdown refactoring, adds supplementary technical tests where useful, and reruns verification. Once ChatGPT accepts the RF1 baseline, it is frozen for that refactor unit and cannot be weakened or reinterpreted after implementation begins without explicit ChatGPT authorization.

For higher-risk changes, ChatGPT may request a fresh executor session or a second compatible executor product to repeat verification. This increases execution independence without creating a new governance role.

## D052 oracle boundary

When D052 applies, an executor may diagnose or mechanically repair a harness defect only within the durable task/review authority and without changing acceptance meaning. Expected results, classifications, thresholds, security expectations, semantic negative controls, or frozen characterization meaning remain Orchestrator-owned.

If the executor believes the oracle is semantically wrong, it reports the affected claim as blocked/`ORACLE_DEFECT`-equivalent with evidence rather than changing the oracle to make implementation pass.

Tests remain evidence, not Governance authority.

## Consequences

- D014 and D015 are superseded where they created a Codex-specific governance role.
- `AGENTS.md`, development/refactoring workflows, tests/evals ownership, and adapters continue to use only `ChatGPT Orchestrator` and `Agente de IA Ejecutor` semantics.
- OpenCode-specific, Codex-specific, Claude-specific, or other instructions MUST remain adapters and MUST NOT enter task semantics.
- D052 supersedes the former blanket statement that all tests/evals are authored by the executor; conformance/oracle authorship follows semantic authority while execution remains executor-owned.
- ChatGPT preserves specification independence by owning Markdown contracts, designated conformance oracles where applicable, and review/acceptance.
