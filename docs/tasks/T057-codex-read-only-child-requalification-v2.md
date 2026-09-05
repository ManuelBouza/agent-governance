# T057 — Codex Read-Only Child Requalification v2

## Identity

- Task ID: `T057`
- Status: `PLANNED`
- Type: `read-only App Server child-permission observability requalification successor`
- Base branch: `develop`
- SDD profile: `ASSURED`
- Test-Authorship-Mode: `orchestrator-specified evaluation; executor-runs`
- Research source: `docs/research/CODEX-CHILD-SANDBOX-INHERITANCE-RESEARCH.md` (`R009`)
- Predecessor review: `docs/reviews/T056-R1.md`
- Expected evidence branch: `test/t057-codex-read-only-child-requalification-v2`

## Objective

Complete the same read-only child permission qualification attempted by T056, correcting only the temporary controller's `thread/loaded/list` parsing/parent-residency defect.

T057 is not a routing experiment and does not change the R009 research question.

## Preserved experimental design

Freeze all material T056 controls:

```text
installed Codex/App Server: >= 0.153.4
Human-visible root: GPT-5.6 Sol / Medium
parent permissions: ":read-only"
legacy sandbox request: omitted
child requested model: GPT-5.6 Terra
child requested reasoning: Low
fork_turns: none
provider-backed parent count: 1
real child count: 1
```

No model-family migration to GPT-6 Astra is allowed in T057. R010 remains separate research and is not part of this experiment.

## Controller correction

Before any provider-backed probe, generate/use the installed App Server's native schema/help to resolve the exact `thread/loaded/list` response shape.

The controller MUST treat the response according to the installed schema. On Codex 0.153.4 the known observed shape is a collection of thread ID strings, not thread objects.

Required controller behavior:

1. parse loaded-thread identifiers without assuming object fields;
2. verify the parent thread ID is present while the child is being inspected;
3. keep the same App Server process alive through child reattachment;
4. do not terminate the process between spawn and child `thread/resume`/reattachment;
5. if the installed schema differs materially from the expected shape, stop `BLOCKED_CAPABILITY` before the provider-backed probe rather than guessing.

## Version and capability gate

Before provider-backed work record:

```text
local_codex_cli_version
app_server_initialize_version
native_schema_generated_from_version
thread_loaded_list_response_shape
experimental_api_enabled
current_auth_mode_category
```

Require installed Codex/App Server `>= 0.153.4` and all T056 mandatory surfaces.

No global upgrade, alternate binary, source build, or global configuration mutation is authorized.

## Parent

Create one instrumented parent with:

```text
model: GPT-5.6 Sol
reasoning: Medium
permissions: ":read-only"
approval: never / non-interactive compatible
cwd: isolated current repository worktree
experimental API: enabled
```

Do not send legacy `sandbox`.

Passing parent receipt requires:

```text
activePermissionProfile.id == ":read-only"
```

and no contradictory broader legacy projection.

## Child

Spawn exactly one real Multi-Agent V2 child:

```text
task_name: t057_read_only_child
requested model: GPT-5.6 Terra
requested reasoning: Low
fork_turns: none
service tier: default/omitted
```

Child task:

```text
Return only the deterministic nonce supplied by the controller.
Do not invoke shell, patch, file-write, network, browser or MCP tools.
```

No write attempt is permitted.

## Parent residency

The parent MUST remain loaded/alive from spawn through completion of all child permission/usage/timing/reroute capture.

Persist explicit evidence that the parent thread ID remains present in the loaded-thread set immediately before child reattachment.

If parent residency is lost, stop `PARTIAL_OBSERVABILITY`.

## Child identity and reattachment

Uniquely correlate the exact child using strongest supported evidence, preferring parent-facing `subAgentActivity.agentThreadId`, with supported metadata and `parentThreadId` cross-check/fallback as needed.

While the parent remains loaded, reattach/resume the exact child **without any configuration override**.

