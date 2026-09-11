# T063 — Adaptive Worker Routing Requalification

## Identity

- Task ID: `T063`
- Status: `READY / AUTHORIZED_AWAITING_HUMAN_START`
- Type: `read-only matched-arm Executor/subagent evaluation`
- SDD profile: `ASSURED`
- Base branch: `develop`
- Expected topic branch: `test/t063-adaptive-worker-routing-requalification-v4`
- Expected executor handoff: `handoffs/T063-executor-handoff-v4.json`
- Expected telemetry: `handoffs/T063-adaptive-worker-routing-telemetry-v4.json`
- Test-Authorship-Mode: `orchestrator-conformance`
- Owner: ChatGPT Orchestrator (specification/oracle/acceptance and D068 Stage 5) / Agente de IA Ejecutor (Stage 6 execution/evidence) / Human Owner (final authority and Human-mediated launch)
- Current launch review: `docs/reviews/T063-R8.md`
- Measurement authority: `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md`
- Version authority: `docs/decisions/D077-version-sensitive-upstream-revalidation.md`
- Materialization boundary: `docs/decisions/D076-stage6-ephemeral-executable-materialization-boundary.md`

## Objective

Run one clean six-arm evaluation to determine whether task-adaptive **delegated worker** compute profiles can preserve first-attempt quality while reducing configured compute and/or exact attributable usage relative to root-equivalent controls.

T063 evaluates Stage B worker compute routing only. Delegation-worthiness is fixed by D075/D065 and is not an experimental variable. This Task Contract does not adopt a global adaptive routing policy.

## Current specification carrier / controlling references

The minimum controlling set is:

- `AGENTS.md`;
- this Task Contract;
- `docs/reviews/T063-R8.md`;
- `docs/research/R021-T063-V3-CONFIG-AUTHORITATIVE-WORKER-RECEIPTS.md`;
- `docs/research/R022-T063-V3-EMPTY-ROLLOUT-REATTACH-RACE.md`;
- D063, D075, D076 and D077.

Historical T063 reviews/evidence remain provenance only and MUST NOT be used for v4 scoring.

## Requirement / specification delta

### MODIFIED

- **T063-RQ-1 — authoritative execution carrier:** all active v4 execution semantics now reside in this Task Contract and its referenced canonical Git authority. The Human-visible launch prompt is transport/bootstrap only.
- **T063-RQ-2 — child reattachment:** after public `subAgentActivity(kind=Started, agentThreadId=<child>)` correlation, exact-child `thread/resume` may retry only the same child/params for the exact empty-rollout persistence failure class under the bounded barrier defined below.
- **T063-RQ-3 — clean restart:** v4 is a new homogeneous six-arm run. Consumed v1/v2/v3 attempts are historical and excluded from every v4 score/metric/pilot decision.

### PRESERVED

- **T063-RQ-4 — D063 measurement:** exact child identity, permission, parent residency, configured profile, exact usage/duration and reroute receipts remain mandatory.
- **T063-RQ-5 — config-authoritative task/profile:** substantive child task and requested child model/reasoning remain frozen by Stage 5 configuration; the parent is transport-only.
- **T063-RQ-6 — first-attempt scoring:** valid first attempts determine quality score; failures are never rewritten by reruns.
- **T063-RQ-7 — read-only children:** scored workers remain read-only and measurement must not mutate tracked/global product state.
- **T063-RQ-8 — no policy adoption:** the Executor produces evidence only; R007 remains an Orchestrator decision after convergence.

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

Public child correlation uses:

```text
subAgentActivity(kind=Started, agentThreadId=<exact child>)
```

Internal experimental raw-response events are not passing evidence.

### V4 same-child reattachment barrier

The v3 failure was a persistence-visibility race: public child-start correlation could arrive before persisted rollout metadata was readable by `thread/resume`.

V4 may retry `thread/resume` only when the exact represented failure is the empty-rollout thread-store class. Each retry MUST:

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

## Plan & Trace

