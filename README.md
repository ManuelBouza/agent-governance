# Agent Governance

Portable, agent-neutral governance framework for deterministic collaboration between a Human Owner, a Strategy/Governance Agent, and an Implementation Agent.

This repository is the **public source product and testbed** for the governance framework. It is intended to be reusable by external projects and contributors, not only by its original author. It is not itself a governed project instance and must not be interpreted as an installed `.agent-governance/` / `.agent-coordination/` footprint.

## Product layout

```text
governance-core/     Canonical reusable governance protocol modules
governance-skill/    Reusable operational Agent Skill (under development)
docs/                Product design, decisions, and development records
tests/               Deterministic framework/Skill tests
evals/               Agent-facing Skill/governance evaluations
```

## Separation of concerns

- `governance-core/` is the normative, vendor-independent source of truth.
- `governance-skill/` is an operational/distribution layer and MUST NOT become authority.
- `tests/` and `evals/` validate the governance product itself, not application-task implementation quality.
- A consumer project receives an installed footprint derived from this repository; consumer mission/task state never belongs in this source repository.

## Public distribution

The project is deliberately public so compatible agent users, teams, and tool vendors can inspect, test, adopt, adapt, and contribute to the framework.

Agent Governance is licensed under **Apache-2.0**. See `LICENSE`.

Public visibility does not weaken the framework's Skill supply-chain rules: third-party Skills, contributions, releases, and installed artifacts remain subject to provenance, review, exact-version verification, and the applicable governance controls.

Project policies:
- `CONTRIBUTING.md` — contribution scope and pull-request expectations;
- `SECURITY.md` — security-relevant defect scope and reporting guidance;
- `docs/RELEASES.md` — stability model and stable-release gate.

## Current status

Protocol source version: **1.8.0**.

The Core architecture and Governance Skill functional/package design are established. The executable Governance Skill and its focused test/eval harness are the next product-development phase.

`main` is development state. Consumers should pin an immutable release or commit rather than treating the floating branch as an approved dependency.

## Historical origin

The framework was initially designed inside `ManuelBouza/script-uh` as a testbed. Product development has now been separated into this dedicated repository so application concerns cannot contaminate governance design or testing.
