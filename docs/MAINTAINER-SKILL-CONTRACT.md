# Maintainer Skill Functional Contract

Status: DESIGN-APPROVED

## Purpose

Define the Agent Skill used only for developing, refactoring, testing, evaluating, and releasing the canonical `agent-governance` source product.

This Skill is NOT the consumer Governance Skill and MUST NOT install or operate a live consumer-project governance instance in this repository.

This contract describes the intended source-maintainer capability surface. It does not by itself assert completion of the T022 runtime/profile implementation.

## Activation boundary

Trigger for work such as:
- changing Governance Core architecture or instructions;
- implementing/refactoring source-product tooling;
- creating or modifying conformance/oracle tests, implementation tests or eval assets according to D052/D068 ownership;
- running product verification;
- applying `docs/DEVELOPMENT-WORKFLOW.md` or `docs/REFACTORING-WORKFLOW.md`;
- preparing releases or migration artifacts;
- validating source-product structure and public distribution readiness.

Do not trigger merely because another repository uses Agent Governance.

## Repository context

The Skill MAY route to source-specific context including:
- `AGENTS.md`;
- `docs/DEVELOPMENT-WORKFLOW.md`;
- `docs/REFACTORING-WORKFLOW.md`;
- `docs/BRANCHING.md`;
- `docs/RELEASES.md`;
- `docs/TESTING-AND-EVALUATION.md`;
- `docs/TESTING-SKILL-CAPABILITIES.md`;
- `docs/CONFORMANCE-ORACLE-CONTRACT.md` when D052 conformance ownership is material;
- `docs/LIBRARY-FIRST-SOURCE-MAINTENANCE.md` and D068 when Library-first candidate materialization is active;
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`;
- `docs/decisions/D023-python-testing-stack.md`;
- `docs/decisions/D024-testing-skill-capability-model.md`;
- `docs/decisions/D025-local-development-toolchain.md`;
- `docs/decisions/D052-specification-owned-conformance-test-authorship.md` when test/eval authorship is material;
- `docs/decisions/D068-library-first-candidate-materialization-executor-verification-boundary.md` for D068-mode source maintenance;
- assigned `docs/tasks/` Task Contracts and `handoffs/` policy;
- product Decision Records;
- `governance-core/`;
- `governance-skill/`;
- `maintainer-skill/`;
- `tests/` and `evals/`.

It MUST preserve progressive context loading rather than preloading the whole repository.

## Role-aware progressive routing

The Maintainer Skill is one source-maintenance Skill with two internal role routes. It MUST NOT be split into separate top-level `ChatGPT Orchestrator Skill` and `Executor Skill` merely because the repository has two agent roles.

The Skill selects the smallest route required by the active source-maintenance role and task:

```text
maintainer-skill
  -> Orchestrator route
  -> Executor route
```

The routes are context/routing surfaces only. They do not create new authority, replace repository policy, or alter the binary role model. Role/test ownership follows current repository policy, including D016/D053 as prospectively refined by D052 and D068 for source maintenance.

### D068 route boundary

For D068-mode source maintenance:

```text
Stages 1-4  Explore / Specify / Design / Plan & Trace
            -> Orchestrator route
Stage 5     Complete candidate materialization
            -> Orchestrator route
Stage 6     Execute / diagnose / bounded repair / verify
            -> Executor route
Stage 7     Converge / accept / integrate / evolve
            -> Orchestrator route
