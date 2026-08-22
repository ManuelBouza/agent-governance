# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O132  
Canonical-Branch: `develop`  
Current-Work-Unit: Native-Windows deterministic-baseline portability blocker before T021-R1  
Chat-Closure: KEEP_CURRENT_CHAT

## Completed

- Human Owner selected the new ChatGPT desktop app on native Windows, using its Codex view, as the next Agente de IA Ejecutor surface. Codex CLI remains diagnostic-only and is not the primary task transport.
- The host change remains an executor-independence test. Git, repository instructions, Task Contracts/reviews and persisted handoffs remain authoritative; no OpenCode/Gentle-IA or quarantined prior Codex project state was imported.
- The active Codex home was recreated cleanly. Local memories and memory generation are disabled for the independence baseline, project-semantic custom instructions are absent, and the old Codex home remains quarantined outside the active tree.
- Codex is configured Windows-native with PowerShell, `workspace-write`, `on-request`, Human approval review and command network off by default. The preferred `elevated` Windows sandbox remains blocked by the local helper `SetSecurityInfo` failure; Human Owner previously approved the documented `unelevated` restricted-token fallback rather than weakening Windows security.
- Native workstation tooling is now present and verified from a fresh PowerShell session: Git `2.53.0.windows.2`, GitHub CLI `2.88.1` authenticated to the canonical repository over HTTPS, and uv `0.11.32`, which satisfies the repository-declared `>=0.11.32,<0.12` requirement.
- A fresh native checkout now exists at `C:\Manuel\Projects\agent-governance`. It was cloned from the canonical GitHub repository directly on `develop`; local `HEAD` and `origin/develop` both matched `51a8842e252ee172dab453d5a92eaf18e75d36c4`, with a clean working tree.
- `uv sync --locked` succeeded on that checkout using CPython `3.13.14` and created the repository-local `.venv` from locked state.
- A fresh Codex-app chat was then used for a **read-only baseline diagnosis**. Codex did not modify repository files, create commits, switch branches, or start T021. It finished with the checkout still clean on `develop` at the same HEAD.
- The fresh Codex diagnostic exposed two host-layer issues: the already-running desktop app had not inherited the newly installed uv PATH (`C:\Users\Manuel\.local\bin\uv.exe`), and the `unelevated` restricted-token sandbox produced ACL/access-denied failures for uv cache and pytest temporary directories. These are host-execution issues, not repository acceptance defects; permanent Full Access is not authorized as a workaround.
- After removing sandbox noise with a specifically externalized diagnostic invocation, the native-Windows repository baseline itself was still red: `27 failed, 237 passed, 57 errors`.
- The diagnostic identified and the Orchestrator remotely confirmed the main repository portability classes on current `develop`:
  - `src/agent_governance/engine.py` imports POSIX-only `fcntl` unconditionally and uses `fcntl.flock`, so the production engine cannot import on native Windows;
  - the repository has no root `.gitattributes`, while the workstation has `core.autocrlf=true` and repository formatting/byte-canonicalization requires LF, so ordinary Windows checkout conversion changes working-tree bytes;
  - several repository-context tests create text using platform-translating writers while asserting canonical LF byte counts/JSON, leaving genuine Windows fixture defects even in an LF checkout;
  - `src/agent_governance/artifact.py` sorts `Path` objects directly, while the artifact regression expects canonical case-sensitive string ordering, producing platform-dependent inventory order on Windows.
- T021 correctly stopped at the preflight boundary. The existing `refactor/t021-consumer-profile-abstraction` implementation branch was not touched.
- The Orchestrator created planning branch `docs/o132-native-windows-baseline-blocker` from current `develop` and persisted `docs/tasks/T033-native-windows-portability-baseline.md` to govern the unrelated portability repair before T021 can resume.

Executable order is now `T033 -> T021 R1 -> T022 -> MG1 -> T023 -> T024`; T026 remains separately gated.

## Controlling References

For the immediate blocker:

- `docs/tasks/T033-native-windows-portability-baseline.md`
- `docs/CODEX-WINDOWS-EXECUTOR-SETUP.md`
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`
- `docs/TASK-CONTRACTS.md`

For T021 only after T033 acceptance and a green fresh `develop` baseline:

- `docs/tasks/T021-consumer-profile-abstraction-zero-drift.md`
- `docs/reviews/T021-R1.md`
- `docs/REFACTORING-WORKFLOW.md`
- `docs/decisions/D048-normal-task-single-final-push.md`

T033 is a portability repair only. It must not absorb T021 profile semantics, RCAB policy changes, or a Codex-specific product dependency.

## Active Remote Artifacts

```text
Canonical develop       = 51a8842e252ee172dab453d5a92eaf18e75d36c4
Planning branch         = docs/o132-native-windows-baseline-blocker
T033 Task Contract      = docs/tasks/T033-native-windows-portability-baseline.md
T033 expected branch    = fix/t033-native-windows-portability-baseline
T033 expected handoff   = handoffs/T033-executor-handoff.json

