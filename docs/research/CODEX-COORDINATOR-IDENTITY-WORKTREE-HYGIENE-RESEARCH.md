# R011 — Codex Coordinator Identity and Worktree Hygiene Research

Research-ID: R011  
Research-State: COMPLETE  
Decision-State: DECIDED  
Opened: 2026-09-05  
Last-Reviewed: 2026-09-05  
Owner: ChatGPT Orchestrator  
Scope: source-maintenance Executor coordinator identity, concurrent local worktree isolation, and post-integration local Git hygiene  
Question: How should Agent Governance identify Codex coordinator chats and prevent parallel/stale worktrees, branches, or a stale primary checkout from causing task confusion or cross-task mutation?  
Evaluation-Refs: current source-maintenance workflow; T056/T057 execution lineage  
Decision-Ref: docs/decisions/D058-executor-coordinator-session-and-worktree-hygiene.md  
Supersedes: none  
Superseded-By: none

## Executive conclusion

Agent Governance already has strong remote branch retirement and remote-baseline freshness rules, but two operational identities remained implicit:

1. which Human-visible Codex coordinator chat represents a work unit and should be continued;
2. which local worktree/checkout owns a writable work unit, and what local state must remain after integration.

Current Codex supports explicit thread naming. Current Agent Governance policy already requires topic-branch retirement and inspection of local worktrees, but it does not make actual obsolete-worktree removal plus primary-checkout convergence an explicit closure postcondition.

The recommended correction is therefore additive rather than a new Git lifecycle:

- give every named-session-capable Executor coordinator a deterministic Human-visible session name;
- keep the host thread/session ID as corroborating identity when a supported surface exposes it;
- treat the name as navigation metadata, never authority;
- require one writable work unit per writable worktree/topic branch;
- prohibit two concurrent writable coordinators from sharing a worktree;
- extend integration closure to retire obsolete worktrees safely and leave the designated primary checkout clean and current with its authorized long-lived remote branch;
- preserve/stop on unrepresented or ambiguous local work instead of reset/clean/delete to manufacture hygiene.

## Existing Agent Governance coverage

### Branch lifecycle is already strong

`docs/BRANCHING.md` and `docs/BRANCH-CLEANUP.md` already require:

- short-lived topic branches;
- merged-branch freeze at the exact reviewed PR head;
- remote branch retirement after integration;
- local topic-branch cleanup in every accessible checkout;
- `git worktree list` during local cleanup;
- fail-closed treatment of ambiguous/unrepresented local work;
- cleanup before the next task when a checkout was inaccessible at merge time.

The missing postcondition is narrower: a checkout may inspect worktrees yet still leave an obsolete registered worktree/directory behind, and a primary checkout may remain on an old topic branch or stale long-lived branch even after remote integration is complete.

### D042 already protects baseline freshness

D042 requires the Executor to establish a safe local baseline equal to current canonical remote state before loading execution authority. It prevents a stale local branch from being treated as current merely because it is named `develop`.

That bootstrap rule does not by itself define end-of-task local topology. A separate closure invariant is therefore justified.

## Codex coordinator naming evidence

Official current `openai/codex` source inspected on 2026-09-05 at:

```text
531f3836a1e38ea61eaaba3dccda6711eb6c0dca
```

shows:

- `SlashCommand::Rename` with the user-visible description `rename the current thread`;
- `/rename <name>` accepts inline arguments and sends the normalized name through the thread-name event path;
- `/new <name>` can start a new session with an explicit name;
- Codex separately maintains a thread/session identity.

Relevant files:

- `codex-rs/tui/src/slash_command.rs`
- `codex-rs/tui/src/chatwidget/slash_dispatch.rs`

This capability is host-specific and volatile. The governance conclusion does not depend on the exact slash-command syntax: when a selected Executor exposes user-visible session naming, the Orchestrator can supply a deterministic name and the Human/host can apply it through the supported UI or command surface.

## Why a chat name is useful but insufficient as authority

A deterministic coordinator name directly solves the Human navigation problem:

- identify what a chat did;
- distinguish two active tasks in the same repository;
- know which chat to continue for same-task rework;
- avoid accidentally continuing an unrelated coordinator context.

However names are mutable and may not be globally unique. Therefore:

```text
Coordinator chat name = Human navigation / continuity metadata
Task Contract + branch + Git state = execution authority
Host thread/session ID = corroborating identity when supported
```

No Task Contract or acceptance result may depend solely on a UI title.

## Naming scheme

