# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O187  
Canonical-Branch: `develop`  
Current-Work-Unit: T049/MG1-v10 Windows workspace-ACL-compatible restart is specified and ready for integration; T023 must not relaunch until v10 is canonical  
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
- V9 submitted Executor branch `test/t023-skill-activation-topology-evals-v9`, submitted HEAD `9a2d216a66e8ec786e6f41fccd9d0abe4d269519`, implementation HEAD `b7b665d5d495be2dd2bf2cbb8f4849fa65ad99c4`, base `develop@f44227768a911207ac84dcbe20cf88f5d479f74d`.
- V9 evidence/infrastructure integration PR `#251`, merge `1076a8eccc5003d92e677e83c8ddab3bd165fa90`.
- V9 issued two synthetic canaries, zero acceptance prompts, zero scored observations and no topology selection.
- V9 changed no committed Markdown, oracle, corpus, trial envelope, topology, presentation, Core/runtime or profile semantics on the Executor branch.
- V9 deterministic verification: focused harness 55 PASS; full pytest 460 PASS; profile isolation 48 PASS; Consumer/source independence 8 PASS; Ruff PASS.
- Capability source remains `MG1-2026-08-25-v3`; presentations remain `MG1-T023-PRESENTATIONS-v3`; corpus remains `MG1-T023-CORPUS-v4`; trial envelope remains `MG1-T023-TRIAL-ENVELOPE-v2`.

## V9 terminal evidence

The v9 backend gate worked as designed:

- Codex CLI `0.149.0`;
- native Windows 11;
- `elevated` backend attempted first and timed out before provider/model use;
- `unelevated` backend initialized successfully before provider/model use;
- logical `read-only` canary repetition 1 failed;
- logical `workspace-write` canary repetition 1 failed;
- no second canary repetition was required after terminal first-repetition failure;
- no acceptance prompt was issued.

Both canary traces show that the sandboxed process could not enumerate/read the **workspace root itself**, not merely `.agents/skills/mx-canary/SKILL.md`.

## Deeper root cause

Research: `docs/research/MG1-V9-WINDOWS-TEMP-ACL-ANALYSIS.md`.

The v9 harness created outer canary/acceptance roots with Python `tempfile.TemporaryDirectory()` under `%TEMP%`. The exact runtime was Python `3.13.14`.

Python 3.13 Windows private `0o700` directory semantics can apply an ACL restricting the new directory to the interactive user/Administrators. Codex's restricted token can then receive `Access denied` while traversing/reading that root even though the Codex logical policy otherwise allows the workspace.

Independent Codex issue `openai/codex#19791` documents the same restricted-token incompatibility with Python/pytest/tempfile-style private `0o700` temporary directories.

Exact Codex 0.149.0 source also shows:

- its Windows sandbox smoke workspace is a normal user-profile directory rather than a Python private temp root;
- `.agents` workspace protection is deny-write, not blanket deny-read;
- restricted-token workspace permissions rely on Windows ACL/capability access to the underlying root.

Therefore v9 is an Execution Adapter workspace-creation confound. It is not candidate evidence and does not prove that local Skills are unreadable under `unelevated`.

## T049 / MG1-v10 proposed identity

```text
Task: T049
Status: ORCHESTRATOR-CONFORMANCE / READY_FOR_INTEGRATION
Task Contract: docs/tasks/T049-mg1-v10-windows-workspace-acl-compatible-restart.md
Prior Review: docs/reviews/T023-R8.md
Research: docs/research/MG1-V9-WINDOWS-TEMP-ACL-ANALYSIS.md
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

## V10 provider-free sequencing

Before any synthetic model canary:

1. resolve the native Windows backend without provider/model use;
2. create a fresh v10 workspace with sandbox-compatible inherited ACL semantics;
3. run a provider-free workspace-access probe under the exact backend/logical sandbox;
4. prove the workspace root can be enumerated/read and a neutral probe nonce can be read exactly;
5. persist provider/model-call count = zero.

A profile failing the workspace-access gate MUST NOT reach the synthetic model canary.

If no permitted profile has a readable workspace, stop:

`BLOCKED / WINDOWS_WORKSPACE_ACL_UNAVAILABLE`

with zero canaries, zero acceptance prompts and zero scored observations.

## V10 synthetic canary

Only after workspace access passes, run the unchanged mx-canary.

A complete profile is:

```text
Codex version
+ native Windows backend
+ logical sandbox
+ workspace creation/ACL profile
+ model/effort
+ ignored config/rules
+ minimal feature surface
```

Two fresh canary PASS repetitions are required before acceptance. If workspace access is proven but the unchanged Skill-body canary fails, classify `HOST_CAPABILITY_PREFLIGHT` rather than workspace ACL failure.

## Preserved semantics

V10 changes no candidate or product/eval semantic variable:

- candidate/reference bytes unchanged;
- corpus v4 unchanged;
- trial envelope v2 unchanged;
- semantic expectations unchanged;
- thresholds unchanged;
- zero-tolerance gates unchanged;
- D050 reference/materiality/tie-break rules unchanged;
- paired 2+1 unchanged;
- consequence-first ordering unchanged;
- qualification/materiality futility unchanged;
- observed-context meaning unchanged;
- Sol/Medium acceptance cell unchanged;
- Codex CLI 0.149.0 unchanged.

No v9 or earlier observation may enter v10 score.

## Forbidden shortcuts

Do not use:

- Python private `tempfile.TemporaryDirectory` / `mkdtemp` for the outer live workspace;
- dangerous/full-access bypass;
- interactive approval;
- broad `Everyone` ACL grants;
- shared parent temporary-directory ACL mutation;
- manual candidate/Skill read grants;
- explicit `$skill`/`/skills` acceptance substitution;
- candidate-body injection into model context;
- silent Codex upgrade;
- candidate/corpus/threshold/D050 changes.

## Next action

1. Validate the complete T049 branch against canonical `develop@1076a8eccc5003d92e677e83c8ddab3bd165fa90`.
2. Confirm changes are limited to Orchestrator-owned Markdown plus authorized D052 `oracle.json`.
3. Confirm `corpus.json`, `trial-envelope.json`, `topologies.json`, all presentation/reference bytes and product/runtime assets are untouched.
4. Integrate T049/MG1-v10 through PR only if that boundary is clean.
5. Refresh canonical `develop` and checkpoint v10 as `INTEGRATED / CONTROLLING`.
6. Only then show D055 and relaunch T023 from fresh canonical `develop`.
7. Executor adapts only technical workspace factory/ACL evidence/provider-free readability mechanics plus tests, then executes the frozen v10 gates.
8. Orchestrator independently converges any successor handoff/evidence before topology acceptance.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not rerun v9; do not import prior observations; do not change corpus v4; do not upgrade Codex inside v10; do not weaken host-observed activation; do not broaden privileges to make the probe/canary pass; do not alter candidate bytes/thresholds/D050 rules; do not write directly to `main`/`develop`.