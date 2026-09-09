# T063 — Adaptive Worker Routing Requalification

## Identity

- Task ID: `T063`
- Status: `READY / NOT_AUTHORIZED_PENDING_SEPARATE_HUMAN_LAUNCH`
- Type: `read-only matched-arm Executor/subagent evaluation`
- SDD profile: `ASSURED`
- Owner: ChatGPT Orchestrator (specification/oracle/acceptance) / Executor (execution/evidence after Human launch)
- Research source: `R007 — docs/research/ADAPTIVE-SUBAGENT-COMPUTE-ROUTING-RESEARCH.md`
- Routing-gate authority: `D075 — docs/decisions/D075-coordinator-direct-execution-gate.md`
- Measurement authority: `D063 — docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md`
- Predecessor evaluation: `T054` / `docs/reviews/T054-R1.md`
- Expected evidence branch: `test/t063-adaptive-worker-routing-requalification`

## Objective

Run the corrected successor evaluation required by D063/R007 to determine whether task-adaptive **delegated worker** compute profiles can preserve first-attempt quality while reducing configured compute and/or exact attributable usage relative to a root-equivalent control.

T063 evaluates **Stage B** of the routing architecture only:

```text
Stage A — already governed by D075/D065
    COORDINATOR_DIRECT | DELEGATED | CONTRACT_FIXED

Stage B — T063 experimental variable
    delegated child role / model tier / reasoning / bounded context
```

All T063 probes are deliberately material/read-heavy enough to be `DELEGATED` under D075/D065. T063 does not experimentally vary whether the coordinator should delegate. This avoids confounding delegation-worthiness with child-compute quality.

No global adaptive routing policy is authorized by this Task Contract. Qualification may support a later ChatGPT Orchestrator decision under D057.

## Why T063 is required

T054 was faithfully executed but ended `NOT_QUALIFIED`:

- P1 `Luna / Low` failed an exact physical-LOC requirement on first attempt;
- P2 had a shared task/oracle semantic ambiguity that caused both CONTROL and ADAPTIVE to add the same extra edge;
- P3 passed for both arms;
- the then-current surface lacked the exact effective child-profile/usage receipts required for a strong quantitative claim.

D063 subsequently qualified a version-sensitive Codex App Server measurement substrate for exact read-only child permission/profile/usage/duration/reroute receipts.

T063 corrects the remaining experimental defects:

1. use an unambiguous P1 with a less aggressive first-attempt economy mapping;
2. remove the P2 dependency-definition ambiguity;
3. require D063 measurement revalidation before scoring;
4. freeze requested->resolved child mappings before each scored turn;
5. preserve first-attempt scoring and bounded escalation without rewriting failures.

## Preserved governance

D039, D041, D055, D058, D060, D063, D065, D068 and D075 remain controlling.

T063 does not:

- modify D055 root-launch policy;
- adopt Luna/Terra/Sol names as provider-neutral semantics;
- authorize child writes;
- change product code or committed Markdown during Executor execution;
- let children redefine probes/oracles/thresholds;
- select a global routing policy from Executor evidence;
- treat configured/resolved child profile as provider-signed backend execution identity.

The Human-visible root owns task coordination. Children are bounded read-only workers. ChatGPT Orchestrator owns later convergence/decision acceptance.

## Human launch gate

T063 MUST NOT start from this definition alone.

A later explicit Human launch is required. Immediately before launch, ChatGPT Orchestrator must revalidate current `develop`, D063/D075, current Codex capabilities and current model availability, then persist the exact concrete launch/profile matrix without changing probe semantics.

No current T062 authorization, coordinator or scientific branch is reusable for T063. T063 is a distinct work unit and requires `NEW` under D060/D055.

## Root profile

The concrete root model/effort is selected and frozen at launch under then-current D055 guidance.

For matched-arm validity:

- one root profile remains fixed for the complete run;
- CONTROL children inherit the exact root-equivalent configured model/effort;
- root profile cannot change mid-run;
- a root profile change is a stop/re-entry condition, not an experimental adjustment.

Current design assumption is a frontier-capable root at proportionate `Medium` effort, but exact provider model names are launch-time adapter data.

## D063 measurement preflight

Before any scored child probe, the Executor must revalidate the current native Codex surface against D063.

Required exact-child receipts are the semantic equivalent of:

```text
real parent/child correlation
parent activePermissionProfile.id == :read-only
continuous parent residency for child reattachment
child activePermissionProfile.id == :read-only
requested child model/reasoning
resolved configured child model/reasoning
exact non-estimated child/turn token usage
exact child-turn duration
exact-child reroute signal/event observation
no tracked/global mutation caused by measurement
```

Persist separately:

```text
requested_profile
resolved_thread_profile
reroute_observed
backend_served_profile_verified
```

Unless a stronger qualified receipt exists at execution time, `backend_served_profile_verified` remains `false` exactly as D063 requires.

If the mandatory D063 surface cannot be revalidated, return `BLOCKED_MEASUREMENT_SURFACE`; do not fall back to inferred/estimated usage or profile identity.

## Execution topology

