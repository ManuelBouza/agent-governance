---
name: durable-work-checkpoint
description: Use when material work must resume safely across sessions, agents, hosts or context boundaries from durable authority and stale or contradictory continuation state must fail closed. Do not use for conversation summaries, ordinary notes, transient scratch state or one-time status queries.
---

# Durable work checkpoint — evaluation fixture

Intent: persist the minimum authoritative frontier required for safe later continuation without private conversational memory.

Required behavior:
- persist frontier facts, not transcript history;
- reference controlling durable artifacts rather than duplicating them;
- identify current work identity, baseline, blockers and exact next permitted action;
- provide bounded minimum-load routing;
- require the successor to compare expected identities with current authoritative state;
- fail closed on material mismatch, missing controlling state or ambiguous active artifacts.

Anti-triggers: convenient summaries, meeting notes, transient scratch state, one-time status inspection, evidence provenance itself, or executor launch packaging itself.

Postcondition: a fresh compatible session can reconstruct what controls now, what is blocked, what may happen next, and whether observed current state contradicts the saved frontier. The authoritative system remains stronger than the checkpoint.
