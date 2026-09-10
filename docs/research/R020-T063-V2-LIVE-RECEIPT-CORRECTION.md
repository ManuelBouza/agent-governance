# R020 — T063 V2 Live Receipt Correction

Research-ID: R020  
Research-State: COMPLETE  
Decision-State: NOT_REQUIRED  
Opened: 2026-09-10  
Last-Reviewed: 2026-09-10  
Owner: ChatGPT Orchestrator  
Scope: T063 v2 live-blocker convergence and exact Codex `0.153.4` Multi-Agent V2 receipt semantics  
Question: Why did the T063 v2 first scored arm block despite a correct diagnostic worker answer, and does the qualified `0.153.4` App Server expose a suitable receipt for exact child correlation and task-message equality?  
Evaluation-Refs: `docs/tasks/T063-adaptive-worker-routing-requalification.md`; `docs/reviews/T063-R4.md`; `handoffs/T063-adaptive-worker-routing-telemetry-v2.json@3ff745a8d29e031ca818c1bc618b15a54e0cbf2b`; D063; D076  
Decision-Ref: none  
Supersedes: R019 Finding 4 and R019's V2 spawn-correlation/message-attestation assumptions only; the remaining R019 findings stay valid  
Superseded-By: none

## Result

The v2 block is a Stage 5 / adapter-authority defect, not a worker-quality failure, profile-resolution failure, or D076 process violation.

The first and only provider-backed scored attempt was `P1 ADAPTIVE`. Its worker answer matched the P1 oracle diagnostically, but the attempt is invalid and unscored because the published harness waited for a V2 `collabAgentToolCall` item that the live `0.153.4` spawn path does not emit to App Server. The original App Server process then ended before the required D063 child reattachment/permission/usage/reroute receipts could be captured.

No compensating rerun occurred. No pilot decision exists.

## Evidence from the terminal v2 run

Remote evidence is preserved at:

```text
branch: test/t063-adaptive-worker-routing-requalification-v2
HEAD:   3ff745a8d29e031ca818c1bc618b15a54e0cbf2b
```

The terminal run records:

```text
provider scored child attempts: 1
provider scored parent turns:   1
valid scored children:          0
invalid attempt:                P1 ADAPTIVE
requested child profile:        gpt-5.6-luna / medium
resolved child profile:         gpt-5.6-luna / medium
worker oracle result:           PASS_DIAGNOSTIC_ONLY_UNSCORED
rerun performed:                false
pilot_decision:                 null
```

The preflight itself passed on native Windows with Codex/App Server `0.153.4`, chatgpt auth, the required schema markers, and the read-only parent preflight.

Two bounded Stage 6 repairs occurred before the provider-backed attempt:

```text
8472718db9f6a82b4c79b9493255f3c314ef27b2
  parse the actual 0.153.4 App Server version receipt

3088501147b408503acdd93b8bc7b76e6f957bac
  avoid archiving the provider-free preflight parent before clean close
```

Both repairs changed only the published harness/tests and preserve the frozen experimental semantics. They are legitimate D068/D076 technical repairs, not missing first-pass private materialization.

## Exact official source reviewed

OpenAI Codex source was revalidated at the exact frozen runtime tag:

```text
rust-v0.153.4
```

Relevant exact-tag files:

- `codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs`
- `codex-rs/core/src/tools/handlers/multi_agents_v2.rs`
- `codex-rs/core/src/session/handlers.rs`
- `codex-rs/core/src/session/input_queue.rs`
- `codex-rs/app-server-protocol/src/protocol/v2/item.rs`
- `codex-rs/app-server-protocol/src/protocol/v2/thread.rs`
- `codex-rs/app-server-protocol/src/protocol/thread_history.rs`
- `codex-rs/protocol/src/models.rs`
- `codex-rs/protocol/src/protocol.rs`

## Finding 1 — V2 spawn correlation is `subAgentActivity`, not a live `collabAgentToolCall` item

At `rust-v0.153.4`, the Multi-Agent V2 spawn handler builds a `CollabAgentToolCallItem` after spawn but sends that structure to `analytics.track_collab_tool_call(...)`. The handler separately emits a `SubAgentActivityItem` with:

```text
id             = spawn call id
agent_thread_id = new child thread id
agent_path      = spawned task path
kind            = Started
```

The App Server V2 `ThreadItem` schema exposes `subAgentActivity` with those fields.

Therefore the T063 v2 harness assumption:

```text
item/started|completed
  -> type == collabAgentToolCall
  -> receiverThreadIds[0]
```

