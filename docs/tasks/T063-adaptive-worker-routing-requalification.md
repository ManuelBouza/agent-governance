# T063 — Adaptive Worker Routing Requalification

## Identity

- Task ID: `T063`
- Status: `BLOCKED / STAGE5_REENTRY_REQUIRED`
- Type: `read-only replicated matched-arm Executor/subagent evaluation`
- SDD profile: `ASSURED`
- Base branch: `develop`
- Expected topic branch: `test/t063-adaptive-worker-routing-requalification-v8`
- Expected executor handoff: `handoffs/T063-executor-handoff-v8.json`
- Expected telemetry: `handoffs/T063-adaptive-worker-routing-telemetry-v8.json`
- Test-Authorship-Mode: `orchestrator-conformance`
- Owner: ChatGPT Orchestrator (specification/oracle/acceptance and D068 Stage 5) / Agente de IA Ejecutor (Stage 6 execution/evidence when authorized) / Human Owner (final authority and Human-mediated launch)
- Controlling design review: `docs/reviews/T063-R16.md`
- Readiness revocation: `docs/reviews/T063-R18.md`
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

Load only the smallest controlling set needed for the current stage:

- `AGENTS.md`;
- this Task Contract;
- `docs/reviews/T063-R16.md`;
- `docs/reviews/T063-R18.md`;
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

The Stage 5 implementation MUST use a safe literal/data parser for the represented mapping, not `eval`, and MUST compare typed fields exactly. Any parse failure, non-mapping payload, wrong code, message prefix/suffix drift, missing/different ID or unrelated invalid-request error is nonmatching and blocks immediately.

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
| hardened v8 persistence adapter | RQ-6/RQ-6A; R025 | `evals/adaptive_worker_routing_v8/*` | safe structured parse; exact code/message/child; shared budget; residency/no-new-provider invariants |
| hardened v8 conformance | RQ-6/RQ-6A | `tests/test_t063_adaptive_worker_routing_v8_reattach.py` | positive exact shape plus wrong-code/message-drift/malformed/wrong-child negatives; mixed sequence; exhaustion; ordering |
| terminal evidence | all | v8 telemetry + handoff JSON | exact 24-arm accounting or exact blocker; quality/usage/reattach audit |

## Stage ownership and candidate boundary

T063 is D068-mode work.

```text
Stages 2-4 -> ChatGPT Orchestrator — COMPLETE, with R025 narrowing
Stage 5    -> ChatGPT Orchestrator — REENTRY REQUIRED
Stage 6    -> Agente de IA Ejecutor — NOT AUTHORIZED
Stage 7    -> ChatGPT Orchestrator
```

## Published candidate freeze

There is currently **no authorized Stage 6 candidate**.

Withdrawn historical Stage 5 candidate:

```text
candidate_branch: test/t063-adaptive-worker-routing-requalification-v8
withdrawn_head:   83f38bd9813cfdd107486ad40d39df6335513ce8
withdrawn_base:   621e9ae0d73378b1013699e8726b315128c95891
reason:           R025 structured-classifier hardening required before launch
```

A new candidate MUST be a fresh exact HEAD materialized by ChatGPT Orchestrator and receive a new readiness review before Stage 6 authorization.

## Authorized scope

No Stage 6 execution scope is currently authorized.

ChatGPT Orchestrator Stage 5 may:

- materialize the hardened v8 adapter and conformance suite;
- promote accepted v3-v7 blobs without historical terminal JSON;
- run available provider-free syntax/smoke/structural checks;
- publish a clean exact candidate;
- perform readiness review and update this contract/checkpoint prospectively.

## Explicit exclusions

Until a fresh readiness review authorizes Stage 6:

- do not launch Codex for T063 v8;
- do not consume provider/model calls;
- do not execute withdrawn candidate `83f38bd...`;
- do not reuse v1-v7 attempts as v8 score data;
- do not weaken D063, parent-surface, profile, schedule, oracle, retry-budget or quality semantics;
- do not treat no-rollout as proof of transience merely because the child ID exists.

## Invariants / constraints

Future launch profile remains frozen unless a later readiness review changes it:

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

`root-8` was reserved but never launched and remains unconsumed.

