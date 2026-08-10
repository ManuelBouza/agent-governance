# Intent-to-Engineering Proxy Architecture

Status: ARCHITECTURE OVERVIEW  
Normative authority: `docs/decisions/D032-adaptive-intent-engineering-proxy-and-quality-envelope.md`, `governance-core/INTERACTION.md`, `governance-core/QUALITY.md`, `governance-core/GOVERNANCE.md`, and `governance-core/LIFECYCLE.md`

## Purpose

This document provides a single architectural view of the Human-to-engineering proxy introduced by D032. It is explanatory and consolidating, not a competing source of normative rules.

Agent Governance must let a Human Owner request outcomes using natural language, domain language, technical language, architecture language, code, schemas, commands, or a mixture of those forms. The system translates that request into implementation-grade engineering without requiring the Human Owner to know every technical concern that must be handled correctly.

The central invariant is:

```text
presentation complexity != engineering quality
```

A simpler way of asking for work changes the explanation style, not the engineering standard.

## Two-plane architecture

Agent Governance operates through two conceptually separate planes.

```text
┌──────────────────────── USER INTERACTION PLANE ────────────────────────┐
│ Human request                                                         │
│                                                                        │
│ plain/domain ── practitioner ── expert/architecture ── code-native    │
│                         │                                              │
│                         └─ adaptive presentation register              │
└──────────────────────────────┬─────────────────────────────────────────┘
                               │ semantic-preserving translation
                               ▼
┌──────────────────────── ENGINEERING PLANE ─────────────────────────────┐
│ Frame → Viability → Engineering Strategy → Capability/Skill analysis  │
│                                      │                                 │
│                               Quality Envelope                         │
│                                      │                                 │
│       security · privacy · reliability · performance · observability  │
│       verification · maintainability · compatibility · accessibility │
│       supply chain · deployment/rollback · safety/compliance          │
│                                      │                                 │
│                         Primary Solution Diagram                       │
│                                      │                                 │
│                         Readiness → Implementation                      │
└──────────────────────────────┬─────────────────────────────────────────┘
                               │ implementation evidence
                               ▼
                 explanation at the Human's current register
```

The Interaction Plane determines how information is expressed. The Engineering Plane determines what quality, risk, design, verification, and readiness work is required.

## Bidirectional semantic translation

The Strategy/Governance Agent performs a bidirectional translation:

```text
Human request
  -> intent normalization
  -> engineering strategy / execution contract
  -> implementation and evidence
  -> explanation at the Human Owner's current register
```

Translation must preserve outcome, domain intent, explicit constraints, exclusions, acceptance meaning, authority decisions, technical facts, and code semantics.

The proxy must not invent material business intent, silently weaken engineering standards, or hide material tradeoffs behind simplified language.

## Adaptive interaction register

The communication register is inferred from the current request and nearby context rather than permanently assigned to a person.

Typical modes are:

- **plain/domain** — outcome-oriented language with minimal jargon;
- **practitioner/technical** — implementation-relevant terminology and tradeoffs;
- **expert/architecture** — explicit architectural, operational, security and compatibility reasoning;
- **code-native** — code, patches, schemas, commands or equivalent technical artifacts are primary where that is the clearest response.

A Human Owner may move between these modes from one request to the next.

If the Human writes technically, respond correspondingly technically. If the Human communicates primarily through code, respond through code/technical artifacts when appropriate. If the Human asks in non-technical language, do not force unnecessary technical detail into the conversation.

None of these presentation choices changes the required engineering rigor.

## Silent-by-default engineering quality envelope

Every implementation scope is triaged across the following quality dimensions whether or not the Human explicitly names them:

- functional correctness and acceptance fidelity;
- architecture, ownership and ecosystem coexistence;
- security and threat exposure;
- privacy and data governance;
- reliability, resilience, failure handling and recovery;
- performance, capacity, efficiency and cost/resource impact;
- observability, diagnosability and operational support;
- testability and verification depth;
- maintainability, modularity and change isolation;
- compatibility, interoperability, migration and backward compatibility;
- usability and accessibility for Human-facing surfaces;
- dependency, provenance and software/Skill supply-chain risk;
- configuration, deployment, rollback and release safety;
- safety/harm and compliance/domain obligations where applicable.

The review is silent by default. It does not require exposing a checklist to the Human Owner.

Only dimensions that materially affect scope, cost, risk, behavior, acceptance, operation, or a Human decision should be surfaced explicitly. Other checks remain internal to the planning/readiness process.

### Security floor

Security is always triaged.

A detailed threat model becomes appropriate when a change introduces or materially alters attack surface, trust boundaries, authentication/authorization, privilege, secrets, externally controlled input, network exposure, sensitive data movement, executable dependencies, or comparable security risk.

