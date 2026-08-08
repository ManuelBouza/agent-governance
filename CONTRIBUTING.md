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

Do not include secrets, credentials, proprietary consumer-project data, or copied project-specific mission/task state.

## Governance Skill

The Governance Skill is an operational layer, not an authority source. Contributions must not make the Skill the sole carrier of protocol semantics or durable project state.

## Licensing

Unless explicitly stated otherwise, contributions intentionally submitted for inclusion in this repository are provided under the Apache License 2.0, consistent with Section 5 of that license.
