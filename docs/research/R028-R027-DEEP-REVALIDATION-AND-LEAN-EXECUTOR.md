# R028 — R027 deep revalidation and Lean Executor architecture

Research-ID: R028  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-12  
Last-Reviewed: 2026-09-12  
Owner: ChatGPT Orchestrator  
Repository-Baseline: `develop@cd5dbafd25a6fd531f6852426b5417d7f42cfa46`  
Scope: deeply revalidate R027 and the prospective T066 evaluation, actively search for alternatives, and optimize the ChatGPT + Codex architecture without adopting policy before empirical qualification  
Question: Is R027's proposed responsibility split actually optimal once current model economics, instruction loading, subagent overhead, progressive verification and causal experimental design are considered, and how should T066 be changed before any scored execution?  
Evaluation-Refs: T066; D079; R027; R007; R010; R012; R017; R018; D053; D054; D055; D057; D060; D063; D065; D068; D075; D076; D077  
Decision-Ref: `docs/decisions/D079-lean-executor-qualification-and-adoption-boundary.md`  
Supersedes: none  
Superseded-By: none

## Executive conclusion

R027 identified the right **authority boundary**, but its economic thesis needs a more precise optimization target and a stronger evaluation architecture.

The best current candidate is not either extreme:

```text
D068 universal frozen materialization
  ChatGPT specifies + materializes
  Codex mostly verifies

or

Codex full autonomy
  Codex specifies + materializes + judges itself
```

The stronger candidate is **R027+ / Lean Executor**:

```text
ChatGPT Orchestrator
  intent / external research / requirements
  Specification / Design / Plan / acceptance
  normative governance / semantic oracles
  final semantic acceptance

Codex Executor
  repository-local exploration
  technical materialization
  implementation-coupled tests/config/tooling
  execution / diagnosis / bounded repair
  technical verification

Deterministic tooling / CI
  mechanically enforceable checks
  progressive feedback and final repository gates
```

Inside Codex, the economic strategy is:

```text
minimum useful context
+ minimum qualified model/effort
+ STANDARD speed by default
+ progressive verification
+ escalation after evidence, not pre-emptively
+ subagents only when total-system ROI is positive
```

This architecture should be evaluated, not adopted from research alone.

## What R028 changes relative to R027

R028 **retains** R027's principal responsibility split but changes five important points.

First, raw Codex tokens are not the sole objective. Moving implementation from ChatGPT to Codex can mechanically increase Codex work even when it is the better operating architecture. The primary economic measure should be **Codex economic cost per accepted work unit**, with raw token classes reported separately. ChatGPT technical-materialization burden is a distinct operational benefit and must not be falsely monetized without comparable telemetry.

Second, the current T066 design is best treated as a **screening experiment**, not sufficient evidence of global optimality. Three pairs per phase can falsify a poor candidate cheaply and detect large effects, but cannot provide a precise general non-inferiority or savings claim.

Third, root context architecture is a first-order variable. Agent Governance's current root `AGENTS.md` was measured by R027 at 34,567 bytes, while current Codex documentation states that combined project instructions stop at `project_doc_max_bytes`, 32 KiB by default. T066 must therefore prove complete instruction loading before any scored arm. A future thin-root/progressive-disclosure policy should be evaluated separately rather than silently bundled into the ownership comparison.

Fourth, subagents are not an automatic savings mechanism. OpenAI explicitly states that comparable subagent workflows consume more tokens because every child performs its own model/tool work. Cheap specialized children can still be economically useful when they displace expensive root exploration or isolate noisy context, but that is a separate ROI hypothesis and should not be mixed into T066 ownership/model screening.

Fifth, T066 should lead to a separate confirmatory evaluation only if screening produces sufficient signal. Confirmation should use a fresh independent corpus, blocked randomization and a sample size frozen from a prospective power calculation rather than reusing the small screening sample as proof.

## Current official evidence revalidated on 2026-09-12

### Model family and economics

Current official OpenAI model documentation describes:

- GPT-5.6 Sol as a flagship model for complex professional work;
- GPT-5.6 Terra as balancing intelligence and cost;
- GPT-5.6 Luna as optimized for cost-sensitive, high-volume workloads;
- GPT-6 Astra as the current most capable model for the hardest end-to-end work.

