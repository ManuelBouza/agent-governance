# D026 — Ecosystem coexistence and capability reuse

Status: ACCEPTED
Authority: Human Owner

## Decision

Agent Governance SHALL integrate into consumer repositories using a **capability-first, reuse-before-install, no-authority-collision** policy.

A repository may already use a Spec-Driven Development (SDD) system, Agent Skills, memory/context tooling, permissions, testing workflows, branch/release helpers, or other agent-development infrastructure. Agent Governance MUST detect and classify those capabilities before adding overlapping project-local behavior.

Agent Governance is a governance/coordination layer. It MUST NOT replace a project's development methodology merely because Governance is installed.

## Core rules

1. **Detect before adding** — inspect project-local and, where relevant/authorized, user-level capabilities before proposing new Skills, SDD workflows, adapters, or tooling.
2. **Classify capabilities, not product names** — Gentle-AI, Spec Kit, OpenSpec, custom SDD, native agent workflows, and no-SDD repositories are examples, not hard-coded governance roles.
3. **Reuse before install** — if an existing capability satisfies the required function and is compatible with Governance, reuse it rather than installing a duplicate.
4. **Adapt instead of mirror** — when an existing system owns specs/plans/tasks, Governance references/adapts those artifacts instead of generating a parallel source of truth for the same intent.
5. **One writer per artifact/capability boundary** — two systems MUST NOT concurrently own the same specification, task lifecycle, Skill identity, permission block, or generated agent instruction surface without an explicit integration decision.
6. **Governance authority remains distinct** — external SDD/Skill/tool instructions cannot override the Human Owner, Governance Core, mission authority, readiness/acceptance gates, Skill supply-chain policy, or task disclosure rules.
7. **No-SDD is valid** — Agent Governance MUST work when no SDD framework or third-party Skill ecosystem is installed; it MUST NOT install one by default.
8. **Conflicts fail closed** — unresolved semantic/authority overlap is a planning/readiness blocker rather than permission to let competing systems both act.

## Capability inventory

Before governance bootstrap materially mutates a consumer repository, and again when F2/F3 requirements expose a relevant capability question, Strategy SHALL inventory only the capabilities material to the current scope.

At minimum the inventory model can represent:
- requirements/specification/SDD;
- engineering planning/task decomposition;
- implementation orchestration;
- testing/TDD/verification;
- Skill discovery/registry/activation;
- persistent memory/context mechanisms;
- agent permissions/security controls;
- Git branch/PR/release workflows;
- documentation/research/tool integrations when material.

Each relevant capability is classified as one of:
- `REUSE` — existing capability is sufficient and remains the primary provider;
- `ADAPT` — existing capability remains primary, with a bounded Governance adapter/reference layer;
- `COEXIST` — distinct non-overlapping responsibilities can operate side by side;
- `MISSING` — no suitable capability exists;
- `CONFLICT` — overlap/authority ambiguity must be resolved before readiness.

The inventory is evidence/routing state, not a new authority tier.

## SDD coexistence

When a consumer repository already uses an SDD/specification system:

- its existing specifications/plans/task artifacts remain native to that system unless the Human Owner explicitly chooses a migration;
- Governance MAY treat those artifacts as controlling project evidence by referencing them from MISSION, Decision Records, WORKPLAN, or the current task contract;
- Governance MUST NOT copy full native specifications/tasks into parallel Governance artifacts merely to make them "owned" by Governance;
- Governance validates that the native outputs satisfy F0-F5 requirements and adds only missing governance metadata/boundaries;
- when native task decomposition is sufficient, F4 may adopt/reference it rather than generate a second decomposition;
- when native SDD phases conflict with Governance readiness, authority, or disclosure invariants, Strategy records the conflict and blocks until a single operating boundary is chosen.

### Known examples

These examples are evidence for the generic model, not permanent product-specific branches in the Core.

- **Gentle-AI** already provides SDD orchestration, testing-capability detection, a Skill registry, persistent memory, permissions, and agent-specific integration. Governance should normally reuse those capabilities where compatible instead of installing equivalent SDD/testing/registry mechanisms.
- **GitHub Spec Kit** provides a Spec -> Plan -> Tasks -> Implement workflow plus extensions/presets/workflows. Governance should reference/adapt resulting artifacts and gates rather than maintain duplicate specs/plans/tasks.
- **OpenSpec** maintains current specs plus change artifacts/proposals/design/tasks. Governance should reference those artifacts as project evidence and add only governance-specific authority/readiness/execution controls.
- **No SDD framework** is also supported. Governance's own F0-F6 lifecycle remains sufficient and no external SDD installation is implied.

## Skill coexistence

Existing Agent Skills are capability candidates, not automatically approved guidance.

During F3:
1. inspect already-present project/user Skills and existing registries first;
2. map them to required capabilities;
3. apply deterministic host precedence only to identify which artifact would activate, never as trust evidence;
4. audit the exact selected artifact under `SKILL-SUPPLY-CHAIN.md` before normative use;
5. if an existing audited Skill covers the capability, reuse it rather than installing another;
6. if two Skills have overlapping names/descriptions or authority claims, classify the case `CONFLICT` until deterministic precedence plus semantic scope are acceptable;
7. project-level shadowing of a user-level Skill is observable behavior that must be recorded/reviewed when material, not silently assumed safe.

