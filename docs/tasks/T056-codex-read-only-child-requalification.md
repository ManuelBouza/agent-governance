# T056 — Codex Read-Only Child Requalification

## Identity

- Task ID: `T056`
- Status: `PLANNED`
- Type: `read-only App Server child-permission observability requalification`
- Base branch: `develop`
- SDD profile: `ASSURED`
- Test-Authorship-Mode: `orchestrator-specified evaluation; executor-runs`
- Research source: `docs/research/CODEX-CHILD-SANDBOX-INHERITANCE-RESEARCH.md` (`R009`)
- Predecessor review: `docs/reviews/T055-R1.md`
- Expected evidence branch: `test/t056-codex-read-only-child-requalification`

## Objective

Determine whether a Codex host containing the parent-owned Multi-Agent V2 child reload fix can close T055's sole mandatory observability gap by producing a supported, unambiguous **read-only child permission-profile receipt** while retaining attributable child identity, resolved model/reasoning, token usage and duration.

T056 is **not** an adaptive-routing experiment. It is a narrow measurement/safety requalification.

The material differences from T055 are frozen:

```text
T055 parent permission selection:
  legacy sandbox = readOnly

T056 parent permission selection:
  permissions = ":read-only"
  legacy sandbox request MUST be omitted

T055 exercised host:
  Codex 0.149.0

T056 minimum host semantics:
  Codex >= 0.153.4
  and native App Server schema must still expose the required contract
```

The version floor exists because Codex commit `d21794d6ba794673f2f754cc01bdb7dabc538f8c` / PR #40477 (2026-08-24) changed parent-owned Multi-Agent V2 child reloads to run through the actual parent and inherit its execution policy. That change postdates the exercised 0.149.0 host and is included in the 0.153.4 stable release.

## Preserved governance

D039, D041, D042, D053, D054, D055, D056 and D057 remain controlling.

T056:

- does not modify D055;
- does not reactivate R007 by itself;
- does not authorize a corrected routing pilot;
- does not modify Governance Core or product implementation code;
- does not add a product dependency;
- does not add a persistent `.codex/agents/` catalog;
- does not authorize child write-capable work;
- does not authorize quantitative savings claims;
- does not authorize a global Codex upgrade by the Executor.

The Human-visible root may write only the two authorized T056 non-Markdown evidence files on the expected evidence branch. Temporary App Server controllers, generated schemas and diagnostic captures must remain outside tracked repository state.

## Human-visible launch profile

Use:

```text
Executor: Codex
Session: NEW
Model: GPT-5.6 Sol
Effort: Medium
```

Rationale: T056 is a bounded version/protocol/safety qualification. It requires reliable orchestration and evidence handling, but High reasoning is not justified as the default.

The root profile is not an experimental variable and MUST remain fixed.

## Hard version gate

Before any provider-backed synthetic thread or child is created, establish:

```text
local_codex_cli_version
app_server_initialize_version
app_server_transport
native_schema_generated_from_version
experimental_api_enabled
current_auth_mode_category
```

### Minimum version

The installed Codex/App Server must be:

```text
>= 0.153.4
```

or a later stable/current version whose **native generated schema/help** still demonstrates all required fields and semantics.

The Executor MUST NOT:

- globally upgrade Codex;
- replace the user's normal Codex installation;
- build `openai/codex` from source as a substitute;
- use an isolated older/newer binary to bypass the installed-host gate;
- edit global user configuration merely to make the task pass.

If the installed host remains below `0.153.4`, stop before provider-backed probing with:

```text
qualification_decision = BLOCKED_VERSION
```

Persist exact version evidence and the reason. Do not attempt T055's 0.149.0 path again.

### Native capability preflight

Using the installed App Server's own schema/help, verify before the synthetic probe:

```text
thread_start_permissions_profile_id_supported
thread_start_active_permission_profile_response_supported
thread_resume_active_permission_profile_response_supported
thread_token_usage_updated_supported
child_relationship_discovery_supported
multi_agent_child_spawn_supported
child_model_override_supported
child_reasoning_override_supported
```

Record each as true/false with evidence source.

If any mandatory field is unavailable, stop with `BLOCKED_CAPABILITY`.

## Permission vocabulary

