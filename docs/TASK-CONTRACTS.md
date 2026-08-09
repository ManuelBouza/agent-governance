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

Active and completed source-maintenance Task Contracts live under:

`docs/tasks/`

Recommended naming:

`TNNN-<short-slug>.md`

Task IDs are stable once assigned.

Each executable task SHOULD identify its expected persisted executor handoff path under `handoffs/`, normally:

`handoffs/TNNN-executor-handoff.json`

## Required fields

Each task should contain:

### Identity
- Task ID
- Status: `DRAFT`, `BLOCKED`, `READY`, `IN_PROGRESS`, `DONE`, `ACCEPTED`, `CANCELLED`
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

## Contract integration gate

An executable Task Contract is not ready for execution merely because it exists on a planning branch.

Before launching an executor:
1. ChatGPT creates/updates the Task Contract on a policy-compliant planning/Markdown topic branch;
2. ChatGPT reviews the contract and controlling Markdown/Decision Records;
3. the planning change is merged into `develop`;
4. the task status is `READY` only when all known prerequisite decisions are resolved;
5. the executor implementation branch is then created from a `develop` revision containing that exact contract.

This creates two durable stages:

`contract history -> implementation history`

The executor MUST NOT begin executable work from a branch/revision that predates the controlling Task Contract.

## Freeze and revision semantics

The original objective, scope, exclusions, invariants, acceptance criteria, and verification meaning are the durable request.

After implementation begins:
- the executor cannot edit the Task Contract;
- ChatGPT must not silently rewrite the original task semantics to match implementation;
- a material change requires an explicit persisted revision before execution continues;
- lifecycle metadata and explicit review/revision/acceptance notes may be updated/appended by ChatGPT as long as the original request remains auditable.

A reviewer must be able to distinguish the original task from later authorized revisions.

## Lifecycle

1. ChatGPT frames/researches the change.
2. ChatGPT creates the Task Contract on a planning branch.
3. The Task Contract is reviewed and integrated into `develop`.
4. ChatGPT launches the executor with a minimal pointer to the Task Contract.
5. The executor creates/uses the authorized implementation topic branch from the `develop` revision containing the contract.
6. The executor performs only authorized non-Markdown work.
7. Material task changes require a persisted ChatGPT revision before execution continues.
8. The executor runs required verification and persists its non-Markdown handoff under `handoffs/`.
9. The executor commits and pushes the implementation branch, including the current handoff artifact.
10. The executor returns only status, handoff path, branch, and pushed HEAD.
11. ChatGPT reads the Task Contract, handoff, and remote Git diff/evidence.
12. Rework repeats on the same task branch using durable review/revision instructions.
13. After ChatGPT acceptance, the implementation proceeds through PR to `develop`.
14. ChatGPT may update lifecycle/acceptance metadata without rewriting original execution semantics.

## Minimal launch prompt pattern

A product-specific launch prompt should be equivalent to:

> Operate as the Agente de IA Ejecutor for `ManuelBouza/agent-governance`. Read `AGENTS.md`, then load and execute the Task Contract at `<path>` from current `develop`. Follow all referenced repository policies. Do not edit Markdown. Persist, commit and push the required executor handoff before returning.

Additional task semantics should not be duplicated into the launch prompt.

## Minimal executor response pattern

After persisting/committing/pushing the required handoff, the executor should return only:

`STATUS: DONE | BLOCKED | PARTIAL`

`HANDOFF: handoffs/TNNN-executor-handoff.json`

`BRANCH: <topic-branch>`

`HEAD: <pushed-commit-sha>`

## Audit invariant

A reviewer must be able to reconstruct from Git alone:
- what was requested before implementation;
- any explicit revisions/review directives;
- what the executor reports it did;
- what actually changed.

Chat history must not be required for this reconstruction.
