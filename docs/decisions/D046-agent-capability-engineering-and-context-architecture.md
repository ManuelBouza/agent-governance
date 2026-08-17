# D046 — Agent Capability Engineering and Context Architecture

Status: ACCEPTED
Date: 2026-08-15
Scope: source-product engineering methodology, assurance routing, repository context architecture, evidence traceability

## Decision

Agent Governance adopts **ICAE — Ingeniería de Capacidades Agénticas dirigida por Especificación, Contrato y Evaluación** as its prospective engineering/assurance method for agent-consumed capabilities.

ICAE is a composition of existing repository governance with specification/contract-driven engineering, deterministic verification, property/state-machine testing, eval-driven development for model-mediated behavior, security assurance, and reproducible package/provenance evidence. It is not a second task lifecycle and does not replace D022, Task Contracts, EGLL, or release authority.

Repository Context Architecture & Budgeting (**RCAB**) is adopted as a cross-cutting ICAE assurance dimension, not as a separate methodology.

D052 later refines authorship of executable conformance oracles without changing ICAE's assurance routing: when semantic authority belongs to ChatGPT and a Task Contract selects `orchestrator-conformance` or `mixed`, ChatGPT may author the designated acceptance/conformance assets; the executor still performs technical implementation, supplementary testing, execution and evidence.

## Core assurance rule

If a property must always hold, violation is material, and the property is machine-decidable from observable state, prose or model instructions MUST NOT be its sole enforcement.

Use the least probabilistic verifier that preserves the requirement meaning:

- mechanically decidable invariant -> deterministic validator/test/control;
- formalizable state space -> property/state-machine verification;
- activation/routing -> repeated agent evals with positive, negative and near-miss cases;
- semantic/open behavior -> behavioral evals with objective assertions where possible;
- architecture/authority/risk judgment -> Human/Orchestrator review;
- distribution -> reproducibility, identity, boundary and provenance evidence.

Model-generated judgments are evidence only and never isolated Governance acceptance authority.

## Evidence traceability

For material acceptance criteria, Task Contracts and reviews SHOULD use stable criterion identities when doing so improves auditability. Evidence MUST identify what it actually proves. A weaker evidence class MUST NOT silently satisfy a stronger claim; for example, `surface-present` is not equivalent to `executed-successfully`.

Where relevant, evidence may distinguish classes such as deterministic assertion, property/state replay, executed-successfully, negative-control, reproducibility, routing/behavioral eval, security/adversarial evidence, package/isolation evidence, and review-only judgment.

D052 adds an authorship distinction without changing this evidence hierarchy:

```text
acceptance meaning / conformance oracle authorship
    !=
verification execution
    !=
Governance acceptance
```

A pre-authored conformance oracle is an executable projection of accepted semantics, not independent authority. An executor may add stronger supplementary evidence but may not silently weaken or reinterpret an Orchestrator-owned expected outcome.

This decision selects the systemic control direction for L003 and L004. Those learnings remain unverified until the corresponding controls are implemented and replay-proven.

## RCAB — repository context architecture

Agent-visible repository information MUST be designed for progressive disclosure.

The governing principle is:

> **Budget the load path, not just the file.**

File size is a useful signal, but context cost depends on when and how often material is loaded, how much routing fan-out it causes, and whether the information can be discovered without loading irrelevant authority/history.

Agent Governance therefore:

- does NOT impose a universal line, byte, token or LOC limit across all file types;
- does NOT automatically split normative Markdown when a numeric threshold is crossed;
- uses semantic responsibility as the primary split boundary;
- treats indexes/manifests as discovery projections, never second authority;
- measures tokenizer-neutral physical size in UTF-8 bytes and labels token counts with the tokenizer/host/model that produced them;
- uses baseline-and-ratchet adoption before source-repository hard size budgets;
- permits large evidence/history/generated artifacts when normal reads remain bounded and on-demand;
- preserves positive source/distribution boundaries.

D052 permits a pre-authored executable conformance oracle to reduce semantic reconstruction work for an executor, but token/context savings MUST be measured from actual load paths before being claimed. Test code/data must not become a second normative authority or an excuse to omit controlling references required for safe interpretation.

The existing Consumer budgets in `governance-core/CONTEXT.md` remain unchanged. They are project-design targets for the Consumer context model and are not automatically copied into source-repository policy.

## Adoption sequence

Source-repository RCAB adopts controls incrementally:

1. measure current tracked repository context deterministically without mutating/splitting content;
2. freeze an accepted baseline;
3. introduce a compact human-readable context map and a reproducible machine-readable projection if evidence supports them;
4. make unequivocal integrity failures (for example broken registered references, stale generated indexes, recursive includes, or source/distribution leaks) blocking only when their semantics are mechanically defined;
5. introduce warning/ratchet budgets from measured baselines;
6. perform semantic decompositions one concern at a time;
7. observe real host/model token usage where available and tune budgets empirically.

No vector database, embedding pipeline, semantic database, or remote retrieval service is required for the initial architecture.

## Program boundary

T018–T020 are grandfathered under their accepted contracts. ICAE/RCAB apply prospectively from T021 onward and to newly contracted cross-cutting work.

D052 is separately prospective for test authorship. T032 R1 and T021 R1 remain under their already-launched contracts; T022 may complete under its already-integrated runtime/profile contract. MG1/T023 is the first strong planned D052 application because the Orchestrator already owns the topology definitions, corpus meaning and pre-registered victory/non-regression criteria.

T021 remains a deterministic, zero-behavior-drift refactor. It does not require model eval ceremony unless its implementation changes a model-mediated activation/routing surface.

T023 is the natural first strong probabilistic profile-routing gate. T024 remains a distribution/provenance gate. T029 must include the applicable final ICAE/RCAB release conformance established by then.

T026 remains separately gated and MUST NOT be launched by this decision.

## Authority

ICAE and RCAB structure evidence and assurance; they do not create a new agent role or acceptance authority.

- Human Owner retains final product/risk/release authority.
- ChatGPT Orchestrator retains Markdown, architecture, Task Contract and acceptance authority and, under D052-designated modes, the narrow conformance/oracle assets that directly encode its acceptance semantics.
- Agente de IA Ejecutor retains authorized product implementation, implementation/exploratory testing, technical harness work, verification execution and evidence ownership except for those D052-designated conformance assets.
- Git remains the authoritative source-product state.
