# D048 — Normal-task single final push boundary

Status: ACCEPTED  
Date: 2026-08-15  
Scope: executor remote-publication timing for normal source-product tasks

## Problem

T031 exposed an ambiguity in the existing executor lifecycle. Repository policy defined the normal order as implementation -> verification -> handoff -> push -> visible completion response, but it did not state strongly enough whether an executor could publish an intermediate task-branch state to the canonical remote before the normal final publication boundary.

During T031, an intermediate handoff commit with `status = PARTIAL` was pushed before the final `DONE` handoff successor. The remote publication remained confined to the task branch and did not mutate `develop`, but the intermediate publication was not an explicitly contracted checkpoint.

The gap is process-policy precision, not an implementation-acceptance defect and not individual blame.

## Decision

For a **normal executor task** whose execution remains in progress toward its intended completion status, the canonical remote topic branch MUST NOT be pushed as an intermediate progress checkpoint unless the controlling Task Contract or referenced workflow explicitly authorizes that remote checkpoint.

The normal publication sequence is:

```text
local implementation
    -> required verification
    -> final implementation/test/eval commit
    -> final handoff candidate
    -> handoff/finalization commit
    -> one planned final push of the complete topic-branch state
    -> remote HEAD verification
    -> visible DONE/BLOCKED/PARTIAL response
```

The rule is a **single planned final push boundary**, not a prohibition on all later corrective Git activity. If Orchestrator review subsequently requires rework, or a post-push handoff-only defect is discovered, a later authorized corrective push may occur on the same task branch under the normal review/rework rules.

## Explicit exceptions

A pre-completion remote push is allowed only when at least one of the following is true:

1. the controlling Task Contract/workflow explicitly requires an intermediate remote checkpoint, such as an RF1 characterization checkpoint awaiting Orchestrator approval; or
2. execution is terminating with `BLOCKED` or `PARTIAL` as the actual returned task outcome and a remotely auditable handoff can be safely persisted before that terminal response.

Merely having a handoff JSON whose status field says `PARTIAL` does not create an implicit checkpoint authorization while the executor is still continuing the same invocation toward `DONE`.

## Rationale

Keeping normal work local until the final publication boundary:

- reduces ambiguous remotely visible candidate states;
- prevents an intermediate handoff from looking like the current review candidate while execution still continues;
- reduces stale handoff/HEAD combinations;
- minimizes unnecessary permission prompts and remote mutations;
- preserves GitHub as the durable review surface without turning it into a scratch-progress transport.

This does not reduce auditability: the complete task state remains pushed before the executor reports its terminal status.

## Enforcement boundary

This decision is immediately normative in `docs/TASK-CONTRACTS.md` and `docs/EXECUTOR-HANDOFFS.md`.

A future deterministic control MAY detect unexpected pre-final publication where the executor host exposes sufficient observable state, but no automation may infer private execution progress or become acceptance authority merely to enforce this rule.

## Compatibility

Existing accepted task history is not rewritten. T031's intermediate push is retained as normal Git history; no reset, force-push, or history deletion is authorized.
