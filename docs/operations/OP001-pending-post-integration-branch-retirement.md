# OP001 — Pending post-integration branch retirement

Operation ID: OP001  
Status: READY  
Type: post-integration branch cleanup  
Base branch: `develop`

## Objective

Retire the currently pending integrated topic branches remotely and in the executor-controlled local checkout, leaving no eligible merged topic branch from the durable targets below while preserving `main`, `develop`, unresolved unique work, and inaccessible checkouts.

This operation creates no repository content and does not reopen T007, D039, T008, T006, or any merged Markdown scope.

## Durable targets

The executor MUST derive branch identity and reviewed head evidence from these integration records:

- PR #53 — T007 acceptance (`docs/t007-acceptance`);
- PR #54 — accepted T007 handoff (`chore/branch-hygiene-cleanup`);
- PR #55 — T007 post-integration checkpoint (`docs/t007-post-integration`);
- PR #56 — canonical post-integration cleanup prompt (`docs/post-integration-cleanup-prompt`);
- PR #57 — cleanup target generalization (`docs/post-integration-cleanup-target`);
- PR #58 — merged-branch freeze policy (`docs/merged-branch-freeze`);
- PR #59 — D039 research (`docs/governance-learning-loop-research`);
- PR #60 — D039 acceptance/T008 contract (`docs/d039-acceptance-t008-contract`);
- PR #61 — persisted Operational Contract policy and this OP001 contract (`docs/persisted-operational-contracts`).

PR #61 is intentionally included before merge so its source branch can be retired by this same operation after integration without creating a recursive cleanup contract.

## Special resolved-review evidence for PR #55

`docs/t007-post-integration` advanced after PR #55 merged, which is a recorded workflow nonconformance. Those later Markdown commits were recovered through fresh branch/PR #56 and are represented in current `develop`.

For this operation only, the executor MAY retire `docs/t007-post-integration` after independently verifying:

1. PR #55 is merged;
2. the current branch head differs from PR #55 reviewed head because of the recorded post-merge advancement;
3. the post-merge changes are fully represented by merged PR #56/current `develop`;
4. no additional unique work exists beyond that recovered content.

If any fact cannot be established, classify that branch `REVIEW` and return `PARTIAL`/`BLOCKED`; do not delete by assumption.

## Controlling references

- `AGENTS.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`
- current merged PR/Git history for the durable targets above

## Authorized operations

The Agente de IA Ejecutor may fetch/prune and inspect canonical remote refs, PR metadata, local branches, worktrees and clean/dirty state; verify every target's merged/reviewed/current identity; retire remote branches proven safe; remove corresponding safe local branches and stale tracking refs in accessible controlled checkouts; and report inaccessible checkouts as unverified.

## Explicit exclusions

The executor MUST NOT modify/create/commit/push repository content; delete `main`/`develop`; delete branches not derived from these durable targets; infer safety from naming/ancestry alone; discard uncommitted or unique work; alter tags/releases/settings/rulesets/history; start T008/T006; or use chat-provided branches/SHAs/deletion decisions as authority.

## Safety invariants

For normal unchanged merged branches:

```text
merged PR + reviewed head_sha == current remote branch HEAD + no unique later work
=> eligible for retirement
```

For PR #55 use the explicit resolved-review rule above. Unexpected head drift, unrepresented work, dirty local state, worktree ambiguity, missing PR evidence, or permission/tool failure becomes `REVIEW`/stop for the affected branch.

## Verification requirements

Before returning, re-fetch and report final remote branch inventory; final local branch inventory for every accessible controlled checkout; retained/review branches with exact reason; confirmation `main`/`develop` remain; confirmation no repository content commit/push was created; and inaccessible local checkouts explicitly unverified.

## Stop / escalation

Return `PARTIAL` or `BLOCKED` rather than guessing if any target cannot be mapped to authoritative evidence, current state conflicts with this contract, unique work may exist, a checkout cannot be safely cleaned, or deletion permissions are unavailable.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP001
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```
