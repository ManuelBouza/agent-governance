# ChatGPT Git workspace, Library persistence, and GitHub transport research

Research-ID: R014  
Research-State: COMPLETE  
Decision-State: NOT_REQUIRED  
Opened: 2026-09-05  
Last-Reviewed: 2026-09-05  
Owner: ChatGPT Orchestrator  
Scope: ChatGPT temporary-workspace Git behavior, GitHub connector transport, ChatGPT Library persistence/version behavior, cross-chat repository-snapshot persistence, storage/retention boundaries, synchronization/conflict behavior, and snapshot lifecycle/garbage collection  
Question: Can ChatGPT combine a real local Git repository in the temporary workspace, persistent working-file or repository-snapshot storage in ChatGPT Library, and explicit GitHub connector operations into a reliable Git-oriented maintenance workflow; and which state, transport, retention, conflict, and cleanup boundaries remain separate?  
Evaluation-Refs: workspace/GitHub experiment against `ManuelBouza/agent-governance` at `develop` `20ed0e64dd6c98f38be42cd3cc28fcc220d06c5e`, temporary branch `test/chatgpt-git-workflow`, remote commit `c4a2c43a65554ed9c52a4047f954373935b06a07`; Library/GitHub experiments against `ManuelBouza/test_biblioteca`, commits `d82750a45f43f45a16c498674391a7a7e15dc319`, `af02345fcfed0ebe7d4b6503af7e89cdf48b84cf`, `5d04c16e5705e308457072792e4f3c5204768864`, and `dafe8a821e09a09a6200e4c5afed447fcf03320e`; cross-chat Library snapshot round trip verified 2026-09-05; Library lifecycle qualification using `test_biblioteca` PRs `#1` and `#2`; supporting lifecycle appendix `docs/research/CHATGPT-GIT-WORKSPACE-LIBRARY-SNAPSHOT-LIFECYCLE-APPENDIX.md`  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Summary

The experiments establish three distinct capability layers that can be composed but must not be conflated:

```text
GitHub canonical repository
        |
        | explicit connected GitHub read/write operations
        v
ChatGPT temporary workspace
  - executable filesystem
  - may contain real .git state
  - local status/diff/staging/commit semantics when Git is available
        |
        | explicit materialization / persistence operations
        v
ChatGPT Library
  - persistent file storage across chats
  - can preserve packaged repository snapshots including .git
  - not itself a native Git working tree or Git remote
```

The validated composition now includes:

- real local Git semantics in the temporary workspace;
- explicit GitHub connector reads/writes while direct CLI GitHub transport was unavailable in the tested runtime;
- GitHub -> Library -> modification -> GitHub round-trip synchronization;
- multiple Library working-file versions before one final GitHub update;
- a packaged complete repository including `.git` persisted in Library and restored as a valid Git repository;
- a two-chat persistence round trip in which Chat B restored the snapshot, created a local commit, uploaded a second snapshot, and Chat A independently recovered and verified that new Git history;
- multi-file reconstruction into one remote GitHub commit;
- stale-base conflict detection through GitHub blob-SHA preconditions and HTTP `409`;
- empirical non-preservation of local commit SHA identity when equivalent content is reconstructed through the tested GitHub connector path;
- a fail-closed Library snapshot lifecycle qualified with a real merged PR, a closed-unmerged PR, safe target-snapshot rotation, real Library deletion, and an intentionally corrupt candidate.

The result is a usable persistence/transport/checkpoint pattern, not a native Git remote hosted by Library. GitHub remains canonical remote authority. Library is persistent storage. Git semantics execute only after files or repository snapshots are materialized into an executable workspace.

The lifecycle/garbage-collection **core is empirically qualified but non-normative**. The remaining GC-specific gap is the automatic selector under actual or simulated quota pressure.

## Capability model

The investigation separates seven concerns:

1. **Local Git semantics** — a temporary workspace can host a real `.git` repository and run ordinary Git commands.
2. **Direct Git CLI transport** — the local Git process may or may not have network/DNS access to GitHub in a given runtime.
3. **Connected GitHub transport** — the GitHub connector/API surface can read and mutate canonical remote state independently of local CLI networking.
4. **Library persistence** — Library can retain files independently from the originating chat and make them reusable later.
5. **Repository snapshot persistence** — a packaged repository including `.git` can be stored in Library, materialized later, extracted, and resumed with Git history intact.
6. **Synchronization/conflict control** — local/Library state is not automatically synchronized; remote writes must be explicit and can use remote SHA preconditions to detect stale state.
7. **Snapshot lifecycle / garbage collection** — redundant merged/superseded snapshots can be retired safely only after positive GitHub state and replacement-snapshot verification; ambiguous or failed validation remains fail-closed.

