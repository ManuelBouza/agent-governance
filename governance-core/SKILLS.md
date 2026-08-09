# Skill Governance

Skills-Version: 1.3.0

Load this module during lifecycle F3, when approving technical expertise, or when a task is blocked by missing capability.

## States

Capability state: `COVERED`, `MISSING`, `NOT_REQUIRED`.

Skill lifecycle state: `DISCOVERED`, `ACQUIRED`, `AUDITED`, `APPROVED`, `INSTALLED`, `REVOKED`.

Only an exact `APPROVED` Skill artifact may act as normative technical guidance for the mission. Availability, discovery, host precedence, registry selection or installation alone never implies approval.

WORKPLAN records approved/required Skill IDs; detailed provenance/audit records live under `.agent-coordination/skills/` and task records identify task-specific required Skills.

## Capability-First Audit

Audit capabilities derived from the approved F2 engineering strategy, not Skill names alone.

For each mandatory capability:
1. inspect already-present project/user Skills, existing Skill registries and existing approved Skill artifacts first;
2. apply `COEXISTENCE.md` when same-name shadowing, semantic overlap or an existing registry/provider affects which artifact would activate;
3. identify gaps;
4. discover candidates under `SKILL-DISCOVERY.md` without installing them;
5. resolve each candidate to its canonical owner/repository/path;
6. audit the exact external artifact under `SKILL-SUPPLY-CHAIN.md`;
7. classify the capability as `COVERED`, `MISSING` or `NOT_REQUIRED`;
8. persist exact approved Skill artifact records before F3 passes.

If an already-present Skill is suitable and passes the same artifact audit, reuse it instead of installing a duplicate Skill for the same capability.

Host/project precedence may determine which same-name Skill is selected by the agent runtime. That is activation evidence only. If the runtime-selected artifact differs from the exact approved artifact, F3/readiness fails until the collision is resolved.

## Candidate Quality

Evaluate purpose, provenance/author, maintenance, scope, embedded instructions, authority conflicts, permissions/risk, technical currency, compatibility and redundancy.

`COEXISTENCE.md` governs overlap with existing SDD/Skill/tooling surfaces. `SKILL-DISCOVERY.md` governs where/how new candidates are found. `SKILL-SUPPLY-CHAIN.md` governs acquisition, quarantine, audit, approval and installation. A directory, registry or marketplace may improve discovery/selection but never establishes artifact trust.

A Skill provides expertise, never project authority. It must not override GOVERNANCE, MISSION, WORKPLAN, controlling project-native artifacts bound by Strategy, or Human Owner instructions.

## Installation

Discovery/audit MUST occur before installation. Approval is bound to an immutable revision/content digest and its approved permission/dependency envelope.

The Implementation Agent MUST NOT install/adopt/update arbitrary external Skills autonomously. A required non-approved capability is a strategic blocker with `x:"missing_skill"`.

Do not install a second Skill merely because a public candidate is available when an existing approved Skill already covers the capability. A changed Skill revision or expanded dependency/permission set requires re-audit before use.

## Collisions and overlap

Same-name and semantic collisions are distinct:

- **same-name collision** — use the host's deterministic precedence only to identify the artifact that would activate; record/warn on material shadowing and verify it is the approved artifact;
- **semantic overlap** — compare activation descriptions, scope and authority claims; if two Skills could both own the same governance/orchestration responsibility, classify the ecosystem capability `CONFLICT` under `COEXISTENCE.md` until Strategy resolves it.

Project-level precedence over user-level Skills is common in Agent Skills clients, but precedence never substitutes for trust or Governance approval.

## Context Rule

During F3 load `COEXISTENCE.md` only when existing Skill/registry overlap matters; load `SKILL-DISCOVERY.md` only while locating/resolving new candidates and `SKILL-SUPPLY-CHAIN.md` only while auditing/acquiring/approving them. Load only candidate material required for the capability currently under review.

During implementation load only Skills required by the current task. Do not load the whole approved Skill catalog or external registry into every session.
