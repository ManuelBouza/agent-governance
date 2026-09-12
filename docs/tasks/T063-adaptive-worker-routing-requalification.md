# T063 — Adaptive Worker Routing Requalification

## Identity

- Task ID: `T063`
- Status: `READY / AUTHORIZED_AWAITING_HUMAN_START`
- Type: `read-only replicated matched-arm Executor/subagent evaluation`
- SDD profile: `ASSURED`
- Base branch: `develop`
- Expected topic branch: `test/t063-adaptive-worker-routing-requalification-v8`
- Expected executor handoff: `handoffs/T063-executor-handoff-v8.json`
- Expected telemetry: `handoffs/T063-adaptive-worker-routing-telemetry-v8.json`
- Test-Authorship-Mode: `orchestrator-conformance`
- Owner: ChatGPT Orchestrator (specification/oracle/acceptance and D068 Stage 5) / Agente de IA Ejecutor (Stage 6 execution/evidence) / Human Owner (final authority and Human-mediated launch)
- Controlling design review: `docs/reviews/T063-R16.md`
- Current readiness review: `docs/reviews/T063-R19.md`
- Prior readiness revocation: `docs/reviews/T063-R18.md`
- Withdrawn readiness: `docs/reviews/T063-R17.md`
- Current persistence research: `docs/research/R025-T063-V8-REATTACH-CLASSIFIER-HARDENING.md`
- Prior persistence research: `docs/research/R024-T063-V7-NO-ROLLOUT-REATTACH-RACE.md`
- Measurement authority: `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md`
- Delegation authority: `docs/decisions/D065-semantic-executor-delegation-obligation.md`
- Routing gate authority: `docs/decisions/D075-coordinator-direct-execution-gate.md`
- Materialization boundary: `docs/decisions/D076-stage6-ephemeral-executable-materialization-boundary.md`
- Version authority: `docs/decisions/D077-version-sensitive-upstream-revalidation.md`

## Objective

Run one clean, prospectively replicated qualification evaluation to determine whether the frozen task-adaptive delegated-worker profiles preserve absolute oracle-scored quality across repeated first attempts and, when CONTROL also meets accepted quality, whether ADAPTIVE provides material exact-token efficiency and/or a validated lower-tier routing result.

T063 evaluates Stage B worker compute routing only. Delegation-worthiness is fixed by D075/D065 and is not an experimental variable. This Task Contract does not adopt a global adaptive-routing policy.

## Current specification carrier / controlling references

Load only the smallest controlling set needed for execution:

- `AGENTS.md`;
- this Task Contract;
- `docs/reviews/T063-R16.md`;
- `docs/reviews/T063-R19.md`;
- `docs/reviews/T063-R18.md` for the withdrawn-candidate boundary;
- `docs/research/R025-T063-V8-REATTACH-CLASSIFIER-HARDENING.md`;
- `docs/research/R024-T063-V7-NO-ROLLOUT-REATTACH-RACE.md`;
- R021/R022/R023 when earlier adapter provenance is needed;
- D063, D065, D075, D076 and D077.

`T063-R17` and candidate `83f38bd9813cfdd107486ad40d39df6335513ce8` are historical withdrawn readiness evidence only and MUST NOT be used as launch authority.

Historical T054/T063 v1-v7 attempts are planning/provenance evidence only and MUST NOT be reused for v8 scoring.

## Requirement / specification delta

### MODIFIED

- **T063-RQ-1 — clean successor run:** v8 is one new homogeneous 24-arm run; v1-v7 are excluded from every v8 score, metric and decision.
- **T063-RQ-6 — same-child persistence barrier:** after exact public child correlation, reattachment may retry only the accepted exact `EMPTY_ROLLOUT` family or a structurally exact `ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD` availability condition. Both share one ten-attempt budget and all R022 same-child/residency/no-new-provider invariants.
- **T063-RQ-6A — structured no-rollout classifier:** the represented JSON-RPC error mapping must parse safely and satisfy `code == -32600` and `message == "no rollout found for thread id <exact child id>"` exactly. Wrong code, message drift, malformed payload or different/missing child ID does not match.
- **T063-RQ-13 — policy boundary:** v8 can qualify/reject only this frozen calibration mapping; R007 global policy remains an Orchestrator decision after convergence.

