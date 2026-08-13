# OP009 — Retire T010 integration branches

Operation ID: OP009  
Status: DRAFT  
Type: post-integration branch cleanup  
Base branch: `develop`

## Objective

Retire the merged source branches used for T010 acceptance, T010 implementation integration, and this OP009 cleanup contract after all three PR identities are durably recorded, while preserving `main`, `develop`, the still-pending D041/OP008 branch and repository content.

## Durable targets

The sole retirement targets are the source branches of these merged PRs:

- T010 acceptance PR #75;
- T010 implementation PR #76;
- the PR integrating this OP009 contract.

The third PR identity MUST be persisted here before OP009 becomes `READY`.

## Controlling references

- `AGENTS.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`
- merged Git/GitHub records for the durable targets

## Authorized operations

The executor may inspect canonical remote refs, merged PR metadata, local branches/worktrees and clean/dirty state; verify exact reviewed/current branch identity; delete only target branches proven safe; prune corresponding local/tracking refs in accessible controlled checkouts; and report inaccessible checkouts as unverified.

## Explicit exclusions

The executor MUST NOT modify/create/commit/push repository content; delete `main` or `develop`; delete `docs/executor-process-autonomy` under OP008; delete unrelated branches; discard unique/uncommitted work; alter tags/releases/settings/rulesets/history; perform D040 Phase-B activation; change T010/D036/D041 semantics; initialize CodeGraph or external SDD/project state; act on L002; or use chat-provided branch names/SHAs/deletion decisions as authority.

## Safety invariant

```text
merged PR + reviewed head_sha == current remote branch HEAD + no unique later work
=> eligible for retirement
```

Unexpected drift, missing evidence, unique work, dirty local state, worktree ambiguity or permission failure becomes `REVIEW`/stop for that branch.

## Verification requirements

Before returning, re-fetch and report final remote/local branch inventories, retained/review branches with exact reason, confirmation that `main` and `develop` remain, confirmation that the OP008 target branch remains untouched if still present, confirmation no repository content commit/push was created, and inaccessible local checkouts explicitly unverified.

## Stop / escalation

Return `PARTIAL` or `BLOCKED` rather than guessing if any target cannot be proven safe.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP009
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```
