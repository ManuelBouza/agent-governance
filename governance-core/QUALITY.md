# Implicit Engineering Quality Envelope

Quality-Module-Version: 1.0.0

Load this module during F2 engineering strategy, F5 readiness, material risk review, or when a quality/security/operations concern needs explicit treatment.

## Purpose

Every implementation scope receives professional engineering quality controls even when the Human Owner asks only for a functional outcome in natural language.

Quality review is **silent by default, explicit when material**. The Strategy/Governance Agent considers the complete envelope internally and persists/surfaces only requirements that affect implementation, acceptance, risk, operation, scope, cost or Human decisions.

This module defines a review envelope, not a requirement to adopt one external framework or generate a large checklist artifact.

## Baseline dimensions

For every implementation scope, triage at least the following dimensions:

1. **Functional correctness and acceptance fidelity** — the result satisfies the requested outcome, invariants, edge cases and acceptance meaning.
2. **Architecture and coexistence** — responsibilities, boundaries, coupling, existing native capabilities and ownership are coherent; `COEXISTENCE.md` controls overlapping providers.
3. **Security** — attack surface, trust boundaries, authentication/authorization, privilege, secrets, external inputs, network exposure, dependency execution and abuse cases are appropriately bounded.
4. **Privacy and data governance** — data minimization, sensitivity, collection/use/storage/retention/disclosure and applicable privacy risk are addressed independently from cybersecurity.
5. **Reliability and resilience** — expected failures, retries/timeouts/idempotency where relevant, state integrity, availability assumptions, graceful degradation, backup/recovery and recovery objectives are appropriate.
6. **Performance and resource efficiency** — latency/throughput/capacity, algorithmic/resource use and material operational cost constraints are appropriate to the use case.
7. **Observability and operability** — failures and important state can be diagnosed; relevant logs/metrics/traces/events, runbook/support needs and operational ownership are considered without leaking sensitive data.
8. **Testability and verification** — the change has evidence proportionate to risk, including deterministic tests, integration/e2e/property/security/eval layers when applicable.
9. **Maintainability and change isolation** — responsibilities are clear, complexity is bounded, interfaces are intentional and future changes do not require unnecessary cross-cutting edits.
10. **Compatibility, interoperability and migration** — existing consumers, protocols, schemas, APIs, data and tooling have an explicit compatibility/migration strategy when affected.
11. **Usability, accessibility and internationalization** — human-facing behavior is understandable and accessible; applicable interfaces consider relevant accessibility standards and language/locale behavior.
12. **Dependency and supply-chain integrity** — reuse-before-install, provenance, version pinning, transitive risk, licensing/permission and exact artifact trust are considered; Skill-specific policy remains in the Skill modules.
13. **Configuration, deployment, rollback and release safety** — environment/config changes, rollout sequencing, reversibility, migrations and rollback/fallback paths are defined when material.
14. **Safety, harm and compliance** — domain-specific safety, misuse, legal/regulatory or organizational obligations are surfaced when applicable.

A dimension may be non-material for a particular scope. Non-material does not mean forgotten; it means the triage found no requirement that must enter the current execution contract.

## Quality routing

Use three conceptual outcomes per dimension:

- `BASELINE` — ordinary engineering practice is sufficient; no special user-visible requirement is needed.
- `MATERIAL` — the dimension changes strategy, task constraints, acceptance, risk or operations and must be represented in the controlling contract/decision/evidence.
- `NOT_APPLICABLE` — the dimension genuinely does not apply to the current scope.

These outcomes need not be persisted as a full matrix. Persist the rationale only when future agents need it or when a `MATERIAL` requirement controls implementation/readiness.

## Security floor

Security triage is mandatory for every implementation scope.

Require a more explicit threat/security design when the scope materially introduces or changes any of the following:

- authentication, authorization or privilege;
- trust boundary or cross-system communication;
- externally controlled/untrusted input;
- network or public exposure;
- secrets, credentials or cryptographic material;
- personal/confidential/regulated data;
- executable plugins, scripts, dependencies, models, Skills or supply-chain artifacts;
- persistence/state whose compromise has material impact;
- security-sensitive configuration or deployment controls;
- abuse/fraud/destructive actions or meaningful multi-tenant isolation.

For security-sensitive data movement, a data-flow diagram with trust boundaries SHOULD accompany the Primary Solution Diagram when it adds risk clarity.

Security requirements must exist before implementation, not be deferred to post-implementation testing alone.

