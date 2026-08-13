# OP014 — Retire D040 Phase-B assurance activation branch

Operation ID: OP014  
Status: DRAFT  
Type: post-integration branch cleanup  
Base branch: `develop`

## Objective

Retire the merged Markdown activation branch that completes D040 Phase B and activates D036 Assurance Core under Protocol `1.13.0`, while preserving `main`, `develop`, repository content and any later unrelated work.

## Durable target

The PR integrating the D040 Phase-B activation candidate MUST be recorded here before OP014 becomes `READY`.

Its merged source branch is the sole retirement target of this operation.

## Controlling references

- `AGENTS.md`
- `docs/decisions/D040-atomic-protocol-migration-and-single-version-authority.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`
- merged Git/GitHub record for the durable target

## Authorized operations

The executor may synchronize canonical remote refs; establish a safe current local `develop` baseline under D042; inspect merged PR metadata, branches/worktrees and clean/dirty state; verify exact reviewed/current branch identity; delete only the target branch proven safe; prune corresponding local/tracking refs in accessible controlled checkouts; and report inaccessible checkouts as unverified.

## Explicit exclusions

The executor MUST NOT modify/create/commit/push repository content; delete `main` or `develop`; delete unrelated branches; discard unique/uncommitted work; alter tags/releases/settings/rulesets/history; change D036/D040/L001 semantics; initialize CodeGraph/SDD tracked state; or use chat-provided branch names/SHAs/deletion decisions as authority.

## Safety invariant

```text
merged PR + reviewed head_sha == current remote branch HEAD + no unique later work
=> eligible for retirement
```

If a safe current canonical baseline cannot be established without risking local work, return `BLOCKED`/`PARTIAL` rather than destructively synchronizing.

## Verification requirements

Before returning, re-fetch and report final remote/local branch inventories, retained/review branches with exact reason, confirmation that `main` and `develop` remain, confirmation no repository content commit/push was created, and inaccessible local checkouts explicitly unverified.

## Stop / escalation

Return `PARTIAL` or `BLOCKED` rather than guessing if the target cannot be proven safe.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP014
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```
