# Source Product Operational Contracts

Status: ACTIVE  
Controlling decision: `docs/decisions/D059-operational-receipt-and-terminal-transport-separation.md`

## Purpose

Define the persistent instruction format used when ChatGPT Orchestrator delegates repository operations that are not implementation work and therefore do not belong in a normal Task Contract.

Examples include post-integration branch retirement and other bounded repository-maintenance actions that intentionally create no product/content implementation.

## Authority invariant

Every delegated executor action MUST be reconstructable from canonical Git/GitHub without relying on chat/terminal prompt semantics or on the Human Owner reproducing executor output accurately.

```text
prompt = bootstrap transport only
persisted contract + referenced Git policy = complete instruction
executor receipt = durable detailed completion evidence
terminal response = compact convergence pointer only
```

A prompt MAY identify the repository, base branch, abstract executor role, exactly one persisted contract path, the canonical-remote freshness precondition, an optional D043 `AGENTS.md` reload when the governing integrated change modified that file, and the standard compact completion response shape. It MUST NOT carry operation-specific targets, branch names, SHAs, deletion decisions, commands, exceptions, or acceptance semantics that are absent from the persisted contract.

If concrete information is required to perform the operation safely or correctly, ChatGPT MUST persist it in the Operational Contract or a controlling Git policy before launch.

## Relationship to Task Contracts

Use exactly one persisted contract type per delegated action:

- `docs/tasks/TNNN-*.md` — implementation/test/refactor/release/infrastructure work that creates or changes authorized repository content and produces the normal executor handoff;
- `docs/operations/OPNNN-*.md` — bounded repository operations whose concrete instruction must be durable but which intentionally do not create another implementation scope or handoff commit.

An Operational Contract is not a second Task Contract and does not reopen accepted implementation scope.

## Location and identity

Operational Contracts live under `docs/operations/` and use stable IDs such as `OP001`.

## Required fields

Each Operational Contract MUST contain:

- Operation ID;
- Status: `DRAFT | READY | IN_PROGRESS | DONE | BLOCKED | CANCELLED`;
- operation type;
- authorized base branch/revision rule;
- objective/result;
- exact durable target identities required to derive the operation;
- controlling references;
- authorized operations;
- explicit exclusions;
- safety/precondition invariants;
- evidence/verification requirements;
- stop/escalation conditions;
- exact detailed durable-receipt schema;
- a durable GitHub receipt anchor identifying the PR or issue where the executor must publish the completion receipt.

The interactive completion response is not operation-specific. D059 fixes it to the standard compact terminal envelope defined below.

Dynamic facts MAY remain dynamic only when the contract explicitly identifies the authoritative source and deterministic derivation rule. The prompt MUST NOT supply those facts as an alternative authority.

## Durable executor receipt

Operational completion MUST NOT depend on the Human Owner copying the executor response from one chat or terminal into another.

Every READY Operational Contract executed under this policy MUST define a durable GitHub receipt anchor. Normally this is the merged PR that integrated the Operational Contract into `develop`; another repository-local PR or issue may be used only when the contract names it explicitly.

Before the first mutation, the executor MUST establish that the configured GitHub identity can publish a top-level comment to the receipt anchor. If it cannot establish that capability safely, it MUST stop before mutation and report `BLOCKED` through the available interactive channel.

After verification and before claiming `DONE`, the executor MUST publish one final top-level receipt comment to the configured anchor using the exact detailed envelope defined by the Operational Contract. The durable receipt contains all operation-specific status/reason, exception and evidence fields required for reconstruction and review.

A `DONE` claim is valid only when the durable receipt publication succeeded. If repository mutation completed but final receipt publication fails, the executor MUST report `PARTIAL` through the interactive channel, perform no broader compensating mutation, and preserve enough local evidence for recovery.

ChatGPT MUST read the durable receipt directly from GitHub before closing the operation. Human-relayed completion text is non-authoritative convenience transport and MAY be omitted, truncated, or malformed without losing the canonical receipt. The Human Owner therefore only needs to signal that the executor has finished; precise copy/paste of receipt fields is not required.

The receipt is execution evidence, not governance acceptance authority. ChatGPT still independently verifies all GitHub-observable acceptance criteria and treats local-only claims according to the contract.

