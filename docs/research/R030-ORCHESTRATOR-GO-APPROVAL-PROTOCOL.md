# R030 — Orchestrator `go` Approval Protocol Research

Research-ID: R030  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-13  
Last-Reviewed: 2026-09-13  
Owner: ChatGPT Orchestrator  
Scope: ChatGPT Orchestrator Human-intent interpretation, proposal confirmation, approval token semantics, contextual refinement, freshness and fail-closed interaction boundaries  
Question: How should Agent Governance support a compact `go` interaction in which the Orchestrator first proposes its interpretation of a material Human request, `go` approves that exact proposal, and `go,<context>` approves while applying a bounded contextual delta without creating unsafe or ambiguous standing authority?  
Evaluation-Refs: none  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Executive conclusion

A `go` mechanism is compatible with the current Agent Governance architecture if it is modeled as a **proposal-bound, one-shot Human approval token**, not as a generic synonym for consent and not as standing authorization.

The recommended candidate protocol is:

```text
material Human prompt
    -> bounded read-only interpretation/context load
    -> concrete proposal
    -> PROPOSAL_PENDING

exact whole-message `go` (case-insensitive)
    -> revalidate proposal freshness
    -> approve latest pending proposal once
    -> execute

exact whole-message `go,<context>`
    -> apply context as a delta to latest pending proposal
    -> NON_MATERIAL delta: approve + execute without rewriting the proposal
    -> MATERIAL or uncertain delta: proposal becomes stale; re-propose and wait for a new `go`

any other Human prompt
    -> interaction/refinement/correction/question
    -> no approval
    -> update or replace proposal as needed
    -> wait for `go`
```

The design should be fail-closed: no pending proposal means `go` authorizes nothing; stale proposals are not silently resumed; duplicate `go` does not repeat an action; approval does not survive chat turnover; and untrusted/tool/web/repository content can never synthesize a valid Human `go`.

R030 is research evidence only. No `go` policy, parser, protocol migration, `AGENTS.md` change, Governance Core change, or implementation is authorized by this artifact.

## Problem framing

The Human Owner wants a low-friction confirmation loop that reduces repeated restatement while making Orchestrator interpretation visible before material work begins.

The desired interaction has three semantic classes:

```text
ordinary prompt
    -> "show me what you understood and intend to do"

`go`
    -> "yes, execute that proposal"

`go,<context>`
    -> "yes, but incorporate this bounded context while proceeding"
```

The hard part is not recognizing the string `go`. The governance problem is deciding **what object is being approved**, when that approval becomes stale, and how contextual additions interact with existing objective, authorization, safety, specification, Design and acceptance boundaries.

## Current project constraints

The candidate protocol must complement, not replace, existing controls.

- D067 keeps one explicit Human objective per ChatGPT Orchestrator chat. A pending proposal is not a second objective and `go` must not silently change objective identity.
- D080 controls `SINGLE_EXECUTION` versus `MULTI_EXECUTION`; `go` authorizes a proposal but does not redefine execution geometry.
- D081 allows in-scope Human adaptations only while objective, authority, specification/Design, safety and acceptance meaning remain materially unchanged. This is the natural boundary for `go,<context>`.
- D033 already establishes that Human approval should cover a coherent bounded operation rather than command-by-command mechanics, and that materially changed operations require refreshed authorization.
- D042/D067 require canonical freshness and fail-closed handling of stale authority. A chat proposal cannot outrank current Git.
- D057 requires this research to remain evidence until a separate accepted normative artifact adopts it.

## External evidence

### OpenAI Agents SDK human-in-the-loop pattern

Current OpenAI Agents SDK documentation models approval as a durable interruption bound to a specific pending operation. Execution pauses, the pending approval is surfaced, the caller approves or rejects, and the original run resumes from `RunState`. Approvals are associated with concrete call identities; malformed approval-rule arguments fail closed into manual approval. The SDK also recommends storing version markers when approval can remain pending while definitions change.

This supports four R030 design properties:

1. approval should refer to a specific pending object rather than free-floating assent;
2. state should pause before the gated effect and resume from the same logical context;
3. ambiguity should fail closed rather than broaden authorization; and
4. stale/version-changed pending work requires explicit compatibility/freshness handling.

