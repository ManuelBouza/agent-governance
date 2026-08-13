# OP018 — Retire D040/T011 completion branches

Operation ID: OP018  
Status: DRAFT  
Type: bounded post-integration / superseded-branch cleanup  
Base branch: `develop`

## Objective

Retire the completed D040 Phase-B / T011 topic branches after Protocol `1.13.0` activation, while preserving `main`, `develop`, Git/PR audit history, repository content and any branch that cannot be proven safe.

This operation also retires the Markdown branch that integrates L001 recovery and the OpenCode worktree preflight once that PR is merged and recorded below.

## Durable cleanup set

The executor derives exact branch names, reviewed heads and merge/closure state from canonical GitHub records. Chat-provided branch names or SHAs are not deletion authority.

### Merged cleanup targets

- PR #83 — T011-R1 acceptance;
- PR #84 — T011 executable implementation;
- PR #86 — D040 Phase-B v2 verification-control planning (`OP017`);
- PR #87 — D040 Phase-B v2 activation;
- the PR integrating this OP018 + L001 recovery + OpenCode worktree preflight, recorded here before OP018 becomes `READY`.

For each merged PR target, ordinary merged-branch freeze rules apply:

```text
merged PR + reviewed head == current remote branch HEAD + no unique later work
=> eligible for retirement
```

### Superseded historical candidate

PR #81 is closed without merge and is explicitly superseded by merged PR #87 after OP012 blocked the original candidate and T011 readiness was integrated.

Its source branch may be retired only if canonical GitHub evidence shows:

- PR #81 remains closed/unmerged;
- current source-branch HEAD still equals the exact closed PR #81 head;
- no commits were appended after that reviewed candidate;
- all intended activation semantics are represented by merged PR #87;
- no unique later work would be discarded.

If any condition is uncertain, retain it as `REVIEW` and return `PARTIAL` rather than deleting.

### Abandoned temporary refresh branch

A temporary branch named `docs/d040-candidate-refresh-operation` was created during the failed attempt to refresh the old Phase-B candidate, but no repository change was intentionally persisted from that branch.

It may be retired only if the executor proves from Git that it contains no unique commits/work relative to an authoritative retained ref. If any unique commit exists or provenance is ambiguous, retain it as `REVIEW` and return `PARTIAL`.

## Controlling references

- `AGENTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`
- `docs/decisions/D040-atomic-protocol-migration-and-single-version-authority.md`
- `docs/reviews/T011-R1.md`
- `docs/learning/L001-protocol-version-baseline-drift.md`
- canonical Git/GitHub records for PRs #81, #83, #84, #86, #87 and the integration PR recorded below

## Integration PR for this contract

Status: `DRAFT` until populated.

- PR: `<record after opening>`
- Purpose: integrate L001 recovery, OpenCode worktree preflight and OP018
- Source branch/head: derive from that merged PR and canonical GitHub state at execution time

OP018 becomes `READY` only after this section names the actual PR and that PR is merged.

## Authorized operations

The executor may synchronize canonical refs; establish a safe current local `develop` baseline under D042; inspect PR/branch/worktree metadata; classify only the bounded cleanup set above; delete remote branches proven eligible; prune corresponding local/tracking refs and disposable worktrees in accessible controlled checkouts; and report inaccessible checkouts as unverified.

## Explicit exclusions

The executor MUST NOT:

- modify/create/commit/push repository content;
- delete `main` or `develop`;
- delete any branch outside the bounded cleanup set;
- delete a `REVIEW`/ambiguous branch;
- discard uncommitted or unique work;
- change tags/releases/settings/rulesets/history;
- change D040/D036/T011/L001 semantics;
- initialize CodeGraph or alter `.gitignore`;
- change OpenCode host configuration;
- use chat-provided branch names/SHAs as deletion authority.

## OpenCode preflight

If the selected executor host is OpenCode and this operation may create/use repository worktrees outside the OpenCode session working directory, the Human/Orchestrator pre-launch step must apply `docs/OPENCODE-WORKTREE-PREFLIGHT.md` before delegation.

This contract does not itself authorize or modify host configuration.

## Verification requirements

Before returning, re-fetch and report the final remote/local branch inventories and verify:

- `main` and `develop` remain;
- every deleted merged branch matched its merged PR reviewed head and had no later unique work;
- PR #81 branch was deleted only if the supersession conditions above were proven;
- the abandoned temporary refresh branch was deleted only if it had no unique commits;
- every retained branch has a concrete `REVIEW`/retention reason;
- no repository content commit/push was created;
- inaccessible local checkouts are explicitly unverified.

## Stop / escalation

Return `PARTIAL` or `BLOCKED` instead of guessing when canonical freshness, branch identity, supersession, uniqueness or local-work safety cannot be established.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP018
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```
