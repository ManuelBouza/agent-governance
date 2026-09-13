# Maintainer Orchestrator Route

Use only while ChatGPT Orchestrator owns the active source-maintenance stage. `AGENTS.md` and canonical Git authority control.

## Route by intent

- Research / architecture / Decision work -> load only the current research/Decision artifacts and `docs/RESEARCH-TRACEABILITY.md` when lineage is material.
- Task Contract creation/revision/readiness/launch -> load `TASK-CONTRACT-TEMPLATE-USAGE.md`, `TASK-CONTRACT-V4-TEMPLATE.md`, `docs/TASK-CONTRACTS.md`, and only the controlling specification/Decision references.
- D068 Stage 5 -> load the Task Contract, D068, D052 when semantic oracles are in scope, applicable source workflow, and the exact candidate surfaces to materialize.
- Branch mutation -> apply `docs/BRANCHING.md`, D061/D062 and compose `repository-change-control` when change-path resolution is material.
- Checkpoint/chat turnover -> apply `docs/ORCHESTRATOR-CHECKPOINTS.md`, D027/D067/D080 and compose `durable-work-checkpoint` when a durable resumable frontier is being written or validated.
- Version-sensitive reliance -> apply D077 and compose `upstream-version-revalidation`; persist consequential evidence through the research adapter when material.
- Stage 7 -> verify the remote Executor handoff/final branch, perform semantic convergence/acceptance, then integrate only through authorized PR flow.

## D053 / D068 / D076 boundary

For current D068 source maintenance:

```text
Stages 1-4 -> Orchestrator
Stage 5    -> Orchestrator complete candidate materialization
Stage 6    -> Executor execution/diagnosis/bounded repair/verification
Stage 7    -> Orchestrator convergence/acceptance/integration
```

Stage 5 includes all in-scope Markdown, source, tests, config, schemas, fixtures, scripts, and semantic conformance assets required for first-pass verification. Do not intentionally leave substantial executable qualification/materialization work for Stage 6.

If later execution discovers a material requirement/Design/Plan/acceptance/oracle defect or a D076-material missing executable artifact, re-enter the earliest affected Orchestrator stage before execution continues.

## Source-specific adapters retained here

Agent Governance-specific semantics remain domain-side, including D052/D053/D054/D055/D058/D060/D061/D062/D065/D068/D076/D077/D080, exact Task Contract/checkpoint/research/handoff schemas, `main`/`develop` release policy, source testing/evaluation policy, local toolchain policy, and source-vs-consumer separation.

Transverse Skills never own these semantics.
