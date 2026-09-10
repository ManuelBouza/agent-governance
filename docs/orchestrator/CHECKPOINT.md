# Orchestrator Checkpoint

Checkpoint-ID: O264  
Date: 2026-09-10  
Current-Objective: T063 — adaptive worker routing requalification  
State: T063_V3_STAGE6_AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Active-Executor: none — Codex selected for pending Human launch  
Executor-Launch-State: AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Coordinator-ID: `AG | agent-governance | T063 | root-3` — reserved NEW failover root; not yet started  
T063-V3-Candidate-Branch: `test/t063-adaptive-worker-routing-requalification-v3`  
T063-V3-Candidate-HEAD: `9b8a8d96b7586c25e808e93c3cec02d1f2fa3467`  
T063-V3-Candidate-Base: `7772886f174ae06e0a377fc04612f1059af961b6`  
T063-V3-Launch-Authority: `docs/reviews/T063-R6.md`  
T063-V3-Receipt-Research: `docs/research/R021-T063-V3-CONFIG-AUTHORITATIVE-WORKER-RECEIPTS.md`  
Historical-T063-V2-Evidence-HEAD: `3ff745a8d29e031ca818c1bc618b15a54e0cbf2b`  
Historical-T063-V1-Evidence-HEAD: `3d8a9460988351383a90adfc6b76e2deff056504`  
Held-Work-Unit: T062 / T023 v15 Stage 6  
Held-State: HUMAN_HOLD_R32_UNCONSUMED  
Chat-Closure: KEEP_CURRENT_CHAT

## Canonical transition

O263 required Orchestrator re-entry after the T063 v2 adapter blocked on unsupported Multi-Agent V2 receipt assumptions.

The Human explicitly continued T063 repair. ChatGPT Orchestrator completed D068 Stage 5 re-entry without provider/model calls and published a new candidate:

```text
branch: test/t063-adaptive-worker-routing-requalification-v3
HEAD:   9b8a8d96b7586c25e808e93c3cec02d1f2fa3467
base:   7772886f174ae06e0a377fc04612f1059af961b6
```

