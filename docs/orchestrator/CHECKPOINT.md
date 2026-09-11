# Orchestrator Checkpoint

Checkpoint-ID: O265  
Date: 2026-09-11  
Current-Objective: T063 — adaptive worker routing requalification  
State: T063_V4_STAGE6_AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Active-Executor: none — Codex selected for pending Human launch  
Executor-Launch-State: AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Coordinator-ID: `AG | agent-governance | T063 | root-4` — reserved NEW same-work-unit failover root; not yet started  
T063-V4-Candidate-Branch: `test/t063-adaptive-worker-routing-requalification-v4`  
T063-V4-Candidate-HEAD: `f06c8f48f7b1d59dff9fc117cca5b42453ad23e8`  
T063-V4-Candidate-Base: `9da2b6fed64ded9af8d38f67cd53cd066abef838`  
T063-V4-Launch-Authority: `docs/reviews/T063-R7.md`  
T063-V4-Race-Research: `docs/research/R022-T063-V3-EMPTY-ROLLOUT-REATTACH-RACE.md`  
Historical-T063-V3-Evidence-HEAD: `746519abc6f159e959120f68d5c9f920d88d5797`  
Historical-T063-V2-Evidence-HEAD: `3ff745a8d29e031ca818c1bc618b15a54e0cbf2b`  
Historical-T063-V1-Evidence-HEAD: `3d8a9460988351383a90adfc6b76e2deff056504`  
Held-Work-Unit: T062 / T023 v15 Stage 6  
Held-State: HUMAN_HOLD_R32_UNCONSUMED  
Chat-Closure: KEEP_CURRENT_CHAT

## Canonical transition

O264/R6 authorized T063 v3 on `root-3`.

The Human launched that authority. V3 terminated `BLOCKED` on the verified remote scientific branch:

```text
branch: test/t063-adaptive-worker-routing-requalification-v3
HEAD:   746519abc6f159e959120f68d5c9f920d88d5797
```

The run consumed one P1 ADAPTIVE parent/child first attempt. The exact child had started, but immediate public App Server `thread/resume` failed because persisted rollout/session metadata was not yet readable and the thread store reported an empty rollout.

No subsequent arm ran. No pilot decision exists. The consumed v3 P1 is invalid/unscored and historical.

R022 classifies the blocker as:

```text
BLOCKED_MEASUREMENT_SURFACE
cause: SAME_CHILD_ROLLOUT_PERSISTENCE_VISIBILITY_RACE
worker-quality failure: no
profile-resolution failure: no
D076 violation: no
```

ChatGPT Orchestrator re-entered D068 Stage 5 and published the successor v4 candidate without provider/model calls:

```text
branch: test/t063-adaptive-worker-routing-requalification-v4
HEAD:   f06c8f48f7b1d59dff9fc117cca5b42453ad23e8
base:   9da2b6fed64ded9af8d38f67cd53cd066abef838
```

## V4 candidate and persistence barrier

The v4 branch is three commits ahead of its exact `develop` base. It includes the repaired v3 executable evaluation package plus the v4 adapter and adapter tests; no committed Markdown authority or product-source change is present on the scientific branch.

All nine reused v3 code/test blobs were verified byte-for-byte against the repaired v3 state represented by:

```text
4a1bc28b83bffecc706df0f2e42aafe29456c54e
```

V4 changes only measurement reattachment behavior after the exact child is already correlated.

On exact empty-rollout thread-store failure only:

```text
wait 0.2 seconds
-> recheck exact parent loaded residency
-> if parent absent: BLOCK
-> retry thread/resume for the same exact child id/params
-> maximum 10 total resume attempts
```

The parent residency check occurs **after the delay and immediately before each retry**.

The adapter never replays `spawn_agent`, never restarts the parent turn, and never creates another child/provider turn. Reattachment RPC retries are counted separately from scored parent/child attempts.

Any nonmatching error, parent-residency loss, or retry exhaustion blocks fail-closed.

## Provider-free verification

Provider-free Orchestrator verification of the final v4 adapter candidate:

```text
v4 adapter tests:      6 passed
Python compileall:     PASS
Codex/App Server runs: 0
provider/model calls:  0
```

The executed v4 source/test copies matched the remote Git blobs exactly:

```text
evals/adaptive_worker_routing_v4/runner.py
  3996ad60619d8f4822707389e13878b5a134f7fe

tests/test_t063_adaptive_worker_routing_v4_adapter.py
  4c50e3a47c41d9cb42d1f709356ba89f924656ff
```

Stage 6 must still run repository-native deterministic lint/test/compile checks before the first provider-backed turn. Failure at that gate blocks with zero scored provider calls.

## D063 measurement preservation

R021's config-authoritative substantive child contract remains unchanged.

V4 retains the complete D063 exact-child measurement requirements:

```text
real parent/child correlation
parent activePermissionProfile.id == :read-only
non-contradictory legacy read-only projection
continuous loaded-parent residency before and through child reattachment
child parentThreadId == exact parent
child activePermissionProfile.id == :read-only
requested child model/reasoning from frozen Stage 5 config
resolved configured child model/reasoning exact match
exact non-estimated child-turn usage
exact child-turn duration
exact-child reroute observation
no tracked/global mutation attributable to measurement
```

Public child correlation remains:

```text
subAgentActivity(kind=Started, agentThreadId=<exact child>)
```

Internal raw-response events are not passing evidence.

`backend_served_profile_verified = false` remains controlling.

## D077 version-sensitive revalidation

Immediately before R7/O265, official upstream release state was revalidated.

Current stable remains:

```text
Codex 0.154.0
release tag: rust-v0.154.0
```

No newer stable appeared after R021/R6.

Exact source review establishes that `0.154.0` still calls persisted `read_stored_thread_for_resume(... include_history=false)` when reattaching an already-running thread and still contains the `rollout at <path> is empty` failure. Fresh upstream `main` review also retains the running-thread persisted-read dependency.

Therefore:

```text
version disposition: PIN_RETAINED
qualified runtime:   0.153.4
upgrade fixes race:  false based on current stable review
```

This does not qualify `0.154.0` or `main` under D063.

If a newer stable Codex release appears before Human launch of `root-4`, stop and return to Orchestrator for D077 relevance classification before any provider-backed execution.

## Scientific restart rule

V4 must be one homogeneous clean six-arm run:

```text
P1 ADAPTIVE -> CONTROL
P2 CONTROL  -> ADAPTIVE
P3 ADAPTIVE -> CONTROL
```

Historical v1/v2/v3 results are excluded from every v4 score, metric and pilot decision:

```text
v1  3d8a9460988351383a90adfc6b76e2deff056504
v2  3ff745a8d29e031ca818c1bc618b15a54e0cbf2b
v3  746519abc6f159e959120f68d5c9f920d88d5797
```

Frozen source/oracle baseline remains:

```text
69e910f329a2294c3b40df0f6ee983f9905f4677
```

No v4 provider/model calls have occurred.

## Launch profile

T063-R7 freezes:

```text
Executor:        Codex
Surface:         Codex Local / native Windows
Session:         NEW
Coordinator-ID:  AG | agent-governance | T063 | root-4
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

No model/effort/runtime substitution is authorized after provider-backed execution starts.

## D076 Stage 6 boundary

Codex executes/diagnoses/verifies the published v4 candidate and may make only bounded represented technical repairs that preserve R7 semantics.

Substantial missing executable controller/harness/fixture/oracle or a changed reattachment/receipt strategy is immediate Orchestrator re-entry. Persistence status does not change ownership.

Executor-authored committed Markdown remains prohibited.

The terminal evidence must audit both ordinary ephemeral aids and material ephemeral artifacts as required by `docs/EXECUTOR-HANDOFFS.md`.

## Evidence and terminal return

Normal evidence paths:

```text
handoffs/T063-adaptive-worker-routing-telemetry-v4.json
handoffs/T063-executor-handoff-v4.json
```

Terminal Human return after Codex completes or blocks:

```text
STATUS: COMPLETED | BLOCKED
HANDOFF: handoffs/T063-executor-handoff-v4.json
BRANCH: test/t063-adaptive-worker-routing-requalification-v4
HEAD: <actual remote pushed HEAD>
```

A `BLOCKED` terminal result authorizes no compensating provider call without new Orchestrator review.

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
- R007 remains `EVALUATING`; R7 authorizes an experiment, not a global routing policy.

## Next Chat Minimum Load

After normal bootstrap (`develop`, `AGENTS.md`, this checkpoint):

1. for pending T063 v4 launch or convergence, load `docs/reviews/T063-R7.md` first;
2. load R022 for the same-child persistence-race diagnosis and retry boundary;
3. load R021 only when config-authoritative child-contract details are needed;
4. load D063 before interpreting measurement validity;
5. load D076 before accepting Stage 6 repair/ephemeral executable behavior;
6. load D077 before consequential launch if upstream stable state changed;
7. load the v4 candidate adapter/v3 measurement implementation only when execution mechanics or evidence conflict requires it;
8. for T062 resumption, instead load T023-R31/R32/R33 plus the held scientific branch/handoff;
9. do not reconstruct either frontier from prior chat/Project Memory.

## Next Action

After O265/R7/R022 are integrated into `develop`, T063 v4 Stage 6 is authorized.

The Human should start a **NEW** Codex session with exact visible title:

```text
AG | agent-governance | T063 | root-4
```

Use the R7-frozen root profile and exact candidate branch/HEAD. The transport prompt must remain thin and load canonical authority from `develop`; the published candidate owns experiment mechanics and the scientific contract.

ChatGPT must not start or directly control Codex under D071.

After the Human returns the terminal four-line result, ChatGPT performs remote verification and Stage 7 convergence.
