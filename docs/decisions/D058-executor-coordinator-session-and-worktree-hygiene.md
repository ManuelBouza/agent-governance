# D058 — Executor Coordinator Session and Worktree Hygiene

Status: ACCEPTED  
Date: 2026-09-05  
Authority: Human Owner / ChatGPT Orchestrator  
Research: `docs/research/CODEX-COORDINATOR-IDENTITY-WORKTREE-HYGIENE-RESEARCH.md` (`R011`)  
Refines: D042, D055, `docs/BRANCHING.md`, `docs/BRANCH-CLEANUP.md`  
Preserves: D041 executor process autonomy, D053 stage ownership, D054 execution-mechanics ownership, persisted Git authority

## Problem

The source-maintenance workflow already separates authoritative Git state from Executor chat context and already retires merged topic branches. Two local execution concerns remained implicit:

1. multiple Human-visible Executor coordinator chats can exist for the same repository, making it unclear which chat represents which work unit or which chat should be continued;
2. topic branches can be isolated in worktrees, but the lifecycle did not explicitly require obsolete worktree retirement plus restoration of a clean/current primary checkout after integration.

Those gaps increase the risk of continuing the wrong coordinator context, running two writable tasks in the same directory, leaving orphaned local worktrees/branches, or starting later work from a stale primary checkout.

## Decision

Agent Governance adopts an explicit **Coordinator Session Identity + Workspace Hygiene** invariant for source-maintenance execution.

The operational companion is:

`docs/EXECUTOR-SESSION-WORKTREE-HYGIENE.md`.

### 1. Coordinator session identity

Before every `NEW` launch on an Executor host that supports Human-visible session/thread naming, the Orchestrator SHALL provide a deterministic `Coordinator-Chat` value in the Human-facing launch card.

For the current Codex adapter, use:

```text
AG | <repo> | <work-unit> | root-<n>
```

Example:

```text
AG | agent-governance | T057 | root-1
```

The first Human-visible coordinator for a work unit is `root-1`. Same-work-unit `CONTINUE` keeps the same name. If a fresh session is required for the same work unit, increment the ordinal.

The Human/host applies that name through the supported UI/session naming surface before substantive task execution.

A session name is **navigation metadata only**. It never replaces the Task Contract, Operational Contract, branch, handoff, review, checkpoint, or Git state as authority.

When a supported host surface exposes a stable thread/session ID, the Executor SHOULD persist it as corroborating evidence. If unavailable through a supported surface, record null/unavailable rather than inspecting private persistence merely to obtain it.

### 2. Continuation identity

`CONTINUE` is valid only when all of the following still identify the same represented work:

```text
same work-unit
same represented branch/workspace
same coordinator chat identity
context remains clean/current enough under D055
```

If the Human cannot determine which existing chat satisfies that identity, use `NEW` rather than guessing.

### 3. Concurrent writable worktree isolation

Each concurrently writable Executor work unit SHALL have an exclusive writable workspace.

Normal mapping:

```text
one writable work unit -> one topic branch -> one exclusive worktree
```

Two writable coordinators MUST NOT share the same worktree or topic branch.

The same repository/object database may support multiple concurrent task worktrees. The primary checkout is not a shared scratch surface for parallel implementation work.

Read-only inspection may share repository objects/state only when it cannot mutate or interfere with another work unit and the controlling contract permits it.

### 4. Durable coordinator/workspace identity

Before mutation, a writable Executor must establish which checkout/worktree owns the work unit and verify that no other active writable coordinator owns that same surface.

For D058-governed work that produces a durable handoff or Operational Contract receipt, the evidence SHALL identify:

```text
coordinator_session.name
coordinator_session.mode
workspace.branch
workspace.worktree_label
workspace.isolation
```

When a supported host surface exposes a stable thread/session ID, also persist:

```text
coordinator_session.host_thread_id
```

If that ID is unavailable through a supported surface, record null/unavailable with a reason; do not inspect private persistence merely to obtain it.

