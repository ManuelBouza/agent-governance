# T064 — T023 v16 Selective Capability Routing Evaluation

Status: READY  
Stage-Readiness: READY_FOR_STAGE5  
Executor-Authorization: NOT_AUTHORIZED_PENDING_SEPARATE_HUMAN_LAUNCH  
Owner: ChatGPT Orchestrator (D053/D068 Stages 3–5 and semantic conformance) / Executor (Stage 6 only after separate Human launch)  
Date: 2026-09-12  
Prospective-Scientific-Branch: `test/t023-selective-capability-routing-evals-v16`

`READY_FOR_STAGE5` means the T023 v16 specification, Design, analysis plan and Stage 5 materialization boundary are complete enough for Orchestrator-owned candidate/eval materialization. It does **not** authorize an Executor or any provider/model call.

## Objective

Evaluate B2, F2 and G3 as **activation-packaging hypotheses over one topology-independent capability truth**, qualify routing before paying full specialist-execution cost, and select a topology only when routing, safety, execution quality and context/cost evidence support the decision under the pre-registered v16 analysis plan.

T064 implements D078. It does not retrofit or execute the frozen T062/v15 epoch.

## Authority and trace

- `docs/decisions/D050-canonical-capability-source-and-evaluated-skill-topology.md`
- `docs/decisions/D052-specification-owned-conformance-test-authorship.md`
- `docs/decisions/D053-native-spec-driven-development.md`
- `docs/decisions/D061-orchestrator-branch-target-write-guard.md`
- `docs/decisions/D068-library-first-candidate-materialization-executor-verification-boundary.md`
- `docs/decisions/D074-reference-independent-topology-qualification.md`
- `docs/decisions/D076-stage6-ephemeral-executable-materialization-boundary.md`
- `docs/decisions/D077-version-sensitive-upstream-revalidation.md`
- `docs/decisions/D078-selective-capability-routing-evaluation-boundary.md`
- `docs/research/T023-SELECTIVE-CAPABILITY-ROUTING-RESEARCH.md`
- `docs/reviews/T023-R37.md`
- historical retained-control reference: `docs/tasks/T062-t023-riq-nbc-v15-reference-independent-evaluation.md`

D078 controls the v16 methodology. D050 remains the architectural authority for one product/capability source and an evaluated activation projection. D074's candidate independence is retained, but its v15-specific selection mechanics are superseded by this contract for v16.

## Frozen historical boundary

T062 / T023 v15 remains frozen and unconsumed:

```text
scientific branch:  test/t023-skill-activation-topology-evals-v15
scientific HEAD:    5a2a3effeabede6640d10a8aa80ae6f70008764c
Stage5 candidate:   3e0d0b71cf382db502e186622f40a23bcd915390
Freeze E:           5b025087bc7b6996f683a34fdd1ce441d3d6dd82
Freeze F:           5b8ac55980ecdbb6a2bf3784812b933647f2f13d
provider calls:     0
observations:       0
```

Do not execute, rewrite, merge, rebase or repurpose that branch. Its holdout is not a v16 confirmatory dataset.

## Canonical capability taxonomy

v16 uses exactly the three capabilities already represented by D050 and the accepted topology metadata:

```text
consumer-lifecycle
source-maintainer
external-skill-trust
```

The semantic truth for a request is independent of B2/F2/G3 packaging.

A request may have:

- zero capabilities;
- exactly one capability;
- multiple capabilities.

No topology-specific entrypoint name may appear in `capability_truth`.

## Routing dispositions

Every v16 case has one of three dispositions:

### `ROUTE`

There is enough information to identify a non-empty capability set.

```text
routing_disposition = ROUTE
capability_truth = {one or more canonical capabilities}
```

### `NONE`

Agent Governance is not applicable.

```text
routing_disposition = NONE
capability_truth = {}
```

This is a correct no-activation/direct outcome, not uncertainty.

### `ABSTAIN`

The request is materially underdetermined for safe specialist selection and should trigger clarification/fail-closed behavior rather than a guessed specialist.

