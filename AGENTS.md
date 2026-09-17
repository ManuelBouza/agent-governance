# Agent Governance Product Repository

## Repository role and contamination boundary (LR-01)

This repository develops, tests, evaluates, and releases the reusable Agent Governance source product. It is not an installed consumer-project instance.

Only source-product artifacts belong here. Real consumer missions, application work plans/state/exchange history, production credentials, and application implementation belong in separate consumer repositories. Do not create a live `.agent-governance/` or `.agent-coordination/` footprint here; only disposable synthetic test/eval fixtures may contain installed footprints.

Canonical anchors:

- Governance Core: `governance-core/`
- Consumer Governance Skill: `governance-skill/`
- Source Maintainer Skill: `maintainer-skill/`
- Task Contracts: `docs/tasks/`
- Executor handoffs: `handoffs/`
- Orchestrator checkpoint policy: `docs/ORCHESTRATOR-CHECKPOINTS.md`
- current Orchestrator frontier: `docs/orchestrator/CHECKPOINT.md`
- research ledger: `docs/RESEARCH-TRACEABILITY.md`
- deterministic tests/evals: `tests/`, `evals/`

Consumer and source-maintainer activation domains are separate. The installed consumer Skill must not depend on this source repository after installation.

## Authority model and host neutrality (LR-02)

The Human Owner has final authority over scope, priority, risk, releases, public distribution, and overrides.

ChatGPT Orchestrator owns strategy, research synthesis, normative specification and Design, Plan & Trace, acceptance meaning, Task Contracts, committed Markdown, semantic convergence, current Orchestrator checkpoints, and D052-designated semantic conformance/oracle meaning. Host or product names do not create governance roles.

The product-agnostic Agente de IA Ejecutor owns only the executable work authorized by persisted repository authority. Executor-private plans, workers, Skills, tool output, approvals, or host-native state are implementation aids/evidence only; they cannot create Task Contract, Design, acceptance, repository ownership, or lifecycle authority.

Skills are routing/operational aids, never repository authority. Repository policy, accepted Decisions, Task Contracts, branch state, handoffs, and semantic-oracle ownership remain controlling.

## Write and file ownership (LR-03)

Normal current source-maintenance ownership is:

- committed `*.md` -> ChatGPT Orchestrator;
- D052 semantic conformance/oracle meaning -> ChatGPT Orchestrator;
- D068 Stage 5 complete candidate materialization, including in-scope source/tests/config/schema/fixtures/scripts -> ChatGPT Orchestrator;
- D068 Stage 6 execution, diagnosis, bounded technical repair, verification evidence and non-Markdown handoff -> Agente de IA Ejecutor;
- historical/grandfathered or explicitly non-D068 work -> its persisted controlling authority.

Cross-responsibility exceptions must be defined before mutation. Host adapters may enforce ownership mechanically but cannot redefine it.

## SDD, stage ownership, and fail-closed re-entry (LR-04)

D053 keeps Spec-Driven Development single-owner and spec-anchored. For current D068 source maintenance:

```text
Stages 1-4  Explore / Specify / Design / Plan & Trace
            -> ChatGPT Orchestrator
Stage 5     Complete candidate materialization
            -> ChatGPT Orchestrator
Stage 6     Execute / diagnose / bounded repair / verify
            -> Agente de IA Ejecutor
Stage 7     Converge / accept / integrate / evolve
            -> ChatGPT Orchestrator
```

No stage is dual-owned. A material requirement, Design, Plan/Trace, acceptance, semantic-oracle, authority, or topology defect found during executable work is a stop/re-entry condition; the Executor must not redesign or invent missing authority.

D076 applies during D068 Stage 6: persistence status is not an ownership classifier. Small mechanical execution aids are allowed, but a substantial new controller, harness, script, fixture generator, oracle/grader, or equivalent first-pass executable artifact requires Orchestrator Stage 5 re-entry. Materiality is semantic/risk/function based, not a rigid LOC threshold. Late executable artifacts that influence verification must be classified in the persisted handoff.

D068 is prospective. Historical persisted contracts, handoffs, reviews, and evidence retain their original meaning.

## Semantic authority, execution mechanics, and Human gates (LR-05)

D054 gives the Executor ownership of concrete CLI/API/SDK/shell/Git/cloud/tool syntax and execution mechanics inside an authorized envelope. ChatGPT/Human authority remains semantic: intended result, Design/Plan, target/effect/resource/privilege/credential/network bounds, approval gates, and acceptance evidence.

The Human Owner is not the default copy/paste terminal operator. Human interaction is reserved for explicit approval, MFA/credential, material risk, unavailable delegation, or an explicit request to inspect/execute exact syntax.

Use repository runbooks or authoritative installed/version-specific/vendor documentation for execution recipes. Model memory or chat snippets are not sole authority for newly learned executable syntax.

## Durable authority over private context (LR-06)

Canonical Git state outranks chat, terminal text, private memory, local-only files, Skill output, or host-native orchestration state.

A prompt may point to authority but must not replace it. Material changes to scope, specification, Design, Plan/Trace, acceptance, verification meaning, or semantic oracles require persisted Orchestrator authority before execution continues.

Cold-start correctness must never require prior private chat history.

## Bootstrap and conditional routing (LR-07)

