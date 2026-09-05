# ChatGPT Git workspace, Library persistence, and GitHub transport research

Research-ID: R014  
Research-State: COMPLETE  
Decision-State: NOT_REQUIRED  
Opened: 2026-09-05  
Last-Reviewed: 2026-09-05  
Owner: ChatGPT Orchestrator  
Scope: ChatGPT temporary-workspace Git behavior, GitHub connector transport, ChatGPT Library persistence/version behavior, and their boundaries for source-product maintenance experiments  
Question: Can ChatGPT reproduce a VS Code/Codex-like Git working-copy workflow by combining a real local Git repository in the temporary chat workspace, persistent working-file storage in ChatGPT Library, and explicit GitHub connector operations; and which state/transport boundaries remain separate?  
Evaluation-Refs: empirical workspace/GitHub experiment against `ManuelBouza/agent-governance` at `develop` `20ed0e64dd6c98f38be42cd3cc28fcc220d06c5e`, temporary branch `test/chatgpt-git-workflow`, remote test commit `c4a2c43a65554ed9c52a4047f954373935b06a07`; empirical Library/GitHub round-trip experiments against `ManuelBouza/test_biblioteca`, GitHub commits `d82750a45f43f45a16c498674391a7a7e15dc319` and `af02345fcfed0ebe7d4b6503af7e89cdf48b84cf`  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Summary

The experiments support three separate capability layers that can be composed but must not be conflated:

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
        | explicit file materialization / persistence operations
        v
ChatGPT Library
  - persistent file storage/version surface
  - not a Git repository or Git remote