```text
routing_disposition = ABSTAIN
capability_truth = null
admissible_capability_sets = <two or more plausible canonical sets when representable>
```

`NONE` and `ABSTAIN` MUST NOT be merged in scoring.

## Topology projection

The v16 candidate set remains exactly `B2`, `F2`, `G3`. No candidate wording tuning is authorized merely because the methodology changed.

The accepted mapping is the v15 `MG1-T023-TOPOLOGIES-v4` mapping:

### B2 — `positive-anchor-single-router`

```text
consumer-lifecycle    -> agent-governance
source-maintainer     -> agent-governance
external-skill-trust  -> agent-governance
```

### F2 — `generated-profile-peers`

```text
consumer-lifecycle    -> consumer-governance
source-maintainer     -> source-maintainer
external-skill-trust  -> consumer-governance
```

### G3 — `hybrid-challenger`

```text
consumer-lifecycle    -> consumer-lifecycle
source-maintainer     -> source-maintainer
external-skill-trust  -> external-skill-trust
```

For a `ROUTE` multi-label case, expected activation units are the set-union of the mapped entrypoints. Duplicate mappings collapse to one entrypoint. For `NONE` and `ABSTAIN`, the expected activation set is empty; `ABSTAIN` additionally requires the pre-registered clarification/fail-closed semantic outcome.

Portable Skill-to-Skill invocation remains forbidden as a requirement. The host/current Agent is the portable router under D050.

## Candidate provenance and no-tuning rule

The v16 scientific branch MUST be created fresh from the then-current protected `develop`; it MUST NOT inherit the v15 scientific branch.

Exact candidate/presentation bytes may be copied only from the pre-holdout v15 Candidate Freeze E:

`5b025087bc7b6996f683a34fdd1ce441d3d6dd82`

using `evals/skill_activation_topology/candidate-hashes-v15.json` and the immutable source blobs it records.

The following identities remain fixed unless Stage 5 discovers a concrete contradiction requiring Orchestrator re-entry:

```text
capability source:      MG1-2026-09-06-v4
topology metadata:      MG1-T023-TOPOLOGIES-v4
presentation revision:  MG1-T023-PRESENTATIONS-v5
candidate set:          B2 / F2 / G3
```

v16 must create a new candidate manifest identity and provenance receipt without changing those candidate bytes.

## v16 scientific identities

Stage 5 SHALL materialize coherent identities equivalent to:

```text
evaluation:              MG1-T023-EVALUATION-v16
capability routing:      MG1-T023-CAPABILITY-ROUTING-v1
candidate hashes:        MG1-T023-CANDIDATE-HASHES-v4
corpus:                  MG1-T023-CORPUS-v10
oracle:                  MG1-T023-TOPOLOGY-ORACLE-v16
execution:               MG1-T023-EXECUTION-v16
trial envelope:          MG1-T023-TRIAL-ENVELOPE-v4
analysis plan:           MG1-T023-ANALYSIS-v1
candidate freeze:        Freeze G
holdout freeze:          Freeze H
```

Schema version strings are Stage 5 implementation details only if they preserve these semantic identities and the contract below.

## Development / calibration boundary

Before Freeze G, Stage 5 may create an explicitly non-confirmatory development/calibration set of **90 unique cases** for:

- validating capability labels and disposition encoding;
- validating the routing-only harness and trace extraction;
- validating topology projection mechanics;
- calibrating a real router score only if a candidate actually exposes and uses such a score.

Recommended fixed geometry:

```text
consumer-lifecycle single-label:       20
source-maintainer single-label:        20
external-skill-trust single-label:     20
NONE:                                  15
ABSTAIN:                                5
cross-profile challenge:                5
multi-intent challenge:                 5
total:                                 90
```

These cases are development data only. They MUST NOT enter confirmatory v16 routing or end-to-end scoring.

A raw LLM-authored confidence value is not a calibrated score. If the host-native baseline exposes no meaningful decision score, calibration metrics are `NOT_APPLICABLE`; no artificial confidence field may be invented.

