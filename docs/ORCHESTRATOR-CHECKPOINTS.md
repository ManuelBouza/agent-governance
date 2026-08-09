# ChatGPT Orchestrator Checkpoints

Status: ACTIVE

## Purpose

Define the durable source-repository checkpoint used to resume `agent-governance` maintenance from a fresh ChatGPT conversation without relying on private chat history.

This mechanism is source-product maintenance infrastructure. It does not create a consumer Governance instance and does not replace `.agent-coordination/STATE.json` in adopting repositories.

Canonical current checkpoint:

`docs/orchestrator/CHECKPOINT.md`

## Design principles

1. **Frontier, not transcript** — persist only context required to continue correctly.
2. **References, not duplication** — point to controlling decisions/contracts/handoffs instead of copying them.
3. **Git-native** — the commit containing the checkpoint versions it; do not embed a self-referential commit SHA.
4. **Cold-start sufficient** — a new ChatGPT chat must not need pasted chat history.
5. **Progressive loading** — the new chat loads only the checkpoint's minimum references before deciding what else is needed.
6. **Remote evidence only** — active branches/PRs/handoffs referenced by a checkpoint must be remotely accessible when they control the next action.

## Required checkpoint fields

The current checkpoint is Markdown owned by ChatGPT and SHOULD remain compact. It contains these logical fields/sections:

- `Checkpoint-State` — normally `CURRENT`;
- `Checkpoint-Sequence` — monotonic human-readable identifier such as `O001`, used for discussion/history navigation;
- `Canonical-Branch` — normally `develop`;
- `Current-Work-Unit` — concise description of the coherent unit just completed/currently active;
- `Completed` — only material outcomes that changed the frontier;
- `Controlling-References` — exact paths/decision IDs required for the next action;
- `Active-Remote-Artifacts` — Task Contract, executor handoff, topic branch, PR, or exact pushed SHA when applicable;
- `Open-Questions-Or-Blockers` — only unresolved items that constrain what can happen next;
- `Next-Action` — one explicit next permitted action or ordered immediate sequence;
- `Next-Chat-Minimum-Load` — exact files a cold ChatGPT session should read after `AGENTS.md` and the checkpoint;
- `Do-Not-Load-Or-Do` — optional guardrails that prevent unnecessary context expansion or premature work;
- `Chat-Closure` — `KEEP_CURRENT_CHAT`, `ELIGIBLE`, or `NEW_CHAT_RECOMMENDED`.

The checkpoint MAY include other compact routing fields when required, but it MUST NOT become a second decision log or task specification.

## What belongs in the checkpoint

Persist facts such as:

- D0xx decisions just accepted and relevant to the frontier;
- a Task Contract becoming READY or blocked;
- the exact executor handoff path awaiting ChatGPT review;
- the exact branch/HEAD/PR whose diff must be reviewed;
- a material unresolved Human Owner decision;
- the next action after a merge or review;
- minimum controlling files required by the next ChatGPT session.

## What does not belong

Do not persist:

- full conversation summaries;
- copied research already stored in a Decision Record/normative document;
- full diffs;
- terminal transcripts already captured by a handoff;
- entire decision inventories;
- speculative future work not yet controlling;
- secrets, credentials, personal data, or hidden chain-of-thought;
- a self-referential SHA for the checkpoint commit itself.

## Cold-start procedure for a new ChatGPT chat

When the Human Owner starts a new chat with the minimal continuation prompt, ChatGPT SHALL:

1. use GitHub to fetch current `develop`;
2. read `AGENTS.md`;
3. read `docs/orchestrator/CHECKPOINT.md`;
4. load only `Next-Chat-Minimum-Load` and directly controlling remote artifacts;
5. verify that any referenced active branch/PR/handoff still exists and has not advanced unexpectedly;
6. if it advanced, inspect the minimum delta and reconcile the checkpoint before mutation;
7. continue from `Next-Action` without asking the Human Owner to re-explain completed work.

If the checkpoint is missing, contradictory, obviously stale, or references unavailable remote state, ChatGPT stops normal mutation and reconstructs the frontier from the smallest authoritative Git evidence available. It then refreshes the checkpoint before continuing.

## Refresh procedure

ChatGPT refreshes `docs/orchestrator/CHECKPOINT.md` when the durable frontier changes materially.

A refresh SHOULD occur after:

- accepted planning/research decisions;
- Task Contract readiness/revision/status changes;
- executor return/review/rework decisions;
- PR integration that changes what is allowed next;
- new blocking Human Owner decisions;
- intentional chat closure.

A refresh is not required for every reply or every intermediate tool call.

Because checkpoint Markdown is committed repository content, normal source-change branch/PR rules still apply. When a checkpoint refresh is part of a coherent Markdown planning change, include it in that same planning branch/PR rather than creating unnecessary extra PRs.

When the checkpoint must change solely because a prior PR has just merged, ChatGPT MAY include the new frontier in the next coherent Markdown planning change. Chat closure is allowed only after a remotely persisted checkpoint already describes a safe resumable frontier.

## Chat closure decision

`Chat-Closure: NEW_CHAT_RECOMMENDED` is appropriate when:

- the current chat has completed a coherent work unit;
- repository state contains everything a new chat needs;
- the checkpoint names the next action and minimum load;
- no active requirement exists only in chat;
- continuing to accumulate conversation context offers no material benefit.

`Chat-Closure: ELIGIBLE` means a new chat is safe but not specifically recommended yet.

`Chat-Closure: KEEP_CURRENT_CHAT` means material work is in flight or the checkpoint is not sufficient for a clean restart.

## Visible close/restart contract

When `NEW_CHAT_RECOMMENDED`, ChatGPT tells the Human Owner clearly that this chat can be closed and the next interaction should use a new chat.

Minimal restart prompt:

```text
Continue agent-governance from develop. Use GitHub. Read AGENTS.md and docs/orchestrator/CHECKPOINT.md, then follow next_action.
```

The restart prompt is transport only. The repository checkpoint remains the source of continuity.

## Relationship to executor handoffs

Executor handoffs and Orchestrator checkpoints solve different problems:

- `handoffs/TNNN-executor-handoff.json` — what the Agente de IA Ejecutor did/reported on an executable task;
- `docs/orchestrator/CHECKPOINT.md` — what ChatGPT currently needs to know to continue source-product orchestration.

When an executor handoff is the current frontier, the checkpoint points to it; it does not copy the complete handoff.

## Relationship to consumer Governance

Consumer repositories already have durable cold-start machinery through Governance Core, STATE, EXCHANGE, MISSION/WORKPLAN/task records, decisions, Skills, and adapters.

Do not copy this source-maintenance checkpoint into a consumer repository as a second state system. The design principle is shared — private chat history is not required — but the persistence surfaces remain distinct.
