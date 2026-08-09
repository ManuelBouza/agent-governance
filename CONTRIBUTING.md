# Contributing

Contributions are welcome. This repository develops a public, agent-neutral governance framework and its operational Skills.

## Scope

Good contributions improve one or more of:
- Governance Core correctness, portability, clarity, or context efficiency;
- consumer Governance Skill behavior without expanding its authority;
- source-product Maintainer Skill behavior;
- deterministic tests of governance mechanics;
- agent-facing evals of governance/Skill behavior;
- adapters, templates, documentation, security, or release engineering.

Application-specific business requirements and tests of an agent's general coding ability are out of scope for this repository.

## Maintainer agent workflow

Repository maintainers use the two-role model defined in `AGENTS.md`:
- ChatGPT acts as Orchestrator and owns committed Markdown, strategy, contracts, handoffs, and review;
- an agent-product-neutral **Agente de IA Ejecutor** owns authorized non-Markdown implementation, tests/evals, fixtures, and their execution.

OpenCode, Codex, Claude Code, Antigravity, or another compatible coding agent may fulfill the executor role. No executor product has special governance authority.

Human external contributors are not required to use those tools. Contributions are evaluated by the resulting contract, architecture, tests/evals, security, branch policy, and review quality rather than by which tools produced the patch.

Coding agents working directly in this repository should follow `AGENTS.md` and any applicable repository-native adapter restrictions.

## Local development toolchain

D025 and `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md` define the canonical source-maintainer toolchain.

Baseline workstation requirements:
- Git;
- a compatible uv version as enforced by repository configuration once the executable harness is present;
- working GitHub authentication for the repository when push access is required.

The repository uses uv to provision/manage Python, `.venv`, development dependencies, and the lockfile. A globally installed Python is therefore not a mandatory prerequisite when uv can provision the required runtime.

The first executable test-harness task is responsible for materializing the approved non-Markdown configuration (`pyproject.toml`, `.python-version`, `uv.lock`, appropriate `.gitignore` entries, pytest/Ruff configuration). Until that task is integrated, the policy is authoritative even though those executable configuration files do not yet exist on `develop`.

After that configuration exists, the canonical local bootstrap/verification path is:

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

Ruff must be configured to exclude committed Markdown so executor tooling cannot modify ChatGPT-owned `.md` files.

GitHub CLI (`gh`) is recommended for authentication and diagnostics but is not required when Git over SSH/HTTPS is already configured correctly.

Do not install source-maintainer tools into consumer projects merely because this repository uses them; consumer repositories retain their native development toolchains unless their own governed task explicitly authorizes a change.

## Branching

Normal contributions follow `docs/BRANCHING.md`.

- `main` is stable/default and is not the normal contribution target.
- `develop` integrates the next unreleased state.
- create a short-lived topic branch from `develop` using `feat/`, `fix/`, `refactor/`, `test/`, `docs/`, or `chore/`.
- open the normal pull request back to `develop`.
- normal topic branches MUST NOT target `main`.

`release/*` and `hotfix/*` are exceptional paths defined in the branching policy.

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

## Skill boundaries

The consumer Governance Skill and source-product Maintainer Skill are distinct operational surfaces. Contributions must not merge their activation/context responsibilities into one broad Skill or make either Skill the sole carrier of protocol semantics or durable consumer state.

## Licensing

Unless explicitly stated otherwise, contributions intentionally submitted for inclusion in this repository are provided under the Apache License 2.0, consistent with Section 5 of that license.