The candidate is exactly eight commits / eight files ahead of its base and contains only:

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
candidate harness tests: 23 passed
Python compile check:    PASS
provider/model calls:    0
```

Repository-native lint remains a Stage 6 **pre-provider** technical gate because the Orchestrator environment did not provide the lint executable.

## V3 receipt repair

R021/R6 replace the invalid v2 exact spawned-task-message receipt with a config-authoritative architecture.

The substantive child task and requested child model/reasoning are materialized by the Stage 5 harness into App Server `thread/start.config` before the measurement parent acts:

```text
features.multi_agent_v2.subagent_developer_instructions = <frozen child contract>
agents.default_subagent_model = <frozen arm model>
agents.default_subagent_reasoning_effort = <frozen arm effort>
features.multi_agent_v2.expose_spawn_agent_model_overrides = false
features.multi_agent_v2.hide_spawn_agent_metadata = true
```

The parent is transport-only. It may spawn exactly one child with the harness-provided `task_name`, a deterministic non-substantive trigger and `fork_turns="none"`; it may not select `agent_type`, model, reasoning or task semantics.

The child must return the frozen contract nonce, task digest and exact received trigger. Any mismatch invalidates the arm. This is a controlled transport/contract consistency receipt, not provider-signed prompt identity.

Public child correlation uses:

```text
subAgentActivity(kind=Started, agentThreadId=<exact child>)
```

Internal raw response events are not used.

## D063 measurement preservation

V3 retains the mandatory D063 exact-child measurement set:

```text
real parent/child correlation
parent activePermissionProfile.id == :read-only
non-contradictory legacy read-only projection
continuous parent residency before child reattachment
child parentThreadId == exact parent
child activePermissionProfile.id == :read-only
requested child model/reasoning from frozen Stage 5 config
resolved configured child model/reasoning exact match
exact non-estimated child-turn usage
exact child-turn duration
exact-child reroute observation
no tracked/global mutation attributable to measurement
```

`backend_served_profile_verified = false` remains controlling.

Custom/local agent-role ambiguity is a pre-provider blocker.

## D077 version-sensitive revalidation

D077 is now the global rule for material version-dependent research/launch authority.

R021 reviewed:

```text
0.153.4            D063-qualified T063 reference
0.154.0            current stable Codex release at review/authority time
0.155.0-alpha.2    later relevant prerelease
```

The reviewed higher versions do not remove the public exact spawned-task-message blocker. T063 therefore records:

```text
version disposition: PIN_RETAINED
runtime:             0.153.4
upgrade fixes blocker: false
```

If a newer stable Codex release appears before the Human actually launches `root-3`, stop and classify its relevance under D077 before provider-backed execution.

## Scientific restart rule

V3 must be one homogeneous clean six-arm run:

```text
P1 ADAPTIVE -> CONTROL
P2 CONTROL  -> ADAPTIVE
P3 ADAPTIVE -> CONTROL
```

Historical T063 v1/v2 results are excluded from every v3 score/metric/pilot decision.

Frozen source/oracle baseline remains:

```text
69e910f329a2294c3b40df0f6ee983f9905f4677
```

No v3 provider/model calls have occurred yet.

## Launch profile

T063-R6 freezes:

```text
Executor:        Codex
Surface:         Codex Local / native Windows
Session:         NEW
Coordinator-ID:  AG | agent-governance | T063 | root-3
Root model:      gpt-5.6-sol
Root reasoning:  medium
Codex CLI:       exactly 0.153.4
App Server:      exactly 0.153.4
Auth category:   chatgpt
```

Child matrix:

```text
P1 ADAPTIVE  gpt-5.6-luna  / medium
P1 CONTROL   gpt-5.6-sol   / medium
P2 CONTROL   gpt-5.6-sol   / medium
P2 ADAPTIVE  gpt-5.6-terra / medium
P3 ADAPTIVE  gpt-5.6-terra / high
P3 CONTROL   gpt-5.6-sol   / medium
```

No model/effort/runtime substitution is authorized after provider-backed execution begins.

## D076 Stage 6 boundary

Codex executes/diagnoses/verifies the published v3 candidate and may make only bounded represented technical repairs that preserve R6 semantics.

Substantial missing controller/harness/fixture/oracle implementation outside the candidate is a stop/re-entry condition. File-based non-candidate executable aids actually used in verification remain subject to the D076 `ephemeral_artifacts` audit.

Executor-authored committed Markdown remains prohibited.

## Evidence and terminal return

Normal evidence paths:

```text
handoffs/T063-adaptive-worker-routing-telemetry-v3.json
handoffs/T063-executor-handoff-v3.json
```

Terminal Human return after Codex completes or blocks:

```text
STATUS: COMPLETED | BLOCKED
HANDOFF: handoffs/T063-executor-handoff-v3.json
BRANCH: test/t063-adaptive-worker-routing-requalification-v3
HEAD: <actual remote pushed HEAD>
```

A `BLOCKED` result authorizes no compensating provider call unless the existing R6 rules explicitly cover it; otherwise return to Orchestrator review.

## T062 held frontier

T023-R33 remains controlling. T062 is not resumed.

```text
scientific branch:               test/t023-skill-activation-topology-evals-v15
terminal Stage 5 HEAD:           3e0d0b71cf382db502e186622f40a23bcd915390
Candidate Freeze E:              5b025087bc7b6996f683a34fdd1ce441d3d6dd82
Holdout/oracle Freeze F:         5b8ac55980ecdbb6a2bf3784812b933647f2f13d
blocked Stage 6 evidence HEAD:   b9034e450f04fbc9736543425e531159d4b79d49
provider/model calls:            0
R32 provider continuation authority: valid but unconsumed
R32 transport:                   PAUSED by T023-R33
```

Do not execute the old T062 R32 continuation prompt.

## Other durable constraints

- T024 remains unauthorized until T023 selects a topology from valid evidence.
- T058 remains frozen by explicit Human decision; do not resume, integrate, clean or copy it without new explicit Human authorization.
- D061/D062 continue to require PR-mediated long-lived branch mutation.
- D071 continues to require Human-mediated Codex transport.
- R007 remains `EVALUATING`; R6 authorizes an experiment, not a global routing policy.

## Next Chat Minimum Load

After normal bootstrap (`develop`, `AGENTS.md`, this checkpoint):

1. for pending T063 v3 launch or convergence, load `docs/reviews/T063-R6.md` first;
2. load R021 when receipt/version rationale is needed;
3. load D063 before interpreting measurement validity;
4. load D076 before accepting any Stage 6 repair/ephemeral executable behavior;
5. load the v3 candidate `config.py` / `measurement.py` / `runner.py` only when execution mechanics or evidence conflict requires it;
6. for T062 resumption, instead load T023-R31/R32/R33 plus the held scientific branch/handoff;
7. do not reconstruct either frontier from prior chat/Project Memory.

D077 is bootstrap-visible in `AGENTS.md` and controls any newly changed upstream version state.

## Next Action

After O264/R6/D077/R021 are merged into `develop`, T063 v3 Stage 6 is authorized.

The Human should start a **NEW** Codex session with exact title:

```text
AG | agent-governance | T063 | root-3
```

Use the R6-frozen root profile and exact candidate branch/HEAD. The transport prompt should remain thin and point Codex to canonical Git authority rather than duplicating experiment semantics.

ChatGPT must not start or directly control Codex under D071. After the Human returns the terminal four-line result, ChatGPT performs remote verification and Stage 7 convergence.
