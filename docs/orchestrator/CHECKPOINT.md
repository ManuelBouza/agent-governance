# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O245
Canonical-Branch: `develop`  
Current-Work-Unit: T061 / D068 Stage 6 MG1-v14 launch — `AUTHORIZED_AWAITING_HUMAN_CODEX_START`
Chat-Closure: KEEP_CURRENT_CHAT
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows  
Executor-Launch-State: AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Coordinator-ID: `AG | agent-governance | T061 | root-2`

## Durable frontier

- D070 remains controlling for visible substantive work narration and compact completion reporting.
- D069 remains controlling for final Human-facing closure with the exact section title `Próxima Tarea`.
- D071 controls ChatGPT -> Codex transport: ChatGPT SHALL NOT start, continue, invoke, control, or search for a direct Codex execution transport. ChatGPT renders the launch card and complete copy/paste-ready prompt; the Human performs the Codex UI/session transition.
- D072 now controls Codex coordinator-title handling. Every Codex launch/continuation prompt MUST contain the exact `Coordinator-ID` and explicitly instruct Codex to use that exact value as the visible chat title.
- If the current Codex surface cannot set/rename the chat title from within the session, Codex MUST NOT claim success. It must emit exactly `CHAT_TITLE_ACTION_REQUIRED: <Coordinator-ID>` so the Human can apply the title in the UI, then continue under the same coordinator identity.
- A launch prompt that carries the coordinator name only in the Human-facing launch card is incomplete under D072.
- Visible chat title remains navigation metadata only; Git/persisted contracts/branch/handoff evidence remain authority. Inability to rename is not a Stage 6 technical blocker unless a future controlling experiment explicitly makes title material.
- The Human Owner explicitly selected renewed T061 Stage 6 on 2026-09-07T17:57:59Z.
- `docs/reviews/T023-R19.md` remains the controlling T061 MG1-v14 Stage 6 execution authority.
- `docs/reviews/T023-R20.md` remains the controlling Human-mediated transport correction.
- `docs/reviews/T023-R21.md` is the controlling coordinator-title correction for the current T061 prompt.
- Represented Stage 6 branch: `test/t023-skill-activation-topology-evals-v14`.
- Reviewed Stage 5 HEAD: `a8caf6338dbae3a3ce4cefdc7965acd0d37f1557`.
- Candidate Freeze C: `1fc38f979d67ff29649f69ae39b8d46d2523518b`.
- Holdout/oracle Freeze D: `f8cee7c72688f0486211474d2678d018772e2a58`.
- Candidate identity remains `MG1-T061-CANDIDATE-HASHES-v2`; presentation revision `MG1-T023-PRESENTATIONS-v5`; topology revision `MG1-T023-TOPOLOGIES-v4`; corpus `MG1-T023-CORPUS-v8`; oracle `MG1-T023-TOPOLOGY-ORACLE-v14`; execution epoch `MG1-T023-EXECUTION-v14`; trial envelope `MG1-T023-TRIAL-ENVELOPE-v2`.
- Frozen live cell remains Codex / native Windows / GPT-5.6 Sol / Medium / exact Codex CLI `0.149.0`.
- Coordinator remains explicit D060 failover `NEW` / `AG | agent-governance | T061 | root-2`.
- Mandatory Stage 6 order remains deterministic/provider-free gates -> prove provider/model calls = 0 -> frozen native-Windows backend/workspace preflight -> unchanged synthetic canary 2/2 PASS -> B2 Stage R -> F2/G3 only if B2 qualifies -> Code Review & Verify -> Executor-owned handoff -> terminal pushed response.
- T061 remains `ASSURED`; D065 delegation evaluation is required before substantial Stage 6 work and again before final Code Review & Verify.
- No semantic candidate/corpus/oracle/capability-source/topology/presentation/trial-envelope/threshold/scheduling/materiality change is Executor-authorized.
- No real v14 Executor execution has yet been reported or verified. No deterministic gate, host preflight, synthetic canary, B2/F2/G3 observation, or provider/model call is claimed.
- Expected v14 handoff remains `handoffs/T061-executor-handoff.json`; no v14 handoff is currently accepted.
- Historical v13 evidence remains immutable; T058 remains frozen; D066 gaps remain unchanged; no release topology is selected; T024 remains blocked.

## Active remote artifacts

