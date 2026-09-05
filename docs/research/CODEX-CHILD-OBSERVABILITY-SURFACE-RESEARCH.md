# R008 — Codex Child Observability Surface Research

Research-ID: `R008`  
Research-State: `COMPLETE`  
Decision-State: `EVALUATING`  
Date: 2026-09-05  
Last-Reviewed: 2026-09-05  
Owner: ChatGPT Orchestrator  
Volatility: `HIGH` — Codex App Server, SDK and multi-agent surfaces are evolving rapidly  
Applies to: successor evaluation after `docs/reviews/T054-R1.md`

## Question

Does the current Codex ecosystem expose a sufficiently supported and auditable surface to measure, per spawned child:

1. child identity and parent relationship;
2. resolved/configured model and reasoning effort;
3. sandbox/capability state;
4. attributable token usage and duration;
5. enough provenance to distinguish requested configuration from observed/resolved configuration;

without scraping private chat state, inventing token estimates, or relying on the sparse parent-facing `spawn_agent` return used by T054?

The downstream purpose is narrow: determine whether Agent Governance should run a **small observability qualification** before considering any corrected successor to T054. This research does not itself reopen R007, adopt adaptive routing, change D055, or authorize a quantitative savings claim.

## Source snapshot

Primary authority was refreshed on 2026-09-05.

### Public OpenAI documentation

- Codex App Server: <https://learn.chatgpt.com/docs/app-server>
- Codex SDK: <https://learn.chatgpt.com/docs/codex-sdk>
- Codex subagents: <https://learn.chatgpt.com/docs/agent-configuration/subagents>

### Official OpenAI Codex repository

Repository: <https://github.com/openai/codex>

Current `main` inspected:

```text
ddf04ad26789d040f9ef6a96736f76602e35a6cc
```

Latest stable release inspected:

```text
Codex CLI 0.153.4
release: 2026-09-04
release commit: 3d2ee51ca2d5db578f328aa75e20aa22c0197c9a
```

Important implementation/schema paths:

- `codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs`
- `codex-rs/app-server-protocol/src/protocol/v2/thread_data.rs`
- `codex-rs/app-server-protocol/src/protocol/v2/thread.rs`
- `codex-rs/app-server/src/request_processors/token_usage_replay.rs`
- `codex-rs/app-server/tests/suite/v2/thread_list.rs`
- `codex-rs/state/src/model/thread_metadata.rs`
- `sdk/python/docs/api-reference.md`
- generated `ThreadTokenUsage` / `TokenUsageBreakdown` v2 schemas

### Secondary evidence

Open issue `openai/codex#32504`, filed against CLI 0.144.1, documents the earlier MultiAgentV2 gap where the canonical parent-facing activity item did not carry resolved child identity/model/effort metadata. The issue remains useful historical evidence, but it is not used to characterize 0.153.4 without checking current source/docs because the query surface has materially evolved.

## Executive finding

**Yes, with an important qualification.**

Codex 0.153.4 exposes a materially stronger, documented App Server / Python SDK surface than the direct collaboration surface available to the T054 root. It is sufficient to justify a bounded observability-qualification experiment before any new routing pilot.

The strongest current path is:

```text
parent/root thread
    -> spawn bounded subagent
    -> obtain/discover child thread id
    -> App Server thread query/resume
       -> parentThreadId / source
       -> configured/persisted model
       -> configured/persisted reasoning effort
       -> sandbox response on resume
    -> thread/tokenUsage/updated
       -> threadId + turnId + token breakdown
    -> turn timing / duration
```

However, these observations are **not equivalent to a cryptographic/provider receipt proving the exact backend model that served every response**. Current `Thread.model` and `Thread.reasoningEffort` are explicitly described in the protocol source as current configured values when loaded or latest persisted values otherwise, and as **not per-turn execution telemetry**.

Therefore a future evaluator must distinguish at least:

```text
requested_profile
resolved_thread_profile
reroute_observed
backend_served_profile
```

`backend_served_profile` remains `UNVERIFIED` unless a future public surface exposes an authoritative per-response receipt. A configured/resolved thread profile may still be sufficient for a controlled routing experiment if the claim is framed as configured-compute allocation rather than guaranteed provider execution identity.

## Finding 1 — direct parent-facing MultiAgentV2 activity remains too sparse

Current MultiAgentV2 spawn code accepts child `model`, `reasoning_effort` and `fork_turns`. Internally it obtains an agent configuration snapshot after spawning and uses that snapshot in analytics.

The canonical parent-facing `SubAgentActivityItem`, however, remains much smaller: it carries child thread identity/path/lifecycle rather than the complete resolved profile.

This preserves the central lesson from T054: **do not use the parent tool return alone as the telemetry contract**.

The historical `openai/codex#32504` report accurately describes this limitation for 0.144.1. The key difference in 0.153.4 is that a separate supported child-thread query surface now exists and can be used instead of internal JSONL/SQLite scraping for the main fields required by Agent Governance.

