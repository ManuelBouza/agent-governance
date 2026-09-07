# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O240
Canonical-Branch: `develop`  
Current-Work-Unit: T061 / D068 Stage 6 launch and execution — `AUTHORIZED_AWAITING_EXECUTOR_START`
Chat-Closure: KEEP_CURRENT_CHAT
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows  
T061-Human-Hold: LIFTED_BY_HUMAN_2026-09-07  
Executor-Launch-State: AUTHORIZED_AWAITING_HOST_START  
Coordinator-ID: `AG | agent-governance | T061 | root-1`

## Durable frontier

- D070 remains controlling for two-layer Human-facing reporting: substantive visible work narration during non-trivial execution and compact outcome-oriented final responses.
- D069 remains controlling for final response closure with the exact section title `Próxima Tarea`; that footer remains navigation metadata and never creates authority.
- The Human Owner explicitly lifted the T061 Human Hold and selected continuation of T061 on 2026-09-07.
- `docs/reviews/T023-R15.md` is the persisted Stage 6 launch gate. It satisfies T061's requirement for a separate Human-selected Executor launch objective.
- T061 remains technically `READY_FOR_STAGE6`; Stage 5 assets are unchanged. The represented Stage 6 branch remains `test/t023-skill-activation-topology-evals-v13` at verified Stage 5 HEAD `f893a03d17596182db209322f5357cda75ea3781` at launch preparation.
- Candidate Freeze A remains `a454091aff7bb932372a6057e2d9804f94e66320`; Freeze B remains `7b990f4d60ba7ca0dfafe1b95785e007f8697c28`; candidate hash manifest blob remains `6d3a8025a1923dd5738f65e8aa07488cbd58e245`.
- Remote comparison Freeze B -> represented Stage 5 HEAD contains only Stage 5 control Markdown and no candidate/corpus/oracle/harness mutation.
- Current `develop` at launch preparation is `9f01b3e2d925b50185ac1dc815d54fb4c7a8d1d3`. The v13 branch is intentionally behind the later Stage 5-frontier and D070/O239 Markdown commits; this known divergence is not permission to rebase, reset, merge or rewrite the frozen candidate. Stage 6 must refresh remote refs and verify the exact represented branch/Freeze B relationship before execution.
- The T061 live cell remains frozen at Codex / native Windows / GPT-5.6 Sol / Medium with Codex CLI exactly `0.149.0`. Current official OpenAI Help was rechecked on 2026-09-07 and still documents GPT-5.6 Sol in Codex, Medium reasoning for Sol, and a GPT-5.6 Codex CLI minimum of `0.144.0`; the pinned `0.149.0` remains within the documented compatibility floor. This does not authorize a model/CLI upgrade.
- Human-facing launch profile: `NEW`, Coordinator-ID `AG | agent-governance | T061 | root-1`, GPT-5.6 Sol, Medium, native Windows, exact CLI `0.149.0`.
- D065 applies because T061 is ASSURED. The Executor must evaluate bounded delegation before substantial work and before final Code Review & Verify, while preserving the frozen experiment topology, one-writer/worktree safety and semantic read-only assets.
- Stage 6 order remains deterministic gates -> prove provider/model calls during deterministic gates = `0` -> frozen native-Windows preflight -> unchanged synthetic canary `2/2 PASS` -> B2 Stage R -> F2/G3 only if B2 qualifies -> technical Code Review & Verify -> Executor-owned `handoffs/T061-executor-handoff.json` -> terminal push/response.
- The current ChatGPT Orchestrator runtime does not expose a general Codex execution transport. Plugin discovery found no general Codex Executor integration that can replace the required native-Windows coordinator. Therefore Stage 6 is authorized but no Executor session/provider call/deterministic gate/preflight/canary/acceptance observation has run yet.
- The Executor handoff does not yet exist and MUST be created by the Executor, not the Orchestrator.
- No release topology is selected. T024 remains blocked. D066 gaps remain unchanged. T058 remains frozen.

## Active remote artifacts

