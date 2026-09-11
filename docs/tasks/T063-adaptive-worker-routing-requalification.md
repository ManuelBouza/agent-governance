# T063 — Adaptive Worker Routing Requalification

## Identity

- Task ID: `T063`
- Status: `READY / AUTHORIZED_AWAITING_HUMAN_START`
- Type: `read-only matched-arm Executor/subagent evaluation`
- SDD profile: `ASSURED`
- Base branch: `develop`
- Expected topic branch: `test/t063-adaptive-worker-routing-requalification-v6`
- Expected executor handoff: `handoffs/T063-executor-handoff-v6.json`
- Expected telemetry: `handoffs/T063-adaptive-worker-routing-telemetry-v6.json`
- Test-Authorship-Mode: `orchestrator-conformance`
- Owner: ChatGPT Orchestrator (specification/oracle/acceptance and D068 Stage 5) / Agente de IA Ejecutor (Stage 6 execution/evidence) / Human Owner (final authority and Human-mediated launch)
- Current launch review: `docs/reviews/T063-R11.md`
- Measurement authority: `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md`
- Delegation authority: `docs/decisions/D065-semantic-executor-delegation-obligation.md`
- Routing gate authority: `docs/decisions/D075-coordinator-direct-execution-gate.md`
- Materialization boundary: `docs/decisions/D076-stage6-ephemeral-executable-materialization-boundary.md`
- Version authority: `docs/decisions/D077-version-sensitive-upstream-revalidation.md`

## Objective

Run one clean six-arm evaluation to determine whether task-adaptive **delegated worker** compute profiles can preserve first-attempt quality while reducing configured compute and/or exact attributable usage relative to root-equivalent controls.

T063 evaluates Stage B worker compute routing only. Delegation-worthiness is fixed by D075/D065 and is not an experimental variable. This Task Contract does not adopt a global adaptive routing policy.

## Current specification carrier / controlling references

The smallest controlling set is:

- `AGENTS.md`;
- this Task Contract;
- `docs/reviews/T063-R10.md`;
- `docs/reviews/T063-R11.md`;
- `docs/research/R021-T063-V3-CONFIG-AUTHORITATIVE-WORKER-RECEIPTS.md`;
- `docs/research/R022-T063-V3-EMPTY-ROLLOUT-REATTACH-RACE.md`;
- `docs/research/R023-T063-V5-LIVE-SPAWN-RECEIPT-PERSISTENCE-GAP.md`;
- D063, D065, D075, D076 and D077.

Historical T063 v1/v2/v3/v4/v5 reviews, handoffs and telemetry are provenance only and MUST NOT be reused for v6 scoring.

## Requirement / specification delta

### MODIFIED

- **T063-RQ-1 — clean successor run:** v6 is a new homogeneous six-arm run. Consumed v1/v2/v3/v4/v5 attempts are historical and excluded from every v6 score, metric and pilot decision.
- **T063-RQ-2 — parent spawn receipt:** public live App Server notifications for the exact parent turn are authoritative for spawn cardinality/correlation. Exactly one unique logical `subAgentActivity(kind=Started)` item must be observed; `item/started` and `item/completed` notifications for the same item ID are one logical activity.
- **T063-RQ-3 — completed parent snapshot:** `turn/completed` must preserve exact parent-turn identity and final `PARENT_SPAWNED` text and must not contradict the live correlation. The already-observed live `Started` item is **not** required to be duplicated in the completed snapshot.
- **T063-RQ-4 — parent activity safety:** the live public window and the completed snapshot must contain no forbidden parent tool/item activity; another/different live `Started` child activity blocks fail-closed.
- **T063-RQ-5 — launch continuity:** v5 `root-5` is retired after its consumed blocked run. v6 uses NEW failover root `AG | agent-governance | T063 | root-6`.

### PRESERVED

