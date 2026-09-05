# D066 — ChatGPT Portable Git Workspace Transport

Status: ACCEPTED  
Date: 2026-09-05  
Authority: Human Owner / ChatGPT Orchestrator  
Research: R014, R015  
Scope: source-product ChatGPT Orchestrator workspace/transport adapter; no Governance Core or consumer-protocol change

## Decision

Agent Governance adopts a **portable local-Git workspace transport** for ChatGPT Orchestrator source-maintenance work when the active ChatGPT runtime exposes the required capabilities.

The adapter separates four planes:

```text
GitHub
  = canonical repository / branch / PR authority

local temporary workspace + Git
  = executable authoring and local commit/diff surface

ChatGPT Library
  = optional persistent snapshot storage across chat/runtime turnover

coordination-only GitHub lock branch
  = cross-chat writable ownership authority when portable concurrent/resumable mode is used
```

Library is not a Git remote, is not canonical repository authority, and is not the concurrency mutex. A local Git commit or Library version does not become accepted source state until represented and verified on the canonical GitHub branch/PR path.

The normal optimization target is:

```text
bootstrap/verify topic branch
-> perform many edits and local Git operations without per-edit GitHub mutation
-> persist local snapshots to Library when cross-chat durability is needed
-> publish a batched/final topic-branch state to GitHub with freshness protection
-> PR / review / integration / verification
```

This decision is intended to reduce GitHub write amplification and chat/tool-call overhead while preserving D061, branch protection, GitHub canonical authority, and fail-closed concurrency behavior.

## Applicability and fallback

The adapter is the preferred Orchestrator transport for non-trivial or multi-file Markdown/source-maintenance authoring when all capabilities required by the selected mode are available.

Before relying on it, the Orchestrator must establish the relevant runtime capabilities:

- executable temporary filesystem;
- local Git for local-authoring mode;
- Library materialize/upload/read operations for portable cross-chat persistence;
- connected GitHub reads/writes for canonical synchronization;
- exact branch/base identity needed by D061.

If a required capability is unavailable, use the existing protected topic-branch GitHub workflow. Do not emulate missing Library/Git/CAS semantics by weakening freshness, ownership, or branch-target checks.

## Relationship to D061

D061 remains controlling and is not weakened.

Before any normal Orchestrator-owned change becomes writable:

```text
refresh develop
-> create short-lived topic branch from exact intended develop SHA
-> verify exact branch/base
-> establish selected workspace mode
-> only then author/mutate the work unit
```

No local/Library optimization authorizes a direct write to `main`, `develop`, another long-lived branch, or an omitted/default branch target.

D066 refines the transport after the D061 identity gate: intermediate authoring may remain local and/or in Library instead of being represented as many remote GitHub content commits.

## Workspace modes

### Ephemeral local-Git mode

Use when one ChatGPT Orchestrator chat will complete the work without relying on cross-chat persistent writable state.

```text
one work unit
-> one verified topic branch
-> one temporary standalone Git workspace
-> local edits/commits/diffs
-> batched/final GitHub publication
```

Library and a cross-chat lock are not required merely to edit locally in one runtime.

### Portable cross-chat mode

Use when writable state must survive chat/runtime turnover or when multiple ChatGPT chats may hold concurrent writable work units for the same repository.

Each portable writable work unit maps to:

```text
one work unit
-> one unique topic branch
-> one coordination-only GitHub lock branch
-> expected lock-branch HEAD / optimistic CAS freshness
-> one `.chatgpt-worktree-lock.json` owner sentinel
-> one unique standalone Git repository snapshot in Library
-> one ownership/freshness receipt
```

A native linked `git worktree` directory is not a valid portable snapshot by itself because its `.git` may point to external `.git/worktrees/*` metadata. Portable mode persists a self-contained repository including the real `.git` directory.

D058 remains the Executor workspace-isolation authority. D066 applies the same isolation intent to ChatGPT Orchestrator portable workspaces; it does not replace native Executor worktree rules.

## Cross-chat lock authority

The reusable lock model is:

```text
coordination-only lock branch
+ expected-HEAD freshness/CAS
+ .chatgpt-worktree-lock.json sentinel
```

The sentinel must identify at least:

```text
schema
repository
owner
work_unit
topic_branch
target_branch
state
```

Normal active state is `ACTIVE`.

The lock branch must contain coordination state only. Ordinary product/Markdown work must never share the lock branch because an unrelated branch-head movement invalidates the acquisition CAS state.

### Acquisition

Conceptual sequence:

```text
1. read lock branch
2. record expected lock HEAD H
3. require sentinel absent
4. attempt sentinel creation against that observed branch state
5. success -> re-read sentinel and verify owner/work-unit -> ACQUIRED
6. stale expected HEAD / HTTP 409 -> BLOCKED_STALE_LOCK_HEAD
7. existing sentinel / create collision -> BLOCKED_OWNER_EXISTS
8. missing/corrupt/ambiguous ownership state -> BLOCKED_AMBIGUOUS_LOCK
```

A stale `409` is never an automatic retry signal. The caller must re-read and reclassify the lock. It must not silently retry until it wins.

## Portable snapshot contract

A portable workspace snapshot must be self-contained and include the repository `.git` state.

Before a snapshot is promoted or used for writable resume, validate at least:

```text
archive/checksum integrity
safe extraction
repository identity receipt
git fsck --full
clean pre-mutation status
local HEAD/tree
expected topic branch
remote topic branch freshness
exact Git-tree equivalence when commit identity is intentionally reconstructed
```

