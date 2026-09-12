# R027 — Codex host pilot run evidence

Research-ID: R027  
Status: IN PROGRESS — TURNS 1-2 + REVIEW/MERGE BARRIER COMPLETE  
Date: 2026-09-12  
Execution repository: `ManuelBouza/test_biblioteca`  
Work unit: `R027-PILOT-1`  
Topic branch: `test/r027-codex-host-pilot-1`  
Normative change: none

## Turn 1 — G0 + LOCAL

Codex returned `LOCAL_READY`.

Reported/local identities:

```text
base              56a72cf847663c6af47e718fc52373072bf840a4
local HEAD         23a15db763c57ce1eab095de6c7186c94deb4d17
worktree           C:\Manuel\Projects\Test\test_biblioteca-r027-pilot-1
remote topic       absent
```

Behavioral result:

- canonical `main` refreshed before mutation;
- exclusive clean pilot worktree established;
- intentional failing unittest observed and diagnosed;
- source repaired and test passed;
- one local commit created and amended while unpublished;
- generated Python `__pycache__` classified and removed;
- no remote topic publication in Turn 1.

Independent GitHub verification confirmed canonical `main` was exactly `56a72cf847663c6af47e718fc52373072bf840a4` and no `test/r027-codex-host-pilot-1` branch existed remotely.

## Turn 2 — CONTINUE revalidation + G1

Codex returned `G1_PUBLISHED`.

```text
implementation HEAD   23a15db763c57ce1eab095de6c7186c94deb4d17
final published HEAD  ba5b002bfea3d36feb92739a59ca5cc994eb5907
remote HEAD           ba5b002bfea3d36feb92739a59ca5cc994eb5907
handoff               r027_codex_host/handoff.json
publication           normal non-force
```

Independent GitHub comparison established:

- `ba5b002...` is exactly 2 commits ahead of the original `main@56a72cf...`;
- changed paths are exactly:
  - `r027_pilot_1/library_math.py`
  - `r027_pilot_1/test_library_math.py`
  - `r027_codex_host/handoff.json`
- `23a15db...` is exactly one ancestor commit below `ba5b002...`;
- that final commit adds only the persisted handoff;
- the canonical remote topic ref resolves exactly to `ba5b002...`.

The remote handoff is parseable and records:

```text
G0 revalidation events:
  1. initial entry -> PASS
  2. CONTINUE re-entry -> PASS
additional material G0 triggers: []
```

This supports the candidate behavior that ordinary LOCAL operations do not create a per-command full-G0 loop while `CONTINUE` does create a re-entry revalidation event.

The handoff also records passing final unittest verification, no verification-affecting residue, and normal non-force publication.

## Host observability finding

The persisted handoff records:

```text
executor_host      Codex desktop
model              GPT-5
reasoning_effort   not exposed to the executor runtime
Git                2.53.0.windows.2
Python             3.14.0
PowerShell         7.6.5
OS                 Microsoft Windows NT 10.0.26200.0
```

The Human-facing launch profile requested `GPT-5.6 Sol / Medium`, but the Executor runtime did not expose that exact UI profile and instead self-reported the coarser label `GPT-5` plus no reasoning-effort introspection.

Classification at this barrier: **HOST_ADAPTER_GAP candidate — profile observability only**.

This does not invalidate the Git transaction semantics observed in Turns 1-2. It does mean R027 must not claim that the Executor independently attested the exact Human-selected UI model/effort. Final pilot disposition should retain this adapter-observability caveat unless stronger host evidence is captured.

## Review / integration barrier

Orchestrator review bound integration to exact G1 head:

```text
PR                ManuelBouza/test_biblioteca#6
reviewed head     ba5b002bfea3d36feb92739a59ca5cc994eb5907
base before merge 56a72cf847663c6af47e718fc52373072bf840a4
changed files     3
```

GitHub recalculated the PR as mergeable and the Orchestrator merged using `expected_head_sha=ba5b002bfea3d36feb92739a59ca5cc994eb5907`.

Integration result:

```text
merge SHA         e9b169780d0f23c3ceefbcc4a2e65ddf6738aac2
main after merge  e9b169780d0f23c3ceefbcc4a2e65ddf6738aac2
source remote HEAD ba5b002bfea3d36feb92739a59ca5cc994eb5907
```

The source branch therefore remains frozen at the exact reviewed head for the Turn-3 G2 negative case.

## Current pilot state

```text
Turn 1 G0 + LOCAL                  PASS
Turn 1 no early publication       PASS
Turn 2 CONTINUE revalidation      PASS
Turn 2 G1 exact publication       PASS
per-command G0-loop avoidance     SUPPORTED by persisted event list
exact review identity             PASS
merge at expected reviewed head   PASS
profile observability             HOST_ADAPTER_GAP candidate
Turn 3 G2 unique-commit block     NOT YET RUN
Turn 4 authorized close           NOT YET RUN
normative adoption                NONE
```

Next action: same Codex coordinator `CONTINUE` for the protocol Turn 3. It must create exactly one known synthetic local-only commit above the reviewed head, keep the worktree otherwise clean, then classify G2 as `REVIEW` without deleting the remote branch, local branch/worktree, or synthetic commit.