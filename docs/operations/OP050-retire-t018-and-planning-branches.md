# OP050 — Retire T018 and planning branches

Operation ID: OP050
Status: DONE
Type: branch cleanup
Authorized base: `develop`

## Completion / lifecycle

OP050 completed before T019 execution. The executor reported all three target branches retired, remote remaining `develop, main`, local remaining `develop, main, origin`, and no exceptions. ChatGPT independently re-read GitHub after completion and verified the canonical remote exposed exactly `develop` and `main`; `develop` remained unchanged at `9148be3c11c85d2bc7e0c43e3e8e86f110b2682f`. No repository-content mutation was attributed to the cleanup operation.

## Objective

After PR #121 is integrated into `develop`, retire exactly the merged topic branches left by MG0/T018 acceptance and restore the canonical remote branch inventory to `develop`, `main` before T019 begins.

## Durable target identities

The operation covers exactly these merged PR source branches:

1. PR #119
   - base: `develop`
   - source branch: `docs/unified-governance-refactor-plan`
   - reviewed head: `c3b043db8b72437c4679e776ba120c24c05ca8cb`
   - integration commit: `f8782e93c446bab1f16bc9022bb3ec868dff7fc5`
2. PR #120
   - base: `develop`
   - source branch: `test/t018-consumer-v1-characterization`
   - reviewed head: `fe66bda778147648c30e3ed3c7c11c11f547ca00`
   - integration commit: `85bdb75537eab98bf8b1bd1f603809a33ab23603`
3. PR #121
   - base: `develop`
   - source branch: `docs/t018-accept-t019-ready`
   - reviewed head: derive from the authoritative merged PR #121 GitHub record after integration
   - integration commit: derive from the authoritative merged PR #121 GitHub record after integration

PR #121 is deliberately resolved dynamically because this Operational Contract is authored on its own source branch. The authoritative derivation rule is: read merged PR #121 from GitHub after integration and use its recorded `head_sha` and merge/integration identity. No chat-carried SHA may substitute for that record.

## Controlling references

- `AGENTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/OPERATIONAL-CONTRACTS.md`
- PR #119
- PR #120
- PR #121

## Preconditions and safety invariants

- This contract is reachable from current `origin/develop` before execution.
- PRs #119, #120, and #121 are all merged into `develop`, not merely closed.
- For every target branch that still exists remotely, its current remote HEAD must equal the reviewed PR `head_sha` from the authoritative PR record.
- A missing target remote branch is already-retired and is not an error.
- `develop` and `main` are long-lived protected targets for this operation and MUST NOT be moved or deleted.
- No branch may be reset or moved backward to manufacture a reviewed-head match.
- Local/uncommitted work must be preserved. If safe local cleanup cannot be established, report the checkout as an exception rather than discarding work.
- Squash-merge ancestry is not deletion authority; merged PR identity plus exact head equality controls remote retirement.

## Authorized operations

- Read the authoritative PR #119, #120, and #121 merge/head records.
- Re-read current remote branch identities.
- Delete exactly these remote branches when their safety checks pass:
  - `docs/unified-governance-refactor-plan`
  - `test/t018-consumer-v1-characterization`
  - `docs/t018-accept-t019-ready`
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

- any target PR is not merged into `develop`;
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
OPERATION: OP050
DESCRIPTION: Retire merged T018 planning and implementation branches
RETIRED: <comma-separated retired/already-absent target branches, or none>
REMOTE_REMAINING: <comma-separated remote branches>
LOCAL_REMAINING: <comma-separated local branches visible in accessible checkouts>
EXCEPTIONS: <none or concise branch/checkout exceptions>
```