### PRESERVED

- **T063-RQ-2 — parent spawn receipt:** public live App Server notifications for the exact parent turn are authoritative for spawn cardinality/correlation.
- **T063-RQ-3 — completed parent snapshot:** exact completion identity/final `PARENT_SPAWNED` text remain required; the live Started item need not be duplicated in the completed snapshot.
- **T063-RQ-4 — parent activity safety:** forbidden/multiple/contradictory parent activity remains fail-closed.
- **T063-RQ-7 — D063 measurement:** exact child identity, permission, parent residency, configured profile, exact usage/duration and reroute receipts remain mandatory.
- **T063-RQ-8 — config-authoritative task/profile:** substantive child task and requested profile remain frozen by Stage 5 configuration; the parent is transport-only.
- **T063-RQ-9 — first-attempt scoring:** valid quality failures are preserved and never rewritten/replayed.
- **T063-RQ-10 — model-evidence attribution:** every fully measured child is quality evidence; PASS children are per-child efficiency eligible; aggregate cost-per-success includes valid failed attempts.
- **T063-RQ-11 — run validity:** a run is execution-valid only when all 24 scheduled children complete with mandatory receipts; quality PASS/FAIL does not define execution validity.
- **T063-RQ-12 — read-only children:** scored workers remain read-only and measurement must not mutate tracked/global product state.
- **T063-RQ-14 — fixed replication:** four replicate blocks, 24 scored first-attempt children on a complete valid run.
- **T063-RQ-15 — counterbalanced order:** for each probe, ADAPTIVE runs first twice and CONTROL first twice according to the frozen schedule.
- **T063-RQ-16 — quality-failure continuation:** a fully measured valid `WORKER_QUALITY` FAIL remains model-quality evidence and does not stop the fixed schedule.
- **T063-RQ-17 — absolute profile qualification:** each profile/probe requires 4/4 PASS; global profile qualification requires 12/12 plus intact profile/reroute evidence.
- **T063-RQ-18 — complete outcome taxonomy:** every complete valid 24-arm run produces one non-null frozen pilot decision.
- **T063-RQ-19 — quality-adjusted operational usage:** report total tokens/duration and tokens/duration per successful first attempt; resources spent on valid FAILs remain in numerators.
- **T063-RQ-20 — material exact-token gate:** when both profiles globally qualify, ADAPTIVE exact tokens per success must improve by at least 10% to support the usage-efficiency-qualified outcome.

## Controlling Design

### Scientific interpretation

V8 is a fixed-n replicated qualification calibration, not a formal population-level non-inferiority trial. Four replicates are project-specific pilot policy. There are no p-values, adaptive sample expansion, outcome-conditioned reruns, or population-level confidence claims.

Quality is defined by frozen deterministic/oracle semantics. CONTROL is a comparator, not the source of truth for acceptance.

### Frozen root and child profiles

```text
root: gpt-5.6-sol / medium

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
Block 1: P1 A->C, P2 C->A, P3 A->C
Block 2: P1 C->A, P2 A->C, P3 C->A
Block 3: P1 A->C, P2 C->A, P3 A->C
Block 4: P1 C->A, P2 A->C, P3 C->A
```

Each arm uses a fresh App Server and fresh exact child. Mutable session state is not shared between trials. Each fully measured child MUST carry exact `replicate`, `sequence_index`, `within_block_index` and deterministic `trial_id` metadata.

### Config-authoritative child contract and parent surface

Before each measurement parent acts, the published Stage 5 candidate fixes substantive worker task and requested model/reasoning in App Server configuration. The parent may trigger exactly one child but does not select task semantics, model or reasoning.

Public child correlation uses only `subAgentActivity(kind=Started, agentThreadId=<exact child>)` from the exact live parent-turn window. Internal/raw response events are not passing evidence.

The v6-qualified parent window remains controlling: deduplicate public Started activity by public item ID; require exactly one logical matching Started activity; reject second/different/contradictory spawn or forbidden parent activity; require exact parent completion identity and final `PARENT_SPAWNED`; the completed snapshot need not duplicate the live Started item.

### V8 same-child persistence barrier

After exact live child correlation, `thread/resume` may retry only the same exact child with the same params object inside one common persistence barrier.

