# ChatGPT Portable Git Workspace Runbook

Status: ACTIVE AFTER D066 INTEGRATION  
Authority: D066, D061, D058, D062  
Research evidence: R014, R015

## Purpose

Operate ChatGPT Orchestrator source-maintenance work with local Git as the authoring surface, ChatGPT Library as optional cross-chat persistence, and GitHub as the canonical repository/PR authority.

The runbook is designed to reduce GitHub write amplification without weakening branch-target, freshness, ownership, or cleanup safety.

## Select a mode

### Mode A — ephemeral local Git

Use when the work will remain in one ChatGPT runtime and no cross-chat writable continuation is required.

Required:

- exact current `develop`;
- verified unique topic branch;
- executable local filesystem;
- Git;
- connected GitHub publication path.

Do not create a Library snapshot or cross-chat lock merely for ceremony.

### Mode B — portable Library workspace

Use when the work must survive chat/runtime turnover or when multiple writable ChatGPT work units may coexist for one repository.

Required in addition to Mode A:

- Library materialize/upload/read capability;
- unique Library namespace;
- coordination-only lock branch;
- sentinel acquisition with expected lock-branch HEAD freshness/CAS;
- ownership/freshness receipt.

If a required capability is unavailable, do not partially emulate Mode B. Fall back to Mode A only when same-runtime completion is safe; otherwise block.

## Phase 1 — D061 bootstrap

1. Read canonical `develop` from GitHub.
2. Create the exact short-lived topic branch from that SHA.
3. Re-read the branch and verify it equals the intended base.
4. Record repository, base branch/SHA, topic branch and work unit.
5. Only after this gate may the work unit become writable.

Never use `main`, `develop`, the default branch, or an omitted branch as a normal mutation target.

## Phase 2A — materialize local authoring workspace

Construct or restore a standalone Git repository representing the topic branch.

Minimum checks before editing:

```text
git rev-parse --is-inside-work-tree
git fsck --full
git status --porcelain
git rev-parse HEAD
git rev-parse HEAD^{tree}
```

Expected status before new mutation is clean unless a previously validated same-work-unit snapshot intentionally carries represented local work.

Use local Git for iterative edits, diffs, staging and local commits. These local commits are working history; GitHub remains canonical.

## Phase 2B — acquire portable cross-chat ownership

For Mode B only.

Use a coordination-only lock branch associated with the logical portable workspace. Do not put product/Markdown changes on that branch.

Acquisition:

1. Read the lock branch and record exact HEAD `H`.
2. Fetch `.chatgpt-worktree-lock.json`.
3. Require sentinel absent.
4. Attempt sentinel creation from the observed state.
5. On success, re-read sentinel and verify repository/owner/work-unit/topic/state.
6. Enter owned state only after the verification succeeds.

Classify failures exactly:

```text
expected H != actual lock HEAD / HTTP 409
  -> BLOCKED_STALE_LOCK_HEAD

sentinel exists / create collision
  -> BLOCKED_OWNER_EXISTS

sentinel missing/corrupt/inconsistent after ambiguous mutation
  -> BLOCKED_AMBIGUOUS_LOCK
```

Never automatically retry a stale `409` until acquisition succeeds. Re-read and reclassify first.

Recommended sentinel shape:

```json
{
  "schema": "chatgpt-portable-workspace/v1",
  "repository": "owner/repo",
  "owner": "<chat/workspace owner>",
  "work_unit": "<Txxx/OPxxx/or explicit work unit>",
  "topic_branch": "<topic branch>",
  "target_branch": "develop",
  "state": "ACTIVE"
}
```

## Phase 3 — persist a Library snapshot

For Mode B, package a **standalone repository including `.git`**. A linked `git worktree` directory with a `.git` pointer to another repository is not portable.

Preferred logical namespace:

```text
/git-workspaces/<owner>/<repo>/worktrees/<work-unit>/current.tar.gz
```

Long-lived snapshots use:

```text
/git-workspaces/<owner>/<repo>/canonical/main/current.tar.gz
/git-workspaces/<owner>/<repo>/canonical/develop/current.tar.gz
```

A portable receipt must bind at least:

```text
schema
repository
owner
work_unit
topic_branch
target_branch
remote_head_sha
remote_tree_sha
local_snapshot_head_sha
local_snapshot_tree_sha
lock_branch when Mode B uses one
working_tree_clean
```

After upload, materialize the object back from Library and validate the actual persisted bytes. An upload response alone is not snapshot qualification.

Validation order:

```text
checksum
-> safe archive extraction
-> receipt identity
-> git fsck --full
-> clean status
-> HEAD/tree
-> remote topic freshness/tree equivalence where applicable
```

A candidate is not `current` until its round trip passes.

