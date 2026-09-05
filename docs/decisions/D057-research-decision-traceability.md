# D057 — Research-to-decision traceability

Status: ACCEPTED  
Date: 2026-09-05  
Authority: Human Owner / ChatGPT Orchestrator  
Scope: source-product research, evaluation, decision and checkpoint traceability

## Problem

Agent Governance increasingly uses external documentation, specialized sources, experiments and repository evidence to inform design choices. A research memo can be complete without its recommendation being adopted, while a later pilot may validate only part of the hypothesis. If research state and decision state are not explicit, later iterations can accidentally:

- treat research conclusions as normative policy;
- forget whether a recommendation was evaluated, deferred, rejected or superseded;
- lose the provenance between source evidence, pilot evidence and an accepted decision;
- rewrite historical research to match a later conclusion;
- require prior chat memory to reconstruct why the current policy exists.

Git must be able to answer both questions independently:

1. What did the research establish?
2. What, if anything, did Agent Governance decide because of it?

## Decision

Every material ChatGPT Orchestrator research effort that may influence product design, policy, evaluation method, Executor configuration or future implementation SHALL be persisted in Git and tracked through an explicit **Research -> Evaluation -> Decision disposition** lifecycle.

Research findings are evidence and analysis. They are not normative authority by themselves.

The canonical research registry is:

`docs/RESEARCH-TRACEABILITY.md`

The registry MUST identify every current and grandfathered research artifact and record its independent research state and decision state.

## Research state

Each research item has exactly one `Research-State`:

- `ACTIVE` — evidence gathering or synthesis is still open;
- `COMPLETE` — the research question has a stable synthesis for its stated scope;
- `SUPERSEDED` — a later research artifact replaces it as the current analytical treatment, while the original remains historical evidence.

`COMPLETE` does **not** mean `DECIDED`.

## Decision state

Each research item has exactly one `Decision-State`:

- `NOT_REQUIRED` — diagnostic/factual research that does not itself require a governance/product decision;
- `EVALUATING` — the recommendation/hypothesis is being tested or validated and no normative decision has been accepted yet;
- `DECIDED` — a normative decision has been accepted and the registry MUST name its `docs/decisions/Dxxx-*.md` authority;
- `DEFERRED` — a decision was consciously postponed; the registry MUST record why and the condition/reference for reconsideration;
- `REJECTED` — the recommendation was considered and not adopted; the registry MUST record the rejecting authority/reference or concise reason;
- `SUPERSEDED` — the prior disposition was replaced by a later research/decision path, with a forward reference.

A Task Contract, pilot, review or checkpoint can move research into `EVALUATING`, but none of those automatically imply `DECIDED` unless an accepted decision artifact or already-controlling normative artifact explicitly adopts the conclusion.

## Mandatory metadata for new research

Every new material file under `docs/research/` SHALL begin with durable metadata containing at least:

```text
Research-ID: Rxxx
Research-State: ACTIVE | COMPLETE | SUPERSEDED
Decision-State: NOT_REQUIRED | EVALUATING | DECIDED | DEFERRED | REJECTED | SUPERSEDED
Opened: YYYY-MM-DD
Last-Reviewed: YYYY-MM-DD
Owner: ChatGPT Orchestrator
Scope: <bounded scope>
Question: <research question>
Evaluation-Refs: <task/review/eval refs or none>
Decision-Ref: <Dxxx path or none>
Supersedes: <Rxxx/path or none>
Superseded-By: <Rxxx/path or none>
```

Sources/evidence MAY remain in the body, but source provenance must be sufficient for a later Orchestrator to revalidate time-sensitive claims before making a new decision.

Existing research files created before D057 are grandfathered without mandatory in-place header rewrites, provided they are represented in the canonical registry with equivalent state and provenance.

## Transition rules

1. **Persist before relying.** Material research that will influence a Task Contract, evaluation design or normative change must be in canonical Git before that downstream artifact is executed or accepted.
2. **No implicit promotion.** Wording such as “recommended”, “selected”, “preferred” or “executive conclusion” inside research does not promote the finding to policy.
3. **Evaluation is explicit.** If a recommendation needs empirical validation, set `Decision-State: EVALUATING` and link the exact Task Contract/eval/review.
4. **Decision is explicit.** When accepted policy/design is created, update the research registry to `DECIDED` and link the exact decision artifact. The decision SHOULD cite the source Research-ID(s).
5. **Deferral/rejection is durable.** `DEFERRED` and `REJECTED` require a reason/reference so later chats do not reopen or silently discard the same question without knowing its prior disposition.
6. **Supersession preserves history.** Do not silently rewrite a closed research artifact to match later evidence. Mark it `SUPERSEDED` and create or reference the successor artifact. Git history plus the registry must preserve the analytical lineage.
7. **Time-sensitive evidence is revalidated.** Before promoting research based materially on changing vendor documentation, pricing, model capabilities, regulations or other volatile facts, refresh the relevant sources and update `Last-Reviewed` or create a successor research artifact.
8. **Checkpoint carries only the live frontier.** `docs/orchestrator/CHECKPOINT.md` SHOULD reference research with active operational relevance (`ACTIVE`, `EVALUATING`, or a pending `DEFERRED` reconsideration), while `docs/RESEARCH-TRACEABILITY.md` remains the complete research ledger.
9. **Chat turnover is not a state transition.** Starting a new chat, summarizing context, or changing Executor sessions cannot alter research or decision state. Only persisted Git changes can do so.

## Research-to-decision gate

Before ChatGPT Orchestrator states that research has become an Agent Governance decision, all of the following must be true:

- the research artifact/registry entry exists in canonical Git;
- relevant evaluation evidence is linked when evaluation was required;
- contradictory or superseding evidence has been reconciled;
- time-sensitive material facts have been refreshed when needed;
- an accepted normative artifact explicitly adopts the conclusion;
- the registry is updated to `Decision-State: DECIDED` with the authority reference;
- the current checkpoint reflects the resulting live frontier when operationally relevant.

Failing any of these conditions, the result remains research/evaluation, not decision authority.

## Current bootstrap application

D057 is applied immediately to the existing `docs/research/` corpus through `docs/RESEARCH-TRACEABILITY.md`.

In particular:

- persistent Executor coordinator research is complete and has produced T053 pilot evidence, but no global D055 persistence policy decision is implied;
- adaptive subagent compute routing research is complete analytically and remains `EVALUATING` through T054; T054-specific launch/profile choices are experimental controls, not a global child-routing decision;
- historical MG1 research/analyses remain preserved and are linked to the later evaluation lineage rather than deleted or silently reinterpreted.

## Relationship to existing decisions

- D027 remains the chat-turnover/checkpoint mechanism; D057 ensures research/decision provenance survives that turnover.
- D039 remains the evidence-driven learning loop; D057 makes the evidence-to-decision state transition auditable.
- D053 remains SDD ownership/lifecycle authority; research belongs to Explore/Frame and may feed Specify/Design, but does not skip those stages.
- D055 remains the current Human-facing Executor launch-profile policy. Research about compute profiles does not modify D055 until a later accepted decision explicitly does so.

## Consequences

- a fresh Orchestrator can distinguish evidence, experiment and accepted policy from Git alone;
- completed research is not lost merely because it did not immediately become a decision;
- recommendations cannot silently acquire normative authority through repetition in later chats;
- rejected/deferred paths remain discoverable and need not be rediscovered from scratch;
- time-sensitive research is less likely to fossilize into stale product policy;
- decision provenance becomes bidirectional: decisions point back to research, and research points forward to its disposition.
