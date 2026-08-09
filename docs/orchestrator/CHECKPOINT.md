# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O001  
Canonical-Branch: `develop`  
Chat-Closure: NEW_CHAT_RECOMMENDED

## Current Work Unit

Source-product foundation/readiness decisions are complete through D027. The first executable deterministic harness task is ready but has not been launched.

## Completed

- D022 established contract-first, remote-first source-product change procedure.
- D023 selected Python >=3.13, pytest 9.x, and Hypothesis 6.x for applicable stateful layers.
- D024 established the testing Skill/capability model: no generic testing Skill is required; Maintainer Skill is optional routing when available.
- D025 selected the local source-maintenance toolchain: Git + uv + Python + pytest + Ruff, with locked reproducible commands.
- D026 established capability-first/reuse-before-install coexistence with existing SDD systems, Skills, registries, permissions, and project tooling; protocol source is 1.9.0.
- D027 established this ChatGPT Orchestrator checkpoint/cold-start/chat-closure mechanism.
- `docs/tasks/T001-deterministic-test-harness-foundation.md` is `READY` and has not been executed.

## Controlling References

For the next work unit:

- `AGENTS.md`
- `docs/tasks/T001-deterministic-test-harness-foundation.md`
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`
- `docs/ORCHESTRATOR-CHECKPOINTS.md`

T001 itself references the deeper D019/D023-D026 contracts needed by the Agente de IA Ejecutor; do not preload the full decision history unless a concrete conflict requires it.

## Active Remote Artifacts

- Ready Task Contract: `docs/tasks/T001-deterministic-test-harness-foundation.md`
- Expected executor branch when launched: `test/governance-harness`
- Expected executor handoff: `handoffs/T001-executor-handoff.json`
- No executor implementation branch/handoff is active yet.

## Open Questions or Blockers

None for T001 readiness.

The workstation has not yet been prepared in this workflow and OpenCode has not yet been launched against T001.

## Next Action

Start the next ChatGPT interaction in a **new chat**.

That new chat should guide the Human Owner through the minimal local workstation/bootstrap sequence required by D025, then provide the minimal OpenCode launch prompt pointing to `AGENTS.md` and T001.

Do not redesign D022-D026 unless new evidence reveals a concrete conflict. Do not execute T001 from ChatGPT; execution belongs to the Agente de IA Ejecutor.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint, load only:

1. `docs/tasks/T001-deterministic-test-harness-foundation.md`;
2. `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`.

Load other controlling references only if T001/toolchain routing requires them.

## Do Not Load or Do

- Do not require the previous ChatGPT conversation.
- Do not summarize/replay D001-D027 wholesale.
- Do not start a consumer `.agent-coordination/` instance in this source repository.
- Do not implement T001 as ChatGPT.
- Do not ask OpenCode to infer task semantics from chat; point it to the persisted Task Contract.
