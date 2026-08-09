# Consumer Governance Skill Functional Contract

Status: DESIGN-APPROVED

## Purpose

Define the reusable consumer-facing Agent Skill that installs and operates the portable governance framework inside adopting repositories without becoming an authority source, replacing the project's development methodology, or storing upstream product-maintenance state.

This Skill is distinct from the source-product Maintainer Skill defined in `MAINTAINER-SKILL-CONTRACT.md`.

The Consumer Governance Skill must work across compatible agent products by targeting governance roles rather than vendor identities.

## Source Independence Invariant

After installation/bootstrap, a governed consumer repository MUST remain operable without read/write access to the canonical `agent-governance` source repository.

Consumers SHOULD use an immutable release/tag/commit artifact. The Skill MUST NOT require a floating `main`/`develop` checkout, upstream mutation, or source-product PD/RF maintenance context during normal consumer operation.

## Non-Authority Invariant

The Skill MUST NOT replace or redefine the Governance Core or project authority/state records. If Skill instructions conflict with repository authority sources, repository authority sources win. Governance MUST remain operable when the Skill is unavailable or unsupported.

Existing SDD/specification systems, Skills, registries, memory, permissions, testing and other project-native capabilities remain governed by `COEXISTENCE.md`: detect first, reuse/adapt before adding, and fail closed on unresolved authority/ownership overlap.

## Supported Operations

### 1. Bootstrap governance
Initialize the canonical modular Core, project instance skeleton and adapter requirements without inventing mission requirements, replacing an existing development methodology, or silently overwriting existing/third-party managed state.

Before material mutation, inspect relevant project-native capability/instruction surfaces under `COEXISTENCE.md` and stop on unresolved collisions.

### 2. Validate installation
Validate required files, Core/project separation, protocol-version consistency, direct references, context budgets, adapter boundaries, EXCHANGE integrity, STATE coherence, coexistence boundaries and absence of project-specific contamination in reusable assets.

### 3. Cold-start reconstruction
Start from STATE + GOVERNANCE, follow routed context only, replay EXCHANGE after the checkpoint when needed, and identify protocol, phase/gates, current frontier, blockers, controlling decisions and next permitted action.

### 4. Validate state
Determine whether STATE is VALID or STALE/INVALID and return the minimal reconstruction delta without making strategic decisions.

### 5. Process handoff
For Strategy, review only required completion/blocker evidence. For Implementation, recover the current sequence position and disclosed task only. Handoff MUST be delta-only.

### 6. Validate protocol events
Validate JSONL syntax, monotonic sequence, role actors, event enum, task IDs, state transitions, supersede semantics and compactness. Legacy pre-1.5 actor aliases `gpt`/`oc` remain valid; new events use `strategy`/`implementation`/`human`.

### 7. Refresh checkpoint
Materialize effective frontier after authoritative records/events already exist. STATE editing MUST NOT create decisions.

### 8. Initialize mission
Create MISSION, indexed WORKPLAN, task-record structure, initialized EXCHANGE and minimal STATE from Human/Strategy inputs. Distinguish missing strategy from technical implementation choices. Reference controlling project-native SDD/spec artifacts rather than duplicating them when they remain the project's source for that concern.

### 9. Archive completed mission
Preserve history, validate no unresolved active state unless explicitly cancelled, and prepare a clean active instance without destructive rewriting.

### 10. Portability test
Verify reusable assets are project-independent and work with at least two distinct agent-adapter configurations without depending on one vendor when generic repository capabilities suffice.

### 11. Validate sequential execution
Validate that:
- WORKPLAN exposes deterministic order/dependency metadata without embedding future task content;
- task records are agent-product neutral;
- exactly one task record is disclosed during normal execution;
- DONE/ACCEPTED dependency semantics match EXECUTION;
- future task records are not required to execute the current task;
- referenced native SDD/spec artifacts are loaded only for the current task;
- a valid blocker stops the sequence before later-task disclosure.

### 12. Discover Skill candidates
Support Strategy in locating external Skill candidates under `SKILL-DISCOVERY.md` without installing or trusting them.

The operation MUST:
- start from a required capability, not a preferred marketplace;
- inspect already-present project/user Skills and available project registries before broader discovery;
- search higher-priority external sources only for uncovered capabilities;
- distinguish discovery/registry source from canonical artifact provenance;
- resolve candidate owner/repository/path before acquisition;
- reject unresolved-provenance candidates;
- treat rankings, install counts, stars and directory security badges only as prioritization signals;
- never execute marketplace/CLI install commands against the active project during discovery.

Known public directories or existing registries may be used as discovery inputs, but the Skill MUST NOT encode any directory/registry as an approval authority.

### 13. Audit Skill supply chain
Support Strategy in validating resolved external Skill candidates under `SKILL-SUPPLY-CHAIN.md` without installing them first.

The operation MUST be able to record/check at least:
- discovery source separately from provenance tier;
- canonical owner/source/path;
- immutable revision/content digest;
- package inventory;
- scripts/hooks/config/dependency surfaces;
- network/filesystem/process/secret/permission behavior;
- risk classification;
- material audit exceptions;
- exact approval status and supersession/revocation;
- runtime-selected/host-precedence artifact identity when same-name Skills exist.

It MUST reject installation/update validation when the artifact does not match the exact approved canonical source/revision/digest, exceeds the approved permission/dependency envelope, or host shadowing would activate a different artifact.

The Skill MUST treat directory/platform/registry scanning as supplemental evidence, never as a replacement for project audit.

### 14. Inspect ecosystem coexistence
Support Strategy in detecting and classifying relevant pre-existing project capabilities under `COEXISTENCE.md` before Governance adds overlapping behavior.

