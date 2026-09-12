# R026 — ChatGPT Web adaptive GitHub write transport qualification

Research-ID: R026  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-12  
Last-Reviewed: 2026-09-12  
Owner: ChatGPT Orchestrator  
Scope: qualification and selection of GitHub write transports for ChatGPT Web source-maintenance work; repository reads remain direct from GitHub  
Question: Given the already-accepted D048/D066 publication model, when should ChatGPT Web use direct per-file GitHub writes versus Git Data batched publication?  
Evaluation-Refs: D048; D066; GitHub official Git Data documentation; empirical R026 qualification in `ManuelBouza/test_biblioteca`; Human scope corrections 2026-09-12  
Decision-Ref: none  
Supersedes: earlier R026 interpretations that treated Git Data batching as a universal process optimization  
Superseded-By: none

## Executive conclusion

R026 does **not** establish a new universal optimization of the Agent Governance publication process.

The repository already contains the relevant optimization intent:

- **D048** requires a normal Executor task to keep work local and perform one planned final push of the complete topic-branch state.
- **D066** already prefers batched/final GitHub publication and explicitly allows one represented multi-file tree/commit update instead of one GitHub commit per edit when the connected surface supports it.

Therefore R026's actual contribution is narrower and surface-specific:

> R026 empirically qualifies the current ChatGPT Web GitHub connector's Git Data write path and defines when that transport is preferable to direct per-file Contents API writes.

The result is **adaptive transport selection**, not replacement of normal Git/Git-push workflows.

## Current environment boundary

For this research, the active Orchestrator surface is ChatGPT Web.

The current operating assumptions are:

```text
READS
  direct GitHub connector reads

AUTHORING
  ChatGPT reasoning and temporary sandbox when useful

WRITES
  select the cheapest safe GitHub transport for the intended change
```

R026 does not depend on:

```text
ChatGPT Library
PC-local repositories
Work Desktop repositories
snapshot/archive read caches
GitHub Actions artifact bootstrap
```

Those earlier read-side explorations remain historical evidence only.

## Existing process authority

### D048 — Executor/Codex final publication

D048 already defines the normal publication boundary for Executor work:

```text
local implementation
-> verification
-> final local commits/handoff
-> one planned final push
-> remote verification
```

R026 does not replace `git push` in that path. A native Git push already transfers the repository state efficiently and preserves normal Git semantics.

### D066 — Orchestrator batched publication intent

D066 already states that Orchestrator source-maintenance work should avoid one remote GitHub mutation per local edit and, when the connected surface supports it, should publish a represented multi-file state as one batched tree/commit update.

R026 therefore qualifies the concrete ChatGPT Web mechanism for that existing design intent.

## Qualified ChatGPT Web write transports

### Transport A — direct Contents API write

Use the connector's direct `create_file`, `update_file`, or `delete_file` operation when the change is small and independent.

For one text file:

```text
1 changed file
-> 1 remote mutation
```

This is strictly cheaper in mutation count than Git Data batching, which requires three publication mutations.

### Transport B — Git Data batch

For a coherent multi-file change, ChatGPT Web can publish:

```text
create_tree
-> create_commit(parent = expected topic HEAD)
-> update_ref(force = false)
```

Text additions/modifications can be carried inline in `create_tree`; deletions use `sha: null`.

For N inline text changes:

```text
N files
-> 3 publication mutations
```

The mutation count is constant with respect to N within the qualified request envelope.

### Binary objects

The current connector's direct file-write wrappers are UTF-8 text oriented. R026 qualified binary publication through:

```text
create_blob(base64)
-> reference blob SHA from create_tree
-> create_commit
-> update_ref(force=false)
```

Each new binary blob that must be created adds one `create_blob` mutation before the common three-step publication path.

## Adaptive selection rule

The transport should be selected by both **cost** and **coherence**, not file count alone.

### Normal default

