# ChatGPT Git workspace, Library persistence, and GitHub transport research

Research-ID: R014  
Research-State: COMPLETE  
Decision-State: NOT_REQUIRED  
Opened: 2026-09-05  
Last-Reviewed: 2026-09-05  
Owner: ChatGPT Orchestrator  
Scope: ChatGPT temporary-workspace Git behavior, GitHub connector transport, ChatGPT Library persistence/version behavior, cross-chat persistence, storage/retention boundaries, and their composition for source-product maintenance experiments  
Question: Can ChatGPT combine a real local Git repository in the temporary workspace, persistent working-file or repository-snapshot storage in ChatGPT Library, and explicit GitHub connector operations into a reliable Git-oriented maintenance workflow; and which state, transport, retention, and conflict boundaries remain separate?  
Evaluation-Refs: empirical workspace/GitHub experiment against `ManuelBouza/agent-governance` at `develop` `20ed0e64dd6c98f38be42cd3cc28fcc220d06c5e`, temporary branch `test/chatgpt-git-workflow`, remote test commit `c4a2c43a65554ed9c52a4047f954373935b06a07`; empirical Library/GitHub experiments against `ManuelBouza/test_biblioteca`, commits `d82750a45f43f45a16c498674391a7a7e15dc319`, `af02345fcfed0ebe7d4b6503af7e89cdf48b84cf`, `5d04c16e5705e308457072792e4f3c5204768864`, and `dafe8a821e09a09a6200e4c5afed447fcf03320e`; cross-chat Library snapshot round trip verified 2026-09-05  
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

The validated composition now includes all of the following:

- real local Git semantics in the temporary workspace;
- explicit GitHub connector reads/writes while direct CLI GitHub transport was unavailable in the tested runtime;
- GitHub -> Library -> modification -> GitHub round-trip synchronization;
- multiple Library working-file versions before one final GitHub update;
- a packaged complete repository including `.git` persisted in Library and restored as a valid Git repository;
- a two-chat persistence round trip in which Chat B restored the Git snapshot, created a new local commit, uploaded a second snapshot, and Chat A independently recovered and verified that new commit;
- multi-file reconstruction into one remote GitHub commit;
- stale-base conflict detection through GitHub blob-SHA preconditions and HTTP 409;
- empirical non-preservation of local commit SHA identity when equivalent content is reconstructed through the GitHub connector.

The result is a usable persistence/transport pattern, not a native Git remote hosted by Library. GitHub remains canonical remote authority. Library is a persistent storage layer, and Git semantics execute only after files or repository snapshots are materialized into an executable workspace.

## Capability model

The investigation separates six concerns:

1. **Local Git semantics** — a temporary workspace can host a real `.git` repository and run ordinary Git commands.
2. **Direct Git CLI transport** — the local Git process may or may not have network/DNS access to GitHub in a given runtime.
3. **Connected GitHub transport** — the GitHub connector/API surface can read and mutate canonical remote state independently of local CLI networking.
4. **Library persistence** — Library can retain files independently from the originating chat and make them reusable later.
5. **Repository snapshot persistence** — a packaged repository including `.git` can be stored in Library, materialized later, extracted, and resumed with Git history intact.
6. **Synchronization/conflict control** — local/Library state is not automatically synchronized; remote writes must be explicit and can use remote SHA preconditions to detect stale state.

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

This is a runtime observation, not a universal product limitation. DNS/network availability is volatile and must be revalidated per runtime.

### A3 — explicit GitHub connector transport succeeded

The connected GitHub surface independently succeeded at remote repository operations including:

- reading canonical branches/files;
- creating a temporary branch;
- writing file content;
- creating remote commits;
- comparing remote refs;
- re-reading remote state after mutation.

The original experiment produced remote commit:

`c4a2c43a65554ed9c52a4047f954373935b06a07`

and verified the temporary branch as one commit ahead with only `.gitignore` changed by two additions. The branch ref was then reset to its baseline.

### A4 — local and remote commit identity are separate

A local Git commit is not automatically the GitHub commit created later by connected transport. Content/tree reconstruction through the connector can produce a different commit object and SHA.

This was later demonstrated explicitly in Experiment C.

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