## Finding 2 — child threads have queryable model and reasoning state

The App Server v2 `Thread` schema in stable 0.153.4 contains:

- `id`;
- `sessionId`;
- `parentThreadId` for subagents;
- `modelProvider`;
- `model`;
- `reasoningEffort`;
- source/thread-source information;
- agent nickname/role where available;
- CLI version and working directory.

The schema documentation is precise:

- `model` is the current configured model when loaded, otherwise latest persisted model;
- `reasoningEffort` is the current configured reasoning effort when loaded, otherwise latest persisted effort;
- neither is documented as per-turn execution telemetry.

Current official integration tests also resume root/child threads with different model/effort settings and verify that `thread/list` returns the corresponding settings for loaded subagents.

### Interpretation

This is a much stronger receipt than the T054 root had. It allows an evaluator to verify that the child thread resolved to the intended Codex configuration.

It does **not** justify the stronger statement:

> “The provider definitely served every child response using exactly this model/effort.”

That distinction must remain explicit in telemetry and acceptance language.

## Finding 3 — child relationship discovery is available, but the best relation filters are experimental

Public App Server documentation says `thread/list` supports normal filters and experimental relationship filters:

- `parentThreadId` for direct children;
- `ancestorThreadId` for descendants.

Those relationship filters require `capabilities.experimentalApi = true` as of the reviewed documentation.

The returned `Thread.parentThreadId` field itself is part of the v2 thread model, and `sourceKinds` includes subagent sources. Therefore an evaluator has two possible strategies:

1. **Preferred stable-first discovery:** list relevant `subAgent*` source kinds and correlate returned `parentThreadId` with the known parent root.
2. **Experimental convenience path:** use `parentThreadId` directly when experimental API capability is explicitly enabled and recorded.

A successor evaluation should not make experimental relation filtering a hidden correctness dependency when stable-first enumeration/correlation is feasible.

## Finding 4 — per-thread token usage is a first-class App Server event

Public App Server documentation lists:

```text
thread/tokenUsage/updated
```

for active-thread usage updates.

Official implementation goes further: when a client attaches to an existing thread, App Server can replay the latest persisted token-usage snapshot and constructs `ThreadTokenUsageUpdatedNotification` with:

```text
thread_id
turn_id
token_usage
```

The stable 0.153.4 generated schema defines token usage with:

```text
totalTokens
inputTokens
cachedInputTokens
cacheWriteInputTokens
outputTokens
reasoningOutputTokens
```

and supplies total/last usage plus model context window.

The public Python SDK also documents `TurnResult.usage: ThreadTokenUsage | None` for turns it runs directly.

### Interpretation

For Agent Governance, this is the most important R008 improvement over T054: token usage can be **attributed to a concrete child thread and turn** instead of being estimated from wall-clock duration or left completely unavailable.

A qualification run must still verify this behavior on the actual installed host/version before treating it as usable experimental telemetry.

## Finding 5 — sandbox is explicit at the thread/turn App Server boundary

Public App Server and Python SDK surfaces expose sandbox selection. The SDK documents stable presets:

- `read_only`;
- `workspace_write`;
- `full_access`.

App Server `thread/start` / `thread/resume` responses include the active sandbox policy. Named permission profiles are available through an experimental API.

Direct MultiAgentV2 `spawn_agent` arguments do not currently provide the same explicit per-child sandbox argument alongside model/reasoning/fork settings. Child sandbox may instead arise through parent inheritance or configured agent-role settings.

### Interpretation

A successor qualification should verify two separate facts rather than conflating them:

```text
child sandbox state observable?     -> expected YES via child resume/response
spawn-time child sandbox override?  -> do not assume; record actual capability
```

The experiment does not need a project-persistent `.codex/agents/` catalog merely to prove observability. If a configured-role sandbox test is later needed, it should use disposable configuration outside tracked product state and be explicitly authorized.

## Finding 6 — public Python SDK is a supported automation surface

OpenAI's current Codex SDK documentation states that the Python SDK controls local Codex App Server through JSON-RPC and that published SDK builds pin a Codex CLI runtime. The stable package is installed with:

```text
pip install openai-codex
```

The public SDK surface includes thread start/list/resume/fork, model and sandbox controls, streamed turn handling, duration, and `ThreadTokenUsage` in results.

OpenAI documentation recommends the SDK for automation/CI and App Server for deeper custom-client integration.

### Consequence

A future Agent Governance measurement harness should prefer:

1. a version-pinned current stable SDK/App Server surface;
2. public protocol types/events;
3. source inspection only as characterization/diagnostic evidence;
4. persisted internal SQLite/JSONL only as a last-resort cross-check, never the primary portability contract.

## Finding 7 — rerouting must be recorded separately from configured model

Current public App Server documentation includes a `model/rerouted` event with source model, target model and reason when the service reroutes a request.

This is useful negative/exception telemetry. A successor evaluation should record whether any reroute event was observed for each child.

