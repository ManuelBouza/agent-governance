# Product Development Workflow

Status: ACTIVE

## Purpose

Define how agents modify the canonical `agent-governance` source product without turning this repository into a consumer instance of its own Governance Core.

This is a repository-maintenance workflow, not an installed `.agent-coordination/` lifecycle. Real consumer-project governance is exercised only in separate repositories or synthetic disposable fixtures.

All mutation follows `docs/BRANCHING.md`. Verification follows `docs/TESTING-AND-EVALUATION.md`. D022 defines the controlling staged-change decision. D027 and `docs/ORCHESTRATOR-CHECKPOINTS.md` define ChatGPT source-maintenance continuity across conversations.

## Roles

- **Human Owner** — final authority.
- **ChatGPT Orchestrator** — research/specification/architecture owner, reviewer, Task Contract owner, source-maintenance checkpoint owner, and exclusive normal author of committed Markdown.
- **Agente de IA Ejecutor** — product-agnostic coding-agent role fulfilled by OpenCode, Codex, Claude Code, Antigravity, or another compatible agent; owns authorized non-Markdown implementation, tests/evals, execution, and persisted executor handoffs.

`AGENTS.md` is the normative repository adapter for these responsibilities.

## ChatGPT session cold start and turnover

Source-product orchestration must survive a ChatGPT chat change without requiring copied conversation history.

### Cold start

A fresh ChatGPT conversation SHALL:

1. fetch current `develop` through GitHub;
2. read `AGENTS.md`;
3. read `docs/orchestrator/CHECKPOINT.md`;
4. load only the checkpoint's `Next Chat Minimum Load` and directly controlling remote artifacts;
5. verify active referenced Task Contracts, handoffs, branches, PRs, and pushed SHAs before acting;
6. continue from the checkpoint's `Next Action` without asking the Human Owner to reconstruct completed work.

If the checkpoint is stale or contradictory, reconstruct the smallest safe frontier from authoritative Git state and refresh the checkpoint before mutation continues.

### Checkpoint refresh

ChatGPT refreshes `docs/orchestrator/CHECKPOINT.md` when the durable source-maintenance frontier changes materially, including accepted decisions, Task Contract readiness/status, executor review/rework, material blockers, or the next permitted action.

The checkpoint is a compact router/frontier, not a transcript. Reference controlling documents instead of copying them.

When a checkpoint update belongs to the same coherent Markdown planning change, include it in that same topic branch/PR rather than creating a separate PR merely for bookkeeping.

### Intentional chat closure

ChatGPT may explicitly recommend closing the current chat and using a new one only when:

- all material work/context is already persisted remotely;
- the current checkpoint is sufficient to resume;
- remote references required by the next action are available;
- no requirement, blocker, acceptance change, or review directive exists only in chat.

When closure is recommended, give the Human Owner the checkpoint path and a minimal new-chat prompt. Do not make the Human Owner paste a long summary.

The source checkpoint is not consumer Governance state and MUST NOT create a live `.agent-coordination/` instance in this repository.

## Change classes

ChatGPT classifies the proposed change before mutation.

### Markdown-only / research / decision

Examples:
- architecture decisions;
- Governance Core wording/protocol changes that require no delegated executable work;
- operating policy;
- Task Contracts;
- documentation.

ChatGPT performs these changes on an appropriate short-lived topic branch from `develop`, reviews the diff, and integrates by PR to `develop`.

A Task Contract is not required unless executable verification or non-Markdown work is delegated.

### Executable product change

Examples:
- implementation code;
- deterministic test/eval infrastructure;
- scripts/CLI;
- adapters/configuration;
- non-Markdown fixtures/assets.

Executable work requires a Task Contract already integrated into `develop` before the executor begins.

### Behavior-preserving refactor

Use `docs/REFACTORING-WORKFLOW.md`. The normal branch/contract/handoff rules in this document still apply.

### Release/hotfix

Use `docs/BRANCHING.md` and `docs/RELEASES.md`. Release promotion is separate from normal acceptance into `develop`.

