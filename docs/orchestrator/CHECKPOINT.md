# Orchestrator Checkpoint

Checkpoint-ID: O265  
Date: 2026-09-11  
Current-Objective: T063 — adaptive worker routing requalification  
State: T063_V4_STAGE6_AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Active-Executor: none — Codex Desktop selected for pending Human launch  
Executor-Launch-State: AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Coordinator-ID: `AG | agent-governance | T063 | root-4` — reserved NEW failover root; not yet started  
T063-V4-Candidate-Branch: `test/t063-adaptive-worker-routing-requalification-v4`  
T063-V4-Candidate-HEAD: `89da4d5b5fbeeb32e6dcf4dd4fde7839f043dfa5`  
T063-V4-Candidate-Base: `9da2b6fed64ded9af8d38f67cd53cd066abef838`  
T063-V4-Launch-Authority: `docs/reviews/T063-R7.md`  
T063-V4-Adapter-Research: `docs/research/R022-T063-V3-EMPTY-ROLLOUT-REATTACH-RACE.md`  
Historical-T063-V3-Evidence-HEAD: `746519abc6f159e959120f68d5c9f920d88d5797`  
Historical-T063-V2-Evidence-HEAD: `3ff745a8d29e031ca818c1bc618b15a54e0cbf2b`  
Historical-T063-V1-Evidence-HEAD: `3d8a9460988351383a90adfc6b76e2deff056504`  
Held-Work-Unit: T062 / T023 v15 Stage 6  
Held-State: HUMAN_HOLD_R32_UNCONSUMED  
Chat-Closure: KEEP_CURRENT_CHAT

## Canonical transition

O264/R6 authorized a clean T063 v3 execution. The Human launched NEW Codex root-3 and returned:

```text
STATUS: BLOCKED
HANDOFF: handoffs/T063-executor-handoff-v3.json
BRANCH: test/t063-adaptive-worker-routing-requalification-v3
HEAD: 746519abc6f159e959120f68d5c9f920d88d5797
```

Remote verification confirmed that returned HEAD exactly matches the branch.

The terminal v3 state is accepted by:

```text
docs/research/R022-T063-V3-EMPTY-ROLLOUT-REATTACH-RACE.md
docs/reviews/T063-R7.md
```

## V3 terminal accounting

Accepted accounting:

```text
scored parent turns:       1
scored child attempts:     1
valid scored children:     0
diagnostic child attempts: 0
compensating attempts:     0
invalid attempt:            P1 ADAPTIVE
pilot_decision:             null
```

The v3 P1 ADAPTIVE attempt is invalid/unscored historical evidence and cannot be reused.

No worker-quality or profile-resolution conclusion is drawn from it.

## V3 Stage 6 review

The represented pre-provider repair:

```text
4a1bc28b83bffecc706df0f2e42aafe29456c54e
```

contains bounded Ruff/formatting repair only and is accepted under D068/D076.

V3 terminal evidence reports no material ephemeral executable artifact, no Executor Markdown mutation and no raw-response-event use.

## Desktop runtime result

V3 native preflight proved the effective Codex Desktop runtime was:

```text
bundled/effective codex.exe: 0.153.4
App Server:                  0.153.4
auth category:               chatgpt
```

No separate standalone CLI installation is required when the Desktop-bundled runtime satisfies this gate.

## V3 blocker root cause

The child was publicly correlated through:

```text
subAgentActivity(kind=Started, agentThreadId=<exact child>)
```

but immediate `thread/resume` failed because the new child rollout JSONL existed before its first metadata line was durable:

```text
thread-store error
failed to read session metadata
rollout ... is empty
```

Exact source review establishes that the running-thread resume path reads persisted rollout metadata before it rejoins/returns the in-memory running thread. Therefore `Started` and rollout-metadata durability have a narrow race.

Classification:

```text
BLOCKED_EXECUTION_INVALID
cause: CODEX_APP_SERVER_EMPTY_ROLLOUT_REATTACH_RACE
worker quality failure:      NO
profile resolution failure:  NO
D076 violation:              NO
Executor noncompliance:      NO
```

## D077 result

R022 reviewed the relevant resume path in:

```text
0.153.4
0.154.0
0.155.0-alpha.2
current upstream main
```

The higher reviewed versions preserve the same material path and do not remove the blocker.

```text
version disposition: PIN_RETAINED
retained runtime:     0.153.4
upgrade fixes blocker: false
```

If a newer stable release appears before v4 provider execution, classify its relevance under D077 before continuing.

## V4 Stage 5 candidate

ChatGPT Orchestrator published a clean successor candidate:

```text
branch: test/t063-adaptive-worker-routing-requalification-v4
base:   9da2b6fed64ded9af8d38f67cd53cd066abef838
HEAD:   89da4d5b5fbeeb32e6dcf4dd4fde7839f043dfa5
```

The candidate is one commit ahead of its base and contains only eval/test material.

It reuses the accepted pre-provider repaired v3 harness/test blobs and adds:

```text
evals/adaptive_worker_routing_v4/__init__.py
evals/adaptive_worker_routing_v4/__main__.py
evals/adaptive_worker_routing_v4/runner.py
tests/test_t063_adaptive_worker_routing_v4_adapter.py
```

No v4 provider/model calls have occurred.

## V4 persistence barrier

V4 changes only child reattachment mechanics:

```text
thread/resume same exact child
  if exact empty-rollout race:
    confirm exact parent remains loaded
    wait 0.2 seconds
    retry same thread/resume
    maximum 10 attempts / 1.8 seconds total retry wait
  any other resume error:
    fail immediately
  exhaustion or parent loss:
    fail closed
```

Retries create no child and no provider/model turn. Retry count and result are persisted separately from provider attempt accounting.

All R6 experiment semantics remain frozen: probes, task-message digests, profile matrix, matched order, D063 receipts, oracles, first-attempt scoring and pilot definitions.

## Mandatory pre-provider Stage 6 gate

The Orchestrator environment could not execute a remote checkout. Before any provider-backed scored call, Codex must establish:

```text
both targeted v3 + v4 pytest suites PASS
repository Ruff check PASS for v3/v4 candidate/test paths
Python compile check PASS
exact Desktop-bundled/effective codex.exe == 0.153.4
exact App Server == 0.153.4
auth == chatgpt
all R7/D063 native preflight gates PASS
```

Bounded represented formatting/technical repair is allowed only when it preserves R7 semantics. A material adapter/probe/oracle/profile/scoring change requires Orchestrator re-entry before provider work.

## Scientific restart

V4 must be one clean homogeneous six-arm run:

```text
P1 ADAPTIVE -> CONTROL
P2 CONTROL  -> ADAPTIVE
P3 ADAPTIVE -> CONTROL
```

All v1/v2/v3 scored/invalid attempts are excluded from v4 scoring.

Frozen source/oracle baseline remains:

```text
69e910f329a2294c3b40df0f6ee983f9905f4677
```

## Launch profile

```text
Executor/UI:      Codex Desktop / native Windows
Session:          NEW
Coordinator-ID:   AG | agent-governance | T063 | root-4
Root model:       gpt-5.6-sol
Root reasoning:   medium
Effective codex.exe: exactly 0.153.4
App Server:          exactly 0.153.4
Auth:                chatgpt
```

Root-3 is historical and must not be reused because it observed the consumed v3 attempt/failure context.

Child matrix remains:

```text
P1 ADAPTIVE  gpt-5.6-luna  / medium
P1 CONTROL   gpt-5.6-sol   / medium
P2 CONTROL   gpt-5.6-sol   / medium
P2 ADAPTIVE  gpt-5.6-terra / medium
P3 ADAPTIVE  gpt-5.6-terra / high
P3 CONTROL   gpt-5.6-sol   / medium
```

## Evidence and terminal return

Normal evidence paths:

```text
handoffs/T063-adaptive-worker-routing-telemetry-v4.json
handoffs/T063-executor-handoff-v4.json
```

Terminal Human return:

```text
STATUS: COMPLETED | BLOCKED
HANDOFF: handoffs/T063-executor-handoff-v4.json
BRANCH: test/t063-adaptive-worker-routing-requalification-v4
HEAD: <actual remote pushed HEAD>
```

No blocked v4 arm authorizes a compensating provider call.

## T062 held frontier

T023-R33 remains controlling. T062 is not resumed.

```text
scientific branch:               test/t023-skill-activation-topology-evals-v15
terminal Stage5 HEAD:            3e0d0b71cf382db502e186622f40a23bcd915390
Candidate Freeze E:              5b025087bc7b6996f683a34fdd1ce441d3d6dd82
Holdout/oracle Freeze F:         5b8ac55980ecdbb6a2bf3784812b933647f2f13d
blocked Stage6 evidence HEAD:    b9034e450f04fbc9736543425e531159d4b79d49
provider/model calls:            0
R32 continuation authority:     valid but unconsumed
T023-R33 state:                  HUMAN_HOLD
```

Do not execute the old T062 R32 continuation prompt.

## Other durable constraints

- R007 remains `EVALUATING`; no global adaptive routing policy is adopted.
- T024 remains unauthorized until T023 selects a topology from valid evidence.
- T058 remains frozen by explicit Human decision.
- D061/D062 still require PR-mediated long-lived branch mutation.
- D071 still requires Human-mediated Codex transport.
- D076 applies to every Stage 6 executable aid/repair.

## Next Chat Minimum Load

After normal bootstrap (`develop`, `AGENTS.md`, this checkpoint):

1. for pending T063 v4 launch or convergence, load `docs/reviews/T063-R7.md` first;
2. load R022 for empty-rollout root cause/version rationale;
3. load D063 before interpreting measurement validity;
4. load D076 before accepting any Stage 6 repair/ephemeral executable behavior;
5. load the v4 adapter plus reused v3 candidate only when execution mechanics/evidence conflict requires it;
6. for T062 resumption, instead load T023-R31/R32/R33 plus the held branch/handoff;
7. do not reconstruct frontiers from prior chat or Project Memory.

D077 remains bootstrap-visible in `AGENTS.md`.

## Next Action

After R022/R7/O265 and the research-registry update are merged into `develop`, T063 v4 Stage 6 is authorized.

The Human should start a **NEW** Codex Desktop session with exact title:

```text
AG | agent-governance | T063 | root-4
```

Use the R7-frozen launch profile and exact candidate branch/HEAD. The transport prompt should remain thin and point to canonical Git authority.

ChatGPT must not start or directly control Codex. After the Human returns the terminal four-line result, ChatGPT performs remote verification and Stage 7 convergence.
