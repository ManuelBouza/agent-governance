# D071 — Human-mediated Codex transport boundary

Status: ACCEPTED  
Date: 2026-09-07  
Authority: Human Owner / ChatGPT Orchestrator  
Scope: ChatGPT Orchestrator -> Codex launch transport for Agent Governance source-product work  
Refines: D055, D058, D060, D068  
Preserves: Executor ownership, Task Contract authority, Git authority, D069/D070 response closure

## Problem

Agent Governance already separates persisted execution authority, Human-facing launch metadata, and the minimal Executor transport prompt. The existing wording, however, left one operational boundary ambiguous: it did not state strongly enough that ChatGPT Orchestrator cannot directly start, continue, or control a Codex Executor session.

That ambiguity creates two failure modes:

- ChatGPT may waste effort searching for a plugin/tool/transport that could invoke Codex directly even though Codex launch is Human-mediated in this workflow;
- after a launch gate is authorized, ChatGPT may tell the Human only to use a prompt persisted in Git instead of rendering the complete copy/paste-ready prompt that the Human must actually give to Codex.

Both behaviors are launch-quality defects. They do not change Executor authority or Stage 6 semantics, but they make the Human transport step unnecessarily ambiguous.

## Decision

For the Codex adapter used by Agent Governance source-product orchestration, **ChatGPT Orchestrator SHALL NOT attempt to start, continue, invoke, control, or otherwise operate the Codex session directly**.

Codex launch is always **Human-mediated** unless a later explicit Human-accepted decision supersedes D071.

For this adapter, the word `launch` means:

```text
ChatGPT verifies/persists launch authority
        -> ChatGPT emits the Human-facing launch card
        -> ChatGPT emits the complete copy/paste-ready Codex transport prompt
        -> Human opens/selects the required Codex NEW or CONTINUE session
        -> Human configures the stated model/effort/host requirements
        -> Human pastes the prompt into Codex
        -> Codex executes and publishes required Git evidence
        -> Human returns the terminal STATUS/HANDOFF/BRANCH/HEAD to ChatGPT
        -> ChatGPT verifies remote Git and resumes Orchestrator convergence
```

ChatGPT authorization of Stage 6 is therefore **not** an attempt to invoke Codex. It is preparation of the exact Human-mediated handoff.

## Mandatory Human-facing launch response

After the Human selects/authorizes a Codex execution objective and the required launch gate is persisted, the same ChatGPT response SHALL include both:

1. the complete launch card, including `Executor`, `Session`, `Coordinator-ID`, `Model`, `Effort`, and any material host/CLI requirement; and
2. the **complete transport prompt**, ready for the Human to copy and paste into Codex.

It is insufficient to respond only with wording such as:

```text
use the prompt persisted in docs/reviews/...
```

or otherwise require the Human to open Git merely to recover the prompt that ChatGPT already owns as part of the launch handoff.

The persisted review/gate remains canonical authority. Rendering the prompt in the Human-facing response is transport convenience and must preserve the persisted wording/semantics.

## No direct-transport discovery during Codex launch

Normal Codex launch handling SHALL NOT search the plugin directory, connector catalog, or other ChatGPT tools for a general Codex execution transport.

The Orchestrator must not treat integrations such as OpenAI documentation/developer tools, Codex Security, or unrelated connectors as potential substitutes for the Human-operated Codex session.

A future product capability does not silently invalidate this rule. Direct ChatGPT-to-Codex invocation may be adopted only through a later explicit Human-accepted decision that supersedes or narrows D071.

## Launch-state vocabulary

When a Codex launch gate is authorized but the Human has not yet started/prompted Codex, the preferred state is:

```text
AUTHORIZED_AWAITING_HUMAN_CODEX_START
```

This state means:

- the execution authority exists;
- ChatGPT has completed its launch preparation responsibility;
- the Human transport step is next;
- no Executor execution evidence is yet claimed.

Do not characterize this normal state as a missing-tool or missing-plugin blocker.

## Executor return boundary

ChatGPT SHALL resume only from terminal Executor output supplied by the Human and backed by remote Git evidence.

For normal Task Contract execution this remains the compact terminal shape required by the active authority, typically:

```text
STATUS: <COMPLETED|BLOCKED>
HANDOFF: <persisted handoff path>
BRANCH: <represented branch>
HEAD: <remote pushed HEAD sha>
```

Chat-only Executor prose is not acceptance evidence. Existing Git/handoff verification rules remain controlling.

## Interaction with D055/D058/D060

D055 still controls model/effort/session recommendations. D058 still controls deterministic coordinator naming/worktree hygiene. D060 still controls same-task coordinator continuity/failover.

D071 adds only the transport invariant:

- ChatGPT prepares and renders the handoff;
- the Human performs the Codex UI/session transition;
- Codex performs Stage 6 execution;
- ChatGPT later verifies remote evidence.

`NEW` and `CONTINUE` therefore describe what the Human must select in Codex, not an action ChatGPT performs on the Codex host.

## Interaction with D068

D068 Stage 6 ownership is unchanged. The Executor still owns Execute / Diagnose / Repair / Verify after the Human delivers the authorized prompt.

D071 does not make the Human a terminal operator for Executor mechanics. The Human's role is only the unavoidable cross-product transport step: select/configure the Codex session and paste the Orchestrator-supplied prompt. Once Codex begins, D054 execution mechanics remain Executor-owned.

## Consequences

- ChatGPT will no longer search for or speculate about a direct Codex invocation channel during normal Agent Governance launches.
- Every authorized Codex launch response will provide the complete prompt the Human needs immediately.
- `AUTHORIZED_AWAITING_HUMAN_CODEX_START` becomes the normal post-authorization/pre-execution state for Codex.
- The persisted gate remains canonical while the visible prompt is a faithful transport copy.
- A future direct-invocation capability cannot silently change this workflow; a new Human-accepted decision is required.
