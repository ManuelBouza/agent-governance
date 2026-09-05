# ChatGPT Library worktree simulator research

Research-ID: R015  
Research-State: COMPLETE  
Decision-State: NOT_REQUIRED  
Opened: 2026-09-05  
Last-Reviewed: 2026-09-05  
Owner: ChatGPT Orchestrator  
Scope: concurrent writable ChatGPT work-unit isolation for one GitHub repository when separate chats do not share a persistent local filesystem or native `git worktree` topology  
Question: Can ChatGPT emulate the safety properties of exclusive Git worktrees across separate chat/workspace runtimes by combining GitHub branch/ref ownership with portable Library Git snapshots, while preventing two chats from writing through the same logical worktree?  
Evaluation-Refs: R014; D058; empirical qualification against `ManuelBouza/test_biblioteca` on 2026-09-05; remote commits `c1208d6bb5f9e6cc28df7fcc4463d6144750cda9` and `1904904cde94c87bee17ab2e26d757d880f3fb07`; dedicated lock refs `lock/worktree-sim-chat-a-20260905` and `lock/worktree-sim-chat-b-20260905`; Library paths under `/git-workspaces/ManuelBouza/test_biblioteca/worktree-simulator/`  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Summary

R014 established that ChatGPT Library can persist packaged complete Git repositories across chats, and that GitHub remains canonical remote authority. D058 independently requires concurrent writable work units to have exclusive workspaces and forbids two writable coordinators from sharing the same worktree or topic branch.

R015 qualifies a non-normative **worktree simulator** for runtimes where separate ChatGPT chats cannot share one persistent native Git worktree topology.

The qualified model is:

```text
GitHub canonical repository
  |
  +-- target branch
  +-- topic branch A --------------------------+
  +-- topic branch B ----------------------+   |
  +-- lock ref A -> owner/work-unit A      |   |
  +-- lock ref B -> owner/work-unit B      |   |
                                               |
ChatGPT Library                                |
  |                                            |
  +-- worktree-simulator/chat-a/current.tar.gz |
  +-- worktree-simulator/chat-b/current.tar.gz |
                                               |
Temporary chat workspace                       |
  |                                            |
  +-- materialize A -> standalone .git repo <--+
  +-- materialize B -> standalone .git repo <---
```

The simulator reproduces the safety semantics needed by D058:

```text
one writable work unit
  -> one topic branch
  -> one exclusive lock ref
  -> one portable Library snapshot namespace
  -> one ownership receipt
```

It does **not** reproduce the disk-sharing optimization of native `git worktree`. Each persisted simulated worktree is intentionally self-contained.

Core qualification result:

`PASS`

Qualified behaviors:

- two logical chats can start from the same repository base and mutate the same file independently on different topic branches;
- neither mutation changes the other branch or the target branch;
- a deterministic GitHub lock ref can act as an atomic exclusivity primitive;
- a second claim for the same lock ref is rejected by GitHub with HTTP `422 Reference already exists`;
- a linked native Git worktree directory alone is not portable because its `.git` entry points back to the primary repository's worktree metadata;
- each logical chat can instead persist a standalone repository snapshot with a real `.git` directory;
- round-tripped Library snapshots preserve exact branch tree state, pass `git fsck --full`, and restore clean;
- ownership receipts can reject a chat attempting to use another chat's worktree snapshot before mutation;
- local snapshot commit SHA may differ from the GitHub commit SHA while exact Git tree equality proves represented file state.

The mechanism remains non-normative. True simultaneous cross-chat acquisition timing, stale-lock retirement, lease expiry/heartbeat, and crash recovery between lock creation and owner annotation remain future qualification items.

## Relationship to R014

R014 proved the persistence and transport substrate:

- complete `.git` repositories can be packaged and stored in Library;
- Library snapshots survive chat boundaries;
- restored repositories can continue local Git history;
- exact Git tree equality can validate content-equivalent local/remote repository state even when commit SHA identity differs;
- merged-branch snapshot lifecycle/GC can retire redundant Library snapshots fail-closed.

R015 uses those capabilities specifically for concurrent-work isolation.

R015 does not supersede R014.

## Relationship to D058

D058 already establishes the normative source-maintenance invariant:

```text
one writable work unit -> one topic branch -> one exclusive worktree
```

and:

```text
Two writable coordinators MUST NOT share the same worktree or topic branch.
```

R015 does not change that decision. It qualifies one possible adapter mechanism for environments where separate chats cannot literally share a native persistent `git worktree` object database.

Therefore:

