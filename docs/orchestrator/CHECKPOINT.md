# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O135  
Canonical-Branch: `develop`  
Current-Work-Unit: Post-T033 native-Windows `develop` baseline validation before T021-R1  
Chat-Closure: KEEP_CURRENT_CHAT

## Completed

- Human Owner selected the new ChatGPT desktop app on native Windows, using its Codex view, as the Agente de IA Ejecutor surface. Codex CLI remains diagnostic-only.
- The executor-independence boundary remains intact: canonical Git plus repository instructions/Task Contracts/reviews are authority; prior OpenCode/Gentle-IA and quarantined Codex project state were not imported.
- Native Windows workstation bootstrap is established: Git `2.53.0.windows.2`, GitHub CLI `2.88.1` authenticated over HTTPS, uv `0.11.32`, native checkout `C:\Manuel\Projects\agent-governance`, and repository-local `.venv` from `uv sync --locked` under CPython `3.13.14`.
- The first clean Codex-app baseline exposed native-Windows repository portability defects, so T021 correctly stopped before mutation.
- T033 was created to repair those unrelated portability defects.
- T033-R1 accepted the locking, LF-checkout, LF-fixture and canonical artifact-ordering repairs but rejected seven Windows `pytest.skip(...)` outcomes that weakened existing unsafe-link/security negative controls.
- Codex completed T033-R1 rework on the preserved `fix/t033-native-windows-portability-baseline` branch. Executor terminal HEAD was `f17f8d22f78ed06062c139d2d4fc5f18773eafb6`; implementation anchor was `77ba22fce6c15a09ab4235b59311f6bb9a189ebd`.
- The corrected handoff reports `75 passed, 0 skipped` for the affected Consumer security suite and `325 passed, 0 skipped` for the full native-Windows deterministic suite, plus Ruff lint/format green, repeated concurrent appender stress green, LF checkout under `core.autocrlf=true`, and no executor Markdown diff.
- T033-R2 accepts AC-T033-1 through AC-T033-5. Implementation PR #179 was squash-merged to `develop` as `c111d00aa7b3ff1adaa5883f9850d109c29dc7a7`.
- After the executor terminal handoff but before PR #179, the Orchestrator accidentally created and deleted six temporary `noop*` files on the T033 topic branch while attempting PR mechanics. Those twelve reviewer-side commits changed no final tree content: comparison from executor HEAD `f17f8d22f78ed06062c139d2d4fc5f18773eafb6` to PR head `0f8b88ecd4f64c6b92947815ae4777cad5947bdd` reports no changed files. This was an Orchestrator tooling error, not executor noncompliance or an authorized workflow pattern.
- T033 is now `ACCEPTED`; `docs/reviews/T033-R2.md` is the durable acceptance record.

Executable order returns to `T021 R1 -> T022 -> MG1 -> T023 -> T024`; T026 remains separately gated. T021 still has one launch precondition: a fresh canonical native-Windows verification of current `develop` after this acceptance/checkpoint record is integrated.

## Controlling References

For the immediate baseline gate:

- `docs/reviews/T033-R2.md`
- `docs/CODEX-WINDOWS-EXECUTOR-SETUP.md`
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`

For T021 re-entry after the baseline is green:

- `docs/tasks/T021-consumer-profile-abstraction-zero-drift.md`
- `docs/reviews/T021-R1.md`
- `docs/REFACTORING-WORKFLOW.md`
- `docs/decisions/D048-normal-task-single-final-push.md`

## Active Remote Artifacts

```text
T033 status                = ACCEPTED
T033 Review                = docs/reviews/T033-R2.md
T033 executor HEAD         = f17f8d22f78ed06062c139d2d4fc5f18773eafb6
T033 implementation anchor = 77ba22fce6c15a09ab4235b59311f6bb9a189ebd
T033 integration PR        = #179
T033 integrated commit     = c111d00aa7b3ff1adaa5883f9850d109c29dc7a7

