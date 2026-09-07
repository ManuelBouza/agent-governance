# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O244
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
- D071 is now controlling for every ChatGPT -> Codex launch transport in Agent Governance source-product work.
- D071 establishes a Human-mediated transport invariant: ChatGPT SHALL NOT start, continue, invoke, control, or search for a direct Codex execution transport. ChatGPT prepares/persists authority and always gives the Human the launch card plus the complete copy/paste-ready Codex prompt; the Human opens/configures Codex and pastes the prompt.
- A launch response that only points to a persisted prompt path is insufficient under D071. The complete prompt must be rendered in the same Human-facing response.
- Normal post-authorization/pre-execution Codex state is `AUTHORIZED_AWAITING_HUMAN_CODEX_START`, not a missing-plugin/tool blocker.
- A future direct ChatGPT-to-Codex capability does not silently supersede D071; a later explicit Human-accepted decision is required.
- The Human Owner explicitly selected renewed T061 Stage 6 on 2026-09-07T17:57:59Z.
- `docs/reviews/T023-R19.md` remains the controlling T061 MG1-v14 Stage 6 execution launch authority.
- `docs/reviews/T023-R20.md` is the controlling transport correction for that launch and applies D071 to the current T061 handoff.
- Canonical `develop` before this correction: `34a5b408514c1741b7f2c1dba3110cfe79632edc`.
- Represented Stage 6 branch: `test/t023-skill-activation-topology-evals-v14`.
- Reviewed Stage 5 HEAD: `a8caf6338dbae3a3ce4cefdc7965acd0d37f1557`.
- Candidate Freeze C: `1fc38f979d67ff29649f69ae39b8d46d2523518b`.
- Holdout/oracle Freeze D: `f8cee7c72688f0486211474d2678d018772e2a58`.
- Candidate identity: `MG1-T061-CANDIDATE-HASHES-v2`; presentation revision `MG1-T023-PRESENTATIONS-v5`; topology revision `MG1-T023-TOPOLOGIES-v4`.
- Fresh holdout identity: `MG1-T023-CORPUS-v8`; oracle `MG1-T023-TOPOLOGY-ORACLE-v14`; execution epoch `MG1-T023-EXECUTION-v14`; trial envelope `MG1-T023-TRIAL-ENVELOPE-v2`.
- Frozen live cell remains Codex / native Windows / GPT-5.6 Sol / Medium / exact Codex CLI `0.149.0`.
- Coordinator remains explicit D060 failover `NEW` / `AG | agent-governance | T061 | root-2`.
- Mandatory Stage 6 order remains: deterministic/provider-free gates -> prove provider/model calls = 0 -> frozen native-Windows backend/workspace preflight -> unchanged synthetic canary 2/2 PASS -> B2 Stage R -> F2/G3 only if B2 qualifies -> Code Review & Verify -> Executor-owned handoff -> terminal pushed response.
- T061 remains `ASSURED`; D065 delegation evaluation is required before substantial Stage 6 work and again before final Code Review & Verify.
- No semantic candidate/corpus/oracle/capability-source/topology/presentation/trial-envelope/threshold/scheduling/materiality change is Executor-authorized.
- No real v14 Executor execution has yet been reported or verified. No deterministic gate, host preflight, synthetic canary, B2/F2/G3 observation, or provider/model call is claimed.
- Expected v14 handoff remains `handoffs/T061-executor-handoff.json`; no v14 handoff is currently accepted.
- Historical v13 evidence remains immutable; T058 remains frozen; D066 gaps remain unchanged; no release topology is selected; T024 remains blocked.

## Active remote artifacts

- Governing Task Contract: `docs/tasks/T061-mg1-v13-positive-anchor-reference-evaluation.md` — historical filename retained; v14 is prospectively controlled by R17/R18/R19/R20.
- v14 Stage 5 re-entry authority: `docs/reviews/T023-R17.md`.
- v14 Stage 5 completion/readiness: `docs/reviews/T023-R18.md`.
- v14 Stage 6 execution launch gate: `docs/reviews/T023-R19.md`.
- v14 Human-mediated transport correction: `docs/reviews/T023-R20.md`.
- Global Codex transport invariant: `docs/decisions/D071-human-mediated-codex-transport-boundary.md`.
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
6. For any Codex launch/continuation/transport interaction, load `docs/decisions/D071-human-mediated-codex-transport-boundary.md` before responding.
7. For current T061 Stage 6, also load R19 and R20.
8. Do not reconstruct the frontier from prior chats or Project Memory.

## Codex launch invariant

For every current or future Codex launch while D071 controls:

1. ChatGPT verifies/persists the applicable launch authority.
2. ChatGPT emits the exact Human-facing launch card.
3. ChatGPT emits the complete copy/paste-ready Codex prompt in the same response.
4. ChatGPT does **not** search plugins/connectors/tools for a direct Codex invocation path and does **not** claim it can start or continue Codex itself.
5. The Human opens/selects the required `NEW` or `CONTINUE` Codex session, configures the stated settings, and pastes the prompt.
6. Codex executes and publishes required remote Git evidence.
7. The Human returns `STATUS/HANDOFF/BRANCH/HEAD` to ChatGPT.
8. ChatGPT verifies the reported remote HEAD and handoff before Stage 7 conclusions.

## Next action

Deliver the current R20 Human-mediated T061 launch handoff to the Human Owner:

- `Executor: Codex`
- `Surface: ChatGPT desktop / Codex / native Windows`
- `Session: NEW`
- `Coordinator-ID: AG | agent-governance | T061 | root-2`
- `Model: GPT-5.6 Sol`
- `Effort: Medium`
- `Codex CLI: exactly 0.149.0`
- render the complete R20 transport prompt directly in the Human-facing response for copy/paste.

After the Human runs Codex and returns terminal `STATUS/HANDOFF/BRANCH/HEAD`, verify the evidence from GitHub and perform D068 Stage 7 convergence.

## Completion condition

This transport-policy correction objective is complete when D071, R20 and O244 are durably integrated on `develop`. T061 itself remains incomplete and authorized for Stage 6, awaiting the Human-mediated Codex start and later terminal evidence.

## Do not

Do not attempt direct ChatGPT-to-Codex invocation. Do not search for a Codex execution plugin/transport. Do not tell the Human merely to open a persisted prompt path without also rendering the complete prompt. Do not treat the normal Human transport step as a blocker. Do not claim Stage 6 execution before real Codex evidence exists. Do not mutate Freeze C/Freeze D or historical v13 evidence. Do not change the frozen model/effort/CLI/host cell silently. Do not start T024. Do not modify or silently close D066 gaps. Do not reopen T058. Do not perform historical branch cleanup.
