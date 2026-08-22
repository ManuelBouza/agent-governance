# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O134  
Canonical-Branch: `develop`  
Current-Work-Unit: T033-R1 native-Windows portability rework launch before T021-R1  
Chat-Closure: KEEP_CURRENT_CHAT

## Completed

- Human Owner selected the new ChatGPT desktop app on native Windows, using its Codex view, as the next Agente de IA Ejecutor surface. Codex CLI remains diagnostic-only.
- The executor-independence boundary remains intact: canonical Git state plus repository instructions/Task Contracts/reviews are authority; no prior OpenCode/Gentle-IA or quarantined Codex project state was imported.
- Native Windows workstation bootstrap is established: Git `2.53.0.windows.2`, GitHub CLI `2.88.1` authenticated over HTTPS, uv `0.11.32`, native checkout at `C:\Manuel\Projects\agent-governance`, and `uv sync --locked` using CPython `3.13.14`.
- The Codex app cold diagnostic correctly stopped T021 when clean native-Windows `develop` exposed real portability defects.
- T033 was persisted and integrated through PR #176.
- Codex executed T033 on `fix/t033-native-windows-portability-baseline` and pushed terminal HEAD `e97ad4f7593548ad3b6277f265a41be48d812133`; implementation anchor is `4f5bc9d7ec7ce9c6aef68c6a23db9eb6fe5860ef` and handoff is `handoffs/T033-executor-handoff.json`.
- T033-R1 review found AC-T033-1 through AC-T033-4 satisfied by the submitted locking, LF checkout, LF fixture, and canonical artifact-ordering repairs.
- AC-T033-5 failed because the submitted branch introduced Windows `pytest.skip(...)` handling for `WinError 1314`, converting seven existing unsafe-symlink/security negative controls into host-capability skips. This conflicts with the Task Contract's explicit prohibition on weakening/skipping deterministic assertions merely to make Windows pass.
- `docs/reviews/T033-R1.md`, the T033 `IN_PROGRESS` lifecycle update, and checkpoint O133 were integrated through PR #177.
- Current canonical `develop` is now `ad761094b4e3a9a3d05f0fe5239a7c779db0718b`.
- The existing T033 implementation branch remains at submitted HEAD `e97ad4f7593548ad3b6277f265a41be48d812133`; compared with current `develop` it is two commits ahead and one commit behind, with merge-base `c581d25d3cfb162d3c4e13838db2af3d1fb3887f`. Rework must reconcile current `develop` into that represented branch without rewriting history.

Executable order remains `T033 R1 -> T021 R1 -> T022 -> MG1 -> T023 -> T024`; T026 remains separately gated.

## Controlling References

For the immediate rework:

- `docs/tasks/T033-native-windows-portability-baseline.md`
- `docs/reviews/T033-R1.md`
- `docs/CODEX-WINDOWS-EXECUTOR-SETUP.md`
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`

For T021 only after T033 acceptance/integration and a green fresh native-Windows `develop` baseline:

- `docs/tasks/T021-consumer-profile-abstraction-zero-drift.md`
- `docs/reviews/T021-R1.md`
- `docs/REFACTORING-WORKFLOW.md`
- `docs/decisions/D048-normal-task-single-final-push.md`

T033 rework is limited to satisfying its existing portability/security verification contract. It must not absorb T021 profile semantics, RCAB policy changes, Governance Core semantics, or host-specific product dependencies.

## Active Remote Artifacts

```text
Canonical develop          = ad761094b4e3a9a3d05f0fe5239a7c779db0718b
T033 Task Contract         = docs/tasks/T033-native-windows-portability-baseline.md
T033 Review                = docs/reviews/T033-R1.md
T033 branch                = fix/t033-native-windows-portability-baseline
T033 submitted HEAD        = e97ad4f7593548ad3b6277f265a41be48d812133
T033 implementation anchor = 4f5bc9d7ec7ce9c6aef68c6a23db9eb6fe5860ef
T033 handoff               = handoffs/T033-executor-handoff.json