## Experiment A — temporary workspace Git + GitHub connector

### Setup

Repository:

`ManuelBouza/agent-governance`

Canonical baseline during the experiment:

`develop = 20ed0e64dd6c98f38be42cd3cc28fcc220d06c5e`

Temporary branch:

`test/chatgpt-git-workflow`

Test file:

`.gitignore`

Original blob:

`d90d927a47936445fc975791ebedae651450cfd7`

### A1 — real local Git state

A repository initialized in the temporary ChatGPT execution workspace behaved as a normal Git working tree. The following succeeded locally:

- repository initialization;
- `git status`;
- `git diff`;
- `git add`;
- local `git commit`;
- ordinary file edits between commits.

This is actual `.git` state, distinct from Library metadata.

### A2 — direct Git CLI transport unavailable in the tested runtime

Direct GitHub transport from the local repository failed with:

```text
Could not resolve host: github.com
```

A later recheck during the `test_biblioteca` capability-matrix experiment reproduced the same result with `git ls-remote`:

```text
fatal: unable to access 'https://github.com/ManuelBouza/test_biblioteca.git/': Could not resolve host: github.com
```

Therefore these sessions did not establish a working path of:

```text
local .git -> git fetch/pull/push -> github.com
```

This is a dated runtime observation, not a universal product limitation. DNS/network availability must be revalidated per runtime.

### A3 — explicit GitHub connector transport succeeded

The connected GitHub surface independently succeeded at operations including:

- reading canonical branches/files;
- creating a temporary branch;
- writing file content;
- creating remote commits;
- comparing remote refs;
- re-reading remote state after mutation.

The original experiment produced remote commit:

`c4a2c43a65554ed9c52a4047f954373935b06a07`

and verified the temporary branch as one commit ahead with only `.gitignore` changed by two additions. The test branch ref was then reset to its baseline.

### A4 — local and remote commit identity are separate

A local Git commit is not automatically the GitHub commit created later by connected transport. Content/tree reconstruction through the connector can produce a different commit object and SHA. Experiment C demonstrates this explicitly.

## Experiment B — GitHub -> Library -> modification -> GitHub round trip

### Setup

Repository:

`ManuelBouza/test_biblioteca`

Branch:

`main`

File:

`app.py`

Initial GitHub state:

```text
content: print("Hello World")
blob SHA: ad35e5ae34d7df6d469bfe65dbfcefe988e0169f
```

Library working path:

`/test_biblioteca_flow/app.py`

### B1 — GitHub content persisted in Library

The GitHub file was read, copied into the temporary workspace, uploaded to Library, rediscovered, and read successfully.

One transient reference-visibility issue occurred immediately after upload: a newly returned file ID was temporarily not readable until rediscovered through Library listing. Later reads succeeded, so this was not treated as an upload failure.

### B2 — Library materialization, modification, overwrite, and verification

The Library copy was materialized into the executable workspace, changed to:

```python
print("Hello from ChatGPT Library")
```

and persisted back to Library. A later Library read verified the modified content.

### B3 — explicit write-back to GitHub

Before the remote write, GitHub was re-read and still contained the original content/blob. The Library-derived content was then written through the GitHub connector.

GitHub returned:

```text
commit SHA: d82750a45f43f45a16c498674391a7a7e15dc319
content/blob SHA: 45eac8ae8769283e63eec44d199100e7dfb6def2
```

A subsequent GitHub read confirmed:

```python
print("Hello from ChatGPT Library")
```

This completed:

```text
GitHub read
-> Library persist
-> Library materialize/modify/persist/read
-> GitHub update
-> GitHub read-back verification
```

### B4 — multiple Library states before one remote update

A second experiment performed multiple Library overwrites while GitHub remained unchanged.

Observed progression:

```text
version 2 -> print("Library change 1")
version 3 -> distinct intermediate persisted state
version 4 -> print("Library final change")
```

Immediately before the final GitHub write, the remote still contained:

```text
content: print("Hello from ChatGPT Library")
blob SHA: 45eac8ae8769283e63eec44d199100e7dfb6def2
```

Only after the final Library state was selected was GitHub updated once:

```text
commit SHA: af02345fcfed0ebe7d4b6503af7e89cdf48b84cf
message: Apply accumulated Library changes
content/blob SHA: 830b8d6471d5f1e09e0f13a0982b5849cd61f4b6
parent: d82750a45f43f45a16c498674391a7a7e15dc319
```

