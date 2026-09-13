# R029-S1 — Root Preservation Map

Status: COMPLETE  
Parent: `R029 — AGENTS.md / Skill Architecture Refactor Research`  
Subtask: `R029-S1 — Root preservation-map audit`  
Baseline-Develop: `8113b9d0963e4d9ddfa10e5b7c5bf9cc66348eec`  
Audited-AGENTS-Blob: `dd2e2d814aee8f682bde54f6d5d0d462d7e1de87`  
Decision-State: EVALUATING  
Normative-Effect: none

## Purpose

This artifact closes R029-S1 by converting the coarse R029 inventory into an atomic preservation map. Every material semantic unit of the current root `AGENTS.md` is assigned exactly one preservation classification and one intended destination class. The map is analytical only: it does not authorize a root rewrite, Skill topology decision, Skill implementation, Executor launch, or provider/model evaluation.

The current `AGENTS.md` blob is unchanged from the R029 research baseline. A compare from the R029 baseline commit `35367824dd22b714bc07ce873656856788d85519` to the S1 bootstrap `develop` shows no `AGENTS.md` change. Therefore this audit consumes the same source semantics R029 inventoried, but splits mixed rows so no atomic unit has two classifications.

## Classification vocabulary

- `ROOT_INVARIANT` — authority/safety/identity that must remain available before optional routing.
- `ROOT_TRIGGER_DOMAIN` — concise root trigger/invariant remains always loaded; detailed workflow routes to the Agent Governance Maintainer/domain material.
- `ROOT_TRIGGER_TRANSVERSE` — concise root trigger/invariant remains always loaded; reusable workflow is a transverse-Skill candidate for later evaluation.
- `DOMAIN_ROUTE` — Agent-Governance-specific detail can be progressively disclosed through Maintainer/domain references without an independent root rule beyond its controlling trigger.
- `REFERENCE_DETERMINISTIC` — procedural/mechanical detail belongs in narrow references, scripts, CI, or host/tool-specific adapters rather than repeated root prose.

`ROOT_TRIGGER_DOMAIN` and `ROOT_TRIGGER_TRANSVERSE` are single classifications here: each means one concise always-on trigger plus one routed destination class. They are not two independent destinations for the same atomic semantic unit.

## Atomic preservation map

