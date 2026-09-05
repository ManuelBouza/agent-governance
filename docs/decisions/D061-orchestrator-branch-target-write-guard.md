# D061 — Orchestrator Branch-Target Write Guard

Status: ACCEPTED  
Date: 2026-09-05  
Owner: Human Owner / ChatGPT Orchestrator

## Decision

ChatGPT Orchestrator remote repository writes MUST fail closed on branch target.

For normal source-maintenance Markdown work, no content mutation may target `main`, `develop`, or another long-lived integration/release branch directly. The only normal path is:

```text
refresh canonical develop
-> create short-lived topic branch
-> verify topic branch exists at the intended base SHA
-> perform all content mutations with that exact topic branch explicitly supplied
-> review diff
-> merge through PR
```

A missing, invalid, ambiguous, or unverified topic branch is a STOP condition. It MUST NOT trigger a retry against `develop`, `main`, the repository default branch, or a branch omitted from the mutation call.

## Root cause

The repository policy already prohibited direct writes to `main`/`develop`, but the GitHub mutation surface still accepted them and `develop` had no enforced branch protection/ruleset.

Three Orchestrator authoring incidents exposed the gap:

- `2a2f34baa5e90724c46555c876aabe68309a8b99` — accidental direct `develop` placeholder during R012 authoring;
- `59c44d88e202c24928fd4908470bd91099703023` — accidental direct `develop` placeholder during R013 authoring;
- `7a116b92c706801c9259ce152096609adb465563` — accidental direct `develop` placeholder while preparing this write guard.

The common failure mode is not a Git merge bug. It is an Orchestrator-side mutation target error combined with a repository-side absence of enforced protection. GitHub accepted the requested long-lived branch target exactly as supplied.

The incidents remain in history. Do not rewrite history merely to hide them.

## Mandatory pre-write gate

Before the first content mutation for an Orchestrator-owned change:

1. refresh and read current `develop` identity;
2. choose the topic branch name;
3. create the topic branch from the intended current `develop` SHA;
4. verify through a branch-read/search surface that the exact topic branch exists;
5. verify that the branch points at the intended base SHA before the first mutation;
6. only then issue content mutations.

No `create_file`, `update_file`, `delete_file`, tree/ref content update, or equivalent content-changing operation is allowed before this gate passes.

## Explicit-target invariant

Every Orchestrator content mutation MUST specify the exact already-verified topic branch.

Forbidden during normal source maintenance:

```text
branch omitted / null
branch = main
branch = develop
branch = default branch
branch = release/* or hotfix/* without explicit authorized workflow
```

If an API wrapper permits an omitted branch and interprets omission as the repository default, the Orchestrator MUST still provide the explicit verified topic branch.

If a mutation call fails because the topic branch does not exist, the only allowed recovery is to create/verify that topic branch or stop. Retrying the same content mutation on a long-lived branch is prohibited.

## Post-write invariant

After the first topic-branch mutation and before opening the PR:

- verify the topic branch contains the intended change;
- verify the long-lived base branch has not advanced because of the Orchestrator mutation itself;
- if the base branch changed unexpectedly, stop and classify the incident before further authoring;
- compare the complete topic-branch delta against the intended base.

PR merge remains the only normal mechanism that advances `develop` for Orchestrator Markdown changes.

## Repository-side hardening

Process rules alone are insufficient because an erroneous API call can still be emitted.

The repository SHOULD enforce a GitHub branch ruleset or branch-protection rule targeting at least `develop` and `main` with:

- require a pull request before merging;
- block direct updates except actors explicitly required for repository administration/recovery;
- block force pushes;
- block branch deletion for protected long-lived branches;
- no routine bypass for the actor/connection used by ChatGPT Orchestrator repository writes.

The intended property is:

```text
Orchestrator mistake + protected branch
-> GitHub rejects direct write
-> no accidental commit reaches develop/main
```

Repository protection is a Human/repository-administration control. If the active connector cannot mutate repository rules, ChatGPT must report the protection gap rather than pretending it is enforced.

## Relationship to existing policy

D061 strengthens the existing branching invariant and the earlier L007 fail-closed branch-target requirement. It does not authorize direct long-lived-branch writes under any role.

D022/D053 continue to govern source-change lifecycle and ownership. D058/D060 continue to govern Executor worktrees/coordinator continuity. This decision is specifically about ChatGPT Orchestrator remote write targeting.

## Emergency/recovery exception

A direct long-lived-branch mutation is allowed only under an explicit persisted emergency/recovery authority that names:

- the exact target branch;
- the exact intended mutation;
- why PR flow is unavailable or unsafe;
- Human approval when required;
- postcondition and recovery evidence.

Absence of a topic branch, convenience, connector friction, or a failed API call is never an emergency exception.

## Effective rule

```text
No verified topic branch
= no Orchestrator content write.

Long-lived branch supplied to a normal content mutation
= STOP, do not execute.
```
