# D027 — Orchestrator chat checkpoints

Status: ACCEPTED
Authority: Human Owner

## Decision

Source-product maintenance by ChatGPT SHALL be resumable from a fresh ChatGPT conversation without relying on prior chat history, hidden context, or memory of earlier sessions.

Because this source repository deliberately does not install its own consumer `.agent-coordination/` instance, ChatGPT Orchestrator continuity is represented by a separate repository-maintenance checkpoint mechanism rather than by consumer `STATE.json` / `EXCHANGE.jsonl`.

The canonical current checkpoint is:

`docs/orchestrator/CHECKPOINT.md`

Its operating contract is:

`docs/ORCHESTRATOR-CHECKPOINTS.md`

## Core invariant

`PRIVATE CHAT HISTORY IS OPTIONAL; GIT IS SUFFICIENT TO RESUME`.

A fresh ChatGPT conversation must be able to determine the current source-maintenance frontier by reading the repository, not by reconstructing the prior conversation.

## Checkpoint purpose

The checkpoint is a compact routing/frontier artifact. It SHALL contain enough durable context to answer:

- what coherent work has just been completed;
- what branch/state is authoritative now;
- which accepted decisions/contracts control the next step;
- which Task Contract, executor handoff, branch, or PR is active when applicable;
- unresolved blockers/questions that materially constrain the next action;
- the exact next permitted action;
- the minimum files a new ChatGPT chat must load before acting;
- whether the current chat may be closed and replaced by a new one.

The checkpoint MUST reference canonical files instead of duplicating long specifications, research, diffs, or historical debate.

## Checkpoint lifecycle

ChatGPT SHALL refresh the checkpoint when any of the following occurs:

1. a coherent planning/research/architecture unit is completed and affects what should happen next;
2. a Task Contract becomes READY, BLOCKED, REVISED, ACCEPTED, or CANCELLED;
3. an executor handoff is received/reviewed and the review changes the frontier;
4. a source-maintenance PR is merged and the next permitted action changes;
5. a material blocker, risk, or Human Owner decision changes the current frontier;
6. ChatGPT intends to close the current conversation and recommend continuing in a new chat.

The checkpoint need not be rewritten for every conversational message. It represents durable frontier changes, not a transcript.

## Git identity and staleness

The Git commit containing `docs/orchestrator/CHECKPOINT.md` versions the checkpoint. The checkpoint MUST NOT attempt to self-store the SHA of the commit that contains itself.

A fresh ChatGPT session SHALL:

1. fetch current `develop`;
2. read `AGENTS.md` and `docs/orchestrator/CHECKPOINT.md` from that current revision;
3. follow only the controlling references named by the checkpoint;
4. if relevant referenced branches, PRs, Task Contracts, or handoffs have advanced since the checkpoint was written, inspect the minimum remote delta before acting;
5. refresh the checkpoint before another intentional chat closure if the frontier changes.

## Chat closure protocol

ChatGPT MAY recommend ending the current chat only when:

- all material decisions from the current coherent work unit are already persisted remotely;
- there is no unpersisted requirement or acceptance change that a new chat would need;
- the checkpoint accurately represents the current frontier and next action;
- any relevant topic branch, PR, Task Contract, or handoff references are remotely accessible;
- the next chat can resume from repository state alone.

When these conditions hold, ChatGPT SHALL make the closure explicit to the Human Owner and provide a minimal restart instruction pointing to the repository checkpoint.

Recommended visible closure form:

```text
CHAT STATUS: CLOSE / NEW CHAT RECOMMENDED
CHECKPOINT: docs/orchestrator/CHECKPOINT.md
NEXT: Start a new ChatGPT chat and say:
"Continue agent-governance from develop. Use GitHub. Read AGENTS.md and docs/orchestrator/CHECKPOINT.md, then follow next_action."
```

The exact wording may vary, but it MUST identify the canonical checkpoint and explicitly recommend a new chat when closure is intended.

ChatGPT MUST NOT recommend chat closure while material context exists only in the conversation.

## New-chat cold start

A new ChatGPT conversation SHOULD require only this minimal user prompt:

```text
Continue agent-governance from develop. Use GitHub. Read AGENTS.md and docs/orchestrator/CHECKPOINT.md, then follow next_action.
```

The new session SHALL NOT require the Human Owner to paste a summary of the previous chat.

## Scope boundary

This decision governs **source-product ChatGPT Orchestrator continuity** in `ManuelBouza/agent-governance`.

It does not replace consumer Governance cold-start/state semantics. Consumer repositories continue to use `.agent-coordination/STATE.json`, EXCHANGE deltas, Governance Core routing, and their own persisted authority records.

The source repository must continue to avoid creating a live consumer `.agent-coordination/` instance for its own maintenance.

## Consequences

- `docs/ORCHESTRATOR-CHECKPOINTS.md` defines the normative checkpoint fields and operating procedure.
- `docs/orchestrator/CHECKPOINT.md` is the single current mutable source-maintenance checkpoint.
- `AGENTS.md` and `docs/DEVELOPMENT-WORKFLOW.md` route ChatGPT cold starts and intentional chat closure through this mechanism.
- source-maintenance prompts for a new ChatGPT chat can remain small because Git stores the required frontier.
- prior chats become audit/convenience history rather than required execution context.
