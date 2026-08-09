# D021 — Persisted executor handoffs

Status: ACCEPTED
Authority: Human Owner
Refined by: D022 — Source product change procedure

## Decision

The result of executable work performed by an `Agente de IA Ejecutor` MUST be persisted in the canonical repository before the executor reports completion, blocking, or partial progress to ChatGPT Orchestrator.

Executor chat/terminal output is transport only and MUST NOT be the sole authoritative record of implementation status, verification evidence, changed artifacts, unresolved issues, or branch/commit identity.

The canonical executor-return artifact is a non-Markdown handoff record under:

`handoffs/`

Normal naming:

`handoffs/TNNN-executor-handoff.json`

D022 further requires the implementation/test/eval/handoff state to be committed and the topic branch pushed to the canonical remote before normal status is returned, so ChatGPT can review the exact remote branch rather than local-only evidence.

## Symmetric handoff model

The normal auditable flow is:

1. ChatGPT Orchestrator persists the requested work in `docs/tasks/TNNN-*.md` and integrates the contract stage into `develop`.
2. The Agente de IA Ejecutor executes that contract on the authorized topic branch created from the contract-containing `develop` revision.
3. The executor runs the required verification.
4. The executor persists `handoffs/TNNN-executor-handoff.json` on the same branch.
5. The executor commits and pushes the review state.
6. The executor's visible response contains only concise status and pointers: handoff path, branch and pushed HEAD.
7. ChatGPT reads the remote handoff plus the actual Git diff/evidence and decides acceptance/rework/next action.

## Ownership

- ChatGPT owns the Markdown Task Contract and acceptance meaning.
- The Agente de IA Ejecutor owns the non-Markdown executor handoff artifact and technical evidence it reports.
- The Human Owner retains final authority.

The executor MUST NOT edit the Markdown Task Contract to reflect what it happened to implement.

## Audit requirement

Canonical Git history/remote state alone MUST allow a reviewer to reconstruct:
- what was requested;
- what the executor reports it performed;
- which remote branch/commit contains the work;
- which tests/evals were executed and their reported results;
- unresolved blockers/risks;
- the actual repository diff.

Chat history or an executor's unpushed local filesystem MUST NOT be required.

## Visible executor response

After the handoff and review state are persisted, committed, and pushed, the executor SHOULD respond only with a compact pointer equivalent to:

`STATUS: DONE | BLOCKED | PARTIAL`
`HANDOFF: handoffs/TNNN-executor-handoff.json`
`BRANCH: <topic-branch>`
`HEAD: <pushed-commit-sha>`

## Consequences

- `docs/EXECUTOR-HANDOFFS.md` is the normative handoff format and lifecycle.
- D022 requires commit + push before normal remote review.
- `docs/TASK-CONTRACTS.md` requires a persisted executor handoff and contract-first implementation base.
- Task Contracts specify their expected handoff path.
- `AGENTS.md` requires executors to persist/push their result before claiming completion/blocking.
- ChatGPT review starts by reading the assigned Task Contract, executor handoff, and actual remote branch diff.
