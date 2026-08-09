# ChatGPT Project Setup

Status: ACTIVE

## Purpose

Configure the dedicated ChatGPT Project used by the ChatGPT Orchestrator so every new conversation cold-starts from the canonical Git repository instead of depending on previous chat history.

## ChatGPT Project configuration

Canonical repository:

`https://github.com/ManuelBouza/agent-governance`

Normal bootstrap branch:

`develop`

OpenAI Project Instructions are intentionally kept small. They are a stable adapter into Git, not a copy of project state.

### Recommended Project Instructions

Copy this exact block into **Project settings -> Project instructions**:

```text
You are the ChatGPT Orchestrator for the Agent Governance source product.

Canonical repository: https://github.com/ManuelBouza/agent-governance
Use GitHub for repository reads and writes.
Treat Git as the authoritative source of project state; Project Memory and prior chats are non-authoritative context only.

At the start of every new chat, before acting on the user's first project request:
1. Read current `develop` from GitHub.
2. Read `AGENTS.md` from `develop`.
3. Read `docs/orchestrator/CHECKPOINT.md` from `develop`.
4. Follow the checkpoint's `Next Chat Minimum Load` and `Next Action`.
5. Load no additional project history unless the checkpoint or a concrete conflict requires it.

Do not ask the user to paste or summarize previous chats when repository state is sufficient.
Do not reconstruct the current frontier from Project Memory or chat history.
Follow all role, ownership, branching, Task Contract, handoff, and chat-closure rules referenced by `AGENTS.md` and the checkpoint.
Use `develop` as the normal maintenance bootstrap branch unless an authorized release/hotfix workflow or the checkpoint explicitly routes elsewhere.
```

## Why this is intentionally short

Do not add current task IDs, branch SHAs, active PR numbers, completed decisions, tool versions, or temporary blockers to Project Instructions.

Those facts change and belong in Git, especially `docs/orchestrator/CHECKPOINT.md` and the files it references.

The Project Instructions should change only when the bootstrap contract itself changes.

## Memory mode

For a newly created dedicated ChatGPT Project, prefer **project-only memory** when available to isolate this work from unrelated chats outside the Project.

Project-only memory is not the state mechanism. Other conversations inside the same Project may still be available as context, so the Git-first cold start remains mandatory.

If the current Project uses default memory, keep using the same Git-first rule. Repository correctness does not depend on memory mode.

## Starting a new chat

After the Project Instructions above are configured, the Human Owner may start a fresh chat with simply:

```text
Continue.
```

ChatGPT then loads `AGENTS.md`, the current Orchestrator checkpoint, and only the minimum routed context before proceeding.

## Closing a chat

When `docs/orchestrator/CHECKPOINT.md` is current and the D027 closure conditions are satisfied, ChatGPT should explicitly recommend a new chat.

Because the Project Instructions already contain the bootstrap coordinates, the closure message does not need to repeat a long restart prompt. It should identify the checkpoint and tell the Human Owner that the next chat may begin with `Continue.`.

## Audit rule

This file is the canonical repository copy of the recommended ChatGPT Project configuration. If the UI Project Instructions are changed materially, update this file through the normal source Markdown workflow so the intended bootstrap remains auditable.
