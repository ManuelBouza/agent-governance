# T031 — RCAB Context Manifest And Bootstrap Ratchet

## Identity

- Task ID: `T031`
- Status: `READY`
- Type: infrastructure/test
- Base branch: `develop`
- Expected topic branch: `infra/t031-context-manifest-ratchet`
- Expected executor handoff: `handoffs/T031-executor-handoff.json`
- Assurance-Class: `deterministic`
- Baseline: `T030-R2 accepted repository-context baseline`
- Verification-Planes: `static, deterministic, package/isolation`
- Release-Impact: `none`
- Context-Impact: `focused`

## Objective

Implement the smallest deterministic RCAB v1 machine projection and bootstrap/router warning ratchet selected by D047.

The task projects the canonical registry embedded in `docs/CONTEXT-MAP.md` into a reproducible source-only manifest, validates mechanically decidable registry/projection integrity, and reports non-blocking bootstrap growth warnings against the accepted T030-R2 reference.

It does not split source documents, impose universal size budgets, alter Consumer behavior, or add retrieval infrastructure.

## Controlling references

- `AGENTS.md`
- `docs/decisions/D046-agent-capability-engineering-and-context-architecture.md`
- `docs/decisions/D047-rcab-context-map-and-ratchet-policy.md`
- `docs/AGENT-CAPABILITY-ENGINEERING.md`
- `docs/CONTEXT-ARCHITECTURE.md`
- `docs/CONTEXT-MAP.md`
- `docs/TASK-CONTRACTS.md`
- `docs/TESTING-AND-EVALUATION.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `docs/reviews/T030-R2.md`
- `baselines/repository-context-source-v1.json`
- `tools/repository_context.py`

## Authorized scope

- Extend source-only `tools/repository_context.py` or an equivalently small source-only helper to parse the exact `RCAB-MAP-V1` registry markers from `docs/CONTEXT-MAP.md`.
- Add deterministic manifest generation/check behavior.
- Add the generated non-Markdown projection at `baselines/repository-context-manifest-v1.json`.
- Add focused deterministic tests, normally by extending `tests/test_repository_context.py`.
- Add an optional non-Markdown schema under `schemas/` only if it materially improves deterministic validation.
- Persist `handoffs/T031-executor-handoff.json`.

## Explicit exclusions

- Any committed Markdown edit.
- Any change to D047 policy meaning, map routes/classes, ratchet values, or T030 accepted semantics.
- Any change to `governance-core/`, `governance-skill/`, Consumer runtime/profile behavior, or Consumer artifact contents.
- Any document split/rewrite.
- Any hard failure caused solely by bootstrap/router physical growth warning.
- Any universal per-file byte/line/LOC/token threshold.
- Any dependency, lockfile or host configuration change.
- Any network, tokenizer, LLM, embeddings, vector database, telemetry or remote retrieval dependency.
- Any attempt to infer semantic route membership beyond the explicit map registry.

## Required manifest surface

The canonical generated projection must include at least:

- projection schema version;
- SHA-256 of the exact canonical machine-readable registry payload extracted from `docs/CONTEXT-MAP.md`;
- canonically ordered registered entries with path, class and route membership;
- for each registered tracked path: current byte size, meaningful line count, SHA-256/content identity and any already-supported deterministic classification metadata useful to the projection;
- `registered_content_digest` derived from ordered registered path/content identities;
- bootstrap/router current file count, UTF-8 byte size and line count;
- the exact accepted T030-R2 bootstrap ratchet reference carried by the registry;
- current delta/reference ratio and warning state.

The manifest MUST avoid self-reference. Its own path must not participate in any content identity that would make unchanged regeneration impossible.

The manifest MUST NOT require or embed the Git commit SHA that contains itself as canonical identity.

## Registry parsing invariants

- Parse only the content between the exact `RCAB-MAP-V1:BEGIN` / `RCAB-MAP-V1:END` markers.
- Require exactly one registry block.
- Require valid JSON and supported registry schema version.
- Require unique registered paths.
- Reject conflicting/invalid classifications or malformed route membership.
- Require every registered target to exist as a tracked Git path.
- Do not infer routes/classes from Markdown prose, reference counts, filenames, embeddings, heuristics or model judgment.

## Warning semantics

D047 is authoritative:

- accepted bootstrap/router reference: `2` files, `21,471` UTF-8 bytes, `298` lines;
- warning relative-growth threshold: `5%` over accepted byte reference;
- any registered bootstrap/router file-count increase above `2` also warns;
- line delta is diagnostic and is not independently blocking;
- warning state is non-blocking.

Tooling MUST expose the current delta and warning reason deterministically.

A warning-only run MUST return success unless another deterministic integrity failure is present.

If current bootstrap/router bytes are below the accepted reference, tooling MAY emit a lower ratchet candidate but MUST NOT alter the authoritative registry or committed Markdown.

## Deterministic blocking checks

Once implemented, the following are allowed to fail a check command because their semantics are mechanically decidable:

- malformed/ambiguous registry;
- duplicate/conflicting registered paths;
- missing/untracked registered target;
- generated manifest differs from deterministic regeneration for the same registered content/map;
- non-reproducible canonical projection;
- source/distribution leakage detected by existing package-isolation tests.

A physical size warning alone MUST NOT produce failure.

## Acceptance criteria

### AC-RCAB-1 — deterministic projection
Repeated generation from the same map/registered tracked content produces byte-identical canonical manifest output with canonical ordering and stable content identity.

### AC-RCAB-2 — registry integrity
Malformed, duplicate/conflicting, or missing/untracked registered targets fail deterministically; valid registry content succeeds without semantic inference.

### AC-RCAB-3 — warning ratchet
Bootstrap/router bytes and file count are computed from registered entries and compared exactly to the D047/T030-R2 reference. A synthetic >5% byte growth or >2-file cohort produces a warning while preserving success exit status when no integrity error exists; at/below-threshold cases do not false-positive.

### AC-RCAB-4 — stale manifest detection
A check mode deterministically rejects a stale/tampered committed manifest and accepts a freshly generated projection for the same registered content/map.

### AC-RCAB-5 — source-only isolation
The map projection, manifest and tooling remain outside the T020 Consumer package; existing artifact isolation remains green.

### AC-RCAB-6 — no enforcement/mutation drift
Running generation/check/warning behavior does not rewrite Markdown, split files, change policy, introduce dependencies/network access, or fail solely because a focused/evidence file is physically large.

## Verification requirements

- Focused tests covering AC-RCAB-1 through AC-RCAB-6.
- Positive and negative registry parser fixtures.
- Repeated byte-identity generation test.
- Stale/tampered manifest negative control.
- Warning boundary tests including below threshold, above 5% byte growth, and bootstrap/router file-count growth.
- Negative control proving warning-only status exits successfully.
- Existing `tests/test_repository_context.py` T030 behavior remains green.
- T020 artifact-isolation regression remains green.
- Full deterministic regression suite.
- Ruff check/format and Python compilation for changed Python.
- Baseline/manifest JSON parse and `git diff --check`.
- Diff inspection proving no Markdown, dependency/lock/configuration, Core/Skill, Consumer runtime/profile, release or package drift.
- No network access.

The handoff MUST map `AC-RCAB-1` through `AC-RCAB-6` to exact tests/evidence and evidence type.

## Stop / escalation conditions

Stop and report `BLOCKED` rather than broadening scope if:

- deterministic projection requires changing the Markdown registry/policy;
- a new dependency or remote service appears necessary;
- a self-reference problem cannot be avoided without changing D047 semantics;
- source-only tooling cannot remain outside the Consumer artifact boundary;
- acceptance would require semantic/model judgment in the executable checker.

## Expected handoff

Before claiming completion, persist `handoffs/T031-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit/push all authorized work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
