# OP023 — Retire Consumer Skill v1 planning branch

Operation ID: OP023
Status: DRAFT
Type: post-integration cleanup
Base branch: `develop`

## Objective

After the planning PR containing the Consumer Governance Skill v1 release gate and T013 is merged, retire only its merged source branch when Git proves no later unique work exists.

## Durable target

- planning PR: `<record after opening>`
- source branch: `docs/consumer-governance-skill-v1-release-gate`

OP023 becomes READY only after the PR identity is recorded and merged.

## Boundaries

Preserve `main`, `develop`, unrelated branches, repository content and uncommitted work. Do not execute T013, author `governance-skill/SKILL.md`, or mutate product state.

## Completion response

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP023
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```
