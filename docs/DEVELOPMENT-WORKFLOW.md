# Product Development Workflow

Status: ACTIVE

## Purpose

Define how agents modify the canonical `agent-governance` source product without turning this repository into a consumer instance of its own Governance Core.

This is a repository-maintenance workflow, not an installed `.agent-coordination/` lifecycle. Real consumer-project governance is exercised only in separate repositories or synthetic disposable fixtures.

All mutation follows `docs/BRANCHING.md`. Verification follows `docs/TESTING-AND-EVALUATION.md`. D022 defines the controlling staged-change decision. D027 and `docs/ORCHESTRATOR-CHECKPOINTS.md` define ChatGPT source-maintenance continuity across conversations. D052 and `docs/CONFORMANCE-ORACLE-CONTRACT.md` control specification-owned conformance authorship where applicable. Accepted D053 defines native Spec-Driven Development stage ownership for source work.

## Native SDD mapping

Source maintenance remains PD0-PD6. D053 overlays the stages rather than creating a parallel lifecycle:

```text
PD0 -> Orchestrator Explore / Frame + Specify + initial Design
PD1 -> Orchestrator complete Design + Plan & Trace + Task Contract/conformance persistence
PD2 -> execution readiness/bootstrap only; no transfer of SDD Design/Plan authority
PD3 -> Executor Implement
PD4 -> Executor Code Review & Verify + handoff/publish evidence
PD5 -> Orchestrator Converge / Accept / explicit re-entry
PD6 -> Orchestrator Integrate & Evolve
```

Every applicable source change receives proportionate `COMPACT`, `STANDARD`, or `ASSURED` SDD coverage. Material requirement changes use `ADDED / MODIFIED / REMOVED / PRESERVED`. Existing normative source artifacts may serve as current specification carriers; do not create duplicate truth merely to manufacture a new spec file.

## Roles

- **Human Owner** — final authority.
- **ChatGPT Orchestrator** — owns SDD Explore/Frame, Specify, complete controlling Design, Plan & Trace, semantic convergence/acceptance/current-spec evolution, research, Task Contracts, source-maintenance checkpoints, exclusive normal committed Markdown authoring, and D052-designated semantic conformance/oracle assets.
- **Agente de IA Ejecutor** — product-agnostic coding-agent role fulfilled by OpenCode, Codex, Claude Code, Antigravity, or another compatible agent; owns SDD Implement plus Code Review & Verify for authorized non-Markdown technical implementation, implementation/exploratory tests/evals, harness/configuration, verification execution/evidence, and persisted executor handoffs, subject to D052-designated Orchestrator conformance assets.

No SDD stage is dual-owned. Executor-local coding choices remain implementation details only while they preserve the Orchestrator-approved Design. A material specification/Design/Plan defect discovered during PD3/PD4 requires explicit re-entry to the earliest affected Orchestrator stage before work continues.

`AGENTS.md` is the normative repository adapter for these responsibilities.

### D052 test-authorship overlay

When test/eval ownership is material, a new or materially revised Task Contract SHOULD select `orchestrator-conformance`, `executor-implementation`, or `mixed` under D052.

```text
orchestrator-conformance / mixed
    Orchestrator -> required semantic conformance/oracle assets
    Executor     -> implementation/exploratory tests + execution/evidence

executor-implementation
    Executor     -> implementation/exploratory tests + execution/evidence
```

The D052 exception is narrow: it does not transfer general implementation, runner plumbing, provider adapters, technical debugging helpers, measurements, traces, executor handoffs, or ordinary implementation tests to ChatGPT.

Semantic oracle changes require persisted Orchestrator authority. A test/eval remains evidence, never Governance authority.

D052 is prospective. Existing T032/T021 work remains grandfathered and T022 may complete under its already-integrated contract as stated by D052. D053 is likewise prospective/delta-first; historical Task Contracts are not rewritten merely to attach SDD labels.

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

ChatGPT refreshes `docs/orchestrator/CHECKPOINT.md` when the durable source-maintenance frontier changes materially, including accepted specification/Design/Plan decisions, Task Contract readiness/status, executor review/rework, material blockers, or the next permitted action.

The checkpoint is a compact router/frontier, not a transcript. Reference controlling documents instead of copying them.

