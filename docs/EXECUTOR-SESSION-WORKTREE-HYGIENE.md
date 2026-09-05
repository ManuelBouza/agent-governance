# Executor Session and Worktree Hygiene

Status: ACTIVE  
Controlling decisions: `docs/decisions/D058-executor-coordinator-session-and-worktree-hygiene.md`, `docs/decisions/D060-task-scoped-executor-coordinator-continuity.md`

## Purpose

Define the source-maintenance operating procedure for Human-visible Executor coordinator identity, task-scoped session continuity, concurrent writable worktree isolation, and safe local Git topology after integration.

This document refines D042/D055 and the existing branch-cleanup procedure. It does not replace Task Contracts, Operational Contracts, D054 execution-mechanics ownership, or Git/GitHub as authoritative project state.

## Coordinator chat identity

For an Executor host that supports naming Human-visible sessions, every `NEW` coordinator launch gets an Orchestrator-assigned name.

Current Codex convention:

```text
AG | <repo> | <work-unit> | root-<n>
```

Examples:

```text
AG | agent-governance | T057 | root-1
AG | agent-governance | OP067 | root-1
```

The `<work-unit>` is the exact persisted Task Contract or Operational Contract identity.

## Task-scoped coordinator lifecycle

D060 makes the Human-visible root lifecycle equal to the governed work-unit lifecycle:

```text
new Task/Operational Contract -> NEW root-1
same contract lifecycle        -> CONTINUE same root
contract closes                -> retire root for governance purposes
next contract                  -> NEW root-1 for that new work unit
```

Normal same-task phases, Orchestrator barriers, persisted review/rework and additional verification do not create a new Human-visible coordinator when the current root remains safely recoverable.

Fresh independent reasoning inside the same task should normally come from a bounded child/subagent or equivalent fresh internal context. It does not require a second Human-visible coordinator.

### Ordinal rule

- first coordinator for the durable work unit: `root-1`;
- normal same-task `CONTINUE`: keep the exact same coordinator name/thread;
- `root-2+`: exceptional failover only when the prior root cannot safely continue;
- never recycle an old root ordinal for a different coordinator thread;
- never reuse a completed task's root for a different Task/Operational Contract.

Valid failover causes include unrecoverable thread/session loss, host/runtime failure, irreparable context contamination, adapter migration that prevents resume, supported session-state corruption, or explicit persisted experimental authority requiring root replacement.

Independent review, exploration, testing or a desire for a cleaner context alone are not failover causes; use internal fresh contexts instead.

When failover occurs, record the reason and do not leave the old and replacement Human-visible roots concurrently writable for the same task/worktree.

The name is a Human navigation aid. If a host exposes a stable thread/session ID through a supported surface, preserve that ID as corroborating evidence when useful. Do not scrape private persistence merely to obtain it.

## Coordinator context hygiene

The root should remain compact enough to coordinate the full task without becoming a transcript archive.

Retain primarily:

```text
exact authority pointer
current phase/status
branch/worktree identity
relevant accepted constraints
concise child findings
completed actions represented in Git/evidence
unresolved blockers/findings
latest Orchestrator review/gate
next action
```

Avoid retaining unnecessary raw test logs, large command output, full file dumps, full child transcripts, abandoned implementation traces and repeated copies of persisted authority.

When supported, safe host-native compaction may be used. Compaction is execution state only and never substitutes for D042 freshness or Git authority.

D060 does not itself require a specific child topology. R012 separately controls the pending semantic delegation-policy question.

## Launch card

For Codex and other named-session-capable adapters, the launch card is:

```text
Executor: <host>
Session: NEW | CONTINUE
Coordinator-Chat: <deterministic name>
Model: <model>
Effort: <reasoning setting>
Rationale: <concise rationale>
```

Before substantive execution, the Human or supported host session surface applies the exact `Coordinator-Chat` name.

If `CONTINUE` is recommended, the Orchestrator identifies the same coordinator name. Under D060, same-task continuation is the normal rule when the matching root is safely recoverable.

If the matching root cannot be identified/recovered, use `NEW` with the next ordinal and state explicit failover rationale rather than guessing.

## Writable workspace isolation

### Normal rule

Every concurrently writable work unit gets an exclusive worktree and topic branch.

```text
work unit A -> worktree A -> branch A
work unit B -> worktree B -> branch B
```

A writable worktree cannot be shared between two active coordinators.

The primary checkout remains a baseline/maintenance surface while parallel implementation worktrees are active.

### Operational exception

A repository-hygiene Operational Contract may operate from the primary checkout when its explicit purpose is to inspect/normalize the local worktree topology. Such an operation must not run concurrently with an implementation coordinator that could be affected by the cleanup.

## Prelaunch topology gate

Before creating or selecting the task worktree, establish from supported Git state:

```text
canonical remote identity
current origin/<authorized-base>
primary checkout branch/status
registered worktree inventory
branch bound to each registered worktree
candidate topic branch availability
unrepresented/ambiguous local state
```

Required postcondition before writable execution:

- selected task worktree is uniquely owned by the work unit;
- selected topic branch is uniquely represented by that work unit;
- no other active writable coordinator uses either;
- no cleanup/destructive action was needed to hide unrepresented work.

If a collision or ambiguous local state cannot be resolved safely, stop before mutation.

For same-task `CONTINUE`, reuse the represented task worktree/branch when still valid rather than creating parallel mutable state merely because a new Executor turn begins.

## Worktree labels

Local paths are workstation implementation details. Use a short attributable worktree label when evidence needs an identifier, for example:

```text
t057-read-only-child-v2
op067-local-hygiene
```

Absolute personal paths are not required in canonical handoffs when a label plus branch/base identity is sufficient.

## Terminal task handoff

A task does not remove its own review worktree when it returns `DONE`, `BLOCKED` or `PARTIAL` if that branch/worktree remains the Orchestrator review surface.

For D058/D060-governed handoffs, persist or make determinable:

```text
coordinator_session:
  name
  mode
  host_thread_id      # nullable if unsupported/unavailable
  thread_id_reason    # when null
  failover_reason     # nullable; required when root ordinal > 1
workspace:
  branch
  worktree_label
  isolation
  base_branch
  base_sha
```

Task-specific evidence schemas may use equivalent field names.

A same-task rework handoff should preserve the same coordinator identity unless a documented failover occurred.

## Post-integration cleanup

After accepted content is integrated, follow the existing PR/head safety rules in `docs/BRANCH-CLEANUP.md`, then close local execution scaffolding.

Semantic sequence:

1. verify integration and exact reviewed branch head;
2. retire the remote topic branch when eligible;
3. inspect the associated local worktree for unrepresented work;
4. remove the obsolete worktree only when safe;
5. retire the local topic branch only after no worktree uses it;
6. prune remote-tracking refs and stale worktree metadata;
7. inventory remaining worktrees/branches;
8. restore/verify the primary checkout baseline.

The Executor chooses exact compatible Git commands under D054.

Once the governed work unit is operationally closed, its Human-visible coordinator root is historical navigation state and MUST NOT be reused as the root for a new Task/Operational Contract.

## Orphan classification

A worktree/branch is not “orphaned” merely because it is old.

Every non-primary local worktree and non-long-lived branch is classified as:

```text
ACTIVE  - owned by a current work unit
RETAIN  - intentionally retained with explicit reason
REVIEW  - ambiguous/unique state requiring disposition
DELETE  - evidence proves safe retirement
```

Only `DELETE` is automatically retired.

`REVIEW` state is preserved. If it can collide with the next work unit or prevents primary-checkout convergence, the next writable launch remains blocked.

## Primary checkout invariant

For this repository's normal source-maintenance state:

```text
branch        = develop
HEAD          = current origin/develop
tracked state = clean
```

`main` is used as the primary baseline only when an authorized stable/release/hotfix workflow explicitly routes there.

A primary checkout with unrepresented changes or unique commits is not forcibly normalized. Preserve it and return `BLOCKED`/`PARTIAL` with the conflict identified.

## Parallel-task example

Two simultaneous source-maintenance tasks may safely coexist as:

```text
Coordinator-Chat: AG | agent-governance | T057 | root-1
Branch: test/t057-codex-read-only-child-requalification-v2
Worktree: t057-read-only-child-v2

Coordinator-Chat: AG | agent-governance | T058 | root-1
Branch: feat/t058-example
Worktree: t058-example
```

They share the repository object database and canonical remote, but not writable directories or topic branches.

Within T057 itself, a rework turn should normally continue `T057 | root-1`; it should not create `T057 | root-2` unless root-1 has a documented failover condition.

## Codex naming/continuity surface

Current official Codex source inspected for R011 supports explicit thread rename/new-session naming. Current OpenAI long-running-agent guidance also supports preserving compact task-relevant state and using compaction where appropriate.

Exact commands/UI/compaction surfaces may change and are not governance authority.

The Orchestrator should prefer the host's supported session-name and resume controls rather than embedding runtime thread mechanics as Task Contract semantics.

## Fail-closed rules

Do not:

- delete a worktree because its name looks stale;
- delete a local branch while another worktree uses it;
- use destructive reset/clean to make the primary checkout appear current;
- let two writable coordinators share one worktree;
- run two Human-visible coordinator roots concurrently for the same work unit/worktree;
- open `root-2` merely to get an independent review or cleaner context;
- infer a `CONTINUE` target from a similar chat title when identity is uncertain;
- reuse a completed task's root for a different Task/Operational Contract;
- treat a chat title or local path as Task Contract authority;
- remove the task review worktree before Orchestrator convergence/integration.