Final GitHub content:

```python
print("Library final change")
```

Therefore Library can hold several persistent working-file states while GitHub remains unchanged, followed by one explicit remote update. Library versions are not Git commits.

## Experiment C — repository snapshot, multi-file write, conflict detection, and commit identity

### Setup

Repository:

`ManuelBouza/test_biblioteca`

Isolated remote branch:

`test/library-git-capability-matrix`

A local reconstructed Git repository used:

`HEAD = 55f8e089179c5bc6a93d2d56385fb9d18203d6a8`

### C1 — complete `.git` snapshot can be persisted in Library

The complete repository, including `.git`, was packaged as:

`test_biblioteca_git_snapshot.tar.gz`

and stored at:

`/test_biblioteca_git_capability/test_biblioteca_git_snapshot.tar.gz`

Verified metadata:

```text
file_id: file_000000007794822fa2612ecab1f4dd4f
size: 11158 bytes
SHA-256: ee2cb5dbd3e7817315b17bd3931f89c1bbd2dee71cbc6c6504fc267baad4ff39
```

After Library materialization and extraction:

```text
git rev-parse HEAD -> 55f8e089179c5bc6a93d2d56385fb9d18203d6a8
git fsck --full    -> exit 0 / no findings
git status --short -> clean
```

This proves binary preservation of a packaged full Git repository including `.git`. It does **not** prove that Library exposes `.git` natively as a directly executable repository without materialization/extraction.

### C2 — multi-file reconstruction in one GitHub commit

Three changes were prepared:

- `app.py` -> `print("Library multi-file test")`
- `multi_a.txt` -> `multi-file A from Library`
- `multi_b.txt` -> `multi-file B from Library`

The remote GitHub tree was emitted as one tree and one commit:

```text
remote commit: 5d04c16e5705e308457072792e4f3c5204768864
message: Test multi-file Library synchronization
parent: af02345fcfed0ebe7d4b6503af7e89cdf48b84cf
```

GitHub reported exactly the three expected changed files. Multi-file reconstruction in one remote commit is therefore empirically supported for the tested case.

### C3 — connector reconstruction does not automatically preserve local commit SHA

Equivalent local Git commit:

`8cdedb9753126fa17a435756b3702c3a271af135`

Remote connector-created commit:

`5d04c16e5705e308457072792e4f3c5204768864`

The SHAs differ. Equivalent file content transported through this workflow does not automatically preserve local Git commit identity.

This does not rule out deliberately reconstructing an exact Git object if every tree/parent/author/committer/message/timestamp field is reproduced; that exact-object path was not tested.

### C4 — stale-base conflict detection

`app.py` initially had:

```text
content: print("Library multi-file test")
blob SHA: 9c7b101b815b6fc95672224de719e90ac0354e4a
```

A concurrent remote change advanced the branch to:

```text
commit: dafe8a821e09a09a6200e4c5afed447fcf03320e
content: print("Concurrent remote change")
new blob SHA: 1d4eade294f9d741e9bdf5087db38f607311d6ec
```

A write using the stale prior blob SHA was rejected with HTTP `409`.

Therefore stale remote state can be detected when the adapter carries forward and supplies the exact base blob SHA. The test qualifies stale-write detection, not automatic merge/reconciliation.

## Experiment D — cross-chat Library persistence of complete Git history

### Objective

Test actual persistence between separate chats rather than restoring the archive twice inside one runtime.

```text
Chat A
  full Git repo + .git
  -> Library source snapshot

Chat B
  find/materialize/extract source snapshot
  -> verify Git
  -> create new local commit
  -> package complete repo + .git
  -> upload second snapshot

Chat A
  find/materialize/extract second snapshot
  -> verify new Git history
```

### D1 — Chat B recovered the source snapshot

```text
path: /test_biblioteca_git_capability/test_biblioteca_git_snapshot.tar.gz
file_id: file_000000007794822fa2612ecab1f4dd4f
size: 11158 bytes
SHA-256: ee2cb5dbd3e7817315b17bd3931f89c1bbd2dee71cbc6c6504fc267baad4ff39
GIT_WORKTREE_VALID: true
HEAD_BEFORE: 55f8e089179c5bc6a93d2d56385fb9d18203d6a8
git fsck --full: PASS
```

### D2 — Chat B created a local commit

Created file:

`cross_chat_test.txt`

Exact content:

```text
Cross-chat Library persistence test
```

Local commit:

```text
SHA: 1a9bf18114de99fe385b8222c9c57c0b19de020a
message: Test cross-chat Library Git persistence
```

The working tree was clean after commit.

