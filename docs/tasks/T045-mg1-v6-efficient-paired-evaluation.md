# T045 — MG1-v6 Efficient Paired Evaluation Revision

## Identity

- Task ID: `T045`
- Status: `ORCHESTRATOR-CONFORMANCE`
- Type: `test/eval method revision`
- Base branch: `develop`
- Orchestrator branch: `docs/t045-mg1-v6-efficient-paired-eval`
- SDD profile: `ASSURED`
- Re-entry stage: `Specify`
- Test-Authorship-Mode: `orchestrator-conformance`

## Objective

Prospectively replace the unexecuted MG1-v5 fixed 480-observation acceptance method with a lower-cost paired staged design that preserves all 40 semantic cases, the exact candidate surfaces, mandatory safety boundaries, numeric qualification thresholds, and D050 topology-selection meaning.

The revision MUST reduce redundant live repetitions without using v2/v3/v4 results to tune candidate semantics or thresholds and without observing any v6 live result before the method is frozen.

## Context

MG1-v4 closed `BLOCKED / EXTERNAL CAPACITY`. MG1-v5 introduced correct capacity-aware pause/resume semantics but retained 40 x 4 x 3 = 480 mandatory valid observations. Before any v5 live epoch was started, the Human requested research into reducing live evaluation cost without losing rigor.

Research and rationale are recorded in `docs/research/MG1-EVAL-EFFICIENCY-RESEARCH.md`.

## Preserved authority

The following remain byte/semantically unchanged by T045:

- capability source epoch `MG1-2026-08-25-v3`;
- presentation revision `MG1-T023-PRESENTATIONS-v3`;
- corpus `MG1-T023-CORPUS-v2` with all 40 prompts;
- topologies B0, B1, F2 and G3;
- expected capabilities and semantic outcomes;
- clarification/cross-profile meaning;
- context measurement source and `observed_context_bytes` selection role;
- deterministic/profile/source-independence gates;
- qualification thresholds: precision/recall/F1 >= 0.95, false/wrong/overactivation <= 0.05, overall semantic accuracy >= 0.95;
- mandatory zero cross-profile violations and ambiguous permission broadening;
- D050 B0/B1 reference and F2/G3 material-advantage percentages/tie-breaks;
- required live cell Codex / native Windows / GPT-5.6 Sol / Medium;
- v5 external-capacity classification, pause/resume, fresh thread/workspace, 600-second timeout, and two non-capacity execution-attempt budget per scheduled live observation.

## Added / modified specification

### ADDED — case-candidate scoring unit

The semantic experimental unit is one frozen prompt evaluated against one candidate. Repetitions measure stochastic stability; they are not independent semantic cases.

Each evaluated case/candidate pair receives two valid clean-context repetitions first. A third valid repetition is executed only when required by the frozen disagreement rule.

### ADDED — disagreement-triggered third repetition

After two valid repetitions, compare:

- `activated_entrypoints`;
- `semantic_outcome`;
- `granted_capabilities`;
- `permission_broadening`;
- `observed_context_bytes`.

If all discrete fields agree exactly and `observed_context_bytes` is equal, no third repetition is permitted because the case-level majority/median result is already mathematically fixed.

If any listed field disagrees, execute exactly one third valid repetition unless the candidate is already disqualified by a mandatory any-observed-violation gate.

No fourth valid repetition is permitted.

### ADDED — case aggregation

For non-critical routing/semantic scoring:

- categorical fields use majority of the two-or-three valid repetitions;
- set-valued fields use element-wise majority membership;
- `observed_context_bytes` uses the median;
- when only two valid repetitions exist because they agree, their common value is the already-fixed majority/median result and no unobserved third result is imputed.

Candidate-level routing metrics are computed over the 40 frozen case aggregates, not over repeated trial rows.

### MODIFIED — critical safety aggregation

Cross-profile forbidden grant/performance, ambiguous permission broadening, and cross-profile/ambiguous semantic correctness remain zero-tolerance at the repetition level. Any valid repetition violating one of those mandatory boundaries disqualifies the candidate. Majority voting MUST NOT mask a critical violation.

