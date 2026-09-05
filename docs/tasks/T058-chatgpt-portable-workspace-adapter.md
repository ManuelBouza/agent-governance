# T058 — ChatGPT Portable Workspace Adapter

## Identity

- Task ID: `T058`
- Status: `READY`
- Type: `feature / source-maintenance infrastructure`
- Base branch: `develop`
- Expected topic branch: `feat/t058-chatgpt-portable-workspace-adapter`
- Expected executor handoff: `handoffs/T058-executor-handoff.json`
- SDD-Profile: `ASSURED`
- Test-Authorship-Mode: `executor-implementation`
- Research: R014, R015
- Controlling decision: `docs/decisions/D066-chatgpt-portable-git-workspace-transport.md`
- Operating procedure: `docs/CHATGPT-PORTABLE-GIT-WORKSPACE.md`

## Objective

Implement a deterministic, fail-closed source-maintainer helper that materializes the locally testable semantics of D066 for ChatGPT portable Git workspaces.

The helper SHALL validate and classify local Git snapshots, ownership/freshness receipts, lock-state observations, portable resume/write gates, release preconditions, publication plans, and post-merge snapshot-GC eligibility without performing GitHub or ChatGPT Library network mutations itself.

The implementation must make the R014/R015-qualified behavior reusable and auditable while preserving GitHub as canonical authority and preserving every unresolved R014/R015 gap as an explicit stop/fail-closed boundary.

## Current specification carrier

Controlling semantics:

- `docs/decisions/D066-chatgpt-portable-git-workspace-transport.md`
- `docs/CHATGPT-PORTABLE-GIT-WORKSPACE.md`
- `docs/decisions/D061-orchestrator-branch-target-write-guard.md`
- `docs/decisions/D058-executor-coordinator-session-and-worktree-hygiene.md`
- `docs/decisions/D062-repository-long-lived-branch-protection-bootstrap.md`
- `docs/decisions/D065-semantic-executor-delegation-obligation.md`

Evidence provenance:

- `docs/research/CHATGPT-GIT-WORKSPACE-AND-GITHUB-TRANSPORT-RESEARCH.md` (R014)
- `docs/research/CHATGPT-GIT-WORKSPACE-LIBRARY-SNAPSHOT-LIFECYCLE-APPENDIX.md`
- `docs/research/CHATGPT-LIBRARY-WORKTREE-SIMULATOR-RESEARCH.md` (R015)
- `docs/research/CHATGPT-LIBRARY-WORKTREE-SIMULATOR-LOCK-LIFECYCLE-APPENDIX.md`
- `docs/research/CHATGPT-LIBRARY-WORKTREE-SIMULATOR-CROSS-CHAT-RACE-APPENDIX.md`

The research is evidence. D066 and this Task Contract control implementation semantics.

## Requirement / specification delta

### ADDED — T058-R1 portable snapshot validation

Provide a deterministic helper capable of validating a standalone repository snapshot containing real `.git` state.

Validation must cover, directly or through composable functions:

- archive SHA-256 calculation/verification;
- safe archive extraction that rejects traversal and unsafe link behavior;
- expected receipt identity;
- `git fsck --full` success;
- clean pre-mutation worktree status when required;
- local Git HEAD and tree identity;
- expected repository/work-unit/topic-branch binding;
- expected remote HEAD/tree values supplied as observations by the caller.

The helper does not discover Library state or GitHub state itself; those external observations are inputs.

### ADDED — T058-R2 ownership and lock classification

Represent a coordination-only lock observation containing at least:

- expected lock branch HEAD;
- observed lock branch HEAD;
- sentinel presence/absence;
- sentinel repository/owner/work-unit/topic/state when present;
- sentinel blob SHA when present.

Classify acquisition fail-closed with stable machine-readable meanings equivalent to:

```text
ACQUIRE_ALLOWED
BLOCKED_STALE_LOCK_HEAD
BLOCKED_OWNER_EXISTS
BLOCKED_AMBIGUOUS_LOCK
```

The exact concurrent rule is:

```text
expected lock HEAD H != observed lock HEAD
=> BLOCKED_STALE_LOCK_HEAD
=> no automatic retry / no ownership transition
```

