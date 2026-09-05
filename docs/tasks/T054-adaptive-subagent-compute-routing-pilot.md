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

Test whether Codex can execute bounded child tasks with **task-adaptive model and reasoning profiles** at accepted quality while using less configured compute than root-equivalent inheritance, without changing Governance authority, persistent-root policy, product code, or write-safety semantics.

T054 is a controlled calibration pilot. It isolates child compute routing from T053's persistence experiment by using one fresh root, fresh disposable read-only children, matched tasks, fixed minimal child context, deterministic oracles, and no tracked product-code mutation.

The pilot evaluates three child task classes:

1. deterministic inventory / evidence collection;
2. dependency and symbol mapping;
3. independent adversarial technical review.

Each class runs one **CONTROL** child and one **ADAPTIVE** child over the same bounded input. The control inherits the root-equivalent profile. The adaptive arm receives an explicit lower-cost profile appropriate to the task class.

## Preserved governance

D039, D041, D042, D053, D054, D055 and D056 remain controlling.

T054 does not change D055. The Human-facing root launch profile remains separate from Executor-internal child execution profiles.

Git/current authority remains authoritative. Child model selection grants no authority and cannot compensate for missing specification, Design, Plan, acceptance, or evidence.

Children MUST NOT:

- edit tracked repository files;
- edit committed Markdown;
- redefine the probes, oracle, thresholds, task classes, or routing policy;
- create lifecycle authority;
- become a durable correctness dependency;
- read this Task Contract during a probe when the root's bounded probe message explicitly forbids it to prevent oracle leakage.

The root may write only the authorized non-Markdown T054 handoff/telemetry evidence on the expected topic branch. Ephemeral probe fixtures must live outside tracked repository state and must be deleted or left outside the repository worktree.

## Experimental variable

The primary experimental variable is **child model + reasoning effort**.

To avoid confounding the first calibration, child conversational context is fixed to the smallest safe setting for both arms:

```text
Context-Fork: MINIMAL
Codex mapping: fork_turns = none
```

`service_tier` remains default/omitted in both arms unless the current host requires an explicit neutral value. Tool/sandbox capability must be equivalent between matched arms.

This pilot therefore validates task-adaptive compute routing first. More aggressive context-fork optimization may be evaluated separately after this result.

## Root launch profile

D055 Human-facing root guidance for T054:

```text
Executor: Codex
Session: NEW
Model: GPT-5.6 Sol
Effort: High
```

Rationale: the new root coordinates a controlled model-routing experiment and also supplies the fixed root-equivalent CONTROL baseline; root compute must not change between matched arms.

The concrete model names are adapter-operational values, not Governance semantics.

## Capability preflight

Before executing probes, the root MUST satisfy D042 and then establish what the current Codex surface actually exposes for child spawn configuration and telemetry.

Required preflight fields:

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

- if explicit child model or reasoning override is not supported, stop with pilot decision `BLOCKED_CAPABILITY`;
- do not emulate adaptive routing by opening separate Human-visible roots;
- do not add a project `.codex/agents/` catalog solely for T054;
- prefer direct spawn-time overrides so task-by-task routing remains observable and does not depend on static role files;
- if requested overrides are accepted but effective values are not observable, the pilot may continue for quality/operational evidence, but no quantitative or verified-effective-profile claim may be made.

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

Also persist effective/resolved model, reasoning and service tier when the host exposes them. Otherwise store `null` plus an explicit availability reason.

## Matched profiles

### CONTROL arm

For every probe:

```text
Compute-Tier: FRONTIER
Model: inherited from root / GPT-5.6 Sol equivalent
Reasoning: inherited from root / High equivalent
fork_turns: none
Capability: read-only
service_tier: default
```

The control should normally omit child-specific model/effort arguments so native inheritance is exercised. Record that as `requested_profile = INHERITED_ROOT_EQUIVALENT`.

### ADAPTIVE arm

| Probe | Task class | Compute tier | Codex model | Reasoning | fork_turns |
| --- | --- | --- | --- | --- | --- |
| P1 | deterministic inventory/evidence | ECONOMY | GPT-5.6 Luna | Low | none |
| P2 | dependency/symbol mapping | BALANCED | GPT-5.6 Terra | Medium | none |
| P3 | adversarial independent review | BALANCED | GPT-5.6 Terra | High | none |

If an exact named tier is unavailable but the current Codex surface exposes a documented equivalent, record the exact replacement and why. Do not silently substitute Sol for a lower-tier adaptive arm and count it as successful routing.

## Execution topology