- one NEW Human-visible Executor coordinator root;
- three matched probe classes P1/P2/P3;
- one fresh CONTROL child + one fresh ADAPTIVE child per probe;
- all scored children read-only;
- identical bounded task message, repository input and tool surface within each matched pair;
- child context fork minimized/equivalent across matched arms;
- no child reuse between probes;
- maximum two concurrently open children, but sequential matched arms are preferred for evidence clarity;
- close each child after evidence capture;
- concise structured child return only; no full transcript persistence.

The coordinator may perform D075 conforming microactions for Git identity, oracle execution and evidence checks. Those root actions are not the experimental variable.

## Experimental profiles

Concrete model names MUST be frozen in the launch review after current capability revalidation.

Current intended Codex adapter mapping, derived from official current guidance and T054 evidence, is:

| Probe | Task class | CONTROL | ADAPTIVE hypothesis | Reasoning |
| --- | --- | --- | --- | --- |
| P1 | narrow deterministic evidence retrieval | root-equivalent | Luna-class economy worker | `Medium` |
| P2 | broader code/dependency exploration | root-equivalent | Terra-class balanced worker | `Medium` |
| P3 | adversarial independent technical review | root-equivalent | Terra-class balanced worker | `High` |

The P1 mapping intentionally does **not** repeat T054's failed `Luna / Low` hypothesis.

A launch-time model substitution is allowed only before any scored probe and only when official current Codex capabilities provide a documented equivalent tier. The exact frozen matrix must then be persisted. No mid-run substitution is allowed.

## Matched-arm order

Freeze the complete child task message before the first arm of each pair.

Use alternating order to reduce simple order bias:

```text
P1: ADAPTIVE -> CONTROL
P2: CONTROL -> ADAPTIVE
P3: ADAPTIVE -> CONTROL
```

Do not reveal one arm's result to the other arm before both first attempts are complete.

## Probe P1 — exact Git evidence inventory

### Purpose

Test a narrow, clear, repetitive evidence task that should be suitable for an economy worker without the physical-LOC semantic ambiguity that invalidated T054 P1.

### Frozen task semantics

At launch, the Orchestrator freezes a list of exactly six tracked UTF-8 repository files from current `develop`.

Each child must return for every file:

```text
path
Git blob SHA
byte size from Git object metadata
exists_at_frozen_HEAD: true|false
```

The child must also return the exact frozen HEAD it evaluated and concise evidence commands/APIs used.

### Oracle

The root independently derives exact values from Git object metadata at the frozen HEAD. Files and values are compared exactly.

P1 PASS requires all paths, blob SHAs, sizes and HEAD identity exact with no invented path/value.

### Adaptive intent

Economy worker / Medium reasoning. The task tests precise bounded tool use rather than ambiguous measurement interpretation.

## Probe P2 — unambiguous static dependency/symbol map

### Purpose

Re-evaluate the T054 code-mapping class without the shared dependency-definition confound.

### Frozen definition

At launch, select one existing Python package slice with a deterministic repository-owned characterization.

For T063, `dependency edge` means **only a static Python import edge represented in the AST between the frozen in-scope source files**.

Explicit exclusions:

- package bootstrap execution;
- dynamic loader side effects;
- `sys.modules` runtime reuse;
- filesystem/package-discovery relationships that are not AST import statements;
- imports to modules outside the frozen in-scope file set.

The child returns:

```text
exact internal static AST edge set
acyclic: true|false
owner module for six frozen symbols
concise evidence
```

### Oracle

Before execution, the Orchestrator freezes the package slice, six symbols and exact deterministic AST characterization. Root verification recomputes the same definition independently.

P2 PASS requires exact edge-set equality, correct acyclicity and all symbol owners exact.

### Adaptive intent

Balanced exploration worker / Medium reasoning.

## Probe P3 — adversarial independent review

### Purpose

Test whether a balanced worker with higher task-specific reasoning can preserve material review quality below the root model tier.

### Fixture

Use one ephemeral, non-tracked fixture with exactly one frozen material defect. The defect must be mechanically seeded from current source and independently reproducible by the root.

The fixture/oracle must be frozen before child execution and must not be disclosed to either arm.

Prefer a same-process isolation/cache, ordering, fail-closed or ownership defect that has one objectively testable mechanism and does not require broad product redesign.

### Child return

```text
status
material findings with severity
mechanism/evidence
minimal reproduction/proof direction
minimal fix direction
```

P3 PASS requires detection of the seeded material defect, correct mechanism, appropriate severity and no invented material finding.

### Adaptive intent

Balanced worker / High reasoning.

## First-attempt mapping gate

Before each scored ADAPTIVE turn:

1. spawn/configure the fresh child with the frozen requested model/effort;
2. use the D063-qualified surface to verify the resolved configured child profile and read-only permission before relying on the turn;
3. fail closed if requested->resolved mapping is not the frozen mapping;
4. record reroute events separately;
5. never infer backend-served identity beyond D063.

A mapping mismatch is `BLOCKED_PROFILE_RESOLUTION`, not an adaptive quality failure.

## Escalation

First-attempt quality is the scored result.

