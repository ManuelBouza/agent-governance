---
name: consumer-governance
description: Operate Agent Governance inside an adopting repository for explicit governance bootstrap, validation, state reconstruction, mission/state/event/handoff work, native SDD governance, coexistence inspection, Governance Skill discovery or audit, and sequential-disclosure readiness. Do not use for generic planning, coding, testing, refactoring, releases, unrelated generic SDD workflows, generic Skill installation, or source-product maintenance.
---

# Consumer Governance Skill

Use this Skill only for explicit Agent Governance work in an adopting repository. Repository authority and installed Governance Core remain authoritative; this Skill is routing and operational guidance, not a replacement authority.

Native Spec-Driven Development is part of installed Governance Core through `.agent-governance/SDD.md`; it does not require this Skill to become a generic SDD/coding agent and does not require an external SDD product.

## Activation boundary

Activate for explicit requests to:

- bootstrap or install Agent Governance in an adopting repository;
- validate an installed governance instance or reconstruct its current frontier without relying on prior chat history;
- initialize or advance governance mission/state/event/handoff records;
- operate or validate the installed native SDD lifecycle/ownership/trace boundary for governed work;
- inspect coexistence with existing SDD, Skill, testing, memory/context, permission, branch/PR, or orchestration capabilities;
- discover or audit Governance-related external Skill artifacts under the installed supply-chain rules;
- validate sequential disclosure, current-task readiness, dependency state, Implementation Code Review & Verify evidence, or Governance handoff/convergence boundaries.

Do not activate merely because Governance is present. In particular, do not activate for ordinary application implementation, generic planning/coding/testing/refactoring/release work, unrelated generic spec/plan/tasks workflows, generic Skill installation, or maintenance of the canonical `agent-governance` source product.

## Authority and source independence

Treat the adopting repository's installed `.agent-governance/GOVERNANCE.md` as the protocol entry point and follow its routed modules. Project authority/state remains in `.agent-coordination/` and project-native sources referenced from it.

For governed development, `.agent-governance/SDD.md` defines the single-owner stage model:

```text
Strategy       -> Explore / Specify / Design / Plan & Trace
Implementation -> Implement / Code Review & Verify
Strategy       -> Converge / Accept / Evolve
```

If this Skill conflicts with installed Governance Core, project authority records, or compatible project-native ownership, those repository sources win. Do not invent strategy, requirements, Design, Plan/Trace, approvals, task completion, acceptance, or authority decisions.

Normal consumer operation must not require access to the canonical `agent-governance` source repository. Do not load source-product maintainer decisions, PD/RF workflows, branch-maintenance state, or unrelated source checkout history during consumer operation.

## Progressive routing

Start with the smallest context required for the requested governance operation:

1. Read `.agent-governance/GOVERNANCE.md`.
2. Follow only the modules it routes for the current operation.
3. Read `.agent-coordination/STATE.json` for current frontier when state/current work matters.
4. Read `.agent-coordination/WORKPLAN.md` only for order/dependency metadata.
5. Load `.agent-governance/SDD.md` when framing/specifying/designing/planning governed development, validating Implementation review evidence, resolving SDD re-entry, or performing Strategy convergence/acceptance.
6. During implementation sequencing, disclose only the active task record and the exact project-native specification/Design artifacts it references; do not preload future task records.
7. Read `.agent-governance/COEXISTENCE.md` only when existing project capabilities, managed files, SDD/Skill ownership, or authority overlap is material.
8. Read `.agent-governance/SKILL-DISCOVERY.md` only while locating/resolving Skill candidates, and `.agent-governance/SKILL-SUPPLY-CHAIN.md` only while auditing the specific candidate.
9. During bootstrap or repository writable-readiness validation, load `assets/REPOSITORY-BRANCH-PROTECTION.md` only when branch/PR protection state is material.

Reconstruct stale or missing conversational context from repository state; do not depend on prior chat memory as authority.

