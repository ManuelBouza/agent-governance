# R014 Appendix — ChatGPT Library snapshot lifecycle and garbage collection

Research-ID: R014 (supporting appendix)  
Status: QUALIFIED / NON_NORMATIVE  
Opened: 2026-09-05  
Last-Reviewed: 2026-09-05  
Owner: ChatGPT Orchestrator  
Parent-Research: `docs/research/CHATGPT-GIT-WORKSPACE-AND-GITHUB-TRANSPORT-RESEARCH.md`  
Decision-Ref: none

## Purpose

R014 established that ChatGPT Library can persist individual working files and packaged Git repositories, including `.git`, across chats. Official OpenAI documentation checked by R014 also establishes finite Library quotas and does not establish automatic oldest-file eviction when the quota is reached.

Therefore a Library-backed Git checkpoint workflow needs an explicit snapshot lifecycle so persistent storage does not accumulate obsolete branch state indefinitely.

This appendix defines and now empirically qualifies the **core lifecycle mechanism** derived from R014 evidence. It remains non-normative: it is not Agent Governance policy, does not amend the branching model, and does not authorize automatic deletion outside the safety conditions below.

## Design objective

Use GitHub for durable canonical history and Library only for recoverable active/canonical working checkpoints.

Desired steady state per repository:

```text
<repository>/
  main/
    current snapshot
  develop/
    current snapshot              # only when the repository uses develop
  active-branches/
    <branch>/
      current snapshot            # only while branch/work remains active
```

The steady-state intent is:

```text
GitHub
  = permanent canonical commit/merge history

Library
  = current recoverable snapshots for main/develop + active work
```

Merged feature/task branch snapshots should not become a second permanent history archive because GitHub already retains that history canonically.

## Snapshot classes

### Canonical branch snapshot

A snapshot associated with a long-lived canonical branch such as `main` or `develop`.

Default retention:

- keep one currently validated snapshot per canonical branch;
- during refresh, the previous snapshot may remain temporarily until the replacement is validated;
- after successful validation and promotion, the previous canonical snapshot becomes deletion-eligible.

A repository that does not use `develop` should not manufacture a `develop` snapshot merely for this mechanism.

### Active branch snapshot

A snapshot associated with work that has not yet been conclusively integrated or discarded.

Examples:

- feature branch with an open PR;
- task branch under active development;
- local branch checkpoint not yet represented canonically in the target branch.

Default retention:

- preserve while work is active;
- do not delete merely because the branch is old;
- do not delete merely because a PR is closed;
- do not delete merely because the remote branch disappears.

### Merged branch snapshot

A branch snapshot becomes cleanup-eligible only after GitHub provides positive evidence that the work was integrated into its intended target.

The minimum GitHub gate is:

```text
PR merged == true
```

`state == closed` is insufficient because closed-unmerged work may still be the only recoverable copy of abandoned or deferred changes.

## Fail-closed deletion rule

Deletion is destructive. The lifecycle therefore uses a fail-closed classification:

```text
MERGED + target refreshed + target snapshot verified
    -> branch snapshot MAY be deleted

OPEN / ACTIVE
    -> retain

CLOSED but NOT MERGED
    -> retain

remote branch missing but merge not proven
    -> retain

merge/target status unavailable or ambiguous
    -> retain

snapshot validation failure
    -> retain previous snapshots
```

Any uncertainty resolves to **retain**, not delete.

## Canonical snapshot rotation

For `main` and `develop`, replacement should be transactional in ordering even though Library itself is not a Git transaction system.

Required order:

```text
1. read current canonical branch from GitHub
2. create candidate repository snapshot
3. upload candidate to Library
4. rediscover/materialize candidate from Library
5. verify archive integrity/checksum
6. extract repository
7. run git fsck --full
8. verify expected Git tree / branch state
9. promote candidate as current
10. re-materialize and re-verify promoted current
11. delete superseded prior canonical snapshot
12. re-list Library and confirm expected retained state
```

The previous canonical snapshot must **not** be deleted before the replacement passes validation and promotion verification.

If steps 2-10 fail, retain the old canonical snapshot unchanged.

## Merged branch cleanup algorithm

For a branch associated with a pull request:

