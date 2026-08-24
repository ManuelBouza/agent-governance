# T037 — Canonical Verification Baseline Restoration

## Identity

- Task ID: `T037`
- Status: `PLANNED`
- Type: `executor-implementation`
- Base branch: `develop`
- Expected topic branch: `fix/t037-canonical-verification-baseline-restoration`
- Expected executor handoff: `handoffs/T037-executor-handoff.json`
- SDD-Profile: `STANDARD`
- Test-Authorship-Mode: `executor-implementation`
- Assurance-Class: `deterministic-baseline, repository-integrity, formatting`
- Verification-Planes: `static, deterministic, portability`
- Release-Impact: `restores the canonical green baseline required before T036 acceptance and D040 Phase-B`

## Objective

Restore the canonical native-Windows verification baseline reported red by T036 without changing product semantics.

T037 is upstream baseline maintenance. It is not T036 oracle rework and does not activate D054.

## Trigger / evidence

The T036 Executor handoff at `handoffs/T036-executor-handoff.json` on submitted HEAD `7919f6050d9d67b3ca27c9d49b9a0f4dd32f6160` reports:

- focused T035/T036 oracle PASS (`6 passed`);
- full pytest BLOCKED only by two `tests/test_repository_context.py` failures because committed `baselines/repository-context-manifest-v1.json` is not canonical;
- `ruff check .` PASS;
- `ruff format --check .` BLOCKED because 14 pre-existing files would be reformatted;
- `git diff --check` PASS.

The current committed repository-context manifest records an older `docs/orchestrator/CHECKPOINT.md` identity, while canonical `develop` has advanced through O154. The manifest is therefore expected to require deterministic regeneration from current tracked repository state.

## Controlling references

- `AGENTS.md`
- `docs/tasks/T036-d054-phase-b-oracle-transition.md`
- `handoffs/T036-executor-handoff.json`
- `tests/test_repository_context.py`
- `tools/repository_context.py`
- `baselines/repository-context-manifest-v1.json`
- current repository Ruff configuration and locked toolchain

## Requirement / specification delta

### MODIFIED

- **R-T037-1 — canonical manifest refresh**: regenerate `baselines/repository-context-manifest-v1.json` using the repository-authoritative deterministic context tooling against the exact current T037 implementation baseline; do not hand-edit digest/identity fields.
- **R-T037-2 — formatter baseline restoration**: make `uv run --locked ruff format --check .` pass by applying only formatter-equivalent mechanical changes to the exact files identified by the locked Ruff formatter.

### PRESERVED

- **R-T037-P1** — no normative/product/runtime/test semantics change.
- **R-T037-P2** — no Markdown semantic edits; if Ruff touches Markdown-unrelated Python formatting, changes must be mechanically equivalent only.
- **R-T037-P3** — no T035/T036 oracle assertion changes.
- **R-T037-P4** — no protocol version, Core routing, Consumer CLI, recipe/runbook behavior or package capability changes.
- **R-T037-P5** — do not modify files merely to reduce diff noise; only canonical manifest regeneration and exact formatter-required mechanical normalization are authorized.
- **R-T037-P6** — if any failing test or formatter change requires semantic code/test/config modification, stop and return `BLOCKED` for Orchestrator re-entry.

## Controlling Design

### 1. Manifest repair uses the canonical generator

Use the existing `tools/repository_context.py` generation/validation semantics. The persisted manifest must be a deterministic projection of the current registered context, not a manually repaired snapshot.

### 2. Formatting repair is semantics-preserving

Use the locked repository Ruff formatter as the authority for formatter output. Do not combine formatting with refactoring, renaming, import redesign, fixture changes, test expectation changes or logic changes.

Review the resulting diff to prove formatting-only equivalence. If a formatter result appears to alter material string/data semantics, block rather than normalize it blindly.

### 3. Baseline convergence

After the authorized repairs, the same native-Windows canonical commands that blocked T036 must be green. T037 does not waive or reinterpret those gates.

## Authorized scope

- `baselines/repository-context-manifest-v1.json`;
- only non-Markdown files mechanically changed by the locked Ruff formatter when required for repository-wide `ruff format --check .` convergence;
- supplementary executor-owned regression tests only if required to prove a purely mechanical baseline repair without changing semantics;
- `handoffs/T037-executor-handoff.json`.

## Explicit exclusions

- committed Markdown edits;
- any T035/T036 oracle edit;
- product/runtime feature changes;
- protocol/Core/Skill activation;
- test expectation weakening/removal;
- broad refactoring or cleanup beyond exact formatter output;
- dependency/tool-version changes;
- T021/T022 resumption;
- direct writes to `develop`/`main`.

## Acceptance criteria

### AC-T037-1 — manifest canonical

Repository-context canonicality tests pass with the regenerated committed manifest.

### AC-T037-2 — formatting baseline green

`uv run --locked ruff format --check .` passes repository-wide.

### AC-T037-3 — deterministic suite green

`uv run --locked pytest` passes completely on the supported native-Windows baseline.

### AC-T037-4 — static checks green

`uv run --locked ruff check .` and `git diff --check` pass.

### AC-T037-5 — semantic zero-drift

Code Review & Verify confirms every non-manifest content change is formatter-equivalent only and no T035/T036 oracle/product semantics changed.

### AC-T037-6 — T036 blocker removed, not bypassed

After T037 integration, T036 can be independently re-verified from fresh canonical `develop`; T037 itself does not accept T036.

## Verification / trace

```text
R-T037-1 -> repository-context canonicality tests + full pytest
R-T037-2 -> locked Ruff format check + diff review
R-T037-P1..P6 -> git diff review + focused T035/T036 oracle + full suite
```

Required evidence in handoff:

- exact base SHA and submitted HEAD;
- exact files changed and classification `manifest-regeneration` or `formatter-only`;
- focused `tests/test_repository_context.py` result;
- focused T035/T036 oracle result;
- full pytest result;
- Ruff check/format results;
- `git diff --check` result;
- technical review statement confirming zero semantic drift.

## Stop / re-entry conditions

Return `BLOCKED` rather than expanding scope if:

- canonical manifest regeneration requires changing context-map/registry semantics;
- a repository-context failure remains after deterministic regeneration;
- Ruff requires a semantic code/test/config change rather than formatter-only normalization;
- another independent canonical failure appears;
- any T035/T036 oracle or protocol/Core change appears necessary.

## Expected handoff

Before terminal status, persist, commit and push `handoffs/T037-executor-handoff.json`. Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T037-executor-handoff.json
BRANCH: fix/t037-canonical-verification-baseline-restoration
HEAD: <pushed-commit-sha>
```
