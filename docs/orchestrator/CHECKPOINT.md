# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O129  
Canonical-Branch: `develop`  
Current-Work-Unit: Codex/Windows executor-host onboarding before T021-R1  
Chat-Closure: KEEP_CURRENT_CHAT

## Completed

- Human Owner selected Codex on native Windows as the next Agente de IA Ejecutor host, replacing the previous OpenCode + Gentle-IA/WSL workstation path for the next execution.
- The host change is explicitly an executor-independence test; it does not change the abstract executor role, T021 semantics, acceptance criteria, or authority model.
- Codex/Windows configuration and cold-start controls are documented in `docs/CODEX-WINDOWS-EXECUTOR-SETUP.md`.
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md` now points to separate OpenCode and Codex host adaptations while preserving host neutrality.
- No T021 implementation mutation or new T021 publication has been authorized or performed during host onboarding.
- The last verified remote `refactor/t021-consumer-profile-abstraction` remains `969e2130ca9abb27c6ae5ad830923582f45b8a2f`; it must be re-verified immediately before launch.

Executable order remains `T021 R1 -> T022 -> MG1 -> T023 -> T024`; T026 remains separately gated.

## Controlling References

For host readiness:

- `docs/CODEX-WINDOWS-EXECUTOR-SETUP.md`
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`

For T021 execution after host readiness:

- `docs/tasks/T021-consumer-profile-abstraction-zero-drift.md`
- `docs/reviews/T021-R1.md`
- `docs/REFACTORING-WORKFLOW.md`
- `docs/decisions/D048-normal-task-single-final-push.md`

The T021 Task Contract plus `docs/reviews/T021-R1.md` remain the exclusive semantic rework authority. Codex configuration is host/workstation adaptation only.

## Active Remote Artifacts

```text
Task Contract      = docs/tasks/T021-consumer-profile-abstraction-zero-drift.md
Review             = docs/reviews/T021-R1.md
Topic branch       = refactor/t021-consumer-profile-abstraction
Last verified HEAD = 969e2130ca9abb27c6ae5ad830923582f45b8a2f
Selected host      = Codex, Windows native
```

No T021 implementation PR is authorized before fresh Orchestrator acceptance of the terminal rework handoff and remote diff.

## Open Questions Or Blockers

The Codex/Windows workstation preflight has not yet been confirmed complete by the Human Owner.

Before T021 launch, the Human Owner must validate the launch-condition checklist in `docs/CODEX-WINDOWS-EXECUTOR-SETUP.md`, including native Windows execution, Git/uv/GitHub readiness, `elevated` sandbox, `workspace-write` + `on-request`, repository instruction discovery, memories disabled for the baseline, and absence of prior-host project context from Gentle-IA/MCP/Skills/hooks/rules.

The executor MUST stop/escalate rather than absorb unrelated work if either:

- the remote T021 branch has advanced from the last verified HEAD before re-entry; or
- the canonical deterministic baseline on current `develop` is not green for reasons outside T021 scope.

## Independence-Test Boundary

The first Codex T021 run must start from a fresh Codex chat and canonical Git state, not from migrated OpenCode/Gentle-IA context.

Project semantics come from repository `AGENTS.md`, this checkpoint, the T021 Task Contract and review. Codex-home memories/instructions/extensions must not substitute hidden prior task state.

For T021-R1, prefer the native-Windows **Local checkout** rather than an automatically managed Codex worktree because the existing T021 remote branch already carries represented history that must be reconciled without discard/recreation or force-push rewriting.

D048 still controls publication. No intermediate progress push is authorized.

## Next Action

1. Human Owner configures/validates the Codex native-Windows workstation against `docs/CODEX-WINDOWS-EXECUTOR-SETUP.md` and confirms whether the launch-condition checklist passes.
2. Orchestrator re-verifies current remote `develop` and the exact T021 remote HEAD immediately before launch, then provides only the minimal repository/Task Contract transport.
3. Codex re-bootstraps from current remote `develop`, safely reconciles the existing T021 topic branch without losing represented history, and performs only T021-R1 under the unchanged Task Contract plus `docs/reviews/T021-R1.md`.
4. Codex completes the required characterization/regression verification, persists the terminal `handoffs/T021-executor-handoff.json`, commits the complete authorized state, performs the D048 final push, verifies remote HEAD, and returns only the canonical completion fields.
5. Orchestrator reviews the pushed T021 branch/handoff/diff and either accepts/integrates T021 or persists further rework. T022 MUST NOT start before T021 acceptance.

## Next Chat Minimum Load

If orchestration resumes before Codex preflight completion, load only:

- `docs/CODEX-WINDOWS-EXECUTOR-SETUP.md`;
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`;
- `docs/tasks/T021-consumer-profile-abstraction-zero-drift.md`;
- `docs/reviews/T021-R1.md`;
- `docs/decisions/D048-normal-task-single-final-push.md`.

Then verify the active remote T021 branch before acting. Do not load T022 until T021 acceptance.

## Do Not Load Or Do

Do not migrate old OpenCode/Gentle-IA project state into Codex; enable hidden project-aware Codex memory/extensions for the baseline; rerun T032/OP066; resume T021 from stale WSL/local session state; discard or rewrite represented T021 history; start T022; pre-register MG1/T023; choose R*/B*; launch T026; or batch downstream implementation before T021 acceptance.
