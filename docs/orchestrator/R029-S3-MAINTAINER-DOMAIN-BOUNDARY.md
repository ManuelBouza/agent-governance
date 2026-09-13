# R029-S3 — Maintainer Skill Domain Boundary

Status: COMPLETE  
Parent: `R029 — AGENTS.md / Skill Architecture Refactor Research`  
Subtask: `R029-S3 — Maintainer Skill domain boundary`  
Baseline-Develop: `44760f50c9763de22b712423a99548179b0da9b1`  
Inputs: `docs/orchestrator/R029-S1-ROOT-PRESERVATION-MAP.md`, `docs/orchestrator/R029-S2-LEAN-ROOT-RESPONSIBILITY-CONTRACT.md`, `docs/MAINTAINER-SKILL-CONTRACT.md`  
Decision-State: EVALUATING  
Normative-Effect: none

## Purpose

Define the boundary of the existing Agent Governance source-product Maintainer Skill after S1 preservation and S2 lean-root separation. This artifact does not redesign or implement the Skill. It classifies which routed responsibilities remain Agent-Governance-specific domain material and which semantics may be evaluated later as transverse capabilities.

The approved Maintainer Skill contract is controlling for this boundary: there is one top-level source-maintenance Skill with internal Orchestrator and Executor routes. R029-S3 does not create role-named top-level Skills and does not treat portability across ChatGPT/Codex as authority to split the domain.

## Domain inclusion test

A routed responsibility belongs to the Maintainer Skill/domain surface when correct execution depends materially on Agent Governance-specific product identity, accepted decisions, repository conventions, lifecycle/state vocabulary, source-maintenance stage ownership, product release/testing architecture, or canonical paths.

A semantic pattern may be evaluated as transverse only when its useful intent survives removal of Agent Governance-specific names, IDs, stage vocabulary, file layout, authority records, and repository lifecycle conventions. Even then, the Agent Governance adapter/policy remains in the Maintainer/domain surface.

## Domain responsibilities retained in the Maintainer Skill

| ID | Agent Governance domain responsibility | Why it remains domain-specific | S1/S2 coverage |
| --- | --- | --- | --- |
| MD-01 | Source-product identity/navigation and source-vs-consumer separation | Depends on this product's Core, consumer Skill, Maintainer Skill, checkpoints, tasks, tests/evals and prohibition on live consumer state in the source repository | S1-001..005; LR-01/LR-07 |
| MD-02 | D053/D068/D076 SDD and source-maintenance stage routing | Stage numbers, candidate publication boundary, Stage 5/6 ownership and late-artifact re-entry are accepted Agent Governance policy | S1-007..017, 026, 029, 045..048, 076..078; DR-01 |
| MD-03 | D052 semantic-oracle ownership and source testing/eval routing | `orchestrator-conformance`, mixed ownership and semantic-oracle authority are repository-specific governance semantics | S1-021, 022, 061..064, 075; DR-01/DR-05 |
| MD-04 | Task Contract, persisted handoff and acceptance lifecycle | Exact Task Contract authority, published-candidate relationship, completion states and reconstruction requirements are Agent Governance lifecycle semantics | S1-048..052; DR-02 |
| MD-05 | Agent Governance checkpoint adapter | Exact single-checkpoint path, frontier schema, refresh/closure rules and source-only checkpoint semantics are repository-specific | S1-053..056; DR-03 |
| MD-06 | Agent Governance research/decision adapter | `Rxxx`, independent Research-State/Decision-State, ledger, accepted normative promotion and supersession conventions are product-specific | S1-057..060; DR-03 |
| MD-07 | Repository-specific branch/release adapter | `main`/`develop` roles, release/hotfix conventions, protected-base freshness and product release flow are repository policy | S1-070..072; DR-04 |
| MD-08 | Source-product testing/evaluation and Skill supply-chain architecture | Graders, thresholds, fixtures, Skill discovery/supply-chain and source testing architecture are product-specific | S1-061..066, 073..075; DR-05/DR-06 |
| MD-09 | Local source-maintainer toolchain adapter | Git/uv/Ruff configuration and source-only tooling constraints are repository implementation policy, not generic Skill semantics | S1-034, 035, 065..067; DR-06 |
| MD-10 | Maintainer role-aware progressive routing | One top-level Maintainer Skill with internal Orchestrator/Executor routes is an approved source-product architecture constraint | S1-006, 024..032, 062..064; Maintainer contract |
| MD-11 | Source-product mutation/refactor/change discipline | Markdown ownership, D068 materialization, characterization/refactor semantics and smallest-Core-module change rules depend on product decisions and repository structure | S1-024..026, 036, 042..047, 068..069, 076..079; DR-01 |
| MD-12 | Agent Governance adapters for any future transverse capability | A generic capability cannot redefine current D052/D053/D054/D055/D058/D068/D076/D077 authority, paths, gates or lifecycle state | all candidate-trigger units below |

