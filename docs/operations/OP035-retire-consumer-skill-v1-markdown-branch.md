# OP035 — Retire Consumer Skill v1 Markdown branch

Operation ID: OP035
Status: READY_AFTER_MERGE
Base branch: `develop`

## Objective

Retire the merged ChatGPT-owned branch `docs/consumer-governance-skill-v1` after its exact final head has been integrated into `develop`.

## Preconditions

Before deletion, prove from canonical remote state that:

- the source branch is `docs/consumer-governance-skill-v1`;
- its integration PR is merged to `develop`;
- the merged PR head SHA equals the current remote branch HEAD;
- that exact source head is an ancestor of current `origin/develop`;
- no later unique work exists on the source branch.

If any identity, ancestry, merge-state, or freshness check fails, stop and report BLOCKED rather than deleting.

## Actions

Delete only the exact remote/local `docs/consumer-governance-skill-v1` branch once all preconditions are proven.

Preserve `develop`, `main`, unrelated branches, dirty/uncommitted work, tags, repository content and history. Do not rebase, force-push, rewrite content or merge additional work.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP035
REMOTE_REMAINING: <comma-separated-branches>
LOCAL_REMAINING: <comma-separated-branches>
```
