# R019 — T063 Multi-Agent V2 Harness Re-entry

Research-ID: R019  
Research-State: COMPLETE  
Decision-State: NOT_REQUIRED  
Opened: 2026-09-10  
Last-Reviewed: 2026-09-10  
Owner: ChatGPT Orchestrator  
Scope: T063 Stage 5 executable-harness re-entry and exact Codex 0.153.4 Multi-Agent V2 adapter behavior  
Question: Can T063 be restarted cleanly with a published Stage 5 harness that preserves D063/T063 semantics while removing the P3 input-access and D076 materialization regressions?  
Evaluation-Refs: `docs/tasks/T063-adaptive-worker-routing-requalification.md`; `docs/reviews/T063-R2.md`; `docs/reviews/T063-R3.md`; D063; D068; D076  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Result

Yes, subject to a clean complete six-arm rerun and exact Codex/App Server `0.153.4` execution.

The corrected Stage 5 candidate is published as repository code rather than left for the Executor to recreate as temporary controller logic. Provider-free deterministic verification of the materialized candidate is `21 passed`, and Python bytecode compilation succeeds.

R019 makes no global routing decision and authorizes no provider identity claim beyond D063. Its role is to record the exact adapter facts and experimental corrections needed by T063-R4.

## Sources revalidated on 2026-09-10

Official OpenAI Codex source was inspected at the exact qualified tag:

```text
rust-v0.153.4
```

Relevant source paths include:

- `codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs`
- `codex-rs/core/src/tools/handlers/multi_agents_spec.rs`
- `codex-rs/core/src/tools/handlers/multi_agents_v2.rs`
- `codex-rs/features/src/lib.rs`
- `codex-rs/features/src/feature_configs.rs`
- `codex-rs/app-server-protocol/schema/typescript/v2/ThreadItem.ts`
- `codex-rs/app-server-protocol/schema/typescript/v2/UserInput.ts`

Official release state was also revalidated through `https://github.com/openai/codex/releases`.

## Finding 1 — 0.154.0 is now stable, but T063 must remain pinned to 0.153.4

Codex `0.154.0` became the current stable release after R018 was written.

That vendor change does not justify silently changing the T063 runtime. D063 qualified the required child measurement substrate on `0.153.4`, and T063-R2 froze `0.153.4` to avoid an unnecessary runtime confound.

Therefore T063 v2 deliberately treats:

```text
0.153.4 = qualified frozen experimental baseline
0.154.0 = newer current stable release, not part of this rerun
```

This corrects R018's now-stale volatile phrase that called `0.153.4` the current stable runtime while preserving its substantive recommendation for T063.

## Finding 2 — Multi-Agent V2 requires `task_name` and uses `fork_turns`, not `fork_context`

At `rust-v0.153.4`, the V2 `spawn_agent` arguments require:

```text
message
task_name
```

and optionally accept model/reasoning plus `fork_turns`.

The V2 handler explicitly rejects `fork_context`. A child with no parent-history fork must therefore use:

```text
fork_turns = "none"
```

The corrected harness freezes a deterministic per-arm `task_name`, sends the frozen child message unchanged, and uses `fork_turns="none"`.

## Finding 3 — Multi-Agent V2 cannot depend on the user's ambient feature configuration

At `0.153.4`:

```text
features.multi_agent       -> stable / default enabled
features.multi_agent_v2    -> stable / default disabled
```

and V2 exposes child `model` / `reasoning_effort` only when `expose_spawn_agent_model_overrides` is enabled.

The harness therefore starts App Server with these explicit overrides:

```text
features.multi_agent=true
features.multi_agent_v2.enabled=true
features.multi_agent_v2.expose_spawn_agent_model_overrides=true
```

The live preflight must still fail closed if the actual native surface does not realize the required schema or profiles.

## Finding 4 — the V2 collab receipt is not a full child-message attestation

The V2 spawn path does not provide a reliable full prompt receipt in the `collabAgentToolCall` item; its analytics representation can carry `prompt: None`.

T063 must not convert that surface into a stronger claim than the protocol supports.