```text
D058 = semantic isolation requirement
R015 = non-normative adapter feasibility evidence
```

No source-maintenance policy adoption is created by this research.

## Native `git worktree` portability finding

### Local setup

A local Git repository was initialized in the temporary workspace with one base commit and two real linked worktrees:

```text
base worktree
chat-a worktree -> branch sim-chat-a
chat-b worktree -> branch sim-chat-b
```

Each linked worktree modified `app.py` independently and committed successfully.

Observed local state:

```text
base content:   print("Library final change")
chat-a content: print("Local worktree A")
chat-b content: print("Local worktree B")
```

The worktrees were correctly isolated locally.

### Linked `.git` is not self-contained

The linked worktrees contained `.git` files equivalent to:

```text
chat-a/.git:
  gitdir: /mnt/data/worktree_sim_local/base/.git/worktrees/chat-a

chat-b/.git:
  gitdir: /mnt/data/worktree_sim_local/base/.git/worktrees/chat-b
```

Therefore a tar archive containing only one linked worktree directory would contain a pointer to Git metadata outside that archive.

That archive is not a portable cross-chat repository snapshot.

Supported conclusion:

```text
native linked worktree directory != portable Library snapshot
```

A cross-chat worktree simulator must therefore persist either:

- a standalone full Git repository per logical worktree; or
- another self-contained Git object/package representation plus enough checkout metadata to reconstruct the worktree.

R015 qualified the first approach.

## Qualification repository and isolation topology

Repository:

`ManuelBouza/test_biblioteca`

Canonical `main` remained unchanged throughout the R015 experiment:

```text
main: af02345fcfed0ebe7d4b6503af7e89cdf48b84cf
app.py: print("Library final change")
blob: 830b8d6471d5f1e09e0f13a0982b5849cd61f4b6
```

Isolated test target:

`test/worktree-sim-target-20260905`

Logical Chat A topic branch:

`test/worktree-sim-chat-a-20260905`

Logical Chat B topic branch:

`test/worktree-sim-chat-b-20260905`

Both topic branches were created from the same canonical base SHA:

`af02345fcfed0ebe7d4b6503af7e89cdf48b84cf`

No R015 write targeted `main`.

## Experiment A — branch isolation for two logical chats

Both Chat A and Chat B began from the same `app.py` blob:

`830b8d6471d5f1e09e0f13a0982b5849cd61f4b6`

Chat A wrote:

```python
print("Worktree simulator - chat A")
```

Result:

```text
commit: c1208d6bb5f9e6cc28df7fcc4463d6144750cda9
blob:   3bfca5a381fe300d4fa82124d13ad1be452f0d20
tree:   2b8ed91cadeb83f1788993c5fb461d47bb2f3a16
```

Chat B independently wrote:

```python
print("Worktree simulator - chat B")
```

Result:

```text
commit: 1904904cde94c87bee17ab2e26d757d880f3fb07
blob:   0c31c87093bb7539e992e9ebd41739aa2f7c1877
tree:   a9f3a25c164205be8292487977a18ad938609ce6
```

After both writes, the isolated target still contained:

```python
print("Library final change")
```

with its original blob:

`830b8d6471d5f1e09e0f13a0982b5849cd61f4b6`

Therefore two logical chats can mutate the same path from the same base without stepping on each other when each owns a distinct topic branch.

This qualifies branch-level workspace isolation, not conflict-free later integration. If both branches change the same lines, their eventual merge/rebase may still require explicit conflict handling.

## Experiment B — lock authority

### Initial shared-registry candidate

An initial candidate used a dedicated coordination branch:

`test/worktree-sim-registry-20260905`

with deterministic lock files:

```text
locks/test__worktree-sim-chat-a-20260905.json
locks/test__worktree-sim-chat-b-20260905.json
```

A second attempt to create Chat A's existing lock path without the existing blob SHA failed with HTTP `422`.

This demonstrated path-level collision rejection, but a shared registry branch is itself a mutable shared ref.

### Improved design — one lock ref per logical worktree

R015 therefore tested a stronger primitive:

```text
lock/worktree-sim-chat-a-20260905
lock/worktree-sim-chat-b-20260905
```

Each lock is its own Git ref.

Both distinct refs were created successfully.

A second attempt to create:

`lock/worktree-sim-chat-a-20260905`

was rejected by GitHub with:

```text
HTTP 422
Reference already exists
```

This provides an atomic exclusivity gate at ref creation time.

Recommended authority model:

```text
lock ref exists
  -> logical worktree is claimed

lock ref absent
  -> acquisition may be attempted

create lock ref succeeds
  -> caller owns acquisition attempt

create lock ref returns already-exists
  -> fail closed; do not enter writable mode
```

### Owner annotation

After successful lock-ref creation, each lock branch received a marker:

`.chatgpt-worktree-lock.json`

containing at least:

```text
schema
repository
owner
work_unit
topic_branch
target_branch
base_sha
state
```

For Chat A:

```text
lock ref: lock/worktree-sim-chat-a-20260905
owner: chat-a
work_unit: WT-SIM-A
topic_branch: test/worktree-sim-chat-a-20260905
state: ACTIVE
lock annotation commit: 854952358a22750cb6979eff3d50d071c84e04ec
```

For Chat B:

```text
lock ref: lock/worktree-sim-chat-b-20260905
owner: chat-b
work_unit: WT-SIM-B
topic_branch: test/worktree-sim-chat-b-20260905
state: ACTIVE
lock annotation commit: cccb5408cad24ffd0d64dbbb6416c7fdc6c3c12f
```

If a runtime fails after creating the lock ref but before writing valid owner metadata, the lock is **ambiguous**, not free. A later runtime must retain/fail closed until the orphan lock is explicitly reconciled.

## Experiment C — portable standalone worktree snapshots

Because native linked worktrees are not individually portable, R015 built a standalone Git repository for each logical chat.

The local commit identity was allowed to differ from GitHub. Exact tree equality was used as the represented-state invariant.

### Chat A snapshot

Library path:

`/git-workspaces/ManuelBouza/test_biblioteca/worktree-simulator/chat-a/current.tar.gz`

Library identifiers:

```text
file_id: file_000000009fa4822fb1d30f2f64dd36dc
library_file_id: libfile_89a49affcf9481918009f551ee971bd7
```

Archive:

```text
size: 11480 bytes
SHA-256: 7bd8003eded552e35d24189880a5538be8a5c53e26c2c759d90a31f3a23780f9
```

Restored Git state:

```text
local snapshot HEAD: 1d5f6800517d04967f3c2eaefd4d878a38eef79f
local tree:          2b8ed91cadeb83f1788993c5fb461d47bb2f3a16
remote branch tree:  2b8ed91cadeb83f1788993c5fb461d47bb2f3a16
git fsck --full:     PASS
working tree:        clean
```

### Chat B snapshot

Library path:

`/git-workspaces/ManuelBouza/test_biblioteca/worktree-simulator/chat-b/current.tar.gz`

Library identifiers:

```text
file_id: file_00000000759c822f9d67ac6d99760ff1
library_file_id: libfile_68d9a8c3d1ec8191bb9b6ec6d7c27072
```

Archive:

```text
size: 11473 bytes
SHA-256: 9aa9104da4a56c5aa70285571326f7538dd6ef046272187dadf25953956a093c
```

Restored Git state:

```text
local snapshot HEAD: 8a6d11626365f4a23eab95f482d9df6658175436
local tree:          a9f3a25c164205be8292487977a18ad938609ce6
remote branch tree:  a9f3a25c164205be8292487977a18ad938609ce6
git fsck --full:     PASS
working tree:        clean
```

Both archives were materialized back from Library before verification.

This establishes the portable representation:

```text
logical worktree
  = topic branch identity
  + exclusive lock identity
  + standalone repository snapshot
  + ownership receipt
```

rather than a literal linked `git worktree` directory.

## Snapshot receipt

Each archive contains a sidecar `receipt.json` outside the repository worktree so the Git working tree remains clean.

The qualified receipt fields include:

```text
schema
repository
owner
work_unit
topic_branch
remote_head_sha
remote_tree_sha
local_snapshot_head_sha
local_snapshot_tree_sha
lock_path / lock identity
portable_git_dir
working_tree_clean
```

The receipt is evidence and routing metadata. GitHub remains canonical for remote branch/lock state.

## Experiment D — wrong-owner write gate

Chat A's restored receipt stated:

```text
owner: chat-a
topic_branch: test/worktree-sim-chat-a-20260905
```

A simulated attempt to enter writable mode as:

```text
expected owner: chat-b
requested branch: test/worktree-sim-chat-a-20260905
```

was rejected before mutation:

```text
WRITE_GATE=BLOCKED
owner mismatch: receipt=chat-a expected=chat-b
```

The local gate returned a non-zero failure code (`42`) intentionally.

GitHub owner metadata for the same logical worktree also identified Chat A.

