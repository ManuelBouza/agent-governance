# L001 — Protocol-version baseline drift

Learning ID: L001  
State: CONTROL_PLANNED  
Fingerprint: `verification.regression.protocol_version_drift`

## Detection

Detected during T008 executor verification at executor HEAD `59f0b8bc443636c5a7fbf5d417f185d528cc63e2` against base `bb1a2de8db622141fc975d1c341e82b9bdc4c3c6`.

Affected records:

- T008 — `docs/tasks/T008-egll-deterministic-learning-detectors.md`;
- review — `docs/reviews/T008-R1.md`;
- source protocol declaration — `governance-core/GOVERNANCE.md`;
- deterministic baseline helpers/tests — `tests/_helpers.py`, `tests/test_execution_control_contract.py`.

## Factual evidence

At the reviewed base:

- `governance-core/GOVERNANCE.md` declares `Protocol-Version: 1.12.0`;
- `tests/_helpers.py` declares `SOURCE_PROTOCOL_VERSION = "1.11.0"`;
- `tests/test_execution_control_contract.py` explicitly asserts `SOURCE_PROTOCOL_VERSION == "1.11.0"` and requires the Core declaration to equal that stale constant;
- T008's full pytest therefore reports two failures while its focused detector tests pass.

The T008 diff does not modify any of those pre-existing protocol-version assertions.

## Immediate containment

T008 remains unaccepted. The executor correctly returned `PARTIAL` and did not change unrelated baseline tests or Governance Core outside its Task Contract.

## Causal/systemic analysis

Observed condition: a protocol-version bump reached canonical `develop` without the deterministic test baseline that pins the source protocol version being updated in the same executable change lifecycle.

Systemic gap: protocol-version synchronization currently depends on manual coordination across Markdown/Core authority and non-Markdown deterministic tests. A Markdown-only protocol change can therefore leave `develop` with a known failing deterministic suite until a later executable task discovers it.

This record does not attribute blame to an agent/product. The failure class is repository-level version-authority drift.

## Selected control

Immediate corrective control: T009 will restore the deterministic baseline by aligning the existing protocol-version test expectation with the already-authoritative Core protocol version, without changing protocol semantics.

Preventive control candidate: retain one canonical mechanically checked source-version expectation and ensure future protocol-version changes cannot be treated as integration-complete while deterministic version-alignment verification is stale. T009 SHALL implement the smallest honest regression check permitted by existing test architecture; it MUST NOT create a second protocol authority.

Control owner: Agente de IA Ejecutor under T009; acceptance owned by ChatGPT Orchestrator.

## Verification requirement

This learning case cannot reach `VERIFIED` merely because the stale literal is changed. Verification requires:

1. the canonical full pytest suite is green after T009;
2. a focused deterministic test proves the declared Core protocol version is mechanically aligned with the source-test expectation;
3. T008 subsequently reruns successfully on the corrected baseline;
4. no new protocol authority or duplicated semantic version source is introduced.

## Recurrence

A future mismatch between authoritative Core protocol version and deterministic source-test version expectation is the same fingerprint unless evidence establishes a materially different condition. Recurrence after this case reaches `VERIFIED` becomes `CONTROL_FAILURE` under D039.
