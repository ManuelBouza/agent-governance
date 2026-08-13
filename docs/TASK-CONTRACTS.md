# Source Product Task Contracts

Status: ACTIVE

## Purpose

Define the persistent handoff format used when ChatGPT Orchestrator delegates executable work in the canonical `agent-governance` source repository.

Task Contracts are auditable source-product maintenance records. They are intentionally separate from consumer-project `.agent-coordination/` tasks.

## Authority

- ChatGPT Orchestrator authors and revises Task Contract Markdown.
- The Agente de IA Ejecutor reads Task Contracts as authoritative execution scope and MUST NOT edit them.
- The Human Owner retains final authority.

A chat/terminal prompt is only a pointer to a Task Contract. It is not the canonical task specification.

## Executor process autonomy invariant

Task Contracts define **what must be delivered and what boundaries must hold**. They do not normally define **how the executor must organize its internal implementation process**.

Under D041, the Agente de IA Ejecutor may independently choose and compose any compatible executor-native methods and capabilities needed to satisfy the contract, including direct work, internal planning, SDD/specification workflows, sub-agents/workers, Skills, code-graph/navigation tools, testing/review helpers, or other mechanisms.

```text
Task Contract = outcome + scope + invariants + acceptance + evidence
Executor       = implementation process + internal orchestration
```

ChatGPT MUST NOT prescribe executor-specific agent types, delegation topology, SDD routing, internal planning structure, or tool selection unless the method itself is material to an accepted safety/security/reproducibility/ownership requirement or to the requested product behavior.

Likewise, review MUST NOT require the executor's private orchestration trace unless a particular process artifact was explicitly part of the persisted deliverable/evidence contract. Governance evaluates remote Git state, persisted handoff and required verification evidence.

Executor-native workflows remain subordinate implementation mechanisms: they may not redefine Task Contract semantics, acquire Governance acceptance authority, or introduce tracked/generated repository state outside authorized scope.

## Location and naming

Active and completed source-maintenance Task Contracts live under:

`docs/tasks/`

Recommended naming:

`TNNN-<short-slug>.md`

Task IDs are stable once assigned.

Each executable task SHOULD identify its expected persisted executor handoff path under `handoffs/`, normally:

`handoffs/TNNN-executor-handoff.json`

## Required fields

Each task should contain:

### Identity
- Task ID
- Status: `DRAFT`, `BLOCKED`, `READY`, `IN_PROGRESS`, `DONE`, `ACCEPTED`, `CANCELLED`
- Type: feature, fix, refactor, test/eval, release, infrastructure, or mixed
- Base branch
- Expected topic branch
- Expected executor handoff path

### Objective
A concise description of the observable result required.

### Controlling references
Only the repository files/decisions needed to interpret the task correctly. `AGENTS.md` is always controlling.

### Authorized scope
Artifacts and behavior the executor is allowed to modify or create.

Authorized scope constrains externally visible repository mutation/result, not the executor's private internal organization or compatible local tooling unless the contract explicitly states otherwise for a material reason.

### Explicit exclusions
Things the executor must not change or expand into.

Exclusions should protect product scope, authority, safety, reproducibility or repository state. Avoid using exclusions to ban an executor-internal methodology/tool merely because the current host provides it.

### Invariants / constraints
Architecture, compatibility, safety, ownership, or behavioral properties that must remain true.

### Acceptance criteria
Objective conditions ChatGPT will use to accept or reject the implementation.

### Verification requirements
Tests/evals that must be created or executed and the minimum evidence expected.

Verification requirements define required evidence/results. They should not dictate internal execution topology unless that topology is itself part of the behavior or assurance property being verified.

### Stop / escalation conditions
Conditions requiring the executor to stop instead of guessing or expanding scope.

### Expected handoff
The executor MUST persist its result according to `docs/EXECUTOR-HANDOFFS.md` at the task's expected handoff path before claiming `DONE`, `BLOCKED`, or `PARTIAL`.

## Contract integration gate

An executable Task Contract is not ready for execution merely because it exists on a planning branch.

Before launching an executor:
1. ChatGPT creates/updates the Task Contract on a policy-compliant planning/Markdown topic branch;
2. ChatGPT reviews the contract and controlling Markdown/Decision Records;
3. the planning change is merged into `develop`;
4. the task status is `READY` only when all known prerequisite decisions are resolved;
5. the executor implementation branch is then created from a `develop` revision containing that exact contract.

This creates two durable stages:

`contract history -> implementation history`

The executor MUST NOT begin executable work from a branch/revision that predates the controlling Task Contract.

## Freeze and revision semantics

The original objective, scope, exclusions, invariants, acceptance criteria, and verification meaning are the durable request.

After implementation begins:
- the executor cannot edit the Task Contract;
- ChatGPT must not silently rewrite the original task semantics to match implementation;
- a material change requires an explicit persisted revision before execution continues;
- lifecycle metadata and explicit review/revision/acceptance notes may be updated/appended by ChatGPT as long as the original request remains auditable.

A reviewer must be able to distinguish the original task from later authorized revisions.

## Lifecycle

