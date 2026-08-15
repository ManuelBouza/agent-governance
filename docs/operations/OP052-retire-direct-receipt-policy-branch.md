# OP052 — Retire direct-receipt policy branch

Operation ID: OP052
Status: READY
Type: branch cleanup
Authorized base: `develop`
Receipt anchor: PR #124

## Objective

After PR #124 integrating the direct Operational Contract receipt policy is merged into `develop`, retire exactly its Markdown source branch `docs/direct-operation-receipts` and restore the canonical remote branch inventory to `develop`, `main` before T020 begins.

## Durable target identity

The operation covers exactly PR #124:

- base: `develop`
- source branch: `docs/direct-operation-receipts`
- reviewed head: derive from the authoritative merged PR #124 record after integration
- integration commit: derive from the authoritative merged PR #124 record after integration

The authoritative derivation rule is: read merged PR #124 from GitHub after integration and use its recorded source branch, `head_sha`, base, and merge/integration identity. No chat-carried SHA may substitute for that record.

## Controlling references

- `AGENTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/OPERATIONAL-CONTRACTS.md`
- PR #124

## Preconditions and safety invariants

- This contract is reachable from current `origin/develop` before execution.
- PR #124 is merged into `develop`, not merely closed.
- The current remote HEAD of `docs/direct-operation-receipts`, if the branch still exists, exactly equals PR #124's authoritative `head_sha`.
- Before the first branch mutation, the executor establishes that it can publish a top-level comment to PR #124. If it cannot, it returns `BLOCKED` before mutation.
- `develop` and `main` MUST NOT be moved or deleted.
- No branch may be reset or moved to manufacture a reviewed-head match.
- Local/uncommitted work must be preserved. Unsafe or inaccessible local cleanup is reported as an exception rather than discarded.
- Squash ancestry is not deletion authority; merged PR identity plus exact head equality controls retirement.

## Authorized operations

- Read authoritative PR #124 and current remote branch identities.
- Delete exactly remote branch `docs/direct-operation-receipts` if all safety checks pass.
- In accessible local checkouts/worktrees, switch away safely, prune remote-tracking refs, and remove only the matching local branch after confirming no unrepresented work.
- Re-read the remote branch inventory.
- Publish the final durable completion receipt as a top-level comment to PR #124 using `docs/OPERATIONAL-CONTRACTS.md`.

## Explicit exclusions

- Any repository file edit or commit.
- Any mutation of `develop`, `main`, or a branch other than `docs/direct-operation-receipts`.
- Any force update/reset.
- Any deletion when current branch HEAD differs from PR #124's authoritative reviewed head.
- Any issue/PR mutation other than publishing the contract-defined receipt comment to PR #124.
- Any inference that inaccessible local checkouts are clean.

## Verification requirements

PASS requires:

- the remote branch inventory is exactly `develop`, `main` after cleanup;
- the retired branch either was already absent or matched PR #124's authoritative merged-PR head immediately before deletion;
- `develop` and `main` identities are unchanged by cleanup;
- accessible local checkouts report remaining local branches;
- exceptions are explicit;
- no repository files were modified;
- the final durable GitHub receipt was successfully published to PR #124 and contains every completion field below.

## Stop / escalation conditions

Return `BLOCKED` before mutation when:

- PR #124 cannot be resolved or is not merged into `develop`;
- durable receipt publication capability cannot be established;
- current remote branch HEAD differs from PR #124's authoritative reviewed head;
- unique/unrepresented local work may exist and safe retirement cannot be established;
- requested action would exceed exact scope.

If branch mutation completes but final receipt publication unexpectedly fails, stop further mutation and return `PARTIAL` through the interactive channel.

## Completion response

Publish this exact completion block inside the required durable receipt envelope, then return the same block interactively:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP052
DESCRIPTION: Retire direct-receipt policy branch
RETIRED: <docs/direct-operation-receipts or already-absent or none>
REMOTE_REMAINING: <comma-separated remote branches>
LOCAL_REMAINING: <comma-separated local branches visible in accessible checkouts>
EXCEPTIONS: <none or concise branch/checkout/receipt exceptions>
```
