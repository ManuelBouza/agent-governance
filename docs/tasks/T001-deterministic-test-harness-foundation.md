# T001 — Deterministic test harness foundation

Status: BLOCKED
Type: test/eval infrastructure
Base branch: `develop`
Expected topic branch: `test/governance-harness`
Expected executor handoff: `handoffs/T001-executor-handoff.json`
Owner for execution: Agente de IA Ejecutor
Specification owner/reviewer: ChatGPT Orchestrator

## Readiness block

Do NOT launch this task yet.

Resolved foundation decisions:
- programming language/testing stack: `docs/decisions/D023-python-testing-stack.md`;
- testing Skill/capability model: `docs/decisions/D024-testing-skill-capability-model.md` and `docs/TESTING-SKILL-CAPABILITIES.md`.

T001 does **not** require a released Maintainer Skill or any external testing/pytest/TDD Skill. The executor can bootstrap from repository contracts and approved tooling.

T001 remains blocked until ChatGPT/Human Owner resolve and persist:
1. the local CLI/development toolchain required to support the Agente de IA Ejecutor;
2. the coexistence/non-overlap policy for pre-existing SDD systems, Skills, and equivalent project capabilities.

After those decisions are integrated into `develop`, ChatGPT must reconcile this contract with them and explicitly change T001 to `READY` before execution.

## Objective

Establish the first small, executable, repository-owned deterministic testing foundation for Agent Governance and implement an initial useful set of mechanical tests derived from D019.

The result must provide a repeatable local command that verifies a focused subset of Governance product invariants without LLM judgment, production services, consumer business repositories, hosted evaluation dependencies, or mandatory Agent Skill activation.

## Controlling references

