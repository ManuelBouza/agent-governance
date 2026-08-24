# T032 — RCAB Snapshot / Live-State Separation

## Identity

- Task ID: `T032`
- Status: `IN_PROGRESS`
- Type: `infrastructure/test`
- Base branch: `develop`
- Expected topic branch: `fix/t032-rcab-snapshot-live-separation`
- Expected executor handoff: `handoffs/T032-executor-handoff.json`
- Assurance-Class: `deterministic`
- Baseline: `T031-R1 accepted RCAB projection + D049 snapshot/live separation`
- Verification-Planes: `static, deterministic, negative-control, package/isolation`
- Release-Impact: `none`
- Context-Impact: `focused`
- Rework authority: `docs/reviews/T032-R1.md`
- Submitted R1 HEAD rejected for acceptance: `b43b306e56c6b90969c3dd10e23ccf8e00cc8ba5`

## Objective

Implement D049 by separating committed RCAB manifest snapshot evidence from live repository currentness, while preserving explicit stale/current comparison and live bootstrap/router warning computation.

Restore a green canonical full deterministic baseline without requiring ordinary accepted Markdown evolution to rewrite the committed non-Markdown snapshot after every registered-file change.

## Controlling references

- `AGENTS.md`
- `docs/decisions/D046-agent-capability-engineering-and-context-architecture.md`
- `docs/decisions/D047-rcab-context-map-and-ratchet-policy.md`
- `docs/decisions/D049-rcab-snapshot-live-separation.md`
- `docs/CONTEXT-ARCHITECTURE.md`
- `docs/CONTEXT-MAP.md`
- `docs/reviews/T031-R1.md`
- `docs/reviews/T032-R1.md` when rework is active
- `docs/learning/L006-rcab-manifest-live-freshness-coupling.md`
- `tools/repository_context.py`
- `tests/test_repository_context.py`
- `baselines/repository-context-manifest-v1.json`

## Authorized scope

- Source-only RCAB tooling under `tools/repository_context.py` or an equivalently small source-only helper.
- Deterministic tests under `tests/test_repository_context.py` or a narrowly focused RCAB test module.
- `baselines/repository-context-manifest-v1.json` as the refreshed generated snapshot epoch.
- An optional non-Markdown schema under `schemas/` only if it materially improves deterministic snapshot validation.
- `handoffs/T032-executor-handoff.json`.

## Explicit exclusions

- Any committed Markdown edit.
- Any change to D047 bootstrap warning thresholds, registered route/class policy, or T030-R2 reference values.
- Any T021 implementation/rework change.
- Any `governance-core/`, `governance-skill/`, Consumer runtime/profile behavior, Skill activation, or Consumer artifact semantic change.
- Any source-document split or universal source-size hard budget.
- Any dependency, lockfile, host configuration, tokenizer, model, embeddings/vector, telemetry, remote retrieval, or network dependency.
- Any weakening of explicit malformed/duplicate/missing-target registry checks or explicit stale/tampered comparison capability.

## Required behavior

### Snapshot evidence

The committed manifest must clearly represent an **epoch snapshot** rather than claim continuous live-currentness.

Its canonical form must remain deterministic and self-contained for the registered content measured at generation time. It must preserve canonical ordering, registered path/class/route/physical metrics, content digests, accepted bootstrap reference and snapshot-era ratchet observation.

The implementation SHOULD make snapshot semantics machine-visible in the projection schema or equivalent deterministic field so a consumer of the JSON cannot honestly mistake it for live authority.

During R1 rework, the snapshot's offline integrity boundary MUST also bind all canonical epoch-evidence fields and deterministically verify derived registry/ratchet consistency as specified by `docs/reviews/T032-R1.md`.

### Live state

The tool must expose an explicit live-status/current-measurement path that derives current registry integrity, registered content measurements and bootstrap/router warning state directly from current `docs/CONTEXT-MAP.md` plus current tracked registered files.

Live status MUST NOT trust the committed snapshot's stored current measurements.

### Explicit currentness comparison

