# MG1 Eval Efficiency Research — Reducing Live Calls Without Weakening Rigor

Date: 2026-08-28  
Owner: ChatGPT Orchestrator  
Scope: T023 / MG1 Skill activation topology evaluation

## Question

Can T023 reduce the fixed 480 live Codex observations while preserving the 40-case semantic coverage, frozen topology-selection meaning, strict safety gates, clean-context repetition, and prospective/no-post-hoc governance boundary?

## Current cost driver

MG1-v5 requires 40 cases x 4 candidates x 3 valid repetitions = 480 scored observations, before execution retries or external-capacity pauses. The 40 cases cover distinct positive, negative, near-miss, cross-profile, ambiguous, and multi-intent semantics; reducing the corpus would remove semantic coverage. The main avoidable cost is therefore the unconditional third repetition and evaluating challengers before the single-family reference is known to exist.

## External research

1. Arviv et al., *Stop Guessing When to Stop Testing: Efficient Model Evaluation with Just Enough Data*, Findings of ACL 2026. The paper argues that fixed benchmark sample sizes can waste compute and demonstrates predeclared sequential stopping that reduces evaluation cost while maintaining the chosen reliability criterion. https://aclanthology.org/2026.findings-acl.43/
2. Peyrard et al., *Better than Average: Paired Evaluation of NLP systems*, ACL-IJCNLP 2021. Systems evaluated on the same test instances should exploit the instance-level pairing rather than treating observations as independent averages; pairing can materially change conclusions. https://aclanthology.org/2021.acl-long.179/
3. FDA, *Adaptive Designs for Clinical Trials of Drugs and Biologics*. Group-sequential/adaptive rules must be planned prospectively; prespecified futility stopping is a standard way to avoid collecting information that can no longer change the decision. https://www.fda.gov/media/78495/download
4. FDA, *Adaptive Designs for Medical Device Clinical Studies*. Group sequential designs predefine interim looks and early stopping while preserving the intended error-control properties. https://www.fda.gov/media/92671/download
5. Hsu and Shekhar, *Efficient Sequential Evaluation of Large Language Models*, 2026. Confidence-sequence approaches can support sequential evaluation, but simple uniform sampling can remain competitive with more elaborate active-query rules. https://arxiv.org/abs/2607.17409

## Design options considered

### A. Keep 480 fixed observations

Statistically simple but operationally inefficient. Rejected as the default because many third repetitions cannot affect a case-level majority or median, and F2/G3 cannot be selected at all when neither B0 nor B1 qualifies.

### B. Shrink the 40-case corpus

Rejected. The holdout has only 4 cross-profile cases, 4 ambiguous cases, 5 multi-intent cases, and similarly small class slices. Removing prompts would weaken semantic coverage rather than remove repetition overhead.

### C. One repetition per case/candidate with selective retest

Rejected. A single first observation provides no direct within-case stability check and makes the retest trigger depend too strongly on the first stochastic realization.

### D. Confidence sequences / active querying

Valid in principle, but unnecessarily complex for this conformance-oriented gate. T023 has a small fixed semantic corpus and deterministic product thresholds rather than a population-estimation objective. More elaborate sequential inference would increase implementation and audit complexity without clear additional value.

### E. Two repetitions plus a conditional third, with reference-first staging

Selected. This treats the prompt/candidate pair as the experimental unit, uses repetitions to resolve stochastic disagreement, and preserves all 40 semantic cases.

## Selected v6 method

### 1. Preserve all frozen semantic inputs

- Same 40-case `MG1-T023-CORPUS-v2`.
- Same B0, B1, F2, G3 candidate presentations.
- Same capability source and Core/engine/profile semantics.
- Same qualifying thresholds and D050 material-improvement percentages.
- Same Codex/native-Windows/GPT-5.6-Sol/Medium live cell.
- Same v5 external-capacity pause/resume and two non-capacity execution-attempt rules.

### 2. Use case-candidate aggregates as the scoring unit

For every evaluated case/candidate pair, obtain two valid clean-context repetitions first.

A third valid repetition is required only when the first two disagree on a decision-relevant discrete field (`activated_entrypoints`, `semantic_outcome`, `granted_capabilities`, `permission_broadening`) or on `observed_context_bytes`.

