# Agent Governance Product Repository

## Repository role

This repository develops, refactors, tests, evaluates, and releases the reusable Agent Governance product. It is NOT an installed consumer-project instance.

Only product artifacts belong here:
- canonical governance instructions/protocol structure;
- consumer Governance Skill and source-product Maintainer Skill;
- supporting implementation code/configuration/assets;
- product-development instructions and decisions;
- deterministic tests and agent-facing evals;
- minimal synthetic fixtures required by those tests/evals.

Real project missions, application task plans, consumer STATE/EXCHANGE history, production credentials, and application implementation MUST live in separate consumer repositories.

Do not create a live `.agent-governance/` / `.agent-coordination/` consumer footprint in this repository. Synthetic installed footprints are allowed only inside disposable test/eval fixtures.

## Canonical product paths

- Canonical protocol source: `governance-core/`.
- Native consumer SDD semantics: `governance-core/SDD.md`.
- Consumer Governance Skill: `governance-skill/` when release gates permit it.
- Source-product Maintainer Skill: `maintainer-skill/` when its own gate permits it.
- Consumer Skill design: `docs/GOVERNANCE-SKILL-CONTRACT.md` and `docs/GOVERNANCE-SKILL-PACKAGE.md`.
- Maintainer Skill design: `docs/MAINTAINER-SKILL-CONTRACT.md`.
- Testing/evaluation strategy: `docs/TESTING-AND-EVALUATION.md`.
- Testing Skill/capability policy: `docs/TESTING-SKILL-CAPABILITIES.md`.
- Source local toolchain: `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`.
- Source-product Task Contract policy: `docs/TASK-CONTRACTS.md`.
- Executor handoff policy: `docs/EXECUTOR-HANDOFFS.md`.
- Executor launch-profile guidance: `docs/EXECUTOR-LAUNCH-PROFILES.md`.
- Executor coordinator/worktree hygiene: `docs/decisions/D058-executor-coordinator-session-and-worktree-hygiene.md` and `docs/EXECUTOR-SESSION-WORKTREE-HYGIENE.md`.
- ChatGPT Orchestrator checkpoint policy: `docs/ORCHESTRATOR-CHECKPOINTS.md`.
- Current ChatGPT Orchestrator checkpoint: `docs/orchestrator/CHECKPOINT.md`.
- Research-to-decision traceability: `docs/decisions/D057-research-decision-traceability.md` and `docs/RESEARCH-TRACEABILITY.md`.
- Executable source-maintenance task records: `docs/tasks/`.
- Persisted executor handoffs: `handoffs/`.
- Product decisions and operating instructions: `docs/`.
- Deterministic product tests: `tests/`.
- Agent-facing product evals: `evals/`.

The consumer and maintainer Skills have separate activation/triggers and operational contexts. The consumer Skill MUST NOT depend on modifying or reading this source repository after installation.

## Agent operating model

Repository development uses two agent roles plus the Human Owner. Agent-product names are adapters, never governance roles.

### D053 native SDD stage ownership

D053 is accepted and controls Spec-Driven Development responsibility for this source product and governed consumer projects.

The native D053 stage map is:

```text
1 Explore / Frame           -> ChatGPT Orchestrator
2 Specify                   -> ChatGPT Orchestrator
3 Design                    -> ChatGPT Orchestrator
4 Plan & Trace              -> ChatGPT Orchestrator
5 Implement                 -> Agente de IA Ejecutor for authorized technical implementation
6 Code Review & Verify      -> Agente de IA Ejecutor for that technical implementation
7 Converge/Accept/Evolve    -> ChatGPT Orchestrator
```

No SDD stage is dual-owned. ChatGPT must hand off a complete controlling specification, Design and Plan/Trace boundary before executable work starts. Executor-local coding choices remain implementation details only while they preserve that approved Design. A material requirement/design/plan defect discovered during implementation or technical review is a stop/re-entry condition, not authority for the executor to redesign the task.

