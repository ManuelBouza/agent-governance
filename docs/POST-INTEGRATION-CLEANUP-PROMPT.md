# Post-Integration Cleanup Prompt

Status: ACTIVE

## Purpose

Define the canonical executor prompt used after an authorized source-product change has been integrated and only branch-retirement work remains.

This prompt is distinct from the normal Task Contract launch prompt in `docs/TASK-CONTRACTS.md`.

The normal launch prompt starts or continues executable task work. The post-integration cleanup prompt performs repository hygiene only after the relevant content is already integrated.

## Cleanup target

A cleanup target is exactly one durable integration identity:

- `TASK <task-id>` for a Task-Contract-governed change; or
- `PR <number>` for an integrated source change that has no Task ID, such as a Markdown-only maintenance PR.

Do not identify the cleanup target with a branch list. Branch candidates are derived from Git/GitHub history.

## Authority boundary

Post-integration cleanup MUST NOT create a new implementation scope, modify product content, reopen acceptance, or invent another Task Contract.

The cleanup authority is the combination of:

- current `develop`;
- `AGENTS.md`;
- the cleanup target identity;
- the target's merged PR records and related integration history;
- `docs/BRANCHING.md`;
- `docs/BRANCH-CLEANUP.md`.

The executor uses Git/GitHub state to derive which already-integrated branches remain eligible for retirement.

## Canonical prompt

```text
Operate as the Agente de IA Ejecutor for <owner>/<repository>.

Start from current develop and read AGENTS.md first.

Then perform post-integration branch cleanup for <cleanup-target> under the authoritative procedure:
docs/BRANCH-CLEANUP.md

Treat current Git/GitHub state, the cleanup target's integrated records, and the referenced repository policies as the complete cleanup specification. Do not modify repository content, reopen scope, or infer deletion safety from branch names or ancestry alone.

Complete remote and accessible-local branch retirement and verification, then return only:

STATUS: DONE | BLOCKED | PARTIAL
TARGET: <cleanup-target>
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```

Normal substitutions are limited to repository identity and exactly one cleanup target (`TASK <task-id>` or `PR <number>`).

## Required semantics

The prompt is transport/bootstrap only. The executor MUST derive cleanup candidates from authoritative Git/GitHub records rather than from a chat-provided branch list.

For each candidate branch, the executor follows `docs/BRANCH-CLEANUP.md`, including exact merged-PR `head_sha` verification before deletion.

The executor cleans every accessible local checkout/worktree it controls and reports inaccessible checkouts as unverified rather than claiming they are clean.

No handoff commit is required solely for this closure phase because the governed content is already integrated. The durable audit surfaces are the Task Contract/reviews when applicable, merged PRs, Git history, and the Orchestrator's verified final remote state.

## Completion invariant

```text
integrated change != operationally closed change

operational closure = integrated change + post-integration branch retirement
```

A cleanup target is not operationally closed until its eligible merged topic/review/acceptance/implementation branches are absent remotely and the accessible local checkout has been pruned accordingly, except for branches explicitly retained under `docs/BRANCH-CLEANUP.md`.

## Non-duplication rule

Do not add branch names, SHA values, cleanup commands, or deletion decisions to the prompt. Those facts belong to Git/GitHub state and repository policy.

If cleanup cannot be derived safely from authoritative state, return `BLOCKED` or `PARTIAL`; do not compensate with chat-only deletion instructions.