| Unit | Requirement / Design ref | Candidate artifact(s) | Required evidence |
| --- | --- | --- | --- |
| V4 adapter | T063-RQ-2 | `evals/adaptive_worker_routing_v4/runner.py`; v4 adapter tests | bounded same-child retry behavior; exact retry count; residency-before-retry evidence |
| P1 | T063-RQ-4..7 | published v3 evaluation package reused in v4 candidate | exact Git evidence oracle + complete D063 receipts |
| P2 | T063-RQ-4..7 | published v3 evaluation package reused in v4 candidate | exact static-AST map oracle + complete D063 receipts |
| P3 | T063-RQ-4..7 | published v3 evaluation package reused in v4 candidate | seeded-defect review oracle + complete D063 receipts |
| terminal evidence | T063-RQ-1..8 | v4 telemetry + handoff JSON | six-arm validity, mutation audit, scoring, pilot decision or exact blocker |

## Stage ownership and published candidate freeze

T063 is D068-mode work.

```text
Stages 1-5 -> ChatGPT Orchestrator
Stage 6    -> Agente de IA Ejecutor
Stage 7    -> ChatGPT Orchestrator
```

Authorized Stage 6 candidate:

```text
candidate_branch: test/t063-adaptive-worker-routing-requalification-v4
candidate_head:   f06c8f48f7b1d59dff9fc117cca5b42453ad23e8
candidate_base:   9da2b6fed64ded9af8d38f67cd53cd066abef838
```

No provider-backed call is authorized from another initial candidate HEAD.

The candidate contains the repaired v3 executable evaluation package plus the v4 reattachment adapter/tests. No new substantial harness/controller/oracle may be created privately in Stage 6.

## Authorized Stage 6 scope

The Executor may:

- synchronize/establish the exact authorized remote candidate safely;
- run deterministic pre-provider checks;
- execute the published v4 evaluation;
- diagnose failures;
- make bounded represented technical repairs that preserve this Task Contract's semantics/Design;
- perform technical Code Review & Verify;
- persist and push authorized non-Markdown v4 telemetry/handoff evidence.

A bounded technical repair may correct candidate mechanics only. Any change to probe semantics, oracle meaning, arm order, compute matrix, receipt strategy, retry contract, thresholds or pilot criteria requires Orchestrator re-entry.

## Explicit exclusions

The Executor MUST NOT:

- edit/commit Markdown;
- redesign T063 or change this Task Contract;
- change frozen probe/oracle semantics or task messages;
- change the requested model/reasoning matrix after scored execution begins;
- treat historical v1/v2/v3 results as v4 evidence;
- silently rerun/rewrite a consumed invalid scored child;
- infer backend-served identity beyond D063;
- use internal raw-response events as passing evidence;
- create substantial private/ephemeral controller, harness, fixture generator, oracle/grader, lifecycle controller or telemetry system absent from the candidate;
- decide the global R007 routing policy.

## Invariants / constraints

### Root/runtime launch profile

The Human-facing D055 launch card is separate from the transport prompt. Current frozen launch profile:

```text
Executor:        Codex
Surface:         Codex Desktop / native Windows
Session:         NEW
Coordinator-ID:  AG | agent-governance | T063 | root-4
Root model:      gpt-5.6-sol
Root reasoning:  medium
Codex runtime:   exactly 0.153.4
App Server:      exactly 0.153.4
Auth category:   chatgpt
```

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

### Historical evidence excluded from v4

