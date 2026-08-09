# Testing Skill / Capability Policy

Status: ACTIVE

## Purpose

Define which Agent Skills and skill-like capabilities are required, optional, or prohibited when developing and executing `agent-governance` tests/evals.

This policy is source-product specific. It does not define the application-testing Skills that consumer repositories may use.

## Core rule

**The test suite is code, not a Skill.**

Deterministic and property/state-machine tests must be executable by ordinary repository tooling without model-driven Skill activation.

Skills may improve routing, procedural consistency, or specialized context, but they cannot become hidden prerequisites for test correctness, CI, or release verification.

## Capability matrix

| Test/eval surface | Project-owned Skill requirement | Capability/context | External Skill requirement |
|---|---|---|---|
| D019 Layer 1 deterministic | None required; Maintainer Skill optional routing when available | D023 Python/pytest, repository invariants, synthetic fixtures, Task Contract/handoff | None |
| D019 Layer 2 property/state-machine | None required; Maintainer Skill optional routing | Hypothesis stateful/property guidance and approved invariants | None |
| D019 Layer 3 adapter/install contracts | None required; Maintainer Skill optional routing | fixture/install boundary knowledge, adapter-neutral expectations | None |
| D019 Layer 4 Skill trigger evals | Maintainer Skill is the project-owned routing Skill when available | trigger corpus design, positives/negatives/near misses, repeated trials, holdout | Optional audited authoring/eval Skill only |
| D019 Layer 5 Governance behavior evals | Maintainer Skill is the project-owned routing Skill when available | clean-context trials, traces/outcomes, grader selection, portability | Optional audited eval assistance only |
| D019 Layer 6 security/adversarial | Maintainer Skill is the project-owned routing Skill when available | Skill supply-chain/security policies, isolated adversarial fixtures | Optional audited security Skill only |

## Maintainer Skill composition

The Maintainer Skill should remain one coherent top-level source-maintenance Skill.

It SHOULD progressively disclose testing detail through internal references/resources instead of creating separate top-level Skills for every framework or test layer.

Conceptual routing:

```text
maintainer-skill
  -> deterministic testing context
  -> stateful/property testing context
  -> Skill/eval context
  -> security/supply-chain testing context
```

The exact package filenames are deferred until Maintainer Skill implementation, but each reference must state when it should be loaded so unrelated test context is not preloaded.

## Skills that are NOT required

Do not create or mandate any of the following merely to execute the approved test stack:

- a generic `pytest` Skill;
- a generic `python-testing` Skill;
- a generic `test-runner` Skill;
- a generic TDD Skill;
- an executor-product-specific OpenCode/Codex/Claude testing Skill.

The executor's normal coding capability plus repository contracts and pytest/Hypothesis tooling are sufficient for these mechanics.

A future additional top-level Skill requires evidence that:
1. it represents a coherent user intent distinct from Maintainer Skill activation;
2. a capable executor performs materially better with it than without it;
3. trigger evals demonstrate an acceptably low overlap/false-positive rate;
4. it does not duplicate canonical repository policy or ordinary tool documentation;
5. its supply chain and permission envelope are approved.

## External Skill-authoring/evaluation capability

Skill-specific work in D019 Layers 4–6 may benefit from an external Skill that specializes in creating or evaluating Agent Skills.

Such a Skill is **optional**, not required.

If one is used:
- it must be discovered/audited under `governance-core/SKILL-DISCOVERY.md` and `governance-core/SKILL-SUPPLY-CHAIN.md`;
- generated test cases, descriptions, or reports remain candidate artifacts until verified by repository-owned evals/review;
- product-specific mechanics must not redefine Agent Governance semantics;
- absence of the external Skill cannot block canonical regression testing.

Anthropic's public `skill-creator` is a useful reference pattern: it combines creation, improvement, eval generation/execution, benchmarking, and trigger-description optimization inside one coherent Skill. It is not adopted as a mandatory dependency.

## Consumer Skill boundary

The Consumer Governance Skill must not trigger for:
- source-repository pytest/Hypothesis work;
- Maintainer Skill trigger/eval development;
- source-product release verification;
- source-product security/supply-chain testing.

Those activities belong to source-product maintenance.

Conversely, the Maintainer Skill must not become the generic testing Skill for consumer application code.

## Bootstrap path before Maintainer Skill release

Until the Maintainer Skill is implemented and released, an executor performs source test/eval tasks by reading:

1. `AGENTS.md`;
2. the assigned `docs/tasks/TNNN-*.md` contract;
3. only the controlling references named by that task;
4. the approved local test/development tooling.

This path remains supported after the Skill exists and serves as the fallback/audit path.

## Research references

- Agent Skills specification: https://agentskills.io/specification
- Agent Skills best practices: https://agentskills.io/skill-creation/best-practices
- Agent Skills progressive-disclosure client model: https://agentskills.io/client-implementation/adding-skills-support
- Anthropic public `skill-creator`: https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md

These sources support coherent Skill scope and progressive disclosure. The specific four-capability decomposition above is Agent Governance policy, not an external standard.