- **T063-RQ-6 — empty-rollout classifier:** same-child reattachment recognizes the exact observed family by requiring all of `thread/resume failed:`, `thread-store`, `failed to read session metadata`, `rollout at`, and `is empty`.
- **T063-RQ-7 — D063 measurement:** exact child identity, permission, parent residency, configured profile, exact usage/duration and reroute receipts remain mandatory.
- **T063-RQ-8 — config-authoritative task/profile:** substantive child task and requested child model/reasoning remain frozen by Stage 5 configuration; the parent is transport-only.
- **T063-RQ-9 — first-attempt scoring:** valid first attempts determine quality score; failures are never rewritten by reruns.
- **T063-RQ-10 — model-evidence attribution:** only fully measured scored children are model-quality evidence; blocked/unscored attempts remain model-neutral.
- **T063-RQ-11 — efficiency eligibility:** a valid PASS is eligible for quality-preserving efficiency analysis; a valid FAIL remains quality evidence but is not an efficiency-preserving observation.
- **T063-RQ-12 — read-only children:** scored workers remain read-only and measurement must not mutate tracked/global product state.
- **T063-RQ-13 — no policy adoption:** the Executor produces evidence only; R007 remains an Orchestrator decision after convergence.

## Controlling Design

### Routing topology

```text
Stage A — already governed
    COORDINATOR_DIRECT | DELEGATED | CONTRACT_FIXED

T063 scored topology
    one fixed Human-visible root
        -> one fresh exact read-only child per arm
        -> three matched probe classes
        -> CONTROL versus ADAPTIVE profile only
```

All scored probes are material/read-heavy `DELEGATED` units. The matched topology is `CONTRACT_FIXED` because topology is experimentally material.

### Config-authoritative child contract

Before the measurement parent acts, the published Stage 5 candidate fixes substantive worker task and requested compute profile in App Server configuration. The parent may trigger exactly one child but does not select task semantics, model or reasoning.

Public child correlation uses only public App Server item notifications:

```text
subAgentActivity(kind=Started, agentThreadId=<exact child>)
```

Internal experimental raw-response events are not passing evidence.

### V6 public live parent window

For each exact parent turn, capture public `item/started` and `item/completed` notifications beginning immediately before the parent `turn/start`.

Filter the window to exact:

```text
threadId == exact parent id
turnId   == exact parent turn id
```

For `subAgentActivity(kind=Started)` items:

1. require a non-empty public item `id`;
2. deduplicate `item/started` and `item/completed` by that item ID;
3. require exactly one unique logical Started activity;
4. require its `agentThreadId` to equal the already-correlated exact child;
5. require its normalized `agentPath` to equal the frozen expected task name;
6. reject a second/different Started activity;
7. reject contradictory representations of the same item ID.

The live window must also contain none of:

```text
commandExecution
fileChange
mcpToolCall
dynamicToolCall
webSearch
imageView
imageGeneration
```

The completed parent turn:

```text
must have the exact parent turn id
must provide final agent text == PARENT_SPAWNED
must contain no forbidden parent item type
must not contain a Started activity contradicting the live exact-child/task correlation
need not duplicate the already-observed live Started activity
```

This is the only material v6 measurement change relative to v5.

### Same-child reattachment barrier

After exact live child correlation, `thread/resume` may retry only the same child/params when the represented failure contains all of:

```text
thread/resume failed:
thread-store
failed to read session metadata
rollout at
is empty
```

Each retry MUST:

```text
reuse same exact child id
reuse same thread/resume parameters
wait 0.2 seconds
recheck exact parent loaded residency after the wait
if parent absent -> BLOCK
retry thread/resume for that same child
```

Maximum total `thread/resume` attempts: `10`.

The adapter MUST NOT replay `spawn_agent`, replay the parent turn, create another child, or create another provider turn. Reattachment RPC retries are adapter transport retries and MUST be counted separately from scored child attempts.

Any nonmatching error, residency loss or exhaustion blocks fail-closed.

### Model-evidence attribution

A child enters `scored_children` only after all mandatory child/parent identity, permission, residency, configured-profile, stable-turn, exact-duration, exact-token-usage, reroute, contract-receipt and oracle-leak checks complete.

