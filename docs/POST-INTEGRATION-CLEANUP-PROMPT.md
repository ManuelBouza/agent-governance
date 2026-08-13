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

It MAY carry the generic D042 bootstrap requirement to synchronize the canonical remote and verify a safe current local `develop` baseline before reading repository instructions. That requirement selects the correct persisted Git state; it is not cleanup-specific operation semantics.

If any operation-specific fact is needed, persist it in the Operational Contract before launch.

## Canonical prompt

```text
Operate as the Agente de IA Ejecutor for <owner>/<repository>.

Synchronize the canonical remote and ensure the local develop baseline used for bootstrap is current with origin/develop. Preserve local/uncommitted work; if a safe current baseline cannot be established, stop and report BLOCKED rather than using stale repository state.

From that current baseline, read AGENTS.md first.

Then load and execute the authoritative Operational Contract:
<operation-contract-path>

Treat that Operational Contract and its referenced repository policies as the complete operation specification. Do not infer, supplement, or expand operation scope from this prompt.

Complete the contract-defined operation and verification, then return only the completion response defined by the Operational Contract.
```

Normal substitutions are limited to repository identity and exactly one integrated Operational Contract path. The executor chooses its compatible safe Git workflow for establishing current remote identity.

## Required semantics

The Operational Contract identifies the durable integration targets, any resolved-review exceptions, deterministic derivation rules, safety constraints, and completion evidence.

The executor derives dynamic repository facts only from the authoritative sources named by that contract. Chat/terminal text is never an alternative authority.

The executor MUST NOT attempt to load the Operational Contract from an older task/topic branch merely because that branch is currently checked out. D042 requires canonical remote freshness before `AGENTS.md`/contract load.

Post-integration cleanup MUST NOT create a new implementation scope, modify repository content, reopen acceptance, or invent another Task Contract.

## Completion invariant

```text
integrated change != operationally closed change
operational closure = integrated change + verified post-integration branch retirement
```

If cleanup cannot be performed safely from the persisted contract and referenced Git/GitHub evidence, return `BLOCKED` or `PARTIAL`; do not compensate with chat-only instructions.
