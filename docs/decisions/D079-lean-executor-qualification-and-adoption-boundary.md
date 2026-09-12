# D079 — Lean Executor Qualification and Adoption Boundary

Status: ACCEPTED  
Date: 2026-09-12  
Authority: Human Owner / ChatGPT Orchestrator  
Trigger: Human instruction to formalize R027/R028 after R028 deep revalidation and before any T066 Stage 5 materialization or scored provider/model execution  
Research: R027, R028  
Evaluation: T066 v2  
Refines: D057 for the R027/R028 research-to-decision path  
Preserves: D052, D053, D054, D055, D060, D063, D065, D068, D075, D076, D077, current Markdown ownership  
Production-Policy-State: UNCHANGED_PENDING_QUALIFICATION

## Problem

R027 identified a plausible comparative-advantage split between ChatGPT and Codex. R028 then revalidated that proposal against current OpenAI product/model economics, Codex instruction loading, subagent overhead, progressive verification and causal evaluation design.

The resulting `R027+ / Lean Executor` architecture is stronger than either extreme:

- universal ChatGPT technical materialization followed by Codex verification; or
- unconstrained Codex autonomy that also owns requirements, Design and semantic acceptance.

However, the research itself explicitly concludes that the candidate architecture should be **evaluated rather than adopted from research alone**. T066 has not begun Stage 5, has consumed zero provider/model calls and has produced zero scored observations.

Agent Governance therefore needs a formal decision that converts the research into durable authority **without pretending that an unexecuted experiment has already qualified the production policy**.

## Decision

Agent Governance SHALL treat **R027+ / Lean Executor as the selected architecture candidate for prospective qualification**, and SHALL use the staged evidence boundary in this decision before any production ownership, launch-profile, context, delegation or Markdown-policy migration is adopted.

The selected candidate architecture is:

```text
ChatGPT Orchestrator — semantic control plane
  intent / external research / requirements
  Specification / Design / Plan / acceptance
  normative governance and semantic-oracle authority
  final semantic convergence / acceptance / integration decision

Codex Executor — repository-local technical plane
  repository exploration
  technical materialization
  implementation-coupled tests / config / tooling
  execution / diagnosis / bounded repair
  technical verification and concise represented evidence

Deterministic tooling / CI — mechanical proof plane
  mechanically enforceable checks
  progressive technical feedback
  mandatory final repository / merge gates
```

This architecture is **selected for qualification**, not activated as the normal source-maintenance lifecycle by D079.

## Current production authority remains unchanged

D068 remains the normative source-maintenance control boundary unless and until a later accepted Decision explicitly changes it.

Therefore, outside an expressly authorized experimental topology:

```text
current D068 mode
  ChatGPT Orchestrator -> complete Stage 5 candidate materialization
  Executor             -> Stage 6 execute / diagnose / bounded-repair / verify
```

continues to control.

D079 does not authorize ordinary source-maintenance work to switch immediately to Executor first-pass materialization.

The prospective names:

```text
EXECUTOR_MATERIALIZED
ORCHESTRATOR_FROZEN_CANDIDATE
```

are approved as **qualification vocabulary** only. They do not acquire production authority merely because this decision names them.

## T066 is the required screening gate

T066 v2 is the canonical first empirical gate for the R027+ ownership/compute hypothesis.

Its role is screening only:

1. isolate the ownership shift under equal Sol/Medium/Standard compute;
2. isolate Terra/Medium/Standard versus Sol/Medium/Standard after ownership is fixed to Executor materialization;
3. compare the integrated Lean Executor bundle with the current D068 bundle on fresh matched work;
4. stop cheaply when quality, protocol, measurement or economics do not justify further evaluation.

The earlier implication that three matched pairs per phase could directly qualify global policy is rejected. T066 results are descriptive screening evidence and SHALL NOT, by themselves, modify D068, D055, D065, Markdown ownership or root instruction policy.

No provider/model call is authorized by D079. T066 still requires its own completed provider-free Stage 5 readiness and a later separate Human launch authorization.

## Quality is a hard gate; economics are conditional on accepted work

For the R027+ qualification line, quality and semantic correctness SHALL gate economic interpretation.