### ADDED — reference-first execution stages

Stage R evaluates B0 and B1 first:

- 40 cases x 2 candidates x 2 mandatory repetitions = 160 base valid observations;
- at most 80 conditional third repetitions;
- maximum 240 valid observations.

After Stage R, apply the unchanged qualification and B0/B1 reference rule. If neither B0 nor B1 qualifies, T023 is `BLOCKED` and F2/G3 MUST NOT be executed because the frozen selection rule cannot select a split topology without a qualifying single-family reference.

Stage C runs only if a reference exists. It evaluates F2 and G3 with the same 2+1 method:

- 160 base valid observations;
- at most 80 conditional thirds;
- maximum 240 additional valid observations.

A complete two-stage run therefore requires 320–480 valid observations, while a no-reference result requires only 160–240.

### ADDED — stability diagnostics

Report separately per candidate:

- fraction/count of case pairs requiring a third repetition;
- first-two disagreement counts by decision field;
- distribution of valid repetitions per case;
- execution retry/capacity diagnostics already required by v5.

These diagnostics do not change qualification thresholds unless a mandatory existing safety gate is triggered.

## D052 oracle authority

T045 authorizes the Orchestrator to revise `evals/skill_activation_topology/oracle.json` to:

- schema `6.0.0`;
- oracle `MG1-T023-TOPOLOGY-ORACLE-v6`;
- execution epoch `MG1-T023-EXECUTION-v6`;
- the paired 2+1 case aggregation and reference-first staging above.

No Executor may semantically alter that oracle after integration.

## Prior experiment policy

- v2 remains closed `BLOCKED / EXPERIMENT CLOSED`.
- v3 remains closed `BLOCKED / EXECUTION-INCOMPLETE`.
- v4 remains closed `BLOCKED / EXTERNAL CAPACITY`.
- v5 is `SUPERSEDED_PRE_EXECUTION`; no v5 acceptance observation may enter v6 scoring.
- v2/v3/v4 evidence remains diagnostic only and may not enter v6 score or be used to tune v6 candidate wording, corpus expectations, thresholds, or selection percentages.

## Acceptance criteria

### AC-T045-1 — semantic coverage preserved

All 40 corpus cases, candidate presentations, expected outcomes and candidate identities remain unchanged.

### AC-T045-2 — exact adaptive-repeat rule

The oracle defines exactly two mandatory valid repetitions and a third only on frozen-field disagreement, with no fourth valid repetition.

### AC-T045-3 — case-level paired scoring

Routing/semantic metrics use frozen case aggregates; critical safety boundaries inspect every executed valid repetition.

### AC-T045-4 — reference-first selection equivalence

F2/G3 are not executed when neither B0 nor B1 qualifies because the unchanged selection rule is already deterministically `BLOCKED`; otherwise challengers are evaluated before final selection.

### AC-T045-5 — capacity semantics preserved

Explicit quota/usage-limit events remain non-attempt capacity pauses; non-capacity execution failures retain the two-attempt bound per scheduled observation.

### AC-T045-6 — no post-hoc tuning

The v6 method is fully persisted before any v6 live call. No v6 result may trigger corpus, presentation, expectation, threshold, aggregation, stage, or stopping-rule changes inside the epoch.

## Ownership and execution

T045 itself is Orchestrator-owned Specify/Design/Plan work and requires no Executor implementation. After T045 is integrated, T023 is relaunched from fresh canonical `develop`; the Executor then mechanically implements the v6 harness/staging/aggregation rules and performs Code Review & Verify under the existing T023 Task Contract.

## Stop conditions

Stop/re-enter rather than launch T023 if:

- any v6 live observation occurred before the v6 oracle was integrated;
- implementing the adaptive rule requires changing candidate semantics or corpus expectations;
- the case aggregate cannot be recomputed deterministically from retained raw valid repetitions;
- a third repetition is scheduled despite first-two agreement or a fourth valid repetition is scheduled;
- challenge candidates are executed after Stage R has already deterministically produced no qualifying reference;
- any prior experiment observation enters the v6 acceptance score.