T021 Task Contract         = docs/tasks/T021-consumer-profile-abstraction-zero-drift.md
T021 Review                = docs/reviews/T021-R1.md
T021 topic branch          = refactor/t021-consumer-profile-abstraction
T021 last verified HEAD    = 969e2130ca9abb27c6ae5ad830923582f45b8a2f

Selected host              = ChatGPT desktop app, Codex view, Windows native
Primary surface            = graphical Codex app workflow; CLI diagnostics only
Sandbox backend            = unelevated Human-approved fallback; elevated helper remains blocked
Native checkout            = C:\Manuel\Projects\agent-governance
uv                         = 0.11.32
```

The T021 remote branch identity above is historical until reverified immediately before launch.

## Open Questions Or Blockers

T033 implementation acceptance is complete. T021 remains temporarily blocked only by the required **fresh current-`develop` native-Windows canonical baseline** after the T033 acceptance/checkpoint Markdown is integrated.

The baseline gate must run without repository mutation:

```text
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

If the Codex unelevated sandbox still interferes with uv cache/pytest temporary-state ACLs, narrowly approve only the command escalation needed to execute canonical verification. Permanent Full Access, Windows ACL weakening, Defender disablement, global Git changes, or repository-encoded Codex workarounds remain prohibited.

If the fresh current-`develop` suite is red for any cause outside T021, T021 must stop again and the unrelated defect must be governed separately.

## Independence-Test Boundary

The Codex app has now demonstrated cold repository diagnosis, contract-driven implementation, durable handoff, rework from persisted review authority, preservation of represented branch history, and successful terminal publication without importing prior executor project history.

This does not remove normal review gates: Codex execution evidence is not acceptance authority. ChatGPT independently reviewed and rejected T033-R1 before accepting T033-R2.

The first T021-R1 mutation on this host must still start from a **fresh Codex app chat** and use the native-Windows **Local checkout**, not an automatically managed worktree, because the existing T021 remote branch carries represented history that must be reconciled without discard/recreation or force-push rewriting.

## Next Action

1. Integrate this T033 acceptance/checkpoint Markdown branch to `develop`.
2. In the Codex app, synchronize the native local checkout to the resulting current `origin/develop` and run the canonical baseline read-only. Do not start T021 during that verification.
3. If the baseline is green, the Orchestrator re-verifies current remote `develop` and the exact remote `refactor/t021-consumer-profile-abstraction` HEAD immediately before launch.
4. Launch only T021-R1 in a fresh Codex app chat using the unchanged T021 Task Contract plus `docs/reviews/T021-R1.md`; safely reconcile current `develop` into the existing represented T021 branch without discard/recreation/force-push.
5. Codex performs only the narrow T021-R1 correction, full required verification, terminal handoff, commit and D048 final push.
6. Orchestrator reviews the pushed T021 branch/handoff/diff and either accepts/integrates it or persists further rework. T022 MUST NOT start before T021 acceptance.

## Next Chat Minimum Load

If orchestration resumes before the post-T033 baseline is validated, load only:

- `docs/reviews/T033-R2.md`;
- `docs/CODEX-WINDOWS-EXECUTOR-SETUP.md`;
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`.

After a green baseline makes T021 active, load only:

- `docs/tasks/T021-consumer-profile-abstraction-zero-drift.md`;
- `docs/reviews/T021-R1.md`;
- `docs/REFACTORING-WORKFLOW.md`;
- `docs/decisions/D048-normal-task-single-final-push.md`.

Then verify the exact remote T021 branch before launch. Do not load T022 until T021 acceptance.

## Do Not Load Or Do

Do not start T021 before the fresh current-`develop` native-Windows baseline is green; start T022; rerun/modify T032; change RCAB acceptance semantics; weaken deterministic security claims; use global `core.autocrlf` changes as a fix; enable permanent Codex Full Access; weaken Windows security; substitute Codex CLI as the primary executor; import prior hidden project state; directly write `main`/`develop`; discard/recreate/force-push represented T021 history; or batch downstream work before T021 acceptance.
