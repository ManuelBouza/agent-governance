# T001 — Deterministic test harness foundation

Status: READY
Type: test/eval infrastructure
Base branch: `develop`
Expected topic branch: `test/governance-harness`
Owner for execution: Agente de IA Ejecutor
Specification owner/reviewer: ChatGPT Orchestrator

## Objective

Establish the first small, executable, repository-owned deterministic testing foundation for Agent Governance and implement an initial useful set of mechanical tests derived from D019.

The result must provide a repeatable local command that verifies a focused subset of Governance product invariants without using LLM judgment, production services, consumer business repositories, or hosted evaluation dependencies.

## Controlling references

Read and follow:
- `AGENTS.md`
- `docs/BRANCHING.md`
- `docs/DEVELOPMENT-WORKFLOW.md`
- `docs/TASK-CONTRACTS.md`
- `docs/TESTING-AND-EVALUATION.md`
- `docs/decisions/D010-governance-testing-scope.md`
- `docs/decisions/D016-binary-agent-role-model.md`
- `docs/decisions/D017-two-skill-architecture.md`
- `docs/decisions/D019-testing-and-evaluation-strategy.md`
- `tests/README.md`
- `evals/README.md`

Inspect the repository's existing non-Markdown configuration before choosing test tooling or adding dependencies.

## Checkout / branch precondition

If the repository is not yet cloned locally:
1. clone `https://github.com/ManuelBouza/agent-governance.git` into the current intended project directory;
2. fetch remotes;
3. checkout current `develop`;
4. verify the working tree is clean;
5. create `test/governance-harness` from current `develop` before modifying files.

If a checkout already exists, verify it represents the canonical repository and start from current `develop` before creating/reusing the expected topic branch.

Do not write directly to `main` or `develop`.

## Authorized scope

The executor may create or modify non-Markdown artifacts required for this first testing increment, including:
- deterministic test source files under `tests/`;
- non-Markdown synthetic fixtures under `tests/`;
- minimal test configuration/dependency files if justified;
- small reusable non-Markdown test helpers where they reduce duplication;
- lock/dependency metadata required by the selected local test stack.

The executor owns implementation and execution of these tests under D016.

## Required first-increment test surface

Implement a focused deterministic baseline that proves mechanical properties available from the current source tree. Prioritize the following, in this order where practical:

1. **Canonical source layout**
   - required product directories exist;
   - canonical Governance Core modules required by the current product contract exist;
   - Consumer and Maintainer Skill source boundaries are distinguishable;
   - the source repository does not contain a live consumer `.agent-coordination/` instance.

2. **Direct local reference integrity**
   - repository-internal references that the deterministic harness can resolve mechanically point to existing expected files/paths;
   - avoid attempting to judge semantic correctness of prose.

3. **Repository/product separation invariants**
   - fixtures/tests distinguish source-product artifacts from consumer installed-footprint paths;
   - no real consumer/business state is required by the suite.

4. **Harness foundation**
   - one documented-by-command executable entrypoint exists for the deterministic suite;
   - tests run locally without network access or credentials;
   - failures are actionable and identify the violated invariant.

Choose the smallest coherent subset that can be implemented cleanly in one PR. Do not inflate this task merely to cover every D019 layer.

## Explicit exclusions

Do NOT in T001:
- edit, create, rename, or delete any committed `*.md` file;
- implement final Consumer or Maintainer `SKILL.md`;
- implement the full `governance.py` product CLI unless a tiny test-only helper is strictly necessary (prefer not to);
- implement behavioral/model eval execution;
- implement trigger-rate measurement;
- add hosted eval frameworks;
- add OPA/Rego merely because OPA is a research reference;
- add Hypothesis unless a genuinely stateful property is included in this first increment and the dependency is justified; simple deterministic assertions should remain simple;
- access production/external services, credentials, or real consumer repositories;
- create a live `.agent-governance/` / `.agent-coordination/` consumer instance at repository root;
- change branch/release policy;
- open or merge a PR before ChatGPT Orchestrator reviews the implementation and evidence.

## Invariants / constraints

- Mechanical properties are tested by code, not by LLM graders.
- Tests validate Agent Governance itself, never general coding ability.
- Test implementation must not redefine the Markdown contract.
- No named executor product receives special semantics.
- Keep dependencies minimal and local-first.
- The suite must be deterministic for identical repository content/environment inputs.
- The implementation should be portable enough to run in normal contributor/CI environments without secrets.

## Acceptance criteria

ChatGPT may accept T001 only if all are true:

1. Work occurred on `test/governance-harness` based on current `develop`.
2. No committed Markdown was modified by the executor.
3. A deterministic test harness exists and has a clear local execution command inferable from the non-Markdown project configuration/tooling.
4. The first test set covers meaningful current Governance product invariants from the required first-increment surface.
5. Tests require no network, production service, credential, or real business repository.
6. The full implemented T001 suite was actually executed.
7. The implemented suite is green, or any pre-existing/blocking failure is explicitly reported rather than hidden/skipped.
8. No test was weakened merely to make implementation pass.
9. Added dependencies are minimal and justified by the test surface.
10. The executor returns reproducible evidence sufficient for ChatGPT to review the change.

## Verification requirements

The executor must:
- run the complete T001 deterministic suite after implementation;
- provide the exact command(s) used;
- report test count and pass/fail/skip outcome;
- report interpreter/runtime and relevant test-tool versions;
- confirm whether network access was required (expected: no);
- show working-tree status at handoff;
- identify any dependency/configuration files added or modified.

Do not claim success from static inspection alone.

## Stop / escalation conditions

Stop and report to ChatGPT instead of guessing if:
- repository Markdown contracts conflict materially;
- satisfying a requirement appears to require editing Markdown;
- the expected `develop` baseline differs materially from the task assumptions;
- testable mechanical behavior cannot be determined without a new architectural decision;
- implementation would require production/external access;
- a required dependency creates a significant supply-chain/security decision not already authorized;
- the task appears to require changing public Governance semantics rather than only testing them.

Normal test implementation choices do not require escalation.

## Expected handoff

Return to ChatGPT Orchestrator:
- current branch and HEAD;
- base `develop` SHA used;
- files created/modified;
- concise implementation/tooling rationale;
- exact verification commands;
- exact results, including count/failures/skips;
- runtime/test-tool versions;
- dependencies/config changes;
- `git status` summary;
- unresolved issues/ambiguities;
- a proposed next incremental testing task, without implementing it unless separately authorized.

Do not open or merge a PR until ChatGPT has reviewed this handoff and the repository diff.
