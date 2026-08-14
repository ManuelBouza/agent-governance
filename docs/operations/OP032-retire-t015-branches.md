# OP032 — Retire T015 branches

Operation ID: OP032
Status: READY_AFTER_BOTH_MERGES
Type: post-integration cleanup
Base branch: `develop`

## Objective

After the T015 acceptance and implementation PRs are both merged, retire only their merged source branches when Git proves their remote HEADs still match the exact merged heads and no later unique work exists.

## Durable targets

- acceptance branch: `docs/t015-acceptance`
- implementation branch: `test/consumer-governance-trigger-corpus`
- reviewed implementation head: `56b787677a5df029534a6ca6320606adfbec2812`

Resolve the exact acceptance PR/head and implementation PR/head from the merged GitHub PR records at execution time. The implementation PR head must equal the reviewed implementation head above. The acceptance branch is eligible only when its remote HEAD matches its merged PR head; do not rely on an earlier acceptance-branch SHA if later contract-only commits were included before merge.

OP032 is executable only after both PRs are merged. Each branch is eligible for retirement only when its remote HEAD still matches its corresponding merged PR head and Git proves no later unique work exists.

## Boundaries

Preserve `main`, `develop`, unrelated branches, repository content and uncommitted work. Do not author final `governance-skill/SKILL.md`, run release evals or mutate product/eval state. Any mismatch, ambiguity or later unique work must be retained and reported as PARTIAL/BLOCKED.

## Completion response

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP032
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```
