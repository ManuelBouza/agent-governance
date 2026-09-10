# R021 — T063 V3 Config-Authoritative Worker Receipts

Research-ID: R021  
Research-State: COMPLETE  
Decision-State: DECIDED  
Opened: 2026-09-10  
Last-Reviewed: 2026-09-10  
Owner: ChatGPT Orchestrator  
Scope: T063 v3 worker/task/profile receipt repair and version-sensitive Codex upstream revalidation  
Question: Can T063 avoid the unsupported V2 exact spawn-message receipt that blocked v2, while preserving D063 exact-child measurement and scientific comparability, and does a newer Codex release already remove that blocker?  
Evaluation-Refs: `docs/tasks/T063-adaptive-worker-routing-requalification.md`; `docs/reviews/T063-R5.md`; candidate `test/t063-adaptive-worker-routing-requalification-v3@9b8a8d96b7586c25e808e93c3cec02d1f2fa3467`  
Decision-Ref: `docs/decisions/D077-version-sensitive-upstream-revalidation.md`  
Supersedes: R020 only for the future T063 repair strategy; R020 remains historical diagnosis of v2  
Superseded-By: none

## Result

T063 can remove the v2 blocker without adopting Codex internal raw-response events and without relying on `thread/read` to reconstruct an `InterAgentCommunication` spawn message.

The v3 design moves **substantive task authority and child compute authority out of the model-authored `spawn_agent` arguments** and into the App Server `thread/start.config` created by the published Stage 5 harness before the measurement parent acts.

The parent remains a transport-only read-only carrier. Its only material action is one `spawn_agent` call containing a deterministic task name, a non-substantive trigger value and `fork_turns="none"`. The parent is not allowed to choose `agent_type`, child model, child reasoning effort or task semantics.

The exact child is correlated through the public `subAgentActivity(kind=Started)` item. D063 live permission/profile/residency/usage/duration/reroute receipts remain mandatory.

## Version-sensitive upstream review

The exact version set reviewed for this repair is:

```text
0.153.4            D063-qualified T063 reference
0.154.0            current stable Codex release at 2026-09-10 review time
0.155.0-alpha.2    later relevant prerelease available at review time
```

Official upstream evidence was taken from the OpenAI Codex GitHub repository and release metadata.

`0.154.0` is the current non-prerelease release. The relevant `multi_agents_v2/spawn.rs` implementation at `0.154.0` and `0.155.0-alpha.2` remains materially unchanged for the T063 blocker: the spawn path emits public `subAgentActivity` for child correlation, while the `CollabAgentToolCallItem` is sent to analytics with `prompt: None`.

The public thread-history reducer in the reviewed higher versions also continues to ignore persisted `RolloutItem::InterAgentCommunication` when reconstructing public thread history.

Therefore no reviewed higher version supplies the public exact spawned-task-message receipt that R020 identified as missing.

Disposition:

```text
version-sensitive classification: PIN_RETAINED
upgrade_fixes_blocker:             false
retained runtime:                  0.153.4
reason:                            D063-qualified reference; no newer reviewed release removes the blocker
```

Moving the experiment to `0.154.0` or a prerelease would add a new qualification/version variable without solving the actual receipt problem.

## Finding 1 — v2 failed because substantive authority lived in an unobservable spawn message

R020 established that Codex `0.153.4` delivers the V2 spawn task as `InterAgentCommunication`, not as a child `userMessage`, and public `thread/read` does not reconstruct that item.

R4 therefore required a receipt the supported public surface could not provide.

The repair principle is not to invent another inference of the same hidden message. It is to stop making that hidden message carry the substantive frozen task.

## Finding 2 — v3 makes task authority config-authoritative

The v3 Stage 5 harness creates each parent thread with configuration containing the exact child developer contract:

```text
features.multi_agent_v2.subagent_developer_instructions = <frozen child contract>
```

That contract contains:

- the exact frozen P1/P2/P3 substantive task;
- the exact task-message SHA-256;
- a per-arm deterministic contract nonce;
- the required compact result shape and receipt fields;
- isolation rules prohibiting T063 authority/oracle inspection and writes.

Because the harness supplies this configuration in `thread/start` before the parent model acts, the parent does not author or select the substantive child task.

The v3 spawn message is reduced to a deterministic non-substantive trigger. The child reports the exact trigger it received as a bounded transport consistency receipt. A trigger mismatch invalidates the arm.

This is not represented as provider-signed prompt proof. It is a controlled experiment receipt whose substantive authority comes from the harness-controlled thread configuration rather than the unobservable inter-agent message.

## Finding 3 — v3 makes child compute config-authoritative

For each arm the harness sets:

```text
agents.default_subagent_model
agents.default_subagent_reasoning_effort
features.multi_agent_v2.expose_spawn_agent_model_overrides = false
```

