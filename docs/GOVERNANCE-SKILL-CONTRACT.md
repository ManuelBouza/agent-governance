# Governance Skill Functional Contract

Status: DESIGN-APPROVED

## Purpose

Define the reusable Agent Skill that operates the portable governance framework without becoming an authority source or storing project state.

The Skill must work across compatible agent products by targeting governance roles (`strategy`, `implementation`) rather than vendor identities.

## Non-Authority Invariant

The Skill MUST NOT replace or redefine the Governance Core or project authority/state records. If Skill instructions conflict with repository authority sources, repository authority sources win. Governance MUST remain operable when the Skill is unavailable or unsupported.

## Supported Operations

### 1. Bootstrap governance
Initialize the canonical modular Core, project instance skeleton and adapter requirements without inventing mission requirements or silently overwriting existing state.

### 2. Validate installation
Validate required files, Core/project separation, protocol-version consistency, direct references, context budgets, adapter boundaries, EXCHANGE integrity, STATE coherence and absence of project-specific contamination in reusable assets.

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
Create MISSION, indexed WORKPLAN, task-record structure, initialized EXCHANGE and minimal STATE from Human/Strategy inputs. Distinguish missing strategy from technical implementation choices.

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
- a valid blocker stops the sequence before later-task disclosure.

### 12. Discover Skill candidates
Support Strategy in locating external Skill candidates under `SKILL-DISCOVERY.md` without installing or trusting them.

The operation MUST:
- start from a required capability, not a preferred marketplace;
- search higher-priority sources first;
- distinguish discovery source from canonical artifact provenance;
- resolve candidate owner/repository/path before acquisition;
- reject unresolved-provenance candidates;
- treat rankings, install counts, stars and directory security badges only as prioritization signals;
- never execute marketplace/CLI install commands against the active project during discovery.

Known public directories may be used as discovery inputs, but the Skill MUST NOT encode any directory as an approval authority.

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
- exact approval status and supersession/revocation.

It MUST reject installation/update validation when the artifact does not match the exact approved canonical source/revision/digest or exceeds the approved permission/dependency envelope.

The Skill MUST treat directory/platform scanning as supplemental evidence, never as a replacement for project audit.

## Explicitly Out of Scope

The Skill MUST NOT:
- decide project strategy without authority input;
- generate/change business requirements autonomously;
- implement application code merely because governance is active;
- replace the project's development methodology;
- install, update or trust arbitrary third-party Skills without exact artifact approval;
- treat a marketplace/directory listing as canonical provenance or approval;
- contact production/external systems without authority;
- store credentials/secrets;
- become the only copy of governance rules/templates/state;
- assume a project domain;
- assume OpenCode, Codex, Claude Code, Antigravity, ChatGPT or another named product is always active;
- expose future task contents merely to optimize planning or implementation.

## Deterministic vs Judgment Operations

Use deterministic tooling for layout/reference/budget checks, JSON/JSONL validation, role/event validation, state-transition validation, stale-checkpoint detection, execution-order/dependency checks, Skill canonical-source/revision/approval-record matching and template/bootstrap generation.

Use agent judgment for Human strategic input, genuine scope/acceptance ambiguity, evidence review against strategic acceptance, candidate relevance, provenance confidence, risk interpretation and Skill approval suitability.

A script MUST NOT encode strategic decisions belonging to Human or Strategy roles.

## Minimal Context Principle

The Skill MUST follow progressive disclosure:
- `SKILL.md` provides activation and operational routing;
- Core modules are loaded only when routed;
- deterministic tooling replaces duplicated validation prose;
- project state stays in the project instance;
- implementation loads WORKPLAN metadata plus only the currently disclosed task record and its exact required approved Skill artifacts;
- F3 loads `SKILL-DISCOVERY.md` only while locating/resolving candidates and `SKILL-SUPPLY-CHAIN.md` only for the candidate being audited.

## Safety and Mutation Policy

Read-only validation is default. Mutation requires an identified target, preserved authority ordering, non-destructive behavior, audit preservation, stop-on-strategic-conflict semantics and no bypass of adapter restrictions.

External Skill acquisition MUST occur in a quarantine/review location before active installation. Approval is artifact-specific; revision/dependency/permission changes require re-audit.

## Functional Acceptance Criteria

The Governance Skill is acceptable only if:
1. a clean unrelated repository can be bootstrapped without project knowledge;
2. a stateless compatible agent reconstructs state without chat history;
3. stale STATE is detected correctly;
4. valid/invalid EXCHANGE transitions and role actors are distinguished;
5. handoffs consume only required deltas;
6. removing the Skill leaves governance/state intact;
7. reusable assets contain no project-specific facts;
8. mutation never invents strategy;
9. canonical semantics work with at least two agent adapters;
10. trigger tests include positive, negative and near-miss cases;
11. one Implementation Agent can execute an authorized multi-task fixture one task at a time without reading future task records, stopping only on completion or a valid blocker;
12. a directory result cannot become installation-valid until its canonical artifact is resolved and separately audited;
13. an external Skill cannot become valid for installation without an exact provenance/revision audit record, and a changed artifact fails validation until re-audited.

## Release Gate

Do not author/release final `SKILL.md` until operation boundaries, package layout, exact trigger corpus, activation description, CLI contracts and template fields are finalized and validated against the current protocol, including sequential disclosure, Skill discovery resolution and supply-chain semantics.
