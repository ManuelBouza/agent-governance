# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O238
Canonical-Branch: `develop`  
Current-Work-Unit: T061 / D068 Stage 5 MG1-v13 candidate publication — OBJECTIVE_COMPLETE
Chat-Closure: WAITING_FOR_NEXT_OBJECTIVE
Active-Executor: none  
Active-Executor-Surface: none

## Durable frontier

- D069 remains controlling for Human-facing response closure: project status/work responses end with `Próxima Tarea`, derived from canonical Git state, and that footer never creates task authority.
- The Human Owner explicitly selected and completed D068 Stage 5 for `T061`.
- The published Stage 5 / future Stage 6 branch is `test/t023-skill-activation-topology-evals-v13`, based on `develop@af2f68590ace167947815bb93f12cce4ac2fa5f2`.
- Candidate Freeze A is `a454091aff7bb932372a6057e2d9804f94e66320`. It froze capability-source v4, topology/presentation v4, B2 exact bytes, byte-identical F2/G3/shared copies and the candidate hash manifest before any exact v13 holdout prompt existed.
- Freeze B is `7b990f4d60ba7ca0dfafe1b95785e007f8697c28`. It freezes the fresh 70-case corpus v7, oracle v13 and candidate-immutable v13 harness/integrity support.
- Remote comparison Freeze A -> Freeze B contains no changed `presentations-v4/**` path and no change to `candidate-hashes-v13.json`, `topologies.json`, `presentations/manifest.json` or `docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md`.
- `candidate-hashes-v13.json` has the same Git blob `6d3a8025a1923dd5738f65e8aa07488cbd58e245` at Freeze A and Freeze B. Candidate/reference bytes remain frozen.
- Corpus v7 has exactly 70 fresh cases: 18 positives, 10 negatives, 30 near-misses, 4 ambiguous, 4 cross-profile and 4 multi-intent. The false-activation denominator is exactly 40; the 30 near-misses are six cases on each of five frozen axes; exact V12 prompt reuse is forbidden and guarded.
- Oracle v13 uses candidate set `[B2, F2, G3]`, reference stage `[B2]`, challengers `[F2, G3]`, the preserved multidimensional thresholds, paired 2+1 method, critical any-occurrence gates, exact futility and D050 materiality/tie-break semantics.
- B2 full reference base schedule is 140 observations. If B2 is non-qualifying/futile, the result is `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE` and F2/G3 remain unscheduled. If B2 qualifies, F2/G3 may execute only in the same v13 epoch.
- T061 is `READY_FOR_STAGE6`; `docs/reviews/T023-R14.md` records Stage 5 completion. This readiness does not authorize an Executor.
- Stage 5 issued zero provider/model calls and launched no Executor. Deterministic verification code was materialized but Stage 6 runtime gates have not yet been claimed as executed or passing.
- No release topology is selected. T024 remains blocked. D066 gaps remain unchanged. T058 remains frozen.

## Active remote artifacts

- Task Contract: `docs/tasks/T061-mg1-v13-positive-anchor-reference-evaluation.md`
- Stage 5 review: `docs/reviews/T023-R14.md`
- Topic branch: `test/t023-skill-activation-topology-evals-v13`
- Candidate Freeze A: `a454091aff7bb932372a6057e2d9804f94e66320`
- Holdout/oracle Freeze B: `7b990f4d60ba7ca0dfafe1b95785e007f8697c28`
- Future Executor handoff path: `handoffs/T061-executor-handoff.json` — not yet created because Stage 6 is not authorized.

## Successor interaction requirement

For every new source-maintenance objective:

1. **Bootstrap** — load and validate only the canonical state required to start safely; do not perform substantive objective work during this action.
2. **Task execution** — begin only after Bootstrap has been explicitly validated.

For every final Human-facing Agent Governance project response that reports work, status, convergence, closure or a persisted repository change:

3. End with a section titled exactly **`Próxima Tarea`**.
4. Give one short description of the next task/action derived from canonical Git/checkpoint state.
5. If the named task is only permitted and not selected, say so; the footer never creates authorization.

## Next Chat Minimum Load

When the Human Owner supplies the next objective:

1. Read current `develop` identity from GitHub.
2. Read current `AGENTS.md` from that same `develop`.
3. Read `docs/orchestrator/CHECKPOINT.md` and verify `Checkpoint-Sequence: O238`.
4. Load `docs/tasks/T061-mg1-v13-positive-anchor-reference-evaluation.md` and `docs/reviews/T023-R14.md`.
5. Verify the remote v13 topic branch and that Freeze B `7b990f4d60ba7ca0dfafe1b95785e007f8697c28` remains in its ancestry without candidate/reference drift.
6. If the Human selects Stage 6, additionally load only the direct D054/D055/D058, Executor-handoff and host/eval references required to construct the launch profile and handoff.
7. Verify the concrete Executor identity and current supported model/effort options before launch recommendations.
8. Explicitly report whether Bootstrap is valid before starting task execution.

Do not reconstruct the frontier from prior chats or Project Memory.

## Next action

No Stage 6 execution objective is selected yet.

1. Remain `WAITING_FOR_NEXT_OBJECTIVE`.
2. If the Human Owner selects continuation of D050/T023, the next permitted substantive objective is a separate **D068 Stage 6 T061 launch/execution objective**.
3. That objective must verify the published v13 branch, create the required Executor handoff/launch profile, and authorize the Executor to execute deterministic gates first.
4. The Executor must prove candidate/holdout integrity, full deterministic/profile/source-independence gates and provider/model calls during those deterministic gates = `0` before host preflight.
5. The frozen native Windows / Codex CLI `0.149.0` / GPT-5.6 Sol / Medium preflight and unchanged synthetic Skill canary must pass before any acceptance prompt.
6. Stage R executes B2 first. F2/G3 execute only after a qualifying same-epoch B2 reference.
7. Only a later Orchestrator Stage 7 acceptance of T023 may select a release topology or unblock T024.

## Completion condition

Satisfied: T061 Stage 5 is coherently published with remotely verified Freeze A and Freeze B, frozen candidate/reference bytes, fresh corpus v7/oracle v13, candidate-immutable harness/integrity support, T061 Stage-Readiness `READY_FOR_STAGE6`, and no Executor/provider/model execution during Stage 5.

## Do not

Do not treat `Próxima Tarea` or `READY_FOR_STAGE6` as Executor authorization. Do not rerun or reinterpret V12. Do not relax any threshold, denominator, critical gate, candidate wording, expected semantics, scheduling or materiality rule. Do not change B2/F2/G3/reference bytes while retaining corpus v7/oracle v13. Do not execute F2/G3 without a qualifying same-epoch B2 reference. Do not silently change the Codex `0.149.0` host cell. Do not start T024. Do not modify or silently close D066 gaps. Do not reopen T058. Do not perform historical branch cleanup. Do not select a release topology before valid prospective evidence.