An external Skill registry such as Gentle-AI's registry MAY be used as a discovery/index input. Its selection/precedence is not approval; Governance still binds approval to the exact canonical audited artifact revision/digest.

## Consumer Governance Skill collision rule

Before installing/activating the Consumer Governance Skill in a repository with existing Skills or orchestration instructions:
- inspect same-name and semantically overlapping governance/orchestration Skills;
- do not silently shadow or replace them;
- prefer coexistence only when responsibilities are distinct;
- require an explicit Human/Strategy decision when two systems both claim mission authority, readiness/task ownership, Skill approval, or equivalent governance responsibility.

Trigger/near-miss evals MUST include repositories containing other SDD/orchestration Skills so the Consumer Governance Skill does not activate as a generic planning/SDD Skill.

## Generated instruction/config surfaces

Agent Governance MUST preserve repository-native and third-party managed instruction/config files.

Installation/adaptation MUST NOT blindly replace files such as `AGENTS.md`, `CLAUDE.md`, agent command/skill directories, OpenCode configuration, Spec Kit/OpenSpec/Gentle-AI managed files, or equivalent surfaces.

When an adapter needs a shared file:
- prefer a bounded reference/include/managed section supported by that ecosystem;
- preserve unrelated content;
- do not edit third-party managed blocks that will be regenerated by their owner;
- if safe composition is not possible, use a separate project-local adapter file and point the host to it when supported;
- otherwise block and require an explicit integration decision.

## Authority and artifact ownership

A foreign system's claim that its specs are "truth" applies inside its methodology, but it does not automatically change Agent Governance authority ordering.

Strategy explicitly binds native project artifacts into Governance by reference when they are controlling for a mission/task. Their requirement content then controls that scope through the referencing MISSION/Decision Record/task contract, while Governance continues to own coordination semantics such as lifecycle gates, task readiness, Skill approval, handoff, and disclosure.

This creates composition rather than competing global authorities.

## Implementation routing

For each current implementation task, disclose only:
- the Governance task envelope/current task record;
- exact referenced native SDD/spec artifacts required for that task;
- exact approved Skills required for that task;
- adapter/tool instructions needed for the active executor.

Do not preload the full SDD project history, all native tasks, all Skills, or future Governance tasks.

## Research basis

### Agent Skills client implementation

https://agentskills.io/client-implementation/adding-skills-support

Relevant guidance:
- discover project-level and user-level Skills;
- project-level Skills conventionally override same-name user-level Skills;
- collisions should use deterministic precedence and emit a warning;
- progressive disclosure loads only metadata first and full Skill instructions only when activated;
- project-level Skill loading should consider repository trust.

Agent Governance adopts deterministic collision visibility and progressive disclosure but adds its own artifact-specific supply-chain approval gate.

### Agent Skills description optimization / best practices

https://agentskills.io/skill-creation/optimizing-descriptions
https://agentskills.io/skill-creation/best-practices

Relevant guidance:
- over-broad Skill descriptions trigger when they should not;
- coherent, well-scoped Skills reduce overlap;
- detailed content should be progressively disclosed rather than making one broad activation surface.

### Gentle-AI

https://github.com/Gentleman-Programming/gentle-ai
https://github.com/Gentleman-Programming/gentle-ai/blob/main/docs/intended-usage.md
https://github.com/Gentleman-Programming/gentle-ai/blob/main/docs/usage.md

Relevant current behavior:
- Gentle-AI configures SDD, memory, Skills, MCP/tooling, permissions and agent integrations;
- `/sdd-init` detects stack/testing capabilities;
- its Skill registry scans project/user Skill locations and project conventions;
- project-local same-name Skills win over global Skills;
- its orchestrator passes exact selected `SKILL.md` paths to sub-agents.

These are reasons to reuse/compose rather than install duplicate Governance-owned equivalents.

### GitHub Spec Kit

https://github.com/github/spec-kit/blob/main/docs/index.md
https://github.com/github/spec-kit/blob/main/docs/reference/overview.md

Relevant current behavior:
- default SDD flow is Spec -> Plan -> Tasks -> Implement;
- integrations, extensions, presets and workflows are explicit extensibility surfaces;
- only one agent integration is active per project at a time while multiple extensions/presets can coexist.

### OpenSpec

https://github.com/Fission-AI/OpenSpec
https://github.com/Fission-AI/OpenSpec/blob/main/docs/overview.md

Relevant current behavior:
- specs are maintained as the current behavior source;
- a change is a bounded unit holding proposal/spec/design/task artifacts;
- OpenSpec intentionally acts as a specification/agreement layer over coding assistants.

## Consequences

- add a focused Governance Core coexistence module and route to it only when ecosystem/capability integration matters;
- bootstrap/F0/F2/F3 must inspect relevant existing capabilities before proposing additions;
- Skill discovery starts from installed/project-owned candidates before public discovery, consistent with existing Core policy;
- Consumer Skill installation/validation must include non-destructive coexistence checks;
- future deterministic tooling SHOULD support a compact capability/coexistence inventory without placing it in STATE;
- tests/evals must include Gentle-AI-like, Spec Kit-like, OpenSpec-like, generic custom-SDD, overlapping-Skill, and no-SDD synthetic fixtures;
- D025's consumer `reuse project-native tooling` rule extends to SDD/Skills/orchestration capabilities;
- T001's final readiness blocker is resolved by this decision; T001 may be moved to `READY` only after its Task Contract is reconciled with D026 and the new Core coexistence module.