Absence of a reroute event plus a matching configured thread model is stronger evidence than the T054 requested-only record, but still should not be mislabeled as a provider-signed backend execution receipt.

## Finding 8 — exact cost telemetry has additional constraints

Current Codex source has evolved beyond raw tokens:

- per-thread backend usage query support exists internally;
- App Server can emit estimated turn-cost telemetry for OpenAI API-key sessions when the relevant telemetry export is enabled.

These are not adopted as the baseline Agent Governance surface for the next qualification because availability depends on authentication mode, telemetry setup and/or lower-level backend interfaces.

The next step should qualify **token usage**, not USD cost. Cost can be derived or evaluated later only under an explicitly sourced, versioned pricing/usage method.

## Capability matrix

| Need | Current evidence | Status for next qualification |
| --- | --- | --- |
| Child ID | spawn lifecycle + thread records | `SUPPORTED` |
| Parent/child relationship | `Thread.parentThreadId`; relation filters | `SUPPORTED`, relation filters experimental |
| Resolved/configured child model | `Thread.model` | `SUPPORTED_CONFIG_RECEIPT` |
| Resolved/configured child reasoning | `Thread.reasoningEffort` | `SUPPORTED_CONFIG_RECEIPT` |
| Provider-served per-turn model receipt | no authoritative public receipt established | `UNVERIFIED` |
| Provider-served per-turn reasoning receipt | no authoritative public receipt established | `UNVERIFIED` |
| Reroute signal | `model/rerouted` event | `SUPPORTED_EXCEPTION_SIGNAL` |
| Child token usage | `thread/tokenUsage/updated` by thread/turn | `SUPPORTED`, host qualification required |
| Token breakdown | input/cached/cache-write/output/reasoning/total | `SUPPORTED` |
| Duration | turn timestamps/duration / SDK result | `SUPPORTED` |
| Sandbox state | thread start/resume response | `SUPPORTED` |
| Direct per-spawn sandbox override | not established on MultiAgentV2 spawn args | `NOT_ESTABLISHED` |
| Named permission profile provenance | App Server permission profile | `EXPERIMENTAL` |
| USD cost | authentication/telemetry dependent | `OUT_OF_SCOPE_FOR_NEXT_QUALIFICATION` |

## Decision analysis

### Option A — rerun T054 unchanged

Rejected.

It would preserve the P2 semantics confound, repeat the failed P1 Luna/Low mapping, and still use the weaker direct parent-facing observability path.

### Option B — immediately adopt App Server telemetry as sufficient and rerun routing

Rejected.

Documentation/source capability is not equivalent to evidence that the Human's actual installed Codex surface exposes and correctly correlates all required fields. Version skew, runtime selection, authentication mode, experimental-capability flags and event replay behavior remain operational variables.

### Option C — run a bounded observability qualification first

Selected.

A small evidence-only Task Contract should verify on the actual host that a child can be spawned and then correlated to:

- its child thread record;
- configured/resolved model and reasoning;
- sandbox state;
- attributable token usage;
- duration;
- reroute evidence if any;
- exact Codex/App Server/SDK version identity.

The qualification should make **no routing-quality comparison** and no cost-saving claim. Its sole purpose is to determine whether the measurement substrate is good enough for a corrected successor routing pilot.

## Research disposition

```text
Research-State: COMPLETE
Decision-State: EVALUATING
Selected next step: T055 Codex Child Observability Qualification
Global routing policy: unchanged
D055: unchanged
R007: remains DEFERRED
```

R008 itself does not reactivate R007. R007 may return to `EVALUATING` only after T055 demonstrates an adequate measurement surface and the Orchestrator separately specifies a corrected routing experiment.

## Requirements for T055

The next qualification should be fail-closed and evidence-only.

It must:

1. pin and record actual Codex CLI/App Server/SDK identities;
2. prefer the stable Python SDK/App Server public protocol;
3. avoid adding a source-product runtime dependency merely for the experiment;
4. keep temporary controller/configuration assets outside tracked product state unless the Task Contract explicitly authorizes a non-Markdown evidence artifact;
5. spawn at least one bounded child through the real multi-agent path rather than only creating unrelated top-level threads;
6. discover/correlate that child through supported thread records;
7. verify configured model/reasoning from the child thread surface;
8. record child sandbox state and whether direct spawn-time sandbox override is actually available;
9. collect attributable child token usage by child thread/turn;
10. record duration and any `model/rerouted` event;
11. label provider-served model/reasoning as unverified unless a stronger public receipt is actually exposed;
12. stop without routing claims if the actual host cannot provide the required telemetry.

## Revalidation trigger

Because this surface is highly volatile, revalidate R008 before reuse when any of the following is true:

- installed Codex/App Server/SDK version changes materially;
- public App Server or SDK docs change the thread/usage contract;
- MultiAgentV2 lifecycle schema changes;
- `openai/codex#32504` or a successor issue is resolved with a new canonical child receipt;
- a public per-turn effective model/reasoning receipt becomes available.
