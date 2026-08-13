# OP020 — Retire T012 planning branch

Operation ID: OP020  
Status: DRAFT  
Type: post-integration branch cleanup  
Base branch: `develop`

## Objective

Retire the merged Markdown planning branch that integrates T012 CodeGraph local-state ignore readiness, while preserving `main`, `develop`, repository content and unrelated work.

## Durable target

- PR: `<record after opening>`
- Purpose: integrate T012 planning, OP020 and checkpoint update
- Source branch/head identity: derive from that merged PR and canonical Git/GitHub state.

OP020 becomes `READY` only after the actual PR is recorded here and merged.

## Controlling references

- `AGENTS.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`
- merged GitHub record for the integration PR

## Authorized operations

Synchronize canonical refs, establish a safe current `develop` baseline, prove the exact merged source branch/head has no later unique work, retire only that branch, prune corresponding local/tracking refs in accessible checkouts, and report inaccessible checkouts as unverified.

## Exclusions

Do not modify repository content, delete `main`/`develop` or unrelated branches, discard unique/uncommitted work, initialize CodeGraph, or alter `.gitignore`.

## Verification

Return final remote/local branch inventories and confirm no repository content commit/push was created.

## Completion response

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP020
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```
