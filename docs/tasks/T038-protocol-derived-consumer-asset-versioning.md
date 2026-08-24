# T038 — Protocol-Derived Consumer Asset Versioning

## Identity

- Task ID: `T038`
- Status: `PLANNED`
- Type: `executor-implementation`
- Base branch: `develop`
- Expected topic branch: `fix/t038-protocol-derived-consumer-assets`
- Expected executor handoff: `handoffs/T038-executor-handoff.json`
- SDD-Profile: `STANDARD`
- Test-Authorship-Mode: `executor-implementation`
- Assurance-Class: `deterministic-baseline, compatibility, protocol-migration`
- Verification-Planes: `static, deterministic, package, portability`
- Release-Impact: `restores the canonical T020 artifact/bootstrap baseline after Protocol 1.15.0 activation without changing Consumer CLI semantics`

## Objective

Restore the canonical Consumer artifact/bootstrap baseline by eliminating independently authored exact-current protocol literals from package templates and T020 verification.

`governance-core/GOVERNANCE.md` remains the single current protocol-version authority under D040. Consumer bootstrap must materialize the current version from that Core authority into installed coordination state rather than requiring manual synchronization of `governance-skill/assets/*.template.json` whenever Core advances.

T038 is upstream baseline repair. It does not implement T021-R1, source-maintainer behavior, a new protocol bump, or a Consumer CLI expansion.

## Trigger / evidence

Fresh T021-R1 execution on native Windows reconciled the represented T021 branch with canonical `develop@bfac31d4f7daf14ef04ece3d3e881d96c4fab0c1` and then stopped before rework because the frozen T020 artifact gate is red on clean canonical `develop`:

- `tests/test_governance_artifact.py`: `2 failed, 2 passed` on clean canonical develop;
- built artifact identity derives Core `Protocol-Version: 1.15.0` correctly;
- `governance-skill/assets/STATE.template.json` still contains `"protocol_version": "1.14.0"`;
- `governance-skill/assets/CAPABILITIES.template.json` still contains `"protocol_version": "1.14.0"`;
- bootstrap fails closed because package asset protocol identity does not match Core `1.15.0`;
- T020 tests also contain free-standing exact-current `1.14.0` expectations.

This is the D040 cross-owner synchronization hazard recurring in Consumer asset/template form. Replacing those literals with `1.15.0` would repair only the current incident and would leave the hazard intact for the next legitimate protocol transition.

## Controlling references

- `AGENTS.md`
- `docs/decisions/D040-atomic-protocol-migration-and-single-version-authority.md`
- `docs/reviews/D054-PHASE-B-R1.md`
- `docs/tasks/T020-self-contained-build-artifact-and-identity.md`
- `docs/tasks/T021-consumer-profile-abstraction-zero-drift.md`
- `docs/reviews/T021-R1.md`
- `handoffs/T021-executor-handoff.json` at blocked HEAD `b2ec49e210a752fa539832e06b48b2bcdc00a8dd`
- `governance-core/GOVERNANCE.md`
- `governance-skill/assets/STATE.template.json`
- `governance-skill/assets/CAPABILITIES.template.json`
- `src/agent_governance/engine.py`
- `src/agent_governance/artifact.py`
- `tests/test_governance_artifact.py`

## Requirement / specification delta

### MODIFIED

- **R-T038-1 — version-neutral package templates**: source `STATE.template.json` and `CAPABILITIES.template.json` MUST no longer encode an independently authored exact current protocol version. Their source representation must carry an explicit unbound value (`protocol_version: null`) that cannot be mistaken for current Governance authority.
- **R-T038-2 — Core-derived bootstrap materialization**: bootstrap MUST derive the current protocol version from canonical packaged Core and deterministically materialize that value into installed `.agent-coordination/STATE.json` and `.agent-coordination/CAPABILITIES.json` before ordinary validation. Installed documents MUST contain a strict SemVer equal to packaged Core.
- **R-T038-3 — template validation**: package-asset validation MUST fail closed unless the two source templates have the exact version-neutral contract required by R-T038-1 and otherwise satisfy their existing structural requirements. A concrete current version embedded in either source template is invalid package input.
- **R-T038-4 — derived T020 verification**: deterministic artifact/bootstrap tests MUST derive current protocol expectations from `governance-core/GOVERNANCE.md` or from artifact identity that itself derives from Core. They MUST NOT retain a free-standing mutable literal for the current protocol version.

### PRESERVED

- **R-T038-P1** — `governance-core/GOVERNANCE.md` remains the sole current protocol-version authority and remains `1.15.0`; T038 does not bump or reinterpret protocol semantics.
- **R-T038-P2** — the stable Consumer CLI command set remains exactly `{bootstrap, validate, state, event, skill, ecosystem, archive}`.
- **R-T038-P3** — a bootstrapped Consumer repository still receives concrete current protocol identity in its installed STATE/CAPABILITIES files; only source-template binding mechanics change.
- **R-T038-P4** — T020 self-contained artifact behavior, source independence, reproducible identity, payload isolation, installed-footprint semantics and rollback reference remain intact.
- **R-T038-P5** — T021 implementation/rework semantics and represented T021 branch are untouched by T038.
- **R-T038-P6** — no committed Markdown may be edited by the Executor; no Skill activation/description, profile routing, source-maintainer behavior, release promotion, dependency/toolchain or unrelated RCAB behavior changes are authorized.

## Controlling Design

### 1. Separate template state from installed state