Native SDD is `spec-anchored`, brownfield `delta-first`, tool-neutral and proportionate through `COMPACT`, `STANDARD` and `ASSURED` profiles. `ADDED / MODIFIED / REMOVED / PRESERVED` express material requirement deltas. `docs/decisions/D053-native-spec-driven-development.md`, `docs/SDD-ADOPTION-PLAN.md` and the applicable source workflow define source-product application; `governance-core/SDD.md` carries the reusable consumer semantics.

### D068 source-maintenance stage refinement

D068 prospectively refines the D053 Stage 5/6 boundary for source-product maintenance objectives operating in D068 mode. It does not change Governance Core or consumer-project SDD semantics.

The effective D068 source-maintenance stage map is:

```text
1 Explore / Frame                 -> ChatGPT Orchestrator
2 Specify                         -> ChatGPT Orchestrator
3 Design                          -> ChatGPT Orchestrator
4 Plan & Trace                    -> ChatGPT Orchestrator
5 Candidate Materialize           -> ChatGPT Orchestrator
6 Execute / Diagnose / Repair /
  Verify                          -> Agente de IA Ejecutor
7 Converge / Accept / Integrate /
  Evolve                          -> ChatGPT Orchestrator
```

For D068-mode work, ChatGPT owns complete candidate materialization, including in-scope source code, tests, configuration, schemas, fixtures, scripts and documentation. Before Stage 6, ChatGPT publishes the complete coherent candidate plus its controlling Task Contract/Plan, applicable specification/Decision deltas and required D052 semantic conformance assets to the verified topic branch on GitHub.

That coherent published topic-branch checkpoint is sufficient authority for Executor verification. D068-mode work does **not** require a separate planning/candidate merge into `develop` before Stage 6. The topic branch must still satisfy D061/D062 protection/freshness rules and have an auditable current protected-base relationship.

During Stage 6, the Executor owns actual execution, diagnosis, bounded technical repair and verification under D054 mechanics. Repairs are allowed only when they preserve the approved semantics and Design; material requirement/Design/Plan/acceptance defects require Orchestrator re-entry. D065 delegation obligations remain intact, and D060 coordinator continuity remains intact.

D052 semantic-oracle ownership remains intact. D066 unresolved gaps remain unresolved, including orphan recovery, TTL/heartbeat, ownership transfer, closed-unmerged resume, automatic retirement / GC selection, unusual-ref canonicalization, and unqualified ruleset behavior.

D068 is prospective. Historical executed Task Contracts, handoffs, reviews and evidence keep the authority and meaning they had when executed. Any later unqualified wording in this file that assigns first-pass D068 Stage 5 implementation to the Executor, requires a separate pre-verification merge into `develop`, or assigns all non-Markdown D068 candidate materialization to the Executor is subject to this D068 refinement and retains only explicit historical/grandfathered or non-D068 scope.

### D052 test-authorship override

D052 prospectively refines semantic test/eval ownership. When the controlling Task Contract/gate selects `orchestrator-conformance` or `mixed`, ChatGPT Orchestrator owns the narrowly designated conformance/oracle assets that directly encode ChatGPT-owned acceptance semantics; the Agente de IA Ejecutor owns Stage 6 execution, technical harness work and authorized supplementary technical testing/repair. Under D068, ChatGPT may also materialize candidate implementation/regression/integration tests during Stage 5 without transferring semantic-oracle authority. Semantic changes to an Orchestrator-owned oracle require persisted ChatGPT authority. Existing T032/T021 work is grandfathered and T022 may complete under its existing contract; MG1/T023 remains governed by its persisted authority unless prospectively revised.

Where later sections of this file discuss non-Markdown tests/evals, read that wording subject to D052 semantic-oracle ownership and the D068 Stage 5/6 source-maintenance refinement.

### Human Owner

Final authority over product scope, priorities, risk, public distribution, releases, and overrides.

### ChatGPT — Orchestrator and Markdown Owner