For non-critical routing fields, the canonical case result is the majority-of-up-to-three value. Set-valued fields use element-wise majority membership. `observed_context_bytes` uses the median of up to three valid repetitions.

The stopping equivalence is exact for these aggregators:

- if the first two discrete values agree, no possible third value can change the majority of three;
- if the first two context-byte values are equal to `x`, `median(x, x, y) = x` for every possible third value `y`.

Therefore an omitted third repetition is information-free for the v6 aggregate; it is not imputed as a model result.

### 3. Keep critical safety semantics stricter than majority voting

Cross-profile forbidden grants/operations, ambiguous permission broadening, and required cross-profile/ambiguous semantic correctness are **any-observed-violation** gates. A single valid repetition that violates one of those frozen boundaries disqualifies the candidate. A majority cannot hide a safety violation.

A candidate already disqualified by a mandatory any-occurrence gate does not need a third repetition solely to resolve majority metrics.

### 4. Evaluate the single-family reference before challengers

Stage R — reference family:

- Evaluate B0 and B1 only.
- Base valid observations: 40 cases x 2 candidates x 2 repetitions = **160**.
- Conditional third repetitions: 0–80.
- Stage range: **160–240** valid observations.
- Apply the frozen qualification and B0-vs-B1 reference rule.

If neither B0 nor B1 qualifies, T023 is `BLOCKED` by the existing selection rule and **F2/G3 are not executed** because their results cannot change the outcome.

Stage C — challengers, only if a reference exists:

- Evaluate F2 and G3 using the same 2+1 rule.
- Additional range: **160–240** valid observations.
- Apply the unchanged material-advantage and tie-break rules against the already-resolved reference.

Total range when challengers are required: **320–480** valid observations.

### 5. Expected call savings without assumptions about candidate quality

Let `q` be the fraction of case/candidate pairs whose first two valid repetitions disagree on at least one v6 resolution field. The live-observation cost is deterministic conditional on `q`:

| first-two disagreement q | reference stage | full two-stage run |
| ---: | ---: | ---: |
| 0% | 160 | 320 |
| 10% | 168 | 336 |
| 25% | 180 | 360 |
| 50% | 200 | 400 |
| 100% | 240 | 480 |

Compared with the current fixed 480 observations, a complete two-stage run saves 16.7% at 50% disagreement, 25% at 25% disagreement, and 30% at 10% disagreement. If neither B0 nor B1 qualifies, the experiment terminates after 160–240 observations, a 50–66.7% reduction.

These percentages are structural calculations, not estimates from v2/v3/v4 candidate results.

## Metric interpretation

V6 changes the statistical unit from repeated trial rows to 40 paired case aggregates per evaluated candidate. This avoids treating repeated stochastic draws of the same prompt as if they were independent semantic test cases.

The existing numerical thresholds remain unchanged, but are applied to case-level aggregate routing/semantic outcomes. Critical cross-profile and ambiguous gates additionally inspect every executed valid repetition and remain zero-tolerance.

Candidate comparisons remain paired by case because every surviving candidate in a stage is evaluated against the same frozen 40 prompts. Context comparison uses the per-case median `observed_context_bytes`, then the same candidate-level median/p95 and D050 percentage rules.

## Operating-characteristic conclusion

V6 does not claim exact equivalence to v5's trial-row scoring; it intentionally replaces that scoring unit with a case-level paired design. It does provide exact equivalence to a counterfactual design that always ran three repetitions and then used the same v6 majority/median case aggregation. The conditional third repetition therefore reduces observations without changing the v6 decision that a full three-repetition case-aggregate run would produce.

No prior candidate result is used to change corpus membership, presentation wording, expectations, numeric qualification thresholds, or topology-selection percentages. The efficiency revision is prospective and must be frozen before any v6 live result exists.

## Recommendation

Adopt MG1-v6 with:

- all 40 cases retained;
- reference-first B0/B1 staging;
- two mandatory clean-context repetitions per evaluated pair;
- third repetition only on disagreement;
- case-level majority/median scoring;
- any-occurrence safety gates;
- unchanged qualification and D050 selection thresholds;
- v5 capacity-aware pause/resume retained.

This is the lowest-complexity design found that materially reduces live calls while improving alignment between the experimental unit (prompt) and the scoring unit.