Current token pricing shown by official model pages is:

| Model | Input USD / 1M | Cached USD / 1M | Output USD / 1M |
| --- | ---: | ---: | ---: |
| GPT-5.6 Sol | 4.00 | 0.40 | 20.00 |
| GPT-5.6 Terra | 2.00 | 0.20 | 12.00 |
| GPT-5.6 Luna | 0.20 | 0.02 | 1.20 |

The current ChatGPT credit rate card additionally shows a **promotional Sol rate** for eligible purchased-credit usage, available at least through **2026-11-21**:

| Model | Input credits / 1M | Cached credits / 1M | Output credits / 1M |
| --- | ---: | ---: | ---: |
| GPT-5.6 Sol | 100 | 10 | 500 |
| GPT-5.6 Terra | 50 | 5 | 300 |
| GPT-5.6 Luna | 5 | 0.5 | 30 |

This corrects the older R027 same-token comparison that used Sol `125 / 12.5 / 750`. The exact economic advantage is workload-mix dependent: Terra is currently 50% of Sol's input/cache credit rate and 60% of Sol's output credit rate, not a uniform 40% of Sol under the promotional table.

Because this fact is explicitly time-sensitive, **no T066 gate may rely on these numbers without D077 revalidation immediately before scored launch**. If the applicable account is not on the cited token-based credit schedule, the experiment must use the actually applicable measurable rate card or block economic attribution.

Official sources reviewed:

- https://developers.openai.com/api/docs/models
- https://developers.openai.com/api/docs/models/gpt-5.6-sol
- https://developers.openai.com/api/docs/models/gpt-5.6-terra
- https://developers.openai.com/api/docs/models/gpt-5.6-luna
- https://help.openai.com/en/articles/11481834-cha

### Instruction loading

Current Codex documentation states that project instructions are concatenated from repository root toward the working directory and stop when the combined size reaches `project_doc_max_bytes`, **32 KiB by default**. It also recommends concise review rules and reserving formatting/lint checks for CI.

OpenAI's Harness Engineering report independently describes a large monolithic `AGENTS.md` as a failed pattern and reports using a short root file, roughly 100 lines, as a map into structured repository documentation with progressive disclosure and mechanical validation.

R028 does **not** convert “100 lines” into an Agent Governance rule. The durable hypothesis is smaller: a root file should contain only stable, high-value, non-inferable invariants and routing pointers; detailed policy belongs in canonical docs and mechanically checkable rules belong in tooling/CI where practical.

Official sources reviewed:

- https://developers.openai.com/codex/guides/agents-md
- https://openai.com/index/harness-engineering/

### Speed

Current OpenAI speed documentation states that GPT-5.6 Fast mode increases model speed by about **1.5x** while consuming ChatGPT credits at **2.5x the Standard rate**. Therefore Standard remains the correct economic experimental constant and the strongest default candidate for non-latency-critical work.

Fast should remain a separate SLA/latency hypothesis, not a T066 variable.

Official source reviewed:

- https://developers.openai.com/codex/speed

### Subagents

Current OpenAI subagent documentation states that comparable subagent workflows consume more tokens than single-agent runs because each child performs its own model/tool work. The same guidance recommends parallelism primarily for independent/read-heavy exploration, tests, triage and summarization, and greater caution for parallel write-heavy workflows.

This supports a future ROI-gated specialist hypothesis, not default multiagent execution.

Official source reviewed:

- https://developers.openai.com/codex/subagents

## External empirical evidence

R028 retains the external evidence from R027 but narrows how it is used.

- Lulla et al., arXiv:2601.20404, report lower median runtime and output-token use in their studied coding-agent tasks when useful repository instruction files are present.
- Gloaguen et al., arXiv:2602.11988, find that repository context files do not generally improve task success and can increase inference cost substantially, especially when they contain unnecessary generated context.
- Terminus-4B reports that a small specialized execution subagent can reduce main-agent token usage on its evaluated workloads.
- FastContext, arXiv:2606.14066, reports benefits from separating repository exploration into a specialized context-isolated component in evaluated configurations.

These results do not prove that Agent Governance should add children. They support the principle that **useful context can save work while unnecessary context creates work**, and that specialized children should be judged on total-system economics rather than root-token reduction alone.

