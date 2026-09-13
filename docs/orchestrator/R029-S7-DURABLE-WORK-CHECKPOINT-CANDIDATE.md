# R029-S7 — `durable-work-checkpoint` Candidate Evaluation

Status: COMPLETE  
Parent: `R029 — AGENTS.md / Skill Architecture Refactor Research`  
Subtask: `R029-S7 — durable-work-checkpoint candidate`  
Baseline-Develop: `661c4edb17b7ed7c12de7acd7c6fe9fd21363c6c`  
Inputs: accepted R029-S1 through R029-S6 artifacts; D027; D067; `docs/ORCHESTRATOR-CHECKPOINTS.md`  
Decision-State: EVALUATING  
Normative-Effect: none  
Analytical-Disposition: `KEEP_CANDIDATE`

## Purpose

Evaluate whether durable cold-start/frontier persistence is a reusable transverse capability distinct from Agent Governance's source-maintenance checkpoint schema and ChatGPT chat lifecycle. This artifact evaluates a candidate only; it does not create or adopt a Skill.

## Reusable semantic intent

The reusable intent is:

> Persist the minimum authoritative frontier required for a later agent/session to resume a bounded work unit safely without private conversational memory, while detecting stale or contradictory continuation state before mutation.

This intent survives removal of Agent Governance-specific paths, D027/D067 state names, ChatGPT chat semantics, `Oxxx` sequences, Task Contract conventions and source-product lifecycle rules.

The capability is not a transcript/summarization mechanism. It is a compact durable routing and resumption contract.

## Positive triggers

Activate/evaluate this capability when:

- material work spans sessions, agents, hosts or context boundaries;
- private conversation/history cannot be assumed available or authoritative;
- a later continuation needs an exact current frontier, blockers and next permitted action;
- remote branches/PRs/contracts/handoffs may have advanced and must be revalidated before mutation;
- a work unit must be resumable from durable state alone;
- closure/hand-off is unsafe unless all continuation-critical facts are persisted.

## Negative triggers / anti-triggers

Do not activate merely for:

- summarizing a conversation for convenience;
- ordinary notes or meeting minutes;
- transient scratch state with no later execution consequence;
- repository status queries that need no future continuation;
- evidence provenance itself (S6 owns that semantic intent);
- executor launch/transport packaging itself (S8 owns that semantic intent).

## Host-neutral contract

### Inputs

A generic implementation needs:

- authoritative persistence surface and current identity/version;
- current bounded work-unit/objective identity;
- last completed coherent outcome;
- controlling references needed for continuation;
- active remote artifacts when applicable;
- unresolved blockers/questions;
- one explicit next permitted action or immediate ordered sequence;
- minimum load needed by a successor;
- explicit prohibitions/guards when omission could cause unsafe continuation.

### Required behavior

The capability should:

1. persist frontier facts, not transcript history;
2. reference durable controlling artifacts rather than duplicate them;
3. identify the current authoritative baseline and active artifacts;
4. express unresolved blockers and the exact next permitted action;
5. provide bounded minimum-load routing for cold start;
6. require a successor to compare expected frontier identities with current authoritative state;
7. fail closed on material mismatch, missing controlling state or unavailable active artifacts;
8. refresh the durable frontier when a coherent state transition changes what may happen next.

### Postcondition

A fresh compatible agent/session can determine, from durable authoritative state alone:

- what work unit is active or just completed;
- what state controls now;
- what must be loaded next;
- what is blocked or unresolved;
- what action is permitted next;
- whether observed current state contradicts the persisted frontier.

No prior private chat memory is required for correctness.

## Fail-closed boundary

The candidate does not authorize a successor to guess through a discrepancy.

If authoritative state materially disagrees with the persisted frontier, the capability should produce a bounded mismatch/block result and require reconciliation under the governing domain policy before new mutation.

The authoritative system remains authoritative; a checkpoint is routing state, not superior authority.

## Agent Governance adapter boundary

The following remain Agent-Governance-specific and MUST NOT become generic candidate semantics:

- D027 source-product ChatGPT checkpoint authority;
- D067 one-Human-objective-per-chat lifecycle and predecessor/successor states;
- `docs/orchestrator/CHECKPOINT.md` path and Markdown ownership;
- `Checkpoint-Sequence: Oxxx` convention;
- exact `Checkpoint-State`, `Chat-Closure`, `Next-ChatGPT-Effort` and `Next-Execution-Shape` fields;
- exact `Next-Chat-Minimum-Load` schema and source-maintenance bootstrap ordering;
- D066 Library snapshot references;
- Agent Governance Task Contract, handoff, PR and branch naming conventions;
- source-vs-consumer distinction and prohibition on using consumer `.agent-coordination/` state in this source repository;
- Human Owner selection gates and same-chat R029 session sequence.

Agent Governance may invoke the generic capability through these adapters, but these policies remain repository/domain authority.

## Relationship to adjacent candidates

- S6 `research-evidence-traceability` answers whether consequential evidence can be reconstructed and trusted; S7 answers whether the **work frontier** can be resumed safely.
- S8 `executor-launch-handoff` will evaluate preparation/transport of executable delegated work; S7 only preserves the durable frontier that may point to such a handoff.
- S4 `repository-change-control` governs mutation path safety; S7 may reference that path but does not own repository mutation policy.

## Host portability

The semantic contract is host-neutral. ChatGPT, Codex/Executor or another compatible agent may use different APIs, files, databases or repository mechanisms to read/write the durable frontier.

Host adapters own transport and persistence mechanics. They do not alter frontier semantics or create authority.

## Disposition

`KEEP_CANDIDATE`

Rationale:

- the intent is coherent outside Agent Governance;
- it has clear positive/negative triggers;
- it has a concrete cold-start/resumption postcondition;
- it is distinct from evidence traceability, repository change control and executor handoff;
- it supports fail-closed continuation across session/context boundaries;
- Agent Governance-specific lifecycle/schema details can remain cleanly adapter-side.

This disposition is analytical only. It does not approve a Skill name, package, implementation, installation, routing policy or final topology.

## S7 completion gate

Satisfied:

- generic durable-resume semantics separated from D027/D067/checkpoint policy;
- reusable intent and trigger boundary explicit;
- authority and fail-closed boundary explicit;
- host-neutral semantics separated from adapters;
- analytical disposition assigned;
- no root rewrite, Skill implementation, Executor/provider/model call, normative adoption or T066 mutation occurred.