## Deterministic CLI v1

The packaged deterministic surface is exactly:

```text
python governance-skill/scripts/governance.py bootstrap <target>
python governance-skill/scripts/governance.py validate <target>
python governance-skill/scripts/governance.py state <target> [--refresh]
python governance-skill/scripts/governance.py event <target> --actor <role> --event <event> [event fields]
python governance-skill/scripts/governance.py skill <target> --approval <record> --candidate <facts>
python governance-skill/scripts/governance.py ecosystem <target> --facts <facts> [--update]
python governance-skill/scripts/governance.py archive <target> [--prepare]
```

Treat read-only/check behavior as default. Use mutation flags such as `--refresh`, `--update`, or `--prepare` only after reviewing the derived result and confirming the governing operation authorizes mutation. Do not infer strategy/specification/Design from deterministic output.

The current deterministic CLI does not itself administer remote repository rulesets/protected-branch settings. When branch-protection setup is required, use the provider's supported administration surface under Human/repository authority, then verify the effective state before clearing writable readiness. Do not pretend `bootstrap` has enforced a remote control it does not implement.

## Operation routing

### Bootstrap and validate

Before mutation, inspect relevant existing capability/instruction surfaces and stop on unresolved managed-file or governance/orchestration collisions. Never silently overwrite `.agent-governance/`, `.agent-coordination/`, third-party managed files, or an existing governance/orchestration Skill.

As part of bootstrap preflight, discover the repository provider, actual long-lived branches, existing branch/PR controls, and bypass actors when those facts are available through supported project/provider surfaces. Preserve stronger compatible project-native controls.

Before normal agentic writable operation, require the semantic protection defined in `assets/REPOSITORY-BRANCH-PROTECTION.md`: normal long-lived-branch changes use PR/MR transport, deletion is restricted, force/non-fast-forward updates are blocked, the normal agentic writer has no routine bypass, and the control is active/enforced.

If the control is missing and the active agent cannot administer repository settings, return `REQUIRE_HUMAN` with the bounded provider action, wait for the repository administrator to apply it, then verify the effective provider-side state. Missing administration capability is not permission to continue unprotected. Read-only discovery/validation may continue while writable readiness remains blocked.

Record the verified protection in an existing compatible project-native security/operations/governance ledger when one exists. Do not invent a competing authority file merely to match the source product's ledger filename; if no durable receipt surface exists, Strategy must establish one before relying on chat-only setup evidence.

Use `bootstrap` only for an existing adopting-repository directory after coexistence/collision preflight. It creates the managed Governance Core and coordination skeleton and validates the result. Use `validate` for read-only structural validation of an installed consumer instance.

A successful native-SDD bootstrap must ultimately expose `.agent-governance/SDD.md` through the same single-install Governance distribution; if the current packaged runtime cannot do so, report that as a product/version capability gap rather than inventing a local substitute.

### State, handoff, events, mission, archive, and sequential execution

For cold start or state validation, begin with STATE + GOVERNANCE, then replay only the required EXCHANGE delta and controlling records. Use `state` to derive/check the constant-size frontier; `--refresh` may materialize already-authoritative state but must not create decisions.

Use `event` only to append an already-authorized role/event transition. It validates actor, sequence, transition, dependency, evidence, and supersession constraints; it does not decide which event should occur.

For handoffs, consume only the required completion/blocker delta. For implementation sequencing, expose exactly one current task record and stop on a valid blocker before later-task disclosure. Implementation `DONE` means implementation plus technical Code Review & Verify completed; Strategy still performs Converge/Accept/Evolve.

If Implementation reports a material requirement/Design/Plan defect, route the work back to the earliest affected Strategy-owned SDD stage. Do not let Implementation repair upstream authority by silently changing the task/spec/design.

For mission initialization, follow installed Core/project records and authoritative Human/Strategy inputs. For completed/cancelled missions, use `archive` as a safety check first and `--prepare` only when archival mutation is authorized. Preserve history and do not generate business requirements or strategic choices autonomously.

