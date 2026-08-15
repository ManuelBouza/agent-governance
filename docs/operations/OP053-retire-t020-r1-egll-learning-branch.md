# OP053 — Retire T020-R1 EGLL learning branch

Operation ID: OP053
Status: READY
Type: branch cleanup
Authorized base: `develop`
Receipt anchor: PR #125

## Objective

After PR #125 is merged into `develop`, retire exactly its Markdown source branch `docs/t020-r1-egll-learning` while preserving the active T020 implementation branch and all canonical long-lived branches.

## Durable target identity

The operation covers exactly PR #125:

- base: `develop`
- source branch: `docs/t020-r1-egll-learning`
- reviewed head: derive from the authoritative merged PR #125 record after integration
- integration commit: derive from the authoritative merged PR #125 record after integration

The authoritative derivation rule is: read merged PR #125 from GitHub after integration and use its recorded source branch, `head_sha`, base, and merge/integration identity. No chat-carried SHA may substitute for that record.

## Controlling references

- `AGENTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/OPERATIONAL-CONTRACTS.md`
- PR #125

## Preconditions and safety invariants

- This contract is reachable from current `origin/develop` before execution.
- PR #125 is merged into `develop`, not merely closed.
- The current remote HEAD of `docs/t020-r1-egll-learning`, if the branch still exists, exactly equals PR #125's authoritative `head_sha`.
- Before the first branch mutation, the executor establishes that it can publish a top-level comment to PR #125. If it cannot, it returns `BLOCKED` before mutation.
- `develop`, `main`, and active T020 implementation branch `feat/t020-self-contained-governance-artifact` MUST NOT be moved or deleted.
- No branch may be reset or moved to manufacture a reviewed-head match.
- Local/uncommitted work must be preserved. Unsafe or inaccessible local cleanup is reported as an exception rather than discarded.
- Squash ancestry is not deletion authority; merged PR identity plus exact head equality controls retirement.

## Authorized operations

- Read authoritative PR #125 and current remote branch identities.
- Delete exactly remote branch `docs/t020-r1-egll-learning` if all safety checks pass.
- In accessible local checkouts/worktrees, switch away safely, prune remote-tracking refs, and remove only the matching local branch after confirming no unrepresented work.
- Re-read the remote branch inventory.
- Publish the final durable completion receipt as a top-level comment to PR #125 using `docs/OPERATIONAL-CONTRACTS.md`.

## Explicit exclusions

- Any repository file edit or commit.
- Any mutation of `develop`, `main`, `feat/t020-self-contained-governance-artifact`, or a branch other than `docs/t020-r1-egll-learning`.
- Any force update/reset.
- Any deletion when current branch HEAD differs from PR #125's authoritative reviewed head.
- Any issue/PR mutation other than publishing the contract-defined receipt comment to PR #125.
- Any inference that inaccessible local checkouts are clean.

## Verification requirements

PASS requires:

- `docs/t020-r1-egll-learning` is absent from the remote after cleanup;
- `develop`, `main`, and `feat/t020-self-contained-governance-artifact` remain present and unchanged by cleanup;
- the retired branch either was already absent or matched PR #125's authoritative merged-PR head immediately before deletion;
- accessible local checkouts report remaining local branches;
- exceptions are explicit;
- no repository files were modified;
- the final durable GitHub receipt was successfully published to PR #125 and contains every completion field below.

## Stop / escalation conditions

Return `BLOCKED` before mutation when:

- PR #125 cannot be resolved or is not merged into `develop`;
- durable receipt publication capability cannot be established;
- current remote branch HEAD differs from PR #125's authoritative reviewed head;
- unique/unrepresented local work may exist and safe retirement cannot be established;
- requested action would exceed exact scope.

If branch mutation completes but final receipt publication unexpectedly fails, stop further mutation and return `PARTIAL` through the interactive channel.

## Completion response

Publish this exact completion block inside the required durable receipt envelope, then return the same block interactively:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP053
DESCRIPTION: Retire T020-R1 EGLL learning branch
RETIRED: <docs/t020-r1-egll-learning or already-absent or none>
REMOTE_REMAINING: <comma-separated remote branches>
LOCAL_REMAINING: <comma-separated local branches visible in accessible checkouts>
EXCEPTIONS: <none or concise branch/checkout/receipt exceptions>
```
