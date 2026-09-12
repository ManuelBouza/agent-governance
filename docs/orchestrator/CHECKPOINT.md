# Orchestrator Checkpoint

Checkpoint-ID: O283  
Date: 2026-09-12  
Current-Objective: T064 / T023 v16 — selective capability routing evaluation  
State: T023_V16_DESIGN_COMPLETE_T064_READY_FOR_STAGE5  
Active-Executor: none  
Executor-Launch-State: NOT_AUTHORIZED  
Task-Contract: `docs/tasks/T064-t023-selective-capability-routing-v16.md`  
Current-Design-Review: `docs/reviews/T023-R38.md`  
Current-Decision: `docs/decisions/D078-selective-capability-routing-evaluation-boundary.md`  
Current-Research: `docs/research/T023-SELECTIVE-CAPABILITY-ROUTING-RESEARCH.md`  
Prospective-Scientific-Branch: `test/t023-selective-capability-routing-evals-v16`  
Prior-Task: `T062 / T023 v15 RIQ-NBC` — frozen unconsumed  
Prior-Scientific-Branch: `test/t023-skill-activation-topology-evals-v15`  
Prior-Scientific-HEAD: `5a2a3effeabede6640d10a8aa80ae6f70008764c`  
Prior-Freeze-E: `5b025087bc7b6996f683a34fdd1ce441d3d6dd82` — authorized candidate-byte source only  
Prior-Freeze-F: `5b8ac55980ecdbb6a2bf3784812b933647f2f13d` — historical holdout only; forbidden v16 confirmatory source  
Provider-Model-Calls-Consumed-v16: `0`  
Scientific-Observations-v16: `0`  
Chat-Closure: KEEP_CURRENT_CHAT

## Canonical transition

O282 required T023 v16 Explore/Specify/Design/Plan re-entry before any new scientific materialization.

That design is now complete in T064 and T023-R38.

The v16 semantic truth is topology-independent and uses exactly:

```text
consumer-lifecycle
source-maintainer
external-skill-trust
```

with first-class dispositions:

```text
ROUTE
NONE
ABSTAIN
```

Multi-intent truth is set-valued.

B2/F2/G3 remain the candidate packaging hypotheses without wording tuning. Their accepted `MG1-T023-TOPOLOGIES-v4` mapping is retained, but routing truth no longer depends on that packaging.

## v16 experiment boundary

T064 pre-registers:

```text
development/calibration:       90 non-confirmatory cases
routing-confirmatory:         270 unique cases
  primary backbone:           240
  challenge cases:             30
reliability subset:             30 cases, one additional trial
disjoint end-to-end reserve:    60 cases
routing candidates:              3 (B2/F2/G3)
max end-to-end finalists:         2
```

Primary `0.95 / 0.05` thresholds are corpus SLOs. Exact one-sided 95% intervals are reported separately; repeated trials are measures of within-case reliability and do not increase independent N.

Candidate comparisons are paired. The design pre-registers non-inferiority/materiality handling and removes the v15 forced tie-break: unresolved finalists produce no topology selection.

## Freeze plan

T064 Stage 5 must create a fresh scientific branch from the then-current protected `develop`.

The only authorized source for retained candidate/presentation bytes is pre-holdout v15 Freeze E:

`5b025087bc7b6996f683a34fdd1ce441d3d6dd82`

The v15 branch itself must not be inherited.

The new boundaries are:

```text
Freeze G
  candidate bytes/provenance
  capability-routing contract
  topology mapping
  complete analysis-plan pre-registration
  development/calibration boundary

Freeze H
  fresh routing-confirmatory holdout
  disjoint end-to-end reserve
  topology-independent oracle
  trial envelope
```

The v16 confirmatory holdout must not exist before remote Freeze G verification and must have zero exact prompt overlap against required v12–v15 corpora.

## Provider and Executor boundary

Stage 5 provider/model calls must remain exactly `0`.

No Executor is authorized.

The prospective Stage 6 design ceiling is `1264` provider/model attempts including preflight, canary, scientific execution and technical retries, but this is not launch authority. The historical R36 Human provider approval does not transfer to v16.

A future Stage 6 launch requires:

- completed and remotely verified Stage 5 materialization;
- a Stage 5 readiness review integrated on `develop`;
- D077 revalidation of the then-current live cell/runtime surface;
- fresh Human authorization for the exact v16 provider destination/payload/usage envelope;
- D055/D071 Human-mediated Executor transport.

D076 applies prospectively: all foreseeable substantial routing/evaluation harness, oracle, analysis and finalist-gating mechanics must be materialized during Orchestrator Stage 5.

## Frozen adjacent work

T062/v15 remains frozen unconsumed: no preflight, canary or acceptance execution.

T063 remains closed/frozen `NOT QUALIFIED`; do not reuse its observations.

T058 remains frozen and must not be resumed, integrated, cleaned, copied or consumed without new explicit Human authorization.

T024 remains blocked until T023 actually selects a topology.

## Next Chat Minimum Load

After normal bootstrap (`develop`, `AGENTS.md`, this checkpoint):

1. load `docs/tasks/T064-t023-selective-capability-routing-v16.md`;
2. load `docs/reviews/T023-R38.md`;
3. load D078;
4. load D050 only when candidate/capability/topology semantics need revalidation;
5. use v15 Freeze E and its candidate manifest only as the explicit candidate-byte provenance source;
6. load historical v12–v15 corpora only as needed to implement the zero-overlap guard;
7. do not load or reuse v15 provider/evidence observations because none exist and the epoch is frozen;
8. do not launch an Executor or provider/model call during Stage 5.

## Next Action

ChatGPT Orchestrator shall execute T064 Stage 5 candidate/eval materialization under D068.

Required order:

1. refresh protected `develop` and verify D061/D062 branch targeting;
2. create `test/t023-selective-capability-routing-evals-v16` from that exact `develop` HEAD;
3. copy only the authorized exact candidate/presentation/topology/capability material from v15 Freeze E;
4. materialize the v16 candidate manifest, capability-routing contract, frozen analysis plan, 90-case development/calibration set, complete routing/e2e harness mechanics, tests and provider-free candidate guard;
5. publish and remotely verify Freeze G;
6. only then author the fresh 270-case routing holdout plus disjoint 60-case end-to-end reserve, oracle, trial envelope and holdout guard;
7. publish and remotely verify Freeze H;
8. complete provider-free Stage 5 verification with exactly zero provider/model calls;
9. persist Stage 5 readiness evidence/review/checkpoint on `develop`;
10. stop before any Executor launch.
