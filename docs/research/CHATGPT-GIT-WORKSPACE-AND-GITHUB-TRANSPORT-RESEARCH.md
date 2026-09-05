# ChatGPT Git workspace and GitHub transport research

Research-ID: R012  
Research-State: COMPLETE  
Decision-State: NOT_REQUIRED  
Opened: 2026-09-05  
Last-Reviewed: 2026-09-05  
Owner: ChatGPT Orchestrator  
Scope: ChatGPT project workspace Git behavior, GitHub connector transport, and the boundary between local Git state and ChatGPT Library persistence for source-product maintenance experiments  
Question: Can ChatGPT reproduce a VS Code/Codex-like Git working-copy workflow by combining a real local Git repository in the chat workspace with explicit GitHub connector operations, and what are the transport and persistence boundaries?  
Evaluation-Refs: empirical session experiment against `ManuelBouza/agent-governance` at `develop` `20ed0e64dd6c98f38be42cd3cc28fcc220d06c5e`; temporary branch `test/chatgpt-git-workflow`; remote test commit `c4a2c43a65554ed9c52a4047f954373935b06a07`  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Summary

A ChatGPT project session can support a real local Git working tree in its temporary execution workspace and can separately read and mutate GitHub through the connected GitHub surface. The two mechanisms are not one native `git clone`/`git push` transport path.

The experimentally supported architecture is:

```text
GitHub canonical repository
        |
        | explicit GitHub read operations
        v
ChatGPT temporary workspace with real .git state
        |
        | git status / diff / add / commit / local tests
        v
explicit GitHub write operations
        |
        v
GitHub topic branch / commit / PR
```

Direct Git CLI network transport from the temporary workspace was not available in the tested session, while GitHub connector writes succeeded. ChatGPT Library is a separate persistence surface and must not be treated as the `.git` working tree or as an automatically synchronized Git remote.

## Research question decomposition

The investigation separated four capabilities that are easy to conflate:

1. **Local Git semantics** — whether the temporary execution workspace can contain a real `.git` repository and execute ordinary Git commands.
2. **Remote repository transport** — whether that local Git CLI can directly fetch/push GitHub.
3. **Connected GitHub mutation** — whether ChatGPT can perform branch/file/commit/PR operations through its GitHub connection even when CLI network transport is unavailable.
4. **Library persistence** — whether persistent ChatGPT Library files are themselves a Git working tree or an automatic Git synchronization layer.

## Empirical setup

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

## Findings

### F1 — real local Git state is available

A repository initialized in the temporary ChatGPT execution workspace behaved as a normal Git working tree. The following operations succeeded locally:

- repository initialization;
- `git status`;
- `git diff`;
- `git add`;
- local `git commit`;
- ordinary file edits between commits.

This is materially different from Library metadata operations: the workspace can contain actual `.git` state and Git can calculate tracked/untracked status and diffs there.

### F2 — direct Git CLI transport to GitHub was unavailable in the tested session

Direct network checks from the local Git working tree failed when attempting GitHub transport. The observed failure was:

```text
Could not resolve host: github.com
```

Therefore this experiment did **not** establish a supported path of:

```text
local .git -> git fetch/pull/push -> github.com
```

This is an environment observation, not a universal claim about every ChatGPT execution surface. It must be revalidated if future runtime networking changes.

### F3 — explicit GitHub connector transport succeeded

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

The test branch was then moved back to the original `develop` commit, leaving no content divergence from the baseline. The temporary branch itself remained because branch deletion was not exposed by the connected action set used in that turn.

### F4 — local Git commits and GitHub commits are separate histories unless explicitly synchronized

A local `git commit` in the ChatGPT workspace does not automatically become the commit later created by the GitHub connector. Synchronization must be explicit at the file/tree/content level, after which GitHub creates or advances its own canonical commit history.

Consequently, local commit SHAs should be treated as temporary workspace evidence unless the exact Git objects are deliberately reconstructed remotely. The authoritative source-product state remains GitHub.

### F5 — ChatGPT Library is not the Git working tree

Separate Library testing established that ChatGPT can persist and organize files with operations such as upload, rename, move, overwrite/version update, folder creation, and deletion. Those capabilities do not make Library paths into a native `.git` working tree.

The safe conceptual boundary is:

```text
Library = persistent file/reference storage
Workspace = temporary executable filesystem where real .git state may exist
GitHub = canonical repository and remote authority
```

No automatic Library <-> GitHub synchronization was observed or documented by this experiment.

### F6 — a VS Code/Codex-like workflow is feasible through an adapter boundary

For bounded ChatGPT-owned work, a functional workflow can be composed as:

1. read the exact base revision and required files from GitHub;
2. materialize/reconstruct a temporary working copy in the execution workspace;
3. maintain real local Git state for `status`, `diff`, staging, local checkpoints, and tests;
4. review the resulting local diff;
5. write the approved file contents/tree to an explicit GitHub topic branch through the connected GitHub surface;
6. verify the remote comparison/commit/PR from GitHub;
7. treat GitHub, not the temporary workspace or Library, as canonical state.

This approximates the developer ergonomics of a local editor plus Git while retaining an explicit transport adapter between the temporary workspace and GitHub.

## Boundaries and non-findings

This research does **not** establish that:

- ChatGPT Library can contain or execute a persistent `.git` repository;
- local `.git` state survives arbitrary chat/runtime turnover;
- `git push` from the temporary workspace is generally available;
- local commit SHA identity can be preserved automatically when writing through the GitHub connector;
- the connector exposes every Git operation, including branch deletion, in every session;
- this workflow is already adopted Agent Governance policy.

The experiment also did not complete a controlled end-to-end `GitHub -> Library -> workspace Git -> Library -> GitHub` qualification. Library remains useful as an optional persistence/cache layer, but it is not required for the core working-copy pattern.

## Volatile versus durable conclusions

### Durable analytical conclusion

Local Git semantics and remote GitHub transport are separate capability layers. A workflow can use a real temporary Git working tree for local development semantics while using an explicit GitHub adapter for canonical remote writes.

### Volatile runtime facts

The following must be revalidated before relying on them operationally because available ChatGPT tools and execution networking can change:

- whether the current workspace can resolve/reach `github.com` directly;
- which GitHub write operations are currently exposed;
- whether Library mutation/version behavior is available in the current client/session;
- whether generated/Library files are automatically materialized into the executable workspace.

## Implications for Agent Governance

This result is diagnostic capability research only. It does not change the current source-maintenance workflow, D054 execution-adapter ownership, branching policy, or the rule that GitHub is canonical authority.

If Agent Governance later wants to make this a standard Orchestrator maintenance workflow, that adoption should be handled separately through normal Specify/Design/Plan authority and, if normative policy changes are required, an explicit decision artifact. A future qualification should test restart persistence, multi-file synchronization, conflict detection against a moving remote base, exact remote tree reconstruction, and deterministic cleanup.

## Evidence provenance

Repository evidence from the experiment:

- baseline `develop`: `20ed0e64dd6c98f38be42cd3cc28fcc220d06c5e`;
- original `.gitignore` blob: `d90d927a47936445fc975791ebedae651450cfd7`;
- temporary branch: `test/chatgpt-git-workflow`;
- experimental remote commit: `c4a2c43a65554ed9c52a4047f954373935b06a07`;
- remote comparison: one commit ahead, only `.gitignore`, two additions;
- cleanup: temporary branch ref moved back to baseline `develop` SHA.

Chat-local observations about direct CLI networking are recorded here because the original transient runtime cannot itself be canonical evidence. They should be treated as dated empirical observations and requalified before future operational reliance.