| ID | Current root semantic unit | Classification | Preservation destination |
| --- | --- | --- | --- |
| S1-001 | Repository is the reusable Agent Governance source product, not a consumer installation | `ROOT_INVARIANT` | Root identity/scope invariant |
| S1-002 | Only source-product artifacts belong here; real consumer missions/state/credentials/application implementation do not | `ROOT_INVARIANT` | Root source-vs-consumer boundary |
| S1-003 | Live `.agent-governance/` / `.agent-coordination/` consumer footprints are forbidden except disposable synthetic fixtures | `ROOT_INVARIANT` | Root contamination/safety invariant |
| S1-004 | Bootstrap-critical canonical locations exist for Core, Skills, task contracts, handoffs, checkpoint, research, tasks, tests and evals | `ROOT_TRIGGER_DOMAIN` | Concise root bootstrap pointers; full path catalog to Maintainer/domain reference |
| S1-005 | Consumer and Maintainer Skills have separate activation contexts; consumer Skill must not depend on this source repo after installation | `ROOT_INVARIANT` | Root product/installation boundary |
| S1-006 | Repository governance roles are Human Owner, ChatGPT Orchestrator and product-agnostic Executor; host product names are adapters | `ROOT_INVARIANT` | Root authority model |
| S1-007 | D053 SDD stages have single ownership; Explore–Plan and Converge are Orchestrator-owned, authorized implementation/review are Executor-owned in native mode | `ROOT_TRIGGER_DOMAIN` | Concise root stage-ownership rule; detailed D053 profile/delta semantics to domain route |
| S1-008 | Missing/material requirement, design or plan defects discovered during implementation require stop/re-entry rather than Executor redesign | `ROOT_INVARIANT` | Root authority/stop invariant |
| S1-009 | D053 profile mechanics (`COMPACT`/`STANDARD`/`ASSURED`, delta vocabulary, source/consumer references) | `DOMAIN_ROUTE` | Maintainer/domain SDD reference |
| S1-010 | In D068 source maintenance, Stage 5 candidate materialization is ChatGPT-owned, Stage 6 execution/diagnosis/bounded repair/verification is Executor-owned, Stage 7 convergence/integration is ChatGPT-owned | `ROOT_TRIGGER_DOMAIN` | Concise root D068 ownership boundary; procedural sequence to domain route |
| S1-011 | D068 Stage 5 publishes one coherent candidate + authority on verified topic branch; no separate pre-verification merge to `develop` is required | `DOMAIN_ROUTE` | Maintainer/source-change procedure reference |
| S1-012 | D068 Stage 6 repair is bounded by approved semantics/design; material semantic defects require Orchestrator re-entry | `ROOT_INVARIANT` | Root Stage 6 authority boundary |
| S1-013 | D068 is prospective; historical/grandfathered persisted authority retains its historical meaning | `ROOT_INVARIANT` | Root historical-authority preservation invariant |
| S1-014 | Persistence status (`ephemeral`, `untracked`, outside worktree, deleted before commit) is not an ownership classifier | `ROOT_INVARIANT` | Root D076 loophole-closure invariant |
| S1-015 | Small mechanical Stage 6 execution aids are allowed; substantial new controller/harness/script/fixture-oracle implementation requires stop/re-entry to ChatGPT Stage 5 | `ROOT_TRIGGER_DOMAIN` | Concise root D076 materiality trigger; classification detail to domain route |
| S1-016 | D076 materiality is semantic/risk/function based, not governed by a rigid LOC threshold | `DOMAIN_ROUTE` | Maintainer/domain D076 reference |
| S1-017 | Late Stage 6 executable artifacts that influence verification require persisted D076 classification; material/uncertain discoveries require re-entry | `DOMAIN_ROUTE` | Maintainer/handoff procedure |
| S1-018 | Consequential version-sensitive reliance requires comparison of pinned/reference version, current stable, relevant higher releases and relevant prereleases when warranted | `ROOT_TRIGGER_TRANSVERSE` | Concise root D077 trigger; later evaluate `upstream-version-revalidation` |
| S1-019 | Version-sensitive outcomes use explicit dispositions and a materially new stable release before launch requires relevance classification | `DOMAIN_ROUTE` | Agent Governance D077 adapter/reference |
| S1-020 | D077 does not auto-extend prior qualification to later versions or make prereleases authority | `ROOT_INVARIANT` | Root qualification-authority invariant |
| S1-021 | D052 semantic conformance/oracle assets are Orchestrator-owned when selected; Executor owns Stage 6 execution/technical supplementary testing/repair | `ROOT_TRIGGER_DOMAIN` | Concise root semantic-oracle ownership boundary; testing workflow to domain route |
| S1-022 | Semantic changes to Orchestrator-owned oracle assets require persisted ChatGPT authority | `ROOT_INVARIANT` | Root semantic-authority invariant |
| S1-023 | Human Owner has final authority over scope, priorities, risk, public distribution, releases and overrides | `ROOT_INVARIANT` | Root ultimate-authority invariant |
| S1-024 | ChatGPT owns strategy, research synthesis, normative specs/design/plan, acceptance, Task Contracts, handoffs, convergence, checkpointing and committed Markdown | `ROOT_INVARIANT` | Root Orchestrator authority |
| S1-025 | Only ChatGPT may normally create/rewrite/persist committed Markdown instruction/design/decision/task/checkpoint files | `ROOT_INVARIANT` | Root Markdown write-ownership invariant |
| S1-026 | In D068 mode ChatGPT owns complete Stage 5 candidate materialization, including non-Markdown, without gaining Stage 6 execution mechanics | `ROOT_INVARIANT` | Root D068 materialization/verification split |
| S1-027 | Source orchestration must be resumable from canonical Git without prior chat history | `ROOT_TRIGGER_TRANSVERSE` | Concise root cold-start invariant; later evaluate `durable-work-checkpoint` |
| S1-028 | Executor role is host/product agnostic; host identity does not alter authority or acceptance | `ROOT_INVARIANT` | Root role-neutrality invariant |
| S1-029 | Executor owns D068 Stage 6 execution, diagnosis, bounded repair, technical review and verification evidence for the published candidate | `ROOT_TRIGGER_DOMAIN` | Concise root Executor Stage 6 boundary; enumerated workflow to domain route |
| S1-030 | Executor may choose private/internal implementation aids, workers, Skills and tooling only inside authorized execution/repair scope; these do not become governance authority | `ROOT_INVARIANT` | Root process-autonomy/authority invariant |
| S1-031 | Executor-internal plans/worker results/Skill outputs/approvals cannot become Task Contract, Design or acceptance authority or create unauthorized tracked/lifecycle state | `ROOT_INVARIANT` | Root non-authority invariant |
| S1-032 | D054 assigns command/API/SDK/shell/cloud/Git/uv execution mechanics to the Executor while Human/ChatGPT retain semantic target/risk/approval/acceptance authority | `ROOT_TRIGGER_DOMAIN` | Concise root semantic-vs-mechanics boundary; adapter procedure to domain route |
| S1-033 | Human Owner is not default terminal copy/paste operator; Human interaction is reserved for explicit approval/MFA/credential/risk/syntax-inspection gates | `ROOT_INVARIANT` | Root Human-gate invariant |
| S1-034 | D054 runbook-first operation resolution and version-specific/vendor documentation procedure | `REFERENCE_DETERMINISTIC` | Execution adapter/runbook reference and eventual deterministic recipe mechanism |
| S1-035 | Until native recipe persistence exists, newly learned operation syntax remains provisional handoff evidence | `DOMAIN_ROUTE` | Agent Governance execution/handoff reference |
| S1-036 | Orchestrator repository writes remain subject to branching policy and L007 fail-closed branch targeting | `ROOT_INVARIANT` | Root write-safety invariant |
| S1-037 | Every Executor launch requires concrete Executor, NEW/CONTINUE, current model, effort and rationale; checkpoint records selected adapter | `ROOT_TRIGGER_TRANSVERSE` | Concise root launch-profile trigger; later evaluate `executor-launch-handoff` |
| S1-038 | NEW/CONTINUE selection and minimum-sufficient model/effort heuristics are launch workflow detail, not correctness semantics | `DOMAIN_ROUTE` | Agent Governance D055 launch-profile adapter/reference |
| S1-039 | Coordinator names are deterministic navigation metadata only; Git/contracts/branches/handoffs/reviews remain authority | `DOMAIN_ROUTE` | Executor session/worktree hygiene reference |
| S1-040 | Concurrent writable work units require isolated writable worktree/topic-branch ownership; shared writable workspace is forbidden | `ROOT_TRIGGER_TRANSVERSE` | Concise root collision/isolation trigger; later evaluate repository-change-control/workspace placement |
| S1-041 | Prelaunch/post-integration workspace hygiene preserves ambiguous work and forbids destructive cleanup as a default mechanism | `REFERENCE_DETERMINISTIC` | Workspace hygiene reference/procedure |
| S1-042 | Executor must not edit Markdown, redefine semantics/design/plan/acceptance, invent missing authority, weaken contrary tests, mutate protected oracles without authority, change accepted refactor baseline, claim acceptance from green tests, or treat local-only state as completed handoff | `ROOT_INVARIANT` | Root Executor prohibition set |
| S1-043 | Executor may inspect Markdown/tests/evals read-only | `ROOT_INVARIANT` | Root read-permission invariant |
| S1-044 | Source product is governed by source-maintenance workflow, not by installing its consumer F0–F6 lifecycle onto itself | `ROOT_INVARIANT` | Root source-governance boundary |
| S1-045 | Markdown-only source changes use short-lived topic branch from `develop`, ChatGPT diff review and PR to `develop`; no Executor is introduced merely for ceremony | `ROOT_TRIGGER_DOMAIN` | Concise root mutation trigger; detailed Markdown workflow to Maintainer route |
| S1-046 | D068 executable source changes follow persisted authority -> ChatGPT Stage 5 candidate -> published checkpoint -> Executor Stage 6 -> persisted handoff/push -> ChatGPT Stage 7 -> PR/integration | `DOMAIN_ROUTE` | Maintainer/source-change procedure |
| S1-047 | Historical/non-D068 contracts retain their earlier persisted sequence; no silent migration | `ROOT_INVARIANT` | Root historical-authority invariant |
| S1-048 | Executor does not normally open/merge implementation PR unless Task Contract explicitly delegates the mechanical action | `ROOT_TRIGGER_DOMAIN` | Root delegation trigger; source-change procedure detail to domain route |
| S1-049 | Persisted Task Contract/published candidate/Git authority outrank chat/terminal transport; prompts must not supply missing semantics from chat history | `ROOT_INVARIANT` | Root durable-authority invariant |
| S1-050 | Material scope/spec/design/plan/acceptance/verification changes require persisted revision before execution continues | `ROOT_INVARIANT` | Root change-authority invariant |
| S1-051 | Executor completion states require persisted, committed and pushed handoff/current branch state; remote Git must reconstruct request/candidate/result/evidence/change | `ROOT_TRIGGER_DOMAIN` | Concise root durable-handoff requirement; detailed lifecycle/template to domain route |
| S1-052 | Private/internal Executor orchestration trace is not required unless explicitly contracted as deliverable/evidence | `ROOT_INVARIANT` | Root evidence-boundary invariant |
| S1-053 | `docs/orchestrator/CHECKPOINT.md` is the single current source Orchestrator frontier; session bootstrap starts from current `develop`, root `AGENTS.md`, then checkpoint | `ROOT_TRIGGER_TRANSVERSE` | Root cold-start trigger; later evaluate `durable-work-checkpoint` |
| S1-054 | Checkpoint references deeper authority instead of duplicating it; private chat is not required authority | `DOMAIN_ROUTE` | Agent Governance checkpoint adapter/reference |
| S1-055 | Checkpoint is refreshed on material frontier change and before intentional chat closure; closure requires remotely persisted reconstructable context | `DOMAIN_ROUTE` | Agent Governance checkpoint lifecycle reference |
| S1-056 | Checkpoint is source-maintenance state only and cannot create/substitute consumer `.agent-coordination/` state | `ROOT_INVARIANT` | Root source/consumer state boundary |
| S1-057 | Material research that can affect consequential product decisions must be persisted before downstream reliance; research evidence is not policy until explicit accepted normative promotion | `ROOT_TRIGGER_TRANSVERSE` | Concise root provenance trigger; later evaluate `research-evidence-traceability` |
| S1-058 | Agent Governance research uses stable `Rxxx`, independent Research/Decision state, complete ledger, durable non-decided states and successor/supersession lineage | `DOMAIN_ROUTE` | Agent Governance research-traceability adapter/reference |
| S1-059 | Volatile external facts must be refreshed before consequential later reliance, with version-sensitive cases additionally subject to D077 | `ROOT_TRIGGER_TRANSVERSE` | Root freshness trigger; route to research-evidence/upstream-revalidation candidates |
| S1-060 | Chat/session turnover cannot alter research/decision state; only persisted Git changes can | `ROOT_INVARIANT` | Root durable-state invariant |
| S1-061 | Test/eval suite must execute without requiring model-driven Skill activation | `ROOT_INVARIANT` | Root correctness-independence invariant |
| S1-062 | Maintainer Skill is the only project-owned top-level source test/eval maintenance Skill; it routes internally instead of spawning generic overlapping testing Skills | `ROOT_TRIGGER_DOMAIN` | Concise root domain-Skill boundary; detailed routing to Maintainer/testing reference |
| S1-063 | Cold Executor can bootstrap verification from published candidate + AGENTS + Task Contract + controlling refs/conformance assets/tooling even before Maintainer Skill exists | `ROOT_INVARIANT` | Root no-Skill dependency invariant |
| S1-064 | External testing/security Skills are optional supplemental aids after approval and cannot replace repository-owned verification; Consumer Governance Skill must not activate for source maintenance | `ROOT_INVARIANT` | Root Skill authority/coexistence invariant |
| S1-065 | Git is canonical source branch/commit/push mechanism; uv locked environment and Ruff are canonical source-maintainer execution/quality mechanisms | `REFERENCE_DETERMINISTIC` | Local toolchain reference/scripts/CI |
| S1-066 | Ruff must exclude committed Markdown; `.venv` is disposable; dependency truth is `pyproject.toml` + `uv.lock`; GitHub CLI is optional helper; executor hosts are not source dependencies | `REFERENCE_DETERMINISTIC` | Local toolchain reference/configuration |
| S1-067 | Source-maintainer toolchain must not be copied automatically into consumer repositories | `ROOT_INVARIANT` | Root source/consumer tooling boundary |
| S1-068 | Current file-category write ownership: Markdown/oracles/D068 Stage 5 candidate to ChatGPT, bounded D068 Stage 6 repair/evidence/handoff to Executor, historical exceptions by persisted authority | `ROOT_INVARIANT` | Root file-ownership invariant |
| S1-069 | Cross-responsibility file exceptions must be explicitly defined before mutation; host products never gain special authority and adapters cannot redefine ownership | `ROOT_INVARIANT` | Root exception/adapter invariant |
| S1-070 | `main` is stable/default, `develop` is unreleased integration, normal work uses short-lived topic branch from `develop` and PR back to `develop`; direct writes to long-lived branches and normal topic PRs to `main` are forbidden | `ROOT_TRIGGER_TRANSVERSE` | Concise root repository-change invariant; later evaluate `repository-change-control` |
| S1-071 | Release promotion/hotfix/release branch details and branch naming conventions | `DOMAIN_ROUTE` | Agent Governance branching reference |
| S1-072 | Neither ChatGPT nor Executor may bypass branching policy because of role or host identity | `ROOT_INVARIANT` | Root branch-authority invariant |
| S1-073 | Governance Core stays host-neutral; consumer mission/state stays out of source repo; Skills are tooling not authority; Skill packages require release gates | `ROOT_INVARIANT` | Root product-boundary invariant |
| S1-074 | Tests/evals validate Governance/Skill behavior rather than application-task implementation quality | `ROOT_INVARIANT` | Root verification-scope invariant |
| S1-075 | Verification architecture, isolation, fixtures, grader/threshold policy, and external Skill supply-chain/discovery procedures | `DOMAIN_ROUTE` | Testing/evaluation and supply-chain domain references |
| S1-076 | Prefer one coherent independently reviewable change; separate refactors, behavior changes, bug fixes, dependency upgrades and unrelated cleanup | `ROOT_TRIGGER_DOMAIN` | Concise root change-discipline rule; detailed refactor workflow to domain route |
| S1-077 | Refactor preserved behavior is explicit Orchestrator-owned acceptance meaning; characterization baselines follow the refactoring workflow | `DOMAIN_ROUTE` | Agent Governance refactoring reference |
| S1-078 | D068 protocol behavior change procedure: smallest relevant Core Markdown + authority updates + complete Stage 5 candidate + Stage 6 verification + Stage 7 acceptance | `DOMAIN_ROUTE` | Maintainer/source-change procedure |
| S1-079 | Preserve progressive context loading and avoid duplicating normative rules | `ROOT_INVARIANT` | Root instruction-architecture invariant |