`EMPTY_ROLLOUT` retains the accepted R022 marker family.

`ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD` is **not** defined as intrinsically transient. It is a retryable availability condition only when the flattened `AppServerError` safely yields exactly one represented JSON-RPC mapping satisfying:

```text
method prefix exactly: thread/resume failed: 
error.code:             integer -32600
error.message:          exactly "no rollout found for thread id <exact child id>"
```

The published Stage 5 implementation uses `ast.literal_eval` as a safe literal parser for the represented mapping, never `eval`, and compares typed fields exactly. Any parse failure, non-mapping payload, wrong code, `bool` code, message prefix/suffix drift, missing/different ID or unrelated invalid-request error is nonmatching and blocks immediately.

Both accepted availability conditions consume one shared maximum of ten total `thread/resume` attempts. The budget does not reset across a mixed sequence. For every retry after attempt 1:

```text
wait 0.2 seconds
-> recheck exact parent loaded residency immediately before retry
-> retry identical thread/resume params for the same child
```

No spawn replay, parent-turn replay, child replacement, provider/model quality turn, profile/oracle change or alternate receipt surface is allowed. Parent loss, exhaustion or any nonmatching error blocks immediately.

A mixed sequence such as `ROLLOUT_NOT_FOUND_FOR_EXACT_CHILD -> EMPTY_ROLLOUT -> success` is permitted only within that single shared budget.

Exhaustion is classified as persistence/materialization failure. It does not retroactively prove that the observed no-rollout condition was transient.

The reattachment audit MUST record ordered availability conditions, child/parent IDs, attempt/retry counts, parent-residency rechecks, same-child reuse and `new_provider_turn_created=false`.

### Frozen probe semantics

- **P1:** exact Git evidence inventory for the frozen six-file set; exact oracle equality required.
- **P2:** static Python AST dependency/symbol map; exact edge set, acyclicity and ownership required.
- **P3:** adversarial independent review of one frozen high-severity fail-open authority/profile defect; detection/mechanism/severity/proof/fix direction required without invented material finding.

Frozen source/oracle baseline:

```text
69e910f329a2294c3b40df0f6ee983f9905f4677
```

### First-attempt, quality and usage semantics

Each scheduled arm has exactly one quality attempt. A valid quality FAIL has:

```text
execution_validity = VALID
failure_domain = WORKER_QUALITY
model_quality_eligible = true
model_efficiency_eligible = false
```

It does not stop the schedule and does not authorize replay/replacement/compensating scored calls. Persistence retries are transport operations, not additional provider/model quality attempts.

Per profile/probe:

```text
QUALITY_QUALIFIED     = 4/4 first-attempt PASS
QUALITY_NOT_QUALIFIED = 0-3/4 first-attempt PASS
```

Global profile qualification requires all three probes 4/4 plus intact profile/reroute evidence.

For each probe/profile and globally persist `attempt_count`, `pass_count`, `total_tokens`, `total_duration`, `tokens_per_success`, `duration_per_success`, and `profile_integrity`. Valid failed attempts remain in resource numerators.

Accepted-quality exact usage comparison occurs only when both global profiles qualify:

```text
exact_token_improvement = 1 - (adaptive_tokens_per_success / control_tokens_per_success)
material floor          = 0.10
```

### Complete pilot decision taxonomy

For a complete 24-arm execution-valid run, `pilot_decision` MUST be exactly one of:

- `QUALIFIED_PROFILE_AND_USAGE_EFFICIENCY`;
- `QUALIFIED_PROFILE_ROUTING_ONLY`;
- `ADAPTIVE_QUALITY_QUALIFIED_CONTROL_DEFICIENT`;
- `NOT_QUALIFIED`.

`pilot_decision=null` is reserved for incomplete/blocked non-quality execution.

## Plan & Trace

