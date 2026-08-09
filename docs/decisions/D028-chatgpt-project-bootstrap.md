# D028 — ChatGPT Project bootstrap

Status: ACCEPTED
Authority: Human Owner

## Decision

The ChatGPT Project that hosts source-product Orchestrator conversations SHALL use its Project Instructions only as a small, stable bootstrap adapter into the canonical Git repository.

Project Instructions MUST NOT duplicate the current project frontier, Task Contract content, decision history, or Orchestrator checkpoint. Dynamic state remains in Git.

The canonical repository is:

`https://github.com/ManuelBouza/agent-governance`

The normal source-maintenance bootstrap branch is `develop`.

At the start of each new ChatGPT conversation inside the Project, ChatGPT SHALL use GitHub to read, in order:

1. `AGENTS.md` from current `develop`;
2. `docs/orchestrator/CHECKPOINT.md` from current `develop`;
3. only the files named by the checkpoint under its minimum-load/next-action routing.

Project chat history and Project Memory MAY help conversationally, but they are non-authoritative for repository state. ChatGPT MUST reconstruct the operational frontier from Git before acting and MUST NOT require the Human Owner to paste a prior-chat summary.

## Rationale

ChatGPT Projects support project-specific instructions, files, chats, memory and tools. Project Instructions apply within the Project and replace global custom instructions there. Project memory can also reference earlier conversations in the same Project. Therefore the safest architecture is:

- Project Instructions: stable entrypoint and repository coordinates;
- Git repository: auditable source of truth and current frontier;
- Project Memory/chat history: optional convenience only.

This prevents Project Instructions from becoming stale dynamic state and preserves D027's invariant that private chat history is optional.

## Project memory recommendation

For a newly created dedicated ChatGPT Project, project-only memory is preferred when available because it isolates the Project from unrelated conversations outside the Project.

Project-only memory does not replace the Git checkpoint: chats inside the same Project may still reference one another, so every new Orchestrator chat still cold-starts from Git.

If an existing ChatGPT Project was created with default memory, no migration of repository state is required. The Git-first bootstrap remains mandatory regardless of memory mode.

## Canonical Project Instructions

The exact recommended text is maintained in:

`docs/CHATGPT-PROJECT-SETUP.md`

That repository copy is the auditable canonical template. The Human Owner copies the compact instruction block into ChatGPT Project Settings.

## Minimal new-chat interaction

Once the Project Instructions are configured, a new Orchestrator chat MAY begin with only:

`Continue.`

The Project Instructions provide repository/bootstrap routing; `docs/orchestrator/CHECKPOINT.md` determines the actual next action.

## Boundary

This is a source-repository ChatGPT adapter rule only. It does not change the portable Consumer Governance protocol, consumer adapter semantics, or executor Task Contracts.
