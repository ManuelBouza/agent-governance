# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O175  
Canonical-Branch: `develop`  
Current-Work-Unit: T023 MG1-v4 closed BLOCKED / EXTERNAL CAPACITY; T044/MG1-v5 capacity-aware execution is the current Orchestrator gate  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: ChatGPT Orchestrator

## Durable frontier

- D053, D054, D040, D042, D048, D050, D051, D052, D055 and D056 remain controlling. Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`.
- T023 v2: closed `BLOCKED / EXPERIMENT CLOSED`; review `docs/reviews/T023-R1.md`.
- T023 v3: closed `BLOCKED / EXECUTION-INCOMPLETE`; review `docs/reviews/T023-R2.md`.
- T023 v4: closed `BLOCKED / EXTERNAL CAPACITY`; review `docs/reviews/T023-R3.md`.
- V4 submitted Executor HEAD `4656afb34d4d4a8297107e2d8276c6e8be765bbb`; evidence integration PR `#235`; merge `05d41fe83183e287ab4e29468fbd6638536a8180`.
- V4 produced 31 valid logical observations. Eight failed calls across four logical observations all contain explicit Codex usage-limit events. No partial score or topology selection was produced.
- V2/v3/v4 evidence is diagnostic only for later epochs and must not enter v5 scoring.
- Frozen capability source remains `MG1-2026-08-25-v3`; presentations `MG1-T023-PRESENTATIONS-v3`; corpus `MG1-T023-CORPUS-v2`.
- T044 is the Orchestrator-owned capacity-aware execution authority: `docs/tasks/T044-mg1-v5-capacity-aware-execution.md`.
- New oracle `MG1-T023-TOPOLOGY-ORACLE-v5`; new execution epoch `MG1-T023-EXECUTION-v5`.
- V5 still requires 480 logical scored observations under Codex/native-Windows/GPT-5.6-Sol/Medium.
- Each logical observation has at most two non-capacity model attempts, fresh thread/workspace and 600-second timeout.
- Explicit usage-limit/quota-capacity events are external capacity events: they do not consume model-attempt budget, are persisted separately and pause new scheduling.
- The same v5 epoch may resume after capacity is available; previously valid v5 observations remain authoritative and are not rerun/replaced.
- Resume must verify epoch/frozen hashes/harness/runtime identity, observation uniqueness, attempt ordinals and evidence integrity before new live calls.
- At most one non-scored trivial capacity probe is permitted before launch/resume; it contains no holdout/candidate contents.
- Corpus, presentations, expected outcomes, thresholds, context scoring and D050 selection percentages remain unchanged.

## T044 / MG1-v5 identity

```text
Task: T044
Status: ORCHESTRATOR-CONFORMANCE / PENDING INTEGRATION
Task Contract: docs/tasks/T044-mg1-v5-capacity-aware-execution.md
Oracle: MG1-T023-TOPOLOGY-ORACLE-v5
Execution epoch: MG1-T023-EXECUTION-v5
Capability source epoch: MG1-2026-08-25-v3
Presentation revision: MG1-T023-PRESENTATIONS-v3
Corpus: MG1-T023-CORPUS-v2
Scored matrix after integration: 480 logical observations
```

## Next action

1. Review and integrate `docs/t044-mg1-v5-capacity-aware-execution` into `develop` through PR.
2. Refresh canonical `develop` and checkpoint v5 as controlling.
3. Do not launch T023 while the configured Codex account is known to be at usage limit.
4. Once capacity is available, show D055: Codex `NEW`, GPT-5.6 Sol, High, and relaunch T023 from fresh canonical `develop` using only its persisted Task Contract plus D042 freshness.
5. Executor implements v5 capacity detection/pause/resume mechanics, starts a fresh v5 epoch, and may resume that same epoch across later capacity windows without reusing v4 evidence.
6. Orchestrator scores/selects only after all 480 v5 logical observations are complete.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not import v2/v3/v4 observations into v5 score; do not classify ambiguous provider failures as capacity events without explicit usage-limit/quota evidence; do not change corpus/presentations/thresholds/selection semantics based on prior results; do not write directly to `main`/`develop`.
