# D073 — Codex prompt-driven coordinator title adoption

Status: ACCEPTED  
Date: 2026-09-07  
Authority: Human Owner / ChatGPT Orchestrator  
Scope: current Codex adapter launch/continuation presentation for Agent Governance source-product work  
Refines: D039, D055, D058, D060, D071, D072  
Preserves: Git authority, Task Contract authority, Executor ownership, coordinator identity semantics, Human-mediated Codex transport

## Context

D058 defines the deterministic Human-visible coordinator identity:

```text
AG | <repo> | <work-unit> | root-<n>
```

D071 establishes Human-mediated ChatGPT -> Codex transport, and D072 requires every Codex transport prompt to state the exact `Coordinator-ID`, explicitly request that Codex use it as the visible chat title, and fall back truthfully to `CHAT_TITLE_ACTION_REQUIRED` when the active surface cannot perform the rename.

D072 was deliberately conservative because public product documentation did not establish that a Codex agent could reliably rename its own visible chat from inside the conversation.

During the T061 MG1-v14 launch on 2026-09-07, the Human Owner applied the R21 prompt on the current ChatGPT desktop / Codex / native Windows surface and reported that the exact instruction worked as intended: the Codex conversation adopted the requested coordinator title `AG | agent-governance | T061 | root-2`.

This is direct operational evidence for the current adapter surface. It is not a claim that every future Codex version or every other Executor supports the same behavior.

## Decision

For the current Codex adapter, **prompt-driven visible coordinator titling is the standard launch behavior**.

Every Codex `NEW` or `CONTINUE` transport prompt SHALL carry the exact deterministic `Coordinator-ID` near the top and SHALL directly instruct Codex to set or preserve the visible chat title to that exact value.

Canonical semantic form:

```text
Coordinator-ID: AG | <repo> | <work-unit> | root-<n>

Set the visible Codex chat title to exactly:
AG | <repo> | <work-unit> | root-<n>
```

For `NEW`, `Set` is the normal verb. For `CONTINUE`, the prompt SHOULD instruct Codex to preserve the same visible title and report an unexpected mismatch rather than silently creating a new coordinator identity.

The D072 fallback remains mandatory:

```text
CHAT_TITLE_ACTION_REQUIRED: <Coordinator-ID>
```

If the active Codex surface cannot set or rename the title from within the session, Codex must emit that exact fallback instead of claiming success. The Human may then apply the title in the UI. This fallback is compatibility behavior, not the normal expected path on the currently validated surface.

## Standard launch-card relationship

The Human-facing launch card and the in-prompt coordinator identity SHALL agree exactly.

Example:

```text
Executor: Codex
Session: NEW
Coordinator-ID: AG | agent-governance | TNNN | root-1
Model: <selected model>
Effort: <selected effort>
```

The prompt then repeats that same coordinator identity and requests that exact visible title.

The title remains navigation metadata. It does not replace branch, worktree, Task Contract, review, checkpoint or handoff identity.

## Implementation requirement

The source-product Codex launch guidance SHALL encode this behavior generically rather than requiring task-specific launch reviews to rediscover it.

At minimum:

1. `docs/EXECUTOR-LAUNCH-PROFILES.md` SHALL identify D071/D072/D073 as controlling Codex transport/title guidance;
2. its canonical Codex transport shape SHALL include the exact `Coordinator-ID` and title instruction block;
3. its `NEW` and `CONTINUE` examples SHALL preserve the same identity semantics;
4. `AGENTS.md` SHALL expose the D071/D072/D073 invariant at the source-product operating-model level so a fresh Orchestrator bootstrap cannot omit it;
5. checkpoints/reviews may specialize the exact coordinator value but MUST NOT weaken the generic rule.

No executable code is required for this adoption because the behavior is implemented through the Human-mediated launch prompt and Codex host conversation itself.

## Evidence classification

The T061 observation is **Human-observed adapter evidence** under the D039 learning loop.

It supports promoting prompt-driven titling from an uncertain capability attempt to the current adapter default, while preserving the fallback because:

- the observation covers one current host/product surface rather than every future Codex build;
- coordinator title is operational navigation metadata, so fail-closed execution blocking would be disproportionate;
- the explicit fallback preserves truthful behavior if the capability regresses or differs on another supported host.

No T061 scientific result, candidate qualification or Stage 6 acceptance claim is derived from this naming observation.

## NEW semantics

For a new coordinator root:

```text
Session: NEW
Coordinator-ID: AG | <repo> | <work-unit> | root-<n>
```

The prompt SHALL request that exact visible title before substantive task execution.

`root-1` remains the first root for a work unit. `root-2+` remains D060 failover only.

## CONTINUE semantics

For a recoverable same-task coordinator:

```text
Session: CONTINUE
Coordinator-ID: <same existing coordinator id>
```

The continuation prompt SHALL restate the same identity and instruct Codex to preserve that visible title. A title mismatch does not by itself create authority to allocate a new root.

## Consequences

- the exact `AG | <repo> | <work-unit> | root-<n>` identity becomes visible consistently in the Codex conversation itself;
- the Human no longer depends on automatic host-generated titles for task navigation;
- future Codex prompts do not need a task-specific discovery step for naming;
- D072's fallback remains available for capability regression or unsupported surfaces;
- naming success does not become acceptance evidence or change Git authority;
- this adoption does not modify or interrupt the currently running T061 scientific execution.
