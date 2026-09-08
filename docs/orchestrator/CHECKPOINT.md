# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O250  
Canonical-Branch: `develop`  
Current-Work-Unit: T061 / D068 Stage 6 — `AUTHORIZED_AWAITING_HUMAN_CODEX_START`  
Chat-Closure: KEEP_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: Codex Local / native Windows / isolated official `@openai/codex@0.149.0` realization  
Executor-Launch-State: AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Last-Coordinator-ID: `AG | agent-governance | T061 | root-4`

## Durable frontier

- D069 remains controlling for final Human-facing closure with the exact section title `Próxima Tarea`.
- D070 remains controlling for visible substantive work narration and compact completion reporting.
- D071 controls Human-mediated ChatGPT -> Codex transport. ChatGPT SHALL NOT attempt to start/control Codex directly and SHALL render the complete launch prompt.
- D072 controls exact Codex coordinator-title instruction and truthful `CHAT_TITLE_ACTION_REQUIRED` fallback.
- D073 controls current-adapter prompt-driven Codex coordinator titles; its generic rollout remains queued separately.
- Candidate Freeze C remains `1fc38f979d67ff29649f69ae39b8d46d2523518b`.
- Holdout/oracle Freeze D remains `f8cee7c72688f0486211474d2678d018772e2a58`.
- Historical Stage 6 terminal evidence remains immutable at `test/t023-skill-activation-topology-evals-v14@75f52f64adddfc738ab1d5362efdfe90cf327786`.
- T061 v14-r1 ready implementation head remains `6f98f2d64babbbbae32ff7f8b6460a9123c993b9`.
- T061 v14-r1 terminal Stage 5 evidence head/current task-branch head at launch authorization remains `aea43441a424fe18003176cb05b5594b8b561a68`.
- R24 accepted Stage 5 readiness with candidate/holdout integrity, Ruff lint/format, code-health, deterministic subsets, scheduler and full locked pytest all green; full pytest = `477 passed`; T061 harness provider/model calls through Stage 5 = exactly `0`.
- Stage 5 reconfirmed exact Codex CLI `0.149.0` is realizable on native Windows through isolated official `@openai/codex@0.149.0` invocation without replacing the default desktop-bundled `0.153.4` installation.
- The Human explicitly selected renewed T061 Stage 6 after O249 by replying `go`.
- R25 is the new current Stage 6 launch gate. R19 remains consumed/historical and MUST NOT be reused.
- R25 selects `NEW` coordinator `AG | agent-governance | T061 | root-4` because `root-3` was bounded Stage 5 verification/formatter work and did not operate as the exact provider-backed Stage 6 cell.
- Stage 6 launch profile is exactly: Codex / native Windows / GPT-5.6 Sol / Medium / Codex CLI `0.149.0`.
- No renewed Stage 6 Executor evidence, synthetic canary, B2, F2, G3 or provider-backed T061 call is claimed yet.

## Current Stage 6 authority

Current launch authority:

`docs/reviews/T023-R25.md`

Represented execution branch:

`test/t023-skill-activation-topology-evals-v14-r1`

Expected branch HEAD before substantive Stage 6 execution:

`aea43441a424fe18003176cb05b5594b8b561a68`

Ready implementation head:

`6f98f2d64babbbbae32ff7f8b6460a9123c993b9`

Required launch profile:

```text
Executor: Codex
Surface: Codex Local / native Windows / isolated official @openai/codex@0.149.0 realization
Session: NEW
Coordinator-ID: AG | agent-governance | T061 | root-4
Model: GPT-5.6 Sol
Effort: Medium
Codex CLI: exactly 0.149.0
```

Default desktop-bundled `0.153.4` is not equivalent and MUST NOT be silently substituted.

## Mandatory Stage 6 order

R25 requires fail-closed execution in this order:

1. safe Git synchronization and represented branch/head/Freeze ancestry verification;
2. exact native-Windows GPT-5.6 Sol / Medium / Codex CLI `0.149.0` realization verification;
3. candidate-integrity and holdout-integrity guards;
4. Ruff lint/format, code-health, deterministic subsets, scheduler and full locked pytest;
5. prove T061 harness provider/model calls so far = `0`;
6. frozen backend/workspace preflight;
7. unchanged synthetic Skill canary requiring `2/2 PASS`;
8. B2 Stage R only after canary PASS;
9. F2/G3 only if B2 qualifies under frozen scheduler/materiality rules;
10. Executor-owned Code Review & Verify and terminal remote handoff.

