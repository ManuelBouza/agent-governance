# R016 — MG1 V12 reference-family overactivation re-entry

Research-ID: R016  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-06  
Last-Reviewed: 2026-09-06  
Owner: ChatGPT Orchestrator  
Scope: D050 / T023 single-reference-family activation behavior after accepted MG1-v12  
Question: Why did B0/B1 overactivate on maintenance/Skill near-misses, and what prospective reference-family architecture can preserve D050 intent while reducing false activation?  
Evaluation-Refs: `docs/reviews/T023-R11.md`; `evals/skill_activation_topology/corpus.json`; `evals/skill_activation_topology/oracle.json`; `evals/skill_activation_topology/presentations-v3/B0/agent-governance/SKILL.md`; `evals/skill_activation_topology/presentations-v3/B1/agent-governance-router/SKILL.md`  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Authority and evidence boundary

This investigation is prospective Explore / Specify work under D050 after T023-R11 accepted MG1-v12 as a valid terminal experiment with no qualifying B0/B1 reference.

V12 is not rerun, rescored or reinterpreted. Its exposed corpus and outcomes are design evidence only. No V12 observation may become acceptance evidence for a redesigned candidate.

D050 remains controlling: one Agent Governance product, one normative `governance-core/`, one shared deterministic engine, one canonical capability source, profile isolation, source independence, portable activation, bounded permissions/security, one atomic distribution identity and pre-registered multidimensional selection.

## Observed failures

V12 established two independent single-family false activations:

- B0 activated `agent-governance` on `WM02`: an unrelated Go-library maintainer-policy request with no Agent Governance applicability.
- B1 activated `agent-governance-router` on `WM05`: a linting-Skill request that explicitly states Agent Governance is not installed.

Each single false activation over the frozen 11-case negative/near-miss denominator produced `1/11 = 0.090909...`, above the frozen `false_activation_rate <= 0.05` threshold. B0 and B1 therefore became mathematically non-qualifying under V12.

The failures occur on different stimuli and different near-miss axes. They are not evidence of one corrupted prompt, scheduler error or shared execution artifact.

## Structural diagnosis

### 1. The failing boundary is catalog activation, not post-activation routing

D050's portable model makes the host/current Agent discover Skill catalog metadata and select a Skill before the Skill body can progressively load references or apply its internal router.

B0 and B1 both contain safe post-activation routing instructions, but those instructions execute too late to prevent a host-observed false activation. A router that activates and then decides "not applicable" still fails the false-activation metric.

Therefore the relevant design surface is the host-facing activation metadata, especially the top-level Skill name/description, not the internal capability router alone.

### 2. B0/B1 expose a union-shaped activation description

A single top-level entrypoint must advertise three materially different intent families at once:

- governed Consumer lifecycle work;
- canonical Agent Governance source maintenance;
- Agent Governance-scoped external Skill trust.

The B0/B1 descriptions consequently contain generic high-similarity terms such as `source`, `maintenance`, `Skill`, `Governance` and related exclusions. Those terms overlap strongly with unrelated maintenance and Skill requests even when the actual Agent Governance applicability condition is absent.

This is a structural precision cost of the current single-reference metadata surface, not a defect in the shared Core, engine or capability semantics.

### 3. Negative exclusions are not a reliable hard filter

Both descriptions try to suppress near-misses by enumerating exclusions such as unrelated source maintenance or generic Skill installation. That wording still places the excluded vocabulary inside the activation metadata presented to the host selector.

V12 shows that negative wording cannot be treated as a deterministic catalog filter. Semantic/lexical similarity can remain high even when the description says "do not activate". The two failures expose complementary weaknesses:

- `WM02`: generic `maintainer` / `source code` language can attract the source-maintainer portion of the union even without an Agent Governance anchor;
- `WM05`: an explicit `Agent Governance` mention plus `Skill` language can attract the Skill-trust/router surface even when applicability is explicitly negated.

Adding more negative examples would increase metadata vocabulary and risks tuning to exposed prompts rather than fixing the boundary.

### 4. B0 preloading is not the root cause; B1 proves progressive disclosure is insufficient

B0 preloads all three references after activation, which is costly for context and increases downstream surface once selected. But the `WM02` false activation happens before that preload can matter.

B1 correctly avoids preloading and routes references progressively, yet it still fails on `WM05`. Therefore thin routing improves context behavior but does not by itself solve activation precision while the host-facing description remains a broad union of intents.

### 5. The reference-family defect is applicability ambiguity

The current metadata gives too much weight to topic similarity and too little to affirmative product applicability.

The missing invariant is a positive conjunction:

```text
affirmative Agent Governance applicability
AND
an Agent Governance capability intent
```

Generic maintenance, governance or Skill vocabulary must never be sufficient by itself. A mere mention of Agent Governance, especially a statement that it is absent or inapplicable, must also be insufficient.

## Alternatives considered

### Expand the negative list — reject

Pros: minimal edit.

Cons: overfits exposed V12 stimuli, increases near-miss vocabulary inside the retrieval surface, and still depends on the host treating negation as a hard selector constraint.

### Post-activation self-demotion — reject as false-activation remedy