T021 Task Contract      = docs/tasks/T021-consumer-profile-abstraction-zero-drift.md
T021 Review             = docs/reviews/T021-R1.md
T021 topic branch       = refactor/t021-consumer-profile-abstraction
T021 last verified HEAD = 969e2130ca9abb27c6ae5ad830923582f45b8a2f

Selected host           = ChatGPT desktop app, Codex view, Windows native
Primary surface         = graphical Codex app workflow; CLI diagnostics only
Sandbox backend         = unelevated Human-approved fallback; elevated helper remains blocked
Native checkout         = C:\Manuel\Projects\agent-governance
uv                      = 0.11.32
```

The T033 contract is not executable merely because it exists on the planning branch. The planning change must first be reviewed and integrated into `develop` under the normal Task Contract integration gate.

## Open Questions Or Blockers

T021 is now blocked by a **real repository portability defect**, not merely by workstation setup. The canonical deterministic suite must become green on native Windows before T021 re-entry.

Host readiness also has two remaining operational details:

- fully restart the ChatGPT desktop app so the Codex process inherits the newly persistent uv PATH, then verify `uv --version` from Codex without using the absolute executable path;
- the `unelevated` sandbox currently interferes with uv cache/pytest temp ACLs. If this persists during T033, keep normal repository work under `workspace-write` and approve only the specific command escalation needed for canonical verification. Do not enable permanent Full Access, weaken ACLs, disable Defender, or encode a host workaround into repository correctness.

T033 acceptance must not use a Human-specific `git config --global core.autocrlf false` change as the fix. Repository state must control the canonical line-ending behavior needed for deterministic source/fixture/artifact bytes.

The executor must stop/escalate if the T033 fixes expose a different unrelated red-baseline cause outside its contract.

## Independence-Test Boundary

The successful read-only diagnosis already demonstrates that the Codex app can enter the repository cold, obey the no-mutation/T021 stop boundary, use the local toolchain and return technically useful evidence without imported previous-agent project history.

The first **mutation** by Codex must now be T033 after its contract is integrated. T021 remains a later, separate re-entry task and still requires a fresh Codex app chat plus preservation of its represented remote branch history.

Host-native Skills, plugins, subagents and compatible technical tools remain available to the executor under D041. They are implementation aids only; they may not supply hidden Agent Governance history or redefine Task Contract authority.

## Next Action

1. Review the O132 planning diff, open its Markdown-only PR to `develop`, and integrate the T033 Task Contract/checkpoint update.
2. Human Owner fully restarts the ChatGPT desktop app so the Codex process inherits `C:\Users\Manuel\.local\bin` and verifies `uv --version` inside a fresh Codex project chat.
3. Orchestrator re-verifies current remote `develop` after O132 integration and launches only T033 using the canonical minimal Task Contract transport.
4. Codex executes T033 on `fix/t033-native-windows-portability-baseline`, fixes only the persisted portability scope, runs the required native-Windows verification, persists `handoffs/T033-executor-handoff.json`, performs the normal terminal publication, and returns only the canonical completion fields.
5. Orchestrator reviews the pushed T033 branch/handoff/diff. Only after T033 is accepted/integrated does the Human run a fresh native-Windows `develop` bootstrap/verification.
6. If that baseline is green, Orchestrator re-verifies the exact remote T021 branch identity and resumes T021-R1. T022 remains blocked until T021 acceptance.

## Next Chat Minimum Load

If orchestration resumes before T033 acceptance, load only:

- `docs/tasks/T033-native-windows-portability-baseline.md`;
- `docs/CODEX-WINDOWS-EXECUTOR-SETUP.md`;
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`.

Then verify current remote `develop` and the T033 planning/implementation branch state as applicable. Do not load T021 rework detail until T033 acceptance makes T021 the active frontier again.

## Do Not Load Or Do

Do not start or modify T021; start T022; rerun/modify T032; change RCAB acceptance semantics; use a global `core.autocrlf` workstation change as the repository fix; weaken canonical byte/digest/order/locking assertions; enable permanent Codex Full Access; weaken Windows ACL/security; substitute Codex CLI as the primary executor surface; import the quarantined prior Codex/OpenCode/Gentle-IA project state; directly write `main`/`develop`; force-push represented history; or batch downstream work before T033 acceptance and a green native-Windows baseline.
