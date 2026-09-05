# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O220  
Canonical-Branch: `develop`  
Current-Work-Unit: closure repair — fully offline/self-contained Transfer Bundle delivery  
Chat-Closure: WAITING_FOR_NEXT_OBJECTIVE  
Active-Executor: none  
Active-Executor-Surface: none; T058 remains frozen BLOCKED by Human direction

## Durable frontier

- O219/PR #303 integrated the source-side Transfer Bundle.
- Human Owner then identified a material portability defect: the generated target bootstrap still assumed the target-adoption chat could read `ManuelBouza/agent-governance`.
- This closure repair removes that dependency.
- The bundle now defines an OFFLINE / SELF-CONTAINED delivery mode through:
  - `docs/transfer/source-maintenance-operating-model/OFFLINE-START-HERE.md`
  - `docs/transfer/source-maintenance-operating-model/OFFLINE-EXPORT-MANIFEST.md`
  - source-independent `TARGET-ADOPTION-BOOTSTRAP-TEMPLATE.md`
- A target-adoption chat may operate from the exported package plus target repository state only.
- Source access is optional provenance revalidation, never a target-bootstrap prerequisite.
- The offline package must include portable core files, evidence/gaps, selected exact source-reference snapshots, `EXPORT-RECEIPT.txt`, and `SHA256SUMS.txt`.
- Source-reference material remains provenance/evidence, not target authority.
- T058 remains `BLOCKED / FROZEN_BY_HUMAN`, branch `feat/t058-chatgpt-portable-workspace-adapter`, HEAD `6ed319a1802cfd90d50d9dc95d969435c295a164`, implementation/review anchor `00134357e77f46d9cfcf82b03cedca3f386688f5`, classification `DO_NOT_COPY`.
- No target repository has been modified.

## Portable operating-model closure

The exported package carries, without live source lookup:

- objective-scoped Orchestrator lifecycle and mismatch semantics;
- SDD/single-owner role boundaries and delta-first specification;
- semantic oracle/test ownership;
- Executor process autonomy and operation resolution;
- effect/target execution authorization and runbook separation;
- branch-target fail-closed controls and server-side branch protection;
- task-scoped Executor coordinator continuity and semantic delegation;
- writable workspace/worktree isolation;
- local Git / persistent snapshot / canonical provider separation;
- cross-chat lock branch + expected-head CAS + owner sentinel;
- snapshot validation, freshness, publication, resynchronization and GC;
- Execute/Diagnose/bounded Repair/Verify authority boundary;
- research/evidence-to-decision separation;
- unresolved gaps and explicit non-claims.

## Next action

Wait for an explicit Human Owner next objective.

For target adoption, the Human may take the generated offline archive into the other project. The successor chat should read `OFFLINE-START-HERE.md` and the package-local bootstrap, then inspect the target repository. It must not require access to this source repository.

## Next chat minimum load for target adoption

1. the complete exported Transfer Bundle available locally/in the target project;
2. `OFFLINE-START-HERE.md`;
3. package `EXPORT-RECEIPT.txt` + `SHA256SUMS.txt`;
4. portable operating model, manifest, gaps, checklist and evidence appendix;
5. target canonical repository identity;
6. target governing instructions and current frontier/state carrier;
7. source-reference material only if needed to resolve a concrete ambiguity/audit question.

## Do not

Do not require the target project to access `ManuelBouza/agent-governance`. Do not resume/integrate/clean up T058. Do not copy its implementation. Do not copy source `AGENTS.md` wholesale. Do not promote research to target authority. Do not infer target branch topology/provider/model/Library behavior. Do not weaken stronger compatible target controls.