T021 Task Contract         = docs/tasks/T021-consumer-profile-abstraction-zero-drift.md
T021 Review                = docs/reviews/T021-R1.md
T021 topic branch          = refactor/t021-consumer-profile-abstraction
T021 last verified HEAD    = 969e2130ca9abb27c6ae5ad830923582f45b8a2f

Selected host              = ChatGPT desktop app, Codex view, Windows native
Sandbox backend            = unelevated Human-approved fallback; elevated helper remains blocked
Native checkout            = C:\Manuel\Projects\agent-governance
uv                         = 0.11.32
```

## Open Questions Or Blockers

T033 is **REWORK_REQUIRED**. The native-Windows suite may not claim canonical green by converting the existing symlink/security negative controls to host-capability skips.

The rework must preserve the accepted locking/EOL/LF-fixture/artifact-ordering improvements unless correction requires otherwise, remove the verification weakening, and execute semantically equivalent native-Windows evidence for the affected unsafe-symlink claims. If faithful coverage cannot be achieved without changing accepted semantics or weakening host security, the executor must return `BLOCKED` rather than normalize skips into acceptance.

T021 remains blocked until corrected T033 is accepted/integrated and a fresh native-Windows `develop` bootstrap/verification is green.

The `unelevated` Codex sandbox may still require narrowly approved command escalation for uv cache/pytest temporary-state ACL behavior. Permanent Full Access, Windows ACL weakening, Defender disablement, global Git changes, or repository-encoded Codex workarounds remain prohibited.

## Independence-Test Boundary

The first mutating Codex task demonstrated that the executor can bootstrap from integrated repository authority, create the required topic branch, implement, verify, persist a handoff and publish terminal state without imported previous-host task history.

The current review failure is a governance/acceptance result, not a host-independence failure: Codex produced useful implementation but the Orchestrator independently rejected a test-coverage weakening against the persisted contract.

Executor-native Skills, plugins, subagents and compatible technical tools remain available under D041. They remain implementation aids, not authority.

## Next Action

1. Launch T033-R1 rework in the Codex app against the existing `fix/t033-native-windows-portability-baseline` branch.
2. The executor must synchronize the canonical remote, establish current `develop@ad761094b4e3a9a3d05f0fe5239a7c779db0718b`, and safely reconcile that integrated review authority into the existing represented T033 branch without discard, recreation, force-push, or loss of the submitted implementation history.
3. Load and execute `docs/tasks/T033-native-windows-portability-baseline.md` together with `docs/reviews/T033-R1.md` as the complete rework authority.
4. Remove the skip-based acceptance weakening, execute faithful native-Windows negative-control evidence, rerun the complete T033 matrix, update the handoff, commit the complete rework, perform the normal terminal final push, verify remote HEAD, and return only the canonical completion fields.
5. Orchestrator reviews the new remote T033 HEAD. Only after acceptance does the implementation proceed through PR to `develop`.
6. After T033 integration, run a fresh native-Windows `develop` canonical baseline. If green, re-verify the exact T021 remote HEAD and resume T021-R1. T022 remains blocked until T021 acceptance.

## Next Chat Minimum Load

If orchestration resumes before T033 acceptance, load only:

- `docs/tasks/T033-native-windows-portability-baseline.md`;
- `docs/reviews/T033-R1.md`;
- `docs/CODEX-WINDOWS-EXECUTOR-SETUP.md`.

Then verify current remote `develop` and `fix/t033-native-windows-portability-baseline`. Do not load T021 rework detail until T033 acceptance makes T021 the active frontier again.

## Do Not Load Or Do

Do not merge submitted T033 HEAD `e97ad4f7593548ad3b6277f265a41be48d812133`; start or modify T021; start T022; rerun/modify T032; change RCAB acceptance semantics; weaken or skip deterministic security claims merely for Windows; use global `core.autocrlf` changes as the fix; enable permanent Codex Full Access; weaken Windows security; substitute Codex CLI as the primary executor; import prior hidden project state; directly write `main`/`develop`; force-push represented history; or batch downstream work before T033 acceptance and a green native-Windows baseline.