If an ADAPTIVE child fails the task oracle after valid profile resolution:

- preserve the failure;
- optionally run one fresh diagnosis-only escalation child at the next stronger justified tier;
- record escalation cause, requested/resolved profile and outcome;
- do not replace the failed first-attempt score.

CONTROL may be rerun once only to diagnose host/tool instability. Preserve the original score.

No indefinite retries.

## Telemetry

Persist only authorized non-Markdown evidence on the T063 evidence branch:

- `handoffs/T063-adaptive-worker-routing-telemetry.json`
- `handoffs/T063-executor-handoff.json`

Per scored child capture at least:

```text
child_id
probe
arm
role
task_class
requested_profile
requested_model
requested_reasoning_effort
resolved_model
resolved_reasoning_effort
permission_profile
reroute_observed
backend_served_profile_verified
input_tokens
cached_input_tokens
output_tokens
reasoning_tokens
total_tokens
duration_seconds
result_status
oracle_score
verification_result
retry_or_escalation_reason
closed
```

Unavailable fields may be `null` only when D063 permits them to be non-mandatory. Never estimate mandatory quantitative fields.

Also capture root profile, Codex version/capabilities, exact frozen HEAD, task-message digests, matched-arm equality, oracle digests, child closure and tracked-worktree mutation check.

Do not persist private chain-of-thought or full worker transcripts.

## Scoring

Compute:

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
```

## Pilot decision

Final `pilot_decision` is exactly one of:

### `QUALIFIED`

Require all:

- CONTROL `3/3` first-attempt PASS;
- ADAPTIVE `3/3` first-attempt PASS;
- adaptive escalation count `0`;
- no material false negative/false positive;
- no profile-resolution failure or reroute that invalidates the intended comparison;
- D063 mandatory exact-child receipts valid for all scored children;
- exact adaptive total token usage is lower than exact control total token usage across the complete matched set **or** a predeclared normalized compute-cost mapping shows lower total configured cost without unsupported backend identity claims;
- no offsetting material increase in root rework;
- no safety/authority/branch incident.

`QUALIFIED` supports later policy consideration. It is not itself a global routing decision.

### `QUALIFIED_QUALITY_ONLY`

Allowed only if all quality/profile-resolution conditions pass but the exact current provider pricing/cost normalization needed for a monetary claim is unavailable or unsuitable. Exact token/duration receipts must still be reported. This outcome supports quality feasibility but not a savings claim or global preferred mapping by itself.

### `NOT_QUALIFIED`

Use when a valid ADAPTIVE first attempt has a material quality regression, requires escalation, produces a material false result, or creates offsetting root rework that defeats minimum-sufficient-compute intent.

### `BLOCKED_MEASUREMENT_SURFACE`

Use when D063 mandatory measurement cannot be revalidated.

### `BLOCKED_PROFILE_RESOLUTION`

Use when a requested frozen child model/effort cannot resolve to the required configured thread profile before a scored turn.

## Acceptance criteria

- **AC-T063-1:** separate Human launch; NEW task-scoped root; root profile frozen before probes.
- **AC-T063-2:** D063 native measurement surface revalidated before scored work.
- **AC-T063-3:** all probes are fixed `DELEGATED` units under D075/D065; delegation-worthiness is not an experimental variable.
- **AC-T063-4:** P1 removes T054 physical-LOC ambiguity and uses the revised first-attempt economy/Medium hypothesis.
- **AC-T063-5:** P2 static-AST edge semantics are explicit and exclude the T054 package-bootstrap ambiguity.
- **AC-T063-6:** P3 uses one independently reproducible seeded material defect with no oracle leakage.
- **AC-T063-7:** matched-arm messages/input/tools/context are equivalent except frozen compute profile.
- **AC-T063-8:** requested/resolved profile, permission, reroute, exact usage and duration receipts satisfy D063 for every scored child.
- **AC-T063-9:** all first-attempt failures/retries/escalations are preserved; no score rewriting.
- **AC-T063-10:** children remain read-only; no tracked product mutation or Executor-authored Markdown.
- **AC-T063-11:** one frozen pilot decision is computed exactly; no unsupported provider-backend identity or savings claim.
- **AC-T063-12:** final evidence explicitly states that D075 direct-execution policy and R007 adaptive compute-routing policy are separate claims.

## Non-goals

T063 does not:

- retest whether D075 microactions should be root-local;
- test write-capable workers;
- optimize worker count/parallelism;
- optimize context-fork depth as a separate variable;
- change D055 root policy;
- establish model names as durable governance semantics;
- authorize automatic routing rollout;
- modify T062 or resume its held scientific execution.

## Completion and convergence

Executor terminal evidence must be pushed to the expected T063 evidence branch and return only the Task-Contract-defined terminal shape.

After remote verification, ChatGPT Orchestrator performs convergence under D057:

- accept/reject execution validity;
- transition R007 based on the frozen pilot decision;
- only if evidence is sufficient, specify a later normative Stage-B routing decision/rollout;
- otherwise preserve the failed/deferred disposition without tuning post hoc.

No Executor launch is authorized by this definition.