The GitHub file was read, copied into the temporary workspace, and uploaded to Library. Folder creation and file upload succeeded. The Library file was then rediscovered and read successfully.

One transient detail was observed: an immediate direct read using the just-returned file ID was initially rejected as not currently visible. Rediscovering the file through Library listing made it readable. This was a reference-visibility/routing issue, not a failed upload.

### B2 — Library materialization, modification, overwrite, and verification

The Library copy was materialized into the executable workspace, changed to:

```python
print("Hello from ChatGPT Library")
```

and uploaded back with overwrite semantics. A later Library read verified the modified content.

### B3 — explicit write-back to GitHub

Before the remote write, GitHub was re-read and still contained the original content/blob. The verified Library-derived content was then written through the GitHub connector.

GitHub returned:

```text
commit SHA: d82750a45f43f45a16c498674391a7a7e15dc319
content/blob SHA: 45eac8ae8769283e63eec44d199100e7dfb6def2
```

A subsequent GitHub read confirmed:

```python
print("Hello from ChatGPT Library")
```

This completed the end-to-end path:

```text
GitHub read
-> Library persist
-> Library materialize/modify/overwrite/read
-> GitHub update
-> GitHub read-back verification
```

### B4 — multiple Library states before one remote update

A second experiment performed multiple successive Library overwrites while GitHub remained unchanged.

Observed Library progression:

```text
version 2 -> print("Library change 1")
version 3 -> distinct intermediate overwrite/version state
version 4 -> print("Library final change")
```

Immediately before the final GitHub write, the remote was still:

```text
content: print("Hello from ChatGPT Library")
blob SHA: 45eac8ae8769283e63eec44d199100e7dfb6def2
```

Only after the final Library state was selected and verified was GitHub updated once:

```text
commit SHA: af02345fcfed0ebe7d4b6503af7e89cdf48b84cf
commit message: Apply accumulated Library changes
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

```text
HEAD: 55f8e089179c5bc6a93d2d56385fb9d18203d6a8
```

### C1 — complete `.git` snapshot can be persisted in Library

The complete repository, including `.git`, was packaged as:

`test_biblioteca_git_snapshot.tar.gz`

and stored at:

`/test_biblioteca_git_capability/test_biblioteca_git_snapshot.tar.gz`

Verified Library metadata:

```text
file_id: file_000000007794822fa2612ecab1f4dd4f
size: 11158 bytes
SHA-256: ee2cb5dbd3e7817315b17bd3931f89c1bbd2dee71cbc6c6504fc267baad4ff39
```

After Library materialization and extraction into a new directory:

```text
git rev-parse HEAD -> 55f8e089179c5bc6a93d2d56385fb9d18203d6a8
git fsck --full    -> exit 0 / no findings
git status --short -> clean
```

This proves binary preservation of a packaged full Git repository including `.git`.

It does **not** prove that Library exposes `.git` natively as a directly executable repository without materialization/extraction.

### C2 — multi-file reconstruction in one GitHub commit

Three file changes were prepared:

- `app.py` -> `print("Library multi-file test")`
- `multi_a.txt` -> `multi-file A from Library`
- `multi_b.txt` -> `multi-file B from Library`

The remote GitHub tree was created as one tree and one commit:

```text
remote commit: 5d04c16e5705e308457072792e4f3c5204768864
message: Test multi-file Library synchronization
parent: af02345fcfed0ebe7d4b6503af7e89cdf48b84cf
```

GitHub reported exactly the three expected changed files. Thus multi-file reconstruction in one remote commit is empirically supported.

This does not yet qualify failure atomicity for arbitrarily large trees or every connector failure mode.

### C3 — connector reconstruction does not automatically preserve local commit SHA

The equivalent local Git commit was:

`8cdedb9753126fa17a435756b3702c3a271af135`

The remote connector-created commit was:

`5d04c16e5705e308457072792e4f3c5204768864`

The SHAs differ. Therefore equivalent file content transported through the tested connector workflow does not automatically preserve local Git commit identity.

This does not rule out deliberately reconstructing exact Git objects if every commit field/tree/parent identity is reproduced; that exact-object path was not tested.

### C4 — stale-base conflict detection

On the isolated branch, `app.py` initially had:

```text
content: print("Library multi-file test")
blob SHA: 9c7b101b815b6fc95672224de719e90ac0354e4a
```

A concurrent remote change then advanced the branch to:

```text
commit: dafe8a821e09a09a6200e4c5afed447fcf03320e
message: Simulate concurrent remote change
content: print("Concurrent remote change")
new blob SHA: 1d4eade294f9d741e9bdf5087db38f607311d6ec
```

An attempted write using the stale prior blob SHA was rejected by GitHub with HTTP `409`.

Therefore a safe adapter can detect stale remote state when it carries forward and supplies the exact base blob SHA. The test qualifies stale-write detection, not automatic merge/reconciliation.

## Experiment D — cross-chat Library persistence of complete Git history

### Objective

Test actual persistence between separate chats rather than merely restoring the archive twice inside one runtime.

The sequence was:

```text
Chat A
  full Git repo + .git
  -> Library source snapshot

