# OP060 — Retire T031 branches and start T021

Operation ID: OP060  
Status: READY  
Type: branch cleanup with D045 preauthorized continuation  
Authorized base: `develop`  
Receipt anchor: PR #136

## Objective

After T031 acceptance PR #136, exact accepted implementation PR #135, and wording-correction PR #137 are merged into `develop`, retire exactly their source branches, publish the normal durable Operational receipt, and — only if every deterministic cleanup/re-bootstrap condition passes — continue in the same executor invocation with the already-authorized T021 implementation.

This operation uses D045 only to remove transport/acknowledgement latency between deterministic post-integration cleanup and one already-authorized executor Task. It does not delegate Markdown, architecture, policy, review, or acceptance authority.

## Stage A — retire T031 branches

Targets exactly:

1. PR #136 source branch `docs/t031-r1-acceptance-push-policy`;
2. PR #135 source branch `infra/t031-context-manifest-ratchet`;
3. PR #137 source branch `docs/t031-policy-wording-fix`.

For each target, derive the reviewed source HEAD and merge identity from the authoritative merged PR record. Do not use chat-carried SHAs as cleanup authority.

PR #135 is eligible for cleanup only when its merged reviewed head equals the exact T031-R1 accepted executor HEAD recorded in `docs/reviews/T031-R1.md`.

Before deletion, verify:

- PR #136 is merged into `develop`;
- PR #135 is merged into `develop` and corresponds to the exact accepted T031-R1 head;
- PR #137 is merged into `develop`;
- each target branch is already absent or still equals its authoritative reviewed PR head;
- no later unique work exists on any target;
- `develop` and `main` identities will not be mutated;
- receipt publication capability to PR #136 is available;
- local/uncommitted work can be preserved.

If eligible, delete only the three target branches, safely remove/prune matching accessible local/tracking state, and re-read inventories.

Stage A passes only when:

- all three targets are absent remotely;
- remote branches are exactly `develop, main`;
- local branch inventory is reported;
- repository content is unchanged by cleanup;
- exceptions are `none`;
- durable receipt publication to PR #136 succeeds.

## Stage-A durable receipt

Publish a top-level PR #136 comment containing:

```text
AGENT-GOVERNANCE-OPERATION-RECEIPT v1
CONTRACT: docs/operations/OP060-retire-t031-branches-and-start-t021.md
BASE_SHA: <current canonical develop used for the operation>

STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP060
DESCRIPTION: Retire accepted T031 branches before T021 continuation
RETIRED: <comma-separated targets or none>
REMOTE_REMAINING: <comma-separated remote branches>
LOCAL_REMAINING: <comma-separated local branches visible in accessible checkouts>
EXCEPTIONS: <none or concise exceptions>
```

No Stage B work is eligible until this receipt exists durably and Stage-A postconditions pass.

## Stage B — D045 preauthorized T021 continuation

When and only when Stage A passes:

1. synchronize `origin/develop` again;
2. establish a safe local baseline equal to current `origin/develop`;
3. verify that current canonical `develop` contains:
   - this OP060 contract;
   - `docs/reviews/T031-R1.md` with T031 ACCEPTED and corrected publication-policy wording;
   - D048 and the updated `docs/EXECUTOR-HANDOFFS.md` publication rule;
   - `docs/tasks/T021-consumer-profile-abstraction-zero-drift.md` with status `READY`;
4. load current `AGENTS.md` through normal repository-native bootstrap, then load T021 and its referenced authority directly from current canonical `develop`;
5. create/use only T021's expected implementation branch from that current canonical base;
6. execute T021 exactly as authorized, including D048's normal-task single planned final push boundary;
7. persist/push the T021 handoff and return T021's canonical completion response.

No Human acknowledgement is required between eligible Stage A and Stage B because T021 is already authorized, T030/T031 have cleared its RCAB sequencing prerequisite, and no Human/Orchestrator judgment gate remains between deterministic cleanup and task launch.

## Explicit exclusions

- No repository content mutation during Stage A.
- No deletion of `develop`, `main`, or unrelated branches.
- No force/reset/history rewrite.
- No Markdown edit in Stage B.
- No T031 implementation/review semantic change.
- No source-maintainer profile implementation.
- No document split or hard source size budget.
- No Consumer Skill activation/description change.
- No release action or T026 action.
- No continuation if Stage-A receipt/postconditions fail.

## Stop / escalation

Return `BLOCKED` before mutation/continuation if:

- any required PR is not merged;
- PR #135 does not correspond to the exact accepted T031-R1 head;
- a cleanup target advanced beyond its reviewed PR head or contains unrepresented unique work;
- receipt publication capability is unavailable;
- cleanup would exceed scope or risk local work;
- current `develop` after Stage A does not contain the required acceptance/policy/T021 authority;
- a safe current canonical bootstrap cannot be established.

If Stage A succeeds but receipt publication fails, return `PARTIAL` and do not start T021.

If Stage A passes and T021 later blocks, return T021's contract-defined `BLOCKED` handoff/status; do not broaden scope.
