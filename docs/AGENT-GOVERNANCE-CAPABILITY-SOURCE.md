# Agent Governance Canonical Capability Source

Status: `MG1-FROZEN-FOR-T061-V13`  
Authority: ChatGPT Orchestrator under D050 / D052  
Capability-Source-Epoch: `MG1-2026-09-06-v4`

## Purpose

This document is the canonical authoring/routing source used by MG1/T023 to project Agent Governance activation topologies. It does not replace `governance-core/`, the shared deterministic engine, profile contracts, or source-product policy overlays.

Every evaluated topology presents the same governed capability semantics. Topology may change activation metadata, grouping and progressive-disclosure/load behavior only; it must not change authority, permissions, deterministic runtime behavior or product identity.

## Top-level activation boundary

Top-level Agent Governance activation requires both affirmative Agent Governance applicability and an Agent Governance capability intent.

Affirmative applicability is limited to:

- an adopting/governed Consumer repository where Agent Governance applies;
- the canonical Agent Governance source product identified by the exact supported source-product signal; or
- an explicit request to apply Agent Governance trust requirements to an external Agent Skill.

Generic topic similarity, unrelated maintenance/Skill/governance wording, or incidental Agent Governance mention is insufficient. Explicit absence, opt-out, or non-applicability is not affirmative applicability.

When Agent Governance applicability is affirmative but source-versus-Consumer role is unresolved, the single-reference B2 router may activate only to ask for context. It must not grant a profile/capability, load a capability reference, or authorize governed mutation during that clarification.

No capability definition, runtime permission, or authority changes in v4.

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

Agent Governance should not activate when the top-level activation boundary is not satisfied, including generic coding, SDD/tooling, Git, releases, corporate governance, unrelated source maintenance, generic Skill/package installation without Agent Governance trust scope, explicit Agent Governance absence/opt-out, or incidental product mention without governed intent.

For source-versus-Consumer ambiguity where Agent Governance applicability is affirmative, required semantics are `clarify-context` with no profile/capability grant, no capability-reference load and no governed mutation. Under v4 B2 may activate solely to ask for that context. Profile-specific F2/G3 peers must remain unselected until enough context exists. Neutral clarification activation is not permission broadening.

## Cross-profile boundary

A legitimate current-context capability may activate to enforce a boundary and return `bounded-rejection`. A violation exists only when a forbidden capability/profile is granted or performed, or the required bounded rejection is not returned.

## Multi-intent behavior

A request may legitimately require multiple capability families. Topology determines whether those capabilities map to one or several entrypoints. Unnecessary peer activation remains overactivation.

## Frozen v4 projection authority

- Candidate mapping: `evals/skill_activation_topology/topologies.json`
- Exact v4 presentation sources/load plans: `evals/skill_activation_topology/presentations/manifest.json`
- Candidate integrity manifest: `evals/skill_activation_topology/candidate-hashes-v13.json`
- Candidate integrity guard: `evals/skill_activation_topology/verify_v13_candidate_integrity.py`
- Fresh v13 acceptance holdout: `evals/skill_activation_topology/corpus.json` (Freeze B only)
- Metric/trial/matrix/selection oracle: `evals/skill_activation_topology/oracle.json` (Freeze B only)
- Task Contract: `docs/tasks/T061-mg1-v13-positive-anchor-reference-evaluation.md`

The v4 candidate `SKILL.md` files and shared references under `evals/skill_activation_topology/presentations-v4/` are Orchestrator-owned D052 semantic assets. B2 is exact Design authority from T061. F2/G3 and shared references are byte-identical copies of their v3 sources.

## Prior experiment boundary

MG1-v12 is closed and immutable under `docs/reviews/T023-R11.md`. B0/B1 remain historical v3 candidates and are not scheduled in v13. V12 cases/results cannot enter the v13 acceptance score or be used for post-freeze tuning.

The exact v13 corpus/oracle are intentionally absent at Freeze A and may be authored only after the pushed Freeze A commit has been remotely verified.