Chat B
  find source snapshot in Library
  -> materialize/extract
  -> verify Git
  -> create new local commit
  -> package complete repo + .git
  -> upload new snapshot to Library

Chat A
  find new snapshot in Library
  -> materialize/extract
  -> verify the new Git commit and file
```

### D1 — Chat B recovered the source snapshot

Source Library object:

```text
path: /test_biblioteca_git_capability/test_biblioteca_git_snapshot.tar.gz
file_id: file_000000007794822fa2612ecab1f4dd4f
size: 11158 bytes
SHA-256: ee2cb5dbd3e7817315b17bd3931f89c1bbd2dee71cbc6c6504fc267baad4ff39
```

Chat B restored a normal `.git` directory and verified:

```text
GIT_WORKTREE_VALID: true
HEAD_BEFORE: 55f8e089179c5bc6a93d2d56385fb9d18203d6a8
git fsck --full: PASS
```

### D2 — Chat B created a new local commit

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

The working tree was clean after the commit.

### D3 — Chat B persisted a second full Git snapshot

New archive:

`test_biblioteca_git_snapshot_cross_chat.tar.gz`

New Library object:

```text
path: /test_biblioteca_git_capability/test_biblioteca_git_snapshot_cross_chat.tar.gz
file_id: file_00000000ae8c822fa55d081b693f2dcc
library_file_id: libfile_00e7453c5a3c8191b8a42f657020fd62
size: 12052 bytes
SHA-256: 2ae7113c674f9caa29054833650f10c0904dba7f0ac51ef92ab885740ef0dbf4
```

Chat B re-materialized that upload and confirmed the same byte-level SHA-256.

### D4 — Chat A independently recovered Chat B's new snapshot

Back in the original chat, the new Library path and `file_id` were independently rediscovered. The file was materialized and rechecked:

```text
size: 12052 bytes
SHA-256: 2ae7113c674f9caa29054833650f10c0904dba7f0ac51ef92ab885740ef0dbf4
git rev-parse --is-inside-work-tree: true
HEAD: 1a9bf18114de99fe385b8222c9c57c0b19de020a
git fsck --full: PASS
```

The restored repository contained:

```text
cross_chat_test.txt -> Cross-chat Library persistence test
latest commit message -> Test cross-chat Library Git persistence
```

This is direct empirical evidence that a complete packaged Git repository can persist through Library across separate chats, be advanced by local Git in the second chat, and be recovered with the new history intact in the first chat.

The verified mechanism is **snapshot persistence**, not a persistent mounted working tree. The executable Git repository still has to be materialized/extracted into the current workspace.

## Official ChatGPT Library product limits and retention

The following are vendor-documented product facts, checked against official OpenAI Help Center documentation on 2026-09-05. They are time-sensitive and must be revalidated before future operational or normative reliance.

Primary source:

https://help.openai.com/en/articles/20001052-file-storage-and-library-in-chatgpt

Retention source:

https://help.openai.com/en/articles/8983778-how-are-files-vs-chats-retained

### Storage quotas

Current official documentation states:

```text
Free:      500 MB
Go:          4 GB
Plus:       20 GB
Business:   20 GB
Pro:       100 GB
```

For the tested Plus context, the documented Library quota is therefore `20 GB`.

### Per-file limits

Current official documentation states:

- maximum uploaded file size: `512 MB`;
- text/document files: `2 million tokens` per file;
- CSV/spreadsheets: approximately `50 MB`, depending on row size;
- images: `20 MB` each.

For packaged Git repository snapshots such as `.tar.gz`, the most relevant documented file-size boundary is the `512 MB` maximum upload size. This investigation did not test behavior near that maximum.

### Library storage is separate from daily attachment/chat limits

Official documentation states that Library storage is separate from daily attachment/chat limits.

This means the persistent Library quota and ordinary per-day attachment/chat allowances are separate controls.

### Files persist independently from the originating chat

Official documentation states that uploaded/created files saved to Library can be found and reused later. It also states that chats and Library files are managed separately: deleting a chat does not delete files saved to Library.

The cross-chat experiment above independently confirms that behavior for the tested repository snapshots.

### No documented automatic oldest-file eviction at quota

Official documentation states that files are saved to the account until the user deletes them manually. It also documents a Library storage view that reports total usage, remaining storage, and whether the account is over its limit.

No automatic oldest-first or quota-triggered eviction policy is documented in the reviewed official material. Therefore the supported conclusion is:

```text
Library files are documented as retained until manual deletion;
no automatic eviction mechanism was established by the reviewed documentation or by these experiments.
```

This must not be strengthened into a universal guarantee beyond the current documented product behavior.

### Deletion retention

When a Library file is deleted, official documentation states that it is removed from the main Library view immediately and scheduled for permanent deletion from OpenAI systems within `30 days`, unless legal/security exceptions apply. If `Recently deleted` is available, a file may remain recoverable there until permanent deletion or explicit `Delete forever`.

Enterprise, Edu, and Healthcare workspaces may instead retain Library files according to the workspace retention policy.

### Temporary Chat exception

Official Library documentation states that files uploaded in Temporary Chat are not saved to the account or Library.

Therefore Temporary Chat should not be assumed to provide the persistent snapshot mechanism validated here.

## Confirmed capability matrix

| Capability | Status | Evidence |
| --- | --- | --- |
| local `git status` / `diff` / staging / commit | VERIFIED | Experiment A |
| direct CLI GitHub transport in tested runtime | UNAVAILABLE | DNS failure reproduced |
| GitHub connector read/write/verify | VERIFIED | Experiments A-C |
| Library working-file persistence/versioning | VERIFIED | Experiment B |
| accumulate multiple Library states before one GitHub write | VERIFIED | Experiment B4 |
| full repository snapshot including `.git` stored/restored | VERIFIED | Experiment C1 |
| full Git snapshot survives separate chats | VERIFIED | Experiment D |
| advance restored Git repo with a new local commit in another chat | VERIFIED | Experiment D2 |
| recover that new commit back in the original chat | VERIFIED | Experiment D4 |
| multi-file remote reconstruction in one commit | VERIFIED | Experiment C2 |
| stale remote state detected with blob SHA precondition | VERIFIED | Experiment C4 / HTTP 409 |
| automatic preservation of local commit SHA via connector | NOT SUPPORTED BY TESTED FLOW | local `8cdedb9...` != remote `5d04c16...` |
| Library itself acts as a native Git working tree | NOT VERIFIED / NOT OBSERVED | Git runs only after materialization/extraction |
| Library acts as Git remote / automatic sync | NOT VERIFIED / NOT OBSERVED | all synchronization was explicit |
| automatic merge/reconciliation after conflict | NOT VERIFIED | only conflict detection was tested |
| exact arbitrary Git-object reconstruction preserving commit identity | NOT VERIFIED | connector-created equivalent commit had a different SHA |
| large repository snapshot behavior near 512 MB | NOT VERIFIED | tested snapshots were ~11-12 KB |

## Synchronization semantics

The strongest supported architecture is:

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
```