## Phase 4 — resume in another chat

Before any write:

1. Locate the exact work-unit Library snapshot.
2. Materialize it into the temporary workspace.
3. Verify checksum and safely extract it.
4. Run `git fsck --full`.
5. Require clean/expected local status.
6. Read receipt and require repository/owner/work-unit/topic equality.
7. Read the coordination lock branch and sentinel.
8. Require sentinel owner/work-unit/topic/state equality.
9. Re-read the GitHub topic branch.
10. Require the remote HEAD to match the receipt's expected freshness state.
11. Compare exact Git tree when the local/remote commit IDs intentionally differ.
12. Only then set `WRITE_ALLOWED`.

Any mismatch sets `WRITE_BLOCKED`.

Do not repair a mismatch with destructive reset/clean, owner replacement, force update, or silent remote overwrite.

## Phase 5 — publish to GitHub

Before publication:

1. Re-read the topic branch.
2. Require remote HEAD equals the expected remote base/freshness receipt.
3. Derive the complete local change set/tree.
4. Prefer one batched tree/commit publication through the connected GitHub surface for the represented checkpoint.
5. Verify resulting remote HEAD/tree and changed paths.
6. Update the local/Library receipt only after remote verification.

If the topic branch moved unexpectedly, classify stale and stop. Do not silently merge/rebase/overwrite inside the adapter.

The optimization target is:

```text
many local edits
-> one bounded/final remote publication
```

not:

```text
one GitHub commit per local file edit
```

## Phase 6 — integration and canonical snapshot refresh

After PR integration:

1. Require positive `merged == true`.
2. Verify the exact work is represented in the target.
3. Read the current target branch.
4. Build a fresh target snapshot candidate.
5. Upload it.
6. Materialize it back.
7. Verify checksum/archive/`git fsck`/clean/tree.
8. Promote target `current`.
9. Materialize promoted `current` again.
10. Revalidate it.
11. Only then classify the merged feature/worktree snapshot as GC-eligible.

For `main`/`develop`, keep the prior validated generation until the replacement has passed the second verification.

## Phase 7 — feature snapshot GC

Delete/move to Library Trash only when:

```text
merged == true
AND integration verified
AND target current refreshed
AND target candidate validated
AND promoted target current revalidated
```

Retain on:

```text
closed && !merged
missing remote branch without positive integration evidence
ambiguous PR/Library state
validation failure
unknown owner
```

The automatic quota-pressure selector is not qualified and must not be invented.

## Phase 8 — release portable lock

For Mode B:

1. Fetch the exact current sentinel.
2. Verify repository/owner/work-unit/topic/state.
3. Obtain the exact current sentinel blob SHA.
4. Delete the sentinel using that SHA.
5. Re-fetch and require `404 / absent`.

If release fails, the namespace remains occupied/ambiguous.

Lock-branch deletion is not required for ordinary release and remains governed separately by branch-cleanup capability/authority.

## Fail-closed status vocabulary

Implementations/helpers should use stable meanings equivalent to:

```text
ACQUIRE_ALLOWED
ACQUIRED
BLOCKED_STALE_LOCK_HEAD
BLOCKED_OWNER_EXISTS
BLOCKED_AMBIGUOUS_LOCK
BLOCKED_IDENTITY_MISMATCH
BLOCKED_STALE_OR_WRONG_SNAPSHOT
BLOCKED_INVALID_SNAPSHOT
BLOCKED_STALE_BASE
WRITE_ALLOWED
WRITE_BLOCKED
RELEASE_ALLOWED
RELEASED
GC_ELIGIBLE
RETAIN_ACTIVE
RETAIN_CLOSED_UNMERGED
RETAIN_AMBIGUOUS
RETAIN_INVALID_TARGET_SNAPSHOT
```

Exact CLI enum names may be implemented by T058, but they must remain unambiguous and fail closed.

## Open-gap stop conditions

Do not improvise automatic behavior for:

- crash/orphan owner recovery;
- TTL/heartbeat;
- abandoned lock reclamation;
- closed-unmerged cross-chat resume;
- ownership transfer;
- automatic branch-ref retirement;
- quota-driven GC selection;
- unusual ref-name canonicalization;
- unqualified ruleset interaction.

These require explicit later authority/qualification if they become necessary.

## Audit minimum

A portable-workspace operation should be reconstructable from compact receipts containing:

```text
repository/work unit
mode
topic branch / target branch
expected and observed remote HEAD/tree
owner
lock branch/head/sentinel blob when applicable
snapshot checksum
local snapshot HEAD/tree
git fsck result
clean status
publication result
integration/GC classification
release result
```

Do not persist private chain-of-thought or raw chat transcripts as workspace authority.