# Offline Export Manifest

Status: PORTABLE DELIVERY MANIFEST

This manifest defines the material that must be exported so a target project can adopt the operating model without any live access to the source repository.

## A. Portable adoption core

These files are the primary target-adoption inputs:

- `OFFLINE-START-HERE.md` — `PORTABLE`
- `README.md` — `PORTABLE`
- `PORTABLE-OPERATING-MODEL.md` — `PORTABLE`
- `PORTABILITY-MANIFEST.md` — `PORTABLE`
- `EVIDENCE-APPENDIX.md` — `EVIDENCE_ONLY`
- `UNRESOLVED-GAPS.md` — `PORTABLE`
- `TARGET-ADOPTION-CHECKLIST.md` — `ADAPT_REQUIRED`
- `TARGET-ADOPTION-BOOTSTRAP-TEMPLATE.md` — `ADAPT_REQUIRED`
- `OFFLINE-EXPORT-MANIFEST.md` — `PORTABLE`

## B. Offline source-reference set

The generated archive should also carry exact source snapshots under `source-reference/`. These are **not target authority**. Their only purpose is audit, provenance, conflict resolution and implementation clarification when the target cannot open the source repository.

### Repository/source policy — `SOURCE_ONLY`

- `AGENTS.md`
- `docs/DEVELOPMENT-WORKFLOW.md`
- `docs/TASK-CONTRACTS.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `docs/ORCHESTRATOR-CHECKPOINTS.md`
- `docs/EXECUTOR-SESSION-WORKTREE-HYGIENE.md`
- `docs/EXECUTOR-LAUNCH-PROFILES.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/LONG-LIVED-BRANCH-PROTECTION-RUNBOOK.md`
- `docs/LIBRARY-FIRST-SOURCE-MAINTENANCE.md`
- `docs/OBJECTIVE-SCOPED-CHAT-HANDOFF.md`
- `docs/RESEARCH-TRACEABILITY.md`
- `docs/SDD-ADOPTION-PLAN.md`
- `governance-core/SDD.md`

### Accepted source decisions — `SOURCE_ONLY`

Include exact snapshots of:

- D022 source-product change procedure
- D026 coexistence/capability reuse semantics
- D027 Orchestrator checkpoints
- D033 execution access control plane
- D034 runbook-first terminal-neutral execution
- D041 Executor process autonomy
- D042 remote baseline freshness
- D052 specification-owned conformance authorship
- D053 native spec-driven development
- D054 Executor-owned operation resolution/runbook recipes
- D055 Executor launch session/compute profile
- D057 research-to-decision traceability
- D058 coordinator session/worktree hygiene
- D060 task-scoped Executor coordinator continuity
- D061 branch-target write guard
- D062 long-lived branch protection bootstrap
- D063 qualified child measurement surface
- D065 semantic Executor delegation obligation
- D066 ChatGPT portable Git workspace/transport
- D067 objective-scoped Orchestrator lifecycle
- D068 Library-first candidate materialization / Executor verification boundary

### Research and experiment evidence — `EVIDENCE_ONLY`

Include exact source snapshots for the evidence lineage used by the portable model, especially:

- persistent Executor coordinator research (R006)
- adaptive subagent compute routing research (R007)
- child observability research (R008)
- child sandbox inheritance research (R009)
- coordinator/worktree hygiene research (R011)
- coordinator delegation policy research (R012)
- task-scoped coordinator continuity research (R013)
- ChatGPT Git workspace/Library/GitHub transport research (R014)
- R014 Library snapshot lifecycle appendix
- ChatGPT Library worktree-simulator research (R015)
- R015 lock lifecycle appendix
- R015 real cross-chat race appendix
- source SDD research used by D053

Research remains evidence even when the source later adopted a related decision.

## C. Explicit exclusions

Do not export as target implementation:

- T058 helper/code/tests or any other frozen/unaccepted implementation;
- source repository secrets or credentials;
- source `.git` history as a target dependency;
- source branch names, model names or paths as mandatory target semantics;
- source `AGENTS.md` as a ready-to-install target policy.

A compact T058 frozen-state notice may be included for audit, but it must remain `DO_NOT_COPY`.

## D. Export receipt

Every generated offline archive should add:

```text
EXPORT-RECEIPT.txt
  source_repository
  source_commit
  extraction_baseline
  package_schema
  generated_at
  t058_state
  t058_head

SHA256SUMS.txt
  SHA-256 for every exported file except the checksum file itself
```

The archive is complete only when the portable core and the declared source-reference set are present or the receipt explicitly records a justified omission.