was wrong for this live V2 path. The correct public child-correlation event for this exact runtime is the emitted `subAgentActivity` item.

This explains the 120-second spawn wait timeout while the child nevertheless ran and completed successfully.

## Finding 2 — the spawn task is inter-agent communication, not a child `userMessage`

The V2 spawn handler converts `message` into `InterAgentCommunication` and passes it through `spawn_agent_with_communication(...)` with `trigger_turn=true`.

The child input queue represents that as:

```text
TurnInput::InterAgentCommunication
```

not as `TurnInput::UserInput`.

The protocol converts inter-agent communication to agent/assistant-role model input. It is therefore incorrect to require a child `userMessage` containing the exact task text.

The App Server thread-history reducer also deliberately ignores persisted `RolloutItem::InterAgentCommunication` when reconstructing public `thread/read` turns. Consequently `thread/read` cannot be used to recover and byte-compare the original inter-agent spawn task in the way R019/R4 required.

The live observation `child_user_message_item_present=false` is thus expected runtime behavior, not evidence of message loss.

## Finding 3 — R019 Finding 4 is prospectively superseded

R019 correctly rejected the analytics `collabAgentToolCall.prompt` as a reliable full prompt receipt, but its replacement method was also incorrect:

```text
spawn child
-> thread/read child
-> require one userMessage equal to frozen task
```

That method is not supported by the exact `0.153.4` V2 storage/projection path.

R020 supersedes only that message-attestation/correlation portion of R019. R019's runtime pin, V2 `task_name` / `fork_turns="none"`, explicit feature configuration, P3 runtime-root correction, clean-rerun requirement, and D076 boundary remain valid.

## Finding 4 — raw response events can expose function-call arguments, but are not currently qualified authority

The exact `0.153.4` App Server protocol includes:

```text
thread/start.experimentalRawEvents = true
rawResponseItem/completed
```

and `RawResponseItemCompletedNotification` carries:

```text
thread_id
turn_id
item: ResponseItem
```

`ResponseItem::FunctionCall` includes the function name, raw JSON `arguments`, and `call_id`. In principle this could reveal the parent model's actual `spawn_agent` arguments, including the exact `message`, `task_name`, model, reasoning effort, and `fork_turns`, rather than inferring them from downstream state.

However, the exact protocol explicitly documents `experimentalRawEvents` / raw response item emission as **internal use only**. Raw response notifications are also intentionally excluded from normal generated notification schemas.

D063 did not qualify this internal raw-event surface as part of the accepted T057 measurement substrate. T063-R4 did not authorize it either.

Therefore R020 does **not** silently adopt raw response items as passing T063 evidence. A future continuation may use that route only after separate Orchestrator qualification/authority establishes that the concrete native surface is acceptable, stable enough for the experiment, non-leaky, and semantically sufficient.

## Finding 5 — the blocked P1 result cannot be scored or reused

The P1 ADAPTIVE child resolved to the requested Luna/Medium configuration and its post-run answer matched the oracle, but required D063 receipts were not captured from the live parent/child relationship:

- exact live child permission profile;
- continuous parent residency at child reattachment;
- exact non-estimated child-turn usage;
- exact-child reroute observation;
- the R4 task-message equality condition.

The answer is diagnostic evidence only. It is not a PASS or FAIL for T063.

Because R4 requires a homogeneous clean six-arm run, any corrected successor execution must start another clean six-arm set. The consumed v2 P1 attempt remains historical invalid evidence and is not reused.

## Finding 6 — D076 held

Terminal v2 evidence reports:

```text
executor_material_ephemeral_artifacts: []
ephemeral_artifacts: []
```

The only candidate-owned runtime artifact was the already-materialized P3 fixture lifecycle. No new private substantial controller/harness/oracle was created by Codex.

This run therefore does not reproduce the D076 regression that triggered the earlier re-entry.

## Disposition

```text
v2 remote evidence:                  ACCEPTED AS BLOCKED EVIDENCE
P1 ADAPTIVE quality result:          DIAGNOSTIC PASS ONLY / UNSCORED
valid scored arms:                   0 / 6
provider-backed scored attempts:     1
pilot decision:                      NONE
profile-resolution failure:          NO
worker-quality failure:              NO
D076 violation:                      NO
root cause:                          STAGE 5 / R019-R4 V2 RECEIPT ASSUMPTION
R019 Finding 4:                      PARTIALLY SUPERSEDED BY R020
additional provider calls:           NOT AUTHORIZED
future continuation:                 ORCHESTRATOR REENTRY REQUIRED
```

No global R007 adaptive-worker routing decision follows from this blocked run.