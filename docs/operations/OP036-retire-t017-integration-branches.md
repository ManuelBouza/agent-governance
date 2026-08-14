# OP036 — Retire integrated T017 branches

Operation ID: OP036
Status: READY_AFTER_CARRYING_PR_AND_T017_MERGED
Type: branch cleanup
Base branch: `develop`

## Objective

Retire the ChatGPT-owned T017 acceptance/release-transition branch and the accepted T017 executor branch after both carrying pull requests are proven merged.

## Authorized targets

1. `docs/t017-acceptance-release-transition`
   - eligible only after the pull request carrying T017-R1, this Operational Contract and checkpoint O073 is proven merged into `develop`;
   - required head is the exact merged PR head for this branch.

2. `feat/consumer-governance-cli-v1`
   - required reviewed head: `6a6343a78ebce5fb585722840b6d728d9d1fab93`;
   - eligible only after its implementation pull request is proven merged into `develop`.

## Boundaries

Branch retirement only. Do not modify repository files, rewrite commits, force-push surviving refs, close an unmerged PR, or delete `develop`, `main`, or unrelated branches.

If a target PR is unmerged, a target head differs from its required identity, or identity is ambiguous, leave that target untouched and report BLOCKED/PARTIAL.

Preserve and report any unrelated branch rather than broadening cleanup scope.

## Verification

Before deletion, synchronize the canonical remote and establish a current safe local `develop` baseline. Prove each target PR is merged and each branch still points to its required head.

After deletion, enumerate remote branches and local branches. Prune only stale tracking data needed to observe the result.

Expected remote result if no unrelated branch exists: exactly `develop`, `main`.

## Completion response

STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP036
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
