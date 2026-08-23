# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O151  
Canonical-Branch: `develop`  
Current-Work-Unit: T035 runbook operation resolution readiness is READY for Executor implementation  
Chat-Closure: KEEP_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD remains accepted with single-owner stages.
- D054 Executor-owned execution mechanics and RB001 source bootstrap remain integrated and controlling.
- D042 requires canonical GitHub remote synchronization/freshness before the Executor loads `AGENTS.md` or persisted execution authority.
- D055 requires a Human-facing Executor Launch Profile before every Executor prompt; `docs/EXECUTOR-LAUNCH-PROFILES.md` carries the current Codex mapping and pointer-only prompt shape.
- D056 requires concise Human-visible progress notes around meaningful GitHub/remote operation phases.
- T034 is `ACCEPTED` and integrated.
- The pre-T035 native-Windows canonical baseline passed on `develop@219904a352785d49dabe4f688d5cc65bde3dd547`: Ruff check PASS, Ruff format PASS, pytest `340 passed`, worktree clean.
- T035-G1 pre-freeze verification passed on the represented oracle branch: diff scope PASS, reconcile PASS, semantic delta UNCHANGED, Ruff check/format PASS, pytest collection PASS, oracle RED only for expected missing T035 behavior.
- T035 oracle `T035-D054-v1` is integrated/frozen on canonical `develop` through commit `3df2b4a91c94c99c160477ed031a37132070b228`.
- T035 Task Contract is `READY` once this O151 transition is integrated.
- Expected T035 implementation branch: `feat/t035-runbook-operation-resolution-readiness`.
- Expected T035 handoff: `handoffs/T035-executor-handoff.json`.
- T021/T022 remain paused.

## Mandatory Executor prompt transport invariant

Every prompt sent to the active Executor remains pointer-only and includes D042 freshness.

Canonical shape:

```text
Operate as the Agente de IA Ejecutor for <repository>.

Synchronize with GitHub and establish a safe current local baseline from the canonical remote state before loading repository instructions or execution authority, per D042/RB001. Do not discard unrepresented local work.

Use <canonical/base or represented topic branch as applicable>.

Load current repository instructions, then execute exactly:
<persisted authority path>

Return only the output required by that persisted authority.
```

Do not carry task requirements, acceptance criteria, implementation instructions, copied contract text, or routine Git/CLI/uv/PowerShell commands in the prompt. Exact adapter mechanics belong to the Executor under D054.

`CONTINUE` preserves chat context only; it never exempts D042 remote synchronization/freshness.

## D055 launch invariant

Before every Executor prompt, ChatGPT Orchestrator shows:

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

## T035 frozen oracle

```text
Oracle-ID: T035-RUNBOOK-OPERATION-READINESS
Oracle-Revision: T035-D054-v1
Oracle-Asset: tests/test_t035_runbook_operation_resolution_conformance.py
Oracle-Freeze-State: FROZEN
Integrated oracle commit: 3df2b4a91c94c99c160477ed031a37132070b228
Pre-freeze gate: docs/reviews/T035-G1-oracle-prefreeze-verification.md
```

The Executor MUST NOT edit the frozen oracle. A semantic concern is `ORACLE_DEFECT`-equivalent and requires D053 Orchestrator re-entry.

## Next action

1. Integrate the T035 `READY` Task Contract transition and this O151 checkpoint.
2. Reverify canonical `develop`.
3. Launch T035 implementation in a NEW Codex session using the D055 launch profile and the mandatory D042 pointer-only prompt.
4. Await only the Task Contract-defined terminal pointer.
5. Perform remote GitHub D053 Converge/Accept review of the submitted implementation/handoff.
6. Do not resume T021/T022 automatically.

## Next chat minimum load

Load only:

- current `develop` identity;
- `AGENTS.md`;
- this checkpoint.

For the T035 Executor launch, additionally load `docs/EXECUTOR-LAUNCH-PROFILES.md` and `docs/tasks/T035-runbook-operation-resolution-readiness.md`.

## Do not

Do not omit D042 remote freshness from an Executor prompt; do not duplicate task semantics into the prompt; do not give routine CLI/API/shell commands to the Human; do not edit or weaken `T035-D054-v1` during implementation; do not activate D054 routed Core/protocol semantics inside T035; do not resume T021/T022 automatically; do not expose private chain-of-thought instead of D056 progress notes; and do not write directly to `main`/`develop`.
