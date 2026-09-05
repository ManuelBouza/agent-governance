# T054 — Adaptive Subagent Compute Routing Pilot

## Identity

- Task ID: `T054`
- Status: `PLANNED`
- Type: `read-only matched-arm Executor/subagent evaluation`
- Base branch: `develop`
- SDD profile: `ASSURED`
- Test-Authorship-Mode: `orchestrator-specified evaluation; executor-runs`
- Research source: `docs/research/ADAPTIVE-SUBAGENT-COMPUTE-ROUTING-RESEARCH.md`
- Predecessor evidence: `docs/reviews/T053-R1.md`
- Expected evidence branch: `test/t054-adaptive-subagent-compute-routing-pilot`

## Objective

Test whether Codex can execute bounded child tasks with **task-adaptive model and reasoning profiles** at accepted quality while using less configured compute than a root-equivalent baseline, without changing Governance authority, persistent-root policy, product code, or write-safety semantics.

T054 is a controlled calibration pilot. It isolates child compute routing from T053's persistence experiment by using one fresh root, fresh disposable read-only children, matched tasks, fixed minimal child context, deterministic oracles, and no tracked product-code mutation.

The pilot evaluates three child task classes:

1. deterministic inventory / evidence collection;
2. dependency and symbol mapping;
3. independent adversarial technical review.

Each class runs one **CONTROL** child and one **ADAPTIVE** child over the same bounded input. CONTROL inherits the root-equivalent profile. ADAPTIVE receives an explicit task-appropriate profile.

## Pre-execution correction

T054 was specified but **not executed** before this correction.

The initial draft used `GPT-5.6 Sol / High` for the coordinator and therefore for the inherited CONTROL arm. That baseline is replaced before any experimental evidence exists.

The corrected baseline is:

```text
Coordinator root: GPT-5.6 Sol / Medium
CONTROL child: inherited GPT-5.6 Sol / Medium
```

Reason: current OpenAI guidance treats `Medium` as the balanced default for most agent work and reserves `High` for work whose complexity, review burden, edge-case analysis, security posture, or eval evidence justifies additional reasoning. T054 should therefore test adaptive child routing against a proportionate coordinator baseline rather than an intentionally expensive one.

This correction does not change D055 globally. It is the frozen T054 launch profile only.

## Preserved governance

D039, D041, D042, D053, D054, D055 and D056 remain controlling.

T054 does not change D055. Human-facing root launch guidance remains separate from Executor-internal child execution profiles.

Git/current authority remains authoritative. Child model selection grants no authority and cannot compensate for missing specification, Design, Plan, acceptance, or evidence.

Children MUST NOT:

- edit tracked repository files;
- edit committed Markdown;
- redefine probes, oracle, thresholds, task classes, or routing policy;
- create lifecycle authority;
- become a durable correctness dependency;
- read this Task Contract during a probe when the root's bounded probe message explicitly forbids it to prevent oracle leakage.

The root may write only the authorized non-Markdown T054 handoff/telemetry evidence on the expected topic branch. Ephemeral probe fixtures must remain outside tracked repository state.

## Experimental variable

The primary experimental variable is **child execution profile**, especially model + reasoning effort.

Child conversational context is fixed for both arms:

```text
Context-Fork: MINIMAL
Codex mapping: fork_turns = none
```

`service_tier` remains default/omitted unless the host requires an explicit neutral value. Tool/sandbox capability must be equivalent between matched arms.

The Human-visible root profile is also fixed for the complete pilot. Do not change root model or reasoning effort during execution. If the root cannot complete the coordinator role at the frozen profile, stop for Orchestrator re-entry rather than silently escalating the root and contaminating the matched comparison.

## Root launch profile

Human-visible launch profile for T054:

```text
Executor: Codex
Session: NEW
Model: GPT-5.6 Sol
Effort: Medium
```

Rationale: Sol supplies sufficient coordinator capability for planning, routing, oracle execution and result synthesis; Medium is the proportionate balanced baseline. The experiment tests whether bounded children can use still lower or differently allocated compute while preserving quality.

