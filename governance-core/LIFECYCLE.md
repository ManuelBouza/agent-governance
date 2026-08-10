# Pre-Implementation Governance Lifecycle

Lifecycle-Version: 1.6.0

This file is part of the reusable Governance Core. It defines the mandatory lifecycle that must complete before implementation work becomes READY.

## Principle

Separate problem framing, viability, engineering strategy, ecosystem/capability reuse, Skill capability audit, atomic planning, readiness review, and implementation handoff. Decisions affecting future work are persisted as approved; final handoff is consolidation, not first persistence.

Human-facing communication and engineering rigor are separate planes. Use `INTERACTION.md` to translate between the Human Owner's current register and engineering execution. Apply `QUALITY.md` as a silent-by-default quality envelope. Before implementation readiness, present the intended solution graphically through the Primary Solution Diagram required by `QUALITY.md`.

## Specification Quality Ownership

The Strategy/Governance role owns the quality of the execution contract delivered to Implementation.

A task MUST be designed and written so a competent Implementation Agent can complete it successfully using the task's disclosed context, exact approved Skills, referenced project-native artifacts, repository evidence and normal technical judgment. The executor is responsible for implementation decisions, not for reconstructing missing strategy or guessing hidden requirements.

Before F5 may pass, Strategy MUST ensure each task provides enough information to determine:
- the result that must exist when the task is complete;
- scope and meaningful boundaries;
- dependencies and required prior outcomes;
- verifiable acceptance criteria;
- required approved Skills/capabilities;
- material constraints, risks and references needed for execution;
- material quality/security/privacy/reliability/operational constraints derived from `QUALITY.md`;
- which project-native SDD/spec artifacts are controlling for this task, when any;
- which choices remain intentionally delegated to Implementation.

Do not over-specify implementation mechanics. The goal is a complete execution contract, not a code recipe.

If successful execution would require the Implementation Agent to infer unstated business intent, strategic architecture, acceptance meaning or hidden constraints, the task is not READY. Such ambiguity is a planning/readiness defect and must be resolved by Strategy before handoff.

## Interaction and Quality Overlay

`INTERACTION.md` and `QUALITY.md` apply across F0-F6 rather than creating new lifecycle phases.

Strategy SHALL:

- infer the Human Owner's current interaction register from the current request/context and adapt presentation accordingly;
- preserve semantic intent while translating natural/domain/technical/code-native requests into engineering constraints;
- keep presentation complexity independent from engineering quality;
- triage every implementation scope through the quality envelope even when the Human Owner did not name those dimensions;
- surface only material quality/risk/tradeoff concerns by default;
- present the Primary Solution Diagram before F5 can pass;
- refresh the diagram and affected strategy if a material design boundary changes before implementation.

These overlays must not become a large mandatory user-facing checklist or a redundant approval ceremony.

## F0 — Frame
Question: what problem/result is being requested?

Define problem/need, desired outcome, known constraints, out-of-scope boundaries and unresolved strategic questions. Do not design implementation.

Normalize the Human Owner's request under `INTERACTION.md` without forcing them to use engineering vocabulary. Preserve the requested result and acceptance meaning; ask for clarification only when multiple plausible interpretations would materially change outcome, scope, risk or acceptance.

When the repository already contains an SDD/specification/workflow system that materially defines the requested scope, identify the relevant native artifact/provider and load `COEXISTENCE.md` only as needed to decide whether Governance should `REUSE`, `ADAPT`, `COEXIST`, or flag `CONFLICT`. Do not regenerate equivalent specifications merely because Governance is present.

Gate F0 passes when the Human Owner and Strategy/Governance Agent share an unambiguous problem frame and any material authority/source conflict for that frame is resolved.

## F1 — Viability
Question: should/how can this problem reasonably be solved?

Assess functional viability, compatibility, dependencies, major risks, high-level alternatives, required research and materially simpler solutions.

Existing compatible project-native capabilities are part of viability evidence and SHOULD be preferred over introducing redundant tooling/workflows.

Identify early any quality/security/privacy/safety constraint under `QUALITY.md` that could make the requested result infeasible, materially more expensive/risky, or dependent on a Human decision. Do not expand every baseline quality check into visible discussion.

