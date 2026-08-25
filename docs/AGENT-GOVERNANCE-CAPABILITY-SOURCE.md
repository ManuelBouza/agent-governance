# Agent Governance Canonical Capability Source

Status: `MG1-FROZEN-FOR-T023`  
Authority: ChatGPT Orchestrator under D050 / D052  
Capability-Source-Epoch: `MG1-2026-08-25-v2`

## Purpose

This document is the canonical authoring/routing source used by MG1/T023 to project Agent Governance activation topologies. It does not replace `governance-core/`, the shared deterministic engine, profile contracts, or source-product policy overlays.

Every topology evaluated by T023 MUST be a presentation of the same capability set below. Candidate topology may change activation metadata, grouping and progressive reference exposure only; it MUST NOT change governed behavior, authority, permissions or deterministic semantics.

## Canonical capability families

### `consumer-lifecycle`

Profile: `consumer`  
Actor/context: governed Consumer repository.  
Risk/mutation boundary: durable Consumer `.agent-governance/` / `.agent-coordination/` footprint only through accepted Consumer runtime semantics.

Intents include bootstrap/validate, state, lifecycle events, mission/workplan/task sequencing, handoffs, archive preparation, coexistence and ordinary Consumer Governance guidance. External Skill discovery/approval/audit remains a Consumer capability even when projected as a separate activation peer.

### `source-maintainer`

Profile: `source-maintainer`  
Actor/context: Agent Governance source repository identified by the exact supported source-product signal.  
Risk/mutation boundary: source adapters and source-only policy records; no Consumer installation state at source root.

Intents include source context validation, live Core/Task Contract/checkpoint/decision/testing/handoff routing, source workflow/branch/release policy and authorized source handoff JSON paths.

### `external-skill-trust`

Profile: `consumer` capability surface, not a third runtime profile.  
Actor/context: Consumer/user evaluating external Agent Skills or supply-chain trust.

Intents include external Skill discovery, provenance/trust review, approval eligibility and supply-chain audit. It grants neither source-maintainer authority nor independent product identity.

## Negative and ambiguous intents

Agent Governance SHOULD NOT activate for ordinary coding, generic SDD/tooling, generic Git operations, unrelated documentation/release work, or generic package/Skill installation without an Agent Governance intent. Near-miss words such as `agent`, `governance`, `skill`, `source`, `profile`, `task`, or `release` are insufficient alone.

When a prompt plausibly refers to multiple Governance contexts but lacks enough information to identify the required profile safely, the expected outcome is bounded clarification rather than permission broadening.

## Multi-intent behavior

A request may legitimately require multiple capability families. The topology determines whether those families map to one or several entrypoints. Multiple activation is correct only when required by the frozen case expectation; unnecessary peers count as overactivation.

## Frozen projection authority

Exact candidate mapping: `evals/skill_activation_topology/topologies.json`  
Exact host-visible presentation sources and load plans: `evals/skill_activation_topology/presentations/manifest.json`  
Frozen acceptance corpus: `evals/skill_activation_topology/corpus.json`  
Frozen metric/trial/matrix/selection oracle: `evals/skill_activation_topology/oracle.json`

The seven candidate `SKILL.md` files and three shared capability references under `evals/skill_activation_topology/presentations/` are part of the D052 semantic oracle. T023 may copy them byte-for-byte into isolated temporary host-visible candidate directories but must not rewrite or synthesize their wording.

MG1 v1 was superseded before any comparative trial because it lacked exact candidate presentation surfaces. T023 blocker evidence at `b7402bbaea52d7ac4342b848c73bf56a7bb4bbef` records `0/360` trials. This v2 revision changes presentation completeness only; corpus expectations and selection thresholds remain unchanged.
