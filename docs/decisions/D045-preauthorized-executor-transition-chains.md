# D045 — Preauthorized executor transition chains

Status: ACCEPTED  
Decision owner: Human Owner  
Applies to: source-maintenance executor workflow transitions between a bounded Operational Contract and already-authorized executor Task/rework work

## Context

Agent Governance currently separates post-integration repository cleanup from the next executable task. That separation preserves auditability, but it can create unnecessary Human relay friction when the cleanup is deterministic, its durable receipt is machine-persisted, and the next executor-owned task/rework authority is already fully integrated in Git.

The Human Owner identified the repeated acknowledgement step — “cleanup finished, now start the next task” — as avoidable transport friction.

The existing invariants remain valid:

```text
prompt = bootstrap transport only
receipt = durable execution evidence
receipt != Governance acceptance
Task/Operational Contract = execution authority
```

The problem is not missing authority. It is unnecessary interactive serialization between two already-authorized executor stages.

## Decision

Agent Governance SHALL support a narrow **preauthorized executor transition chain** for eligible source-maintenance flows.

A chain contains exactly two stages:

1. **Stage A — Operational Contract**: a bounded deterministic repository operation with its normal durable GitHub receipt;
2. **Stage B — executor work**: exactly one already-integrated Task Contract, optionally constrained by one already-integrated durable review/rework record.

The chain is authorized only when the Stage-A Operational Contract explicitly declares the Stage-B continuation according to `docs/CHAINED-EXECUTOR-TRANSITIONS.md`.

The initiating chat prompt still points to exactly one persisted Operational Contract. It MUST NOT carry the next task, branch, SHA, rework semantics, or continuation conditions.

## Authority semantics

Continuation is **preauthorized conditionally by Governance in Git**. It is not acceptance authority granted to the executor or to the operational receipt.

```text
persisted chain authorization + deterministic Stage-A PASS
    => executor may begin Stage B on an isolated topic branch

Stage-A receipt
    != Orchestrator closure
    != Task acceptance
    != integration authorization
```

ChatGPT still independently reads and verifies the Stage-A durable receipt when reviewing the final chain result. If Stage A was incorrectly reported as `DONE` or its observable invariants do not hold, Stage B cannot be accepted/integrated even if its implementation is otherwise correct.

This permits useful work to continue without a Human acknowledgement round-trip while preserving Governance acceptance authority at the integration boundary.

## Eligibility constraints

A transition chain is allowed only when all of the following are true before launch:

- both Stage-A and Stage-B authorities are already integrated into current `develop`;
- Stage A has fully deterministic continuation conditions and a durable receipt anchor;
- Stage B is executor-owned non-Markdown work under an existing Task Contract;
- if Stage B is rework, the exact durable review/rework authority is already integrated;
- no Human decision, architecture decision, acceptance review, release approval, Markdown-authoring gate, or unresolved scope decision is required between the stages;
- Stage B mutates only its authorized topic branch and cannot directly integrate to `develop`/`main`;
- the chain contains no release promotion, destructive long-lived-branch mutation, secret/configuration permission change, or other action whose safety depends on a fresh Human/Orchestrator judgment after Stage A.

If any intermediate judgment is required, the chain MUST stop after Stage A and normal orchestration resumes.

## Fail-closed continuation

Stage B may start only if Stage A:

- publishes its required durable receipt successfully;
- reports `STATUS: DONE`;
- satisfies every contract-defined deterministic postcondition visible to the executor;
- leaves all protected/canonical refs required by the chain unchanged;
- has no continuation-blocking exception.

`BLOCKED`, `PARTIAL`, receipt-publication failure, unexpected branch/ref drift, or any ambiguous postcondition stops the chain. The executor returns the Stage-A completion response and MUST NOT start Stage B.

Before Stage B, the executor MUST synchronize the canonical remote again, establish a safe current `origin/develop` baseline containing the declared Stage-B authority, preserve local/uncommitted work, and stop rather than guess if that baseline cannot be established safely.

## Interactive completion semantics

For a normal non-chained Operational Contract, existing completion semantics remain unchanged.

For a D045 chain only:

- Stage A always publishes its normal durable receipt before continuation;
- if Stage A does not continue, the interactive response is the normal Stage-A response;
- if Stage B runs, the final interactive response is the normal Stage-B Task response (`STATUS`, `HANDOFF`, `BRANCH`, `HEAD`);
- the Stage-A response need not be copied again interactively because its canonical durable receipt already exists.

This is a narrow exception to the convenience-copy expectation of `docs/OPERATION-CONTRACTS.md`; it does not weaken the durable-receipt requirement.

## Limits

- Maximum chain length is two stages. No recursive or open-ended executor pipelines.
- A chain cannot cross an Orchestrator-owned Markdown/decision/MG gate.
- A chain cannot make external/provider evidence Governance authority.
- A chain cannot auto-merge Stage B.
- A chain cannot convert `DONE` into acceptance.
- A chain cannot infer the next task from naming, chat history, or repository heuristics; the continuation pointer must be explicit in Git.

## Consequences

This removes the Human relay step for safe deterministic transitions while preserving:

- Git-only reconstructability;
- durable Operational receipts;
- Task/review scope authority;
- independent Orchestrator verification before acceptance/integration;
- fail-closed behavior when cleanup or freshness is uncertain.

The mechanism should be used where it reduces transport friction, not as a default excuse to create long autonomous pipelines.
