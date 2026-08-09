# D020 — Repository-persisted task handoffs

Status: ACCEPTED
Authority: Human Owner

## Decision

Executable work requested from an `Agente de IA Ejecutor` MUST be defined first as a versioned Task Contract stored in the canonical repository.

Chat prompts, terminal prompts, or product-specific agent messages are transport only. They MUST NOT be the sole authoritative source of task objective, scope, constraints, acceptance criteria, verification requirements, or handoff expectations.

The normal handoff is:

1. ChatGPT Orchestrator defines and persists the Task Contract as Markdown in the repository.
2. The Task Contract is reviewed as part of the source history and references the controlling repository policies/decisions needed for execution.
3. The external prompt to OpenCode, Codex, Claude Code, Antigravity, or another executor is intentionally minimal and points the executor to the repository instructions and exact Task Contract path.
4. The executor loads the repository rules plus that Task Contract, performs only the authorized non-Markdown work, executes required verification, and reports evidence against the persisted contract.
5. ChatGPT reviews the implementation and evidence against the same versioned contract.

## Canonical task location

Source-product maintenance tasks live under:

`docs/tasks/`

These records are source-repository maintenance artifacts. They are NOT consumer `.agent-coordination/` task records and MUST NOT create a live consumer governance instance in this repository.

## Task Contract minimum content

Each executable Task Contract MUST identify at least:
- task ID and status;
- objective / required outcome;
- controlling references;
- authorized scope;
- explicit exclusions;
- branch/base requirements;
- artifact ownership/write restrictions;
- acceptance criteria;
- required tests/evals and evidence;
- stop/escalation conditions;
- expected executor handoff.

The contract SHOULD specify outcomes and invariants without over-prescribing implementation mechanics that belong to the executor.

## Prompt minimization

A normal executor-launch prompt SHOULD contain only enough information to:
- identify the executor role;
- identify the canonical repository or local checkout;
- identify the expected base branch/current branch condition;
- identify the exact Task Contract path to load;
- instruct the executor to read `AGENTS.md` and follow referenced repository policy.

If task instructions in a prompt conflict with the persisted Task Contract, the persisted repository contract wins unless the Human Owner or ChatGPT Orchestrator explicitly supersedes it in a new persisted revision.

## Auditability

Task Contracts remain in Git history after completion. They provide an auditable record of what was actually requested independently of chat history or the agent product used.

Completion evidence may be captured in the PR, commit, CI/test artifacts, or executor handoff; the Task Contract itself MUST NOT be silently rewritten after implementation starts merely to match the resulting implementation. Material scope/acceptance changes require an explicit persisted contract revision before continued implementation.

## Consequences

- `docs/DEVELOPMENT-WORKFLOW.md` must require a persisted Task Contract before executor work begins.
- `AGENTS.md` must tell executors to load the exact assigned Task Contract and not infer scope from chat history.
- product-specific launch prompts become small pointers rather than duplicated specifications.
- switching executor products does not lose task intent because task semantics live in the repository.
