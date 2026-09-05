# OP068 — Retire D059 and OP068 Post-Integration Branches

Status: READY  
Operation-ID: OP068  
Type: post-integration branch/worktree closure  
Base branch: `develop`  
Controlling policy: `docs/BRANCH-CLEANUP.md`, `docs/OPERATION-CONTRACTS.md`, D058, D059  
Receipt anchor: GitHub issue `#289`  
Target integrated PR: `#288`  
Target branch: `docs/d059-operational-terminal-transport`  
Contract-authoring branch: `docs/op068-retire-d059-branch`  
Contract-authoring PR: `#290`

## Objective

Complete operational closure after D059 integration by retiring the merged PR #288 source branch and, after this contract is integrated, retiring the OP068 contract-authoring branch itself. Verify canonical remote absence, prune corresponding accessible local state safely, and leave the primary checkout on current clean `develop`.

This operation changes no tracked product content.

## Durable target identities

### PR #288

```text
PR: 288
base: develop
head branch: docs/d059-operational-terminal-transport
reviewed head: e12b669cf89e20bf8278d0f095603b9d0a68e50b
integrated commit: c7be7ad4cb52620a8f7dc2ad01f31ceec13d6e6c
```

The branch is eligible for deletion only if GitHub still reports PR #288 merged and the current remote branch head equals the reviewed head above.

### OP068 contract-authoring PR

```text
PR: 290
base: develop
head branch: docs/op068-retire-d059-branch
reviewed head: derive from the final merged GitHub PR #290 record at execution time
```

The executor MUST read merged PR #290 from GitHub after synchronizing the canonical remote, take its exact recorded `head_sha`, and require the current remote `docs/op068-retire-d059-branch` head to equal that value before deletion. This dynamic derivation avoids impossible self-referential SHA persistence while retaining exact merged-PR/head deletion authority.

Execution is forbidden unless PR #290 is merged into `develop`.

## Human-visible coordinator

Launch as:

```text
AG | agent-governance | OP068 | root-1
```

## Preconditions

Before mutation:

- synchronize canonical remote under D042/RB001;
- establish current safe local `develop == origin/develop` without discarding local work;
- verify GitHub receipt publication capability to issue #289;
- verify PR #288 and PR #290 are both merged into `develop`;
- verify each current remote target branch head exactly equals the applicable reviewed PR head;
- inspect accessible worktrees/local branches for either target branch;
- preserve any unrepresented/ambiguous local work.

If either target branch differs from its reviewed PR head, stop `BLOCKED_REVIEW`.

## Authorized effects

- delete remote `docs/d059-operational-terminal-transport` after exact PR #288/head verification;
- delete remote `docs/op068-retire-d059-branch` after exact PR #290/head verification;
- switch away from either branch in accessible local checkouts;
- remove safe local copies of those two topic branches after verifying no unique/unrepresented work;
- remove obsolete linked worktrees for those branches only when evidence-safe;
- fetch/prune remote-tracking refs;
- confirm primary checkout current clean `develop`;
- publish the detailed durable receipt to issue #289.

## Forbidden effects

Do not:

- modify tracked repository content;
- delete `main` or `develop`;
- delete any branch other than the two exact authorized targets;
- delete a target whose remote head differs from the reviewed PR head;
- discard uncommitted/unrepresented work or unique commits;
- force-push or rewrite history;
- delete unrelated retained/review worktrees or branches from OP067;
- launch or modify T057.

## Acceptance

`DONE` requires:

- PR #288 and PR #290 confirmed merged into `develop`;
- both target remote branches absent after deletion;
- any accessible local copies/worktrees safely retired or explicitly absent;
- primary checkout `develop == origin/develop` and tracked clean;
- durable receipt successfully published to issue #289.

If local ambiguous state prevents safe retirement, preserve it and use `BLOCKED_REVIEW`.

## Durable receipt

Post one final top-level comment to issue #289:

```text
OP068_STATUS: DONE | BLOCKED_REVIEW
CANONICAL_DEVELOP: <sha>
PR288_BRANCH_REMOTE: ABSENT | PRESENT
OP068_BRANCH_REMOTE: ABSENT | PRESENT
LOCAL_PR288_BRANCH: ABSENT | RETAIN/<reason>
LOCAL_OP068_BRANCH: ABSENT | RETAIN/<reason>
WORKTREES_REMOVED: <labels or none>
PRIMARY_CHECKOUT: <branch> / <head> / CLEAN|DIRTY
REVIEW_ITEMS: <items or none>
COORDINATOR_CHAT: AG | agent-governance | OP068 | root-1
```

## Interactive completion

Per D059 and `docs/OPERATION-CONTRACTS.md`, return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
RECEIPT: https://github.com/ManuelBouza/agent-governance/issues/289
COORDINATOR: AG | agent-governance | OP068 | root-1
```
