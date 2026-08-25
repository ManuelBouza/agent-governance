# Agent Governance Canonical Capability Source

Status: `MG1-FROZEN-FOR-T023`  
Authority: ChatGPT Orchestrator under D050 / D052  
Capability-Source-Epoch: `MG1-2026-08-25-v3`

## Purpose

This document is the canonical authoring/routing source used by MG1/T023 to project Agent Governance activation topologies. It does not replace `governance-core/`, the shared deterministic engine, profile contracts, or source-product policy overlays.

Every evaluated topology presents the same governed capability semantics. Topology may change activation metadata, grouping and progressive-disclosure/load behavior only; it must not change authority, permissions, deterministic runtime behavior or product identity.

## Capability families

### `consumer-lifecycle`

Profile: `consumer`. Context: adopting/governed Consumer repository.

Includes bootstrap/validate, state/frontier reconstruction, lifecycle events, mission/workplan/task sequencing, handoffs, archive preparation, coexistence and other accepted Consumer Governance operations. It never authorizes source-product maintenance.

### `source-maintainer`

Profile: `source-maintainer`. Context: canonical Agent Governance source product identified by the exact supported source-product signal.

Includes source-context validation; live Core, Task Contract, checkpoint, decision, testing/eval, branch/release and handoff routing; and authorized source handoff JSON path resolution. It never creates Consumer Governance state at source root and never inherits Consumer/external-install authority.

### `external-skill-trust`

Consumer-side capability surface, not a third runtime profile.

Includes Governance-scoped external Agent Skill discovery, provenance/integrity review, approval eligibility and supply-chain audit. It does not itself grant installation approval, source-maintainer authority or Consumer lifecycle mutation authority.

## Negative and ambiguous intents

Agent Governance should not activate for generic coding, SDD/tooling, Git, releases, corporate governance, unrelated source maintenance or generic Skill/package installation without explicit Agent Governance intent.

For source-versus-Consumer ambiguity, required semantics are `clarify-context` with no profile/capability grant and no governed mutation. Under v3 a neutral B0/B1 dispatcher/router may activate solely to ask for context. Profile-specific F2/G3 peers must remain unselected until enough context exists. Neutral clarification activation is not permission broadening.

## Cross-profile boundary

A legitimate current-context capability may activate to enforce a boundary and return `bounded-rejection`. A violation exists only when a forbidden capability/profile is granted or performed, or the required bounded rejection is not returned.

## Multi-intent behavior

A request may legitimately require multiple capability families. Topology determines whether those capabilities map to one or several entrypoints. Unnecessary peer activation remains overactivation.

## Frozen v3 projection authority

- Candidate mapping: `evals/skill_activation_topology/topologies.json`
- Exact v3 presentation sources/load plans: `evals/skill_activation_topology/presentations/manifest.json`
- Fresh v3 acceptance holdout: `evals/skill_activation_topology/corpus.json`
- Metric/trial/matrix/selection oracle: `evals/skill_activation_topology/oracle.json`
- T042 restart contract: `docs/tasks/T042-mg1-v3-independent-holdout-restart.md`

The v3 candidate `SKILL.md` files and shared references under `evals/skill_activation_topology/presentations-v3/` are Orchestrator-owned D052 semantic assets. T023 may byte-copy them into isolated candidate directories but must not rewrite or synthesize their wording.

## Prior experiment boundary

MG1-v2 executed all 360 live trials and is closed `BLOCKED`; review: `docs/reviews/T023-R1.md`. Its evidence remains immutable. V3 is a new experiment with new oracle, presentations and 40-case holdout. V2 cases/results cannot enter the v3 acceptance score or be used for post-start tuning.
