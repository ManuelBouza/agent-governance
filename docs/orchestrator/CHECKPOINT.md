# Orchestrator Checkpoint

Checkpoint-ID: O262  
Date: 2026-09-10  
Current-Objective: T063 — adaptive worker routing requalification  
State: T063_V2_STAGE6_AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Active-Executor: Codex  
Executor-Launch-State: AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Coordinator-ID: `AG | agent-governance | T063 | root-2`  
T063-V2-Branch: `test/t063-adaptive-worker-routing-requalification-v2`  
Historical-T063-Evidence-Branch: `test/t063-adaptive-worker-routing-requalification`  
Historical-T063-Evidence-HEAD: `3d8a9460988351383a90adfc6b76e2deff056504`  
Held-Work-Unit: T062 / T023 v15 Stage 6  
Held-State: HUMAN_HOLD_R32_UNCONSUMED  
Chat-Closure: KEEP_CURRENT_CHAT

## Canonical transition

O261 required Orchestrator re-entry after the blocked T063 run and D076 correction.

The Human continued the T063 repair path. ChatGPT then materialized a complete published Stage 5 harness rather than delegating substantial controller reconstruction to Codex.

New controlling records:

```text
docs/research/R019-T063-MULTI-AGENT-V2-HARNESS-REENTRY.md
docs/reviews/T063-R4.md
```

The executable candidate is published under:

```text
evals/adaptive_worker_routing/
tests/test_t063_adaptive_worker_routing_harness.py
```

The exact remote candidate/authority SHA is the remotely verified HEAD of `test/t063-adaptive-worker-routing-requalification-v2` containing O262 and T063-R4. The Human launch card must state that exact SHA; no remembered or locally inferred SHA controls.

## Stage 5 verification

Provider-free candidate verification before publication:

```text
python -m pytest -q tests/test_t063_adaptive_worker_routing_harness.py
21 passed

python -m compileall -q evals tests
PASS

provider/model calls during repair: 0
```

## R019 adapter correction

Fresh exact-source revalidation of `rust-v0.153.4` established:

```text
Multi-Agent V2 spawn requires: message + task_name
no-history V2 spawn uses:      fork_turns = "none"
fork_context in V2:            rejected
model/reasoning exposure:      explicit config required
multi_agent_v2 default:        disabled
V2 collab prompt receipt:      insufficient for full message attestation
```

The harness therefore forces:

```text
features.multi_agent=true
features.multi_agent_v2.enabled=true
features.multi_agent_v2.expose_spawn_agent_model_overrides=true
```

and verifies exact child task-message equality from the child thread before scoring.

Codex `0.154.0` is now the current stable release, but T063 v2 remains deliberately pinned to exact `0.153.4` because D063 qualified that surface and R2 froze it as the experiment baseline. This is now an explicit experimental pin, not a claim that `0.153.4` remains vendor-current.

## Scientific restart

The v2 pilot is a full clean rerun.

Historical P1/P2 PASS results remain preserved evidence but are excluded from final v2 scoring because the corrected harness changes material execution conditions.

Fresh scored order remains:

```text
P1 ADAPTIVE -> CONTROL
P2 CONTROL  -> ADAPTIVE
P3 ADAPTIVE -> CONTROL
```

Frozen probe source/oracle baseline remains:

```text
69e910f329a2294c3b40df0f6ee983f9905f4677
```

Frozen child profiles remain:

```text
P1 ADAPTIVE  gpt-5.6-luna  / medium
P1 CONTROL   gpt-5.6-sol   / medium
P2 CONTROL   gpt-5.6-sol   / medium
P2 ADAPTIVE  gpt-5.6-terra / medium
P3 ADAPTIVE  gpt-5.6-terra / high
P3 CONTROL   gpt-5.6-sol   / medium
```

Frozen task-message SHA-256 values:

```text
P1  9aa60aef807873669690a2ad2b564fed58e0731ff0d6e0162fbef40c621a2164
P2  031c06d7544f6146901e633d4bceb8af0e15325c0124dc586e10f545aaadfe4a
P3  9d980424d08517c72911eaacaa9cee36ddf2003d50c21ad6b4d0c25786d9554f
```

## P3 correction

The published harness creates the P3 fixture under a fresh runtime directory that must be an unused sibling of the exclusive T063 v2 worktree, outside the repository and outside Windows system temp.

The fixture semantics/oracle remain frozen from `69e910...`; the Executor supplies the safe runtime-root location only. The harness verifies exact fixture SHA, host readability and cleanup.

## D060/D055 launch authority

Use:

```text
Executor:        Codex
Surface:         Codex Local / native Windows
Session:         NEW
Coordinator-ID:  AG | agent-governance | T063 | root-2
Model:           gpt-5.6-sol
Effort:          medium
Codex/App Server: exactly 0.153.4
Auth:            chatgpt
```

Root-2 is justified D060 failover/re-entry. Root-1 is historical, has observed the blocked-run results/failure context, and predates the new published harness; continuing it would contaminate the clean rerun boundary.

D071/D072/D073 control Human-mediated transport/title behavior.

## D076 Stage 6 boundary

Codex executes/diagnoses/repairs/verifies the published harness. It does not recreate another substantial private controller.

Any non-candidate file-based executable aid actually used by Stage 6 must be inventoried as `ephemeral_artifacts`. A `material` or `uncertain` missing-candidate artifact is an immediate Orchestrator re-entry condition.

The final normal evidence paths are:

```text
handoffs/T063-adaptive-worker-routing-telemetry-v2.json
handoffs/T063-executor-handoff-v2.json
```

No Executor-authored committed Markdown is authorized.

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
- D066 intentional gaps remain unchanged.
- R007 remains `EVALUATING`; T063 v2 has not produced a pilot result yet.
- Historical T063 evidence branch/HEAD remains preserved and must not be rewritten.

## Next Chat Minimum Load

After normal bootstrap (`develop`, `AGENTS.md`, this checkpoint):

1. for T063 v2 execution return, load `docs/reviews/T063-R4.md` first;
2. load T063 and D063 only when interpreting/scoring terminal evidence or a measurement blocker;
3. load R019 only when adapter/version/message-transport provenance is material;
4. load T063-R3 and historical handoff/telemetry only when comparing against the blocked run or diagnosing regression;
5. load D076 when Stage 6 reports any non-candidate file-based executable artifact;
6. for T062 resumption, instead load T023-R31/R32/R33 plus the held scientific branch/handoff;
7. do not reconstruct either frontier from prior chat/Project Memory.

## Next Action

Human-mediated Codex transport is next.

The Human must start a **NEW** Codex session using the exact launch card supplied by ChatGPT:

```text
Coordinator-ID: AG | agent-governance | T063 | root-2
Model: gpt-5.6-sol
Effort: medium
Native runtime: exact Codex/App Server 0.153.4
```

The Human pastes the complete T063-R4 transport prompt. Codex executes the published candidate and returns only:

```text
STATUS: COMPLETED | BLOCKED
HANDOFF: handoffs/T063-executor-handoff-v2.json
BRANCH: test/t063-adaptive-worker-routing-requalification-v2
HEAD: <actual remote pushed HEAD>
```

ChatGPT then verifies remote Git before accepting any scientific result.