## Common branch invariant

Normal work MUST NOT write directly to `main` or `develop`.

- `main` = stable/potentially releasable state.
- `develop` = next unreleased integration state.
- planning/Markdown changes use an appropriate short-lived topic branch -> PR -> `develop`.
- executor implementation uses the Task Contract's short-lived topic branch -> PR -> `develop` only after ChatGPT review.

Prefer one coherent, independently reviewable change per branch/PR. Split unrelated features, fixes, refactors, dependency upgrades, and cleanup.

## PD0 — Frame and research

ChatGPT determines:
- requested product outcome;
- change class;
- scope and exclusions;
- affected compatibility/security surface;
- whether external research is required;
- whether a Decision Record is required;
- whether executable work will be delegated;
- intended branch class/target.

Research conclusions that materially control future work are persisted in Markdown/Decision Records. Do not rely on chat history as the only durable rationale.

If the completed PD0 work changes the durable frontier or next action, refresh the Orchestrator checkpoint as part of the coherent Markdown change.

Do not create consumer mission/workplan/state records for repository development.

## PD1 — Persist the contract before execution

For every executable handoff, ChatGPT creates/updates the exact Task Contract under `docs/tasks/`.

The Task Contract defines at minimum:
- objective/result;
- controlling references;
- authorized scope and explicit exclusions;
- architecture/invariants/compatibility constraints;
- base/topic branch requirements;
- expected executor handoff path;
- acceptance criteria;
- verification/evidence requirements;
- stop/escalation conditions.

### Contract integration gate

The Task Contract and any controlling Markdown/Decision Records MUST be integrated into `develop` before executor implementation begins.

Normal sequence:

`planning branch -> PR -> develop (contract present) -> executor topic branch`

The executor implementation branch MUST be created from a `develop` revision that already contains the exact Task Contract it is expected to execute.

This keeps the requested work independently auditable before implementation exists.

### Contract freeze

Once implementation starts, the original task semantics are not silently rewritten to match the implementation.

- The executor never edits the Task Contract.
- Material changes to objective, scope, exclusions, invariants, acceptance, or verification meaning require ChatGPT to persist an explicit revision before execution continues.
- ChatGPT may update lifecycle metadata or append explicit review/revision/acceptance notes, provided the original request is not obscured.

## PD2 — Executor checkout and verification plan

After PD1 is integrated, ChatGPT gives the executor only a minimal launch prompt pointing to `AGENTS.md` and the exact Task Contract.

The executor MUST:
1. fetch the canonical repository/remotes;
2. start from current `develop` containing the Task Contract;
3. verify the working tree/base identity;
4. create or checkout the Task Contract's topic branch;
5. read only the controlling context required by the contract;
6. determine the implementation/test approach inside the approved contract.

Depending on task type, the executor may:
- add/update deterministic tests;
- add/update agent-facing evals;
- establish an approved pre-change characterization baseline;
- identify expected failing tests for intentional new behavior.

Tests/evals verify the approved contract; they do not redefine it.

## PD3 — Implement

The Agente de IA Ejecutor performs only authorized non-Markdown work.

The executor:
- edits implementation/config/assets inside scope;
- authors/updates applicable non-Markdown tests/evals/fixtures;
- does not edit committed Markdown;
- does not change strategic scope or acceptance;
- resolves ordinary technical implementation/test-design choices autonomously inside the contract;
- keeps the branch focused on one coherent task.

Markdown-only changes are performed by ChatGPT and skip executor implementation unless executable verification was explicitly delegated.

## PD4 — Verify, persist, commit, and push

The executor runs all verification required by the Task Contract and writes/updates the task's handoff under `handoffs/` according to `docs/EXECUTOR-HANDOFFS.md`.

Before returning any `DONE`, `BLOCKED`, or `PARTIAL` status, the executor MUST:
1. make the implementation/test/eval state internally coherent;
2. run the required verification;
3. update the persisted executor handoff so it describes the final local state;
4. commit all authorized implementation/test/eval/handoff changes on the topic branch;
5. push the topic branch to the canonical remote;
6. ensure the handoff identifies the pushed commit SHA and base SHA.

