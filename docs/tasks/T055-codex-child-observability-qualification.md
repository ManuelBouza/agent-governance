# T055 — Codex Child Observability Qualification

## Identity

- Task ID: `T055`
- Status: `PLANNED`
- Type: `read-only host/App-Server observability qualification`
- Base branch: `develop`
- SDD profile: `ASSURED`
- Test-Authorship-Mode: `orchestrator-specified evaluation; executor-runs`
- Research source: `docs/research/CODEX-CHILD-OBSERVABILITY-SURFACE-RESEARCH.md` (`R008`)
- Predecessor review: `docs/reviews/T054-R1.md`
- Expected evidence branch: `test/t055-codex-child-observability-qualification`

## Objective

Determine whether the **actual installed Codex host available to the Executor** exposes a sufficiently supported and attributable measurement surface for a future adaptive-child-routing experiment.

T055 does **not** test routing quality or savings. It tests only the measurement substrate.

The qualification must demonstrate whether one real spawned child can be correlated to:

1. a child thread identity and parent relationship;
2. a resolved/configured child model and reasoning effort;
3. the child's sandbox state;
4. attributable token usage by child thread and turn;
5. attributable duration;
6. exact Codex/App Server/SDK version provenance;
7. any observable model-reroute signal.

T055 exists because T054's direct Human-visible collaboration surface accepted child model/reasoning overrides but did not expose effective-profile receipts or attributable token usage. R008 found that current Codex 0.153.4 App Server / Python SDK surfaces are materially stronger and justify a bounded live qualification before any corrected routing pilot.

## Preserved governance

D039, D041, D042, D053, D054, D055, D056 and D057 remain controlling.

T055:

- does not modify D055;
- does not reactivate R007 by itself;
- does not adopt a global child-routing policy;
- does not test persistent-root policy;
- does not modify Governance Core;
- does not modify product implementation code;
- does not add a product runtime dependency;
- does not create a persistent project `.codex/agents/` catalog;
- does not authorize a token/cost-saving claim.

The Human-visible Executor root may write only the authorized T055 non-Markdown evidence files on the expected evidence branch. Any controller scripts, temporary SDK environments, App Server message captures, or disposable agent configuration used to conduct the qualification MUST remain outside tracked repository state unless this Task Contract explicitly names them as evidence content embedded inside the authorized JSON telemetry.

## Human-visible launch profile

Use:

```text
Executor: Codex
Session: NEW
Model: GPT-5.6 Sol
Effort: Medium
```

Rationale: the root coordinates a bounded protocol/observability experiment, performs D042/version verification, and evaluates evidence. This requires reliable technical orchestration but does not justify High reasoning as a default.

The Human-visible root profile is not the experimental variable and MUST remain fixed during T055.

## Measurement vocabulary

T055 MUST distinguish these fields and MUST NOT collapse them:

```text
requested_profile
resolved_thread_profile
reroute_observed
backend_served_profile
```

Definitions:

- `requested_profile`: model/reasoning explicitly requested for the child spawn.
- `resolved_thread_profile`: model/reasoning reported by the supported child `Thread` / App Server surface after configuration layering.
- `reroute_observed`: whether a supported `model/rerouted` event was observed for the child turn, including from/to/reason when available.
- `backend_served_profile`: authoritative provider-served model/reasoning receipt for the actual response, if a public supported surface exposes one.

R008 established that `Thread.model` / `Thread.reasoningEffort` are configured/persisted thread state and are explicitly not documented as per-turn execution telemetry. Therefore:

```text
resolved_thread_profile_verified = true
```

MUST NOT be reported as:

```text
backend_served_profile_verified = true
```

unless T055 actually obtains a stronger public authoritative receipt.

## Version and surface preflight

Before any provider-backed probe, establish and persist:

```text
local_codex_cli_version
app_server_initialize_version
app_server_protocol_version_or_capabilities
python_sdk_used
python_sdk_version
python_sdk_pinned_runtime_version_if_exposed
app_server_transport
experimental_api_enabled
experimental_features_used
current_auth_mode_category
```

Rules:

- do not record secrets, tokens, account identifiers or credential material;
- record auth only as a coarse category needed to understand capability, such as `chatgpt`, `api_key`, `unknown`;
- prefer the current installed stable Codex/App Server surface;
- if the installed surface is older than the R008 characterized 0.153.4 baseline, first determine from native help/schema whether equivalent required fields are present;
- do not upgrade the user's global Codex installation merely to make T055 pass;
- if a Python SDK is needed and not already available, the Executor MAY use an isolated temporary environment outside the repository with a stable version compatible with the actual App Server/runtime; do not change `pyproject.toml`, `uv.lock`, repository `.venv`, or product dependencies;
- direct App Server JSON-RPC is an acceptable alternative to the Python SDK;
- do not build `openai/codex` from source as a substitute for testing the installed host;
- source-code inspection may characterize behavior but cannot replace the live qualification.

If no installed/compatible App Server or SDK surface can be exercised without changing product dependencies or global user configuration, stop with `BLOCKED_CAPABILITY`.

## Synthetic parent/child topology

T055 MUST create one disposable **instrumented parent thread** through the live App Server/SDK surface and cause that parent to spawn exactly one real multi-agent child.

Do not use an unrelated second top-level thread as a fake child.

### Instrumented parent

Required parent configuration:

```text
Model: GPT-5.6 Sol or exact current documented equivalent
Reasoning: Medium
Sandbox: read-only
Approval: non-interactive/no-write compatible setting
Working directory: current repository checkout, read-only for the synthetic agent
```

If the exact model name differs on the installed host, record the exact available replacement and why. Do not silently substitute.

### Child request

The parent must be instructed to spawn exactly one bounded child using the real collaboration/multi-agent path with:

```text
Task name: t055_observability_child
Requested model: GPT-5.6 Terra or exact current documented equivalent
Requested reasoning: Low
Context fork: none
Requested service tier: default/omitted
Child task: deterministic nonce-only bounded task
```

The prepared child task MUST be independent of repository semantic knowledge. Use a deterministic nonce such as:

```text
T055-OBSERVABILITY-CHILD-OK
```

and require the child to return that nonce exactly after one minimal read-only action or reasoning step. The task is intentionally trivial because T055 tests instrumentation, not model quality.

The parent prompt MUST explicitly require a real child spawn and must not itself answer the child task instead.

If the actual collaboration spawn schema cannot request child model and reasoning explicitly, stop with `BLOCKED_CAPABILITY`; do not emulate with a second Human-visible root or unrelated top-level thread.

## Child discovery

After child completion, identify the exact child thread using supported App Server/SDK thread records.

Preferred order:

1. use stable/public thread enumeration restricted to subagent source kinds and correlate returned `parentThreadId` with the known instrumented parent;
2. if necessary, enable the documented experimental `parentThreadId` relation filter and record that dependency;
3. do not use internal SQLite/JSONL scraping as the primary discovery mechanism.

Private/internal persistence MAY be inspected only as a diagnosis cross-check after a supported-surface failure, and if used it must be explicitly marked `diagnostic_only` and cannot upgrade the qualification outcome.

The discovered child must satisfy:

```text
child_thread_id != parent_thread_id
child.parent_thread_id == parent_thread_id
child source is a subagent/thread-spawn source compatible with the actual host
exactly one matching T055 child exists
```

Multiple ambiguous matching children without deterministic disambiguation fail the discovery gate.

## Resolved/configured child profile receipt

Using the supported child `Thread` record and/or `thread/resume` with **no model/reasoning override**, record:

```text
child_model_provider
child_model
child_reasoning_effort
child_agent_role
child_agent_nickname
child_cli_version
```

The qualification requires:

```text
child_model == requested_child_model_or_recorded_documented_equivalent
child_reasoning_effort == requested_reasoning
resolved_thread_profile_verified = true
```

If resume is used, prove no model/reasoning override was sent during observation.

Do not treat provider/model aliases as equal unless the host/documentation explicitly identifies the relationship; record the exact values.

## Sandbox/capability receipt

Obtain the child's sandbox state from a supported App Server/SDK response. `thread/resume` with no sandbox override is acceptable if needed to obtain the response envelope.

Record:

```text
child_sandbox_policy
child_active_permission_profile_if_exposed
direct_spawn_sandbox_override_supported
sandbox_receipt_source
```

The synthetic parent is read-only, so the expected child sandbox is read-only by inheritance unless the host explicitly documents/resolves a different safe representation.

Qualification requires a supported receipt showing the child remains within a non-write sandbox.

`direct_spawn_sandbox_override_supported` is informational for T055 and may be `false`; it does not fail T055 if inherited read-only state is supported and observable.

Do not create a persistent `.codex/agents/` catalog solely to force a child sandbox override.

## Token usage attribution

Collect the supported child token-usage record.

Preferred evidence:

```text
thread/tokenUsage/updated
```

including a notification replay after attaching/resuming the completed child when the host supports it.

Persist:

```text
usage_thread_id
usage_turn_id
total_tokens
input_tokens
cached_input_tokens
cache_write_input_tokens
output_tokens
reasoning_output_tokens
model_context_window
usage_receipt_source
```

Requirements:

- `usage_thread_id` MUST equal the discovered `child_thread_id`;
- `usage_turn_id` MUST correspond to the child's bounded task turn;
- token fields MUST come from the supported host record and MUST NOT be estimated;
- integer zero is valid where the host reports zero;
- unavailable optional fields must be `null` plus a reason;
- `total_tokens` and the principal input/output fields must be non-null for qualification.

If token usage is available only for the parent or aggregate session and cannot be attributed to the child thread/turn, T055 cannot qualify the measurement surface.

## Duration attribution

From the supported child turn/thread result, persist:

```text
child_turn_started_at
child_turn_completed_at
child_turn_duration_ms
```

`child_turn_duration_ms` must be non-null for qualification. Do not reconstruct a synthetic duration from parent wall-clock timestamps when the supported child turn already exposes duration.

## Model reroute observation

Record:

```text
model_reroute_signal_supported
reroute_observed
reroute_from_model
reroute_to_model
reroute_reason
```

If the host exposes `model/rerouted`, observe it when possible during the synthetic run. Absence of a captured reroute event is **not** sufficient to claim backend-served-profile verification.

A reroute event does not automatically fail observability qualification; it must instead be persisted because it materially changes how future routing experiments interpret `requested_profile` and `resolved_thread_profile`.

## Backend-served profile

Record:

```text
backend_served_model
backend_served_reasoning_effort
backend_served_profile_verified
backend_served_profile_receipt_source
```

Default expectation from R008:

```text
backend_served_profile_verified = false
```

with a reason that the supported `Thread` fields are configured/persisted state rather than per-turn backend execution telemetry.

T055 may set this true only if the actual current public host supplies an authoritative provider-execution receipt. Internal analytics, private database fields, guessed aliases or absence of a reroute event are insufficient.

This field is **not required** for T055 measurement-surface qualification. Its purpose is to keep later claims honest.

## Evidence artifacts

Persist only:

- `handoffs/T055-child-observability-telemetry.json`;
- `handoffs/T055-executor-handoff.json`.

Both must be valid JSON.

The telemetry must include at minimum:

```text
schema_version
recorded_at_utc
canonical_develop_sha
d042_result
executor_root_profile
version_preflight
surface_selection
instrumented_parent
child_spawn_request
child_discovery
resolved_thread_profile
sandbox_receipt
child_token_usage
child_duration
reroute_observation
backend_served_profile
tracked_worktree_postcondition
qualification_decision
qualification_reasons
limitations
```

Do not persist credentials, hidden reasoning, chain-of-thought, full child transcripts, or private raw rollout contents.

A concise prepared parent/child prompt or deterministic prompt digest may be stored for reproducibility.

## Qualification decisions

Final `qualification_decision` MUST be exactly one of:

```text
QUALIFIED_STABLE_SURFACE
QUALIFIED_WITH_EXPERIMENTAL_DISCOVERY
PARTIAL_OBSERVABILITY
BLOCKED_CAPABILITY
```

### `QUALIFIED_STABLE_SURFACE`

Use only when all required gates pass without relying on experimental relation filters or internal persistence as a correctness dependency:

- real child identity/parent relation established;
- requested model/reasoning accepted;
- supported child thread receipt matches requested/equivalent model and reasoning;
- non-write child sandbox receipt obtained;
- attributable child token usage obtained by exact child thread/turn;
- child duration obtained;
- version provenance complete;
- no tracked product mutation;
- no internal/private persistence needed for the passing evidence.

### `QUALIFIED_WITH_EXPERIMENTAL_DISCOVERY`

Use only when all measurement gates above pass, but deterministic child discovery required the documented experimental `parentThreadId` / `ancestorThreadId` relation filter.

This outcome is sufficient to consider a controlled successor routing evaluation, but the experimental dependency must remain explicit and version-pinned.

### `PARTIAL_OBSERVABILITY`

Use when the host provides useful supported telemetry but one or more required measurement gates are missing, including:

- resolved child model/reasoning receipt unavailable or mismatched;
- child sandbox receipt unavailable;
- token usage cannot be attributed to the child thread/turn;
- child duration unavailable;
- child relationship cannot be established without internal persistence.

