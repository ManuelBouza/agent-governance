# Consumer Skill Capability Baseline

Status: CHARACTERIZATION  
Observed baseline: `develop@a29a3278839524eb918892e0a3c2d38926eb1be4`  
Catalog: `docs/CAPABILITY-CATALOG.md`  
Decision context: D050

## Purpose

Characterize the accepted Consumer Governance Skill v1 against the topology-neutral capability catalog before future MG1/T023 experiments.

This document records current structure and candidate progressive-disclosure cuts. It does **not** change Skill behavior, select B0/B1/F2/G3, pre-register T023 corpus/thresholds, or claim source-maintainer runtime completion.

## Baseline identity

Observed source state:

- `governance-skill/STATUS.md`: `FINAL-AUTHORED / RELEASE-APPROVED`;
- activation entrypoint: `governance-skill/SKILL.md`;
- Skill name: `consumer-governance`;
- deterministic CLI v1: `bootstrap`, `validate`, `state`, `event`, `skill`, `ecosystem`, `archive`;
- `maintainer-skill/` has no Maintainer `SKILL.md` at this baseline.

Therefore this is **Consumer v1 / pre-T022**, not the complete future D050 B0 dispatcher topology.

## Physical source observations

GitHub source metadata reports:

| Surface | Observed size / structure |
| --- | --- |
| `governance-skill/SKILL.md` | 8,910 UTF-8 bytes |
| `governance-skill/scripts/governance.py` | 1,413 bytes |
| seven visible templates under `governance-skill/assets/` | 1,744 bytes total |
| Skill-local `references/` directory | absent |
| deterministic script files | one |

`STATUS.md` is source-maintenance metadata, not activation guidance.

These values characterize the visible source Skill directory only. They are not the full D051 distribution size, and no tokenizer/runtime-context conclusion is inferred from bytes alone.

## Current disclosure structure

`SKILL.md` currently contains all Skill-local routing for:

1. activation/negative boundary;
2. authority/source independence;
3. progressive routing to installed Core/project state;
4. seven-command CLI synopsis;
5. installation/validation;
6. state/handoff/event/mission/archive/sequential execution;
7. coexistence;
8. Skill discovery/audit;
9. mutation/safety.

After activation it routes to focused installed `.agent-governance/*` modules, but the source Skill itself has no focused reference layer.

```text
host activates consumer-governance
    -> complete Skill-local SKILL.md body
    -> operation-specific installed Core module(s)
    -> current project state / exact task / exact candidate
```

The second half is already progressively disclosed; the Skill-local layer is monolithic.

## Capability mapping

### Consumer lifecycle

| Catalog ID | Current Skill-local surface | CLI mapping |
| --- | --- | --- |
| `consumer.lifecycle.installation` | activation/progressive rules + `Bootstrap and validate` | `bootstrap`, `validate`; no dedicated portability command |
| `consumer.lifecycle.state` | combined state/handoff/event/mission/archive/sequential section | `state`, `event` |
| `consumer.lifecycle.execution` | same combined section | no dedicated handoff/sequential command |
| `consumer.lifecycle.mission` | same combined section | `archive`; no dedicated mission-init command |
| `consumer.lifecycle.coexistence` | conditional progressive route + dedicated coexistence section | `ecosystem` |

### External Skill trust

| Catalog ID | Current Skill-local surface | CLI mapping |
| --- | --- | --- |
| `consumer.skill-trust.discovery` | shared discovery/audit section | none; `skill` explicitly does not discover/fetch candidates |
| `consumer.skill-trust.audit` | same trust section + safety rules | `skill` validates candidate facts against approval/selected artifact identity |

The CLI relationship is many-to-many. Command count is not a valid proxy for capability or Skill count.

### Source maintenance

`source.maintenance.*` is intentionally absent from the Consumer Skill. `source-maintainer-target` remains prospective and must not be read as implemented T022 behavior.

## Cross-cutting top-level guidance

Several constraints appear across activation, authority, operation and mutation sections:

- installed repository/Core authority wins over Skill guidance;
- do not invent strategy, requirements, approval or acceptance;
- read-only behavior is default;
- preserve project-native ownership and managed state;
- do not silently overwrite;
- Consumer operation is source-independent;
- registry/marketplace/host precedence is not approval authority;
- future task contents are not disclosed for convenience.

These constraints are real safety/authority requirements. A thinner router may relocate or deduplicate them only if their visibility and enforcement remain sufficient.

## Candidate internal cuts

The catalog exposes plausible **reference boundaries** for later characterization/evaluation without asserting new top-level Skills:

```text
thin Consumer router
    -> lifecycle.installation
    -> lifecycle.state
    -> lifecycle.execution
    -> lifecycle.mission
    -> lifecycle.coexistence
    -> skill-trust.discovery/audit
```

A future B1 design may combine some routes into fewer references. F2/G3 may project the same catalog differently. No grouping is selected here.

Likely top-level invariants that must survive any cut include:

- explicit Agent Governance activation plus strong negative boundary;
- repository/Core authority;
- source independence;
- read-only/mutation fail-closed default;
- no invented strategy/approval;
- correct capability routing;
- honesty when a deterministic capability is missing.

Whether each invariant belongs in metadata, top-level body, a shared reference or deterministic guard is a later design/eval question.

## D050 candidate observations

### B0

Consumer v1 shows lifecycle and Skill-trust concerns can coexist in one Consumer entrypoint sharing Core/runtime semantics. It does **not** prove the future Consumer+source-maintainer unified dispatcher because source-maintainer is not yet complete.

### B1

The baseline already routes from Skill guidance to installed Core modules but has no Skill-local reference layer. A thin-router challenger therefore has a concrete structural hypothesis: move capability-specific routing detail out of the top-level body while preserving safety and correctness.

No context or activation benefit is assumed before measurement.

### F2

Consumer v1 already has a distinct Consumer activation identity and explicitly rejects source maintenance. This is compatible with later peer-entrypoint evaluation but provides no evidence yet about a future Source Maintainer entrypoint.

### G3

Discovery/audit has visibly distinct guidance, deterministic coverage and provenance/permission risk. This makes `consumer.skill-trust` a legitimate challenger boundary to measure, not proof that a separate `External Skill Trust` Skill is superior.

## No-decision boundary

This characterization MUST NOT be used to claim before MG1/T023 that:

- B0/B1/F2/G3 is the winner;
- `consumer.skill-trust` must become a separate release Skill;
- every catalog sub-capability needs its own reference file;
- smaller `SKILL.md` means lower runtime context;
- host activation behavior is portable/identical;
- source-maintainer is implemented;
- current Consumer v1 trigger accuracy is known from structural review.

## Future evidence hooks

After T022, MG1 may use this baseline to define:

- candidate presentation construction without semantic drift;
- top-level-body versus focused-reference load-path measurement;
- activation positives/negatives/near misses by capability family;
- overactivation and multi-intent cases;
- capability-to-command/task-success invariants;
- preservation of cross-cutting safety after progressive-disclosure cuts.

Actual corpus, thresholds, holdout, host/model matrix and selection rule remain MG1 authority and are intentionally absent here.