For each scored child:

```text
execution_validity = VALID
model_quality_eligible = true
failure_domain = null             when result_status == PASS
failure_domain = WORKER_QUALITY   when result_status == FAIL
model_efficiency_eligible = true  only when result_status == PASS
```

A valid FAIL remains first-attempt model-quality evidence and can disqualify adaptive routing. It is not treated as a quality-preserving efficiency observation.

Attempts that fail before producing a fully measured scored-child snapshot are neither model-quality nor efficiency evidence. Their run-level blocker is classified as one of:

```text
PROFILE_RESOLUTION
MEASUREMENT_SURFACE
MEASUREMENT_ADAPTER
EXECUTION_VALIDITY
UNCLASSIFIED_EXECUTION
```

A blocked or partial run has:

```text
run_execution_validity = INVALID
run_model_comparison_eligible = false
pilot_eligible = false
```

A complete six-arm run is run-valid only when all six arms produce scored-child snapshots and the harness reaches `COMPLETED_SCORED`.

## Plan & Trace

| Unit | Requirement / Design ref | Candidate artifact(s) | Required verification/evidence |
| --- | --- | --- | --- |
| v3 core harness | T063-RQ-7..12 | `evals/adaptive_worker_routing_v3/*`; v3 harness tests | deterministic oracle construction; D063 receipts; exact scoring |
| v4 reattachment adapter | T063-RQ-6 | `evals/adaptive_worker_routing_v4/runner.py`; v4 adapter tests | exact classifier; same-child retry; residency-before-retry; bounded exhaustion |
| v5 evidence adapter | T063-RQ-1,10,11 | `evals/adaptive_worker_routing_v5/runner.py`; v5 evidence tests | quality/efficiency eligibility; run validity; blocker-domain attribution |
| v6 parent surface | T063-RQ-2..5 | `evals/adaptive_worker_routing_v6/runner.py`; `tests/test_t063_adaptive_worker_routing_v6_parent_surface.py` | live receipt dedupe/cardinality; wrong-child rejection; forbidden activity rejection; v5 regression |
| P1 | T063-RQ-7..12 | published evaluation package | exact Git evidence oracle + complete D063 receipts |
| P2 | T063-RQ-7..12 | published evaluation package | exact static-AST map oracle + complete D063 receipts |
| P3 | T063-RQ-7..12 | published evaluation package | seeded-defect review oracle + complete D063 receipts |
| terminal evidence | T063-RQ-1..13 | v6 telemetry + handoff JSON | six-arm validity, mutation audit, model-evidence attribution, scoring, pilot decision or exact blocker |

## Stage ownership and candidate boundary

T063 is D068-mode work.

```text
Stages 1-5 -> ChatGPT Orchestrator
Stage 6    -> Agente de IA Ejecutor
Stage 7    -> ChatGPT Orchestrator
```

## Published candidate freeze

Authorized Stage 6 candidate:

```text
candidate_branch: test/t063-adaptive-worker-routing-requalification-v6
candidate_head:   af2de380569285b63e33de3f53628cadcf4052b6
candidate_base:   d5ff447d3ad162ddfc8afd8baadeac67154d7a6a
```

No provider-backed call is authorized from another initial candidate HEAD.

The candidate is exactly one commit ahead of its protected-base snapshot. It promotes the accepted v3/v4/v5 executable/test package without v5 terminal evidence and adds only the v6 adapter package plus its deterministic parent-surface regression test.

The Orchestrator environment again could not clone GitHub because sandbox DNS resolution was unavailable. Static AST parsing of the new v6 Python material succeeded, but no local pytest/Ruff/compileall PASS is claimed. Stage 6 MUST execute all provider-free gates successfully before the first provider/model call.

## Authorized scope

The Executor may:

- synchronize/establish the exact authorized remote candidate safely;
- run deterministic/provider-free pre-provider checks;
- execute the published v6 evaluation;
- diagnose failures;
- make bounded represented technical repairs that preserve this Task Contract's semantics/Design;
- perform technical Code Review & Verify;
- persist and push authorized non-Markdown v6 telemetry/handoff evidence.