```text
1. read PR from GitHub
2. require merged == true
3. identify the actual target/base branch
4. read current target branch from GitHub
5. confirm the integrated result is represented in the target branch
6. create/refresh the target branch Library snapshot
7. materialize the new target snapshot back from Library
8. verify checksum/archive readability
9. extract and run git fsck --full
10. verify expected target Git tree/state
11. promote and re-verify target current
12. only then delete Library snapshots belonging exclusively to the merged branch
13. re-list Library to verify cleanup
```

Where commit ancestry/reachability can be inspected, the adapter should additionally verify that the merge/integration history reaches the feature commit before deleting the branch snapshot.

A failure at any gate stops cleanup and preserves the branch snapshot.

## Closed-unmerged and abandoned work

A closed PR is not evidence of integration.

For:

```text
PR state: closed
merged: false
```

automatic deletion is prohibited by this mechanism.

Cleanup requires either:

- explicit Human authorization to discard the work; or
- a future normative rule with equivalent positive abandonment evidence.

The same rule applies when a remote branch has been manually deleted but its integration status cannot be proven.

## Quota-pressure cleanup order

If Library storage approaches its quota, cleanup should prioritize redundant state rather than active recovery state.

Recommended order:

1. snapshots of branches already proven merged and whose target snapshot is validated;
2. superseded generations of `main`/`develop` after a newer validated generation exists;
3. duplicate/test snapshots whose contents are independently proven redundant;
4. closed-unmerged/abandoned snapshots only with explicit Human approval;
5. never automatically evict the sole current validated snapshot of `main`, `develop`, or active work merely to recover quota.

This ordering is a design recommendation, not a claim about OpenAI product behavior. R014 found no documented automatic Library eviction policy.

The selector itself has **not** yet been qualified against an actual or simulated quota-pressure trigger. That is the remaining GC-specific qualification gap.

## Suggested naming model

A deterministic layout reduces accidental deletion across projects:

```text
/git-workspaces/<owner>/<repo>/canonical/main/current.tar.gz
/git-workspaces/<owner>/<repo>/canonical/develop/current.tar.gz
/git-workspaces/<owner>/<repo>/active/<encoded-branch>/current.tar.gz
```

If temporary candidate files are required during rotation:

```text
.../canonical/develop/candidate-<timestamp-or-head>.tar.gz
```

A candidate should be promoted conceptually to `current` only after round-trip validation. Exact Library rename/overwrite mechanics remain tooling-dependent and should be revalidated in the runtime performing the operation.

Branch names must be encoded deterministically so `/`, spaces, or other path-sensitive characters cannot cause cross-branch ambiguity.

## Snapshot verification receipt

Before any destructive cleanup, retain a compact receipt containing at least:

```text
repository
source branch
source/target GitHub ref
expected Git HEAD or tree
archive SHA-256
git fsck result
Library path/file identifier when exposed
verification timestamp
cleanup classification
```

The receipt may live in the controlling chat/task record or another durable governance artifact when the mechanism becomes normative. It is not a substitute for GitHub canonical state.

## Relationship to GitHub branch deletion

Library cleanup and GitHub branch deletion are separate operations.

This appendix does not require deletion of the GitHub branch and does not treat a missing GitHub branch as proof that the Library snapshot is disposable.

If a later workflow deletes merged GitHub branches, recommended ordering is still:

```text
verify merge
-> refresh/verify target snapshot
-> retire Library branch snapshot
-> independently apply GitHub branch-retirement policy
```

The exact ordering of remote branch deletion relative to Library deletion should be decided by the normative source-maintenance workflow if this mechanism is adopted.

## Empirical qualification — 2026-09-05

### Scope

The core lifecycle was exercised end-to-end in `ManuelBouza/test_biblioteca` using isolated test branches. Repository `main` was not modified.

Branches:

```text
target:   test/library-gc-target-20260905
positive: test/library-gc-merged-20260905
negative: test/library-gc-unmerged-20260905
```

Library qualification root:

`/git-workspaces/ManuelBouza/test_biblioteca/qualification`

### Positive merged-branch case

Positive feature HEAD:

`799a4976a438ee70bde9b9634e7ad51d483b90e7`

Positive feature remote tree:

