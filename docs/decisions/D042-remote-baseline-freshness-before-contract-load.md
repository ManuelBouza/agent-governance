# D042 — Remote baseline freshness before contract load

Status: ACCEPTED  
Authority: Human Owner / ChatGPT Orchestrator

## Problem

Source-maintenance launch prompts have said `Start from current <base-branch> and read AGENTS.md first.` That wording is insufficient when the executor host is currently checked out on an older topic branch or has stale local refs.

A concrete OP009 launch exposed the ambiguity: the executor remained on the already-integrated T010 implementation branch, attempted to read the newly integrated OP009 contract from that stale checkout, and only afterward inspected Git state. The persisted contract existed on canonical `origin/develop`, but not in the local branch being read.

This is a bootstrap/freshness defect, not an executor methodology issue.

## Decision

Before reading repository policy or the persisted Task/Operational Contract for a delegated action, the executor MUST establish that its local execution baseline reflects the current canonical remote base branch.

Core invariant:

```text
canonical remote freshness
    -> verified local base identity
    -> AGENTS.md
    -> persisted contract
    -> execution
```

`current <base-branch>` means the current canonical remote branch state, normally `origin/develop`, not merely a local branch named `develop` and not the executor's currently checked-out topic branch.

The executor MUST synchronize remote references using its compatible Git workflow and verify that the local baseline used to load the contract is current with the canonical remote base branch before contract execution begins.

If local uncommitted/untracked state, worktree constraints, permissions, connectivity, divergent history or another condition prevents establishing the required baseline without risking data loss, the executor MUST stop/escalate rather than overwrite, discard, guess, or read the contract from stale state.

## Transport boundary

This requirement governs bootstrap identity/freshness only. It does not prescribe the executor's internal implementation methodology, agent topology, SDD use, Skills, CodeGraph, planning process, or other proprietary execution choices under D041.

The launch prompt MAY therefore require remote synchronization and baseline verification because those facts determine which persisted Git instruction is being loaded. It MUST NOT carry task/operation-specific commands, SHAs, targets, or implementation semantics that belong in the persisted contract.

## Canonical bootstrap semantics

The structural launch order is:

1. synchronize the canonical remote;
2. ensure the local base branch/worktree used for bootstrap is at the current canonical remote base state;
3. read `AGENTS.md` from that baseline;
4. load exactly one persisted Task Contract or Operational Contract from that baseline;
5. execute under the contract;
6. return the contract-defined result.

A compatible executor may choose the concrete safe Git commands needed to satisfy this sequence.

## Safety boundary

Freshness MUST NOT be achieved by destructive reset of unrelated or uncommitted work.

```text
stale baseline + safe synchronization unavailable
    != permission to discard work
    = BLOCKED / escalation
```

Untracked local runtime state such as `.codegraph/` may coexist if it does not prevent safe baseline establishment and remains outside unauthorized tracked mutation.

## Relationship to D041 and existing prompt policy

D041 remains fully authoritative for executor process autonomy. D042 addresses only the external Git bootstrap precondition necessary to load the correct Governance instruction.

`docs/TASK-CONTRACTS.md`, `docs/OPERATION-CONTRACTS.md`, and `docs/POST-INTEGRATION-CLEANUP-PROMPT.md` SHALL use this remote-freshness meaning for `Start from current <base-branch>`.

## Consequences

- an executor must not attempt to load a newly integrated contract from an older task branch;
- local branch-name equality alone is insufficient proof of freshness;
- launch prompts stay generic and pointer-only while gaining an explicit remote-freshness precondition;
- stale/local-state conflicts fail closed without destructive cleanup;
- executor-internal implementation autonomy remains unchanged.