Therefore a restored snapshot is not considered writable merely because it can be materialized. The runtime must prove that current work-unit identity matches the snapshot receipt and remote lock authority.

## Required writable-entry gate

Before a simulated worktree may mutate repository state, require all applicable checks:

```text
1. expected repository == receipt.repository
2. expected owner/work-unit == receipt owner/work-unit
3. expected topic branch == receipt.topic_branch
4. dedicated lock ref exists
5. lock annotation matches owner/work-unit/topic branch
6. lock state is ACTIVE
7. current remote topic branch exists
8. remote HEAD/tree is compatible with the restored receipt
9. restored repository passes archive/checksum validation
10. git fsck --full passes
11. restored Git tree matches the expected represented remote tree
12. working tree has no unexplained changes before new mutation
```

Any mismatch is fail-closed.

No automatic reset/clean/delete should be used to force the gate to pass.

## Suggested acquisition protocol

For a new writable work unit:

```text
1. identify repository + target + work-unit
2. choose deterministic unique topic branch
3. derive deterministic lock-ref name from repository/topic branch
4. attempt atomic lock-ref creation
5. if lock already exists -> BLOCKED / inspect owner; do not write
6. annotate acquired lock with owner/work-unit/topic/target/base
7. create or verify the topic branch
8. build/materialize the portable standalone worktree snapshot
9. validate checksum + fsck + clean status + tree identity
10. persist snapshot under branch/work-unit-specific Library namespace
11. enter writable mode
```

The lock must be acquired before writable execution, not after changes have already been made.

## Suggested resume protocol in another chat

A later chat continuing the same work unit should:

```text
1. locate the exact Library worktree snapshot
2. materialize/extract it
3. read receipt.json
4. verify expected coordinator/work-unit identity
5. read the dedicated GitHub lock ref and lock annotation
6. require owner/work-unit/topic equality
7. read current GitHub topic branch
8. compare remote freshness with receipt
9. validate archive + fsck + tree + status
10. only then continue local mutation
```

This is the cross-chat analogue of checking that the correct native worktree is still owned by the correct task.

## Freshness and moving-branch rule

A valid ownership lock does not imply that a previously restored snapshot is current.

Before any remote write:

- re-read the topic branch;
- compare expected remote HEAD/blob/tree preconditions;
- if the branch moved unexpectedly, stop and reconcile rather than overwrite;
- persist a refreshed snapshot only after the represented state has been validated.

R014's stale-base `409` evidence remains applicable.

Ownership safety and freshness safety are separate gates.

## Release and garbage collection

Worktree lock retirement and Library snapshot GC are related but distinct.

Recommended ordering after successful integration:

```text
1. prove PR merged / work integrated
2. refresh and verify target snapshot under R014 lifecycle rules
3. prove no unique/unrepresented work remains in the topic snapshot
4. retire/delete merged topic Library snapshot as allowed by R014
5. mark worktree ownership closed/released
6. remove dedicated lock ref under an explicit safe cleanup operation
7. optionally retire remote topic branch under normal branch policy
```

For closed-unmerged or ambiguous work:

```text
retain snapshot
retain or explicitly classify lock/ownership state
fail closed on automatic destructive cleanup
```

A stale-looking lock is not by itself deletion authority.

## Why GitHub is the lock authority

Library is appropriate for persistent worktree data, but R015 does not use Library as the exclusivity authority.

Reasons:

- Library is not the canonical Git remote;
- file overwrite/version semantics are distinct from Git ref ownership;
- this research did not establish a compare-and-swap primitive suitable for a cross-chat lock race;
- GitHub ref creation provides an explicit create-or-already-exists result;
- branch/ref state is already part of the canonical source-maintenance authority plane.

Therefore the simulator separates roles:

```text
GitHub lock ref = ownership/exclusivity authority
GitHub topic branch = canonical work branch
Library snapshot = persistent portable worktree state
receipt = routing/evidence metadata
workspace = temporary execution surface
```

## Failure classification

### Lock ref already exists

Result:

`BLOCKED_OWNER_EXISTS`

Do not write.

### Lock exists but marker missing/corrupt

Result:

`BLOCKED_AMBIGUOUS_LOCK`

Do not assume abandoned; preserve for explicit reconciliation.

### Receipt owner differs from lock owner

Result:

`BLOCKED_IDENTITY_MISMATCH`

Do not write.

### Snapshot tree differs from expected remote tree

Result:

`BLOCKED_STALE_OR_WRONG_SNAPSHOT`

Refresh/reconcile; do not silently overwrite remote state.