Other invariants: native Windows; fresh App Server per scored arm; exact read-only parent/child posture; no tracked/global mutation; no provider call before provider-free gates pass; no outcome-conditioned sample extension or early-success stopping.

## Executor process autonomy

When Stage 6 is later authorized, the Executor owns mechanics under D041/D054 inside the durable contract envelope. It may not change experiment semantics, profiles, schedule, evidence meaning or stop conditions.

## D076 executable-materialization boundary

The structured two-class persistence controller and its conformance tests are material executable behavior and MUST exist in the Stage 5 candidate before Stage 6 authorization.

```text
small mechanical execution aid -> Stage 6 may create/use it
substantial controller/harness/fixture/oracle behavior -> STOP -> Stage 5 re-entry
```

## Acceptance criteria

- **AC-T063-1:** a new exact v8 candidate materializes R025's safe structured no-rollout classifier before readiness.
- **AC-T063-2:** exact `-32600` + exact message + exact child is the only accepted no-rollout shape; wrong code, message drift, malformed payload or wrong/missing child fails closed.
- **AC-T063-3:** accepted R022 empty-rollout behavior remains unchanged.
- **AC-T063-4:** both availability conditions share one ten-attempt budget with wait -> parent-residency -> identical same-child resume ordering and no new provider turn.
- **AC-T063-5:** inherited v3-v7 schedule, parent surface, oracle, quality, usage and decision semantics remain intact.
- **AC-T063-6:** no provider/model call occurs before a new readiness review and Human-mediated launch.
- **AC-T063-7:** once later authorized, all D063 receipts/read-only/mutation/evidence obligations remain mandatory for every scored child.
- **AC-T063-8:** a complete valid 24-arm run computes the frozen quality/usage/pilot taxonomy; incomplete validity blockers retain `pilot_decision=null`.

## Verification and trace requirements

New Stage 5 conformance coverage MUST prove:

- exact code/message/child classification positive case;
- wrong code rejection;
- exact-code message prefix/suffix drift rejection;
- wrong/missing child rejection;
- malformed/unparseable represented mapping rejection;
- unrelated `-32600` rejection;
- empty-rollout preservation;
- mixed-class success under one common budget;
- common-budget exhaustion;
- `sleep -> parent residency -> retry` ordering;
- exact same child and same params object reuse;
- no new provider turn;
- parent-loss fail-closed.

Before any future provider call, Stage 6 must also pass all repository-native deterministic v3-v8 tests, compile/lint/oracle/environment gates and D077 launch-time revalidation defined by the subsequent readiness authority.

## Stop / escalation / SDD re-entry conditions

STOP rather than guess when candidate identity, structured error shape, D063 receipt, runtime/profile exactness, parent correlation/residency, semantic oracle, D076 boundary or D077 version relevance cannot be established safely.

A valid `WORKER_QUALITY` FAIL is not a stop condition once Stage 6 is authorized.

## Version-sensitive launch gate

Current reviewed state:

```text
qualified pin:           Codex/App Server 0.153.4
current stable reviewed: 0.154.0
current stable tag:      rust-v0.154.0
version disposition:     PIN_RETAINED
```

R025 confirms that reviewed later source retains the relevant rollout-resolution architecture. D063 remains qualified specifically on 0.153.4. Any newer stable release before a future first provider call requires D077 relevance classification.

## Expected handoff / evidence

No v8 Executor handoff is currently authorized. After a fresh readiness review, the expected paths remain:

```text
handoffs/T063-adaptive-worker-routing-telemetry-v8.json
handoffs/T063-executor-handoff-v8.json
```

## Terminal return shape

When Stage 6 is later authorized, return exactly:

```text
STATUS: COMPLETED | BLOCKED
HANDOFF: handoffs/T063-executor-handoff-v8.json
BRANCH: test/t063-adaptive-worker-routing-requalification-v8
HEAD: <actual remote pushed HEAD>
```

## Human launch gate

```text
launch_state: NOT_AUTHORIZED
```

ChatGPT MUST NOT start or directly control Codex. Human-mediated transport may be issued only after a fresh exact candidate and readiness review re-authorize Stage 6.

## Thin transport invariant

No transport prompt is valid while `launch_state=NOT_AUTHORIZED`. The prior transport for `83f38bd...` is withdrawn. A future transport must remain a thin pointer to the then-current canonical Task Contract and exact authorized candidate.
