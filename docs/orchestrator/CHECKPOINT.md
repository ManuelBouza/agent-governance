# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O003  
Canonical-Branch: `develop`  
Chat-Closure: NEW_CHAT_RECOMMENDED

## Current Work Unit

The dedicated ChatGPT Project bootstrap is configured by the Human Owner. Source-product foundation/readiness decisions are complete through D028. The first executable deterministic harness task is ready but has not been launched.

## Completed

- D022 established contract-first, remote-first source-product change procedure.
- D023 selected Python >=3.13, pytest 9.x, and Hypothesis 6.x for applicable stateful layers.
- D024 established the testing Skill/capability model: no generic testing Skill is required; Maintainer Skill is optional routing when available.
- D025 selected the local source-maintenance toolchain: Git + uv + Python + pytest + Ruff, with locked reproducible commands.
- D026 established capability-first/reuse-before-install coexistence with existing SDD systems, Skills, registries, permissions, and project tooling; protocol source is 1.9.0.
- D027 established the ChatGPT Orchestrator checkpoint/cold-start/chat-closure mechanism.
- D028 established ChatGPT Project Instructions as a stable Git bootstrap adapter rather than a dynamic source of project state.
- The Human Owner created the dedicated ChatGPT Project, configured the canonical Project Instructions from `docs/CHATGPT-PROJECT-SETUP.md`, and moved the current chat into that Project.
- `docs/tasks/T001-deterministic-test-harness-foundation.md` is `READY` and has not been executed.

## Controlling References

For the next work unit:

- `AGENTS.md`
- `docs/tasks/T001-deterministic-test-harness-foundation.md`
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`
- `docs/ORCHESTRATOR-CHECKPOINTS.md`

Do not preload the full decision history unless a concrete conflict requires it.

## Active Remote Artifacts

- ChatGPT Project setup contract: `docs/CHATGPT-PROJECT-SETUP.md`
- Ready Task Contract: `docs/tasks/T001-deterministic-test-harness-foundation.md`
- Expected executor branch when launched: `test/governance-harness`
- Expected executor handoff: `handoffs/T001-executor-handoff.json`
- No executor implementation branch/handoff is active yet.

## Open Questions or Blockers

None for T001 readiness.

The local workstation/bootstrap for T001 has not yet been performed in this workflow and OpenCode has not yet been launched against T001.

## Next Action

Start a **new chat inside the dedicated ChatGPT Project** with only:

`Continue.`

The new chat must use GitHub, read current `develop`, `AGENTS.md`, and this checkpoint before acting. It then guides the Human Owner through the minimal local workstation/bootstrap sequence required by D025 and provides the minimal OpenCode launch prompt pointing to `AGENTS.md` and T001.

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
