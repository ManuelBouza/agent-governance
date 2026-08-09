# D016 — Binary agent role model

Status: ACCEPTED
Authority: Human Owner

## Context

The source-repository workflow previously distinguished OpenCode/other implementation executors from Codex as a separate test/eval owner. That distinction was based on product names rather than stable governance responsibilities.

OpenCode, Codex, Claude Code, Antigravity, and similar local/coding agents belong to the same operational category: an AI executor capable of modifying repository artifacts and running technical verification.

## Decision

Repository development uses only two agent roles plus the Human Owner:

1. **ChatGPT Orchestrator**
   - owns strategy, research synthesis, architecture, task contracts, scope, acceptance criteria, handoffs, review, and all committed Markdown (`*.md`);
   - decides what must be built or changed and what evidence is sufficient;
   - does not depend on a specific executor product.

2. **Agente de IA Ejecutor**
   - is an abstract, product-agnostic role that may be fulfilled by OpenCode, Codex, Claude Code, Antigravity, or another compatible coding agent;
   - owns authorized non-Markdown implementation, deterministic tests, agent-facing evals, fixtures/data, and execution of tests/evals;
   - makes technical implementation/test decisions inside the ChatGPT-approved contract;
   - has no authority to edit committed Markdown, change strategic scope, redefine acceptance, or weaken verification contrary to the approved contract.

The **Human Owner** retains final authority over product scope, priorities, risk, public distribution, releases, and overrides.

No executor product has special governance status. Product-specific configuration files are adapters only and may enforce the same executor contract mechanically.

## Refactoring consequence

Refactor safety does not require a third agent role.

ChatGPT defines behavior-preservation invariants. The Agente de IA Ejecutor establishes and runs the pre-change characterization baseline, performs authorized non-Markdown refactoring, and reruns verification. Once ChatGPT accepts the RF1 baseline, it is frozen for that refactor unit and cannot be weakened or reinterpreted after implementation begins without explicit ChatGPT authorization.

For higher-risk changes, ChatGPT may request a fresh executor session or a second compatible executor product to repeat verification. This increases execution independence without creating a new governance role.

## Consequences

- D014 and D015 are superseded where they created a Codex-specific governance role.
- `AGENTS.md`, development/refactoring workflows, tests/evals ownership, and adapters use only `ChatGPT Orchestrator` and `Agente de IA Ejecutor` semantics.
- OpenCode-specific, Codex-specific, Claude-specific, or other instructions MUST remain adapters and MUST NOT enter task semantics.
- Tests/evals are owned and executed by the same abstract executor role that may also implement code.
- ChatGPT preserves specification independence by owning Markdown contracts and reviewing implementation plus verification evidence.