### D3 — Chat B persisted a second full Git snapshot

```text
path: /test_biblioteca_git_capability/test_biblioteca_git_snapshot_cross_chat.tar.gz
file_id: file_00000000ae8c822fa55d081b693f2dcc
library_file_id: libfile_00e7453c5a3c8191b8a42f657020fd62
size: 12052 bytes
SHA-256: 2ae7113c674f9caa29054833650f10c0904dba7f0ac51ef92ab885740ef0dbf4
```

Chat B re-materialized that upload and confirmed the same SHA-256.

### D4 — Chat A independently recovered Chat B's new snapshot

Back in the original chat:

```text
size: 12052 bytes
SHA-256: 2ae7113c674f9caa29054833650f10c0904dba7f0ac51ef92ab885740ef0dbf4
git rev-parse --is-inside-work-tree: true
HEAD: 1a9bf18114de99fe385b8222c9c57c0b19de020a
git fsck --full: PASS
cross_chat_test.txt: expected content present
latest commit message: expected message present
```

This is direct empirical evidence that a complete packaged Git repository can persist through Library across separate chats, be advanced by local Git in the second chat, and be recovered with the new history intact in the first chat.

The verified mechanism is **snapshot persistence**, not a persistent mounted working tree.

## Experiment E — Library snapshot lifecycle and garbage-collection qualification

Detailed procedure and receipts are preserved in:

`docs/research/CHATGPT-GIT-WORKSPACE-LIBRARY-SNAPSHOT-LIFECYCLE-APPENDIX.md`

### E1 — isolated test topology

Repository:

`ManuelBouza/test_biblioteca`

`main` was not modified.

Branches:

```text
target:   test/library-gc-target-20260905
positive: test/library-gc-merged-20260905
negative: test/library-gc-unmerged-20260905
```

Library root:

`/git-workspaces/ManuelBouza/test_biblioteca/qualification`

### E2 — positive merged branch

Positive feature HEAD:

`799a4976a438ee70bde9b9634e7ad51d483b90e7`

Remote feature tree:

`fab3804804953725837aa6470a65c4f82600b9ed`

Its Library snapshot was round-trip verified before merge:

```text
library_file_id: libfile_0ca487987a758191b6ecfcc715454097
file_id: file_000000000350822f9143fd905775af6d
size: 11687 bytes
SHA-256: b78e91ddb225dca65bd1055ac5b15c92ac26a775d59271479af6fe5a8ae581c7
git fsck: PASS
working tree: clean
snapshot tree == remote feature tree == fab3804804953725837aa6470a65c4f82600b9ed
```

GitHub PR `test_biblioteca#1` targeted only the isolated test target. Before merge it was `mergeable: true / clean`.

The merge was executed with expected feature head and produced:

```text
merged: true
merge commit: 40315fe606b906b9c4abc075eb636328c77e1f6c
parent 1: d3e9048e27448264d8dc9601d1821963cc24cc3a
parent 2: 799a4976a438ee70bde9b9634e7ad51d483b90e7
```

The second parent provides positive feature reachability evidence.

Post-merge target remote tree:

`718b6d6c83d40d3f389b3430c190aacafb21727a`

A local merged reconstruction produced exactly the same tree SHA.

### E3 — target candidate round-trip and promotion

Post-merge candidate:

```text
candidate file_id: file_00000000a0c8822fb1183ca0ea481ffc
library_file_id: libfile_f431e2e6d9b88191bc07fd89430261b8
size: 12013 bytes
SHA-256: 2dbca71e3006230b696ce6392e5d8ca3739d3e3a20eccba86ec14f9d3354afb0
snapshot tree: 718b6d6c83d40d3f389b3430c190aacafb21727a
remote target tree: 718b6d6c83d40d3f389b3430c190aacafb21727a
git fsck: PASS
working tree: clean
```

Safe rotation order was:

```text
old current -> previous-premerge
candidate -> current
re-list
re-materialize promoted current
re-verify checksum / fsck / exact tree
then delete old + merged-feature snapshot
```

Promoted current:

```text
file_id: file_0000000090e4822fbaf957ff5981adb6
library_file_id: libfile_f431e2e6d9b88191bc07fd89430261b8
size: 12013 bytes
SHA-256: 2dbca71e3006230b696ce6392e5d8ca3739d3e3a20eccba86ec14f9d3354afb0
tree: 718b6d6c83d40d3f389b3430c190aacafb21727a
git fsck: PASS
```

Only after re-verification were these Library objects deleted from the active view:

- superseded pre-merge target `file_00000000adcc822fb55fc7e127fb3fc3`;
- merged feature snapshot `file_000000000350822f9143fd905775af6d`.

The delete operation moved them to Library Trash. It did not prove immediate permanent erasure.

A post-delete listing showed one canonical `current` and no active snapshot for the merged positive branch.

### E4 — closed-unmerged retention

Negative feature HEAD:

`18e4c045677e1a9824fb02c12dac1ff927ec8f00`

Remote tree:

`d110de0171073576023005293d1a56f92b1f305f`

Library snapshot:

```text
library_file_id: libfile_18219e40cf378191979b5029cba38e5b
file_id: file_000000000a30822faafb41d32ace5634
size: 11691 bytes
SHA-256: 6359e5edef0204555243631cecff77689952419b4f339e8dade27299aba6eed5
```

GitHub PR `test_biblioteca#2` was explicitly closed without merge:

```text
state: closed
merged: false
```

The snapshot was intentionally retained and revalidated:

```text
SHA-256: exact
fsck: PASS
working tree: clean
snapshot tree == remote tree == d110de0171073576023005293d1a56f92b1f305f
```

This qualifies `closed + not merged -> retain`.

### E5 — corrupt candidate preserves current

A deliberately invalid candidate was uploaded:

```text
file_id: file_000000004c2c822fa23cb05a8cc5e89c
library_file_id: libfile_abbaa01cdaa4819181cda64acff0a1aa
size: 41 bytes
SHA-256: a47fca924ebd2cc5e1f0fc8a555cd8ab09d505e81421263d9914983b4ba6ffd8
```

Materialization succeeded byte-for-byte, but archive validation failed as intended:

```text
gzip: stdin: not in gzip format
tar: Child returned status 1
tar: Error is not recoverable: exiting now
validation exit: 2
```

After the failure, canonical `current` remained the previously validated `file_0000000090e4822fbaf957ff5981adb6`, size `12013`, with the same validated checksum/tree. Only the corrupt candidate was then removed to Trash.

This qualifies fail-closed replacement behavior.

### E6 — qualification result

Core lifecycle/GC result:

`PASS`

Qualified:

- positive `merged == true` gating;
- target/base identification;
- merge-history reachability through the feature parent;
- target candidate round-trip checksum/archive/fsck validation;
- exact target-state validation by Git tree SHA equality;
- candidate promotion followed by second verification;
- previous canonical deletion only after successful promotion verification;
- actual merged-feature snapshot deletion;
- post-delete Library audit;
- closed-unmerged retention;
- corrupt-candidate failure preserving current.

Not yet qualified:

- automatic quota-pressure selection under an actual or simulated quota condition.

The mechanism remains non-normative.

## Official ChatGPT Library product limits and retention

The following are vendor-documented product facts checked against official OpenAI Help Center documentation on 2026-09-05. They are time-sensitive and must be revalidated before future operational or normative reliance.

Primary source:

https://help.openai.com/en/articles/20001052-file-storage-and-library-in-chatgpt

Retention source:

https://help.openai.com/en/articles/8983778-how-are-files-vs-chats-retained

### Storage quotas

Current documentation states:

```text
Free:      500 MB
Go:          4 GB
Plus:       20 GB
Business:   20 GB
Pro:       100 GB
```

For the tested Plus context, the documented Library quota is `20 GB`.

### Per-file limits

Current documentation states:

- maximum uploaded file size: `512 MB`;
- text/document files: `2 million tokens` per file;
- CSV/spreadsheets: approximately `50 MB`, depending on row size;
- images: `20 MB` each.

For packaged Git repository snapshots such as `.tar.gz`, the most relevant documented boundary is the `512 MB` maximum upload size. R014 did not test behavior near that maximum.

### Separate storage and chat/file-upload controls

Official documentation states that Library storage is separate from daily attachment/chat limits.

### Files persist independently from the originating chat

Official documentation states that uploaded/created files saved to Library can be found and reused later, and that deleting a chat does not delete files saved to Library.

Experiment D independently confirms cross-chat reuse for the tested snapshots.

### No documented automatic oldest-file eviction at quota

Official documentation states that files are saved to the account until the user deletes them manually and exposes storage usage/remaining-space information. No automatic oldest-first or quota-triggered eviction policy was established in the reviewed official material.

Supported statement:

```text
Library files are documented as retained until manual deletion;
no automatic eviction mechanism was established by the reviewed documentation or R014 experiments.
```

This is a volatile vendor fact, not a timeless guarantee.

### Deletion retention

