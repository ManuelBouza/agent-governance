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

## Durable GitHub receipt envelope

For every operation governed by the durable-receipt rule in `docs/OPERATION-CONTRACTS.md`, the executor MUST publish the final completion response as a top-level comment on the contract-defined GitHub receipt anchor before claiming `DONE`.

The comment MUST use this envelope exactly:

```text
AGENT-GOVERNANCE-OPERATION-RECEIPT v1
CONTRACT: <docs/operations/OPNNN-*.md>
BASE_SHA: <canonical base SHA used for execution>

STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP###
DESCRIPTION: <stable operation description>
<all operation-specific completion fields in contract-defined order>
```

Rules:

- `CONTRACT` MUST equal the integrated Operational Contract path actually executed.
- `BASE_SHA` MUST identify the canonical base commit established during bootstrap before the operation begins.
- The block beginning with `STATUS` MUST be the exact completion response required by the Operational Contract; no required field may be omitted.
- The interactive response returned to the caller MUST reproduce that same completion block. It is a convenience copy, not the durable authority.
- ChatGPT MUST read the receipt from GitHub and match `CONTRACT`, `BASE_SHA`, `OPERATION`, required fields, and final status before closing the operation.
- A receipt comment is execution evidence only. It does not substitute for ChatGPT's independent verification or Human authority.

If the executor cannot publish to the configured receipt anchor before mutation, it MUST stop before mutation and report `BLOCKED`. If mutation has already occurred and final receipt publication unexpectedly fails, the executor MUST stop further mutation and report `PARTIAL` through the available interactive channel.

## Scope

This convention applies to new Operational Contracts and to any existing READY operation before its next execution when ChatGPT can safely revise its completion shape without changing operation authority, mutation scope, or acceptance criteria.

Task Contract executor handoff shapes remain governed by `docs/TASK-CONTRACTS.md` and `docs/EXECUTOR-HANDOFFS.md` and are not changed by this document.
