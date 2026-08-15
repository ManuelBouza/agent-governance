# D047 — RCAB context map and ratchet policy

Status: ACCEPTED  
Date: 2026-08-15  
Scope: source-repository context routing, generated projection, warning/ratchet policy

## Decision

Agent Governance adopts the first source-repository RCAB policy gate from the accepted T030 baseline.

The source context architecture SHALL use two deliberately small layers:

1. `docs/CONTEXT-MAP.md` — the human-readable canonical routing/classification registry for stable source context routes;
2. `baselines/repository-context-manifest-v1.json` — a reproducible machine-readable projection generated from the registered map entries and their current tracked content.

The generated manifest is discovery/evidence only. It MUST NOT acquire authority over the Markdown files it projects and MUST NOT duplicate the current frontier carried by `docs/orchestrator/CHECKPOINT.md`.

## Smallest-useful-map boundary

The context map registers only stable, high-value source routes. It does not enumerate all tracked files, all reviews, all handoffs, or all historical evidence.

Dynamic task/review/evidence selection remains the responsibility of the current checkpoint plus the active Task/Operational Contract. The map gives a stable route to the governing families; the checkpoint gives the current exact frontier.

This avoids replacing progressive disclosure with a large index that itself becomes mandatory context.

## Bootstrap/router ratchet

T030-R2 establishes the accepted physical source cold-start reference for the mandatory bootstrap/router cohort:

- files: `AGENTS.md` + `docs/orchestrator/CHECKPOINT.md`;
- file count: `2`;
- UTF-8 bytes: `21,471`;
- lines: `298`.

UTF-8 bytes remain the canonical tokenizer-neutral size metric. Lines are diagnostic only.

RCAB v1 SHALL always report the current delta against that accepted reference.

A non-blocking bootstrap-growth warning is emitted when either:

- the registered `bootstrap` + `router` cohort contains more than `2` files; or
- its aggregate UTF-8 byte size exceeds `105%` of the accepted T030-R2 reference.

The 5% band is a review-sensitivity margin, not a safety limit, token estimate, or claim about model capacity. It exists to avoid warning on trivial editorial churn while surfacing material growth in context that is paid on nearly every source-maintenance bootstrap.

A warning MUST NOT fail a task, block a merge, or automatically rewrite/split source files.

If the current bootstrap/router footprint drops below the accepted reference, tooling MAY report a lower `ratchet_candidate`, but MUST NOT silently change the authoritative reference. Advancing or lowering the reference requires an Orchestrator-owned reviewed policy update grounded in a newly accepted baseline.

## Focused/task/evidence policy

No absolute source size warning is adopted for `focused`, `task`, `evidence`, `generated-data`, or `exempt-on-demand` artifacts in RCAB v1.

For those classes, physical size remains report-only evidence. Large files may be healthy when their normal load path is bounded.

Semantic decomposition remains a separate Orchestrator judgment requiring evidence of independently loadable responsibilities, improved routing, or reduced mandatory context. Numeric size alone does not authorize a split.

## Deterministic integrity boundary

The first machine-enforceable RCAB checks are limited to mechanically decidable integrity properties:

- malformed or ambiguous registered map data;
- duplicate registered paths with conflicting classifications;
- registered targets that do not exist in the tracked tree;
- non-reproducible or stale generated manifest content relative to the registered map/targets;
- source/distribution boundary leakage covered by existing Consumer artifact-isolation tests.

These integrity failures MAY be blocking once implemented and replay-tested because their semantics are deterministic.

Bootstrap-growth warnings remain non-blocking under this decision.

## Manifest identity

The generated manifest SHOULD identify its source deterministically without creating Git-self-reference churn.

At minimum it SHALL contain:

- projection schema version;
- SHA-256 of the canonical machine-readable registry embedded in `docs/CONTEXT-MAP.md`;
- canonically ordered registered paths, classifications and route membership;
- current per-path tracked content SHA-256 and physical metrics;
- a `registered_content_digest` derived from the ordered registered path/content identities;
- bootstrap/router current totals, accepted reference and warning state.

The committed projection MUST NOT require the commit SHA that contains itself. A content identity is sufficient for freshness of the projected registered surface.

## Source/distribution boundary

The context map, generated manifest and source context tooling are source-maintenance artifacts only.

They MUST remain outside the T020 Consumer package boundary. Existing package-isolation regressions remain mandatory for implementation work that touches source context tooling.

## No new retrieval infrastructure

RCAB v1 does not authorize embeddings, vector databases, remote semantic retrieval, tokenizer dependencies, telemetry services, or host-specific context infrastructure.

Canonical Git + direct Markdown routing + a deterministic local projection remains the selected architecture until evidence shows it is insufficient.

## Program sequencing

T031 implements the generated projection, deterministic integrity checks and non-blocking bootstrap warning semantics selected here.

T021 remains READY but SHALL not launch until T031 is accepted, so the prospective D044 refactor proceeds with the RCAB gate actually implemented rather than merely documented.

T026 remains separately gated and is unaffected by this decision.
