# Agent Governance Canonical Capability Source

Status: `MG1-FROZEN-FOR-T023`  
Authority: ChatGPT Orchestrator under D050 / D052  
Capability-Source-Epoch: `MG1-2026-08-24-v1`

## Purpose

This document is the canonical authoring/routing source used by MG1/T023 to project Agent Governance activation topologies. It does not replace `governance-core/`, the shared deterministic engine, profile contracts, or source-product policy overlays.

Every topology evaluated by T023 MUST be a presentation of the same capability set below. Candidate topology may change activation metadata, grouping and progressive reference exposure only; it MUST NOT change governed behavior, authority, permissions or deterministic semantics.

## Canonical capability families

### `consumer-lifecycle`

Profile: `consumer`  
Actor/context: governed Consumer repository.  
Risk/mutation boundary: durable Consumer `.agent-governance/` / `.agent-coordination/` footprint only through accepted Consumer runtime semantics.

Intents include:

- bootstrap and validate a Consumer installation;
- inspect/refresh Governance state;
- record lifecycle events and sequencing/handoff state;
- mission/workplan and task-governance interactions;
- archive preparation;
- coexistence and ordinary Consumer governance guidance;
- external Skill discovery/approval/audit when that capability is not projected as a separate activation peer.

### `source-maintainer`

Profile: `source-maintainer`  
Actor/context: Agent Governance source repository identified by the exact supported source-product signal.  
Risk/mutation boundary: source adapters and source-only policy records; no Consumer installation state at source root.

Intents include:

- inspect/validate source-maintainer context;
- locate live Core, Task Contracts, checkpoint, decisions, testing/eval and handoff records;
- reason about source-maintenance workflow, branching, release and verification policy;
- resolve authorized source handoff JSON paths;
- maintain strict source/Consumer isolation.

### `external-skill-trust`

Profile: `consumer` capability surface, not a third runtime profile.  
Actor/context: Consumer/user evaluating external Agent Skills or supply-chain trust.  
Risk boundary: discovery, approval and audit semantics already governed by accepted Consumer Skill trust mechanisms; no broadened package/runtime authority.

Intents include:

- discover or evaluate an external Skill;
- inspect candidate provenance/trust evidence;
- decide whether a candidate is eligible for Governance approval;
- reason about supply-chain risk and approval boundaries.

## Negative / non-Governance intents

Agent Governance SHOULD NOT activate for ordinary coding, generic SDD/tooling questions, generic Git operations, unrelated documentation editing, broad product advice, or generic package installation where no Governance, source-maintenance or external-Skill-trust intent is present.

Near-miss wording containing terms such as `agent`, `governance`, `skill`, `source`, `profile`, `task`, or `release` is insufficient by itself.

## Ambiguous intents

When a prompt plausibly refers to more than one Governance context but lacks enough information to identify the required profile/capability safely, the expected semantic outcome is bounded clarification/insufficient-context behavior rather than silent permission broadening.

## Multi-intent behavior

A prompt may legitimately require multiple capability families. The topology projection determines whether those families map to one activated entrypoint or multiple generated peers. Multiple activation is correct only when required by the frozen case expectation; unnecessary peer activation counts as overactivation.

## Frozen topology projection rule

The exact B0/B1/F2/G3 entrypoint identities and capability-to-entrypoint mapping are frozen in:

`evals/skill_activation_topology/topologies.json`

The frozen acceptance corpus is:

`evals/skill_activation_topology/corpus.json`

The frozen metric, trial, matrix and selection oracle is:

`evals/skill_activation_topology/oracle.json`

T023 may implement technical runners/adapters and supplementary diagnostics, but MUST NOT modify this document or those three semantic assets unless a new persisted Orchestrator revision explicitly restarts the experiment before the affected comparative claim.
