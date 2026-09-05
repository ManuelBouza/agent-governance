# D065 — Semantic Executor Delegation Obligation

Status: ACCEPTED  
Date: 2026-09-05  
Owner: Human Owner / ChatGPT Orchestrator  
Research: `docs/research/CODEX-COORDINATOR-DELEGATION-POLICY-RESEARCH.md` (`R012`)  
Scope: source-product Executor coordination policy; no Governance Core / consumer-protocol change

## Decision

Agent Governance adopts a **semantic delegation obligation** for non-trivial Executor-governed source-maintenance work.

The Human-visible Executor root remains the task coordinator. Agent Governance defines **when bounded delegation is required and the safety/evidence bounds**; the Executor coordinator owns **how** eligible work is decomposed and orchestrated.

```text
Agent Governance owns WHEN + bounds.
Executor coordinator owns HOW + mechanics.
```

This decision prospectively refines D041 process autonomy and D060 coordinator semantics. It does not prescribe a universal worker graph, worker count, vendor role name, model, reasoning effort, spawn API, sequencing primitive, or parallelism strategy.

## Applicability

For new or materially revised `STANDARD` and `ASSURED` Task Contracts with Executor-owned stages 5–6, the coordinator MUST evaluate delegation:

1. before substantial implementation/exploration; and
2. before final technical Code Review & Verify.

`COMPACT` work and bounded Operational Contracts may remain root-local by default when the work is small, mechanical, tightly serial, or otherwise dominated by the anti-triggers below, unless persisted authority makes delegation/topology material.

A Task Contract may freeze a different topology when topology itself is part of an experiment, safety invariant, independent-review requirement, or acceptance evidence.

## Material delegation triggers

The coordinator MUST treat delegation as eligible when at least one material trigger applies:

1. **Independent read-heavy exploration** — codebase/API/dependency mapping can be isolated and summarized without changing authority.
2. **Noisy execution/evidence collection** — tests, logs, traces, repetitive command output, or large diagnostic material would pollute the root context.
3. **Independent verification** — correctness, security, compatibility, or test-gap review materially benefits from a fresh reasoning path.
4. **Parallelizable bounded scopes** — two or more non-overlapping slices can execute independently and materially reduce wall time or improve coverage.
5. **Specialized capability** — a bounded child context/tool/domain orientation is materially better suited to a slice.
6. **Root-context protection** — disposable reasoning can be delegated so the root retains requirements, constraints, branch/worktree identity, decisions, findings, and synthesis cleanly.

When at least one trigger applies and no anti-trigger/safety constraint below materially dominates, the coordinator **MUST delegate at least the eligible bounded slice** instead of performing all work in the Human-visible root.

## Material anti-triggers

Root-local execution remains conforming when one or more of these materially dominate:

1. the task/slice is small and straightforward;
2. work is tightly serial and benefits from one continuous mental model;
3. delegation would duplicate most orientation/context and provide little independent value;
4. child coordination cost is likely greater than the work saved or quality gained;
5. mutable ownership overlaps such that delegation would increase conflict/race risk;
6. the root is an exact controller/state machine whose topology is itself frozen, as T057 was;
7. persisted authority explicitly fixes another topology;
8. the available child surface cannot satisfy the required permission, isolation, evidence, or reliability boundary.

The presence of an anti-trigger is not a blanket exemption. The coordinator must apply it to the concrete eligible slice.

## Coordinator accountability

The Human-visible root retains responsibility for:

- current Task/Operational Contract authority;
- workspace/branch/worktree identity;
- final represented repository state;
- synthesis of child results;
- Code Review & Verify completion;
- final handoff accuracy;
- stop/re-entry when upstream specification/Design/Plan authority is defective.

Children are bounded implementation contexts. They do not become governance authorities, alternative Task Contracts, or independent lifecycle owners.

## Executor-owned orchestration

