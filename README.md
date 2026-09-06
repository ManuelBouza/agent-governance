# Agent Governance

Portable, agent-neutral governance framework for deterministic collaboration between a Human Owner, a Strategy/Governance Agent, and an Implementation Agent.

This repository is the **public source product and testbed** for the governance framework. It is intended to be reusable by external projects and contributors, not only by its original author. It is not itself a governed project instance and must not be interpreted as an installed `.agent-governance/` / `.agent-coordination/` footprint.

## Repository boundary

Only the governance product lives here:
- canonical governance instructions and protocol structure;
- consumer Governance Skill and source-product Maintainer Skill;
- supporting implementation/tooling;
- source-product operating instructions and architectural decisions;
- deterministic tests and agent-facing governance/Skill evals;
- minimal synthetic fixtures required to test those artifacts.

Real application implementation, consumer missions/tasks, consumer STATE/EXCHANGE history, production configuration, and project-specific governance instances live in separate repositories.

## Product layout

```text
governance-core/     Canonical reusable governance protocol modules
governance-skill/    Consumer-facing Governance Skill (under development)
maintainer-skill/    Source-product Maintainer Skill (under development)
docs/                Product design, decisions, development and release rules
tests/               Deterministic framework/Skill tests
evals/               Agent-facing Governance/Skill evaluations
```

The Governance Core includes a focused `COEXISTENCE.md` module so adopting repositories can reuse existing SDD, Skills, testing, memory, permissions and workflow capabilities instead of receiving duplicate toolchains/methodologies.

## Two Skill surfaces

Agent Governance deliberately separates two coherent operational Skills:

- **Maintainer Skill** — used only to develop, refactor, test/evaluate, and release this canonical source product.
- **Consumer Governance Skill** — used inside adopting repositories to install, bootstrap, validate, operate, recover, hand off, audit, archive, and coexist safely with existing project capabilities.

The consumer Skill MUST operate without requiring read/write access to this canonical source repository after installation. Consumers should use immutable release/tag/commit artifacts rather than depend on a floating source branch.

It is not a replacement SDD methodology: existing compatible systems such as Gentle-AI, Spec Kit, OpenSpec or project-specific workflows are detected and reused/adapted under capability-first coexistence rules; repositories with no SDD remain supported without installing one.

See `docs/decisions/D017-two-skill-architecture.md`, `docs/decisions/D026-ecosystem-coexistence-and-capability-reuse.md`, and `docs/MAINTAINER-SKILL-CONTRACT.md`.

## Source-repository agent operation

Development uses two agent roles plus the Human Owner:

- **ChatGPT Orchestrator** — strategy, research synthesis, architecture/specification, work contracts, handoffs, review, source-maintenance checkpoints, all committed Markdown (`*.md`), and, for D068-mode source maintenance, complete Stage 5 candidate materialization.
- **Agente de IA Ejecutor** — product-agnostic technical executor; OpenCode, Codex, Claude Code, Antigravity, or another compatible coding agent may fill the role. For D068-mode source maintenance it owns Stage 6 execution, diagnosis, bounded technical repair, and verification of the published candidate.
- **Human Owner** — final authority.

No named executor product has special governance status. D052 semantic-oracle ownership and D054 execution-mechanics ownership remain intact under D068, and D068 does not change Governance Core or consumer-project SDD semantics.

For D068-mode source maintenance, ChatGPT publishes the complete coherent candidate and controlling authority on the verified topic branch before Executor verification. That published topic-branch checkpoint is sufficient verification authority; a separate planning/candidate merge to `develop` is not required first. Historical and grandfathered work retains its original persisted authority.

ChatGPT source-maintenance sessions are designed to survive conversation turnover. The current orchestration frontier is persisted in `docs/orchestrator/CHECKPOINT.md`; a new ChatGPT chat can resume from current `develop` by loading `AGENTS.md`, that checkpoint, and only the minimum controlling files it references. Prior chat history is not required.

See `AGENTS.md`, `docs/DEVELOPMENT-WORKFLOW.md`, `docs/ORCHESTRATOR-CHECKPOINTS.md`, `docs/REFACTORING-WORKFLOW.md`, and `docs/decisions/D068-library-first-candidate-materialization-executor-verification-boundary.md`.

## Branch and release model

- `main` — primary/default stable branch; latest accepted potentially releasable state.
- `develop` — integration branch for the next unreleased state.
- normal work — short-lived topic branches from `develop`, merged back by PR.
- normal direct writes to `main` or `develop` are prohibited.
- published releases/tags originate from `main` only.

See `docs/BRANCHING.md` and `docs/RELEASES.md`.

## Public distribution

The project is deliberately public so compatible agent users, teams, and tool vendors can inspect, test, adopt, adapt, and contribute to the framework.

Agent Governance is licensed under **Apache-2.0**. See `LICENSE`.

Public visibility does not weaken the framework's Skill supply-chain rules: third-party Skills, contributions, releases, and installed artifacts remain subject to provenance, review, exact-version verification, and applicable governance controls.

Project policies:
- `CONTRIBUTING.md` — contribution scope and pull-request expectations;
- `SECURITY.md` — security-relevant defect scope and reporting guidance;
- `docs/BRANCHING.md` — stable/integration/topic branch policy;
- `docs/RELEASES.md` — stability model and stable-release gate.

## Current status

Protocol source version: **1.9.0**.

The live source-maintenance frontier is intentionally not duplicated in this README. `docs/orchestrator/CHECKPOINT.md` is the canonical current-state router for active/accepted work, controlling references, and the next permitted Orchestrator action. D068 is the accepted prospective Stage 5/6 boundary for source-maintenance objectives operating in that mode.

Consumers should pin an immutable release or commit. `develop` is explicitly unreleased integration state; `main` is stable but a release/tag remains the preferred dependency identity once releases exist.

## Historical origin

The framework was initially designed inside `ManuelBouza/script-uh` as a testbed. Product development has now been separated into this dedicated repository so application concerns cannot contaminate governance design or testing.