When a checkpoint update belongs to the same coherent Markdown planning change, include it in that same topic branch/PR rather than creating a separate PR merely for bookkeeping.

### Intentional chat closure

ChatGPT may explicitly recommend closing the current chat and using a new one only when:

- all material work/context is already persisted remotely;
- the current checkpoint is sufficient to resume;
- remote references required by the next action are available;
- no requirement, blocker, acceptance change, Design/Plan revision, or review directive exists only in chat.

When closure is recommended, give the Human Owner the checkpoint path and a minimal new-chat prompt. Do not make the Human Owner paste a long summary.

The source checkpoint is not consumer Governance state and MUST NOT create a live `.agent-coordination/` instance in this repository.

## Change classes and SDD proportionality

ChatGPT classifies the proposed change before mutation and selects the proportionate SDD profile.

### Markdown-only / research / decision

Examples:
- architecture/specification decisions;
- Governance Core wording/protocol changes that require no delegated executable work;
- operating policy;
- Task Contracts;
- documentation.

ChatGPT performs these changes on an appropriate short-lived topic branch from `develop`, reviews the diff, and integrates by PR to `develop`.

A Task Contract is not required unless executable verification or non-Markdown work is delegated. D053 still applies: ChatGPT performs the applicable Explore/Specify/Design/Plan/Converge reasoning itself for Orchestrator-owned artifacts; no Executor is inserted merely for ceremony.

### Executable product change

Examples:
- implementation code;
- deterministic test/eval infrastructure;
- scripts/CLI;
- adapters/configuration;
- non-Markdown fixtures/assets;
- D052-designated non-Markdown semantic conformance/oracle assets.

Executable Executor work requires a complete SDD-anchored Task Contract already integrated into `develop` before the executor begins. When D052 selects `orchestrator-conformance` or `mixed`, required Orchestrator-owned conformance assets are persisted/reviewed before Executor implementation when they are needed to define acceptance.

### Behavior-preserving refactor

Use `docs/REFACTORING-WORKFLOW.md`. The normal branch/contract/handoff rules in this document still apply. Under D053, material non-regression behavior is expressed as `PRESERVED` requirements/accepted characterization owned by the Orchestrator.

### Release/hotfix

Use `docs/BRANCHING.md` and `docs/RELEASES.md`. Release promotion is separate from normal acceptance into `develop`.

## Common branch invariant

Normal work MUST NOT write directly to `main` or `develop`.

- `main` = stable/potentially releasable state.
- `develop` = next unreleased integration state.
- planning/specification/Design/Markdown and Orchestrator-owned D052 conformance changes use an appropriate short-lived topic branch -> review/PR -> `develop`.
- executor implementation uses the Task Contract's short-lived topic branch -> PR -> `develop` only after ChatGPT convergence review.

Prefer one coherent, independently reviewable change per branch/PR. Split unrelated features, fixes, refactors, dependency upgrades, and cleanup.

## PD0 — Explore / Frame, Specify, and initial Design

ChatGPT determines:
- requested product outcome;
- change class and SDD profile;
- touched capability/artifact and accepted current specification carrier when one exists;
- scope and exclusions;
- material `ADDED / MODIFIED / REMOVED / PRESERVED` requirement delta or explicit zero-behavior-delta/PRESERVED contract;
- affected compatibility/security/privacy/reliability/operational surface;
- whether external research is required;
- whether a Decision Record is required;
- initial controlling solution/architecture direction;
- whether executable work will be delegated;
- intended branch class/target.

Material requirements should be independently traceable/verifiable where useful and should identify verification methods when that affects Design/Plan. Given/When/Then scenarios may be used where they materially reduce ambiguity.

Research conclusions, specification semantics and controlling Design decisions that materially affect future work are persisted in Markdown/Decision Records. Do not rely on chat history as the only durable rationale.

If the completed PD0 work changes the durable frontier or next action, refresh the Orchestrator checkpoint as part of the coherent Markdown change.

Do not create consumer mission/workplan/state records for repository development.

## PD1 — Complete Design and persist Plan & Trace before execution

For every executable handoff, ChatGPT completes the controlling Design and creates/updates the exact Task Contract under `docs/tasks/`.

