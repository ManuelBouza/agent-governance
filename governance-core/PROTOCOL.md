# Durable Coordination Protocol

Protocol-Module-Version: 1.1.0

Load this module for STATE reconstruction, EXCHANGE/event semantics, Decision Records, protocol corrections or version upgrades.

## STATE

`.agent-coordination/STATE.json` is a compact derived frontier, never an authority source.

It should contain only fields required to identify the current protocol/mission focus, lifecycle phase/gates, active/ready work, next permitted action, controlling record IDs/paths and the latest incorporated EXCHANGE sequence.

STATE must not contain full work inventories, decision history or self-referential current commit SHA. The Git commit containing STATE versions the snapshot.

If valid EXCHANGE events exist with `q > STATE.exchange_q`, replay those events and relevant authority records before relying on STATE.

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

Routine decisions that do not need preserved rationale should remain EXCHANGE events.

## Continuous Persistence

Persist the operational effect of approved decisions before a context switch or handoff. STATE is refreshed after authoritative records/events exist; editing STATE itself never creates a decision.

## Versioning

Semantic versioning:
- patch: clarification without behavioral change;
- minor: backward-compatible rule/capability extension;
- major: incompatible protocol change.

Protocol upgrades require an EXCHANGE decision. Work normally completes under the version active when it started unless safety or Human Owner direction requires otherwise.

## Archival

EXCHANGE remains append-only for an active mission. Completed missions may be archived under `.agent-coordination/archive/` after authoritative closure. Do not destroy historical audit material.
