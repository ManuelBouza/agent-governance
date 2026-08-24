# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O160  
Canonical-Branch: `develop`  
Current-Work-Unit: T038 planned to restore the Core-derived Consumer protocol identity baseline; T021-R1 remains blocked pending T038 acceptance/integration  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D040 single current protocol-version authority, D042 freshness, D048 final-publication boundary, D055 launch profiles and D056 progress-note rules remain controlling.
- Routed Core protocol remains `1.15.0`. Historical D054 Phase-B acceptance is not rewritten, but its current verification posture was invalidated by fresh T021 evidence showing a canonical Consumer package baseline regression.
- T034, T035, T036 and T037 remain `ACCEPTED`.
- Human Owner explicitly resumed T021 on 2026-08-24. T021 remains `REWORK_REQUIRED` under `docs/reviews/T021-R1.md`; its sole semantic defect remains the AC-T021-2 direct unsupported-`Profile` bypass.
- Fresh T021 execution reconciled represented branch `refactor/t021-consumer-profile-abstraction` with current canonical `develop@bfac31d4f7daf14ef04ece3d3e881d96c4fab0c1` through a history-preserving normal merge. Reconciliation HEAD is `f078928734be4ed0d272821955ba4d8ccdd7cd53`.
- T021 terminal blocked HEAD is `b2ec49e210a752fa539832e06b48b2bcdc00a8dd`; handoff `handoffs/T021-executor-handoff.json` reports no T021-R1 correction was committed.
- The blocker reproduces on clean canonical develop: `tests/test_governance_artifact.py` reports `2 failed, 2 passed` because Core is `1.15.0` while `governance-skill/assets/STATE.template.json` and `CAPABILITIES.template.json` still encode `1.14.0`; T020 tests also contain free-standing exact-current `1.14.0` expectations.
- This is outside T021 scope and recreates D040's cross-owner mutable-current-version synchronization hazard in Consumer asset/template form.
- T038 is persisted at `docs/tasks/T038-protocol-derived-consumer-asset-versioning.md` to remove that hazard systemically rather than changing literals from `1.14.0` to `1.15.0`.
- T038 Design: source STATE/CAPABILITIES templates use `protocol_version: null`; bootstrap derives current version from packaged Core and materializes concrete installed values; T020 verification derives expectations from Core/artifact identity; no second current-version authority remains.
- T021 represented branch MUST remain untouched by T038. After T038 acceptance/integration, relaunch T021-R1 from its represented reconciled branch and independently complete the profile-boundary correction.
- T022 remains `BLOCKED` until T021 is accepted. MG1/T023 and later unified-refactor work remain ineligible.

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

## T038 current identity

```text
Task: T038
Status: PLANNED / NEXT EXECUTABLE WORK
Task Contract: docs/tasks/T038-protocol-derived-consumer-asset-versioning.md
Expected branch: fix/t038-protocol-derived-consumer-assets
Expected handoff: handoffs/T038-executor-handoff.json
Base: current canonical develop after this planning/checkpoint PR
Purpose: restore T020/canonical green baseline by deriving Consumer installed protocol identity from Core
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
Handoff: handoffs/T021-executor-handoff.json
Pending semantic correction: AC-T021-2 direct unsupported-Profile fail-closed boundary
```

## Next action

1. Integrate this T038 planning/checkpoint Markdown branch into `develop` through PR.
2. Refresh canonical `develop` identity after merge.
3. Show D055 launch profile for T038: Codex `NEW`, GPT-5.6 Sol, Medium; this is a bounded but semantic runtime/package baseline repair with future protocol-migration consequences.
4. Launch T038 from fresh canonical `develop` using only pointer `docs/tasks/T038-protocol-derived-consumer-asset-versioning.md` plus D042 freshness.
5. Executor performs only T038 Implement + Code Review & Verify, persists/pushes terminal handoff/head, and returns canonical completion fields.
6. Orchestrator independently reviews T038 remote evidence/diff. If accepted, integrate and persist acceptance/checkpoint.
7. Only then relaunch T021-R1 on its represented reconciled branch; do not recreate/rewrite that branch history.
8. Do not start T022 or later program work before T021 acceptance.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not repair T038 by replacing `1.14.0` with another duplicated exact-current literal; do not bump Core protocol; do not modify T021 in T038; do not discard/rewrite represented T021 history; do not start T022 before T021 acceptance; do not write directly to `main`/`develop`.
