# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O173  
Canonical-Branch: `develop`  
Current-Work-Unit: T023 MG1-v3 closed execution-incomplete; T043/MG1-v4 recovery is the current Orchestrator gate, then T023 full restart  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: ChatGPT Orchestrator

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D040 single current protocol-version authority, D042 freshness, D048 final-publication boundary, D050 topology evaluation, D051 one-product/single-install, D052 conformance ownership, D055 launch profiles and D056 progress-note rules remain controlling.
- Current routed Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`.
- T023 MG1-v2 is closed `BLOCKED / EXPERIMENT CLOSED`; review `docs/reviews/T023-R1.md`.
- T023 MG1-v3 is closed `BLOCKED / EXECUTION-INCOMPLETE`; review `docs/reviews/T023-R2.md`.
- V3 submitted Executor HEAD: `2c412022a449b8ae78466decded515fdef71b042`; evidence integration PR `#232`; merge `0105379f07cabe04a3e62a93cbfccbdb105512f1`.
- V3 attempted 75 clean sessions, retained 74 complete observations, and stopped on `HC04--G3--r2` after one 300-second unclassified timeout. No retry, partial scoring, or topology selection occurred.
- Frozen v3 corpus, topologies, presentation wording, thresholds and selection semantics remain valid and unchanged.
- The 74 v3 complete observations are diagnostic only and must never enter a later acceptance score.
- T043 is the Orchestrator-owned execution-recovery authority: `docs/tasks/T043-mg1-v4-uniform-execution-recovery.md`.
- MG1-v4 oracle identity: `MG1-T023-TOPOLOGY-ORACLE-v4`; execution epoch: `MG1-T023-EXECUTION-v4`.
- Capability source remains `MG1-2026-08-25-v3`; presentations remain `MG1-T023-PRESENTATIONS-v3`; corpus remains `MG1-T023-CORPUS-v2`.
- V4 requires a complete restart from zero: 40 cases x 4 candidates x 3 repetitions = 480 logical scored observations.
- Each logical observation permits at most two attempts, each in a fresh Codex thread/disposable workspace with identical frozen inputs and a uniform 600-second timeout.
- Failed attempts are retained but never scored. The first valid structured observation is the sole scored result. Two failed attempts for any logical observation block the full run; partial metrics/selection are forbidden.
- Retry/failure counts are diagnostic only. Routing thresholds, context-selection semantics and D050 material-improvement percentages remain unchanged.
- T025 remains independently dependency-eligible but is not the selected critical-path action.

## Process incident

During earlier convergence the Orchestrator accidentally created `tmp/placeholder` directly on `develop`, commit `6799335c757bfe60dc4401c481cbcf342b5963e3`, then immediately deleted it in `5743aaae90c1b967f4da436493ba67ac9d8cced6`. Net repository content is unchanged; these commits are administrative incident history only.

## Mandatory Executor prompt transport invariant

Every Executor prompt is pointer-only and includes D042 freshness:

```text
Operate as the Agente de IA Ejecutor for <repository>.

Synchronize with GitHub and establish a safe current local baseline from the canonical remote state before loading repository instructions or execution authority, per D042/RB001. Do not discard unrepresented local work.

Use <canonical/base or represented topic branch as applicable>.

Load current repository instructions, then execute exactly:
<persisted authority path>

Return only the output required by that persisted authority.
```

Do not duplicate Task Contract/review semantics or routine command syntax in the transport prompt.

## D055 launch invariant

Before every Executor prompt, show concrete Executor, `NEW|CONTINUE`, exact recommended model, effort and one-line rationale.

Current Codex mapping:

```text
read-only/repetitive observation -> GPT-5.6 Luna / Low
narrow mechanical implementation -> GPT-5.6 Terra / Low
standard AG implementation/rework -> GPT-5.6 Sol / Medium
complex/high-risk technical work  -> GPT-5.6 Sol / High
exceptional long-horizon work     -> GPT-5.6 Sol / highest mode only when justified
```

## T043 / MG1-v4 identity

```text
Task: T043
Status: ORCHESTRATOR-CONFORMANCE / PENDING INTEGRATION
Task Contract: docs/tasks/T043-mg1-v4-uniform-execution-recovery.md
Oracle: MG1-T023-TOPOLOGY-ORACLE-v4
Execution epoch: MG1-T023-EXECUTION-v4
Capability source epoch: MG1-2026-08-25-v3
Presentation revision: MG1-T023-PRESENTATIONS-v3
Corpus: MG1-T023-CORPUS-v2
Scored matrix after integration: 480 logical observations
```

## T023 re-entry identity

```text
Task: T023
Status: BLOCKED UNTIL T043/MG1-v4 INTEGRATION; THEN FULL RESTART
Task Contract: docs/tasks/T023-unified-skill-profile-activation-evals.md
Expected branch: test/t023-skill-activation-topology-evals
Expected handoff: handoffs/T023-executor-handoff.json
Previous v3 submitted HEAD: 2c412022a449b8ae78466decded515fdef71b042
Previous v3 result: BLOCKED / execution-incomplete
Previous v3 scored observations allowed in v4: 0
```

## Next action

1. Review and integrate `docs/t043-mg1-v4-execution-recovery` into `develop` through an Orchestrator PR.
2. Refresh canonical `develop` identity.
3. Show D055 for T023: Codex `NEW`, GPT-5.6 Sol, High.
4. Relaunch T023 from fresh canonical `develop` using only `docs/tasks/T023-unified-skill-profile-activation-evals.md` plus D042 freshness.
5. Executor mechanically implements the frozen v4 attempt/recovery protocol and executes a complete new 480-observation matrix; prior v3 observations remain diagnostic only.
6. Orchestrator independently reviews complete evidence and applies the frozen v4 selection rule before any topology acceptance.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not reuse v3 partial observations in v4 score; do not tune corpus/presentations/thresholds after v4 execution begins; do not allow Executor-authored candidate activation wording; do not change Core/engine/profile behavior to favor a candidate; do not introduce independent products, portable Skill-to-Skill dependency or multi-install packaging; do not write directly to `main`/`develop`.