A material requirement/specification/Design/Plan/oracle defect requires stop and Orchestrator re-entry. Frozen scientific semantics must not be tuned by the Executor.

## Terminal return contract

Codex SHALL persist and push:

`handoffs/T061-executor-handoff-v14-r1.json`

Then return only:

```text
STATUS: <COMPLETED|BLOCKED>
HANDOFF: handoffs/T061-executor-handoff-v14-r1.json
BRANCH: test/t023-skill-activation-topology-evals-v14-r1
HEAD: <remote pushed HEAD sha>
```

ChatGPT resumes only after the Human returns that terminal shape and remote Git evidence is verified.

## Active remote artifacts

- Governing Task Contract: `docs/tasks/T061-mg1-v13-positive-anchor-reference-evaluation.md` — historical filename retained.
- v14 Stage 5 re-entry authority: `docs/reviews/T023-R17.md`.
- superseded practical readiness: `docs/reviews/T023-R18.md`.
- consumed historical Stage 6 launch authority: `docs/reviews/T023-R19.md`.
- Human-mediated transport correction: `docs/reviews/T023-R20.md`.
- coordinator-title correction: `docs/reviews/T023-R21.md`.
- Stage 6 blocker convergence: `docs/reviews/T023-R22.md`.
- Stage 5 local-validation convergence: `docs/reviews/T023-R23.md`.
- Stage 5 readiness: `docs/reviews/T023-R24.md`.
- current Stage 6 launch gate: `docs/reviews/T023-R25.md`.
- task branch: `test/t023-skill-activation-topology-evals-v14-r1`.
- ready implementation head: `6f98f2d64babbbbae32ff7f8b6460a9123c993b9`.
- terminal Stage 5 evidence head: `aea43441a424fe18003176cb05b5594b8b561a68`.
- terminal Stage 5 evidence: `handoffs/T061-stage5-local-validation-r1.json`.
- Candidate Freeze C: `1fc38f979d67ff29649f69ae39b8d46d2523518b`.
- Holdout/oracle Freeze D: `f8cee7c72688f0486211474d2678d018772e2a58`.
- Human-mediated Codex transport invariant: `docs/decisions/D071-human-mediated-codex-transport-boundary.md`.
- Codex coordinator-title invariant: `docs/decisions/D072-codex-coordinator-title-instruction.md`.
- prompt-driven title adoption: `docs/decisions/D073-codex-prompt-driven-coordinator-title-adoption.md`.

## Next Chat Minimum Load

For every new source-maintenance chat:

1. Read current `develop` and record HEAD.
2. Read current `AGENTS.md` from that `develop`.
3. Read this checkpoint from that `develop`.
4. Report `BOOTSTRAP_VALID` before substantive work.
5. Apply D070/D069 to visible narration/final closure.
6. For Codex launch/continuation/transport interactions, load D071/D072/D073.
7. For T061 Stage 6, load R25 and R24; load older R17-R23 only if a concrete conflict requires them.
8. Do not reconstruct the frontier from prior chats or Project Memory.

## D073 rollout queue

D073 generic rollout remains a separate Markdown-only follow-up. Do not mix it into T061 unless the Human explicitly selects that objective.

## Next action

Human performs the D071 transport step:

1. start/select NEW Codex Local coordinator `AG | agent-governance | T061 | root-4`;
2. use native Windows, GPT-5.6 Sol, Medium and exact isolated Codex CLI `0.149.0` realization;
3. paste the complete R25 transport prompt rendered by ChatGPT;
4. let Codex execute Stage 6 under R25;
5. return only `STATUS / HANDOFF / BRANCH / HEAD` to ChatGPT.

After terminal return, ChatGPT verifies remote Git and performs D068 Stage 7 convergence.

## Completion condition

This launch-preparation objective is complete when R25 and O250 are durably integrated on `develop` and the Human has the complete launch card + copy/paste-ready prompt.

T061 itself remains incomplete until Stage 6 terminal evidence is remotely verified and Stage 7 converges.

## Do not

Do not reuse R19. Do not reuse `root-3` for the provider-backed Stage 6 cell. Do not rewrite `75f52f64...`, `6ef147812...`, `aea43441...`, Freeze C or Freeze D. Do not silently substitute Codex CLI `0.153.4` for `0.149.0`. Do not run B2 before deterministic gates/backend/canary authorize it. Do not schedule F2/G3 unless B2 qualifies. Do not start T024. Do not modify or silently close D066 gaps. Do not reopen T058. Do not perform historical branch cleanup.