| Unit | Requirement / Design ref | Candidate artifact(s) | Required verification/evidence |
| --- | --- | --- | --- |
| inherited v3 core | RQ-2..12 | `evals/adaptive_worker_routing_v3/*`; v3 tests | D063 receipts; frozen oracles; first-attempt quality |
| inherited v4-v6 measurement | RQ-2..12 | v4/v5/v6 packages/tests | empty-rollout behavior; model evidence; live parent surface |
| inherited v7 replication | RQ-14..20 | v7 package/test at accepted implementation state | 24-arm schedule; trial metadata; aggregate/decision semantics |
| hardened v8 persistence adapter | RQ-6/RQ-6A; R025 | `evals/adaptive_worker_routing_v8/*` | safe structural parse; exact code/message/child; shared budget; residency/no-new-provider invariants |
| hardened v8 conformance | RQ-6/RQ-6A | `tests/test_t063_adaptive_worker_routing_v8_reattach.py` | positive exact shape plus wrong-code/message-drift/malformed/wrong-child negatives; mixed sequence; exhaustion; ordering |
| terminal evidence | all | v8 telemetry + handoff JSON | exact 24-arm accounting or exact blocker; quality/usage/reattach audit |

## Stage ownership and candidate boundary

T063 is D068-mode work.

```text
Stages 2-4 -> ChatGPT Orchestrator — COMPLETE, including R025 narrowing
Stage 5    -> ChatGPT Orchestrator — COMPLETE by T063-R19
Stage 6    -> Agente de IA Ejecutor — AUTHORIZED after Human launch
Stage 7    -> ChatGPT Orchestrator
```

## Published candidate freeze

Authorized Stage 6 candidate:

```text
candidate_branch: test/t063-adaptive-worker-routing-requalification-v8
candidate_head:   afdae0050226d61a10269f63017e2fac99eef644
candidate_base:   8b3cc5af3e70367eff6e55ebd416a554c8096763
```

No provider-backed call is authorized from another initial candidate HEAD.

The candidate is exactly one commit above the protected O276 base and contains exactly 28 executable/test files: 24 accepted v3-v7 blobs plus four v8 adapter/test files. Historical terminal JSON evidence is excluded.

Withdrawn candidate `83f38bd9813cfdd107486ad40d39df6335513ce8` remains prohibited launch authority.

A bounded Stage 6 repair may correct represented mechanics/test/config defects only when it preserves this Task Contract's frozen experiment semantics. Any change to parser acceptance shape, retry conditions, probes, oracles, sample size, schedule, profiles, thresholds, parent-surface semantics, shared retry budget, evidence taxonomy, quality rules or pilot-decision meaning requires Orchestrator re-entry.

## Authorized scope

The Executor may:

- synchronize/establish the exact authorized candidate safely;
- execute all deterministic/provider-free pre-provider checks;
- execute the published fixed 24-arm v8 evaluation;
- diagnose failures;
- make bounded represented mechanics-preserving repairs explicitly allowed above;
- perform technical Code Review & Verify;
- persist and push authorized non-Markdown v8 telemetry/handoff evidence.

## Explicit exclusions

The Executor MUST NOT:

- edit/commit Markdown;
- redesign T063 or change this Task Contract;
- broaden or weaken the structured no-rollout classifier;
- change frozen probes/oracles/task messages;
- change replicate count, schedule, profiles, thresholds or decision taxonomy;
- change accepted retry conditions, shared ten-attempt budget or retry ordering;
- stop, replay or replace an arm because of a valid quality FAIL;
- reuse v1-v7 attempts as v8 score data;
- infer backend-served identity beyond D063;
- use internal/raw response events as passing evidence;
- weaken exact live parent/child correlation or permit multiple spawned children;
- replay the measurement parent or create compensating provider calls after a validity block;
- create substantial private/ephemeral controller, harness, fixture generator, oracle/grader, lifecycle controller or telemetry system absent from the published candidate;
- execute withdrawn candidate `83f38bd...`;
- decide the global R007 routing policy.

## Invariants / constraints

### Root/runtime launch profile

The Human-facing D055 launch card is separate from the transport prompt. Frozen v8 launch profile:

```text
Executor:        Codex
Surface:         Codex Desktop / native Windows
Session:         NEW
Coordinator-ID:  AG | agent-governance | T063 | root-8
Root model:      gpt-5.6-sol
Root reasoning:  medium
Codex runtime:   exactly 0.153.4
App Server:      exactly 0.153.4
Auth category:   chatgpt
```

`root-8` was reserved but never launched under withdrawn O275 and remains the NEW same-work-unit successor root.

Other invariants:

- native Windows host;
- fresh App Server per scored arm;
- exact read-only parent/child permission posture;
- no tracked/global mutation attributable to measurement;
- no historical evidence enters v8 scoring;
- no provider call before every provider-free gate passes;
- no outcome-conditioned sample extension or early-success stopping.

## Executor process autonomy

Inside the authorized Stage 6 envelope, the Executor owns mechanics and private execution organization under D041/D054. This Task Contract controls experiment semantics, profiles, schedule, evidence and stop conditions; private process autonomy cannot change them.

## D076 executable-materialization boundary

The structured two-condition persistence controller and negative conformance suite are material Stage 5 behavior and are present in the published candidate.

```text
small mechanical execution aid -> Stage 6 may create/use it
substantial controller/harness/fixture/oracle behavior -> STOP -> Orchestrator Stage 5 re-entry
```

Terminal handoff MUST include:

```text
ephemeral_artifacts: [...]
executor_material_ephemeral_artifacts: []
```

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
- all repository-native deterministic tests covering v3-v8 pass;
- Python compile verification for the published eval/test candidate passes;
- repository-native Ruff/lint verification for the changed candidate passes;
- provider-free P1/P2/P3 oracle preparation passes;
- no newer stable Codex release requiring D077 re-entry has appeared.

The Orchestrator readiness review did not execute repository-native pytest, Ruff or compileall because its container could not resolve GitHub and GitHub reports no automatic CI statuses for the candidate. Those gates are mandatory Stage 6 preconditions, not optional duplicate checks.

Any pre-provider gate failure returns `BLOCKED` with zero new scored provider calls.

## Acceptance criteria

- **AC-T063-1:** exact hardened v8 candidate/runtime/profile and all provider-free gates pass before first provider call.
- **AC-T063-2:** exact `-32600` + exact canonical message + exact child is the only accepted no-rollout shape; wrong code, `bool`, message drift, malformed/non-mapping payload, wrong method or wrong/missing child fails closed.
- **AC-T063-3:** accepted R022 empty-rollout behavior remains unchanged.
- **AC-T063-4:** both availability conditions share one ten-attempt budget with wait -> parent-residency -> identical same-child resume ordering and no new provider turn.
- **AC-T063-5:** one clean v8 run executes exactly the frozen 24-arm schedule unless a non-quality validity blocker stops it; v1-v7 are excluded.
- **AC-T063-6:** every persisted scored child satisfies complete D063 receipts and remains read-only.
- **AC-T063-7:** P1/P2/P3 and v6 parent-surface semantics remain frozen without leakage.
- **AC-T063-8:** valid quality FAILs are retained, do not stop/replay the schedule and do not make a technically complete run execution-invalid.
- **AC-T063-9:** complete valid runs compute per-probe/global quality states, quality-adjusted usage metrics and exactly one frozen non-null pilot decision.
- **AC-T063-10:** exact-token usage qualification is claimed only when both profiles are 12/12 and the predeclared 10% materiality floor is met.
- **AC-T063-11:** no score rewriting, compensating provider calls, profile substitution, oracle leakage, D076 violation or tracked/global mutation occurs.
- **AC-T063-12:** telemetry/handoff persist exact trial/replicate identity, provider/reattachment accounting including ordered availability conditions, quality states, usage metrics and decision/blocker.

## Verification and trace requirements

Orchestrator-owned semantic/conformance assets:

- frozen P1/P2/P3 oracle construction/scoring;
- inherited v4 empty-rollout reattachment tests;
- inherited v5 model-evidence tests;
- inherited v6 parent-surface tests;
- inherited v7 schedule/taxonomy/aggregate tests;
- hardened v8 structured-classifier/persistence tests.

V8-specific deterministic coverage MUST prove exact structured positive classification, wrong-code/`bool`/message-drift/malformed/non-mapping/wrong-method/wrong-child rejection, empty-rollout preservation, mixed-condition success under one budget, common exhaustion, `sleep -> parent residency -> retry` ordering, identical child/params reuse, no new provider turn and parent-loss stop.

Required terminal evidence includes provider-free verification results; one telemetry item per fully measured scheduled child; replicate/trial identity; requested/resolved profiles and reroute evidence; exact token/duration evidence; per-probe/global quality states; quality-adjusted usage; exact token-improvement calculation when eligible; run/model-comparison/pilot eligibility; exact provider-attempt and reattachment-RPC accounting including ordered availability conditions; mutation/oracle-leak/D076 audit; and final technical review summary.

