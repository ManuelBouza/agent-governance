# T066 — R027/R028 ChatGPT + Codex Efficiency Screening Evaluation

Status: READY  
Revision: v2 — R028 deep-revalidation optimization  
Stage-Readiness: READY_FOR_STAGE5  
Executor-Authorization: NOT_AUTHORIZED_PENDING_SEPARATE_HUMAN_LAUNCH  
Owner: ChatGPT Orchestrator (evaluation specification, fixtures/oracles, control materialization, scoring and acceptance) / Codex Executor (scored technical execution only after separate Human launch)  
Type: test/eval  
SDD-Profile: ASSURED  
Test-Authorship-Mode: mixed  
Date: 2026-09-12  
Base-Branch: `develop`  
Prospective-Scientific-Branch: `test/r027-chatgpt-codex-efficiency-v1`  
Expected-Handoff: `handoffs/T066-executor-handoff.json`  
Experimental-Scope: SCREENING_ONLY

## Objective

Prospectively **screen** whether Agent Governance can move ordinary repository-local technical materialization from ChatGPT to Codex without lowering accepted quality, then determine whether Terra/Medium/Standard shows enough realized economic advantage over Sol/Medium/Standard on that bounded Executor-materialized class to justify a larger independent confirmatory evaluation.

T066 also compares the integrated Lean Executor candidate against the current D068 bundle on fresh matched work, but it does **not** claim global optimality or project-wide savings from three pairs.

T066 is an experimental qualification only. It does not change D055, D060, D065, D068, D075, D076, Markdown ownership, root instruction architecture, or the normal source-maintenance lifecycle.

No provider/model call is authorized by this Task Contract alone.

## Research authority

Current deep revalidation:

- `docs/research/R028-R027-DEEP-REVALIDATION-AND-LEAN-EXECUTOR.md`

Prior research:

- `docs/research/R027-CHATGPT-CODEX-COST-EFFICIENT-RESPONSIBILITY-SPLIT.md`

Controlling repository authority:

- D042 — remote baseline freshness;
- D052 — semantic conformance/oracle ownership;
- D053 — native SDD;
- D054 — Executor execution mechanics;
- D055 — current launch-profile policy;
- D057 — research/evaluation/decision traceability;
- D058 — worktree isolation;
- D060 — task-scoped coordinator continuity;
- D061 / D062 — protected branch controls;
- D063 — only where an already-qualified measurement surface is actually used;
- D065 / D075 — delegation/direct-execution policy, except where this experiment explicitly freezes scored-arm topology;
- D068 — current source-maintenance control boundary and experimental-topology applicability exception;
- D076 — material executable artifact boundary;
- D077 — version-sensitive upstream revalidation;
- D079 — Lean Executor qualification and adoption boundary.

## Experimental authority boundary

D068 remains the normative control policy.

T066 uses D068's explicit applicability exclusion for persisted experimental authority that fixes another authorship topology. The `EXECUTOR_MATERIALIZED` arms are therefore **experiment-only exceptions**, not prospective normal policy.

```text
CONTROL arm
  ChatGPT materializes subject candidate
  Codex verifies / diagnoses / bounded-repairs

EXECUTOR arm
  ChatGPT freezes intent / Spec / Design / Plan / acceptance
  Codex materializes subject candidate + verifies / diagnoses / repairs
```

No stage is dual-owned inside one arm.

## Screening questions

T066 answers only these bounded questions:

1. Does moving ordinary technical materialization from ChatGPT to Codex preserve accepted quality when Codex compute is held at Sol/Medium/Standard?
2. What incremental Codex token/credit cost is caused by that ownership shift under equal compute?
3. Within Executor-materialized work, does Terra/Medium/Standard show a strong enough **realized cost-per-accepted-work** signal versus Sol/Medium/Standard to justify confirmatory evaluation?
4. On new matched work, does the integrated `EXECUTOR_MATERIALIZED + Terra/Medium/Standard` bundle economically dominate the current D068 + Sol/Medium/Standard control, or does it expose a measurable Codex-cost versus Orchestrator-load tradeoff?

T066 does **not** establish:

- a project-wide savings percentage;
- a small-margin quality non-inferiority claim;
- a globally optimal model-routing policy;
- a slim-root-`AGENTS.md` policy;
- a global Standard/Fast policy;
- adaptive child routing or delegation-ROI policy;
- Markdown ownership changes;
- Luna as a normal implementation model;
- GPT-6 Astra routing policy;
- any global D068 or D055 change.

