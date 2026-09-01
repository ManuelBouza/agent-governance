# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O188  
Canonical-Branch: `develop`  
Current-Work-Unit: T049/MG1-v10 Windows workspace-ACL-compatible restart is integrated and controlling; T023 is ready for a fresh v10 epoch gated by backend, provider-free workspace-readability and synthetic canary  
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
- T023 v9: closed `BLOCKED / HOST_CAPABILITY_PREFLIGHT — EXECUTION ADAPTER WORKSPACE ACL CONFOUND`; review `docs/reviews/T023-R8.md`.
- V9 submitted Executor HEAD `9a2d216a66e8ec786e6f41fccd9d0abe4d269519`; evidence/infrastructure integration PR `#251`, merge `1076a8eccc5003d92e677e83c8ddab3bd165fa90`.
- V9 issued two synthetic canaries, zero acceptance prompts, zero scored observations and no topology selection.
- T049/MG1-v10 integrated by PR `#252`, merge `904162ea708b44b4d754bc2f98ccf9dc35890583`.
- V9 root-cause research: `docs/research/MG1-V9-WINDOWS-TEMP-ACL-ANALYSIS.md`.
- Current oracle: `MG1-T023-TOPOLOGY-ORACLE-v10`; execution epoch: `MG1-T023-EXECUTION-v10`.
- Capability source: `MG1-2026-08-25-v3`; presentations: `MG1-T023-PRESENTATIONS-v3`; corpus: `MG1-T023-CORPUS-v4`; trial envelope: `MG1-T023-TRIAL-ENVELOPE-v2`.
- Corpus v4 is reused byte-identically because both v8 and v9 issued zero acceptance prompts.
- Candidate/reference bytes, semantic expectations, thresholds, zero-tolerance gates, paired 2+1, consequence-first ordering, futility/materiality, context meaning, D050 selection and live Sol/Medium cell are unchanged.

## V9 terminal finding

V9 correctly proved `unelevated` could initialize under Codex 0.149.0, but both synthetic canaries failed before testing Skill semantics because the sandboxed process could not enumerate/read the disposable workspace root itself.

The v9 harness created roots with Python 3.13.14 `tempfile.TemporaryDirectory()` under `%TEMP%`. Python 3.13 Windows private `0o700` directory ACL semantics can exclude Codex's restricted token from traversing/reading the root. Independent Codex issue `openai/codex#19791` documents the same private-temp-directory access-denied class.

Exact Codex 0.149.0 evidence also shows `.agents` workspace protection is deny-write, not a blanket read denial. V9 therefore does not establish that local Skills are unreadable under the supported backend.

Classification: Execution Adapter workspace-creation/ACL confound, not candidate evidence.

## T049 / MG1-v10 controlling identity

```text
Task: T049
Status: INTEGRATED / CONTROLLING
Task Contract: docs/tasks/T049-mg1-v10-windows-workspace-acl-compatible-restart.md
Prior Review: docs/reviews/T023-R8.md
Research: docs/research/MG1-V9-WINDOWS-TEMP-ACL-ANALYSIS.md
Integration PR: #252
Integration merge: 904162ea708b44b4d754bc2f98ccf9dc35890583
Oracle: MG1-T023-TOPOLOGY-ORACLE-v10
Execution epoch: MG1-T023-EXECUTION-v10
Capability source epoch: MG1-2026-08-25-v3
Presentation revision: MG1-T023-PRESENTATIONS-v3
Corpus: MG1-T023-CORPUS-v4 (byte-identical reuse)
Trial envelope: MG1-T023-TRIAL-ENVELOPE-v2
Codex CLI baseline: 0.149.0
Native Windows backend: explicit, elevated-first / unelevated fallback
Workspace profile: fresh disposable root with inherited Windows ACL semantics; Python private 0o700 outer root forbidden
Required live cell: Codex / native Windows / GPT-5.6 Sol / Medium
Full-completion ceiling: 480 valid acceptance repetitions
```

## V10 provider-free gates

Before a synthetic model canary, the Executor must:

1. resolve the permitted native Windows backend without provider/model use;
2. create a fresh disposable workspace with the exact v10 ACL-compatible factory;
3. avoid Python `TemporaryDirectory`/`mkdtemp` or equivalent private `0o700` outer-root semantics;
4. run a provider-free sandbox command under the requested logical sandbox;
5. prove the exact workspace root can be enumerated/read;
6. prove a neutral probe file/nonce can be read exactly;
7. persist provider/model calls issued = zero plus workspace factory/ACL diagnostics.

If a profile fails workspace readability, no synthetic model canary may be sent for it.

If no permitted profile has a readable workspace, stop:

`BLOCKED / WINDOWS_WORKSPACE_ACL_UNAVAILABLE`

with zero synthetic model canaries, zero acceptance prompts and zero scored observations.

## V10 backend/profile order

Backend policy remains:

1. `elevated` first;
2. `unelevated` fallback only when elevated cannot initialize/is unavailable or reaches a preregistered profile-level failure;
3. disabled backend forbidden;
4. Codex CLI stays `0.149.0`.

For each profile:

```text
backend resolution
-> ACL-compatible workspace
-> provider-free workspace-readability gate
-> unchanged synthetic Skill canary
-> acceptance only after canary 2/2 PASS
```

## V10 synthetic canary and acceptance

The mx-canary prompt/body semantics remain unchanged and contain no holdout/candidate content.

A complete selected profile binds:

```text
Codex version
+ native Windows backend
+ logical sandbox
+ workspace creation/ACL profile
+ GPT-5.6 Sol / Medium
+ ignored config/rules
+ minimal feature surface
```

Two fresh synthetic canary PASS repetitions are required before acceptance.

If workspace access passes but the Skill-body canary fails, classify `HOST_CAPABILITY_PREFLIGHT`, not workspace ACL failure.

Acceptance uses the exact complete profile and workspace factory that passed preflight. Loss of workspace readability, backend/logical-sandbox/ACL-profile drift, required candidate-body rejection or prohibited unrelated host-surface reappearance is `HOST_SURFACE_DRIFT`; the affected observation is not scored.

Host-observed candidate-body read/use remains activation authority. Model self-report or metadata discovery alone cannot create scored activation.

## Preserved cost-bounded method

- paired 2+1 only for still-required pairs;
- consequence-first class order: cross-profile, ambiguous, negative, near-miss, positive Consumer, positive source-maintainer, positive external-Skill trust, multi-intent;
- immediate zero-tolerance candidate stop;
- optimistic-completion qualification futility;
- challenger materiality futility after a reference exists;
- 180-second non-capacity attempts;
- capacity events are non-attempt pauses;
- token/tool/backend/workspace telemetry retained;
- 480 is a worst-case ceiling, not a required spend.

## Forbidden shortcuts

Do not use:

- Python private tempfile semantics for the outer live workspace;
- `--yolo`, dangerous/full-access bypass;
- interactive approvals;
- broad `Everyone`/world ACL grants;
- parent temporary-directory ACL mutation;
- manual candidate/Skill-specific read grants;
- explicit `$skill`/`/skills` acceptance substitution;
- candidate-body injection into model context;
- OS/model/effort substitution;
- silent Codex upgrade;
- candidate/corpus/threshold/D050 changes.

## T023 next executable identity

```text
Task: T023
Status: READY / FRESH V10 EPOCH
Task Contract: docs/tasks/T023-unified-skill-profile-activation-evals.md
Controlling revision: docs/tasks/T049-mg1-v10-windows-workspace-acl-compatible-restart.md
Expected handoff: handoffs/T023-executor-handoff.json
Implementation Executor launch: Codex NEW / GPT-5.6 Sol / High
Live acceptance cell: Codex / native Windows / GPT-5.6 Sol / Medium
Codex CLI baseline: 0.149.0
Prior observations allowed in v10 score: 0
Pre-provider requirement: explicit backend resolution + ACL-compatible workspace + provider-free workspace-readability PASS
Pre-acceptance requirement: unchanged synthetic canary 2/2 PASS under one complete profile
```

## Next action

1. Refresh current canonical `develop` before Executor launch.
2. Show D055: Codex `NEW`, GPT-5.6 Sol, High for technical v10 workspace factory/ACL diagnostics/provider-free readability adaptation; live acceptance observations remain Sol / Medium.
3. Relaunch T023 from fresh canonical `develop` using only `docs/tasks/T023-unified-skill-profile-activation-evals.md` plus D042 freshness.
4. Executor adapts only technical workspace factory/ACL evidence/provider-free probe/harness tests and preserves frozen D052 assets.
5. Executor runs deterministic verification, backend resolution and provider-free workspace gate before any model call.
6. Only after workspace gate PASS may the unchanged synthetic canary run; only after canary 2/2 PASS may acceptance begin.
7. If acceptance begins, send only observations still required by frozen futility/materiality logic.
8. Orchestrator independently reviews successor handoff/evidence before topology acceptance.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not rerun v9; do not import prior observations; do not change corpus v4; do not upgrade Codex inside v10; do not weaken host-observed body-use semantics; do not broaden privileges to make workspace/canary pass; do not alter candidate bytes/thresholds/D050 rules; do not write directly to `main`/`develop`.