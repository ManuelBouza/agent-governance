# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O044  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T001, T002, T003, T005 and T007 are `ACCEPTED` and integrated. T004 remains terminal `CANCELLED_BY_HUMAN` under D037.

D039 — Evidence-Driven Governance Learning Loop (EGLL) — is `ACCEPTED`.

T009 is `ACCEPTED` and integrated. PR #63 integrated `docs/reviews/T009-R1.md`; PR #64 integrated exact accepted executor HEAD `e0c80c62c1c543504719616c547d4df03d1b3d21` into `develop` at `fdb815394fd5ef91bd513f3701fa99c895536b8b`.

L001 is `CONTROL_INTEGRATED`, not `VERIFIED`. T008 remains `REWORK_REQUIRED` until T009 post-integration cleanup completes and T008 reruns successfully on current `develop` without detector-semantic changes.

T006 remains `READY` after T008. D036 remains after T006.

## Persisted executor-instruction invariant

```text
prompt = bootstrap transport only
persisted contract + referenced Git policy = complete instruction
```

Use exactly one persisted Task Contract or Operational Contract pointer. Chat MUST NOT supply concrete semantics absent from Git.

## OP003 — READY after PR #65 integration

Operational Contract:

`docs/operations/OP003-retire-t009-integration-branches.md`

OP003 covers only merged branches from:

- PR #63 — `docs/t009-acceptance`;
- PR #64 — `test/protocol-version-baseline-alignment`;
- PR #65 — `docs/t009-post-integration-cleanup`.

It explicitly preserves `main`, `develop`, and active T008 branch `test/egll-deterministic-learning-detectors`.

## L001 — CONTROL_INTEGRATED

Learning record: `docs/learning/L001-protocol-version-baseline-drift.md`  
Fingerprint: `verification.regression.protocol_version_drift`

T009 restored the deterministic version-alignment baseline while preserving Core as authority and the test-side value as verifier expectation. L001 becomes `VERIFIED` only after OP003 closes and T008 passes its original focused/full/Ruff gates on the corrected current `develop` baseline.

## T009 — ACCEPTED / INTEGRATED

Task Contract: `docs/tasks/T009-protocol-version-baseline-alignment.md`  
Review: `docs/reviews/T009-R1.md`  
Accepted executor HEAD: `e0c80c62c1c543504719616c547d4df03d1b3d21`  
Integration PR: #64  
Integrated `develop`: `fdb815394fd5ef91bd513f3701fa99c895536b8b`

Accepted implementation changed only:

- `tests/_helpers.py`;
- `tests/test_execution_control_contract.py`;
- `handoffs/T009-executor-handoff.json`.

Reported gates before integration: focused 47 passed; full pytest 126 passed; Ruff check/format PASS.

## T008 — REWORK_REQUIRED AFTER OP003

Task Contract: `docs/tasks/T008-egll-deterministic-learning-detectors.md`  
Review: `docs/reviews/T008-R1.md`  
Active branch: `test/egll-deterministic-learning-detectors`

After OP003 is independently verified, resume T008 on the existing branch. Incorporate current `develop`, rerun the original T008 focused/full/Ruff gates, refresh `handoffs/T008-executor-handoff.json`, commit/push, and return for re-review. No detector-semantic changes are authorized by this step.

## T006 — READY AFTER T008

Task Contract: `docs/tasks/T006-d035-deterministic-security-verification-contract.md`

T006/D035 semantics remain unchanged. Do not fold T008/T009 or D036 into T006.

## Branch lifecycle

```text
merge -> freeze -> cleanup
new work -> new branch from current develop
```

Merged branches are frozen; operational cleanup uses persisted Operational Contracts only.

## Procedural audit history

Preserve existing audit history, including T007 classify-before-delete recovery, Orchestrator direct-write incidents, post-merge reuse of `docs/t007-post-integration`, and accidental `46050487d3a066afd37cf340ccd58ab09daddfb9` direct write corrected by PR #61. Do not rewrite or hide those records.

## Next Action

1. Integrate PR #65 and freeze `docs/t009-post-integration-cleanup`.
2. Launch OP003 using only the Operational Contract pointer; independently verify final remote/local branch inventories.
3. Resume T008 exactly per T008-R1 on its existing branch and re-review.
4. If T008 passes and is accepted/integrated/cleaned, mark L001 `VERIFIED` with persisted evidence and resume T006 unchanged.
5. Do not start D036 until T006 closes.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. if OP003 is incomplete, load `docs/operations/OP003-retire-t009-integration-branches.md` plus branch-cleanup policy;
2. for T008 re-review load its Task Contract, T008-R1, current handoff, D039, L001 and `docs/GOVERNANCE-LEARNING.md`;
3. after T008 closes, load T006 + D035 + `governance-core/SECURITY.md`;
4. do not reload older history absent regression/audit need.

## Do Not Load or Do

- Do not delete `main` or `develop`.
- Do not delete or repurpose active T008 branch through OP003.
- Do not append commits to merged topic branches.
- Do not place concrete executor instructions in chat when absent from the persisted contract.
- Do not mark L001 `VERIFIED` before T008 passes on corrected baseline.
- Do not modify T008 detector semantics merely to consume T009.
- Do not fold T008/T009 into T006 or D036.
- Do not hide procedural/audit history.
