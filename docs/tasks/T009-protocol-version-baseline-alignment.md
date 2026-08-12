# T009 — Protocol-version deterministic baseline alignment

Task ID: T009  
Status: READY  
Type: test/infrastructure  
Base branch: `develop`  
Expected topic branch: `test/protocol-version-baseline-alignment`  
Expected executor handoff: `handoffs/T009-executor-handoff.json`

## Objective

Restore the canonical deterministic test baseline after the already-integrated source protocol version advanced to `1.12.0` while existing non-Markdown tests remained pinned to `1.11.0`.

T009 is a narrow corrective prerequisite for T008. It does not change Governance Core protocol semantics or introduce a new protocol version.

## Controlling references

- `AGENTS.md`
- `governance-core/GOVERNANCE.md`
- `docs/learning/L001-protocol-version-baseline-drift.md`
- `docs/reviews/T008-R1.md`
- `docs/TASK-CONTRACTS.md`
- `docs/EXECUTOR-HANDOFFS.md`
- D037 deterministic code-only verification

## Authorized scope

The Agente de IA Ejecutor may modify only the smallest necessary non-Markdown deterministic test/helper artifacts required to align the source test baseline with the authoritative `Protocol-Version` declared by `governance-core/GOVERNANCE.md`.

Expected affected surfaces are limited to:

- `tests/_helpers.py`;
- `tests/test_execution_control_contract.py`;
- optionally one focused non-Markdown regression test/helper if needed to avoid another stale duplicated literal;
- `handoffs/T009-executor-handoff.json`.

## Explicit exclusions

The executor MUST NOT:

- edit committed Markdown, including `governance-core/GOVERNANCE.md`;
- change the authoritative protocol version or any Governance Core semantics;
- modify T008 implementation files except to inspect them read-only;
- change T006/D035/D036 behavior;
- weaken/remove existing deterministic assertions merely to make the suite green;
- introduce model/network/provider/external-service dependencies;
- add unrelated refactors, dependencies, configuration, CI/ruleset, release, or consumer-footprint changes.

## Invariants

```text
Core Protocol-Version = authority
source test expectation = deterministic verifier of that authority
stale test literal != independent protocol authority
```

The correction MUST preserve a deterministic failure when the tested source protocol declaration and expected current source version disagree.

Prefer the smallest design that avoids creating multiple independently maintained current-version literals inside tests. If repository architecture requires one test-side version constant, it must be clearly a verifier expectation and covered by focused alignment assertions.

## Required execution sequence

1. Start from current `develop` containing this exact T009 contract and L001/T008-R1.
2. Create `test/protocol-version-baseline-alignment` from that revision.
3. Reproduce the current two protocol-version failures before mutation.
4. Make the smallest authorized non-Markdown correction.
5. Run focused protocol/version-alignment tests.
6. Run full pytest.
7. Run Ruff check and Ruff format check.
8. Persist `handoffs/T009-executor-handoff.json` with before/after failure evidence and exact changed-file inventory.
9. Commit/push and return only the canonical minimal executor response.

## Acceptance criteria

ChatGPT accepts T009 only when remote evidence shows:

- no committed Markdown or Governance Core content changed;
- the stale `1.11.0` source-test expectation no longer contradicts authoritative Core `1.12.0`;
- deterministic protocol-version mismatch detection remains present rather than being removed/bypassed;
- the previously failing protocol-version tests pass;
- the full pytest suite passes on the T009 branch;
- Ruff check and Ruff format check pass;
- no unrelated T008/T006/D036/dependency/configuration scope expansion occurred;
- handoff/base/head identity is remotely auditable.

## Verification requirements

At minimum run:

```text
uv run --locked pytest -q tests/test_execution_control_contract.py
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

If protocol-version alignment is also exercised by another focused test, run it and record it in the handoff.

The handoff must include:

- base/branch/head identity;
- exact pre-fix reproduced failures;
- changed-file inventory;
- explanation of how deterministic mismatch detection is preserved;
- exact verification commands/results;
- confirmation of no Markdown/Core/T008/dependency/config/network/model/provider scope expansion;
- any ambiguity or procedural nonconformance.

## Stop / escalation

Return `BLOCKED` or `PARTIAL` instead of guessing if restoring the suite would require changing Core semantics, committed Markdown, unrelated T008 implementation, a new dependency/service, or weakening deterministic version verification.

## Sequencing

T009 executes before T008 rework acceptance.

After T009 is accepted, integrated, and post-integration-cleaned, the T008 executor resumes on its existing task branch by incorporating current `develop`, rerunning the original T008 verification gates, refreshing the handoff, and returning the canonical T008 response. T006 remains after T008.

## Expected handoff

Persist `handoffs/T009-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push it on `test/protocol-version-baseline-alignment`, then return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T009-executor-handoff.json
BRANCH: test/protocol-version-baseline-alignment
HEAD: <pushed-commit-sha>
```