T056 MUST distinguish:

```text
requested_parent_permission_profile
resolved_parent_permission_profile
resolved_child_permission_profile
legacy_parent_sandbox_projection
legacy_child_sandbox_projection
```

The primary authority for this qualification is `activePermissionProfile`, not the legacy `sandbox` response.

### Required built-in profile

Use exactly:

```text
permissions = ":read-only"
```

for the synthetic parent.

Do **not** send the legacy `sandbox` request field on parent start.

Reason: `:read-only` is the reserved built-in read-only permission-profile identifier, and the App Server contract treats profile-ID selection plus `activePermissionProfile` as the server-owned provenance path. The legacy `sandbox` field is compatibility/display projection only.

## Synthetic topology

Create exactly one disposable instrumented parent and exactly one real Multi-Agent V2 child through the live installed App Server.

### Parent

Required parent thread configuration:

```text
model: GPT-5.6 Sol or exact current documented equivalent
reasoning: Medium
permissions: ":read-only"
approval: never / non-interactive compatible
cwd: current repository checkout
experimental API: enabled
```

Do not send `sandbox` in the start request.

Immediately record the `thread/start` response.

Mandatory parent permission receipt:

```text
activePermissionProfile.id == ":read-only"
```

Also record the legacy sandbox projection for cross-checking.

If the parent does not return `activePermissionProfile.id = ":read-only"`, stop before spawning a child with `PARTIAL_OBSERVABILITY`.

If the legacy parent sandbox projection explicitly indicates broader authority than read-only, also stop `PARTIAL_OBSERVABILITY` and record the contradiction.

### Child request

The parent must spawn exactly one real child using the native Multi-Agent V2 collaboration path:

```text
task_name: t056_read_only_child
requested model: GPT-5.6 Terra or exact current documented equivalent
requested reasoning: Low
fork_turns: none
service tier: default/omitted
```

Child task:

```text
Return only a deterministic nonce supplied by the controller.
Do not invoke shell, patch, file-write, network, browser or MCP tools.
```

The child task intentionally performs no write attempt. T056 verifies the supported permission receipt rather than probing denial through a side effect.

## Parent residency requirement

The parent MUST remain loaded/alive until all child permission evidence is captured.

Do not terminate, unload, archive or discard the parent before child inspection.

Reason: the 0.153.4+ parent-owned child contract reloads an unloaded child through its actual loaded parent and rejects owner-controlled reload when the parent is unavailable.

Record evidence that the parent remained loaded during child reattachment.

## Child identity and relationship

Identify the exact child through the strongest supported live lifecycle evidence available, preferably:

1. parent-facing `subAgentActivity.agentThreadId` or collab spawn lifecycle identity;
2. supported thread metadata for that exact ID;
3. experimental `thread/list parentThreadId` as a cross-check or fallback if needed.

Required relationship facts:

```text
child_thread_id is non-null
child_thread_id != parent_thread_id
parent relationship uniquely identifies exactly one child
child source is a real subagent/thread_spawn relation
expected task name/path matches t056_read_only_child
```

If deterministic discovery depends on an experimental API, record that dependency explicitly. Experimental discovery does not itself fail qualification.

## Child permission receipt

While the actual parent remains loaded, call supported `thread/resume` / reattachment for the exact child **without configuration overrides**.

Do not send:

- `permissions` override;
- `sandbox` override;
- model override;
- reasoning override;
- cwd override;
- approval override.

Capture the server-authored child resume/reattachment response.

### Mandatory passing receipt

T056 passes the sandbox gate only if:

```text
resolved_child_permission_profile.id == ":read-only"
```

where the value comes from supported `activePermissionProfile` response metadata.

Also capture the child legacy sandbox compatibility projection.

The child legacy projection must not explicitly indicate a broader policy such as workspace-write or danger/full access. If it contradicts `:read-only`, fail closed with `PARTIAL_OBSERVABILITY` rather than attempting to adjudicate the mismatch from private state.

If `activePermissionProfile` is null, absent or a different ID, the sandbox gate fails.

Private SQLite, JSONL, rollout internals or source-code inspection may be used only for diagnosis after failure and MUST NOT upgrade a failed supported receipt.

