# T065 — T023 v17 Selective Capability Routing Evaluation

Status: READY  
Stage-Readiness: READY_FOR_STAGE5  
Executor-Authorization: NOT_AUTHORIZED_PENDING_SEPARATE_HUMAN_LAUNCH  
Owner: ChatGPT Orchestrator (Stages 3–5 / semantic conformance) / Executor (Stage 6 only after separate Human launch)  
Date: 2026-09-12  
Prospective-Scientific-Branch: `test/t023-selective-capability-routing-evals-v17`

## Objective

Produce the successor T023 selective-routing experiment after T064 Freeze G exposed model-visible instrumentation contamination and an incorrect conditional execution denominator.

T065 preserves the D078 experiment question and all unobserved statistical design controls while correcting the measurement surface before any confirmatory holdout or provider/model observation exists.

## Authority

- D050 — canonical capability source and evaluated Skill topology
- D052 — specification-owned conformance authorship
- D053 — native spec-driven development
- D061 / D062 — protected branch transport
- D068 — Orchestrator Stage 5 candidate materialization
- D074 — reference-independent topology qualification controls retained where compatible
- D076 — substantial executable materialization boundary
- D077 — version-sensitive upstream revalidation before live execution
- D078 — selective capability routing evaluation boundary
- `docs/reviews/T023-R39.md`
- predecessor design reference: `docs/tasks/T064-t023-selective-capability-routing-v16.md`

R39 controls the v16-to-v17 correction. T064 is failed historical evidence, not a candidate source.

## Historical failed boundary

```text
T064 branch: test/t023-selective-capability-routing-evals-v16
T064 Freeze G: 2a1742b04af589166da6bf1bab9a74d0429af1d9
T064 provider/model calls: 0
T064 scientific observations: 0
T064 confirmatory holdout: never authored
```

Do not rewrite or continue that branch.

## Canonical truth and candidate set

Canonical capabilities remain exactly:

```text
consumer-lifecycle
source-maintainer
external-skill-trust
```

Canonical dispositions remain:

```text
ROUTE
NONE
ABSTAIN
```

Truth may contain zero, one, or multiple capabilities. `NONE` is a confident empty set; `ABSTAIN` is underdetermination requiring clarification/fail-closed behavior.

Candidate packaging remains exactly B2/F2/G3 under `MG1-T023-TOPOLOGIES-v4`:

```text
B2:
  all capabilities -> agent-governance

F2:
  consumer-lifecycle   -> consumer-governance
  source-maintainer    -> source-maintainer
  external-skill-trust -> consumer-governance

G3:
  each capability -> same-named entrypoint
```

Candidate/presentation wording is not tuned.

Exact candidate/presentation bytes must be copied from pre-holdout v15 Freeze E:

`5b025087bc7b6996f683a34fdd1ce441d3d6dd82`

using the v15 candidate-hash provenance manifest and recorded immutable Git blobs.

## Measurement integrity correction

### Routing-only phase

The routing-only user stimulus is:

```text
fresh case prompt
+ two newlines
+ frozen domain-neutral planning/no-execution suffix
```

The suffix may instruct the agent not to perform material task execution and to return only a short planning disposition. It MUST NOT contain:

- `Agent Governance` / `agent-governance`;
- canonical capability names;
- candidate IDs B2/F2/G3;
- candidate entrypoint names;
- topology language or expected class labels.

The routing-only structured output contract is also domain-neutral. It may expose generic fields such as:

```text
clarification_requested: boolean
bounded_refusal: boolean
response_summary: string
```

It MUST NOT enumerate or ask the model to report capability names, entrypoint names, expected routing class, task success, or semantic execution success.

### Routing observation authority

Scored routing evidence comes from host-observed successful body/reference reads.

```text
observed_activation_set
  = entrypoint SKILL.md bodies successfully read/used by host trace

observed_capability_set
  = candidate capability references successfully read/used by host trace
```

Model self-report MUST NOT override contradictory trace evidence.

Derived disposition:

```text
observed activation/capability non-empty -> ROUTE
otherwise clarification_requested       -> ABSTAIN
otherwise                               -> NONE
```

For a shared entrypoint such as B2 or F2, activating the shared entrypoint is insufficient to prove correct capability routing; the loaded capability-reference set must match topology-independent truth.

### End-to-end phase

End-to-end confirmation uses a separate phase-specific domain-neutral result schema that may include generic execution fields such as task success, bounded refusal, and semantic outcome. It still must not reveal oracle capability labels or expected answer classes.

Routing correctness on end-to-end reserve cases is computed from trace with the same exact-set rule as routing qualification.

The conditional execution estimand is exactly:

```text
P(execution success | exact routing correct)
```

A reserve observation with wrong capability set, wrong activation projection, false activation, or missed routing is an end-to-end failure and is excluded from the conditional execution-success denominator.

## Development / calibration boundary

Before Freeze I, Stage 5 may materialize exactly 90 non-confirmatory cases:

```text
consumer-lifecycle single-label:       20
source-maintainer single-label:        20
external-skill-trust single-label:     20
NONE:                                  15
ABSTAIN:                                5
cross-profile:                          5
multi-intent:                           5
total:                                 90
```

Development cases do not enter confirmatory scoring.

No artificial confidence score is introduced. If the host exposes no real router score, calibration probability metrics are `NOT_APPLICABLE`.

## Freeze I — corrected candidate / analysis boundary

Before any v17 confirmatory holdout exists, publish and remotely verify Freeze I containing:

- exact B2/F2/G3 bytes from v15 Freeze E;
- new v17 candidate provenance receipt;
- capability-routing contract;
- unchanged topology projection;
- complete statistical analysis plan;
- 90-case development boundary;
- corrected domain-neutral routing-only instrumentation;
- separate end-to-end instrumentation;
- trace parser/materializer/scheduler/budget/resume mechanics;
- preflight and canary scoring mechanics;
- provider-free candidate/instrumentation guards and tests.

The v17 confirmatory corpus/oracle/trial-envelope MUST NOT exist at Freeze I.

## Fresh confirmatory geometry

Only after remote Freeze I verification, author a fresh holdout.

### Routing-confirmatory — 270 unique cases

```text
consumer-lifecycle:                    60
source-maintainer:                     60
external-skill-trust:                  60
NONE:                                  60
  of which fresh near-misses:          30
ABSTAIN:                               10
cross-profile:                         10
multi-intent / multi-label:            10
total:                                270
```

Primary backbone = the 240 single-label/NONE cases. Challenge = 30 ABSTAIN/cross-profile/multi-intent cases.

The 30 near-misses should preserve five semantically applicable axes with six cases each:

```text
unrelated-source-maintenance
generic-skill-tooling
explicit-non-applicability
incidental-mention
homonym-outside-product
```

### Reliability subset

Pre-designate exactly 30 routing case IDs before Stage 6. Each candidate receives exactly one additional independent trial for those IDs after first-trial routing is complete.

Repeated trials measure within-case agreement only and never increase independent N.

### End-to-end reserve — 60 unique cases

```text
consumer-lifecycle:                    15
source-maintainer:                     15
external-skill-trust:                  15
multi-intent:                          10
cross-profile:                          5
total:                                 60
```

The reserve is disjoint from routing qualification and is not opened to routing-ineligible candidates.

### Historical overlap

All v17 IDs/prompts are unique and exact prompt overlap must be zero against exposed T023 v12, v13, v14, v15 and any T064 development prompts. T064 has no confirmatory prompts.

Historical observations never enter v17 scoring.

## Freeze J — holdout boundary

Freeze J contains:

- fresh routing-confirmatory corpus;
- disjoint end-to-end reserve;
- topology-independent oracle;
- 30-case reliability subset;
- phase-specific domain-neutral trial envelope;
- historical-overlap and geometry guard.

Freeze I must be an ancestor of Freeze J. Candidate bytes, topology mapping, routing contract and analysis plan must remain byte-stable I -> J.

## Primary routing corpus SLOs

These are corpus acceptance SLOs:

```text
activation precision >= 0.95
per-capability recall >= 0.95
micro activation F1 >= 0.95
macro activation F1 >= 0.95
NONE false activation rate <= 0.05
wrong-specialist rate <= 0.05
overactivation rate <= 0.05
critical cross-profile / permission-invalid activation = 0
ABSTAIN correct disposition >= 0.90
multi-intent exact-set routing >= 0.90
critical ambiguous permission broadening = 0
```

All generalization rates use unique first-trial cases.

## Uncertainty and paired analysis

Report exact one-sided 95% binomial intervals for each per-capability recall and NONE false-activation rate. Sixty independent cases per primary stratum preserves the v16 rationale and does not imply a population guarantee unless the interval supports it.

All candidates use common cases. Pre-register:

- exact paired/McNemar-compatible binary comparison;
- paired case-level bootstrap for nonlinear quality/context/cost/latency deltas;
- Holm correction across planned pairwise claims;
- no post-hoc selection metric.

Default primary paired routing endpoint:

`exact routing correctness on the 240-case primary backbone`.

## Routing finalist rule

A candidate must pass every absolute routing/safety SLO and reliability SLO.

Reliability SLO:

```text
exact-set/disposition agreement >= 0.90
critical safety disagreement = 0
```

If B2 qualifies, a split may be materially eligible only when:

```text
all absolute SLOs pass
paired exact-routing non-inferiority lower bound >= -0.02 vs B2
median observed routing/context load <= 0.85 * B2
paired evidence does not show material context regression
critical violations = 0
```

At most two finalists proceed.

If both F2 and G3 are materially eligible, choose one challenger only when the frozen paired evidence shows it non-worse on exact routing and context and strictly better on at least one observed dimension. Otherwise return `NO_TOPOLOGY_SELECTED` rather than force a tie-break.

If B2 is routing-ineligible, up to two independently qualified splits may proceed.

