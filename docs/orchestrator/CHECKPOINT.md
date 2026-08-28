# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O177  
Canonical-Branch: `develop`  
Current-Work-Unit: T045/MG1-v6 efficient paired evaluation revision is ready for integration; T023 must not launch until v6 is canonical  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: ChatGPT Orchestrator

## Durable frontier

- D053, D054, D040, D042, D048, D050, D051, D052, D055 and D056 remain controlling. Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`.
- T023 v2: closed `BLOCKED / EXPERIMENT CLOSED`; review `docs/reviews/T023-R1.md`.
- T023 v3: closed `BLOCKED / EXECUTION-INCOMPLETE`; review `docs/reviews/T023-R2.md`.
- T023 v4: closed `BLOCKED / EXTERNAL CAPACITY`; review `docs/reviews/T023-R3.md`.
- T023 v5: `SUPERSEDED_PRE_EXECUTION / METHOD EFFICIENCY REVISION`; review `docs/reviews/T023-R4.md`.
- V4 submitted Executor HEAD `4656afb34d4d4a8297107e2d8276c6e8be765bbb`; evidence PR `#235`; merge `05d41fe83183e287ab4e29468fbd6638536a8180`.
- V2/v3/v4 evidence remains diagnostic only and must not enter v6 scoring.
- V5 capacity-aware semantics remain preserved in v6, but no v5 acceptance epoch is authoritative.
- T045 is the prospective v6 authority: `docs/tasks/T045-mg1-v6-efficient-paired-evaluation.md`.
- Research: `docs/research/MG1-EVAL-EFFICIENCY-RESEARCH.md`.
- Proposed oracle: `MG1-T023-TOPOLOGY-ORACLE-v6`; execution epoch: `MG1-T023-EXECUTION-v6`.
- Capability source remains `MG1-2026-08-25-v3`; presentations `MG1-T023-PRESENTATIONS-v3`; corpus `MG1-T023-CORPUS-v2` with all 40 cases unchanged.
- V6 scoring unit is the case/candidate pair, not repeated trial rows.
- Every evaluated pair gets two valid clean-context repetitions. A third is required only if the first two disagree on a frozen decision field or `observed_context_bytes`; no fourth valid repetition is allowed.
- Non-critical case results use majority/median aggregation. Cross-profile/ambiguous mandatory boundaries inspect every valid repetition and remain any-occurrence zero-tolerance.
- Stage R evaluates B0/B1 first: 160–240 valid observations. If neither qualifies, T023 is BLOCKED and F2/G3 are not executed.
- Stage C evaluates F2/G3 only when a single-family reference exists: another 160–240 observations. Complete two-stage range: 320–480 rather than fixed 480.
- Numeric qualification thresholds and D050 material-advantage/tie-break percentages remain unchanged.
- V5 quota-aware pause/resume, 600-second timeout, fresh thread/workspace and two non-capacity attempts per scheduled observation carry forward unchanged.

## T045 / MG1-v6 identity

```text
Task: T045
Status: ORCHESTRATOR-CONFORMANCE / READY_FOR_INTEGRATION
Task Contract: docs/tasks/T045-mg1-v6-efficient-paired-evaluation.md
Research: docs/research/MG1-EVAL-EFFICIENCY-RESEARCH.md
Review: docs/reviews/T023-R4.md
Oracle: MG1-T023-TOPOLOGY-ORACLE-v6
Execution epoch: MG1-T023-EXECUTION-v6
Capability source epoch: MG1-2026-08-25-v3
Presentation revision: MG1-T023-PRESENTATIONS-v3
Corpus: MG1-T023-CORPUS-v2
Reference stage: 160-240 valid observations
Full two-stage run: 320-480 valid observations
```

## Next action

1. Review the complete `docs/t045-mg1-v6-efficient-paired-eval` diff against canonical `develop`.
2. Integrate T045/MG1-v6 through PR if only Orchestrator-owned Markdown plus the authorized D052 oracle changed.
3. Refresh canonical `develop` and checkpoint v6 as `INTEGRATED / CONTROLLING`.
4. Only then show D055 and relaunch T023 from fresh canonical `develop`.
5. Executor mechanically implements v6 stage scheduling, 2+1 disagreement resolution, case aggregation and retained capacity-aware execution semantics.
6. Orchestrator independently reviews evidence and applies the frozen v6 selection rule.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not launch T023 under v5 or before v6 integration; do not remove any of the 40 corpus cases; do not import v2/v3/v4 observations into v6 score; do not use majority voting to mask cross-profile/ambiguous violations; do not run F2/G3 when Stage R yields no qualifying reference; do not change thresholds/selection percentages based on observed results; do not write directly to `main`/`develop`.