### Native SDD operation

When Governance is managing development work:

- select proportionate `COMPACT`, `STANDARD`, or `ASSURED` coverage;
- identify/reuse the accepted current specification carrier when one exists;
- represent material change semantics with `ADDED / MODIFIED / REMOVED / PRESERVED`;
- keep Strategy as the sole owner of Explore/Specify/Design/Plan and final convergence/acceptance;
- allow Implementation only the technical Implement and Code Review & Verify stages;
- maintain enough requirement -> Design -> task -> implementation -> evidence -> acceptance trace for the selected profile;
- re-enter the earliest affected Strategy stage when implementation/review evidence invalidates an upstream assumption;
- evolve accepted current-spec state after Strategy acceptance without duplicating adequate living truth.

Do not create proposal/spec/design/task files merely to imitate a vendor layout when existing project/Governance artifacts carry the semantics adequately.

### Ecosystem coexistence

When overlap is material, follow `.agent-governance/COEXISTENCE.md`. Use `ecosystem` with bounded mechanical facts to derive `REUSE`, `ADAPT`, `COEXIST`, `MISSING`, or `CONFLICT`; use `--update` only to materialize the reviewed classification.

Prefer references and adapters to duplication. Preserve adequate project-native SDD/spec/plan/task artifacts while mapping their authority to the Governance single-owner SDD stages. If authority or ownership overlap cannot be resolved from accepted project evidence, return `CONFLICT` and stop rather than choosing a winner.

A repository with no external/project-native SDD product remains governable because native `.agent-governance/SDD.md` supplies the method. Do not propose or install OpenSpec, Spec Kit, Kiro or another SDD framework merely because no external provider is present.

### Skill discovery and supply-chain audit

Start from the required capability, not a preferred marketplace. Inspect already-present project/user Skills and project registries before broader discovery.

A directory or registry result is discovery evidence only. Resolve canonical owner/repository/path and immutable artifact identity before approval. Audit exact revision/digest, package inventory, scripts/hooks/config/dependencies, network/filesystem/process/secret/permission behavior, risk, exceptions, approval state, and host-selected artifact identity.

Use `skill` only to validate candidate facts against the canonical current approval record and exact selected artifact identity. It does not discover candidates, fetch remote artifacts, or grant approval.

Do not execute marketplace/registry install commands against the active project during discovery. Acquire candidates only in a quarantine/review location when authorized. Reject changed, shadowed, unresolved-provenance, over-permissioned, or otherwise non-matching artifacts until re-audited and re-approved.

## Mutation and safety rules

Read-only validation is the default. Mutation requires an identified target and an authoritative operation that permits the change.

Normal governed writable work MUST NOT proceed while long-lived-branch protection is missing or unverified on a provider that supports an equivalent enforceable control, unless Human authority has explicitly accepted a documented alternative because the provider cannot supply the invariant.

Never:

- invent strategy, requirements, controlling Design, Plan/Trace, acceptance, or approval;
- overwrite existing Governance or third-party managed state silently;
- replace an adequate project-native development methodology when `REUSE`/`ADAPT` can satisfy Governance SDD semantics;
- let an Implementation/executor-native SDD workflow become a competing authoritative specification/Design/Plan/acceptance system;
- duplicate compatible project-native specs/plans/tasks;
- expose future task contents for convenience;
- contact production/external systems without authority;
- store credentials or secrets;
- treat model/provider output, marketplace ranking, registry metadata, or host precedence as governance authority;
- make this Skill the only copy of Governance rules or project state;
- weaken or bypass compatible project-native branch protection merely to make automation easier.

If the installed artifact does not expose a required deterministic command or required native SDD Core module, report the missing capability explicitly and continue only through an authorized repository-native path that preserves the same Governance invariants. Do not pretend the missing tool/capability exists.
