# Refactoring Workflow

Status: ACTIVE

## Purpose

Define the repository-specific workflow for restructuring `agent-governance` without changing its externally observable behavior or governance semantics.

A change that intentionally changes behavior, protocol semantics, authority, compatibility, or acceptance outcomes is NOT a refactor and must use `DEVELOPMENT-WORKFLOW.md` as a behavior-changing product change.

## Why this workflow

Safe refactoring depends on small behavior-preserving transformations and a known-good verification baseline. This repository strengthens that model by separating specification, implementation, and verification ownership across agents.

## RF0 — Classify and Define Invariants

ChatGPT determines that the proposed work is genuinely behavior-preserving and records the invariants that must remain true.

Examples:
- public protocol meaning is unchanged;
- CLI/API behavior is unchanged;
- installed footprint semantics are unchanged;
- file/reference routing still resolves correctly;
- Skill activation/operation semantics are unchanged;
- no new permissions, dependencies, or external effects are introduced.

If intended behavior changes, stop and use the normal product-development flow.

## RF1 — Characterization Baseline

Codex inspects the affected surface before implementation.

Codex MUST:
1. identify existing tests/evals that characterize the behavior;
2. add focused characterization tests/evals when material behavior is insufficiently covered;
3. execute the relevant suite against the pre-refactor revision;
4. establish a green baseline before refactoring begins.

If the baseline is already failing, the failure must be resolved or explicitly isolated before the refactor. Do not use a refactor to hide an unrelated defect.

For Markdown/protocol structure refactors, characterization may include deterministic reference/layout/invariant tests and focused agent evals where semantics cannot be proven mechanically.

## RF2 — Atomic Refactor Contract

ChatGPT decomposes the refactor into the smallest coherent, independently reviewable units practical.

Each unit states:
- target structure/code smell;
- behavior/invariants that must remain unchanged;
- affected files/surface;
- explicit exclusions;
- Codex verification required after the unit.

Do not mix feature work, bug fixes, protocol behavior changes, dependency upgrades, or unrelated cleanup into the same refactor unit.

## RF3 — Apply Refactor

Ownership depends on artifact type:

### Executable/configuration refactor
The Implementation Executor performs the refactor and edits only its authorized non-test, non-Markdown surface.

### Markdown/instruction refactor
ChatGPT performs the refactor because committed Markdown is ChatGPT-owned. The Implementation Executor is not inserted merely to satisfy a generic workflow.

### Test/eval refactor
Codex performs the refactor when the change concerns test/eval structure only and does not alter what product behavior is required.

No role may mutate another role's owned surface merely because the refactor spans multiple categories; split the work into ordered units instead.

## RF4 — Independent Verification

After each atomic refactor unit, Codex runs the relevant characterization/regression suite.

Required result: the same behavioral contract remains satisfied.

If a test/eval fails:
- implementation regression -> return the unit to the Implementation Executor or ChatGPT for Markdown-owned changes;
- genuine test/eval defect -> Codex may repair it only when the pre-refactor behavior and approved invariant demonstrate the test was wrong;
- ambiguity over intended behavior -> stop and return to ChatGPT;
- discovered need for changed behavior -> terminate the refactor classification and re-enter normal product development.

Never change a test merely because the new implementation prefers different behavior.

## RF5 — Structural Review

ChatGPT reviews whether the refactor actually improved the intended structural property without increasing hidden complexity or coupling.

Check at minimum:
- behavior remained stable;
- architecture/progressive-context boundaries remain coherent;
- duplication and indirection did not simply move elsewhere;
- public compatibility was not changed accidentally;
- role/write boundaries were respected;
- Codex verification is green.

## RF6 — Integrate

Integrate the refactor only after RF5 acceptance.

Prefer small standalone refactor PRs/commits. Each accepted unit must leave the repository in a working state so rollback and diagnosis remain straightforward.

## Special rule: Core Markdown refactoring

Because much of the Governance Core is Markdown, a refactor can be behaviorally significant even when no executable code changes.

For Core Markdown:
- ChatGPT owns every wording/structure edit;
- semantic invariants must be explicit before editing;
- Codex owns structural/reference tests and relevant agent evals;
- moving a normative rule between modules must preserve authority, routing, direct references, and progressive-loading behavior;
- if wording changes interpretation rather than structure, treat it as a protocol change, not a refactor.

## Core invariant

The agent that performs a product refactor does not own the evidence that proves it safe, except when the changed artifact itself is in Codex's test/eval ownership surface. Verification remains an independent handoff before acceptance.