The corrected design instead:

1. freezes the P1/P2/P3 child messages and SHA-256 digests in Stage 5;
2. instructs the read-only measurement parent to pass the exact frozen message unchanged in its single `spawn_agent` call;
3. reads the exact child thread through the supported App Server thread surface;
4. requires the child's single substantive `userMessage` text to equal the frozen message byte-for-byte before scoring;
5. uses D063 receipts separately for parent/child identity, permission, configured profile, usage, duration and reroute observation.

This is a controlled transport-equality check, not a provider-signed prompt attestation.

## Finding 5 — the corrected P3 input must be a readable worktree-sibling artifact

The historical P3 fixture was semantically correct but placed under Windows system temp, where the read-only child could not access it.

The corrected Stage 5 harness requires an unused runtime root that is:

```text
outside the repository/worktree
not inside the system temporary directory
a sibling of the exclusive T063 worktree
nonexistent before the harness creates it
```

The P3 fixture is mechanically derived from the frozen `69e910...` source blob, its exact expected SHA-256 is verified, host readability is checked immediately, and the fixture is removed after the matched pair while preserving its digest in evidence.

This keeps the fixture non-tracked while placing it inside the Windows sandbox's intended readable project-neighborhood surface.

## Finding 6 — the final T063 result requires a complete clean rerun

The historical P1/P2 PASS pairs remain useful diagnostic evidence but are not scientifically reusable in the final pilot after the harness correction.

The corrected run changes material experimental execution conditions:

- controller/harness implementation becomes published Stage 5 authority;
- V2 child transport is corrected and explicitly frozen;
- App Server feature configuration is explicit;
- child message equality gains a native thread check;
- P3 input placement changes;
- every scored arm is moved to a fresh App Server/parent boundary.

Mixing four historical arms with two repaired P3 arms would therefore produce a heterogeneous six-arm set.

T063-R4 must require six fresh first attempts in the original frozen arm order and preserve the historical branch separately.

## Finding 7 — fresh App Server per scored arm is the lower-confound boundary

Each scored arm now receives:

```text
fresh App Server process
-> fresh read-only parent
-> exactly one fresh scored child
-> evidence capture
-> process close
```

This avoids accidental parent/child state, loaded-thread residency or ambient session reuse across arms while retaining D063's continuous parent-residency requirement inside the affected arm.

A separate provider-free/native-capability preflight App Server runs before scored work.

## Finding 8 — D076 Stage 6 boundary is now executable and auditable

The published Stage 5 candidate contains the substantial controller/harness behavior.

During Stage 6, Codex may still use ordinary commands, native schema/help captures, inline glue and other small D076 mechanical aids. Any file-based executable artifact created outside the published candidate and actually used for verification must be listed in the final handoff's `ephemeral_artifacts` inventory.

If a missing artifact becomes material or uncertain, the run stops for Orchestrator re-entry rather than growing a second private controller.

## Frozen Stage 5 message digests

The corrected child task-message SHA-256 values are:

```text
P1  9aa60aef807873669690a2ad2b564fed58e0731ff0d6e0162fbef40c621a2164
P2  031c06d7544f6146901e633d4bceb8af0e15325c0124dc586e10f545aaadfe4a
P3  9d980424d08517c72911eaacaa9cee36ddf2003d50c21ad6b4d0c25786d9554f
```

The harness fails closed if those messages drift.

## Provider-call accounting

R019 and the Stage 5 repair made:

```text
provider/model calls: 0
```

All local validation was deterministic/provider-free.

## Disposition

```text
D063 qualified runtime:            preserve 0.153.4 for T063 v2
current vendor stable:             0.154.0, intentionally not adopted mid-evaluation
V2 task transport:                 corrected
V2 feature/profile exposure:       explicitly configured
P3 readable fixture strategy:      corrected
historical P1/P2 final reuse:      rejected
complete rerun:                    required
published Stage 5 harness:         required and materialized
D076 Stage 6 private controller:   forbidden
R007 routing policy:               still EVALUATING
new normative decision:            NOT REQUIRED
```
