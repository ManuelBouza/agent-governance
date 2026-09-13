---
name: durable-work-checkpoint
description: Persist the minimum authoritative work frontier needed for safe cold resumption across sessions, agents, hosts, or context boundaries, including exact controlling identities, blockers, next permitted action, minimum load, and fail-closed mismatch handling. Do not use for conversation summaries, ordinary notes, transient scratch state, one-off status queries, evidence provenance itself, or executor launch packaging itself.
---

# Durable Work Checkpoint

Use when material work must be resumable without private conversational memory.

## Trigger

Activate when a later session/agent/host must reconstruct an exact current frontier, when remote artifacts may have advanced, when continuation requires explicit blockers/next action/minimum load, or when closure is unsafe until continuation-critical state is durable.

Do not activate for transcript summaries, ordinary notes, transient scratch state, status queries with no future continuation, research provenance itself, or executor launch/transport packaging itself.

## Workflow

1. Identify the authoritative persistence surface and bounded work-unit identity.
2. Record the last completed coherent outcome and controlling references.
3. Record active remote artifacts, blockers, explicit next permitted action/ordered sequence, minimum successor load, and safety guards.
4. Reference authority instead of duplicating it.
5. Require the successor to compare expected identities with current canonical state.
6. Fail closed on material mismatch, missing controlling state, or unavailable active artifacts.
7. Refresh the frontier after coherent state transitions that change what may happen next.

## Postcondition

A fresh compatible agent can determine from durable authority alone what work is active/completed, what controls now, what to load, what is blocked, what action is permitted next, and whether observed state contradicts the persisted frontier.

## Authority boundary

A checkpoint is routing state, not superior authority. This Skill cannot guess through mismatches or invent domain lifecycle semantics.

For Agent Governance, D027/D067/D080, `docs/orchestrator/CHECKPOINT.md`, Oxxx fields, exact bootstrap order, Task Contract/branch/handoff conventions, and Human gates remain Maintainer-domain policy.