The operation MUST:
- inspect only capability surfaces relevant to the current bootstrap/mission/task;
- classify providers `REUSE`, `ADAPT`, `COEXIST`, `MISSING`, or `CONFLICT`;
- identify native ownership of SDD specs/plans/tasks, testing, Skill registries, memory/context, permissions and branch/PR workflows when material;
- identify same-name/semantic Skill collisions and managed instruction/config files;
- prefer references/adapters to duplication;
- preserve third-party managed blocks/files;
- return `CONFLICT` instead of choosing an authority winner when responsibilities collide;
- work when no SDD/third-party Skill ecosystem is installed.

Known systems such as Gentle-AI, GitHub Spec Kit and OpenSpec are compatibility fixtures/examples, not special Governance roles.

## Explicitly Out of Scope

The Consumer Governance Skill MUST NOT:
- develop, refactor, test, or release the canonical `agent-governance` source product merely because it is reachable;
- load source-product maintainer decisions, `PD*`/`RF*` workflows, or branch-maintenance instructions during ordinary consumer operation;
- decide project strategy without authority input;
- generate/change business requirements autonomously;
- implement application code merely because governance is active;
- replace the project's development methodology or install an SDD framework merely because none is present;
- duplicate existing specs/plans/tasks when a compatible native SDD system already owns them;
- silently overwrite third-party managed instruction/config/Skill surfaces;
- silently shadow or replace an existing governance/orchestration Skill;
- treat host Skill precedence or a Skill registry as artifact approval;
- install, update or trust arbitrary third-party Skills without exact artifact approval;
- treat a marketplace/directory listing as canonical provenance or approval;
- contact production/external systems without authority;
- store credentials/secrets;
- become the only copy of governance rules/templates/state;
- assume a project domain;
- assume OpenCode, Codex, Claude Code, Antigravity, ChatGPT or another named product is always active;
- expose future task contents merely to optimize planning or implementation.

## Deterministic vs Judgment Operations

Use deterministic tooling for layout/reference/budget checks, JSON/JSONL validation, role/event validation, state-transition validation, stale-checkpoint detection, execution-order/dependency checks, Skill canonical-source/revision/approval-record matching, host-selected Skill identity comparison, coexistence evidence discovery where mechanically detectable, and template/bootstrap generation.

Use agent judgment for Human strategic input, genuine scope/acceptance ambiguity, evidence review against strategic acceptance, capability-provider classification where semantics matter, authority/ownership conflict interpretation, candidate relevance, provenance confidence, risk interpretation and Skill approval suitability.

A script MUST NOT encode strategic decisions belonging to Human or Strategy roles.

## Minimal Context Principle

The Skill MUST follow progressive disclosure:
- `SKILL.md` provides activation and operational routing;
- Core modules are loaded only when routed;
- `COEXISTENCE.md` is loaded only when existing SDD/Skill/tooling boundaries matter;
- deterministic tooling replaces duplicated validation prose;
- project state stays in the project instance;
- implementation loads WORKPLAN metadata plus only the currently disclosed task record, exact referenced native artifacts, and exact required approved Skill artifacts;
- F3 loads `SKILL-DISCOVERY.md` only while locating/resolving candidates and `SKILL-SUPPLY-CHAIN.md` only for the candidate being audited.

## Safety and Mutation Policy

Read-only validation is default. Mutation requires an identified target, preserved authority ordering, non-destructive behavior, audit preservation, stop-on-strategic-conflict semantics and no bypass of adapter restrictions.

Shared/third-party managed project files require safe composition under `COEXISTENCE.md`; unsafe overwrite is a blocker.

External Skill acquisition MUST occur in a quarantine/review location before active installation. Approval is artifact-specific; revision/dependency/permission changes require re-audit.

## Functional Acceptance Criteria

The Consumer Governance Skill is acceptable only if:
1. a clean unrelated repository can be bootstrapped without project knowledge;
2. a stateless compatible agent reconstructs state without chat history;
3. stale STATE is detected correctly;
4. valid/invalid EXCHANGE transitions and role actors are distinguished;
5. handoffs consume only required deltas;
6. removing the Skill leaves governance/state intact;
7. reusable assets contain no project-specific facts;
8. mutation never invents strategy;
9. canonical semantics work with at least two agent adapters;
10. trigger tests include positive, negative and near-miss cases including SDD/orchestration near misses;
11. one Implementation Agent can execute an authorized multi-task fixture one task at a time without reading future task records, stopping only on completion or a valid blocker;
12. a directory/registry result cannot become installation-valid until its canonical artifact is resolved and separately audited;
13. an external Skill cannot become valid for installation without an exact provenance/revision audit record, and a changed/shadowed artifact fails validation until re-audited/resolved;
14. normal operation succeeds without access to the canonical source repository after installation;
15. maintainer-only triggers do not activate this Skill;
16. a repository with Gentle-AI-like, Spec Kit-like, OpenSpec-like or custom SDD fixtures reuses/adapts existing capability ownership without duplicate specs/plans/tasks;
17. a repository with no SDD/third-party Skills remains fully governable without Governance installing them;
18. unsafe managed-file or governance-Skill overlap is detected and fails closed rather than being overwritten/shadowed.

## Release Gate

Do not author/release final `SKILL.md` until operation boundaries, package layout, exact consumer trigger corpus, activation description, CLI contracts and template fields are finalized and validated against the current protocol, including source independence, sequential disclosure, Skill discovery resolution, supply-chain semantics, ecosystem coexistence and non-overlap with existing SDD/orchestration Skills.