The helper MUST NOT implement a retry loop that converts a stale observation into acquisition.

### ADDED — T058-R3 portable resume / writable-entry gate

Given validated snapshot state plus externally supplied remote/lock observations, classify writable entry.

WRITE_ALLOWED requires all applicable identities/freshness checks to pass:

```text
repository
owner
work_unit
topic_branch
lock owner/work_unit/topic/state
remote topic HEAD freshness
expected tree equivalence when applicable
snapshot integrity/fsck/clean state
```

Any mismatch yields an unambiguous WRITE_BLOCKED classification, with a specific reason such as identity mismatch, stale/wrong snapshot, invalid snapshot, or stale base.

A wrong worktree/snapshot can never become writable merely because it is locally readable.

### ADDED — T058-R4 release classification

Given the exact current sentinel observation and expected ownership, classify whether release is allowed.

Release eligibility requires:

- sentinel exists;
- repository/owner/work-unit/topic/state match expected values;
- exact current sentinel blob SHA is present.

The helper SHALL return the exact blob SHA required for host-side deletion only on `RELEASE_ALLOWED`.

It SHALL also support deterministic verification of a host-reported post-delete sentinel absence as `RELEASED`; mismatch/continued presence remains blocked/occupied.

The helper itself does not call GitHub delete APIs.

### ADDED — T058-R5 post-merge snapshot GC classification

Classify feature/work-unit snapshot retention or GC eligibility from explicit observations.

`GC_ELIGIBLE` requires all applicable positive evidence:

```text
merged == true
integration_verified == true
target_snapshot_validated == true
target_snapshot_promoted == true
target_snapshot_revalidated == true
```

Fail closed:

```text
closed && !merged -> RETAIN_CLOSED_UNMERGED
ambiguous integration/target state -> RETAIN_AMBIGUOUS
invalid target candidate/current -> RETAIN_INVALID_TARGET_SNAPSHOT
active/not-integrated -> RETAIN_ACTIVE
```

Do not implement an automatic quota-pressure selector.

### ADDED — T058-R6 batched publication plan

Provide a deterministic local publication-plan/manifest function or CLI operation that records at least:

```text
repository
work_unit
topic_branch
expected_remote_head
local_head
local_tree
changed_paths
```

The manifest is an input to the host's connected GitHub publication step. It must not perform network I/O or claim that publication succeeded.

The design should support one bounded/final remote synchronization of many local edits instead of one GitHub content mutation per edit.

### ADDED — T058-R7 machine-readable interface

Expose the helper through a small CLI and importable functions with deterministic JSON output suitable for ChatGPT/Executor adapter use.

Failures used as safety gates must produce non-zero process status and structured status/reason output rather than relying only on prose.

### PRESERVED — T058-P1 canonical authority

GitHub remains canonical repository/branch/PR authority. Local Git state, Library snapshots, receipts, and helper output are evidence/transport state only.

### PRESERVED — T058-P2 D061/D062 branch safety

Nothing in T058 may authorize direct writes to `main`/`develop`, weaken server-side long-lived branch protection, or infer that a local snapshot can bypass the protected PR path.

### PRESERVED — T058-P3 unresolved research gaps

T058 must not implement or claim solved:

- crash/orphan recovery after lock acquisition;
- TTL/heartbeat;
- automatic abandoned-lock reclamation;
- closed-unmerged cross-chat resume;
- ownership transfer;
- automatic lock/topic branch retirement;
- quota-pressure GC selection;
- unusual ref-name canonicalization at scale;
- unqualified ruleset interactions.

### PRESERVED — T058-P4 no external runtime dependency in deterministic tests

The required test suite must not need GitHub, ChatGPT Library, network access, credentials, or account-specific state. Use temporary local Git repositories and synthetic observations.

## Controlling Design

### Architecture

Use a thin CLI plus small cohesive Python modules rather than expanding an unrelated existing module.

Expected shape, with exact module split left to the Executor where semantics remain unchanged:

```text
tools/chatgpt_workspace.py

tools/_chatgpt_workspace/
  models.py
  git_state.py
  snapshot.py
  locking.py
  workspace_gate.py
  gc.py
  publish.py
```

