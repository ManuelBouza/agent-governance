# Orchestrator Checkpoint

Checkpoint-ID: O279  
Date: 2026-09-12  
Current-Objective: T062 / T023 v15 — RIQ-NBC Stage 6 continuation  
State: T062_STAGE6_CONTINUATION_REAUTHORIZED_AWAITING_HUMAN_CODEX_CONTINUE  
Active-Executor: Codex  
Executor-Launch-State: AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Coordinator-ID: `AG | agent-governance | T062 | root-1` — CONTINUE when safely recoverable  
Task-Contract: `docs/tasks/T062-t023-riq-nbc-v15-reference-independent-evaluation.md`  
Current-Launch-Review: `docs/reviews/T023-R34.md`  
Prior-Continuation-Review: `docs/reviews/T023-R32.md`  
Prior-Hold-Review: `docs/reviews/T023-R33.md`  
Scientific-Branch: `test/t023-skill-activation-topology-evals-v15`  
Scientific-HEAD: `b9034e450f04fbc9736543425e531159d4b79d49`  
Stage5-Candidate: `3e0d0b71cf382db502e186622f40a23bcd915390`  
Freeze-E: `5b025087bc7b6996f683a34fdd1ce441d3d6dd82`  
Freeze-F: `5b8ac55980ecdbb6a2bf3784812b933647f2f13d`  
Provider-Model-Calls-Consumed: `0`  
D077-Disposition: `PIN_RETAINED` — Codex CLI `0.149.0`  
Chat-Closure: KEEP_CURRENT_CHAT

## Canonical transition

The Human Owner explicitly selected T062/T023 v15 on 2026-09-12 to leave `HUMAN_HOLD_R32_UNCONSUMED`, while forbidding automatic consumption of any prior execution without canonical revalidation.

T023-R34 completed that revalidation against current Git authority and records:

```text
T062 Stage 6:                   REAUTHORIZED
R32 authority:                 valid and previously unconsumed
scientific branch HEAD:        b9034e450f04fbc9736543425e531159d4b79d49
provider/model calls consumed: 0
D077:                          PIN_RETAINED at exact Codex CLI 0.149.0
session:                       CONTINUE T062 root-1 when safely recoverable
```

The scientific HEAD is still exactly one blocked-evidence commit above the terminal Stage 5 candidate and the only delta is `handoffs/T062-executor-handoff.json`. Freeze E and Freeze F remain ancestors. The persisted handoff records zero canary, acceptance, and total provider/model attempts.

No prior live execution is consumed by the resumed authority.

## D077 launch condition

T062 remains bound to the frozen live cell:

```text
Host:       Codex
Runtime:    native Windows
Model:      GPT-5.6 Sol
Reasoning:  Medium
Codex CLI:  exactly 0.149.0
```

Official OpenAI Codex release state checked during R34 revalidation:

```text
current stable:         0.154.0
higher prerelease seen: 0.155.0-alpha.3.9
```

The pin is retained because CLI `0.149.0` is part of the prospective scientific cell and the prior blocker occurred before process creation at the external-transmission/cost-approval boundary. Moving to a newer CLI would change the experiment surface rather than transparently repair the blocker.

Before any provider-backed call, exact `0.149.0` must be available and verified. If the official stable release advances beyond `0.154.0` before Human launch, stop for D077 reclassification rather than executing on stale upstream assumptions.

## D076 launch condition

D076 applies prospectively to resumed Stage 6.

The Executor may execute, diagnose, boundedly repair the already-published harness, and use small subordinate execution mechanics. It must stop before first-pass creation of a substantial new controller, harness, oracle, semantic fixture generator, workflow state machine, or equivalent material executable artifact and request Orchestrator Stage 5 re-entry.

Any file-based ephemeral executable aid actually used must be represented in terminal handoff evidence as required by D076.

## Continuity and transport

D060/D058 make `CONTINUE` on `AG | agent-governance | T062 | root-1` the normal path because this is the same Task Contract and blocked work unit.

Continuation is valid only if the Human can identify the same recoverable T062 coordinator, represented scientific branch/workspace, and exclusive task worktree, and that coordinator can reload current authority from `origin/develop`.

If identity, workspace ownership, recoverability, or instruction freshness cannot be established, do not guess and do not silently create another root. Return for Orchestrator failover classification.

D071 remains controlling: ChatGPT does not invoke Codex directly. ChatGPT renders the launch card and complete thin transport prompt; the Human performs the Codex CONTINUE action and returns terminal STATUS/HANDOFF/BRANCH/HEAD after execution.

## Resumed Stage 6 order

Before any provider/model call, the Executor must:

1. fetch `origin` and load current `origin/develop`, `AGENTS.md`, the T062 Task Contract, R31/R32/R33/R34, D076 and D077;
2. revalidate the exact scientific branch/HEAD, parent/delta relation, Freeze E/F ancestry, and zero-call accounting;
3. rerun required provider-free integrity/verification gates;
4. verify native Windows, GPT-5.6 Sol, Medium, exact Codex CLI `0.149.0`, and current D077 stable-release assumption;
5. perform the previously blocked backend/workspace/model behavioral preflight;
6. only then execute the frozen 2/2 canary followed by the frozen acceptance schedule within the existing T062/R32 ceilings;
7. persist and push terminal evidence for Orchestrator review.

Any mismatch is fail-closed. No scientific semantics, frozen inputs, candidate set, model, reasoning, runtime, CLI version, or attempt ceiling may be silently changed.

## Closed/frozen adjacent work

T063 remains closed under O278/T063-R20 as frozen mapping `NOT QUALIFIED`. Do not reopen it, rerun it, or reuse any T063 observations as scored T062 evidence.

T058 remains frozen by explicit Human decision. Do not resume, integrate, clean, copy, or otherwise consume it without new explicit Human authorization.

## Next Chat Minimum Load

After normal bootstrap (`develop`, `AGENTS.md`, this checkpoint):

1. load `docs/reviews/T023-R34.md` first for T062 launch authority;
2. load the T062 Task Contract;
3. load R32/R33 only when destination/payload/cost or prior-hold provenance is needed;
4. load the scientific handoff when zero-call/blocker evidence is needed;
5. apply D076/D077 prospectively;
6. do not reconstruct the frontier from prior chat/Project Memory;
7. do not load or reuse T063 scored observations for T062.

## Next Action

Render the D055 launch card separately, then the complete thin D071 transport prompt for Human-mediated Codex `CONTINUE` on `AG | agent-governance | T062 | root-1`.

The Human selects the existing recoverable T062 coordinator, configures GPT-5.6 Sol / Medium on native Windows, and pastes the prompt. The Executor must complete all provider-free launch gates before issuing any provider/model call.

If the required coordinator/workspace identity is not safely recoverable, if exact Codex CLI `0.149.0` is unavailable, if the scientific HEAD moved, if zero-call accounting no longer holds, or if the official stable Codex release has advanced beyond `0.154.0`, execution is not authorized and must return to the Orchestrator.