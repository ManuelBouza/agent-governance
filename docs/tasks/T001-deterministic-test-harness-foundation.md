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

T001 remains blocked until ChatGPT/Human Owner resolve and persist the following source-product foundation decisions:
1. programming language and concrete testing stack;
2. Skills/capabilities required for test development/execution;
3. local CLI/development toolchain required to support the Agente de IA Ejecutor;
4. coexistence/non-overlap policy with pre-existing SDD systems, Skills, and equivalent project capabilities.

Once those decisions are persisted and this Task Contract is reconciled with them, ChatGPT may move T001 back to `READY` through a normal Markdown planning change.

## Objective

Establish the first small, executable, repository-owned deterministic testing foundation for Agent Governance and implement an initial useful set of mechanical tests derived from D019.

The result must provide a repeatable local command that verifies a focused subset of Governance product invariants without using LLM judgment, production services, consumer business repositories, or hosted evaluation dependencies.

## Controlling references

Read and follow:
- `AGENTS.md`
- `docs/BRANCHING.md`
- `docs/DEVELOPMENT-WORKFLOW.md`
- `docs/TASK-CONTRACTS.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `docs/TESTING-AND-EVALUATION.md`
- `docs/decisions/D010-governance-testing-scope.md`
- `docs/decisions/D016-binary-agent-role-model.md`
- `docs/decisions/D017-two-skill-architecture.md`
- `docs/decisions/D019-testing-and-evaluation-strategy.md`
- `docs/decisions/D021-persisted-executor-handoffs.md`
- `docs/decisions/D022-source-product-change-procedure.md`
- `tests/README.md`
- `evals/README.md`

Future decisions resolving this task's readiness block become controlling references before execution.

## Checkout / branch precondition

When and only when status becomes `READY`:
1. clone/fetch the canonical repository as needed;
2. checkout current `develop` containing the final READY Task Contract and all readiness decisions;
3. verify the working tree is clean;
4. create `test/governance-harness` from that current `develop` before modifying files.

Do not write directly to `main` or `develop`.

## Authorized scope

Once READY, the executor may create or modify non-Markdown artifacts required for this first testing increment, including:
- deterministic test source files under `tests/`;
- non-Markdown synthetic fixtures under `tests/`;
- minimal test configuration/dependency files explicitly consistent with the persisted language/toolchain decisions;
- small reusable non-Markdown test helpers where they reduce duplication;
- lock/dependency metadata required by the approved local test stack;
- `handoffs/T001-executor-handoff.json` as the authoritative persisted executor result.

The executor owns implementation, test execution, and the persisted executor handoff under D016/D021/D022.

## Required first-increment test surface

Implement a focused deterministic baseline that proves mechanical properties available from the current source tree. Prioritize:

1. **Canonical source layout**
   - required product directories exist;
   - canonical Governance Core modules required by the current product contract exist;
   - Consumer and Maintainer Skill source boundaries are distinguishable;
   - the source repository does not contain a live consumer `.agent-coordination/` instance.

2. **Direct local reference integrity**
   - mechanically resolvable repository-internal references point to expected existing files/paths;
   - do not attempt to judge semantic prose correctness with deterministic assertions.

3. **Repository/product separation invariants**
   - fixtures/tests distinguish source-product artifacts from consumer installed-footprint paths;
   - no real consumer/business state is required by the suite.

4. **Harness foundation**
   - one approved local executable entrypoint exists for the deterministic suite;
   - tests run without production credentials/services;
   - failures identify the violated invariant.

Choose the smallest coherent subset that can be implemented cleanly in one PR. Do not inflate T001 into all D019 layers.

## Explicit exclusions

Do NOT in T001:
- execute while this Task Contract is `BLOCKED`;
- edit, create, rename, or delete committed `*.md` as the executor;
- implement final Consumer or Maintainer `SKILL.md`;
- implement the full product CLI unless explicitly justified by later approved toolchain decisions and this Task Contract is revised accordingly;
- implement behavioral/model eval execution;
- implement trigger-rate measurement;
- add hosted eval frameworks without explicit authorization;
- add OPA/Rego merely because OPA is a research reference;
- add Hypothesis unless the approved testing-stack decision and actual stateful scope justify it;
- access production/external services, credentials, or real consumer repositories;
- create a live `.agent-governance/` / `.agent-coordination/` consumer instance at repository root;
- change branch/release policy;
- open or merge a PR before ChatGPT Orchestrator reviews the pushed implementation and persisted handoff.

## Invariants / constraints

- Mechanical properties are tested by code, not by LLM graders.
- Tests validate Agent Governance itself, never general coding ability.
- Test implementation must not redefine the Markdown contract.
- No named executor product receives special semantics.
- Approved language/toolchain/Skill/coexistence decisions control implementation once persisted.
- Keep dependencies minimal and local-first.
- The suite must be deterministic for identical repository content/environment inputs.
- The implementation should be portable enough for normal contributor/CI environments without secrets.
- The executor handoff is evidence/reporting, not acceptance authority.

## Acceptance criteria

ChatGPT may accept T001 only if all are true:
1. all readiness-block decisions were persisted before execution and T001 was explicitly returned to `READY`;
2. work occurred on `test/governance-harness` based on the correct current `develop`;
3. no committed Markdown was modified by the executor;
4. an approved deterministic test harness exists with the official local execution command defined by the persisted stack/toolchain decisions;
5. the first test set covers meaningful current Governance product invariants;
6. tests require no production service, credential, or real business repository;
7. the full implemented T001 suite was actually executed;
8. the implemented suite is green, or any pre-existing/blocking failure is explicitly reported rather than hidden/skipped;
9. no test was weakened merely to make implementation pass;
10. dependencies are minimal and consistent with approved toolchain policy;
11. `handoffs/T001-executor-handoff.json` accurately describes the final pushed implementation branch and verification evidence;
12. the executor committed and pushed the reviewable task branch before returning status;
13. the visible response points ChatGPT to the persisted handoff rather than duplicating the report in chat.

## Verification requirements

The executor must:
- run the complete T001 deterministic suite after implementation;
- record exact commands;
- record test count and pass/fail/skip outcome;
- record runtime/test-tool versions;
- confirm network/service requirements;
- record working-tree status;
- identify dependency/configuration files changed;
- persist all evidence in `handoffs/T001-executor-handoff.json`;
- commit and push the final review state before returning status.

Do not claim success from static inspection alone.

## Stop / escalation conditions

Stop and persist a `BLOCKED`/`PARTIAL` executor handoff instead of guessing if:
- this Task Contract is not `READY`;
- repository contracts conflict materially;
- satisfying a requirement appears to require executor Markdown edits;
- the expected `develop` baseline differs materially from task assumptions;
- testable behavior cannot be determined without a new architectural decision;
- implementation would require unauthorized production/external access;
- a dependency creates a significant supply-chain/security decision not authorized by the toolchain decision;
- the task requires changing public Governance semantics rather than testing them;
- existing SDD/Skill capabilities conflict with the approved coexistence policy.

## Expected persisted handoff

Before returning to ChatGPT, write/update exactly:

`handoffs/T001-executor-handoff.json`

Follow `docs/EXECUTOR-HANDOFFS.md`. At minimum include:
- `task_id`: `T001`;
- `status`: `DONE`, `BLOCKED`, or `PARTIAL`;
- `task_contract_path`;
- current branch and pushed final HEAD;
- base `develop` SHA;
- files created/modified;
- concise implementation/tooling rationale;
- exact verification commands/results/counts;
- runtime/test-tool versions;
- dependencies/config changes;
- network/service requirement flags;
- `git status` summary;
- unresolved issues/ambiguities;
- proposed next incremental testing task;
- `chatgpt_read_path`: `handoffs/T001-executor-handoff.json`.

## Visible executor response

After the handoff and final review state are committed and pushed, return only:

`STATUS: DONE | BLOCKED | PARTIAL`

`HANDOFF: handoffs/T001-executor-handoff.json`

`BRANCH: test/governance-harness`

`HEAD: <pushed-final-commit-sha>`

Do not open or merge a PR unless the Task Contract explicitly delegates that action after ChatGPT review.
