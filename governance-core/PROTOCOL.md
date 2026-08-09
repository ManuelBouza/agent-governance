# Durable Coordination Protocol

Protocol-Module-Version: 1.2.0

Load this module for STATE reconstruction, EXCHANGE/event semantics, Decision Records, protocol corrections, capability-inventory persistence or version upgrades.

## STATE

`.agent-coordination/STATE.json` is a compact derived frontier, never an authority source.

It should contain only fields required to identify the current protocol/mission focus, lifecycle phase/gates, active/ready work, next permitted action, controlling record IDs/paths and the latest incorporated EXCHANGE sequence.

STATE must not contain full work inventories, capability/ecosystem inventories, decision history or self-referential current commit SHA. The Git commit containing STATE versions the snapshot.

If valid EXCHANGE events exist with `q > STATE.exchange_q`, replay those events and relevant authority records before relying on STATE.

## CAPABILITIES

`.agent-coordination/CAPABILITIES.json` is the compact project capability/coexistence inventory defined by `COEXISTENCE.md`.

It records only capabilities material to current/recent governance decisions, such as:
- capability identifier/category;
- provider/system and scope;
- evidence/reference sufficient to rediscover the provider;
- coexistence classification: `REUSE|ADAPT|COEXIST|MISSING|CONFLICT`;
- artifact/Skill identity when material;
- controlling Decision Record/event reference when classification affects strategy/readiness.

CAPABILITIES is evidence/routing metadata, not authority and not a substitute for Skill approval records. It MUST NOT contain full Skill catalogs, full SDD specs/plans/tasks, secrets, executable payloads or duplicated third-party instructions.

A material provider/version/path/Skill-selection change invalidates the affected inventory entry until re-evaluated. STATE may point to a current coexistence blocker/decision but does not copy the inventory.

Repositories with no material external capability decisions MAY keep the inventory minimal; absence of a third-party SDD/Skill ecosystem is a valid state.

## EXCHANGE

`.agent-coordination/EXCHANGE.jsonl` is UTF-8, one compact JSON object per line, append-only.

Keys:
- `q` mandatory monotonically increasing sequence;
- `a` protocol role actor: `human|strategy|implementation`;
- `e` event;
- `k` task id for task-scoped events;
- `r` Git/evidence reference;
- `v` concise verification;
- `x` reason code;
- `n` next action;
- `z` newly introduced risks;
- `s` superseded sequence;
- `m` exceptional concise note.

Legacy compatibility: events written before protocol 1.5.0 MAY use `gpt` as alias for `strategy` and `oc` as alias for `implementation`. New events MUST use role names rather than product identities.

Events: `start`, `progress`, `done`, `blocked`, `resume`, `accept`, `reject`, `decision`, `scope_change`, `cancel`.

Never edit, reorder or truncate history. Correct an erroneous event by appending a superseding event with `s`.

Normal handoff reads only events after the checkpoint. During one continuous implementation sequence, the Implementation Agent may accumulate multiple task events after `STATE.exchange_q`; this does not require STATE refresh between tasks.

## Task Sequence Semantics

`done` means the Implementation Agent has completed and verified the disclosed task against its acceptance criteria. A later task may become READY from WORKPLAN ordering/dependencies using DONE or ACCEPTED prerequisites under EXECUTION rules.

`accept`/`reject` represents Strategy/Human review and is not a default prerequisite for inter-task continuation.

## Decision Records

Use `.agent-coordination/decisions/<ID>-<slug>.md` when future agents need rationale, considered alternatives or consequences. A Decision Record is authoritative only through its controlling authority/event relationship; it does not outrank GOVERNANCE/MISSION/WORKPLAN.

A capability/coexistence classification that changes authority boundaries, provider ownership or readiness SHOULD reference a Decision Record when future agents need the rationale. `CAPABILITIES.json` points to that decision; it does not carry the rationale itself.

Routine decisions that do not need preserved rationale should remain EXCHANGE events.

## Continuous Persistence

Persist the operational effect of approved decisions before a context switch or handoff. STATE is refreshed after authoritative records/events exist; editing STATE itself never creates a decision.

Capability inventory entries are refreshed after the relevant provider/ownership decision exists. Editing CAPABILITIES itself never creates authority.

## Versioning

Semantic versioning:
- patch: clarification without behavioral change;
- minor: backward-compatible rule/capability extension;
- major: incompatible protocol change.

Protocol upgrades require an EXCHANGE decision. Work normally completes under the version active when it started unless safety or Human Owner direction requires otherwise.

## Archival

EXCHANGE remains append-only for an active mission. Completed missions may be archived under `.agent-coordination/archive/` after authoritative closure. Do not destroy historical audit material.

Capability inventories MAY be archived with the mission when they are mission-specific; project-wide reusable capability entries MAY remain active if still current and validated.
