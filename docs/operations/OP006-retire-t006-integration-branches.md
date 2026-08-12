# OP006 — Retire T006 integration branches

Operation ID: OP006  
Status: READY  
Type: post-integration branch cleanup  
Base branch: `develop`

## Objective

Retire the merged branches created to accept, integrate, and close T006 while preserving `main`, `develop`, unrelated work, and repository content.

## Durable targets

The executor MUST derive branch identity and exact reviewed-head evidence from:

- PR #70 — T006 acceptance (`docs/t006-acceptance`);
- PR #71 — accepted T006 implementation (`test/security-verification-contract`);
- PR #72 — T006 post-integration cleanup contract (`docs/t006-post-integration-cleanup`).

The source branch of PR #72 is intentionally included so this operation can retire its own merged planning branch without recursive chat-only cleanup authority.

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

The executor MUST NOT modify/create/commit/push repository content; delete `main` or `develop`; delete unrelated branches; discard unique/uncommitted work; alter tags/releases/settings/rulesets/history; start or modify D036; modify D035/T006 semantics; fold L002 into cleanup; or use chat-provided branch names/SHAs/deletion decisions as authority.

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
OPERATION: OP006
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```