```text
Executor / Codex with native Git
  -> preserve D048 single final git push

ChatGPT Web, one independent text file
  -> direct Contents API write

ChatGPT Web, coherent multi-file change
  -> compare direct-write cost against Git Data batch
  -> choose Git Data when it reduces mutations or when one-commit coherence materially matters
```

### Mutation-count comparison for text files

| Changed text files | Direct per-file writes | Git Data batch | Count-only preference |
|---:|---:|---:|---|
| 1 | 1 | 3 | direct write |
| 2 | 2 | 3 | direct write unless atomic coherence matters |
| 3 | 3 | 3 | choose by coherence/safety |
| 4+ | N | 3 | Git Data batch |

This table is a transport-selection aid, not a hard governance threshold.

A two-file change may still justify Git Data if the files must land as one coherent commit. Conversely, independent file updates should not be forced into a batch merely because batching is available.

## Safety invariant for Git Data publication

When Transport B is selected:

```text
1. read and record expected topic-branch HEAD
2. prepare complete intended change set
3. create_tree against the expected parent tree
4. create_commit with parent = expected topic HEAD
5. update_ref(force = false)
6. if ref movement is rejected, fail closed and reread/reconcile
7. verify resulting branch ref
8. for material multi-file changes, compare expected base/head paths
```

No R026 transport authorizes direct writes to `develop`, `main`, or another long-lived branch. D061 remains controlling.

## Empirical qualification

R026 exercised the Git Data transport on the disposable repository `ManuelBouza/test_biblioteca`.

Qualified results:

- delete using `sha: null` — PASS;
- rename represented as delete-old + add-new in one tree — PASS;
- binary object using base64 `create_blob` plus tree SHA reference — PASS;
- 64 inline text files in one `create_tree` — PASS;
- three common publication mutations for that 64-file text batch — PASS;
- explicit stale-ref race with `force=false` — PASS / HTTP 422 `Update is not a fast forward`;
- losing stale candidate did not overwrite the concurrent winner — PASS;
- bounded post-publication branch/diff verification — PASS.

The detailed evidence is preserved in:

`docs/research/R026-WRITE-PATH-EMPIRICAL-QUALIFICATION.md`

## Payload boundary

The 64-file test establishes only a proven lower bound for small inline text entries.

GitHub's official Create Tree documentation does not publish a create-request ceiling that Agent Governance can safely promote to a governance constant. Therefore:

```text
64 small inline files = empirically proven
exact maximum = NOT QUALIFIED
```

If a runtime rejects a batch because of payload/connector limits, the caller must use a bounded fallback or split publication deliberately. It must not infer a permanent product-wide threshold from one connector/runtime version.

## What R026 actually improves

R026 improves the **transport choice available to ChatGPT Web**, not the already-efficient native Git process.

It prevents two opposite inefficiencies:

```text
inefficiency A:
  N-file coherent ChatGPT Web change
  -> N separate remote content commits

inefficiency B:
  trivial 1-file ChatGPT Web change
  -> unnecessarily force create_tree + create_commit + update_ref
```

The adaptive policy selects the simpler safe path for each case.

## Non-goals

R026 does not propose:

- replacing native Executor/Codex `git push`;
- changing D048's single-final-push boundary;
- replacing D066 wholesale;
- optimizing repository reads;
- reviving T058;
- making Library operationally required;
- defining a universal batch-size ceiling;
- weakening topic-branch freshness or branch-target controls.

## Decision question

The remaining decision is not whether Git Data batching works; that is empirically qualified within the stated envelope.

The remaining governance question is:

> Should D066 / the Orchestrator operating procedure explicitly encode adaptive ChatGPT Web write-transport selection, using direct Contents API writes for trivial independent changes and Git Data batching for coherent multi-file changes where batching provides lower mutation cost or stronger one-commit coherence?

Until that is adopted explicitly:

```text
Research-State: COMPLETE
Decision-State: EVALUATING
Evidence: QUALIFIED
Universal process replacement: NO
ChatGPT Web adaptive transport candidate: YES
T058: remains frozen
```