ChatGPT owns product strategy, research synthesis, normative specification/spec deltas, complete controlling Design/architecture, work decomposition and Plan/Trace semantics, acceptance criteria, Task Contracts, agent handoffs, semantic convergence/acceptance, current-spec evolution, remote review, source-maintenance checkpointing, and all committed Markdown (`*.md`) authoring/editing.

Only ChatGPT may create, rewrite, or persist Markdown instruction/design/decision/task/checkpoint files in normal agentic development. This includes `AGENTS.md`, `README.md`, `docs/**/*.md`, `governance-core/*.md`, Skill Markdown, and Markdown files inside test/eval fixtures.

For D068-mode source maintenance, ChatGPT also owns complete Stage 5 candidate materialization across in-scope non-Markdown artifacts. This does not transfer D054 execution mechanics or Stage 6 technical verification authority to ChatGPT.

A fresh ChatGPT conversation MUST be able to resume source-product orchestration from the canonical Git repository without requiring prior chat history. D027 and `docs/ORCHESTRATOR-CHECKPOINTS.md` define that cold-start/chat-turnover contract.

### Agente de IA Ejecutor — product agnostic

The executor is an abstract role that MAY be fulfilled by OpenCode, Codex, Claude Code, Antigravity, or another compatible local/coding agent. Product identity does not change task semantics, authority, or acceptance.

For D068-mode work, the Agente de IA Ejecutor owns Stage 6 execution, diagnosis, bounded technical repair, technical Code Review & Verify and verification evidence for the complete published candidate, including as authorized:
- execution of product implementation code/configuration/assets;
- execution and technical diagnosis of deterministic implementation/test code and fixtures;
- execution and technical diagnosis of agent-facing implementation/eval code/data/fixtures;
- technical code review against the approved specification/Design/Plan;
- collection of verification evidence;
- correction of implementation/test/config defects that remain inside approved semantics/Design;
- persisted non-Markdown executor handoffs under `handoffs/`;
- in-scope technical repair/refactoring during Stage 6.

Explicit historical/grandfathered or non-D068 work may retain first-pass implementation ownership exactly where its persisted authority says so. That earlier topology is not the default for new D068-mode source maintenance.

Within its authorized Stage 6 Task Contract boundary, the executor owns its **execution and technical repair process**. It may independently choose and compose direct work, private/internal planning, private SDD/specification workflows, sub-agents/workers, Skills, code-graph/navigation tools, testing/review helpers, or other compatible executor-native capabilities. Those mechanisms are implementation aids only. Agent Governance does not prescribe executor-specific methodology, topology or tool routing unless a method itself is material to an accepted safety/security/reproducibility/ownership invariant. D041 defines this process-autonomy boundary; D053/D068 prevent that autonomy from becoming authoritative Explore/Specify/Design/Plan/Acceptance state.

Executor-internal plans, worker results, SDD state, Skill output, graph state or host-native approvals are implementation aids/evidence only. They do not become Task Contract authority, controlling Design, or Agent Governance acceptance, and they must not create tracked repository state or external lifecycle authority outside authorized scope.

### D054 execution-mechanics ownership

D054 prospectively makes the command/API interaction boundary explicit for delegated executable work.

Inside authorized Executor work, including D068 Stage 6, the Agente de IA Ejecutor owns Execution Adapter mechanics: CLI/API/SDK invocation, Git/uv command selection, PowerShell/Bash/shell syntax, cloud/database/cluster/deployment tooling, SSH/remote-management operations and equivalent technical execution details.

ChatGPT/Human authority remains semantic: requested outcome, controlling Design/Plan, actual target/effect/resource/privilege/credential/network envelope, required semantic runbook/checkpoints, approval/Human gates and acceptance evidence. The Human Owner MUST NOT become the default copy/paste terminal operator merely because a command is needed. Human interaction is reserved for D033 `REQUIRE_HUMAN` gates, MFA/external approvals that cannot be delegated, material credential/risk decisions, or an explicit request to inspect/execute exact syntax.