## End-to-end confirmation

Each finalist receives exactly one scientific execution over all 60 reserve cases, subject only to technical retry rules.

Report separately:

```text
P(execution success | exact routing correct)
end-to-end task success
semantic accuracy
critical profile/permission violations
context / latency / provider usage
```

Corpus SLOs:

```text
semantic accuracy conditional on exact routing correct >= 0.95
end-to-end task success >= 0.95
critical cross-profile / permission violations = 0
deterministic/profile/source/distribution/integrity gates = PASS
```

If B2 and a split both remain qualified, the split must be execution-quality non-inferior at absolute margin `-0.02`, retain the pre-registered context/Pareto advantage, and have zero critical regressions to replace B2.

Unresolved non-dominated finalists produce no topology selection.

## Stage 6 budget

Stage 5 provider/model calls MUST remain exactly `0`.

Prospective Stage 6 envelope:

```text
routing first trials:       270 * 3 = 810
reliability repeats:         30 * 3 =  90
end-to-end reserve:   60 * max 2 = 120
base scientific maximum:             1020
behavioral preflight reserve:            4 attempts
synthetic canary reserve:                4 attempts
absolute attempt ceiling:             1264
```

Thus up to 236 attempts remain as global technical retry reserve after nominal science + maximum preflight/canary.

Each scheduled scientific observation may use at most two attempts. Exhausting the global ceiling is technical incompleteness; sample geometry may not be silently reduced.

This budget is NOT provider authorization.

## Behavioral preflight and canary

Stage 5 must materialize explicit expected pass/fail semantics.

Behavioral preflight may use at most four total model attempts and must prove the selected runtime can expose the trace/read and structured-response surfaces required by the frozen harness.

Synthetic canary may use at most four total model attempts and requires **2/2 logical canary cases PASS** before confirmatory routing begins.

A process exit code alone is insufficient to pass either gate.

## Stage 5 materialization order

1. refresh protected `develop` and D061/D062 state;
2. create `test/t023-selective-capability-routing-evals-v17` from that exact `develop`;
3. copy exact candidate/presentation/topology bytes only from v15 Freeze E;
4. materialize corrected routing/e2e instrumentation, analysis, 90-case development data, complete substantial harness/controller/oracle mechanics, tests and candidate guard;
5. run provider-free candidate/instrumentation verification;
6. publish and remotely verify Freeze I;
7. only then author the fresh 270 + 60 confirmatory corpus/oracle/trial envelope and holdout guard;
8. publish and remotely verify Freeze J;
9. complete full provider-free repository verification with provider/model calls exactly 0;
10. persist Stage 5 readiness review/checkpoint on `develop`;
11. stop before Executor launch.

## Stage 6 pre-acceptance order

Only after separate future Human launch authority:

1. provider-free candidate/holdout/integrity/quality gates;
2. D077-revalidated exact live cell/backend/workspace/version behavioral preflight;
3. synthetic canary 2/2 PASS;
4. B2/F2/G3 routing first trials;
5. 30-case reliability repeats;
6. frozen routing analysis and finalist determination;
7. end-to-end reserve for at most two finalists;
8. complete evidence/handoff.

## Required handoff

Future handoff path:

`handoffs/T065-executor-handoff.json`

It must record exact attempts by phase/retries, routing metrics/intervals, reliability, paired comparisons, finalist determination, end-to-end conditional and total metrics, D076 ephemeral-artifact audit, D077 state, and any re-entry condition.

## Live cell and provider authorization

No live cell is inherited or authorized here.

Before Stage 6, Orchestrator must freshly revalidate the exact host/runtime/model/reasoning/CLI surface under D077 and obtain fresh Human authorization for the exact provider destination, payload and usage/cost envelope.

T062/R36 authorization and all prior v15/v16 authorization states are non-transferable.

## Stage 5 acceptance

Stage 5 completes only when:

- v17 scientific branch is rooted at then-current protected develop;
- exact candidate provenance from Freeze E is verified;
- corrected domain-neutral instrumentation tests pass;
- Freeze I exists and is remotely verified before any confirmatory holdout exists;
- fresh holdout is authored only after Freeze I;
- Freeze J exists and is remotely verified;
- holdout geometry/independence/overlap/oracle guards pass;
- all foreseeable substantial Stage 6 executable mechanics are represented per D076;
- full provider-free repository tests/lint/format/code-health/symbol-map gates pass;
- Stage 5 provider/model calls = 0;
- no Executor has been launched;
- readiness review/checkpoint is merged on develop.

## Fail closed

Any model-visible oracle-label contamination, candidate-byte mismatch, holdout leakage, historical exact prompt overlap, topology/capability coupling error, frozen-analysis drift, unauthorized Stage 5 provider call, missing material Stage 6 controller/oracle behavior, or lineage ambiguity is a STOP condition.

After Freeze I or Freeze J, a material semantic/design/statistical defect requires another explicit successor epoch; never rewrite a published freeze.
