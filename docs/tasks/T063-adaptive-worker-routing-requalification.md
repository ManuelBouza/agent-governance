# T063 — Adaptive Worker Routing Requalification

## Identity

- Task ID: `T063`
- Status: `DRAFT / STAGE5_REQUIRED / NOT_AUTHORIZED`
- Type: `read-only replicated matched-arm Executor/subagent evaluation`
- SDD profile: `ASSURED`
- Base branch: `develop`
- Expected topic branch: `test/t063-adaptive-worker-routing-requalification-v7`
- Expected executor handoff: `handoffs/T063-executor-handoff-v7.json`
- Expected telemetry: `handoffs/T063-adaptive-worker-routing-telemetry-v7.json`
- Test-Authorship-Mode: `orchestrator-conformance`
- Owner: ChatGPT Orchestrator (specification/oracle/acceptance and D068 Stage 5) / Agente de IA Ejecutor (Stage 6 execution/evidence) / Human Owner (final authority and Human-mediated launch)
- Current design review: `docs/reviews/T063-R13.md`
- Prior convergence: `docs/reviews/T063-R12.md`
- Measurement authority: `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md`
- Delegation authority: `docs/decisions/D065-semantic-executor-delegation-obligation.md`
- Routing gate authority: `docs/decisions/D075-coordinator-direct-execution-gate.md`
- Materialization boundary: `docs/decisions/D076-stage6-ephemeral-executable-materialization-boundary.md`
- Version authority: `docs/decisions/D077-version-sensitive-upstream-revalidation.md`

## Objective

Run one clean, prospectively replicated qualification evaluation to determine whether the frozen task-adaptive delegated-worker profiles preserve absolute oracle-scored quality across repeated trials and, when the root-equivalent CONTROL also meets accepted quality, whether ADAPTIVE provides material provider-neutral token efficiency and/or a validated lower-tier routing result.

T063 evaluates Stage B worker compute routing only. Delegation-worthiness is fixed by D075/D065 and is not an experimental variable. This Task Contract does not adopt a global adaptive routing policy.

## Current specification carrier / controlling references

Load only the smallest controlling set needed for execution:

- `AGENTS.md`;
- this Task Contract;
- `docs/reviews/T063-R13.md`;
- `docs/reviews/T063-R12.md` for v6 convergence/provenance;
- `docs/research/R021-T063-V3-CONFIG-AUTHORITATIVE-WORKER-RECEIPTS.md`;
- `docs/research/R022-T063-V3-EMPTY-ROLLOUT-REATTACH-RACE.md`;
- `docs/research/R023-T063-V5-LIVE-SPAWN-RECEIPT-PERSISTENCE-GAP.md`;
- D063, D065, D075, D076 and D077.

Historical T054/T063 v1-v6 attempts are planning/provenance evidence only and MUST NOT be reused for v7 scoring.

## Requirement / specification delta

### ADDED

- **T063-RQ-14 — fixed replication:** execute exactly four replicate blocks, giving 24 scored first-attempt child trials when the run completes validly.
- **T063-RQ-15 — counterbalanced order:** for each probe, ADAPTIVE is first exactly twice and CONTROL is first exactly twice according to the frozen schedule below.
- **T063-RQ-16 — quality-failure continuation:** a fully measured valid `WORKER_QUALITY` FAIL is preserved and does not stop the remaining fixed schedule or invalidate the run.
- **T063-RQ-17 — absolute profile qualification:** each profile/probe requires 4/4 PASS; global profile qualification requires 12/12 PASS and intact profile/reroute evidence.
- **T063-RQ-18 — complete outcome taxonomy:** complete valid runs classify CONTROL and ADAPTIVE quality separately and always produce one non-null pilot decision from the frozen enum below.
- **T063-RQ-19 — quality-adjusted operational usage:** report total tokens/duration and tokens/duration per successful first-attempt result; failed valid attempts remain in resource numerators.
- **T063-RQ-20 — material exact-token gate:** when both profiles are globally quality qualified, exact ADAPTIVE tokens per success must improve by at least 10% to support the usage-efficiency-qualified outcome.

