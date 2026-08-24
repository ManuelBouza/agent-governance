# MG1 — Skill Activation Topology and Eval Pre-registration Gate

Status: `READY_FOR_INTEGRATION`  
Date: 2026-08-24  
Owner: ChatGPT Orchestrator  
Applies to: `T023`  
Test-Authorship-Mode: `mixed`  
Oracle revision: `MG1-T023-TOPOLOGY-ORACLE-v1`

## Gate purpose

MG1 freezes the semantic experiment authority required by T023 before comparative topology results are observed.

T022 is accepted. The accepted Core, shared deterministic engine, Consumer profile, source-maintainer profile, external Skill trust semantics, source-independence boundary and one-product/single-install constraint are held constant. T023 may compare activation presentation only.

No T023 comparative result was available to the Orchestrator when this revision was authored.

## Frozen capability source

Canonical capability/routing source for this experiment:

`docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md`

Capability-Source-Epoch:

`MG1-2026-08-24-v1`

It defines exactly three capability families for topology projection:

- `consumer-lifecycle`;
- `source-maintainer`;
- `external-skill-trust`.

This source is subordinate to `governance-core/`, accepted runtime/profile semantics and controlling source/Consumer policy. It does not authorize new deterministic behavior.

## Frozen topology candidates

Executable candidate identity data:

`evals/skill_activation_topology/topologies.json`

Required candidates are exactly:

- B0 — unified dispatcher baseline;
- B1 — thin single router;
- F2 — Consumer Governance + Source Maintainer generated profile peers;
- G3 — Consumer Lifecycle + Source Maintainer + External Skill Trust hybrid challenger.

No additional candidate may enter the T023 acceptance comparison without a new persisted Orchestrator revision that restarts the affected experiment before results for that candidate are used.

All candidates are projections of one Agent Governance product, one Core, one shared engine and one capability-source epoch. Portable Skill-to-Skill invocation is forbidden.

## Frozen D052 corpus

Acceptance corpus:

`evals/skill_activation_topology/corpus.json`

Corpus-ID:

`MG1-T023-CORPUS-v1`

The corpus contains 30 pre-registered cases spanning:

- positive Consumer lifecycle;
- positive source-maintainer;
- positive external Skill trust;
- negative generic coding/SDD/tooling/release prompts;
- near-miss Governance/Skill/profile/source wording;
- cross-profile mutation/permission traps;
- ambiguous context cases;
- multi-intent cases.

Expected semantics are frozen as capability sets plus one of `activate`, `no-activation`, `bounded-rejection`, or `clarify-context`. Expected physical entrypoints are derived mechanically from the frozen topology mapping; they are not rewritten per candidate after trials.

## Frozen trial and host/model method

Selection oracle:

`evals/skill_activation_topology/oracle.json`

Required live activation cell:

- Host: Codex
- Platform: native Windows
- Model: GPT-5.6 Sol
- Effort: Medium

Each case/candidate combination receives 3 clean-context acceptance trials. Candidate order rotates deterministically by case/repetition. No training partition is used because topology definitions, corpus semantics and thresholds are frozen before trials and may not be fitted to the acceptance corpus. Mechanical runner smoke cases may exist but do not enter acceptance scores.

If the required live cell cannot be executed reproducibly, T023 is `BLOCKED`; the Executor may not silently substitute a different host/model and present it as the pre-registered result.

## Metrics and context evidence

T023 must compute the oracle-defined:

- activation precision, recall and F1;
- negative/near-miss false activation;
- wrong-specialist rate;
- overactivation;
- semantic-outcome accuracy;
- cross-profile violations;
- median and p95 deterministic loaded-reference bytes;
- one-product/single-install feasibility;
- source/distribution integrity.

`loaded_reference_bytes` is an explicitly labelled deterministic load model, not an exact token count. Host-observed token/context traces, if available, are additional host-specific evidence and must be recorded separately.

## Mandatory non-regression boundaries

Every selected candidate must preserve:

- full deterministic regression PASS;
- profile-isolation regression PASS;
- Consumer source-independence regression PASS;
- one Core / one shared engine / one capability-source epoch;
- D051 one-product/single-install feasibility;
- zero cross-profile permission/mutation violations;
- zero ambiguous-context permission broadening;
- 100% correct bounded behavior for cross-profile and ambiguous cases.

Any violation disqualifies the candidate regardless of routing/context score.

## Qualifying thresholds

A candidate must additionally meet all of:

- activation precision >= 0.95;
- activation recall >= 0.95;
- activation F1 >= 0.95;
- false activation rate <= 0.05;
- wrong-specialist rate <= 0.05;
- overactivation rate <= 0.05;
- overall semantic-outcome accuracy >= 0.95.

These thresholds are frozen before T023 comparative results and may not be weakened post hoc.

## Material-improvement and final selection rule

The exact machine-readable rule is frozen in the oracle JSON. In summary:

1. Disqualify candidates failing mandatory or qualifying thresholds.
2. Establish a single-family reference from B0/B1. B1 replaces B0 only when it is essentially routing-non-regressive and reduces median deterministic load to <=80% of B0; otherwise B0 remains the reference. If only one qualifies, that one is the reference. If neither qualifies, T023 is blocked.
3. F2/G3 count as material challengers only when they improve activation F1 by at least 0.03 absolute over the single-family reference, reduce median deterministic load to <=85% of reference, do not worsen false activation, and keep wrong-specialist/overactivation within 0.01 absolute of reference.
4. If no split challenger meets that bar, select the single-family reference. Fragmentation is not forced.
5. If both split challengers qualify materially, apply the frozen F1 -> false-activation -> load -> fewer-entrypoints tie-break sequence. Exact remaining ties select F2.

## D052 ownership boundary

The following are Orchestrator-owned semantic conformance assets and are frozen for T023:

- `docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md`;
- `evals/skill_activation_topology/topologies.json`;
- `evals/skill_activation_topology/corpus.json`;
- `evals/skill_activation_topology/oracle.json`;
- this MG1 gate.

The Executor owns technical runner/provider adapters, trial isolation, result collection, metric computation, deterministic load instrumentation, package-feasibility plumbing, supplementary diagnostics and ordinary implementation/regression tests.

The Executor must stop the affected claim with an `ORACLE_DEFECT`-equivalent blocker if it finds a semantic defect in the frozen assets. It must not change corpus membership, expected semantic outcomes, topology mapping, thresholds or selection meaning.

## T023 readiness

T023 becomes executable only after this MG1 branch is reviewed and integrated into canonical `develop` and the checkpoint records the exact integrated MG1 revision/base.

T023 remains evaluative: it selects an activation topology only. It may not alter Core/runtime/profile semantics, create independently maintained Governance products, require portable Skill-to-Skill invocation, or implement final T024 distribution wrappers.