## Code Review & Verify obligations

Before terminal `COMPLETED` or `BLOCKED`, the Executor must review the represented candidate/repair delta against this Task Contract, verify no Stage 6 repair changed experiment semantics, verify inherited v3-v7 behavior remains intact, verify v8 schedule is exactly 24 arms/counterbalanced, verify valid quality FAIL continuation, verify structured classifier/shared-budget semantics, verify decision taxonomy and persist handoff evidence required by `docs/EXECUTOR-HANDOFFS.md`.

## Stop / escalation / SDD re-entry conditions

STOP rather than guess when any of these occurs:

- candidate/base/branch identity cannot be established safely;
- a material requirement, Design, Plan/Trace or acceptance defect/ambiguity is discovered;
- a semantic oracle appears defective;
- required runtime/model/reasoning profile cannot resolve exactly;
- a mandatory D063 receipt is unavailable;
- live parent activity cannot be represented under v6-qualified public semantics;
- a reattachment error matches neither exact accepted v8 availability condition;
- structured no-rollout parsing/code/message/child equality fails;
- the shared retry budget exhausts or parent residency is lost;
- a D076-material executable artifact is missing;
- a bounded repair would change approved semantics/Design;
- a newer stable Codex release requires D077 re-entry;
- a safety/security/permission/reproducibility invariant cannot be satisfied.

A valid `WORKER_QUALITY` FAIL is explicitly **not** a stop condition.

Persist available evidence, make no compensating scored call, and identify the earliest affected SDD stage before returning control.

## Version-sensitive launch gate

Reviewed official upstream state on 2026-09-12 after hardened candidate publication:

```text
qualified pin:           Codex/App Server 0.153.4
current stable reviewed: 0.154.0
current stable tag:      rust-v0.154.0
current stable date:     2026-09-09
newer stable observed:   none
version disposition:     PIN_RETAINED
```

R025 establishes that reviewed later source retains the relevant rollout-resolution architecture. D063 qualification is not automatically extended to later releases. If a stable Codex release newer than `0.154.0` appears before the first v8 provider-backed call, STOP and return to Orchestrator for D077 relevance classification. Do not independently upgrade/downgrade/substitute the runtime.

## Expected handoff / evidence

The Executor MUST persist:

```text
handoffs/T063-adaptive-worker-routing-telemetry-v8.json
handoffs/T063-executor-handoff-v8.json
```

The evidence must capture at least canonical authority/candidate identity, pre-provider verification, represented Stage 6 repairs, exact provider/reattachment accounting and ordered availability conditions, per-child receipts/results, replicate metadata, profile-quality/usage aggregates, model-evidence eligibility, blocker or pilot decision, mutation/oracle-leak review, and D076 ephemeral-artifact audit.

Do not persist private chain-of-thought.

## Terminal return shape

Return exactly:

```text
STATUS: COMPLETED | BLOCKED
HANDOFF: handoffs/T063-executor-handoff-v8.json
BRANCH: test/t063-adaptive-worker-routing-requalification-v8
HEAD: <actual remote pushed HEAD>
```

## Human launch gate

```text
launch_state: AUTHORIZED_AWAITING_HUMAN_START
```

ChatGPT MUST NOT start or directly control Codex. Human-mediated transport is required.

## Thin transport invariant

The Human-visible launch prompt is transport/bootstrap only. A compliant hardened-v8 transport contains only:

```text
Set the visible Codex chat title to exactly:
AG | agent-governance | T063 | root-8

Repository: https://github.com/ManuelBouza/agent-governance
Session: NEW
Task Contract: docs/tasks/T063-adaptive-worker-routing-requalification.md
Authorized candidate: test/t063-adaptive-worker-routing-requalification-v8@afdae0050226d61a10269f63017e2fac99eef644

Synchronize canonical Git authority, load the repository instructions/checkpoint and the Task Contract, then execute that Task Contract exactly. Return only its defined terminal result.
```

D055 launch-profile information is presented separately. Do not duplicate schedule, scoring, retry, acceptance, test runbook or evidence semantics in the transport prompt.
