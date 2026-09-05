# R015 Appendix — reusable lock lifecycle and post-merge worktree retirement

Research-ID: R015 (supporting appendix)  
Status: QUALIFIED / NON_NORMATIVE  
Opened: 2026-09-05  
Last-Reviewed: 2026-09-05  
Owner: ChatGPT Orchestrator  
Parent-Research: `docs/research/CHATGPT-LIBRARY-WORKTREE-SIMULATOR-RESEARCH.md`  
Related-Research: R014  
Normative-Authority: D058 remains the workspace-isolation requirement  
Decision-Ref: none

## Purpose

R015 originally qualified the core cross-chat worktree-simulator model:

```text
one writable work unit
  -> one topic branch
  -> one exclusive GitHub lock identity
  -> one portable standalone Git snapshot in Library
  -> one ownership/freshness receipt
```

The first R015 lock experiment used creation of a dedicated Git ref as the atomic acquisition primitive. Duplicate ref creation correctly failed with HTTP 422, but the connected GitHub surface available during the later lifecycle qualification did not expose ref deletion. A ref-existence-only lock could therefore be acquired but could not be cleanly released and reused through the tested connector surface.

This appendix qualifies a reusable refinement and closes the R015 post-integration retirement gap:

```text
dedicated persistent lock branch
  + .chatgpt-worktree-lock.json sentinel
```

The branch is a stable lock namespace. The sentinel file, not branch existence, is the occupancy signal.

## Current recommended non-normative lock model

For a logical writable worktree:

```text
lock branch exists + sentinel absent
    -> lock namespace is FREE

create sentinel succeeds
    -> ACQUIRED

create sentinel when sentinel already exists
    -> BLOCKED_OWNER_EXISTS

sentinel exists but metadata is corrupt/ambiguous
    -> BLOCKED_AMBIGUOUS_LOCK

release
    -> fetch sentinel + exact blob SHA
    -> delete sentinel with that SHA

sentinel absent after delete
    -> RELEASED

later create sentinel succeeds again
    -> REACQUIRED
```

The dedicated lock branch can remain permanently as a reusable namespace. This avoids requiring Git ref deletion for ordinary lock release.

The topic branch and lock branch remain different authorities:

```text
topic branch = canonical work changes
lock branch  = ownership namespace only
Library      = portable worktree state
receipt      = owner/freshness evidence
```

## Why the original ref-only lock is retained as evidence but not preferred for lifecycle

The original R015 experiment remains valid evidence that GitHub ref creation provides create-or-already-exists collision behavior:

```text
create dedicated ref once  -> success
create same ref again       -> HTTP 422 Reference already exists
```

However, the later connector surface exposed create/move ref operations but no delete-ref operation. Therefore:

```text
ref-only acquisition = VERIFIED
ref-only reusable release through tested connector = NOT AVAILABLE
```

This appendix does not erase that finding. It refines the operational candidate to a sentinel-file lock that supports both acquisition and release with available connected operations.

## Experiment E — post-merge simulated-worktree retirement

### E1 — controlled merge topology

Repository:

`ManuelBouza/test_biblioteca`

Isolated target:

`test/worktree-sim-target-20260905`

Chat A topic branch:

`test/worktree-sim-chat-a-20260905`

Chat B topic branch remained active during Chat A retirement:

`test/worktree-sim-chat-b-20260905`

Canonical `main` was not a merge target.

A controlled PR was opened:

```text
PR: test_biblioteca#3
title: test: qualify worktree simulator release lifecycle
base: test/worktree-sim-target-20260905
head: test/worktree-sim-chat-a-20260905
head SHA: c1208d6bb5f9e6cc28df7fcc4463d6144750cda9
```

Direct GitHub PR state before merge returned:

```text
mergeable: true
mergeable_state: clean
```

The merge used the expected feature head SHA and succeeded:

```text
merged: true
merge commit: 364e576c172dc651f1ff30fc94e3e2f3667caf2c
```

Merge commit parents:

```text
parent 1: af02345fcfed0ebe7d4b6503af7e89cdf48b84cf
parent 2: c1208d6bb5f9e6cc28df7fcc4463d6144750cda9
```

The second parent positively proves that the exact Chat A feature head is represented in the merge history.