Important consequences:

- Library is not `origin`;
- Library versions are not Git commits;
- a `.tar.gz` Library snapshot can preserve actual Git commit history because it contains the real `.git` bytes;
- GitHub does not change merely because Library changes;
- the connector-created remote commit may differ in SHA from a local equivalent commit;
- stale-base detection is possible if the adapter preserves the original GitHub blob SHA and supplies it on update;
- canonical acceptance still requires re-reading GitHub after writes.

## Transient failure evidence

A prior session observed Library mutation operations becoming unavailable/disabled at runtime before execution. The failure reproduced for both `app.py` and a minimal `hello.txt`.

Later sessions successfully exercised:

- folder creation;
- upload;
- listing/search;
- materialization;
- overwrite/versioning;
- cross-chat retrieval;
- re-upload from another chat.

Therefore the earlier failure is historical evidence of runtime/session/tool-routing unavailability, not proof that Library mutation is unsupported as a product capability.

The supported statement is:

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
- GitHub remains the canonical remote authority in the tested maintenance pattern.

### Volatile runtime/vendor facts

Revalidate before future operational reliance:

- whether the temporary workspace currently has Git installed;
- whether that runtime can resolve/reach `github.com` directly;
- which GitHub write/ref/tree operations the connector currently exposes;
- which Library mutation/materialization/version operations are currently exposed;
- Library storage quotas and per-file limits;
- Library retention/deletion behavior;
- internal Library file/version identifiers and their visibility timing.

