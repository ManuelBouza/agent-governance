# R027 — Codex host pilot launch authority

Research-ID: R027  
Status: HUMAN-AUTHORIZED PILOT LAUNCH — NON-NORMATIVE  
Date: 2026-09-12  
Human authorization: explicit `Go` received 2026-09-12T07:48:39Z  
Pilot protocol: `docs/research/R027-CODEX-HOST-PILOT-PROTOCOL.md`  
Candidate contract: `docs/research/R027-POST-E2E-CANDIDATE-GATE-CONTRACT.md`  
Execution repository: `ManuelBouza/test_biblioteca`  
Work unit: `R027-PILOT-1`  
Expected topic branch: `test/r027-codex-host-pilot-1`  
Normative change: none

## Authorization boundary

The Human explicitly authorizes launching the bounded R027 Codex-host behavioral pilot defined by the persisted protocol.

This authorization does not:

- authorize any T062/T023 provider/model execution;
- modify or consume T062 scientific evidence or call accounting;
- authorize writes to `agent-governance` `develop`, `main`, or the T062 scientific branch;
- authorize force-push or destructive cleanup of unknown work;
- adopt G0/LOCAL/G1/G2 as normative product policy;
- authorize implementation of a new Git-control subsystem.

The pilot remains isolated to `ManuelBouza/test_biblioteca` and must follow the persisted four-turn protocol and exact stop/review conditions.

## Canonical source snapshot

Immediately before launch preparation:

```text
agent-governance develop = d458e4e9ae0d932237c867c22b6a2b50294e6df8
checkpoint                = O281
T062 launch state          = AUTHORIZED_AWAITING_HUMAN_CODEX_START
T062 provider/model calls  = 0
R027 pilot relationship    = parallel / isolated; does not supersede O281
```

O281 remains the canonical Agent Governance frontier for T062. This R027 pilot is a separate disposable research work unit in another repository.

## D077 launch revalidation

Official upstream Codex release state was refreshed immediately before this launch authority was persisted.

Observed upstream state:

```text
latest stable Codex CLI = 0.154.0
higher prerelease seen  = 0.155.0-alpha.3.8
```

Disposition for this pilot: `NO_MATERIAL_CHANGE`.

Reason: the stable baseline remains `0.154.0`, matching the already prepared R027 protocol snapshot. The higher `0.155.0-alpha.*` line remains prerelease evidence and does not by itself change pilot authority. The pilot must record the actual Codex app/CLI/runtime version exposed by the host; any material mismatch or newer stable release discovered at execution becomes `VERSION_SURFACE_GAP` / D077 re-entry evidence rather than silently extending qualification.

## Launch profile

```text
Executor: Codex
Session: NEW
Coordinator-ID: AG | test_biblioteca | R027-PILOT-1 | root-1
Host: native Windows / Codex Local
Model: GPT-5.6 Sol
Effort: Medium
```

The first launched turn is Section 6 (`Turn 1 — G0 + LOCAL autonomy, no publication`) of the persisted pilot protocol.

## Stop condition after Turn 1

Codex must stop after the repaired state is committed locally and verification passes. The topic branch must not be published remotely during Turn 1.

The Orchestrator will evaluate the returned fields and canonical GitHub state before authorizing Turn 2.
