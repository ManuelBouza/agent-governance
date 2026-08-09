# T001 — Deterministic test harness foundation

Status: READY
Type: test/eval infrastructure
Base branch: `develop`
Expected topic branch: `test/governance-harness`
Expected executor handoff: `handoffs/T001-executor-handoff.json`
Owner for execution: Agente de IA Ejecutor
Specification owner/reviewer: ChatGPT Orchestrator

## Readiness status

All source-product foundation decisions required before this task are now resolved and persisted:
- programming language/testing stack: `docs/decisions/D023-python-testing-stack.md`;
- testing Skill/capability model: `docs/decisions/D024-testing-skill-capability-model.md` and `docs/TESTING-SKILL-CAPABILITIES.md`;
- local development toolchain: `docs/decisions/D025-local-development-toolchain.md` and `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`;
- ecosystem/SDD/Skill coexistence: `docs/decisions/D026-ecosystem-coexistence-and-capability-reuse.md` and `governance-core/COEXISTENCE.md`.

T001 does **not** require a released Maintainer Skill, any external testing/pytest/TDD Skill, or any SDD framework. The executor can bootstrap from repository contracts and approved tooling.

This Task Contract is `READY`. Execution starts only when the Human Owner/ChatGPT assigns this exact contract to an Agente de IA Ejecutor. Moving the contract to READY does not itself launch work.

## Objective

Establish the first small, executable, repository-owned deterministic testing foundation for Agent Governance and implement an initial useful set of mechanical tests derived from D019.

The result must provide a repeatable local command that verifies a focused subset of Governance product invariants without LLM judgment, production services, consumer business repositories, hosted evaluation dependencies, mandatory Agent Skill activation, or dependency on a particular SDD ecosystem.

## Controlling references

Read and follow:
- `AGENTS.md`
- `docs/BRANCHING.md`
- `docs/DEVELOPMENT-WORKFLOW.md`
- `docs/TASK-CONTRACTS.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `docs/TESTING-AND-EVALUATION.md`
- `docs/TESTING-SKILL-CAPABILITIES.md`
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`
- `docs/decisions/D010-governance-testing-scope.md`
- `docs/decisions/D016-binary-agent-role-model.md`
- `docs/decisions/D017-two-skill-architecture.md`
- `docs/decisions/D019-testing-and-evaluation-strategy.md`
- `docs/decisions/D021-persisted-executor-handoffs.md`
- `docs/decisions/D022-source-product-change-procedure.md`
- `docs/decisions/D023-python-testing-stack.md`
- `docs/decisions/D024-testing-skill-capability-model.md`
- `docs/decisions/D025-local-development-toolchain.md`
- `docs/decisions/D026-ecosystem-coexistence-and-capability-reuse.md`
- `governance-core/COEXISTENCE.md`
- `tests/README.md`
- `evals/README.md`

## Approved testing/capability/toolchain baseline

T001 uses:
- Git for branch/commit/push operations;
- uv compatible with D025 (`>=0.11.32,<0.12` at decision time);
- Python `>=3.13`, with the local minimum-runtime request represented as Python minor series `3.13`;
- pytest `>=9,<10`;
- Ruff `>=0.16,<0.17`;
- `python -m pytest` as the pytest framework invocation;
- Python standard library first for filesystem/JSON/subprocess/digest operations;
- pytest fixtures, `tmp_path`/`tmp_path_factory`, `pathlib.Path`, and parametrization where appropriate.

Do not add Hypothesis to T001 unless this Task Contract is deliberately revised to include genuine property/state-machine scope.

No Agent Skill is a T001 execution prerequisite. If the Maintainer Skill is available it may assist routing, but correctness and acceptance must be reconstructable from this contract, repository state, executable configuration, test code, and persisted evidence alone.

No SDD system is a T001 prerequisite. If Gentle-AI, Spec Kit, OpenSpec, another SDD system, a Skill registry, or equivalent tooling exists in the executor's environment, D026 applies: do not modify, replace, duplicate or make T001 depend on those capabilities unless this contract explicitly requires them. T001 remains a repository-native test-harness task.

## Workstation precondition

Before mutation the executor must verify that:
- Git is available;
- uv is available and compatible with the repository-required range;
- canonical-repository fetch/push authentication works for the authorized topic branch;
- the executor host can invoke local processes and write authorized non-Markdown files.

Do not install or alter global workstation tools inside T001 unless a later explicit contract revision authorizes that action. If the required workstation baseline is unavailable, persist `BLOCKED` rather than silently substituting a different environment manager.

Existing global/user-level Skills, SDD tooling, registries or agent configuration are outside T001 mutation scope. Their mere presence must not change the canonical test commands or dependencies.

## Checkout / branch precondition

1. clone/fetch the canonical repository as needed;
2. checkout current `develop` containing this READY Task Contract and D023-D026;
3. verify the working tree is clean;
4. create `test/governance-harness` from that current `develop` before modifying files.

