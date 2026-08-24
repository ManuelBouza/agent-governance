# Testing Skill / Capability Policy

Status: ACTIVE  
Controlling methodology: D019, D024, D046, D052

## Purpose

Define which Agent Skills and skill-like capabilities are required, optional, or prohibited when developing and executing `agent-governance` tests/evals, and how those capabilities route D052 test-authorship ownership.

This policy is source-product specific. It does not define the application-testing Skills that consumer repositories may use.

## Core rule

**The test suite is code, not a Skill.**

Deterministic and property/state-machine tests must be executable by ordinary repository tooling without model-driven Skill activation.

Skills may improve routing, procedural consistency, semantic-oracle authoring, or specialized context, but they cannot become hidden prerequisites for test correctness, CI, or release verification.

Test/eval ownership is independent from whether a Skill is used. D052 controls semantic conformance authorship:

```text
orchestrator-conformance / mixed
    Orchestrator -> required semantic conformance/oracle assets
    Executor     -> execution + supplementary technical/exploratory tests

executor-implementation
    Executor     -> implementation/exploration tests + execution
```

Tests/evals are executable evidence, never Governance authority.

## Capability matrix

| Test/eval surface | Project-owned Skill requirement | Capability/context | D052 ownership guidance | External Skill requirement |
|---|---|---|---|---|
| D019 Layer 1 deterministic | None required; Maintainer Skill optional routing when available | D023 Python/pytest, repository invariants, synthetic fixtures, Task Contract/handoff | Usually Executor implementation testing; exact normative acceptance assertions may be Orchestrator-owned when the Task Contract selects `orchestrator-conformance`/`mixed` | None |
| D019 Layer 2 property/state-machine | None required; Maintainer Skill optional routing | Hypothesis stateful/property guidance and approved invariants | Executor owns exploratory/property generation; frozen semantic properties/expected invariants may be Orchestrator-owned when explicitly designated | None |
| D019 Layer 3 adapter/install contracts | None required; Maintainer Skill optional routing | fixture/install boundary knowledge, adapter-neutral expectations | Often `mixed`: Orchestrator may own accepted portability/install oracle semantics; Executor owns harness, integration mechanics and execution | None |
| D019 Layer 4 Skill trigger evals | Maintainer Skill is the project-owned routing Skill when available | trigger corpus design, positives/negatives/near misses, repeated trials, holdout | Skill/governance acceptance corpora, expected classifications and thresholds are strong D052 Orchestrator-conformance candidates; Executor executes and may add supplementary cases | Optional audited authoring/eval Skill only |
| D019 Layer 5 Governance behavior evals | Maintainer Skill is the project-owned routing Skill when available | clean-context trials, traces/outcomes, grader selection, portability | Usually `mixed` when normative behavior/expected outcome is Orchestrator-owned; Executor owns runner/provider mechanics, trials, traces and supplementary exploration | Optional audited eval assistance only |
| D019 Layer 6 security/adversarial | Maintainer Skill is the project-owned routing Skill when available | Skill supply-chain/security policies, isolated adversarial fixtures | Semantic security acceptance/negative controls may be Orchestrator-owned; Executor owns technical adversarial execution and may add supplementary attacks | Optional audited security Skill only |

The table does not force one authorship mode solely from D019 layer number. The governing Task Contract or durable Orchestrator gate selects the mode when ownership is material.

## Maintainer Skill composition

The Maintainer Skill should remain one coherent source-maintenance Skill surface unless D050/MG1/T023 later accepts another generated activation topology.

It SHOULD progressively disclose testing detail through internal references/resources instead of creating separate top-level Skills for every framework or test layer.

Conceptual routing:

```text
maintainer-skill
  -> Orchestrator semantic-conformance route when D052 assigns it
  -> Executor technical verification route
       -> deterministic testing context
       -> stateful/property testing context
       -> Skill/eval execution context
       -> security/supply-chain testing context
```

These are role/context routes, not new agent roles or independently versioned Skills.

The exact package filenames are deferred until Maintainer Skill implementation/topology gates, but each reference must state when it should be loaded so unrelated test context is not preloaded.

## D052 conformance boundary

When a source Task Contract selects `orchestrator-conformance` or `mixed`:

- the Orchestrator may author the narrow non-Markdown conformance assets permitted by D052;
- required oracle assets should be persisted/reviewed before implementation when they are needed to define acceptance;
- the Executor executes the complete required suite and remains responsible for environment/harness mechanics, traces, measurements and evidence;
- the Executor should add implementation, integration, property/fuzz, edge-case and supplementary adversarial tests rather than treating the Orchestrator suite as exhaustive;
- a purely mechanical oracle defect may be corrected only when the applicable durable contract authorizes that correction class;
- expected results, semantic classifications, thresholds, acceptance assertions and negative-control meaning may not be weakened unilaterally by the Executor;
- a semantic disagreement uses the D052 `ORACLE_DEFECT` boundary.

Use `docs/CONFORMANCE-ORACLE-CONTRACT.md` for oracle identity/freeze/revision rules rather than duplicating them here.

## Skills that are NOT required

Do not create or mandate any of the following merely to execute the approved test stack:

- a generic `pytest` Skill;
- a generic `python-testing` Skill;
- a generic `test-runner` Skill;
- a generic TDD Skill;
- an executor-product-specific OpenCode/Codex/Claude testing Skill.

The Executor's normal coding capability plus repository contracts and pytest/Hypothesis tooling are sufficient for test execution and technical mechanics. The Orchestrator's D052 conformance-authoring responsibility likewise does not require an extra generic testing Skill.

A future additional top-level Skill requires evidence that:
1. it represents a coherent user intent distinct from Maintainer Skill activation;
2. a capable agent performs materially better with it than without it;
3. trigger evals demonstrate an acceptably low overlap/false-positive rate;
4. it does not duplicate canonical repository policy or ordinary tool documentation;
5. its supply chain and permission envelope are approved;
6. it remains a generated/product-consistent projection under D050 rather than an independently maintained Governance authority.

## External Skill-authoring/evaluation capability

Skill-specific work in D019 Layers 4–6 may benefit from an external Skill that specializes in creating or evaluating Agent Skills.

Such a Skill is **optional**, not required.

If one is used:
- it must be discovered/audited under `governance-core/SKILL-DISCOVERY.md` and `governance-core/SKILL-SUPPLY-CHAIN.md`;
- generated test cases, descriptions, expected outcomes or reports remain candidate artifacts until accepted by the repository role that owns their semantics under D052;
- product-specific mechanics must not redefine Agent Governance semantics;
- absence of the external Skill cannot block canonical regression testing or D052 conformance authoring.

Anthropic's public `skill-creator` is a useful reference pattern: it combines creation, improvement, eval generation/execution, benchmarking, and trigger-description optimization inside one coherent Skill. It is not adopted as a mandatory dependency.

## Consumer Skill boundary

The Consumer Governance Skill must not trigger for:
- source-repository pytest/Hypothesis work;
- Maintainer Skill trigger/eval development;
- source-product release verification;
- source-product security/supply-chain testing.

Those activities belong to source-product maintenance.

Conversely, the Maintainer Skill must not become the generic testing Skill for consumer application code.

## No-Skill bootstrap path

The source repository must remain testable before and after Maintainer Skill release.

### Orchestrator conformance authoring

When D052 assigns semantic conformance ownership, a cold Orchestrator resumes from:

1. `AGENTS.md`;
2. `docs/orchestrator/CHECKPOINT.md`;
3. the exact controlling Decision/Task Contract/functional contract;
4. D052 + `docs/CONFORMANCE-ORACLE-CONTRACT.md` only when oracle authoring/revision is material;
5. the smallest assurance-plane references needed for the case being encoded.

The Orchestrator does not need an implemented Maintainer Skill to author/review its designated oracle assets.

### Executor test/eval execution

An Executor performs authorized source test/eval execution by reading:

1. `AGENTS.md`;
2. the assigned `docs/tasks/TNNN-*.md` contract;
3. any frozen required Orchestrator conformance assets designated by that contract;
4. only the controlling references named by that task;
5. the approved local test/development tooling.

This path remains supported after the Skill exists and serves as the fallback/audit path.

Nothing in this policy asserts completion of the T022 source-maintainer profile/Skill runtime before its normal acceptance gate.

## Research references

- Agent Skills specification: https://agentskills.io/specification
- Agent Skills best practices: https://agentskills.io/skill-creation/best-practices
- Agent Skills progressive-disclosure client model: https://agentskills.io/client-implementation/adding-skills-support
- Anthropic public `skill-creator`: https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md

These sources support coherent Skill scope and progressive disclosure. The specific testing-capability decomposition and D052 ownership overlay above are Agent Governance policy, not an external standard.