`fab3804804953725837aa6470a65c4f82600b9ed`

The Library feature snapshot was round-trip materialized and validated before merge:

```text
path: /git-workspaces/ManuelBouza/test_biblioteca/qualification/active/test-library-gc-merged-20260905/current.tar.gz
library_file_id: libfile_0ca487987a758191b6ecfcc715454097
file_id before deletion: file_000000000350822f9143fd905775af6d
size: 11687 bytes
SHA-256: b78e91ddb225dca65bd1055ac5b15c92ac26a775d59271479af6fe5a8ae581c7
git fsck --full: PASS
working tree: clean
local snapshot tree: fab3804804953725837aa6470a65c4f82600b9ed
remote feature tree: fab3804804953725837aa6470a65c4f82600b9ed
```

GitHub PR `#1`, `test: qualify Library GC merged-branch cleanup`, targeted only `test/library-gc-target-20260905`. Before merge GitHub reported `mergeable: true` and `mergeable_state: clean`.

The PR was merged with expected head `799a4976a438ee70bde9b9634e7ad51d483b90e7`.

Merge result:

```text
merged: true
merge commit: 40315fe606b906b9c4abc075eb636328c77e1f6c
parent 1 / target pre-merge: d3e9048e27448264d8dc9601d1821963cc24cc3a
parent 2 / feature:          799a4976a438ee70bde9b9634e7ad51d483b90e7
```

The second parent provides positive reachability evidence for the exact positive feature HEAD.

Post-merge target remote tree:

`718b6d6c83d40d3f389b3430c190aacafb21727a`

A locally merged reconstruction produced the same tree SHA exactly:

`718b6d6c83d40d3f389b3430c190aacafb21727a`

The post-merge target candidate snapshot was created and uploaded as:

```text
candidate path: /git-workspaces/ManuelBouza/test_biblioteca/qualification/canonical/target/candidate-40315fe606b906b9c4abc075eb636328c77e1f6c.tar.gz
candidate file_id: file_00000000a0c8822fb1183ca0ea481ffc
library_file_id: libfile_f431e2e6d9b88191bc07fd89430261b8
size: 12013 bytes
SHA-256: 2dbca71e3006230b696ce6392e5d8ca3739d3e3a20eccba86ec14f9d3354afb0
```

Round-trip candidate validation passed:

```text
archive SHA-256: exact match
git fsck --full: PASS
working tree: clean
snapshot tree: 718b6d6c83d40d3f389b3430c190aacafb21727a
remote target tree: 718b6d6c83d40d3f389b3430c190aacafb21727a
```

### Safe canonical rotation and destructive cleanup

The old target `current` was not deleted first. Rotation used:

```text
old current -> previous-premerge.tar.gz
validated candidate -> current.tar.gz
re-list
re-materialize promoted current
re-verify checksum / fsck / clean / exact target tree
```

Promoted current:

```text
file_id: file_0000000090e4822fbaf957ff5981adb6
library_file_id: libfile_f431e2e6d9b88191bc07fd89430261b8
size: 12013 bytes
SHA-256: 2dbca71e3006230b696ce6392e5d8ca3739d3e3a20eccba86ec14f9d3354afb0
tree: 718b6d6c83d40d3f389b3430c190aacafb21727a
git fsck --full: PASS
```

Only after this second verification were these files deleted from the active Library view:

- superseded pre-merge target snapshot `file_00000000adcc822fb55fc7e127fb3fc3`;
- merged positive feature snapshot `file_000000000350822f9143fd905775af6d`.

The Library delete operation moved the deleted files to Trash; it did not imply immediate physical erasure. This is consistent with the product deletion-retention distinction already recorded by R014.

Post-delete audit verified:

```text
canonical target: exactly one current snapshot retained
positive active branch folder: no current snapshot retained
```

This qualifies the intended merged-branch retirement order.

### Negative closed-unmerged case

Negative feature HEAD:

`18e4c045677e1a9824fb02c12dac1ff927ec8f00`

Remote negative feature tree:

`d110de0171073576023005293d1a56f92b1f305f`

Library snapshot:

```text
path: /git-workspaces/ManuelBouza/test_biblioteca/qualification/active/test-library-gc-unmerged-20260905/current.tar.gz
library_file_id: libfile_18219e40cf378191979b5029cba38e5b
file_id: file_000000000a30822faafb41d32ace5634
size: 11691 bytes
SHA-256: 6359e5edef0204555243631cecff77689952419b4f339e8dade27299aba6eed5
```

GitHub PR `#2`, `test: qualify Library GC closed-unmerged retention`, was explicitly closed without merge:

```text
state: closed
merged: false
```

After closure, the snapshot was re-listed and re-materialized. Verification still passed:

```text
SHA-256: 6359e5edef0204555243631cecff77689952419b4f339e8dade27299aba6eed5
git fsck --full: PASS
working tree: clean
snapshot tree: d110de0171073576023005293d1a56f92b1f305f
remote feature tree: d110de0171073576023005293d1a56f92b1f305f
```

The snapshot was intentionally retained. This qualifies the `closed + not merged -> retain` gate.

### Corrupt-candidate failure case

A deliberately invalid candidate was uploaded under the target canonical folder:

```text
path: .../canonical/target/candidate-invalid.tar.gz
file_id: file_000000004c2c822fa23cb05a8cc5e89c
library_file_id: libfile_abbaa01cdaa4819181cda64acff0a1aa
size: 41 bytes
SHA-256: a47fca924ebd2cc5e1f0fc8a555cd8ab09d505e81421263d9914983b4ba6ffd8
```

The object materialized byte-for-byte, but archive validation failed as intended:

```text
gzip: stdin: not in gzip format
tar: Child returned status 1
tar: Error is not recoverable: exiting now
validation exit: 2
```

After that failure, the canonical `current.tar.gz` was re-listed and remained unchanged as `file_0000000090e4822fbaf957ff5981adb6`, size `12013`, with the previously validated SHA-256. Only the invalid candidate was then removed to Trash.

This qualifies the fail-closed rule that a failed candidate must not displace or delete the current validated snapshot.

## Core qualification result

`PASS`

The empirical exercise qualifies these lifecycle gates:

- create/refresh canonical snapshot after a real merge;
- round-trip checksum and `git fsck` validation;
- positive `merged == true` gating;
- exact feature reachability through the merge commit parent;
- exact post-merge target-state validation using Git tree SHA equality;
- candidate promotion followed by second validation;
- Library merged-branch snapshot deletion only after target validation;
- post-delete Library listing verification;
- closed-unmerged PR fail-closed retention;
- corrupt/invalid candidate failure without current-snapshot loss.

## Remaining qualification gap

The only lifecycle/GC-specific item from the prior checklist not exercised is:

- automatic quota-pressure selection under a real or simulated quota trigger, including proof that the selector never chooses the sole current validated copy of canonical or active work.

General R014 limitations remain separate, including behavior near the 512 MB file limit, exact arbitrary remote Git-object identity reconstruction, and the fact that Library is not itself a native Git working tree or remote.

## Current test artifacts

The older R014 experimental files under `/test_biblioteca_git_capability/` remain separate capability evidence and were not automatically deleted by this qualification.

Within the qualification hierarchy:

- the merged positive feature snapshot was retired as part of the successful test;
- the superseded pre-merge target snapshot was retired after the promoted target snapshot passed revalidation;
- the closed-unmerged negative feature snapshot remains intentionally retained;
- the deliberately corrupt candidate was removed after proving fail-closed behavior;
- the promoted target `current.tar.gz` remains as the validated canonical qualification snapshot.

## Disposition

This appendix now records an empirically **qualified core, non-normative lifecycle mechanism**:

```text
steady state = main + develop (when used) + active branches
merged branch = retire only after verified integration and verified/promoted target snapshot
closed-unmerged / ambiguous = retain
canonical refresh = validate new snapshot before deleting old snapshot
invalid candidate = preserve current
```

R014 remains `COMPLETE / NOT_REQUIRED`. Qualification demonstrates feasibility and safety properties of the tested mechanism; it does not adopt automatic Library garbage collection as Agent Governance policy.

If Agent Governance later standardizes this mechanism, the appropriate normative Specify/Design/Plan and decision path should define the triggering cadence, quota threshold/selector, receipts/audit location, branch naming/encoding contract, and explicit authority for destructive Library operations.