Do not write directly to `main` or `develop`.

## Authorized scope

The executor may create or modify only the non-Markdown artifacts required for this increment, including:
- Python deterministic tests under `tests/`;
- non-Markdown synthetic fixtures under `tests/`;
- root `pyproject.toml` consistent with D023/D025;
- root `.python-version` requesting `3.13`;
- root `uv.lock` generated from the approved dependency metadata;
- root `.gitignore` entries required for `.venv`, Python/pytest/Ruff caches, and other generated local state actually introduced by this task;
- small reusable Python test helpers where they reduce duplication;
- `handoffs/T001-executor-handoff.json`.

The executor owns implementation, executable configuration, test execution, and persisted technical handoff under D016/D021/D022.

The executor is not authorized to initialize, update, or rewrite Gentle-AI/Spec Kit/OpenSpec/other SDD assets, third-party Skill registries, user-level agent configuration, or third-party managed instruction blocks as part of T001.

## Required configuration outcome

The T001 implementation must establish a root development configuration with these semantics:

1. the repository remains a non-package/virtual Python development harness unless evidence requires otherwise;
2. Python compatibility matches D023;
3. `tool.uv.required-version` enforces the D025 uv compatibility line;
4. the initial development dependencies include pytest and Ruff only;
5. pytest configuration is repository-owned in `pyproject.toml`;
6. Ruff configuration is repository-owned in `pyproject.toml`;
7. Ruff explicitly excludes committed `*.md` from formatter/linter operations used by executor workflows;
8. `.venv` and generated caches are not versioned;
9. `uv.lock` is committed and consistent with `pyproject.toml`.

Do not introduce a packaging/build backend merely to host the test configuration.

## Required first-increment test surface

Implement the smallest coherent deterministic baseline that provides meaningful protection for the current source tree.

Prioritize:

1. **Canonical source layout**
   - required product directories exist;
   - required Governance Core modules exist, including `COEXISTENCE.md` under protocol 1.9.0;
   - Consumer and Maintainer Skill source boundaries are distinguishable;
   - repository root contains no live consumer `.agent-coordination/` instance.

2. **Direct local reference integrity**
   - mechanically resolvable repository-internal references point to expected existing files/paths;
   - the Core/package references to `COEXISTENCE.md` resolve correctly;
   - deterministic code does not attempt to judge prose semantics.

3. **Source-product / consumer separation**
   - fixtures/tests distinguish source-product artifacts from installed consumer footprints;
   - no real consumer/business repository or state is required;
   - source tests do not require Gentle-AI, Spec Kit, OpenSpec, another SDD, external Skill registry, or live third-party project state.

4. **Harness foundation**
   - locked uv commands execute the suite/quality checks in the approved local environment;
   - tests require no production credential/service;
   - failures identify the violated invariant.

D026 defines substantial future coexistence test/eval coverage, but T001 must not inflate into all coexistence or all D019 layers. T001 only needs to establish the harness and mechanically protect the current canonical layout/reference boundaries relevant to this increment.

## Canonical final verification

After creating/updating the dependency metadata and lockfile, final verification must include:

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

During implementation the executor may run focused tests or authorized Ruff fixes against non-Markdown code, but the final quality gate uses non-mutating Ruff checks and the complete implemented pytest suite.

`uv lock` or equivalent uv dependency-resolution operations are expected when initially generating/updating `uv.lock`; the final handoff state must then pass locked commands without changing the lockfile.

## Network boundary

Provisioning network and test-runtime network are distinct:

- Git fetch/push and first-time uv/Python/dependency provisioning may use network as needed;
- deterministic test execution itself must not access production/external services or require network access;
- the handoff must report these two categories separately when network was used during setup.

## Explicit exclusions

Do NOT in T001:
- edit/create/delete committed `*.md` as the executor;
- use another primary language/test framework/environment manager without a persisted decision;
- require or install a generic testing/pytest/TDD Agent Skill;
- require the final Maintainer Skill to exist;
- require or initialize Gentle-AI, Spec Kit, OpenSpec, another SDD framework, or external Skill registry;
- overwrite third-party/user-managed agent instructions/configuration merely because they exist on the workstation;
- require GitHub CLI when ordinary Git authentication already satisfies the branch workflow;
- implement final Consumer or Maintainer `SKILL.md`;
- implement behavioral/model eval execution or trigger-rate measurement;
- add hosted eval frameworks;
- add OPA/Rego merely because OPA is a research reference;
- add Hypothesis unless the task is revised to genuine stateful/property scope;
- add static type checkers, coverage plugins, Docker, tox/nox, pre-commit, Make, jq, Node.js, or unrelated tooling without an explicit contract revision;
- add unrelated test libraries where stdlib/pytest suffices;
- access production services, credentials, or real consumer repositories;
- create a live `.agent-governance/` / `.agent-coordination/` instance at repository root;
- change branch/release policy;
- open or merge a PR before ChatGPT reviews the pushed implementation and persisted handoff.

