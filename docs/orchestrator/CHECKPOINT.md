# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O162  
Canonical-Branch: `develop`  
Current-Work-Unit: T040 sequencing correction integrated next; then T038 re-entry/re-verification before final T039 verification  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D040 single current protocol-version authority, D042 freshness, D048 final-publication boundary, D052 conformance ownership, D055 launch profiles and D056 progress-note rules remain controlling.
- Current routed Core protocol is `1.15.0`.
- T034, T035, T036 and T037 remain `ACCEPTED` as historical work units.
- Human Owner explicitly resumed T021 on 2026-08-24. T021 remains `REWORK_REQUIRED`; its represented branch is history-preserved and reconciled, but no T021-R1 semantic correction has been committed because canonical T020 artifact verification was red.
- T038 implementation exists on represented branch `fix/t038-protocol-derived-consumer-assets`; implementation anchor `8aa32b32fb15e01bfbc56e327a910b82b3674c32`, prior blocked submitted HEAD `6dd2f99c5cc78ddc53f9719b4d2df4dc735d70e7`.
- T038's authorized focused surface was green: combined artifact/Consumer `46 passed`, T020 artifact `4 passed`, protocol-derived assets `3 passed`, Ruff check/format PASS and `git diff --check` PASS. Its sole blocker was the stale T034 live-current-version oracle.
- T039 corrected that D052 oracle temporal defect and is integrated in canonical `develop@43641a0646baf5866c1cd0b58aa237d74f172e42` as Oracle revision `T039-T034-PROTOCOL-HISTORY-TRANSITION-v1`.
- Independent T039 verification submitted HEAD `0197e1899cb0933c7345b373a5dfdbd015d078fc` is `BLOCKED` with no product changes. Its base is exact canonical `develop@43641a0646baf5866c1cd0b58aa237d74f172e42`; branch delta is handoff-only.
- T039 review found the oracle revision itself correct and narrow. Verification remains red because canonical `develop` still lacks the T038 Consumer asset repair; focused T034 bootstrap and dependent full-suite tests fail on the pre-T038 `1.14.0` package assets versus Core `1.15.0`.
- The prior O161 sequence created a circular dependency by requiring T039 acceptance/full green before T038 could re-enter, while canonical full green requires T038.
- T040 is persisted at `docs/tasks/T040-t038-t039-convergence-sequencing-correction.md` and supersedes only that sequencing condition. It changes no T038 product semantics and no T039 oracle semantics.
- Correct order is: T039 oracle revision integrated -> T038 re-entry/re-verification on represented history -> if green, T038 accept/integrate -> fresh T039 verification on resulting canonical develop -> T039 accept -> resume T021-R1.
- The blocked T039 handoff at `0197e189...` MUST NOT be repeated before T038 acceptance/integration.
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

## T040 active identity

```text
Task: T040
Status: PLANNED / ORCHESTRATOR-CONVERGENCE
Task Contract: docs/tasks/T040-t038-t039-convergence-sequencing-correction.md
Purpose: remove T038/T039 circular verification order without semantic change
```

## T038 next executable identity

```text
Task: T038
Status: BLOCKED / RE-ENTRY AUTHORIZED AFTER T040 INTEGRATION
Task Contract: docs/tasks/T038-protocol-derived-consumer-asset-versioning.md
Represented branch: fix/t038-protocol-derived-consumer-assets
Implementation anchor: 8aa32b32fb15e01bfbc56e327a910b82b3674c32
Prior submitted HEAD: 6dd2f99c5cc78ddc53f9719b4d2df4dc735d70e7
Required action: preserve history, reconcile current develop containing T039, rerun complete verification, publish new terminal handoff/head
```

## T039 deferred final verification

```text
Task: T039
Status: BLOCKED / ORACLE REVISION INTEGRATED / FINAL VERIFY AFTER T038
Task Contract: docs/tasks/T039-t034-protocol-history-oracle-transition.md
Oracle revision: T039-T034-PROTOCOL-HISTORY-TRANSITION-v1
Blocked verification HEAD: 0197e1899cb0933c7345b373a5dfdbd015d078fc
Do not rerun until T038 is accepted/integrated.
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

1. Integrate T040 planning/checkpoint through PR after remote diff review.
2. Refresh canonical `develop` identity.
3. Show D055 launch profile for T038: Codex `NEW`, GPT-5.6 Sol, Medium; represented implementation exists and must be safely reconciled with T039 before complete re-verification.
4. Launch T038 from fresh canonical `develop` using only pointer `docs/tasks/T038-protocol-derived-consumer-asset-versioning.md` plus D042 freshness.
5. Executor preserves represented T038 history, reconciles current develop, performs no semantic redesign unless the unchanged T038 authority requires it, runs complete verification, persists/pushes a new terminal handoff/head, and returns canonical completion fields.
6. Orchestrator independently reviews T038. If fully green, accept/integrate T038.
7. Only then launch fresh T039 read-only verification from the new canonical develop; if fully green, accept T039.
8. Only after T038 acceptance may T021-R1 resume on its represented branch. T022 remains blocked until T021 acceptance.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not rerun T039 before T038 integration; do not redesign T038 merely because sequencing was wrong; do not replace protocol literals with another duplicated current literal; do not rewrite represented T038/T021 history; do not start T021 before T038 acceptance; do not start T022 before T021 acceptance; do not write directly to `main`/`develop`.
