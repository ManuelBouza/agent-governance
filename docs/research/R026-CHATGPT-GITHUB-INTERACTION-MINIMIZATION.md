# R026 — ChatGPT/GitHub interaction minimization

Research-ID: R026  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-12  
Last-Reviewed: 2026-09-12  
Owner: ChatGPT Orchestrator  
Scope: ChatGPT Orchestrator repository interaction minimization, with current effective scope narrowed by Human direction to GitHub write-path minimization only  
Question: How can Agent Governance minimize routine ChatGPT write interactions with GitHub without weakening canonical Git authority, branch isolation, conflict detection, review traceability or the Human/Orchestrator/Executor ownership model?  
Evaluation-Refs: desk research 2026-09-12; empirical Git Data publication exercised during R026; later Human corrections narrow current applicability  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Current effective scope

R026 was initially opened as a broader read/write interaction-minimization investigation. Human direction later narrowed the active problem:

```text
READS
  remain direct from GitHub

WRITES
  are the optimization target
```

The detailed historical investigation remains preserved in the R026 correction appendices and Git history. The current candidate architecture is intentionally simpler:

```text
GitHub direct reads
  -> exact refs/files/searches as needed

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

No current R026 proposal depends on Library, a PC-local repository, Work Desktop, repository snapshots, or GitHub Actions artifacts for the read path.

## Write amplification problem

Per-file Contents API writes produce an undesirable shape:

```text
update file A -> remote mutation/commit
update file B -> remote mutation/commit
update file C -> remote mutation/commit
...
```

For an N-file documentation or specification change, this creates O(N) remote mutations and can create multiple intermediate commits that do not represent a complete coherent change set.

GitHub's Git Data model supports a bounded alternative:

```text
N changed files
-> one tree containing all changes
-> one commit over the expected parent
-> one ref update
```

The number of publication mutations is therefore constant with respect to N.

## Evidence

### GitHub official Git Data behavior

GitHub's Git Trees API supports creating a tree with multiple entries and a `base_tree`. Entries may carry content directly. A new commit can point to the resulting tree, and the branch ref can then be updated to that commit.

Relevant official documentation reviewed during R026:

- GitHub REST API — Git trees: https://docs.github.com/en/rest/git/trees
- GitHub REST API — Git commits: https://docs.github.com/en/rest/git/commits
- GitHub REST API — Git refs: https://docs.github.com/en/rest/git/refs

### Current ChatGPT GitHub plugin capability

The active GitHub connector exposes the required primitives:

```text
create_tree
create_commit
update_ref
compare_commits
```

It also exposes per-file `create_file`, `update_file`, and `delete_file`, but those are not the preferred publication primitive for coherent multi-file changes when the Git Data route is available.

### Empirical evidence gathered during R026

R026 successfully used:

```text
create_tree
-> create_commit
-> update_ref(force=false)
```

to publish multiple R026 files as a single commit on its research topic branch.

The same round-trip was independently exercised on the disposable repository `ManuelBouza/test_biblioteca`: a sandbox-prepared edit was published through the same three-mutation sequence and verified remotely. This demonstrates current connector compatibility with the bounded Git Data path.

That disposable-repository pilot also explored snapshot/artifact read optimization. The Human Owner subsequently removed read optimization from scope. Those artifact results remain experimental evidence only and are not part of the current architecture.

## Preferred write algorithm

### Preconditions

Before publication, ChatGPT must know:

```text
target repository
target topic branch
expected topic-branch HEAD SHA
expected parent tree or commit tree
complete intended change set
```

Normal repository reads remain direct GitHub reads.

### Publication

For text files that can be represented inline:

```text
1. create_tree(
     base_tree = expected parent tree,
     entries = all changed paths/content
   )

2. create_commit(
     tree = new tree,
     parent = expected topic HEAD
   )

3. update_ref(
     branch = topic branch,
     sha = new commit,
     force = false
   )
