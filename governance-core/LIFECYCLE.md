# Pre-Implementation Governance Lifecycle

Lifecycle-Version: 1.4.0

This file is part of the reusable Governance Core. It defines the mandatory lifecycle that must complete before implementation work becomes READY.

## Principle

Separate problem framing, viability, engineering strategy, Skill capability audit, atomic planning, readiness review, and implementation handoff. Decisions affecting future work are persisted as approved; final handoff is consolidation, not first persistence.

## Specification Quality Ownership

The Strategy/Governance role owns the quality of the execution contract delivered to Implementation.

A task MUST be designed and written so a competent Implementation Agent can complete it successfully using the task's disclosed context, exact approved Skills, repository evidence and normal technical judgment. The executor is responsible for implementation decisions, not for reconstructing missing strategy or guessing hidden requirements.

Before F5 may pass, Strategy MUST ensure each task provides enough information to determine:
- the result that must exist when the task is complete;
- scope and meaningful boundaries;
- dependencies and required prior outcomes;
- verifiable acceptance criteria;
- required approved Skills/capabilities;
- material constraints, risks and references needed for execution;
- which choices remain intentionally delegated to Implementation.

Do not over-specify implementation mechanics. The goal is a complete execution contract, not a code recipe.

If successful execution would require the Implementation Agent to infer unstated business intent, strategic architecture, acceptance meaning or hidden constraints, the task is not READY. Such ambiguity is a planning/readiness defect and must be resolved by Strategy before handoff.

## F0 — Frame
Question: what problem/result is being requested?

Define problem/need, desired outcome, known constraints, out-of-scope boundaries and unresolved strategic questions. Do not design implementation.

Gate F0 passes when the Human Owner and Strategy/Governance Agent share an unambiguous problem frame.

## F1 — Viability
Question: should/how can this problem reasonably be solved?

Assess functional viability, compatibility, dependencies, major risks, high-level alternatives, required research and materially simpler solutions.

Outcomes: `VIABLE`, `VIABLE_WITH_CONDITIONS`, `NEEDS_RESEARCH`, `NOT_RECOMMENDED`.

## F2 — Engineering Strategy
Question: what engineering principles and architectural boundaries should govern the solution?

May define system boundaries, architectural/design patterns, ownership, failure model, idempotency/concurrency, security/observability, testing, deployment/rollback and compatibility constraints.

Remain implementation-agnostic: define constraints/patterns, not filenames, methods, class names or agent-product syntax unless strategically required.

## F3 — Skill Capability Audit
Question: does the future Implementation Agent have exact approved expertise required to execute F2 correctly?

1. derive required capabilities from strategy;
2. inspect already-approved Skill artifacts first;
3. identify gaps;
4. discover external candidates under `SKILL-DISCOVERY.md` without installing them;
5. resolve every candidate to its canonical owner/repository/path and reject candidates whose provenance cannot be resolved;
6. apply `SKILL-SUPPLY-CHAIN.md` to the canonical artifact: pin an immutable revision/digest, quarantine, inspect all content/dependencies/permissions, and dynamically verify risky executable behavior when practical;
7. persist an approval record only for the exact audited artifact;
8. classify each mandatory capability `COVERED`, `MISSING`, or `NOT_REQUIRED`.

Directory ranking, install count, automated marketplace scan or listing by a vendor never establishes artifact approval. Discovery source and canonical provenance are separate facts.

Skills are selected for capabilities, independent of which compatible agent product executes the tasks.

F3 MUST NOT pass while a mandatory capability depends on an unresolved-provenance, unaudited or unapproved external Skill.

## F4 — Atomic Work Planning
Question: how should the approved solution be decomposed into independently verifiable work units?

Each task defines id, objective/result, scope/boundary, dependencies, acceptance criteria, required exact approved Skill IDs, material constraints/risks and execution-relevant references where needed.

Additionally define a deterministic execution order/queue containing metadata only. Detailed task content remains in separate task records.

Task records MUST be agent-product neutral. Vendor-specific tool syntax/configuration belongs to adapters or approved Skills unless the Human Owner explicitly makes a product a requirement.

Atomicity/quality criteria:
- one coherent result;
- independently verifiable within dependencies;
- bounded enough to diagnose/rework;
- no unrelated conceptual changes bundled together;
- acceptance strong enough for Implementation to mark DONE without strategic review;
- sufficient context to execute without hidden assumptions;
- technical design freedom remains with Implementation unless a choice is strategically controlling.

## F5 — Readiness Review
Question: can one Implementation Agent execute the authorized plan autonomously and sequentially without private chat context?

Verify:
- objective/result and scope are explicit and non-conflicting;
- controlling strategy required for execution is represented or directly referenced;
- acceptance criteria are unambiguous and evidentially verifiable;
- required Skills refer to exact APPROVED canonical artifacts and their approved permission/dependency envelope is compatible with the task;
- dependency graph and deterministic execution order are coherent;
- material safety/production risks are bounded;
- tasks are agent-product neutral;
- future task content can remain undisclosed until the preceding task is DONE;
- normal technical failures can be resolved inside Implementation responsibility;
- no task requires the executor to invent missing requirements or strategic intent;
- a cold-start compatible agent can determine exactly what is currently allowed and what success means.

If any requirement fails, reopen the appropriate earlier phase. Do not use executor discretion to compensate for a defective task contract or unaudited Skill.

Gate F5 passes with `READY_FOR_IMPLEMENTATION`.

## F6 — Persist and Handoff
Question: is the approved plan durably recorded and safe for autonomous sequential execution?

F6 introduces no new strategy. It MUST:
- persist controlling decisions and strategic records;
- ensure WORKPLAN contains the execution metadata/order and task record pointers;
- ensure required Skill approval records identify exact audited canonical artifacts;
- refresh STATE;
- ensure EXCHANGE contains required gate/decision events;
- ensure a Git revision exists for handoff;
- mark only the first eligible task READY;
- authorize automatic PLANNED -> READY progression for later tasks under EXECUTION rules after predecessors are DONE;
- make the next permitted action unambiguous.

After F6, the Implementation Agent continues through the full authorized sequence without inter-task Strategy/Human approval unless a valid blocker, human intervention, or explicit pre-approved external gate stops it.

## Continuous Persistence

Persistence occurs throughout F0-F5. Approved decisions may later be superseded explicitly; never silently rewrite their meaning.

## Lifecycle Re-entry

This lifecycle is gated, not a rigid waterfall. F3 may reopen F2; F4 may reopen F2; F5 may reopen any earlier phase. Re-entry is explicit and controlling decisions are persisted.

## Core Invariant

Implementation receives a complete, distilled execution contract one task at a time, not the full strategic debate or future task contents. Strategy owns correctness/completeness of that contract and canonical provenance/approval of every required Skill; Implementation owns how to realize the task technically within delegated boundaries.
