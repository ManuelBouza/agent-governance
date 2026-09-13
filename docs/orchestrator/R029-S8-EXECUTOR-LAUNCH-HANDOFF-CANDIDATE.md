# R029-S8 — `executor-launch-handoff` Candidate Evaluation

Status: COMPLETE  
Parent: `R029 — AGENTS.md / Skill Architecture Refactor Research`  
Subtask: `R029-S8 — executor-launch-handoff candidate`  
Baseline-Develop: `102ad237c8736124a2c705d987dbbb7c27ef9c42`  
Inputs: accepted R029-S1 through R029-S7 artifacts; `docs/TASK-CONTRACTS.md`; `docs/EXECUTOR-HANDOFFS.md`; `docs/EXECUTOR-LAUNCH-PROFILES.md`  
Decision-State: EVALUATING  
Normative-Effect: none  
Analytical-Disposition: `KEEP_CANDIDATE`

## Purpose

Evaluate whether executor launch/handoff preparation contains a reusable transverse capability distinct from Agent Governance's Task Contract authority, launch-profile policy, execution-mechanics ownership, coordinator continuity, source-maintenance stage model and repository-specific handoff schema. This artifact evaluates a candidate only; it does not create or adopt a Skill and does not launch an Executor.

## Reusable semantic intent

The reusable intent is:

> Bind a concrete delegated executor/session to one persisted execution authority, establish a fresh and safe execution baseline, transport only the minimum routing information needed to reach that authority, and require a durable return artifact/pointer that lets the delegating agent reconstruct the executor result without treating chat transport as authority.

This intent survives removal of Agent Governance-specific Task IDs, D055 model/effort policy, D060 coordinator naming, D068 stage numbering, `handoffs/TNNN-*.json`, Codex model names and source-product branch conventions.

The capability is not a task-specification generator, an executor methodology, a model router, a shell/Git runbook, or an acceptance authority.

## Positive triggers

Activate/evaluate this capability when:

- a bounded work unit is delegated from one agent/role to another executor/worker;
- the delegated executor must act from persisted authority rather than conversational paraphrase;
- the executor must establish a fresh remote/repository baseline before relying on task state;
- session/adapter identity materially affects safe continuation or Human navigation;
- transport should remain minimal and point to canonical authority instead of duplicating it;
- the executor result must survive session turnover through a durable handoff/evidence artifact;
- the delegating agent must be able to verify the returned branch/state/evidence before semantic acceptance.

## Negative triggers / anti-triggers

Do not activate merely because:

- an agent invokes a local helper tool inside the same execution context;
- the work is ordinary direct execution with no delegation boundary;
- a user asks which model is best without an actual delegated work unit;
- a task needs specification, Design, acceptance criteria or decomposition — those belong to upstream authority, not launch transport;
- a shell/Git/API command must be selected — execution mechanics remain executor/tool-adapter concerns;
- a final result is already durably represented and no new executor launch/handoff is occurring;
- a repository wants a particular Task ID, JSON schema, branch naming rule or coordinator title — those are adapter/domain policy.

## Candidate contract

### Inputs

A portable invocation needs, at minimum:

- the persisted authority locator for the delegated work unit;
- the repository/resource context in which that authority is valid;
- the concrete executor/host adapter selected by the caller or local policy;
- session-continuity state when continuation versus new-session behavior matters;
- the required baseline/freshness source and safe-reconciliation boundary;
- the expected durable return channel/artifact or equivalent completion pointer;
- any explicit stop/fail-closed conditions imposed by the governing domain.

The capability may consume a domain-selected compute/session profile, but it does not originate normative compute policy unless a separate policy explicitly delegates that choice.

### Processing semantics

The reusable flow is:

```text
persisted delegated authority exists
    -> bind concrete executor/adapter and session context
    -> establish/verify safe fresh baseline
    -> load authority from that represented state
    -> transport only routing/minimum execution context
    -> executor acts inside delegated authority using its own mechanics
    -> executor persists terminal/blocked/partial result in the required durable return channel
    -> delegating agent verifies returned durable identity/evidence
    -> semantic acceptance remains with the governing authority
```

### Output / postcondition

Successful preparation/return yields enough durable information to establish:

- which executor/session acted;
- which persisted authority it was supposed to execute;
- which fresh baseline or represented state controlled execution;
- where the authoritative result/handoff is persisted;
- which durable state identifies the returned result;
- whether the result is terminal, partial or blocked;
- whether the caller can safely proceed to its own review/acceptance stage.

Chat text may carry a pointer, but the required persistent artifact/state is the audit surface when the governing domain requires durable evidence.

## Fail-closed boundary

