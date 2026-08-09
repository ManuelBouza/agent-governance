# Contributing

Contributions are welcome. This repository develops a public, agent-neutral governance framework and its operational Governance Skill.

## Scope

Good contributions improve one or more of:
- Governance Core correctness, portability, clarity, or context efficiency;
- Governance Skill behavior without expanding its authority;
- deterministic tests of governance mechanics;
- agent-facing evals of governance/Skill behavior;
- adapters, templates, documentation, security, or release engineering.

Application-specific business requirements and tests of an agent's general coding ability are out of scope for this repository.

## Maintainer agent workflow

The repository maintainers use the role-separated workflow defined in `AGENTS.md`, `docs/DEVELOPMENT-WORKFLOW.md`, and `docs/REFACTORING-WORKFLOW.md`: ChatGPT orchestrates and owns committed Markdown, an Implementation Executor handles implementation artifacts, and Codex owns tests/evals and their execution.

This is the project's internal agentic maintenance model. Human external contributors are not required to use those specific products. Contributions are evaluated by the resulting contract, architecture, tests/evals, security, and review quality rather than by which tools produced the patch.

Coding agents working directly in this repository should follow `AGENTS.md` and any applicable repository-native adapter restrictions.

## Before changing normative behavior

Changes that alter authority, lifecycle gates, execution states, disclosure semantics, Skill trust, persistence, or other protocol behavior should:
1. explain the problem being solved;
2. identify compatibility impact;
3. update or add a Decision Record when future maintainers need the rationale;
4. update the relevant Core module rather than duplicating the rule elsewhere;
5. add deterministic tests and/or focused eval cases as appropriate.

## Pull requests

Keep pull requests focused and independently reviewable. Include:
- what changed and why;
- affected protocol/Skill behavior;
- compatibility or migration impact;
- tests/evals performed;
- any security or supply-chain implications.

Behavior-preserving refactors should be separated from intentional behavior changes where practical and should demonstrate a pre-change characterization baseline when relevant coverage was missing.

Do not include secrets, credentials, proprietary consumer-project data, or copied project-specific mission/task state.

## Governance Skill

The Governance Skill is an operational layer, not an authority source. Contributions must not make the Skill the sole carrier of protocol semantics or durable project state.

## Licensing

Unless explicitly stated otherwise, contributions intentionally submitted for inclusion in this repository are provided under the Apache License 2.0, consistent with Section 5 of that license.