## Transverse-candidate seams

S3 separates reusable semantic intent from the Agent Governance adapter but does not decide whether any candidate becomes a Skill.

| Candidate seam | Reusable intent that may leave the domain | Agent Governance material that must stay domain-side | Later owner |
| --- | --- | --- | --- |
| `repository-change-control` | safe topic-branch/PR mutation, protected-target avoidance, collision/isolation preconditions | `main`/`develop` release semantics, D061/D062 freshness, D068 stage publication, L007 and exact repository policy | S4; workspace placement S9 |
| `upstream-version-revalidation` | compare relied-on version with current/higher relevant releases before consequential reliance | D077 dispositions, D063 qualification relation, project-specific pins and launch authority | S5 |
| `research-evidence-traceability` | persist consequential research, distinguish evidence from decision authority, refresh volatile evidence | `Rxxx`, ledger schema, Decision-State transitions, checkpoint frontier integration | S6 |
| `durable-work-checkpoint` | persist enough durable frontier state to resume work without private chat context | exact `docs/orchestrator/CHECKPOINT.md` schema, D027/D067 lifecycle and Agent Governance references | S7 |
| `executor-launch-handoff` | prepare bounded executor launch/session handoff and durable return evidence | D055 model/effort policy, Task Contract authority, D054/D058/D065 semantics, Stage 6 acceptance boundaries | S8 |
| workspace isolation | prevent concurrent writable workspace/branch collisions and preserve ambiguous work | D058 coordinator naming, Agent Governance branch/task identity and closure policy | S9 |

These seams are intentionally asymmetric: generic workflow intent may be reusable, while the authoritative Agent Governance policy adapter remains inside the Maintainer/domain context.

## Internal route boundary

The existing Maintainer Skill retains two internal routes:

```text
Maintainer Skill
  -> Orchestrator route
  -> Executor route
```

The split is by active repository role and stage, not by top-level Skill identity.

### Orchestrator route remains responsible for progressively disclosing

- Agent Governance strategy/research/Decision/Task Contract and checkpoint context;
- D053/D068 Explore–Plan and Stage 5 candidate materialization context;
- D052 semantic-oracle authoring context;
- source-product Markdown and acceptance/convergence context;
- source-specific adapters for transverse workflows when ChatGPT owns the semantic decision/gate.

### Executor route remains responsible for progressively disclosing

- exact authorized Task Contract and published candidate identity;
- Stage 6 execution/diagnosis/bounded repair/verification context;
- frozen semantic-oracle assets where applicable;
- local toolchain/test/eval and handoff mechanics;
- source-specific adapters for transverse workflows only within the Executor's authorized mechanics envelope.

A transverse capability never creates permission to cross from one internal route to the other. Role switching still requires explicit authority/context reload under the repository policy.

## What must not become a transverse Skill merely because it is reusable-looking

The following remain domain/reference material unless future evidence demonstrates a genuinely separate intent:

- generic `coding`, `testing`, `pytest`, `TDD`, `git commands`, `Markdown editing` or `branching` Skills;
- D053/D068 stage ownership as a portable generic workflow;
- D052 semantic-oracle ownership;
- Task Contract semantics and Agent Governance acceptance authority;
- source release/testing architecture;
- product-specific toolchain configuration;
- Orchestrator and Executor as separate top-level Skills.

These surfaces either lack a distinct user intent, are already internal capability areas, or would duplicate authority/routing rather than reduce context safely.

## Boundary invariants

1. The Maintainer Skill remains the sole project-owned top-level source-maintenance Skill unless a later explicit architecture decision changes that contract.
2. Internal Orchestrator/Executor routes remain context selectors, not governance roles or authority sources.
3. Agent Governance-specific accepted decisions and lifecycle vocabulary remain domain-side even when a generic workflow is later extracted.
4. A transverse Skill may supply workflow mechanics/structure but cannot own or supersede repository policy, Task Contracts, stage ownership, write ownership or acceptance.
5. Source maintenance and consumer governance remain separate activation domains.
6. Deterministic tests, CI and no-Skill bootstrap paths remain valid without Maintainer or transverse Skill activation.
7. S3 does not adopt any transverse candidate; it only makes their domain seams explicit for S4-S9.

## Coverage and completion

S3 consumes the S2 routed classes without leaving an orphaned destination:

- DR-01 through DR-06 are retained as Maintainer/domain/reference surfaces;
- DR-07 through DR-11 are candidate seams whose Agent Governance adapters remain inside MD-12 and whose generic portions are deferred to S4-S8/S9;
- the approved Maintainer Skill one-top-level/two-internal-route architecture is preserved;
- no root `AGENTS.md` wording or Skill implementation is changed;
- no individual candidate disposition is decided.

R029-S3 completion gate is satisfied analytically: source-maintenance-specific workflows are separated from transverse candidate seams without splitting the approved Maintainer Skill by role. Human review/acceptance is required before R029-S4 may be selected.