# Branch Cleanup Procedure

Status: ACTIVE

## Purpose

Define the repeatable post-integration procedure for retiring short-lived source-product branches without discarding unrepresented work.

`docs/BRANCHING.md` is the normative branch policy. This document is the operational procedure used after merge and for periodic backlog cleanup.

## Core invariant

```text
merged work != completed branch lifecycle
completed branch lifecycle = integration + frozen branch + remote retirement + local pruning
branch deletion requires evidence that no unique work is being discarded
```

Normal topic branches are disposable integration surfaces. `main` and `develop` are long-lived repository state and are excluded from this procedure.

## Responsibility split

- **ChatGPT Orchestrator / merge operator** — verifies PR/base/head identity, classifies the remote branch, delegates cleanup with the canonical prompt when an executor performs it, and verifies the canonical remote no longer exposes the retired topic branch.
- **Agente de IA Ejecutor / local checkout owner** — when delegated cleanup, performs authorized remote retirement plus cleanup of every checkout/worktree actually accessible in its execution environment; it MUST report inaccessible checkouts as unverified.
- **Human/local checkout owner** — for a checkout not accessible to the delegated executor, verifies there is no unrepresented local work, deletes the local branch, and prunes stale remote-tracking refs before beginning the next repository task there.
- **Human Owner** — resolves ambiguous retention/deletion cases when unique work or intent cannot be reconstructed safely from Git.

Remote cleanup is centrally auditable. Local branch cleanup is checkout-specific and cannot be inferred from GitHub alone.

## Merged-branch freeze precondition

Before any cleanup classification, apply the merged-branch freeze invariant from `docs/BRANCHING.md`.

Once a PR is merged, its source branch is expected to remain exactly at the reviewed PR `head_sha`. No new work may be appended to it.

If the current branch HEAD differs from the merged PR `head_sha`, do not treat that as ordinary stale-branch cleanup. Classify the branch `REVIEW` and determine what the post-merge commits represent.

Resolution must make the new work explicit:

- if the post-merge commits are valid new work, reproduce/persist them on a new topic branch from the current authorized base and integrate them normally;
- if they are intentionally abandoned, record that disposition before deletion;
- if their intent or uniqueness is uncertain, retain the branch until Human/Orchestrator review resolves it.

Never move the branch backward merely to manufacture a matching PR head and make deletion easier. The divergent state is evidence and must remain auditable until resolved.

## Canonical post-integration cleanup delegation

When branch retirement is delegated to an Agente de IA Ejecutor after an authorized source change is integrated, ChatGPT MUST use the canonical prompt defined in `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`.

The prompt identifies exactly one durable cleanup target: `TASK <task-id>` for Task-Contract-governed work or `PR <number>` for an integrated change without a Task ID.

Do not replace that prompt with an ad hoc branch list or chat-only deletion instructions. The executor derives cleanup candidates from the cleanup target, current Git/GitHub state, merged PR records, and this procedure.

This closure phase is not a new implementation task and does not create another implementation handoff commit. It is operational retirement of already-integrated branches.

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
- different -> `REVIEW`; this is also a merged-branch-freeze violation unless separately explained by an authorized specialized lifecycle;
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
- the branch received commits after merge, violating the frozen-branch invariant;
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

For normal future topic work, integration and operational branch closure are distinct states.

The integrated change is not operationally closed until:

- the accepted/authorized content is integrated into the authorized target;
- the merged source branch has remained frozen at the reviewed PR head until retirement;
- the canonical post-integration cleanup prompt has been executed when cleanup is delegated;
- every eligible merged branch associated with the cleanup target is absent remotely;
- any `REVIEW`/`RETAIN` exception has an explicit durable reason;
- the merge operator has verified final remote state;
- local cleanup has been performed in controlled/accessed checkouts, or is an explicit mandatory precondition before the next repository task in an inaccessible checkout.

Do not preserve stale topic branches merely as history. PRs, commits, Task Contracts, reviews, handoffs, and Git history are the durable audit surfaces.

## Operational lesson — post-merge branch reuse

The T007 closure exposed a concrete failure mode: a documentation branch was merged, then received new documentation commits before retirement. That made its remote HEAD diverge from the reviewed PR head and converted an otherwise deterministic deletion into a `REVIEW` case that required recovery through a fresh branch/PR.

The preventive rule is now explicit:

```text
merge -> freeze -> cleanup
new work -> new branch from current develop
```

Do not use a merged branch as a convenient continuation surface, even for closely related follow-up work.