Remote post-merge tree:

`2b8ed91cadeb83f1788993c5fb461d47bb2f3a16`

### E2 — post-merge target snapshot refresh

The pre-existing portable Chat A repository already represented the exact post-merge file tree. It was relabeled as a target snapshot and given a new local snapshot commit while preserving the exact Git tree.

Local target snapshot:

```text
local snapshot HEAD: 8ff3f8a047cdfef48e4df442630e65d34c8e46b4
local tree:          2b8ed91cadeb83f1788993c5fb461d47bb2f3a16
remote merge HEAD:   364e576c172dc651f1ff30fc94e3e2f3667caf2c
remote merge tree:   2b8ed91cadeb83f1788993c5fb461d47bb2f3a16
```

As in R014/R015, commit SHA identity was not required for the portable snapshot; exact Git-tree identity plus a receipt carrying the canonical remote HEAD was the represented-state invariant.

A target candidate archive was created:

```text
size: 11928 bytes
SHA-256: fe62583e892d2d3b72b877b347f74bb7f2fc3169c4696f35abb9437747f2f384
```

Library candidate:

```text
path: /git-workspaces/ManuelBouza/test_biblioteca/worktree-simulator/target/candidate.tar.gz
file_id: file_00000000943c81f4be5c8956dbd55b02
library_file_id: libfile_343ddfec0c5081919a6d1e19ab451034
```

The candidate was materialized back from Library and passed:

```text
archive SHA-256: exact
tar extraction: PASS
git fsck --full: PASS
working tree: clean
local tree == remote merge tree: true
```

### E3 — safe promotion before destructive cleanup

After candidate validation:

```text
candidate.tar.gz -> current.tar.gz
```

Promoted Library target:

```text
path: /git-workspaces/ManuelBouza/test_biblioteca/worktree-simulator/target/current.tar.gz
file_id: file_00000000943c81f4be5c8956dbd55b02
library_file_id: libfile_343ddfec0c5081919a6d1e19ab451034
size: 11928 bytes
SHA-256: fe62583e892d2d3b72b877b347f74bb7f2fc3169c4696f35abb9437747f2f384
tree: 2b8ed91cadeb83f1788993c5fb461d47bb2f3a16
```

The promoted `current` was materialized a second time and revalidated before any Chat A cleanup:

```text
SHA-256: exact
git fsck --full: PASS
working tree: clean
tree == remote target tree: true
```

This preserves the R014 fail-closed ordering:

```text
merge proven
-> target candidate
-> Library round-trip validation
-> promote target current
-> revalidate promoted current
-> only then retire feature worktree state
```

### E4 — Chat A Library snapshot retirement

Only after the target `current` passed its second validation was the Chat A snapshot removed from the active Library view:

```text
old path: /git-workspaces/ManuelBouza/test_biblioteca/worktree-simulator/chat-a/current.tar.gz
file_id: file_000000009fa4822fb1d30f2f64dd36dc
library_file_id: libfile_89a49affcf9481918009f551ee971bd7
original SHA-256: 7bd8003eded552e35d24189880a5538be8a5c53e26c2c759d90a31f3a23780f9
```

Library reported:

```text
File moved to trash
```

A recursive post-delete listing contained:

- target `current.tar.gz`;
- Chat B `current.tar.gz`;
- no active Chat A `current.tar.gz`.

As with R014, Library Trash is not evidence of immediate physical erasure.

### E5 — Chat A lock release

Before release, Chat A's lock sentinel was re-read:

```text
lock branch: lock/worktree-sim-chat-a-20260905
sentinel: .chatgpt-worktree-lock.json
owner: chat-a
work_unit: WT-SIM-A
state: ACTIVE
blob SHA: 586d32036b2ad24791a0669d26aef9a3b6962cd3
```

Release used the exact current blob SHA:

```text
delete commit: 146673469c03328b516e4064a8fa98d31a0fb2bc
```

A subsequent fetch of `.chatgpt-worktree-lock.json` on the same lock branch returned HTTP 404 / Not Found.

Therefore:

```text
Chat A snapshot retired
+ Chat A sentinel absent
= logical Chat A simulated worktree released
```

The lock branch itself remained as a reusable namespace.

### E6 — Chat B remained active and untouched