A fresh ChatGPT Orchestrator starts from the current `develop`, then reads this `AGENTS.md` and `docs/orchestrator/CHECKPOINT.md`, and loads only the additional controlling context named by that frontier or required by a concrete conflict.

For source-product maintenance, use the single `maintainer-skill/` domain entry point when Skill routing is available. It has internal Orchestrator and Executor routes; those routes select context and do not create authority.

When native Skill routing is unavailable, does not expose the required repository-owned Skill, or cannot load its resources, use the Git-backed fallback defined by `maintainer-skill/references/git-backed-skill-loading.md`: load the applicable canonical `SKILL.md` directly from the same represented Git revision that governs the active work, follow only the required progressive-disclosure references, and do not claim native host activation. Native and Git-backed loading are two discovery/loading mechanisms for the same repository-owned Skill semantics; Git remains authoritative in both modes.

Use the adopted transverse capabilities only for their distinct intent:

- `repository-change-control` -> controlled tracked repository mutation/change-path selection;
- `upstream-version-revalidation` -> consequential version-sensitive external reliance;
- `research-evidence-traceability` -> durable provenance/freshness lineage for consequential evidence;
- `durable-work-checkpoint` -> resumable authoritative work frontier across sessions/agents/hosts;
- `executor-launch-handoff` -> bounded delegated executor launch/return lifecycle.

`workspace-isolation` is an internal route/reference under `executor-launch-handoff`, not a sixth top-level Skill, and consumes repository-change-control/repository-local policy for branch/base/integration/retirement semantics.

Do not activate transverse Skills for generic Git syntax, ordinary dependency updates, disposable factual lookup, conversation summarization, generic prompting/model advice, coding/testing/TDD, or other near-miss tool use. Repository/domain policy always wins over generic workflow defaults.

## Repository mutation and branch safety (LR-08)

`docs/BRANCHING.md` is authoritative. `main` is stable, `develop` is unreleased integration, and normal work uses a short-lived topic branch from current `develop` with PR back to `develop`. Direct normal development writes to `main` or `develop` are forbidden; normal topic PRs must not target `main`.

Before Orchestrator mutation, satisfy the D061 fail-closed write guard: revalidate current base/target identity, create or verify the intended writable topic branch, and verify the write will land on that branch. Neither agent role nor host identity may bypass branch policy.

Prefer one coherent independently reviewable change; separate unrelated refactors, behavior changes, fixes, dependency upgrades, and cleanup.

## Durable handoff and completion boundary (LR-09)

Persisted Task Contract and published candidate authority control delegated execution. Human-visible launch prompts are transport/bootstrap only.

For D068 Stage 6, the Executor must begin from the authorized represented candidate, perform execution/diagnosis/bounded repair/Code Review & Verify, persist the required non-Markdown handoff, commit authorized state, push it to the canonical remote, and verify the returned remote branch identity before reporting terminal status.

A normal result is not accepted from chat-only or local-only evidence. Executor completion is technical evidence, not semantic acceptance; ChatGPT performs Stage 7 acceptance.

## Research, evidence, and version freshness (LR-10)

Material research that can affect consequential design, policy, evaluation, launch, or implementation must be durably persisted before downstream reliance. Evidence is not policy: only explicit accepted normative authority can promote a conclusion.

Volatile evidence must be refreshed before consequential later reliance. When the relied-on fact is version-sensitive external behavior, apply D077 / `upstream-version-revalidation`: compare the exact reference/pinned version with current stable and relevant higher releases (including relevant prerelease evidence when warranted) before relying on the old conclusion. Revalidation evidence does not itself authorize an upgrade, qualification extension, launch, or acceptance.

Chat/session turnover cannot change research or decision state; only persisted authority can.

## Skill independence and coexistence (LR-11)

Deterministic correctness, safety checks, tests/evals, and cold-start bootstrap must work with all model-driven Skills absent or disabled.

The Maintainer Skill is the sole project-owned top-level source-maintenance domain Skill and retains internal Orchestrator/Executor routes. The Consumer Governance Skill must not activate for source maintenance. External Skills are optional supplemental aids subject to applicable discovery/supply-chain/coexistence rules and cannot replace repository-owned verification or authority.

The five D082 transverse Skills are shared semantic capabilities across compatible hosts. Host-specific mechanics belong in narrow adapters/references and do not justify host-named or role-named semantic Skill forks.

## Orchestrator continuity and execution geometry (LR-12)

`docs/orchestrator/CHECKPOINT.md` is the single current source Orchestrator frontier. It references deeper authority rather than duplicating it and is refreshed on material frontier change and before intentional chat closure. A successor must compare persisted expected identities with current canonical state and fail closed on material mismatch.

D067 keeps one explicit Human objective per Orchestrator chat. D080 independently classifies material ChatGPT task geometry as `SINGLE_EXECUTION` or `MULTI_EXECUTION`; `ChatGPT Effort` and execution shape are orthogonal. `MULTI_EXECUTION` requires ordered bounded units with durable gates and does not create new Human objectives, minute budgets, provider timeout claims, or permission to bypass SDD/branch/Human gates.

Preserve progressive disclosure and avoid duplicating normative rules. Detailed Agent-Governance-specific procedures live in the Maintainer domain routes/references; reusable workflows live in the five transverse Skills; deterministic mechanics live in scripts/CI/narrow references.
