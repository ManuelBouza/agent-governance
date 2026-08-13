# OP011 — Retire conditional AGENTS reload planning branch

Operation ID: OP011  
Status: READY  
Type: post-integration branch cleanup  
Base branch: `develop`

## Objective

Retire the merged Markdown planning branch that integrates D043 host-native repository-instruction loading and the conditional `AGENTS.md` reload policy, while preserving `main`, `develop`, the still-pending OP010 target and repository content.

## Durable target

- PR: `#79`
- Purpose: D043 host-native repository-instruction loading plus conditional `AGENTS.md` reload policy
- Source branch/head identity: derive from merged PR #79 and canonical Git/GitHub state at execution time.

The merged source branch of PR #79 is the sole retirement target of this operation.

## Controlling references

- `AGENTS.md`
- `docs/decisions/D043-host-native-repository-instruction-loading.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`
- merged Git/GitHub record for PR #79

## Authorized operations

The executor may synchronize canonical remote refs; establish a safe current local `develop` baseline under D042; inspect merged PR metadata, branches/worktrees and clean/dirty state; verify exact reviewed/current branch identity; delete only the target branch proven safe; prune corresponding local/tracking refs in accessible controlled checkouts; and report inaccessible checkouts as unverified.

## Explicit exclusions

The executor MUST NOT modify/create/commit/push repository content; delete `main` or `develop`; delete the OP010-controlled branch; delete unrelated branches; discard unique/uncommitted work; alter tags/releases/settings/rulesets/history; perform D040 Phase-B activation; initialize CodeGraph/SDD project state; or use chat-provided branch names/SHAs/deletion decisions as authority.

## Safety invariant

```text
merged PR + reviewed head_sha == current remote branch HEAD + no unique later work
=> eligible for retirement
```

If a safe current canonical baseline cannot be established without risking local work, return `BLOCKED`/`PARTIAL` rather than destructively synchronizing.

## Verification requirements

Before returning, re-fetch and report final remote/local branch inventories, retained/review branches with exact reason, confirmation that `main` and `develop` remain, confirmation the OP010 target was untouched, confirmation no repository content commit/push was created, and inaccessible local checkouts explicitly unverified.

## Stop / escalation

Return `PARTIAL` or `BLOCKED` rather than guessing if the target cannot be proven safe.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP011
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```
