# Orchestrator Checkpoint

Checkpoint-ID: O282  
Date: 2026-09-12  
Current-Objective: T023 v16 — selective capability routing redesign  
State: T023_V15_FROZEN_UNCONSUMED_V16_DESIGN_REENTRY  
Active-Executor: none  
Executor-Launch-State: NOT_AUTHORIZED  
Prior-Task: `T062 / T023 v15 RIQ-NBC` — frozen unconsumed  
Prior-Scientific-Branch: `test/t023-skill-activation-topology-evals-v15`  
Prior-Scientific-HEAD: `5a2a3effeabede6640d10a8aa80ae6f70008764c`  
Prior-Stage5-Candidate: `3e0d0b71cf382db502e186622f40a23bcd915390`  
Prior-Freeze-E: `5b025087bc7b6996f683a34fdd1ce441d3d6dd82`  
Prior-Freeze-F: `5b8ac55980ecdbb6a2bf3784812b933647f2f13d`  
Provider-Model-Calls-Consumed-v15: `0`  
Scientific-Observations-v15: `0`  
Current-Decision: `docs/decisions/D078-selective-capability-routing-evaluation-boundary.md`  
Current-Convergence-Review: `docs/reviews/T023-R37.md`  
Current-Research: `docs/research/T023-SELECTIVE-CAPABILITY-ROUTING-RESEARCH.md`  
Chat-Closure: KEEP_CURRENT_CHAT

## Canonical transition

T062 / T023 v15 reached launch-ready state under O281/R36 but had not consumed any provider/model calls or produced any live scientific observation.

Before the Human started that execution, advanced research identified a material evaluation-design improvement: routing correctness should be isolated from specialist execution and end-to-end correctness, using topology-independent capability truth, first-class `NONE`, separate `ABSTAIN / ASK`, multi-label semantics, repeated-measure-aware statistics, and paired comparison.

The Human approved methodology re-entry.

D078 is now accepted prospectively and R37 supersedes R36 for execution purposes. The v15 scientific branch and freezes remain preserved as an unconsumed historical epoch. They are not scientific results and must not be modified to retrofit the new design.

## v15 frozen state

Do not launch or continue Codex for T062 v15.

Do not run:

- backend/workspace/model preflight;
- synthetic canary;
- B2/F2/G3 acceptance schedule;
- any provider-backed v15 scientific execution.

Do not reuse the v15 holdout as the v16 confirmatory holdout.

R36's provider authorization is not transferable to v16.

T063 remains closed/frozen `NOT QUALIFIED`. T058 remains frozen.

## v16 controlling methodology

The next epoch must follow D078.

Minimum design invariants:

```text
canonical capability truth independent of topology
zero / one / multiple capabilities
NONE / DIRECT distinct from ABSTAIN / ASK
topology-specific activation mapping
routing-only qualification before full specialist execution
separate routing and execution estimands
repeated trials != independent cases
paired common-case comparison
uncertainty-aware gates
fresh calibration/development boundary
fresh confirmatory holdout
finalist-only end-to-end confirmation
```

An explicit pre-router is not assumed to be portable architecture. Host-native Skill routing may remain the portable baseline and be evaluated as a black box.

## Next Chat Minimum Load

After normal bootstrap (`develop`, `AGENTS.md`, this checkpoint):

1. load `docs/decisions/D078-selective-capability-routing-evaluation-boundary.md`;
2. load `docs/reviews/T023-R37.md`;
3. load `docs/research/T023-SELECTIVE-CAPABILITY-ROUTING-RESEARCH.md` only to the extent needed for design rationale;
4. load D050 and D074 because v16 refines their T023 activation/topology semantics;
5. load the v15 Task Contract only for retained controls/provenance patterns, not as v16 authority;
6. do not reconstruct the frontier from prior chats or Project Memory;
7. do not launch an Executor or provider/model experiment until a new v16 Task Contract and launch authority exist.

## Next Action

ChatGPT Orchestrator shall perform T023 v16 Explore/Specify/Design/Plan under D053/D068.

First define the canonical capability taxonomy and routing truth contract independent of B2/F2/G3 packaging. Then define `NONE` versus `ABSTAIN / ASK`, multi-label semantics, topology mapping, routing-only evidence, statistical estimands/sample-size rationale, fresh calibration/confirmatory boundaries, and finalist-only end-to-end confirmation.

Only after that design is coherent should the Orchestrator decide the v16 candidate set, assign a new Task Contract/task ID, materialize any required Stage 5 candidate/eval assets, and later prepare separate Human-mediated Stage 6 launch authority.