A caller must still be able to explicitly compare a committed snapshot with current registered content and deterministically learn whether it matches or is stale/tampered relative to current source.

Existing CLI behavior may be retained or a clearer explicit comparison mode may be introduced, provided compatibility is handled deliberately and tests prove both fresh and stale outcomes.

An explicit currentness comparison may return failure for stale state. That behavior is not the default invariant of the ordinary full deterministic regression suite.

### Default regression semantics

The normal deterministic suite must not fail merely because a valid historical committed snapshot predates a legitimate change to a registered Markdown file.

Tests must distinguish:

- snapshot canonical/internal integrity;
- explicit snapshot-vs-current comparison;
- live current status/warning computation.

## Acceptance criteria

### AC-T032-1 — deterministic snapshot semantics
Repeated snapshot generation from identical registry/content inputs produces byte-identical canonical output with explicit epoch/snapshot semantics, canonical ordering, stable registered-content identity and no self-reference or Git-commit self-reference requirement.

For R1 acceptance, the canonical snapshot integrity identity must bind the complete epoch-evidence payload rather than only `path + sha256`.

### AC-T032-2 — live source authority
Live RCAB status is computed directly from current registry + current tracked registered files and reports current bootstrap/router file count, bytes, lines, delta and warning state without trusting stored snapshot measurements.

### AC-T032-3 — explicit currentness detection preserved
Explicit comparison accepts a snapshot generated from the same current registered content and rejects/reports stale after registered content changes. Tampered projection remains deterministically detectable.

R1 requires representative independent negative controls for tampering of registered metadata/physical metrics, registry identity, and bootstrap/ratchet derived state, not only direct corruption of `registered_content_digest`.

### AC-T032-4 — historical snapshot does not poison ordinary regression
A fixture with a valid snapshot followed by legitimate registered-source evolution keeps the ordinary/default regression path green while explicit currentness comparison reports the snapshot as stale.

The repository's normal full deterministic suite must be green on the final T032 candidate.

### AC-T032-5 — D047 ratchet preserved
The accepted `2 files / 21,471 bytes / 298 lines / 5% warning` policy remains unchanged. Live warning-only state remains non-blocking. Snapshot age does not alter the accepted reference.

### AC-T032-6 — source-only/package isolation
RCAB tooling/snapshot remain source-only and outside the T020 Consumer artifact. No Core/Skill/runtime/profile/dependency/network drift occurs.

## Verification requirements

- Focused tests mapped exactly to `AC-T032-1` through `AC-T032-6` with evidence types.
- Repeated byte-identity snapshot generation.
- Fresh and stale explicit currentness fixtures.
- Tampered snapshot negative controls covering all R1 classes in `docs/reviews/T032-R1.md`.
- Registered-source-evolution fixture proving default regression does not fail solely on snapshot age.
- Live-status fixture proving current metrics/warning are recomputed from current files rather than copied from the snapshot.
- Warning boundary tests remain green and warning-only status remains success.
- Existing T030 behavior remains green.
- Existing T031 registry/parser/projection/isolation coverage remains green except for intentional D049 expectation changes.
- T020 artifact-isolation/source-consumer-separation regressions remain green.
- Full deterministic suite must be green.
- Ruff check/format and Python compilation for changed Python.
- Manifest JSON parse and `git diff --check`.
- Diff inspection proving no Markdown, T021, dependency/lock/configuration, Core/Skill, Consumer runtime/profile, release or package drift.
- No network access.

The handoff MUST map every acceptance criterion to exact verifier/test evidence and evidence type.

## Stop / escalation conditions

Stop and report `BLOCKED` rather than broadening scope if:

- restoring a green baseline requires weakening D047's warning policy or registry integrity;
- the design requires changing the RCAB map/policy Markdown;
- currentness cannot be separated from snapshot evidence without changing Consumer/runtime surfaces;
- a new dependency/network/model service appears necessary;
- implementation would require changing T021 or another active task branch.

## Expected handoff

Before claiming completion, persist `handoffs/T032-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, follow D048's normal-task publication boundary, commit/push all authorized work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