## Standard interactive completion response

After successful durable receipt publication, the Executor returns only:

```text
STATUS: DONE | BLOCKED | PARTIAL
RECEIPT: <durable GitHub receipt URL>
COORDINATOR: <Human-visible coordinator name or n/a>
```

Rules:

- do not repeat the detailed receipt envelope in chat;
- operation-specific blocked reasons remain in the durable receipt while terminal `STATUS` is `BLOCKED`;
- if receipt publication fails after mutation, return `STATUS: PARTIAL` and `RECEIPT: unavailable`;
- `COORDINATOR` uses the D058 Human-visible coordinator identity when applicable, otherwise `n/a`.

This terminal response is navigation/transport only. It is not the detailed operation evidence surface.

## Integration gate

An Operational Contract is executable only when:

1. ChatGPT authors it on a fresh policy-compliant Markdown branch from current `develop`;
2. the complete concrete instruction is reviewed;
3. the contract is integrated into `develop`;
4. its status is `READY`;
5. its durable GitHub receipt anchor is resolvable from the integrated contract;
6. the executor synchronizes the canonical remote and establishes a safe local baseline equal to the current remote base branch containing that exact contract;
7. if the governing integrated change modified `AGENTS.md`, ChatGPT includes the D043 reload line and the executor reloads current `AGENTS.md` from that baseline;
8. the executor loads the Operational Contract from that current baseline.

If the executor cannot establish the current remote baseline without risking local/uncommitted work, it MUST stop/escalate rather than discard work or attempt to execute the contract from stale state. D042 defines this bootstrap-freshness rule.

Repository-level instructions remain authoritative. Under D043, compatible executor hosts load them natively; an explicit `AGENTS.md` read/reload is therefore omitted from normal launches and added only after a governing `AGENTS.md` change.

If the operation contract itself is integrated by a PR whose source branch must be retired by that same operation, ChatGPT MUST persist that PR identity into the Operational Contract before merge. The same merged PR MAY also be the durable receipt anchor because its conversation remains available after source-branch deletion. This allows the executor to retire the contract-authoring branch without creating another recursive cleanup instruction.

## Freeze and revision

Once execution begins, the executor MUST NOT edit the Operational Contract. Material changes require a persisted ChatGPT revision integrated into `develop` before execution continues. Chat-only corrections are not valid operational authority.

Completed operations remain governed historically by the contract revision that was integrated when they executed. A later policy refinement MUST NOT retroactively relabel a contract-conforming historical terminal response as an Executor defect.

## Canonical launch prompt

Normal form:

```text
Operate as the Agente de IA Ejecutor for <owner>/<repository>.

Synchronize the canonical remote and ensure the local <base-branch> baseline used for bootstrap is current with origin/<base-branch>. Preserve local/uncommitted work; if a safe current baseline cannot be established, stop and report BLOCKED rather than using stale repository state.

Then load and execute the authoritative Operational Contract:
<operation-contract-path>

Treat that Operational Contract and its referenced repository policies as the complete operation specification. Do not infer, supplement, or expand operation scope from this prompt.

Publish the contract-defined detailed durable GitHub completion receipt, then return only the standard compact interactive completion response from docs/OPERATION-CONTRACTS.md.
```

If and only if the governing integrated change modified `AGENTS.md`, insert this line after the remote-freshness paragraph and before the contract pointer:

```text
AGENTS.md changed in the governing integrated change; reload current AGENTS.md from this baseline before loading the Operational Contract.
```

Normal substitutions are limited to repository identity, base branch, exactly one Operational Contract path, and the conditional D043 reload line when Git history requires it. The executor chooses the concrete compatible Git/GitHub workflow used to establish freshness and publish the receipt; the prompt does not prescribe implementation methodology or task-specific commands.

## Audit invariant

A reviewer must be able to reconstruct from Git/GitHub, without the initiating chat and without Human copy/paste, what operation was authorized, why, which durable targets it covered, which safety rules controlled it, what detailed completion receipt the executor published, what ChatGPT independently verified, and what canonical state resulted.

If reconstruction requires prompt text beyond the contract pointer/bootstrap or Human-relayed executor output, the delegation is nonconforming.