A bounded repair may correct candidate mechanics only. Any change to probe semantics, oracle meaning, arm order, compute matrix, live parent-surface meaning, receipt strategy, retry contract, evidence-eligibility semantics, thresholds or pilot criteria requires Orchestrator re-entry.

## Explicit exclusions

The Executor MUST NOT:

- edit/commit Markdown;
- redesign T063 or change this Task Contract;
- change frozen probe/oracle semantics or task messages;
- change requested model/reasoning matrix after scored execution begins;
- treat historical v1/v2/v3/v4/v5 results as v6 evidence;
- silently rerun/rewrite a consumed invalid scored child;
- convert an unscored execution/measurement block into model-quality evidence;
- treat a valid quality FAIL as quality-preserving efficiency evidence;
- infer backend-served identity beyond D063;
- use internal/raw response events as passing evidence;
- weaken exact live parent/child correlation or permit multiple spawned children;
- restore the v5 requirement that live `Started` activity must appear in `turn/completed`;
- create substantial private/ephemeral controller, harness, fixture generator, oracle/grader, lifecycle controller or telemetry system absent from the candidate;
- decide the global R007 routing policy.

## Invariants / constraints

### Root/runtime launch profile

The Human-facing D055 launch card is separate from the transport prompt. Frozen v6 launch profile:

```text
Executor:        Codex
Surface:         Codex Desktop / native Windows
Session:         NEW
Coordinator-ID:  AG | agent-governance | T063 | root-6
Root model:      gpt-5.6-sol
Root reasoning:  medium
Codex runtime:   exactly 0.153.4
App Server:      exactly 0.153.4
Auth category:   chatgpt
```

`root-6` is a same-work-unit failover after the consumed blocked v5 run and material adapter/Task Contract revision. It is not a concurrent second root.

The Desktop-bundled `codex.exe` may satisfy the runtime requirement when its effective version is exactly `0.153.4`; no standalone CLI installation is required merely for interface use.

### Frozen child matrix

```text
P1 ADAPTIVE  gpt-5.6-luna  / medium
P1 CONTROL   gpt-5.6-sol   / medium
P2 CONTROL   gpt-5.6-sol   / medium
P2 ADAPTIVE  gpt-5.6-terra / medium
P3 ADAPTIVE  gpt-5.6-terra / high
P3 CONTROL   gpt-5.6-sol   / medium
```

No profile/runtime substitution is authorized after provider-backed execution begins. A required profile that cannot resolve exactly is `BLOCKED_PROFILE_RESOLUTION`.

### Frozen arm order

```text
P1 ADAPTIVE -> CONTROL
P2 CONTROL  -> ADAPTIVE
P3 ADAPTIVE -> CONTROL
```

### Frozen source/oracle baseline

```text
69e910f329a2294c3b40df0f6ee983f9905f4677
```

### Historical evidence excluded from v6

```text
v1  3d8a9460988351383a90adfc6b76e2deff056504
v2  3ff745a8d29e031ca818c1bc618b15a54e0cbf2b
v3  746519abc6f159e959120f68d5c9f920d88d5797
v4  4135a13ce8daa4f6b1fcabe45063364fbbdd16f1
v5  3f9830a65a152ad595653961205e0ca52b9c5ccc
```

V5 consumed one parent turn and one child attempt. Its public exact-child correlation and same-child reattachment succeeded, but it produced no valid scored child because of the completed-snapshot duplication assumption. It remains historical measurement evidence only.

## Executor process autonomy

Inside the authorized Stage 6 envelope, the Executor owns mechanics and private execution organization under D041/D054, including CLI/API/SDK/shell choices and compatible native tools/workers.

This Task Contract defines what, bounds, invariants, evidence and stop conditions. It does not prescribe private Executor topology unless that topology is experimentally or safety-material.

## Probe semantics