```

The Orchestrator publishes the coherent candidate and controlling authority on the verified topic branch before the Executor route begins. That topic-branch checkpoint is sufficient Stage 6 authority; no separate planning/candidate merge into `develop` is required first.

D052 semantic-oracle ownership, D054 execution-mechanics ownership, D060 coordinator continuity, D061/D062 protections/freshness, and D065 delegation obligations remain intact. D068 does not change Governance Core or consumer-project SDD semantics. Historical executed Task Contracts, handoffs, reviews, and evidence retain their original meaning.

### Orchestrator route

Use when the active role is ChatGPT Orchestrator and the work concerns strategy, research synthesis, architecture, Decision Records, Task Contracts, committed Markdown, acceptance/review, Executor launch/handoff control, Orchestrator checkpointing, D052-designated semantic conformance/oracle authoring, or D068 Stage 5 complete candidate materialization.

The route SHOULD progressively disclose only the required source-maintenance context, such as:

- `AGENTS.md`;
- `docs/orchestrator/CHECKPOINT.md` and `docs/ORCHESTRATOR-CHECKPOINTS.md`;
- `docs/TASK-CONTRACTS.md` and `docs/EXECUTOR-HANDOFFS.md`;
- D052 + `docs/CONFORMANCE-ORACLE-CONTRACT.md` when semantic conformance assets are being authored/revised;
- D066/D068 + `docs/LIBRARY-FIRST-SOURCE-MAINTENANCE.md` when candidate materialization uses the Library-first adapter;
- applicable development/refactoring/branch/release policy;
- the smallest relevant Decision Records and Core modules;
- current Task Contract/review artifacts when the frontier requires them.

For D068-mode work, the Orchestrator route may materialize all in-scope candidate artifacts during Stage 5, including source code, tests, configuration, schemas, fixtures, scripts, and documentation. That authority remains subordinate to the approved specification/Design/Plan and does not transfer D054 command/API/browser execution mechanics or Stage 6 verification authority to ChatGPT.

Outside D068-mode Stage 5 or another explicit accepted exception, the Skill MUST NOT infer new non-Markdown authorship merely because it can describe the work.

### Executor route

Use when the active role is the product-agnostic Agente de IA Ejecutor and executable source work has been authorized by a persisted Task Contract/published candidate checkpoint.

For D068 mode, the route SHOULD progressively disclose only the Stage 6 execution context required by that contract, such as:

- `AGENTS.md`;
- exactly the assigned Task Contract and its controlling references;
- exact published topic-branch candidate identity;
- frozen Orchestrator-owned conformance assets when the Task Contract selects `orchestrator-conformance` or `mixed`;
- `docs/EXECUTOR-HANDOFFS.md`;
- applicable local toolchain/test/eval guidance;
- relevant implementation/test surfaces and synthetic fixtures.

The Executor route MUST NOT expose a parallel strategy layer or allow the Executor to edit committed Markdown, expand task scope, redefine acceptance, silently change semantic oracle meaning, infer task semantics from prior chat history, or recreate a D068 candidate from scratch. It may make bounded technical repairs only inside the approved Stage 6 envelope and must rerun affected verification.

### Role-routing invariants

```text
role != Skill
Skill routing != authority
D068 Orchestrator route = Stage 5 complete candidate materialization
D068 Executor route = Stage 6 execution / diagnosis / bounded repair / verification
Executor route != strategy/acceptance/oracle-semantic ownership
D052 conformance ownership != third role
```

A single session MUST NOT blend the two routes in a way that changes ownership semantics. If the operating role changes, the caller must establish the new role explicitly and reload only the context appropriate to that role.

Standing rules remain canonical in Git. The Skill SHOULD reference repository policy rather than duplicate it in role-local instructions.

A future separate top-level source-maintenance Skill for either role requires new evidence of a distinct non-overlapping intent, measurable routing benefit, acceptable trigger separation, and an explicit Human/Orchestrator architecture decision.

## Testing/evaluation capability routing

The Maintainer Skill is the project-owned source-maintenance Skill surface for source-product testing/evaluation work. It does not replace the test runner and source tests MUST remain runnable without the Skill.

D052 controls semantic-oracle ownership; D068 controls Stage 5/6 authorship/execution for D068-mode source maintenance:

```text
D068 Stage 5
    Orchestrator -> complete candidate tests/evals as in-scope materialization

orchestrator-conformance / mixed
    Orchestrator -> semantic conformance/oracle meaning

D068 Stage 6
    Executor -> execution + diagnosis + bounded technical test/implementation repair
              + supplementary technical coverage inside approved semantics