Do not upgrade a partial result using internal SQLite/JSONL evidence.

### `BLOCKED_CAPABILITY`

Use when the actual host cannot exercise the required real multi-agent + App Server/SDK path at all, including incompatible installed version, unavailable App Server/SDK surface, unavailable child model/reasoning override, or an environmental capability block before useful measurement evidence exists.

## Acceptance criteria

### AC-T055-1 — Fresh authoritative baseline

PASS when D042/RB001 succeeds against current canonical `develop` and the Human-visible root uses the frozen NEW / Sol / Medium profile.

### AC-T055-2 — Exact version provenance

PASS when local Codex/App Server/SDK identities and relevant capability flags are recorded without secrets.

### AC-T055-3 — Real child topology

PASS when one real multi-agent child is spawned and deterministically correlated to its instrumented parent through supported thread records.

### AC-T055-4 — Requested vs resolved profile separation

PASS when requested child model/reasoning and supported resolved thread model/reasoning are both persisted and equality/equivalence is explicitly evaluated.

### AC-T055-5 — Honest backend receipt boundary

PASS when configured/resolved thread profile is not mislabeled as backend-served execution identity; `backend_served_profile_verified` is false unless a genuinely stronger public receipt exists.

### AC-T055-6 — Sandbox receipt

PASS when a supported child sandbox receipt demonstrates a non-write child envelope and direct per-spawn sandbox override capability is separately recorded.

### AC-T055-7 — Child-attributable usage

PASS when supported token telemetry is attributable to the exact child thread and task turn, with non-estimated token counts.

### AC-T055-8 — Child-attributable duration

PASS when the supported child turn exposes non-null duration/timestamps.

### AC-T055-9 — No private telemetry dependency

PASS when internal JSONL/SQLite/source inspection is not required to produce a passing qualification. Diagnostic-only inspection after a supported-surface failure is allowed but cannot upgrade the result.

### AC-T055-10 — No authority or product leakage

PASS when no Governance Core, D055, product code, product dependency, committed Markdown, persistent `.codex/agents/` catalog, routing policy or tracked implementation artifact is modified by the Executor.

### AC-T055-11 — Frozen outcome

PASS when exactly one qualification decision is persisted and unsupported compute/cost/profile claims are absent.

## Verification

Before terminal handoff, verify:

- current Git identity and D042 baseline evidence;
- exactly the two authorized T055 JSON evidence files differ from the task base;
- both JSON files parse successfully;
- child identity/parent correlation consistency;
- requested vs resolved profile values;
- sandbox receipt provenance;
- token usage `threadId` / `turnId` attribution;
- duration provenance;
- no credentials or private raw traces in evidence;
- `git diff --check`;
- no tracked product/Markdown/dependency changes.

## Non-goals

T055 does not:

- compare CONTROL vs ADAPTIVE model quality;
- rerun P1/P2/P3;
- fix T054's P2 probe;
- select a routing policy;
- measure persistence benefit;
- claim USD savings;
- require backend-served model identity if the public host does not expose it;
- modify provider configuration globally;
- upgrade the user's global Codex installation;
- add repository dependencies;
- create a reusable custom-agent catalog.

## Re-entry conditions

Stop for Orchestrator re-entry rather than redesigning T055 if:

- the installed Codex/App Server surface materially differs from R008 and the required fields have moved/changed semantics;
- a supported measurement field would require product/dependency mutation;
- the actual child-spawn surface cannot request the frozen child model/reasoning profile;
- the only available path to child identity/model/usage is private persistence scraping;
- a material security/credential issue arises;
- the Task Contract's measurement vocabulary is insufficient for an observed new form of routing/fallback.

## Ownership

ChatGPT Orchestrator owns:

- R008 interpretation;
- T055 measurement semantics;
- qualification gates;
- requested-vs-resolved-vs-backend distinction;
- final convergence and research-state transition.

Agente de IA Ejecutor owns:

- D042 execution;
- native installed-version and capability discovery;
- App Server/SDK invocation mechanics per D054;
- ephemeral external-to-repo controller/environment mechanics;
- synthetic parent/child execution exactly inside this contract;
- telemetry/handoff JSON;
- branch/commit/push mechanics;
- technical verification.

## Required terminal output

Return only:

```text
STATUS: DONE | BLOCKED
HANDOFF: handoffs/T055-executor-handoff.json
BRANCH: <branch>
HEAD: <pushed-head>
```
