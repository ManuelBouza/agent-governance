# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O130  
Canonical-Branch: `develop`  
Current-Work-Unit: Codex/Windows executor-host onboarding before T021-R1  
Chat-Closure: KEEP_CURRENT_CHAT

## Completed

- Human Owner selected Codex on native Windows as the next Agente de IA Ejecutor host, replacing the previous OpenCode + Gentle-IA/WSL workstation path for the next execution.
- The host change is explicitly an executor-independence test; it does not change the abstract executor role, T021 semantics, acceptance criteria, or authority model.
- Codex/Windows configuration and cold-start controls are documented in `docs/CODEX-WINDOWS-EXECUTOR-SETUP.md`.
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md` points to separate OpenCode and Codex host adaptations while preserving host neutrality.
- The Windows-native Codex runtime was refreshed to standalone Codex CLI `0.149.0` and authenticated through ChatGPT.
- Prior Codex home state was quarantined outside the active `%USERPROFILE%\.codex` tree rather than migrated into the independence baseline. The active Codex home was recreated with `workspace-write`, `on-request`, Human approval review, private desktop, and command network disabled by default.
- The preferred native Windows `elevated` sandbox was reproducibly blocked during helper setup by `helper_sandbox_lock_failed` / `SetSecurityInfo sandbox dir failed: 5`, including from an Administrator PowerShell. Read-only ACL inspection showed the sandbox-bin directory owned by Administrators with FullControl for SYSTEM, Administrators, and the Human user; setup logs showed sandbox-user and WFP/firewall provisioning succeeded before the helper ACL lock step failed.
- Codex then self-diagnosed the host using local evidence only under a disposable non-project directory. Its reported result is that normal native-Windows agent command execution works through the `unelevated` restricted-token backend, including successful real command execution and enforced denial outside writable roots; it attributed the direct `codex sandbox windows` `CreateProcessAsUserW failed: 2` result to an invalid diagnostic invocation that attempted to execute the nonexistent command `windows` rather than to failure of the working unelevated agent path.
- The current practical sandbox choice during diagnosis is therefore the guide's documented fallback: `windows.sandbox = "unelevated"`. The `elevated` backend remains host-blocked pending a fixed Codex helper/version or a separately authorized version experiment; no manual ACL weakening, Defender disablement, sandbox bypass, downgrade, or prohibited backup import was used.
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
Sandbox backend    = unelevated fallback under evaluation; elevated blocked by local Codex 0.149.0 helper failure
```

No T021 implementation PR is authorized before fresh Orchestrator acceptance of the terminal rework handoff and remote diff.

## Open Questions Or Blockers

The Codex/Windows **core execution path** is now validated with the documented `unelevated` fallback, but the complete Agent Governance launch-condition checklist is not yet finished.

Before T021 launch, the Human Owner must still validate the remaining workstation/repository-specific items from `docs/CODEX-WINDOWS-EXECUTOR-SETUP.md`, including:

- explicit Human confirmation that `unelevated` is accepted as the documented sandbox fallback for the T021 independence baseline;
- native Git identity/read path against the canonical repository;
- `uv` installation/version plus `uv sync --locked` bootstrap;
- GitHub authentication/read diagnostics sufficient for fetch and later authorized final push;
- the intended native-Windows checkout identity and deliberate repository trust after verification;
- root `AGENTS.md` instruction discovery from a fresh Codex chat;
- no project-semantic Codex-home `AGENTS.md` / `AGENTS.override.md`;
- local Codex memories disabled for the baseline chat;
- no Gentle-IA or project-aware MCP/Skill/hook/rule importing hidden prior Agent Governance state;
- canonical deterministic baseline green before T021 mutation;
- exact current remote T021 branch identity re-verified immediately before execution.

The `elevated` sandbox is a host-only blocker rather than a T021 semantic defect. The active guide permits a Human-approved documented fallback, but T021 must not launch until that fallback is explicitly accepted for this baseline. If accepted, it must remain `workspace-write` + `on-request` with Human approval review and command network off by default.

The executor MUST stop/escalate rather than absorb unrelated work if either:

- the remote T021 branch has advanced from the last verified HEAD before re-entry; or
- the canonical deterministic baseline on current `develop` is not green for reasons outside T021 scope.

## Independence-Test Boundary

The first Codex T021 run must start from a fresh Codex chat and canonical Git state, not from migrated OpenCode/Gentle-IA context or the quarantined prior Codex home.

Project semantics come from repository `AGENTS.md`, this checkpoint, the T021 Task Contract and review. Codex-home memories/instructions/extensions must not substitute hidden prior task state.

For T021-R1, prefer the native-Windows **Local checkout** rather than an automatically managed Codex worktree because the existing T021 remote branch already carries represented history that must be reconciled without discard/recreation or force-push rewriting.

D048 still controls publication. No intermediate progress push is authorized.

## Next Action

1. Human Owner explicitly accepts or rejects the `unelevated` documented fallback, then completes the remaining Codex/Windows launch-condition checks: Git/GitHub/uv readiness, fresh native checkout identity/trust, instruction-source isolation, memory/extension isolation, and clean deterministic repository bootstrap.
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

Do not migrate old OpenCode/Gentle-IA project state or the quarantined prior Codex home into the active Codex baseline; enable hidden project-aware Codex memory/extensions for the baseline; weaken Windows security or repository authority merely to make the `elevated` sandbox pass; rerun T032/OP066; resume T021 from stale WSL/local session state; discard or rewrite represented T021 history; start T022; pre-register MG1/T023; choose R*/B*; launch T026; or batch downstream implementation before T021 acceptance.