The Task Contract defines at minimum:
- objective/result;
- SDD profile;
- current specification carrier/reference when one exists;
- material requirement/spec delta, including `PRESERVED` invariants where applicable;
- controlling references;
- authorized scope and explicit exclusions;
- complete implementation-relevant Design/architecture/invariants/compatibility/security/privacy/reliability constraints;
- base/topic branch requirements;
- expected executor handoff path;
- acceptance criteria;
- requirement-to-verification/implementation trace sufficient for the work's complexity/risk;
- verification/evidence requirements and intended methods;
- D052 `Test-Authorship-Mode` and required frozen conformance-asset references when test ownership is material;
- stop/escalation/re-entry conditions.

The Design must be complete enough that the Executor does not need to invent material architecture, interfaces, state/data flow, trust boundaries, compatibility/migration, failure behavior or acceptance meaning. It need not prescribe every local code-level choice that cannot change the approved Design.

### Contract integration gate

The Task Contract and any controlling Markdown/Decision Records MUST be integrated into `develop` before executor implementation begins.

When `orchestrator-conformance` or `mixed` requires preimplementation oracle assets, those assets MUST also be integrated into the Executor's starting `develop` baseline before implementation begins.

Normal sequence:

`spec/Design/plan/oracle branch -> PR -> develop (complete contract + required oracle present) -> executor topic branch`

The executor implementation branch MUST be created from a `develop` revision that already contains the exact Task Contract and any required frozen D052 conformance assets it is expected to execute.

This keeps requested semantics, Design, Plan/Trace and acceptance oracle independently auditable before implementation exists.

### Contract freeze and SDD re-entry

Once implementation starts, the original task semantics are not silently rewritten to match implementation.

- The executor never edits the Task Contract.
- Material changes to objective, specification delta, scope, exclusions, Design/invariants, Plan/Trace, acceptance, verification meaning, or semantic oracle meaning require ChatGPT to persist an explicit revision before execution continues.
- ChatGPT may update lifecycle metadata or append explicit review/revision/acceptance notes, provided the original request is not obscured.
- When executor evidence exposes an upstream defect, work stops at the affected claim and re-enters the earliest affected Orchestrator SDD stage before resume.

### D052 oracle freeze

When an Orchestrator-owned oracle is required, its identity/expected meaning is frozen under `docs/CONFORMANCE-ORACLE-CONTRACT.md` before the implementation is allowed to optimize against it.

The Executor may not change expected results, classifications, thresholds, semantic negative-control membership, or acceptance assertion meaning. A suspected semantic defect is reported through the D052 `ORACLE_DEFECT` boundary.

Purely mechanical corrections are allowed only when the Task Contract or durable Orchestrator revision explicitly authorizes that correction class.

## PD2 — Executor checkout/bootstrap readiness

After PD1 is integrated, ChatGPT gives the executor only the canonical minimal launch prompt pointing to the exact Task Contract; current `AGENTS.md` is reloaded explicitly only when the governing integrated change modified it and D043 requires that reload.

The executor MUST:
1. fetch/synchronize the canonical repository/remotes;
2. establish a safe current `develop` baseline containing the Task Contract and required D052 conformance assets;
3. verify the working tree/base identity;
4. create or checkout the Task Contract's topic branch;
5. read only the controlling context required by the contract;
6. include every required frozen Orchestrator conformance asset in its execution/verification path without redefining semantics.

PD2 is an execution prerequisite, not a second SDD Design or Plan stage. The Executor may privately organize its coding/review process under D041, but private plans/SDD/tool state are implementation aids only and do not become repository authority.

Depending on task type and selected authorship mode, the executor may inside its implementation/review authority:
- add/update deterministic implementation/regression tests;
- add/update supplementary agent-facing evals;
- add property/fuzz/edge/adversarial exploration that does not redefine acceptance;
- establish an Executor-owned characterization artifact only when the controlling refactor workflow/contract assigns that technical authorship and Orchestrator acceptance meaning remains fixed;
- identify expected failing implementation tests for intentional new behavior.

Under `orchestrator-conformance`/`mixed`, the Executor does not reconstruct or silently replace a required semantic oracle already frozen by ChatGPT.

Tests/evals verify the approved specification/Design/Plan; they do not redefine it.

## PD3 — Implement

The Agente de IA Ejecutor performs only authorized non-Markdown work outside the narrow D052 Orchestrator-owned conformance exception.

