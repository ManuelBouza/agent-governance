# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O002  
Canonical-Branch: `develop`  
Chat-Closure: ACTION_REQUIRED

## Current Work Unit

Source-product foundation/readiness decisions are complete through D028. The first executable deterministic harness task is ready but has not been launched. The remaining pre-launch action is to configure the dedicated ChatGPT Project with the canonical Git-first Project Instructions.

## Completed

- D022 established contract-first, remote-first source-product change procedure.
- D023 selected Python >=3.13, pytest 9.x, and Hypothesis 6.x for applicable stateful layers.
- D024 established the testing Skill/capability model: no generic testing Skill is required; Maintainer Skill is optional routing when available.
- D025 selected the local source-maintenance toolchain: Git + uv + Python + pytest + Ruff, with locked reproducible commands.
- D026 established capability-first/reuse-before-install coexistence with existing SDD systems, Skills, registries, permissions, and project tooling; protocol source is 1.9.0.
- D027 established the ChatGPT Orchestrator checkpoint/cold-start/chat-closure mechanism.
- D028 established ChatGPT Project Instructions as a stable Git bootstrap adapter rather than a dynamic source of project state.
- `docs/CHATGPT-PROJECT-SETUP.md` contains the canonical Project Instructions to copy into ChatGPT Project settings.
- `docs/tasks/T001-deterministic-test-harness-foundation.md` is `READY` and has not been executed.

## Controlling References

For the immediate next action:

- `docs/CHATGPT-PROJECT-SETUP.md`

After the ChatGPT Project Instructions are configured, a fresh chat bootstraps from:

- `AGENTS.md`
- `docs/orchestrator/CHECKPOINT.md`

and then follows the minimum load declared below.

## Active Remote Artifacts

- ChatGPT Project setup: `docs/CHATGPT-PROJECT-SETUP.md`
- Ready Task Contract: `docs/tasks/T001-deterministic-test-harness-foundation.md`
- Expected executor branch when launched: `test/governance-harness`
- Expected executor handoff: `handoffs/T001-executor-handoff.json`
- No executor implementation branch/handoff is active yet.

## Open Questions or Blockers

No repository-design blocker remains for T001.

Human/UI action remains: copy the canonical instruction block from `docs/CHATGPT-PROJECT-SETUP.md` into this dedicated ChatGPT Project's **Project settings -> Project instructions**.

For a newly created dedicated ChatGPT Project, project-only memory is preferred when available. If this Project already uses default memory, the Git-first bootstrap remains valid; changing memory mode is not required for T001.

The workstation has not yet been prepared in this workflow and OpenCode has not yet been launched against T001.

## Next Action

1. Human Owner configures the ChatGPT Project Instructions using the exact block in `docs/CHATGPT-PROJECT-SETUP.md`.
2. After configuration, start a **new chat inside this ChatGPT Project** with only: `Continue.`
3. The new chat must use GitHub, read current `develop`, `AGENTS.md`, and this checkpoint before acting.
4. It then guides the Human Owner through the minimal local workstation/bootstrap sequence required by D025 and provides the minimal OpenCode launch prompt pointing to `AGENTS.md` and T001.

Do not execute T001 from ChatGPT; execution belongs to the Agente de IA Ejecutor.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint, load only:

1. `docs/tasks/T001-deterministic-test-harness-foundation.md`;
2. `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`.

Load other controlling references only if T001/toolchain routing requires them.

## Do Not Load or Do

- Do not require the previous ChatGPT conversation.
- Do not reconstruct operational state from Project Memory or prior chats.
- Do not summarize/replay D001-D028 wholesale.
- Do not start a consumer `.agent-coordination/` instance in this source repository.
- Do not implement T001 as ChatGPT.
- Do not ask OpenCode to infer task semantics from chat; point it to the persisted Task Contract.