### MODIFIED

- **T063-RQ-1 — clean successor run:** v7 is a new homogeneous 24-arm run. V1-v6 attempts are excluded from every v7 score, metric and pilot decision.
- **T063-RQ-9 — first-attempt scoring:** valid quality failures are never rewritten, but they no longer convert a technically complete run into execution-invalid state.
- **T063-RQ-10 — model-evidence attribution:** all fully measured children are model-quality evidence; PASS children remain per-child quality-preserving efficiency eligible, while aggregate cost-per-success includes resources spent on valid FAILs.
- **T063-RQ-11 — run validity:** a run is execution-valid when all 24 scheduled child attempts complete with mandatory receipts; quality PASS/FAIL does not define run execution validity.
- **T063-RQ-13 — policy boundary:** v7 may qualify or reject the frozen routing mapping only for this calibration; R007 global policy remains an Orchestrator decision after convergence.

### PRESERVED

- **T063-RQ-2 — parent spawn receipt:** public live App Server notifications for the exact parent turn remain authoritative for spawn cardinality/correlation.
- **T063-RQ-3 — completed parent snapshot:** exact parent completion identity/final `PARENT_SPAWNED` text remain required; duplication of the live Started item remains unnecessary.
- **T063-RQ-4 — parent activity safety:** forbidden/multiple/contradictory parent activity remains fail-closed.
- **T063-RQ-6 — empty-rollout classifier:** same-child reattachment recognizes the exact authorized error family and is bounded to ten attempts.
- **T063-RQ-7 — D063 measurement:** exact child identity, permission, parent residency, configured profile, exact usage/duration and reroute receipts remain mandatory.
- **T063-RQ-8 — config-authoritative task/profile:** substantive child task and requested profile remain frozen by Stage 5 configuration; the parent is transport-only.
- **T063-RQ-12 — read-only children:** scored workers remain read-only and measurement must not mutate tracked/global product state.

## Controlling Design

### Scientific interpretation

V7 is a **fixed-n replicated qualification calibration**, not a formal statistical non-inferiority trial.

It uses repeated first-attempt observations to expose run-to-run instability and counterbalance arm order. It does not use p-values, adaptive sample expansion, outcome-conditioned reruns, or a population-level confidence claim. Four replicates are project-specific pilot policy, not an external standard.

Quality is defined by the frozen deterministic/oracle semantics. CONTROL is a comparator, not the source of truth for acceptance.

### Routing topology

```text
Stage A — already governed
    COORDINATOR_DIRECT | DELEGATED | CONTRACT_FIXED

T063 v7 scored topology
    one fixed Human-visible root
        -> fresh exact read-only parent per arm
        -> exactly one fresh exact read-only child per arm
        -> 4 replicate blocks
        -> 3 frozen probe classes per block
        -> CONTROL versus ADAPTIVE profile only
```

All scored probes are material/read-heavy `DELEGATED` units. The matched topology remains `CONTRACT_FIXED` because topology is experimentally material.

### Frozen root and child matrix

Root constant:

```text
gpt-5.6-sol / medium
```

Profiles:

```text
P1 ADAPTIVE  gpt-5.6-luna  / medium
P1 CONTROL   gpt-5.6-sol   / medium
P2 ADAPTIVE  gpt-5.6-terra / medium
P2 CONTROL   gpt-5.6-sol   / medium
P3 ADAPTIVE  gpt-5.6-terra / high
P3 CONTROL   gpt-5.6-sol   / medium
```

No profile/runtime substitution is authorized after provider-backed execution begins.

### Frozen 24-arm schedule

```text
Block 1
  P1 ADAPTIVE -> CONTROL
  P2 CONTROL  -> ADAPTIVE
  P3 ADAPTIVE -> CONTROL

Block 2
  P1 CONTROL  -> ADAPTIVE
  P2 ADAPTIVE -> CONTROL
  P3 CONTROL  -> ADAPTIVE

Block 3
  P1 ADAPTIVE -> CONTROL
  P2 CONTROL  -> ADAPTIVE
  P3 ADAPTIVE -> CONTROL

Block 4
  P1 CONTROL  -> ADAPTIVE
  P2 ADAPTIVE -> CONTROL
  P3 CONTROL  -> ADAPTIVE
```

