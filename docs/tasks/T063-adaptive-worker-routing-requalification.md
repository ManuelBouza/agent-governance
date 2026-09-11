# T063 — Adaptive Worker Routing Requalification

## Identity

- Task ID: `T063`
- Status: `READY / AUTHORIZED_AWAITING_HUMAN_START`
- Type: `read-only replicated matched-arm Executor/subagent evaluation`
- SDD profile: `ASSURED`
- Base branch: `develop`
- Expected topic branch: `test/t063-adaptive-worker-routing-requalification-v7`
- Expected executor handoff: `handoffs/T063-executor-handoff-v7.json`
- Expected telemetry: `handoffs/T063-adaptive-worker-routing-telemetry-v7.json`
- Test-Authorship-Mode: `orchestrator-conformance`
- Owner: ChatGPT Orchestrator (specification/oracle/acceptance and D068 Stage 5) / Agente de IA Ejecutor (Stage 6 execution/evidence) / Human Owner (final authority and Human-mediated launch)
- Current design review: `docs/reviews/T063-R13.md`
- Current readiness review: `docs/reviews/T063-R14.md`
- Prior convergence: `docs/reviews/T063-R12.md`
- Measurement authority: `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md`
- Delegation authority: `docs/decisions/D065-semantic-executor-delegation-obligation.md`
- Routing gate authority: `docs/decisions/D075-coordinator-direct-execution-gate.md`
- Materialization boundary: `docs/decisions/D076-stage6-ephemeral-executable-materialization-boundary.md`
- Version authority: `docs/decisions/D077-version-sensitive-upstream-revalidation.md`

## Objective

Run one clean, prospectively replicated qualification evaluation to determine whether the frozen task-adaptive delegated-worker profiles preserve absolute oracle-scored quality across repeated trials and, when root-equivalent CONTROL also meets accepted quality, whether ADAPTIVE provides material exact-token efficiency and/or a validated lower-tier routing result.

T063 evaluates Stage B worker compute routing only. Delegation-worthiness is fixed by D075/D065 and is not an experimental variable. This Task Contract does not adopt a global adaptive-routing policy.

## Current specification carrier / controlling references

Load only the smallest controlling set needed for execution:

- `AGENTS.md`;
- this Task Contract;
- `docs/reviews/T063-R13.md`;
- `docs/reviews/T063-R14.md`;
- `docs/reviews/T063-R12.md` only for v6 convergence/provenance;
- `docs/research/R021-T063-V3-CONFIG-AUTHORITATIVE-WORKER-RECEIPTS.md`;
- `docs/research/R022-T063-V3-EMPTY-ROLLOUT-REATTACH-RACE.md`;
- `docs/research/R023-T063-V5-LIVE-SPAWN-RECEIPT-PERSISTENCE-GAP.md`;
- D063, D065, D075, D076 and D077.

Historical T054/T063 v1-v6 attempts are planning/provenance evidence only and MUST NOT be reused for v7 scoring.

## Requirement / specification delta

### ADDED

- **T063-RQ-14 — fixed replication:** execute exactly four replicate blocks, giving 24 scored first-attempt children on a complete valid run.
- **T063-RQ-15 — counterbalanced order:** for each probe, ADAPTIVE runs first exactly twice and CONTROL first exactly twice according to the frozen schedule.
- **T063-RQ-16 — quality-failure continuation:** a fully measured valid `WORKER_QUALITY` FAIL is preserved, remains model-quality evidence, and does not stop the remaining fixed schedule or invalidate the run.
- **T063-RQ-17 — absolute profile qualification:** each profile/probe requires 4/4 PASS; global profile qualification requires 12/12 PASS plus intact profile/reroute evidence.
- **T063-RQ-18 — complete outcome taxonomy:** every complete valid 24-arm run produces one non-null frozen pilot decision.
- **T063-RQ-19 — quality-adjusted operational usage:** report total tokens/duration and tokens/duration per successful first-attempt result; resources spent on valid FAILs remain in numerators.
- **T063-RQ-20 — material exact-token gate:** when both profiles globally qualify, ADAPTIVE exact tokens per success must improve by at least 10% to support the usage-efficiency-qualified outcome.