## Duplicate / ambiguity / conflict audit

### Resolved by atomic split

The original R029 inventory intentionally used several mixed rows such as `ROOT_INVARIANT plus DOMAIN_ROUTE`, `ROOT_TRIGGER + TRANSVERSE_CANDIDATE / REFERENCE_OR_DETERMINISTIC`, or similar. Those were adequate for research but did not satisfy the S1 exact-one-classification gate. S1 resolves them by splitting the coarse row into separate atomic semantics, for example:

- Executor authority/prohibitions vs enumerated Stage 6 workflow;
- D058 collision/isolation invariant vs workspace cleanup mechanics;
- Testing Skill authority boundary vs deterministic test execution/tooling detail;
- Product identity invariants vs detailed verification/supply-chain references.

No semantic meaning is deleted by those splits.

### Remaining explicit ambiguity

`S1-059` (volatile-fact refresh) can later route operationally through either the research-evidence or upstream-version-revalidation capability depending on the dependency. This is **not** a preservation-classification ambiguity: its preservation class is uniquely `ROOT_TRIGGER_TRANSVERSE`. The later routing topology remains intentionally unresolved for S6/S5/S10.

`S1-040` (workspace isolation) is uniquely classified `ROOT_TRIGGER_TRANSVERSE`, but its eventual transverse placement remains unresolved between a repository-change-control sub-route/reference and a standalone capability. S9 owns that later placement decision.

### Conflicts

No contradiction was found between the current root and the R029 preservation hypothesis that requires resolution in S1. S1 does not adjudicate whether any candidate transverse Skill should ultimately exist; it only preserves the semantics needed if a future architecture refactor is adopted.

### Uncovered semantics

None. The audit found no material current root semantic unit without a preservation classification/destination.

## Coverage result

- Atomic semantic units audited: `79`.
- Unclassified material units: `0`.
- Delete-without-replacement units: `0`.
- Preservation-classification ambiguities: `0`.
- Explicit later topology/placement questions retained: `2` (`S1-040`, `S1-059`).
- Normative decisions made: `0`.

R029-S1 completion gate is satisfied: every material semantic unit of the current root `AGENTS.md` has exactly one explicit preservation classification/destination, while later topology questions remain recorded rather than silently decided.
