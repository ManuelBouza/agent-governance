# OP004 — Retire T008-R2 planning branch

Operation ID: OP004  
Status: READY  
Type: post-integration branch cleanup  
Base branch: `develop`

## Objective

After PR #66 is merged, retire only its source planning branch while preserving the active T008 implementation branch and long-lived branches.

## Durable target

- PR #66 — `docs/t008-r2-handoff-identity`.

The executor MUST derive current branch identity and reviewed head evidence from Git/GitHub.

## Controlling references

- `AGENTS.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`
- merged PR #66 records

## Authorized operations

Inspect canonical remote/local refs and PR metadata; verify PR #66 merged and source branch remains at its reviewed head with no unique later work; retire that remote branch and corresponding safe accessible-local branch/tracking ref; report inaccessible checkouts as unverified.

## Explicit exclusions

Do not modify repository content; do not delete `main`, `develop`, or `test/egll-deterministic-learning-detectors`; do not delete unrelated branches; do not start/modify T008; do not infer safety from naming or ancestry alone; do not use chat-supplied branch/SHA decisions as authority.

## Safety invariant

```text
merged PR #66 + reviewed head_sha == current source branch HEAD + no unique later work
=> eligible for retirement
```

Unexpected drift, unique work, dirty local state, worktree ambiguity, or missing evidence becomes `REVIEW` and returns `PARTIAL`/`BLOCKED`.

## Verification

Re-fetch final remote/local inventories; confirm `main`, `develop`, and active T008 branch remain; confirm PR #66 source branch is absent if safely retired; confirm no repository content commit/push occurred.

## Completion response

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP004
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```
