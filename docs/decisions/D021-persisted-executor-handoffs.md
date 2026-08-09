# D021 — Persisted executor handoffs

Status: ACCEPTED
Authority: Human Owner

## Decision

The result of executable work performed by an `Agente de IA Ejecutor` MUST be persisted in the canonical repository before the executor reports completion, blocking, or partial progress to ChatGPT Orchestrator.

Executor chat/terminal output is transport only and MUST NOT be the sole authoritative record of implementation status, verification evidence, changed artifacts, unresolved issues, or branch/commit identity.

The canonical executor-return artifact is a non-Markdown handoff record under:

`handoffs/`

Normal naming:

`handoffs/TNNN-executor-handoff.json`

## Symmetric handoff model

The normal auditable flow is:

1. ChatGPT Orchestrator persists the requested work in `docs/tasks/TNNN-*.md`.
2. The Agente de IA Ejecutor executes that contract on the authorized topic branch.
3. The executor runs the required verification.
4. The executor persists `handoffs/TNNN-executor-handoff.json` on the same branch.
5. The executor's visible response contains only concise status and pointers: handoff path, branch and HEAD.
6. ChatGPT reads the persisted handoff plus the actual Git diff/evidence and decides acceptance/rework/next action.

## Ownership

- ChatGPT owns the Markdown Task Contract and acceptance meaning.
- The Agente de IA Ejecutor owns the non-Markdown executor handoff artifact and technical evidence it reports.
- The Human Owner retains final authority.

The executor MUST NOT edit the Markdown Task Contract to reflect what it happened to implement.

## Audit requirement

Git history alone MUST allow a reviewer to reconstruct:
- what was requested;
- what the executor reports it performed;
- which branch/commit contains the work;
- which tests/evals were executed and their reported results;
- unresolved blockers/risks;
- the actual repository diff.

Chat history from ChatGPT, OpenCode, Codex, Claude Code, or another product MUST NOT be required.

## Visible executor response

After the handoff is persisted, the executor SHOULD respond only with a compact pointer equivalent to:

`STATUS: DONE | BLOCKED | PARTIAL`
`HANDOFF: handoffs/TNNN-executor-handoff.json`
`BRANCH: <topic-branch>`
`HEAD: <commit-sha>`

## Consequences

- `docs/EXECUTOR-HANDOFFS.md` is the normative handoff format and lifecycle.
- `docs/TASK-CONTRACTS.md` must require a persisted executor handoff.
- Task Contracts must specify their expected handoff path.
- `AGENTS.md` must require executors to persist their result before claiming completion/blocking.
- ChatGPT review starts by reading the assigned Task Contract, executor handoff, and actual branch diff.
