# OP056 — Retire ICAE/RCAB gate branch and start T030

Operation ID: OP056  
Status: READY  
Type: D045 preauthorized cleanup-to-task transition  
Authorized base: `develop`  
Receipt anchor: PR #129

## Objective

After PR #129 is merged into `develop`, retire exactly its Markdown source branch and, only if Stage A completes with exact deterministic postconditions, continue in the same executor invocation to the already-integrated T030 measure-only Task Contract.

## Stage A — branch retirement

Target PR: #129  
Target source branch: derive from merged PR #129; expected `docs/icae-rcab-adoption`.

### Authorized operations

- Read merged PR #129 and current remote/local refs.
- Verify the surviving PR source branch, if present, still equals the exact reviewed/merged PR head with no unique later work.
- Delete exactly that source branch remotely when eligible.
- Safely remove matching accessible-local branch/tracking refs when no unrepresented work exists.
- Re-read remote/local inventories.
- Publish the final Stage-A durable receipt to PR #129.

### Stage-A exclusions

- Any repository-content edit or commit.
- Mutation/deletion of `develop`, `main`, or unrelated branches.
- Force/reset or branch movement to manufacture equality.
- Deletion if the source branch advanced after PR review/merge.
- Inference that inaccessible local checkouts are clean.

### Stage-A preconditions

- This contract is reachable from current `origin/develop`.
- PR #129 is merged into `develop`.
- Durable receipt publication capability to PR #129 is established before first mutation.
- Any surviving target branch equals PR #129's authoritative merged head immediately before deletion.
- `develop` and `main` identities are never moved by cleanup.
- Local/uncommitted work is preserved.

### Stage-A PASS requirements

- PR #129 source branch is absent remotely after cleanup;
- remote branch inventory is exactly `develop`, `main`;
- `develop` and `main` identities are unchanged by cleanup;
- accessible local inventory is reported;
- `EXCEPTIONS: none`;
- no repository content was modified;
- final durable receipt publication succeeded.

### Stage-A durable receipt

Publish to PR #129:

```text
AGENT-GOVERNANCE-OPERATION-RECEIPT v1
CONTRACT: docs/operations/OP056-retire-icae-rcab-gate-and-start-t030.md
BASE_SHA: <develop-sha-before-cleanup>

STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP056
DESCRIPTION: Retire ICAE/RCAB gate branch and start T030
RETIRED: <retired/already-absent target or none>
REMOTE_REMAINING: <remote branches>
LOCAL_REMAINING: <accessible local branches>
EXCEPTIONS: <none or concise exceptions>
```

If Stage A is `BLOCKED`, `PARTIAL`, ambiguous, fails receipt publication, or any PASS requirement is false, STOP. T030 is not authorized to start from this operation.

## D045 preauthorized continuation

If and only if Stage A is durable `DONE` with `EXCEPTIONS: none` and every Stage-A PASS requirement holds, continuation to Stage B is preauthorized under D045 without Human acknowledgement.

Before Stage B:

1. synchronize the canonical remote again;
2. establish a safe current local `develop` equal to `origin/develop` containing PR #129 and this OP056;
3. preserve all local/uncommitted work;
4. if that baseline cannot be established safely, stop before T030 and report the Stage-A DONE receipt plus a Stage-B BLOCKED result.

## Stage B — T030

Authoritative Task Contract:

`docs/tasks/T030-repository-context-baseline-and-measure-linter.md`

Stage B is governed exclusively by that integrated Task Contract and its controlling repository policies. Do not infer, supplement, or broaden T030 from this Operational Contract.

In particular, OP056 does not authorize document splitting, budget enforcement, new dependencies, network/model services, Consumer runtime/package changes, or Markdown edits.

The executor creates/uses the T030 Task Contract branch and returns the T030 canonical completion response defined by `docs/TASK-CONTRACTS.md` after verification, handoff, commit and push.

## Combined completion behavior

When Stage A succeeds and Stage B runs, the visible final response is the T030 completion response:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T030-executor-handoff.json
BRANCH: <T030 topic branch>
HEAD: <pushed-commit-sha>
```

The Stage-A result remains independently auditable from the required PR #129 durable receipt. Human copy/paste of that receipt is not required for Orchestrator review.
