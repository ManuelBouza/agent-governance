# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O178  
Canonical-Branch: `develop`  
Current-Work-Unit: T045/MG1-v6 integrated; T023 is ready for a fresh v6 acceptance epoch  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053, D054, D040, D042, D048, D050, D051, D052, D055 and D056 remain controlling. Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`.
- T023 v2: closed `BLOCKED / EXPERIMENT CLOSED`; review `docs/reviews/T023-R1.md`.
- T023 v3: closed `BLOCKED / EXECUTION-INCOMPLETE`; review `docs/reviews/T023-R2.md`.
- T023 v4: closed `BLOCKED / EXTERNAL CAPACITY`; review `docs/reviews/T023-R3.md`.
- T023 v5: `SUPERSEDED_PRE_EXECUTION / METHOD EFFICIENCY REVISION`; review `docs/reviews/T023-R4.md`.
- V4 submitted Executor HEAD `4656afb34d4d4a8297107e2d8276c6e8be765bbb`; evidence PR `#235`; merge `05d41fe83183e287ab4e29468fbd6638536a8180`.
- V2/v3/v4 evidence remains diagnostic only and must not enter v6 scoring.
- T045/MG1-v6 integrated by PR `#238`, merge `81097d3d39b9da83a02275ee0fea05244f8a8390`.
- Research: `docs/research/MG1-EVAL-EFFICIENCY-RESEARCH.md`.
- Current oracle: `MG1-T023-TOPOLOGY-ORACLE-v6`; execution epoch: `MG1-T023-EXECUTION-v6`.
- Capability source remains `MG1-2026-08-25-v3`; presentations `MG1-T023-PRESENTATIONS-v3`; corpus `MG1-T023-CORPUS-v2` with all 40 cases unchanged.
- V6 scoring unit is the case/candidate pair. Each evaluated pair gets two valid clean-context repetitions; a third is required only when the first two disagree on a frozen decision field or `observed_context_bytes`; no fourth valid repetition is allowed.
- Non-critical routing/semantic results use case-level majority and context uses the case-level median. Cross-profile/ambiguous mandatory boundaries inspect every valid repetition and remain any-occurrence zero-tolerance.
- Stage R evaluates B0/B1 first: 160–240 valid observations. If neither qualifies, T023 is `BLOCKED` and F2/G3 MUST NOT run.
- Stage C evaluates F2/G3 only if a single-family reference exists: another 160–240 valid observations. Complete two-stage range: 320–480 valid observations.
- Numeric qualification thresholds and D050 material-advantage/tie-break percentages are unchanged.
- Explicit usage-limit/quota events remain non-attempt capacity pauses. Each scheduled valid repetition retains a 600-second timeout, fresh thread/workspace and at most two non-capacity model attempts.
- Same-epoch v6 pause/resume preserves prior valid v6 observations after exact identity/integrity verification.

## T045 / MG1-v6 identity

```text
Task: T045
Status: INTEGRATED / CONTROLLING
Task Contract: docs/tasks/T045-mg1-v6-efficient-paired-evaluation.md
Research: docs/research/MG1-EVAL-EFFICIENCY-RESEARCH.md
Review: docs/reviews/T023-R4.md
Integration PR: #238
Integration merge: 81097d3d39b9da83a02275ee0fea05244f8a8390
Oracle: MG1-T023-TOPOLOGY-ORACLE-v6
Execution epoch: MG1-T023-EXECUTION-v6
Capability source epoch: MG1-2026-08-25-v3
Presentation revision: MG1-T023-PRESENTATIONS-v3
Corpus: MG1-T023-CORPUS-v2
Reference stage: 160-240 valid observations
Full two-stage run: 320-480 valid observations
```

## T023 next executable identity

```text
Task: T023
Status: READY / FRESH V6 EPOCH
Task Contract: docs/tasks/T023-unified-skill-profile-activation-evals.md
Expected handoff: handoffs/T023-executor-handoff.json
Required live cell: Codex / native Windows / GPT-5.6 Sol / Medium
Prior v2/v3/v4 observations allowed in v6 score: 0
Prior v5 live observations: 0
```

## Next action

1. Refresh canonical `develop` identity.
2. Show D055 for T023: Codex `NEW`, GPT-5.6 Sol, High.
3. Relaunch T023 from fresh canonical `develop` using only `docs/tasks/T023-unified-skill-profile-activation-evals.md` plus D042 freshness.
4. Executor mechanically implements v6 stage scheduling, 2+1 disagreement resolution, case aggregation and retained capacity-aware execution semantics.
5. If Stage R yields neither B0 nor B1 qualifying, stop `BLOCKED` without executing F2/G3.
6. If a reference exists, execute Stage C and apply the frozen challenger rules.
7. Orchestrator independently reviews complete v6 evidence and applies the frozen selection rule.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not execute T023 under v5; do not remove any of the 40 corpus cases; do not import v2/v3/v4 observations into v6 score; do not use majority voting to mask cross-profile/ambiguous violations; do not run an unnecessary third repetition after first-two agreement; do not run a fourth valid repetition; do not run F2/G3 when Stage R has no qualifying reference; do not change thresholds/selection percentages based on observed results; do not write directly to `main`/`develop`.
