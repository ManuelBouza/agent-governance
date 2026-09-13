# R029-S6 — `research-evidence-traceability` Candidate Evaluation

Status: COMPLETE  
Parent: `R029 — AGENTS.md / Skill Architecture Refactor Research`  
Subtask: `R029-S6 — research-evidence-traceability candidate`  
Baseline-Develop: `e539c976b382d5841fca7fd89b30d5d185c8c73f`  
Inputs: accepted R029-S1 through R029-S5 artifacts; `docs/decisions/D057-research-decision-traceability.md`  
Decision-State: EVALUATING  
Normative-Effect: none  
Analytical-Disposition: `KEEP_CANDIDATE`

## Purpose

Evaluate whether research/evidence provenance and freshness form a reusable transverse capability distinct from Agent Governance's own research IDs, decision records, ledger, checkpoint and lifecycle vocabulary. This artifact is analytical only; it does not create or adopt a Skill.

## Reusable semantic intent

> Persist material evidence with enough provenance, state and freshness information that a later agent can distinguish what was observed, what was inferred, what remains uncertain or stale, and what—if anything—was actually decided.

This intent survives removal of Agent Governance-specific `Rxxx`/`Dxxx` identifiers, Decision-State names, registry paths, checkpoint rules, stage ownership and repository layout.

The capability is not generic note-taking, citation formatting, web research, or decision making. It is the durable traceability layer between consequential evidence and the authority that may later consume that evidence.

## Positive triggers

Use/evaluate this capability when evidence materially informs durable design/policy/evaluation/compatibility/security/launch/implementation work; must survive the current session; requires provenance or freshness; could be confused with accepted policy; has been contradicted/superseded/deferred; or must be reconstructable without private chat history.

## Negative triggers

Do not activate for disposable factual lookup, immediate-only citations, deterministic current repository facts with no analytical lineage, ordinary editing/coding/testing/Git mechanics, or as a substitute for the authority that actually decides. When another capability owns the primary intent—such as upstream version revalidation—this capability may preserve its evidence but must not duplicate its workflow.

## Generic contract

Inputs:

1. bounded evidence question or claim;
2. sources/observations and source class where material;
3. observation date/version/baseline when freshness matters;
4. conclusion or unresolved uncertainty;
5. current evidence state (collecting/synthesizing/evaluating/superseded/consumed);
6. durable destination supplied by the project/host adapter;
7. downstream authority reference, if one exists.

Workflow:

```text
bound the evidence question
-> identify material evidence and provenance
-> separate observation from inference/recommendation
-> record freshness/baseline where volatility matters
-> record uncertainty, contradiction or supersession explicitly
-> persist enough lineage for reconstruction
-> link downstream authority when supplied
-> never promote evidence into authority by implication
```

If material evidence cannot be sourced, reconstructed or refreshed sufficiently, fail closed with an explicit evidence gap.

## Output/postcondition

A successful invocation leaves a durable record containing the bounded question, provenance, observation date/version/baseline where relevant, clear separation of evidence/analysis/authority, unresolved conflicts or freshness risk, supersession lineage, downstream reference when available, and enough context for a later agent to decide whether reliance is still valid.

The postcondition is traceability, not normative adoption.

## Authority boundary

The candidate cannot create policy, approve/reject recommendations, invent project IDs or lifecycle transitions, declare volatile evidence current without refresh, override repository authority, rewrite history to fit later conclusions, collapse evidence into decision state, launch an Executor, mutate product state, or bypass project gates.

## Relationship to S5

`upstream-version-revalidation` determines whether a version-sensitive external assumption remains materially valid. `research-evidence-traceability` preserves consequential evidence and its lineage. S5 may emit evidence that S6-style traceability persists; S6 does not absorb S5's version comparison or disposition logic.

## Agent Governance adapter boundary

Agent Governance keeps domain-side:

- D057 and its normative Research -> Evaluation -> Decision lifecycle;
- exact `Rxxx`/`Dxxx` identifiers;
- `Research-State` and `Decision-State` vocabularies/transitions;
- `docs/RESEARCH-TRACEABILITY.md` as canonical ledger;
- mandatory metadata and grandfathering rules;
- exact research/decision paths;
- checkpoint live-frontier integration;
- D053 stage ownership and Task Contract/evaluation relationships;
- Human/Orchestrator normative authority;
- project-specific supersession/deferral/rejection/promotion rules;
- D077 when version-sensitive upstream behavior is the primary question.

A generic capability may supply provenance discipline but cannot redefine these semantics.

## Host-adapter boundary

The semantic contract is host-neutral. ChatGPT may use web/connected-source retrieval and GitHub persistence; Codex/Executor may use repository/source/test/log inspection and return durable evidence within an authorized task. Host mechanics do not justify separate Skills.

## Non-overlap

The candidate does not own general web research, bibliography formatting, decision frameworks, repository change control, upstream version comparison, durable frontier/checkpoint semantics (S7), Executor launch/handoff (S8), or Agent Governance's exact research registry/state machine.

## Analytical disposition

`KEEP_CANDIDATE`

Rationale: it has distinct reusable intent; clear positive/negative triggers; a concrete durable postcondition; a safe authority boundary; host-neutral semantics; and clean non-overlap with S5/S7/S8. This remains evaluation only; Human authority is required before adoption or implementation.

## Completion gate

S6 is complete because reusable provenance/freshness semantics have been separated from Agent Governance's `Rxxx`/`Dxxx`, ledger, Decision-State, checkpoint and promotion rules; triggers, contract, authority boundary, host adapters and disposition are explicit.

No root `AGENTS.md` change, Skill implementation, Executor/Codex launch, provider/model call, normative adoption or T066 mutation occurred.
