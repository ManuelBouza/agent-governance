# R029-S9 — Workspace-isolation Placement

Status: COMPLETE  
Parent: `R029 — AGENTS.md / Skill Architecture Refactor Research`  
Subtask: `R029-S9 — Workspace-isolation placement`  
Baseline-Develop: `54b7350b49d6b412e1a9e8395f8f8358140b72d6`  
Inputs: accepted R029-S4 and R029-S8 artifacts; D058; `docs/EXECUTOR-SESSION-WORKTREE-HYGIENE.md`  
Decision-State: EVALUATING  
Normative-Effect: none  
Analytical-Disposition: `INTERNAL_ROUTE`  
Placement: `executor-launch-handoff` internal route/reference, with `repository-change-control` as the repository-policy dependency for branch/base/integration semantics

## Purpose

Resolve the deferred R029 question of whether workspace isolation should become a standalone transverse capability, remain Agent-Governance-specific, or be placed under an existing transverse candidate.

This artifact evaluates placement only. It does not create a Skill, change D058, rewrite repository policy, launch an Executor, or adopt the R029 candidate architecture.

## Distinguishing semantic intent

The reusable workspace-isolation intent is:

> Before delegated writable execution, bind one work unit to one exclusive writable workspace and detect ambiguous or conflicting local state before mutation; preserve that attribution through continuation and retire the workspace safely only after its review/integration lifecycle no longer requires it.

The important semantic center is not generic Git worktree management. It is safe writable-execution attribution across a delegated executor lifecycle.

## Trigger analysis

Workspace isolation is materially triggered when:

- delegated work will mutate a repository or equivalent shared writable resource;
- more than one work unit, coordinator, or execution context may coexist;
- the selected writable surface must be attributable to exactly one active work unit;
- continuation must reuse the represented workspace rather than create conflicting mutable state;
- ambiguous, unique, unrepresented, or unknown-owner local state could collide with the delegated task;
- terminal/integrated work requires safe retirement of its local execution surface without destroying unrepresented work.

It is not independently triggered merely by:

- ordinary repository mutation when there is only one already-safe workspace;
- read-only inspection that cannot interfere with writable work;
- generic questions about `git worktree` commands;
- branch naming or PR target selection alone;
- local scratch directories outside a governed delegated execution path;
- a request to clean old workspaces without durable ownership/evidence semantics.

## Placement alternatives evaluated

### 1. Standalone transverse candidate — rejected

Workspace isolation has reusable semantics, but its activation is normally subordinate to a broader delegated-execution or repository-mutation workflow. Promoting it to a top-level Skill would create a narrow routing surface whose trigger is usually discovered only after `executor-launch-handoff` or repository change preparation is already active.

It also has no independent acceptance authority and would require substantial context from adjacent capabilities: work-unit identity, session/continuation state, repository branch policy, current baseline and completion/integration state.

A standalone Skill would therefore increase routing and context overhead without a distinct enough top-level user intent.

### 2. `repository-change-control` internal route — partially applicable but not primary

S4 owns the authorized repository mutation path: base, topic branch, integration target, protection and durable branch/ref provenance.

Workspace isolation depends on those repository-policy facts, particularly branch identity and cleanup/integration state. However, S4 intentionally distinguishes tracked mutation topology from workspace/coordinator lifecycle.

The central workspace question is not "which branch may mutate?" but "which delegated execution context exclusively owns this writable surface, and can that ownership safely continue or retire?"

Therefore `repository-change-control` is a dependency/reference, not the primary placement.

### 3. `executor-launch-handoff` internal route — selected

S8 already owns:

- binding a concrete executor/session to persisted work authority;
- safe fresh-baseline establishment;
- continuation versus new-session context;
- fail-closed ambiguity that could create conflicting writers;
- durable return identity/evidence.

Workspace isolation is a natural subordinate route of that lifecycle:

```text
executor-launch-handoff
    -> resolve persisted delegated authority
    -> bind executor/session
    -> workspace-isolation route
         -> classify writable topology
         -> select/reuse exclusive workspace
         -> block ambiguous/conflicting ownership
    -> establish fresh represented baseline
    -> delegated execution
    -> durable return
    -> retain workspace through review/integration
    -> safe retirement through repository-policy/cleanup reference
```

This placement keeps the top-level Skill trigger narrow and avoids creating a generic worktree Skill.

## Portable internal-route contract

### Inputs

The workspace-isolation route needs:

- delegated work-unit identity;
- selected executor/session or execution context;
- repository/resource identity;
- requested writable branch/resource identity when applicable;
- accessible workspace/topology inventory sufficient to detect collision;
- repository-local policy pointer for branch/base/cleanup semantics;
- continuation/retirement state from the enclosing launch/handoff lifecycle.

### Processing semantics

The route should:

1. determine whether writable isolation is required;
2. inventory relevant existing writable surfaces without treating age/name as deletion authority;
3. establish whether the requested work unit already owns a valid represented workspace;
4. reuse that workspace for safe same-work-unit continuation;
5. otherwise allocate/select an exclusive workspace only when no conflicting ownership or ambiguous state exists;
6. fail closed rather than reset/clean/delete unrepresented or unknown-owner state;
7. keep the workspace attributable through execution and review;
8. at retirement, defer branch/integration safety to repository change-control/local cleanup policy and remove only evidence-safe obsolete surfaces.

### Postcondition

Before writable execution:

- one active writable work unit maps to one exclusive writable surface;
- no concurrent conflicting writer owns the same workspace/branch/resource;
- represented authority, workspace and writable target agree;
- ambiguous/unrepresented state is preserved and reported rather than destroyed.

At retirement:

- the workspace is removed only after its governing review/integration lifecycle permits retirement;
- remaining surfaces are attributable, explicitly retained, or explicitly blocked/review-required;
- no cleanup operation is interpreted as permission to discard unique state.

## Authority boundary

The route may verify attribution, isolation and collision safety. It must not:

- create mutation authority;
- choose repository branch/release policy independently;
- redefine Task Contract scope or Executor permissions;
- decide semantic acceptance;
- delete ambiguous/unique state merely to achieve a clean topology;
- prescribe host-specific Git commands as semantic requirements;
- infer ownership from workspace names or host chat titles alone.

Repository-local change policy remains authoritative for branch/base/integration and retirement rules. Executor mechanics remain host/adapter-owned.

## Agent Governance adapter boundary

Agent Governance retains:

- D058 exact coordinator/worktree invariant;
- D060 coordinator-root lifecycle;
- D042/D043 freshness and instruction-loading details;
- `one writable work unit -> one topic branch -> one exclusive worktree` as current source-maintenance policy;
- exact `Coordinator-ID` and handoff fields;
- primary-checkout `develop` convergence rule;
- ACTIVE/RETAIN/REVIEW/DELETE classification vocabulary;
- branch-cleanup and post-integration sequencing;
- D054 ownership of Git/worktree command mechanics;
- Operational Contract rules for cleanup operations.

Those are project-specific adapters/references, not universal workspace-isolation semantics.

## Relationship to `repository-change-control`

The selected placement does not duplicate S4.

`repository-change-control` answers:

> What authorized repository mutation path, branch/base/target and review/integration route may be used?

The workspace-isolation route answers:

> Which writable execution surface exclusively represents this delegated work unit, and is it safe to use/continue/retire without collision or destructive guessing?

For repository-backed execution, workspace isolation consumes S4/local repository policy facts. At retirement, it calls/references repository change-control/cleanup semantics rather than owning integration policy itself.

## Relationship to `executor-launch-handoff`

Workspace isolation is part of launch readiness and continuation safety, not a peer top-level intent.

A delegated executor cannot safely begin writable work until authority, session identity, baseline and writable surface all identify coherent represented work. Likewise, a handoff lifecycle may need the workspace to remain alive through review/rework and to retire it only after integration/closure.

That shared lifecycle makes `executor-launch-handoff` the narrowest coherent parent capability.

## Host-neutrality

The internal route is host-neutral. A host may implement isolation through Git worktrees, separate clones/checkouts, sandbox directories, cloud workspaces or another compatible exclusive writable surface.

The semantic requirement is exclusive attributable writable state and fail-closed collision handling, not `git worktree` specifically.

## Analytical disposition

`INTERNAL_ROUTE`

Final placement:

```text
executor-launch-handoff
    -> workspace-isolation internal route/reference
         -> consumes repository-change-control/local repository policy for branch/base/integration/retirement constraints
```

Rationale:

1. workspace isolation is reusable but normally subordinate to a delegated writable-execution lifecycle;
2. its strongest trigger is executor/work-unit/workspace attribution rather than generic repository mutation;
3. S8 already contains the necessary authority/session/freshness/return context;
4. S4 remains the correct dependency for branch/base/integration and cleanup policy;
5. a standalone top-level Skill would add routing/context overhead without a sufficiently distinct independent intent;
6. keeping host-specific workspace mechanics in adapters preserves portability.

`INTERNAL_ROUTE` means retain this semantic route for S10 topology synthesis under `executor-launch-handoff`; it does not authorize implementation or normative adoption.

## Completion assessment

S9 completion gate is satisfied:

- all four placement classes were considered;
- workspace isolation has an explicit reusable intent and trigger boundary;
- its relation to S4 and S8 is explicit;
- standalone Skill promotion is rejected with an anti-sprawl rationale;
- Agent Governance-specific D058/D060/worktree policy remains domain-side;
- final disposition is `INTERNAL_ROUTE` under `executor-launch-handoff`, with `repository-change-control` as policy dependency;
- no root rewrite, Skill implementation, Executor/provider/model call, normative adoption or T066 mutation occurred.