- Governing Task Contract: `docs/tasks/T061-mg1-v13-positive-anchor-reference-evaluation.md` — historical filename retained; v14 is prospectively controlled by R17/R18/R19/R20/R21.
- v14 Stage 5 re-entry authority: `docs/reviews/T023-R17.md`.
- v14 Stage 5 completion/readiness: `docs/reviews/T023-R18.md`.
- v14 Stage 6 execution authority: `docs/reviews/T023-R19.md`.
- Human-mediated transport correction: `docs/reviews/T023-R20.md`.
- Coordinator-title correction: `docs/reviews/T023-R21.md`.
- Global Codex transport invariant: `docs/decisions/D071-human-mediated-codex-transport-boundary.md`.
- Global Codex coordinator-title invariant: `docs/decisions/D072-codex-coordinator-title-instruction.md`.
- Stage 6 branch: `test/t023-skill-activation-topology-evals-v14`.
- Reviewed Stage 5 HEAD: `a8caf6338dbae3a3ce4cefdc7965acd0d37f1557`.
- Candidate Freeze C: `1fc38f979d67ff29649f69ae39b8d46d2523518b`.
- Holdout/oracle Freeze D: `f8cee7c72688f0486211474d2678d018772e2a58`.
- Coordinator: `AG | agent-governance | T061 | root-2`.

## Next Chat Minimum Load

For every new source-maintenance chat:

1. Read current `develop` and record HEAD.
2. Read current `AGENTS.md` from that `develop`.
3. Read this checkpoint from that `develop`.
4. Report `BOOTSTRAP_VALID` before substantive work.
5. Apply D070/D069 to visible narration/final closure.
6. For any Codex launch/continuation/transport interaction, load D071 and D072 before responding.
7. For current T061 Stage 6, also load R19, R20 and R21.
8. Do not reconstruct the frontier from prior chats or Project Memory.

## Codex launch invariant

For every current or future Codex launch while D071/D072 control:

1. ChatGPT verifies/persists the applicable launch authority.
2. ChatGPT emits the exact Human-facing launch card.
3. ChatGPT emits the complete copy/paste-ready Codex prompt in the same response.
4. The prompt itself states the exact `Coordinator-ID`.
5. The prompt explicitly instructs Codex to set/preserve the visible chat title to that exact `Coordinator-ID`.
6. If Codex cannot rename from within the current host, it must truthfully emit `CHAT_TITLE_ACTION_REQUIRED: <Coordinator-ID>`; the Human applies the title through the UI when supported.
7. ChatGPT does not search plugins/connectors/tools for a direct Codex invocation path and does not claim it can start/continue Codex itself.
8. The Human opens/selects the required `NEW` or `CONTINUE` Codex session, configures the stated settings, and pastes the prompt.
9. Codex executes and publishes required remote Git evidence.
10. The Human returns `STATUS/HANDOFF/BRANCH/HEAD` to ChatGPT.
11. ChatGPT verifies the reported remote HEAD and handoff before Stage 7 conclusions.

## Next action

Deliver the corrected R21 Human-mediated T061 launch handoff to the Human Owner:

- `Executor: Codex`
- `Surface: ChatGPT desktop / Codex / native Windows`
- `Session: NEW`
- `Coordinator-ID: AG | agent-governance | T061 | root-2`
- `Model: GPT-5.6 Sol`
- `Effort: Medium`
- `Codex CLI: exactly 0.149.0`
- render the complete R21 transport prompt directly in the Human-facing response;
- that prompt must contain the exact title instruction for `AG | agent-governance | T061 | root-2`.

After the Human runs Codex and returns terminal `STATUS/HANDOFF/BRANCH/HEAD`, verify the evidence from GitHub and perform D068 Stage 7 convergence.

## Completion condition

This coordinator-title correction objective is complete when D072, R21 and O245 are durably integrated on `develop`. T061 itself remains incomplete and authorized for Stage 6, awaiting the Human-mediated Codex start and later terminal evidence.

## Do not

Do not omit the exact coordinator-title instruction from a Codex prompt. Do not claim title rename succeeded if the host cannot do it. Do not invent a new root merely because the title requires Human UI action. Do not attempt direct ChatGPT-to-Codex invocation. Do not search for a Codex execution plugin/transport. Do not tell the Human merely to open a persisted prompt path without rendering the complete prompt. Do not claim Stage 6 execution before real Codex evidence exists. Do not mutate Freeze C/Freeze D or historical v13 evidence. Do not change the frozen model/effort/CLI/host cell silently. Do not start T024. Do not modify or silently close D066 gaps. Do not reopen T058. Do not perform historical branch cleanup.
