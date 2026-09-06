# T060 — Governance Artifact Asset Completeness

## Identity

- Task ID: `T060`
- Status: `READY`
- Type: `bugfix / artifact packaging`
- Base branch: `develop`
- Expected implementation branch: `fix/t060-governance-artifact-asset-completeness`
- Expected executor handoff: `handoffs/T060-executor-handoff.json`
- SDD-Profile: `STANDARD`
- Test-Authorship-Mode: `executor-implementation`
- Blocking work: T059 final verification, then T058 re-entry

## Explore / Frame

T059 corrected the reference-integrity false positive and passes its focused verification, but the full repository suite still exposes one independent baseline defect in the Governance Skill artifact builder.

`governance-skill/assets/REPOSITORY-BRANCH-PROTECTION.md` is a tracked canonical source asset. `src/agent_governance/artifact.py` packages Skill assets through the explicit `SKILL_SOURCE_FILES` allowlist, but that allowlist omits this asset. Consequently the generated artifact does not reproduce the canonical source inventory and `tests/test_governance_artifact.py::test_repeated_builds_have_identical_verified_identity` fails.

This is an artifact-packaging completeness defect. The canonical Markdown asset itself is not defective and must not be edited merely to satisfy packaging.

## Specify

### ADDED — T060-R1 package canonical branch-protection asset

The Governance Skill artifact builder SHALL include:

```text
governance-skill/assets/REPOSITORY-BRANCH-PROTECTION.md
```

in the generated artifact at:

```text
assets/REPOSITORY-BRANCH-PROTECTION.md
```

with byte-for-byte content equality to the canonical source file.

### PRESERVED — T060-P1 explicit artifact source boundary

The builder SHALL preserve the existing explicit package-source boundary. This task does not authorize replacing the current explicit source-file selection model with broad recursive copying of all Skill files.

### PRESERVED — T060-P2 artifact identity and determinism

Artifact inventory ordering, payload digest, identity digest, source commit handling, protocol version handling, and deterministic repeated-build semantics SHALL remain unchanged except for the expected inclusion of the newly packaged canonical asset.

### PRESERVED — T060-P3 no Markdown semantic changes

Do not edit `governance-skill/assets/REPOSITORY-BRANCH-PROTECTION.md` or any other committed Markdown. The repair is packaging code/test work only.

### PRESERVED — T060-P4 no T059/T058 mutation

T059 and T058 implementation/handoff files remain out of scope. Their blocked state is resolved only after this baseline repair is integrated and each work unit is revalidated under its own contract.

## Design

Keep the implementation minimal and within the existing artifact-builder architecture.

Expected implementation surface:

- `src/agent_governance/artifact.py`;
- `tests/test_governance_artifact.py`;
- `handoffs/T060-executor-handoff.json`.

The preferred implementation is to add the canonical relative asset path to the existing `SKILL_SOURCE_FILES` allowlist and update focused expectations/regression coverage so the artifact proves byte-for-byte inclusion.

Do not add dependencies, introduce a generalized package-discovery mechanism, or alter the canonical asset contents.

## Plan & Trace

1. Reproduce the artifact completeness failure from exact current `develop`.
2. Confirm the canonical source asset exists and is tracked at `governance-skill/assets/REPOSITORY-BRANCH-PROTECTION.md`.
3. Add or update focused regression coverage proving the generated `assets/REPOSITORY-BRANCH-PROTECTION.md` exists and matches source bytes.
4. Implement the smallest explicit allowlist correction in `src/agent_governance/artifact.py`.
5. Run focused artifact tests.
6. Run the complete repository quality gate.
7. Persist Code Review & Verify evidence in the T060 handoff and push the implementation branch.

Trace:

- T060-R1 -> `SKILL_SOURCE_FILES` correction + artifact byte-equality regression.
- T060-P1 -> changed implementation remains explicit allowlist based.
- T060-P2 -> existing deterministic identity/build tests remain green.
- T060-P3 -> changed-path verification contains no Executor-authored Markdown.
- T060-P4 -> changed-path verification contains no T059/T058 files.

## Authorized scope

Executor may modify only:

- `src/agent_governance/artifact.py`;
- `tests/test_governance_artifact.py`;
- `handoffs/T060-executor-handoff.json`.

Any need to change another file is a stop/re-entry condition.

## Explicit exclusions

Executor MUST NOT:

- edit committed Markdown;
- change the contents or semantics of `governance-skill/assets/REPOSITORY-BRANCH-PROTECTION.md`;
- replace the explicit `SKILL_SOURCE_FILES` model with recursive/generalized discovery;
- modify T059 or T058 files;
- add dependencies or configuration changes;
- weaken artifact identity, inventory, or deterministic-build assertions.

## Acceptance criteria

- **AC-T060-1:** generated artifact contains `assets/REPOSITORY-BRANCH-PROTECTION.md`.
- **AC-T060-2:** generated asset bytes equal canonical source bytes.
- **AC-T060-3:** repeated-build identity/inventory test passes.
- **AC-T060-4:** existing artifact source-boundary and identity semantics remain green.
- **AC-T060-5:** full repository quality gate passes from a clean remote-derived worktree.
- **AC-T060-6:** changed paths stay within authorized scope; no Markdown, T059, or T058 files are modified by Executor.

## Verification

Minimum final verification:

```text
uv run --locked python -m pytest tests/test_governance_artifact.py
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python tools/code_health.py check
uv run --locked python -m pytest
git diff --check
```

Before recording the full-suite result, verification must run from a clean worktree reconstructed from the canonical remote branch state and record `git status --porcelain` as clean before execution.

The handoff must record exact base SHA, implementation HEAD, focused/full-suite results, changed paths, confirmation of source/destination byte equality for the branch-protection asset, and confirmation that no T059/T058 files were modified.

## Stop / SDD re-entry conditions

Stop and report `BLOCKED` if:

- the canonical asset cannot be packaged without changing its contents or governance semantics;
- the correct solution requires generalized artifact discovery or a dependency/configuration change;
- the artifact identity model would need semantic redesign;
- another independent baseline failure remains after this repair.

## Expected handoff

Persist:

`handoffs/T060-executor-handoff.json`

Return only:

```text
STATUS: DONE | BLOCKED
HANDOFF: handoffs/T060-executor-handoff.json
BRANCH: <branch>
HEAD: <pushed-head>
```