Connector-created remote commit SHA may differ from a locally equivalent commit. Exact Git tree equality is an accepted represented-content invariant when the receipt also records the canonical remote HEAD and no task requires exact Git-object identity.

A corrupt/invalid candidate never displaces the current validated snapshot.

## Portable resume gate

Before a later chat enters writable mode:

```text
materialize exact Library snapshot
-> checksum/archive validation
-> safe extract
-> git fsck --full
-> clean-status check
-> verify receipt repository/owner/work-unit/topic
-> verify lock sentinel repository/owner/work-unit/topic/state
-> verify remote topic branch HEAD freshness
-> verify expected Git tree when applicable
-> WRITE_ALLOWED
```

Any mismatch yields `WRITE_BLOCKED`. Do not reset, clean, overwrite, change owner, or delete state merely to force the gate to pass.

## Batched GitHub publication

Before publishing local work:

1. re-read the canonical remote topic branch;
2. require the remote HEAD to equal the expected remote base/freshness receipt;
3. derive the local changed-file set/tree from Git;
4. when the connected surface supports it, publish the represented multi-file state as one batched tree/commit update rather than one GitHub commit per local edit;
5. verify the resulting remote branch HEAD/tree and changed-file set;
6. persist/refresh the portable snapshot only after the represented state is verified.

Unexpected remote branch movement is fail-closed. Do not overwrite or silently reconcile a stale branch.

The normal target is one final/bounded synchronization commit per publication checkpoint, not one remote content write per authoring step. Corrective publications remain allowed when review or a legitimate later checkpoint requires them.

## Snapshot roots and GC

Long-lived canonical branches used by the repository are retained roots. For `agent-governance`, `main` and `develop` are roots.

Canonical rotation is fail-closed:

```text
create replacement candidate
-> materialize it back
-> checksum/archive validation
-> git fsck
-> verify expected HEAD/tree
-> promote current
-> re-materialize/revalidate promoted current
-> only then retire the superseded generation
```

Never delete the current canonical snapshot before its replacement is proven valid.

A feature/work-unit snapshot is GC-eligible only when all applicable evidence is positive:

```text
PR/work integration merged == true
+ exact integration represented/verified
+ target canonical snapshot refreshed
+ target candidate round-trip validated
+ target current promoted and revalidated
=> merged feature snapshot MAY be retired
```

Fail-closed retention:

```text
closed && !merged -> RETAIN
remote branch missing but integration unproven -> RETAIN
ambiguous GitHub/Library state -> RETAIN
snapshot validation failure -> RETAIN previous current
```

No automatic quota-pressure selector is adopted by D066.

## Release

Portable lock release requires exact current ownership:

```text
fetch sentinel
-> verify repository/owner/work-unit/topic/state
-> obtain exact current sentinel blob SHA
-> delete sentinel using that SHA
-> verify sentinel is absent
```

A delete failure or ownership mismatch leaves the lock occupied/ambiguous. It does not become free by assumption.

Post-merge Library GC and lock release are separate from remote branch/ref retirement. Existing branch-cleanup authority controls branch retirement.

## Library namespace

For the current source-maintenance adapter, the preferred logical layout is equivalent to:

```text
/git-workspaces/<owner>/<repo>/
  canonical/
    main/current.tar.gz
    develop/current.tar.gz
  worktrees/
    <work-unit>/current.tar.gz
```

The exact Library file identifier/version is runtime metadata, not identity authority. Two writable work units must never share one writable snapshot namespace.

Automatic canonicalization of arbitrary unusual Git ref names remains outside D066; use an explicit collision-free work-unit identifier rather than inventing unsafe path/ref encodings.

## Open gaps preserved

D066 does **not** claim or authorize automatic solutions for:

- crash/orphan recovery after lock acquisition;
- TTL or heartbeat semantics;
- automatic abandoned-lock reclamation;
- cross-chat resume of closed-unmerged work;
- explicit ownership transfer;
- lock/topic branch-ref retirement when tooling/authority differs;
- automatic Library GC selection under real quota pressure;
- unusual ref-name canonicalization at scale;
- unqualified ruleset/branch-protection interactions outside the current verified repository envelope.

When any of these is material, stop or require explicit new authority/qualification instead of inferring behavior.

## Security and privacy boundary

- snapshots must not introduce credentials/secrets that were not already valid repository state;
- temporary extraction must reject unsafe archive traversal/link behavior;
- no snapshot/receipt is canonical authority over GitHub;
- destructive Library cleanup requires positive classification; uncertainty means retain;
- normal server-side long-lived branch protection remains mandatory under D062;
- D061 remains the hard Orchestrator branch-target rule.

## Research disposition

D066 adopts the technically qualified subset of R014 and R015. The canonical registry transitions both items to:

```text
Research-State: COMPLETE
Decision-State: DECIDED
Decision-Ref: docs/decisions/D066-chatgpt-portable-git-workspace-transport.md
```

The original research artifacts and appendices remain unchanged as historical evidence. Their unresolved gaps remain unresolved.

## Implementation

The source-product deterministic helper and tests are specified by:

`docs/tasks/T058-chatgpt-portable-workspace-adapter.md`

The operating procedure is:

`docs/CHATGPT-PORTABLE-GIT-WORKSPACE.md`

D066 becomes usable as policy after this planning change is integrated; executable helper claims require T058 implementation and Orchestrator acceptance.