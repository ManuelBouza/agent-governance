# T007 — Branch hygiene cleanup

Task ID: T007  
Status: IN_PROGRESS  
Type: infrastructure  
Base branch: `develop`  
Expected topic branch: `chore/branch-hygiene-cleanup`  
Expected executor handoff: `handoffs/T007-executor-handoff.json`

## Objective

Restore branch hygiene across the canonical `agent-governance` repository by safely retiring stale integrated topic branches both remotely and in the executor-controlled local checkout, while preserving every branch that contains active or unresolved unique work.

T007 is a repository-maintenance interruption. It does not change product semantics and does not supersede T006, which remains `READY` and resumes immediately after T007 closes.

## Controlling references

- `AGENTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/TASK-CONTRACTS.md`
- `docs/EXECUTOR-HANDOFFS.md`
- GitHub issue #50 (`chore: audit and clean historical topic branches`)
- Active rework directive: `docs/reviews/T007-R1.md`

## Authorized scope

The Agente de IA Ejecutor is authorized to perform repository/checkout branch-maintenance operations necessary to complete the cleanup, including:

- fetch and inspect the complete canonical remote branch/PR state;
- inspect local branches, remote-tracking refs, worktrees and clean/dirty checkout state;
- associate historical topic branches with merged/closed/open PRs and relevant Task Contracts/reviews/handoffs;
- classify each non-long-lived branch as `DELETE`, `REVIEW`, or `RETAIN` under `docs/BRANCH-CLEANUP.md`;
- delete remote topic branches classified `DELETE` only after exact merged-PR/head verification;
- switch away from stale local topic branches, delete verified stale local branches and prune remote-tracking refs;
- use force local branch deletion only where squash-merge evidence establishes safety as defined by `docs/BRANCH-CLEANUP.md`;
- record a machine-readable T007 handoff containing the complete final branch disposition and verification evidence;
- commit and push only the T007 handoff if repository content changes are required by the handoff policy.

The executor MAY use ordinary Git/GitHub CLI/API capabilities available in its host environment to perform these operational actions.

## Explicit exclusions

The executor MUST NOT:

- delete `main` or `develop`;
- delete a branch classified `REVIEW` or `RETAIN` unless a persisted Orchestrator/Human review directive explicitly resolves its disposition;
- delete an active Task Contract branch or an open-PR branch;
- infer deletion safety from branch naming or `git branch --merged` alone;
- discard uncommitted local work, unique local commits, or a branch still required by another worktree;
- alter product code, tests, fixtures, dependencies, configuration, Governance Core, decisions, Task Contracts, reviews, or other committed Markdown;
- rewrite Git history, force-push long-lived branches, delete tags, or alter repository release state;
- start T006 implementation as part of this task.

## Invariants / constraints

```text
merged work != completed branch lifecycle
completed branch lifecycle = integration + remote retirement + local pruning
branch deletion requires evidence that no unique work is being discarded
squash merge ancestry != deletion authority
```

For each normal merged-PR remote deletion candidate, the executor must establish:

1. the associated PR is actually merged into the authorized target;
2. the reviewed PR `head_sha` is known;
3. the current remote branch HEAD equals that reviewed `head_sha`;
4. no evidence of post-review unique work exists.

Any mismatch or ambiguity becomes `REVIEW` and remains undeleted until a persisted Orchestrator/Human disposition resolves it.

The executor owns only the checkout(s) actually accessible in its execution environment. It MUST NOT claim local cleanup for inaccessible Human/other-agent checkouts. Those must be reported explicitly as outstanding owner-side cleanup.

## Required execution sequence

1. Verify current `develop` contains this exact T007 contract and any active review directive.
2. Create/use `chore/branch-hygiene-cleanup` from a `develop` revision containing the controlling contract; rework continues on the same task branch.
3. Verify local checkout cleanliness/worktree state before destructive branch operations.
4. Fetch/prune and capture complete remote and local branch inventories.
5. Exclude `main` and `develop` from deletion classification.
6. Classify every remaining remote branch exactly once as `DELETE | REVIEW | RETAIN` with evidence.
7. Delete remote `DELETE` branches in bounded batches of at most 10, re-reading remote state after every batch.
8. Resolve no `REVIEW` branch by assumption; only a persisted Orchestrator/Human disposition may authorize its deletion.
9. Clean the executor-controlled local checkout: switch to `develop`, fetch/prune, remove safely retired local topic branches, inspect worktrees, and verify no stale remote-tracking refs remain for deleted remote branches.
10. Re-fetch final remote/local inventories and persist the T007 handoff.
11. Commit/push the handoff on `chore/branch-hygiene-cleanup` and return only the canonical minimal executor response.

## Acceptance criteria

ChatGPT accepts T007 only when remote evidence shows:

- every historical non-long-lived remote branch has an explicit final disposition;
- every branch authorized for deletion is absent from the canonical remote;
- every unresolved `REVIEW` branch remains present unless separately resolved with auditable evidence;
- every `RETAIN` branch has a concrete current reason;
- `main` and `develop` are unchanged by deletion operations;
- the executor-controlled local checkout is on an appropriate retained branch, clean, pruned, and contains no safely retired local topic branch that should have been removed;
- any inaccessible local checkout is explicitly identified as not verified rather than falsely reported clean;
- T006/Product/Core/test semantics are unchanged.

## Verification requirements

The handoff must include, at minimum:

- initial and final remote branch counts/names;
- initial and final local branch counts/names for the executor-controlled checkout;
- per-branch disposition with associated PR where available, reviewed PR head SHA, observed current remote HEAD, and reason;
- deleted remote branch list and post-deletion absence verification;
- deleted local branch list and final `git branch -vv`/equivalent summary;
- `git worktree list`/equivalent verification;
- clean `git status` evidence after cleanup;
- unresolved `REVIEW` branches with exact reason;
- retained branches with exact reason;
- statement identifying any local checkout not accessible/verified;
- any procedural nonconformance discovered during execution, including recovery evidence.

Normal product pytest/Ruff gates are not required because T007 changes no product implementation. The verification authority for T007 is deterministic Git/GitHub state evidence plus Orchestrator review.

## Stop / escalation conditions

Stop deletion of the affected branch and classify it `REVIEW` if:

- current remote HEAD differs from the merged PR head or a persisted resolved-review SHA;
- no reliable associated merged PR can be established and no persisted review disposition resolves it;
- local uncommitted or unique work could be lost;
- another worktree still owns the branch and safe disposition is unclear;
- repository permissions/tooling prevent verified deletion;
- deletion would require history rewriting or weakening branch protection;
- any evidence conflicts about whether work is already represented or intentionally abandoned.

A single `REVIEW` item does not require abandoning safe cleanup of independently verified `DELETE` branches.

## Expected handoff

Persist `handoffs/T007-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push it on `chore/branch-hygiene-cleanup`, then return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T007-executor-handoff.json
BRANCH: chore/branch-hygiene-cleanup
HEAD: <pushed-commit-sha>
```

## Review history

- `T007-R1` reviews executor HEAD `656c71e22f60ae8b235304179dc1d8fee4ec4031`, preserves the classify-before-delete procedural nonconformance, and resolves `eval/d032-agent-capability` as intentionally abandoned T004 work eligible for exact-SHA deletion.