A relative/local worktree label is sufficient. Absolute personal workstation paths are not required as canonical project evidence.

### 5. Prelaunch hygiene gate

Before a new writable task begins in an existing local repository, the accessible local topology must be classified sufficiently to avoid collision:

- primary checkout identity/status;
- registered worktrees;
- branches currently checked out by those worktrees;
- current canonical remote base identity;
- stale/obsolete/ambiguous local work that could conflict with the new work unit.

A stale-looking worktree/branch is never deletion authority by itself.

If unrepresented changes, unique commits, an unknown owner, or ambiguous intent exists, preserve the state and classify it for review rather than reset/clean/delete it.

### 6. Post-integration worktree retirement

For an integrated topic work unit, operational closure now requires both the existing branch-retirement evidence and local workspace retirement.

For every accessible worktree associated with a retired topic branch:

1. verify it contains no unrepresented work;
2. remove/retire the obsolete worktree using compatible Git mechanics;
3. retire the local topic branch only after no worktree uses it;
4. prune stale worktree administrative records;
5. verify every remaining non-primary worktree is attributable to an active work unit or explicit retention/review reason.

`git worktree prune` or equivalent metadata cleanup MUST NOT be treated as permission to discard a live worktree.

### 7. Primary checkout convergence

After post-integration cleanup, the designated primary checkout SHALL be a safe current baseline unless an explicit active workflow requires another state.

For normal Agent Governance source maintenance:

```text
primary checkout branch = develop
local develop            = current origin/develop
tracked status           = clean
```

For an authorized release/hotfix/stable workflow, the controlling workflow may route to `main` or another explicit specialized base.

The invariant MUST NOT be achieved by destructive reset, cleaning, or deletion of unrepresented work. If the primary checkout cannot be converged safely, closure is `BLOCKED`/`PARTIAL` and the conflicting state is preserved.

### 8. Remaining branch/worktree inventory

“No orphan worktrees/branches” means **no unexplained local execution state**, not “delete every non-long-lived ref”.

After a hygiene operation, every remaining non-primary worktree and non-long-lived branch in the accessible environment must be one of:

- actively owned by a current work unit;
- explicitly retained for a durable reason;
- explicitly classified `REVIEW`/blocked pending disposition.

A `REVIEW` item is not silently deleted. If it can collide with the next work unit, the next launch remains blocked until disposition.

### 9. Cleanup is separate from implementation handoff

A task worktree/topic branch remains needed through Executor handoff, Orchestrator convergence and integration. The Executor does not delete its own review surface before acceptance/integration.

Post-integration retirement remains a bounded operation under the existing Operational Contract/branch-cleanup mechanism when delegated.

### 10. D054 mechanics boundary

D058 defines semantic postconditions, not mandatory command syntax.

The Executor owns compatible Git/worktree commands under D054. Repository policy decides what may be removed and what evidence must exist before removal.

## Codex adapter consequence

Codex 0.153.4 supports explicit thread rename/new-session naming. The Orchestrator launch card for Codex therefore adds:

```text
Coordinator-Chat: AG | <repo> | <work-unit> | root-<n>
```

This field supplements D055's Executor/Session/Model/Effort/Rationale fields.

## Current T057 consequence

T057 had not begun when D058 was accepted.

Before T057:

1. perform a bounded local hygiene operation against the current Windows checkout;
2. retire only evidence-safe stale worktrees/branches and preserve ambiguous state;
3. leave the primary checkout clean on current `develop`;
4. then launch T057 in a fresh named coordinator chat and an exclusive task worktree.

T057's scientific controls remain unchanged.

## Consequences

- Human-visible Executor chats become attributable to durable work units.
- Same-repository parallel coordinators can be distinguished and isolated.
- worktree isolation becomes an explicit concurrency safety boundary;
- integrated branches no longer leave unexplained task worktrees as normal residue;
- the primary checkout becomes a reliable bootstrap baseline after closure;
- cleanup remains fail-closed around unique/unrepresented local work;
- Git and persisted contracts remain authoritative; session titles remain convenience metadata.