- Task Contract: `docs/tasks/T061-mg1-v13-positive-anchor-reference-evaluation.md`
- Stage 5 review: `docs/reviews/T023-R14.md`
- Stage 6 launch gate: `docs/reviews/T023-R15.md`
- Topic branch: `test/t023-skill-activation-topology-evals-v13`
- Represented Stage 5 HEAD at launch preparation: `f893a03d17596182db209322f5357cda75ea3781`
- Candidate Freeze A: `a454091aff7bb932372a6057e2d9804f94e66320`
- Holdout/oracle Freeze B: `7b990f4d60ba7ca0dfafe1b95785e007f8697c28`
- Expected Executor handoff: `handoffs/T061-executor-handoff.json` — not yet created
- Coordinator: `AG | agent-governance | T061 | root-1`

## Successor interaction requirement

For every new source-maintenance objective or resumed T061 interaction:

1. **Bootstrap** — read current `develop`, `AGENTS.md`, this checkpoint and only the directly controlling artifacts needed for the immediate frontier.
2. **Explicit validation** — report whether Bootstrap is valid before substantive execution/review.
3. **Visible work narration** — follow D070 at meaningful work boundaries.
4. **Compact completion** — summarize outcome/artifacts/material boundaries rather than replaying the execution narrative.
5. End qualifying final responses with exact section title **`Próxima Tarea`** under D069.

For T061 specifically:

6. Treat the prior Human Hold as lifted. Do not recreate or infer a hold unless the Human Owner explicitly establishes one again.
7. Before Executor work, verify current remote `develop`, the v13 topic branch, Freeze B ancestry and candidate/reference immutability.
8. Preserve `docs/reviews/T023-R15.md` as the current Stage 6 launch authority unless a later persisted Orchestrator gate supersedes it.
9. If the Executor returns, verify the reported remote HEAD and read `handoffs/T061-executor-handoff.json` there before any Stage 7 acceptance claim.
10. Do not accept chat-only/local-only Executor evidence.

Do not reconstruct the frontier from prior chats or Project Memory.

## Next action

T061 Stage 6 is selected and authorized but awaits the concrete Codex host start.

1. The Human Owner starts a **NEW** Codex coordinator on the supported native-Windows surface with Coordinator-ID `AG | agent-governance | T061 | root-1`, model GPT-5.6 Sol, effort Medium, and exact Codex CLI baseline `0.149.0`.
2. Use the transport prompt persisted in `docs/reviews/T023-R15.md` so the Executor refreshes GitHub, loads current canonical launch authority, and operates on `test/t023-skill-activation-topology-evals-v13` without rewriting the frozen candidate history.
3. The Executor executes deterministic gates first and proves provider/model calls during them equal `0`.
4. Only after deterministic PASS may it resolve the frozen host profile, run the unchanged canary, and then issue B2 acceptance observations.
5. F2/G3 remain unscheduled unless B2 qualifies in the same epoch.
6. On terminal Stage 6 state, the Executor persists/pushes `handoffs/T061-executor-handoff.json` and returns only STATUS/HANDOFF/BRANCH/HEAD.
7. ChatGPT Orchestrator then performs Stage 7 Converge/Accept review from the remote Git state.

## Completion condition

Current launch-preparation objective is complete when R15 and O240 are durably integrated on `develop`. T061 Stage 6 itself is complete only after a valid Executor terminal handoff is remotely published and independently reviewable.

## Do not

Do not claim Stage 6 gates, provider/model calls, host preflight, canary or acceptance results before Executor evidence exists. Do not create the Executor handoff from the Orchestrator. Do not rebase/reset/rewrite the v13 branch merely to match later `develop` orchestration Markdown. Do not change B2/F2/G3/reference bytes, corpus v7, oracle v13, trial-envelope semantics, thresholds, denominator, scheduling or materiality rules. Do not silently change Codex CLI `0.149.0` or the GPT-5.6 Sol/Medium live cell. Do not execute F2/G3 without a qualifying same-epoch B2 reference. Do not start T024. Do not modify or silently close D066 gaps. Do not reopen T058. Do not perform historical branch cleanup. Do not select a release topology before valid prospective evidence and Stage 7 acceptance.
