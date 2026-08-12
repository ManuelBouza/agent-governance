# Branch Cleanup Procedure

Status: ACTIVE

## Purpose

Define the repeatable post-integration procedure for retiring short-lived source-product branches without discarding unrepresented work.

`docs/BRANCHING.md` is the normative branch policy. This document is the operational procedure used after merge and for periodic backlog cleanup.

## Core invariant

```text
merged work != completed branch lifecycle

completed branch lifecycle = integration + remote retirement + local pruning

branch deletion requires evidence that no unique work is being discarded
```

Normal topic branches are disposable integration surfaces. `main` and `develop` are long-lived repository state and are excluded from this procedure.

## Responsibility split

- **ChatGPT Orchestrator / merge operator** — verifies PR/base/head identity, classifies the remote branch, performs or requests remote deletion, and verifies the canonical remote no longer exposes the retired topic branch.
- **Local checkout owner** — Human Owner or Agente de IA Ejecutor that controls a workstation/worktree containing the branch; verifies there is no unrepresented local work, deletes the local branch, and prunes stale remote-tracking refs.
- **Human Owner** — resolves ambiguous retention/deletion cases when unique work or intent cannot be reconstructed safely from Git.

Remote cleanup is centrally auditable. Local branch cleanup is checkout-specific and cannot be inferred from GitHub alone.

## Normal post-merge procedure

### 1. Capture the integration identity

For the merged PR record the following facts before deleting anything:

- PR number;
- authorized base/target branch;
- source/head branch name;
- reviewed PR `head_sha`;
- merged state and merge timestamp;
- resulting integration commit where available.

The PR MUST be merged, not merely closed.

### 2. Re-read the current remote branch

If the source branch already no longer exists, remote cleanup passes and the procedure continues with local pruning.

If it still exists, compare its current remote HEAD with the reviewed PR `head_sha`.

- equal -> eligible for remote deletion;
- different -> `REVIEW`; do not delete automatically;
- unavailable/ambiguous -> `REVIEW`; do not delete automatically.

This exact-head check prevents deletion of work pushed after the reviewed PR state.

### 3. Do not use ancestry alone for squash merges

Normal topic PRs prefer squash merge. The topic commits may therefore not be ancestors of the resulting `develop` commit.

Commands such as `git branch --merged develop` are useful diagnostics but MUST NOT be the sole deletion authority for squash-merged branches.

The authoritative evidence is the merged PR plus the exact reviewed head identity and confirmation that the remote branch has not advanced afterward.

### 4. Delete and verify the remote branch

Delete the source branch only after the checks above pass.

Then re-read the canonical remote and verify that the branch is absent.

If repository hosting supports automatic deletion of merged PR head branches, enable/use that control as defense in depth. The workflow still verifies branch absence rather than assuming the setting executed successfully.

### 5. Clean every local checkout that carried the branch

The checkout owner MUST first switch away from the retiring branch and verify that the worktree is coherent.

Typical local sequence:

```bash
git status
git switch develop
git fetch --prune origin
git branch -vv
git worktree list
```

Before local deletion, verify that there are no uncommitted changes, no separate worktree still using the branch, and no commits representing work that was not captured by the merged PR or another retained ref.

After that verification, remove the local topic branch. Because squash merge may make a safe branch appear "unmerged" to Git ancestry checks, a force-delete may be mechanically necessary:

```bash
git branch -D <topic-branch>
git fetch --prune origin
```

`-D` is permitted only after the PR/head evidence above has established that deletion is safe. It MUST NOT be used as a shortcut around inspection.

If a checkout is not available at merge time, its owner MUST perform this local cleanup before beginning the next repository task in that checkout.

## Classification for existing/stale branches

A backlog audit classifies every non-long-lived branch into exactly one state.

### `DELETE`

Use only when all of the following hold:

1. an associated PR is merged into the authorized target;
2. the reviewed PR head identity is known;
3. the current remote branch HEAD equals that reviewed head, or the branch is already absent;
4. no evidence indicates unique post-review work that must be preserved.

### `REVIEW`

Use when any of the following is true:

- the associated PR was closed without merge;
- no associated PR can be established;
- current branch HEAD differs from the merged PR head;
- the branch carries commits whose disposition is unclear;
- the branch may correspond to cancelled, abandoned, superseded, or manually interrupted work;
- the branch state cannot be reconstructed safely from Git metadata.

`REVIEW` branches are never bulk-deleted. Resolve their unique commits/intended disposition first.

### `RETAIN`

Use only for a branch that is intentionally active and has an explicit current reason to exist, such as:

- an open authorized PR;
- an active Task Contract implementation branch;
- an active release/hotfix branch whose propagation is incomplete;
- an explicit Human/Orchestrator retention decision.

Retention is temporary. Once the reason ends, reclassify the branch.

## Periodic cleanup audit

When branch accumulation is detected:

1. fetch the complete remote branch inventory;
2. exclude `main` and `develop`;
3. associate each remaining branch with its PR/task/release history;
4. classify it `DELETE | REVIEW | RETAIN`;
5. delete only the `DELETE` set;
6. verify remote absence after each deletion batch;
7. resolve `REVIEW` items individually before deleting them;
8. instruct/perform local `fetch --prune` and local branch retirement in every known checkout;
9. finish with a fresh remote inventory and record any intentionally retained branches plus their reason.

Large historical cleanups SHOULD be performed in bounded batches so an incorrect classification cannot remove many branches before detection.

## Integration closure gate

For normal future topic work, the integration is not operationally closed until:

- the PR is merged into the authorized target;
- the remote topic branch is absent or has been explicitly placed in `REVIEW` because its HEAD changed;
- the merge operator has verified remote state;
- local cleanup has been performed in controlled checkouts, or is an explicit mandatory precondition before their next repository task.

Do not preserve stale topic branches merely as history. PRs, commits, Task Contracts, reviews, handoffs, and Git history are the durable audit surfaces.
