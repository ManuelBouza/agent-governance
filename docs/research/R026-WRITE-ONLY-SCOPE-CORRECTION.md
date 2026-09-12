# R026 — Write-only scope correction

Research-ID: R026  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-12  
Last-Reviewed: 2026-09-12  
Owner: ChatGPT Orchestrator  
Scope: correction to narrow R026 from read/write interaction minimization to write-path minimization only  
Question: Given the Human Owner decision to keep repository reads direct from GitHub, how should R026 minimize GitHub write amplification without changing the read path?  
Evaluation-Refs: Human Owner direction 2026-09-12; empirical Git Data publication already exercised in R026 and `ManuelBouza/test_biblioteca`  
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

The logical mutation count is therefore constant with respect to the number of files changed.

Branch creation and PR creation remain separate lifecycle operations when required.

## Safety invariant

The bounded write path must remain fail-closed against stale branch movement:

1. read/record the expected topic-branch HEAD before publication;
2. create the candidate commit with that exact SHA as parent;
3. update the topic ref with `force=false`;
4. if the remote branch moved incompatibly, the ref update must fail rather than overwrite the remote state;
5. verify the resulting diff/tree after successful publication.

Normal writes remain restricted to the verified topic branch. No direct development writes to `develop` or `main` are authorized by this correction.

## Current disposition

```text
R026 scope: WRITE MINIMIZATION ONLY
Read path: DIRECT GITHUB
Library: OUT OF SCOPE
Work-local/Desktop: OUT OF SCOPE
Snapshot/artifact bootstrap: OUT OF SCOPE
Preferred write primitive: create_tree -> create_commit -> update_ref(non-force)
Normative change: none yet
T058: remains frozen
T063/O277: unchanged
```

The next useful empirical work, if any, should focus only on write semantics: multi-file batching, deletions/renames, binary-file handling, stale-ref races, maximum payload limits, and exact post-publication verification.
