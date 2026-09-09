# Orchestrator Checkpoint

Checkpoint-ID: O256  
Date: 2026-09-09  
Current-Objective: T023 / T062 — v15 RIQ-NBC reference-independent evaluation  
State: STAGE6_AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Active-Executor: Codex  
Stage6-Authorization: AUTHORIZED_BY_EXPLICIT_HUMAN_GO_AND_T023_R31  
Coordinator-ID: `AG | agent-governance | T062 | root-1`

## Canonical frontier

The Human Owner explicitly launched T062 / D068 Stage 6 on 2026-09-09T07:51:45+02:00 by replying `go` after canonical O255 required a separate explicit Human launch.

Current Stage 6 launch authority:

`docs/reviews/T023-R31.md`

Stage 5 readiness remains:

`docs/reviews/T023-R30.md`

Task Contract remains:

`docs/tasks/T062-t023-riq-nbc-v15-reference-independent-evaluation.md`

Protected `develop` revalidated immediately before launch-gate authoring:

`7cf9a60762cfe07eecd33d94e7cdfbec33fc67a2`

The launch gate is Markdown-only. It does not alter scientific candidate/reference/corpus/oracle/trial-envelope bytes or any frozen selection semantics.

## Scientific branch and frozen boundaries

Represented scientific branch:

`test/t023-skill-activation-topology-evals-v15`

Terminal Stage 5 scientific HEAD / expected remote branch HEAD before substantive Stage 6 execution:

`3e0d0b71cf382db502e186622f40a23bcd915390`

Candidate Freeze E:

`5b025087bc7b6996f683a34fdd1ce441d3d6dd82`

Holdout/oracle Freeze F:

`5b8ac55980ecdbb6a2bf3784812b933647f2f13d`

Remote launch revalidation confirmed the scientific branch still equals the terminal Stage 5 HEAD and both Freeze E and Freeze F remain exact ancestors of it. These boundaries are immutable; do not rewrite/reset/rebase/force-push them.

## Stage 5 readiness receipt

Terminal Stage 5 tree:

`11cd1a5df9b66419f80f7a382181585a616f920a`

Provider-free validation artifact:

```text
name: t062-v15-final-tree
artifact id: 10068441857
sha256: 70841ac0f8f9d3869786eea5a0bb8b14b966e5501b8b32918e3ee7db8c40ffef
```

Exact terminal hosted-validation receipt:

```text
run: 34271270963
job: 102213170730
validated SHA: 3e0d0b71cf382db502e186622f40a23bcd915390
candidate guard: PASS
holdout guard: PASS
harness validate: PASS
ruff check: PASS
ruff format --check: PASS
code health: PASS
symbol map: PASS
characterization: 37 passed
full pytest: 484 passed
provider/model calls: 0
result: SUCCESS
```

Stage 5 launched no Executor and issued exactly `0` scientific provider/model calls.

## D061 / D062 launch revalidation

D061 routing remains fail-closed: the Orchestrator launch gate is authored only on verified short-lived topic branch `docs/t062-v15-stage6-launch`, created from exact `develop@7cf9a60762cfe07eecd33d94e7cdfbec33fc67a2`, then returned through PR.

GitHub ruleset `22339910` remains:

```text
name: Protect long-lived branches
enforcement: active
targets: main, develop
pull request required: yes
deletion blocked: yes
non-fast-forward blocked: yes
bypass actors: none
current user bypass: never
```

No direct Orchestrator content write to `develop` or `main` is authorized.

## Frozen scientific identities

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

B0/B1 remain historical and unscheduled. No v12/v13/v14 observation may enter v15 scoring.

## D055 / D058 launch profile

```text
Executor: Codex
Surface: Codex Local / native Windows
Session: NEW
Coordinator-ID: AG | agent-governance | T062 | root-1
Model: GPT-5.6 Sol
Reasoning: Medium
Codex CLI: exactly 0.149.0
```

This is the first Executor launch for T062, so `NEW` / `root-1` is required. No newer CLI/model/effort is accepted merely because it is available.

If the exact native-Windows / GPT-5.6 Sol / Medium / Codex CLI `0.149.0` cell cannot be realized, Stage 6 fails closed before any provider-backed v15 evaluation call.

## Mandatory Stage 6 execution order

The Executor must fail closed in this order:

1. safe Git synchronization and represented branch/head/Freeze E/F ancestry verification;
2. candidate-integrity guard;
3. holdout-integrity guard;
4. `ruff check`;
5. `ruff format --check`;
6. full locked `pytest`;
7. code-health and symbol-map checks;
8. frozen-input/scheduler characterization and proof that T062 Stage 6 provider/model calls so far equal exactly `0`;
9. native-Windows backend/workspace/version preflight for the exact live cell;
10. unchanged synthetic canary requiring `2/2 PASS`;
11. full independent B2/F2/G3 acceptance schedule;
12. Executor-owned Code Review & Verify, including D065 delegation re-evaluation;
13. pushed terminal non-Markdown handoff/evidence.

No canary or acceptance observation may run before every preceding gate passes.

Acceptance scheduler remains:

```text
per ordered case: B2 -> F2 -> G3
base repetitions: all r1, then all r2
r3: unstable candidate/case pairs only
r4: forbidden
```

B2 scientific non-qualification is non-blocking and does not suppress F2/G3 measurement. B2 still receives its complete required measurement. Exact scientific futility may stop F2 or G3 only candidate-locally. Technical/epoch/integrity invalidity remains a global fail-closed STOP.

Budgets remain:

```text
per candidate base valid observations: 140
per candidate maximum valid observations: 210
global base valid observations: 420
global maximum valid observations: 630
max model attempts / scheduled observation: 2
acceptance model-attempt ceiling: 1260
synthetic canary maximum attempts: 4
absolute Stage 6 provider/model attempt ceiling: 1264
per-attempt timeout: 180 seconds
```

Selection semantics remain exactly T062/D074. The Executor produces measurement/verification evidence but does not perform D068 Stage 7 topology selection.

## Ownership and transport boundary

- Orchestrator owns completed Stage 5 materialization and D052 semantic conformance.
- Executor now owns authorized Stage 6 execution/diagnosis/bounded technical repair/verification under R31/T062.
- Orchestrator retains Stage 7 convergence/acceptance/integration/topology-selection authority.
- Future terminal handoff path is `handoffs/T062-executor-handoff.json`.
- D071 controls Human-mediated Codex transport: ChatGPT does not start/control Codex directly.
- D072/D073 require the exact coordinator title instruction and truthful `CHAT_TITLE_ACTION_REQUIRED` fallback.
- D065 delegation obligations remain applicable before substantial Stage 6 work and again before final Code Review & Verify.

Current state is `AUTHORIZED_AWAITING_HUMAN_CODEX_START`: authority exists, but no Stage 6 execution evidence, deterministic Stage 6 gate, native-Windows preflight, synthetic canary, B2/F2/G3 observation, topology selection or provider-backed v15 evaluation call is yet claimed.

## Other frontier constraints

- T024 remains unauthorized until T023 has an accepted topology selection from Stage 7 convergence over valid Stage 6 evidence.
- T058 remains frozen by explicit Human decision; do not resume, integrate, clean or copy it without new explicit Human authorization.
- D066 intentional gaps remain unchanged.
- Historical scientific branches remain immutable.

## Next Chat Minimum Load

At the start of the next chat, after reading current `develop`, `AGENTS.md` and this checkpoint:

1. load `docs/tasks/T062-t023-riq-nbc-v15-reference-independent-evaluation.md`;
2. load `docs/reviews/T023-R30.md`;
3. load `docs/reviews/T023-R31.md`;
4. for Codex launch/continuation/transport, load D071/D072/D073;
5. load D074 / T023-R28 only if a semantic-selection conflict must be resolved;
6. load T023-R26 only if clean-source provenance or lineage is disputed;
7. do not reconstruct the frontier from prior chats or Project Memory.

Do not load older T023 history unless a concrete conflict requires it.

## Next Action

Human performs the D071 transport step:

1. start/select NEW Codex Local coordinator `AG | agent-governance | T062 | root-1`;
2. use native Windows, GPT-5.6 Sol, Medium and exact Codex CLI `0.149.0`;
3. paste the complete R31 transport prompt rendered by ChatGPT;
4. let Codex execute Stage 6 under R31/T062;
5. return only the terminal Executor shape:

```text
STATUS: <COMPLETED|BLOCKED>
HANDOFF: handoffs/T062-executor-handoff.json
BRANCH: test/t023-skill-activation-topology-evals-v15
HEAD: <remote pushed HEAD sha>
```

After terminal return, ChatGPT verifies remote Git and performs D068 Stage 7 convergence. No additional `go` is required for this already-authorized Stage 6 launch.
