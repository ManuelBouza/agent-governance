# T033 — Native Windows Portability Baseline

## Identity

- Task ID: `T033`
- Status: `ACCEPTED`
- Type: `fix`
- Base branch: `develop`
- Expected topic branch: `fix/t033-native-windows-portability-baseline`
- Expected executor handoff: `handoffs/T033-executor-handoff.json`
- Test-Authorship-Mode: `executor-implementation`
- Assurance-Class: `portability`
- Verification-Planes: `static, deterministic, portability, package`
- Release-Impact: `compatibility`
- Context-Impact: `none`

## Objective

Restore a green canonical deterministic baseline on a native-Windows checkout without weakening existing Governance, artifact, repository-context, or byte-canonicalization semantics.

The task exists because the first clean Codex/Windows executor preflight on current `develop` proved that the repository is not currently portable to native Windows: production code imports POSIX-only `fcntl`, checkout EOL behavior is not repository-controlled, several tests create platform-translated CRLF fixtures while asserting canonical LF bytes, and artifact inventory ordering depends on platform-specific `Path` comparison behavior.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`
- `docs/CODEX-WINDOWS-EXECUTOR-SETUP.md`
- `docs/tasks/T018-consumer-v1-characterization-and-package-baseline.md`
- `docs/tasks/T020-self-contained-build-artifact-and-identity.md`
- `docs/tasks/T030-repository-context-baseline-and-measure-linter.md`
- `docs/tasks/T031-rcab-context-manifest-and-ratchet.md`
- `docs/tasks/T032-rcab-snapshot-live-separation.md`

## Authorized scope

- Non-Markdown implementation required to make the shared Governance engine locking path portable across supported Windows/POSIX hosts.
- Non-Markdown artifact-builder changes required to make deterministic inventory ordering platform-independent.
- Repository configuration needed to make canonical checkout line endings explicit and reproducible, including a root `.gitattributes` if that is the appropriate implementation.
- Non-Markdown test/fixture changes required to construct canonical LF inputs explicitly on Windows while preserving the existing byte-exact expectations.
- Focused supplementary portability/regression tests owned by the executor.
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, regeneration, or semantic normalization.
- Any change to T021 implementation or the existing `refactor/t021-consumer-profile-abstraction` branch.
- RCAB policy/threshold/manifest semantics, snapshot/live separation semantics, Governance Core protocol semantics, Consumer Skill activation semantics, or release promotion.
- Weakening/removing canonical JSON, byte-count, digest, ordering, characterization, locking-safety, or fail-closed assertions merely to make Windows pass.
- Making acceptance depend on changing the Human workstation's global `core.autocrlf` setting.
- Replacing repository portability with a Codex-specific workaround or product dependency.
- Direct writes to `develop` or `main`.
- Force-pushing represented history.

## Invariants / constraints

- Existing accepted Consumer v1 and artifact behavior remain unchanged except for removal of unintended platform dependence.
- Locking must preserve at least the existing safety properties for concurrent EXCHANGE access. A platform implementation may use different primitives, but it must not permit torn/unsafe mutation or silently skip locking when a lock cannot be established.
- Unsupported lock/platform conditions must fail closed with the repository's expected controlled-error behavior rather than degrading to unlocked operation.
- Canonical LF byte semantics remain canonical where tests/artifacts currently require LF. Windows fixture construction must match those semantics explicitly rather than changing expected byte counts to CRLF.
- Checkout EOL behavior needed for deterministic repository-context measurements must be controlled by repository state. A normal Windows clone with `core.autocrlf=true` must not silently convert files whose canonical bytes are measured or formatted as LF.
- Applying checkout normalization controls must not create a content diff in committed Markdown blobs. Any Markdown blob diff is a stop/escalation condition.
- Artifact inventory order must be defined by canonical relative path strings, not by platform-specific `Path` comparison/case behavior.
- The implementation must remain executor-host neutral; Codex is only the host exposing the defect.

## Acceptance criteria

### AC-T033-1 — portable locking

The shared engine imports and executes on native Windows without `fcntl`, while preserving deterministic/fail-closed locking safety for EXCHANGE reads/writes and retaining supported POSIX behavior.

### AC-T033-2 — repository-controlled LF checkout

The repository declares sufficient EOL policy so a fresh native-Windows checkout with ordinary `core.autocrlf=true` produces canonical LF working-tree bytes for files whose exact bytes/format are part of verification. Ruff formatting and repository-context byte measurements must not depend on a user-specific Git setting.

### AC-T033-3 — platform-neutral test fixtures

Tests that intentionally model canonical LF text/JSON/JSONL create those bytes explicitly and pass on native Windows without weakening canonical byte/digest expectations.

### AC-T033-4 — platform-neutral artifact ordering

Artifact identity/inventory ordering is deterministic from canonical relative path strings and yields the same logical order independent of Windows `Path` comparison behavior.

### AC-T033-5 — canonical baseline green

On a native-Windows checkout of the submitted branch, all canonical verification succeeds:

```text
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

