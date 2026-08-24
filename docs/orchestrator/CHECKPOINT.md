# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O155  
Canonical-Branch: `develop`  
Current-Work-Unit: T036 independent verification is BLOCKED by pre-existing canonical baseline failures; T037 baseline restoration is planned and must execute before T036 can be re-verified  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD remains accepted with single-owner stages.
- D054 Executor-owned execution mechanics and RB001 source bootstrap remain integrated and controlling.
- D042 requires canonical GitHub remote synchronization/freshness before the Executor loads repository instructions or execution authority.
- D055 requires a Human-facing Executor Launch Profile before every Executor prompt; `docs/EXECUTOR-LAUNCH-PROFILES.md` carries the current Codex mapping and pointer-only prompt shape.
- D056 requires concise Human-visible progress notes around meaningful GitHub/remote operation phases.
- T034 and T035 remain `ACCEPTED`; T035 historical oracle baseline remains preserved.
- T036 planning/oracle transition `T036-D054-ACTIVATION-TRANSITION-v1` is integrated through PR #204 at `cc4cb59b3979f6260890e94588f3cb071c9b9488`.
- T036 independent Executor verification submitted `BLOCKED` at `7919f6050d9d67b3ca27c9d49b9a0f4dd32f6160`, handoff `handoffs/T036-executor-handoff.json`.
- T036 focused oracle verification passed `6 passed`; Executor review found no T036 runtime/oracle drift.
- T036 full canonical verification is blocked by two unrelated baseline conditions: `tests/test_repository_context.py` reports the committed repository-context manifest is non-canonical, and repository-wide `ruff format --check .` reports 14 pre-existing files require formatting.
- The persisted repository-context manifest records an older checkpoint identity than current canonical state, so deterministic manifest regeneration is required rather than an oracle waiver.
- T037 `docs/tasks/T037-canonical-verification-baseline-restoration.md` is the separate executor-owned work unit for deterministic manifest regeneration plus formatter-only repository normalization. It forbids semantic product/test/oracle changes.
- T036 remains unaccepted. After T037 acceptance/integration, T036 must be re-verified independently from fresh canonical `develop`.
- D040 Phase-B D054 routed-Core activation remains BLOCKED pending T036 acceptance.
- T021/T022 remain paused and MUST NOT auto-resume.

## Mandatory Executor prompt transport invariant

Every prompt sent to the active Executor remains pointer-only and includes D042 freshness.

```text
Operate as the Agente de IA Ejecutor for <repository>.

Synchronize with GitHub and establish a safe current local baseline from the canonical remote state before loading repository instructions or execution authority, per D042/RB001. Do not discard unrepresented local work.

Use <canonical/base or represented topic branch as applicable>.

Load current repository instructions, then execute exactly:
<persisted authority path>

Return only the output required by that persisted authority.
```

Do not copy Task Contract semantics or routine command syntax into the transport prompt. D054 leaves adapter mechanics to the Executor.

## D055 launch invariant

Before every Executor prompt, show:

```text
Executor: <active concrete executor>
Session: NEW | CONTINUE
Model: <exact recommended current model>
Effort: <exact recommended current effort>
Rationale: <one concise sentence>
```

Current Codex mapping:

```text
read-only/repetitive observation -> GPT-5.6 Luna / Low
narrow mechanical implementation -> GPT-5.6 Terra / Low
standard AG implementation/rework -> GPT-5.6 Sol / Medium
complex/high-risk technical work  -> GPT-5.6 Sol / High
exceptional long-horizon work     -> GPT-5.6 Sol / highest mode only when justified
```

## T036 current identity

```text
Task: T036
Status: BLOCKED — upstream canonical baseline
Task Contract: docs/tasks/T036-d054-phase-b-oracle-transition.md
Oracle transition: T036-D054-ACTIVATION-TRANSITION-v1
Integrated planning/oracle anchor: cc4cb59b3979f6260890e94588f3cb071c9b9488
Submitted verification HEAD: 7919f6050d9d67b3ca27c9d49b9a0f4dd32f6160
Handoff: handoffs/T036-executor-handoff.json
Focused oracle: PASS — 6 passed
Blockers: repository-context manifest canonicality; repository-wide Ruff formatting baseline
```

## T037 current identity

```text
Task: T037
Status: PLANNED — planning integration required before Executor launch
Task Contract: docs/tasks/T037-canonical-verification-baseline-restoration.md
Expected Executor branch: fix/t037-canonical-verification-baseline-restoration
Expected handoff: handoffs/T037-executor-handoff.json
Purpose: restore canonical verification baseline only; no semantic product/oracle change
```

## Next action

1. Integrate the T037 Task Contract/checkpoint planning branch into `develop` through PR.
2. Show the D055 launch profile for Codex.
3. Launch a `NEW` Executor session for T037 from then-current canonical `develop` using only the pointer to `docs/tasks/T037-canonical-verification-baseline-restoration.md`, with D042 freshness.
4. Review the submitted T037 handoff/head/diff/evidence and perform T037 Converge/Accept; integrate only if zero semantic drift and all required gates are green.
5. Re-run T036 independent verification from fresh canonical `develop`; T036 acceptance still requires its own clean verification handoff.
6. Only after T036 acceptance may D040 Phase-B restart from fresh canonical `develop`.
7. Do not resume T021/T022 automatically.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not waive the T036 canonical baseline gate; do not edit T035/T036 oracle semantics to bypass unrelated failures; do not allow T037 to introduce semantic code/test/config changes; do not activate D054 Core before T036 acceptance; do not resume T021/T022 automatically; do not write directly to `main`/`develop`.
