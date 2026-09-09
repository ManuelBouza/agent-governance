# Orchestrator Checkpoint

Checkpoint-ID: O257  
Date: 2026-09-09  
Current-Objective: T023 / T062 — v15 RIQ-NBC reference-independent evaluation  
State: STAGE6_CONTINUATION_AUTHORIZED_AWAITING_HUMAN_CODEX_CONTINUE  
Active-Executor: Codex  
Stage6-Authorization: AUTHORIZED_BY_R31_AND_EXPLICIT_R32_PROVIDER_DESTINATION_PAYLOAD_COST_GO  
Coordinator-ID: `AG | agent-governance | T062 | root-1`

## Canonical frontier

T062 Stage 6 was launched under `docs/reviews/T023-R31.md`. The first Executor attempt returned a durable `BLOCKED` handoff because the managed Codex approval boundary rejected the provider-backed harness command before process creation.

Verified blocked scientific branch HEAD:

`test/t023-skill-activation-topology-evals-v15@b9034e450f04fbc9736543425e531159d4b79d49`

Blocked handoff:

`handoffs/T062-executor-handoff.json`

Remote comparison from terminal Stage 5 HEAD `3e0d0b71cf382db502e186622f40a23bcd915390` to blocked HEAD `b9034e45...` contains exactly one commit and one added path: the JSON handoff. No executable/scientific/Markdown path changed on the scientific branch.

The Human Owner then explicitly authorized provider-backed continuation on 2026-09-09T08:37:00+02:00 by replying `go` to the Orchestrator's destination/payload/cost authorization. The controlling continuation review is:

`docs/reviews/T023-R32.md`

R32 does not broaden scientific semantics. It supplies the explicit external-transmission/cost authorization required to continue the already-approved T062 experiment.

## Frozen scientific boundaries

```text
terminal Stage 5 scientific HEAD: 3e0d0b71cf382db502e186622f40a23bcd915390
Candidate Freeze E:              5b025087bc7b6996f683a34fdd1ce441d3d6dd82
Holdout/oracle Freeze F:         5b8ac55980ecdbb6a2bf3784812b933647f2f13d
blocked Stage 6 evidence HEAD:   b9034e450f04fbc9736543425e531159d4b79d49
```

All are durable and must not be rewritten/reset/rebased/force-pushed.

Frozen identities remain:

```text
strategy:              RIQ-NBC
evaluation:            MG1-T023-EVALUATION-v15
candidate hashes:      MG1-T023-CANDIDATE-HASHES-v3
capability source:     MG1-2026-09-06-v4
topology metadata:     MG1-T023-TOPOLOGIES-v4
presentation:          MG1-T023-PRESENTATIONS-v5
corpus:                MG1-T023-CORPUS-v9
oracle:                MG1-T023-TOPOLOGY-ORACLE-v15
execution:             MG1-T023-EXECUTION-v15
trial envelope:        MG1-T023-TRIAL-ENVELOPE-v3
candidates:            B2 / F2 / G3
```

No v12/v13/v14 observation may enter v15 scoring.

## Accepted blocked Stage 6 evidence

The remote handoff at `b9034e45...` records provider-free completion and was verified against GitHub:

```text
candidate integrity: PASS
holdout integrity: PASS
ruff check: PASS
ruff format --check: PASS
full locked pytest: 484 passed
code health: PASS
symbol map: PASS
frozen-input/scheduler validation: PASS
v15 characterization: 31 passed
exact cached native-Windows Codex CLI 0.149.0: PASS
provider/model calls: 0
backend/workspace/model behavioral preflight: NOT_RUN
synthetic canary: NOT_RUN
B2/F2/G3 acceptance: NOT_RUN
topology selected: no
```

The command rejection occurred before provider-backed process creation. This is an authorization blocker, not scientific evidence and not a harness-command defect.

## Explicit provider authorization

R32 records explicit Human authorization for:

### Destination

OpenAI Codex only, using the authenticated frozen scientific cell:

```text
runtime: native Windows
model: GPT-5.6 Sol
reasoning: Medium
Codex CLI: exactly 0.149.0
```

No other external destination is authorized.

### Payload

Transmission to OpenAI Codex of only the frozen T062 v15 evaluation prompts and candidate/fixture/workspace content deliberately exposed by the accepted harness for:

- backend/workspace/model behavioral preflight;
- unchanged synthetic canary;
- B2/F2/G3 acceptance execution.

Unrelated repository data, credentials, secrets, private tokens and material outside the frozen evaluation envelope are not authorized for transmission.

### Usage and cost

The Human explicitly accepts ordinary OpenAI provider usage/cost on the existing account/plan within the frozen limits:

```text
synthetic canary maximum attempts: 4
acceptance model-attempt ceiling: 1260
absolute Stage 6 provider/model attempt ceiling: 1264
per-attempt timeout: 180 seconds
```

