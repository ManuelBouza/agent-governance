# Post-Integration Cleanup Prompt

Status: ACTIVE

## Purpose

Define the canonical executor prompt used after an accepted source-product task has been integrated and only branch-retirement work remains.

This prompt is distinct from the normal Task Contract launch prompt in `docs/TASK-CONTRACTS.md`.

The normal launch prompt starts or continues executable task work. The post-integration cleanup prompt performs repository hygiene only after task implementation/acceptance content is already integrated.

## Authority boundary

Post-integration cleanup MUST NOT create a new implementation scope, modify product content, reopen acceptance, or invent another Task Contract.

The cleanup authority is the combination of:

- current `develop`;
- `AGENTS.md`;
- the completed task identity;
- merged PR records associated with that task;
- `docs/BRANCHING.md`;
- `docs/BRANCH-CLEANUP.md`.

The executor uses Git/GitHub state to derive which already-merged task branches remain eligible for retirement.

## Canonical prompt

```text
Operate as the Agente de IA Ejecutor for <owner>/<repository>.

Start from current develop and read AGENTS.md first.

Then perform post-integration branch cleanup for completed task <task-id> under the authoritative procedure:
docs/BRANCH-CLEANUP.md

Treat current Git/GitHub state, the completed task record, its merged PR records, and the referenced repository policies as the complete cleanup specification. Do not modify repository content, reopen task scope, or infer deletion safety from branch names or ancestry alone.

Complete remote and accessible-local branch retirement and verification, then return only:

STATUS: DONE | BLOCKED | PARTIAL
TASK: <task-id>
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```

Normal substitutions are limited to repository identity and task ID.

## Required semantics

The prompt is transport/bootstrap only. The executor MUST derive cleanup candidates from authoritative Git/GitHub records rather than from a chat-provided branch list.

For each candidate branch, the executor follows `docs/BRANCH-CLEANUP.md`, including exact merged-PR `head_sha` verification before deletion.

The executor cleans every accessible local checkout/worktree it controls and reports inaccessible checkouts as unverified rather than claiming they are clean.

No handoff commit is required solely for this closure phase because the task handoff and acceptance are already integrated. The durable audit surfaces are the completed Task Contract, reviews/acceptance records, merged PRs, Git history, and the Orchestrator's verified final remote state.

## Completion invariant

```text
accepted task != operationally closed task

operational closure = accepted/integrated task + post-integration branch retirement
```

A completed task is not considered branch-cleanup-closed until the merged task topic/review/acceptance branches are absent remotely and the accessible local checkout has been pruned accordingly, except for branches explicitly retained under `docs/BRANCH-CLEANUP.md`.

## Non-duplication rule

Do not add task-specific branch names, SHA values, PR numbers, cleanup commands, or deletion decisions to the launch prompt. Those facts belong to Git/GitHub state and repository policy.

If cleanup cannot be derived safely from authoritative state, return `BLOCKED` or `PARTIAL`; do not compensate with chat-only deletion instructions.