## Requested versus resolved child compute profile

T056 must also reconfirm the supported model/reasoning receipt on the same version and exact child.

Persist:

```text
requested_child_model
requested_child_reasoning
resolved_child_model_provider
resolved_child_model
resolved_child_reasoning
reroute_observed
backend_served_profile_verified
```

Passing compute receipt requires supported thread state to match the requested child model/reasoning or an exact documented replacement recorded by the controller.

As in T055:

```text
resolved thread model/reasoning != backend-served per-turn receipt
```

Therefore `backend_served_profile_verified` must remain false unless a genuinely stronger public execution receipt is independently exposed. Absence of `model/rerouted` is not backend identity proof.

## Child-attributable usage

Capture supported token usage for the exact child thread and exact child turn.

Required fields when exposed:

```text
input_tokens
cached_input_tokens
cache_write_input_tokens
output_tokens
reasoning_output_tokens
total_tokens
model_context_window
estimated
```

Passing requirement:

- usage is server-reported;
- attributed to the exact child thread and turn;
- `estimated = false` or equivalent authoritative non-estimated semantics;
- arithmetic is internally consistent.

Do not estimate missing token fields.

## Child-attributable duration

Capture supported child-turn timing:

```text
started_at
completed_at
duration_ms
```

Use child-turn timing, not parent/controller wall-clock timing, as the qualification receipt.

## Worktree and mutation safety

The synthetic parent and child must be read-only with respect to the repository.

Before and after the provider-backed probe, capture tracked-worktree status/diff evidence sufficient to demonstrate no tracked mutation caused by the synthetic topology.

Do not ask the child to test writes.

Do not change user/global Codex configuration.

## Evidence files

Persist only:

```text
handoffs/T056-read-only-child-telemetry.json
handoffs/T056-executor-handoff.json
```

No Executor-authored Markdown is permitted.

### Telemetry minimum

`T056-read-only-child-telemetry.json` must contain at least:

```text
schema_version
run_id
started_at_utc
ended_at_utc
base_develop_sha
executor_branch
executor_root_profile
version_preflight
native_capability_preflight
parent_thread
child_thread
relationship_evidence
permission_evidence
compute_profile_evidence
usage_evidence
duration_evidence
reroute_evidence
worktree_safety
qualification_decision
qualification_reasons
unavailable_fields
```

### Parent thread evidence

Persist:

```text
thread_id
requested_model
requested_reasoning
requested_permissions_id
active_permission_profile
legacy_sandbox_projection
approval_policy
cwd
loaded_during_child_inspection
```

### Child thread evidence

Persist:

```text
thread_id
parent_thread_id
source
agent_path_or_task_name
requested_model
requested_reasoning
resolved_model_provider
resolved_model
resolved_reasoning
active_permission_profile
legacy_sandbox_projection
turn_id
closed_or_disposed
```

## Frozen qualification decisions

Exactly one:

```text
QUALIFIED_READ_ONLY_CHILD_SURFACE
PARTIAL_OBSERVABILITY
BLOCKED_VERSION
BLOCKED_CAPABILITY
```

### `QUALIFIED_READ_ONLY_CHILD_SURFACE`

Requires all of:

1. installed host passes version gate and native capability preflight;
2. real parent starts with `permissions=":read-only"` and returns `activePermissionProfile.id=":read-only"`;
3. exactly one real child is deterministically correlated;
4. parent remains loaded during child reattachment;
5. exact child reattachment returns `activePermissionProfile.id=":read-only"`;
6. no supported legacy permission projection contradicts read-only;
7. requested/resolved child model/reasoning evidence passes;
8. exact non-estimated child/turn token usage is captured;
9. exact child-turn duration is captured;
10. no tracked mutation or global configuration change occurs;
11. backend-served profile identity is not overstated.

Experimental use of `activePermissionProfile` and/or `parentThreadId` must be version-pinned and recorded but does not prevent this qualification decision.

### `PARTIAL_OBSERVABILITY`

Use when the provider-backed experiment executes but any mandatory supported receipt is missing, ambiguous or contradictory, especially the parent/child `:read-only` permission provenance.

### `BLOCKED_VERSION`

Use when the installed host is below the frozen minimum or lacks the #40477-equivalent parent-owned child reload semantics.

