# D025 — Local development toolchain

Status: ACCEPTED
Authority: Human Owner

## Decision

The canonical `agent-governance` source repository SHALL use a small, cross-platform, repository-declared local development toolchain that is independent of the concrete Agente de IA Ejecutor product.

The source-maintenance baseline is:

- **Git** for repository history, branching, commit, and push operations;
- **uv 0.11.x**, with repository enforcement of `>=0.11.32,<0.12`, as the canonical Python/version/environment/dependency/lock runner for source-product test/eval development;
- **Python >=3.13**, requested at minor-series level with `.python-version` using `3.13` for the minimum-runtime local baseline;
- **pytest >=9,<10** as defined by D023;
- **Ruff >=0.16,<0.17** as the canonical Python lint/format CLI for repository-owned Python code;
- a committed root `pyproject.toml` and `uv.lock` once the executable harness is implemented;
- a disposable project-local `.venv` managed by uv and excluded from version control.

The repository SHALL NOT require a specific coding-agent product, Unix shell, Docker runtime, Node.js runtime, Make, jq, tox, nox, Poetry, or a globally installed Python interpreter for the baseline deterministic harness.

## Executor-host boundary

OpenCode, Codex, Claude Code, Antigravity, or another compatible coding agent is an **executor host**, not part of the canonical repository dependency graph.

A compatible executor host must be able to:
- read the repository and Task Contract;
- invoke local processes;
- use Git on the authorized topic branch;
- invoke the repository-declared development commands;
- persist/commit/push non-Markdown work and handoff evidence according to D016/D021/D022.

The repository must not encode correctness around one executor CLI or require that another contributor install that same agent product.

## Why uv

uv is selected because one cross-platform CLI can:
- install/manage the required Python series when a suitable interpreter is absent;
- create/manage the project `.venv`;
- consume standardized PEP 735 development dependency groups;
- create and use a lockfile;
- synchronize a fresh checkout reproducibly;
- run commands inside the synchronized project environment.

This removes the need for a separate pyenv + venv + pip/pip-tools/Poetry stack for this repository while still storing dependency intent in standard `pyproject.toml` structures where practical.

The source repository uses uv as a development-environment manager, not as Governance Core authority and not as a consumer-project requirement.

## Source repository project shape

The first executable test-harness implementation SHALL establish repository-root non-Markdown configuration consistent with this decision.

Expected direction:

- `.python-version`
  - contains `3.13`, not a single patch version;
- `pyproject.toml`
  - declares Python compatibility consistent with D023;
  - treats this repository as a non-package/virtual development project unless a later product implementation genuinely requires packaging;
  - declares development dependencies with PEP 735 `[dependency-groups]`;
  - declares pytest configuration;
  - declares Ruff configuration;
  - enforces the approved uv compatibility line through `tool.uv.required-version`;
- `uv.lock`
  - is committed;
  - provides concrete reproducible dependency resolution;
- `.venv/`
  - is local/disposable and MUST NOT be committed.

The exact generated TOML/lock syntax is executor-owned non-Markdown implementation, but it must satisfy the contract above.

## Dependency groups

For the first deterministic harness, the default development group SHALL contain only the dependencies justified by the active task, initially:

- pytest `>=9,<10`;
- Ruff `>=0.16,<0.17`.

Hypothesis remains approved by D023 but is not a T001 dependency. When a later Layer-2 task actually requires Hypothesis, it SHOULD be introduced in an explicit stateful/property-testing dependency group or another clearly named task-specific development group rather than silently broadening every baseline environment.

Likewise, future model SDKs, security scanners, coverage tools, type checkers, or eval frameworks require task-specific approval rather than automatic inclusion in the default toolchain.

## Canonical local commands

Once `pyproject.toml` and `uv.lock` exist, a normal fresh checkout uses a locked environment:

```text
uv sync --locked
```

The canonical source-code quality/test verification path is:

```text
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

`python -m pytest` remains the framework-level invocation contract from D023; `uv run --locked` is the source-repository environment wrapper that ensures the command executes against the declared locked environment.

Dependency changes MUST update the declarative dependency metadata and `uv.lock`. Do not make reproducibility depend on ad-hoc packages installed manually into `.venv`.

## Markdown ownership protection

Ruff 0.16 can process Python code blocks in Markdown. That behavior would be incompatible with D016 if an executor could format committed Markdown.

Therefore the repository Ruff configuration MUST explicitly exclude committed `*.md` files from formatter/linter mutation/discovery used by executor workflows. The normal executor quality gate may inspect Python/non-Markdown code but MUST NOT rewrite Markdown through Ruff or another formatter.

A tool capable of touching Markdown does not gain authority to do so merely because it is part of the toolchain.

## Git and remote authentication

Git is mandatory for the source workflow because D022 requires a remotely auditable pushed topic branch before ChatGPT review.

The repository does not mandate one GitHub authentication transport. HTTPS or SSH is acceptable when configured securely and capable of the authorized push operations.

**GitHub CLI (`gh`) is RECOMMENDED but not REQUIRED** on maintainer workstations because it can assist GitHub authentication, repository cloning, and diagnostics. A contributor or executor using working Git SSH/HTTPS credentials does not need `gh` merely to satisfy the test harness or branch handoff contract.

Credentials, tokens, SSH private keys, credential-store data, and agent-provider secrets MUST NOT be stored in this repository or in committed handoff artifacts.

## Provisioning vs test-runtime network access

Environment provisioning and test execution are different security surfaces.

- Initial `uv` setup may require network access to obtain uv/Python/dependencies when they are not already available locally.
- Lock/dependency updates may require package-index access.
- After the declared environment is synchronized, deterministic tests MUST NOT require external network/service access unless a later Task Contract explicitly defines such a test surface.

Executor handoffs SHOULD distinguish provisioning network use from network use during the actual verification command.

## Tools intentionally not required initially

The baseline does not require:

- **Docker/containers** — introduce only for a later isolation/adversarial task when justified;
- **pre-commit** — local hooks may be evaluated later, but release correctness must come from explicit reproducible commands/CI rather than a hook that can be skipped;
- **tox/nox** — unnecessary while the suite has one simple local environment; multi-environment orchestration can be reconsidered when CI/runtime matrices justify it;
- **mypy/Pyright/ty** — static typing tools are not yet justified by the small test-harness code surface;
- **Make** — canonical commands must be directly invokable on Windows, macOS, and Linux without assuming GNU Make;
- **jq** — Python already provides repository-owned JSON processing and jq is not a correctness dependency;
- **Node.js** — not required by the Python test/eval harness;
- **a specific shell** — repository commands must avoid depending on Bash-only behavior for their canonical semantics.

This is a minimum policy, not a prohibition on optional local convenience tools.

## Consumer-project toolchain policy

The source-maintenance toolchain above MUST NOT be imposed automatically on repositories that adopt Agent Governance.

For a consumer repository:

1. Governance first discovers the project's existing language/build/test/package/tooling conventions.
2. Existing project-native tools are reused when they satisfy the required capability.
3. Agent Governance MUST NOT add `uv`, Python, Ruff, pytest, `.venv`, `pyproject.toml`, or another source-maintainer tool merely because the canonical Governance repository uses them.
4. A new consumer-project tool may be introduced only when the governed task requires a missing capability and the applicable Task Contract/governance decision authorizes that addition.
5. Consumer-project test commands and implementation tools remain properties of that project, not global Agent Governance defaults.
6. Any executable tooling shipped as part of Agent Governance itself must declare its own runtime/permissions independently and must not silently convert the consumer repository to the source repository's development stack.

This reuse-first rule applies to toolchains generally. Detailed coexistence/precedence rules for pre-existing SDD systems and Agent Skills are intentionally deferred to the separate coexistence decision.

## Cross-platform requirement

The baseline source development workflow must be usable on Windows, macOS, and Linux using equivalent Git/uv commands.

Repository correctness MUST NOT depend on:
- activating `.venv` manually;
- POSIX-only path semantics;
- Bash-specific scripts;
- globally mutable Python site-packages.

`uv run` is preferred for canonical invocations so activation syntax differences do not become part of the task contract.

## Research basis

### uv installation and Python management

https://docs.astral.sh/uv/getting-started/installation/

Relevant points:
- official standalone installation supports macOS/Linux and Windows;
- current documentation supports installing a specific uv release;
- uv is available as a standalone binary without requiring a pre-existing Python installation.

https://docs.astral.sh/uv/guides/install-python/

Relevant points:
- uv can discover an existing Python installation or install/manage Python itself;
- missing compatible Python versions can be downloaded automatically.

### uv projects, locks and dependency groups

https://docs.astral.sh/uv/concepts/projects/dependencies/

Relevant points:
- development dependencies use standardized PEP 735 dependency groups;
- dependency groups can be selected independently;
- the `dev` group is included by default by normal project commands.

https://docs.astral.sh/uv/concepts/projects/sync/

Relevant points:
- `uv sync` creates/updates the project environment;
- `--locked` requires the lockfile to be current;
- locked dependency versions are preferred and reproducible across subsequent syncs.

https://docs.astral.sh/uv/concepts/projects/layout/

Relevant points:
- `.venv` is a disposable project environment and should not be versioned;
- `uv run` executes commands in the managed project environment.

https://docs.astral.sh/uv/reference/settings/

Relevant points:
- `tool.uv.required-version` can reject an unsupported uv version;
- `tool.uv.package = false` supports non-package/virtual projects.

### Ruff

https://docs.astral.sh/ruff/linter/
https://docs.astral.sh/ruff/formatter/
https://docs.astral.sh/ruff/configuration/

Relevant points:
- one CLI provides linting and formatting;
- configuration lives in `pyproject.toml` or Ruff-specific TOML;
- `ruff check` and `ruff format --check` provide non-mutating verification modes;
- Ruff 0.16 can format Python blocks in Markdown, motivating the explicit Markdown exclusion required by D016.

### Git / GitHub authentication

https://git-scm.com/docs/git-switch
https://git-scm.com/docs/git-push

Relevant points:
- Git provides explicit topic-branch creation/switching and remote push primitives required by D022.

https://cli.github.com/manual/gh_auth_login
https://cli.github.com/manual/gh_repo_clone

Relevant points:
- `gh` can authenticate GitHub access and clone repositories, but those capabilities are helpers around Git/GitHub rather than prerequisites of the Python test harness.

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/about-ssh

Relevant point:
- GitHub supports authenticated repository read/write over SSH using local keys.

## Consequences

- D023's previously deferred environment-manager/lock decision is resolved by uv + committed `uv.lock`.
- T001 may require the executor to create the initial `pyproject.toml`, `.python-version`, `uv.lock`, `.gitignore` entries, pytest configuration, and Ruff configuration consistent with D023/D025.
- Ruff becomes an approved T001 development dependency because it enforces the quality boundary for newly introduced Python code; Hypothesis remains excluded from T001.
- T001's local-toolchain blocker is resolved by this decision; it remains BLOCKED only on the pre-existing SDD/Skill coexistence decision.
- normal consumer repositories inherit/reuse their own toolchains and do not inherit uv/Python/Ruff/pytest merely by installing Agent Governance.
