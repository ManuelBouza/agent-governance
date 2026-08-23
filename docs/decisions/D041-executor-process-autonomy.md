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

The executor MAY choose any compatible internal process or composition of capabilities available to it, including direct work, private/internal planning, private SDD/specification workflows, sub-agents/workers, Skills, code-graph/navigation tools, testing/review helpers, or other executor-native mechanisms.

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

A Task Contract SHOULD NOT prescribe private execution mechanics such as:

- whether the executor uses an internal SDD/planning helper inside its authorized implementation/review stages;
- whether to use one or many sub-agents;
- which executor-native worker type to select;
- how the executor decomposes its own internal coding/review work;
- which compatible navigation/planning/review tool to use;
- executor-internal prompting or context topology.

An internal method may be constrained only when the method itself is material to the product result, safety/security boundary, reproducibility requirement, ownership boundary, deterministic verification architecture, or another accepted Governance invariant.

## Internal executor artifacts and external authority

Executor autonomy does not make executor-internal state part of Agent Governance authority.

```text
internal plan / SDD state / worker result / Skill output / code graph
    = implementation aid or evidence
    != Task Contract authority
    != controlling Governance Design/Plan
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
- required technical Code Review & Verify is completed under applicable policy;
- required verification is completed;
- required handoff is valid;
- committed/pushed state is the state reported for review.

Agent Governance reviews the resulting Git state and evidence, not the executor's private orchestration trace.

## Relationship to D026, D030 and D031

D026 remains capability-first/reuse-before-install/no-authority-collision policy. It does not require or prohibit use of an executor-internal SDD helper inside the executor's authorized technical stages.

D030 prevents executor-host overlays from acquiring overlapping source-maintenance review/delivery/acceptance authority. It does not prohibit using non-authoritative host capabilities internally when they stay within the Task Contract and repository mutation boundary.

D031 permits Gentle-AI discovery/routing capabilities to coexist while preserving Governance authority. The same principle applies generally: capability use is allowed unless it creates a concrete authority or mutation conflict.

Any wording in prior source-maintenance decisions that says not to initialize/migrate this repository into an external SDD system remains a repository-state boundary: it prevents unsolicited tracked/generated project conversion. It MUST NOT be interpreted as a ban on using an executor's SDD capability internally when that capability can operate without unauthorized repository state or authority changes.

## Refinement by D053

Accepted D053 prospectively narrows **where** this process autonomy operates without revoking the autonomy itself.

Native Agent Governance SDD has one accountable owner per stage:

```text
Orchestrator -> Explore / Specify / Design / Plan & Trace
Executor     -> Implement / Code Review & Verify
Orchestrator -> Converge / Accept / Evolve
```

Therefore:

- D041 autonomy applies inside executor stages `Implement` and `Code Review & Verify`;
- executor-private planning/SDD/design-like tools remain implementation aids only;
- the executor does not acquire authoritative specification, controlling Design, Plan/Trace or acceptance ownership merely because its host provides those capabilities;
- local coding choices remain autonomous when they preserve the approved Design;
- a material requirement/Design/Plan defect discovered during implementation/review requires stop/re-entry to the Orchestrator rather than an executor-authored authoritative redesign.

Where earlier D041 wording could be read as giving the executor authority to decide whether the governed task itself uses SDD or to own material technical Design, D053 controls prospectively. The executor remains free to choose private methods for realizing and technically reviewing the already-approved contract.

## Consequences

- Task Contracts remain executor-product neutral while now carrying the complete Orchestrator-owned specification/Design/Plan boundary required by D053.
- Agent Governance does not route work to `General Task`, SDD agents, or any other host-specific agent type.
- The executor is free to select and compose its full compatible toolset inside stages 5-6.
- Review continues to rely on remote Git state, technical review/verification evidence and the persisted handoff rather than internal orchestration behavior.
- Host-specific restrictions are introduced only for demonstrated authority, mutation, security, reproducibility or acceptance conflicts.