- one fresh Human-visible Codex root;
- six fresh read-only children total: one CONTROL + one ADAPTIVE child for each of P1, P2 and P3;
- matched pair runs must use identical repository/fixture inputs and equivalent tool access;
- maximum `2` concurrently open children;
- no write-capable child;
- no child reuse between probes;
- close every child after bounded result transfer;
- child return must be concise and structured; do not ingest full transcripts into the root.

To reduce order bias, execute matched pairs in this fixed alternating order:

```text
P1: ADAPTIVE -> CONTROL
P2: CONTROL -> ADAPTIVE
P3: ADAPTIVE -> CONTROL
```

Do not run the second arm with extra hints learned from the first arm. The root must prepare the complete bounded probe message before launching either child in that pair and use semantically identical task content for both.

## Probe P1 — deterministic inventory

### Child task

Using the current T054 baseline, inspect only:

- `tools/repository_context.py`;
- `tools/_repository_context/*.py`;
- `code-health.json`.

Return:

1. exact runtime module paths in the repository-context facade/package;
2. physical LOC for each runtime module;
3. configured size ratchet for `tools/repository_context.py`;
4. repository hard limit;
5. whether any repository-context runtime module exceeds the hard limit;
6. evidence commands/files used.

### Oracle

The root independently computes the answer from Git/source using deterministic local tooling. Exact paths, exact LOC and exact configured numeric values are required. No semantic judgment is needed.

P1 PASS requires every requested field correct and no invented runtime module.

## Probe P2 — dependency and symbol map

### Child task

Using current `develop` source, return:

1. the exact internal import/dependency edge set among `tools/repository_context.py` and `tools/_repository_context/*.py`;
2. whether that graph is acyclic;
3. the module owning each symbol:
   - `build_report`;
   - `parse_registry`;
   - `compute_rcab_projection`;
   - `build_manifest`;
   - `build_live_status`;
   - `validate_snapshot_integrity`;
4. concise evidence used.

### Oracle

The root independently derives the exact edge set using AST/source characterization and checks it against the deterministic package-cycle characterization already present in the repository. Symbol ownership is checked from the deterministic symbol map/source.

P2 PASS requires exact edge-set equality, correct acyclicity result, and all six symbol owners correct.

## Probe P3 — adversarial independent review

### Ephemeral fixture preparation

The root creates a temporary copy outside the tracked worktree of the current `tools/repository_context.py` plus `tools/_repository_context/` package.

In the temporary facade only, replace the source-path-derived package name with one fixed process-global package name while leaving the rest of the loading approach mechanically equivalent. Do not alter tracked source.

The root must persist in telemetry the fixture digest and the exact mechanical mutation, but MUST NOT disclose the expected defect to either child.

### Child task

Review only the supplied temporary fixture/diff for correctness when two independent source roots/worktrees load their copies in the **same Python process**.

The bounded child message must explicitly instruct the child not to read `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md`, T053 reviews, T053 telemetry, or other oracle-bearing project evidence during this probe.

Return:

```text
status
findings with severity
mechanism/evidence
minimal reproduction or proof direction
minimal fix direction
```

### Oracle

The seeded fixture has one material expected defect: a fixed process-global package name allows the second source root to reuse/cache modules loaded from the first root through `sys.modules`, causing cross-worktree/source-root contamination.

P3 PASS requires the child to identify this defect as material/high severity, explain the same-process cache mechanism, and propose a source-specific namespace/isolation direction. Additional findings must be technically valid; invented high-severity findings fail the probe.

## Escalation

Matched-arm scoring is based on the **first attempt** at the assigned profile.

If an ADAPTIVE child fails its oracle:

1. record the failure unchanged;
2. optionally run one fresh escalation child for diagnosis only, using the next profile:
   - Luna Low -> Terra Medium;
   - Terra Medium -> Sol Medium or High according to failure type;
   - Terra High -> Sol High;
3. record escalation reason and outcome;
4. do not replace the failed first-attempt adaptive score with the escalated result.

Control failure may be rerun once only to distinguish a host/tool fault from model-quality failure; record the original failure.

No indefinite retries.

## Telemetry

Persist `handoffs/T054-adaptive-routing-telemetry.json` and final `handoffs/T054-executor-handoff.json`.

Per child record when observable:

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

Unavailable values must be `null` with an availability reason. Never estimate token counts, model identity, or effective effort.

Also record:

- D042/bootstrap identity;
- root launch profile and host surface;
- capability preflight;
- exact prepared probe messages or their deterministic digests;
- proof that matched arms received semantically identical task content;
- fixture digest/mutation for P3;
- concurrency and closed-child evidence;
- root work performed to validate each oracle;
- any root rework caused by a child result;
- compaction events if observable.

Do not persist private chain-of-thought or full child transcripts.

## Scoring and pilot decision