The full deterministic suite must be green with no T021 changes and no workstation-global `core.autocrlf` change used as the fix.

## Verification requirements

- Add focused technical tests for the portable locking implementation, including negative/error behavior sufficient to prove that lock acquisition is not silently bypassed.
- Run existing Consumer v1 characterization and artifact regression coverage affected by the locking/artifact changes.
- Run affected repository-context/RCAB tests without changing their accepted semantic expectations.
- Prove representative tracked source/test/tool files are checked out as LF under the repository EOL policy on native Windows; include `git check-attr` / `git ls-files --eol` evidence or equivalent in the handoff.
- Verify that introducing/normalizing `.gitattributes` or equivalent produces no committed Markdown content diff.
- Run the complete canonical verification listed in AC-T033-5.
- Map AC-T033-1 through AC-T033-5 to exact test/command evidence in the persisted handoff.

Host-sandbox failures are not repository acceptance failures. If the Codex native-Windows restricted token cannot initialize uv cache/temp state because of the already observed host ACL defect, use only the Human-approved host escalation necessary to execute the canonical commands; do not encode that workaround into repository correctness or enable permanent Full Access.

## Stop / escalation conditions

- Correct locking requires changing observable Governance/Consumer semantics rather than replacing platform-specific mechanics.
- A proposed EOL fix requires committing changed Markdown content/blobs or changing RCAB canonical-byte semantics.
- Existing accepted snapshots/expected digests/byte counts appear semantically wrong rather than merely platform-translated.
- The implementation would require disabling locking, skipping failing tests, weakening deterministic assertions, changing T021, or changing global workstation Git configuration as the acceptance mechanism.
- The canonical suite remains red after the identified Windows portability classes are fixed for an unrelated reason outside this task.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist `handoffs/T033-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push all authorized non-Markdown work on the expected topic branch, verify the pushed remote HEAD, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.

T021-R1 remains blocked until T033 is accepted/integrated and a clean native-Windows `develop` baseline is green.

## Review / rework lifecycle

### T033-R1 — REWORK_REQUIRED

`docs/reviews/T033-R1.md` reviewed submitted executor HEAD `e97ad4f7593548ad3b6277f265a41be48d812133`. AC-T033-1 through AC-T033-4 passed, but AC-T033-5 failed because the submitted test changes converted seven existing unsafe-symlink/security negative controls into Windows host-capability skips when symlink creation returns `WinError 1314`.

That change conflicts with this contract's explicit prohibition on weakening deterministic assertions merely to make Windows pass and its stop condition for an implementation that would require skipping failing tests.

Rework authority remained the unchanged T033 Task Contract plus `docs/reviews/T033-R1.md`. The existing topic branch/history was preserved.

### T033-R2 — ACCEPTED

`docs/reviews/T033-R2.md` reviewed executor terminal HEAD `f17f8d22f78ed06062c139d2d4fc5f18773eafb6` and implementation anchor `77ba22fce6c15a09ab4235b59311f6bb9a189ebd`.

R1 rework removed all skip-based acceptance weakening. Native Windows executes equivalent unsafe-link controls using NTFS junction fixtures when ordinary symbolic-link creation is unavailable. The handoff reports Ruff lint/format green, `75 passed, 0 skipped` for the affected Consumer security suite, `325 passed, 0 skipped` for the full deterministic suite, repeated concurrent appender stress green, repository-controlled LF checkout under `core.autocrlf=true`, and no Markdown blob diff.

PR #179 integrated the accepted implementation to `develop` as squash commit `c111d00aa7b3ff1adaa5883f9850d109c29dc7a7`.

T033 is accepted. The only remaining precondition before T021-R1 re-entry is a fresh canonical native-Windows verification of current `develop` after the acceptance/checkpoint Markdown is integrated.
