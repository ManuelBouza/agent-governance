---
name: consumer-governance
description: Operate Agent Governance inside an adopting repository for explicit governance bootstrap, validation, state reconstruction, mission/state/event/handoff work, coexistence inspection, Governance Skill discovery or audit, and sequential-disclosure readiness. Do not use for generic planning, coding, testing, refactoring, releases, generic SDD workflows, generic Skill installation, or source-product maintenance.
---

# Consumer Governance Skill

Use this Skill only for explicit Agent Governance work in an adopting repository. Repository authority and installed Governance Core remain authoritative; this Skill is routing and operational guidance, not a replacement authority.

## Activation boundary

Activate for explicit requests to:

- bootstrap or install Agent Governance in an adopting repository;
- validate an installed governance instance or reconstruct its current frontier without relying on prior chat history;
- initialize or advance governance mission/state/event/handoff records;
- inspect coexistence with existing SDD, Skill, testing, memory/context, permission, branch/PR, or orchestration capabilities;
- discover or audit Governance-related external Skill artifacts under the installed supply-chain rules;
- validate sequential disclosure, current-task readiness, dependency state, or governance handoff boundaries.

Do not activate merely because Governance is present. In particular, do not activate for ordinary application implementation, generic planning/coding/testing/refactoring/release work, generic spec/plan/tasks workflows, generic Skill installation, or maintenance of the canonical `agent-governance` source product.

## Authority and source independence

Treat the adopting repository's installed `.agent-governance/GOVERNANCE.md` as the protocol entry point and follow its routed modules. Project authority/state remains in `.agent-coordination/` and project-native sources referenced from it.

If this Skill conflicts with installed Governance Core, project authority records, or compatible project-native ownership, those repository sources win. Do not invent strategy, requirements, approvals, task completion, acceptance, or authority decisions.

Normal consumer operation must not require access to the canonical `agent-governance` source repository. Do not load source-product maintainer decisions, PD/RF workflows, branch-maintenance state, or unrelated source checkout history during consumer operation.

## Progressive routing

Start with the smallest context required for the requested governance operation:

1. Read `.agent-governance/GOVERNANCE.md`.
2. Follow only the modules it routes for the current operation.
3. Read `.agent-coordination/STATE.json` for current frontier when state/current work matters.
4. Read `.agent-coordination/WORKPLAN.md` only for order/dependency metadata.
5. During implementation sequencing, disclose only the active task record and the exact project-native artifacts it references; do not preload future task records.
6. Read `.agent-governance/COEXISTENCE.md` only when existing project capabilities, managed files, SDD/Skill ownership, or authority overlap is material.
7. Read `.agent-governance/SKILL-DISCOVERY.md` only while locating/resolving Skill candidates, and `.agent-governance/SKILL-SUPPLY-CHAIN.md` only while auditing the specific candidate.

Reconstruct stale or missing conversational context from repository state; do not depend on prior chat memory as authority.

## Operation routing

### Bootstrap or validate

Before mutation, inspect relevant existing capability/instruction surfaces and stop on unresolved managed-file or governance/orchestration collisions. Never silently overwrite `.agent-governance/`, `.agent-coordination/`, third-party managed files, or an existing governance/orchestration Skill.

The packaged deterministic CLI currently provides:

```text
python governance-skill/scripts/governance.py bootstrap <target>
python governance-skill/scripts/governance.py validate <target>
```

Use `bootstrap` only for an existing adopting-repository directory after coexistence/collision preflight. It creates the managed Governance Core and coordination skeleton and validates the result. Use `validate` for read-only structural validation of an installed consumer instance.

Do not claim that the packaged CLI currently implements other operation-specific subcommands unless the installed artifact actually exposes them.

### State reconstruction, handoff, events, mission, archive, and sequential execution

Route these operations through the installed Governance Core and project records. Use deterministic repository tooling when actually available, but do not fabricate or assume unavailable CLI commands.

For cold start or state validation, begin with STATE + GOVERNANCE, then replay only the required EXCHANGE delta and controlling records. STATE is a constant-size frontier cache; it must not create decisions.

For handoffs, consume only the required completion/blocker delta. For implementation sequencing, expose exactly one current task record and stop on a valid blocker before later-task disclosure.

For mission initialization or archival, preserve history and authority ordering. Do not generate business requirements or strategic choices autonomously.

### Ecosystem coexistence

When overlap is material, follow `.agent-governance/COEXISTENCE.md` and classify relevant providers as `REUSE`, `ADAPT`, `COEXIST`, `MISSING`, or `CONFLICT`.

Prefer references and adapters to duplication. Preserve project-native SDD/spec/plan/task ownership and third-party managed surfaces. If authority or ownership overlap cannot be resolved from accepted project evidence, return `CONFLICT` and stop rather than choosing a winner.

A repository with no SDD or third-party Skills remains governable; do not propose or install an SDD merely because none is present.

### Skill discovery and supply-chain audit

Start from the required capability, not a preferred marketplace. Inspect already-present project/user Skills and project registries before broader discovery.

A directory or registry result is discovery evidence only. Resolve canonical owner/repository/path and immutable artifact identity before approval. Audit exact revision/digest, package inventory, scripts/hooks/config/dependencies, network/filesystem/process/secret/permission behavior, risk, exceptions, approval state, and host-selected artifact identity.

Do not execute marketplace/registry install commands against the active project during discovery. Acquire candidates only in a quarantine/review location when authorized. Reject changed, shadowed, unresolved-provenance, over-permissioned, or otherwise non-matching artifacts until re-audited and re-approved.

## Mutation and safety rules

Read-only validation is the default. Mutation requires an identified target and an authoritative operation that permits the change.

Never:

- invent strategy, requirements, acceptance, or approval;
- overwrite existing Governance or third-party managed state silently;
- replace the project's development methodology;
- duplicate compatible project-native specs/plans/tasks;
- expose future task contents for convenience;
- contact production/external systems without authority;
- store credentials or secrets;
- treat model/provider output, marketplace ranking, registry metadata, or host precedence as governance authority;
- make this Skill the only copy of Governance rules or project state.

If a requested operation requires a deterministic runtime surface that is not present in the installed package, report the missing capability explicitly and continue only through an authorized repository-native path that preserves the same Governance invariants. Do not pretend the missing tool exists.
