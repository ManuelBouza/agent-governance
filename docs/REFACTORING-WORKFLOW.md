# Refactoring Workflow

Status: ACTIVE

## Purpose

Define the repository-specific workflow for restructuring `agent-governance` without changing its externally observable behavior or governance semantics.

A change that intentionally changes behavior, protocol semantics, authority, compatibility, or acceptance outcomes is NOT a refactor and must use `DEVELOPMENT-WORKFLOW.md` as a behavior-changing product change.

All refactor mutation occurs inside the branch lifecycle defined by `docs/BRANCHING.md`.

## Why this workflow

Safe refactoring depends on small behavior-preserving transformations and a known-good verification baseline. This repository uses ChatGPT to define/refine the semantic contract and an agent-product-neutral Agente de IA Ejecutor to implement and verify it.

## Branch precondition

Normal refactors start from current `develop` on a short-lived `refactor/<slug>` branch and return to `develop` through PR after RF5 acceptance.

Do not refactor directly on `main` or `develop`. A hotfix that requires structural work is exceptional and follows `docs/BRANCHING.md` without weakening the RF invariants below.

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

The Agente de IA Ejecutor inspects the affected surface before implementation.

The executor MUST:
1. identify existing tests/evals that characterize the behavior;
2. add focused characterization tests/evals when material behavior is insufficiently covered;
3. execute the relevant suite against the pre-refactor revision;
4. establish a green baseline before refactoring begins;
5. return the baseline test/eval diff, commands, and evidence to ChatGPT when new characterization was added.

Once ChatGPT accepts the baseline, it becomes frozen for that refactor unit. The executor MUST NOT weaken, remove, or reinterpret that baseline after RF3 begins unless ChatGPT explicitly authorizes a baseline correction.

If the baseline is already failing, the failure must be resolved or explicitly isolated before the refactor. Do not use a refactor to hide an unrelated defect.

For Markdown/protocol structure refactors, characterization may include deterministic reference/layout/invariant tests and focused agent evals where semantics cannot be proven mechanically.

## RF2 — Atomic Refactor Contract

ChatGPT decomposes the refactor into the smallest coherent, independently reviewable units practical.

Each unit states:
- target structure/code smell;
- behavior/invariants that must remain unchanged;
- affected files/surface;
- explicit exclusions;
- frozen characterization baseline/reference;
- verification required after the unit.

Do not mix feature work, bug fixes, protocol behavior changes, dependency upgrades, or unrelated cleanup into the same refactor unit.

## RF3 — Apply Refactor

Ownership depends on artifact type:

### Executable/configuration/test infrastructure refactor
The Agente de IA Ejecutor performs the authorized non-Markdown refactor and may update test/eval implementation only when the refactor target itself is test/eval structure or when an RF1 baseline correction was explicitly approved before this phase.

### Markdown/instruction refactor
ChatGPT performs the Markdown refactor because committed Markdown is ChatGPT-owned. The Agente de IA Ejecutor may then run the frozen tests/evals as verification.

No named executor product has special ownership. OpenCode, Codex, Claude Code, Antigravity, or another compatible agent may fulfill the executor role.

## RF4 — Verification

After each atomic refactor unit, the Agente de IA Ejecutor runs the frozen characterization/regression suite plus any additional non-contract-changing checks appropriate to the refactor.

Required result: the same behavioral contract remains satisfied.

If a test/eval fails:
- implementation regression -> executor fixes the refactor within the approved contract;
- genuine pre-existing test/eval defect -> stop and return to ChatGPT before changing the frozen baseline;
- ambiguity over intended behavior -> stop and return to ChatGPT;
- discovered need for changed behavior -> terminate the refactor classification and re-enter normal product development.

Never change the frozen baseline merely because the refactored implementation prefers different behavior.

For higher-risk refactors ChatGPT MAY request verification from a fresh executor session or a second compatible executor product. This is additional independence of execution, not a distinct governance role.

## RF5 — Structural Review

ChatGPT reviews whether the refactor actually improved the intended structural property without increasing hidden complexity or coupling.

Check at minimum:
- behavior remained stable;
- architecture/progressive-context boundaries remain coherent;
- duplication and indirection did not simply move elsewhere;
- public compatibility was not changed accidentally;
- Markdown/executor write boundaries were respected;
- frozen baseline remained intact;
- executor verification is green;
- topic branch and PR target comply with `docs/BRANCHING.md`.

## RF6 — Integrate

Integrate the refactor only after RF5 acceptance.

Normal integration is `refactor/<slug>` -> `develop` through PR, preferably squash merged as one coherent refactor unit. Each accepted unit must leave the repository in a working state so rollback and diagnosis remain straightforward.

## Special rule: Core Markdown refactoring

Because much of the Governance Core is Markdown, a refactor can be behaviorally significant even when no executable code changes.

For Core Markdown:
- ChatGPT owns every wording/structure edit;
- semantic invariants must be explicit before editing;
- the Agente de IA Ejecutor owns structural/reference tests and relevant agent eval execution;
- moving a normative rule between modules must preserve authority, routing, direct references, and progressive-loading behavior;
- if wording changes interpretation rather than structure, treat it as a protocol change, not a refactor.

## Core invariant

Refactoring safety comes from an explicit ChatGPT-owned invariant contract plus a pre-change characterization baseline that the Agente de IA Ejecutor cannot silently move after implementation starts. Executor product identity is irrelevant.