## Freeze G — candidate and analysis pre-registration

Before any confirmatory holdout exists, Stage 5 SHALL publish and remotely verify Freeze G containing at least:

- exact B2/F2/G3 candidate/presentation bytes copied from Freeze E;
- v16 candidate provenance manifest;
- the canonical capability-routing contract;
- unchanged topology mapping/projection metadata;
- the complete v16 analysis plan and thresholds;
- development/calibration data, clearly excluded from confirmatory scoring;
- provider-free guards sufficient to prove candidate identity and no forbidden v15 holdout/evidence import.

The v16 confirmatory corpus/oracle identities MUST NOT exist before Freeze G.

## Fresh confirmatory holdout

Only after remote Freeze G verification, Stage 5 SHALL author a completely fresh v16 holdout.

It consists of two disjoint partitions.

### A. Routing-confirmatory partition — 270 unique cases

Primary inferential/SLO backbone:

```text
consumer-lifecycle single-label:       60
source-maintainer single-label:        60
external-skill-trust single-label:     60
NONE:                                  60
                                        ---
primary backbone:                       240
```

Challenge partition:

```text
ABSTAIN / ASK:                          10
cross-profile:                          10
multi-intent / multi-label:             10
                                        ---
challenge:                               30
```

Total routing-confirmatory cases: `270`.

The 60 `NONE` cases SHOULD include both clear negatives and near-misses. If the prior five near-miss axes remain semantically applicable, use six fresh cases per axis (30 near-misses) plus 30 other clear negatives. No exact prompt may be reused from v12, v13, v14 or v15 corpora.

### B. End-to-end reserve — 60 unique cases

This partition is frozen at the same holdout boundary but hidden from routing qualification and reserved for routing-qualified finalists only.

Geometry:

```text
consumer-lifecycle single-label:       15
source-maintainer single-label:        15
external-skill-trust single-label:     15
multi-intent:                           10
cross-profile:                           5
                                        ---
total:                                  60
```

These 60 cases MUST NOT be used to choose or tune routing thresholds/candidate metadata. They become visible to execution only after finalists are determined by the routing-confirmatory partition.

## Historical-overlap guard

The v16 holdout guard MUST fail closed unless all case IDs/prompts are unique and exact prompt overlap is zero against every prior exposed T023 corpus needed to cover at least v12, v13, v14 and v15.

Historical observations never enter v16 scoring.

## Freeze H — holdout/oracle boundary

Freeze H SHALL contain the complete fresh confirmatory corpus, topology-independent oracle truth, trial envelope and required integrity guards.

Freeze G must be an ancestor of Freeze H. Candidate bytes, topology mapping, routing contract and analysis plan MUST remain byte-stable across Freeze G -> Freeze H.

After Freeze H, changes to semantic holdout truth, sample geometry, margins, thresholds or selection policy require an explicit successor epoch; they are not Stage 6 repairs.

## Routing-only observation model

For each routing-confirmatory case and topology, Stage 6 records at minimum:

```text
case_id
topology
routing_disposition_truth
capability_truth or admissible ambiguity sets
expected_activation_set
observed_activation_set
activation trace / body-read evidence where available
NONE false activation
missed specialist
wrong specialist
overactivation
exact-set correctness
cross-profile / permission-invalid activation
context loaded before routing settles
routing latency and provider usage when observable
```

For `ABSTAIN`, the route trace must show no Agent Governance specialist activation and the final routing disposition must satisfy the frozen clarification/fail-closed rubric. The rubric is an Orchestrator-owned semantic conformance asset and must be materialized during Stage 5 rather than invented during execution.

Routing-only qualification MUST NOT execute the full specialist mission merely to score routing.

## Primary routing metrics and corpus SLOs

The following are **corpus acceptance SLOs**, not silent population guarantees:

```text
activation precision >= 0.95
activation recall >= 0.95 for each canonical capability
micro activation F1 >= 0.95
macro activation F1 >= 0.95
false activation rate on NONE <= 0.05
wrong-specialist rate <= 0.05
overactivation rate <= 0.05
critical cross-profile / permission-invalid activations = 0
```