## Optimization objective

For T066 and successors, separate four dimensions rather than compressing them into one misleading number:

```text
Quality
  accepted outcome
  first-pass acceptance
  semantic drift
  escaped defect / protocol violation

Codex economics
  uncached input tokens
  cached input tokens
  output/reasoning tokens
  total credits
  retries / repair turns / escalations

Latency
  end-to-end wall time
  verification/tool time where measurable

Orchestrator operating load
  whether ChatGPT must materialize repository implementation
  technical mutation actions/bytes attributable to the Orchestrator where deterministically measurable
  semantic re-entry count
```

The primary economic endpoint is:

```text
ECAW = total Codex credits attributable to the complete arm
       ----------------------------------------------------
       accepted work units
```

`total Codex credits` includes root, any authorized child, retries and escalations. T066 itself keeps children disabled, but the metric definition must remain total-system safe for later experiments.

A lower ECAW does not by itself justify adoption if quality degrades. Conversely, a higher Codex token count does not automatically reject a cheaper-model architecture when credits fall and quality is preserved.

## Recommended responsibility modes to evaluate

R028 retains R027's two-mode concept:

```text
EXECUTOR_MATERIALIZED
  candidate normal source-maintenance mode
  ChatGPT freezes semantic authority through Spec/Design/Plan/acceptance
  Executor owns repo-local exploration + technical materialization + verification

ORCHESTRATOR_FROZEN_CANDIDATE
  special control/scientific mode
  pre-execution candidate bytes are part of the controlled experiment,
  exact-byte evidence boundary, semantic fixture/oracle, or another explicit reason
```

The research does not adopt either mode normatively. Current D068 remains controlling until a later accepted Decision says otherwise.

## Recommended compute-routing hypothesis

The future routing policy should be **class-based and evidence-gated**, not “Terra always” or “Sol always”:

| Class | Initial profile candidate | Intended work |
| --- | --- | --- |
| N0 | Luna / Low or Medium / Standard | narrow read/search/classify/summarize or highly mechanical qualified work |
| N1 | Terra / Medium / Standard | bounded implementation with complete Spec/Design/Plan and deterministic feedback |
| N2 | Sol / Medium / Standard | ambiguous, cross-cutting or diagnostically difficult work |
| N3 | Sol / High, or separately qualified premium profile | high-risk or failed N2 work |

GPT-6 Astra is **not** inserted into T066. R010 already treats global Astra adoption as deferred; current availability and flagship positioning do not by themselves justify adding a new experimental variable. A later high-risk/premium routing decision can re-evaluate it under D055/D077.

A bounded N1 attempt should normally permit at most one repair loop before explicit reassessment/escalation. Repeated cheap-model retries can erase the price advantage and increase latency.

## Progressive verification hypothesis

For ordinary technical work, a common verification ladder should be evaluated or used as a frozen constant where it does not change semantics:

```text
L0 deterministic preflight / syntax / static checks
L1 exact reproduction or focal acceptance check
L2 affected-module tests + focal lint/type checks
L3 impacted-dependency/area tests when blast radius justifies them
L4 mandatory full repository/merge gate once before acceptance
```

The optimization is to avoid running the broadest suite after every intermediate repair. Required final gates remain mandatory.

For T066, the verification envelope should be identical within each pair so ownership/model effects remain identifiable.

## T066 redesign conclusion

T066 should remain bounded at a maximum of 18 scored arms and be explicitly labeled **screening**.

It should answer:

1. Does Executor materialization preserve quality under equal Sol/Medium/Standard compute?
2. Under Executor materialization, does Terra/Medium/Standard produce a strong enough economic signal versus Sol/Medium/Standard to justify further study?
3. On fresh work, does the integrated Lean Executor candidate dominate the current bundle, or does it expose a measurable cost-versus-Orchestrator-load tradeoff?

T066 must **not** claim global optimality, non-inferiority at small margins, or project-wide percentage savings from three pairs.

### Screening design improvements

Before Freeze A, T066 should additionally freeze:

- Codex/client/runtime version and applicable usage-accounting surface;
- model identity/alias resolution where observable;
- rate-card snapshot and deterministic credit derivation;
- instruction-loading proof and exact experiment instruction envelope;
- a common progressive verification contract;
- blocked/counterbalanced arm order by archetype with a frozen deterministic seed;
- no reuse of observed arm outputs to redesign later scored fixtures;
- explicit `screening_only: true` metadata in results/review.

