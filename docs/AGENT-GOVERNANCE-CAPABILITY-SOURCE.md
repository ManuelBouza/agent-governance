# Agent Governance Canonical Capability Source

Status: `MG1-FROZEN-FOR-T061-V14-CANDIDATE`  
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

Includes source-context validation; live Core, Task Contract/checkpoint/release-policy lookup; source workflow; authorized source handoff-path work; and source testing/eval/release routing. It never creates Consumer Governance state at source root and never inherits Consumer/external-install authority.

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

## Prospective v14 projection authority

- Stage 5 re-entry authority: `docs/reviews/T023-R17.md`
- Candidate mapping: `evals/skill_activation_topology/topologies.json`
- Exact v5 presentation sources/load plans: `evals/skill_activation_topology/presentations/manifest.json`
- Candidate integrity manifest: `evals/skill_activation_topology/candidate-hashes-v14.json`
- Candidate integrity guard: `evals/skill_activation_topology/verify_v14_candidate_integrity.py`
- Fresh v14 acceptance holdout: not yet authored at Freeze C; later `evals/skill_activation_topology/corpus.json` under `MG1-T023-CORPUS-v8`
- Metric/trial/matrix/selection oracle: not yet authored at Freeze C; later `evals/skill_activation_topology/oracle.json` under `MG1-T023-TOPOLOGY-ORACLE-v14`
- Controlling work unit: `docs/tasks/T061-mg1-v13-positive-anchor-reference-evaluation.md`, prospectively refined by R16/R17 for v14 re-entry

The v5 candidate `SKILL.md` files and shared references under `evals/skill_activation_topology/presentations-v5/` are Orchestrator-owned D052 semantic assets. B2 retains the exact approved T061 design bytes. F2/G3 and shared references are byte-identical copies of their corresponding v3 sources.

## Historical experiment boundary

MG1-v12 and MG1-v13 remain closed historical evidence. Historical v13 Freeze A `a454091aff7bb932372a6057e2d9804f94e66320`, Freeze B `7b990f4d60ba7ca0dfafe1b95785e007f8697c28`, and terminal blocked HEAD `d0ebe46a68c02c66dcfbb21c3dfaee43fb15c27f` are immutable.

Corpus v7/oracle v13/execution-v13 cannot be relabeled or reused as v14 acceptance authority. The exact v14 corpus/oracle are intentionally absent at Freeze C and may be authored only after the pushed Freeze C commit has been remotely verified.
