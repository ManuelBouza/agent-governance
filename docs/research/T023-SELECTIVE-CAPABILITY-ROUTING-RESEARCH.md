# T023 Selective Capability Routing Research

Status: SYNTHESIZED  
Date: 2026-09-12  
Authority: Human-supplied Advanced Research / ChatGPT Orchestrator synthesis  
Scope: T023 routing, activation-unit topology, and evaluation methodology

## Research question

Determine whether T023/T062 should continue discovering a routing/evaluation mechanism primarily through an end-to-end B2/F2/G3 live experiment, or whether established work on selective classification, tool/function routing, model routing, open-set recognition, calibration, and conditional computation provides a better experimental abstraction.

## Executive conclusion

The strongest supported disposition is **HYBRID / REDESIGN**.

T023 still requires product-specific empirical evidence because the native host/model decides whether and which Agent Governance Skill activation unit is loaded, and that behavior cannot be inferred from an external benchmark. However, the current v15 experiment combines three separable questions:

1. routing correctness;
2. specialist execution correctness;
3. end-to-end task correctness.

Established research and documented production patterns support evaluating these layers separately before spending a large end-to-end provider budget.

The recommended abstraction is:

```text
request
  -> canonical capability truth
  -> selective routing decision
       NONE / DIRECT
       one specialist
       multiple specialists
       ABSTAIN / ASK
  -> activation-unit mapping for the candidate topology
  -> specialist execution
  -> independent routing and execution scoring
```

This is compatible with D050 portability when the router is the host-native Skill selection mechanism treated as a black-box classifier. An explicit pre-router is optional adapter behavior, not a new portable product dependency.

## External mechanism families

The advanced research found the following mature analogues.

### Sparse mixture-of-experts and conditional computation

Sparse MoE work formalizes an early gate that selects only a subset of experts. The transferable principle is not to train an MoE for Agent Governance, but to make selection happen before paying the context/execution cost of an unnecessary specialist.

Primary references include Shazeer et al., *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer* (2017), Switch Transformers (Fedus, Zoph, Shazeer), and Expert Choice routing.

### Model routing and cascades

RouteLLM, RouterBench, FrugalGPT and related systems separate selection policy from downstream model execution and explicitly optimize quality/cost trade-offs. The transferable principle is to qualify the router before paying for full specialist execution and to compare routing policies over common cases.

### Tool/function relevance

Tool-use evaluation is the closest operational analogue. Berkeley Function Calling Leaderboard explicitly contains cases where no function is relevant and the correct behavior is to make no function call. This maps directly to Agent Governance false activation and supports making `NONE` a first-class expected outcome.

### Open-set and out-of-scope classification

CLINC150 and open-set recognition literature demonstrate that forcing every input into a known intent is an artificial closed-world assumption. Agent Governance requires an explicit outcome for requests to which no Governance specialist applies.

### Multi-label classification

T023 multi-intent cases are naturally set-valued. The expected truth should be zero, one, or multiple canonical capabilities rather than a single topology-specific class.

### Selective prediction and calibration

Selective classification provides a separate reject/abstain outcome when confidence is insufficient. This must remain distinct from `NONE`:

```text
NONE
  = confidently outside Agent Governance specialist scope

ABSTAIN / ASK
  = insufficient evidence to select safely
```

A numeric confidence emitted by an LLM is not automatically calibrated. Any threshold-bearing confidence must be validated empirically.

## Statistical findings

### Trials are not independent tasks

Repeated executions of one prompt characterize within-case stochastic reliability. They do not multiply the number of independent examples for generalization.

The current v15 schedule therefore represents 70 unique cases with repeated trials, not 420-630 independent scientific samples.

Future evaluation must report separately:

```text
across-case generalization
within-case repeated-trial reliability
```

and cluster statistical analysis by case identity where repeated trials remain.

### Point gates versus population claims

The existing `>= 0.95` and `<= 0.05` thresholds are valid as pre-registered product SLOs on a frozen corpus. They are not, at current denominators, sufficient by themselves to claim with 95% confidence that the corresponding population rates satisfy those bounds.

