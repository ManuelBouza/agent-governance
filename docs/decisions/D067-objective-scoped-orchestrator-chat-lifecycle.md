# D067 — Objective-Scoped Orchestrator Chat Lifecycle

Status: ACCEPTED  
Date: 2026-09-06  
Authority: Human Owner / ChatGPT Orchestrator  
Scope: source-product ChatGPT Orchestrator lifecycle and cross-chat handoff

## Decision

Agent Governance adopts **one clear, verifiable Human objective per ChatGPT Orchestrator chat** for source-product maintenance.

A ChatGPT chat is a bounded orchestration work unit. It may contain all phases needed to satisfy its objective, but once that objective is complete it MUST NOT silently begin a materially new objective in the same chat.

```text
one ChatGPT chat
    -> one explicit objective
    -> one verifiable completion condition
    -> durable persistence
    -> successor bootstrap
    -> retirement
```

This decision refines D027 and `docs/ORCHESTRATOR-CHECKPOINTS.md`. Git and durable project artifacts remain authoritative; chat history is never required authority.

## Objective identity

At the beginning of material work, the Orchestrator SHALL be able to state:

- repository;
- objective/work-unit identity when one exists;
- concise objective;
- observable completion condition;
- controlling canonical branch;
- current checkpoint;
- active topic/workspace identity when writable work is needed.

A Task Contract, Operational Contract, Decision, research item, release/hotfix unit, or other persisted work-unit identifier may provide the objective identity. A separate identifier is not required merely for ceremony.

## Lifecycle

Normal lifecycle:

```text
ACTIVE
  -> OBJECTIVE_COMPLETE
  -> WAITING_FOR_NEXT_OBJECTIVE
  -> HANDOFF_READY
  -> SUCCESSOR_VERIFIED
  -> RETIRED
```

Failure path:

```text
HANDOFF_READY
  -> successor detects material discrepancy
  -> BOOTSTRAP_MISMATCH
  -> predecessor remains recoverable only to repair the handoff/frontier
  -> new bootstrap
  -> SUCCESSOR_VERIFIED
  -> RETIRED
```

### ACTIVE

The chat is executing its one objective.

### OBJECTIVE_COMPLETE

The objective and its required acceptance/persistence/cleanup are complete. No new material objective may start in this chat.

### WAITING_FOR_NEXT_OBJECTIVE

The current objective is complete but the Human Owner has not yet supplied the next objective. The chat may answer status questions and preserve/repair its own closure state, but MUST NOT infer or start backlog work.

If the Human Owner supplies the next objective to this completed chat, the predecessor uses it only to construct the successor bootstrap. It does not execute that new objective itself.

### HANDOFF_READY

The predecessor has generated a successor bootstrap containing the exact next objective and sufficient durable-state identities for fail-closed startup.

### SUCCESSOR_VERIFIED

The successor has performed the required bootstrap checks and found no material discrepancy. The predecessor is no longer needed for normal work.

### RETIRED

The predecessor chat must not be reused for another objective.

## Completion gate

An objective is not `OBJECTIVE_COMPLETE` merely because content was drafted or an Executor returned `DONE`.

The applicable closure set must be complete, including as relevant:

- objective acceptance established;
- required GitHub integration/persistence complete;
- current specification/decision/task state durable;
- Executor handoffs/reviews durable;
- current canonical Git identity known;
- D066 Library snapshot state synchronized/validated when used;
- active locks/workspaces classified and released/retained correctly;
- cleanup/retention state represented;
- checkpoint current;
- no material requirement, blocker, correction, or next-state fact exists only in chat.

If any required item remains unresolved, the chat stays `ACTIVE` or explicitly blocked; it does not hand off an invented clean state.

## Successor bootstrap contract

The predecessor SHALL generate a compact bootstrap prompt when the next objective is known. The prompt is transport, not authority, but it MUST carry enough expected identity to detect a stale or contradictory frontier.

The bootstrap SHOULD include, when applicable:

```text
Repository: <owner/repo>
Predecessor: <chat/work-unit identity>
Completed objective: <concise completed objective>
Next objective: <exact new objective>
Canonical branch: <branch>
Expected canonical HEAD: <sha>
Checkpoint: docs/orchestrator/CHECKPOINT.md
Expected checkpoint sequence: <Oxxx>
Active/retained task state: <paths/branch/head/status>
Library snapshot namespace: <namespace or n/a>
Expected snapshot checksum/tree/represented GitHub HEAD: <values or n/a>
Required minimum load: <exact files>
```

The prompt SHALL instruct the successor to use current GitHub state, not pasted history, and to perform the bootstrap verification before executing the new objective.

## Successor bootstrap verification

Before substantive action, a successor SHALL:

1. fetch current canonical branch identity from GitHub;
2. read current `AGENTS.md`;
3. read current `docs/orchestrator/CHECKPOINT.md`;
4. load the checkpoint's minimum controlling references;
5. compare expected bootstrap identities with observed GitHub state;
6. when Library state is required, materialize and validate the exact snapshot/receipt under D066/D068 before writable use;
7. verify active referenced branches/heads/handoffs/PRs as applicable;
8. only then enter the new objective.

The canonical repository wins over the prompt when the prompt is merely stale, but a material discrepancy is not silently reconciled by the successor.

## Fail-closed discrepancy rule

If expected and observed state materially disagree, the successor SHALL stop before new-objective mutation and classify:

`BOOTSTRAP_MISMATCH`

The successor produces a compact discrepancy packet containing at least:

```text
predecessor identity
next objective
expected value/state
observed value/state
source checked
why the discrepancy blocks safe continuation
```

The successor MUST NOT:

- guess which state was intended;
- repair predecessor closure history as part of the new objective;
- overwrite a branch/snapshot merely to make the bootstrap match;
- reinterpret an unresolved blocker as closed.

Because ChatGPT chats do not have an assumed direct cross-chat messaging channel, the Human Owner transports the discrepancy packet back to the predecessor chat. The predecessor may then repair only its closure/handoff/frontier inconsistency, persist the correction, and generate a replacement bootstrap.

## Predecessor repair boundary

A predecessor in `BOOTSTRAP_MISMATCH` is recoverable only for the bounded purpose of making its completed objective/frontier internally consistent.

It may:

- correct stale checkpoint/handoff metadata;
- complete missing evidence-safe cleanup that belonged to its objective;
- reconcile a Library/GitHub representation mismatch under existing authority;
- correct its bootstrap expectations.

It may not use the repair window to start the successor's new objective.

If resolving the discrepancy requires a new product decision or material new work, the Human Owner must explicitly authorize how that work is classified before either chat continues.

## Checkpoint semantics

`docs/orchestrator/CHECKPOINT.md` remains the canonical cold-start router.

D067 adds/permits these chat-closure meanings:

- `ACTIVE`
- `WAITING_FOR_NEXT_OBJECTIVE`
- `HANDOFF_READY`
- `BOOTSTRAP_MISMATCH`

`SUCCESSOR_VERIFIED` and `RETIRED` may be represented in the successor/current checkpoint when material; they do not require a dedicated bookkeeping commit when no frontier fact depends on it.

The checkpoint should identify the predecessor objective as complete and the next objective only after the Human Owner supplies it. Backlog/history is not an implied next objective.

## Relationship to D060

D060 controls Human-visible **Executor Coordinator** lifetime inside an exact Task/Operational Contract. D067 controls **ChatGPT Orchestrator chat** lifetime.

They are intentionally different:

```text
ChatGPT chat
  -> one Human objective

Codex/Executor root
  -> one exact executable Task/Operational Contract lifecycle
```

A single ChatGPT objective may contain one Executor contract or no Executor at all. It should not accumulate unrelated future objectives merely because an Executor root remains available.

## Relationship to D066

D066 Library snapshots strengthen D067 continuity but do not replace Git authority.

When a completed objective used portable Library state, the handoff must identify the validated snapshot/receipt state needed by the successor or explicitly state that no writable Library state is retained.

## Effective rule

```text
objective complete
=> do not start another material objective in the same ChatGPT chat

next objective known
=> generate fail-closed successor bootstrap

successor state mismatch
=> STOP and return discrepancy to predecessor

successor bootstrap verified
=> predecessor retired
```
