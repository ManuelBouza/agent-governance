# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O163  
Canonical-Branch: `develop`  
Current-Work-Unit: T038 accepted/integrated; next action is final independent T039 verification on the restored canonical baseline before resuming T021-R1  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D040 single current protocol-version authority, D042 freshness, D048 final-publication boundary, D052 conformance ownership, D055 launch profiles and D056 progress-note rules remain controlling.
- Current routed Core protocol remains `1.15.0`.
- T034, T035, T036 and T037 remain `ACCEPTED` as historical work units.
- T039 oracle revision `T039-T034-PROTOCOL-HISTORY-TRANSITION-v1` is integrated and controlling. Its first independent verification at HEAD `0197e1899cb0933c7345b373a5dfdbd015d078fc` was correctly `BLOCKED` because canonical develop did not yet contain T038; that handoff is historical blocker evidence only.
- T040 corrected the T038/T039 convergence cycle. Required order is: T039 oracle integrated -> T038 accepted/integrated -> fresh T039 final verification -> T039 acceptance -> resume T021-R1.
- T038 is now `ACCEPTED`. Review: `docs/reviews/T038-R1.md`.
- Accepted T038 canonical verification base: `b565a54213c1343ba73714a3d1d9a78ae1b78bcc`.
- Accepted T038 reconciled implementation anchor: `1c4634ac07214ea293cc45e4caa7998f615e432c`.
- Accepted T038 submitted Executor HEAD: `cb2e7f86fe08ffd80665b4616d71ebad86a425bf`.
- T038 integration PR: `#217`; integration merge: `b02b6bf2a5d5b843b2803fb454b0316779a5dae8`.
- T038 full locked verification on the reconciled candidate passed: `357 passed`; Ruff check/format and `git diff --check` passed; focused T020 and protocol-derived asset coverage passed.
- T038 source Consumer STATE/CAPABILITIES templates are version-neutral (`protocol_version: null`); bootstrap materializes concrete installed identity from validated packaged Core; installed validation remains strict against Core.
- T038 does not change Core, T021, CLI command names, dependency/toolchain configuration or artifact builder behavior.
- Orchestrator process incident: after the Human supplied T038 submitted HEAD `cb2e7f86...`, Orchestrator accidentally appended Markdown commit `fb3146cdc80968fa0a583a7a8884635cac193350` to the represented Executor branch. That successor commit is non-authoritative, was excluded from integration, and represented history was not force-pushed or rewritten. PR #217 integrated from a separate Orchestrator branch created exactly at `cb2e7f86...`.
- Human Owner explicitly resumed T021 on 2026-08-24. T021 remains `REWORK_REQUIRED` under `docs/reviews/T021-R1.md`; its represented branch/history must remain preserved. Its pending semantic defect remains the AC-T021-2 direct unsupported-`Profile` fail-closed boundary.
- T021 remains paused until T039 final acceptance completes this convergence chain. T022 remains `BLOCKED` until T021 acceptance. MG1/T023 and later unified-refactor work remain ineligible.

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

## T039 next verification identity

```text
Task: T039
Status: ORACLE REVISION INTEGRATED / FINAL VERIFICATION REQUIRED
Task Contract: docs/tasks/T039-t034-protocol-history-oracle-transition.md
Oracle asset: tests/test_t034_native_sdd_conformance.py
Oracle revision: T039-T034-PROTOCOL-HISTORY-TRANSITION-v1
Prior blocked verification HEAD: 0197e1899cb0933c7345b373a5dfdbd015d078fc
Expected new verification branch: verify/t039-t034-oracle-transition
Expected handoff: handoffs/T039-executor-handoff.json
Required action: fresh read-only Code Review & Verify from canonical develop after T038 acceptance/integration; handoff-only mutation permitted
```

## T038 accepted identity

```text
Task: T038
Status: ACCEPTED
Task Contract: docs/tasks/T038-protocol-derived-consumer-asset-versioning.md
Review: docs/reviews/T038-R1.md
Submitted Executor HEAD: cb2e7f86fe08ffd80665b4616d71ebad86a425bf
Integration PR: #217
Integration merge: b02b6bf2a5d5b843b2803fb454b0316779a5dae8
```

## T021 paused identity

```text
Task: T021
Status: REWORK_REQUIRED / PAUSED UNTIL T039 FINAL ACCEPTANCE
Task Contract: docs/tasks/T021-consumer-profile-abstraction-zero-drift.md
Review authority: docs/reviews/T021-R1.md
Represented branch: refactor/t021-consumer-profile-abstraction
Reconciliation HEAD: f078928734be4ed0d272821955ba4d8ccdd7cd53
Blocked submitted HEAD: b2ec49e210a752fa539832e06b48b2bcdc00a8dd
Pending semantic correction: AC-T021-2 direct unsupported-Profile fail-closed boundary
```

## Next action

1. Integrate this T038 acceptance/checkpoint branch into `develop` through PR.
2. Refresh canonical `develop` identity.
3. Show D055 profile for T039 final verification: Codex `NEW`, GPT-5.6 Luna, Low; this is read-only independent verification with no product implementation expected.
4. Launch T039 from fresh canonical `develop` using only pointer `docs/tasks/T039-t034-protocol-history-oracle-transition.md` plus D042 freshness.
5. Executor performs T039 Code Review & Verify only; it may persist/push `handoffs/T039-executor-handoff.json` but must make no product/oracle/Markdown changes.
6. Orchestrator independently reviews the new T039 remote HEAD. If focused T034, full locked pytest, Ruff check/format and `git diff --check` are green with no semantic drift, accept T039 and persist closure.
7. After T039 acceptance, resume T021-R1 on its represented history according to its existing authority; do not recreate/rewrite the branch.
8. Do not start T022 or later unified-refactor work before T021 acceptance.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not treat Orchestrator commit `fb3146cdc80968fa0a583a7a8884635cac193350` as T038 Executor evidence; do not force-rewrite the represented T038 or T021 branch; do not rerun T038 unless a new concrete defect requires re-entry; do not mutate product/oracle semantics during T039 final verification; do not resume T021 before T039 final acceptance; do not start T022 before T021 acceptance; do not write directly to `main`/`develop`.