Each first-attempt child receives probe PASS/FAIL using the frozen oracle above.

Compute these summaries:

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

Final `pilot_decision` is one of:

### `QUALIFIED`

All of the following:

- CONTROL passes all 3 probes;
- ADAPTIVE passes all 3 probes on first attempt;
- adaptive escalation count = 0;
- no material false negative or invented material finding;
- the host verifies effective model + reasoning for all three adaptive children;
- the verified adaptive profiles are genuinely below the root-equivalent CONTROL profile for P1/P2 and lower-model for P3;
- no safety/authority/branch incident.

`QUALIFIED` supports specifying a later normative child-routing decision/adapter refinement. It does **not** by itself prove a precise percentage token/cost saving unless corresponding usage telemetry is available.

### `QUALIFIED_QUALITY_OBSERVABILITY_LIMITED`

- both arms pass all probes at the required quality;
- no escalation/material finding regression;
- requested adaptive overrides were accepted by the host;
- but effective profile identity and/or attributable usage telemetry is insufficient for a verified quantitative routing claim.

This result supports the task-class quality hypothesis but requires a more observable host/run before policy may claim verified lower compute or savings.

### `NOT_QUALIFIED`

Use when the adaptive first-attempt arm has a material quality regression, required escalation, false negative on P3, or other result that defeats minimum-sufficient-compute qualification.

### `BLOCKED_CAPABILITY`

Use when the host cannot request child-specific model and reasoning overrides sufficiently to execute the experiment.

## Acceptance criteria

- **AC-T054-1:** D042 passes before authority/probe execution; root launch is NEW and fixed at the authorized root profile.
- **AC-T054-2:** capability preflight is recorded without inventing unsupported host features.
- **AC-T054-3:** exactly the frozen matched P1/P2/P3 task classes are evaluated with root-equivalent CONTROL and explicit ADAPTIVE profiles unless capability-blocked.
- **AC-T054-4:** matched-arm context/tool access is equivalent; `fork_turns=none` is used to isolate compute routing.
- **AC-T054-5:** P1/P2 deterministic oracles are independently computed by the root; P3 uses the frozen ephemeral isolation defect without tracked mutation or oracle leakage in the child message.
- **AC-T054-6:** all first-attempt results, retries/escalations and oracle scores are preserved honestly; no failed adaptive result is overwritten by escalation.
- **AC-T054-7:** requested and effective profile/usage telemetry is persisted when observable; unavailable values are explicit `null` with reasons.
- **AC-T054-8:** all children are fresh, read-only and closed; max concurrent children `<=2`; no tracked product-code mutation occurs.
- **AC-T054-9:** final handoff computes one frozen `pilot_decision` and avoids quantitative savings claims unsupported by effective-profile/token evidence.
- **AC-T054-10:** no authority leakage, Executor-authored Markdown, static `.codex/agents/` pilot catalog, or D055 change occurs.

## Verification

Minimum root verification:

- exact current Git identity and clean/read-only baseline;
- deterministic P1 source/LOC/config calculation;
- deterministic P2 AST/dependency + symbol ownership calculation;
- P3 fixture digest and same-process reproduction of the seeded contamination independent of child output;
- evidence JSON validity;
- `git diff --check` for authorized evidence branch changes;
- final branch diff contains only T054 non-Markdown handoff/telemetry evidence unless an explicit Orchestrator re-entry authorizes otherwise.

## Non-goals

T054 does not:

- refactor product code;
- test persistent-root continuity;
- test write-capable Worker routing;
- optimize `fork_turns` as a separate causal variable;
- change D055 or consumer governance policy;
- establish provider-independent model names;
- require custom agents or `.codex/agents/`;
- claim token/cost savings when the host does not expose attributable evidence.

A later pilot may extend validated routing to write-capable Worker tasks after this read-only calibration.

## Ownership and handoff

ChatGPT Orchestrator owns this Task Contract, frozen probes/oracles, acceptance and any later policy decision.

Executor owns D042 execution mechanics, child spawning/configuration, ephemeral fixture mechanics within the frozen specification, deterministic oracle execution, telemetry/handoff JSON, and Git mechanics for the authorized evidence branch.

Persist:

- `handoffs/T054-adaptive-routing-telemetry.json`;
- `handoffs/T054-executor-handoff.json`.

Final handoff must include root/branch/base/HEAD, capability preflight, per-child requested/effective profiles, probe scores, escalation evidence, usage/duration telemetry, final `pilot_decision`, verification, unresolved issues, and no-authority-leakage statement.

Return only:

```text
STATUS: DONE | BLOCKED
HANDOFF: handoffs/T054-executor-handoff.json
BRANCH: <branch>
HEAD: <pushed-head>
```
