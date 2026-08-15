# OP051 — Retire T019 and lifecycle branches

Operation ID: OP051
Status: READY
Type: branch cleanup
Authorized base: `develop`

## Objective

After PR #123 is integrated into `develop`, retire exactly the merged T019 implementation branch and the T019-acceptance/T020-readiness lifecycle branch, restoring the canonical remote branch inventory to `develop`, `main` before T020 begins.

## Durable target identities

The operation covers exactly these merged PR source branches:

1. PR #122
   - base: `develop`
   - source branch: `refactor/t019-shared-governance-engine`
   - reviewed head: `fd71070f4b3ed08826fdde99ad34d81916bec21e`
   - integration commit: `e2525c54f4de5703b1614bc303346cb044e24a60`
2. PR #123
   - base: `develop`
   - source branch: `docs/t019-accept-t020-ready`
   - reviewed head: derive from the authoritative merged PR #123 GitHub record after integration
   - integration commit: derive from the authoritative merged PR #123 GitHub record after integration

PR #123 is deliberately resolved dynamically because this Operational Contract is authored on its own source branch. The authoritative derivation rule is: read merged PR #123 from GitHub after integration and use its recorded `head_sha` and merge/integration identity. No chat-carried SHA may substitute for that record.

## Controlling references

- `AGENTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/OPERATIONAL-CONTRACTS.md`
- PR #122
- PR #123

## Preconditions and safety invariants

- This contract is reachable from current `origin/develop` before execution.
- PRs #122 and #123 are both merged into `develop`, not merely closed.
- For every target branch that still exists remotely, its current remote HEAD must equal the reviewed PR `head_sha` from the authoritative PR record.
- A missing target remote branch is already-retired and is not an error.
- `develop` and `main` are long-lived protected targets for this operation and MUST NOT be moved or deleted.
- No branch may be reset or moved backward to manufacture a reviewed-head match.
- Local/uncommitted work must be preserved. If safe local cleanup cannot be established, report the checkout as an exception rather than discarding work.
- Squash-merge ancestry is not deletion authority; merged PR identity plus exact head equality controls remote retirement.

## Authorized operations

- Read the authoritative PR #122 and #123 merge/head records.
- Re-read current remote branch identities.
- Delete exactly these remote branches when their safety checks pass:
  - `refactor/t019-shared-governance-engine`
  - `docs/t019-accept-t020-ready`
- In every accessible local checkout/worktree, switch away from a retiring branch when safe, prune remote-tracking refs, and remove only the matching local branches after confirming no unrepresented work.
- Re-read the remote branch inventory after cleanup.

## Explicit exclusions

- Any repository file edit.
- Any commit, tag, release, issue, PR-content, provider, host configuration, permission, or dependency change.
- Any mutation of `develop`, `main`, or any branch not listed in this contract.
- Any force-update/reset of a target branch.
- Any deletion of a branch whose current HEAD differs from the reviewed merged-PR head.
- Any inference that inaccessible local checkouts are clean.

## Verification requirements

PASS requires:

- remote branches are exactly `develop`, `main` after cleanup;
- every deleted remote branch either was already absent or matched its authoritative reviewed PR head immediately before deletion;
- `develop` and `main` identities are unchanged by the cleanup operation;
- all accessible local checkouts report their remaining local branches after pruning;
- inaccessible or unsafe local checkouts are reported explicitly rather than guessed;
- no repository files were modified.

## Stop / escalation conditions

Return `BLOCKED` or `PARTIAL` without deleting the affected branch when:

- either target PR is not merged into `develop`;
- current remote branch HEAD differs from the merged PR reviewed head;
- the authoritative PR identity cannot be resolved;
- unique/unrepresented local work may exist;
- a target branch is active in a worktree that cannot be made safe without discarding work;
- any requested action would exceed the exact mutation scope above.

A safety failure on one branch must not authorize broader cleanup. Report exactly which target could not be retired.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP051
DESCRIPTION: Retire merged T019 implementation and lifecycle branches
RETIRED: <comma-separated retired/already-absent target branches, or none>
REMOTE_REMAINING: <comma-separated remote branches>
LOCAL_REMAINING: <comma-separated local branches visible in accessible checkouts>
EXCEPTIONS: <none or concise branch/checkout exceptions>
```