For each adapter operation the Executor follows D054's runbook-first resolution rule: reuse a compatible VERIFIED operation recipe when one exists; otherwise resolve the operation from project-native or installed/version-specific help and official vendor/API documentation, execute only inside the current D033 envelope, verify the required postcondition, and promote reusable syntax only through the approved recipe lifecycle. Model memory, community examples or chat snippets are never sufficient sole authority for a newly learned executable recipe.

Until T035 native recipe persistence is integrated, the same ownership/documentation rule applies but newly resolved operations remain provisional handoff evidence rather than pretending a reusable native recipe store already exists.

This D054 rule governs Executor-side technical execution. It does not transfer ChatGPT-owned candidate semantics, Markdown mutation or D068 Stage 5 materialization to the Executor; Orchestrator repository writes remain subject to the branching policy and the L007 fail-closed branch-target control.

### D055 executor launch profile

D055 governs the Human-facing configuration chosen before ChatGPT hands a prompt to a concrete Agente de IA Ejecutor.

Before every Executor prompt, ChatGPT MUST state the active concrete Executor, whether the Human should start a `NEW` session or `CONTINUE` the existing one, the recommended currently available model, the recommended reasoning effort, and one concise rationale. The active Executor adapter must be known before these settings are recommended; the current checkpoint should record it when one is selected.

The default is `NEW` for the first launch of a new Task Contract/work unit and `CONTINUE` for clean same-task/same-branch follow-up or persisted rework. Fresh-context/independence requirements, executor/checkout changes, stale or contaminated context, or inability to reload newly controlling repository instructions require `NEW`.

Model/effort selection uses the minimum sufficient compute for the remaining technical implementation/review risk: `MEDIUM` is the normal center of gravity, `LOW` is deliberate for mechanically bounded work, and `HIGH` is selective for concrete technical complexity. Highest host modes are exceptional. Increased reasoning MUST NOT substitute for missing specification/Design/Plan authority.

The launch profile is separate from the Task Contract and normally separate from the transport prompt. Provider-specific mappings live in `docs/EXECUTOR-LAUNCH-PROFILES.md`; model names never become repository correctness semantics.

### D058 coordinator session/worktree hygiene

D058 governs Human-visible coordinator naming and local workspace isolation/closure for Executor work.

- For a `NEW` launch on a named-session-capable host, ChatGPT MUST provide a deterministic `Coordinator-Chat`; current Codex convention is `AG | <repo> | <work-unit> | root-<n>`.
- Same-work-unit `CONTINUE` keeps the same coordinator identity; a forced new root for the same work unit increments the ordinal.
- Coordinator names are navigation metadata only; Git, persisted contracts, branches, handoffs and reviews remain authority.
- Each concurrently writable work unit MUST have an exclusive writable worktree/topic branch; two writable coordinators MUST NOT share a worktree or branch.
- Prelaunch local topology must be safe enough to rule out workspace collision without discarding unrepresented work.
- Post-integration closure includes evidence-safe retirement of obsolete task worktrees/local branches and restoration of the designated primary checkout to a clean current long-lived baseline, normally local `develop == origin/develop` for source maintenance.
- Ambiguous/unique local work is preserved and classified for review; destructive reset/clean/delete is not a hygiene mechanism.
- `docs/EXECUTOR-SESSION-WORKTREE-HYGIENE.md` defines the operating procedure.

The executor MUST NOT:
- create or edit committed `*.md` files;
- change product scope, normative requirements/spec deltas, controlling Design/architecture, Plan/Trace semantics, acceptance criteria, or strategic intent;
- invent missing upstream specification/design/plan authority instead of stopping for re-entry;
- weaken or reinterpret tests/evals in a way that contradicts the ChatGPT-approved contract;
- semantically change a D052-designated Orchestrator-owned conformance/oracle asset without persisted ChatGPT authorization;
- alter an accepted refactor characterization baseline after structural mutation begins unless ChatGPT explicitly authorizes a correction;
- claim acceptance authority merely because implementation review/tests are green;
- treat local-only/unpushed state as a completed normal handoff.