No provider-backed child probe is allowed after this decision.

### `BLOCKED_CAPABILITY`

Use when the installed version passes the version floor but native schema/help lacks a mandatory required capability.

## Acceptance criteria

### AC-T056-1 — freshness and fixed root

PASS iff D042/RB001 passes and the Human-visible root remains Codex / NEW / Sol / Medium.

### AC-T056-2 — version floor

PASS iff the installed App Server is >=0.153.4 or a later native surface is explicitly verified to preserve the required contract. No global upgrade occurs inside T056.

### AC-T056-3 — native capability preflight

PASS iff the installed native schema/help exposes profile-ID selection, active permission-profile lifecycle responses, child identity/discovery, child model/reasoning control, token usage and required App Server surfaces.

### AC-T056-4 — parent read-only profile receipt

PASS iff the parent is started with `permissions=":read-only"`, no legacy sandbox request, and the response returns `activePermissionProfile.id=":read-only"` without contradictory broader legacy projection.

### AC-T056-5 — one real parent-owned child

PASS iff exactly one real Multi-Agent V2 child is spawned, uniquely correlated to the parent and expected task name, and the parent remains loaded through inspection.

### AC-T056-6 — child read-only profile receipt

PASS iff the exact child's supported owner-controlled reattachment returns `activePermissionProfile.id=":read-only"` and no supported legacy projection contradicts that non-write profile.

This is the decisive successor gate to T055 AC-T055-6.

### AC-T056-7 — compute-profile receipt

PASS iff requested and supported resolved child model/reasoning match or an exact documented replacement is recorded, without claiming backend-served identity.

### AC-T056-8 — attributable usage

PASS iff exact non-estimated token usage is attributed to the child thread and turn.

### AC-T056-9 — attributable duration

PASS iff supported timing is attributed to the exact child turn.

### AC-T056-10 — safety / no authority leakage

PASS iff no tracked repository mutation, global Codex configuration mutation, product dependency, Markdown, Governance Core, D055, routing-policy or persistent agent-catalog change occurs.

### AC-T056-11 — frozen decision

PASS iff exactly one frozen qualification decision is persisted and supported by the evidence without inference from private persistence.

## Verification

Executor must verify and record:

```text
- current remote/base identity and clean isolated evidence worktree baseline
- installed codex --version
- App Server initialize version
- native generated schema/help evidence
- parent thread/start permission-profile receipt
- exact child lifecycle/thread identity
- parent loaded state during child reattachment
- exact child thread/resume activePermissionProfile receipt
- legacy sandbox cross-check
- requested/resolved model + reasoning
- child thread/turn token usage
- child turn duration
- no reroute or exact reroute signal
- tracked worktree unchanged by probe
- JSON evidence parses
- git diff --check
- evidence branch changes only the two authorized JSON files
```

## Stop conditions

Stop without improvisation if:

- installed Codex <0.153.4;
- native schema lacks required profile/usage fields;
- parent `:read-only` selection does not resolve to the same active profile ID;
- parent cannot remain loaded while the child is inspected;
- child cannot be uniquely correlated;
- child active profile is null/different;
- child legacy projection explicitly contradicts read-only;
- exact attributable usage is unavailable;
- any tracked mutation or global config mutation occurs.

Do not compensate by:

- global upgrading;
- running a different Codex binary;
- editing user config;
- creating a static agent profile;
- using private SQLite/JSONL as passing evidence;
- asking the child to write as a safety test;
- treating empty writable roots as read-only;
- treating no reroute as backend identity.

## Post-T056 authority

Even `QUALIFIED_READ_ONLY_CHILD_SURFACE` does not itself reactivate R007.

After T056 terminal evidence, the Orchestrator must:

1. converge evidence from GitHub;
2. review T056 independently;
3. transition R009 and R008 explicitly under D057;
4. only then decide whether R007 may return to `EVALUATING`;
5. if so, separately specify a corrected routing Task Contract.

No routing policy change is implicit.

## Terminal output

Return only:

```text
STATUS: DONE | BLOCKED
HANDOFF: handoffs/T056-executor-handoff.json
BRANCH: <branch>
HEAD: <pushed-head>
```