1. ChatGPT frames/researches the change.
2. ChatGPT creates the Task Contract on a planning branch.
3. The Task Contract is reviewed and integrated into `develop`.
4. ChatGPT launches the executor with the canonical minimal launch prompt defined below.
5. The executor creates/uses the authorized implementation topic branch from the `develop` revision containing the contract.
6. The executor chooses its internal implementation process and performs only authorized non-Markdown work.
7. Material task changes require a persisted ChatGPT revision before execution continues.
8. The executor runs required verification and persists its non-Markdown handoff under `handoffs/`.
9. The executor commits and pushes the implementation branch, including the current handoff artifact.
10. The executor returns only status, handoff path, branch, and pushed HEAD.
11. ChatGPT reads the Task Contract, handoff, and remote Git diff/evidence.
12. Rework repeats on the same task branch using durable review/revision instructions.
13. After ChatGPT acceptance, the implementation proceeds through PR to `develop`.
14. ChatGPT may update lifecycle/acceptance metadata without rewriting original execution semantics.
15. After accepted task content/handoff and acceptance records are integrated, any delegated post-integration branch retirement MUST be governed by an integrated Operational Contract under `docs/OPERATION-CONTRACTS.md` and launched only through `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`.
16. Operational task closure is complete only after required remote/local branch cleanup is verified.

## Canonical minimal executor launch prompt

Every normal source-product executor launch MUST use the same structural contract. The launch prompt is transport/bootstrap only; it MUST NOT become a second task specification.

The prompt contains exactly these semantic parts:

1. **Role** — identify the abstract `Agente de IA Ejecutor` role and canonical repository.
2. **Repository baseline** — instruct the executor to start from the current Task Contract base branch, normally current `develop`.
3. **Bootstrap** — instruct the executor to read `AGENTS.md` first.
4. **Authoritative task pointer** — provide exactly one controlling Task Contract path and state that the Task Contract plus its referenced repository policies are the complete execution specification.
5. **Completion contract** — require the contract-defined verification/handoff, commit and push, then require only the minimal status/handoff/branch/HEAD response.

Canonical template:

```text
Operate as the Agente de IA Ejecutor for <owner>/<repository>.

Start from current <base-branch> and read AGENTS.md first.

Then load and execute the authoritative Task Contract:
<task-contract-path>

Treat that Task Contract and its referenced repository policies as the complete execution specification. Do not infer or expand task scope from this prompt.

Complete the required verification and executor handoff, commit and push all authorized work, then return only:

STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: <path>
BRANCH: <branch>
HEAD: <pushed-commit-sha>
```

For normal launches, substitute only repository identity, base branch and Task Contract path. The output placeholders remain the generic completion schema; the concrete handoff path/branch are resolved from the Task Contract.

### Launch-prompt non-duplication invariant

The launch prompt MUST NOT duplicate task semantics that belong in Git, including:

- objective/result;
- acceptance criteria;
- authorized filenames/scope;
- exclusions;
- architecture/design constraints;
- test commands or fixture families;
- expected implementation branch/handoff path when the Task Contract already defines them;
- provider/product-specific implementation instructions;
- task-specific safety/security restrictions;
- protocol/module versions;
- executor-internal methodology, sub-agent topology, SDD mode, Skill routing, or tool choice.

Standing repository rules such as Markdown ownership also remain in `AGENTS.md`/referenced policy and SHOULD NOT be re-stated task-by-task in the launch prompt.

If any such task-specific fact is necessary to execute safely or correctly, persist it in the Task Contract or its controlling repository policy before launch rather than extending the chat/terminal prompt.

### Launch-prompt authority invariant

The prompt does not supersede or supplement missing Task Contract semantics.

```text
launch prompt = role + repository + bootstrap + task pointer + completion contract
Task Contract + referenced Git policy = execution specification
```

If the Task Contract is missing, not `READY`, not integrated into the stated base branch, or materially incomplete, do not compensate by adding instructions to the launch prompt. Repair/persist the contract first.

If a launch prompt conflicts with the persisted Task Contract or repository policy, the executor MUST stop/escalate rather than choosing the chat-only instruction as a new task scope. Human/ChatGPT changes to objective/scope/acceptance/verification must be persisted through the normal Task Contract revision flow.

## Canonical post-integration cleanup delegation

Post-integration branch retirement is not another implementation launch and MUST NOT be expressed as an ad hoc executor instruction or as a chat-carried `TASK`/`PR` cleanup target.

Before delegating cleanup, ChatGPT MUST persist the complete concrete operation in an integrated `docs/operations/OPNNN-*.md` Operational Contract governed by `docs/OPERATION-CONTRACTS.md`.

The cleanup bootstrap prompt then contains only repository/base/bootstrap context plus exactly one Operational Contract path. All concrete targets, resolved-review exceptions, safety semantics, and required evidence live in Git.

```text
normal task launch -> Task Contract pointer
post-integration cleanup -> Operational Contract pointer
prompt-specific operation semantics -> prohibited
```

If cleanup safety cannot be derived from the persisted Operational Contract and its referenced authoritative Git/GitHub state, the executor returns `BLOCKED` or `PARTIAL`; ChatGPT MUST NOT compensate with chat-only instructions.

## Minimal executor response pattern

After persisting/committing/pushing the required implementation handoff, the executor should return only:

`STATUS: DONE | BLOCKED | PARTIAL`

`HANDOFF: handoffs/TNNN-executor-handoff.json`

`BRANCH: <topic-branch>`

`HEAD: <pushed-commit-sha>`

Operational Contract completion schemas are defined by each integrated Operational Contract and are referenced through `docs/POST-INTEGRATION-CLEANUP-PROMPT.md` for branch retirement.

## Audit invariant

A reviewer must be able to reconstruct from Git alone:
- what was requested before implementation or operation;
- any explicit revisions/review directives;
- what the executor reported it did;
- what actually changed.

Chat history and private executor orchestration traces must not be required for this reconstruction unless a persisted contract explicitly makes a process artifact part of the deliverable/evidence.