# OP003 — Retire T009 integration branches

Operation ID: OP003  
Status: DRAFT  
Type: post-integration branch cleanup  
Base branch: `develop`

## Objective

Retire the merged branches created to accept, integrate, and close T009 while preserving the active T008 implementation branch and long-lived branches.

## Durable targets

The executor MUST derive branch identity and exact reviewed-head evidence from:

- PR #63 — T009 acceptance (`docs/t009-acceptance`);
- PR #64 — accepted T009 implementation (`test/protocol-version-baseline-alignment`).

The PR integrating this OP003 contract MUST be added before OP003 becomes `READY` or is merged. Its source branch is intended to be retired by this same operation after merge.

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

The executor MUST NOT modify/create/commit/push repository content; delete `main`, `develop`, or `test/egll-deterministic-learning-detectors`; delete unrelated branches; discard unique/uncommitted work; alter tags/releases/settings/rulesets/history; start or modify T008/T006; or use chat-provided branch names/SHAs/deletion decisions as authority.

## Safety invariant

```text
merged PR + reviewed head_sha == current remote branch HEAD + no unique later work
=> eligible for retirement
```

Unexpected drift, missing evidence, unique work, dirty local state, worktree ambiguity, or permission failure becomes `REVIEW`/stop for that branch.

## Verification requirements

Before returning, re-fetch and report final remote/local branch inventories, retained/review branches with exact reason, confirmation that `main`, `develop`, and the active T008 branch remain, confirmation no repository content commit/push was created, and inaccessible local checkouts explicitly unverified.

## Stop / escalation

Return `PARTIAL` or `BLOCKED` rather than guessing if any target cannot be proven safe under the controlling policy.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP003
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```
