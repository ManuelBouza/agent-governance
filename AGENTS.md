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

### D076 Stage 6 ephemeral executable materialization boundary

D076 prospectively closes the tracked/untracked loophole at the D068 Stage 5/Stage 6 boundary.

For D068-mode work, persistence status is **not** an ownership classifier. `ephemeral`, `temporary`, `untracked`, `outside the worktree`, `deleted before commit`, or `not part of the final diff` do not make substantial executable material Executor-owned.

The effective rule is:

```text
small mechanical execution aid
    -> Executor Stage 6 may create/use it

substantial new controller/harness/script/fixture-oracle implementation
    -> STOP
    -> Orchestrator re-entry
    -> ChatGPT Stage 5 materialization
    -> publish coherent candidate
    -> Executor Stage 6 execute/diagnose/repair/verify
```

No rigid LOC threshold controls this classification. Materiality depends on semantic function, orchestration responsibility, control/state flow, task-specific logic, risk and whether the artifact implements behavior that should have existed in the complete Stage 5 candidate.

D076 preserves D054 command/API/SDK/shell mechanics and D068 bounded repair of an already-published candidate. It forbids using private-process autonomy as authority for first-pass substantial executable materialization merely because the artifact is temporary.

Any file-based executable artifact created by the Executor during Stage 6 and actually executed or used to influence verification, when not already part of the published/authorized candidate, must be classified in the persisted handoff under D076. Material or uncertain late-discovered artifacts require re-entry rather than silent deletion/continuation.

Any later unqualified wording in this file assigning broad Executor "technical harness work", private tooling or implementation aids is subject to D076. `docs/decisions/D076-stage6-ephemeral-executable-materialization-boundary.md` controls the full rule.

### D077 version-sensitive upstream revalidation

D077 controls consequential research, design, evaluation and launch decisions that materially depend on external version-specific behavior.

Before relying on a pinned runtime/library/provider behavior, ChatGPT Orchestrator must inspect the pinned/reference version, the current stable upstream release, and higher relevant releases needed to determine whether the material behavior changed. Relevant higher prereleases must also be inspected when a blocker remains unresolved and the prerelease plausibly touches that surface.

Do not preserve an old workaround merely because the project was already pinned if a newer supported release fixes the material blocker. Conversely, do not upgrade merely because a newer version exists when the qualified pin remains necessary and the newer version does not solve the problem.

The explicit dispositions are `PIN_RETAINED`, `UPGRADE_REQUIRED`, `REQUALIFICATION_REQUIRED`, or `NO_MATERIAL_CHANGE` (or semantically equivalent unambiguous wording). A materially new stable release appearing between review and consequential launch requires relevance classification before execution.

D077 does not auto-extend D063 qualification to later Codex versions and does not make prereleases production/experiment authority. `docs/decisions/D077-version-sensitive-upstream-revalidation.md` controls the full rule.

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
