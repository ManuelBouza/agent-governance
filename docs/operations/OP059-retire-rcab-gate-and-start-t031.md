# OP059 — Retire RCAB policy branch and start T031

Operation ID: OP059  
Status: READY  
Type: branch cleanup with D045 preauthorized continuation  
Authorized base: `develop`  
Receipt anchor: PR #134

## Objective

After PR #134 is merged into `develop`, retire exactly its Markdown source branch, publish the normal durable Operational receipt, and — only if every deterministic cleanup/re-bootstrap condition passes — continue in the same executor invocation with the already-authorized T031 implementation.

This operation uses D045 only to remove transport/acknowledgement latency between a deterministic Markdown-branch cleanup and one already-authorized executor Task. It does not delegate any Markdown, architecture, policy or acceptance authority to the executor.

## Stage A — retire the RCAB policy branch

Target exactly:

- PR #134 source branch `docs/rcab-v1-context-gate`.

Derive the reviewed source HEAD and merge identity from the authoritative merged PR #134 record. Do not use chat-carried SHAs as authority.

Before deletion, verify:

- PR #134 is merged into `develop`;
- the target remote branch is already absent or still equals PR #134's reviewed source HEAD;
- no later unique work exists on the target;
- `develop` and `main` identities will not be mutated;
- receipt publication capability to PR #134 is available;
- local/uncommitted work can be preserved.

If eligible, delete only `docs/rcab-v1-context-gate`, safely remove/prune matching accessible local/tracking state, and re-read inventories.

Stage A passes only when:

- target branch is absent remotely;
- remote branches are exactly `develop, main`;
- local branch inventory is reported;
- repository content is unchanged by cleanup;
- exceptions are `none`;
- durable receipt publication to PR #134 succeeds.

## Stage-A durable receipt

Publish a top-level PR #134 comment containing:

```text
AGENT-GOVERNANCE-OPERATION-RECEIPT v1
CONTRACT: docs/operations/OP059-retire-rcab-gate-and-start-t031.md
BASE_SHA: <current canonical develop used for the operation>

STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP059
DESCRIPTION: Retire RCAB policy branch before T031 continuation
RETIRED: <docs/rcab-v1-context-gate or none>
REMOTE_REMAINING: <comma-separated remote branches>
LOCAL_REMAINING: <comma-separated local branches visible in accessible checkouts>
EXCEPTIONS: <none or concise exceptions>
```

No Stage B work is eligible until this receipt exists durably and Stage-A postconditions pass.

## Stage B — D045 preauthorized T031 continuation

When and only when Stage A passes:

1. synchronize `origin/develop` again;
2. establish a safe local baseline equal to current `origin/develop`;
3. verify that current canonical `develop` contains:
   - this OP059 contract;
   - D047;
   - `docs/CONTEXT-MAP.md`;
   - `docs/tasks/T031-rcab-context-manifest-and-ratchet.md`;
4. load current `AGENTS.md` through normal repository-native bootstrap and then load the T031 Task Contract plus its referenced authority directly from current canonical `develop`;
5. create/use only the T031 expected implementation branch from that current canonical base;
6. execute T031 exactly as authorized;
7. persist/push the T031 handoff and return the canonical T031 completion response.

No Human acknowledgement is required between eligible Stage A and Stage B because T031 is already authorized by the integrated Task Contract and no Human/Orchestrator judgment gate exists between cleanup and task launch.

## Explicit exclusions

- No repository content mutation during Stage A.
- No deletion of `develop`, `main`, or unrelated branches.
- No force/reset.
- No Markdown edit in Stage B.
- No change to D047 policy/map semantics.
- No T021 implementation in this invocation.
- No document split, hard source size budget, Consumer/Core/Skill/runtime change, release action, or T026 action.
- No continuation if Stage-A receipt/postconditions fail.

## Stop / escalation

Return `BLOCKED` before mutation/continuation if:

- PR #134 is not merged;
- target branch advanced beyond its reviewed PR head or contains unrepresented unique work;
- receipt publication capability is unavailable;
- cleanup would exceed scope or risk local work;
- current `develop` after Stage A does not contain OP059, D047, the context map and T031;
- a safe current canonical bootstrap cannot be established.

If Stage A succeeds but receipt publication fails, return `PARTIAL` and do not start T031.

If Stage A passes and T031 later blocks, return T031's contract-defined `BLOCKED` handoff/status; do not broaden scope.
