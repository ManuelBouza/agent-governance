# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O186  
Canonical-Branch: `develop`  
Current-Work-Unit: T048/MG1-v9 native-Windows sandbox-bound restart is integrated and controlling; T023 is ready for a fresh v9 epoch gated by backend resolution and synthetic canary  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: ChatGPT Orchestrator

## Durable frontier

- D053, D054, D040, D042, D048, D050, D051, D052, D055 and D056 remain controlling. Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`.
- T023 v2: closed `BLOCKED / EXPERIMENT CLOSED`; review `docs/reviews/T023-R1.md`.
- T023 v3: closed `BLOCKED / EXECUTION-INCOMPLETE`; review `docs/reviews/T023-R2.md`.
- T023 v4: closed `BLOCKED / EXTERNAL CAPACITY`; review `docs/reviews/T023-R3.md`.
- T023 v5: `SUPERSEDED_PRE_EXECUTION`; review `docs/reviews/T023-R4.md`.
- T023 v6: closed `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE`; review `docs/reviews/T023-R5.md`.
- T023 v7: closed `BLOCKED / HOST EXECUTION ENVELOPE DEFECT`; review `docs/reviews/T023-R6.md`.
- T023 v8: closed `BLOCKED / HOST_CAPABILITY_PREFLIGHT`; review `docs/reviews/T023-R7.md`.
- V8 evidence integration PR `#247`, merge `1168a55496fd53327d82cdff8080b52770fc0943`.
- V8 issued zero acceptance prompts and zero scored observations. Its two synthetic canaries are diagnostic only.
- T048/MG1-v9 integrated by PR `#249`, merge `ee2b7d53848d33ed73a00735622c21108a92a73d`.
- Root-cause research: `docs/research/MG1-V8-WINDOWS-SANDBOX-ROOT-CAUSE.md`.
- Current oracle: `MG1-T023-TOPOLOGY-ORACLE-v9`; execution epoch: `MG1-T023-EXECUTION-v9`.
- Capability source: `MG1-2026-08-25-v3`; presentations: `MG1-T023-PRESENTATIONS-v3`; corpus: `MG1-T023-CORPUS-v4`; trial envelope: `MG1-T023-TRIAL-ENVELOPE-v2`.
- Corpus v4 is reused byte-identically because v8 issued zero acceptance prompts.
- Candidate/reference bytes, semantic expectations, thresholds, zero-tolerance gates, paired 2+1, consequence-first ordering, futility/materiality rules, context meaning and D050 selection percentages are unchanged from v8.

## Root cause and v9 correction

V8's blocker was an Execution Adapter configuration defect, not candidate evidence.

For the exact Codex CLI 0.149.0 baseline:

- headless `codex exec` defaults approvals to `Never`;
- native Windows sandbox backend selection is distinct from logical `read-only` / `workspace-write` permission mode;
- v8 ignored user config for isolation but did not explicitly restore a native Windows backend;
- Codex's exact 0.149.0 tests show unmatched PowerShell/file reads are forbidden when the backend is disabled and approval cannot be surfaced;
- those tests permit unmatched commands to run inside the native RestrictedToken/Elevated Windows sandbox backends.

V9 therefore preserves the complete v8 experiment while explicitly binding a non-disabled native Windows backend in the hermetic invocation.

## T048 / MG1-v9 controlling identity

```text
Task: T048
Status: INTEGRATED / CONTROLLING
Task Contract: docs/tasks/T048-mg1-v9-native-windows-sandbox-bound-restart.md
Research: docs/research/MG1-V8-WINDOWS-SANDBOX-ROOT-CAUSE.md
Prior Review: docs/reviews/T023-R7.md
Integration PR: #249
Integration merge: ee2b7d53848d33ed73a00735622c21108a92a73d
Oracle: MG1-T023-TOPOLOGY-ORACLE-v9
Execution epoch: MG1-T023-EXECUTION-v9
Capability source epoch: MG1-2026-08-25-v3
Presentation revision: MG1-T023-PRESENTATIONS-v3
Corpus: MG1-T023-CORPUS-v4 (byte-identical reuse)
Trial envelope: MG1-T023-TRIAL-ENVELOPE-v2
Codex CLI baseline: 0.149.0
Native Windows backend: explicitly bound, elevated-first
Required live cell: Codex / native Windows / GPT-5.6 Sol / Medium
Full-completion ceiling: 480 valid acceptance repetitions
Normal behavior: pre-model backend gate + synthetic canary + exact futility/materiality stopping
```

## V9 pre-model backend gate

Before any provider/model call, the Executor must resolve/persist:

- Codex CLI version = `0.149.0`;
- native Windows platform;
- requested non-disabled native Windows sandbox backend;
- logical sandbox to be tested;
- user config ignored;
- user/project execpolicy `.rules` ignored;
- minimal v8 feature surface preserved;
- dangerous approvals/sandbox bypass absent.