Those remain separate decision/evaluation questions even if T066 produces supporting evidence.

## Primary optimization model

T066 separates quality, Codex economics, latency and Orchestrator operating load.

Primary economic endpoint:

```text
ECAW = total attributable Codex credits
       -------------------------------
       accepted work units
```

For T066, scored arms are root-local with children disabled. The definition remains total-system safe: if a later experiment authorizes children, retries or escalations, all of their usage must count.

Raw token counts are **not** interchangeable with economic cost. Report uncached input, cached input, output/reasoning and total tokens separately from credits.

ChatGPT/Orchestrator operating load is also separate from Codex credits. T066 may deterministically record repository materialization attributable to the Orchestrator, but it must not invent a monetary conversion between ordinary Chat and Codex usage.

## Experimental constants

To avoid confounding:

```text
speed                  = STANDARD for every scored arm
reasoning               = MEDIUM for every scored arm
child/subagent topology = disabled for scored work; CONTRACT_FIXED root-local
verification contract   = identical within each matched pair
instruction envelope    = identical within each matched pair
repo/tool permissions   = identical within each matched pair
human intervention      = none after scored arm launch except genuine D033 gate
```

`Speed: STANDARD` is an experimental constant, not adoption of a new D055 default.

The common verification contract shall follow one frozen progressive shape for both arms:

```text
L0 deterministic preflight / syntax / static checks where applicable
L1 exact focal reproduction or acceptance check
L2 affected-module tests and focal lint/type checks
L3 impacted-area/dependency tests only when the frozen task geometry requires them
L4 mandatory full repository/merge gate once before terminal acceptance
```

The broadest gate must not be reflexively rerun after every intermediate repair unless the frozen task-specific contract requires it.

## Instruction-loading control

R027 measured current root `AGENTS.md` at 34,567 bytes. Current Codex documentation reports a default combined project-instruction budget of 32 KiB.

Before any scored arm, Stage 5/preflight MUST establish one identical explicit instruction-loading configuration that proves the complete governing instruction chain is loaded for every arm.

T066 MUST NOT compare a truncated arm with a complete arm, and it MUST NOT silently adopt a thin-root policy to make this experiment cheaper.

The temporary experiment configuration is a measurement/control requirement only. Thin-root/progressive-disclosure architecture is a separate future mechanism evaluation.

## Benchmark design

Stage 5 shall materialize a synthetic but repository-realistic benchmark under `evals/r027_efficiency/`.

Use exactly three ordinary source-maintenance archetypes that do not involve security-critical or exact-byte scientific behavior:

```text
A — localized Python behavior fix with implementation + regression tests
B — bounded multi-file refactor/configuration synchronization with preserved behavior
C — small CLI/API behavior addition with implementation-coupled tests
```

Markdown changes are excluded from scored subject work so Markdown ownership is not a confound.

For each experimental phase, materialize three **isomorphic task pairs**, one per archetype. Pair variants must differ only in non-semantic identifiers/data/constants needed to prevent direct solution copying while preserving equivalent step depth, file-count class, test geometry and acceptance meaning.

Each scored variant starts from a clean independently represented fixture state.

All nine pair definitions and their fixtures/oracles must be frozen before the first scored provider call. Observed results may not be used to redesign later scored fixtures.

## Arm order and independence

No scored arm may inspect another arm's candidate branch, handoff, diff or implementation before its own terminal result is represented.

The Stage 5 scheduler shall use opaque arm IDs and explicit allowed refs/paths. Cross-arm inspection is a protocol failure and invalidates the affected pair.

Within each phase, arm order shall be blocked by archetype and counterbalanced so CONTROL/CANDIDATE is not systematically first. Stage 5 must freeze a deterministic randomization seed and the resulting arm order before scored execution.

For CONTROL pairs, ChatGPT materializes the CONTROL candidate for its isomorphic variant under frozen specification authority. The paired EXECUTOR variant is distinct, so exact implementation bytes are not reusable.

## Stage 5 deliverables

Before any live Codex execution, ChatGPT Orchestrator shall publish and remotely verify a coherent Freeze A containing:

- this revised Task Contract plus R027/R028 links;
- benchmark fixture generator or fully materialized fixture set;
- nine matched pair definitions: three pairs for each of Phases 1–3;
- deterministic task specifications and Design/Plan envelopes;
- deterministic acceptance tests/oracles owned under D052;
- arm scheduler and isolation guards;
- frozen deterministic randomization seed and counterbalanced arm order;
- common progressive verification contract;
- scoring implementation;
- usage/credit normalization implementation;
- terminal result schema including `screening_only: true`;
- cross-arm contamination guard;
- provider-free geometry/integrity tests;
- exact experiment constants and prospective run ceiling;
- Codex/client/runtime version receipt;
- observable model identity/alias-resolution receipt where available;
- applicable usage-accounting/rate-card snapshot;
- instruction-loading proof and exact instruction envelope;
- D077 revalidation receipt for all volatile vendor facts needed at launch.

Freeze A must contain **no scored model outputs**.

Control solution materialization may occur only according to the frozen scheduler and must not expose solution artifacts to the paired Executor arm before that arm terminates.

## Measurement preflight

Before the first scored arm, the live Codex host must prove that each independent root can produce or be correlated with a per-arm usage receipt sufficient to determine, when exposed:

```text
model / resolved model identity where observable
reasoning effort
speed mode
uncached input tokens
cached input tokens
output/reasoning tokens
total tokens
credits or deterministic credit derivation from the frozen applicable rate card
wall-clock duration
```

If exact per-arm token attribution is unavailable, T066 is `BLOCKED_MEASUREMENT` before scored execution. Do not substitute manual estimates for token totals.

If exact credit reporting is unavailable but exact token classes plus the D077-revalidated applicable official rate card are available, deterministic credit derivation is permitted and the derivation must be frozen before scored execution.

If the applicable account does not use the token-based credit schedule assumed by the scorer, either adapt the scorer prospectively to the actually applicable measurable schedule before the first scored call or block the economic experiment.

A material rate-card, model, speed or usage-accounting change after the first scored arm stops the experiment. Do not mix economic regimes inside one scored phase.

## Phase 1 — ownership boundary isolation

Purpose: isolate the quality and incremental Codex-cost effect of **who materializes** while holding Codex compute constant.

Three isomorphic pairs:

```text
CONTROL-OWNERSHIP
  current D068 boundary
  ChatGPT subject candidate materialization
  Codex Sol / Medium / Standard verification + bounded repair

EXECUTOR-OWNERSHIP
  experimental Executor materialization boundary
  Codex Sol / Medium / Standard implementation + verification
```

Child delegation is disabled in both arms.

Phase 1 is diagnostic. It does not require the Executor-materialized arm to use fewer Codex tokens or credits than verification-only CONTROL. Requiring that would bias against the ownership change because CONTROL externalizes first-pass implementation to ChatGPT.

Phase-1 quality gate:

- all three EXECUTOR-OWNERSHIP variants must be accepted;
- no semantic/specification drift;
- no forbidden cross-arm access;
- no unresolved technical defect;
- no more than one additional rework turn in aggregate versus the three CONTROL variants.

Failure of this gate stops T066 before Phase 2.

Phase 1 reports, but does not gate on, paired Codex credits/tokens and deterministic Orchestrator materialization load.

## Phase 2 — compute isolation

Purpose: isolate model economics after ownership is fixed to Executor materialization.

Three new isomorphic pairs:

```text
EXECUTOR-SOL
  Codex materializes + verifies
  Sol / Medium / Standard

EXECUTOR-TERRA
  Codex materializes + verifies
  Terra / Medium / Standard
```

No Sol escalation is allowed inside the Terra arm in Phase 2; otherwise the model comparison is not identifiable.

Terra screening gate for this bounded work class:

- 3/3 Terra variants accepted;
- no semantic/specification drift;
- no more than one additional rework turn in aggregate versus Sol;
- paired geometric-mean Terra credits / Sol credits <= 0.80;
- no individual Terra pair may exceed 1.00x the paired Sol credits.

The `0.80` threshold represents a prospective minimum interesting realized economic signal, not the theoretical rate-card advantage.

If Terra fails this gate, Phase 3 is not executed.

## Phase 3 — integrated Lean Executor bundle

Purpose: compare the practical bundle on new matched work without pretending ChatGPT operating load and Codex credits are the same unit.

Three new isomorphic pairs:

```text
CURRENT-BUNDLE
  ChatGPT materializes subject candidate
  Codex Sol / Medium / Standard verifies + bounded-repairs

LEAN-EXECUTOR-BUNDLE
  ChatGPT owns semantic authority through Task Contract
  Codex materializes + verifies
  Terra / Medium / Standard initially
  at most one Sol / Medium / Standard escalation if a predeclared technical trigger fires
```

