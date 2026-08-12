# OP005 — Retire T008 integration branches

Operation ID: OP005  
Status: READY  
Type: post-integration branch cleanup  
Base branch: `develop`

## Objective

Retire the merged branches created to accept, integrate, and close T008 while preserving `main`, `develop`, and unrelated active work.

## Durable targets

The executor MUST derive branch identity and exact reviewed-head evidence from:

- PR #67 — final T008 acceptance;
- PR #68 — exact accepted T008 implementation;
- PR #69 — T008 post-integration learning/checkpoint closure and this OP005 contract.

The source branch of PR #69 is intentionally included before merge so this operation can retire its own contract branch without recursive cleanup-contract creation.

## Controlling references

- `AGENTS.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`
- merged Git/GitHub records for the durable targets above

## Authorized operations

The executor may inspect canonical remote refs, merged PR metadata, local branches/worktrees and clean/dirty state; verify exact reviewed/current branch identity; delete only target branches proven safe; prune corresponding local/tracking refs in accessible controlled checkouts; and report inaccessible checkouts as unverified.

## Explicit exclusions

The executor MUST NOT modify/create/commit/push repository content; delete `main` or `develop`; delete unrelated branches; discard unique/uncommitted work; alter tags/releases/settings/rulesets/history; start or modify T006/D035/D036; change L001/L002 state; or use chat-provided branch names/SHAs/deletion decisions as authority.

## Safety invariant

```text
merged PR + reviewed head_sha == current remote branch HEAD + no unique later work
=> eligible for retirement
```

Unexpected drift, missing evidence, unique work, dirty local state, worktree ambiguity, or permission failure becomes `REVIEW`/stop for that branch.

## Verification requirements

Before returning, re-fetch and report final remote/local branch inventories, retained/review branches with exact reason, confirmation that `main` and `develop` remain, confirmation no repository content commit/push was created, and inaccessible local checkouts explicitly unverified.

## Stop / escalation

Return `PARTIAL` or `BLOCKED` rather than guessing if any target cannot be proven safe under the controlling policy.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP005
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```