The executor MAY inspect all Markdown and existing tests/evals as read-only specification/context.

## Source-change procedure invariant

D022, D053, D068, `docs/DEVELOPMENT-WORKFLOW.md`, and `docs/REFACTORING-WORKFLOW.md` define how this source product is changed.

This repository does not install its consumer F0–F6 lifecycle to govern itself.

### Markdown-only changes

ChatGPT performs committed Markdown-only work on a short-lived topic branch from `develop`, reviews the resulting diff, and returns the change to `develop` through PR. D053/D068 still apply proportionately: ChatGPT performs the applicable Explore/Specify/Design/Plan/Trace reasoning and final convergence for Orchestrator-owned Markdown artifacts without introducing an Executor merely for ceremony.

### Executable changes

For D068-mode source maintenance, executable work uses this contract-first, SDD-anchored sequence:

1. ChatGPT completes/persists Explore, Specify, Design and Plan & Trace authority in the Task Contract/controlling Markdown and, where D052 requires it, the semantic conformance/oracle assets.
2. ChatGPT completes Stage 5 materialization of the full candidate on a verified short-lived topic branch based on current protected `develop`.
3. ChatGPT publishes one coherent topic-branch checkpoint containing the controlling authority, candidate implementation/tests/config/fixtures and required D052 semantic conformance assets. No separate planning/candidate merge into `develop` is required first.
4. The Executor checks out that exact published topic-branch candidate and performs Stage 6 execution, diagnosis, bounded technical repair and Code Review & Verify under the approved Design/Plan boundary and D054 mechanics; it persists its handoff, commits authorized Stage 6 changes, and pushes the topic branch.
5. The Executor returns only status, handoff path, branch, and pushed HEAD.
6. ChatGPT performs Stage 7 Converge/Accept review of the remote Task Contract, candidate/final repaired state, handoff, base/head identities, complete diff, evidence and current-spec implications through GitHub.
7. Rework/re-entry uses durable Git/contract/review history rather than chat-only requirements; material semantic/Design/Plan/acceptance changes require Orchestrator re-entry.
8. Only after ChatGPT acceptance does the candidate proceed through PR to `develop`, followed by accepted current-spec evolution when applicable.

Explicit historical/grandfathered or non-D068 work retains any earlier persisted sequence, including a planning/conformance merge into `develop` before first-pass Executor implementation. Do not silently migrate historical contracts or evidence.

The Executor does not normally open or merge the implementation PR unless the Task Contract explicitly delegates that mechanical action.

## Persisted task/handoff invariant

- `docs/TASK-CONTRACTS.md` defines the Task Contract format/lifecycle, including D053 SDD profile/spec-carrier/delta/trace semantics and the D068 Stage 5/6 publication boundary for new D068-mode source maintenance.
- `docs/EXECUTOR-HANDOFFS.md` defines Executor return evidence, including Stage 6 Code Review & Verify evidence needed for Orchestrator convergence.
- Chat/terminal prompts are transport only and SHOULD contain only repository/candidate identity plus the exact Task Contract path.
- The Executor MUST NOT infer missing task semantics from prior chat history.
- If a prompt conflicts with the persisted Task Contract/published candidate authority, the persisted Git authority controls unless ChatGPT/Human Owner persists an explicit revision/supersession.
- Material objective/scope/specification/Design/Plan/acceptance/verification changes, including semantic D052 oracle changes, require a persisted Task Contract/review revision before execution continues.
- Before `DONE`, `BLOCKED`, or `PARTIAL`, the Executor MUST persist, commit, and push the handoff/current task branch state.

A reviewer must be able to reconstruct what was requested, what candidate was published, what the Executor reported, what Stage 6 review/evidence exists, and what actually changed from the canonical Git remote alone. The Executor's private/internal orchestration trace is not required for this reconstruction unless a Task Contract explicitly makes a particular process artifact part of the deliverable or evidence.