## Invariants / constraints

- D023 controls language/framework.
- D024 controls the testing Skill/capability boundary.
- D025 controls local source-development tooling.
- D026 controls coexistence/non-overlap with existing SDD/Skills/tooling.
- Tests remain executable without Agent Skill or SDD activation.
- Source-maintainer uv/Python/Ruff choices do not become consumer-project requirements.
- Ruff/tooling cannot rewrite ChatGPT-owned Markdown.
- T001 cannot mutate or depend on unrelated third-party managed ecosystem surfaces.
- Mechanical properties are verified by code, not LLM graders.
- Tests validate Agent Governance, not generic coding ability.
- Test implementation cannot redefine Markdown contracts.
- No executor product receives special semantics.
- Keep dependencies minimal/local-first.
- Results must be deterministic for identical repository/environment inputs.
- The handoff is evidence, not acceptance authority.

## Acceptance criteria

ChatGPT may accept T001 only if:
1. execution started from this or a later explicitly READY Task Contract containing D023-D026;
2. work occurred on `test/governance-harness` from the correct current `develop`;
3. no committed Markdown was modified by the executor;
4. root non-Markdown environment/configuration artifacts satisfy D023/D025;
5. code uses Python `>=3.13` and pytest `>=9,<10` consistently;
6. Ruff `>=0.16,<0.17` is declared and configured to exclude Markdown;
7. `uv.lock` is committed/current and final verification runs with `--locked`;
8. no Agent Skill or SDD framework is required to make the suite run;
9. tests cover meaningful current Governance invariants including the required Core/reference presence for `COEXISTENCE.md`;
10. tests require no production service, credential, real business repository, or live third-party SDD installation;
11. the full canonical final verification path was actually executed and reported honestly;
12. no test was weakened merely to get green;
13. dependencies/configuration comply with D023/D025 and no D026 capability collision was introduced;
14. `handoffs/T001-executor-handoff.json` accurately describes the final pushed branch and verification evidence;
15. the executor committed and pushed the reviewable branch before returning status;
16. the visible response contains the required minimal pointer.

## Verification requirements

The executor must record:
- exact canonical and focused commands run;
- pass/fail/skip counts from pytest;
- Python, uv, pytest, and Ruff versions;
- whether provisioning required network;
- confirmation that deterministic test runtime itself required no network/external service;
- confirmation that no external SDD/Skill ecosystem was required or modified by T001;
- dependency/configuration files created/changed;
- `git status` summary before final commit and final pushed HEAD identity;
- all required evidence in `handoffs/T001-executor-handoff.json`.

Do not claim success from static inspection.

## Stop / escalation conditions

Stop and persist `BLOCKED`/`PARTIAL` instead of guessing if:
- repository contracts materially conflict;
- satisfying scope requires executor Markdown edits;
- current `develop` differs materially from approved assumptions;
- compatible Git/uv/workstation capabilities are unavailable;
- implementing D023/D025 would require an unapproved substitution or global tool change;
- the task would require a new mandatory Agent Skill contrary to D024;
- an installed SDD/Skill/tooling surface creates a material conflict under D026 that cannot be avoided without modifying that external surface;
- testable behavior requires a new architectural decision;
- implementation requires unauthorized production/external access;
- a dependency creates an unapproved supply-chain/security decision;
- the work changes public Governance semantics rather than merely testing them.

## Expected persisted handoff

Before returning, write/update exactly:

`handoffs/T001-executor-handoff.json`

Follow `docs/EXECUTOR-HANDOFFS.md` and include at minimum:
- `task_id`: `T001`;
- `status`: `DONE`, `BLOCKED`, or `PARTIAL`;
- `task_contract_path`;
- branch, pushed final HEAD, base branch and base SHA;
- files changed;
- implementation/tooling rationale;
- exact verification commands/results/counts;
- Python/uv/pytest/Ruff versions and any other actually used tool versions;
- dependencies/config changes;
- provisioning-network and test-runtime-network facts;
- coexistence fact: external SDD/Skill ecosystems required/modified (`false` expected for T001) or blocking conflict if any;
- `git_status` summary;
- unresolved issues/ambiguities;
- proposed next incremental task;
- `chatgpt_read_path`: `handoffs/T001-executor-handoff.json`.

## Visible executor response

After the handoff and final state are committed and pushed, return only:

`STATUS: DONE | BLOCKED | PARTIAL`

`HANDOFF: handoffs/T001-executor-handoff.json`

`BRANCH: test/governance-harness`

`HEAD: <pushed-final-commit-sha>`

Do not open or merge a PR unless the Task Contract explicitly delegates that action after ChatGPT review.
