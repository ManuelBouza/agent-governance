# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O043  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T001, T002, T003, T005 and T007 are `ACCEPTED` and integrated. T004 remains terminal `CANCELLED_BY_HUMAN` under D037.

D039 — Evidence-Driven Governance Learning Loop (EGLL) — is `ACCEPTED`.

T009 implementation at `test/protocol-version-baseline-alignment@e0c80c62c1c543504719616c547d4df03d1b3d21` is `ACCEPTED` by `docs/reviews/T009-R1.md`, pending implementation PR integration and post-integration cleanup.

T008 remains `REWORK_REQUIRED` only because its first run encountered the pre-existing protocol-version baseline drift. After T009 is integrated and cleaned, T008 resumes on its existing branch, incorporates current `develop`, reruns its original gates, refreshes its handoff, and returns for re-review. T006 remains `READY` after T008. D036 remains after T006.

## Persisted executor-instruction invariant

```text
prompt = bootstrap transport only
persisted contract + referenced Git policy = complete instruction
```

Use exactly one persisted contract pointer for delegated work. Prompts MUST NOT carry concrete task/operation semantics absent from Git.

## L001 — CONTROL_PLANNED

Learning record: `docs/learning/L001-protocol-version-baseline-drift.md`  
Fingerprint: `verification.regression.protocol_version_drift`

T009 provides the accepted corrective implementation. L001 MUST NOT become `VERIFIED` until the correction is integrated into `develop` and T008 subsequently passes its original full verification suite on that corrected baseline.

## T009 — ACCEPTED, PENDING INTEGRATION

Task Contract: `docs/tasks/T009-protocol-version-baseline-alignment.md`  
Review: `docs/reviews/T009-R1.md`  
Executor branch: `test/protocol-version-baseline-alignment`  
Reviewed HEAD: `e0c80c62c1c543504719616c547d4df03d1b3d21`  
Implementation anchor: `4d3b2cc440e7f8e0b3d6f720d12540231abed2c0`

Accepted diff is limited to:

- `tests/_helpers.py`: verifier expectation `1.11.0` -> `1.12.0`;
- `tests/test_execution_control_contract.py`: redundant fixed-literal assertion removed;
- `handoffs/T009-executor-handoff.json`.

Deterministic mismatch detection remains: tests continue to parse Core `Protocol-Version` and compare it to the single test-side verifier expectation.

Reported gates:

```text
focused protocol/version tests: 47 passed
full pytest: 126 passed
ruff check: PASS
ruff format --check: PASS
```

No Markdown/Core/T008/T006/D036/dependency/config/network/model/provider scope expansion is accepted.

## T008 — REWORK_REQUIRED AFTER T009

Task Contract: `docs/tasks/T008-egll-deterministic-learning-detectors.md`  
Review: `docs/reviews/T008-R1.md`  
Current task branch: `test/egll-deterministic-learning-detectors`

After T009 integration and cleanup, T008 SHALL incorporate current `develop` into that existing task branch, rerun the original focused/full/Ruff gates, refresh `handoffs/T008-executor-handoff.json`, commit/push, and return for re-review. No detector semantic changes are authorized by this sequencing step.

## T006 — READY AFTER T008

Task Contract: `docs/tasks/T006-d035-deterministic-security-verification-contract.md`

T006/D035 semantics remain unchanged. Do not fold T008/T009 or D036 into T006.

## Branch lifecycle

```text
merge -> freeze -> cleanup
new work -> new branch from current develop
```

Merged topic branches are frozen. Cleanup authority must be persisted through Operational Contracts.

## Procedural audit history

Preserve the existing audit history, including T007 classify-before-delete recovery, Orchestrator direct-write incidents, the post-merge reuse of `docs/t007-post-integration`, and the accidental `46050487d3a066afd37cf340ccd58ab09daddfb9` direct write corrected by PR #61. Do not rewrite or hide those records.

## Next Action

1. Integrate this T009 acceptance Markdown change; freeze its source branch.
2. Open and merge the exact accepted T009 implementation HEAD to `develop`.
3. Persist and integrate an Operational Contract covering retirement of the T009 acceptance branch, T009 implementation branch, and the cleanup-contract branch itself; execute and verify that cleanup.
4. Update L001 to `CONTROL_INTEGRATED` when T009 is integrated; do not mark `VERIFIED` yet.
5. Resume T008 exactly per T008-R1, then re-review.
6. After T008 acceptance/integration/cleanup, resume T006 unchanged.
7. Do not start D036 until T006 closes.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. if T009 integration/cleanup is incomplete, load `docs/reviews/T009-R1.md`, T009 Task Contract, L001, and applicable Operational Contract;
2. for T008 re-review load T008 Task Contract, T008-R1, current handoff, D039 and `docs/GOVERNANCE-LEARNING.md`;
3. after T008 closes, load T006 + D035 + `governance-core/SECURITY.md`;
4. do not reload older task history absent regression/audit need.

## Do Not Load or Do

- Do not delete `main` or `develop`.
- Do not append commits to a merged topic branch.
- Do not place concrete executor instructions in chat when absent from the persisted contract.
- Do not mark L001 `VERIFIED` before T008 passes on the corrected baseline.
- Do not modify T008 detector semantics merely to consume T009.
- Do not fold T008/T009 into T006 or D036.
- Do not hide procedural/audit history.