## Orchestrator chat continuity invariant

D027 and `docs/ORCHESTRATOR-CHECKPOINTS.md` define how ChatGPT source-maintenance sessions survive chat turnover.

- `docs/orchestrator/CHECKPOINT.md` is the single current ChatGPT Orchestrator frontier/checkpoint for this source repository.
- a fresh ChatGPT chat starts from current `develop`, then reads `AGENTS.md` plus that checkpoint before loading deeper context;
- the checkpoint references controlling decisions, Task Contracts, handoffs, branches, PRs, blockers, and the next permitted action instead of duplicating their content;
- private prior chat history is never a required authority or execution dependency;
- ChatGPT refreshes the checkpoint when the durable frontier changes materially and before intentionally recommending chat closure;
- ChatGPT recommends a new chat only when all material context is already persisted remotely and the checkpoint is sufficient for cold-start reconstruction;
- the checkpoint is source-maintenance state only and MUST NOT create or substitute a consumer `.agent-coordination/` instance.

When chat closure is recommended, the minimal next-chat prompt should point only to the repository, `AGENTS.md`, and `docs/orchestrator/CHECKPOINT.md`.

## Research traceability invariant

D057 and `docs/RESEARCH-TRACEABILITY.md` define how material Orchestrator research survives iteration and how it may become normative authority.

- every material research effort that can influence product design, policy, evaluation method, Executor configuration or future implementation MUST be persisted in Git before downstream reliance;
- every new research artifact receives a stable `Rxxx` identity plus independent `Research-State` and `Decision-State` metadata;
- `docs/RESEARCH-TRACEABILITY.md` is the complete research ledger and records evaluation/outcome/decision references;
- a complete research memo is evidence, not policy: only an explicit accepted normative artifact plus a registry transition to `DECIDED` can promote its conclusion to decision authority;
- `EVALUATING`, `DEFERRED`, `REJECTED` and `SUPERSEDED` dispositions remain durable so later chats do not rediscover or silently reinterpret prior work;
- completed research MUST NOT be silently rewritten to match later conclusions; use successor/supersession lineage while preserving Git history;
- volatile vendor/model/pricing/regulatory facts MUST be refreshed before a later decision materially relies on them;
- the current checkpoint carries only live research frontier items, while the registry retains the full historical ledger.

Chat turnover, prompt repetition or Executor session changes never alter research/decision state; only persisted Git changes do.

## Testing Skill/capability invariant

D024, D052 and `docs/TESTING-SKILL-CAPABILITIES.md` define the source-product testing Skill boundary.

- the test/eval suite is executable repository code and MUST NOT require model-driven Agent Skill activation;
- test authorship/semantic ownership may be `orchestrator-conformance`, `executor-implementation`, or `mixed` under D052 when ownership is material, subject to D068 Stage 5 candidate materialization for D068-mode source maintenance;
- the Maintainer Skill, when available, is the only project-owned top-level Skill for source test/eval maintenance;
- it routes progressively to deterministic, property/state-machine, Skill/eval, or security/supply-chain context rather than spawning generic overlapping pytest/testing/TDD Skills;
- a cold D068 Executor can bootstrap from the exact published topic-branch candidate, `AGENTS.md`, its persisted Task Contract, controlling references, applicable conformance assets, and approved tooling before the Maintainer Skill exists;
- external testing/authoring/security Skills are optional supplemental aids only after applicable supply-chain/coexistence approval and never replace repository-owned verification;
- the Consumer Governance Skill MUST NOT activate for source-product test/eval maintenance.

These rules constrain source-product capability authority and dependencies, not the Executor's private choice of compatible internal workers/tools used to execute, diagnose, technically repair and verify an authorized Task Contract.

## Local development toolchain invariant

D025 and `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md` define the source-maintainer toolchain.

