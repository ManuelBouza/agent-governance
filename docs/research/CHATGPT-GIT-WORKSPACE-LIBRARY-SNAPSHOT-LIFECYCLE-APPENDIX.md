# R014 Appendix — ChatGPT Library snapshot lifecycle and garbage collection

Research-ID: R014 (supporting appendix)  
Status: PROPOSED / NON_NORMATIVE  
Opened: 2026-09-05  
Last-Reviewed: 2026-09-05  
Owner: ChatGPT Orchestrator  
Parent-Research: `docs/research/CHATGPT-GIT-WORKSPACE-AND-GITHUB-TRANSPORT-RESEARCH.md`  
Decision-Ref: none

## Purpose

R014 established that ChatGPT Library can persist individual working files and packaged Git repositories, including `.git`, across chats. Official OpenAI documentation checked by R014 also establishes finite Library quotas and does not establish automatic oldest-file eviction when the quota is reached.

Therefore a Library-backed Git checkpoint workflow needs an explicit snapshot lifecycle so persistent storage does not accumulate obsolete branch state indefinitely.

This appendix defines a **candidate operational mechanism** derived from R014 evidence. It is not Agent Governance policy, does not amend the branching model, and does not authorize automatic deletion outside the safety conditions below.

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
- after successful validation, the previous canonical snapshot becomes deletion-eligible.

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
8. verify expected HEAD / branch state
9. mark candidate as current
10. delete superseded prior canonical snapshot
11. re-list Library and confirm expected retained state
```

The previous canonical snapshot must **not** be deleted before the replacement passes validation.

If steps 2-9 fail, retain the old canonical snapshot unchanged.

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
10. verify expected target HEAD/state
11. only then delete Library snapshots belonging exclusively to the merged branch
12. re-list Library to verify cleanup
```

Where commit ancestry/reachability can be inspected, the adapter should additionally verify that the integration commit or resulting history is reachable from the target branch before deleting the branch snapshot.

A failure at any gate stops cleanup and preserves the branch snapshot.

## Closed-unmerged and abandoned work

A closed PR is not evidence of integration.

For:

```text
PR state: closed
merged: false
```

automatic deletion is prohibited by this candidate mechanism.

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
expected Git HEAD
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

## Current test artifacts

The R014 experimental Library files under `/test_biblioteca_git_capability/` should **not** be automatically deleted merely because the experiments completed. The isolated GitHub branch `test/library-git-capability-matrix` was used for capability testing and was not qualified here as a merged branch cleanup case.

They may be removed later as explicit test-data cleanup once their evidence has been captured durably and the Human authorizes disposal, or they may be retained for additional lifecycle qualification.

## Qualification still required before automation

The lifecycle design itself has not yet been exercised end-to-end against a real merged-branch snapshot retirement. Before automatic deletion is adopted, qualify at least:

- create/refresh canonical snapshot after a merge;
- round-trip checksum and `git fsck` validation;
- positive `merged == true` gating;
- target commit/history reachability check where available;
- Library branch-snapshot deletion;
- post-delete Library listing verification;
- failure behavior proving that a failed validation does not delete the previous snapshot;
- closed-unmerged PR behavior proving fail-closed retention;
- quota-pressure selection without deleting active/canonical sole copies.

## Disposition

This appendix converts the storage-limit observation into a concrete **non-normative lifecycle design**:

```text
steady state = main + develop (when used) + active branches
merged branch = retire after verified integration and verified target snapshot
closed-unmerged / ambiguous = retain
canonical refresh = validate new snapshot before deleting old snapshot
```

R014 remains `COMPLETE / NOT_REQUIRED` because this document records feasibility and a candidate mechanism only. If Agent Governance chooses to make automatic Library garbage collection part of the source-maintenance workflow, that adoption should proceed through the appropriate normative Specify/Design/Plan and decision path rather than being inferred from this appendix.