Outcomes: `VIABLE`, `VIABLE_WITH_CONDITIONS`, `NEEDS_RESEARCH`, `NOT_RECOMMENDED`.

## F2 — Engineering Strategy
Question: what engineering principles and architectural boundaries should govern the solution?

Define system boundaries, architectural/design patterns, ownership, failure model, idempotency/concurrency, security/privacy, reliability/observability, testing, performance/resource constraints, deployment/rollback, compatibility and other material quality constraints by applying `QUALITY.md`.

The quality envelope is mandatory triage even when the Human Owner did not mention its dimensions. Only material outcomes need to be carried into decisions/task contracts; `BASELINE`/`NOT_APPLICABLE` checks need not become user-visible ceremony.

For every material capability/provider decision, inspect project-native capabilities first under `COEXISTENCE.md`. Prefer `REUSE` or `ADAPT` over installing/replacing a capability that is already adequate. `CONFLICT` must be resolved strategically before planning proceeds.

Remain implementation-agnostic: define constraints/patterns, not filenames, methods, class names or agent-product syntax unless strategically required.

### F2 graphical solution view

Before F2 is considered complete for an implementation scope, Strategy SHALL prepare and present the Primary Solution Diagram defined by `QUALITY.md`.

Select the smallest useful diagram based on the dominant design question rather than forcing one notation onto all work. C4 is the default architecture family; dynamic/sequence, state, data-flow/trust-boundary, data-model or compact flow/dependency views are used where they communicate the change more accurately.

The diagram:

- shows the proposed solution and change boundary;
- is consistent with F2 strategy;
- is communicated at the Human Owner's current register under `INTERACTION.md`;
- exposes material dependencies/trust boundaries when relevant;
- does not add an extra Human approval gate unless Human/project policy explicitly requires one.

A material strategy/design change after presentation invalidates the affected view until it is refreshed.

## F3 — Skill Capability Audit
Question: does the future Implementation Agent have exact approved expertise required to execute F2 correctly?

1. derive required capabilities from strategy, including specialist capabilities required by material `QUALITY.md` constraints;
2. inspect already-present project/user Skills, existing project Skill registries and already-approved Skill artifacts first;
3. use `COEXISTENCE.md` to identify same-name/semantic overlap, host shadowing and whether an existing capability should be reused;
4. identify gaps;
5. discover external candidates under `SKILL-DISCOVERY.md` without installing them;
6. resolve every candidate to its canonical owner/repository/path and reject candidates whose provenance cannot be resolved;
7. apply `SKILL-SUPPLY-CHAIN.md` to the canonical artifact: pin an immutable revision/digest, quarantine, inspect all content/dependencies/permissions, and dynamically verify risky executable behavior when practical;
8. persist an approval record only for the exact audited artifact;
9. classify each mandatory capability `COVERED`, `MISSING`, or `NOT_REQUIRED`.

Host/registry precedence tells Strategy which Skill artifact may activate; it does not establish trust. Material shadowing or semantic overlap that would select an unapproved/conflicting artifact blocks F3 until resolved.

Directory ranking, install count, automated marketplace scan or listing by a vendor never establishes artifact approval. Discovery source and canonical provenance are separate facts.

Skills are selected for capabilities, independent of which compatible agent product executes the tasks.

F3 MUST NOT pass while a mandatory capability depends on an unresolved-provenance, unaudited, unapproved, shadow-conflicted or authority-conflicting external Skill.

## F4 — Atomic Work Planning
Question: how should the approved solution be decomposed into independently verifiable work units?

Each task defines id, objective/result, scope/boundary, dependencies, acceptance criteria, required exact approved Skill IDs, material constraints/risks and execution-relevant references where needed.

Material `QUALITY.md` requirements are assigned to the smallest tasks that can implement and verify them. Do not create separate quality/security tasks solely to move cross-cutting responsibility out of the implementation that introduces the risk unless separation is strategically justified.

Additionally define a deterministic execution order/queue containing metadata only. Detailed task content remains in separate task records.

When an existing SDD system already provides suitable task decomposition, Strategy MAY adopt/reference its current-task artifacts instead of duplicating the decomposition. The Governance task record still carries the minimal governance execution envelope required for ordering, authority, Skill IDs, disclosure and acceptance routing; detailed native content is referenced rather than mirrored.