- Git is the canonical branch/commit/push mechanism.
- uv is the canonical Python/version/environment/dependency/lock runner for repository-owned test/eval development.
- after the executable harness exists, canonical verification runs in the locked environment using `uv run --locked`.
- repository Python quality checks use Ruff; Ruff configuration MUST exclude committed Markdown so executor tooling cannot rewrite ChatGPT-owned `.md` files.
- the project-local `.venv` is disposable and unversioned; dependency truth lives in `pyproject.toml` plus committed `uv.lock`.
- GitHub CLI is a recommended workstation helper, not a harness dependency when Git authentication already works.
- OpenCode/Codex/Claude Code/another executor host is not a source dependency and must not be encoded into correctness semantics.
- this source-maintainer toolchain MUST NOT be copied automatically into consumer repositories; consumer projects retain/reuse their native toolchains unless a governed task explicitly authorizes a missing tool.

## File ownership invariant

Normal agentic write ownership for current source maintenance is:

- committed `*.md` -> ChatGPT Orchestrator
- D052-designated semantic conformance/oracle assets -> ChatGPT Orchestrator
- D068 Stage 5 in-scope candidate implementation/test/eval/config/assets -> ChatGPT Orchestrator when D068 mode applies
- D068 Stage 6 bounded technical repair/test/eval/evidence/handoff changes -> Agente de IA Ejecutor within the persisted repair/verification envelope
- explicit historical/grandfathered or non-D068 work -> ownership recorded by its persisted controlling authority

`LICENSE` and repository control files may be additionally protected by product-specific adapters. When a file category genuinely crosses responsibilities, ChatGPT defines the exception explicitly before mutation.

No named executor product gains special authority. Product-specific adapter configuration may enforce these rules mechanically but MUST NOT redefine them.

## Branching invariant

`docs/BRANCHING.md` is authoritative for source-repository branch operation.

- `main` is stable/default and is not a normal development target.
- `develop` integrates the next unreleased state.
- normal work starts on a short-lived topic branch from `develop` and returns to `develop` through PR.
- direct development writes to `main` or `develop` are prohibited.
- normal topic branches MUST NOT target `main`.
- release promotion uses `develop` -> `main`; optional `release/*` and exceptional `hotfix/*` follow the branching policy.
- branch names describe product work, never agent identity.
Neither ChatGPT nor an Agente de IA Ejecutor may bypass this policy because of role or product identity.

## Product boundaries

- Keep the Governance Core agent-product neutral.
- Keep consumer mission/task/state out of this repository except minimal synthetic fixtures under tests/evals.
- Both Skills are operational tooling, never authority over the Core.
- Do not author final Skill packages until their documented release gates are satisfied.
- Tests/evals validate Governance/Skill behavior, not application-task implementation quality.
- `docs/TESTING-AND-EVALUATION.md` is normative for verification architecture, isolation, fixtures, grader selection, thresholds, and external technical references; D052 controls semantic authorship ownership where applicable and D068 controls source-maintenance candidate/verification stage ownership.
- External Skill research follows `governance-core/SKILL-DISCOVERY.md` and `governance-core/SKILL-SUPPLY-CHAIN.md`.

## Change discipline

Prefer one coherent, independently reviewable change at a time. Separate behavior-preserving refactors from feature/protocol behavior changes, bug fixes, dependency upgrades, and unrelated cleanup.

For refactors, material preserved behavior is expressed as `PRESERVED` specification/invariants and remains Orchestrator-owned acceptance meaning. Applicable characterization-baseline gates follow `docs/REFACTORING-WORKFLOW.md`; D068 does not retroactively rewrite historical RF1 evidence.

When changing protocol behavior in D068 mode, ChatGPT updates the smallest relevant Core Markdown module and applicable decisions/design/specification documentation, preserves D052 semantic-oracle ownership, and materializes the complete candidate implementation/tests during Stage 5. The Agente de IA Ejecutor then performs Stage 6 execution, diagnosis, bounded technical repair and verification, and supplies evidence. ChatGPT performs Stage 7 convergence/acceptance/integration/evolution.

Preserve progressive context loading and avoid duplicating normative rules.
