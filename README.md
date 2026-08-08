# Agent Governance

Portable, agent-neutral governance framework for deterministic collaboration between a Human Owner, a Strategy/Governance Agent, and an Implementation Agent.

This repository is the **source product and testbed** for the governance framework. It is not a governed project instance and must not be interpreted as an installed `.agent-governance/` / `.agent-coordination/` footprint.

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

## Current status

Protocol source version: **1.8.0**.

The Core architecture and Governance Skill functional/package design are established. The executable Governance Skill and its focused test/eval harness are the next product-development phase.

## Historical origin

The framework was initially designed inside `ManuelBouza/script-uh` as a testbed. Product development has now been separated into this dedicated repository so application concerns cannot contaminate governance design or testing.
