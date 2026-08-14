# OP037 — Retire Consumer Governance v1 release-approval branch

Operation ID: OP037
Status: READY_AFTER_MERGE
Type: branch-cleanup
Base branch: `develop`

## Objective

After the Consumer Governance Skill v1 release-approval Markdown PR is merged, retire its merged topic branch and leave the repository branch set clean.

## Authorized operation

Delete only the merged branch:

- `docs/consumer-governance-v1-release-approval`

Do not delete, rewrite, force-update, merge, rebase, or otherwise mutate `develop` or `main`.

Before deletion, synchronize the canonical remote and confirm the branch is merged into current `origin/develop`. If merge ancestry cannot be established safely, stop and report `BLOCKED`.

After deletion, prune stale local/remote-tracking refs as needed and verify the remaining local and remote branches are exactly:

- `develop`
- `main`

Preserve unrelated local/uncommitted work. Do not modify repository files.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP037
REMOTE_REMAINING: <comma-separated branch names>
LOCAL_REMAINING: <comma-separated branch names>
```
