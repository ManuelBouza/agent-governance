# OP067 — Normalize Local Worktrees and Primary Checkout

Status: READY  
Operation-ID: OP067  
Type: source-maintenance local Git/worktree hygiene  
Base branch: `develop`  
Controlling decision: `docs/decisions/D058-executor-coordinator-session-and-worktree-hygiene.md`  
Operating procedure: `docs/EXECUTOR-SESSION-WORKTREE-HYGIENE.md`  
Existing cleanup policy: `docs/BRANCH-CLEANUP.md` and `docs/BRANCHING.md`  
Receipt anchor: GitHub issue `#286`  
Next gated task: `docs/tasks/T057-codex-read-only-child-requalification-v2.md`

## Objective

Before T057 launches, audit and normalize the accessible native-Windows local checkout topology for `ManuelBouza/agent-governance` so that:

1. no stale/obsolete worktree or topic branch remains unexplained;
2. only evidence-safe stale worktrees/branches are retired;
3. ambiguous or unique local work is preserved and reported rather than discarded;
4. the designated primary checkout finishes clean on current `develop`, with local `develop == origin/develop`;
5. the environment is safe for a new exclusive T057 worktree.

This is a repository operation, not product implementation. It must not modify tracked product files.

## Human-visible coordinator

Launch as a new Codex coordinator named exactly:

```text
AG | agent-governance | OP067 | root-1
```

The name is navigation metadata only. Git and this Operational Contract remain authority.

## Preconditions

Before mutation:

- synchronize/fetch the canonical GitHub remote under D042/RB001;
- load current repository instructions from the refreshed `develop` containing D058 and OP067;
- identify the primary checkout and all registered linked worktrees;
- verify there is no concurrently executing writable Agent Governance task that would be affected by cleanup;
- preserve all unrepresented local work.

If another writable coordinator is active in this repository and its worktree/branch could be touched, stop `BLOCKED_ACTIVE_WORK` rather than racing it.

## Authorized effects

OP067 may perform only local/remote Git hygiene that is proven safe by the existing branch-cleanup policy and this contract:

- fetch/prune canonical remote refs;
- inventory registered worktrees and local/remote branches;
- classify non-primary worktrees and non-long-lived branches as `ACTIVE`, `RETAIN`, `REVIEW`, or `DELETE`;
- remove linked worktrees classified `DELETE` after verifying no unrepresented work;
- retire local topic branches classified `DELETE` after no worktree uses them;
- retire remote topic branches classified `DELETE` only when PR/base/head evidence satisfies `docs/BRANCH-CLEANUP.md`;
- prune stale worktree administrative metadata after live worktree inspection;
- switch/converge the primary checkout safely to `develop` and current `origin/develop`;
- comment the durable result on GitHub issue #286.

Exact Git/GitHub command mechanics are Executor-owned under D054.

## Forbidden effects

Do not:

- modify tracked product files or committed Markdown;
- create implementation commits merely to perform cleanup;
- force-push or rewrite remote history;
- delete `main` or `develop` locally or remotely;
- delete a branch because it merely looks old;
- remove a worktree with uncommitted/unrepresented changes;
- delete a local branch with unique commits not proven represented elsewhere;
- use reset/clean/checkout-force to discard unknown state;
- delete a branch currently checked out by a retained/active worktree;
- remove an active coordinator's worktree;
- infer squash-merge safety from ancestry when PR/head identity is required;
- close or alter T057 itself.

## Required inventory

Build a complete accessible inventory before deletion:

### Primary checkout

Record:

```text
path/label
current branch
HEAD
tracked status
origin/develop
origin/main
```

Absolute path may be redacted to a stable local label in the public receipt.

### Registered worktrees

For each worktree record:

```text
label/path-class
HEAD
branch or detached state
tracked/untracked status relevant to deletion safety
classification: ACTIVE | RETAIN | REVIEW | DELETE
owner/work-unit or reason
```

### Branches

For each non-long-lived local branch and relevant remote topic branch record enough evidence to determine:

```text
branch
checked-out worktree, if any
local head
remote head, if any
PR/integration evidence when deletion is proposed
classification
reason
```

The operation does not need to narrate every historical remote ref if it is clearly outside the accessible cleanup scope, but every branch/worktree that could collide with the primary checkout or T057 must be classified.

## Safe-retirement rules

A worktree/branch may be `DELETE` only when all applicable conditions hold:

- its represented work is integrated/retired or otherwise explicitly obsolete under canonical evidence;
- no uncommitted/unrepresented working-tree change would be lost;
- no unique local commit would be lost without a durable represented copy;
- no active coordinator owns it;
- remote topic deletion, when performed, satisfies exact PR/base/head rules including squash-merge semantics;
- local branch deletion occurs only after no worktree uses it.

Anything that fails deterministic proof becomes `REVIEW` or `RETAIN`, not `DELETE`.

## Primary checkout terminal invariant

For `DONE`, the designated primary checkout must finish as:

```text
branch        = develop
HEAD          = current origin/develop
tracked state = clean
```

It must also be safe to create a fresh T057 linked worktree/topic branch from current `develop`.

If the primary checkout contains unique/unrepresented work that prevents safe convergence, preserve it and return `BLOCKED_REVIEW`.

## Remaining-topology terminal invariant

For `DONE`:

- no remaining registered worktree is unexplained;
- each non-primary worktree is `ACTIVE` or `RETAIN` with an explicit work-unit/reason;
- no `REVIEW` item remains that could collide with T057 or prevent primary-checkout convergence;
- no local topic branch eligible for deterministic safe retirement remains merely because its worktree was forgotten;
- stale administrative worktree entries are pruned;
- T057's expected topic branch/worktree is not pre-created by OP067 unless a supported operation mechanic requires a harmless reservation; normal preference is to let T057 create its own exclusive workspace after launch.

## Durable receipt

Post one concise but sufficient comment to GitHub issue #286 containing:

```text
OP067_STATUS: DONE | BLOCKED_ACTIVE_WORK | BLOCKED_REVIEW
CANONICAL_DEVELOP: <sha>
PRIMARY_CHECKOUT: <branch> / <head> / CLEAN|DIRTY
WORKTREES_REMOVED: <labels or none>
LOCAL_BRANCHES_REMOVED: <branches or none>
REMOTE_BRANCHES_REMOVED: <branches or none>
REMAINING_WORKTREES: <label=classification/reason>
REVIEW_ITEMS: <items or none>
T057_WORKSPACE_READY: true | false
COORDINATOR_CHAT: AG | agent-governance | OP067 | root-1
```

Do not post sensitive absolute workstation paths when labels suffice.

The issue comment is the authoritative operation receipt. Chat output is transport only.

## Acceptance / routing

### `DONE`

Use only when all terminal invariants pass and `T057_WORKSPACE_READY=true`.

### `BLOCKED_ACTIVE_WORK`

Use when a concurrent writable coordinator owns state that OP067 would need to touch.

### `BLOCKED_REVIEW`

Use when unrepresented/ambiguous local state prevents evidence-safe cleanup or primary-checkout convergence.

After either blocked result, do not launch T057 until the Orchestrator/Human resolves the named blocker through persisted authority.

## Terminal output

Return only:

```text
STATUS: DONE | BLOCKED
RECEIPT: https://github.com/ManuelBouza/agent-governance/issues/286
COORDINATOR: AG | agent-governance | OP067 | root-1
```
