# Post-Integration Cleanup Prompt

Status: ACTIVE

## Purpose

Define the canonical bootstrap prompt for delegated post-integration branch retirement.

The concrete cleanup instruction MUST already be persisted in an integrated Operational Contract under `docs/operations/` according to `docs/OPERATION-CONTRACTS.md`.

## Authority invariant

```text
cleanup prompt = bootstrap transport only
Operational Contract + referenced Git policy = complete cleanup instruction
```

The prompt MUST NOT carry cleanup targets, branch names, SHAs, deletion decisions, exceptions, commands, or acceptance semantics.

If any operation-specific fact is needed, persist it in the Operational Contract before launch.

## Canonical prompt

```text
Operate as the Agente de IA Ejecutor for <owner>/<repository>.

Start from current develop and read AGENTS.md first.

Then load and execute the authoritative Operational Contract:
<operation-contract-path>

Treat that Operational Contract and its referenced repository policies as the complete operation specification. Do not infer, supplement, or expand operation scope from this prompt.

Complete the contract-defined operation and verification, then return only the completion response defined by the Operational Contract.
```

Normal substitutions are limited to repository identity and exactly one integrated Operational Contract path.

## Required semantics

The Operational Contract identifies the durable integration targets, any resolved-review exceptions, deterministic derivation rules, safety constraints, and completion evidence.

The executor derives dynamic repository facts only from the authoritative sources named by that contract. Chat/terminal text is never an alternative authority.

Post-integration cleanup MUST NOT create a new implementation scope, modify repository content, reopen acceptance, or invent another Task Contract.

## Completion invariant

```text
integrated change != operationally closed change
operational closure = integrated change + verified post-integration branch retirement
```

If cleanup cannot be performed safely from the persisted contract and referenced Git/GitHub evidence, return `BLOCKED` or `PARTIAL`; do not compensate with chat-only instructions.
