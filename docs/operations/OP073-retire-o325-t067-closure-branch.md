# OP073 — Retire O325 T067 Closure Branch

Status: READY  
Operation-ID: OP073  
Type: task-attached post-integration branch retirement  
Parent-Work-Unit: T067  
Coordinator-Continuity: ATTACHED_CLOSURE  
Parent Task: `docs/tasks/T067-r029-d082-materialization-and-qualification.md`  
Coordinator-ID: `AG | agent-governance | T067 | root-1`  
Base branch: `develop`  
Controlling policy: D058, D059, D060, D064, `docs/OPERATION-CONTRACTS.md`, `docs/BRANCHING.md`, `docs/BRANCH-CLEANUP.md`  
Contract-authoring branch: `docs/o325-t067-closed`  
Contract-authoring PR: `#428`  
Durable receipt anchor: GitHub PR `#428`

## Objective

Complete the final operational closure of T067 by retiring only the branch that persists O325 and this OP073 after that branch is merged into `develop`, then publish the durable receipt. This operation creates no implementation scope, does not reopen T067/D082 acceptance, and must not touch T066 or any unrelated branch/worktree.

## Durable target

```text
head branch: docs/o325-t067-closed
PR: #428
base: develop
```

At execution time derive the exact reviewed `head_sha` and integration commit from merged PR #428. Remote retirement is allowed only when PR #428 is merged into `develop` and the present remote branch head equals the reviewed head, or the branch is already absent.

## Preconditions

- synchronize canonical GitHub state and establish a safe current `develop == origin/develop` baseline without discarding local/uncommitted work;
- load this integrated contract from current `develop`;
- verify GitHub PR #428 accepts a top-level comment before mutation;
- verify PR #428 is merged into `develop`;
- require exact current remote branch head == PR #428 reviewed head before deletion;
- preserve any dirty, unique, ambiguous, or unrepresented local state.

## Authorized operations

The Executor may fetch/prune refs, inspect exact PR/ref state, delete the single authorized remote branch after the exact-head gate passes, remove an evidence-safe accessible local copy/worktree of that branch, restore the accessible primary checkout to clean current `develop`, and publish exactly one final OP073 receipt.

## Forbidden operations

Do not modify tracked repository content; reopen T067; start/modify T066; delete any branch/worktree other than `docs/o325-t067-closed`; delete `main` or `develop`; force-push/rewrite history; reset/clean away local changes; create another implementation handoff or commit.

## Verification requirements

`DONE` requires PR #428 merged into `develop`; remote `docs/o325-t067-closed` absent; every accessible local copy/worktree safely absent; primary checkout on clean current `develop`; no tracked-content mutation; no unrelated target mutation; final receipt published; coordinator identity unchanged.

If an inaccessible local target cannot be verified, return `PARTIAL`. If branch identity/head or unique work is ambiguous, return `BLOCKED` and preserve it.

## Durable receipt

Publish one final top-level comment to PR #428 using exactly:

```text
OP073_STATUS: DONE | BLOCKED | PARTIAL
PARENT_WORK_UNIT: T067
COORDINATOR_CONTINUITY: ATTACHED_CLOSURE
CANONICAL_DEVELOP: <sha>
O325_BRANCH_REMOTE: ABSENT | PRESENT/<reason>
LOCAL_O325_BRANCH: ABSENT | RETAIN/<reason> | INACCESSIBLE/<reason>
O325_WORKTREE: ABSENT | RETAIN/<reason> | INACCESSIBLE/<reason>
PRIMARY_CHECKOUT: <branch> / <head> / CLEAN|DIRTY|INACCESSIBLE
TRACKED_CONTENT_MUTATION: none | <unexpected>
UNRELATED_TARGETS_MUTATED: none | <unexpected>
REVIEW_ITEMS: none | <items>
COORDINATOR_ID: AG | agent-governance | T067 | root-1
HOST_DISPLAY_TITLE: <observed-title-or-unavailable>
```

## Interactive completion

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
RECEIPT: https://github.com/ManuelBouza/agent-governance/pull/428
COORDINATOR: AG | agent-governance | T067 | root-1
```

## Root retirement

ChatGPT Orchestrator must read the durable receipt directly from GitHub and independently verify the remote branch is absent. Only then may `AG | agent-governance | T067 | root-1` be retired and T067 considered fully operationally closed.
