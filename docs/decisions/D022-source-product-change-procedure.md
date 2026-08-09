# D022 — Source product change procedure

Status: ACCEPTED
Authority: Human Owner

## Decision

Changes to the canonical `agent-governance` source repository SHALL use a repository-native staged change procedure. The source repository MUST NOT install or reuse the consumer F0–F6 governance lifecycle for its own maintenance.

The source workflow keeps the existing separation between normal product development (`PD`) and behavior-preserving refactoring (`RF`), but tightens the audit and review boundaries as follows.

### Common rules

- `main` remains stable; `develop` remains the integration base.
- Every mutation occurs on a short-lived topic branch.
- Prefer one coherent, independently reviewable change per branch/PR.
- Separate behavior-preserving refactors from behavior changes, bug fixes, dependency upgrades, and unrelated cleanup.
- ChatGPT Orchestrator owns research synthesis, decisions, architecture, Task Contracts, review, and committed Markdown.
- The Agente de IA Ejecutor remains product-agnostic and owns authorized non-Markdown implementation, tests/evals, execution, and executor handoffs.

### Markdown-only changes

When the change is entirely within ChatGPT-owned Markdown:

1. ChatGPT frames/researches the change.
2. ChatGPT creates a `docs/*`, `fix/*`, or other appropriate topic branch from current `develop`.
3. ChatGPT persists the Markdown change and any Decision Record required by the change.
4. ChatGPT reviews the resulting Git diff for scope, consistency, references, architecture, and branch policy.
5. The change returns to `develop` through PR.

An executor Task Contract is not required unless executable verification or non-Markdown implementation is delegated.

### Executable changes

Executable work uses a two-stage source history:

1. **Contract stage** — ChatGPT persists the Task Contract and any controlling Markdown/Decision Records on a planning/docs topic branch and integrates that planning change into `develop` before executor implementation begins.
2. **Implementation stage** — the executor creates the task's implementation topic branch from the `develop` revision that already contains the approved Task Contract.
3. The executor implements/tests only the authorized non-Markdown scope.
4. The executor runs required verification and writes the task's non-Markdown executor handoff.
5. Before returning status, the executor commits and pushes the implementation branch so the remote branch contains the implementation, tests/evals, and current handoff artifact.
6. The executor returns only the minimal status pointer defined by `docs/EXECUTOR-HANDOFFS.md`.
7. ChatGPT reviews the persisted Task Contract, remote branch diff, executor handoff, and verification evidence through GitHub.
8. If rework is required, ChatGPT persists any material contract revision before the executor continues. Non-material clarifications/review directives must also be durable in Git/PR history rather than chat-only requirements.
9. Only after ChatGPT accepts the implementation does the implementation branch proceed through PR to `develop`.

The executor MUST NOT open or merge the normal implementation PR unless a Task Contract explicitly delegates that mechanical action. ChatGPT normally controls PR creation/review/integration after the remote handoff is auditable.

### Task Contract freeze and revision

The original objective, scope, exclusions, invariants, acceptance criteria, and verification meaning form the execution contract.

After implementation starts:
- the executor cannot edit the Task Contract;
- ChatGPT MUST NOT silently rewrite the contract merely to match the implementation;
- material changes require an explicit persisted revision before execution continues;
- lifecycle metadata, explicit revision notes, review directives, and final acceptance metadata may be appended/updated by ChatGPT without pretending they were part of the original request.

### Refactoring

Behavior-preserving refactors continue to use `docs/REFACTORING-WORKFLOW.md`.

For executable refactors:
- the refactor Task Contract must already be integrated in `develop` before execution starts;
- RF1 characterization/baseline evidence must be persisted and pushed before structural mutation when a new or materially confirmed baseline is required;
- ChatGPT freezes/accepts the baseline before RF3 begins;
- the executor then performs the refactor and produces the final persisted handoff;
- a discovered need to change behavior terminates RF classification and returns to normal PD flow.

### Release boundary

Merging to `develop` accepts a change into the next unreleased integration state. It does not itself publish a release.

Promotion `develop` -> `main`, tags, and release artifacts remain a separate release/stability action under `docs/BRANCHING.md` and `docs/RELEASES.md`.

## Research basis

This procedure adapts established engineering practices rather than claiming a new external standard.

### Google Engineering Practices — Small CLs

https://google.github.io/eng-practices/review/developer/small-cls.html

Adopted principles:
- prefer one self-contained change;
- small changes are easier to review, reason about, merge, and roll back;
- related tests belong with behavior changes;
- refactorings are normally separated from feature/bug changes;
- when behavior lacks coverage, tests can be submitted before a refactor to establish confidence.

### Google Engineering Practices — CL descriptions and review

https://google.github.io/eng-practices/review/developer/cl-descriptions.html
https://google.github.io/eng-practices/review/reviewer/looking-for.html

Adopted principles:
- durable version-control history should explain what changed and why;
- review must consider design, functionality, complexity, tests, documentation, and system-level context;
- tests being green do not replace human/architectural review.

### Martin Fowler — Refactoring

https://www.martinfowler.com/books/refactoring.html

Adopted principle:
- refactoring is performed through small behavior-preserving transformations that keep the system working and reduce regression risk.

### GitHub protected-branch / PR model

https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches

Adopted principle:
- protected long-lived branches should be updated through review/check gates rather than normal direct writes.

## Consequences

- `docs/DEVELOPMENT-WORKFLOW.md` is the canonical normal source-change lifecycle and must encode the contract-first/push-before-review sequence.
- `docs/REFACTORING-WORKFLOW.md` must encode the persisted RF1 baseline checkpoint.
- `docs/TASK-CONTRACTS.md` must require the executable Task Contract to be available in `develop` before implementation starts.
- `docs/EXECUTOR-HANDOFFS.md` must require commit + push before the executor reports status.
- `AGENTS.md` must require ChatGPT to review remote Git evidence, not local/chat-only claims.
- Existing executable task T001 is not ready to run until the separately identified prerequisites for test language/stack, required Skills, local development toolchain, and coexistence with existing SDD/Skill systems are resolved and persisted.