Backend selection order is frozen:

1. `elevated` first;
2. `unelevated` / restricted-token only when elevated cannot initialize/is unavailable or fails the unchanged canary for a backend-specific reason;
3. disabled backend forbidden.

If Codex 0.149.0 cannot explicitly realize a permitted backend while user config remains ignored, stop **before any model call** as `BLOCKED / WINDOWS_SANDBOX_BACKEND_UNAVAILABLE`. Do not upgrade Codex inside v9.

## V9 synthetic canary

The v8 canary semantics are unchanged; it contains no holdout/candidate content.

The complete selected profile is:

```text
Codex version
+ native Windows backend
+ logical sandbox
+ model/effort
+ ignored config/rules
+ minimal feature surface
```

Within a backend:

1. logical `read-only` first;
2. logical `workspace-write` only when read-only cannot operate the body-read/use path;
3. two fresh passing repetitions are required to select a profile;
4. do not waste a second repetition merely to reconfirm a terminal first-repetition failure.

A PASS requires actual `SKILL.md` body read/use, exact full nonce, host trace distinction from metadata discovery, valid structured output, no required-read policy rejection, no unrelated app/plugin material, correct workspace mutation postcondition and identical non-disabled backend identity.

No acceptance prompt may run before one complete profile passes 2/2.

## V9 activation/host binding

Acceptance and resume use exactly the profile that passed the canary.

A disabled/different backend, logical-sandbox drift, required candidate-body policy rejection, or unrelated app/plugin reappearance is `HOST_SURFACE_DRIFT`; the affected observation is not scored and new scheduling stops immediately.

Host-observed body read/use remains the activation authority. The harness may recognize any deterministic first-party Codex event that unambiguously proves actual body load/use; model self-report or metadata discovery alone cannot score activation.

Explicit `$skill`/`/skills` selection, pre-reading/injecting candidate bodies, interactive approvals, manual evaluator-only read grants, `--yolo`/dangerous bypass, OS/model/effort substitution and silent Codex upgrade are forbidden.

## Cost-bounded method preserved

- paired 2+1 only for still-required pairs;
- consequence-first class order: cross-profile, ambiguous, negative, near-miss, positive Consumer, positive source-maintainer, positive external-Skill trust, multi-intent;
- immediate zero-tolerance candidate stop;
- optimistic-completion qualification futility;
- challenger materiality futility after a reference exists;
- 180-second non-capacity attempts;
- capacity events are non-attempt pauses;
- token/tool/backend telemetry retained;
- 480 is a worst-case ceiling, not a required spend.

## T023 next executable identity

```text
Task: T023
Status: READY / FRESH V9 EPOCH
Task Contract: docs/tasks/T023-unified-skill-profile-activation-evals.md
Controlling revision: docs/tasks/T048-mg1-v9-native-windows-sandbox-bound-restart.md
Expected handoff: handoffs/T023-executor-handoff.json
Implementation Executor launch: Codex NEW / GPT-5.6 Sol / High
Live acceptance cell: Codex / native Windows / GPT-5.6 Sol / Medium
Codex CLI baseline: 0.149.0
Prior observations allowed in v9 score: 0
Pre-provider requirement: explicit non-disabled native Windows backend resolution
Pre-acceptance requirement: two passing unchanged synthetic canary repetitions under one complete profile
```

## Next action

1. Refresh current canonical `develop` before Executor launch.
2. Show D055: Codex `NEW`, GPT-5.6 Sol, High for technical v9 backend-binding/harness adaptation; live acceptance observations remain Sol / Medium.
3. Relaunch T023 from fresh canonical `develop` using only `docs/tasks/T023-unified-skill-profile-activation-evals.md` plus D042 freshness.
4. Executor first resolves the exact Codex 0.149.0 native-Windows backend adapter from installed help/official version-specific authority and updates technical harness/tests/evidence mechanics only.
5. Executor runs deterministic verification and the pre-model backend gate. If backend unavailable, stop without a provider/model call.
6. If backend is available, run the unchanged synthetic canary. No acceptance prompt until one complete profile passes 2/2.
7. If canary passes, start fresh v9 acceptance and send only observations still required by frozen futility/materiality logic.
8. Executor MUST NOT alter corpus/oracle/presentation semantics, candidate bytes, thresholds or D050 rules.
9. Orchestrator independently reviews successor handoff/evidence before any topology acceptance.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not rerun v8; do not import prior observations; do not modify corpus v4; do not upgrade Codex inside v9; do not permit a disabled Windows backend; do not use dangerous bypass/full access or interactive approvals; do not substitute explicit Skill activation; do not weaken host-observed body-use semantics; do not alter candidate bytes/thresholds/D050 rules; do not write directly to `main`/`develop`.
