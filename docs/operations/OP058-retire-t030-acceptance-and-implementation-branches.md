# OP058 — Retire T030 acceptance and implementation branches

Operation ID: OP058  
Status: READY  
Type: post-integration branch cleanup  
Authorized base: `develop`  
Receipt anchor: PR #133

## Objective

After both T030-R2 acceptance PR #133 and the exact accepted T030 implementation PR #132 are merged into `develop`, retire only their source branches and restore the normal remote branch inventory to `develop, main`.

This operation performs cleanup only. It does not create a D045 continuation because the next RCAB step is an Orchestrator-owned policy/context-map decision based on the newly canonical T030 baseline.

## Durable targets

1. Acceptance PR #133 source branch `docs/t030-r2-acceptance`.
2. Implementation PR #132 source branch `infra/t030-repository-context-baseline`.

For each target, derive the reviewed source HEAD and merge identity from the authoritative merged PR record. Do not use chat-carried SHAs as authority.

PR #132 is eligible for cleanup only when its merged reviewed HEAD equals the exact T030-R2 accepted executor HEAD recorded in `docs/reviews/T030-R2.md`.

## Controlling references

- `AGENTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/OPERATIONAL-CONTRACTS.md`
- `docs/reviews/T030-R2.md`
- merged PR #132
- merged PR #133

## Authorized operations

- Read authoritative PR #132 and PR #133 records plus current remote/local branch state.
- Verify both PRs are merged into `develop` and PR #132's reviewed head is exactly the accepted T030-R2 head.
- Delete remote branch `docs/t030-r2-acceptance` only when present and equal to PR #133's reviewed source HEAD.
- Delete remote branch `infra/t030-repository-context-baseline` only when present and equal to PR #132's reviewed source HEAD.
- In accessible local checkouts/worktrees, safely switch away, prune tracking refs, and remove only those matching local branches when no unrepresented work exists.
- Re-read remote/local branch inventories.
- Publish the final durable receipt to PR #133.

## Explicit exclusions

- No repository content edits or commits.
- No mutation of `develop` or `main`.
- No force/reset.
- No deletion on reviewed-head mismatch.
- No cleanup of unrelated branches.
- No T021 launch, context-map authoring, budget policy, document split, release action, or T026 action.

## Preconditions and safety invariants

- This contract is reachable from current `origin/develop`.
- PR #133 is merged.
- PR #132 is merged and its reviewed head equals the accepted T030-R2 head.
- `develop` contains both the T030-R2 acceptance record and T030 implementation content.
- Before first mutation, the executor establishes ability to publish a top-level receipt comment to PR #133.
- Local/uncommitted work is preserved.

## Verification requirements

Completion passes only when:

- `docs/t030-r2-acceptance` is absent remotely;
- `infra/t030-repository-context-baseline` is absent remotely;
- remote branches are exactly `develop, main`;
- both retired branches were already absent or matched their authoritative reviewed heads immediately before deletion;
- accessible local branch state is reported;
- no repository files were modified;
- exceptions are explicit;
- the final receipt publication succeeds.

## Stop / escalation

Return `BLOCKED` before mutation if either PR is not merged, PR #132 does not correspond to the exact accepted T030-R2 head, a cleanup target's current head mismatches its authoritative PR head, receipt publication capability is unavailable, local work cannot be preserved safely, or the requested action would exceed scope.

If deletion succeeds but receipt publication fails, return `PARTIAL` and perform no broader compensating mutation.

## Completion response / durable receipt

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP058
DESCRIPTION: Retire accepted T030 acceptance and implementation branches
RETIRED: <comma-separated retired/already-absent targets or none>
REMOTE_REMAINING: <comma-separated remote branches>
LOCAL_REMAINING: <comma-separated local branches visible in accessible checkouts>
EXCEPTIONS: <none or concise exceptions>
```