Allowed Sol escalation triggers are only:

- a technically valid required check still fails after one bounded Terra repair cycle;
- materially ambiguous repository-local diagnosis remains after the bounded Terra attempt but upstream Spec/Design/Plan is complete;
- a compatibility/runtime defect is evidenced that requires broader technical reasoning without changing semantics.

A suspected upstream requirement/Design/acceptance defect is **not** a Sol escalation trigger; it is SDD re-entry and invalidates/blocks the arm as appropriate.

All Terra and Sol usage in an escalated arm counts toward that arm's total ECAW.

## Phase-3 screening classifications

First require 3/3 accepted outcomes in both arms, no semantic drift and no protocol violation. Then classify using paired aggregate evidence:

```text
STRONG_SIGNAL
  Lean Executor total Codex credits < CURRENT-BUNDLE total Codex credits
  AND Lean Executor total tokens <= CURRENT-BUNDLE total Codex tokens
  AND no extra aggregate rework turns
  AND Orchestrator subject-implementation materialization is eliminated

ECONOMIC_SIGNAL
  Lean Executor total Codex credits <= 0.80 * CURRENT-BUNDLE total Codex credits
  AND Lean Executor total tokens <= 1.25 * CURRENT-BUNDLE total Codex tokens
  AND no more than one extra aggregate rework turn
  AND Orchestrator subject-implementation materialization is eliminated

OPERATING_TRADEOFF
  quality/protocol gates pass
  AND Orchestrator subject-implementation materialization is eliminated
  BUT Lean Executor does not meet STRONG_SIGNAL or ECONOMIC_SIGNAL

NOT_QUALIFIED
  candidate quality failure, semantic drift, protocol invalidity,
  or failure of a prior phase gate
```

`OPERATING_TRADEOFF` is deliberately not called a failure. The CURRENT-BUNDLE asks ChatGPT to perform implementation that is not represented in Codex credits. If Lean Executor costs more Codex credits but removes that materialization burden, T066 can identify the tradeoff but cannot assign a universal monetary value to it.

No project-wide percentage claim may be made from T066 alone.

## Primary metrics

Per arm and paired aggregate:

```text
accepted: true|false
first_attempt_accepted: true|false
rework_turns
escalation_count
model/effort/speed sequence
uncached_input_tokens
cached_input_tokens
output_reasoning_tokens
total_tokens
credits
wall_clock_seconds
verification_invocations
verification_level_sequence
changed_path_count
scope_violation: true|false
cross_arm_access_violation: true|false
orchestrator_subject_materialization_bytes
orchestrator_subject_mutation_count
semantic_reentry_count
screening_only: true
```

Derived:

```text
credits_per_accepted_work_unit (ECAW)
tokens_per_accepted_work_unit
paired_credit_ratio
paired_token_ratio
paired geometric-mean ratios by phase
acceptance_rate
first_attempt_acceptance_rate
```

With only three pairs per phase, all ratios are **descriptive screening statistics**, not confirmatory confidence claims.

## Acceptance oracle

A scored arm is accepted only when all applicable conditions hold:

1. the variant's deterministic tests pass;
2. the required behavior/spec delta is satisfied;
3. preserved behavior remains preserved;
4. no out-of-scope files/effects are introduced;
5. no forbidden cross-arm evidence was used;
6. the final represented Git state matches the arm handoff;
7. ChatGPT semantic review finds no acceptance/specification drift.

Tests may be visible to the agent; T066 evaluates governed engineering efficiency, not hidden-benchmark resistance.

## Session / independence topology

Scored arms require independent Human-visible Codex contexts so previous arm implementation cannot reduce later-arm context cost or leak solutions.

T066 therefore exercises D060's explicit persisted-experimental-authority exception:

```text
each scored arm
  -> fresh root context
  -> one isolated writable worktree/ref
  -> terminal handoff
  -> root retired before the next scored arm
```

Roots must never be concurrently writable against the same arm/worktree.

This fresh-root topology is an experimental control and does not modify normal D060 same-task continuity.

## Delegation posture

For all scored subject work:

```text
delegation_posture: CONTRACT_FIXED
children_used: 0
```