## Privacy floor

Privacy is related to but distinct from cybersecurity. A system may be secure against unauthorized access while still processing personal data in ways that create privacy risk.

When personal, confidential, regulated or otherwise sensitive information is material, Strategy must consider at least:

- necessity/minimization;
- source and purpose;
- storage/retention/deletion;
- disclosure/third-party flows;
- logging/telemetry exposure;
- access boundaries;
- user/operator visibility and control where applicable;
- applicable jurisdictional/domain obligations.

## Reliability and operations floor

For stateful, production, externally consumed or availability-sensitive changes, make the failure model explicit enough to answer:

- what can fail;
- what the user/system observes;
- whether retry is safe;
- how partial state is avoided/recovered;
- how the failure is detected/diagnosed;
- how service/state is restored or rolled back.

Observability is not synonymous with verbose logging. Collect only the evidence needed to understand and operate the system, subject to security/privacy constraints.

## Accessibility and usability floor

When the resulting scope is human-facing, interaction quality is an engineering requirement rather than cosmetic polish.

Apply appropriate accessibility/usability constraints to the actual interface type. For web content/interfaces, current WCAG guidance is the default external reference unless the project/domain specifies another standard.

Do not expose internal engineering vocabulary to end users merely because implementation uses it.

## Verification proportionality

The verification layer must be proportional to the failure/risk surface, not to how technically the Human Owner described the request.

A simple-looking natural-language request may require security, migration, load, property or integration verification. A code-native request may require only a focused deterministic check if its risk surface is genuinely small.

Do not add verification ceremony with no risk/acceptance value.

## Primary Solution Diagram gate

Before F5 can pass for an implementation scope, Strategy MUST present one **Primary Solution Diagram** representing the intended solution at the smallest useful abstraction for the Human Owner and the implementation boundary.

Select the primary diagram by the dominant design question:

| Dominant question | Preferred primary view |
| --- | --- |
| What systems/actors and boundaries are affected? | C4 System Context |
| What applications/services/data stores and responsibilities change? | C4 Container |
| What internal components/modules and dependencies change? | C4 Component |
| How do participants collaborate over time for this feature/use case? | Dynamic/sequence diagram |
| How does lifecycle/state change? | State diagram |
| How does sensitive/untrusted data cross processes/stores/trust boundaries? | Data-flow diagram with trust boundaries |
| How does persistent data structure/relationship change? | ER/data-model diagram |
| What local workflow/algorithm/dependency changes without architectural impact? | Compact flow/dependency diagram |

C4 is the default architecture family. Do not force C4 onto a change whose dominant question is behavioral, stateful, data-centric or security-flow-specific.

The diagram MUST:

- show the proposed solution rather than merely the current state;
- identify the change boundary;
- use labels appropriate to the Human Owner's current interaction register under `INTERACTION.md`;
- expose material external dependencies/trust boundaries when relevant;
- be consistent with the controlling engineering strategy/task contract;
- remain small enough to understand without loading unrelated architecture.

Additional diagrams are optional and should exist only when a single primary view cannot communicate a material concern.

## Diagram refresh rule

If implementation-relevant architecture, data flow, state model or responsibility boundaries change materially after the diagram is presented, F5/readiness is invalidated for the affected scope until Strategy refreshes the diagram and contract.

A cosmetic/local implementation detail that preserves the presented solution does not require re-presentation.

## User-visible disclosure

Do not recite this quality envelope by default.

Surface a quality concern when it:

- requires a Human decision;
- changes requested behavior/scope;
- changes meaningful cost/time/operational burden;
- creates a material risk/tradeoff;
- changes acceptance criteria;
- introduces an irreversible/migration/security/privacy consequence;
- is explicitly requested by the Human Owner.

Translate that concern through `INTERACTION.md` to the user's current register.

## External reference posture

External standards/frameworks are evidence sources and quality references, not automatic consumer dependencies.

Relevant reference families include:

- ISO/IEC 25010 product quality models;
- NIST SSDF and Cybersecurity Framework for security lifecycle practices;
- NIST Privacy Framework for privacy risk;
- OWASP threat modeling/security verification guidance;
- W3C WCAG for applicable web accessibility;
- established SRE/reliability practices;
- project/domain-native standards when they already control the repository.

Under `COEXISTENCE.md`, reuse an existing adequate project-native quality/security/SDD process rather than creating duplicate truth.
