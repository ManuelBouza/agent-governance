# OP024 — Open planning review

Operation ID: OP024
Status: READY
Bootstrap branch: `docs/consumer-governance-skill-v1-release-gate`
Target branch: `develop`

Objective: create the GitHub review request for the existing planning branch against `develop` without changing repository content.

Preconditions: synchronize the canonical remote; establish a safe current baseline for the bootstrap branch; confirm it is ahead of and not behind `origin/develop`; confirm the diff is Markdown-only. Otherwise return BLOCKED.

Authorized metadata action: create exactly one pull request from `docs/consumer-governance-skill-v1-release-gate` to `develop` titled `docs: define Consumer Governance Skill v1 release gate`. If an equivalent open PR already exists, report it instead.

Do not edit, commit, push, rebase, merge, force-push, delete refs, modify `develop`/`main`, or create another PR.

Verify the PR is open with the exact head/base pair and report its number and head SHA.

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP024
PR: <number | NONE>
HEAD: <exact-head-sha | UNKNOWN>
REPO_MUTATION: NONE | <description>
```
