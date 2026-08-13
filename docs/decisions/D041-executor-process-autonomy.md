# D041 — Executor process autonomy

Status: ACCEPTED  
Authority: Human Owner / ChatGPT Orchestrator

## Problem

Agent Governance defines the requested result, scope, invariants, acceptance criteria and evidence for source-product implementation tasks. The Agente de IA Ejecutor may itself be a multi-agent host with proprietary planning, SDD, worker, Skill, graph, review, testing or other execution capabilities.

Existing source-maintenance policy correctly prevents external executor-host workflows from acquiring Governance authority, but that boundary can be misread as a restriction on the executor's internal implementation process. Over-constraining that process would make Agent Governance responsible for choosing executor-specific orchestration methods and would reduce portability across capable hosts.

The required boundary is therefore between **Governance authority** and **executor implementation autonomy**, not between allowed and disallowed internal methodologies by product name.

## Decision

For an authorized executable Task Contract, Agent Governance controls **what result is required and what boundaries must hold**. The Agente de IA Ejecutor controls **how to organize and perform the authorized technical work**.

Core invariant:

```text
Governance owns requested outcome + boundaries + acceptance
Executor owns implementation process + internal orchestration
```

The executor MAY choose any compatible internal process or composition of capabilities available to it, including direct work, planning, SDD/specification workflows, sub-agents/workers, Skills, code-graph/navigation tools, testing/review helpers, or other executor-native mechanisms.

Agent Governance MUST NOT prescribe an executor-internal methodology, agent type, delegation topology, planning framework, or tool merely because it is available or preferred by the current host.

## Result-oriented Task Contracts

A source-product Task Contract SHOULD specify only the implementation semantics necessary to make the requested result objectively bounded and reviewable, including the applicable subset of:

- observable objective/result;
- authorized repository scope;
- explicit exclusions;
- architecture/compatibility/security constraints;
- acceptance criteria;
- required verification/evidence;
- branch/handoff/result contract;
- stop/escalation conditions.

A Task Contract SHOULD NOT prescribe internal execution mechanics such as:

- whether to use SDD;
- whether to use one or many sub-agents;
- which executor-native worker type to select;
- how the executor decomposes its own internal work;
- which compatible navigation/planning/review tool to use;
- executor-internal prompting or context topology.

An internal method may be constrained only when the method itself is material to the product result, safety/security boundary, reproducibility requirement, ownership boundary, deterministic verification architecture, or another accepted Governance invariant.

## Internal executor artifacts and external authority

Executor autonomy does not make executor-internal state part of Agent Governance authority.

```text
internal plan / SDD state / worker result / Skill output / code graph
    = implementation aid or evidence
    != Task Contract authority
    != Governance acceptance
```

The executor MAY create/use local or ephemeral internal state when permitted by repository policy and the applicable execution envelope. It MUST NOT commit generated executor-host/project-initialization state outside authorized scope or turn a host-native approval/review state into an additional Agent Governance acceptance requirement.

If an internal methodology would require tracked repository mutation outside authorized scope, conflicting lifecycle authority, or an external mandatory approval gate that overlaps Governance, the executor must choose another compatible method or stop/escalate under the existing coexistence/overlay rules.

## Delegation and accountability

Agent Governance does not govern how an executor host delegates internally.

A sub-agent/worker MAY read the complete Task Contract, perform a whole task, perform a bounded slice, verify another worker, or participate in another executor-native topology if the executor host determines that is appropriate.

The only Governance-relevant requirement is that the abstract Agente de IA Ejecutor remains accountable for the externally visible contract:

- authorized scope is respected;
- required result is produced;
- required verification is completed;
- required handoff is valid;
- committed/pushed state is the state reported for review.

Agent Governance reviews the resulting Git state and evidence, not the executor's private orchestration trace.

## Relationship to D026, D030 and D031

D026 remains capability-first/reuse-before-install/no-authority-collision policy. It does not require or prohibit SDD as an executor-internal implementation method.

D030 prevents executor-host overlays from acquiring overlapping source-maintenance review/delivery/acceptance authority. It does not prohibit using non-authoritative host capabilities internally when they stay within the Task Contract and repository mutation boundary.

D031 permits Gentle-AI discovery/routing capabilities to coexist while preserving Governance authority. The same principle applies generally: capability use is allowed unless it creates a concrete authority or mutation conflict.

Any wording in prior source-maintenance decisions that says not to initialize/migrate this repository into an external SDD system remains a repository-state boundary: it prevents unsolicited tracked/generated project conversion. It MUST NOT be interpreted as a ban on using an executor's SDD capability internally when that capability can operate without unauthorized repository state or authority changes.

## Consequences

- Task Contracts become more strictly result-oriented and executor-product neutral.
- Agent Governance does not route work to `General Task`, SDD agents, or any other host-specific agent type.
- The executor is free to select and compose its full compatible toolset.
- Review continues to rely on remote Git state, deterministic evidence and the persisted handoff rather than internal orchestration behavior.
- Host-specific restrictions are introduced only for demonstrated authority, mutation, security, reproducibility or acceptance conflicts.