The candidate must stop or return a blocked launch/handoff state when:

- no authoritative delegated work unit can be identified;
- baseline/freshness cannot be established without destructive guessing;
- the requested transport conflicts materially with persisted authority;
- the selected executor/session cannot load or represent the required authority safely;
- the return artifact/state cannot be persisted or verified when durability is required;
- session continuity is ambiguous in a way that could create concurrent conflicting writers.

The capability must not repair missing specification/Design/acceptance authority by inventing it inside the prompt.

## Authority boundary

The candidate MUST NOT:

- create task scope, specification, Design, acceptance criteria or Human approval;
- decide that an Executor result is semantically accepted;
- turn provider/model/session settings into product correctness semantics;
- prescribe executor-private planning, delegation topology, shell commands or implementation methods absent a separate material requirement;
- overwrite repository-local ownership/branch/freshness rules;
- treat a launch prompt or terminal chat message as stronger authority than persisted controlling artifacts;
- silently continue when durable return evidence required by the caller cannot be established.

It is a transport/orchestration capability, not a source of semantic authority.

## Agent Governance adapter boundary

The following remain Agent-Governance-specific domain material and are not part of the portable candidate semantics:

- Task Contract format, fields, `docs/tasks/TNNN-*.md`, D053/D068 stage ownership and D052 oracle ownership;
- D055's exact Human-facing launch card, `NEW|CONTINUE`, model/effort selection policy and current provider mapping;
- D060 task-scoped coordinator lifetime, `AG | <repo> | <work-unit> | root-<n>` identity and failover semantics;
- D058 worktree/coordinator hygiene and repository-specific writable-workspace constraints;
- D042/D043 source-maintenance freshness/instruction-loading policy details;
- D054 ownership of CLI/API/SDK/Git/shell mechanics;
- D048 publication timing and D061/D062 branch protection/freshness rules;
- D068 Stage 5/6 candidate/handoff topology and D076 ephemeral-artifact reporting;
- `handoffs/TNNN-executor-handoff.json` schema, required fields, implementation/review SHA relationships and visible response format;
- current Codex/GPT model names, effort labels and host-specific naming/compaction behavior.

A future Skill, if ever adopted, would need adapters/references for those local policies rather than embedding them as universal semantics.

## Relationship to other R029 candidates

- `repository-change-control` controls authorized repository mutation/integration paths; S8 only transports delegated execution into/out of such a path.
- `durable-work-checkpoint` preserves the orchestrator frontier across sessions; S8 preserves a delegated execution boundary and result pointer.
- `research-evidence-traceability` governs provenance/freshness of consequential evidence; S8 may carry evidence pointers but does not own the evidence lifecycle.
- `upstream-version-revalidation` may influence which executor/runtime is valid, but S8 does not perform version comparison.
- workspace isolation remains intentionally unresolved here; S9 decides whether it belongs under repository change control, executor launch/handoff, or as a separate capability.

## Host-neutral versus host-specific mechanics

One semantic candidate can serve ChatGPT, Codex, other coding agents and non-coding executor hosts when they share the same delegation intent. Host adapters may differ in:

- creating versus continuing sessions;
- model/effort controls;
- naming/renaming/compaction surfaces;
- repository synchronization mechanisms;
- how persisted authority is opened;
- how return artifacts are written and how branch/state identity is reported.

Those mechanics do not justify separate top-level Skills by host identity unless later evidence shows materially different intent or permission boundaries.

## Analytical disposition

`KEEP_CANDIDATE`

Rationale:

1. the delegation/launch/handoff intent is reusable beyond Agent Governance;
2. it has positive and negative triggers distinct from generic prompting or model selection;
3. it has a concrete postcondition centered on persisted authority, fresh baseline and durable return identity;
4. it can fail closed without acquiring upstream semantic authority;
5. repository/project-specific launch cards, Task Contracts, branch policy and handoff schemas separate cleanly into adapters;
6. the same semantic contract can span multiple executor hosts while keeping host mechanics local;
7. final workspace-isolation placement can remain deferred to S9 without weakening this candidate boundary.

`KEEP_CANDIDATE` is an analytical R029 result only. It does not authorize implementation, packaging, installation, root routing changes or normative adoption.

## Completion gate

R029-S8 is complete because:

- reusable launch/handoff semantics are explicit;
- Task Contract/D055/D054/D060/repository-specific authority remains domain-side;
- positive/negative triggers and fail-closed behavior are explicit;
- overlap with S4/S6/S7 and the S9 workspace-isolation question is bounded;
- no Executor was launched and no provider/model call was consumed;
- no root `AGENTS.md` rewrite, Skill implementation, normative adoption or T066 mutation occurred.
