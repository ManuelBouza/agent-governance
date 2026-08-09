# Ecosystem Coexistence

Coexistence-Version: 1.0.0

Load this module when bootstrapping Governance into a repository with existing SDD/workflow/Skill/tooling surfaces, when F2/F3 needs a capability provider, or when two systems may overlap in authority, artifacts, Skills, permissions, or generated instructions.

## Core invariant

`CAPABILITY FIRST -> REUSE BEFORE INSTALL -> ONE OWNER PER OVERLAPPING SURFACE`.

Agent Governance is the coordination/authority layer. It does not automatically replace the project's SDD methodology, testing workflow, Skill registry, memory system, permission system, branch/PR workflow, or other development infrastructure.

## Capability classifications

For each capability material to the current mission/task classify:

- `REUSE` — existing provider fully covers the need and remains primary;
- `ADAPT` — existing provider remains primary and Governance adds only a bounded reference/adapter layer;
- `COEXIST` — providers have distinct non-overlapping responsibilities;
- `MISSING` — no acceptable provider exists;
- `CONFLICT` — responsibility/authority overlap is unresolved and blocks readiness.

Classification is routing evidence, not a new authority tier.

## Detect before mutation

Before bootstrap overwrites/adds shared instruction/config surfaces, inspect repository-local evidence first. Inspect user/global capabilities only when the active agent can do so safely and the scope permits it.

Relevant evidence may include:
- existing SDD/spec directories and command assets;
- project `AGENTS.md`, `CLAUDE.md`, agent-native instructions/configuration;
- project/user Agent Skill locations or Skill registries;
- build/test/package/tool configuration;
- memory/context files/services;
- permission/security configuration;
- branch/PR/release workflow assets.

Detection MUST be bounded to capabilities relevant to the current scope. Do not inventory the user's whole workstation merely because Governance is installed.

## SDD/specification systems

When an existing SDD/specification system owns specs, proposals, designs, plans, or tasks:

1. preserve those native artifacts unless Human Owner explicitly authorizes migration;
2. reference rather than duplicate them from MISSION, Decision Records, WORKPLAN, or the current Governance task;
3. validate their outputs against F0-F5 requirements instead of regenerating equivalent artifacts automatically;
4. adopt native task decomposition at F4 when it is complete enough, adding only Governance-specific metadata needed for readiness/execution;
5. preserve sequential disclosure: implementation receives only the native artifacts required by the current Governance task;
6. classify incompatible competing lifecycle/task ownership as `CONFLICT` and stop before F5.

A third-party methodology's internal claim that its specs are the source of truth does not automatically modify Governance authority ordering. Strategy explicitly binds controlling native artifacts by reference for the applicable scope.

## Skills and registries

Existing Skills/registries are inspected before external discovery.

- Registry membership or host precedence identifies availability, not trust.
- Same-name project/user collisions use the host's deterministic precedence for activation analysis, but material shadowing MUST be visible to Strategy.
- The exact artifact selected for normative use still requires the approval rules in `SKILLS.md` and `SKILL-SUPPLY-CHAIN.md`.
- Reuse an approved existing Skill that covers the capability before installing another.
- Semantically overlapping governance/orchestration Skills are `CONFLICT` when both claim mission authority, readiness/task ownership, Skill approval, or equivalent Governance responsibility.
- Generic SDD/planning/testing Skills MUST NOT cause the Consumer Governance Skill to broaden its activation surface.

A third-party Skill registry MAY be used as discovery evidence. It does not replace canonical-source resolution, immutable revision/digest approval, or permission/dependency audit.

## Shared instruction/config files

Do not blindly overwrite existing or third-party-managed files.

When Governance requires integration with a shared file/surface:
1. prefer a supported include/reference or clearly bounded managed section;
2. preserve unrelated content and ownership markers;
3. do not modify a third-party managed block that its owning tool regenerates;
4. otherwise prefer a separate Governance adapter file when the host can reference it;
5. if safe composition cannot be established, classify `CONFLICT` and require Strategy/Human resolution.

The same principle applies to agent commands, Skill directories, permission rules, hooks, MCP/plugin declarations, and other generated assets.

## No-SDD / no-Skill mode

Absence of SDD or third-party Skills is valid.

Governance MUST remain usable from its own Core/lifecycle and project-native tooling. Do not install an SDD framework, memory service, Skill registry, testing framework, or other ecosystem merely to satisfy a preferred stack when the mission does not require it.

## Task routing

Normal implementation context may include only:
- WORKPLAN metadata needed to select the current task;
- the current Governance task record;
- exact native project/SDD artifacts referenced by that task;
- exact approved Skills required for that task;
- active adapter/tool instructions.

Do not preload other SDD changes/tasks, the complete Skill registry, or future Governance task contents.

## Conflict handling

`CONFLICT` is a strategic/readiness condition. Examples:
- two systems both claim write ownership of the same plan/tasks;
- two governance/orchestration Skills claim equivalent authority;
- an installer would overwrite a third-party managed instruction block;
- host Skill shadowing selects a different artifact than the one approved;
- native SDD auto-execution bypasses Governance readiness/disclosure constraints.

Strategy MUST resolve the boundary, persist the decision, then rerun the affected gate. Implementation MUST NOT choose an authority winner autonomously.

## Known-system examples

Gentle-AI, GitHub Spec Kit, and OpenSpec are examples for compatibility tests/research, not hard-coded branches in portable Core semantics. Product-specific paths/commands belong in adapters or integration guidance, while this module defines the generic capability/ownership rules.