```

When test/eval maintenance is in scope, the Skill SHOULD route progressively to the smallest relevant capability area:

1. **Deterministic test maintenance** — Python/pytest source-product invariants, synthetic fixtures, local deterministic verification and persisted evidence, with semantic oracle ownership separated under D052 and D068 Stage 5/6 ownership respected.
2. **Property/state-machine testing** — Hypothesis stateful/property work only when D019 Layer 2 applies; semantic frozen conformance meaning remains Orchestrator-owned when designated, while Stage 6 execution/technical repair remains Executor-owned.
3. **Skill/eval maintenance** — trigger corpora, near misses, repeated clean-context trials, baseline comparison and grader selection; expected semantic classifications/thresholds follow D052 when Orchestrator-owned acceptance is material.
4. **Security/supply-chain testing** — identity/digest/envelope checks plus adversarial Skill fixtures and isolated dynamic checks when separately authorized; semantic acceptance cases may be Orchestrator-owned while technical execution remains Executor-owned.

These capability areas SHOULD be represented through on-demand references/resources inside the eventual Maintainer Skill package rather than separate broad top-level testing Skills unless future trigger/eval evidence demonstrates a distinct, non-overlapping need.

The Maintainer Skill MUST NOT require an external generic pytest/testing/TDD Skill to perform normal source-product testing. External Skills may be supplemental only after approval under the applicable discovery/supply-chain and coexistence policies.

Tests/evals remain evidence rather than Governance authority. If an Executor finds a semantic defect in an Orchestrator-owned oracle, it must use the D052 `ORACLE_DEFECT` boundary rather than weakening expected behavior unilaterally.

## Local toolchain routing

When executable source work requires local setup/verification, the Maintainer Skill SHOULD route the Executor Stage 6 surface to `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md` instead of embedding product-specific installation recipes in its top-level activation instructions.

The Maintainer Skill must preserve these boundaries:
- Git/uv/Python/pytest/Ruff are source-maintainer tooling defined by D023/D025;
- D054 gives the Executor ownership of concrete command/API/SDK/browser/computer-use mechanics during delegated execution;
- the executor host itself remains product-neutral and external to the repository dependency graph;
- GitHub CLI is optional when normal Git authentication already works;
- Ruff must not be allowed to rewrite ChatGPT-owned Markdown;
- source-maintainer tool choices must not be projected automatically into consumer repositories.

Detailed tool commands should be loaded only for tasks that actually execute/verify code.

## Bootstrap / no-Skill operation

The Maintainer Skill is operational assistance, not canonical authority and not a prerequisite for source maintenance or test correctness.

A cold ChatGPT Orchestrator MUST be able to resume source-product orchestration from:
- current `develop`;
- `AGENTS.md`;
- `docs/orchestrator/CHECKPOINT.md`;
- only the additional repository context required by that checkpoint or a concrete conflict.

For D068-mode work, a cold Agente de IA Ejecutor MUST be able to execute/verify an authorized source task from:
- the exact coherent published topic-branch candidate;
- `AGENTS.md` applicable to that represented state;
- the persisted Task Contract;
- the Task Contract's controlling repository references;
- any frozen Orchestrator-owned conformance assets designated by that Task Contract;
- the approved local development/test tooling.

A separate planning/candidate merge into `develop` is not a prerequisite for that D068 Stage 6 bootstrap. D061/D062 freshness and protected-base relationships still must be established.

These bootstrap paths are required so the repository can test and develop the Maintainer Skill before that Skill itself is released. CI and deterministic release checks MUST NOT depend on model-driven Skill activation.

## Agent roles

The Skill follows the repository operating model:
- ChatGPT Orchestrator owns strategy, architecture, Task Contracts, review, handoffs, committed Markdown, acceptance meaning, D052-designated semantic conformance/oracle assets, and D068 Stage 5 complete candidate materialization when that mode applies;
- the product-agnostic Agente de IA Ejecutor owns D068 Stage 6 execution, diagnosis, bounded technical repair, verification execution, measurements/evidence and handoffs, and executes required Orchestrator conformance assets when applicable;
- Human Owner retains final authority.

No executor product receives special governance status.

## Branch discipline

All normal product changes follow `docs/BRANCHING.md`:
- `main` stable;
- `develop` integration;
- work on short-lived topic branches;
- no normal direct writes to `main` or `develop`;
- normal PR target is `develop`;
- promotion to `main` occurs only through release/stability review.

For D068-mode work, the short-lived topic branch remains the candidate/verification surface through Stages 5-6 before Stage 7 PR integration. This does not weaken D061/D062 protection or freshness requirements.

## Explicitly out of scope

The Maintainer Skill MUST NOT:
- initialize consumer `MISSION`, `WORKPLAN`, `STATE`, or `EXCHANGE` in this source repository;
- treat this source repository as a real consumer instance;
- implement application/business features for unrelated consumer projects;
- redefine Governance Core authority inside Skill-local instructions;
- become a mandatory runtime dependency for deterministic source tests;
- duplicate generic pytest/Hypothesis/uv/Ruff documentation when task-specific repository guidance is sufficient;
- impose the source repository's uv/Python/Ruff stack on consumer projects;
- let the Executor redefine D052 semantic oracle meaning to make a failing suite pass;
- treat an Orchestrator-owned conformance suite as exhaustive independent technical verification;
- split into role-named top-level Skills without a separately approved architecture change;
- bypass release, branch, supply-chain, toolchain, Task Contract, D066/D068, or role ownership rules.

## Acceptance

The Maintainer Skill is acceptable only if:
1. it activates for source-product maintenance and not ordinary consumer governance;
2. it respects ChatGPT Orchestrator vs Agente de IA Ejecutor ownership, including D052 semantic-oracle ownership and D068 Stage 5/6 ownership;
3. it uses distinct internal Orchestrator and Executor routing without creating additional governance roles or top-level role Skills;
4. each route progressively loads only the context needed by its active role/task and never blends ownership semantics;
5. it follows PD/RF, D068 publication sequencing, and branch policy correctly;
6. it can guide a cold maintainer session without requiring chat history;
7. both Orchestrator and Executor retain documented no-Skill bootstrap paths;
8. it routes testing/evaluation work to the smallest relevant capability/context without requiring generic overlapping testing Skills;
9. it preserves D052 semantic conformance meaning while allowing D068 candidate test materialization and Stage 6 technical execution/repair without making tests authority;
10. it routes executable Stage 6 work to the repository-declared local toolchain without making the Skill itself a tool installer;
11. source-product deterministic tests remain executable when the Maintainer Skill is absent/disabled;
12. it never creates a live consumer instance in the source repository;
13. removing the Maintainer Skill does not alter the canonical product itself;
14. nothing in this design contract implies completion of the T022 source-maintainer runtime/profile implementation before its normal acceptance gate.