Pros: easy to implement in the router body.

Cons: a body read is already a host-observed activation, so returning "not applicable" cannot satisfy the frozen false-activation metric.

### Deterministic pre-router before Skill discovery — reject as portable baseline

Pros: could enforce exact applicability outside the model selector.

Cons: D050's portable contract does not require a host-independent pre-selection hook or Skill-to-Skill stack. Making such a hook mandatory would introduce a new portability/runtime dependency and would require separate authority.

### Positive-anchor single router — recommended for prospective design

Retain one activatable reference entrypoint but make its catalog surface a minimal positive applicability contract rather than a union of positive and negative topical vocabulary.

This preserves the single-family reference concept while addressing the actual failing boundary.

## Proposed prospective family: Positive-Anchor Single Router

Working name only: **Positive-Anchor Single Router (PASR)**. This is not yet a registered T023 candidate ID and does not select a release topology.

### Host-facing activation contract

Activation requires both:

1. **affirmative Agent Governance applicability**, expressed by one of these product-specific contexts:
   - an installed/governed Agent Governance Consumer repository;
   - the canonical Agent Governance source product;
   - an explicit request to apply Agent Governance trust requirements to an external Skill;
2. **a capability intent** belonging to `consumer-lifecycle`, `source-maintainer`, or `external-skill-trust`.

The activation metadata should be concise, positive and product-specific. It should not enumerate generic negative topics such as generic Git, source maintenance, linting, releases, governance or Skill installation.

A generic topic match is not an applicability anchor. A statement that Agent Governance is absent, not installed, not applicable or intentionally not being used is also not an affirmative applicability anchor.

### Internal routing contract

After activation, use the B1-style thin-router behavior:

- do not preload capability references;
- load only the capability reference(s) required by the qualified intent;
- require the existing exact source-product signal before granting `source-maintainer` context;
- retain `clarify-context` for affirmative Agent Governance requests whose source-versus-Consumer role is genuinely unresolved;
- retain bounded rejection for cross-profile requests;
- preserve all existing authority, permission and isolation boundaries.

### Semantic invariants

PASR changes activation presentation only. It must not change:

- `governance-core/` authority;
- deterministic runtime behavior;
- capability semantics;
- profile definitions;
- source independence;
- mutation/permission/security envelopes;
- one-product/one-version distribution identity;
- portable no-mandatory-Skill-to-Skill rule.

## Prospective evaluation evidence required

Because V12 prompts and outcomes are exposed to this design process, every current V12 corpus case is design evidence only for a redesigned candidate.

A future acceptance epoch must:

1. freeze PASR semantics and exact candidate presentation before the exact new acceptance stimuli are available for tuning;
2. use a new corpus/holdout identity and new execution/oracle epoch;
3. forbid all V12 observations from acceptance scoring;
4. preserve the accepted multidimensional qualification thresholds:
   - activation precision `>= 0.95`;
   - activation recall `>= 0.95`;
   - activation F1 `>= 0.95`;
   - false activation rate `<= 0.05`;
   - wrong-specialist rate `<= 0.05`;
   - overactivation rate `<= 0.05`;
   - semantic outcome accuracy `>= 0.95`;
   - zero critical cross-profile/ambiguous permission violations;
5. preserve mandatory deterministic correctness, profile isolation, Consumer source independence, source/distribution integrity and single-install feasibility;
6. prospectively define a negative/near-miss sample size and sampling rationale sufficient to measure the 5% false-activation boundary without choosing the denominator to rescue a known failure;
7. contain fresh contrastive near-miss classes covering at least:
   - unrelated source/maintainer work with no Agent Governance applicability;
   - generic Skill recommendation/installation/tooling with no Agent Governance trust scope;
   - explicit Agent Governance absence/opt-out/non-applicability;
   - incidental product mention without governed intent;
   - governance/skill/source homonyms outside the product;
   - matched true-positive cases with affirmative Agent Governance applicability;
8. retain fresh positive, ambiguous, cross-profile and multi-intent coverage so precision is not improved by sacrificing recall or safety;
9. pre-register exact prompts, hashes, case semantics, repeated-trial policy, ordering, host/model envelope and futility/selection rules before live acceptance calls;
10. close and rotate the epoch again if exact holdout content is used to tune candidate wording after freeze.

If PASR qualifies, F2/G3 may be evaluated only under a prospectively revised D050/T023 gate using the same fresh acceptance epoch and the qualifying PASR result as the reference. V12 non-execution of F2/G3 remains non-evidence.

## Conclusion

V12 is a valid design result demonstrating that the current B0/B1 single-reference family is too broad at the catalog-activation boundary. The failure is not fixed by more post-activation routing or by adding negative examples.

The strongest prospective direction is a B1-derived thin single router with a minimal positive, conjunctive applicability contract. This preserves D050's one-product/Core/engine/capability-source architecture while directly targeting the false-activation mechanism exposed by `WM02` and `WM05`.

The research question is complete. Empirical qualification remains open; therefore `Decision-State` stays `EVALUATING` until a future accepted experiment establishes whether the redesigned family qualifies and whether any topology should be selected.