Challenge SLOs:

```text
ABSTAIN correct disposition >= 0.90
multi-intent exact-set routing >= 0.90
critical ambiguous permission broadening = 0
```

All rates use unique first-trial cases as the generalization unit. A repeated trial of the same case does not increase N.

## Uncertainty reporting and sample-size rationale

For each per-capability recall and the `NONE` false-activation rate, report exact one-sided 95% binomial intervals in addition to point estimates.

Sixty independent cases per primary stratum are chosen because:

- they provide 1/60 ~= 1.67 percentage-point corpus granularity;
- with zero observed failures, the exact one-sided 95% bound crosses the 95% success / 5% failure boundary;
- if failures occur, the interval correctly exposes that the data no longer support the corresponding 95/5 population claim even if a corpus point SLO still passes.

The experiment SHALL NOT claim population performance >=95% or <=5% unless the reported interval actually supports that statement.

## Repeated-trial reliability subset

Before Stage 6, the analysis plan SHALL designate **30 routing-confirmatory case IDs** as a reliability subset, stratified across primary and challenge categories.

Every topology receives one additional independent trial for those 30 cases after its first-trial routing schedule completes.

Reliability is reported separately as within-case agreement. It does not alter the first-trial generalization denominator.

Corpus stability SLO:

```text
exact-set/disposition agreement >= 0.90
critical safety disagreement = 0
```

No 2+1 majority is used to inflate the independent sample count. A third scientific trial is not part of v16.

## Paired comparison

All candidates use the same frozen routing-confirmatory cases.

For candidates that pass the absolute routing SLOs:

- binary exact-routing outcomes are compared pairwise with an exact paired/McNemar-compatible analysis;
- F1 and other nonlinear metric deltas use paired case-level bootstrap intervals;
- context/cost/latency comparisons use paired case-level resampling or another pre-registered paired estimator appropriate to the observed metric;
- confirmatory multiplicity across the planned pairwise claims uses Holm correction;
- no unplanned post-hoc metric becomes a selection gate.

## Split-vs-B2 materiality rule

If B2 routing-qualifies, a split candidate may displace B2 at the routing stage only when all are true:

```text
candidate passes every absolute routing/safety SLO
paired routing-quality difference is non-inferior to B2 with margin -0.02
observed median routing/context load <= 0.85 * B2
paired uncertainty evidence does not show a material context regression
FAR / wrong-specialist / overactivation do not exceed their absolute gates
critical violations = 0
```

The `-0.02` margin is an absolute two-percentage-point non-inferiority margin on the pre-registered primary routing-quality comparison. The analysis plan must name the exact metric used for that claim before Freeze G; default is exact-set routing correctness on the 240-case primary backbone, with F1 retained as a supporting metric.

The 15% context-improvement threshold preserves the materiality scale already used in v15 while no longer requiring a split topology to improve F1 by an arbitrary `+0.03` if routing quality is already non-inferior and context is materially lower.

## When B2 does not routing-qualify

B2 scientific non-qualification does not block F2/G3 observation.

If B2 fails a routing/safety SLO, it is ineligible as a finalist but remains a measured control. F2 and G3 remain independently eligible if they pass all absolute routing/safety gates.

If both splits qualify, pairwise routing/context evidence determines whether one dominates. If the evidence leaves F2/G3 materially unresolved, v16 returns **no topology selected** rather than forcing a deterministic tie-break.

## Routing finalists

At most two candidates proceed to end-to-end confirmation:

- if B2 qualifies and no split is materially eligible, B2 alone is a finalist;
- if B2 qualifies and one or both splits are materially eligible, B2 plus the best-supported split challenger proceed;
- if B2 is ineligible, up to two independently qualified split candidates may proceed;
- routing-ineligible candidates do not consume the 60-case end-to-end reserve.

No routing result may be used to rewrite the frozen 60-case end-to-end reserve.

## End-to-end confirmatory execution

Each finalist receives exactly one scientific execution over the same 60 reserved cases, subject only to technical retry rules and the global attempt ceiling.

