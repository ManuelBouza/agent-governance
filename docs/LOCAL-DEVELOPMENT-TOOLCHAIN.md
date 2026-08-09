# Local Development Toolchain

Status: ACTIVE

## Purpose

Define the concrete local development tools and canonical commands used to maintain the `agent-governance` source repository, while keeping those source-maintainer choices separate from toolchains used by consumer projects.

This document operationalizes D025. D023 remains authoritative for the Python testing framework, and D024 remains authoritative for the testing Skill/capability model.

## Tooling layers

### 1. Workstation-level required tools

Required for normal source-product executor work:

- Git
- uv compatible with the repository's declared `tool.uv.required-version`
- a configured GitHub write path for the canonical repository/topic branch through SSH or HTTPS
- a compatible Agente de IA Ejecutor host capable of invoking local tools

Python does not need to be installed globally if uv can provision the required version.

### 2. Repository-managed tools

Once the executable harness exists, the repository owns and locks its development dependencies through:

- `.python-version`
- `pyproject.toml`
- `uv.lock`
- local `.venv/`

Initial development dependencies:

- pytest `>=9,<10`
- Ruff `>=0.16,<0.17`

Hypothesis is added only by a later stateful/property-testing task.

### 3. Optional workstation helpers

Recommended but not acceptance requirements:

- GitHub CLI (`gh`) for authentication/repository diagnostics;
- editor/IDE integrations;
- fast local search tools supplied by the executor host or workstation.

No Task Contract may assume an optional helper exists unless that task explicitly promotes it to a required capability.

## Expected repository configuration

The first harness task is expected to establish non-Markdown repository files equivalent in intent to:

- `.python-version` requesting Python `3.13`;
- root `pyproject.toml` with:
  - Python compatibility consistent with D023;
  - `tool.uv.package = false` while this remains a non-package development harness;
  - `tool.uv.required-version` consistent with D025;
  - PEP 735 development dependency groups;
  - pytest configuration;
  - Ruff configuration;
  - explicit Ruff exclusion of committed Markdown;
- `uv.lock` committed to Git;
- `.gitignore` entries for `.venv/`, pytest/Ruff/Python caches, and other generated local state justified by the implemented tools.

The executor owns the exact non-Markdown configuration syntax and generated lock contents. ChatGPT reviews them against D023/D025 rather than prescribing generated transitive versions in Markdown.

## Fresh checkout bootstrap

After the initial harness/configuration has been integrated, the canonical environment bootstrap is:

```text
uv sync --locked
```

This must be sufficient to create/synchronize the project environment from repository-declared state on a supported workstation.

Do not require contributors to activate `.venv` manually before using canonical commands.

## Quality gate

Canonical local verification after the harness exists:

```text
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

A task may run a focused subset while iterating, but the final persisted handoff must run every command required by that Task Contract and include the complete-suite command where acceptance requires it.

### Mutation rule

During implementation, the executor may use explicitly authorized Ruff fix/format operations on executor-owned non-Markdown code.

It MUST NOT run a formatter configuration that can rewrite committed Markdown. Repository Ruff configuration must exclude `*.md`, and the executor remains responsible for checking the resulting diff before commit.

## Dependency-change procedure

Do not treat `.venv` as dependency state.

When a task authorizes a new Python development dependency:

1. update the declarative dependency group in `pyproject.toml` using uv or an equivalent deterministic edit;
2. update `uv.lock`;
3. synchronize the environment;
4. run the affected verification;
5. report the dependency/configuration delta in the executor handoff.

Do not satisfy a Task Contract by installing an undeclared package into `.venv` and leaving repository metadata unchanged.

## Python version policy locally

`.python-version` requests the minimum supported minor series (`3.13`) so ordinary source work continuously exercises the compatibility floor.

D023 still requires compatibility with the current latest stable supported Python feature series at release/CI gates once that matrix is implemented.

No source contract pins a particular `3.13.x` patch version. uv may resolve/install an appropriate current patch within the requested minor series.

## Network boundary

### Provisioning network

Allowed when needed for:
- installing/updating uv outside the repository;
- downloading a compatible Python runtime;
- resolving/downloading authorized dependencies;
- Git fetch/push operations.

### Test-runtime network

Not allowed for ordinary deterministic tests unless a later Task Contract explicitly defines an external/network behavior test.

A handoff should distinguish these two facts. For example, a fresh machine may require network during `uv sync`, while `uv run --locked python -m pytest` itself should exercise only local/synthetic state for T001.

## Git workflow support

The executor uses ordinary Git for the D022 workflow:

1. fetch current remote state;
2. start from the required `develop` revision;
3. create/switch to the Task Contract's topic branch;
4. implement and verify;
5. inspect `git status`/diff;
6. commit task artifacts;
7. push the branch;
8. return the pushed HEAD and persisted handoff path.

Stable machine-readable Git status (`git status --porcelain`) may be used in scripts/handoffs where appropriate.

GitHub CLI may assist authentication or repository operations but is not necessary when Git SSH/HTTPS credentials already work.

## Executor-host neutrality

OpenCode is one valid local executor host, but the repository toolchain is intentionally not `opencode`-dependent.

The same Task Contract should remain executable by another compatible agent host if it can:

- read/write the authorized files;
- invoke Git and uv;
- run the repository verification commands;
- obey D016 ownership restrictions;
- persist/commit/push the required handoff.

Product-specific agent installation/configuration remains outside `pyproject.toml`/`uv.lock` unless a future decision explicitly creates a product adapter artifact.

## Consumer repositories

Do not copy this source toolchain into consumer projects automatically.

When Agent Governance operates in another repository:

- inspect the existing project toolchain first;
- reuse its existing package/build/test/format/lint commands;
- preserve its existing lock/environment conventions;
- do not add Python/uv/Ruff/pytest just to run Governance unless a separately approved Governance executable actually requires them;
- Task Contracts should name the project's native verification commands rather than translating every project to the source-maintainer stack.

Examples:
- a Node project keeps its Node package/test tools;
- a Go project keeps Go modules and `go test`;
- a Python project already using another valid environment manager is not migrated to uv merely because `agent-governance` uses uv upstream.

The detailed rule for overlap with existing SDD systems and installed Agent Skills is separate and not defined by this document.

## Deferred tools

Do not add these to the baseline without a task/decision demonstrating need:

- Docker/container runtime;
- tox/nox;
- pre-commit;
- static type checker;
- coverage plugin;
- hosted eval/model SDK;
- security scanner;
- Make;
- jq;
- Node.js.

A future task can add any of them when its capability, supply-chain impact, portability, and overlap are reviewed explicitly.

## Security rules

- no credentials or private keys in repository files;
- no API/provider tokens in handoff JSON;
- prefer OS credential stores/SSH agents/environment injection for authentication;
- do not loosen executor permissions merely to simplify tool installation;
- dependency additions remain auditable through `pyproject.toml` + `uv.lock`;
- generated local environment directories remain disposable and unversioned.