The current 3-pair gates remain useful as fail-fast screening thresholds. They become evidence for whether to proceed, not proof of a final policy.

## Confirmatory successor design

Only after a positive or materially promising T066 screening result should Agent Governance define a separate confirmatory Task Contract.

The confirmatory study should use a **new independent corpus** and must not reuse T066 scored outcomes as confirmatory observations.

Candidate design:

```text
primary economic estimand
  paired log ratio of ECAW(candidate) / ECAW(control)

minimum interesting economic improvement
  20% unless Human/Decision authority freezes another threshold before execution

alpha
  0.05 two-sided for the primary economic comparison

power target
  >= 0.80

sample size
  prospectively calculated from a frozen variance assumption/estimate
  practical planning range: about 20-48 matched pairs

randomization
  blocked by archetype / difficulty / blast-radius class
  counterbalanced arm order

analysis
  geometric paired ratio
  paired bootstrap 95% CI
  paired permutation/Wilcoxon robustness analysis
  exact/McNemar-style paired analysis for binary quality outcomes where applicable
```

The 20-48 range is a planning bound, not a guaranteed sample size. For example, under a paired log-ratio standard deviation around 0.35 and a 20% effect target, a normal approximation is around 20 pairs; detecting a 15% effect with variance around 0.40 requires materially more, around the high-40s. The final confirmatory N must be frozen before confirmatory scored execution.

A mature policy gate should require both economic evidence and quality non-inferiority; T066 screening alone is insufficient to set a few-percentage-point non-inferiority margin reliably.

## Separate mechanism evaluations after screening

Do not confound T066 by adding all optimizations at once. Evaluate these independently before any integrated normative package:

1. **Thin root context / progressive disclosure** — compare current full instruction architecture with a compact routing-map root while holding task/model constant; require no instruction misses or safety/governance regressions.
2. **Luna N0 routing** — only narrow, repetitive/read-heavy/mechanical classes; compare total ECAW including retries.
3. **Subagent ROI** — only eligible independent/read-heavy tasks; count root + every child + coordination + retry cost; reject if total economics do not improve.
4. **Verification ladder** — compare progressive versus repeated broad verification on equivalent work; require no escaped defects.
5. **Fast mode** — only if a real latency SLA provides an explicit value function; Standard otherwise remains the economic baseline.
6. **Markdown ownership** — evaluate separately because governance authority risk is different from code-execution economics.

Only after mechanism-level evidence exists should an integrated R027+ bundle be compared against the current normative bundle.

## Recommended decision sequence

```text
R028 research complete
  -> revise T066 before any Freeze A/scored run
  -> T066 screening
  -> if poor signal: stop; no normative change
  -> if promising signal: independent mechanism evals as needed
  -> confirmatory ownership/compute evaluation on fresh corpus
  -> integrated bundle evaluation
  -> only then consider D068/D055/D065/Markdown/AGENTS changes through explicit Decisions
```

## Volatile facts requiring D077 revalidation

The following are time-sensitive and must be refreshed before consequential execution or adoption:

- current Codex/ChatGPT model availability;
- exact model aliases/snapshots and reasoning/speed semantics;
- applicable account usage telemetry and credit accounting;
- Sol promotional credit pricing and its expiration/status;
- Terra/Luna/Sol/Astra rate cards;
- Codex `AGENTS.md` instruction-discovery behavior and default byte limit;
- subagent usage/accounting behavior;
- Fast/Standard credit multiplier;
- any Codex runtime/version behavior used for per-arm measurement.

## Final recommendation

R027 should not be discarded. Its authority split remains the strongest candidate found.

The optimized proposal is:

> **ChatGPT controls what/why/acceptance; Codex controls where/how/execution; CI proves deterministic mechanics; compute and context are routed to the cheapest already-qualified configuration; expensive models, extra reasoning, Fast mode and subagents are escalations justified by evidence rather than defaults.**

The immediate action is not a policy migration. It is to revise T066 into a causal, fail-cheap screening experiment and preserve the larger R027+ package as a sequence of independently qualifiable mechanisms before any normative adoption.