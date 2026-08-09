# D019 — Testing and evaluation strategy

Status: ACCEPTED
Authority: Human Owner

## Decision

Agent Governance SHALL use a layered verification strategy combining deterministic code tests, property/state-machine tests, agent-facing evals, and security/supply-chain tests.

The normative operational strategy is `docs/TESTING-AND-EVALUATION.md`.

Mechanical invariants MUST be verified by deterministic code wherever practical. Agent/model evals are reserved for probabilistic or interpretive behavior such as Skill triggering, context routing, cold-start interpretation, handoff/blocker interpretation, and cross-agent portability. Human/ChatGPT review remains the final semantic/architectural acceptance layer.

## External basis

The strategy is informed by current specialized guidance from:
- Agent Skills structured Skill evaluation and trigger-description optimization;
- Anthropic agent evaluation guidance on trials, graders, traces, outcomes, isolation and regression suites;
- Open Policy Agent policy-testing practice;
- Hypothesis rule-based stateful testing;
- SLSA provenance/artifact verification;
- OWASP Agentic Skills security checklist.

Exact references, adopted techniques and local adaptations are documented in `docs/TESTING-AND-EVALUATION.md`.

## Scope

Verification covers:
- Governance Core deterministic mechanics;
- Consumer Governance Skill behavior;
- Maintainer Skill behavior;
- protocol/lifecycle/state transition properties;
- adapter and installed-footprint contracts;
- trigger positives/negatives/near misses;
- cold-start, progressive disclosure, handoff and recovery behavior;
- Skill provenance, immutable artifact identity, permission/dependency drift and adversarial security cases.

It does NOT benchmark whether an Agente de IA Ejecutor writes good application code in real consumer projects. D010 remains controlling for this boundary.

## Release consequences

Stable release gates MUST include:
- complete deterministic regression success;
- zero unresolved configured state-machine counterexamples;
- exact supply-chain identity/revocation verification;
- release-blocking security fixtures behaving as expected;
- mandatory cold-start/protocol behavior across supported adapter fixtures;
- measured trigger classification using repeated trials and held-out validation cases;
- representative transcript/outcome review.

Numeric trigger thresholds defined by the project are local release policy, not claimed industry standards.

## Implementation consequences

- test/eval code and harness implementation belongs to the Agente de IA Ejecutor under D016;
- ChatGPT Orchestrator owns test/eval contracts, Markdown strategy and acceptance meaning;
- initial implementation SHOULD prefer lightweight repository-owned tooling;
- Hypothesis is justified for complex stateful transition spaces but is not required for simple deterministic checks;
- OPA, hosted eval frameworks and security scanners are reference patterns/tools, not mandatory dependencies;
- synthetic fixtures MUST remain protocol-focused and production-independent.

## Local techniques

Agent Governance-specific techniques, such as placing canary markers in synthetic future-task records to detect premature reads through observable traces, MUST be labeled as local applications of established trace/outcome verification rather than external standards.