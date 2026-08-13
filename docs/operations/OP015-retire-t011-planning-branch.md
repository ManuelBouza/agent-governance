# OP015 — Retire T011 planning branch

Operation ID: OP015  
Status: DRAFT  
Type: post-integration branch cleanup  
Base branch: `develop`

## Objective

Retire the merged Markdown planning branch that integrates T011 assurance active-routing verification readiness, while preserving `main`, `develop`, PR #81 activation candidate branch and repository content.

## Durable target

The PR integrating T011, this OP015 contract and the accompanying checkpoint MUST be recorded here before OP015 becomes `READY`.

Its merged source branch is the sole retirement target of this operation.

## Controlling references

- `AGENTS.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`
- merged Git/GitHub record for the durable target

## Authorized operations

The executor may synchronize canonical remote refs; establish a safe current local `develop` baseline under D042; inspect merged PR metadata, branches/worktrees and clean/dirty state; verify exact reviewed/current branch identity; delete only the target branch proven safe; prune corresponding local/tracking refs in accessible controlled checkouts; and report inaccessible checkouts as unverified.

## Explicit exclusions

The executor MUST NOT modify/create/commit/push repository content; delete `main` or `develop`; delete the PR #81 activation branch; delete unrelated branches; discard unique/uncommitted work; alter tags/releases/settings/rulesets/history; execute T011; merge/modify PR #81; initialize CodeGraph/SDD tracked state; or use chat-provided branch names/SHAs/deletion decisions as authority.

## Safety invariant

```text
merged PR + reviewed head_sha == current remote branch HEAD + no unique later work
=> eligible for retirement
```

If a safe current canonical baseline cannot be established without risking local work, return `BLOCKED`/`PARTIAL` rather than destructively synchronizing.

## Verification requirements

Before returning, re-fetch and report final remote/local branch inventories, retained/review branches with exact reason, confirmation that `main` and `develop` remain, confirmation that the PR #81 activation branch is untouched, confirmation no repository content commit/push was created, and inaccessible local checkouts explicitly unverified.

## Stop / escalation

Return `PARTIAL` or `BLOCKED` rather than guessing if the target cannot be proven safe.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP015
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```
