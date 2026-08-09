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

Each task SHOULD also identify its expected persisted executor handoff path under `handoffs/`, normally:

`handoffs/TNNN-executor-handoff.json`

## Required fields

Each task should contain:

### Identity
- Task ID
- Status: `READY`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `ACCEPTED`, `CANCELLED`
- Type: feature, fix, refactor, test/eval, release, infrastructure, or mixed
- Base branch
- Expected topic branch
- Expected executor handoff path

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
The executor MUST persist its result according to `docs/EXECUTOR-HANDOFFS.md` at the task's expected handoff path before claiming `DONE`, `BLOCKED`, or `PARTIAL`.

The persisted handoff normally records:
- branch and HEAD;
- base branch and base SHA;
- files changed;
- concise implementation summary;
- exact test/eval commands;
- results and failures/skips;
- dependencies/configuration changes;
- git status;
- unresolved ambiguity or risk;
- recommended next incremental task, if any.

## Lifecycle

1. ChatGPT creates the Task Contract in a topic branch or other policy-compliant planning change.
2. Once the contract is available on the branch/revision the executor will use, ChatGPT supplies only a minimal launch prompt pointing to it.
3. The executor creates/uses the authorized implementation topic branch and executes against the persisted contract.
4. Material changes to objective, scope, acceptance, or verification require ChatGPT to persist a revised Task Contract before execution continues.
5. The executor does not modify the Task Contract to match its implementation.
6. The executor runs required verification and persists its non-Markdown handoff artifact under `handoffs/`.
7. The executor's visible response reports only status, handoff path, branch and HEAD.
8. ChatGPT reads the Task Contract, persisted executor handoff, and actual Git diff/evidence before accepting or requesting rework.

## Minimal launch prompt pattern

A product-specific launch prompt should be equivalent to:

> Operate as the Agente de IA Ejecutor for `ManuelBouza/agent-governance`. Read `AGENTS.md`, then load and execute the Task Contract at `<path>` from the specified branch/revision. Follow all referenced repository policies. Do not edit Markdown. Persist the required executor handoff before returning.

Additional task semantics should not be duplicated into the launch prompt.

## Minimal executor response pattern

After persisting the required handoff, the executor should return only:

`STATUS: DONE | BLOCKED | PARTIAL`

`HANDOFF: handoffs/TNNN-executor-handoff.json`

`BRANCH: <topic-branch>`

`HEAD: <commit-sha>`

## Audit invariant

A reviewer must be able to reconstruct both the requested work and the executor-reported result from Git alone, without access to ChatGPT/OpenCode/Codex/Claude conversation history.