Each scheduled arm uses a fresh App Server and child. Mutable session state is not shared between trials. Immutable frozen source/oracle input may be reused.

### Config-authoritative child contract

Before each measurement parent acts, the published Stage 5 candidate fixes substantive worker task and requested model/reasoning in App Server configuration. The parent may trigger exactly one child but does not select task semantics, model or reasoning.

Public child correlation uses only public App Server item notifications:

```text
subAgentActivity(kind=Started, agentThreadId=<exact child>)
```

Internal/raw response events are not passing evidence.

### Public live parent window

For each exact parent turn, capture public `item/started` and `item/completed` notifications beginning immediately before parent `turn/start`.

Filter to exact parent thread/turn. Deduplicate Started `subAgentActivity` representations by public item ID. Require exactly one logical Started activity matching exact child and frozen task name; reject second/different/contradictory Started activity and forbidden parent item types.

The completed parent turn must preserve exact identity and final `PARENT_SPAWNED`, contain no forbidden activity and not contradict the live correlation. It need not duplicate the live Started item.

### Same-child reattachment barrier

After exact live child correlation, `thread/resume` may retry only the same child/params when the represented error contains all authorized empty-rollout markers:

```text
thread/resume failed:
thread-store
failed to read session metadata
rollout at
is empty
```

Each retry waits 0.2 seconds, rechecks exact parent loaded residency immediately before retry, reuses the same child and creates no new provider turn. Maximum total attempts: 10.

Any nonmatching error, parent residency loss or exhaustion blocks fail-closed.

### Probe semantics

#### P1 — exact Git evidence inventory

For the frozen six-file set, return exact path, Git blob SHA, byte size from Git object metadata and frozen-HEAD existence. PASS requires exact oracle equality.

#### P2 — static dependency/symbol map

A dependency edge is only a static Python AST import edge between frozen in-scope source files. PASS requires exact edge-set equality, correct acyclicity and exact ownership of all six frozen symbols.

#### P3 — adversarial independent review

Use the published immutable runtime fixture containing exactly one frozen high-severity fail-open authority/profile defect. PASS requires detection of that defect, correct mechanism/severity/proof direction/minimal fix direction and no invented material finding.

Frozen source/oracle baseline:

```text
69e910f329a2294c3b40df0f6ee983f9905f4677
```

### First-attempt and continuation semantics

Each scheduled arm has one quality attempt.

A valid quality FAIL:

- remains `execution_validity=VALID`;
- has `failure_domain=WORKER_QUALITY`;
- remains model-quality evidence;
- is per-child efficiency-ineligible;
- does not stop the schedule;
- does not authorize a replacement or compensating scored call.

A measurement/profile/runtime/permission/oracle-validity failure is not a quality result. It blocks the run and prevents compensating scored calls.

### Absolute quality qualification

Per profile/probe:

```text
QUALITY_QUALIFIED     = 4/4 first-attempt PASS
QUALITY_NOT_QUALIFIED = 0-3/4 first-attempt PASS
```

Global profile status:

```text
ADAPTIVE_QUALITY_QUALIFIED = all three ADAPTIVE probes 4/4 + no reroute/profile-integrity defect
CONTROL_QUALITY_QUALIFIED  = all three CONTROL probes 4/4 + no reroute/profile-integrity defect
```

Per-probe pair outcome is exactly one of:

```text
BOTH_QUALIFIED
ADAPTIVE_ONLY_QUALIFIED
CONTROL_ONLY_QUALIFIED
NEITHER_QUALIFIED
```

CONTROL quality failure never changes a complete valid run into `EXECUTION_INVALID`.

### Efficiency metrics

For each probe/profile and globally record:

```text
pass_count
total_tokens
total_duration
tokens_per_success   = total_tokens / pass_count when pass_count > 0
duration_per_success = total_duration / pass_count when pass_count > 0
```

Valid failed attempts remain in resource numerators.

Accepted-quality exact usage comparison is made only when both global profiles are quality qualified. The v7 material exact-token improvement floor is 10%:

```text
exact_token_improvement = 1 - (adaptive_tokens_per_success / control_tokens_per_success)
```

`>= 0.10` is material usage improvement for this pilot; `< 0.10` is not.

Provider dollar/credit rates may be recorded descriptively but are not normative qualification constants and must not be presented as exact billed cost without complete billing telemetry.

### Complete pilot decision taxonomy

For a complete 24-arm execution-valid run, `pilot_decision` MUST be non-null and is exactly one of:

- `QUALIFIED_PROFILE_AND_USAGE_EFFICIENCY` — ADAPTIVE 12/12; CONTROL 12/12; frozen lower-tier ADAPTIVE profiles resolve exactly with no reroute; no safety/authority/oracle/rework disqualifier; exact token improvement `>=10%`.
- `QUALIFIED_PROFILE_ROUTING_ONLY` — ADAPTIVE 12/12; CONTROL 12/12; frozen lower-tier ADAPTIVE profiles resolve exactly with no reroute; exact token improvement `<10%`.
- `ADAPTIVE_QUALITY_QUALIFIED_CONTROL_DEFICIENT` — ADAPTIVE 12/12 with intact profiles; CONTROL is not globally quality qualified. No accepted-baseline efficiency claim is permitted.
- `NOT_QUALIFIED` — ADAPTIVE is not globally quality qualified or has a profile-integrity/reroute disqualifier, regardless of CONTROL.

`pilot_decision=null` is reserved only for incomplete/blocked non-quality execution.

### Run/model-evidence semantics

A complete 24-child run has:

```text
run_execution_validity = VALID
run_model_comparison_eligible = true
pilot_eligible = true
scored_child_quality_eligible_count = 24
pilot_decision != null
```

Per-child quality FAILs do not create a run-level failure domain. A blocked/incomplete run has `run_execution_validity=INVALID`, `pilot_eligible=false`, `pilot_decision=null`, and an explicit non-quality blocker domain.

## Plan & Trace

| Unit | Requirement / Design ref | Candidate artifact(s) | Required verification/evidence |
| --- | --- | --- | --- |
| inherited v3 core | RQ-2..12 | `evals/adaptive_worker_routing_v3/*`; v3 tests | D063 receipts; frozen oracles; first-attempt quality |
| inherited v4 reattach | RQ-6 | `evals/adaptive_worker_routing_v4/*`; v4 tests | exact classifier; same-child retry; residency; no new provider turn |
| inherited v5 evidence | RQ-9..11 | `evals/adaptive_worker_routing_v5/*`; v5 tests | valid FAIL model evidence; eligibility taxonomy |
| inherited v6 parent surface | RQ-2..4 | `evals/adaptive_worker_routing_v6/*`; v6 tests | live public dedupe/cardinality; completed-snapshot semantics |
| v7 replication adapter | RQ-14..20 | `evals/adaptive_worker_routing_v7/*` | 24-arm schedule; replicate metadata; aggregate/decision semantics |
| v7 conformance regressions | RQ-14..20 | `tests/test_t063_adaptive_worker_routing_v7_replication.py` | counterbalance; CONTROL-fail continuation; all decision states; run-validity semantics |
| terminal evidence | all | v7 telemetry + handoff JSON | exact 24-arm accounting or exact blocker; profile quality; efficiency; pilot decision |

## Stage ownership and candidate boundary

T063 remains D068-mode work.

```text
Stages 1-4 -> ChatGPT Orchestrator — COMPLETE by T063-R13
Stage 5    -> ChatGPT Orchestrator — REQUIRED
Stage 6    -> Agente de IA Ejecutor — NOT AUTHORIZED
Stage 7    -> ChatGPT Orchestrator
```