### MODIFIED

- **T063-RQ-1 — clean successor run:** v7 is a new homogeneous 24-arm run; v1-v6 are excluded from every v7 score, metric and decision.
- **T063-RQ-9 — first-attempt scoring:** valid quality failures are never rewritten and no longer convert a technically complete run into execution-invalid state.
- **T063-RQ-10 — model-evidence attribution:** all fully measured children are quality evidence; PASS children remain per-child efficiency eligible while aggregate cost-per-success includes failed valid attempts.
- **T063-RQ-11 — run validity:** a run is execution-valid when all 24 scheduled children complete with mandatory receipts; quality PASS/FAIL does not define execution validity.
- **T063-RQ-13 — policy boundary:** v7 can qualify/reject only this frozen calibration mapping; R007 global policy remains an Orchestrator decision after convergence.

### PRESERVED

- **T063-RQ-2 — parent spawn receipt:** public live App Server notifications for the exact parent turn are authoritative for spawn cardinality/correlation.
- **T063-RQ-3 — completed parent snapshot:** exact completion identity/final `PARENT_SPAWNED` text remain required; the live Started item need not be duplicated in the completed snapshot.
- **T063-RQ-4 — parent activity safety:** forbidden/multiple/contradictory parent activity remains fail-closed.
- **T063-RQ-6 — empty-rollout barrier:** same-child reattachment recognizes only the exact authorized marker family and is bounded to ten attempts.
- **T063-RQ-7 — D063 measurement:** exact child identity, permission, parent residency, configured profile, exact usage/duration and reroute receipts remain mandatory.
- **T063-RQ-8 — config-authoritative task/profile:** substantive child task and requested profile remain frozen by Stage 5 configuration; the parent is transport-only.
- **T063-RQ-12 — read-only children:** scored workers remain read-only and measurement must not mutate tracked/global product state.

## Controlling Design

### Scientific interpretation

V7 is a **fixed-n replicated qualification calibration**, not a formal statistical non-inferiority trial. It uses repeated first-attempt observations to expose instability and counterbalance arm order. It does not use p-values, adaptive sample expansion, outcome-conditioned reruns, or a population-level confidence claim. Four replicates are project-specific pilot policy, not an external standard.

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

All scored probes are material/read-heavy `DELEGATED` units. The topology remains `CONTRACT_FIXED` because topology is experimentally material.

### Frozen root and child profiles

Root constant:

```text
gpt-5.6-sol / medium
```

Child matrix:

```text
P1 ADAPTIVE  gpt-5.6-luna  / medium
P1 CONTROL   gpt-5.6-sol   / medium
P2 ADAPTIVE  gpt-5.6-terra / medium
P2 CONTROL   gpt-5.6-sol   / medium
P3 ADAPTIVE  gpt-5.6-terra / high
P3 CONTROL   gpt-5.6-sol   / medium
```

No profile/runtime substitution is authorized after provider-backed execution begins. A required profile that cannot resolve exactly is a profile-resolution block, not a quality FAIL.

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

Each scheduled arm uses a fresh App Server and fresh exact child. Mutable session state is not shared between trials. Immutable frozen source/oracle input may be reused.

Each fully measured child snapshot MUST carry exact `replicate`, `sequence_index`, `within_block_index` and `trial_id` metadata from the published candidate schedule.

### Config-authoritative child contract

Before each measurement parent acts, the published Stage 5 candidate fixes substantive worker task and requested model/reasoning in App Server configuration. The parent may trigger exactly one child but does not select task semantics, model or reasoning.

Public child correlation uses only:

```text
subAgentActivity(kind=Started, agentThreadId=<exact child>)
```

Internal/raw response events are not passing evidence.

### V6-qualified public live parent window

For each exact parent turn, capture public `item/started` and `item/completed` notifications beginning immediately before `turn/start`, filter to the exact parent thread/turn, and deduplicate Started `subAgentActivity` representations by public item ID.

Require exactly one logical Started activity matching exact child and frozen task name. Reject second/different/contradictory Started activity and forbidden parent item types. The completed parent turn must preserve exact identity/final `PARENT_SPAWNED`, contain no forbidden activity and not contradict live correlation. It need not duplicate the live Started item.