The primary Codex economic endpoint is:

```text
ECAW = total attributable Codex credits
       -------------------------------
       accepted work units
```

Economic accounting SHALL include all Codex usage attributable to an arm or future governed work unit, including root work, any authorized children, retries, repair turns and escalations.

The following dimensions SHALL remain separately reported rather than collapsed into one unsupported utility number:

```text
Quality
  acceptance / first-pass acceptance
  semantic drift
  escaped defects / protocol violations

Codex economics
  uncached input tokens
  cached input tokens
  output/reasoning tokens
  total tokens
  credits / ECAW
  retries / repair turns / escalations

Latency
  end-to-end wall time
  verification/tool time when measurable

Orchestrator operating load
  subject implementation materialized by ChatGPT
  deterministic materialization bytes/mutations when available
  semantic re-entry count
```

Raw token count SHALL NOT be treated as equivalent to economic cost. ChatGPT operating load SHALL NOT be assigned an invented monetary conversion against Codex credits unless a future accepted method establishes comparable telemetry and valuation.

## Screening outcome boundary

T066 v2 dispositions have the following decision meaning:

```text
STRONG_SIGNAL / ECONOMIC_SIGNAL
  -> candidate may advance to independent confirmation
  -> no automatic production adoption

OPERATING_TRADEOFF
  -> no automatic rejection
  -> Human must explicitly select whether the tradeoff is worth confirming

NOT_QUALIFIED
  -> tested bundle stops
  -> no successor run without a materially new prospective hypothesis

BLOCKED_MEASUREMENT / BLOCKED_EXECUTION
  -> resolve the exact blocker prospectively
  -> do not reinterpret missing evidence as positive evidence
```

Observed T066 outputs may not be reused as confirmatory observations.

## Independent confirmation is mandatory before ownership-policy migration

A positive T066 screening result is necessary but insufficient for changing the normal ownership boundary.

Before a later Decision may adopt `EXECUTOR_MATERIALIZED` as a normal source-maintenance mode, an independent confirmatory evaluation SHALL:

- use a fresh corpus disjoint from T066 scored observations;
- freeze the primary paired economic estimand before execution;
- freeze the minimum interesting effect before execution;
- freeze alpha, power target, blocked randomization and sample size prospectively;
- measure quality non-inferiority or an explicitly stronger quality gate appropriate to the intended scope;
- account for all candidate retries/escalations/children in total-system economics;
- preserve matched instruction, permission, verification and task geometry controls needed for causal attribution;
- satisfy D077 immediately before consequential launch for volatile provider/model/runtime/economic facts.

R028's `20–48 matched pairs` is only a planning range. The exact confirmatory sample size is not decided by D079 and must be frozen from the successor experiment's prospective assumptions before scored execution.

## Integrated adoption requires mechanism isolation

D079 rejects an all-at-once migration in which multiple unqualified optimizations are bundled and a positive aggregate outcome is then attributed to all of them.

The following remain separate mechanism questions unless a later experiment explicitly and causally qualifies them:

- thin root `AGENTS.md` / progressive-disclosure instruction architecture;
- Luna N0 routing;
- subagent/child ROI;
- Standard/Fast latency economics;
- verification-ladder economics as an experimental variable;
- Markdown ownership refinement;
- GPT-6 Astra premium routing.

A future integrated R027+ package may combine only mechanisms that are already qualified for the intended scope or that are themselves prospectively isolated inside the integrated evaluation.

## Context and instruction-budget boundary

R027/R028 identify a material risk that the current root `AGENTS.md` exceeds Codex's documented default combined project-instruction budget.

D079 accepts that finding as a **qualification blocker/risk to control**, not as authority to rewrite `AGENTS.md` immediately.

For T066, complete governing instruction loading must be proven identically across matched arms. A future thin-root/progressive-disclosure change requires its own prospective qualification with no governance/safety instruction misses.

Raising `project_doc_max_bytes` solely to preserve a monolithic root file is not adopted as the preferred long-term architecture by this decision.

## Compute-routing boundary

R028's class-based routing ladder is retained as a hypothesis:

```text
N0 -> Luna / Low-or-Medium / Standard candidate
N1 -> Terra / Medium / Standard candidate
N2 -> Sol / Medium / Standard candidate
N3 -> Sol / High or separately qualified premium candidate
```

D079 does not change D055. In particular:

- Terra/Medium is not yet the normal implementation default;
- Luna is not yet a normal implementation profile;
- Astra is not inserted into the R027+ path by default;
- increased reasoning is not a substitute for missing Spec/Design/Plan authority;
- Fast mode is not adopted as a normal economic default.

Any later routing policy must be based on realized accepted-work economics, not theoretical per-token price alone.

## Subagent/delegation boundary

D065 and D075 remain unchanged.

Subagents are not adopted as a cost-saving primitive by D079. A future subagent optimization must show positive **total-system** ROI after counting root plus every child, coordination, retries and any escalation.

Parallel or specialist children remain plausible only where their independent parallelism, context isolation, cheaper specialist compute, noisy-output containment or independent review benefit is prospectively worth the duplicated agent work.

## Progressive verification boundary

R028's L0→L4 verification ladder is accepted as the common **experimental control shape** for T066 and as a future optimization hypothesis:

```text
L0 deterministic preflight / syntax / static checks
L1 exact focal reproduction / acceptance check
L2 affected-module tests + focal lint/type checks
L3 impacted-area/dependency checks when blast radius requires them
L4 mandatory final repository/merge gate
```

D079 does not waive any mandatory repository gate. It rejects only the assumption that the broadest gate must be rerun after every intermediate repair when the frozen task contract does not require that repetition.

Any future production verification-policy refinement still requires explicit normative adoption.

## Version-sensitive facts remain revalidation-bound

No volatile vendor fact from R027/R028 becomes timeless policy through D079.

Before consequential experiment launch or later adoption, D077 still requires revalidation of materially relevant facts including:

- model availability and aliases;
- reasoning/speed semantics;
- account-specific usage telemetry and credit accounting;
- model/credit rate cards and promotions;
- project-instruction discovery and byte limits;
- subagent accounting/runtime behavior;
- Fast/Standard multipliers;
- Codex runtime/version behavior used for measurement.

## Research disposition

D079 decides the **qualification and adoption boundary** for the R027/R028 line. It does not decide the final production result that the empirical program is designed to measure.

Therefore:

```text
R027: COMPLETE / EVALUATING
  retained as predecessor evidence

R028: COMPLETE / EVALUATING
  current analytical authority for the Lean Executor candidate

D079: ACCEPTED
  selects Lean Executor as the candidate architecture
  adopts the staged evidence/adoption boundary

T066 v2: READY_FOR_STAGE5 but not selected here as live work
  screening evidence = 0
  provider/model calls = 0
```

R027/R028 may move to a final `DECIDED`, `REJECTED`, `SUPERSEDED` or other D057 disposition only through later persisted evidence and authority appropriate to the production question.

## Relationship to the current frontier

D079 does not displace T065/T023 v17 as the current Orchestrator checkpoint frontier.

`docs/orchestrator/CHECKPOINT.md` therefore remains unchanged by this decision.

If the Human later explicitly selects T066 as the active work unit, the cold-start load for that work SHALL include D079 in addition to T066, R028 and the normal bootstrap authority. Stage 5 remains provider-free and must stop before any live Executor launch.

## Consequences

- R027+ / Lean Executor is now the official candidate architecture for qualification, not an informal research suggestion.
- D068 remains the current production ownership policy.
- T066 v2 is the required fail-cheap screening gate for the ownership/compute bundle.
- accepted-work economics, not raw token count alone, controls the economic question.
- ChatGPT materialization burden remains a separate operating-load dimension rather than hidden or falsely monetized.
- a positive screening result cannot directly change production policy;
- independent fresh-corpus confirmation is mandatory before ownership-policy migration;
- context slimming, Luna, subagents, Fast, Markdown ownership and premium-model routing remain separate qualifications;
- D077 revalidation remains mandatory for volatile provider/model/runtime/economic facts;
- no Executor launch, provider/model call, scientific branch creation or production-policy migration is authorized by D079 itself.
