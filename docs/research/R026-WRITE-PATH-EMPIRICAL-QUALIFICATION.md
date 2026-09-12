# R026 — Write-path empirical qualification

Research-ID: R026  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Date: 2026-09-12  
Owner: ChatGPT Orchestrator  
Scope: empirical qualification of the GitHub Git Data write path after Human direction narrowed R026 to write minimization only

## Test boundary

Disposable repository: `ManuelBouza/test_biblioteca`  
Canonical base used by the write tests: `main@af02345fcfed0ebe7d4b6503af7e89cdf48b84cf`  
Primary qualification branch: `research/r026-write-qualification`  
Stale-race branch: `research/r026-stale-qualification`

The tests intentionally leave repository reads direct from GitHub. Snapshot/archive/Library/Work-local read optimization is out of scope.

## Result summary

### 1. Delete and rename semantics — PASS

A single `create_tree` based on the base tree used:

- `sha: null` for `app.py`, deleting it;
- inline content for `renamed_app.py`;
- inline content for `notes.txt`.

The tree was committed and the branch ref advanced with `force=false`.

Remote compare confirmed:

- `app.py` removed;
- `renamed_app.py` added;
- `notes.txt` added.

For this transport, a rename is represented as delete-old-path + add-new-path in one tree. GitHub may or may not classify that pair as a semantic rename in compare output; repository state is nevertheless atomic in the resulting commit.

Evidence commits:

- tree: `8a3c38f2aedf656dc698e523bce85a222d0c4d38`
- commit: `89cd03f0c1510ae3ab31715f67700634b65f0a72`

### 2. Binary publication — PASS with one additional blob mutation

A deterministic 1024-byte binary payload was encoded as base64 and sent through `create_blob`.

- blob SHA: `c8b49c8cd518e58491924bfc364ff26e01a85009`
- tree SHA: `e0e48bcb2582244f5137bbce2e10998b94f316d0`
- commit SHA: `6f43aac2ee6536fee0e90f3da610c140f2f8af2c`

The tree referenced the blob SHA at `fixtures/sample.bin`; commit and `update_ref(force=false)` succeeded. Remote compare reports the binary path as added.

Implication: the normal text-only batch can remain three mutations (`create_tree -> create_commit -> update_ref`), while each binary object that cannot be represented inline requires a preceding `create_blob` mutation unless an equivalent already-known blob SHA can be reused.

### 3. Multi-file batching — PASS at N=64

A single `create_tree` call added 64 text files under `batch/`, all with inline content, on top of the prior tree.

- tree SHA: `06c910edd6f3ef834cf5dc5a3fde846bdf8998a9`
- commit SHA: `693e7b74f540192a932ea511f119a5f647decee8`

Publication required exactly:

1. `create_tree`
2. `create_commit`
3. `update_ref(force=false)`

Remote compare from the original base to the final qualification commit reports 68 changed paths total: 64 batch files plus the binary, the deleted original path, and the two text additions used by the rename/delete test.

This empirically establishes a lower bound: at least 64 small text-file changes can be published through the installed connector with three GitHub write mutations independent of N.

It does **not** establish the maximum accepted request size or entry count.

### 4. Explicit stale-ref race — PASS / fails closed

Two sibling commits were constructed from the same base `af02345fcfed0ebe7d4b6503af7e89cdf48b84cf`:

- stale candidate: `6819044fa5de39cec13b7db3189e8025fcefd4fb`
- concurrent winner: `e2532a450638a4190756016591c7addae8aeb22b`

The stale-race branch was first advanced to the concurrent winner with `force=false`. A subsequent attempt to move that branch to the sibling stale candidate, again with `force=false`, was rejected by GitHub with HTTP 422:

`Update is not a fast forward`

A direct branch read after the failure confirmed the ref remained at `e2532a450638a4190756016591c7addae8aeb22b`.

This validates the required fail-closed concurrency behavior provided that publication always uses `force=false` and the proposed commit has the expected parent.

### 5. Payload limits — bounded evidence, exact ceiling NOT QUALIFIED

Official GitHub `Create a tree` documentation specifies the tree-entry schema, supports `content` or object `sha`, and documents `sha: null` deletion semantics, but does not state a maximum request size or maximum number of entries for the create-tree request.

Official reference:

`https://docs.github.com/en/rest/git/trees`

The same documentation states a 100,000-entry / 7 MB limit for the **recursive Get Tree response**, which must not be misrepresented as a Create Tree write limit.

Official Git blob documentation states that blob retrieval supports blobs up to 100 MB, but the current qualification does not treat that read limit as proof of an identical connector create-blob ceiling.

Official reference:

`https://docs.github.com/en/enterprise-cloud@latest/rest/git/blobs?apiVersion=2022-11-28`

Therefore the only connector-specific payload statement justified by this pilot is:

> One `create_tree` carrying 64 small inline text entries succeeds. The exact connector/API request ceiling remains unspecified and must be handled as an implementation bound rather than a governance constant.

No artificial maximum was probed because doing so would create large disposable objects and would still only measure the current connector/runtime envelope.

## Minimum post-publication verification

For the write-minimized path, the minimum safe sequence is:

```text
prepare complete change set against expected HEAD
-> create_tree(base_tree = expected HEAD tree)
-> create_commit(parent = expected HEAD)
-> update_ref(force = false)
-> read branch ref and require ref == new commit SHA
```

For material multi-file changes, add one bounded `compare_commits(expected_base, new_head)` read to confirm the expected changed-path set before PR/review. Reads are not an optimization target under the current Human-directed scope.

The stale-race experiment demonstrates why successful object creation is not sufficient: unreferenced candidate trees/commits can exist even when the final ref update correctly fails.

## Qualified write architecture

```text
GitHub direct reads
        |
        v
prepare coherent change set
        |
        v
[text changes] create_tree with inline content / sha:null
[binary changes] create_blob as required, then reference SHA in create_tree
        |
        v
create_commit(parent = expected HEAD)
        |
        v
update_ref(force=false)
        |
        +-- non-fast-forward -> FAIL CLOSED / reread and reconcile
        |
        v
verify exact branch ref
        |
        +-- material change -> compare expected base/head paths
        v
PR / review / integration
```

## Disposition

The core write path is empirically qualified for:

- additions and modifications using inline text content;
- deletions;
- rename-as-delete-plus-add;
- binary files via explicit blob creation;
- a 64-file inline text batch in one tree;
- fail-closed stale-ref races with `force=false`;
- bounded post-publication verification.

The exact payload ceiling remains deliberately unqualified. It is a runtime/transport bound, not a product-policy constant.

R026 remains `COMPLETE / EVALUATING`; this evidence does not itself adopt a normative D066 replacement or modify T058/T063 authority.