### P1 — exact Git evidence inventory

For the frozen six-file set, each child returns exact path, Git blob SHA, byte size from Git object metadata and frozen-HEAD existence. PASS requires exact equality with the deterministic repository-owned oracle and exact frozen HEAD identity.

### P2 — static dependency/symbol map

`dependency edge` means only a static Python AST import edge between frozen in-scope source files. Dynamic/bootstrap/package-discovery/runtime-cache relationships and external imports are excluded. The child returns exact internal edge set, acyclicity and owners for the frozen six symbols. PASS requires exact oracle equality.

### P3 — adversarial independent review

Use the published semantic fixture generator to place one fresh runtime fixture outside the repository/worktree and outside Windows system temp. The location must be fresh and readable by the qualified read-only child. The fixture contains exactly one frozen material defect. PASS requires detection of that defect, correct mechanism/severity, proof direction and minimal fix direction without invented material findings.

If P3 prepared input is unreadable, execution is invalid; do not rewrite/rerun a consumed first attempt without new durable authority.

## D063 measurement requirements

Every valid scored child requires:

```text
real exact parent/child correlation from public live subAgentActivity
parent activePermissionProfile.id == :read-only
non-contradictory legacy read-only projection
continuous loaded-parent residency before/through child reattachment
child parentThreadId == exact parent
child activePermissionProfile.id == :read-only
requested child model/reasoning from frozen Stage 5 config
resolved configured child model/reasoning exact match
exact non-estimated child-turn token usage
exact child-turn duration
exact-child reroute observation
exact worker contract/task receipt
no tracked/global mutation attributable to measurement
```

Persist separately at least:

```text
requested_profile
resolved_thread_profile / resolved model+reasoning
reroute_observed
backend_served_profile_verified
```

`backend_served_profile_verified` remains `false` unless a separately qualified stronger receipt exists.

Missing mandatory evidence is a measurement/execution-validity block, not worker-quality failure.

## First-attempt scoring

First-attempt quality is the scored result. Preserve valid failures.

A valid ADAPTIVE first-attempt FAIL is model-quality evidence and makes the pilot `NOT_QUALIFIED`; it is never replaced by a retry. The v6 candidate does not authorize compensating scored reruns or diagnosis-only provider calls after a block.

No indefinite retries and no compensating provider call after a measurement/execution block.

## D076 executable-materialization boundary

Stage 6 may create/use small mechanical execution aids. Substantial new executable material absent from the published candidate requires STOP -> Orchestrator Stage 5 re-entry.

Terminal handoff MUST include:

```text
ephemeral_artifacts: [...]
executor_material_ephemeral_artifacts: []
```

Any material or uncertain late-discovered executable artifact is a re-entry condition.

## Pre-provider gates

Before the first provider/model call, Stage 6 MUST verify:

- exact candidate branch/HEAD and candidate base ancestry;
- native Windows host;
- effective Codex runtime exactly `0.153.4`;
- App Server exactly `0.153.4`;
- auth category `chatgpt`;
- no unauthorized tracked candidate changes;
- no custom/local agent-role ambiguity that could alter child instructions;
- P3 runtime-root requirements can be satisfied;
- all repository-native deterministic tests covering v3 harness, v4 adapter, v5 evidence and v6 parent-surface behavior pass;
- Python compile verification for the published eval/test candidate passes;
- repository-native lint for the changed candidate passes;
- no newer stable Codex release requiring D077 re-entry has appeared.

Any pre-provider gate failure blocks with zero new scored provider calls.

## Version-sensitive launch gate

Reviewed upstream state for v6 authority on 2026-09-11:

```text
qualified pin:              Codex/App Server 0.153.4
current stable reviewed:    0.154.0
newest observed prerelease: 0.155.0-alpha.3.9
version disposition:        PIN_RETAINED
newer stable than 0.154.0:  none at review time
```

Codex `0.154.0` retains the material live-item/history persistence distinction and does not remove the v5 blocker. The appearance of a prerelease does not extend D063 qualification or authorize runtime change.