The Executor may choose a smaller equivalent decomposition if individual modules remain understandable and the repository code-health constraints remain satisfied.

The helper is a **deterministic decision/validation engine**, not a GitHub/Library SDK:

```text
host adapter acquires observations / performs authorized external mutations
        -> deterministic helper validates/classifies/plans
        -> host adapter performs only an explicitly allowed next external mutation
        -> helper validates resulting observations again
```

### Snapshot format

Accept a `.tar.gz` containing one standalone Git repository plus a receipt sidecar or an equivalent deterministic archive layout documented by code/tests.

Safe extraction is mandatory. Python 3.13 stdlib facilities should be preferred; do not add a dependency merely for archive extraction unless a concrete blocker is found and escalated.

### Git execution

Git inspection may use `subprocess` against the local temporary repository. Commands must be read/validation oriented for snapshot checks. Do not use destructive reset/clean to make tests or validation pass.

### External side effects

No production helper path in T058 may:

- call GitHub REST/GraphQL;
- call ChatGPT Library APIs/tools;
- acquire/delete real lock sentinels;
- push/fetch a remote repository;
- delete Library files;
- merge PRs.

Those mechanics remain host-adapter actions governed by D066/D054-equivalent execution boundaries.

## Authorized scope

Executor may create/modify only non-Markdown implementation/test/handoff artifacts necessary for T058, expected primarily under:

- `tools/chatgpt_workspace.py`;
- `tools/_chatgpt_workspace/*.py`;
- `tests/test_chatgpt_workspace*.py` and narrowly related non-Markdown fixtures/helpers;
- `code-health.json` only if required to register legitimate code-health paths/ratchets;
- `handoffs/T058-executor-handoff.json`.

Existing source files outside these paths may be changed only when technically necessary to expose/import the new helper without changing unrelated semantics, and the handoff must explain why.

## Explicit exclusions

Executor MUST NOT:

- edit/create committed Markdown;
- modify Governance Core/protocol semantics;
- add ChatGPT Library/GitHub network integration code;
- add credentials/config secrets;
- add a runtime dependency without Orchestrator re-entry;
- implement automatic retry after stale lock-head classification;
- implement orphan recovery, TTL/heartbeat, ownership transfer, closed-unmerged resume, branch retirement, or quota selector;
- weaken fail-closed classifications to improve convenience;
- alter R014/R015 research artifacts.

## Invariants / constraints

- Python compatibility remains the repository-declared `>=3.13` baseline.
- No new dependency is expected.
- All archive handling is traversal/link safe.
- No validation path may silently repair invalid input.
- A missing field required for a safety decision is ambiguous/blocked, never permissive.
- Local and remote commit SHA equality is not required when exact tree equality plus canonical remote-head receipt is the specified represented-state invariant.
- Error/status enums must remain stable enough for adapter automation and tests.
- Source files remain below normal code-health limits or explicitly justified/ratcheted according to repository policy.

## D065 delegation posture

T058 is `ASSURED` and contains material delegation triggers:

- independent verification of fail-closed behavior;
- noisy/full-suite test execution;
- bounded inspection of archive/Git edge cases;
- root-context protection while the coordinator retains Task Contract/branch/findings synthesis.

The Coordinator MUST evaluate and use delegation for at least one eligible bounded slice unless a concrete safety/capability anti-trigger dominates at runtime.

The Executor retains authority over the concrete child count, roles, decomposition, sequencing and mechanics.

Final handoff must include D065 evidence equivalent to:

```text
delegation_posture
material_triggers_considered
children_used
child_purposes
root_local_reason
```

## Required fail-closed tests

At minimum, deterministic tests SHALL cover:

1. **ownership** — matching owner/work-unit can qualify; mismatched owner blocks;
2. **stale lock HEAD** — expected `H`, observed `H1` yields stale-lock block and no retry/acquisition transition;
3. **wrong worktree** — receipt/topic/work-unit mismatch yields WRITE_BLOCKED before mutation;
4. **corrupt snapshot** — invalid archive/checksum/Git repository fails validation and cannot displace/qualify current state;
5. **release** — exact owner/work-unit/topic/current blob required; wrong blob/owner/missing sentinel cannot release; absent-after-delete verifies RELEASED;
6. **GC post-merge** — positive merged+verified+validated+promoted+revalidated state yields GC_ELIGIBLE;
7. **closed-unmerged retention** — `closed && !merged` is retained;
8. **full snapshot round trip** — a standalone temporary Git repository including `.git` can be archived, extracted safely, pass `git fsck --full`, remain clean, and preserve expected tree/receipt;
9. **publish manifest** — multiple changed paths are represented in one deterministic plan bound to one expected remote HEAD;
10. **unsafe archive** — traversal/unsafe-link member is rejected.

Tests should verify structured status/reason outputs where applicable.

## Acceptance criteria

- **AC-T058-1:** helper architecture implements D066 semantics without network/Library/GitHub mutation dependencies.
- **AC-T058-2:** portable snapshot validation proves checksum, safe extraction, Git fsck, clean status, HEAD/tree and receipt identity.
- **AC-T058-3:** stale lock HEAD fails closed and no helper path automatically retries into ownership.
- **AC-T058-4:** owner/work-unit/topic/wrong-worktree mismatches prevent writable entry.
- **AC-T058-5:** release requires exact current sentinel identity/blob and verifies post-delete absence from supplied observations.
- **AC-T058-6:** GC classifier allows only the qualified post-merge state and retains closed-unmerged/ambiguous/invalid-target state.
- **AC-T058-7:** publication plan supports batched multi-path synchronization bound to an expected remote HEAD without claiming network success.
- **AC-T058-8:** all required fail-closed tests pass with no external network/account dependency.
- **AC-T058-9:** no unresolved R014/R015 gap is silently implemented as solved behavior.
- **AC-T058-10:** full repository quality gate passes and Executor-authored Markdown is absent.
- **AC-T058-11:** D065 delegation evidence is present and consistent with actual execution posture.

## Verification

Minimum final verification:

```text
uv run --locked python -m pytest <focused T058 tests>
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
git diff --check
```

Additionally verify:

- no test requires network access;
- no external credential/config is required;
- submitted branch contains no Executor-authored Markdown changes;
- final changed paths remain inside authorized scope or are individually justified in handoff;
- temporary Git/archive fixtures are created under test temp directories and not persisted as repository residue.

## Code Review & Verify obligations

Executor technical review must specifically inspect:

- archive traversal/symlink safety;
- fail-open defaults caused by missing/unknown fields;
- ownership mismatch paths;
- stale lock/remote-head paths;
- accidental retry/overwrite behavior;
- wrong-worktree acceptance;
- release with stale sentinel/blob identity;
- GC eligibility under partial/ambiguous evidence;
- subprocess error handling and platform portability;
- accidental network/external side effects.

Correct in-authority implementation/test defects and rerun affected verification before handoff.

## Stop / SDD re-entry conditions

Stop and report `BLOCKED`/`PARTIAL` for Orchestrator re-entry if:

- correct implementation requires a GitHub or Library SDK/network integration not described by D066;
- a qualified R014/R015 behavior is internally contradictory when projected into the helper;
- an unresolved gap must be solved for the helper to function;
- a dependency addition becomes materially necessary;
- safe archive extraction cannot be provided on the repository-supported runtime without changing the Design;
- Task Contract semantics require reinterpretation rather than implementation;
- a required test exposes a defect in D066/acceptance meaning rather than an implementation bug.

Do not invent a solution to an upstream semantic gap inside the implementation branch.

## Expected handoff

Persist:

`handoffs/T058-executor-handoff.json`

In addition to repository baseline handoff fields, include:

- mapping from `T058-R1` through `T058-R7` / preserved invariants to implementation and tests;
- structured status vocabulary implemented;
- archive-safety approach;
- explicit statement that production helper performs no GitHub/Library network mutation;
- required fail-closed test results;
- unresolved/open-gap statement confirming no gap was silently closed;
- D065 delegation fields;
- final full-suite/lint/format/diff-check results.

Return only:

```text
STATUS: DONE | BLOCKED
HANDOFF: handoffs/T058-executor-handoff.json
BRANCH: <branch>
HEAD: <pushed-head>
```