The remote topic branch is the review surface. ChatGPT MUST NOT be expected to trust a local-only SHA, copied terminal output, or chat-only claim.

If verification/specification is blocked, persist a `BLOCKED`/`PARTIAL` handoff, commit/push the auditable state when safe, and stop rather than guessing.

The executor MUST NOT make tests green by weakening the ChatGPT-approved contract.

## PD5 — Orchestrator remote review

ChatGPT uses GitHub to review:
- the persisted Task Contract and its revision history;
- the persisted executor handoff at the pushed HEAD;
- the remote base/head relationship;
- every changed file/diff in scope;
- implementation architecture and complexity;
- test/eval quality and whether tests would detect relevant breakage;
- verification evidence;
- dependencies/configuration/security implications;
- ownership and branch-policy compliance.

Green tests are necessary where applicable but are not sufficient for acceptance.

When review changes the durable frontier — accepted, blocked, rework requested, or a new controlling issue is discovered — refresh the Orchestrator checkpoint so another ChatGPT chat can resume the review loop from Git alone.

### Rework loop

If technical rework is required:
- if task semantics are unchanged, ChatGPT persists any durable review directive needed for the executor to act without relying on chat history;
- if objective/scope/acceptance/verification meaning changes materially, ChatGPT persists an explicit Task Contract revision before execution continues;
- the executor pulls the durable update, performs rework on the same task branch, reruns verification, updates the handoff, commits, pushes, and returns the minimal pointer again.

The loop repeats until accepted or cancelled/blocked by Human Owner/ChatGPT.

### Acceptance preparation

When ChatGPT accepts the implementation, ChatGPT may update Task Contract lifecycle/acceptance metadata on the task branch without rewriting the original execution semantics.

## PD6 — PR and integrate to develop

After PD5 acceptance:
1. ChatGPT normally creates the implementation PR from the pushed topic branch to `develop`;
2. the PR description identifies the Task Contract and executor handoff;
3. any available required checks/reviews must pass;
4. ChatGPT performs the final PR review against the accepted branch state;
5. prefer squash merge for one coherent normal topic change;
6. delete/retire the topic branch when appropriate.

The executor does not normally create or merge the implementation PR unless the Task Contract explicitly delegates that mechanical action.

Merging to `develop` means accepted into the next unreleased state. It does not mean released.

Promotion `develop` -> `main` is a separate action governed by `docs/BRANCHING.md` and `docs/RELEASES.md`.

Before intentionally closing the ChatGPT chat after integration, ensure `docs/orchestrator/CHECKPOINT.md` already describes a safe next frontier from which a fresh chat can resume.

## Handoff invariants

- ChatGPT -> repository: persist research/decisions/contracts first.
- Repository -> executor: Task Contract and controlling references are the source of task semantics.
- ChatGPT -> executor: launch prompt is only a minimal pointer.
- Executor -> repository: implementation/tests/evals plus persisted handoff are committed and pushed before status is returned.
- Executor -> ChatGPT: visible response contains only status, handoff path, branch, and pushed HEAD.
- ChatGPT -> executor rework: durable review directive/contract revision first when needed.
- ChatGPT -> PR/integration: only after remote review acceptance.
- ChatGPT -> next ChatGPT chat: `docs/orchestrator/CHECKPOINT.md` plus Git remote state are the source of continuity; prior chat history is optional.
- ChatGPT -> Human Owner: escalate scope/risk/public compatibility/release decisions when final authority is required.

No named executor product is privileged. Switching OpenCode -> Codex -> Claude Code -> another compatible executor does not change this procedure. Switching ChatGPT conversations does not change authority or require reconstructing source state from chat.

## Engineering rationale

This workflow intentionally uses small coherent changes, tests coupled to behavior changes, separate refactoring, durable change rationale, explicit review before integration, and compact cold-start checkpoints rather than ever-growing conversation context. These principles are consistent with the research basis recorded in D022 and the continuity decision in D027.