When a Library file is deleted, official documentation states that it is removed from the main Library view and scheduled for permanent deletion within `30 days`, subject to legal/security exceptions. The lifecycle qualification empirically observed deletion moving files to Library Trash, which is consistent with the distinction between removal from the active Library view and later permanent deletion.

Enterprise, Edu, and Healthcare workspaces may use workspace retention policy instead.

### Temporary Chat exception

Official Library documentation states that files uploaded in Temporary Chat are not saved to the account or Library. Temporary Chat should not be assumed to provide the persistence mechanism validated here.

## Confirmed capability matrix

| Capability | Status | Evidence |
| --- | --- | --- |
| local `git status` / `diff` / staging / commit | VERIFIED | Experiment A |
| direct CLI GitHub transport in tested runtime | UNAVAILABLE | DNS failure reproduced |
| GitHub connector read/write/verify | VERIFIED | Experiments A-C, E |
| Library working-file persistence/versioning | VERIFIED | Experiment B |
| accumulate multiple Library states before one GitHub write | VERIFIED | Experiment B4 |
| full repository snapshot including `.git` stored/restored | VERIFIED | Experiment C1 |
| full Git snapshot survives separate chats | VERIFIED | Experiment D |
| advance restored Git repo with a new local commit in another chat | VERIFIED | Experiment D2 |
| recover that new commit back in the original chat | VERIFIED | Experiment D4 |
| multi-file remote reconstruction in one commit | VERIFIED | Experiment C2 |
| stale remote state detected with blob SHA precondition | VERIFIED | Experiment C4 / HTTP 409 |
| merged branch snapshot retirement after verified target refresh | VERIFIED | Experiment E2-E3 |
| closed-unmerged snapshot retention | VERIFIED | Experiment E4 |
| failed/corrupt candidate preserves current validated snapshot | VERIFIED | Experiment E5 |
| exact local/remote content state comparison by Git tree SHA | VERIFIED | Experiment E2-E4 |
| automatic preservation of local commit SHA via connector | NOT SUPPORTED BY TESTED FLOW | local `8cdedb9...` != remote `5d04c16...` |
| automatic quota-pressure snapshot selector | NOT VERIFIED | only cleanup ordering/design is defined |
| Library itself acts as a native Git working tree | NOT VERIFIED / NOT OBSERVED | Git runs only after materialization/extraction |
| Library acts as Git remote / automatic sync | NOT VERIFIED / NOT OBSERVED | synchronization is explicit |
| automatic merge/reconciliation after conflict | NOT VERIFIED | only conflict detection was tested |
| exact arbitrary Git-object reconstruction preserving commit identity | NOT VERIFIED | equivalent connector commit had different SHA |
| large repository snapshot behavior near 512 MB | NOT VERIFIED | tested repositories were very small |

## Synchronization and lifecycle semantics

Strongest supported architecture:

```text
GitHub canonical remote
        |
        | explicit connector read
        v
workspace / local Git
        |
        | optional packaged checkpoint
        v
ChatGPT Library
        |
        | materialize / restore in same or later chat
        v
workspace / local Git
        |
        | explicit connector write using fresh remote preconditions
        v
GitHub canonical remote
        |
        | positive merge / target-state evidence
        v
validated target Library snapshot
        |
        | only after promotion verification
        v
retire redundant merged/superseded Library snapshot
```

Consequences:

- Library is not `origin`;
- Library versions are not Git commits;
- a `.tar.gz` snapshot can preserve actual Git history because it contains the real `.git` bytes;
- GitHub does not change merely because Library changes;
- connector-created commits can differ in SHA from local equivalents;
- Git tree SHA is a useful exact state comparator when commit identities intentionally differ;
- stale-base detection is possible with base blob SHA preconditions;
- canonical acceptance requires GitHub read-back;
- destructive Library cleanup should require positive integration evidence plus validated replacement state;
- `closed` is not equivalent to `merged`;
- failed candidate validation must preserve current state.

## Transient failure evidence

A prior session observed Library mutation operations unavailable/disabled before execution. The failure reproduced for both `app.py` and a minimal `hello.txt`.

Later sessions successfully exercised:

- folder creation;
- upload;
- listing/search;
- materialization;
- overwrite/versioning;
- rename;
- deletion to Trash;
- cross-chat retrieval;
- re-upload from another chat.

Therefore the earlier failure is historical runtime/session/tool-routing evidence, not proof that Library mutation is unsupported as a product capability.

Supported statement:

```text
A Library capability may be unavailable in a particular runtime/session even though the product and other sessions support it.
```

## Durable conclusions versus volatile facts

### Durable analytical conclusions from the experiments

