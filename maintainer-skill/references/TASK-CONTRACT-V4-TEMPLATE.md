# Source Product Task Contract Template v4

Status: CANONICAL TEMPLATE  
Owner: ChatGPT Orchestrator  
Applies to: new or materially revised source-product Task Contracts  
Policy: `docs/TASK-CONTRACTS.md`

> This template is a structural authority carrier, not a task specification by itself. Replace bracketed placeholders with task-specific durable authority and remove sections that are genuinely not applicable. Do not move task semantics into a chat/terminal launch prompt.

## Identity

- Task ID: `[TNNN]`
- Status: `[DRAFT | BLOCKED | READY | IN_PROGRESS | DONE | ACCEPTED | CANCELLED]`
- Type: `[feature | fix | refactor | test/eval | release | infrastructure | mixed]`
- SDD profile: `[COMPACT | STANDARD | ASSURED]`
- Base branch: `[develop or explicitly authorized base]`
- Expected topic branch: `[branch]`
- Expected executor handoff: `[handoffs/TNNN-executor-handoff.json]`
- Test-Authorship-Mode: `[orchestrator-conformance | executor-implementation | mixed | not-material]`
- Owner: `ChatGPT Orchestrator (specification/Design/Plan/acceptance) / Agente de IA Ejecutor (authorized execution/verification stage) / Human Owner (final authority)`

## Objective

[Concise observable result required from this work unit.]

## Current specification carrier / controlling references

Load only the smallest authoritative set needed to interpret this Task Contract.

- `[specification / Decision / protocol / review / research refs]`
- `AGENTS.md` remains controlling repository policy.

Do not duplicate a complete controlling specification here when a canonical carrier already exists; reference it precisely.

## Requirement / specification delta

### ADDED

- `[REQ-ID] ...`

### MODIFIED

- `[REQ-ID] ...`

### REMOVED

- `[REQ-ID] ...`

### PRESERVED

- `[REQ-ID] ...`

Use only the delta classes that are material. For fixes/refactors, `PRESERVED` is the normal non-regression carrier.

## Controlling Design

Persist or reference the complete implementation-relevant Design needed so the Executor does not have to invent material architecture, interfaces, state/data flow, trust boundaries, failure behavior, compatibility/migration behavior, or acceptance meaning.

[Task-specific Design.]

## Plan & Trace

Define the durable work decomposition and requirement-to-candidate/evidence trace at the level needed for the selected SDD profile.

| Unit | Requirement / Design ref | Candidate artifact(s) | Required verification/evidence |
| --- | --- | --- | --- |
| `[U1]` | `[REQ/Design]` | `[paths]` | `[tests/inspection/eval]` |

## Stage ownership and candidate boundary

For D068-mode source maintenance:

```text
Stages 1-4  Explore / Specify / Design / Plan & Trace
            -> ChatGPT Orchestrator
Stage 5     Complete candidate materialization
            -> ChatGPT Orchestrator
Stage 6     Execute / diagnose / bounded repair / verify
            -> Agente de IA Ejecutor
Stage 7     Converge / accept / integrate / evolve
            -> ChatGPT Orchestrator
```

If D068 does not apply, state the controlling ownership topology explicitly.

## Published candidate freeze

Use this section whenever Stage 6 verifies a published candidate.

```text
candidate_branch: [topic branch]
candidate_head:   [exact SHA]
candidate_base:   [exact protected-base SHA]
```

The Executor MUST establish this exact represented state before executable work. A different initial candidate HEAD requires Orchestrator re-entry unless durable authority explicitly permits otherwise.

If the candidate may receive bounded Stage 6 repairs, state the allowed repair class and evidence requirements below; do not treat the freeze as permission to redesign.

## Authorized scope

The Executor may:

- execute the published/authorized candidate;
- diagnose failures inside the approved specification/Design/Plan;
- make bounded represented technical repairs explicitly permitted by this contract;
- run required technical review and verification;
- persist the authorized non-Markdown handoff/evidence.

Task-specific authorized artifacts/behaviors:

- `[paths / effects / resources]`

## Explicit exclusions

The Executor must not:

- redefine requirements, Design, Plan/Trace, acceptance meaning, frozen semantic oracle meaning, or task decomposition;
- expand product scope outside this Task Contract;
- author/edit committed Markdown unless explicit durable authority says otherwise;
- create substantial executable material during D068 Stage 6 that should have existed in Stage 5, subject to D076;
- use chat history or the transport prompt as substitute task authority;
- `[task-specific exclusions]`.

## Invariants / constraints

- `[architecture / compatibility / ownership / security / reproducibility invariant]`
- `[version/runtime requirement when material]`
- `[branch/worktree/permission constraint]`

For version-sensitive behavior, apply D077 and record the current disposition (`PIN_RETAINED`, `UPGRADE_REQUIRED`, `REQUALIFICATION_REQUIRED`, or `NO_MATERIAL_CHANGE`).

## Executor process autonomy

Inside the authorized Stage 6 envelope, the Executor owns mechanics and private execution organization under D041/D054, including command/API/SDK/shell choices and compatible native tools/workers.

