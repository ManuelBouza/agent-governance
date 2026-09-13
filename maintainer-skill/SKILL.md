---
name: source-maintainer
description: Maintain the canonical Agent Governance source product: research/decision/Task Contract/checkpoint work, D068 candidate materialization, source testing/evaluation, Executor verification handoff, refactoring, release readiness, and source-repository convergence. Do not use for ordinary consumer-project governance or unrelated generic coding/testing/Git work.
---

# Agent Governance Source Maintainer

Use this Skill only for maintenance of the canonical `agent-governance` source product. Repository authority remains in `AGENTS.md`, accepted Decisions, Task Contracts, branches, handoffs, and other canonical Git records; this Skill only selects the smallest source-maintenance context.

## Activation boundary

Activate for source-product work such as:

- changing Governance Core, product instructions, architecture, Decisions, Task Contracts, checkpoints, source Skills, tests/evals, release or migration artifacts;
- D068 Stage 5 complete candidate materialization;
- D068 Stage 6 execution/diagnosis/bounded repair/verification against a published candidate;
- source refactoring, conformance/oracle maintenance, source-toolchain verification, or distribution readiness.

Do not activate merely because another repository uses Agent Governance. Consumer mission/state/lifecycle work belongs to the Consumer Governance Skill. Do not activate for unrelated generic coding, testing, Git syntax, package updates, or ordinary project planning.

## Authority and role routing

One top-level Maintainer Skill has exactly two internal context routes:

```text
source-maintainer
  -> Orchestrator route
  -> Executor route
```

The active repository role/stage selects the route. Routes do not create roles or authority and must not be blended in a way that changes ownership.

### Orchestrator route

Load `references/orchestrator-route.md` when ChatGPT owns strategy/research/decision/specification/Design/Plan, Markdown, semantic oracles, Task Contract/checkpoint work, D068 Stage 5 candidate materialization, Stage 7 acceptance/integration, or source release/convergence.

When creating, materially revising, readiness-reviewing, or launching an executable Task Contract, also load:

- `references/TASK-CONTRACT-TEMPLATE-USAGE.md`
- `references/TASK-CONTRACT-V4-TEMPLATE.md`

### Executor route

Load `references/executor-route.md` only for an authorized Executor operating from persisted Task Contract/published-candidate authority during D068 Stage 6 or explicit historical authority.

## Transverse composition

Compose only the minimum required transverse capability:

- tracked mutation/change-path control -> `repository-change-control`;
- consequential external version behavior -> `upstream-version-revalidation`;
- consequential evidence provenance/freshness -> `research-evidence-traceability`;
- resumable work frontier -> `durable-work-checkpoint`;
- delegated executor/session launch or durable return -> `executor-launch-handoff`.

Workspace isolation is subordinate to `executor-launch-handoff`; repository mutation semantics remain controlled by repository policy / `repository-change-control`.

A transverse Skill can structure workflow but cannot override Agent Governance stage ownership, write ownership, Task Contract/checkpoint/handoff semantics, branch/release/testing policy, or acceptance.

## Progressive disclosure

Start from `AGENTS.md` plus the current frontier/Task Contract. Load only the applicable route, controlling Decisions/policy, and exact source surfaces needed for the current stage. Prefer references to standing repository policy rather than copying it into Skill-local prose.

Deterministic tests, CI, source tooling, and cold-start bootstrap remain valid when this Skill is absent or disabled.
