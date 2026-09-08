# Orchestrator Checkpoint

Checkpoint-ID: O255  
Date: 2026-09-08  
Current-Objective: T023 / T062 — v15 RIQ-NBC reference-independent evaluation  
State: STAGE5_COMPLETE_READY_FOR_STAGE6_HUMAN_LAUNCH  
Active-Executor: NONE  
Stage6-Authorization: NOT_AUTHORIZED_PENDING_SEPARATE_HUMAN_LAUNCH

## Canonical frontier

D068 Stage 5 is complete for T062. The accepted scientific materialization is:

`test/t023-skill-activation-topology-evals-v15@3e0d0b71cf382db502e186622f40a23bcd915390`

Durable Stage 5 review:

`docs/reviews/T023-R30.md`

Task Contract:

`docs/tasks/T062-t023-riq-nbc-v15-reference-independent-evaluation.md`

T062 now has `Stage-Readiness: READY_FOR_STAGE6` and `Executor-Authorization: NOT_AUTHORIZED_PENDING_SEPARATE_HUMAN_LAUNCH`.

`READY_FOR_STAGE6` is a readiness state only. It does not authorize an Executor, a provider/model call, preflight, canary or acceptance execution.

## Stage 5 canonical receipts

Protected `develop` used for v15 scientific branch creation:

`ddb41724c76d92f55e0d7ff78cc2bf0272b1a2bc`

Clean authorized historical byte source:

`aea43441a424fe18003176cb05b5594b8b561a68`

Forbidden provider-backed ancestor/import source:

`67884f52912aeb51821d8f7e8ae7753c40b608fc`

Candidate Freeze E:

`5b025087bc7b6996f683a34fdd1ce441d3d6dd82`

Holdout/oracle Freeze F:

`5b8ac55980ecdbb6a2bf3784812b933647f2f13d`

Terminal Stage 5 scientific SHA:

`3e0d0b71cf382db502e186622f40a23bcd915390`

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
full pytest: 460 passed
provider/model calls: 0
result: SUCCESS
```

Holdout geometry/novelty receipt:

```text
cases: 70
FAR denominator: 40
near-miss axes: 5 x 6
exact prompt overlap v12: 0
exact prompt overlap v13: 0
exact prompt overlap v14: 0
```

No Executor was launched in Stage 5.

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

B0/B1 remain historical and unscheduled.

No v12/v13/v14 observation may enter v15 scoring.

## Frozen Stage 6 execution semantics

If and only if a future Human explicitly authorizes Stage 6, execution remains:

```text
host: Codex
runtime: native Windows
model: GPT-5.6 Sol
reasoning: Medium
Codex CLI baseline: 0.149.0
workers: 1 for full acceptance
per-attempt timeout: 180 seconds
```

Provider-free gate order before any live model call:

1. candidate-integrity guard;
2. holdout-integrity guard;
3. `ruff check`;
4. `ruff format --check`;
5. full `pytest`;
6. code-health and symbol-map checks;
7. frozen-input/scheduler characterization.

Only after every deterministic gate passes:

8. native-Windows backend/workspace/version preflight;
9. synthetic canary 2/2;
10. full independent B2/F2/G3 acceptance schedule.

Acceptance scheduler:

```text
per ordered case: B2 -> F2 -> G3
base repetitions: all r1, then all r2
r3: unstable candidate/case pairs only
r4: forbidden
```

B2 scientific non-qualification is non-blocking. B2 must still receive its complete required measurement. Exact scientific futility may stop F2 or G3 only candidate-locally. Technical/epoch/integrity invalidity remains a global fail-closed STOP.

Budgets:

```text
per candidate base valid observations: 140
per candidate maximum valid observations: 210
global base valid observations: 420
global maximum valid observations: 630
max model attempts / scheduled observation: 2
acceptance model-attempt ceiling: 1260
synthetic canary maximum attempts: 4
absolute Stage 6 provider/model attempt ceiling: 1264
```

Selection semantics remain exactly T062/D074:

- every candidate must pass the same absolute gates;
- Regime A: if B2 qualifies, split eligibility additionally requires F1 `>= B2 + 0.03`, median context `<= 0.85 * B2`, FAR no worse, wrong-specialist no more than `B2 + 0.01`, overactivation no more than `B2 + 0.01`;
- Regime B: if B2 is validly measured but scientifically non-qualifying, B2 is ineligible/non-blocking and F2/G3 use absolute gates plus admissibility dominance; the relative F1 `+0.03` uplift does not apply;
- invalid B2 technical measurement invalidates the epoch rather than becoming Regime B;
- deterministic split tie-break: higher F1, lower FAR, lower median context, fewer entrypoints, exact tie -> F2.

## Ownership and launch boundary

- Orchestrator owns completed Stage 5 materialization and D052 semantic conformance.
- Executor owns Stage 6 execution/diagnosis/repair/verification only after separate Human launch.
- Orchestrator owns Stage 7 convergence/integration after terminal Executor evidence.
- Future Executor evidence/handoff path remains `handoffs/T062-executor-handoff.json`.
- No Stage 6 handoff is authorized or required while this checkpoint is waiting for Human launch.
- Before any future Executor prompt, D055 requires a concrete Executor identity, NEW/CONTINUE state, model, effort and rationale.

## Scientific branch invariants

The following are immutable accepted Stage 5 boundaries:

- Freeze E `5b025087...`;
- Freeze F `5b8ac559...`;
- terminal Stage 5 scientific SHA `3e0d0b71...`.

Do not rewrite/reset/rebase/force-push these scientific boundaries.

Temporary validation branches used to obtain provider-free hosted execution are technical evidence surfaces only and MUST NOT be merged into the scientific branch or `develop`.

## Other frontier constraints

- T024 remains unauthorized until T023 has an accepted topology selection from Stage 6.
- T058 remains frozen by explicit Human decision; do not resume, integrate, clean or copy it without new explicit Human authorization.
- D066 intentional gaps remain unchanged.
- Historical scientific branches remain immutable.
- Do not infer a Stage 6 launch from `go`, readiness state, prior launch history or Stage 5 completion. Stage 6 requires an explicit Human launch objective after this checkpoint is canonical on `develop`.

## Next Chat Minimum Load

At the start of the next chat, after reading current `develop`, `AGENTS.md` and this checkpoint:

1. load `docs/tasks/T062-t023-riq-nbc-v15-reference-independent-evaluation.md`;
2. load `docs/reviews/T023-R30.md`;
3. load D074 / T023-R28 only if a semantic-selection conflict must be resolved;
4. load T023-R26 only if clean-source provenance or lineage is disputed;
5. do not reconstruct the frontier from prior chats or Project Memory.

Do not load older T023 history unless one of those concrete conflicts requires it.

## Next Action

**STOP — await separate explicit Human Stage 6 launch authorization.**

No Executor launch, provider/model call, native-Windows preflight, synthetic canary, acceptance observation or topology selection is authorized by this checkpoint.

If the Human later explicitly launches Stage 6:

1. refresh current protected `develop` and re-read this checkpoint/T062/R30;
2. confirm scientific branch still equals `3e0d0b71cf382db502e186622f40a23bcd915390` and Freeze E/F are intact;
3. revalidate D061/D062 routing/protection state;
4. select and state the exact D055 Executor launch profile before emitting the handoff;
5. persist the Human launch frontier durably before live execution;
6. delegate Stage 6 only within the frozen T062 execution envelope.