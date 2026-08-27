# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O176  
Canonical-Branch: `develop`  
Current-Work-Unit: T044/MG1-v5 integrated; T023 is capacity-gated before a fresh v5 acceptance epoch  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: ChatGPT Orchestrator

## Durable frontier

- D053, D054, D040, D042, D048, D050, D051, D052, D055 and D056 remain controlling. Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`.
- T023 v2: closed `BLOCKED / EXPERIMENT CLOSED`; review `docs/reviews/T023-R1.md`.
- T023 v3: closed `BLOCKED / EXECUTION-INCOMPLETE`; review `docs/reviews/T023-R2.md`.
- T023 v4: closed `BLOCKED / EXTERNAL CAPACITY`; review `docs/reviews/T023-R3.md`.
- V4 submitted Executor HEAD `4656afb34d4d4a8297107e2d8276c6e8be765bbb`; evidence PR `#235`; merge `05d41fe83183e287ab4e29468fbd6638536a8180`.
- V4 produced 31 valid observations; eight failed calls across four observations all contain explicit Codex usage-limit events. No partial score or topology selection exists.
- V2/v3/v4 evidence is diagnostic only and must not enter v5 scoring.
- T044/MG1-v5 integrated by PR `#236`, merge `5e4ffab4dc593e01318e0518b00b99fac5911c21`.
- Current oracle: `MG1-T023-TOPOLOGY-ORACLE-v5`; execution epoch: `MG1-T023-EXECUTION-v5`.
- Capability source remains `MG1-2026-08-25-v3`; presentations `MG1-T023-PRESENTATIONS-v3`; corpus `MG1-T023-CORPUS-v2`.
- V5 requires 480 logical scored observations under Codex/native-Windows/GPT-5.6-Sol/Medium.
- Each logical observation has at most two non-capacity model attempts, fresh thread/workspace and 600-second timeout.
- Explicit usage-limit/quota-capacity events are external capacity events: they do not consume model-attempt budget, are persisted separately and pause new scheduling.
- The same v5 epoch may resume after capacity becomes available; previously valid v5 observations remain authoritative and are never rerun/replaced.
- Resume verifies epoch/frozen hashes/harness/runtime identity, observation uniqueness, attempt ordinals and evidence integrity before new live calls.
- At most one non-scored trivial capacity probe is permitted before initial launch or resume and contains no holdout/candidate contents.
- Corpus, presentations, expected outcomes, thresholds, context scoring and D050 selection percentages remain unchanged.

## T044 / MG1-v5 identity

```text
Task: T044
Status: INTEGRATED / CONTROLLING
Task Contract: docs/tasks/T044-mg1-v5-capacity-aware-execution.md
Integration PR: #236
Integration merge: 5e4ffab4dc593e01318e0518b00b99fac5911c21
Oracle: MG1-T023-TOPOLOGY-ORACLE-v5
Execution epoch: MG1-T023-EXECUTION-v5
Capability source epoch: MG1-2026-08-25-v3
Presentation revision: MG1-T023-PRESENTATIONS-v3
Corpus: MG1-T023-CORPUS-v2
Scored matrix: 480 logical observations
```

## Next action

1. Do not launch T023 while the configured Codex account is known to be at usage limit.
2. When capacity is available, show D055: Codex `NEW`, GPT-5.6 Sol, High.
3. Relaunch T023 from fresh canonical `develop` using only `docs/tasks/T023-unified-skill-profile-activation-evals.md` plus D042 freshness.
4. Executor implements v5 capacity detection/pause/resume mechanics and starts a fresh v5 epoch. If an explicit capacity event occurs later, preserve the same v5 epoch and resume it after capacity returns rather than restarting completed v5 observations.
5. Orchestrator scores/selects only after all 480 v5 logical observations are complete.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not import v2/v3/v4 observations into v5 score; do not classify ambiguous provider failures as capacity events without explicit usage-limit/quota evidence; do not change corpus/presentations/thresholds/selection semantics based on prior results; do not write directly to `main`/`develop`.