Read and follow:
- `AGENTS.md`
- `docs/BRANCHING.md`
- `docs/DEVELOPMENT-WORKFLOW.md`
- `docs/TASK-CONTRACTS.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `docs/TESTING-AND-EVALUATION.md`
- `docs/TESTING-SKILL-CAPABILITIES.md`
- `docs/decisions/D010-governance-testing-scope.md`
- `docs/decisions/D016-binary-agent-role-model.md`
- `docs/decisions/D017-two-skill-architecture.md`
- `docs/decisions/D019-testing-and-evaluation-strategy.md`
- `docs/decisions/D021-persisted-executor-handoffs.md`
- `docs/decisions/D022-source-product-change-procedure.md`
- `docs/decisions/D023-python-testing-stack.md`
- `docs/decisions/D024-testing-skill-capability-model.md`
- `tests/README.md`
- `evals/README.md`

The later toolchain and coexistence decisions become controlling references before T001 is moved to READY.

## Approved testing/capability baseline

Subject to the later local-toolchain decision, T001 uses:
- Python `>=3.13`;
- pytest `>=9,<10`;
- `python -m pytest` as the canonical framework-level invocation;
- Python standard library first for filesystem/JSON/subprocess/digest operations;
- pytest fixtures, `tmp_path`/`tmp_path_factory`, `pathlib.Path`, and parametrization where appropriate.

Do not add Hypothesis to T001 unless this Task Contract is deliberately revised to include genuine property/state-machine scope.

No Agent Skill is a T001 execution prerequisite. If the Maintainer Skill is available it may assist routing, but correctness and acceptance must be reconstructable from this contract, repository state, test code, and persisted evidence alone.

## Checkout / branch precondition

When and only when status becomes `READY`:
1. clone/fetch the canonical repository as needed;
2. checkout current `develop` containing the final READY contract and all readiness decisions;
3. verify the working tree is clean;
4. create `test/governance-harness` from that current `develop` before modifying files.

Do not write directly to `main` or `develop`.

## Authorized scope

Once READY, the executor may create or modify non-Markdown artifacts required for this first increment, including:
- Python deterministic tests under `tests/`;
- non-Markdown synthetic fixtures under `tests/`;
- minimal test/dependency/configuration files allowed by D023 and the later toolchain decision;
- small reusable Python test helpers where they reduce duplication;
- approved lock/dependency metadata;
- `handoffs/T001-executor-handoff.json`.

The executor owns implementation, test execution, and persisted technical handoff under D016/D021/D022.

## Required first-increment test surface

Implement the smallest coherent deterministic baseline that provides meaningful protection for the current source tree.

Prioritize:

1. **Canonical source layout**
   - required product directories exist;
   - required Governance Core modules exist;
   - Consumer and Maintainer Skill source boundaries are distinguishable;
   - repository root contains no live consumer `.agent-coordination/` instance.

2. **Direct local reference integrity**
   - mechanically resolvable repository-internal references point to expected existing files/paths;
   - deterministic code does not attempt to judge prose semantics.

3. **Source-product / consumer separation**
   - fixtures/tests distinguish source-product artifacts from installed consumer footprints;
   - no real consumer/business repository or state is required.

4. **Harness foundation**
   - `python -m pytest` executes the suite in the approved local environment;
   - tests require no production credential/service;
   - failures identify the violated invariant.

Do not inflate T001 into all D019 layers.

## Explicit exclusions

Do NOT in T001:
- execute while status is `BLOCKED`;
- edit/create/delete committed `*.md` as the executor;
- use another primary language/test framework without a persisted decision;
- require or install a generic testing/pytest/TDD Agent Skill;
- require the final Maintainer Skill to exist;
- implement final Consumer or Maintainer `SKILL.md`;
- implement behavioral/model eval execution or trigger-rate measurement;
- add hosted eval frameworks;
- add OPA/Rego merely because OPA is a research reference;
- add Hypothesis unless the task is revised to genuine stateful/property scope;
- add unrelated test libraries where stdlib/pytest suffices;
- access production/external services, credentials, or real consumer repositories;
- create a live `.agent-governance/` / `.agent-coordination/` instance at repository root;
- change branch/release policy;
- open or merge a PR before ChatGPT reviews the pushed implementation and persisted handoff.

## Invariants / constraints

- D023 controls language/framework.
- D024 controls the testing Skill/capability boundary.
- Tests must remain executable without Agent Skill activation.
- Mechanical properties are verified by code, not LLM graders.
- Tests validate Agent Governance, not generic coding ability.
- Test implementation cannot redefine Markdown contracts.
- No executor product receives special semantics.
- Keep dependencies minimal/local-first.
- Results must be deterministic for identical repository/environment inputs.
- The handoff is evidence, not acceptance authority.

## Acceptance criteria

ChatGPT may accept T001 only if:
1. all remaining readiness decisions were persisted and T001 was explicitly moved to `READY` before execution;
2. work occurred on `test/governance-harness` from the correct current `develop`;
3. no committed Markdown was modified by the executor;
4. code uses Python `>=3.13` and pytest `>=9,<10` consistently with D023;
5. `python -m pytest` executes the full deterministic suite in the approved environment;
6. no Agent Skill is required to make the suite run;
7. tests cover meaningful current Governance invariants;
8. tests require no production service, credential, or real business repository;
9. the full suite was actually executed and results reported honestly;
10. no test was weakened merely to get green;
11. dependencies/configuration comply with the approved toolchain policy;
12. `handoffs/T001-executor-handoff.json` accurately describes the final pushed branch and verification evidence;
13. the executor committed and pushed the reviewable branch before returning status;
14. the visible response contains the required minimal pointer.

## Verification requirements

The executor must:
- run the complete T001 suite through the approved local environment;
- include `python -m pytest` in the final complete-suite verification path;
- record exact commands and pass/fail/skip counts;
- record Python/pytest and other actually used tool versions;
- state network/service requirements;
- record dependency/configuration changes and working-tree status;
- persist all evidence in `handoffs/T001-executor-handoff.json`;
- commit and push the final review state before returning.

Do not claim success from static inspection.

## Stop / escalation conditions

Stop and persist `BLOCKED`/`PARTIAL` instead of guessing if:
- this Task Contract is not `READY`;
- repository contracts materially conflict;
- satisfying scope requires executor Markdown edits;
- current `develop` differs materially from the approved assumptions;
- D023 cannot be implemented under the later approved toolchain;
- the task would require a new mandatory Agent Skill contrary to D024;
- testable behavior requires a new architectural decision;
- implementation requires unauthorized production/external access;
- a dependency creates an unapproved supply-chain/security decision;
- the work changes public Governance semantics rather than merely testing them;
- installed SDD/Skill capabilities conflict with the later coexistence policy.

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
- Python/pytest and other tool versions;
- dependencies/config changes;
- network/service requirement flags;
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
