# D024 — Testing Skill capability model

Status: ACCEPTED
Authority: Human Owner

## Decision

Testing and evaluation of the canonical `agent-governance` source product SHALL NOT require a separate generic "testing", "pytest", "TDD", or "test-runner" Agent Skill.

The source-product **Maintainer Skill** defined by D017 is the only project-owned top-level Skill intended to activate for source-repository test/eval maintenance. It routes progressively to the repository's testing contracts and task-specific capability references; it does not duplicate pytest/Hypothesis documentation or become the test runner itself.

The test/eval suites MUST remain executable without any Agent Skill installed. Repository Markdown contracts plus the approved code/tooling are sufficient authority for correctness and for bootstrapping the Maintainer Skill itself.

## Required capability model

The Maintainer Skill SHALL expose or route to the following source-maintenance capabilities when relevant:

1. **Deterministic test maintenance**
   - repository/layout/reference/policy checks;
   - Python/pytest conventions from D023;
   - synthetic fixture construction;
   - local deterministic verification and persisted evidence.

2. **Property/state-machine test maintenance**
   - Hypothesis-based generated/stateful verification only when D019 Layer 2 applies;
   - invariant/counterexample handling;
   - conversion of useful minimized failures into regression cases.

3. **Skill/eval maintenance**
   - Consumer and Maintainer Skill trigger corpora;
   - positive/negative/near-miss cases;
   - with-Skill vs baseline/previous-version comparison;
   - repeated clean-context trials;
   - deterministic/model/human grader routing according to D019.

4. **Security/supply-chain test maintenance**
   - canonical source/revision/digest and approval-envelope checks;
   - malicious/adversarial synthetic Skill fixtures;
   - permission/dependency/external-reference drift cases;
   - isolated dynamic checks when later tooling explicitly authorizes them.

These are **capability areas**, not four additional top-level Agent Skills.

## Progressive disclosure

The Maintainer Skill SHOULD keep its activation surface focused on source-product maintenance and load detailed testing context only for tasks that need it.

Its eventual package SHOULD therefore route from a concise `SKILL.md` to task-specific references/resources such as deterministic testing, stateful testing, Skill evals, and security testing. Exact filenames/package layout may be finalized during Maintainer Skill implementation, but the semantic rule is fixed: specialized testing detail is disclosed on demand rather than preloaded or split into broad overlapping top-level Skills without evidence.

## Bootstrap invariant

The Maintainer Skill is operational tooling, not authority and not a prerequisite for repository correctness.

Therefore:
- T001 and other source-product tests may execute before the final Maintainer Skill exists;
- a cold executor can work from `AGENTS.md`, the persisted Task Contract, controlling repository references, and approved tooling;
- CI/test execution MUST NOT depend on model-driven Skill activation;
- removing/disabling the Maintainer Skill cannot make deterministic tests impossible to run.

This avoids a circular dependency in which the Skill would be required to test the code/evals used to validate that same Skill.

## External Skills

External Skills MAY be used as supplemental development aids only when explicitly approved under the Skill discovery/supply-chain policy and later coexistence rules.

They are never canonical test dependencies and their output does not replace repository-owned tests/evals.

In particular:
- an external Skill-authoring/evaluation Skill may assist with generating cases or reviewing a Skill;
- an external security/testing Skill may assist analysis;
- no external Skill is required for T001 acceptance, deterministic CI, release regression, or reconstruction of test semantics.

The official Anthropic `skill-creator` Skill is a useful reference pattern because it combines Skill creation, improvement, evaluation, benchmarking, and trigger optimization in one coherent Skill rather than requiring a separate testing Skill. Agent Governance does **not** depend on that implementation or its Claude-specific mechanics.

## Consumer Skill exclusion

The Consumer Governance Skill MUST NOT activate for maintenance of source-product tests/evals in this repository.

Source testing belongs to the Maintainer Skill boundary. Consumer projects may have their own application-testing Skills, but those are outside the source-product testing capability defined here.

## Why no generic testing Skill

Agent Skills guidance recommends coherent, well-scoped Skills and notes that if an agent already handles a task well without a Skill, the Skill may not add value. A generic pytest/test-runner Skill would mostly restate tool documentation and compete with ordinary coding capability.

The specialized knowledge that *is* valuable here is Agent Governance-specific: which invariants matter, which suite/layer applies, how Task Contracts/handoffs work, how source vs consumer boundaries behave, and how Skill trigger/security evals are interpreted. That knowledge belongs under the Maintainer Skill and canonical repository contracts.

## Research basis

### Agent Skills specification

https://agentskills.io/specification

Relevant points:
- a Skill packages specialized instructions and may bundle scripts/references/assets;
- `description` states what the Skill does and when to use it;
- large Skills should use referenced resources and progressive disclosure;
- environment/tool requirements can be described separately from task semantics.

### Agent Skills — Best practices for skill creators

https://agentskills.io/skill-creation/best-practices

Relevant points:
- Skills should represent coherent units of work;
- overly narrow Skills force unnecessary multi-Skill loading, while overly broad Skills trigger imprecisely;
- if the agent already handles the whole task well without a Skill, the Skill may not add value;
- detailed material should be moved to references and loaded when needed.

### Agent Skills — Adding Skills support

https://agentskills.io/client-implementation/adding-skills-support

Relevant points:
- skills-compatible clients use three-tier progressive disclosure: catalog, activated instructions, and resources on demand;
- Skills are specialized guidance layered over the agent/tool environment rather than replacements for the underlying tools.

### Anthropic `skill-creator` reference implementation

https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md

Relevant pattern:
- one coherent Skill covers creation, improvement, evaluation, benchmarking, and trigger optimization;
- its own workflow explicitly avoids requiring another generic testing Skill.

This implementation is cited as evidence of a composition pattern, not as a mandatory Agent Governance dependency.

## Consequences

- `docs/MAINTAINER-SKILL-CONTRACT.md` must include progressive routing for the four testing capability areas.
- `docs/TESTING-AND-EVALUATION.md` must state that Skills assist routing/knowledge but never form a prerequisite for deterministic execution.
- T001's Skill/capability readiness blocker is resolved by this decision; T001 remains blocked only on the local development toolchain and coexistence/non-overlap policy.
- no `testing-skill/`, `pytest-skill/`, or equivalent new project-owned top-level Skill is created by default.
- creation of any future additional top-level testing Skill requires evidence from trigger/eval results that it has a distinct user intent, adds measurable value, and does not create an overlap problem with the Maintainer Skill.