The executor:
- edits implementation/config/assets inside scope;
- authors/updates applicable technical, exploratory, implementation, integration and supplementary test/eval/fixture assets inside its ownership boundary;
- executes required frozen Orchestrator-owned conformance assets when applicable;
- does not edit committed Markdown;
- does not semantically change Orchestrator-owned oracle assets without persisted authorization;
- does not change specification, controlling Design, Plan/Trace, strategic scope or acceptance;
- resolves ordinary local coding/test implementation choices autonomously when they preserve the approved Design;
- blocks/reports rather than invents missing upstream requirement/Design/Plan authority;
- keeps the branch focused on one coherent task.

Markdown-only and D052-designated Orchestrator conformance-authoring changes are performed by ChatGPT under their applicable branch/review gate. Executor implementation begins only after required preimplementation assets are integrated.

## PD4 — Code Review & Verify, persist, commit, and push

After implementation, the Executor owns the native SDD `Code Review & Verify` stage for its technical work.

The executor SHALL review the implementation against the approved specification/Design/Plan for the applicable subset of:
- requirement/spec-delta and `PRESERVED` fidelity;
- Design/task-boundary fidelity;
- correctness, edge cases and failure behavior;
- maintainability and unnecessary complexity;
- represented security/privacy/reliability/compatibility obligations;
- required deterministic/property/integration/eval/conformance evidence;
- unauthorized scope additions.

It MAY correct implementation/test defects found by this review when the correction stays inside approved authority. If review exposes an upstream specification/Design/Plan/acceptance defect, the affected work is `BLOCKED`/`PARTIAL` for Orchestrator re-entry; the Executor does not redesign or reinterpret semantics.

The executor then runs all verification required by the Task Contract, including every applicable frozen Orchestrator-owned conformance asset, and writes/updates the task's handoff under `handoffs/` according to `docs/EXECUTOR-HANDOFFS.md`.

Before returning any `DONE`, `BLOCKED`, or `PARTIAL` status, the executor MUST:
1. make the implementation/Executor-owned test/eval state internally coherent;
2. complete the technical code review and resolve all in-authority findings required for the terminal status;
3. run the required verification, including designated Orchestrator conformance assets;
4. update the persisted executor handoff so it describes the final implementation/review state and requirement-to-evidence mapping;
5. commit all authorized implementation/Executor-owned test/eval/handoff changes on the topic branch;
6. push the topic branch to the canonical remote according to D048 publication timing;
7. ensure the handoff identifies the implementation review anchor/base identity required by `docs/EXECUTOR-HANDOFFS.md`.

The remote topic branch is the review surface. ChatGPT MUST NOT be expected to trust a local-only SHA, copied terminal output, or chat-only claim.

If verification/specification/Design/Plan is blocked, persist a `BLOCKED`/`PARTIAL` handoff, commit/push the auditable terminal state when safe, and stop rather than guessing.

The executor MUST NOT make tests green by weakening the ChatGPT-approved contract or the semantic meaning of a D052-designated oracle.

Executor `DONE` is evidence only; it is not acceptance.

## PD5 — Orchestrator Converge / Accept / re-entry

ChatGPT uses GitHub to review:
- the persisted Task Contract and its revision history;
- current specification carrier and material requirement/spec delta;
- controlling Design and Plan/Trace;
- applicable frozen D052 conformance/oracle identity and revision history;
- the persisted executor handoff at the pushed HEAD;
- the remote base/head relationship;
- every changed file/diff in scope;
- implementation architecture/complexity relative to approved Design;
- Executor code-review evidence/findings;
- test/eval quality and whether required + supplementary tests would detect relevant breakage;
- verification evidence and requirement-to-evidence coverage;
- dependencies/configuration/security implications;
- ownership and branch-policy compliance.

Before acceptance, ChatGPT establishes native SDD convergence:

- `completeness` — every required change has implementation and evidence;
- `correctness` — evidence actually proves the specified outcome;
- `coherence` — specification, Design, Plan, implementation and evidence do not materially contradict;
- `containment` — no material unauthorized behavior/scope was added;
- `persistence` — accepted current-spec state and resulting product state will agree after integration.

Green tests are necessary where applicable but are not sufficient for acceptance.

When review changes the durable frontier — accepted, blocked, rework/re-entry requested, or a new controlling issue is discovered — refresh the Orchestrator checkpoint so another ChatGPT chat can resume the review loop from Git alone.