```

The original workspace experiment established real local Git semantics and successful GitHub connector transport while direct Git CLI network transport to `github.com` failed in that runtime because DNS resolution was unavailable.

A later controlled experiment against `ManuelBouza/test_biblioteca` additionally validated the previously unproven end-to-end path:

```text
GitHub -> Library -> modify/persist -> materialize/read -> GitHub -> remote verification
```

The Library path was not an automatic synchronization channel and no Git operations were executed *inside* Library. Remote mutation occurred through the connected GitHub surface. GitHub remained canonical throughout.

## Research question decomposition

The investigation separates capabilities that are easy to conflate:

1. **Local Git semantics** — whether the temporary execution workspace can contain a real `.git` repository and execute ordinary Git commands.
2. **Direct Git CLI transport** — whether that local Git process can directly fetch/push GitHub from the runtime network.
3. **Connected GitHub transport** — whether ChatGPT can read and mutate GitHub through its connected GitHub/API surface independently of local CLI networking.
4. **Library persistence** — whether ChatGPT Library can persist working files and versions across explicit operations.
5. **Library/Git synchronization** — whether Library itself behaves as a Git working tree/remote or automatically synchronizes with GitHub.
6. **Composed end-to-end workflow** — whether GitHub content can be moved through Library, modified, recovered, and explicitly written back to GitHub with remote verification.

## Experiment A — temporary workspace Git + GitHub connector

### Setup

Repository:

`ManuelBouza/agent-governance`

Canonical baseline during the experiment:

`develop = 20ed0e64dd6c98f38be42cd3cc28fcc220d06c5e`

Temporary remote branch:

`test/chatgpt-git-workflow`

Test file:

`.gitignore`

Original blob observed from `develop`:

`d90d927a47936445fc975791ebedae651450cfd7`

A harmless two-line test modification was used so the remote comparison could be verified without changing `develop`.

### A1 — real local Git state was available

A repository initialized in the temporary ChatGPT execution workspace behaved as a normal Git working tree. The following operations succeeded locally:

- repository initialization;
- `git status`;
- `git diff`;
- `git add`;
- local `git commit`;
- ordinary file edits between commits.

This is actual local Git state, not Library metadata. When the runtime provides Git and an executable filesystem, `.git` can track staged/unstaged state and local commits in that temporary workspace.

### A2 — direct Git CLI transport to GitHub was unavailable in that runtime

Direct network checks from the local Git working tree failed when attempting GitHub transport. The observed failure was:

```text
Could not resolve host: github.com
```

Therefore this experiment did **not** establish a supported path of:

```text
local .git -> git fetch/pull/push -> github.com
```

This is a dated runtime observation, not a universal product limitation. Network/DNS availability must be revalidated in any future runtime before assuming CLI transport is available or unavailable.

### A3 — explicit GitHub connector transport succeeded

The connected GitHub surface successfully performed remote repository operations independently of local Git CLI networking:

- read current `develop`;
- create temporary branch `test/chatgpt-git-workflow`;
- read `.gitignore` from the canonical branch and the test branch;
- write the experimental `.gitignore` change to the test branch;
- create remote commit `c4a2c43a65554ed9c52a4047f954373935b06a07`;
- compare `develop` against the test branch.

The remote comparison reported:

```text
status: ahead
ahead_by: 1
behind_by: 0
changed file: .gitignore
additions: 2
deletions: 0
```

The test branch was then moved back to the original `develop` commit, leaving no content divergence from that baseline. The temporary branch itself remained because branch deletion was not exposed by the connected action set used in that turn.

### A4 — local and remote commits are separate unless explicitly reconstructed/synchronized

A local `git commit` in the temporary workspace does not automatically become the commit created later through the GitHub connector. Synchronization must be explicit at file/tree/content/ref level. GitHub then creates or advances canonical remote history through the connected operation.

Local commit SHAs are therefore temporary-workspace evidence unless the exact Git objects are deliberately reconstructed remotely.

## Experiment B — GitHub -> Library -> modification -> GitHub round trip

### Setup

Repository:

`ManuelBouza/test_biblioteca`

Branch:

`main`

Test file:

`app.py`

Before the first Library round trip, GitHub returned:

```text
content: print("Hello World")
blob SHA: ad35e5ae34d7df6d469bfe65dbfcefe988e0169f
```

The Library working location used by the successful experiment was:

`/test_biblioteca_flow/app.py`

### B1 — GitHub content could be persisted in Library

The experiment read `app.py` through the GitHub connection and persisted a corresponding working copy in ChatGPT Library. Library folder creation and file upload succeeded.

The resulting Library object was subsequently discoverable/readable through the Library surface at the path above.

### B2 — Library copy could be materialized, modified, overwritten, and re-read

The Library copy was materialized into the temporary executable workspace, modified, and uploaded back with overwrite semantics. A later Library read verified the persisted content:

```python
print("Hello from ChatGPT Library")
```

The Library state exposed version metadata; after this overwrite the observed version was `1`.

This demonstrates persistent working-file/version behavior. It does **not** demonstrate that Library contains `.git`, can run Git commands, or automatically stages/commits changes.

### B3 — the Library-derived content could be written to GitHub and verified remotely

Immediately before remote mutation, GitHub was re-read and still contained:

```text
content: print("Hello World")
blob SHA: ad35e5ae34d7df6d469bfe65dbfcefe988e0169f
```

The verified Library-derived content was then used for a GitHub file update. GitHub returned:

```text
commit SHA: d82750a45f43f45a16c498674391a7a7e15dc319
content/blob SHA: 45eac8ae8769283e63eec44d199100e7dfb6def2
```

A subsequent GitHub read verified the remote final content exactly:

```python
print("Hello from ChatGPT Library")
```

This completed the previously missing end-to-end qualification:

```text
GitHub read
-> Library persist
-> materialize/modify
-> Library overwrite/read verification
-> GitHub update
-> GitHub read-back verification
```

### B4 — multiple Library changes could accumulate before one remote GitHub update

A second experiment started from the Library copy corresponding to the GitHub state above and performed several Library overwrites before any new GitHub mutation.

Observed Library progression:

```text
version 2 -> print("Library change 1")
version 3 -> second persisted intermediate state
version 4 -> print("Library final change")
```

The version-3 transition itself was observed as a distinct Library version; the experiment did not preserve a separately quoted content receipt for that intermediate version in the research evidence, so no content is asserted here for version 3 beyond the fact that it was a distinct overwrite/version state.

Before the final GitHub update, GitHub was explicitly re-read and still contained:

```text
content: print("Hello from ChatGPT Library")
blob SHA: 45eac8ae8769283e63eec44d199100e7dfb6def2
```

Thus the intermediate Library writes had not automatically affected the remote repository.

Only after the final Library state was verified was GitHub updated once. The resulting remote commit was:

```text
commit SHA: af02345fcfed0ebe7d4b6503af7e89cdf48b84cf
commit message: Apply accumulated Library changes
content/blob SHA: 830b8d6471d5f1e09e0f13a0982b5849cd61f4b6
```

The commit parent was:

`d82750a45f43f45a16c498674391a7a7e15dc319`

The GitHub commit patch was exactly one replacement in `app.py`:

```diff
-print("Hello from ChatGPT Library")
+print("Library final change")
```

A final GitHub read confirmed:

```python
print("Library final change")
```

Therefore several persistent Library versions can be accumulated as working-file states while the GitHub canonical state remains unchanged, followed by one explicit remote update containing only the final selected file content.

This is **not** equivalent to retaining multiple Git commits in Library. The Library versions are Library persistence/version states, not Git commit objects or branches.

## Confirmed capability boundaries

### GitHub connector / GitHub API surface

Empirically verified across the experiments:

- read repository/branch/file state;
- create a branch in the earlier workspace experiment;
- create/update remote file content;
- receive resulting remote commit/blob SHAs;
- compare/inspect remote changes;
- re-read GitHub after mutation to verify canonical final content.

These operations constitute explicit remote transport. They do not imply that every possible Git/GitHub operation is exposed in every session.

### Temporary ChatGPT workspace

Empirically verified in the earlier experiment:

- executable temporary filesystem;
- real local Git semantics when Git is available;
- `git status`, `git diff`, staging and local commits;
- ordinary file modification/materialization work.

Not established as universal:

- persistence of local `.git` state across arbitrary runtime/chat turnover;
- direct GitHub CLI transport;
- stable network/DNS availability.

### ChatGPT Library

Empirically verified in the successful `test_biblioteca` experiment:

- folder creation;
- file upload/persistence;
- discover/read of the persisted file;
- materialization into the temporary workspace;
- overwrite/version update;
- multiple successive persisted versions;
- re-read verification of selected persisted versions.

Previously, separate Library-management testing in the same investigation also exercised rename, move and delete operations. Those file-management capabilities remain distinct from Git semantics.

Not established:

- Library as a native Git repository;
- presence/persistence of `.git` metadata in Library;
- execution of `git status`, `git diff`, staging, commits or branches *inside* Library;
- Library as a Git remote;
- automatic Library <-> GitHub synchronization.

The safe conceptual boundary is:

```text
Library = persistent file/version storage
Workspace = temporary executable filesystem; may host real .git state
GitHub = canonical repository and remote authority
```

## Synchronization semantics

The successful end-to-end experiment demonstrates **composition**, not automatic synchronization.

The data path was explicitly driven by ChatGPT/tool operations:

```text
GitHub connector read
-> explicit Library upload
-> explicit Library materialization/read/write
-> explicit GitHub connector update
-> explicit GitHub verification
```

Library did not behave as `origin`, and no `git push` originated from Library. The final GitHub commit was created by the connected GitHub capability after the desired Library state had been selected and verified.

For source-product maintenance, GitHub remains the canonical state. Library can be used as persistent working-file storage or a checkpoint/cache layer, but it does not replace Git history, branch identity, merge semantics, or canonical remote verification.

## Transient failure evidence

A prior session observed Library mutation operations becoming unavailable/disabled at runtime before the requested operation executed. The failure reproduced for both `app.py` and a minimal `hello.txt`, so that observation did not appear extension-specific.

The later `test_biblioteca` experiment succeeded with Library folder creation, upload, overwrite/versioning, read and materialization and completed the full round trip. Therefore the earlier failure must **not** be promoted to a permanent product limitation.

The supported conclusion is narrower:

```text
Library mutation availability may be runtime/session/tool-routing dependent.
```

A failure in one runtime proves capability unavailability for that session/operation attempt; it does not, by itself, prove that the product does not support the capability.

## Volatile versus durable conclusions

### Durable analytical conclusions

- local Git semantics, Library persistence and remote GitHub transport are separate capability layers;
- Library persistence/version state is not Git canonical state;
- GitHub can remain canonical while Library holds several intermediate working-file versions;
- the GitHub -> Library -> modification -> GitHub round trip is empirically achievable through explicit operations;
- synchronization is explicit, not automatic.

### Volatile runtime/tool facts

The following must be revalidated before operational reliance in a future session:

- whether the current temporary workspace has Git installed/usable;
- whether the runtime can resolve/reach `github.com` directly;
- which GitHub connector write operations are exposed;
- whether Library mutation/materialization/version actions are available in that session;
- exact Library internal file/version identifiers and materialization behavior;
- whether branch deletion or other GitHub operations are exposed by the current connector action set.

## Limitations and non-findings

This research does **not** establish that:

- Library can preserve a full Git repository including `.git` and later resume it as such;
- Library versions are equivalent to commits, branches, tags or reflog entries;
- local Git state survives arbitrary ChatGPT runtime turnover;
- `git push` from the temporary workspace is generally available;
- local commit SHA identity can be preserved automatically when writing through the GitHub connector;
- the connector exposes every Git operation in every session;
- multi-file transactional synchronization has been qualified;
- conflict detection/reconciliation against a concurrently moving GitHub base has been qualified;
- exact remote tree reconstruction from an arbitrary local Git commit has been qualified;
- this composed workflow is adopted Agent Governance policy.

## Implications for Agent Governance

This remains diagnostic capability research. It does not change D054 execution-adapter ownership, the branching policy, source-maintenance workflow, or the rule that GitHub is canonical authority.

The new Library round-trip evidence materially strengthens the factual capability conclusion but does not create a normative need by itself. `Research-State: COMPLETE` and `Decision-State: NOT_REQUIRED` remain appropriate.

If Agent Governance later wants to standardize this as an Orchestrator maintenance workflow, that would require a separate normative Specify/Design/Plan path and, if policy changes are required, an explicit decision artifact.

Potential future qualifications include:

- restart/session persistence of a composed workspace/Library workflow;
- multi-file synchronization and atomicity expectations;
- moving-base conflict detection;
- exact Git object/tree reconstruction;
- deterministic cleanup/branch retirement;
- comparison between Library-version checkpoints and local Git checkpoint strategies.

## Evidence provenance

### Workspace/GitHub experiment

- repository: `ManuelBouza/agent-governance`;
- baseline `develop`: `20ed0e64dd6c98f38be42cd3cc28fcc220d06c5e`;
- original `.gitignore` blob: `d90d927a47936445fc975791ebedae651450cfd7`;
- temporary branch: `test/chatgpt-git-workflow`;
- experimental remote commit: `c4a2c43a65554ed9c52a4047f954373935b06a07`;
- remote comparison: one commit ahead, only `.gitignore`, two additions;
- cleanup: temporary branch ref moved back to the baseline `develop` SHA.

### Library/GitHub round-trip experiment

- repository: `ManuelBouza/test_biblioteca`;
- initial `app.py` content: `print("Hello World")`;
- initial blob SHA: `ad35e5ae34d7df6d469bfe65dbfcefe988e0169f`;
- Library path: `/test_biblioteca_flow/app.py`;
- first verified Library-derived content: `print("Hello from ChatGPT Library")`;
- first remote round-trip commit: `d82750a45f43f45a16c498674391a7a7e15dc319`;
- first resulting blob SHA: `45eac8ae8769283e63eec44d199100e7dfb6def2`;
- observed later Library versions: `2`, `3`, `4`;
- version `2` verified content: `print("Library change 1")`;
- version `4` verified content: `print("Library final change")`;
- remote state remained at `print("Hello from ChatGPT Library")` / blob `45eac8ae8769283e63eec44d199100e7dfb6def2` immediately before the final remote write;
- final remote commit: `af02345fcfed0ebe7d4b6503af7e89cdf48b84cf`;
- final commit message: `Apply accumulated Library changes`;
- final resulting blob SHA: `830b8d6471d5f1e09e0f13a0982b5849cd61f4b6`;
- final verified GitHub content: `print("Library final change")`;
- final commit parent: `d82750a45f43f45a16c498674391a7a7e15dc319`.

Chat/runtime-local observations remain dated empirical evidence. Runtime-specific failures or capabilities must be requalified before being promoted to operational assumptions.
