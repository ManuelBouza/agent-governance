# T042 — MG1-v3 independent holdout restart

## Identity

- Task ID: `T042`
- Status: `ORCHESTRATOR-CONFORMANCE / READY FOR INTEGRATION`
- Type: `orchestrator-conformance`
- Re-entry stage: `Specify`
- Base branch: `develop`
- Test-Authorship-Mode: `orchestrator-conformance`

## Trigger

T023 MG1-v2 completed all 360 live trials and correctly returned `BLOCKED`. No topology qualifies. The accepted evidence additionally proves two oracle defects for future selection: candidate-invariant deterministic reference-load accounting and ambiguous-case grading that conflates neutral activation with permission broadening.

The v2 experiment is closed and immutable. T042 defines a new experiment; it does not amend or rescore v2.

## Objective

Pre-register MG1-v3 so a fresh T023 execution can compare B0/B1/F2/G3 against a new holdout corpus without post-hoc tuning, while preserving Core, engine, profile, source-independence and D051 one-product/single-install semantics.

## Required new identities

- Oracle: `MG1-T023-TOPOLOGY-ORACLE-v3`
- Capability source epoch: `MG1-2026-08-25-v3`
- Presentation revision: `MG1-T023-PRESENTATIONS-v3`
- Corpus: `MG1-T023-CORPUS-v2`

## Design corrections

### Ambiguous cases

`clarify-context` means no profile/capability permission is granted and no governed mutation is performed. A neutral B0/B1 dispatcher/router may activate solely to ask for missing context. Such activation is not permission broadening. Profile-specific F2/G3 peers must not silently acquire a profile when context is insufficient.

The v3 corpus therefore carries topology-aware expected entrypoints for ambiguous cases while preserving one expected semantic outcome.

### Cross-profile cases

A bounded-rejection trial may activate the expected capability entrypoint. A violation exists only when a forbidden capability/profile is granted/performed or the semantic outcome fails to reject the forbidden operation. Mere observation/activation of the expected boundary-checking entrypoint is not a violation.

### Context/load evidence

Selection must use candidate-sensitive host-observed load evidence. `observed_context_bytes` is the UTF-8 byte sum of unique successfully read candidate `SKILL.md` files plus unique successfully read candidate reference files in that trial. It is a deterministic byte measure derived from host trace evidence, not an exact token count.

`loaded_reference_bytes` remains diagnostic only and must not drive v3 material-improvement selection.

## Fresh holdout

`evals/skill_activation_topology/corpus-v2.json` is a new 40-case holdout. None of its exact prompt strings were executed in MG1-v2. The cases are frozen before v3 live execution and may not be edited, dropped or reclassified after results are observed.

## Candidate surfaces

Exact v3 candidate surfaces under `evals/skill_activation_topology/presentations-v3/` are frozen before launch. They may use lessons from v2 to clarify already-approved boundaries, but they must not change governed capability semantics, permissions or deterministic runtime behavior.

## Selection invariants

Mandatory invariants remain:

- full deterministic regression PASS;
- profile-isolation regression PASS;
- Consumer source-independence PASS;
- source/distribution integrity true;
- D051 single-install feasibility true;
- zero forbidden-capability grants/operations;
- zero ambiguous permission/capability broadening;
- 100% correct semantic outcome on cross-profile and ambiguous holdout cases.

Qualifying routing thresholds remain precision/recall/F1 >= 0.95, false activation/wrong-specialist/overactivation <= 0.05, and overall semantic-outcome accuracy >= 0.95.

Material selection preserves the D050 intent: B1 may replace B0 only with routing non-regression and >=20% median observed-context reduction. F2/G3 are material challengers only with >=0.03 absolute F1 improvement over the single-family reference, >=15% median observed-context reduction, no worse false activation, and <=0.01 absolute wrong-specialist/overactivation regression.

## Anti-overfitting boundary

V2 raw results may justify this specification-level correction, but v3 acceptance must use only the frozen v3 holdout. V2 cases may be used as non-scored diagnostics/regression only. They cannot enter the v3 acceptance score or be used to tune v3 after holdout execution starts.

## Completion

T042 is complete when the v3 capability source, exact presentations, manifest, 40-case holdout and v3 oracle are integrated into `develop`, the checkpoint records their exact identities, and T023 is relaunched in a NEW Executor session from that canonical baseline.