The blocked attempt issued `0` provider/model calls, so the complete frozen attempt ceiling remains available.

No separate purchase, subscription/plan change, credential change or new billing arrangement is authorized. Such a requirement is a new Human gate.

## Continuation profile

```text
Executor: Codex
Session: CONTINUE
Coordinator-ID: AG | agent-governance | T062 | root-1
Model: GPT-5.6 Sol
Reasoning: Medium
Runtime: native Windows
Codex CLI: exactly 0.149.0
```

`CONTINUE` is required because this is a clean same-task/same-branch continuation from a single managed-approval blocker with durable evidence, no semantic drift and zero provider/model calls.

## Continuation revalidation and resume point

The prior provider-free suite may be reused only if Codex first confirms:

1. remote scientific branch still equals `b9034e450f04fbc9736543425e531159d4b79d49`;
2. `b9034e45...` remains a direct child of `3e0d0b71...` and its only delta is `handoffs/T062-executor-handoff.json`;
3. Freeze E/F remain exact ancestors;
4. current `origin/develop` contains R31 and R32;
5. v15 candidate-integrity guard PASS;
6. v15 holdout-integrity guard PASS;
7. provider/model calls still equal exactly `0`;
8. exact native-Windows Codex CLI `0.149.0` remains active.

If these checks pass, resume at the previously blocked backend/workspace/model behavioral preflight. Do not repeat the full `484`-test provider-free suite merely for ceremony.

If any executable/scientific drift exists, fail closed or rerun the complete R31 provider-free sequence as technically appropriate before any provider-backed call.

After approved preflight:

1. unchanged synthetic canary, require `2/2 PASS`;
2. full independent acceptance schedule: per ordered case `B2 -> F2 -> G3`, all r1 then all r2, r3 only for unstable pairs, no r4;
3. preserve frozen thresholds, aggregation, budgets and RIQ-NBC selection semantics;
4. B2 scientific non-qualification remains non-blocking;
5. F2/G3 exact scientific futility may stop only candidate-locally;
6. technical/epoch/integrity invalidity remains global fail-closed STOP;
7. Executor Code Review & Verify plus D065 re-evaluation;
8. update/push `handoffs/T062-executor-handoff.json` and terminal non-Markdown evidence.

Executor must not select a topology. Stage 7 convergence/selection remains Orchestrator-owned.

If the managed approval system still rejects the provider-backed command after R32's explicit authorization, do not bypass/disable it; return `BLOCKED` with the exact denial and call counts.

## D061 / D062 state

Continuation-authority authoring base:

`develop@0b3685a2d2bc5ad6988e8839f3dc188602a04307`

Orchestrator writes use verified topic branch:

`docs/t062-v15-provider-continuation-auth`

Ruleset `22339910` was revalidated active over `main`/`develop`, requiring PR transport, blocking deletion/non-fast-forward updates and providing no routine bypass.

## Other frontier constraints

- T024 remains unauthorized until T023 has an accepted topology selection from Stage 7 convergence over valid Stage 6 evidence.
- T058 remains frozen by explicit Human decision; do not resume, integrate, clean or copy it without new explicit Human authorization.
- D066 intentional gaps remain unchanged.
- Historical scientific branches remain immutable.

## Next Chat Minimum Load

At the start of the next chat, after reading current `develop`, `AGENTS.md` and this checkpoint:

1. load `docs/tasks/T062-t023-riq-nbc-v15-reference-independent-evaluation.md`;
2. load `docs/reviews/T023-R31.md` and `docs/reviews/T023-R32.md`;
3. load `handoffs/T062-executor-handoff.json` from the current scientific branch;
4. for Codex continuation/transport, load D071/D072/D073;
5. load R30 only if Stage 5 readiness details are needed;
6. load D074/R28 only if a semantic-selection conflict must be resolved;
7. do not reconstruct the frontier from prior chats or Project Memory.

## Next Action

Human performs D071 continuation transport:

1. continue the existing Codex coordinator `AG | agent-governance | T062 | root-1`;
2. preserve native Windows / GPT-5.6 Sol / Medium / exact Codex CLI `0.149.0`;
3. paste the complete R32 continuation prompt rendered by ChatGPT;
4. let Codex resume from the blocked provider-backed preflight under the explicit R32 destination/payload/cost authorization;
5. return only:

```text
STATUS: <COMPLETED|BLOCKED>
HANDOFF: handoffs/T062-executor-handoff.json
BRANCH: test/t023-skill-activation-topology-evals-v15
HEAD: <remote pushed HEAD sha>
```

After terminal return, ChatGPT verifies remote Git and performs D068 Stage 7 convergence. No additional `go` is required for this continuation.
