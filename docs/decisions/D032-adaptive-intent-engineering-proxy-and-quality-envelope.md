# D032 — Adaptive intent-engineering proxy and implicit quality envelope

Status: ACCEPTED
Authority: Human Owner / ChatGPT Orchestrator

## Problem

Agent Governance is intended to let a Human Owner request outcomes in the language most natural to them while still producing implementation-grade engineering work. The current Core separates strategy from implementation well, but it does not yet define an explicit interaction contract that keeps conversational complexity independent from engineering rigor.

The current lifecycle also mentions security, observability, testing, deployment/rollback and related concerns in F2, but they are optional examples rather than a mandatory cross-cutting quality review. This permits an implementation scope to become READY without a consistent check for concerns that the user did not know to ask about.

A third gap is visual pre-implementation communication. The lifecycle does not currently require Strategy to show the intended solution graphically before Implementation begins.

## Decision

Agent Governance SHALL operate as a bidirectional proxy between human intent and technical execution.

The proxy has two distinct planes:

1. **Interaction Plane** — adapt vocabulary, abstraction, format and modality to the Human Owner's current technical register.
2. **Engineering Plane** — normalize the request into a complete engineering contract and apply invariant quality, safety and readiness standards independent of the user's technical vocabulary.

The interaction plane is presentation. It MUST NOT be treated as a quality setting.

A non-technical request therefore receives the same engineering discipline as a code-native request. Conversely, a technically sophisticated user SHOULD receive correspondingly technical communication rather than forced simplification.

Detailed rules live in `governance-core/INTERACTION.md` and `governance-core/QUALITY.md`.

## Bidirectional translation contract

The Strategy/Governance Agent performs two translations without changing authority or intent:

```text
Human request
  -> intent normalization
  -> engineering strategy/task contract
  -> implementation/evidence
  -> explanation at the Human Owner's current technical register
```

Translation MUST preserve:

- requested outcome and business/domain intent;
- explicit constraints and exclusions;
- risk/authority decisions;
- acceptance meaning;
- user-provided technical facts and code semantics.

Translation MUST NOT silently:

- downgrade implementation quality because the request is informal;
- invent business intent to fill a material ambiguity;
- expose irrelevant internal complexity merely to demonstrate rigor;
- hide a material tradeoff, risk or required Human decision behind simplification.

## Adaptive interaction register

The interaction register is inferred from the current request and nearby conversational context, not permanently assigned to the person.

Useful presentation modes include:

- plain/domain language;
- practitioner/technical language;
- expert/architecture language;
- code-native interaction where code, patches, schemas, commands or equivalent technical artifacts are the clearest primary response.

These are routing modes, not user labels. A person may move between them from one request to the next.

When the Human Owner explicitly sets a desired detail level or format, that instruction controls presentation unless safety or correctness requires additional material context.

## Implicit engineering quality envelope

Every implementation scope SHALL receive a silent-by-default cross-cutting quality review before readiness. The review considers at least:

- functional correctness and acceptance fidelity;
- architecture, ownership and ecosystem coexistence;
- security and threat exposure;
- privacy and data governance;
- reliability, resilience, failure handling and recovery;
- performance, capacity and resource/cost efficiency;
- observability, diagnosability and operational support;
- testability and verification depth;
- maintainability, modularity and change isolation;
- compatibility, interoperability, migration and backward-compatibility concerns;
- usability and accessibility when humans interact with the resulting product;
- dependency, provenance and software/Skill supply-chain risk;
- configuration, deployment, rollback and release safety;
- safety/harm and compliance/domain obligations when applicable.

Not every dimension needs a dedicated artifact or visible discussion. Strategy MUST surface only the dimensions that materially affect the Human Owner's decision, scope, cost, risk, acceptance or operation. Non-material checks remain implicit.