The source asset templates are reusable inputs, not snapshots of current protocol authority. `protocol_version: null` represents that the template is intentionally unbound before bootstrap.

The installed coordination documents are concrete runtime state. Their `protocol_version` is materialized from the packaged `governance-core/GOVERNANCE.md` authority during bootstrap.

```text
Core GOVERNANCE.md Protocol-Version
             |
             +--> artifact identity protocol_version
             |
             +--> bootstrap materialization
                    +--> installed STATE.json protocol_version
                    +--> installed CAPABILITIES.json protocol_version

source templates: protocol_version = null
```

No reverse flow from asset/template/test literal to Core is permitted.

### 2. Materialize deterministically before installed validation

Bootstrap may parse the two JSON templates, bind the already-validated Core version, and serialize deterministic JSON with the repository's established formatting/newline conventions. Other asset files remain copied under existing semantics.

Do not weaken installed validation: once materialized, installed STATE/CAPABILITIES must still be required to equal current packaged Core.

### 3. Tests verify consequences, not duplicate authority

T020 artifact identity assertions and installed-state assertions must compare against a value parsed/derived from Core (or the artifact identity derived from Core), not against an authored `1.15.0` replacement literal.

Add negative/structural coverage sufficient to prevent reintroduction of a concrete current-version value into the two source templates.

### 4. Baseline restoration precedes T021-R1

T038 must independently make canonical `develop` green. It must not absorb or fix the T021 direct-`Profile` bypass. After T038 acceptance/integration, T021-R1 is relaunched on its already reconciled represented branch and performs its own correction/verification.

## Authorized scope

- `governance-skill/assets/STATE.template.json`;
- `governance-skill/assets/CAPABILITIES.template.json`;
- `src/agent_governance/engine.py` only as required for version-neutral template validation/materialization;
- `src/agent_governance/artifact.py` only if a minimal change is technically required to preserve the Core-derived artifact identity contract;
- executor-owned deterministic tests required to prove R-T038-1 through R-T038-4 and preserved T020 behavior;
- `handoffs/T038-executor-handoff.json`.

## Explicit exclusions

- committed Markdown edits;
- any `governance-core/*.md` edit or protocol-version bump;
- replacing `1.14.0` with a newly duplicated current `1.15.0` literal as the repair strategy;
- T021 profile/rework implementation or test changes specific to AC-T021-2;
- source-maintainer/T022 behavior;
- Consumer CLI command additions/removals;
- Skill activation/description changes;
- release/version promotion unrelated to the derived protocol identity;
- dependency, lockfile or tool-version changes;
- RCAB/context-manifest work;
- direct writes to `develop` or `main`.

## Acceptance criteria

### AC-T038-1 — no mutable current-version template authority

Both source JSON templates use the version-neutral `protocol_version: null` contract, and deterministic coverage rejects a concrete current version in those source-template positions.

### AC-T038-2 — concrete installed identity derives from Core

Bootstrap from source-package and built-artifact paths succeeds and produces installed STATE/CAPABILITIES protocol versions exactly equal to canonical packaged Core `Protocol-Version`.

### AC-T038-3 — T020 artifact baseline green

The unchanged T020 behavioral contract is restored: reproducible artifact identity, source-independent execution, artifact isolation and all seven stable Consumer commands pass.

### AC-T038-4 — D040 single authority preserved

Code Review & Verify confirms no executor-owned test/helper/template contains a free-standing mutable exact-current protocol literal whose manual synchronization is required for the canonical suite to remain green after a future Core bump.

Historical fixture values or explicit migration-transition values remain allowed only when their historical/transition role is mechanically clear.

### AC-T038-5 — canonical deterministic baseline green

Full locked pytest passes on supported native Windows; locked Ruff check/format and `git diff --check` pass.

### AC-T038-6 — T021 remains separate

The T021 branch and T021-R1 defect are not modified by T038. After T038 acceptance/integration, T021 can resume from its represented reconciled branch and independently satisfy T021-R1.

## Verification / trace

```text
R-T038-1 -> source-template structural/negative tests
R-T038-2 -> source bootstrap + artifact-only bootstrap/validate + installed STATE/CAPABILITIES assertions
R-T038-3 -> tests/test_governance_artifact.py + frozen T020 regression surface
R-T038-4 -> code/test diff review + current-version-literal scan constrained by D040 semantics
R-T038-P1..P6 -> complete diff review + full deterministic/static suite
```

Required handoff evidence:

- exact base SHA and submitted HEAD;
- exact files changed;
- focused T020 artifact test result;
- focused new/updated protocol-derived asset tests;
- full locked pytest result on native Windows;
- locked Ruff check/format result;
- `git diff --check` result;
- technical review statement confirming Core remains the sole current-version authority and no T021 semantic change occurred;
- unresolved findings/upstream re-entry, if any.

## Stop / re-entry conditions

Return `BLOCKED` rather than expanding scope if:

- restoring T020 requires changing Core protocol semantics or another Markdown-owned contract;
- installed Consumer behavior must change beyond protocol-version derivation/materialization;
- a concrete exact-current literal appears technically necessary as a second authority;
- T021/profile/source-maintainer changes appear necessary;
- another independent canonical baseline failure remains after the authorized repair;
- dependency/toolchain changes become necessary.

## Expected handoff

Before terminal status, persist, commit and push `handoffs/T038-executor-handoff.json`. Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T038-executor-handoff.json
BRANCH: fix/t038-protocol-derived-consumer-assets
HEAD: <pushed-commit-sha>
```