## Published candidate freeze

No Stage 6 candidate is yet authorized.

```text
candidate_branch: test/t063-adaptive-worker-routing-requalification-v7
candidate_head:   NOT_YET_PUBLISHED
candidate_base:   POST_DESIGN_DEVELOP_HEAD_TO_BE_FROZEN_AT_STAGE5
```

Stage 5 must materialize the complete v7 adapter and deterministic regressions, publish the exact candidate, then this section must be updated and readiness-reviewed before Human launch.

## Authorized scope

No provider-backed Stage 6 execution is currently authorized.

During future authorized Stage 6, the Executor may only:

- establish the exact published candidate;
- execute provider-free preflight/test/compile/lint gates;
- execute the published fixed 24-arm evaluation;
- diagnose failures and make only bounded represented mechanics-preserving repairs explicitly allowed by the later readiness authority;
- persist authorized non-Markdown telemetry/handoff evidence.

## Explicit exclusions

The Executor MUST NOT:

- edit/commit Markdown;
- redesign T063 or change this Task Contract;
- change frozen probes/oracles/task messages;
- change replicate count, schedule, profile matrix, thresholds or decision taxonomy;
- stop or rerun because of a valid quality FAIL;
- reuse v1-v6 attempts as v7 score data;
- silently rerun/replace a consumed v7 quality result;
- infer backend-served identity beyond D063;
- use internal/raw response events as passing evidence;
- weaken exact live parent/child correlation or permit multiple spawned children;
- create substantial private/ephemeral controller, harness, fixture generator, oracle/grader, lifecycle controller or telemetry system absent from the candidate;
- decide the global R007 routing policy.

## Invariants / constraints

- native Windows execution;
- Codex runtime/App Server pin remains exactly `0.153.4` unless D077 authority changes prospectively before execution;
- auth category `chatgpt`;
- children and measurement parents remain exact read-only;
- fresh App Server per scored arm;
- no tracked/global mutation attributable to measurement;
- no historical evidence enters v7 scoring;
- no provider call before provider-free deterministic gates pass;
- no outcome-conditioned sample extension or early success stopping.

## Executor process autonomy

Inside a future authorized Stage 6 envelope, the Executor owns mechanics and private execution organization under D041/D054. This Task Contract controls experiment semantics, profiles, schedule, evidence and stop conditions; private process autonomy cannot change them.

## D076 executable-materialization boundary

```text
small mechanical execution aid
    -> Stage 6 may create/use it

substantial new controller/harness/script/fixture-oracle implementation
    -> STOP
    -> Orchestrator Stage 5 re-entry
```

Required terminal audit fields:

```text
ephemeral_artifacts: [...]
executor_material_ephemeral_artifacts: []
```

## Acceptance criteria

- **AC-T063-1:** exact v7 candidate identity, runtime/profile and all provider-free gates pass before first provider call.
- **AC-T063-2:** one clean v7 run executes exactly the frozen 24-arm schedule unless a non-quality validity blocker stops it; v1-v6 are excluded.
- **AC-T063-3:** every persisted scored child satisfies complete D063 receipts and remains read-only.
- **AC-T063-4:** P1/P2/P3 preserve frozen deterministic/oracle semantics without leakage.
- **AC-T063-5:** live parent-window and completed-parent semantics remain exactly v6-qualified.
- **AC-T063-6:** same-child reattachment remains bounded and separately counted without new provider turns.
- **AC-T063-7:** valid quality FAILs are retained, do not stop the schedule, do not make the run execution-invalid and are never replaced.
- **AC-T063-8:** complete valid runs compute per-probe/global quality states, quality-adjusted operational metrics and exactly one frozen non-null pilot decision.
- **AC-T063-9:** CONTROL quality deficiency produces `ADAPTIVE_QUALITY_QUALIFIED_CONTROL_DEFICIENT` when ADAPTIVE is 12/12, not `BLOCKED_EXECUTION_INVALID`.
- **AC-T063-10:** exact-token usage qualification is claimed only when both profiles are 12/12 and the predeclared 10% materiality floor is met.
- **AC-T063-11:** no score rewriting, compensating provider calls, profile substitution, oracle leakage, D076 violation or tracked/global mutation occurs.
- **AC-T063-12:** telemetry/handoff persist exact trial/replicate identity, provider/reattachment accounting, profile quality state, metrics and decision/blocker.