Security is always triaged. A detailed threat model is required only when the change introduces or materially alters a relevant attack surface, trust boundary, privilege, secret, external input, network exposure, sensitive data flow, executable dependency or comparable security risk.

Privacy is evaluated independently from cybersecurity whenever personal, confidential, regulated or otherwise sensitive data processing is material.

## Quality is independent of conversational simplicity

The following invariant is normative:

```text
presentation complexity != engineering quality
```

Reducing jargon, shortening explanations or communicating through natural language MUST NOT weaken architecture, security, verification, maintainability or other applicable engineering standards.

Likewise, technically dense communication MUST NOT be used to obscure uncertainty or unvalidated assumptions.

## Pre-implementation graphical solution view

Before an implementation scope becomes READY, Strategy SHALL present a **Primary Solution Diagram** that shows the solution to be implemented at the smallest useful level of abstraction for the Human Owner and the change.

No single diagram notation is mandatory for all changes. Select the diagram according to the dominant question:

- C4 System Context — system boundary or cross-system responsibility change;
- C4 Container — application/service/data-store boundary or high-level software architecture change;
- C4 Component — internal component responsibility change when that detail adds value;
- Dynamic/sequence view — runtime collaboration for a feature/use case with meaningful interaction order;
- state diagram — lifecycle/state-transition behavior;
- data-flow diagram with trust boundaries — security/privacy-sensitive data movement and attack-surface reasoning;
- data model/ER view — persistent data structure/relationship change;
- compact flow/dependency diagram — a local algorithmic or workflow change where architecture notation would add noise.

C4 is the default architecture backbone because its zoom levels allow the same system to be explained at different abstraction levels. Supporting behavioral/security diagrams are selected only when they communicate the material concern better.

The diagram is a communication/readiness artifact, not a new authority tier. Presentation of the diagram does not create a mandatory extra Human approval gate unless the Human Owner or project policy explicitly requires approval. If the solution materially changes after presentation, Strategy MUST refresh the affected diagram before implementation continues.

## Research basis

External references reviewed for this decision include:

- C4 Model — architecture diagrams, zoom levels and dynamic diagrams: `https://c4model.com/diagrams`
- NIST SP 800-218 / SSDF — secure development practices integrated into the SDLC: `https://csrc.nist.gov/pubs/sp/800/218/final`
- NIST Cybersecurity Framework 2.0 — Govern/Identify/Protect/Detect/Respond/Recover lifecycle coverage: `https://www.nist.gov/cyberframework`
- NIST Privacy Framework — privacy risk management as a related but distinct engineering concern: `https://www.nist.gov/privacy-framework`
- ISO/IEC 25010:2023 — product quality characteristics used throughout requirements, design, testing and acceptance: `https://www.iso.org/standard/78176.html`
- OWASP Threat Modeling — data-flow/trust-boundary modeling for security analysis: `https://owasp.org/www-community/Threat_Modeling_Process`
- W3C WCAG 2.2 — accessibility requirements for applicable web/user-facing surfaces: `https://www.w3.org/TR/WCAG22/`
- Google SRE literature — reliability and operations across the software lifecycle: `https://sre.google/books/`

These references inform the quality envelope; Agent Governance remains framework-neutral and does not require a consumer repository to adopt those external frameworks wholesale.

## Consequences

- `governance-core/INTERACTION.md` becomes the focused module for user-register adaptation and intent/technical translation.
- `governance-core/QUALITY.md` becomes the focused module for the implicit engineering quality envelope and graphical design readiness.
- `LIFECYCLE.md` must make quality review and the Primary Solution Diagram mandatory before F5 passes.
- `GOVERNANCE.md` must route interaction/quality context progressively rather than always loading the new modules.
- future deterministic/agent-facing tests should verify that conversational simplicity does not lower execution-contract quality and that material change scopes include an appropriate graphical design view.
- Agent Governance does not expose a large technical checklist to the Human Owner by default; it exposes material decisions and risks at the user's current register.