The selected archetypes are intentionally serial/write-heavy. T066 excludes child-routing economics rather than mixing R028's delegation-ROI hypothesis into the ownership/model comparison.

## Prospective run ceiling

Maximum scored arms:

```text
Phase 1: 6 arms
Phase 2: 6 arms, only if Phase 1 quality gate passes
Phase 3: 6 arms, only if Phase 2 Terra gate passes
maximum: 18 scored arms
```

Phase gates are fail-closed. Do not consume later phases after an earlier stop condition.

Preflight must establish any host/runtime-specific provider-turn ceiling needed to make the live budget auditable before execution.

## Stop conditions

Stop before consuming the next scored arm when any of the following occurs:

- measurement attribution becomes ambiguous;
- model/effort/speed cannot be proven for the arm;
- applicable economic/accounting regime changes after scored execution starts;
- experiment instruction envelope differs between a matched pair;
- complete instruction loading cannot be proven;
- fixture/pair is not isomorphic as frozen;
- cross-arm access/solution leakage is detected;
- a required current vendor fact changed and D077 revalidation is incomplete;
- a Task/Design/oracle defect is found;
- branch/worktree isolation cannot be guaranteed;
- an earlier phase gate fails;
- the Human withdraws authorization.

Persist exact partial evidence; do not silently replace or rerun a scored arm after its outcome is known.

## Confirmatory successor gate

T066 is not the final policy experiment.

After terminal T066 review:

- `STRONG_SIGNAL` or `ECONOMIC_SIGNAL` may justify designing a separate confirmatory Task Contract;
- `OPERATING_TRADEOFF` may proceed only after explicit Human selection of the tradeoff as worth confirming;
- `NOT_QUALIFIED` stops the tested bundle absent a materially new hypothesis;
- blocked outcomes require the blocker to be resolved prospectively before any successor experiment.

A confirmatory successor must use a new independent corpus and must not count T066 screening observations as confirmatory observations.

The successor should prospectively freeze a paired economic estimand, a minimum interesting improvement, alpha/power, blocked randomization and sample size. R028 provides a planning range of roughly 20–48 matched pairs depending on the frozen effect/variance assumptions; the exact N must be fixed before confirmatory scored execution.

## Separate mechanism evaluations

T066 deliberately does not bundle these hypotheses:

- thin root `AGENTS.md` + progressive disclosure;
- Luna N0 routing;
- subagent/child ROI;
- Standard/Fast latency economics;
- verification-ladder economics as a variable;
- Markdown ownership refinement;
- GPT-6 Astra premium routing.

If T066 is promising, these should be qualified independently before an integrated R027+ normative package is evaluated.

## Explicit exclusions

T066 must not:

- modify production product behavior as part of scored subject work;
- use T065/T023 scientific branches, fixtures, observations or provider budget;
- resume T062/T063/T058/T024;
- use Fast mode in scored arms;
- use High/XHigh/Max/Ultra reasoning;
- use Luna or Astra for scored implementation;
- use subagents/children for scored subject work;
- change global D055/D065/D068/D075/D076 authority during the experiment;
- change root instruction policy or Markdown ownership;
- treat a successful screening result as automatic normative adoption.

## Stage 7 disposition

After terminal evidence, ChatGPT Orchestrator shall review the complete frozen protocol and represented results and persist a T066 review with exactly one primary experimental disposition:

```text
STRONG_SIGNAL
ECONOMIC_SIGNAL
OPERATING_TRADEOFF
NOT_QUALIFIED
BLOCKED_MEASUREMENT
BLOCKED_EXECUTION
```

Then update R027/R028 disposition as appropriate:

- remain `EVALUATING` while confirmatory/mechanism qualification is still required;
- move to `DECIDED` only if an accepted normative Decision explicitly adopts a conclusion;
- never promote T066 screening evidence directly into policy without the D057 decision gate.

## Current readiness

```text
Task Contract design: COMPLETE (v2 screening revision)
R027 research: COMPLETE / EVALUATING
R028 deep revalidation: COMPLETE / EVALUATING
Stage 5 benchmark/harness materialization: NOT_STARTED
Scientific branch: NOT_CREATED
Executor launch: NOT_AUTHORIZED
Provider/model calls consumed by T066: 0
Scored observations: 0
```

Next action when T066 is explicitly selected as the active work unit: ChatGPT Orchestrator performs Stage 5 provider-free materialization and Freeze A on a fresh scientific branch, then stops before any live Executor launch for a separate Human authorization.