```text
v1  3d8a9460988351383a90adfc6b76e2deff056504
v2  3ff745a8d29e031ca818c1bc618b15a54e0cbf2b
v3  746519abc6f159e959120f68d5c9f920d88d5797
```

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
real exact parent/child correlation
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
no tracked/global mutation attributable to measurement
```

Persist separately at least:

```text
requested_profile
resolved_thread_profile
reroute_observed
backend_served_profile_verified
```

`backend_served_profile_verified` remains `false` unless a separately qualified stronger receipt exists.

Missing mandatory evidence is `BLOCKED_MEASUREMENT_SURFACE`, not worker-quality failure.

## First-attempt scoring and escalation

First-attempt quality is the scored result. Preserve valid failures.

If a valid ADAPTIVE first attempt fails its oracle, at most one fresh diagnosis-only escalation may run at the next stronger justified tier if the published candidate/authority permits it. It never replaces the original first-attempt score.

CONTROL may be rerun at most once only for host/tool diagnosis when authorized by the candidate semantics. Preserve the original score.

No indefinite retries and no compensating provider call after a measurement block unless this Task Contract explicitly authorizes that exact action.

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

- exact candidate branch/HEAD and protected-base relationship;
- native Windows host;
- effective Codex runtime exactly `0.153.4`;
- App Server exactly `0.153.4`;
- auth category `chatgpt`;
- no unauthorized tracked candidate changes;
- no custom/local agent-role ambiguity that could alter child instructions;
- P3 runtime-root requirements can be satisfied;
- repository-native deterministic lint/test/compile/preflight checks required by the candidate pass;
- no newer stable Codex release requiring D077 re-entry has appeared.

Any pre-provider gate failure blocks with zero new scored provider calls.

## Version-sensitive launch gate

Reviewed upstream state at current v4 authority:

```text
qualified pin:          Codex/App Server 0.153.4
current stable reviewed: 0.154.0
higher relevant review:  current upstream main for reattach path
version disposition:    PIN_RETAINED
upgrade fixes v3 race:  false at reviewed state
```

The stable `0.154.0` and upstream main retain the persisted-read dependency in the running-thread `thread/resume` path; `0.154.0` retains the empty-rollout error class.

If a stable Codex release newer than `0.154.0` appears before the first provider-backed v4 call, STOP and return to Orchestrator for D077 relevance classification. Do not independently upgrade/downgrade/substitute the experiment runtime.

## Scoring

Compute from v4 only:

```text
control_pass_count / 3
adaptive_pass_count / 3
adaptive_first_attempt_failures
adaptive_escalation_count
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
```

## Pilot decision

Final `pilot_decision` is one of:

- `QUALIFIED` — CONTROL 3/3 and ADAPTIVE 3/3 first-attempt PASS; no adaptive escalation/material false result/profile-resolution-invalidating reroute; complete D063 receipts; exact adaptive usage lower than control or a predeclared valid configured-cost normalization demonstrates lower compute; no offsetting material root rework or safety/authority incident.
- `QUALIFIED_QUALITY_ONLY` — all quality/profile/measurement requirements pass but a valid savings/cost claim cannot be made; exact token/duration evidence still required.
- `NOT_QUALIFIED` — a valid ADAPTIVE first attempt has a material quality regression/escalation/material false result or offsetting root rework.
- `BLOCKED_MEASUREMENT_SURFACE` — mandatory D063 measurement cannot be obtained.
- `BLOCKED_PROFILE_RESOLUTION` — a frozen requested child profile cannot resolve exactly before its scored turn.

A T063 pilot decision is evidence for later R007 convergence only; it is not itself global policy.

## Acceptance criteria

- **AC-T063-1:** NEW `root-4`; root/runtime profile frozen and all pre-provider gates pass before scored execution.
- **AC-T063-2:** one clean v4 six-arm run in the frozen order; v1/v2/v3 excluded.
- **AC-T063-3:** every valid scored child satisfies complete D063 receipts and remains read-only.
- **AC-T063-4:** P1/P2/P3 satisfy their frozen deterministic/oracle semantics without leakage.
- **AC-T063-5:** v4 retry behavior is same-child/same-params only, bounded to the exact empty-rollout class, with parent residency checked immediately before every retry and separately counted.
- **AC-T063-6:** no score rewriting, unauthorized compensating calls, profile/runtime substitution, or semantic repair.
- **AC-T063-7:** D076 audit is complete and no substantial Executor-created private executable material was used.
- **AC-T063-8:** telemetry/handoff are pushed and sufficient for remote Stage 7 verification.
- **AC-T063-9:** exactly one valid pilot decision is emitted only when its prerequisites are satisfied; otherwise the exact blocker is preserved.
- **AC-T063-10:** R007 global routing policy remains unchanged until Orchestrator convergence.

## Verification and evidence requirements

Stage 6 must persist enough evidence to verify:

- authority/candidate identity and `candidate_head_before_execution`;
- all pre-provider gates and any represented bounded repair before provider execution;
- exact scored parent-turn count;
- exact scored child-attempt count;
- separately counted reattachment RPC attempts/retries;
- per-arm mandatory D063 receipts;
- exact token/duration/reroute receipts;
- task-contract consistency receipts defined by the published candidate;
- tracked/global mutation checks;
- oracle outcomes and frozen first-attempt results;
- pilot decision only when scientifically valid;
- D076 ephemeral-artifact inventory.

Do not persist private chain-of-thought or full worker transcripts.

## Code Review & Verify obligations

Before terminal completion, the Executor must review the executed/repaired candidate against this Task Contract, verify that any Stage 6 repair remained bounded and semantic-preserving, rerun affected deterministic checks, and persist the result in the handoff.

## Stop / escalation / SDD re-entry conditions

STOP rather than guess when:

- exact canonical/candidate identity cannot be established safely;
- a material defect/ambiguity exists in this Task Contract, Design, oracle, acceptance meaning or candidate completeness;
- a frozen model/reasoning/runtime/profile cannot resolve exactly;
- D063 mandatory measurement is unavailable;
- a required repair would alter experiment semantics or the v4 reattachment contract;
- D076-material executable content is missing;
- parent residency is lost during required reattachment;
- retry exhaustion/nonmatching reattach error occurs;
- P3 input/permission requirements cannot be satisfied;
- a newer stable Codex release triggers D077 re-entry;
- any safety/authority/branch invariant fails.

Persist available authorized evidence, push the handoff when possible, and return `BLOCKED`. Do not compensate by expanding the launch prompt or making another provider call unless this Task Contract explicitly authorizes it.

## Expected handoff / evidence

```text
handoffs/T063-adaptive-worker-routing-telemetry-v4.json
handoffs/T063-executor-handoff-v4.json
```

The terminal handoff must include at least:

```text
authority_head
candidate_head_before_execution
represented_stage6_repairs
scored_parent_turns
scored_child_attempts
reattach_resume_attempts_total
reattach_resume_retries_total
ephemeral_artifacts
executor_material_ephemeral_artifacts
pilot_decision
```

plus the per-arm measurement/scoring receipts required above.

## Terminal return shape

After pushing all authorized Stage 6 state, return only:

```text
STATUS: COMPLETED | BLOCKED
HANDOFF: handoffs/T063-executor-handoff-v4.json
BRANCH: test/t063-adaptive-worker-routing-requalification-v4
HEAD: <actual remote pushed HEAD>
```

## Human launch gate

```text
launch_state: AUTHORIZED_AWAITING_HUMAN_START
```

Human-mediated launch under D071 is required. ChatGPT does not start or directly control Codex.

D055 launch profile is presented to the Human separately from the transport prompt.

## Thin transport invariant

The Human-visible transport prompt is only a pointer to canonical Git authority. It MUST NOT restate this contract's experiment matrix, retry logic, acceptance criteria, evidence schema, exclusions, version runbook or stop conditions.

Normal T063 v4 transport:

```text
Set the visible Codex chat title to exactly:
AG | agent-governance | T063 | root-4

Repository: https://github.com/ManuelBouza/agent-governance
Session: NEW
Task Contract: docs/tasks/T063-adaptive-worker-routing-requalification.md
Authorized candidate: test/t063-adaptive-worker-routing-requalification-v4@f06c8f48f7b1d59dff9fc117cca5b42453ad23e8

Synchronize canonical Git authority, load the repository instructions/checkpoint and the Task Contract, then execute that Task Contract exactly. Return only its defined terminal result.
```

If a substantive task instruction appears necessary in transport, STOP and persist it into this Task Contract or another referenced canonical authority before launch.
