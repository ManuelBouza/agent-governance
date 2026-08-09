# Executor Handoffs

Status: ACTIVE

## Purpose

Define how an `Agente de IA Ejecutor` returns implementation status and verification evidence to ChatGPT Orchestrator in a durable, auditable form.

The executor's chat/terminal response is transport only. The authoritative execution result MUST be persisted in Git and pushed to the canonical remote before the executor reports completion, blocking, or partial progress.

## Canonical location

Executor handoffs live under:

`handoffs/`

Recommended naming:

`TNNN-executor-handoff.json`

The handoff MUST be non-Markdown so the Agente de IA Ejecutor can own and persist it under D016.

For refactor baseline checkpoints, a Task Contract MAY require an additional artifact such as:

`handoffs/TNNN-rf1-baseline.json`

## Required fields

Each final handoff MUST record at least:
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

The handoff SHOULD make clear whether `head_sha` is the pushed remote HEAD reviewed by ChatGPT. A local-only SHA is not sufficient for normal handoff acceptance.

## Lifecycle

1. ChatGPT persists the Task Contract and integrates it into `develop`.
2. The executor creates/uses the task branch from the `develop` revision containing that contract.
3. The executor performs the authorized work.
4. The executor runs required verification.
5. The executor writes/updates the task handoff artifact under `handoffs/` on the same task branch.
6. The executor commits the authorized implementation/test/eval/handoff state.
7. The executor pushes the topic branch to the canonical remote.
8. The handoff's `head_sha` must describe the pushed branch state; if the commit changed after writing the file, update/recommit so the handoff and pushed state remain coherent.
9. The executor's visible response contains only status, handoff path, branch, and pushed HEAD.
10. ChatGPT fetches the remote handoff and branch/diff through GitHub before accepting or requesting rework.

## Commit/push invariant

A normal executor handoff is not complete while the authoritative state exists only on the executor's local machine.

Before returning status, the executor MUST ensure:
- all in-scope implementation/test/eval changes intended for review are committed;
- the handoff artifact is committed;
- the topic branch is pushed to the canonical remote;
- the reported HEAD is reachable from that remote topic branch;
- the working tree contains no unreported in-scope changes that would make the handoff misleading.

If pushing is impossible because of credentials/connectivity/permissions, persist a `BLOCKED` handoff locally if possible and report the inability to create a remotely auditable state. ChatGPT cannot accept a normal implementation from chat-only evidence.

## Refactor baseline checkpoints

When `docs/REFACTORING-WORKFLOW.md` requires RF1 baseline approval before structural mutation:
- run the required pre-refactor characterization suite;
- persist the Task Contract-specified baseline handoff/artifact;
- commit and push that checkpoint before RF3 mutation;
- return a minimal `PARTIAL` pointer for ChatGPT baseline review;
- do not begin RF3 until ChatGPT has persisted/communicated baseline acceptance according to the Task Contract/workflow.

This checkpoint freezes evidence without inventing a third governance role.

## Visible response pattern

The executor's terminal/chat response SHOULD be equivalent to:

`STATUS: DONE | BLOCKED | PARTIAL`

`HANDOFF: handoffs/TNNN-executor-handoff.json`

`BRANCH: <topic-branch>`

`HEAD: <pushed-commit-sha>`

For an intermediate RF1 checkpoint, the handoff path may be the baseline artifact specified by the Task Contract.

Additional narrative should be minimal. The repository handoff is authoritative.

## Persistence timing

The executor MUST persist the handoff after running the required verification and before claiming the task is DONE/BLOCKED/PARTIAL.

If implementation changes after a handoff was written, update the handoff and pushed commit so its SHA, file list, and verification evidence describe the actual review state.

## Audit invariant

A reviewer must be able to reconstruct from the canonical Git remote:

- what ChatGPT requested: `docs/tasks/<task>.md`
- what the executor reports it did: `handoffs/<task>-executor-handoff.json`
- what actually changed: pushed commits/diff and test/eval artifacts

Chat history and an executor's unpushed local filesystem MUST NOT be required for this reconstruction.
