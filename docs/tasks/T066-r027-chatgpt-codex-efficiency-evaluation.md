# T066 — R027 ChatGPT + Codex Efficiency Evaluation

Status: READY  
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

## Objective

Prospectively measure whether Agent Governance can move ordinary repository-local technical materialization from ChatGPT to Codex **without lowering accepted quality and without increasing Codex economic cost per accepted work unit**, then separately measure whether Terra/Medium can replace Sol/Medium for that bounded implementation class.

T066 is an experimental qualification only. It does not change D055, D060, D065, D068, D075, D076, Markdown ownership, or the normal source-maintenance lifecycle.

No provider/model call is authorized by this Task Contract alone.

## Research authority

Primary research:

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
- D063 — only where an already-qualified child measurement surface is actually used;
- D065 / D075 — delegation/direct-execution policy, except where this experiment explicitly freezes scored-arm topology;
- D068 — current source-maintenance control boundary and experimental-topology applicability exception;
- D076 — material executable artifact boundary;
- D077 — version-sensitive upstream revalidation.

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

## Questions under test

T066 answers only these bounded questions:

1. What additional Codex token/credit cost is caused by moving ordinary technical materialization from ChatGPT to Codex while holding Codex compute constant?
2. Does that ownership shift preserve accepted technical quality on matched work?
3. Within Executor-materialized work, can Terra/Medium materially reduce credits versus Sol/Medium while preserving quality?
4. Does the integrated `EXECUTOR_MATERIALIZED + Terra/Medium` bundle match or improve the current D068 + Sol/Medium control on Codex cost per accepted work unit?

T066 does **not** qualify:

- slim-root-`AGENTS.md` policy;
- global Standard/Fast policy;
- adaptive child routing;
- delegation-ROI policy;
- Markdown ownership changes;
- Luna as a normal implementation model;
- any global D068 or D055 change.

Those remain separate decision questions even if T066 provides supporting evidence.

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

Because current root `AGENTS.md` exceeds Codex's documented default combined project-instruction budget, Stage 5 readiness MUST establish one identical, explicit experiment instruction-loading configuration for all arms that proves the complete governing instruction chain is loaded. T066 MUST NOT compare an intentionally truncated CONTROL against a complete CANDIDATE or vice versa.

The temporary experiment configuration does not itself decide the future project instruction budget.

## Benchmark design

Stage 5 shall materialize a synthetic but repository-realistic benchmark under `evals/r027_efficiency/`.

Use exactly three ordinary source-maintenance archetypes that do not involve security-critical or exact-byte scientific behavior:

```text
A — localized Python behavior fix with implementation + regression tests
B — bounded multi-file refactor/configuration synchronization with preserved behavior
C — small CLI/API behavior addition with implementation-coupled tests
```

Markdown changes are excluded from scored subject work so Markdown ownership is not a confound.

For each experimental phase, materialize three **isomorphic task pairs**, one per archetype. Pair variants must differ only in non-semantic identifiers/data/constants needed to prevent direct solution copying while preserving equivalent step depth, file count class, test geometry and acceptance meaning.

Each scored variant starts from a clean independently represented fixture state.

## Pair independence

No scored arm may inspect another arm's candidate branch, handoff, diff or implementation before its own terminal result is represented.

The Stage 5 scheduler shall use opaque arm IDs and explicit allowed refs/paths. Cross-arm inspection is a protocol failure and invalidates the affected pair.

For CONTROL pairs, ChatGPT materializes the CONTROL candidate for its isomorphic variant under frozen specification authority. The paired EXECUTOR variant is distinct, so exact implementation bytes are not reusable.

## Stage 5 deliverables

Before any live Codex execution, ChatGPT Orchestrator shall publish and remotely verify a coherent Freeze A containing:

- this Task Contract and R027 link;
- benchmark fixture generator or fully materialized fixture set;
- nine matched pair definitions: three pairs for each of Phases 1–3;
- deterministic task specifications and Design/Plan envelopes;
- deterministic acceptance tests/oracles owned under D052;
- arm scheduler and isolation guards;
- scoring implementation;
- usage/credit normalization implementation;
- terminal result schema;
- cross-arm contamination guard;
- provider-free geometry/integrity tests;
- exact experiment constants and arm order;
- exact prospective run ceiling;
- D077 revalidation receipt for model/speed/usage facts needed at launch.

Freeze A must contain **no scored model outputs**.

Control solution materialization may occur only according to the frozen scheduler and must not expose solution artifacts to the paired Executor arm before that arm terminates.

## Measurement preflight

Before the first scored arm, the live Codex host must prove that each independent root can produce or be correlated with a per-arm usage receipt sufficient to determine, when exposed:

```text
model
reasoning effort
speed mode
uncached input tokens
cached input tokens
output/reasoning tokens
total tokens
credits or a deterministic credit derivation from the frozen current rate card
wall-clock duration
```

If exact per-arm token attribution is unavailable, T066 is `BLOCKED_MEASUREMENT` before scored execution. Do not substitute manual estimates for token totals.

If exact credit reporting is unavailable but exact token classes plus the D077-revalidated official rate card are available, deterministic credit derivation is permitted and the derivation must be frozen before scored execution.

## Phase 1 — ownership boundary isolation

