# D059 — Operational Receipt and Terminal Transport Separation

Status: ACCEPTED  
Date: 2026-09-05  
Authority: Human Owner / ChatGPT Orchestrator  
Refines: `docs/OPERATION-CONTRACTS.md`, D058  
Preserves: durable Git/GitHub authority, Human copy/paste independence, Task Contract terminal-output semantics

## Problem

Source-product Operational Contracts already require a durable GitHub receipt so operation completion can be reconstructed without depending on the Human Owner copying terminal output between chats.

However, the policy also required the Executor to mirror the same detailed receipt envelope back into the interactive chat. OP067 demonstrated that this creates redundant, noisy terminal output containing branch/worktree evidence that is already durable in GitHub.

That duplication has no authority benefit and is inconsistent with the established compact transport pattern used by executable Task Contracts, where the interactive response carries only the minimal pointer needed for Orchestrator convergence.

## Decision

Operational Contracts SHALL separate **durable completion evidence** from **interactive completion transport**.

### 1. Durable receipt

The operation-specific detailed completion envelope remains in the configured GitHub receipt anchor.

It contains the evidence fields required to reconstruct and review the operation, including operation-specific status/reason details, affected refs/worktrees/resources, retained/review items and any other contract-required evidence.

The durable receipt is the authoritative Executor completion record for the operation.

### 2. Interactive terminal output

After the durable receipt is successfully published, the Executor SHALL return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
RECEIPT: <durable GitHub receipt URL>
COORDINATOR: <Human-visible coordinator name or n/a>
```

The interactive response is convenience transport only. It must not mirror the detailed durable receipt.

Operation-specific blocked reasons remain in the durable receipt; the terminal `STATUS` intentionally collapses them to `BLOCKED`.

### 3. Receipt publication failure

If repository mutation completed but the durable receipt cannot be published, the Executor returns:

```text
STATUS: PARTIAL
RECEIPT: unavailable
COORDINATOR: <Human-visible coordinator name or n/a>
```

and performs no broader compensating mutation unless separately authorized.

### 4. Human transport independence

The Human Owner only needs to indicate that the Executor finished. ChatGPT Orchestrator SHALL read the durable receipt directly from GitHub before accepting/closing the operation.

No operation may require the Human Owner to relay the detailed completion envelope accurately.

### 5. Relationship to Task Contracts

D059 does not change executable Task Contract terminal output.

Task Contracts continue to use their contract-defined compact terminal pattern, normally:

```text
STATUS: DONE | BLOCKED
HANDOFF: <persisted handoff path>
BRANCH: <represented branch>
HEAD: <pushed head>
```

Operational Contracts use `RECEIPT` because they intentionally do not create a normal Executor handoff commit.

### 6. Historical OP067 treatment

OP067 executed under the then-integrated contract that explicitly required the detailed durable receipt envelope to be returned verbatim to the interactive caller.

Therefore OP067's full terminal block is **contract-conforming historical execution**, not an Executor defect.

D059 is prospective. OP067's executed completion semantics are not rewritten to pretend the compact terminal pattern controlled that run.

## Consequences

- GitHub remains the detailed operation-evidence surface;
- Executor chats remain concise and navigational;
- Human copy/paste is no longer redundantly encouraged by the terminal output;
- operation-specific evidence can grow without increasing interactive transport noise;
- Task Contract and Operational Contract terminal patterns remain distinct but structurally consistent: compact status plus one durable convergence pointer.
