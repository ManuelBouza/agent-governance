# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O185  
Canonical-Branch: `develop`  
Current-Work-Unit: T048/MG1-v9 native-Windows sandbox-bound restart is ready for integration; T023 must not relaunch until v9 is canonical  
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
- V8 submitted Executor HEAD `a00ce1d87de6a2c955f4080a6c539bf781369f0a`; evidence integration PR `#247`; merge `1168a55496fd53327d82cdff8080b52770fc0943`.
- V8 issued zero acceptance prompts and zero scored observations. `MG1-T023-CORPUS-v4` therefore remains unexposed to the v8 acceptance cell.
- Root-cause research: `docs/research/MG1-V8-WINDOWS-SANDBOX-ROOT-CAUSE.md`.
- T048 is the prospective v9 authority: `docs/tasks/T048-mg1-v9-native-windows-sandbox-bound-restart.md`.
- Proposed oracle: `MG1-T023-TOPOLOGY-ORACLE-v9`; execution epoch: `MG1-T023-EXECUTION-v9`.
- Capability source remains `MG1-2026-08-25-v3`; presentations remain `MG1-T023-PRESENTATIONS-v3`; corpus remains `MG1-T023-CORPUS-v4`; trial envelope remains `MG1-T023-TRIAL-ENVELOPE-v2`.
- Candidate bytes, holdout bytes, semantic expectations, thresholds, zero-tolerance gates, paired 2+1, consequence-first ordering, futility/materiality rules, context meaning and D050 selection percentages are unchanged from v8.

## Root cause established

The v8 blocker is classified as an Execution Adapter configuration defect.

For the exact Codex CLI 0.149.0 baseline:

- headless `codex exec` defaults approval policy to `Never`;
- the native Windows sandbox backend is a separate configuration axis from logical `read-only` / `workspace-write` permission mode;
- `--ignore-user-config` intentionally removed personal host configuration;
- v8 did not explicitly restore a native Windows backend through its hermetic overrides;
- Codex 0.149.0 tests establish that unmatched PowerShell/file-read commands are forbidden under a logical read/workspace profile when the Windows backend is disabled and approval cannot be surfaced;
- the same class of unmatched commands can execute under the RestrictedToken/Elevated native sandbox backends.

The `.agents` protected-metadata carveout is not by itself sufficient to explain the pre-execution read rejection; it is primarily a write-protection concern inside writable roots.

## T048 / MG1-v9 method

### CLI-version isolation

- First corrected epoch remains Codex CLI `0.149.0`.
- Do not upgrade Codex in the same v9 epoch.
- If 0.149.0 cannot explicitly realize a permitted non-disabled native Windows backend, stop before model calls with `BLOCKED / WINDOWS_SANDBOX_BACKEND_UNAVAILABLE` and re-enter Specify for a separate host-version revision.

### Explicit Windows backend binding

Every canary/acceptance invocation must explicitly bind a native Windows backend while user config remains ignored.

Selection order:

1. `elevated` first;
2. `unelevated` / restricted-token only as preregistered fallback when elevated cannot initialize/is unavailable or fails the unchanged canary for a backend-specific envelope reason;
3. disabled backend forbidden;
4. no implicit reliance on `$CODEX_HOME/config.toml`.

Exact installed-version CLI/config syntax is Executor-owned under D054.

### Pre-model backend-resolution gate

Before any provider/model call, verify and persist:

- Codex version;
- native Windows platform;
- requested non-disabled backend;
- logical sandbox to be tested;
- ignored user config and execpolicy rules;
- unchanged minimal feature surface;
- dangerous bypass absent.

If the backend cannot be established, spend zero canary/acceptance calls.

### Synthetic canary

The v8 canary semantics are unchanged and the holdout/candidate content remains absent.

A complete profile is the tuple:

```text
Codex version
+ native Windows backend
+ logical sandbox
+ model/effort
+ ignored config/rules
+ minimal feature surface
```

Within each permitted backend:

1. logical `read-only` first;
2. logical `workspace-write` only if read-only cannot support the body-read/use path;
3. two fresh PASS repetitions are required for selection;
4. do not waste a second repetition merely to reconfirm a terminal first-repetition failure.

PASS still requires actual Skill-body read/use, exact full nonce, host observability, no required-read policy rejection, no unrelated app/plugin material and correct workspace mutation postcondition.

### Acceptance binding

Acceptance uses exactly the complete profile that passed 2/2. Backend/logical-sandbox/profile drift or required Skill-body rejection is `HOST_SURFACE_DRIFT` and stops scheduling before scoring the affected observation.

### Explicit Skill substitution forbidden

Do not replace implicit activation with `$skill`, `/skills`, preselected Skill injection or pre-reading candidate bodies. Codex supports an explicit host-read path, but T023 evaluates implicit routing from ordinary turns.

### Cost-bounded method preserved

V8 scheduling remains intact:

- paired 2+1;
- cross-profile/ambiguous/negative/near-miss first;
- exact qualification futility;
- challenger materiality futility;
- 180-second attempts;
- capacity pauses;
- token/tool telemetry;
- 480 full-matrix ceiling only.

## T048 / MG1-v9 identity

```text
Task: T048
Status: ORCHESTRATOR-CONFORMANCE / READY_FOR_INTEGRATION
Task Contract: docs/tasks/T048-mg1-v9-native-windows-sandbox-bound-restart.md
Research: docs/research/MG1-V8-WINDOWS-SANDBOX-ROOT-CAUSE.md
Prior Review: docs/reviews/T023-R7.md
Oracle: MG1-T023-TOPOLOGY-ORACLE-v9
Execution epoch: MG1-T023-EXECUTION-v9
Capability source epoch: MG1-2026-08-25-v3
Presentation revision: MG1-T023-PRESENTATIONS-v3
Corpus: MG1-T023-CORPUS-v4 (byte-identical reuse; zero v8 acceptance exposure)
Trial envelope: MG1-T023-TRIAL-ENVELOPE-v2
Codex CLI baseline: 0.149.0
Native Windows backend: explicit non-disabled, elevated-first
Full-completion ceiling: 480 valid acceptance repetitions
Normal behavior: preflight + exact early termination when decision becomes irreversible
```

## Next action

1. Validate the complete T048 branch diff against canonical `develop@e836ed5e9ba0376eeb8282880a8e467a0f5c8b20`.
2. Confirm changes are limited to Orchestrator-owned Markdown plus the authorized D052 `oracle.json`; corpus/envelope/topologies/presentation bytes must remain untouched.
3. Integrate T048/MG1-v9 through PR only if that boundary is clean.
4. Refresh canonical `develop` and checkpoint v9 as `INTEGRATED / CONTROLLING`.
5. Only then show D055 and relaunch T023 from fresh canonical `develop`.
6. Executor mechanically binds the native Windows backend, adapts host-profile evidence/extraction and runs deterministic verification + canary before any acceptance prompt.
7. Orchestrator independently converges successor evidence and applies the unchanged selection rule.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not rerun v8; do not import prior observations; do not change corpus v4; do not upgrade Codex inside v9; do not use disabled Windows backend; do not use dangerous bypass/full access; do not use interactive approval; do not substitute explicit Skill activation; do not weaken host-observed body-use semantics; do not alter candidate bytes/thresholds/D050 rules; do not write directly to `main`/`develop`.
