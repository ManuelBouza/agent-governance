# D072 — Codex coordinator title instruction

Status: ACCEPTED  
Date: 2026-09-07  
Authority: Human Owner / ChatGPT Orchestrator  
Scope: Human-visible Codex coordinator title for Agent Governance source-product work  
Refines: D055, D058, D060, D071  
Preserves: Git authority, Executor ownership, Task Contract authority, D069/D070 closure

## Problem

D058 defines a deterministic Human-visible `Coordinator-ID`, and D071 requires ChatGPT to render the complete copy/paste-ready Codex transport prompt. The current transport shape still leaves one operational ambiguity: the launch card can carry the coordinator name without the prompt itself explicitly instructing Codex to use that exact name as the visible chat title.

That ambiguity permits a launch where the correct governance identity exists only outside the Codex conversation, increasing navigation errors and making same-task continuity harder to verify visually.

OpenAI documentation confirms that Codex conversations have visible chat titles, but current public documentation does not establish that a Codex agent can always rename its own chat programmatically from inside the conversation. Therefore Agent Governance must require an exact title instruction without claiming an unsupported rename capability.

## Decision

For every Codex launch or continuation while D072 controls, the complete transport prompt SHALL include the exact `Coordinator-ID` and an explicit title instruction near the top of the prompt.

Required semantic form:

```text
Coordinator-ID: <exact deterministic coordinator id>

Set the visible Codex chat title to exactly:
<exact deterministic coordinator id>

If the current Codex surface does not expose a supported way for you to set or rename the chat title from within this session, do not claim success. State exactly:
CHAT_TITLE_ACTION_REQUIRED: <exact deterministic coordinator id>
so the Human can apply the title in the UI, then continue under the same Coordinator-ID.
```

The exact wording may vary only if it preserves all of these semantics:

1. the coordinator identity is stated verbatim;
2. Codex is explicitly instructed to use it as the visible chat title;
3. Codex must not pretend the rename succeeded when the host does not expose that capability;
4. the exact fallback token `CHAT_TITLE_ACTION_REQUIRED: <Coordinator-ID>` is emitted when Human UI action is required;
5. inability to rename is navigation metadata, not a Stage 6 technical blocker unless a controlling experiment explicitly makes the visible title material.

## Human launch responsibility

D071 remains controlling: the Human performs the cross-product Codex UI/session transition.

When the UI exposes a title/rename control before execution, the Human SHOULD set the visible title to the exact `Coordinator-ID` directly. The prompt must still carry the same explicit title instruction so the Codex session itself receives and preserves the coordinator identity.

If Codex emits `CHAT_TITLE_ACTION_REQUIRED: ...`, the Human applies that exact title in the UI when supported and does not create a new coordinator merely because the rename had to be manual.

## NEW and CONTINUE semantics

For `NEW`:

- the launch card states the exact new `Coordinator-ID`;
- the transport prompt repeats it and explicitly requests that exact visible title.

For `CONTINUE`:

- the same `Coordinator-ID` is repeated in the continuation prompt;
- Codex is instructed to preserve the existing visible title exactly;
- an unexpected title mismatch is reported rather than silently creating a new root.

D060 still controls when `root-2+` failover is legitimate.

## Prompt completeness rule

A Codex transport prompt is incomplete under D072 if it contains only a launch-card `Coordinator-ID` outside the prompt but no explicit in-prompt title instruction.

Pointing to a persisted review that contains the title is also insufficient for Human-facing launch completeness. D071 still requires the complete prompt to be rendered to the Human, and D072 requires that rendered prompt to carry the title instruction itself.

## Evidence and authority

The visible chat title remains navigation metadata, not Git authority. A correct title does not prove task identity, branch ownership, freshness, or acceptance. Git, persisted Task Contracts/reviews, remote branch state and handoff evidence remain controlling.

Conversely, failure of the host to expose agent-driven rename does not invalidate otherwise correct Stage 6 execution. The required behavior is truthful fallback to `CHAT_TITLE_ACTION_REQUIRED`, not fabricated rename success.

## Consequences

- every Codex prompt carries its coordinator identity inside the conversation itself;
- the Human can visually distinguish roots/work units consistently;
- Codex is explicitly asked to use the deterministic governance name rather than relying on automatic title generation;
- unsupported agent-driven rename capability is handled truthfully and predictably;
- future checkpoints and launch reviews must propagate D072 for every Codex launch/continuation.