Source reviewed: OpenAI Agents SDK, "Human-in-the-loop" and `RunState`, reviewed 2026-09-13.  
https://openai.github.io/openai-agents-python/human_in_the_loop/  
https://openai.github.io/openai-agents-python/ref/run_state/

### OpenAI model guidance on reviewable approvals

Current OpenAI model guidance recommends completing work already authorized and necessary to make a proposed action concrete and reviewable before asking for approval. It explicitly distinguishes reversible/read-only preparation from consequential external action.

For R030 this argues against freezing all reasoning and reads before `go`. The Orchestrator should be allowed to perform the bounded read-only canonical inspection needed to form an accurate proposal, while withholding material mutation/execution until the proposal is approved.

Source reviewed: OpenAI API Model guidance, reviewed 2026-09-13.  
https://developers.openai.com/api/docs/guides/latest-model

### OpenAI confirmation and prompt-injection guidance

OpenAI documents confirmation before consequential/state-changing actions as a user-control mechanism and recommends that users review the action details. OpenAI also recommends explicit, well-scoped instructions because broad latitude increases prompt-injection risk.

For R030 this supports strict provenance: only the top-level Human message may satisfy the approval token. Text discovered in web pages, files, tool output, Executor output or other untrusted content must never be parsed as Human approval.

Sources reviewed 2026-09-13:  
https://openai.com/index/prompt-injections/  
https://deploymentsafety.openai.com/chatgpt-agent/threatmodel

### Microsoft Agent Framework comparison

Current Microsoft Agent Framework documentation independently follows the same structural pattern: an approval-requiring function returns a user-input request containing the concrete function call and arguments; the caller supplies an approval response and continues the same agent/session. The framework also exposes a distinct waiting-for-input state for approval, additional information or guidance.

This reinforces the distinction between **approval** and **continued interaction**. A message that is not the explicit approval token should remain ordinary interaction rather than being heuristically interpreted as consent.

Sources reviewed 2026-09-13:  
https://learn.microsoft.com/en-us/agent-framework/agents/tools/tool-approval  
https://learn.microsoft.com/en-us/agent-framework/agents/looping

## Candidate interaction state machine

The protocol can be represented with five logical states:

```text
NO_PENDING_PROPOSAL
    -> Human material prompt
    -> PROPOSAL_BUILDING
    -> proposal emitted
    -> PROPOSAL_PENDING

PROPOSAL_PENDING
    -> exact `go`
        -> freshness/materiality revalidation
        -> AUTHORIZED
        -> ACTIVE

PROPOSAL_PENDING
    -> exact `go,<context>`
        -> classify context delta
        -> NON_MATERIAL: AUTHORIZED -> ACTIVE
        -> MATERIAL/UNCERTAIN: PROPOSAL_BUILDING -> revised PROPOSAL_PENDING

PROPOSAL_PENDING
    -> any other prompt
        -> INTERACTION
        -> answer/refine/correct
        -> PROPOSAL_BUILDING or PROPOSAL_PENDING

PROPOSAL_PENDING
    -> controlling state materially changes
        -> PROPOSAL_STALE
        -> PROPOSAL_BUILDING
        -> revised PROPOSAL_PENDING
```

`AUTHORIZED` is an edge/state transition, not durable standing permission. Once consumed, the approval token cannot be reused to repeat or broaden the work.

## Scope of the proposal gate

The gate should apply to **new material project/action intent**, including material repository mutation, research execution, evaluation execution, Executor/provider launch, external side effects, or a material change of objective/scope.

It should not mechanically intercept every conversational turn. Pure status questions, explanations and ordinary read-only informational requests can be answered directly. To construct an accurate proposal, the Orchestrator may perform bounded read-only inspection of canonical Git/project state and public documentation when that inspection itself does not cross an existing Human or security gate.

This is important because a proposal built without current project context would defeat the purpose of confirming interpretation.

## Proposed approval grammar

The safest candidate grammar is deliberately narrow.

### Valid approval forms

After trimming leading/trailing whitespace and using ASCII case-insensitive comparison:

```text
GO := "go"
GO_WITH_CONTEXT := "go" "," CONTEXT
```

`CONTEXT` must be non-empty after trimming. Thus these examples approve a pending proposal:

```text
go
Go
GO
  go  
go,+usar también el caso B
go, usa también el caso B
```

The leading `+` after the comma may be treated as ordinary additive notation inside the contextual payload. It does not need separate operator semantics; the protocol is simpler if the meaningful form is `go,<context>`.

### Non-approval forms

These should **not** approve:

```text
go!
go por favor
sí
adelante
hazlo
"go"
`go`
no hagas go todavía
g0
Unicode homoglyph variants
go,
```

The reason is intentional determinism: the Human Owner specified that any direct prompt other than the reserved `go` form means more interaction is needed. Natural-language assent therefore remains interaction unless a later decision deliberately broadens the grammar.

Recognition should operate only on the complete top-level Human message, never substring matching.

## Proposal object

A valid pending proposal should make the approval target sufficiently concrete to review. At minimum, when materially applicable, it should expose:

```text
Interpreted objective
Relevant canonical project state / anchor
Intended material actions and scope
Explicit exclusions / invariants
Known Human, Executor, provider or security gates
Observable completion condition
ChatGPT Effort
Execution Shape when D080 applies
```

The proposal may remain concise; the requirement is semantic reviewability, not a verbose template.

Only one proposal should be pending for approval at a time in a ChatGPT objective. A revised proposal supersedes the earlier proposal. `go` always binds to the **latest** pending proposal and never to an older candidate chosen by conversational inference.

## `go,<context>` delta classification

`go,<context>` combines approval with a proposed delta. The Orchestrator should classify that delta before any material effect.

### `NON_MATERIAL_CONTEXT_DELTA`

The delta may be incorporated and execution may start without restating the full proposal when all controlling boundaries remain materially unchanged, including:

- Human objective identity;
- authority and ownership;
- material scope and target/effect envelope;
- accepted specification and controlling Design;
- safety/security posture;
- acceptance criteria/meaning;
- mandatory Human/normative gates; and
- any provider/Executor authorization that the proposal explicitly depended on.

Examples include a presentation preference, an extra read-only comparison, or a bounded implementation/detail preference already inside the proposed scope.

### `MATERIAL_PROPOSAL_DELTA`

The proposal must be considered stale and re-presented when the added context materially changes any controlling boundary above.

Examples include changing the objective, adding a new repository or environment, broadening a mutation/privilege target, changing accepted Design, altering acceptance meaning, introducing a new provider/Executor call not included in the proposal, or bypassing a required Human gate.

### `UNCERTAIN_DELTA`

If the Orchestrator cannot confidently establish that the delta is non-material, it should fail closed: do not execute; produce a revised proposal and wait for a new `go`.

This is the direct conversational counterpart of D081's in-cycle adaptation boundary and D033's stale-authorization rule.

## Freshness and stale proposals

Approval must not freeze canonical repository authority in time.

When Git state materially informs the proposal, the proposal should record or internally bind the relevant canonical branch/HEAD or equivalent durable identity. On receiving `go`, the Orchestrator revalidates the minimum material authority needed to execute.

Disposition:

```text
no material drift
    -> approval remains applicable
    -> execute

non-material drift demonstrably outside proposal semantics
    -> refresh context
    -> approval may remain applicable

material or ambiguous drift affecting authority/scope/spec/design/safety/acceptance
    -> proposal stale
    -> do not execute
    -> re-propose
    -> await new `go`
```

A stale proposal never overrides current Git merely because the Human typed `go`.

## Chat locality and idempotency

The candidate approval should be chat-local and proposal-local.

- `go` with no pending proposal authorizes nothing.
- A pending proposal expires on D067 chat turnover; a successor must reconstruct current authority and present a new proposal before accepting `go`.
- One proposal may be approved once. A duplicate `go` after execution has started or completed does not repeat the operation.
- `go` is not a standing "always approve" preference.
- A later Human message during active execution is governed by normal D081 in-cycle interaction; it is not implicitly a continuation of the consumed approval token.

