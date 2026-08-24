# D049 — RCAB committed snapshot and live-state separation

Status: ACCEPTED  
Date: 2026-08-15  
Scope: RCAB generated-manifest freshness semantics for the source repository

## Problem

T031 introduced `baselines/repository-context-manifest-v1.json` as a deterministic projection of the registered RCAB map and registered file content. Its stale/tampered check correctly compares the committed projection with current registered content.

After T031 was accepted, ordinary Orchestrator-owned Markdown gates legitimately changed registered files, including `docs/EXECUTOR-HANDOFFS.md` and `docs/orchestrator/CHECKPOINT.md`. The generated manifest was not part of those Markdown-only changes. As a result, clean canonical `develop@53b9c39c1111f4b871ef73b7447510195f672ea2` already fails `tests/test_repository_context.py::test_manifest_cli_check_on_real_repository` before T021 changes are applied.

This exposes a lifecycle coupling error:

```text
registered Markdown evolves legitimately
        -> committed generated projection becomes older
        -> ordinary full deterministic suite becomes red
        -> unrelated executable task inherits a pre-existing failure
```

The problem is not stale detection itself. The problem is treating an intentionally persisted generated evidence snapshot as if it must remain a continuously live cache of mutable repository authority.

## Decision

RCAB separates **committed snapshot evidence** from **live repository state**.

### 1. Committed manifest = epoch snapshot evidence

`baselines/repository-context-manifest-v1.json` is a deterministic snapshot of the explicit RCAB registry and registered content at the epoch when that snapshot is generated and accepted.

It is:

- generated evidence;
- non-authoritative;
- canonically ordered and reproducible for the same registry/content inputs;
- allowed to become historically older as canonical source files evolve.

Ordinary source evolution does not make an older committed snapshot intrinsically invalid.

### 2. Live RCAB state must be computed from live authority

Any current bootstrap/router footprint, warning state, registry-integrity result or currentness decision MUST be derived directly from the current `docs/CONTEXT-MAP.md` registry plus current tracked registered files.

A committed snapshot MUST NOT be trusted as current merely because it exists or previously passed.

```text
snapshot evidence != live state
historical projection != current authority
```

### 3. Explicit currentness comparison remains supported

T031 stale/current comparison remains a useful deterministic capability. A caller may explicitly compare a committed snapshot to current registered content and receive a fresh/stale result.

That comparison is a **deliberate currentness check**, not an unconditional invariant of the ordinary full deterministic test suite.

Fixture tests MUST continue proving that currentness comparison detects both fresh and stale/tampered conditions.

### 4. Default deterministic regression must not require a snapshot to equal mutable live state

The normal full deterministic suite MUST remain green when an accepted historical snapshot is internally valid but registered Markdown has legitimately advanced since that snapshot.

Repository tests may validate snapshot structure, canonical identity, internal digest consistency and source-only isolation without asserting that the stored snapshot equals today's live repository unless the test explicitly represents a live-currentness gate.

### 5. Snapshot refresh is explicit

A committed RCAB snapshot is refreshed only when a Task/Operational Contract or accepted RCAB gate explicitly requires a new snapshot epoch.

Normal Markdown maintenance MUST NOT require an incidental non-Markdown manifest rewrite merely to keep unrelated regression suites green.

If a workflow chooses to use a committed manifest as a **live merge/release gate**, that workflow must first prove the manifest is current against the exact candidate state being gated.

### 6. Ratchet semantics are unchanged

D047's bootstrap/router reference remains:

- `2` files;
- `21,471` UTF-8 bytes;
- `298` lines;
- non-blocking warning above `105%` of reference bytes or above two files.

D049 does not change that policy, introduce exact token estimates, impose universal source-size limits, or authorize automatic document splitting.

## T031 compatibility

T031's deterministic projection, canonical ordering, self-reference avoidance, registry validation, stale/tampered detection and warning computation remain valid capabilities.

D049 refines only the lifecycle interpretation of a **committed** projection:

- stale comparison is explicit when currentness matters;
- historical snapshot age is not by itself a generic test failure;
- live warnings/currentness are computed from current source, not from the snapshot.

No T031 implementation history is rewritten.

## Implementation gate

T032 implements this decision and restores a green deterministic baseline before T021 rework resumes.

T032 must preserve source-only isolation and must not modify T021 implementation state, Consumer behavior, Governance Core/Skill semantics, dependencies, network requirements, or RCAB size policy.
