# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O218  
Canonical-Branch: `develop`  
Current-Work-Unit: D067 / D068 — objective-scoped ChatGPT lifecycle plus Library-first candidate materialization / Executor verification boundary  
Chat-Closure: WAITING_FOR_NEXT_OBJECTIVE  
Active-Executor: none  
Active-Executor-Surface: none; T058 is frozen BLOCKED by Human direction

## Durable frontier

- D067 adopts one explicit/verifiable Human objective per ChatGPT Orchestrator chat plus fail-closed successor bootstrap/repair semantics.
- D068 adopts the source-maintenance ChatGPT/Library role boundary:
  - ChatGPT owns Explore / Specify / Design / Plan & Trace / Candidate Materialize;
  - Executor owns Execute / Diagnose / bounded technical Repair / Verify;
  - ChatGPT owns Converge / Accept / Integrate / Evolve.
- D068 is source-product/ChatGPT-adapter specific and does not automatically change Governance Core/consumer SDD.
- D061/D062 remain mandatory: protected `main`/`develop`, verified short-lived topic branch, no routine bypass/direct long-lived writes.
- D066 remains the workspace/transport basis: local Git + optional Library persistent standalone `.git` snapshots, GitHub canonical authority, bounded/final publication checkpoints.
- D060 still controls one Human-visible Executor Coordinator root per exact Task/Operational Contract lifecycle.
- D065 remains controlling generally, with D068 strengthening Stage 6 into coordinator-first delegation for materially separable execution/diagnostic slices.
- R014/R015 remain `COMPLETE / DECIDED -> D066`; original research artifacts remain historical evidence and are not rewritten.
- R007 remains `COMPLETE / DEFERRED`.
- R010 remains `COMPLETE / DEFERRED`.
- Core protocol remains `1.15.0`.

## D067 objective/chat rule

```text
one ChatGPT chat
-> one explicit objective
-> complete/persist/reconcile objective
-> OBJECTIVE_COMPLETE
-> WAITING_FOR_NEXT_OBJECTIVE
-> when Human supplies next objective: generate bootstrap only
-> successor verifies GitHub/Library state
-> mismatch: BOOTSTRAP_MISMATCH back to predecessor
-> verified successor: predecessor RETIRED
```

A completed predecessor chat MUST NOT execute the next material objective.

The successor prompt carries expected identities, but GitHub/persisted state remains authority. A material mismatch blocks successor mutation; the successor reports expected vs observed state and the Human Owner transports that packet to the predecessor for bounded closure repair.

Operating procedure:

`docs/OBJECTIVE-SCOPED-CHAT-HANDOFF.md`

## D068 effective source-maintenance boundary

For new D068-mode source work:

```text
Human objective
-> NEW ChatGPT objective chat
-> bootstrap verification
-> Explore / Specify / Design / Plan
-> D061 topic identity
-> ChatGPT materializes complete candidate in local Git/Library
   (Markdown + code + tests + config + fixtures + docs)
-> bounded candidate publication to GitHub topic branch
   including exact Task Contract/authority
-> NEW/CONTINUE Codex Coordinator for exact Task Contract
-> workers execute tools/tests/lint/build/app/browser/etc. when separable
-> Executor diagnoses and repairs implementation defects inside authority
-> Executor BLOCKS on spec/design/acceptance defects
-> pushed handoff/final candidate
-> ChatGPT re-materializes corrected GitHub state into Library when retained
-> Converge / Accept
-> protected PR / integration
-> canonical Library refresh/validation/GC/lock cleanup as applicable
-> checkpoint / D067 closure
```

Codex MUST NOT execute against authority that exists only in chat/Library. The coherent Task Contract + candidate checkpoint must be remotely represented on the verified topic branch before Stage 6.

Operating procedure:

`docs/LIBRARY-FIRST-SOURCE-MAINTENANCE.md`

## Executor coordinator rule under D068

The Human-visible root is coordinator-first. It retains contract/branch/repair envelope/synthesis/handoff and delegates materially separable execution/noise-heavy slices when a compatible worker surface is available and no safety/ownership anti-trigger dominates.

Examples of worker-eligible execution:

- focused/full tests;
- lint/format/static checks;
- uv/package/build/environment diagnostics;
- app/CLI execution;
- Playwright/browser validation;
- Computer Use or other host-native interactive validation when supported;
- plugin/MCP-backed operations;
- logs/traces;
- independent review/diagnosis;
- bounded repairs with explicit safe writable ownership.

A single ceremonial worker is insufficient when several material separable execution slices exist and compatible workers are available.

## T058 frozen state

T058 is **not resumed, accepted, merged, migrated, or cleaned up** by D067/D068 adoption.

Grandfathered execution state:

```text
Task: docs/tasks/T058-chatgpt-portable-workspace-adapter.md
Status: BLOCKED / FROZEN_BY_HUMAN
Branch: feat/t058-chatgpt-portable-workspace-adapter
Remote HEAD: 6ed319a1802cfd90d50d9dc95d969435c295a164
Implementation/review anchor: 00134357e77f46d9cfcf82b03cedca3f386688f5
Handoff: handoffs/T058-executor-handoff.json at the frozen branch/head
Coordinator: AG | agent-governance | T058 | root-1
Coordinator state: dormant/frozen, not retired and not active
```

Known blocker from the durable handoff:

- T058 focused tests passed (`26 passed`), Ruff/code-health/diff checks passed;
- repository full suite returned `515 passed, 2 failed`;
- both failures reproduced on untouched `develop@2b2c1c0fa7946d8b6f65d55d6755ebe6bcddb29a` and were classified outside T058 authority.

Do not fix those failures, resume T058, open its implementation PR, merge it, or retire its branch/worktree unless the Human Owner explicitly makes that a later objective.

If T058 is ever resumed, explicitly decide whether to continue its grandfathered contract or persist a same-task revision under current D068 authority. No silent migration.

## Legacy source-document precedence

`AGENTS.md`, `docs/DEVELOPMENT-WORKFLOW.md`, `docs/TASK-CONTRACTS.md`, `docs/EXECUTOR-HANDOFFS.md`, and `docs/ORCHESTRATOR-CHECKPOINTS.md` contain pre-D067/D068 wording.

On direct conflict for new D068-mode source-maintenance work:

```text
D067 / D068
> older conflicting source-workflow wording
```

Do not reinterpret old wording to undo these accepted decisions. Mechanical normalization of those documents may be done only as an explicitly authorized objective; it is not automatically inferred as the next task.

## Current operating state

The D067/D068 adoption objective is complete once its reviewed topic branch is integrated into protected `develop`.

After integration this chat is parked at:

`WAITING_FOR_NEXT_OBJECTIVE`

No backlog item is implied.

If the Human Owner provides a new material objective in this completed chat, do **not** execute it here. Generate the D067 successor bootstrap containing that exact objective and the current verified repository state.

## Next action

Wait for explicit Human Owner next objective.

When supplied:

1. refresh current `develop` and this checkpoint;
2. verify no unclosed discrepancy belongs to this objective;
3. generate a D067 bootstrap prompt for a NEW ChatGPT chat;
4. include exact next objective, expected canonical HEAD/checkpoint, retained T058 state if still relevant, and minimum controlling references;
5. instruct successor to stop with `BOOTSTRAP_MISMATCH` on material discrepancy;
6. do not execute the successor objective in this predecessor chat.

## Next chat minimum load

A successor objective chat SHALL load:

1. current `develop` identity;
2. current `AGENTS.md`;
3. this checkpoint;
4. `docs/decisions/D067-objective-scoped-orchestrator-chat-lifecycle.md`;
5. `docs/decisions/D068-library-first-candidate-materialization-executor-verification-boundary.md`;
6. only additional references required by its exact objective.

When D068 Library mode is required, also load `docs/LIBRARY-FIRST-SOURCE-MAINTENANCE.md` and validate the exact retained Library state before writable resume.

## Do not

Do not resume or integrate T058. Do not fix its baseline failures. Do not infer R007/R010/MG1 or documentation normalization as next work. Do not start a new material objective in this chat after D067/D068 integration. Do not let Codex execute against chat-only/Library-only authority. Do not weaken D061/D062/D066 fail-closed controls. Do not treat a stale Library candidate as accepted after Executor repairs.
