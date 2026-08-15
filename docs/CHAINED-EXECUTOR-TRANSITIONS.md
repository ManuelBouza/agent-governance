# Chained Executor Transitions

Status: ACTIVE  
Controlled by: D045

## Purpose

Define the bounded source-maintenance procedure that allows one executor invocation to complete a deterministic Operational Contract and, without a Human acknowledgement round-trip, continue into exactly one already-authorized Task/rework stage.

This procedure reduces transport friction only. It does not merge contract scopes, weaken receipts, or transfer Governance acceptance authority.

## Core invariant

```text
one invocation != one authority

Stage A authority = integrated Operational Contract
Stage B authority = integrated Task Contract + optional integrated review
continuation authority = explicit D045 continuation section in Stage A

receipt != acceptance
continuation != integration
```

## Required Stage-A continuation section

A chained Operational Contract MUST contain a `## Preauthorized continuation` section with all of these fields:

- `Mode: D045_CHAIN`
- `Next contract: docs/tasks/TNNN-...md`
- `Next review: docs/reviews/TNNN-RN.md | none`
- `Continuation branch: <expected existing/new Task topic branch as defined by Task authority>`
- `Continuation eligibility:` explicit deterministic conditions
- `Continuation stop conditions:` explicit fail-closed conditions
- `Final interactive response:` `STAGE_A` on no-continuation, `STAGE_B` after continuation

The section MUST point to existing durable authority; it MUST NOT duplicate or rewrite Task/review semantics.

## Pre-launch requirements

Before ChatGPT launches a chained run:

1. D045 and this procedure are integrated in `develop`.
2. Stage-A Operational Contract is integrated and `READY`.
3. Stage-B Task Contract is integrated and executable under its lifecycle state.
4. If Stage B is rework, the exact durable review/rework record is integrated.
5. Stage A names a durable receipt anchor.
6. No Human/Orchestrator-owned decision, acceptance, Markdown, release, MG, or architecture gate sits between Stage A and Stage B.
7. Stage-B work remains isolated to its authorized topic branch until later Orchestrator review.

## Canonical launch transport

The initiating prompt remains an Operational-Contract bootstrap only:

```text
Operate as the Agente de IA Ejecutor for <owner>/<repository>.

Synchronize the canonical remote and ensure the local develop baseline used for bootstrap is current with origin/develop. Preserve local/uncommitted work; if a safe current baseline cannot be established, stop and report BLOCKED rather than using stale repository state.

Then load and execute the authoritative Operational Contract:
<operation-contract-path>

Treat that Operational Contract and its referenced repository policies as the complete operation and transition specification. Do not infer, supplement, or expand scope from this prompt.

If the contract declares a D045 preauthorized continuation, follow it exactly. Otherwise use normal Operational Contract completion behavior.
```

No task path, review path, branch, SHA, cleanup target, or continuation condition may be supplied in chat as an alternative authority.

## Stage A execution

The executor performs Stage A exactly under the Operational Contract.

Before first mutation, normal durable-receipt capability checks still apply.

After operation verification and before any Stage-B work, the executor MUST:

1. publish the complete normal Stage-A durable receipt to the configured anchor;
2. ensure the receipt reports `STATUS: DONE`;
3. verify every Stage-A continuation eligibility condition;
4. verify no continuation stop condition is present.

If any of those steps fails, Stage B MUST NOT start.

## Stage B bootstrap

Only after Stage A is eligible to continue:

1. synchronize/fetch the canonical remote again;
2. establish a safe local baseline current with `origin/develop`;
3. confirm that baseline contains the exact `Next contract` and, when specified, `Next review`;
4. preserve local/uncommitted work;
5. load the Task Contract and optional review directly from that canonical baseline;
6. execute only the Stage-B scope authorized there.

The Stage-A contract may identify the continuation pointer but must not restate Task acceptance criteria, rework details, implementation methods, or filenames already controlled by Stage-B authority.

## Final interactive response

If Stage A stops with `BLOCKED`, `PARTIAL`, or any continuation-precondition failure, return only the Stage-A completion response.

If Stage B executes, return only the normal Stage-B Task response:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: <path>
BRANCH: <branch>
HEAD: <pushed-commit-sha>
```

The Stage-A completion remains reconstructable from its durable GitHub receipt and does not need Human relay.

## Orchestrator review after a successful chain

When the Human signals that the executor invocation ended, ChatGPT MUST independently review both stages before accepting Stage B:

1. read Stage-A durable receipt directly from GitHub;
2. independently verify GitHub-observable Stage-A postconditions;
3. verify Stage-B branch/base/head/handoff/diff/evidence under the Task Contract/review;
4. reject or require rework if Stage A was not actually valid, even if Stage B is technically correct;
5. only then perform normal Stage-B acceptance/integration.

The chain therefore optimizes execution latency/relay friction, not Governance review.

## Ineligible transitions

Do not chain when the next step is:

- a new or revised Task Contract not yet integrated;
- a ChatGPT-owned Markdown change;
- a Decision/MG/release gate;
- Human risk/architecture approval;
- `main` promotion or release publication;
- an operation whose postcondition requires qualitative judgment;
- a permission/provider/secret/configuration transition requiring fresh authorization;
- any stage that would need chat-carried missing semantics.

## Audit requirement

A cold reviewer must be able to reconstruct from Git/GitHub alone:

- both stage authorities;
- why continuation was allowed;
- Stage-A durable receipt;
- Stage-B handoff;
- exact branch/base/head identities;
- the fact that no Human acknowledgement was required between stages.