This Task Contract defines **what, bounds, invariants, evidence and stop conditions**. It does not prescribe private executor topology unless that topology is itself material to safety, reproducibility, ownership, or the behavior being evaluated.

## D076 executable-materialization boundary

When D068 applies:

```text
small mechanical execution aid
    -> Stage 6 may create/use it

substantial new controller/harness/script/fixture-oracle implementation
    -> STOP
    -> Orchestrator Stage 5 re-entry
```

Required terminal audit fields when applicable:

```text
ephemeral_artifacts: [...]
executor_material_ephemeral_artifacts: []
```

Any material or uncertain late-discovered executable artifact is a re-entry condition, not a silent temporary workaround.

## Acceptance criteria

- **AC-[TNNN]-1:** `[objective acceptance condition]`
- **AC-[TNNN]-2:** `[non-regression condition]`
- **AC-[TNNN]-3:** `[verification/evidence condition]`

Acceptance criteria must be observable and sufficient for ChatGPT Orchestrator Stage 7 convergence.

## Verification and trace requirements

Required deterministic/property/eval/security/manual inspection evidence:

- `[verification requirement]`
- `[verification requirement]`

For D052 `orchestrator-conformance` or `mixed`, identify exact Orchestrator-owned conformance assets and distinguish them from Executor supplementary technical verification.

Evidence must be sufficient to map material requirements and Design claims to the submitted candidate state.

## Code Review & Verify obligations

Before terminal `DONE`/`COMPLETED`, the Executor must perform technical review against the approved specification/Design/Plan and persist evidence required by `docs/EXECUTOR-HANDOFFS.md`.

Task-specific review obligations:

- `[review obligation]`

## Stop / escalation / SDD re-entry conditions

STOP rather than guess when any of these occurs:

- candidate/base/branch identity cannot be established safely;
- a material requirement, Design, Plan/Trace or acceptance defect/ambiguity is discovered;
- a semantic oracle appears defective;
- a required version/runtime/profile cannot be resolved exactly when exactness is material;
- a D076-material executable artifact is missing from the candidate;
- a bounded repair would change approved semantics or Design;
- a safety/security/permission/reproducibility invariant cannot be satisfied;
- `[task-specific stop condition]`.

Persist available evidence and identify the earliest affected SDD stage before returning control.

## Version-sensitive launch gate

Include only when external version-specific behavior is material.

- pinned/reference version: `[version]`
- current stable reviewed: `[version/date]`
- higher relevant version(s) reviewed: `[versions]`
- disposition: `[PIN_RETAINED | UPGRADE_REQUIRED | REQUALIFICATION_REQUIRED | NO_MATERIAL_CHANGE]`
- launch-time rule: `[what to do if upstream state changes before execution]`

## Expected handoff / evidence

The Executor MUST persist the task result at:

```text
[handoffs/TNNN-executor-handoff.json]
```

Additional authorized telemetry/evidence:

```text
[paths]
```

The handoff must capture at least:

- canonical authority and candidate identity;
- represented Stage 6 repairs;
- verification/review results;
- relevant mutation/permission/runtime evidence;
- stop/block reason when incomplete;
- D076 ephemeral-artifact audit when applicable.

Do not persist private chain-of-thought.

## Terminal return shape

Define a compact machine/human-verifiable terminal return. Default:

```text
STATUS: COMPLETED | BLOCKED
HANDOFF: [handoff path]
BRANCH: [topic branch]
HEAD: <actual remote pushed HEAD>
```

Task-specific additional terminal fields require durable justification in this Task Contract, not ad hoc launch-prompt expansion.

## Human launch gate

State whether the Task Contract is immediately executable or requires a separate Human launch/approval.

```text
launch_state: [NOT_AUTHORIZED | AUTHORIZED_AWAITING_HUMAN_START | IN_PROGRESS]
```

If Human-mediated transport is required, the launch prompt MUST remain thin and point to canonical Git authority. It MUST NOT restate this Task Contract's execution semantics.

## Thin transport invariant

The normal Human-visible Executor prompt is only a transport pointer. A compliant transport contains, at most, the information needed to enter the correct governed context, for example:

```text
Set the visible Codex chat title to exactly:
[Coordinator-ID]

Repository: [canonical repository]
Session: [NEW | CONTINUE]
Task Contract: [docs/tasks/TNNN-....md]
Authorized candidate: [branch]@[SHA]

Synchronize canonical Git authority, load the repository instructions/checkpoint and the Task Contract, then execute that Task Contract exactly. Return only its defined terminal result.
```

D055 launch-profile information is presented to the Human separately unless a concrete adapter requires a minimal transport field. Model/provider names, detailed runbooks, frozen experiment semantics, acceptance criteria, retry logic, exclusions, evidence schemas, and stop rules belong in canonical Git authority, not duplicated in the transport prompt.

If a transport prompt starts carrying substantive task instructions, stop and move those instructions into this Task Contract or another referenced canonical authority before launch.