## Remaining limitations and non-findings

This research still does **not** establish that:

- Library exposes a packaged or unpackaged `.git` repository as a directly mounted Git working tree without materialization;
- Library itself can execute `git status`, `git diff`, staging, commit, branch, merge, rebase, or push operations;
- Library is a Git remote or automatically synchronizes with GitHub;
- an arbitrary local Git commit can be reconstructed remotely with exactly the same SHA through the currently tested connector flow;
- merge/conflict resolution can be automated safely after a detected 409;
- large multi-file updates are transactionally atomic under every failure mode;
- repository snapshots approaching the documented 512 MB file limit are practical or performant;
- the workspace's own local filesystem survives arbitrary chat/runtime turnover without Library persistence;
- this composed workflow is adopted Agent Governance policy.

## Implications for Agent Governance

This remains diagnostic capability research. It does not modify D054 execution-adapter ownership, branching policy, source-maintenance workflow, or the rule that GitHub is canonical authority.

The expanded evidence strengthens the feasibility case for Library as a persistent checkpoint/snapshot layer between ChatGPT sessions. It still does not create a normative requirement to use that mechanism.

`Research-State: COMPLETE` and `Decision-State: NOT_REQUIRED` remain appropriate.

If Agent Governance later standardizes this mechanism, a separate normative Specify/Design/Plan path should define at least:

- when to use file-level Library persistence versus full Git snapshots;
- snapshot naming/retention/cleanup rules;
- maximum accepted snapshot size and quota management;
- remote-base freshness checks before GitHub writes;
- conflict/reconciliation behavior;
- cleanup of test branches and Library checkpoints;
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
- source snapshot Library path: `/test_biblioteca_git_capability/test_biblioteca_git_snapshot.tar.gz`;
- source snapshot `file_id`: `file_000000007794822fa2612ecab1f4dd4f`;
- source snapshot SHA-256: `ee2cb5dbd3e7817315b17bd3931f89c1bbd2dee71cbc6c6504fc267baad4ff39`;
- local multi-file commit: `8cdedb9753126fa17a435756b3702c3a271af135`;
- remote multi-file commit: `5d04c16e5705e308457072792e4f3c5204768864`;
- concurrent remote commit: `dafe8a821e09a09a6200e4c5afed447fcf03320e`;
- stale blob: `9c7b101b815b6fc95672224de719e90ac0354e4a`;
- concurrent blob: `1d4eade294f9d741e9bdf5087db38f607311d6ec`;
- stale write result: HTTP `409`.

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
- Chat A independent re-verification: same SHA-256, `HEAD = 1a9bf18114de99fe385b8222c9c57c0b19de020a`, `git fsck --full` pass, expected file/commit message present.

### Official OpenAI documentation checked 2026-09-05

- File storage and Library in ChatGPT: https://help.openai.com/en/articles/20001052-file-storage-and-library-in-chatgpt
- Chat and File Retention Policies in ChatGPT: https://help.openai.com/en/articles/8983778-how-are-files-vs-chats-retained

Vendor documentation is time-sensitive evidence and must be refreshed before future policy adoption.