The advanced research used exact-binomial sanity checks to show the scale mismatch: even zero failures in 40 independent negatives cannot establish an upper 95% one-sided population error bound below 5%. Future design must state explicitly whether a criterion is:

- a corpus acceptance SLO; or
- an inferential population claim.

### Paired comparison

B2/F2/G3 observe common cases, so comparisons are naturally paired. Future confirmatory analysis should pre-register a primary routing endpoint and use paired methods appropriate to the metric, such as exact McNemar for binary discordance and paired/clustered bootstrap intervals for differences in F1, cost, context, or latency.

Where the product question is whether a split topology reduces context without materially degrading quality, non-inferiority/superiority margins are a better formalism than absence of a significant difference.

## Implications for T023

The research does **not** conclude that B2/F2/G3 are meaningless. They remain useful activation-unit packaging hypotheses:

- B2 represents a single-router family;
- F2 partitions two peer activation units;
- G3 partitions three specialized activation units.

What changes is the order of evaluation.

Instead of:

```text
full topology execution
  -> routing + specialist execution + semantic outcome
  -> aggregate qualification
```

use:

```text
canonical capability oracle
  -> topology-specific expected activation set
  -> routing-only qualification
  -> packaging/context economics
  -> end-to-end execution of finalists
  -> topology decision
```

## Prospective v16 requirements

A redesigned epoch should include at least:

1. a topology-independent canonical capability oracle;
2. explicit empty-set / `NONE` truth;
3. explicit `ABSTAIN / ASK` semantics for genuinely ambiguous cases where safe routing cannot be determined;
4. zero/one/multiple expected capability labels;
5. a deterministic mapping from canonical capability set to each candidate topology's expected activation units;
6. router-only evidence before specialist execution;
7. separate routing and execution metrics;
8. repeated-trial analysis that does not treat repetitions as independent cases;
9. pre-registered paired comparisons and uncertainty intervals;
10. a fresh calibration/development boundary distinct from a fresh confirmatory holdout;
11. end-to-end execution only for routing-qualified finalist topology/policies;
12. quality/risk/context/cost/latency reported as distinct dimensions unless a Human-approved utility function is introduced.

## What should be retained from v15

The following controls remain valuable and should carry forward conceptually:

- candidate-before-holdout freeze discipline;
- fresh holdout and overlap guards;
- provenance hashes;
- positives, negatives, near-miss, ambiguity, cross-profile and multi-intent strata;
- independent B2/F2/G3 observation, with no candidate suppressing another;
- false activation, wrong-specialist and overactivation metrics;
- zero-tolerance critical safety/profile violations as observed gates;
- fixed live-cell control where host-native routing is being compared;
- Git-persisted evidence and reproducibility boundaries.

## What should not carry forward unchanged

Do not treat repeated trials as independent sample size.

Do not require all three topology candidates to complete full specialist execution before establishing whether their routing is viable.

Do not use a single aggregate qualification result as a substitute for separate routing, execution, and architecture/materiality conclusions.

Do not interpret `NONE` and uncertainty as the same state.

Do not treat raw model confidence as calibrated probability.

## Evidence classification

The research distinguished evidence classes:

- scientifically validated mechanism: sparse gating, open-set classification, selective prediction, calibration, paired classifier comparison;
- academic/open benchmark: RouteLLM, RouterBench, BFCL, CLINC150;
- documented provider practice: OpenAI manager/handoff/tool-choice patterns; Anthropic routing and agent-eval guidance;
- framework pattern: LangGraph Router/Supervisor, AutoGen Selector/Swarm, Semantic Kernel orchestration, Google ADK composition.

Framework availability is not evidence that a topology is scientifically optimal for Agent Governance.

## Decision recommendation

```text
T023 v15 provider-backed Stage 6:
  do not consume

v15 scientific material:
  preserve as an unconsumed historical epoch/reference

next experiment:
  redesign as v16 around selective capability routing,
  topology-independent truth, NONE/ABSTAIN,
  routing-first qualification, paired inference,
  and finalist-only end-to-end confirmation
```

This recommendation is specifically attractive because v15 remains at zero provider/model attempts and zero live scientific observations, so redesign does not discard consumed experimental evidence.
