# R026 — Human disposition

Research-ID: R026  
Research-State: COMPLETE  
Decision-State: APPROVED_DEFERRED  
Implementation-State: NOT_STARTED  
Normative-State: UNCHANGED  
Date: 2026-09-12  
Human disposition: explicit approval received in chat (`go`) after review of the unresolved R026 decision boundary  
Branch: `research/r026-github-interaction-minimization`  
PR: #371  
Normative change: none

## Decision

The Human approves the R026 technical conclusion as the preferred future direction for ChatGPT Web GitHub write minimization, while explicitly deferring implementation and normative adoption.

The approved direction is:

```text
Repository reads
  -> remain direct from GitHub under the Human-directed R026 scope

Executor / Codex with native Git
  -> preserve D048 local work + one planned final normal git push

ChatGPT Web, one independent text-file change
  -> use direct create/update/delete file transport

ChatGPT Web, coherent multi-file change
  -> choose adaptively between direct writes and Git Data batching
  -> prefer Git Data when it reduces remote mutation count or one-commit coherence materially matters

Git Data publication
  -> create_tree
  -> create_commit(parent = expected topic HEAD)
  -> update_ref(force = false)
  -> bounded verification
```

The empirically qualified guidance remains:

- 1 text file: direct write is cheaper than a three-mutation Git Data batch;
- 2 text files: direct writes are cheaper by count, though one-commit coherence may justify batching;
- 3 text files: mutation-count tie; choose by coherence/safety;
- 4+ coherent text files: Git Data batching reduces common publication mutations from N to 3 within the qualified request envelope;
- binary publication uses `create_blob` as required before the common tree/commit/ref path;
- stale incompatible ref movement must fail closed under `force=false`;
- the 64-file inline-text result is a proven lower bound, not a product-wide maximum.

## Deferred implementation boundary

This approval does **not** authorize implementation now.

It does not authorize:

- modifying D066 or other normative Decision Records;
- changing current Task Contract or Orchestrator operating procedures;
- changing the repository read path;
- replacing D048 native Git publication;
- introducing Library, Work Desktop, snapshot/artifact read caching, or another persistence plane;
- merging PR #371 solely on the basis of this disposition;
- direct writes to `develop` or `main`;
- resuming T058;
- any source-product runtime or automation change.

A future explicit Human implementation authorization is required before any normative or operational adoption work begins.

## Closure meaning

R026 is now decision-closed for research purposes:

```text
Research-State: COMPLETE
Decision-State: APPROVED_DEFERRED
Implementation-State: NOT_STARTED
Normative-State: UNCHANGED
Next implementation action: NONE until explicit Human authorization
```

PR #371 may remain open as the unintegrated research carrier. Its integration/merge is a separate Human-controlled action and is not implied by this disposition.
