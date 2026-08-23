# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O150  
Canonical-Branch: `develop`  
Current-Work-Unit: T035 oracle pre-freeze gate; executor prompt transport corrected to require D042 remote freshness  
Chat-Closure: KEEP_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD remains accepted with single-owner stages.
- D054 Executor-owned execution mechanics and RB001 source bootstrap remain integrated and controlling.
- D042 requires canonical remote synchronization/freshness before the Executor loads `AGENTS.md` or any persisted Task/Operational/Review/Gate authority.
- D055 requires a Human-facing Executor Launch Profile before every Executor prompt; `docs/EXECUTOR-LAUNCH-PROFILES.md` carries the current Codex mapping and canonical minimal transport prompt.
- D056 requires concise Human-visible progress notes around meaningful GitHub/remote operation phases.
- T034 native SDD executable materialization is `ACCEPTED` and integrated.
- A current native-Windows pre-T035 baseline has passed on `develop@219904a352785d49dabe4f688d5cc65bde3dd547`: Ruff check PASS, Ruff format PASS, pytest `340 passed`, worktree clean.
- T035 remains `BLOCKED` until its D052 oracle is technically pre-freeze verified, reviewed/integrated and marked `FROZEN`.
- T035 oracle draft branch: `test/t035-runbook-conformance-oracle`.
- T035 oracle draft asset: `tests/test_t035_runbook_operation_resolution_conformance.py`.
- T035 oracle pre-freeze gate: `docs/reviews/T035-G1-oracle-prefreeze-verification.md`.
- T021/T022 remain paused.

## Mandatory Executor prompt transport invariant

Every prompt sent to the active Executor must remain pointer-only but MUST include the D042 freshness precondition.

Canonical shape:

```text
Operate as the Agente de IA Ejecutor for <repository>.

Synchronize with GitHub and establish a safe current local baseline from the canonical remote state before loading repository instructions or execution authority, per D042/RB001. Do not discard unrepresented local work.

Use <canonical/base or represented topic branch as applicable>.

Load current repository instructions, then execute exactly:
<persisted authority path>

Return only the output required by that persisted authority.
```

The prompt must not carry task requirements, acceptance criteria, implementation instructions, copied contract text, or routine Git/CLI/uv/PowerShell commands. Those live in GitHub. Exact adapter mechanics belong to the Executor under D054.

`CONTINUE` preserves chat context only; it never exempts D042 remote synchronization/freshness.

A remembered SHA is not the source of truth. Exact SHAs belong in prompts only when persisted authority makes them materially necessary for safe reconciliation/verification, and never replace refresh from GitHub.

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

## T035 current gate

The pre-T035 Windows baseline gate is satisfied.

The Orchestrator has authored the D052 oracle in DRAFT on `test/t035-runbook-conformance-oracle` and persisted its technical pre-freeze verification procedure in `docs/reviews/T035-G1-oracle-prefreeze-verification.md`.

Next permitted sequence:

```text
Executor performs T035-G1 pre-freeze verification only
        -> Orchestrator reviews result
        -> if PASS: freeze/integrate T035-D054-v1 oracle and change T035 to READY
        -> only then launch T035 implementation
```

Do not launch T035 implementation before the oracle is `FROZEN` on canonical `develop`.

## Next action

1. Integrate the D042/D055 prompt-template clarification and this O150 checkpoint through a focused Markdown-only PR.
2. Reverify canonical `develop` after merge.
3. Give the Human the corrected minimal Codex prompt for `T035-G1`, with explicit GitHub synchronization and no duplicated task instructions.
4. After Executor result, perform Orchestrator review and either correct the DRAFT oracle or freeze/integrate it and mark T035 READY.

## Next chat minimum load

Load only:

- current `develop` identity;
- `AGENTS.md`;
- this checkpoint.

For an Executor launch also load `docs/EXECUTOR-LAUNCH-PROFILES.md` and the exact persisted authority being launched.

## Do not

Do not omit D042 remote freshness from an Executor prompt; do not duplicate task semantics into the prompt; do not give routine CLI/API/shell commands to the Human; do not freeze or launch T035 before T035-G1 passes; do not resume T021/T022 automatically; do not expose private chain-of-thought instead of D056 progress notes; and do not write directly to `main`/`develop`.
