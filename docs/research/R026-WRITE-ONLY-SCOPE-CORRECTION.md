# R026 — Write-only scope correction

Research-ID: R026  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-12  
Last-Reviewed: 2026-09-12  
Owner: ChatGPT Orchestrator  
Scope: correction to narrow R026 from read/write interaction minimization to write-path minimization only  
Question: Given the Human Owner decision to keep repository reads direct from GitHub, how should R026 minimize GitHub write amplification without changing the read path?  
Evaluation-Refs: Human Owner direction 2026-09-12; `R026-WRITE-PATH-EMPIRICAL-QUALIFICATION.md`; empirical Git Data publication in `ManuelBouza/test_biblioteca`  
Decision-Ref: none  
Supersedes: R026 read-side optimization proposals, including snapshot/artifact bootstrap work  
Superseded-By: none

## Human direction

The Human Owner narrowed the objective:

```text
keep reads direct from GitHub
optimize writes only
```

Therefore R026 no longer proposes replacing ordinary GitHub reads with sandbox snapshots, GitHub Actions artifacts, Library, Work-local repositories, or any other read cache/materialization layer.

The artifact/snapshot experiment executed in `ManuelBouza/test_biblioteca` remains evidence only. It is not part of the current candidate architecture and should not be implemented in `agent-governance` under this scope.

## Effective candidate architecture

```text
GitHub direct reads
  -> read exact refs/files/searches as needed

ChatGPT reasoning / temporary sandbox when useful
  -> prepare complete multi-file change set

GitHub bounded publication
  -> create_tree with all changed paths/content
  -> create_commit with expected parent SHA
  -> update_ref non-force
  -> bounded verification

PR
  -> normal review/integration path
```

## Write-path objective

Replace write amplification of the form:

```text
update file A -> commit
update file B -> commit
update file C -> commit
...
```

with:

```text
N changed files
-> 1 create_tree
-> 1 create_commit
-> 1 update_ref
```

The logical mutation count is therefore constant with respect to the number of inline text-file changes included in one accepted tree request.

Branch creation and PR creation remain separate lifecycle operations when required. Binary objects that require `create_blob` add one mutation per newly created blob before the common tree/commit/ref sequence.

## Safety invariant

The bounded write path must remain fail-closed against stale branch movement:

1. read/record the expected topic-branch HEAD before publication;
2. create the candidate commit with that exact SHA as parent;
3. update the topic ref with `force=false`;
4. if the remote branch moved incompatibly, the ref update must fail rather than overwrite the remote state;
5. read the branch ref after success and require it to equal the candidate commit SHA;
6. for material multi-file changes, compare the expected base and new head to verify the changed-path set before PR/review.

Normal writes remain restricted to the verified topic branch. No direct development writes to `develop` or `main` are authorized by this correction.

## Empirical qualification status

`R026-WRITE-PATH-EMPIRICAL-QUALIFICATION.md` records the disposable-repository qualification completed on 2026-09-12.

Qualified:

- deletion via `sha: null`;
- rename represented as delete-old + add-new in one tree;
- binary publication via base64 `create_blob` plus tree SHA reference;
- one `create_tree` containing 64 inline text-file changes;
- `create_commit` with the expected parent;
- `update_ref(force=false)` stale-race rejection with HTTP 422 non-fast-forward;
- post-failure ref preservation;
- bounded post-publication ref/diff verification.

Payload ceiling:

- the installed connector empirically accepts at least 64 small inline entries in one tree;
- official GitHub Create Tree documentation does not state a create-request maximum that R026 can safely treat as a governance constant;
- therefore the exact ceiling remains an implementation/runtime bound, not an unresolved product-policy requirement.

## Current disposition

```text
R026 scope: WRITE MINIMIZATION ONLY
Read path: DIRECT GITHUB
Library: OUT OF SCOPE
Work-local/Desktop: OUT OF SCOPE
Snapshot/artifact bootstrap: OUT OF SCOPE
Preferred text write primitive: create_tree -> create_commit -> update_ref(non-force)
Binary extension: create_blob as required -> create_tree -> create_commit -> update_ref(non-force)
Stale ref behavior: EMPIRICALLY FAIL-CLOSED
64-file text batch: EMPIRICALLY QUALIFIED
Exact payload ceiling: IMPLEMENTATION BOUND / NOT A GOVERNANCE CONSTANT
Normative change: none yet
T058: remains frozen
T063/O277: unchanged
```

The remaining R026 step is no longer additional transport experimentation by default. It is a governance decision: determine whether this qualified write path should be adopted normatively (for example by refining D066 / repository-write operating rules) or remain research evidence only.