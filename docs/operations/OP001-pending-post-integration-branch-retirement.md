# OP001 — Pending post-integration branch retirement

Operation ID: OP001  
Status: DRAFT  
Type: post-integration branch cleanup  
Base branch: `develop`

## Objective

Retire the currently pending integrated topic branches remotely and in the executor-controlled local checkout, leaving no eligible merged topic branch from the durable targets below while preserving `main`, `develop`, unresolved unique work, and inaccessible checkouts.

This operation creates no repository content and does not reopen T007, D039, T008, T006, or any merged Markdown scope.

## Durable targets

The executor MUST derive branch identity and reviewed head evidence from the following merged integration records:

- PR #53 — T007 acceptance (`docs/t007-acceptance`);
- PR #54 — accepted T007 handoff (`chore/branch-hygiene-cleanup`);
- PR #55 — T007 post-integration checkpoint (`docs/t007-post-integration`);
- PR #56 — canonical post-integration cleanup prompt (`docs/post-integration-cleanup-prompt`);
- PR #57 — cleanup target generalization (`docs/post-integration-cleanup-target`);
- PR #58 — merged-branch freeze policy (`docs/merged-branch-freeze`);
- PR #59 — D039 research (`docs/governance-learning-loop-research`);
- PR #60 — D039 acceptance/T008 contract (`docs/d039-acceptance-t008-contract`).

The PR that integrates this OP001 contract MUST be added to this list before OP001 becomes `READY` or is merged. Its source branch is intentionally eligible for retirement by this same operation after merge, preventing recursive cleanup-contract creation.

## Special resolved-review evidence for PR #55

`docs/t007-post-integration` advanced after PR #55 merged, which is a recorded workflow nonconformance. Those later Markdown commits were recovered through fresh branch/PR #56 and are represented in current `develop`.

Therefore, for this operation only, the executor MAY retire `docs/t007-post-integration` after independently verifying all of the following from Git/GitHub:

1. PR #55 is merged;
2. the current branch head differs from PR #55 reviewed head because of the recorded post-merge advancement;
3. the post-merge changes are fully represented by merged PR #56/current `develop`;
4. no additional unique work exists beyond that recovered content.

If any of those facts cannot be established, classify the branch `REVIEW` and return `PARTIAL`/`BLOCKED`; do not delete by assumption.

## Controlling references

- `AGENTS.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`
- current merged PR/Git history for the durable targets above

## Authorized operations

The Agente de IA Ejecutor may:

- fetch/prune and inspect canonical remote refs, PR metadata, local branches, worktrees, and clean/dirty state;
- verify each durable target's merged state, reviewed head, current remote branch head, and represented-work evidence;
- retire remote branches proven safe under `docs/BRANCH-CLEANUP.md` and this contract;
- remove corresponding safe local branches and stale remote-tracking refs in accessible executor-controlled checkouts;
- use local force deletion only where policy evidence proves no unique work would be discarded;
- report inaccessible local checkouts as unverified.

## Explicit exclusions

The executor MUST NOT:

- modify, create, commit, or push repository content;
- delete `main` or `develop`;
- delete any branch not derived from the durable targets in this contract;
- infer deletion safety from branch naming or ancestry alone;
- discard uncommitted work or unique commits;
- alter tags, releases, branch protection/rulesets, repository settings, or history;
- start T008/T006 or any implementation work;
- use chat-provided branch names, SHAs, or deletion decisions as authority.

## Safety invariants

For normal unchanged merged branches:

```text
merged PR + reviewed head_sha == current remote branch HEAD + no unique later work
=> eligible for retirement
```

For PR #55, use the explicit resolved-review rule above rather than pretending the reviewed head still matches.

Any unexpected branch head drift, unrepresented work, dirty local state, worktree ambiguity, missing PR evidence, or permission/tool failure becomes `REVIEW`/stop for the affected branch.

## Verification requirements

Before returning, the executor must re-fetch and report:

- final remote branch inventory;
- final local branch inventory for each accessible controlled checkout;
- any retained/review branch with exact reason;
- confirmation that `main` and `develop` remain;
- confirmation that no repository content commit/push was created;
- inaccessible local checkouts explicitly unverified.

Expected successful remote end state for the targets in this contract is that none of their eligible topic branches remain. The contract does not authorize deletion of unrelated active branches.

## Stop / escalation

Return `PARTIAL` or `BLOCKED` rather than guessing if any target cannot be mapped to authoritative merged-PR evidence, current branch state conflicts with the contract, unique work may exist, a checkout cannot be safely cleaned, or required deletion permissions are unavailable.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP001
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```
