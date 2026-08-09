# Executor Handoffs

Status: ACTIVE

## Purpose

Define how an `Agente de IA Ejecutor` returns implementation status and verification evidence to ChatGPT Orchestrator in a durable, auditable form.

The executor's chat/terminal response is transport only. The authoritative execution result MUST be persisted in the repository before the executor reports completion, blocking, or partial progress.

## Canonical location

Executor handoffs live under:

`handoffs/`

Recommended naming:

`TNNN-executor-handoff.json`

The handoff MUST be non-Markdown so the Agente de IA Ejecutor can own and persist it under D016.

## Required fields

Each handoff MUST record at least:
- `task_id`
- `status`: `DONE`, `BLOCKED`, or `PARTIAL`
- `task_contract_path`
- `branch`
- `head_sha`
- `base_branch`
- `base_sha`
- `files_changed`
- `implementation_summary`
- `verification.commands`
- `verification.results`
- `verification.runtime`
- `verification.network_required`
- `dependencies_or_config_changes`
- `git_status`
- `unresolved_issues`
- `recommended_next_task`
- `chatgpt_read_path`

The schema MAY evolve as implementation needs become clearer, but the persisted handoff MUST always be sufficient for ChatGPT to reconstruct what happened without relying on executor chat history.

## Lifecycle

1. ChatGPT persists the Task Contract.
2. The executor performs the authorized work on the task branch.
3. Before returning to ChatGPT, the executor writes/updates the task handoff artifact under `handoffs/` on the same task branch.
4. The handoff artifact references the exact task, branch, HEAD/base identities, files changed, and verification evidence.
5. The executor's visible response contains only a concise status plus the exact repository path ChatGPT should read.
6. ChatGPT reads the persisted handoff and independently reviews the branch/diff/evidence before accepting, requesting rework, or authorizing PR creation.

## Visible response pattern

The executor's terminal/chat response SHOULD be equivalent to:

`STATUS: DONE | BLOCKED | PARTIAL`

`HANDOFF: handoffs/TNNN-executor-handoff.json`

`BRANCH: <topic-branch>`

`HEAD: <commit-sha>`

Additional narrative should be minimal. The repository handoff is authoritative.

## Persistence timing

The executor MUST persist the handoff after running the required verification and before claiming the task is DONE or BLOCKED.

If implementation changes after a handoff was written, the executor MUST update the handoff so its `head_sha`, file list and verification evidence describe the actual final branch state.

## Audit invariant

A reviewer must be able to reconstruct both sides of a delegated task from Git alone:

- what ChatGPT requested: `docs/tasks/<task>.md`
- what the executor reports it did: `handoffs/<task>-executor-handoff.json`
- what actually changed: Git commit/diff and test/eval artifacts

Chat history MUST NOT be required for this reconstruction.