If a stable Codex release newer than `0.154.0` appears before the first provider-backed v6 call, STOP and return to Orchestrator for D077 relevance classification. Do not independently upgrade, downgrade or substitute the experiment runtime.

## Scoring

Compute from v6 only:

```text
control_pass_count / 3
adaptive_pass_count / 3
adaptive_first_attempt_failures
adaptive_escalation_count = 0
material_false_negative_count
material_false_positive_count
profile_resolution_failures
control_exact_tokens_total
adaptive_exact_tokens_total
control_exact_duration_total
adaptive_exact_duration_total
root_rework_events_caused_by_children
reattach_resume_attempts_total
reattach_resume_retries_total
scored_child_quality_eligible_count
scored_child_efficiency_eligible_count
run_model_comparison_eligible
pilot_eligible
```

Run-level CONTROL/ADAPTIVE comparisons and a pilot decision require one complete clean six-arm run. Per-child valid quality evidence may remain informative in a partial run, but a partial run is not a matched model comparison and cannot produce a pilot decision.

## Pilot decision

Final `pilot_decision` is one of:

- `QUALIFIED` — CONTROL 3/3 and ADAPTIVE 3/3 first-attempt PASS; no adaptive material false result/profile-resolution-invalidating reroute; complete D063 receipts; exact adaptive usage lower than control or a predeclared valid configured-cost normalization demonstrates lower compute; no offsetting material root rework or safety/authority incident.
- `QUALIFIED_QUALITY_ONLY` — all quality/profile/measurement requirements pass but a valid savings/cost claim cannot be made; exact token/duration evidence still required.
- `NOT_QUALIFIED` — a valid ADAPTIVE first attempt has a material quality regression/material false result or offsetting root rework.
- `null` — run is blocked/incomplete; blocker classification is persisted separately and MUST NOT be presented as a pilot decision.

A T063 pilot decision is evidence for later R007 convergence only; it is not itself global policy.

## Acceptance criteria

- **AC-T063-1:** NEW `root-6`; exact root/runtime profile and all pre-provider gates pass before any scored execution.
- **AC-T063-2:** one clean v6 six-arm run in frozen order; v1-v5 excluded.
- **AC-T063-3:** every persisted scored child satisfies complete D063 receipts and remains read-only.
- **AC-T063-4:** P1/P2/P3 satisfy frozen deterministic/oracle semantics without leakage.
- **AC-T063-5:** live parent window contains exactly one unique Started activity matching the exact child/task; same logical item notifications are deduplicated by item ID; forbidden/multiple/contradictory parent activity blocks.
- **AC-T063-6:** completed parent snapshot need not duplicate the live Started receipt but must preserve exact completion identity/final text and must not contradict the live correlation.
- **AC-T063-7:** retry behavior is same-child/same-params only, bounded to the exact empty-rollout marker family, with parent residency checked immediately before every retry and separately counted.
- **AC-T063-8:** telemetry distinguishes valid child quality evidence from execution/measurement blocks; no unscored block is attributed as model-quality evidence.
- **AC-T063-9:** quality FAILs are retained as model-quality evidence and excluded from quality-preserving efficiency eligibility.
- **AC-T063-10:** no score rewriting, unauthorized compensating provider calls, profile substitution, oracle leakage, D076 materialization violation or tracked/global mutation.
- **AC-T063-11:** terminal handoff/telemetry are persisted and pushed with exact candidate/evidence identity and provider-call accounting.

## Verification and trace requirements

Orchestrator-owned semantic/conformance assets:

- frozen P1/P2/P3 oracle construction and scoring in the published v3 package;
- v4 exact empty-rollout/same-child retry regression tests;
- v5 model-evidence attribution tests;
- v6 live-parent-window/deduplication/forbidden-activity regression tests.

Executor Stage 6 must execute and technically review those assets, may add only bounded supplementary technical verification, and must not change semantic oracle/evidence meaning without Orchestrator re-entry.

