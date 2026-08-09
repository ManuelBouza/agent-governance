# Source Product Task Contracts

Status: ACTIVE

## Purpose

Define the persistent handoff format used when ChatGPT Orchestrator delegates executable work in the canonical `agent-governance` source repository.

Task Contracts are auditable source-product maintenance records. They are intentionally separate from consumer-project `.agent-coordination/` tasks.

## Authority

- ChatGPT Orchestrator authors and revises Task Contract Markdown.
- The Agente de IA Ejecutor reads Task Contracts as authoritative execution scope and MUST NOT edit them.
- The Human Owner retains final authority.

A chat/terminal prompt is only a pointer to a Task Contract. It is not the canonical task specification.

## Location and naming

Active and completed source-maintenance Task Contracts live under `docs/tasks/`.

Recommended naming:

`TNNN-<short-slug>.md`

Task IDs are stable once assigned.

## Required fields

Each task should contain:

### Identity
- Task ID
- Status: `READY`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `ACCEPTED`, `CANCELLED`
- Type: feature, fix, refactor, test/eval, release, infrastructure, or mixed
- Base branch
- Expected topic branch

### Objective
A concise description of the observable result required.

### Controlling references
Only the repository files/decisions needed to interpret the task correctly. `AGENTS.md` is always controlling.

### Authorized scope
Artifacts and behavior the executor is allowed to modify or create.

### Explicit exclusions
Things the executor must not change or expand into.

### Invariants / constraints
Architecture, compatibility, safety, ownership, or behavioral properties that must remain true.

### Acceptance criteria
Objective conditions ChatGPT will use to accept or reject the implementation.

### Verification requirements
Tests/evals that must be created or executed and the minimum evidence expected.

### Stop / escalation conditions
Conditions requiring the executor to stop instead of guessing or expanding scope.

### Expected handoff
Information the executor must return to ChatGPT after work, normally:
- branch and HEAD;
- files changed;
- concise implementation summary;
- exact test/eval commands;
- results and failures/skips;
- dependencies/configuration changes;
- unresolved ambiguity or risk;
- recommended next incremental task, if any.

## Lifecycle

1. ChatGPT creates the Task Contract in a topic branch or other policy-compliant planning change.
2. Once the contract is available on the branch/revision the executor will use, ChatGPT supplies only a minimal launch prompt pointing to it.
3. The executor creates/uses the authorized implementation topic branch and executes against the persisted contract.
4. Material changes to objective, scope, acceptance, or verification require ChatGPT to persist a revised Task Contract before execution continues.
5. The executor does not modify the Task Contract to match its implementation.
6. ChatGPT reviews the resulting implementation and evidence against the persisted contract.

## Minimal launch prompt pattern

A product-specific launch prompt should be equivalent to:

> Operate as the Agente de IA Ejecutor for `ManuelBouza/agent-governance`. Read `AGENTS.md`, then load and execute the Task Contract at `<path>` from the specified branch/revision. Follow all referenced repository policies. Do not edit Markdown. Stop and report if the contract is ambiguous or blocked.

Additional task semantics should not be duplicated into the launch prompt.

## Audit invariant

A reviewer must be able to reconstruct what the executor was asked to do from Git alone, without access to ChatGPT/OpenCode/Codex/Claude conversation history.