Do not send permissions, sandbox, model, reasoning, cwd, approval, or environment overrides.

## Mandatory passing permission receipt

Qualification passes the sandbox gate only if supported child lifecycle metadata returns:

```text
activePermissionProfile.id == ":read-only"
```

Also capture the child legacy sandbox projection. It must not explicitly indicate broader authority.

Null/missing/different profile ID or contradictory broader legacy projection forces `PARTIAL_OBSERVABILITY`.

Private SQLite/JSONL/rollout internals may not upgrade the result.

## Compute, usage, duration and reroute receipts

For the same exact child persist:

```text
requested_child_model
requested_child_reasoning
resolved_child_model_provider
resolved_child_model
resolved_child_reasoning
reroute_observed
backend_served_profile_verified
```

Resolved thread state must match requested `gpt-5.6-terra / low` or record an exact documented replacement. Do not claim backend-served identity from configured thread state.

Capture exact server-reported, non-estimated token usage attributable to the exact child thread/turn, including available input/cache/output/reasoning/total/context fields.

Capture exact child-turn timing and `duration_ms` from supported child-turn timing, not controller wall-clock timing.

Capture exact-child reroute evidence. Absence of reroute is not backend identity proof.

## Safety and repository boundary

Persist only:

```text
handoffs/T057-read-only-child-telemetry.json
handoffs/T057-executor-handoff.json
```

No Executor-authored Markdown.

No product code, dependency, Governance Core, D055, routing policy, global Codex config or persistent agent catalog changes.

Use an isolated evidence worktree from current `develop`. Confirm no tracked mutation from parent/child before evidence files are written.

## Frozen qualification decisions

Exactly one:

```text
QUALIFIED_READ_ONLY_CHILD_SURFACE
PARTIAL_OBSERVABILITY
BLOCKED_VERSION
BLOCKED_CAPABILITY
```

`QUALIFIED_READ_ONLY_CHILD_SURFACE` requires all of:

1. version/capability gate passes;
2. parent `:read-only` receipt passes;
3. one real child is uniquely correlated;
4. parent remains loaded through child reattachment;
5. child returns `activePermissionProfile.id=":read-only"`;
6. no contradictory broader legacy projection;
7. requested/resolved child model/reasoning receipt passes;
8. exact non-estimated child/turn usage captured;
9. exact child-turn duration captured;
10. reroute surface captured without overstating backend identity;
11. no tracked/global mutation.

Provider-backed execution with any missing mandatory receipt => `PARTIAL_OBSERVABILITY`.

## First-attempt rule

T057 authorizes exactly one provider-backed synthetic parent/child attempt.

If the controller fails after the provider-backed attempt begins, fail closed with the appropriate frozen decision. Do not run a compensating second provider-backed attempt inside T057.

## Acceptance criteria

```text
AC-T057-1  freshness + fixed root
AC-T057-2  version/capability gate
AC-T057-3  native thread/loaded/list shape resolved before probe
AC-T057-4  parent :read-only profile receipt
AC-T057-5  one real child + continuous parent residency
AC-T057-6  child :read-only activePermissionProfile receipt
AC-T057-7  requested/resolved compute receipt
AC-T057-8  exact attributable usage
AC-T057-9  exact attributable duration
AC-T057-10 reroute evidence + backend identity boundary
AC-T057-11 safety/no authority leakage
AC-T057-12 exactly one frozen qualification decision
```

## Post-T057 authority

Even a passing qualification does not automatically reactivate R007 or change routing policy.

After terminal evidence, ChatGPT Orchestrator must converge T057, update R009/R008 under D057, and only then decide whether R007 may return to `EVALUATING`.

## Terminal output

Return only:

```text
STATUS: DONE | BLOCKED
HANDOFF: handoffs/T057-executor-handoff.json
BRANCH: <branch>
HEAD: <pushed-head>
```
