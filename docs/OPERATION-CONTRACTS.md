# Source Product Operational Contracts

Status: ACTIVE

## Purpose

Define the persistent instruction format used when ChatGPT Orchestrator delegates repository operations that are not implementation work and therefore do not belong in a normal Task Contract.

Examples include post-integration branch retirement and other bounded repository-maintenance actions that intentionally create no product/content implementation.

## Authority invariant

Every delegated executor action MUST be reconstructable from canonical Git without relying on chat/terminal prompt semantics.

```text
prompt = bootstrap transport only
persisted contract + referenced Git policy = complete instruction
```

A prompt MAY identify the repository, base branch, abstract executor role, exactly one persisted contract path, the canonical-remote freshness precondition, an optional D043 `AGENTS.md` reload when the governing integrated change modified that file, and the completion response shape. It MUST NOT carry operation-specific targets, branch names, SHAs, deletion decisions, commands, exceptions, or acceptance semantics that are absent from the persisted contract.

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
- exact minimal completion response schema.

Dynamic facts MAY remain dynamic only when the contract explicitly identifies the authoritative source and deterministic derivation rule. The prompt MUST NOT supply those facts as an alternative authority.

## Integration gate

An Operational Contract is executable only when:

1. ChatGPT authors it on a fresh policy-compliant Markdown branch from current `develop`;
2. the complete concrete instruction is reviewed;
3. the contract is integrated into `develop`;
4. its status is `READY`;
5. the executor synchronizes the canonical remote and establishes a safe local baseline equal to the current remote base branch containing that exact contract;
6. if the governing integrated change modified `AGENTS.md`, ChatGPT includes the D043 reload line and the executor reloads current `AGENTS.md` from that baseline;
7. the executor loads the Operational Contract from that current baseline.

If the executor cannot establish the current remote baseline without risking local/uncommitted work, it MUST stop/escalate rather than discard work or attempt to execute the contract from stale state. D042 defines this bootstrap-freshness rule.

Repository-level instructions remain authoritative. Under D043, compatible executor hosts load them natively; an explicit `AGENTS.md` read/reload is therefore omitted from normal launches and added only after a governing `AGENTS.md` change.

If the operation contract itself is integrated by a PR whose source branch must be retired by that same operation, ChatGPT MUST persist that PR identity into the Operational Contract before merge. This allows the executor to retire the contract-authoring branch without creating another recursive cleanup instruction.

## Freeze and revision

Once execution begins, the executor MUST NOT edit the Operational Contract. Material changes require a persisted ChatGPT revision integrated into `develop` before execution continues. Chat-only corrections are not valid operational authority.

## Canonical launch prompt

Normal form:

```text
Operate as the Agente de IA Ejecutor for <owner>/<repository>.

Synchronize the canonical remote and ensure the local <base-branch> baseline used for bootstrap is current with origin/<base-branch>. Preserve local/uncommitted work; if a safe current baseline cannot be established, stop and report BLOCKED rather than using stale repository state.

Then load and execute the authoritative Operational Contract:
<operation-contract-path>

Treat that Operational Contract and its referenced repository policies as the complete operation specification. Do not infer, supplement, or expand operation scope from this prompt.

Complete the contract-defined operation and verification, then return only the completion response defined by the Operational Contract.
```

If and only if the governing integrated change modified `AGENTS.md`, insert this line after the remote-freshness paragraph and before the contract pointer:

```text
AGENTS.md changed in the governing integrated change; reload current AGENTS.md from this baseline before loading the Operational Contract.
```

Normal substitutions are limited to repository identity, base branch, exactly one Operational Contract path, and the conditional D043 reload line when Git history requires it. The executor chooses the concrete compatible Git workflow used to establish the required remote freshness; the prompt does not prescribe implementation methodology or task-specific Git commands.

## Audit invariant

A reviewer must be able to reconstruct from Git/GitHub, without the initiating chat, what operation was authorized, why, which durable targets it covered, which safety rules controlled it, what evidence was required, what the executor reported, and what canonical state resulted.

If reconstruction requires prompt text beyond the contract pointer/bootstrap, the delegation is nonconforming.
