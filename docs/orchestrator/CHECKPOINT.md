# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O184  
Canonical-Branch: `develop`  
Current-Work-Unit: T023 MG1-v8 is closed `BLOCKED / HOST_CAPABILITY_PREFLIGHT`; re-entry is Specify before any further acceptance run  
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
- V8 submitted Executor branch `test/t023-skill-activation-topology-evals-v8`, submitted HEAD `a00ce1d87de6a2c955f4080a6c539bf781369f0a`, implementation HEAD `76a591c2d7a3f48d5e4b780712a78bef4c8e212f`, base `develop@23475b7fbcf427c4dac8dcb06796409660434aa2`.
- V8 evidence/review integration PR `#247`, merge `1168a55496fd53327d82cdff8080b52770fc0943`.
- T047/MG1-v8 remains the latest frozen experiment method: oracle `MG1-T023-TOPOLOGY-ORACLE-v8`, epoch `MG1-T023-EXECUTION-v8`, corpus `MG1-T023-CORPUS-v4`, presentations `MG1-T023-PRESENTATIONS-v3`, trial envelope `MG1-T023-TRIAL-ENVELOPE-v2`.
- Candidate presentation/reference bytes, semantic expectations, thresholds, zero-tolerance gates, paired 2+1 aggregation, context meaning and D050 selection percentages were not changed by the V8 Executor branch.

## V8 terminal evidence

The mandatory synthetic host-capability preflight failed before any acceptance prompt:

- `read-only` canary repetition 1 failed: required local `mx-canary/SKILL.md` body-read attempts were rejected by Codex execution policy.
- `workspace-write` fallback repetition 1 failed for the same required body-read path; no unexpected workspace mutation was observed.
- Each sandbox requires two passing repetitions. After a first failure, a second repetition cannot make that sandbox satisfy the frozen 2/2 preflight requirement, so no further canary call was necessary.
- The returned abbreviated value `quartz-heron` is not the full canary body nonce. The full nonce is `The quartz heron carries seven indigo pebbles at noon.`; `body_nonce_correct=false` is therefore correct and does not prove an unobserved body load.
- Selected sandbox: none.
- V8 acceptance prompts issued: `0`.
- V8 scored observations: `0`.
- No candidate/topology selection was computed.
- Prior-epoch observations imported: `0`.

## V8 cost-control evidence

V8's preflight prevented a large invalid acceptance run after only two synthetic provider calls.

Provider telemetry:

- read-only canary: `82,593` input tokens, `61,184` cached input tokens, `1,149` output tokens, `577` reasoning-output tokens, five policy-rejected tool calls;
- workspace-write canary: `49,502` input tokens, `45,056` cached input tokens, `1,474` output tokens, `1,120` reasoning-output tokens, two policy-rejected body-read calls plus one unsuccessful patch attempt.

The fixed host/session context cost remains material even with Apps/remote-plugin/multi-agent/web-search features intended disabled. Do not launch another acceptance corpus until the host-loading/observability problem is resolved.

## Technical verification

- Frozen input validation: PASS.
- Focused V8 harness tests: 51 PASS.
- Full deterministic suite: 456 PASS.
- Profile isolation: 48 PASS.
- Consumer/source independence: 8 PASS.
- Ruff check/format: PASS.
- Frozen D052 assets modified by Executor: false.
- No committed Markdown, candidate presentation, Core/runtime/profile semantic asset or prior evidence was modified by the Executor branch.

The integrated harness contains the V8 synthetic preflight, minimal-surface controls, host-surface drift detection, 180-second attempts, token/tool telemetry and deterministic futility/materiality scheduling. Those mechanics are integrated technical infrastructure only; live host compatibility and topology acceptance remain unestablished.

## Re-entry boundary

Classification is `HOST_CAPABILITY_PREFLIGHT`, not candidate semantic failure, not external capacity, and not an acceptance-score result.

Re-entry stage: `Specify`.

Do not weaken host-observable candidate-body activation merely because Codex shell reads are rejected. Do not broaden sandbox/tool privilege merely to make the canary pass without an explicit safety/reproducibility design.

A future V8 preflight may be rerun only after a materially relevant host/runtime change that can plausibly satisfy the unchanged canary while preserving its frozen semantics. If the required observation mechanism itself must change, create a prospective controlling revision before any new acceptance prompt. No V8 or earlier acceptance observation may enter a successor score.

## Next action

1. Orchestrator researches the current Codex local-Skill loading path and execution-policy behavior on native Windows, prioritizing official/current Codex documentation and source/issue evidence relevant to CLI `exec`, local `.agents/skills`, sandbox read behavior, and host trace observability.
2. Determine whether the unchanged V8 canary can be satisfied by a supported, bounded host/runtime/configuration change without broadening the experiment semantics or safety envelope.
3. If yes, persist the exact supported host-state requirement and decide prospectively whether V8 preflight may be rerun under that changed host state.
4. If no, create a new Orchestrator Specify revision for a different reproducible activation-observability mechanism before any acceptance execution.
5. Do not launch an Executor or any T023 acceptance prompt until that Specify decision is persisted.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not rerun V7; do not relaunch V8 immediately under the same failed host state; do not import any prior observation into a future score; do not treat the preflight failure as evidence against B0/B1/F2/G3; do not weaken activation observability; do not enable broader privileges without a persisted design; do not write directly to `main`/`develop`.
