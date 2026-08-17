# OP066 — Abandon interrupted T032 local work

Operation ID: OP066  
Status: READY  
Type: interrupted local-work retirement  
Authorized base: `develop`  
Receipt anchor: PR #TBD

## Objective

Cancel the interrupted OP062 Stage-B T032 execution and destroy only the local/unpublished T032 work produced by that interrupted executor invocation, while preserving all canonical remote state.

This operation does **not** resume T032. Its sole purpose is to make the executor workspace safe for a later clean T032 re-entry.

Human Owner authorization on 2026-08-17 explicitly permits destruction of the interrupted local-only T032 work because the executor stopped for token/context exhaustion and no corrective T032 push was published.

## Canonical state to preserve

Before any destructive local action, verify from the canonical remote that:

- `develop` is current and contains OP066;
- `fix/t032-rcab-snapshot-live-separation` still equals `b43b306e56c6b90969c3dd10e23ccf8e00cc8ba5`;
- `refactor/t021-consumer-profile-abstraction` still equals `969e2130ca9abb27c6ae5ad830923582f45b8a2f`;
- there is no later remote T032 commit, corrective push, or implementation PR that would make the local interrupted state potentially authoritative;
- the OP062 Stage-A durable receipt on PR #139 remains `STATUS: DONE` with `EXCEPTIONS: none`.

If any of those conditions is false, stop and report `BLOCKED`. Do not destroy local work based on stale assumptions.

## Exact local scope authorized for destruction

The destructive authorization is limited to the local workspace/state used by the interrupted OP062 Stage-B continuation of:

`fix/t032-rcab-snapshot-live-separation`

The executor may discard:

- uncommitted tracked changes created by that interrupted T032 continuation;
- untracked files proven to have been created only by that interrupted T032 continuation;
- local-only T032 commits that are not reachable from any canonical remote ref and were created after the preserved remote T032 head above;
- the local T032 worktree and/or local T032 branch, if removing and later recreating them is the safest way to guarantee no interrupted local state survives.

After cleanup, either of these local results is acceptable:

1. no local T032 branch/worktree exists; or
2. a clean local T032 branch/worktree exists and exactly matches `origin/fix/t032-rcab-snapshot-live-separation@b43b306e56c6b90969c3dd10e23ccf8e00cc8ba5`.

This is an explicit Human-authorized exception to the normal preserve-local-work rule **only for the identified interrupted local T032 state**.

## Prohibited destruction

Do not discard or rewrite:

- any remote branch or commit;
- `develop` or `main`;
- T021 local/remote work;
- D050/D051/D052 documentation branches or their local state;
- unrelated local changes, stashes, worktrees, branches, untracked files, or commits;
- any local commit that is reachable from a canonical remote ref;
- any work whose provenance cannot be determined confidently as belonging only to the interrupted T032 continuation.

If unrelated or ambiguous local work is mixed into the same workspace such that selective destruction is unsafe, stop and report `BLOCKED` rather than guessing.

## Remote mutation prohibition

OP066 authorizes **no push, force-push, branch deletion, PR mutation, implementation commit, or product-content mutation**.

The remote T032 branch must remain exactly at `b43b306e56c6b90969c3dd10e23ccf8e00cc8ba5` throughout this operation.

## Verification

Before claiming `DONE`, verify and record:

- exact current `develop` SHA used for bootstrap;
- remote T032 head before and after cleanup;
- remote T021 head before and after cleanup;
- whether the interrupted local T032 state contained uncommitted changes, untracked files, and/or local-only commits;
- which categories of local T032 state were discarded;
- final local T032 state: `ABSENT` or `CLEAN_AT_REMOTE_HEAD`;
- no remote mutation occurred;
- no unrelated local state was destroyed;
- exceptions are `none`.

## Durable receipt

Publish one top-level comment to the receipt-anchor PR with:

```text
AGENT-GOVERNANCE-OPERATION-RECEIPT v1
CONTRACT: docs/operations/OP066-abandon-interrupted-t032-local-work.md
BASE_SHA: <current canonical develop used for the operation>

STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP066
DESCRIPTION: Abandon interrupted local-only T032 work
REMOTE_T032_BEFORE: <sha>
REMOTE_T032_AFTER: <sha>
REMOTE_T021: <sha>
LOCAL_T032_BEFORE: <concise observed state>
DISCARDED: <uncommitted | untracked | local-only-commits | worktree/local-branch | none, comma-separated>
LOCAL_T032_AFTER: ABSENT | CLEAN_AT_REMOTE_HEAD | <blocked state>
REMOTE_MUTATION: none | <unexpected mutation>
EXCEPTIONS: <none or concise exceptions>
```

A `DONE` claim is valid only when the durable receipt exists and every verification condition above passes.

## No continuation

OP066 has **no D045 continuation**.

After OP066 is `DONE`, stop. Do not restart T032, T021, T022, or any cleanup operation in the same invocation.

A later T032 re-entry must be separately launched from then-current `origin/develop`, reload current `AGENTS.md` because the repository instructions changed after the interrupted invocation, load T032 + T032-R1, and treat the preserved remote T032 head—not any discarded local state—as the implementation starting point.

## Stop / escalation

Return `BLOCKED` before destruction if:

- remote T032 differs from the preserved rejected head;
- a later T032 push/PR exists;
- local provenance is ambiguous;
- unrelated local work cannot be separated safely;
- current `develop` lacks this integrated OP066 contract;
- receipt publication capability is unavailable.

If destruction succeeds but final receipt publication fails, return `PARTIAL` and perform no further mutation.