### Rework / re-entry loop

If technical rework is required:
- if specification/Design/Plan/oracle semantics are unchanged, ChatGPT persists any durable review directive needed for the executor to act without relying on chat history;
- if objective/specification/Design/scope/acceptance/verification/oracle meaning changes materially, ChatGPT re-enters the earliest affected SDD stage and persists an explicit Task Contract/oracle/Design revision before execution continues;
- the executor pulls the durable update, performs rework on the same represented task branch, reruns Code Review & Verify, updates the handoff, commits, pushes, and returns the minimal pointer again.

The loop repeats until accepted or cancelled/blocked by Human Owner/ChatGPT.

### Acceptance preparation

When ChatGPT accepts the implementation, ChatGPT may update Task Contract lifecycle/acceptance metadata without rewriting the original execution semantics. Acceptance also determines how the accepted delta will evolve the current specification carrier after integration.

## PD6 — Integrate & Evolve

After PD5 acceptance:
1. ChatGPT normally creates the implementation PR from the pushed topic branch to `develop`;
2. the PR description identifies the Task Contract, relevant specification/Design/Plan carrier and executor handoff;
3. any available required checks/reviews must pass;
4. ChatGPT performs the final PR review against the accepted branch state;
5. prefer squash merge for one coherent normal topic change unless branch policy/represented history requires another method;
6. merge/integrate into `develop`;
7. fold the accepted delta into the living current specification carrier when a dedicated carrier exists, or recognize the accepted changed normative artifact itself as the new current specification state;
8. preserve historical task/change/review evidence without duplicating living truth;
9. delete/retire the topic branch when appropriate under applicable cleanup policy.

The executor does not normally create or merge the implementation PR unless the Task Contract explicitly delegates that mechanical action.

Merging to `develop` means accepted into the next unreleased state. It does not mean released.

Promotion `develop` -> `main` is a separate action governed by `docs/BRANCHING.md` and `docs/RELEASES.md`.

Before intentionally closing the ChatGPT chat after integration, ensure `docs/orchestrator/CHECKPOINT.md` already describes a safe next frontier from which a fresh chat can resume.

## Handoff invariants

- ChatGPT -> repository: persist specification/Design/Plan/Trace, decisions/contracts and required D052 conformance/oracle assets before executable handoff.
- Repository -> executor: Task Contract, controlling references and applicable frozen conformance assets are the complete source of task/specification/Design/Plan/acceptance semantics.
- ChatGPT -> executor: launch prompt is only a minimal pointer/bootstrap transport.
- Executor -> repository: implementation + Executor-owned tests/evals + Code Review & Verify evidence + persisted handoff are committed/pushed as authorized before status is returned.
- Executor -> ChatGPT: visible response contains only status, handoff path, branch, and pushed HEAD.
- Executor -> Orchestrator oracle: execute as required; do not semantically weaken; report `ORACLE_DEFECT` evidence when meaning appears wrong.
- Executor -> upstream SDD: report spec/Design/Plan defects; do not silently repair them by assuming Orchestrator stage ownership.
- ChatGPT -> executor rework: durable review directive or re-entered contract/Design/oracle revision first when needed.
- ChatGPT -> PR/integration: only after remote convergence acceptance.
- ChatGPT -> current specification: evolve accepted living truth after integration without erasing historical deltas/evidence.
- ChatGPT -> next ChatGPT chat: `docs/orchestrator/CHECKPOINT.md` plus Git remote state are the source of continuity; prior chat history is optional.
- ChatGPT -> Human Owner: escalate scope/risk/public compatibility/release decisions when final authority is required.

No named executor product is privileged. Switching OpenCode -> Codex -> Claude Code -> another compatible executor does not change this procedure. Switching ChatGPT conversations does not change authority or require reconstructing source state from chat.

## Engineering rationale

This workflow intentionally uses native spec-anchored/delta-first SDD, single-owner stages, small coherent changes, tests coupled to behavior changes, separate refactoring, durable change rationale, bidirectional traceability, executor technical Code Review & Verify, Orchestrator convergence before integration, specification-owned conformance when semantically appropriate, and compact cold-start checkpoints rather than ever-growing conversation context. These principles are consistent with D022, D027, D041, D052 and accepted D053.