- local Git state, Library persistence, and GitHub canonical state are distinct layers;
- Library can persist individual working files and packaged full Git repositories;
- a packaged `.git` repository can survive a real chat boundary and continue its Git history;
- Library changes do not automatically mutate GitHub;
- multi-file remote reconstruction can be emitted as one GitHub commit;
- stale remote writes can be rejected using base blob SHA preconditions;
- connector reconstruction does not automatically preserve local commit identity;
- exact Git tree equality can verify content state even when commit SHAs differ;
- merged-branch Library snapshots can be retired safely after positive merge evidence and a replacement target snapshot is round-trip validated/promoted;
- closed-unmerged work is not cleanup-eligible under the tested fail-closed rule;
- an invalid candidate can fail without displacing the validated current snapshot;
- GitHub remains the canonical remote authority in the tested maintenance pattern.

### Volatile runtime/vendor facts

Revalidate before future operational reliance:

- whether the temporary workspace currently has Git installed;
- whether that runtime can resolve/reach `github.com` directly;
- which GitHub write/ref/tree/merge operations the connector currently exposes;
- which Library mutation/materialization/version/rename/delete operations are currently exposed;
- Library storage quotas and per-file limits;
- Library retention/deletion/Trash behavior;
- internal Library file/version identifiers and their visibility timing.

## Remaining limitations and non-findings

R014 still does **not** establish that:

- Library exposes a packaged or unpackaged `.git` repository as a directly mounted Git working tree without materialization;
- Library itself can execute Git commands;
- Library is a Git remote or automatically synchronizes with GitHub;
- an arbitrary local Git commit can be reconstructed remotely with exactly the same SHA through the currently tested connector flow;
- merge/conflict resolution can be automated safely after a detected `409`;
- large multi-file updates are transactionally atomic under every failure mode;
- repository snapshots approaching the documented `512 MB` limit are practical or performant;
- the workspace's own local filesystem survives arbitrary chat/runtime turnover without Library persistence;
- an automatic quota-pressure selector is safe before that selector is separately qualified;
- this composed workflow or GC mechanism is adopted Agent Governance policy.

## Lifecycle and garbage-collection design

The detailed non-normative lifecycle mechanism and empirical qualification receipts are in:

`docs/research/CHATGPT-GIT-WORKSPACE-LIBRARY-SNAPSHOT-LIFECYCLE-APPENDIX.md`

Core rules:

```text
steady state = validated main + develop (when used) + active branches
merged branch = cleanup-eligible only after merged == true and verified target snapshot refresh/promotion
closed-unmerged / missing-branch / ambiguous state = retain fail-closed
canonical refresh = create + round-trip verify + promote + reverify before deleting old
invalid candidate = preserve current
quota pressure = retire proven-redundant state first; selector still unqualified
```

The core lifecycle is now empirically qualified for the tested cases. It remains non-normative.

## Implications for Agent Governance

This remains diagnostic capability research. It does not modify execution-adapter ownership, branching policy, source-maintenance workflow, or the rule that GitHub is canonical authority.

The evidence supports Library as a persistent checkpoint/snapshot layer between ChatGPT sessions and now also supports a concrete fail-closed lifecycle for redundant branch snapshots. It does not create a requirement to use or automate that mechanism.

`Research-State: COMPLETE` and `Decision-State: NOT_REQUIRED` remain appropriate.

If Agent Governance later standardizes the mechanism, a separate normative Specify/Design/Plan path should define at least:

- when to use file-level Library persistence versus full Git snapshots;
- snapshot naming/retention/cleanup rules;
- quota threshold and automatic cleanup selector;
- maximum accepted snapshot size;
- remote-base freshness checks before GitHub writes;
- conflict/reconciliation behavior;
- cleanup receipts/audit location;
- branch-name encoding;
- authority for destructive Library operations;
- whether exact Git-object identity is required or content-equivalent connector commits are acceptable.

## Evidence provenance

### Workspace/GitHub experiment

- repository: `ManuelBouza/agent-governance`;
- baseline `develop`: `20ed0e64dd6c98f38be42cd3cc28fcc220d06c5e`;
- original `.gitignore` blob: `d90d927a47936445fc975791ebedae651450cfd7`;
- temporary branch: `test/chatgpt-git-workflow`;
- experimental remote commit: `c4a2c43a65554ed9c52a4047f954373935b06a07`.

### `test_biblioteca` Library/GitHub round trip

