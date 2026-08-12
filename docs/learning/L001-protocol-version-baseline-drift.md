# L001 — Protocol-version baseline drift

Learning ID: L001  
State: VERIFIED  
Fingerprint: `verification.regression.protocol_version_drift`

## Detection

Detected during T008 executor verification at executor HEAD `59f0b8bc443636c5a7fbf5d417f185d528cc63e2` against base `bb1a2de8db622141fc975d1c341e82b9bdc4c3c6`.

Affected records:

- T008 — `docs/tasks/T008-egll-deterministic-learning-detectors.md`;
- T008 reviews — `docs/reviews/T008-R1.md`, `docs/reviews/T008-R2.md`, `docs/reviews/T008-R3.md`;
- source protocol declaration — `governance-core/GOVERNANCE.md`;
- deterministic baseline helpers/tests — `tests/_helpers.py`, `tests/test_execution_control_contract.py`;
- corrective task — `docs/tasks/T009-protocol-version-baseline-alignment.md`;
- T009 acceptance — `docs/reviews/T009-R1.md`.

## Factual evidence

At the original T008 base:

- `governance-core/GOVERNANCE.md` declared `Protocol-Version: 1.12.0`;
- `tests/_helpers.py` still declared `SOURCE_PROTOCOL_VERSION = "1.11.0"`;
- `tests/test_execution_control_contract.py` still contained a redundant explicit `1.11.0` assertion;
- T008 full pytest failed independently of its detector implementation.

T009 reproduced the drift before mutation and corrected only the deterministic test baseline. The accepted implementation was integrated by PR #64 into `develop` at `fdb815394fd5ef91bd513f3701fa99c895536b8b`.

## Immediate containment

T008 remained unaccepted while the baseline was red. Its executor correctly returned `PARTIAL` and did not modify unrelated tests or Governance Core outside T008 scope.

## Causal/systemic analysis

Observed condition: a protocol-version bump reached canonical `develop` without the deterministic test baseline that pins the source protocol version being updated in the same executable change lifecycle.

Systemic gap: protocol-version synchronization depended on manual coordination across Markdown/Core authority and non-Markdown deterministic tests. A Markdown-only protocol change could therefore leave `develop` with a known failing deterministic suite until a later executable task discovered it.

This record does not attribute blame to an agent/product. The failure class is repository-level version-authority drift.

## Selected control

T009 restored the deterministic baseline while preserving the authority boundary:

```text
Core Protocol-Version = authority
source test expectation = deterministic verifier of that authority
```

The accepted implementation:

- updated the single test-side `SOURCE_PROTOCOL_VERSION` verifier expectation to `1.12.0`;
- removed the redundant fixed-literal assertion from `tests/test_execution_control_contract.py`;
- preserved tests that parse `governance-core/GOVERNANCE.md` and compare the declaration against the verifier expectation.

Control owner: Agente de IA Ejecutor under T009; acceptance owned by ChatGPT Orchestrator.

## Integrated-control evidence

T009-R1 accepted executor HEAD `e0c80c62c1c543504719616c547d4df03d1b3d21`.

Reported verification before integration:

```text
focused protocol/version tests: 47 passed
full pytest: 126 passed
ruff check: PASS
ruff format --check: PASS
```

PR #64 integrated the exact accepted T009 implementation into `develop`.

## Regression/replay verification

T009 post-integration cleanup completed before the final T008 rerun.

T008 then incorporated the corrected current `develop` baseline and, at final accepted HEAD `79df001b6a20a6f363e34e61093c63fc639479fe`, reported:

```text
focused T008 pytest: 8 passed
full pytest: 134 passed
ruff check: PASS
ruff format --check: PASS
```

T008-R3 independently verified that the detector, fixture, and focused-test blobs were byte-identical to the original reviewed T008 implementation anchor, so the green result was not obtained by weakening or changing detector semantics.

PR #68 integrated the exact accepted T008 HEAD into `develop` at `aff36aa65423b11febb81035d307de966745fee5`.

No second protocol authority or duplicated independent current-version source was introduced.

Therefore the selected control is integrated and the original failure class has deterministic regression evidence on the corrected baseline. L001 is `VERIFIED`.

## Recurrence

A future mismatch between authoritative Core protocol version and deterministic source-test version expectation is the same fingerprint unless evidence establishes a materially different condition.

Any recurrence after this `VERIFIED` state becomes `CONTROL_FAILURE` under D039 and requires re-analysis rather than merely another literal update.