Task records MUST be agent-product neutral. Vendor-specific tool syntax/configuration belongs to adapters or approved Skills unless the Human Owner explicitly makes a product a requirement.

Atomicity/quality criteria:
- one coherent result;
- independently verifiable within dependencies;
- bounded enough to diagnose/rework;
- no unrelated conceptual changes bundled together;
- acceptance strong enough for Implementation to mark DONE without strategic review;
- sufficient context to execute without hidden assumptions;
- referenced native artifacts identify a single controlling source for their concern;
- material quality/security/privacy/operational requirements are attached to the work that creates or mitigates them;
- technical design freedom remains with Implementation unless a choice is strategically controlling.

## F5 — Readiness Review
Question: can one Implementation Agent execute the authorized plan autonomously and sequentially without private chat context?

Verify:
- objective/result and scope are explicit and non-conflicting;
- controlling strategy required for execution is represented or directly referenced;
- acceptance criteria are unambiguous and evidentially verifiable;
- the `QUALITY.md` envelope was triaged and every material dimension is represented in strategy/task constraints/acceptance/evidence as needed;
- mandatory security triage is complete and any required threat/security design exists before implementation;
- privacy/data constraints are represented independently when sensitive data is material;
- the Primary Solution Diagram has been presented and still matches the implementation-relevant solution boundary;
- required Skills refer to exact APPROVED canonical artifacts and their approved permission/dependency envelope is compatible with the task;
- any relevant host Skill shadowing resolves to the exact approved artifact;
- dependency graph and deterministic execution order are coherent;
- material safety/production risks are bounded;
- tasks are agent-product neutral;
- future task content can remain undisclosed until the preceding task is DONE;
- native SDD/spec artifacts required by the current task can be disclosed without preloading unrelated/future work;
- no unresolved `CONFLICT` exists between Governance and existing SDD/Skill/tooling ownership/authority;
- normal technical failures can be resolved inside Implementation responsibility;
- no task requires the executor to invent missing requirements or strategic intent;
- a cold-start compatible agent can determine exactly what is currently allowed and what success means.

If any requirement fails, reopen the appropriate earlier phase. Do not use executor discretion to compensate for a defective task contract, conflicting methodology boundary, unaudited Skill, missing material quality constraint or stale solution diagram.

Gate F5 passes with `READY_FOR_IMPLEMENTATION`.

## F6 — Persist and Handoff
Question: is the approved plan durably recorded and safe for autonomous sequential execution?

F6 introduces no new strategy. It MUST:
- persist controlling decisions and strategic records;
- ensure material quality constraints and the current solution-design reference are durable when future agents need them;
- ensure WORKPLAN contains the execution metadata/order and task record pointers;
- ensure each current task references only the native SDD/spec artifacts required for that task;
- ensure required Skill approval records identify exact audited canonical artifacts;
- refresh STATE;
- ensure EXCHANGE contains required gate/decision events;
- ensure a Git revision exists for handoff;
- mark only the first eligible task READY;
- authorize automatic PLANNED -> READY progression for later tasks under EXECUTION rules after predecessors are DONE;
- make the next permitted action unambiguous.

After F6, the Implementation Agent continues through the full authorized sequence without inter-task Strategy/Human approval unless a valid blocker, human intervention, material design/quality invalidation, or explicit pre-approved external gate stops it.

## Continuous Persistence

Persistence occurs throughout F0-F5. Approved decisions may later be superseded explicitly; never silently rewrite their meaning.

## Lifecycle Re-entry

This lifecycle is gated, not a rigid waterfall. F3 may reopen F2; F4 may reopen F2; F5 may reopen any earlier phase. Discovery of a new ecosystem/ownership conflict reopens the earliest phase whose assumptions it invalidates. A newly discovered material security/privacy/reliability/quality issue or a material design change that invalidates the Primary Solution Diagram likewise reopens the earliest affected phase. Re-entry is explicit and controlling decisions are persisted.

## Core Invariant

Implementation receives a complete, distilled execution contract one task at a time, not the full strategic debate, whole external SDD workspace, internal quality checklist or future task contents. Strategy owns correctness/completeness of that contract, user-intent translation, quality/readiness boundaries, graphical solution communication, ecosystem/provider boundaries and canonical provenance/approval of every required Skill; Implementation owns how to realize the task technically within delegated boundaries.