Purpose: isolate the cost/quality effect of **who materializes** while holding Codex compute constant.

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

Phase 1 is diagnostic. It does not require the Executor-materialized arm to use fewer Codex tokens than verification-only CONTROL. It measures the incremental Codex cost of moving implementation while enforcing the quality gate below.

Phase-1 quality gate:

- all three EXECUTOR-OWNERSHIP variants must be accepted;
- no semantic/specification drift;
- no forbidden cross-arm access;
- no unresolved technical defect;
- no more than one additional rework turn in aggregate versus the three CONTROL variants.

Failure of this gate stops T066 before Phase 2.

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

Terra qualification gate for this bounded work class:

- 3/3 Terra variants accepted;
- no semantic/specification drift;
- no more than one additional rework turn in aggregate versus Sol;
- paired median Terra credits / Sol credits <= 0.75;
- no individual Terra pair may exceed 1.00x the paired Sol credits.

If Terra fails the quality gate, Phase 3 is not executed.

## Phase 3 — integrated bundle

Purpose: answer the user's practical combination question on new matched work.

Three new isomorphic pairs:

```text
CURRENT-BUNDLE
  ChatGPT materializes subject candidate
  Codex Sol / Medium / Standard verifies + bounded-repairs

OPTIMIZED-BUNDLE
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

All Terra and Sol usage in an escalated arm counts toward that arm's total cost.

## Integrated outcome classes

For Phase 3, first require 3/3 accepted outcomes in both arms. Then classify the candidate bundle using paired totals:

```text
STRONG_WIN
  candidate total credits < control total credits
  AND candidate total tokens <= control total tokens
  AND no extra aggregate rework turns

ECONOMIC_WIN
  candidate total credits <= 0.80 * control total credits
  AND candidate total tokens <= 1.25 * control total tokens
  AND no more than one extra aggregate rework turn

TRADEOFF
  quality passes but neither STRONG_WIN nor ECONOMIC_WIN holds

NOT_QUALIFIED
  any candidate quality failure, protocol invalidity, or cost gate failure outside TRADEOFF
```

`ECONOMIC_WIN` explicitly permits modestly higher token volume only when cheaper compute produces at least 20% credit savings. This prevents claiming raw-token savings where only credit savings occurred.

No project-wide percentage claim may be made from T066 alone.

## Primary metrics

Per arm and paired aggregate:

```text
accepted: true|false
first_attempt_accepted: true|false
rework_turns
model/effort/speed sequence
uncached_input_tokens
cached_input_tokens
output_reasoning_tokens
total_tokens
credits
wall_clock_seconds
verification_invocations
changed_path_count
scope_violation: true|false
cross_arm_access_violation: true|false
```

Derived:

```text
credits_per_accepted_work_unit
tokens_per_accepted_work_unit
paired_credit_ratio
paired_token_ratio
acceptance_rate
first_attempt_acceptance_rate
```

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

The selected archetypes are intentionally serial/write-heavy. T066 therefore excludes child-routing economics rather than mixing R027's delegation-ROI hypothesis into the ownership/model comparison.

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
- experiment instruction envelope differs between a matched pair;
- fixture/pair is not isomorphic as frozen;
- cross-arm access/solution leakage is detected;
- a required current vendor fact changed and D077 revalidation is incomplete;
- a Task/Design/oracle defect is found;
- branch/worktree isolation cannot be guaranteed;
- an earlier phase gate fails;
- the Human withdraws authorization.

Persist exact partial evidence; do not silently replace or rerun a scored arm after its outcome is known.

## Explicit exclusions

T066 must not:

- modify production product behavior as part of scored subject work;
- use T065/T023 scientific branches, fixtures, observations or provider budget;
- resume T062/T063/T058/T024;
- use Fast mode in scored arms;
- use High/XHigh/Max/Ultra reasoning;
- use Luna for scored implementation;
- use subagents/children for scored subject work;
- change global D055/D065/D068/D075/D076 authority during the experiment;
- change Markdown ownership;
- treat a successful pilot as automatic normative adoption.

## Stage 7 disposition

After terminal evidence, ChatGPT Orchestrator shall review the complete frozen protocol and represented results and persist a T066 review with exactly one primary experimental disposition:

```text
STRONG_WIN
ECONOMIC_WIN
TRADEOFF
NOT_QUALIFIED
BLOCKED_MEASUREMENT
BLOCKED_EXECUTION
```

Then update R027's `Decision-State` disposition as appropriate:

- remain `EVALUATING` when broader qualification or separate decision questions remain;
- move to `DECIDED` only if an accepted normative Decision explicitly adopts a conclusion;
- never promote T066 evidence directly into policy without the D057 decision gate.

## Current readiness

```text
Task Contract design: COMPLETE
Research approval: HUMAN_APPROVED_FOR_EVALUATION_DESIGN
Stage 5 benchmark/harness materialization: NOT_STARTED
Scientific branch: NOT_CREATED
Executor launch: NOT_AUTHORIZED
Provider/model calls consumed by T066: 0
Scored observations: 0
```

Next action when T066 is explicitly selected as the active work unit: ChatGPT Orchestrator performs Stage 5 provider-free materialization and Freeze A on a fresh scientific branch, then stops before any live Executor launch for a separate Human authorization.