Required evidence includes:

- deterministic provider-free test/compile/lint results before first provider call;
- exact preflight runtime/profile/permission receipts;
- one telemetry entry per fully measured scored child;
- exact provider-attempt accounting including reattachment RPC retries separately;
- live parent-surface validation outcome;
- model-evidence eligibility fields and blocker domain;
- mutation/oracle-leak/D076 audit;
- final technical review summary.

## Code Review & Verify obligations

Before terminal `COMPLETED` or `BLOCKED`, the Executor must:

- review the represented candidate/repair delta against this Task Contract;
- verify no Stage 6 repair changed experiment semantics;
- verify v4 repaired adapter behavior remains intact;
- verify v5 evidence attribution remains internally consistent;
- verify v6 live parent-surface semantics match R023/R10;
- persist all required handoff fields under `docs/EXECUTOR-HANDOFFS.md`.

## Stop / escalation / SDD re-entry conditions

STOP rather than guess when any of these occurs:

- candidate/base/branch identity cannot be established safely;
- a material requirement, Design, Plan/Trace or acceptance defect/ambiguity is discovered;
- a semantic oracle appears defective;
- a required runtime/model/reasoning profile cannot be resolved exactly;
- a mandatory D063 receipt is unavailable;
- live parent activity cannot be represented with the public notification semantics above;
- the empty-rollout condition does not match the authorized marker family;
- same-child retry barrier exhausts or parent residency is lost;
- an execution-validity error cannot be represented without changing evidence semantics;
- a D076-material executable artifact is missing from the candidate;
- a bounded repair would change approved semantics/Design;
- a newer stable Codex release requires D077 re-entry;
- a safety/security/permission/reproducibility invariant cannot be satisfied.

Persist available evidence, perform no compensating scored call, and identify the earliest affected SDD stage before returning control.

## Expected handoff / evidence

The Executor MUST persist:

```text
handoffs/T063-adaptive-worker-routing-telemetry-v6.json
handoffs/T063-executor-handoff-v6.json
```

The handoff/telemetry must capture at least:

- canonical authority and exact candidate identity;
- pre-provider verification results;
- represented Stage 6 repairs, if any;
- exact provider and reattachment-RPC accounting;
- per-child D063/profile/usage/duration/reroute/oracle results;
- live parent-surface validation evidence;
- per-child quality/efficiency eligibility;
- run-level execution validity/model-comparison/pilot eligibility;
- exact blocker/failure domain when incomplete;
- mutation/oracle-leak review;
- D076 ephemeral-artifact audit;
- final pilot decision only when a complete clean six-arm run permits one.

Do not persist private chain-of-thought.

## Terminal return shape

Return exactly:

```text
STATUS: COMPLETED | BLOCKED
HANDOFF: handoffs/T063-executor-handoff-v6.json
BRANCH: test/t063-adaptive-worker-routing-requalification-v6
HEAD: <actual remote pushed HEAD>
```

## Human launch gate

```text
launch_state: AUTHORIZED_AWAITING_HUMAN_START
```

ChatGPT MUST NOT start or directly control Codex. Human-mediated transport under D071 is required.

## Thin transport invariant

The Human-visible launch prompt is transport/bootstrap only. A compliant v6 transport contains only:

```text
Set the visible Codex chat title to exactly:
AG | agent-governance | T063 | root-6

Repository: https://github.com/ManuelBouza/agent-governance
Session: NEW
Task Contract: docs/tasks/T063-adaptive-worker-routing-requalification.md
Authorized candidate: test/t063-adaptive-worker-routing-requalification-v6@af2de380569285b63e33de3f53628cadcf4052b6

Synchronize canonical Git authority, load the repository instructions/checkpoint and the Task Contract, then execute that Task Contract exactly. Return only its defined terminal result.
```

D055 launch-profile information is presented to the Human separately. Do not duplicate matrix, parent-surface logic, retry logic, evidence schema, acceptance criteria, test runbook, version logic or stop conditions in the transport prompt.