Concrete model names are adapter-operational values, not Governance semantics.

## Capability preflight

Before probes, the root MUST satisfy D042 and establish what the current Codex surface actually exposes.

Required fields:

```text
explicit_child_model_override_supported
explicit_child_reasoning_override_supported
fork_turns_supported
service_tier_override_supported
effective_child_model_observable
effective_child_reasoning_observable
effective_service_tier_observable
per_child_token_metrics_observable
per_child_duration_observable
```

Rules:

- if explicit child model or reasoning override is not supported, stop with `BLOCKED_CAPABILITY`;
- do not emulate adaptive routing with separate Human-visible roots;
- do not add a project `.codex/agents/` catalog solely for T054;
- prefer direct spawn-time overrides;
- if requested overrides are accepted but effective values are not observable, the pilot may continue for quality/operational evidence, but no verified-effective-profile or quantitative savings claim may be made.

## Child Execution Profile abstraction

For each child persist:

```text
Child-Role
Task-Class
Arm: CONTROL | ADAPTIVE
Compute-Tier: ECONOMY | BALANCED | FRONTIER
Requested-Model
Requested-Reasoning
Context-Fork
Requested-Fork-Turns
Requested-Service-Tier
Capability
Tool-Surface
Escalation-Policy
Expected-Return
```

Persist effective/resolved model, reasoning and service tier when exposed. Otherwise store `null` with an explicit availability reason.

## Frozen matched profiles

### CONTROL

For every probe:

```text
Compute-Tier: FRONTIER
Model: inherited from root / GPT-5.6 Sol equivalent
Reasoning: inherited from root / Medium equivalent
fork_turns: none
Capability: read-only
service_tier: default
requested_profile: INHERITED_ROOT_EQUIVALENT
```

Normally omit child-specific model/effort arguments so native inheritance is exercised.

### ADAPTIVE

| Probe | Task class | Compute tier | Codex model | Reasoning | fork_turns |
| --- | --- | --- | --- | --- | --- |
| P1 | deterministic inventory/evidence | ECONOMY | GPT-5.6 Luna | Low | none |
| P2 | dependency/symbol mapping | BALANCED | GPT-5.6 Terra | Medium | none |
| P3 | adversarial independent review | BALANCED | GPT-5.6 Terra | High | none |

P3 intentionally allocates more reasoning effort than CONTROL while using a lower model tier. The pilot therefore tests **task-appropriate compute allocation**, not a requirement that every adaptive field be numerically lower than CONTROL.

If an exact named tier is unavailable but the current Codex surface exposes a documented equivalent, record the replacement and rationale. Do not silently substitute Sol for a lower-tier ADAPTIVE arm and count it as successful routing.

## Execution topology

- one fresh Human-visible Codex root;
- six fresh read-only children total: one CONTROL + one ADAPTIVE for each P1/P2/P3;
- identical repository/fixture inputs and equivalent tool access within each matched pair;
- maximum `2` concurrently open children;
- no write-capable child;
- no child reuse between probes;
- close every child after bounded result transfer;
- return concise structured conclusions, not full transcripts.

Fixed alternating order:

```text
P1: ADAPTIVE -> CONTROL
P2: CONTROL -> ADAPTIVE
P3: ADAPTIVE -> CONTROL
```

Prepare the full bounded message before either arm. Do not give the second arm hints learned from the first.

## Probe P1 — deterministic inventory

Inspect only:

- `tools/repository_context.py`;
- `tools/_repository_context/*.py`;
- `code-health.json`.

Return:

1. exact runtime module paths;
2. physical LOC for each runtime module;
3. configured size ratchet for `tools/repository_context.py`;
4. repository hard limit;
5. whether any repository-context runtime module exceeds the hard limit;
6. evidence commands/files used.

### P1 oracle

The root independently computes the answer from Git/source using deterministic local tooling. Exact paths, LOC and configured numeric values are required. No invented module is permitted.

P1 PASS requires every requested field correct.

