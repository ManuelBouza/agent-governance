# Executor Handoffs

Status: ACTIVE

## Purpose

Define how an `Agente de IA Ejecutor` returns implementation status and verification evidence to ChatGPT Orchestrator in a durable, auditable form.

The executor's chat/terminal response is transport only. The authoritative execution result MUST be persisted in Git and pushed to the canonical remote before the executor reports completion, blocking, or partial progress.

D029 defines the non-self-referential Git identity model used by this contract. D048 defines the normal-task remote-publication timing boundary.

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
- `implementation_head_sha`
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

`implementation_head_sha` identifies the committed implementation/test/eval state described by the evidence. It MUST be reachable as an ancestor of the final pushed topic-branch HEAD reported after handoff finalization.

The handoff JSON MUST NOT be required to contain the SHA of the commit that contains that same JSON. Such a requirement is self-referential and impossible to satisfy.

For backward compatibility, an existing `head_sha` field MAY be interpreted as the implementation/review anchor when the handoff explicitly states that meaning.

## Lifecycle

1. ChatGPT persists the Task Contract and integrates it into `develop`.
2. The executor creates/uses the task branch from the `develop` revision containing that contract.
3. The executor performs the authorized work locally on the task branch.
4. The executor runs required verification.
5. The executor commits the final implementation/test/eval state that the verification evidence describes.
6. The executor records that commit as `implementation_head_sha` in the task handoff artifact under `handoffs/`.
7. The executor commits the handoff artifact; this may create a handoff-only successor commit.
8. For a normal task, only after steps 3-7 are complete does the executor perform the one planned final push of the complete topic-branch state to the canonical remote.
9. The executor verifies that the remote topic branch resolves to the pushed final HEAD.
10. The executor's visible response contains only status, handoff path, branch, and the actual pushed branch HEAD.
11. ChatGPT fetches the remote branch at that visible HEAD, reads the handoff there, verifies that `implementation_head_sha` is an ancestor, and reviews the implementation diff/evidence before accepting or requesting rework.

If implementation changes after the handoff was generated, the executor MUST rerun affected verification as required, create a new implementation commit, update `implementation_head_sha`, and regenerate the handoff. A handoff-only metadata/finalization commit does not require a new implementation anchor.

## Remote publication timing invariant

For a normal task that is still executing toward its intended terminal result, intermediate progress MUST remain local. The executor MUST NOT push an intermediate topic-branch state merely as a progress checkpoint.

The normal sequence is:

`local implementation -> verification -> implementation commit -> final handoff -> handoff/finalization commit -> one planned final push -> remote HEAD verification -> terminal response`

A pre-completion remote push is allowed only when:

- the controlling Task Contract or referenced workflow explicitly requires an intermediate remote checkpoint, such as an RF1 baseline awaiting Orchestrator approval; or
- the executor is actually terminating the invocation with `BLOCKED` or `PARTIAL` and can safely publish a remotely auditable terminal handoff before returning that status.

Writing `status = PARTIAL` into an intermediate handoff does not create checkpoint authority when the same invocation is continuing toward `DONE`.

This is a publication-timing rule, not a history-rewrite rule. If Orchestrator review later requires rework, or a post-push handoff-only correction is legitimately required, a later authorized corrective push may occur on the same task branch. Do not reset, force-push, or erase prior remote history merely to simulate a single physical push.

## Commit/push invariant

A normal executor handoff is not complete while the authoritative state exists only on the executor's local machine.

Before the planned final push, the executor MUST ensure:
- all in-scope implementation/test/eval changes intended for review are committed;
- required verification is complete for the implementation anchor described by the handoff;
- the handoff artifact is committed;
- no unreported in-scope working-tree changes would make the handoff misleading.

After that push and before returning status, the executor MUST ensure:
- the topic branch is present on the canonical remote;
- the visible reported `HEAD` equals the pushed topic-branch HEAD;
- `implementation_head_sha` is an ancestor of that visible HEAD;
- the handoff file is readable at that visible HEAD.

If pushing is impossible because of credentials/connectivity/permissions, persist a `BLOCKED` handoff locally if possible and report the inability to create a remotely auditable state. ChatGPT cannot accept a normal implementation from chat-only evidence.

## Refactor baseline checkpoints

When `docs/REFACTORING-WORKFLOW.md` requires RF1 baseline approval before structural mutation:
- run the required pre-refactor characterization suite;
- persist the Task Contract-specified baseline handoff/artifact;
- commit and push that checkpoint before RF3 mutation;
- return a minimal `PARTIAL` pointer for ChatGPT baseline review;
- do not begin RF3 until ChatGPT has persisted/communicated baseline acceptance according to the Task Contract/workflow.

This checkpoint is an explicit D048 exception and freezes evidence without inventing a third governance role.

## Visible response pattern

The executor's terminal/chat response SHOULD be equivalent to:

`STATUS: DONE | BLOCKED | PARTIAL`

`HANDOFF: handoffs/TNNN-executor-handoff.json`

`BRANCH: <topic-branch>`

`HEAD: <pushed-final-branch-head-sha>`

The visible `HEAD` is intentionally outside the handoff JSON because it may identify the commit that contains the final handoff itself.

For an intermediate RF1 checkpoint, the handoff path may be the baseline artifact specified by the Task Contract.

Additional narrative should be minimal. The repository handoff is authoritative.

## Persistence timing

The executor MUST persist the handoff after running the required verification and before claiming the task is DONE/BLOCKED/PARTIAL.

For a normal task, the planned sequence is:

`implementation commit -> handoff JSON referencing implementation commit -> handoff/finalization commit -> one final push -> remote HEAD verification -> visible final HEAD`

Intermediate remote publication while the invocation continues toward `DONE` is not part of this sequence unless explicitly contracted.

Additional post-push handoff-only correction commits are allowed when legitimately required by review/finalization and when they do not change implementation/test/eval state and the JSON continues to identify the correct implementation anchor.

## Audit invariant

A reviewer must be able to reconstruct from the canonical Git remote:

- what ChatGPT requested: `docs/tasks/<task>.md` plus any persisted task revision/review directive;
- what implementation state the executor attests to: `implementation_head_sha` in `handoffs/<task>-executor-handoff.json`;
- what exact pushed branch state contains that handoff: the visible `HEAD` verified against the remote branch;
- what actually changed: pushed commits/diff and test/eval artifacts.

Chat history and an executor's unpushed local filesystem MUST NOT be required for this reconstruction.