## Verification and trace requirements

Orchestrator-owned semantic/conformance assets:

- frozen P1/P2/P3 oracle construction/scoring;
- inherited v4 reattachment regression tests;
- inherited v5 model-evidence tests;
- inherited v6 parent-surface tests;
- new v7 schedule/taxonomy/aggregate conformance tests.

Future Stage 6 must execute and technically review all designated assets before provider calls where feasible, plus compile/lint/preflight gates.

Required v7 evidence includes:

- exact provider-free verification results;
- one telemetry item for every fully measured scheduled child;
- replicate block/index and sequence identity;
- requested/resolved profiles and reroute evidence;
- exact token/duration evidence;
- per-probe pass counts and pair taxonomy;
- global ADAPTIVE/CONTROL quality status;
- tokens/duration per success;
- exact 10% token-improvement calculation when eligible;
- run execution/model-comparison/pilot eligibility;
- mutation/oracle-leak/D076 audit;
- final technical review summary.

## Code Review & Verify obligations

Before terminal completion/block, the Executor must review represented candidate/repair state against this Task Contract and verify:

- no Stage 6 repair changed experiment semantics;
- inherited v4/v5/v6 semantics remain intact;
- v7 schedule is exactly 24 arms and counterbalanced;
- valid quality FAILs do not trigger early stop/replay;
- decision taxonomy matches this contract exactly;
- terminal evidence satisfies `docs/EXECUTOR-HANDOFFS.md`.

## Stop / escalation / SDD re-entry conditions

STOP rather than guess when any of these occurs:

- candidate/base/branch identity cannot be established safely;
- a material requirement, Design, Plan/Trace or acceptance defect/ambiguity is discovered;
- a semantic oracle appears defective;
- required runtime/model/reasoning profile cannot resolve exactly;
- mandatory D063 receipt is unavailable;
- live parent surface cannot be represented under v6 semantics;
- same-child retry barrier exhausts or parent residency is lost;
- a D076-material executable artifact is missing;
- a bounded repair would change approved semantics/Design;
- a newer stable Codex release requires D077 re-entry;
- safety/security/permission/reproducibility invariant cannot be satisfied.

A valid `WORKER_QUALITY` FAIL is explicitly **not** a stop condition.

## Version-sensitive launch gate

Current design-time state remains:

```text
qualified pin:           Codex/App Server 0.153.4
last reviewed stable:    0.154.0
last reviewed prerelease:0.155.0-alpha.3.9
disposition:             PIN_RETAINED at v6 convergence
```

Stage 5/readiness MUST revalidate current upstream state. A materially new stable release requires D077 relevance classification before Stage 6 authorization.

## Expected handoff / evidence

Future authorized Executor must persist:

```text
handoffs/T063-adaptive-worker-routing-telemetry-v7.json
handoffs/T063-executor-handoff-v7.json
```

Do not persist private chain-of-thought.

## Terminal return shape

When Stage 6 is later authorized, return exactly:

```text
STATUS: COMPLETED | BLOCKED
HANDOFF: handoffs/T063-executor-handoff-v7.json
BRANCH: test/t063-adaptive-worker-routing-requalification-v7
HEAD: <actual remote pushed HEAD>
```

## Human launch gate

```text
launch_state: NOT_AUTHORIZED
```

No Human/Codex launch prompt is valid yet. Stage 5 candidate materialization and a fresh readiness review are required first.

## Thin transport invariant

When launch is eventually authorized, the Human-visible transport prompt must remain bootstrap-only: coordinator identity, repository, Task Contract pointer and exact authorized candidate identity. It must not duplicate the 24-arm schedule, scoring, retry, acceptance or evidence semantics already persisted here.