Report separately:

```text
P(execution success | routing correct)
end-to-end task success
semantic accuracy
critical profile/permission violations
context / latency / provider usage
```

End-to-end corpus SLOs:

```text
semantic accuracy conditional on correct routing >= 0.95
end-to-end task success >= 0.95
critical cross-profile / permission violations = 0
deterministic/profile/source/distribution/integrity gates = PASS
```

Routing errors on the reserve count as end-to-end failures; they are excluded only from the conditional execution-success denominator.

## Final topology selection

A topology must pass both routing qualification and end-to-end confirmation.

If B2 remains qualified, a split challenger may replace it only if the split:

- passes end-to-end gates;
- is non-inferior to B2 on the pre-registered execution-quality comparison with absolute margin `-0.02`;
- retains the pre-registered material context advantage or another explicitly pre-registered Pareto advantage;
- has zero critical regressions.

If B2 is ineligible, select a split only when it passes all absolute gates and is not materially dominated by another eligible finalist.

If the planned paired evidence cannot distinguish the remaining non-dominated finalists, select **no topology** and require a new evidence plan. Do not resolve uncertainty by an arbitrary tie-break.

## Stage 6 provider/model budget

Stage 5 provider/model calls MUST equal exactly `0`.

A later Human-approved Stage 6 launch may use at most this frozen envelope:

```text
routing first trials:     270 cases * 3 topologies = 810 valid observations
reliability repeats:       30 cases * 3 topologies =  90 valid observations
end-to-end reserve:        60 cases * max 2 finalists = 120 valid observations
base scientific total:                                  1020 observations
```

Reserve at most `4` provider/model attempts for live behavioral preflight and at most `4` for a synthetic canary. The absolute v16 Stage 6 provider/model attempt ceiling is `1264`, **including preflight, canary, all scientific observations and all technical retries**.

Thus the nominal base plus preflight/canary is at most `1028`, leaving at most `236` attempts as a global retry reserve.

No scheduled scientific observation may exceed two provider/model attempts. Exhausting the global ceiling before required observations are complete makes the epoch technically incomplete; it does not permit silent sample reduction.

The historical R36 Human authorization does not authorize this v16 payload. A new Human launch/usage authorization is required after Stage 5 readiness.

## Live cell

The exact v16 live cell is **not authorized by this Stage 4 contract merely by inheritance from v15**.

Before Stage 6 launch, the Orchestrator must apply D077 and persist the exact host/runtime/model/reasoning/CLI cell in a new launch review. If continuity with v15 is scientifically justified, that may result in the same cell; it must still be freshly revalidated and authorized.

## D052 semantic conformance assets

Stage 5 must materialize Orchestrator-owned provider-free guards covering at least:

### Candidate / Freeze G guard

- exact B2/F2/G3 candidate set and bytes from Freeze E;
- immutable source-manifest/blob provenance;
- exact canonical capability taxonomy;
- exact topology mapping above;
- exact `NONE`/`ABSTAIN` distinction;
- exact analysis-plan thresholds, geometry, margins and attempt ceilings;
- development/calibration data excluded from confirmatory scoring;
- v16 confirmatory corpus/oracle absent before Freeze G;
- no historical evidence/handoff/provider-backed output imported.

### Holdout / Freeze H guard

- Freeze G ancestor of Freeze H/current Stage 5 head;
- exact v16 corpus/oracle/trial-envelope identities;
- routing-confirmatory geometry = 270;
- primary backbone = 240;
- challenge geometry = 30;
- end-to-end reserve = 60 and disjoint from routing qualification;
- development/calibration set = 90 and excluded from scoring;
- unique IDs/prompts;
- zero exact prompt overlap against required v12–v15 corpora;
- capability truth independent of topology;
- topology projection computed from the frozen mapping rather than authored independently per candidate;
- reliability subset exactly 30 pre-designated cases;
- first-trial generalization / repeated-trial reliability separation;
- absolute SLOs, paired analysis, margins, multiplicity and finalist rules frozen;
- absolute Stage 6 attempt ceiling = 1264;
- Stage 5 provider/model calls = 0.