```

This should represent the complete logical change in one commit.

### Verification

After a successful ref update, perform a bounded remote verification such as:

```text
compare expected base/head
or
fetch resulting commit/tree
```

Verification should confirm:

- the topic ref points to the intended commit;
- only intended paths changed;
- no unintended deletion or replacement occurred;
- the branch remains based on the expected lineage.

## Stale-write safety

The design must fail closed when another actor moves the topic branch between preparation and publication.

The expected parent SHA is therefore a concurrency token.

Example:

```text
expected topic HEAD = A

ChatGPT creates candidate C with parent A

another actor moves remote topic:
A -> B

ChatGPT attempts:
B -> C with force=false
```

Because C does not contain B, the non-force ref update should be rejected rather than overwrite B.

If this occurs, ChatGPT must re-read the new remote state and reconcile rather than force the ref.

## Interaction budget

For one coherent publication work unit after the topic branch exists:

```text
GitHub reads:        direct/as needed; not optimized by R026

publication writes:
  create_tree:       1
  create_commit:     1
  update_ref:        1

verification read:   1 bounded verification recommended
```

Thus the publication mutation budget is:

```text
3 remote mutations independent of changed-file count
```

Branch creation and PR creation are lifecycle operations and are counted separately when needed.

## Why this is preferable to per-file updates

The bounded Git Data path provides four material advantages:

1. **constant mutation count** for N changed files;
2. **one coherent commit** instead of intermediate per-file commits;
3. **better stale-write semantics** through an explicit expected parent and non-force ref movement;
4. **cleaner verification** because the complete intended change has one commit boundary.

## Out-of-scope read optimization

By current Human direction, the following are not part of R026's active design:

```text
Library persistence
persistent PC/Work Desktop repository
sandbox repository snapshot as read cache
GitHub Actions artifact bootstrap
archive-based repository materialization
attempts to reduce ordinary GitHub file reads
```

Reads continue directly against GitHub using the connector.

## Remaining write-path qualification gaps

Before a normative decision changes D066 or other governance policy, the following write cases should be qualified explicitly:

### 1. Deletions

Confirm the exact `create_tree` representation for deleting paths through the active connector wrapper.

### 2. Renames

Git trees represent a rename as deletion + addition at the tree level. Confirm expected diff quality and policy semantics.

### 3. Binary files

Inline text content is not sufficient for all binary changes. Qualify whether `create_blob(base64)` + `create_tree(sha)` is the appropriate bounded path.

### 4. Payload limits

Measure connector/GitHub practical limits for large multi-file trees and large inline content so the design has a deterministic fallback threshold.

### 5. Stale-ref race

Run an explicit two-writer race test on a disposable branch and confirm `update_ref(force=false)` rejects incompatible remote advancement.

### 6. Verification contract

Choose the minimum required post-write verification primitive for normal writes (`compare_commits`, commit/tree read, or another bounded read).

## Acceptance target for a future normative decision

A write-optimized transport should satisfy:

```text
A. ordinary repository reads remain direct GitHub reads
B. N-file text publication uses constant-count remote mutations
C. the logical change is represented by one commit
D. remote topic movement cannot be silently overwritten
E. no direct development write targets develop/main
F. post-publication verification proves exact intended change boundary
G. per-file Contents API writes are fallback, not the default multi-file path
H. no Library or PC-local dependency is introduced
```

## Relationship to D066 and T058

R026 does not itself change D066.

D066 remains the accepted authority until a later decision explicitly adopts a refined write transport. T058 remains frozen by Human decision and is not resumed by this research.

R026's present recommendation is narrower than its initial investigation:

```text
keep direct GitHub reads
adopt/qualify bounded Git Data publication for writes
```

## Current disposition

```text
Research-State: COMPLETE
Decision-State: EVALUATING
Current scope: WRITE MINIMIZATION ONLY
Read path: DIRECT GITHUB
Preferred candidate: create_tree -> create_commit -> update_ref(non-force)
Normative change: none
T058: remains frozen
```

The next empirical work should focus only on unresolved write semantics: deletion, rename, binary content, payload limits, stale-ref races, and final verification.