### Snapshot fails `git fsck`

Result:

`BLOCKED_INVALID_SNAPSHOT`

Retain last known-good snapshot where available.

### Remote topic branch moved after snapshot

Result:

`BLOCKED_STALE_BASE`

Use explicit reconciliation and fresh remote preconditions.

## Capability matrix

| Capability | Status | Evidence |
| --- | --- | --- |
| native local worktrees isolate branches | VERIFIED | local `git worktree` experiment |
| linked worktree directory alone is portable across chats | NOT SUPPORTED | `.git` points to primary repository worktree metadata |
| two logical chats can mutate same path independently on distinct branches | VERIFIED | remote Chat A / Chat B branch writes |
| target branch remains unchanged by isolated branch writes | VERIFIED | post-write target re-read |
| deterministic same-worktree lock collision is rejected | VERIFIED | GitHub HTTP 422 |
| dedicated per-worktree lock ref create-or-exists gate | VERIFIED | duplicate ref -> `Reference already exists` |
| owner metadata bound to lock ref | VERIFIED | `.chatgpt-worktree-lock.json` on lock branches |
| portable standalone `.git` snapshot per logical worktree | VERIFIED | Library Chat A / Chat B archives |
| Library round-trip checksum/fsck/tree verification | VERIFIED | both worktree snapshots |
| exact remote/local worktree tree equality | VERIFIED | A `2b8ed91c...`, B `a9f3a25c...` |
| wrong-owner restored snapshot blocked before mutation | VERIFIED | `WRITE_GATE=BLOCKED`, exit 42 |
| actual two independent chats racing for same lock at the same instant | NOT VERIFIED | collision semantics tested sequentially |
| lock TTL / heartbeat / automatic stale-owner recovery | NOT VERIFIED | not implemented or tested |
| crash between lock-ref creation and owner annotation | DESIGNED FAIL-CLOSED / NOT FULLY QUALIFIED | lock remains ambiguous |
| lock-ref retirement after integration | NOT VERIFIED | cleanup not exercised in R015 |
| automatic conflict-free integration of two branches editing same lines | NOT VERIFIED / NOT EXPECTED | isolation does not remove Git merge conflicts |

## Important distinction: simulator versus native worktree

The term **worktree simulator** is deliberate.

A native Git worktree shares one repository object database and administrative `.git/worktrees/*` state. Separate ChatGPT chats normally execute in separate temporary runtime filesystems, so they cannot rely on one continuously shared native worktree registry.

R015 instead reproduces the operational invariants:

- unique writable ownership;
- branch isolation;
- no shared mutable checkout;
- durable mapping from work unit to branch/workspace;
- restorable Git state;
- explicit retirement after integration.

It does not reproduce:

- object-database sharing efficiency;
- native `git worktree list` visibility across separate runtimes;
- filesystem-level locking from a continuously mounted repository.

## Remaining qualification gaps

Before treating the simulator as a production adapter, qualify at least:

1. actual two-chat acquisition of different worktrees from separate ChatGPT conversations;
2. actual two-chat collision attempt against the same dedicated lock ref;
3. process/runtime crash immediately after lock creation and orphan-lock recovery;
4. lock release/ref deletion after successful merge plus R014 snapshot GC;
5. closed-unmerged ownership retention and later resume from another chat;
6. lock ownership transfer, if ownership transfer is ever allowed;
7. branch name encoding/canonicalization against unusual Git ref names;
8. long-running work freshness/heartbeat policy if stale locks need automated classification;
9. concurrent creation of many distinct lock refs at scale;
10. interaction with repository branch protection/rulesets when lock refs are used in governed repositories.

## Disposition

R015 is:

```text
Research-State: COMPLETE
Decision-State: NOT_REQUIRED
```

because the investigation has answered the current feasibility question and records a qualified non-normative mechanism.

The evidence supports this bounded conclusion:

```text
ChatGPT can emulate exclusive cross-chat writable worktrees by combining:
  - one topic branch per work unit,
  - one atomically acquired dedicated GitHub lock ref per logical worktree,
  - one portable standalone Git repository snapshot in a unique Library namespace,
  - ownership/freshness receipts checked before mutation.
```

The evidence does not establish a native persistent `git worktree` service inside ChatGPT or Library.

If Agent Governance chooses to adopt this as an official source-maintenance adapter, that adoption should proceed through the appropriate normative decision/design path. D058 already defines the required isolation invariant; R015 only qualifies a mechanism that can satisfy it in a cross-chat Library-backed environment.