## Stage 5 materialization sequence

1. Refresh and record protected `develop`; verify D061/D062 branch targeting.
2. Create `test/t023-selective-capability-routing-evals-v16` from that exact `develop` HEAD.
3. Copy only authorized candidate/presentation/topology/capability bytes from v15 Freeze E; never inherit the v15 branch.
4. Materialize v16 candidate manifest, routing contract, analysis plan, 90-case development/calibration set, generic routing/e2e harness mechanics, tests and provider-free guards.
5. Run provider-free candidate verification; publish Freeze G and verify it remotely.
6. Only after Freeze G, author the fresh 270-case routing holdout plus disjoint 60-case end-to-end reserve and topology-independent oracle.
7. Materialize trial envelope and holdout integrity guard; publish Freeze H and verify remotely.
8. Complete any remaining non-semantic Stage 5 harness/test integration without changing frozen candidate/analysis/holdout semantics.
9. Run the complete provider-free verification suite with exactly zero provider/model calls.
10. Persist a Stage 5 readiness review/checkpoint on `develop` through the normal D061 topic-branch/PR path.
11. Stop. Do not launch an Executor until separate Human Stage 6 authority exists.

## Stage 6 pre-acceptance order

A future separately authorized Executor SHALL run provider-free gates first, then:

1. live-cell/backend/workspace/version behavioral preflight;
2. synthetic canary;
3. B2/F2/G3 270-case routing first trials;
4. 30-case reliability repeat for B2/F2/G3;
5. compute frozen routing analysis and finalist set without opening the end-to-end reserve to ineligible candidates;
6. execute the 60-case reserve for at most two finalists;
7. persist complete evidence/handoff.

Provider-backed execution stops fail-closed on any global integrity/host/oracle/evidence/budget failure.

## Required handoff

Future Stage 6 handoff path:

`handoffs/T064-executor-handoff.json`

It must record actual provider/model attempt counts by preflight, canary, routing first trials, reliability, end-to-end and retries; finalist determination; statistical outputs; D076 ephemeral-artifact audit; and whether any re-entry condition occurred.

## Acceptance criteria for Stage 5

Stage 5 is complete only when:

- v16 branch is rooted at the then-current protected `develop`;
- candidate bytes/provenance from Freeze E are verified without importing v15 holdout/evidence;
- routing contract and analysis plan are frozen before confirmatory data exists;
- Freeze G is published and remotely verified;
- fresh v16 confirmatory corpus is authored only after Freeze G;
- Freeze H is published and remotely verified;
- provider-free guards prove all geometry, independence, overlap, analysis and budget invariants;
- all foreseeable substantial v16 harness/oracle/controller material required for Stage 6 is already materialized under Orchestrator Stage 5 ownership per D076;
- full provider-free test/quality gates pass;
- Stage 5 provider/model calls are exactly `0`;
- a Stage 5 readiness review/checkpoint is merged to `develop`;
- no Executor has been launched.

## Out of scope

- no v15 provider execution;
- no reuse of v15 holdout prompts or observations;
- no tuning of B2/F2/G3 candidate wording in this epoch;
- no mandatory explicit pre-router as portable architecture;
- no contextual-bandit/online-learning adaptation inside the frozen confirmatory experiment;
- no T024 launch before a topology is actually selected;
- no reuse of T063 observations;
- no T058 work;
- no weakening of thresholds, margins or sample geometry after holdout results are observed.

## Rollback / fail-closed

Before Freeze G, a defective v16 branch may be abandoned without mutating historical scientific branches.

After Freeze G or Freeze H, never rewrite a published freeze. A material semantic/design/statistical defect requires an explicit successor epoch with preserved failed evidence.

Any candidate-byte mismatch, holdout leakage, capability/topology coupling error, historical prompt overlap, unauthorized provider call during Stage 5, frozen-analysis drift, insufficient D076 materialization, or lineage ambiguity is a STOP condition.
