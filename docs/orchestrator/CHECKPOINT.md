# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O161  
Canonical-Branch: `develop`  
Current-Work-Unit: T039 Orchestrator-owned T034 protocol-history oracle transition; T038 implementation is complete but blocked only by the stale T034 live-current-version assertion  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D040 single current protocol-version authority, D042 freshness, D048 final-publication boundary, D052 conformance ownership, D055 launch profiles and D056 progress-note rules remain controlling.
- Current routed Core protocol is `1.15.0`.
- T034, T035, T036 and T037 remain `ACCEPTED` as historical work units.
- Human Owner explicitly resumed T021 on 2026-08-24. T021 remains `REWORK_REQUIRED`; its represented branch is history-preserved and reconciled, but no T021-R1 semantic correction has been committed because canonical T020 artifact verification was red.
- T038 was planned to restore that T020/canonical package baseline without creating a second current-version authority.
- T038 Executor result at submitted HEAD `6dd2f99c5cc78ddc53f9719b4d2df4dc735d70e7` is `BLOCKED`, with implementation anchor `8aa32b32fb15e01bfbc56e327a910b82b3674c32`, base `a8f458c8d0334edac8d1a9cdeea7418d5cb860d5`, branch `fix/t038-protocol-derived-consumer-assets`, and handoff `handoffs/T038-executor-handoff.json`.
- T038 implementation is internally green on its authorized surface: combined artifact/Consumer suite `46 passed`, focused T020 artifact `4 passed`, focused protocol-derived asset tests `3 passed`, Ruff check/format PASS and `git diff --check` PASS.
- T038 changed only the two Consumer JSON templates, engine materialization/validation, Consumer/T020 tests and handoff. It did not change Core, Markdown, T021, CLI commands or artifact builder behavior.
- T038 source templates now use `protocol_version: null`; bootstrap materializes both installed STATE/CAPABILITIES protocol versions from the already validated packaged Core; T020/current tests derive expectations from Core rather than duplicated literals.
- Full T038 pytest is `356 passed, 1 failed`. The sole failure is Orchestrator-owned `tests/test_t034_native_sdd_conformance.py::test_core_and_artifact_expect_protocol_1_14_with_sdd`, which still requires a newly built artifact from current Core to report historical T034 version `1.14.0`.
- This is a D052 oracle lifecycle defect, not a T038 implementation defect. T034's accepted Task Contract remains authoritative historical evidence that T034 materialized Protocol `1.14.0`; current `governance-core/GOVERNANCE.md` remains sole authority for current protocol identity.
- T039 is persisted at `docs/tasks/T039-t034-protocol-history-oracle-transition.md` with Oracle revision `T039-T034-PROTOCOL-HISTORY-TRANSITION-v1`.
- T039 changes only the single stale temporal assertion in `tests/test_t034_native_sdd_conformance.py`: historical `1.14.0` is proven from the accepted T034 Task Contract, while a current artifact must equal the protocol dynamically derived from current Core. All other T034 oracle semantics remain frozen.
- T038 MUST NOT be integrated or accepted until T039 is independently verified and accepted, then T038 is re-verified against fresh canonical develop containing T039.
- T021 remains blocked pending T038 acceptance. T022 remains blocked until T021 acceptance. MG1/T023 and later unified-refactor work remain ineligible.

## Mandatory Executor prompt transport invariant

Every Executor prompt is pointer-only and includes D042 freshness:

```text
Operate as the Agente de IA Ejecutor for <repository>.

Synchronize with GitHub and establish a safe current local baseline from the canonical remote state before loading repository instructions or execution authority, per D042/RB001. Do not discard unrepresented local work.

Use <canonical/base or represented topic branch as applicable>.

Load current repository instructions, then execute exactly:
<persisted authority path>

Return only the output required by that persisted authority.
```

Do not duplicate Task Contract/review semantics or routine command syntax in the transport prompt.

## D055 launch invariant

Before every Executor prompt, show concrete Executor, `NEW|CONTINUE`, exact recommended model, effort and one-line rationale.

Current Codex mapping:

```text
read-only/repetitive observation -> GPT-5.6 Luna / Low
narrow mechanical implementation -> GPT-5.6 Terra / Low
standard AG implementation/rework -> GPT-5.6 Sol / Medium
complex/high-risk technical work  -> GPT-5.6 Sol / High
exceptional long-horizon work     -> GPT-5.6 Sol / highest mode only when justified
```

## T039 active identity

```text
Task: T039
Status: PLANNED / ORCHESTRATOR-CONFORMANCE GATE
Task Contract: docs/tasks/T039-t034-protocol-history-oracle-transition.md
Oracle asset: tests/test_t034_native_sdd_conformance.py
Oracle revision: T039-T034-PROTOCOL-HISTORY-TRANSITION-v1
Planning/oracle branch: feat/t039-t034-oracle-transition
Expected verification branch: verify/t039-t034-oracle-transition
Expected handoff: handoffs/T039-executor-handoff.json
Purpose: preserve T034 historical 1.14.0 acceptance without pinning future current artifact identity
```

## T038 blocked identity

```text
Task: T038
Status: BLOCKED BY T039 ORACLE TRANSITION
Task Contract: docs/tasks/T038-protocol-derived-consumer-asset-versioning.md
Branch: fix/t038-protocol-derived-consumer-assets
Base: a8f458c8d0334edac8d1a9cdeea7418d5cb860d5
Implementation anchor: 8aa32b32fb15e01bfbc56e327a910b82b3674c32
Submitted HEAD: 6dd2f99c5cc78ddc53f9719b4d2df4dc735d70e7
Handoff: handoffs/T038-executor-handoff.json
Only failing gate: stale D052 T034 exact-current 1.14.0 oracle assertion
```

## T021 blocked identity

```text
Task: T021
Status: REWORK_REQUIRED / BLOCKED BY T038
Task Contract: docs/tasks/T021-consumer-profile-abstraction-zero-drift.md
Review authority: docs/reviews/T021-R1.md
Represented branch: refactor/t021-consumer-profile-abstraction
Reconciliation HEAD: f078928734be4ed0d272821955ba4d8ccdd7cd53
Blocked submitted HEAD: b2ec49e210a752fa539832e06b48b2bcdc00a8dd
Pending semantic correction: AC-T021-2 direct unsupported-Profile fail-closed boundary
```

## Next action

1. Integrate the T039 planning/oracle/checkpoint branch into `develop` through PR after remote diff review.
2. Refresh canonical `develop` identity.
3. Show D055 launch profile for T039 independent verification: Codex `NEW`, GPT-5.6 Luna, Low; no implementation is expected, only bounded Code Review & Verify of one Orchestrator-owned oracle transition.
4. Launch T039 from fresh canonical `develop` using only pointer `docs/tasks/T039-t034-protocol-history-oracle-transition.md` plus D042 freshness.
5. Executor performs only T039 Code Review & Verify and persists/pushes terminal handoff/head.
6. Orchestrator independently reviews and accepts T039 if focused/full canonical verification is green and no other T034 semantic drift exists.
7. Only after T039 acceptance, re-verify T038 from then-current canonical `develop`, preserving its represented implementation history and without semantic redesign.
8. Only after T038 acceptance/integration may T021-R1 resume on its represented branch.
9. Do not start T022 or later program work before T021 acceptance.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not edit any other T034 oracle semantics; do not replace historical `1.14.0` with a new duplicated current `1.15.0` literal; do not mutate T038 implementation while verifying T039; do not integrate T038 before T039 acceptance; do not touch T021 until T038 acceptance; do not start T022 before T021 acceptance; do not write directly to `main`/`develop`.