These properties avoid accidental replay and preserve Git rather than chat history as the durable authority.

## Downstream Human and execution gates

`go` approves only what the proposal actually exposes.

It must not silently waive a later D033 `REQUIRE_HUMAN`, security, production, irreversible-effect, MFA, normative-decision, Executor-launch or provider-call gate.

A specific downstream Human gate may be satisfied by the same `go` only when the pending proposal explicitly presents that exact bounded operation as the approval object and existing policy permits the Human Owner to authorize it at that point. Otherwise the downstream gate remains separate.

Similarly, an Executor/provider call is authorized by `go` only if the proposal explicitly includes that launch/call and all controlling task/decision prerequisites already permit it. The existence of the `go` mechanism does not itself create provider or Executor authority.

## Trusted-input boundary

The approval parser should only consider a top-level Human Owner message in the active ChatGPT interaction.

The following can inform the proposal but can never themselves satisfy approval:

- repository contents;
- web pages;
- retrieved documents;
- email/message content;
- tool output;
- Executor output;
- model-generated text; or
- quoted/embedded Human text relayed through an untrusted source.

This prevents prompt injection or quoted strings such as `go` from manufacturing authorization.

## Interaction truth table

| State | Human input | Result |
| --- | --- | --- |
| no pending proposal | `go` | no authorization; explain there is nothing pending |
| pending | `go` / case variants | revalidate latest proposal; approve once if fresh |
| pending | `go,<non-material context>` | incorporate delta and execute |
| pending | `go,<material context>` | do not execute; emit revised proposal |
| pending | `go,<uncertain context>` | fail closed; emit revised proposal |
| pending | `go,` | invalid approval / interaction |
| pending | `sí`, `adelante`, `hazlo` | interaction, not approval |
| pending | sentence containing `go` | interaction, not approval |
| active/completed | duplicate `go` | no replay / no standing authorization |
| successor chat | `go` without newly presented proposal | no authorization |
| pending + material canonical drift | `go` | stale proposal; re-propose |

## Candidate evaluation before normative adoption

Before or together with a future normative adoption, the protocol should be checked against synthetic conversational cases covering at least:

- exact `go` case variants and surrounding whitespace;
- false positives from punctuation, quoting and embedded text;
- rejection of natural-language assent as approval;
- `go,<context>` with clearly non-material delta;
- `go,<context>` with material and ambiguous deltas;
- `go` without a pending proposal;
- duplicate/replay `go`;
- chat turnover;
- canonical HEAD/spec drift between proposal and approval;
- preservation of D033 downstream Human gates;
- preservation of D080 execution shape and D081 adaptation semantics; and
- untrusted content containing `go`.

A later decision may determine whether these become normative conformance assets under D052 or remain specification examples. R030 does not authorize that implementation.

## Recommended adoption shape

If the Human Owner chooses to adopt this mechanism, the next normative work should define a dedicated Orchestrator interaction decision (prospectively the next available `Dxxx`) and materialize the smallest coherent instruction/specification surface needed to make the state machine enforceable.

The normative decision should settle at least:

1. exact grammar and normalization;
2. what categories of prompt require a proposal gate versus direct informational handling;
3. minimum proposal fields;
4. materiality classifier for `go,<context>`;
5. proposal freshness anchor and stale-proposal behavior;
6. chat-turnover/replay behavior;
7. interaction with D033/D067/D080/D081 and existing Human gates; and
8. conformance/evaluation requirements.

The design should remain a confirmation layer over current authority, not a replacement for SDD, Task Contracts, branch protection, access control, Executor launch authorization, research-to-decision traceability or canonical Git freshness.

## Research disposition

```text
Research-State: COMPLETE
Decision-State: EVALUATING
Candidate mechanism: QUALIFIED FOR NORMATIVE DESIGN CONSIDERATION
Normative `go` policy adopted: no
Implementation authorized: no
Provider/model calls consumed by this research: 0
Executor launches: 0
```

The research question is sufficiently closed to support a later Human-selected normative decision/design objective. Promotion requires an explicit accepted decision under D057; successful use of `go` in this chat is interaction evidence, not self-adopting policy.
