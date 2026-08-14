# Operational Contracts

## Purpose

Operational Contracts authorize bounded executor operations that are not normal source implementation tasks, including branch cleanup, host configuration, read-only audits, and other narrowly scoped maintenance actions.

The persisted Operational Contract is authoritative. Chat/terminal prompts are bootstrap transport only and MUST NOT carry material operation semantics that are absent from the contract.

## Completion response identity

Every Operational Contract completion response MUST include, immediately after the operation identifier, a short human-readable `DESCRIPTION` field.

Required prefix:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP###
DESCRIPTION: <short description of what this operation does>
```

The description MUST:

- identify the operation in plain language without requiring the reader to open the contract;
- remain short, normally one concise phrase;
- describe the authorized operation, not an inferred result or implementation narrative;
- remain stable across DONE, BLOCKED, and PARTIAL outcomes for the same operation.

Example:

```text
STATUS: DONE
OPERATION: OP047
DESCRIPTION: Retire OP046 contract branch
REMOTE_REMAINING: develop, main
LOCAL_REMAINING: develop, main
```

Operation-specific evidence fields follow this required prefix.

## Scope

This convention applies to new Operational Contracts and to any existing READY operation before its next execution when ChatGPT can safely revise its completion shape without changing operation authority, mutation scope, or acceptance criteria.

Task Contract executor handoff shapes remain governed by `docs/TASK-CONTRACTS.md` and `docs/EXECUTOR-HANDOFFS.md` and are not changed by this document.