## Probe P2 — dependency and symbol map

Using current `develop`, return:

1. exact internal import/dependency edge set among `tools/repository_context.py` and `tools/_repository_context/*.py`;
2. whether that graph is acyclic;
3. module owning each symbol:
   - `build_report`;
   - `parse_registry`;
   - `compute_rcab_projection`;
   - `build_manifest`;
   - `build_live_status`;
   - `validate_snapshot_integrity`;
4. concise evidence used.

### P2 oracle

The root independently derives the exact edge set using AST/source characterization and checks it against the deterministic package-cycle characterization. Symbol ownership is checked from the deterministic symbol map/source.

P2 PASS requires exact edge-set equality, correct acyclicity, and all six symbol owners correct.

## Probe P3 — adversarial independent review

### Ephemeral fixture

Outside the tracked worktree, copy current `tools/repository_context.py` plus `tools/_repository_context/`.

In the temporary facade only, replace the source-path-derived package name with one fixed process-global package name while leaving the rest of the loading approach mechanically equivalent. Do not alter tracked source.

Persist the fixture digest and exact mechanical mutation in telemetry, but do not disclose the expected defect to either child.

### P3 child task

Review only the supplied temporary fixture/diff for correctness when two independent source roots/worktrees load copies in the **same Python process**.

Explicitly forbid reading `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md`, T053 reviews, T053 telemetry, or other oracle-bearing project evidence during this probe.

Return:

```text
status
findings with severity
mechanism/evidence
minimal reproduction or proof direction
minimal fix direction
```

### P3 oracle

The seeded fixture contains one material expected defect: the fixed process-global package name allows the second source root to reuse/cache modules loaded from the first through `sys.modules`, causing cross-worktree/source-root contamination.

P3 PASS requires identifying the defect as material/high severity, explaining the same-process cache mechanism, and proposing source-specific namespace/isolation. Invented material findings fail the probe.

## Escalation

First-attempt assigned-profile result is the matched-arm score.

If ADAPTIVE fails:

1. preserve the failure;
2. optionally run one fresh diagnosis-only escalation child using:
   - Luna Low -> Terra Medium;
   - Terra Medium -> Sol Medium or High according to failure type;
   - Terra High -> Sol High;
3. record reason/outcome;
4. never replace the failed first-attempt adaptive score.

CONTROL may be rerun once only to distinguish host/tool failure from model-quality failure; preserve the original result.

No indefinite retries.

## Telemetry

Persist:

- `handoffs/T054-adaptive-routing-telemetry.json`;
- `handoffs/T054-executor-handoff.json`.

Per child, when observable:

```text
child_id
probe
arm
role
task_class
requested_profile
requested_model
requested_reasoning_effort
requested_fork_turns
requested_service_tier
effective_model
effective_reasoning_effort
effective_service_tier
profile_resolution_verified
started_at_utc
ended_at_utc
duration_seconds
input_tokens
cached_input_tokens
output_tokens
reasoning_tokens
total_tokens
result_status
oracle_score
verification_result
retry_or_escalation_reason
closed
```

Unavailable values must be `null` with reason. Never estimate token counts, model identity or effective effort.

Also record:

- D042/bootstrap identity;
- root launch profile and host surface;
- capability preflight;
- prepared probe messages or deterministic digests;
- proof of semantically identical matched-arm task content;
- P3 fixture digest/mutation;
- concurrency and child closure;
- root oracle-validation work;
- root rework caused by child results;
- compaction events if observable.

Do not persist private chain-of-thought or full child transcripts.

## Scoring

Compute:

```text
control_pass_count / 3
adaptive_pass_count / 3
adaptive_escalation_count
material_false_negative_count
material_false_positive_count
verified_effective_profile_count
available_control_tokens
available_adaptive_tokens
available_control_duration
available_adaptive_duration
```

Final `pilot_decision` is exactly one of:

### `QUALIFIED`

Require all:

- CONTROL 3/3;
- ADAPTIVE 3/3 on first attempt;
- adaptive escalation count = 0;
- no material false negative or invented material finding;
- host verifies effective model + reasoning for all three adaptive children;
- adaptive P1 is below CONTROL in model and reasoning;
- adaptive P2 is below CONTROL in model while retaining Medium reasoning;
- adaptive P3 uses a lower model tier with task-justified High reasoning and preserves quality;
- no safety/authority/branch incident.

`QUALIFIED` supports a later normative routing decision. It does not prove a precise token/cost saving unless attributable usage telemetry exists.

### `QUALIFIED_QUALITY_OBSERVABILITY_LIMITED`

Use when both arms pass all probes without escalation/material regression and requested adaptive overrides were accepted, but effective profile identity and/or attributable usage telemetry is insufficient for a verified quantitative claim.

### `NOT_QUALIFIED`

Use when ADAPTIVE has a material first-attempt quality regression, required escalation, P3 false negative, invalid material finding, or other failure of minimum-sufficient-compute qualification.

### `BLOCKED_CAPABILITY`

Use when the host cannot request child-specific model and reasoning overrides sufficiently to execute the experiment.

## Acceptance criteria

- **AC-T054-1:** D042 passes before authority/probe execution; root launch is NEW and fixed at `GPT-5.6 Sol / Medium` for the whole pilot.
- **AC-T054-2:** capability preflight is recorded without inventing unsupported host features.
- **AC-T054-3:** exactly P1/P2/P3 are evaluated with root-equivalent CONTROL and explicit ADAPTIVE profiles unless capability-blocked.
- **AC-T054-4:** matched-arm context/tool access is equivalent; `fork_turns=none` isolates child compute routing.
- **AC-T054-5:** P1/P2 deterministic oracles are independently computed by root; P3 uses the frozen ephemeral isolation defect without tracked mutation or oracle leakage.
- **AC-T054-6:** all first-attempt results and retries/escalations are preserved honestly.
- **AC-T054-7:** requested/effective profile and usage telemetry is persisted when observable; unavailable values are explicit `null` with reasons.
- **AC-T054-8:** all children are fresh, read-only and closed; max concurrent children `<=2`; no tracked product-code mutation occurs.
- **AC-T054-9:** final handoff computes one frozen `pilot_decision` and avoids unsupported quantitative savings claims.
- **AC-T054-10:** no authority leakage, Executor-authored Markdown, static `.codex/agents/` pilot catalog, D055 change, or mid-pilot root profile escalation occurs.

## Verification

Minimum root verification:

- exact current Git identity and clean/read-only baseline;
- deterministic P1 source/LOC/config calculation;
- deterministic P2 AST/dependency + symbol ownership calculation;
- P3 fixture digest and same-process reproduction independent of child output;
- evidence JSON validity;
- `git diff --check`;
- final branch diff contains only authorized T054 non-Markdown handoff/telemetry evidence unless Orchestrator explicitly re-enters.

## Non-goals

T054 does not:

- refactor product code;
- test persistent-root continuity;
- test write-capable Worker routing;
- optimize `fork_turns` as a separate causal variable;
- change D055 or consumer governance policy;
- establish provider-independent model names;
- require custom agents or `.codex/agents/`;
- claim token/cost savings without attributable evidence.

A later pilot may extend validated routing to write-capable Worker tasks.

## Ownership and handoff

ChatGPT Orchestrator owns this Task Contract, frozen probes/oracles, acceptance and later policy decisions.

Executor owns D042 execution mechanics, child spawning/configuration, ephemeral fixture mechanics within the frozen specification, deterministic oracle execution, telemetry/handoff JSON, and Git mechanics for the authorized evidence branch.

Final handoff must include root/branch/base/HEAD, capability preflight, per-child requested/effective profiles, probe scores, escalation evidence, usage/duration telemetry, final `pilot_decision`, verification, unresolved issues, and no-authority-leakage statement.

Return only:

```text
STATUS: DONE | BLOCKED
HANDOFF: handoffs/T054-executor-handoff.json
BRANCH: <branch>
HEAD: <pushed-head>
```