The parent instructions explicitly prohibit `agent_type`, `model`, `reasoning_effort` and `fork_context` spawn arguments.

Thus the parent cannot choose the scored child profile through the public spawn call. Requested profile authority comes from the per-arm App Server configuration frozen by Stage 5.

After spawn, the harness still requires the D063 resolved-thread receipt to equal the requested model/effort exactly. A mismatch is `BLOCKED_PROFILE_RESOLUTION`, not a quality failure.

## Finding 4 — public child correlation is retained

The v3 harness waits for one parent `subAgentActivity` item with:

```text
kind = Started
agentThreadId = exact child id
agentPath final component = exact frozen task_name
```

It also verifies the completed parent turn contains exactly one matching spawn activity and no substantive tool/item types such as command execution, file change, MCP, dynamic tools, web search or image tools.

The parent's final response must be exactly `PARENT_SPAWNED`.

This closes the R020 child-correlation defect without using analytics or internal raw events.

## Finding 5 — D063 measurement remains unchanged

For every scored child, v3 still requires:

```text
parent activePermissionProfile.id == :read-only
non-contradictory legacy read-only projection
continuous parent residency before child reattachment
child parentThreadId == exact parent
child activePermissionProfile.id == :read-only
resolved child model == frozen requested model
resolved child reasoning == frozen requested reasoning
exact non-estimated child-turn token usage
exact child-turn duration
exact-child reroute observation
no tracked/global mutation attributable to measurement
```

`backend_served_profile_verified` remains `false`.

The repair therefore changes task/profile authority transport but does not weaken the D063 measurement substrate or reinterpret configured model identity as backend-signed identity.

## Finding 6 — custom role ambiguity fails closed

A custom agent role could otherwise cause an `agent_type` selection or role configuration to replace child instructions.

The v3 preflight therefore treats incompatible/custom role state as a blocker before scored execution. The experiment requires the frozen config-authoritative child contract to remain the only substantive child authority.

## Finding 7 — raw response events remain unnecessary and unauthorized

R020 identified `experimentalRawEvents` as a possible way to observe raw function-call arguments, but the exact protocol marks that route internal-only and D063 did not qualify it.

V3 does not use it:

```text
raw_response_events_used = false
```

No new qualification of internal Codex surfaces is required for this repair.

## Stage 5 candidate verification

The complete v3 candidate is published at:

```text
branch: test/t063-adaptive-worker-routing-requalification-v3
HEAD:   9b8a8d96b7586c25e808e93c3cec02d1f2fa3467
base:   7772886f174ae06e0a377fc04612f1059af961b6
```

The candidate is eight commits / eight files ahead of the base and contains only the new evaluation package plus its deterministic test:

```text
evals/adaptive_worker_routing_v3/__init__.py
evals/adaptive_worker_routing_v3/__main__.py
evals/adaptive_worker_routing_v3/app_server.py
evals/adaptive_worker_routing_v3/config.py
evals/adaptive_worker_routing_v3/measurement.py
evals/adaptive_worker_routing_v3/oracles.py
evals/adaptive_worker_routing_v3/runner.py
tests/test_t063_adaptive_worker_routing_v3_harness.py
```

Provider-free Orchestrator verification:

```text
pytest candidate harness tests: 23 passed
Python compile check:            PASS
provider/model calls:            0
```

The Orchestrator environment did not provide the repository lint executable, so repository-native lint remains a mandatory Stage 6 pre-provider gate rather than being claimed as already executed.

## Scientific restart consequence

The v1 and v2 blocked runs remain historical evidence only:

```text
v1  3d8a9460988351383a90adfc6b76e2deff056504
v2  3ff745a8d29e031ca818c1bc618b15a54e0cbf2b
```

The v2 P1 ADAPTIVE diagnostic result is not reused.

Any accepted v3 pilot must be one clean homogeneous six-arm run under this single receipt strategy:

```text
P1 ADAPTIVE -> CONTROL
P2 CONTROL  -> ADAPTIVE
P3 ADAPTIVE -> CONTROL
```

## Disposition

```text
v2 exact-message receipt defect:      CLOSED BY DESIGN CHANGE
public child correlation:             subAgentActivity
substantive task authority:           Stage 5 thread config
child profile request authority:      Stage 5 thread config
resolved profile receipt:             D063 App Server thread state
raw internal events:                  NOT USED
Codex 0.154.0 upgrade required:       NO
0.155.0-alpha.2 adoption required:    NO
runtime pin:                          0.153.4 RETAINED
Stage 5 candidate:                    COMPLETE
provider calls during repair:         0
T063 v3 scientific run:               READY FOR SEPARATE AUTHORITY
```

D077 adopts the general version-sensitive upstream-revalidation rule. T063-R6 separately controls whether the v3 candidate may enter Stage 6.