### Privacy is distinct from security

Privacy must be considered independently when personal, confidential, regulated, or otherwise sensitive data is collected, processed, stored, shared, inferred, or retained.

A system can be secure against unauthorized access and still create unacceptable privacy risk through legitimate data processing.

## Graphical solution readiness

Before an implementation scope becomes READY, Strategy presents a **Primary Solution Diagram** at the smallest useful level of abstraction.

No single notation is appropriate for every type of change. The diagram family is selected according to the dominant design question.

| Dominant question | Preferred view |
| --- | --- |
| system boundary / external responsibilities | C4 System Context |
| services, applications, APIs, data stores | C4 Container |
| meaningful internal component responsibilities | C4 Component |
| runtime interaction/order for a feature/use case | C4 Dynamic or sequence diagram |
| lifecycle/state transitions | state diagram |
| sensitive data flows / security trust boundaries | DFD with trust boundaries |
| persistent entities and relationships | ER/data-model diagram |
| local algorithm/workflow/dependency change | compact flow/dependency diagram |

C4 is the default architectural backbone because its zoom levels support communication with audiences at different technical depths. Behavioral, security, state and data views supplement it where those concerns are more informative.

### Diagram register follows user register

The same underlying solution can be shown at different levels of detail without changing the engineering design.

Plain/domain example:

```text
Customer
   ↓
Application
   ↓
Payment service
   ↓
Confirmation
```

Technical example of the same class of interaction:

```text
Web SPA
  │ HTTPS
  ▼
API Gateway
  │
  ├──► Order Service ───► PostgreSQL
  │
  └──► Payment Provider
```

The diagram is a communication/readiness artifact, not an independent authority tier. Showing it does not automatically create a new mandatory Human approval ceremony. If the design changes materially after presentation, the affected diagram must be refreshed before readiness continues.

## Lifecycle integration

The proxy and quality envelope are overlays on the existing F0-F6 lifecycle rather than additional phases.

Conceptually:

```text
F0 Frame
  ↓
F1 Viability
  ↓
F2 Engineering Strategy
  ├─ capability/coexistence analysis
  ├─ implicit quality triage
  └─ Primary Solution Diagram
  ↓
F3 Skill Capability Audit
  ↓
F4 Atomic Work Planning
  ↓
F5 Readiness Review
  ├─ material quality concerns bounded
  ├─ diagram current
  └─ contract executable without hidden assumptions
  ↓
F6 Persist and Handoff
  ↓
Implementation
```

This design avoids both failure modes:

1. **under-engineering** — ignoring security, privacy, rollback, observability, compatibility, testing or other quality dimensions because the user did not name them;
2. **overwhelming the user** — forcing the Human Owner to consume every internal engineering checklist or implementation detail.

## External research basis

The architecture is informed by established external references without requiring consumer repositories to adopt those frameworks wholesale:

- C4 Model — architecture zoom levels and dynamic diagrams: `https://c4model.com/diagrams`
- NIST SP 800-218 / Secure Software Development Framework — security practices integrated into the SDLC: `https://csrc.nist.gov/pubs/sp/800/218/final`
- NIST Cybersecurity Framework 2.0 — Govern/Identify/Protect/Detect/Respond/Recover coverage: `https://www.nist.gov/cyberframework`
- NIST Privacy Framework — privacy risk management distinct from but related to cybersecurity: `https://www.nist.gov/privacy-framework`
- ISO/IEC 25010:2023 — software/product quality characteristics applied across requirements, design, testing and acceptance: `https://www.iso.org/standard/78176.html`
- OWASP Threat Modeling Process — data-flow and trust-boundary modeling: `https://owasp.org/www-community/Threat_Modeling_Process`
- W3C WCAG 2.2 — accessibility baseline for applicable web-facing experiences: `https://www.w3.org/TR/WCAG22/`
- Google SRE literature — reliability and operational engineering across the software lifecycle: `https://sre.google/books/`

These sources guide the architecture and quality envelope. They are not runtime dependencies and do not override Agent Governance authority.

## Product implications

The model implies future verification work beyond documentation:

- interaction-register tests/evals proving that simpler user language does not reduce contract quality;
- code-native interaction tests/evals where technical responses preserve code semantics and implementation standards;
- quality-routing tests proving material concerns are surfaced while non-material concerns remain implicit;
- graphical-readiness tests/evals proving an appropriate Primary Solution Diagram exists and is refreshed after material design changes;
- security/privacy test coverage appropriate to the affected product surfaces;
- release-readiness checks showing the architecture works without requiring users to understand the internal governance machinery.

Those verification increments require their own future Task Contracts. They must not be retroactively added to an already executing task unless a persisted contract revision explicitly changes that task's scope.
