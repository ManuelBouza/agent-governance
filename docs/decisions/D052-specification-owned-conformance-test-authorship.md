# D052 — Specification-owned conformance test authorship

Status: ACCEPTED  
Date: 2026-08-17  
Authority: Human Owner / ChatGPT Orchestrator

## Problem

Agent Governance previously assigned all committed non-Markdown test/eval implementation to the Agente de IA Ejecutor while ChatGPT Orchestrator owned normative Markdown, architecture, Task Contracts, acceptance criteria and semantic review.

That split is appropriate for ordinary implementation work, but it creates an avoidable second semantic translation for products whose correctness is primarily defined by Orchestrator-authored normative content, especially Agent Skills, governance/policy systems, agent-facing instruction architectures and documentation-managed protocols.

The prior flow can require the executor to load a broad set of normative documents, reconstruct the acceptance boundary, and then translate it into tests/evals before implementation. Internal evidence from T020, T030 and T032 shows that green suites and criterion-to-test mappings can still under-prove the intended semantic boundary when the negative-control or execution surface is narrower than the acceptance meaning.

The required distinction is therefore not `Orchestrator tests` versus `Executor tests`. It is between:

- **conformance/oracle artifacts that encode approved semantic acceptance**, and
- **implementation/exploration tests that validate technical realization**.

## Decision

Agent Governance adopts the following rule:

> **Test authorship follows semantic authority.**

When ChatGPT Orchestrator owns the normative specification/content that defines what correct behavior means, ChatGPT also owns the corresponding acceptance/conformance oracle unless a Task Contract explicitly selects another justified mode.

The Agente de IA Ejecutor remains responsible for executing verification, adapting technical harness mechanics, diagnosing failures, implementing the requested product behavior, and adding implementation-focused or exploratory tests.

This decision does not create a third agent role and does not make tests Governance authority.

```text
normative authority / Task Contract
        -> acceptance meaning
        -> conformance oracle
        -> executor implementation + execution
        -> evidence
        -> Orchestrator acceptance
```

## Test-Authorship-Mode

New or materially revised executable Task Contracts SHOULD declare one of these modes when test ownership is material:

### `orchestrator-conformance`

Use when the dominant correctness surface is an Orchestrator-owned normative specification, Agent Skill, governance/policy protocol, documentation-managed behavior, routing corpus, security policy, or analogous semantic product artifact.

ChatGPT owns the committed conformance/oracle assets needed to encode approved acceptance. The executor executes them and may add supplementary implementation tests.

### `executor-implementation`

Use for ordinary implementation work where the Task Contract defines objective outcomes/boundaries but the executor appropriately owns the technical design and its unit/integration/regression tests.

This remains the normal mode for consumer-application implementation and source-product technical work that does not require an Orchestrator-owned semantic oracle.

### `mixed`

Use when both surfaces are material.

ChatGPT owns the acceptance/conformance oracle; the executor owns implementation-specific, exploratory, property/fuzz, integration and regression tests that do not redefine that oracle.

If the mode is omitted, existing role/Task Contract semantics control. Do not infer a transfer of ownership merely because a task mentions tests.

## Orchestrator-owned conformance assets

Under `orchestrator-conformance` or `mixed`, ChatGPT MAY author and persist non-Markdown conformance/eval assets as an explicit exception to the repository's general non-Markdown executor ownership rule.

Eligible assets include only material that directly encodes approved acceptance semantics, for example:

- deterministic acceptance assertions;
- positive/negative/near-miss/cross-profile/ambiguous test cases;
- expected classifications/outcomes;
- frozen eval corpora and holdout partitions;
- acceptance thresholds and selection rules when represented as data;
- golden fixtures whose contents are part of the approved contract;
- security/adversarial acceptance cases;
- negative controls selected to prove a defined invariant boundary;
- deterministic graders/assertion logic whose expected meaning is specified by the Orchestrator;
- characterization cases explicitly accepted/frozen as the semantic baseline for a refactor.

This exception is narrow. It does not make ChatGPT the owner of general implementation code, runner internals, provider adapters, environment plumbing, benchmarks, traces, executor handoffs, ordinary unit tests, or technical debugging helpers.

## Preimplementation conformance gate

When an executable task uses `orchestrator-conformance` or `mixed` and the conformance assets are required for implementation/acceptance, they SHOULD be persisted and reviewed before the executor begins implementation.

Preferred sequence:

```text
Orchestrator specification / Task Contract
    -> Orchestrator conformance assets
    -> review + integrate into develop
    -> executor starts from that exact develop baseline
    -> executor implementation + supplementary tests
    -> executor executes complete required suite
    -> persisted evidence/handoff
    -> Orchestrator review/acceptance
```

This makes the executable oracle a deterministic projection of already-approved semantics before the implementation can optimize against or reinterpret them.

A conformance asset remains subordinate to its controlling Core/Decision/Task Contract. If a test conflicts with the normative specification, the specification controls and the test must be corrected through Orchestrator-owned persisted change.

## Executor responsibilities

The executor retains ownership of:

- execution of all required deterministic/property/eval/security/package verification;
- environment/toolchain use and compatible runner configuration;
- technical harness plumbing and host/provider adapters where authorized;
- reproduction and diagnosis of failing conformance tests;
- implementation code/config/assets;
- implementation-focused unit/integration/regression tests;
- property/state exploration, fuzzing and additional edge-case discovery;
- supplementary adversarial cases that do not redefine approved expected behavior;
- traces, measurements, result aggregation and verification evidence;
- executor handoff artifacts.

The executor SHOULD add useful tests discovered during implementation rather than relying only on the pre-authored conformance suite.

## Oracle-change boundary

The executor MAY correct a purely mechanical defect in an Orchestrator-owned conformance asset only when the applicable Task Contract or durable Orchestrator revision explicitly authorizes that class of correction and the approved semantics remain unchanged.

Examples of potentially mechanical corrections:

- broken import/path;
- fixture setup defect;
- runner/API compatibility issue;
- serialization syntax defect;
- environment-specific harness wiring.

The following are semantic oracle changes and MUST NOT be made unilaterally by the executor:

- expected result/classification;
- acceptance assertion meaning;
- positive/negative/near-miss classification;
- security expectation;
- material corpus membership chosen as acceptance coverage;
- threshold or victory/non-regression rule;
- frozen characterization meaning;
- removing/weakening a negative control because implementation fails it.

If the executor has evidence that an Orchestrator-owned oracle is semantically defective or inconsistent, it must stop that affected acceptance claim and report an `ORACLE_DEFECT`-equivalent blocker with evidence. ChatGPT then decides whether the test, implementation or specification is wrong and persists any semantic correction before execution continues.

## Independence and anti-overfitting

Specification-owned conformance testing does not eliminate independent technical verification.

The executor remains free and expected to discover additional failure modes through implementation tests, property/state-machine generation, fuzzing, adversarial analysis, cross-platform execution or other compatible techniques. High-risk work may still require a fresh or second executor to repeat verification.

The Orchestrator MUST NOT treat its pre-authored conformance suite as exhaustive merely because it is authoritative for acceptance meaning.

```text
Orchestrator conformance suite = required acceptance oracle
Executor supplementary suite   = independent technical exploration
Both                            = evidence, not acceptance authority
```

## Consumer-project boundary

This decision is source-product methodology and a reusable Governance pattern; it does not require the Orchestrator to author ordinary application unit tests in consumer repositories.

Default routing:

```text
Agent Skill / governance / policy / documentation-managed protocol
    -> orchestrator-conformance or mixed

ordinary consumer feature / business implementation
    -> executor-implementation
```

A consumer Task Contract may still select `mixed` or `orchestrator-conformance` when a Human/Orchestrator-owned acceptance oracle is genuinely material, but this is not the default.

## ICAE / RCAB relationship

D046 remains controlling for assurance-plane selection. D052 changes who authors certain conformance artifacts, not which verifier is appropriate.

The expected context benefit is architectural rather than assumed: a pre-authored conformance suite can allow the executor to load the Task Contract, implementation surface and focused failing-test references instead of reconstructing the entire semantic oracle from broad documentation. RCAB evidence should measure actual load paths before claiming a token reduction.

Tests/evals MUST NOT become a second normative authority or a shortcut around required controlling references. They are executable projections of acceptance semantics.

## Relationship to D041

D041 executor process autonomy remains accepted.

D041 explicitly permits method constraints when the method is material to an ownership, deterministic-verification, safety/security or reproducibility boundary. D052 establishes such an ownership boundary for conformance-oracle authorship while leaving the executor free to choose its internal implementation/testing process beyond that boundary.

## Relationship to earlier testing ownership

D052 prospectively refines and supersedes conflicting test-authorship clauses in D016, D019 and D046 and in operational ownership wording derived from those decisions.

The binary role model remains intact:

- ChatGPT Orchestrator: semantic specification, Markdown, acceptance meaning, and designated conformance/oracle assets;
- Agente de IA Ejecutor: authorized implementation, technical/exploratory tests, verification execution and evidence;
- Human Owner: final product/risk/release/override authority.

## Program adoption and grandfathering

D052 is prospective.

- T032 R1 remains governed by its already-launched contract/rework and is not re-scoped.
- T021 R1 remains governed by its existing contract and is not re-scoped.
- T022 may complete under its already-integrated runtime/profile contract without retrofitting a new authorship gate.
- MG1/T023 is the first strong planned application: MG1 should persist the D050/D051 topology definitions plus the D052 conformance corpus/expected classifications/threshold semantics before T023 execution.
- New Skill-authoring, governance/policy and documentation-managed protocol tasks should select `orchestrator-conformance` or `mixed` unless a different mode is justified.

Do not rewrite historical Task Contracts merely to label them retrospectively.

## Consequences

- `AGENTS.md` and Task Contract policy must represent the narrow Orchestrator non-Markdown conformance exception.
- future executor launch context can be narrower because acceptance semantics may already be executable, but actual RCAB impact must be measured;
- tests authored by ChatGPT must still be executed independently by the executor before acceptance;
- the executor cannot make a failing conformance suite green by silently weakening its expected semantics;
- ordinary consumer implementation continues to use executor-owned implementation testing by default;
- green conformance tests remain evidence, never Governance acceptance authority.