Subject to the controlling contract and safety boundaries, the Executor coordinator chooses:

- concrete decomposition;
- number of children;
- compatible built-in/custom worker roles;
- child context shape;
- sequential versus parallel execution;
- spawn/wait/follow-up/close mechanics;
- which eligible slice remains root-local when a documented anti-trigger dominates.

Agent Governance does not require `Explorer -> Worker -> Verifier`, any fixed child count, or any vendor-specific role graph by default.

## Write/isolation boundary

Delegation never widens task authority.

- A child may operate only inside the parent Task/Operational Contract scope.
- Child permissions may not exceed the authorized execution boundary merely because delegation is used.
- Parallel writable children require an explicitly safe ownership/isolation design; overlapping writable ownership is not the default.
- D058 worktree and one-writer safety remain controlling across concurrently writable work units.
- If exact child permission provenance is material, use the D063-qualified measurement boundary or stronger current supported evidence after version/capability revalidation.

## Handoff evidence

For new/materially revised `STANDARD` and `ASSURED` Task Contracts, final Executor evidence MUST make the delegation decision reconstructable without private chain-of-thought.

The handoff or Task-Contract-defined equivalent SHALL record compact fields equivalent to:

```text
delegation_posture: DELEGATED | ROOT_LOCAL | CONTRACT_FIXED
material_triggers_considered: [<semantic trigger labels>]
children_used: <integer>
child_purposes: [<concise bounded purposes>]
root_local_reason: <required when eligible work remained root-local>
```

This is a decision/evidence receipt, not an orchestration transcript. Child prompts, hidden reasoning, raw worker chats, and private host persistence are not required.

For `CONTRACT_FIXED`, the evidence should point to the persisted topology authority rather than restating it.

## Relationship to D041

D041 process autonomy remains valid for concrete implementation methodology and mechanics.

D065 narrows one semantic dimension:

```text
D041: Executor owns implementation process.
D065: when a material delegation trigger applies and no anti-trigger dominates,
      "do everything in the root" is no longer an unconstrained process choice.
```

The Executor still owns the concrete decomposition and tool mechanics.

## Relationship to D060

D060 remains controlling for Human-visible coordinator lifetime.

Delegation provides fresh technical contexts **inside** one task coordinator lifecycle. It is not a reason to open another Human-visible root. Child results are summarized back into the existing task root.

## Relationship to D055 and R007

D065 does not select root or child compute tiers.

- Human-facing root model/effort remains governed by D055.
- Child model/effort mapping remains the separate R007 question.
- Do not increase root compute merely to induce more proactive delegation.
- Do not infer that a delegated child used a provider-served backend profile unless the accepted evidence surface supports that stronger claim.

## Operational Contracts

Bounded repository operations are not required to create workers merely because an Executor root exists.

A mechanical, serial cleanup with deterministic Git/PR gates normally satisfies the small/serial anti-triggers and may be `ROOT_LOCAL`. An Operational Contract can require independent verification or another topology only when materially justified.

## T057 historical compatibility

T057 remains conforming and unchanged.

Its exact one-parent/one-child provider-backed topology was frozen experimental authority, so it was `CONTRACT_FIXED`. D065 is prospective and does not retroactively require additional children or reinterpret T057 evidence.

## Research disposition

R012 transitions to:

```text
Research-State: COMPLETE
Decision-State: DECIDED
Decision-Ref: docs/decisions/D065-semantic-executor-delegation-obligation.md
```

The adopted conclusion is narrower than exact choreography and stronger than pure optional delegation.

## Effective rule

For applicable non-trivial Executor work after D065 integration:

```text
material trigger + no dominating anti-trigger
=> delegate the eligible bounded slice

anti-trigger/safety constraint dominates
=> root-local allowed, with compact reason

contract fixes topology
=> follow the contract

HOW delegation is performed
=> Executor-owned
```

No Governance Core protocol version change is introduced by this source-maintenance decision.
