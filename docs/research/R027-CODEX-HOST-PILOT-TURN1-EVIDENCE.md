# R027 — Codex host pilot Turn 1 evidence

Research-ID: R027  
Status: EMPIRICAL PILOT EVIDENCE — TURN 1 COMPLETE / TURN 2 AUTHORIZABLE  
Date: 2026-09-12  
Work unit: `R027-PILOT-1`  
Repository: `ManuelBouza/test_biblioteca`  
Coordinator: `AG | test_biblioteca | R027-PILOT-1 | root-1`  
Pilot protocol: `docs/research/R027-CODEX-HOST-PILOT-PROTOCOL.md`  
Launch authority: `docs/research/R027-CODEX-HOST-PILOT-LAUNCH-AUTHORITY.md`  
Normative change: none

## Executor return

Codex returned:

```text
STATUS: LOCAL_READY
BASE_SHA: 56a72cf847663c6af47e718fc52373072bf840a4
BRANCH: test/r027-codex-host-pilot-1
LOCAL_HEAD: 23a15db763c57ce1eab095de6c7186c94deb4d17
WORKTREE: C:\Manuel\Projects\Test\test_biblioteca-r027-pilot-1
G0_RESULT: PASS — canonical main synchronized; clean exclusive worktree; no unexplained local work.
REMOTE_TOPIC_PRESENT: no
TEST_RESULT: PASS — intentional 9 != 5 failure observed, diagnosed, repaired, and unittest passed.
RUNTIME_ARTIFACTS: r027_pilot_1/library_math.py; r027_pilot_1/test_library_math.py; generated __pycache__ removed.
NOTES: Created one local commit and amended it once. Worktree is clean and ahead of origin/main by one commit. Nothing pushed; no remote topic created.
```

## Independent remote verification

Immediately after the return, the Orchestrator queried canonical GitHub state directly.

Observed:

```text
ManuelBouza/test_biblioteca main
= 56a72cf847663c6af47e718fc52373072bf840a4

remote branch search:
test/r027-codex-host-pilot-1
= ABSENT
```

These facts independently confirm the two remote-state claims material to Turn 1:

1. the reported `BASE_SHA` equals current canonical `main`;
2. the topic branch remained unpublished throughout the completed Turn 1 boundary.

The local-only HEAD `23a15db763c57ce1eab095de6c7186c94deb4d17`, worktree cleanliness, amend behavior and local test/diagnosis sequence are not yet independently visible from GitHub. Turn 2 G1 publication is expected to make the represented local ancestry auditable remotely.

## Turn 1 acceptance assessment

| Property | Current evidence | Result |
| --- | --- | --- |
| current canonical base established | Codex return + direct GitHub main ref | PASS |
| exact pilot topic/worktree reported | Codex return | PASS, host-reported |
| no unexplained local work | Codex return | PASS, host-reported |
| remote topic absent through Turn 1 | direct GitHub branch search | PASS |
| intentional failing test observed/diagnosed/repaired | Codex return | PASS, host-reported |
| local commit created and amended | Codex return | PASS, host-reported; ancestry confirmation pending G1 |
| verification-affecting generated residue noticed | `__pycache__` reported and removed | PASS |
| no per-command full-G0 loop | complete transcript not available to Orchestrator | PENDING CORROBORATION |

The `RUNTIME_ARTIFACTS` return mixes tracked pilot source/test paths with generated runtime residue. This is not treated as a gate failure because the material runtime item, `__pycache__`, was explicitly recognized and removed. The final Turn 2 handoff should distinguish implementation/test files from generated/ephemeral runtime artifacts more precisely.

## Authority/freshness revalidation before Turn 2

During Turn 1 review, canonical `agent-governance` `develop` had advanced to:

`5aab6f16490c76c6ca711349fe6f500c8d641c17`

Current checkpoint is O284 for T065 Stage 5. Its `No Executor is authorized` boundary applies to the active T065 scientific work unit; R027-PILOT-1 remains a separately Human-authorized disposable research work unit in `test_biblioteca` and does not touch T065/T062 scientific branches or provider-call accounting.

OpenAI Codex upstream was revalidated under D077 immediately before Turn 2 authorization:

```text
latest stable: 0.154.0
latest observed prerelease: 0.155.0-alpha.3.9
R027 disposition: NO_MATERIAL_CHANGE
```

A new stable release has not appeared. The actual host/app/CLI runtime observed by Codex must still be persisted in the Turn 2 handoff. A material host/runtime mismatch remains `VERSION_SURFACE_GAP`, not silent qualification extension.

## Turn 2 disposition

Turn 1 remote/Git boundary is sufficiently verified to authorize the persisted protocol's Turn 2 `CONTINUE + G0 re-entry + G1` step.

The unresolved behavioral criterion `no per-command full-G0 loop` is carried forward rather than falsely marked PASS. Turn 2 must persist actual G0 revalidation events and reasons. Final pilot acceptance still requires corroborating that G0 was event-triggered rather than command-triggered.

No G1 publication has yet been observed or accepted by the Orchestrator at the time of this record.