After Chat A merge/GC/release, Chat B still had its Library snapshot:

```text
path: /git-workspaces/ManuelBouza/test_biblioteca/worktree-simulator/chat-b/current.tar.gz
file_id: file_00000000759c822f9d67ac6d99760ff1
size: 11473 bytes
```

Chat B's lock sentinel also remained:

```text
lock branch: lock/worktree-sim-chat-b-20260905
owner: chat-b
work_unit: WT-SIM-B
topic branch: test/worktree-sim-chat-b-20260905
state: ACTIVE
blob SHA: e988c4aa2ac58179df7f73c9c62916a74651065a
```

This proves that retirement of one simulated worktree does not require retirement or mutation of another active logical worktree in the same repository.

### E7 — canonical main remained unchanged

After the entire retirement test:

```text
main: af02345fcfed0ebe7d4b6503af7e89cdf48b84cf
message: Apply accumulated Library changes
```

No R015 lifecycle merge targeted `main`.

## Experiment F — reusable sentinel acquisition/release/reacquisition

A separate lock namespace was created:

`lock/worktree-sim-reuse-probe-20260905`

The branch itself is not the occupancy signal. The sentinel file is.

### F1 — first acquisition

Creating:

`.chatgpt-worktree-lock.json`

for owner `reacquire-probe-1` succeeded:

```text
acquisition commit: 9864370bfdc939b3b8cd89694467f211086254ad
sentinel blob: 3ac1446233ab194e8d93b40fcf60641ea5f9b18e
```

### F2 — competing acquisition blocked

A second `create_file` against the same path while the sentinel existed was rejected with HTTP 422:

```text
Invalid request.
"sha" wasn't supplied.
```

For the contents API wrapper, this means the path already exists and cannot be created as a new file without supplying the current SHA for an update.

The existing lock owner remained `reacquire-probe-1`.

Therefore:

```text
first create wins
second create on existing sentinel fails closed
```

This is the tested collision behavior for the reusable sentinel lock.

### F3 — release

The sentinel was deleted using its exact blob SHA:

```text
release commit: 243a2f551d981c1b63d82d1cdfb0149cf55da97d
```

### F4 — reacquisition after release

The same sentinel path was then created again successfully for a different probe owner:

```text
owner: reacquire-probe-2
reacquisition commit: 6b79ce00e41168527f8917ddf31f4c3220b6e3b4
new sentinel blob: 93217360be5101d464eae85f3298f16be6b69ac6
```

This proves the same logical lock namespace can be reused after release.

The probe was finally released again:

```text
final release commit: a842b8b62a68336e406b53bfef355b1986b0402a
```

No active sentinel was intentionally left by the reuse probe.

## Contention semantics versus true simultaneous two-chat timing

R015 now has two layers of collision evidence:

1. duplicate creation of a dedicated Git ref returned `422 Reference already exists`;
2. duplicate creation of an existing sentinel file returned HTTP 422 while preserving the first owner.

These prove create-or-collide semantics at the GitHub authority plane.

This session did **not** create two physically independent ChatGPT runtimes that issued the same acquisition request at exactly the same instant. Therefore the strongest precise statement remains:

```text
same-resource duplicate acquisition is rejected by GitHub;
true wall-clock-simultaneous acquisition from two independent chats remains not directly observed.
```

Do not claim a literal two-chat timing race was empirically run until two separate chats/runtimes actually perform the acquisition against the same free sentinel concurrently.

## Incidental PR #4

During preparation of the lock-reuse probe, an unintended draft pull request was created:

```text
PR: test_biblioteca#4
state: closed
merged: false
title: test: incidental draft - closed
```

It was immediately closed without merge, did not create any new repository content, and is explicitly excluded from qualification evidence.

## Qualified release protocol

The empirically supported non-normative sequence is now:

```text
ACQUIRE
1. choose/verify dedicated lock branch namespace
2. require sentinel absent
3. create .chatgpt-worktree-lock.json
4. if create returns conflict/422 -> BLOCKED
5. re-read sentinel and verify owner/work-unit
6. create/verify unique topic branch
7. materialize/validate unique Library snapshot
8. enter writable mode

RESUME
1. materialize exact Library snapshot
2. verify receipt owner/work-unit/topic
3. fetch sentinel and verify same identity
4. re-read topic branch freshness
5. checksum + fsck + tree validation
6. enter writable mode only if every gate passes

RELEASE AFTER MERGE
1. prove PR merged / feature integrated
2. verify exact feature reachability/history where available
3. build fresh target snapshot candidate
4. upload + round-trip checksum/archive/fsck/tree verification
5. promote target current
6. materialize and verify promoted current again
7. retire merged feature Library snapshot
8. fetch exact current lock sentinel/blob SHA
9. delete sentinel with that SHA
10. verify sentinel absent
11. verify other active worktree snapshots/locks remain intact
12. retire topic/lock branches separately only if an independent branch-cleanup policy and available tooling authorize it
```

A failure before step 7 of release preserves the feature snapshot and sentinel. A failure to delete the sentinel leaves the worktree classified occupied/ambiguous, not free.

## Updated capability matrix

| Capability | Current status | Evidence |
| --- | --- | --- |
| branch-level isolation for separate writable work units | VERIFIED | R015 Experiments A-D |
| portable standalone Git snapshot per worktree | VERIFIED | R015 Library round trips |
| wrong-owner write gate | VERIFIED | R015 Experiment D |
| duplicate ref acquisition collision | VERIFIED | HTTP 422 `Reference already exists` |
| ref-only reusable release through tested connector | NOT AVAILABLE | no delete-ref action exposed in qualification runtime |
| dedicated lock branch + sentinel acquisition | VERIFIED | Experiment F1 |
| second sentinel acquisition blocked | VERIFIED | Experiment F2 / HTTP 422 |
| sentinel release with exact blob SHA | VERIFIED | Experiments E5/F3 |
| same lock namespace reacquired after release | VERIFIED | Experiment F4 |
| real merge -> target snapshot refresh -> feature snapshot GC -> lock release | VERIFIED | Experiment E |
| retirement of Chat A leaves Chat B active | VERIFIED | Experiment E6 |
| target snapshot exact remote-tree equivalence after merge | VERIFIED | `2b8ed91c...` equality |
| canonical `main` unaffected by lifecycle qualification | VERIFIED | `main = af02345...` |
| true physically simultaneous two-chat acquisition of one free sentinel | NOT VERIFIED | duplicate/collision semantics observed, not simultaneous wall-clock race |
| stale-lock TTL / heartbeat | NOT VERIFIED | not implemented |
| post-crash automatic owner recovery | NOT VERIFIED | fail-closed design only |
| branch-ref deletion/retirement via current connector | NOT AVAILABLE / NOT VERIFIED | separate from sentinel release |
| closed-unmerged cross-chat resume lifecycle | NOT YET QUALIFIED | future work |

## Remaining gaps

After this appendix, the material R015 gaps are narrower:

1. a real two-chat/two-runtime wall-clock race for the same free sentinel;
2. crash immediately after sentinel acquisition and durable orphan recovery;
3. TTL/heartbeat policy for long-running or abandoned ownership;
4. closed-unmerged ownership retention followed by resume from another chat;
5. optional ownership transfer semantics, if ever allowed;
6. branch/ref retirement mechanics when the connected GitHub surface exposes or delegates safe deletion;
7. unusual ref-name canonicalization and large-scale many-lock behavior;
8. branch-protection/ruleset interaction in governed repositories.

Post-merge snapshot GC and ordinary lock release/reacquisition are no longer gaps.

## Disposition

The R015 worktree-simulator core plus reusable lock lifecycle is now:

```text
QUALIFIED / NON_NORMATIVE
```

The current bounded architecture is:

```text
D058 isolation invariant
        |
        v
one topic branch per work unit
        +
dedicated persistent lock branch
        +
create/delete sentinel file as reusable ownership mutex
        +
unique portable standalone Git snapshot in Library
        +
receipt + remote freshness/tree validation
        +
R014-qualified target refresh and GC before release
```

GitHub remains the ownership/canonical authority. Library remains persistent worktree storage. The temporary workspace remains the execution surface.

No new Agent Governance normative policy is adopted by this appendix. If this adapter is standardized, the remaining crash/lease/concurrency semantics should be resolved through the appropriate design/decision path rather than inferred from research evidence.