- initial `app.py`: `print("Hello World")`;
- initial blob: `ad35e5ae34d7df6d469bfe65dbfcefe988e0169f`;
- Library path: `/test_biblioteca_flow/app.py`;
- first remote round-trip commit: `d82750a45f43f45a16c498674391a7a7e15dc319`;
- first resulting blob: `45eac8ae8769283e63eec44d199100e7dfb6def2`;
- later Library versions observed: `2`, `3`, `4`;
- final remote commit: `af02345fcfed0ebe7d4b6503af7e89cdf48b84cf`;
- final blob: `830b8d6471d5f1e09e0f13a0982b5849cd61f4b6`.

### Full Git snapshot / capability matrix

- branch: `test/library-git-capability-matrix`;
- baseline local reconstructed HEAD: `55f8e089179c5bc6a93d2d56385fb9d18203d6a8`;
- source snapshot path: `/test_biblioteca_git_capability/test_biblioteca_git_snapshot.tar.gz`;
- source snapshot `file_id`: `file_000000007794822fa2612ecab1f4dd4f`;
- source snapshot SHA-256: `ee2cb5dbd3e7817315b17bd3931f89c1bbd2dee71cbc6c6504fc267baad4ff39`;
- local multi-file commit: `8cdedb9753126fa17a435756b3702c3a271af135`;
- remote multi-file commit: `5d04c16e5705e308457072792e4f3c5204768864`;
- concurrent remote commit: `dafe8a821e09a09a6200e4c5afed447fcf03320e`;
- stale blob: `9c7b101b815b6fc95672224de719e90ac0354e4a`;
- concurrent blob: `1d4eade294f9d741e9bdf5087db38f607311d6ec`;
- stale write: HTTP `409`.

### Cross-chat snapshot experiment

- Chat B source HEAD: `55f8e089179c5bc6a93d2d56385fb9d18203d6a8`;
- Chat B new local commit: `1a9bf18114de99fe385b8222c9c57c0b19de020a`;
- commit message: `Test cross-chat Library Git persistence`;
- created file: `cross_chat_test.txt`;
- new snapshot path: `/test_biblioteca_git_capability/test_biblioteca_git_snapshot_cross_chat.tar.gz`;
- new snapshot `file_id`: `file_00000000ae8c822fa55d081b693f2dcc`;
- new snapshot `library_file_id`: `libfile_00e7453c5a3c8191b8a42f657020fd62`;
- new snapshot size: `12052` bytes;
- new snapshot SHA-256: `2ae7113c674f9caa29054833650f10c0904dba7f0ac51ef92ab885740ef0dbf4`;
- Chat A independent verification: same SHA-256, `HEAD = 1a9bf18114de99fe385b8222c9c57c0b19de020a`, `git fsck` pass, expected file/commit present.

### Lifecycle / GC qualification

- test repository: `ManuelBouza/test_biblioteca`;
- target: `test/library-gc-target-20260905`;
- merged feature: `test/library-gc-merged-20260905`;
- closed-unmerged feature: `test/library-gc-unmerged-20260905`;
- positive feature HEAD: `799a4976a438ee70bde9b9634e7ad51d483b90e7`;
- positive feature tree: `fab3804804953725837aa6470a65c4f82600b9ed`;
- PR `#1` merge commit: `40315fe606b906b9c4abc075eb636328c77e1f6c`;
- post-merge target tree: `718b6d6c83d40d3f389b3430c190aacafb21727a`;
- promoted target Library snapshot SHA-256: `2dbca71e3006230b696ce6392e5d8ca3739d3e3a20eccba86ec14f9d3354afb0`;
- promoted target file ID: `file_0000000090e4822fbaf957ff5981adb6`;
- merged feature snapshot deleted after target validation: `file_000000000350822f9143fd905775af6d`;
- negative feature HEAD: `18e4c045677e1a9824fb02c12dac1ff927ec8f00`;
- negative tree: `d110de0171073576023005293d1a56f92b1f305f`;
- negative retained snapshot SHA-256: `6359e5edef0204555243631cecff77689952419b4f339e8dade27299aba6eed5`;
- PR `#2`: closed / `merged=false`;
- invalid candidate SHA-256: `a47fca924ebd2cc5e1f0fc8a555cd8ab09d505e81421263d9914983b4ba6ffd8`;
- invalid candidate validation: tar exit `2`; current snapshot unchanged.

### Official OpenAI documentation checked 2026-09-05

- File storage and Library in ChatGPT: https://help.openai.com/en/articles/20001052-file-storage-and-library-in-chatgpt
- Chat and File Retention Policies in ChatGPT: https://help.openai.com/en/articles/8983778-how-are-files-vs-chats-retained

Vendor documentation is time-sensitive evidence and must be refreshed before future policy adoption.