For the current Codex adapter, the recommended deterministic form is:

```text
AG | <repo> | <work-unit> | root-<n>
```

Examples:

```text
AG | agent-governance | T057 | root-1
AG | agent-governance | OP067 | root-1
```

Rules:

- `work-unit` is the durable Task/Operation ID when one exists;
- `root-1` is the first Human-visible coordinator for that work unit;
- same-task `CONTINUE` retains the same coordinator name;
- if policy requires a new session for the same work unit, increment the root ordinal rather than reusing the old name;
- subagents are not assigned independent Human coordinator names unless they themselves become Human-visible persistent coordinators, which normal Task Contracts do not do.

This keeps names short, sortable and collision-resistant across repositories/work units.

## Worktree isolation finding

Worktrees are the correct local isolation primitive for parallel writable tasks because each can bind a distinct working directory and topic branch while sharing the same object database.

The safety invariant is not “always use a worktree”; it is:

```text
one concurrently writable work unit -> one exclusive writable worktree/topic branch
```

A bounded repository-maintenance operation may need the primary checkout because it must inspect/normalize the whole local topology. That is an explicit operational exception, not permission for two implementation coordinators to share the primary checkout.

## Primary checkout finding

For this source repository, normal maintenance authority is `develop`. The primary checkout outside task-specific linked worktrees should therefore be a clean baseline checkout that can bootstrap new work.

Normal terminal state:

```text
primary checkout branch = develop
local develop            = origin/develop
tracked status           = clean
```

For an authorized release/hotfix/stable workflow, the controlling contract may instead route the primary checkout to `main` or another explicit long-lived/specialized base.

The invariant must never be achieved by discarding unknown local changes or unique commits. If the primary checkout cannot be made current safely, the correct state is BLOCKED/REVIEW with the work preserved.

## Worktree retirement finding

A completed task worktree is local execution scaffolding, not durable project history. After its represented branch is integrated and safe-retirement evidence exists, closure should include:

- verify no unrepresented changes/commits;
- remove the obsolete linked worktree using compatible Git mechanics;
- retire the corresponding local topic branch after it is no longer checked out anywhere;
- prune stale worktree administrative metadata;
- verify all remaining worktrees are active/intentional and attributable to a live work unit or explicit retention reason.

`git worktree prune` alone is not a deletion authorization. It only cleans stale administrative records; it must not substitute for inspecting a live or ambiguous worktree.

## Parallel coordinator finding

Two coordinators may work in the same repository concurrently only when their writable surfaces are isolated.

Required separation:

```text
coordinator A -> branch A -> worktree A
coordinator B -> branch B -> worktree B
```

They may share the same canonical remote and object database. They must not share a writable worktree, topic branch, handoff path, or task identity.

The primary checkout remains a baseline/maintenance surface rather than a shared scratch directory while parallel writable coordinators are active.

## Handoff/audit implications

For future named-session-capable Executor work, durable evidence should capture enough coordinator/worktree identity to distinguish sessions without turning local UI state into authority:

```text
coordinator_session.name
coordinator_session.mode          # NEW | CONTINUE
coordinator_session.host_thread_id # when supported, otherwise null + reason
workspace.branch
workspace.worktree_label
workspace.isolation
```

Absolute workstation paths are not required as canonical evidence and should be avoided when a relative label is sufficient.

## Current T057 implication

T057 had not started when this research was requested. Its launch should therefore occur only after:

1. the new session/worktree hygiene decision is integrated;
2. a bounded local hygiene operation audits the current Windows checkout/worktrees/branches, preserves ambiguous work, retires only evidence-safe residue, and restores the primary checkout to current `develop`;
3. T057 launches in its own named coordinator session and exclusive task worktree.

This changes no T057 scientific variable. Sol/Medium, Codex 0.153.4+, `:read-only`, one parent/one child, and one provider-backed attempt remain frozen.

## Decision disposition

The Human Owner explicitly requested these controls before T057. D058 adopts them as source-maintenance operating policy.

This research is therefore:

```text
Research-State: COMPLETE
Decision-State: DECIDED
Decision-Ref: docs/decisions/D058-executor-coordinator-session-and-worktree-hygiene.md
```

## Volatility / revalidation

Codex UI/CLI naming commands and thread metadata are vendor surfaces and must be rechecked if materially changed.

The governance requirements themselves are tool-neutral:

- deterministic coordinator identity when the host supports naming;
- exclusive writable workspace per concurrent task;
- evidence-safe worktree/branch retirement;
- safe current primary checkout after closure.