### Same-child reattachment barrier

After exact live child correlation, `thread/resume` may retry only the same child/params when the failure contains all of:

```text
thread/resume failed:
thread-store
failed to read session metadata
rollout at
is empty
```

Each retry waits 0.2 seconds, rechecks exact parent loaded residency immediately before retry, reuses the same child and creates no new provider turn. Maximum total attempts: 10. Any nonmatching error, parent loss or exhaustion blocks fail-closed.

### Frozen probe semantics

**P1 — exact Git evidence inventory.** For the frozen six-file set, return exact path, Git blob SHA, byte size from Git object metadata and frozen-HEAD existence. PASS requires exact oracle equality.

**P2 — static dependency/symbol map.** A dependency edge is only a static Python AST import edge between frozen in-scope source files. PASS requires exact edge-set equality, correct acyclicity and exact ownership of all six frozen symbols.

**P3 — adversarial independent review.** Use the published runtime fixture containing exactly one frozen high-severity fail-open authority/profile defect. PASS requires detection of that defect, correct mechanism/severity/proof direction/minimal fix direction and no invented material finding.

Frozen source/oracle baseline:

```text
69e910f329a2294c3b40df0f6ee983f9905f4677
```

### First-attempt and continuation semantics

Each scheduled arm has exactly one quality attempt.

A valid quality FAIL:

```text
execution_validity = VALID
failure_domain = WORKER_QUALITY
model_quality_eligible = true
model_efficiency_eligible = false
```

It does not stop the fixed schedule and does not authorize replay/replacement/compensating scored calls. The v4 same-child reattachment retry is transport persistence handling, not another provider/model quality attempt.

Measurement/profile/runtime/permission/oracle-validity failure is not a quality result. It blocks the run without compensating scored calls.

### Absolute quality qualification

Per profile/probe:

```text
QUALITY_QUALIFIED     = 4/4 first-attempt PASS
QUALITY_NOT_QUALIFIED = 0-3/4 first-attempt PASS
```

Global profile status:

```text
ADAPTIVE_QUALITY_QUALIFIED = all three ADAPTIVE probes 4/4 + intact profile/reroute evidence
CONTROL_QUALITY_QUALIFIED  = all three CONTROL probes 4/4 + intact profile/reroute evidence
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

For each probe/profile and globally persist:

```text
attempt_count
pass_count
total_tokens
total_duration
tokens_per_success   = total_tokens / pass_count when pass_count > 0
duration_per_success = total_duration / pass_count when pass_count > 0
profile_integrity
```

Valid failed attempts remain in resource numerators.

Accepted-quality exact usage comparison is made only when both global profiles qualify. The prospective materiality floor is:

```text
exact_token_improvement = 1 - (adaptive_tokens_per_success / control_tokens_per_success)
material floor          = 0.10
```

Provider dollar/credit rates may be recorded descriptively but are not normative qualification constants and must not be presented as exact billed cost without complete billing telemetry.

### Complete pilot decision taxonomy

For a complete 24-arm execution-valid run, `pilot_decision` MUST be non-null and exactly one of:

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

Per-child quality FAILs do not create a run-level failure domain. An incomplete/blocked run has `run_execution_validity=INVALID`, `pilot_eligible=false`, `pilot_decision=null`, and an explicit non-quality blocker domain.

## Plan & Trace

| Unit | Requirement / Design ref | Candidate artifact(s) | Required verification/evidence |
| --- | --- | --- | --- |
| inherited v3 core | RQ-2..12 | `evals/adaptive_worker_routing_v3/*`; v3 tests | D063 receipts; frozen oracles; first-attempt quality |
| inherited v4 reattach | RQ-6 | `evals/adaptive_worker_routing_v4/*`; v4 tests | exact classifier; same-child retry; residency; no new provider turn |
| inherited v5 evidence | RQ-9..11 | `evals/adaptive_worker_routing_v5/*`; v5 tests | valid FAIL model evidence; eligibility taxonomy |
| inherited v6 parent surface | RQ-2..4 | `evals/adaptive_worker_routing_v6/*`; v6 tests | public live dedupe/cardinality; completed-snapshot semantics |
| v7 replication adapter | RQ-14..20 | `evals/adaptive_worker_routing_v7/*` | 24-arm schedule; trial metadata; aggregate/decision semantics |
| v7 conformance regressions | RQ-14..20 | `tests/test_t063_adaptive_worker_routing_v7_replication.py` | counterbalance; CONTROL-fail continuation; decision states; run validity |
| terminal evidence | all | v7 telemetry + handoff JSON | exact 24-arm accounting or exact blocker; profile quality; usage; pilot decision |

## Stage ownership and candidate boundary

T063 is D068-mode work.

```text
Stages 1-4 -> ChatGPT Orchestrator — COMPLETE by T063-R13
Stage 5    -> ChatGPT Orchestrator — COMPLETE by T063-R14
Stage 6    -> Agente de IA Ejecutor — AUTHORIZED after Human launch
Stage 7    -> ChatGPT Orchestrator
```

## Published candidate freeze

Authorized Stage 6 candidate:

```text
candidate_branch: test/t063-adaptive-worker-routing-requalification-v7
candidate_head:   9fb55e8f36570f6b91d0a23720ccc6a62a9d0b90
candidate_base:   a3c719ad862128e292c7313b39966fbbbe156799
```

No provider-backed call is authorized from another initial candidate HEAD. The candidate is exactly one commit ahead of its protected-base snapshot and adds 24 executable/test files: exact accepted v3-v6 package/test blobs plus the v7 adapter and conformance test. Historical terminal evidence is excluded.

A bounded Stage 6 repair may correct represented mechanics/test/config defects only when it preserves this Task Contract's frozen experiment semantics. Any change to probes, oracles, sample size, order, profiles, thresholds, parent-surface semantics, retry contract, model-evidence taxonomy, quality rules or pilot-decision meaning requires Orchestrator re-entry.

## Authorized scope

The Executor may:

- synchronize/establish the exact authorized candidate safely;
- execute all deterministic/provider-free pre-provider checks;
- execute the published fixed 24-arm v7 evaluation;
- diagnose failures;
- make bounded represented mechanics-preserving repairs explicitly allowed above;
- perform technical Code Review & Verify;
- persist and push authorized non-Markdown v7 telemetry/handoff evidence.

## Explicit exclusions

The Executor MUST NOT:

- edit/commit Markdown;
- redesign T063 or change this Task Contract;
- change frozen probes/oracles/task messages;
- change replicate count, schedule, profiles, thresholds or decision taxonomy;
- stop, replay or replace an arm because of a valid quality FAIL;
- reuse v1-v6 attempts as v7 score data;
- infer backend-served identity beyond D063;
- use internal/raw response events as passing evidence;
- weaken exact live parent/child correlation or permit multiple spawned children;
- replay the measurement parent or create compensating provider calls after a validity block;
- create substantial private/ephemeral controller, harness, fixture generator, oracle/grader, lifecycle controller or telemetry system absent from the published candidate;
- decide the global R007 routing policy.

## Invariants / constraints

### Root/runtime launch profile

The Human-facing D055 launch card is separate from the transport prompt. Frozen v7 launch profile:

```text
Executor:        Codex
Surface:         Codex Desktop / native Windows
Session:         NEW
Coordinator-ID:  AG | agent-governance | T063 | root-7
Root model:      gpt-5.6-sol
Root reasoning:  medium
Codex runtime:   exactly 0.153.4
App Server:      exactly 0.153.4
Auth category:   chatgpt
```

V6 `root-6` is retired after its consumed run and material successor redesign. `root-7` is a same-work-unit failover, not a concurrent second root.

Other invariants:

- native Windows host;
- fresh App Server per scored arm;
- exact read-only parent/child permission posture;
- no tracked/global mutation attributable to measurement;
- no historical evidence enters v7 scoring;
- no provider call before every provider-free gate passes;
- no outcome-conditioned sample extension or early-success stopping.

## Executor process autonomy

Inside the authorized Stage 6 envelope, the Executor owns mechanics and private execution organization under D041/D054. This Task Contract controls experiment semantics, profiles, schedule, evidence and stop conditions; private process autonomy cannot change them.

## D076 executable-materialization boundary

```text
small mechanical execution aid
    -> Stage 6 may create/use it

substantial new controller/harness/script/fixture-oracle implementation
    -> STOP
    -> Orchestrator Stage 5 re-entry
```

Terminal handoff MUST include:

```text
ephemeral_artifacts: [...]
executor_material_ephemeral_artifacts: []
```

Any material or uncertain late-discovered executable artifact requires re-entry.

## Pre-provider gates

Before the first provider/model call, Stage 6 MUST verify successfully:

- exact candidate branch/HEAD and base ancestry;
- native Windows host;
- effective Codex runtime exactly `0.153.4`;
- App Server exactly `0.153.4`;
- auth category `chatgpt`;
- no unauthorized tracked candidate changes;
- no custom/local agent-role ambiguity that could alter child instructions;
- P3 runtime-root requirements can be satisfied;
- all repository-native deterministic tests covering v3-v7 pass;
- Python compile verification for the published eval/test candidate passes;
- repository-native Ruff/lint verification for the changed candidate passes;
- provider-free P1/P2/P3 oracle preparation passes;
- no newer stable Codex release requiring D077 re-entry has appeared.

The Orchestrator readiness environment could not perform repository-native pytest/Ruff/compileall because its sandbox could not resolve GitHub and did not contain Ruff. Those gates are therefore mandatory Stage 6 preconditions, not optional duplicate checks.

Any pre-provider gate failure returns `BLOCKED` with zero new scored provider calls.

## Acceptance criteria

- **AC-T063-1:** exact v7 candidate/runtime/profile and all provider-free gates pass before first provider call.
- **AC-T063-2:** one clean v7 run executes exactly the frozen 24-arm schedule unless a non-quality validity blocker stops it; v1-v6 are excluded.
- **AC-T063-3:** every persisted scored child satisfies complete D063 receipts and remains read-only.
- **AC-T063-4:** P1/P2/P3 preserve frozen deterministic/oracle semantics without leakage.
- **AC-T063-5:** live parent-window and completed-parent semantics remain exactly v6-qualified.
- **AC-T063-6:** same-child reattachment remains bounded/separately counted and never creates a new provider turn.
- **AC-T063-7:** valid quality FAILs are retained, do not stop the schedule, do not make the run execution-invalid and are never replaced.
- **AC-T063-8:** complete valid runs compute per-probe/global quality states, quality-adjusted usage metrics and exactly one frozen non-null pilot decision.
- **AC-T063-9:** ADAPTIVE 12/12 with deficient CONTROL yields `ADAPTIVE_QUALITY_QUALIFIED_CONTROL_DEFICIENT`, not an execution-validity block.
- **AC-T063-10:** exact-token usage qualification is claimed only when both profiles are 12/12 and the predeclared 10% materiality floor is met.
- **AC-T063-11:** no score rewriting, compensating provider calls, profile substitution, oracle leakage, D076 violation or tracked/global mutation occurs.
- **AC-T063-12:** telemetry/handoff persist exact trial/replicate identity, provider/reattachment accounting, quality states, usage metrics and decision/blocker.

## Verification and trace requirements

Orchestrator-owned semantic/conformance assets:

- frozen P1/P2/P3 oracle construction/scoring;
- inherited v4 reattachment regression tests;
- inherited v5 model-evidence tests;
- inherited v6 parent-surface tests;
- v7 schedule/taxonomy/aggregate conformance tests.

Stage 6 MUST execute and technically review those assets plus all pre-provider gates.

Required terminal evidence includes:

- provider-free verification results;
- one telemetry item per fully measured scheduled child;
- replicate block/index/trial identity;
- requested/resolved profiles and reroute evidence;
- exact token/duration evidence;
- per-probe PASS counts/pair taxonomy;
- global ADAPTIVE/CONTROL quality status;
- tokens/duration per success;
- exact 10% token-improvement calculation when eligible;
- run execution/model-comparison/pilot eligibility;
- exact provider-attempt and reattachment-RPC accounting;
- mutation/oracle-leak/D076 audit;
- final technical review summary.

## Code Review & Verify obligations

Before terminal `COMPLETED` or `BLOCKED`, the Executor must:

- review the represented candidate/repair delta against this Task Contract;
- verify no Stage 6 repair changed experiment semantics;
- verify inherited v4/v5/v6 behavior remains intact;
- verify v7 schedule is exactly 24 arms and counterbalanced;
- verify valid quality FAILs do not trigger early stop/replay;
- verify decision taxonomy matches this contract exactly;
- persist handoff evidence required by `docs/EXECUTOR-HANDOFFS.md`.

## Stop / escalation / SDD re-entry conditions

STOP rather than guess when any of these occurs:

- candidate/base/branch identity cannot be established safely;
- a material requirement, Design, Plan/Trace or acceptance defect/ambiguity is discovered;
- a semantic oracle appears defective;
- required runtime/model/reasoning profile cannot resolve exactly;
- a mandatory D063 receipt is unavailable;
- live parent activity cannot be represented under v6-qualified public semantics;
- the empty-rollout failure does not match the authorized marker family;
- same-child retry exhausts or parent residency is lost;
- a D076-material executable artifact is missing from the candidate;
- a bounded repair would change approved semantics/Design;
- a newer stable Codex release requires D077 re-entry;
- a safety/security/permission/reproducibility invariant cannot be satisfied.

A valid `WORKER_QUALITY` FAIL is explicitly **not** a stop condition.

Persist available evidence, make no compensating scored call, and identify the earliest affected SDD stage before returning control.

## Version-sensitive launch gate

Reviewed upstream state on 2026-09-11 after v7 candidate publication:

```text
qualified pin:              Codex/App Server 0.153.4
current stable reviewed:    0.154.0
newest observed prerelease: 0.155.0-alpha.3.9
version disposition:        PIN_RETAINED
newer stable than 0.154.0:  none at review time
```

D063 qualification is not automatically extended to later releases. If a stable Codex release newer than `0.154.0` appears before the first v7 provider-backed call, STOP and return to Orchestrator for D077 relevance classification. Do not independently upgrade/downgrade/substitute the runtime.

## Expected handoff / evidence

The Executor MUST persist:

```text
handoffs/T063-adaptive-worker-routing-telemetry-v7.json
handoffs/T063-executor-handoff-v7.json
```

The evidence must capture at least canonical authority/candidate identity, pre-provider verification, represented Stage 6 repairs, exact provider/reattachment accounting, per-child receipts/results, replicate metadata, profile-quality/usage aggregates, model-evidence eligibility, blocker or pilot decision, mutation/oracle-leak review, and D076 ephemeral-artifact audit.

Do not persist private chain-of-thought.

## Terminal return shape

Return exactly:

```text
STATUS: COMPLETED | BLOCKED
HANDOFF: handoffs/T063-executor-handoff-v7.json
BRANCH: test/t063-adaptive-worker-routing-requalification-v7
HEAD: <actual remote pushed HEAD>
```

## Human launch gate

```text
launch_state: AUTHORIZED_AWAITING_HUMAN_START
```

ChatGPT MUST NOT start or directly control Codex. Human-mediated transport is required.

## Thin transport invariant

The Human-visible launch prompt is transport/bootstrap only. A compliant v7 transport contains only:

```text
Set the visible Codex chat title to exactly:
AG | agent-governance | T063 | root-7

Repository: https://github.com/ManuelBouza/agent-governance
Session: NEW
Task Contract: docs/tasks/T063-adaptive-worker-routing-requalification.md
Authorized candidate: test/t063-adaptive-worker-routing-requalification-v7@9fb55e8f36570f6b91d0a23720ccc6a62a9d0b90

Synchronize canonical Git authority, load the repository instructions/checkpoint and the Task Contract, then execute that Task Contract exactly. Return only its defined terminal result.
```

D055 launch-profile information is presented separately. Do not duplicate schedule, scoring, retry, acceptance, test runbook or evidence semantics in the transport prompt.
