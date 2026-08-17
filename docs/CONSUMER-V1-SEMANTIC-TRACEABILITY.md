# Consumer v1 Semantic Traceability

Status: CHARACTERIZATION / PRESERVATION BASELINE  
Source: `governance-skill/SKILL.md`  
Source blob: `91b77ce3350695876eba4796289481d39c61709a`  
Routing design: `docs/CONSUMER-L1-GUARD-SPEC.md`, `docs/CONSUMER-L1-ROUTING-CONTRACT.md`, `docs/CONSUMER-L2-PROJECTION-MAPPING-CONTRACT.md`

## Purpose

Map every material semantic family in the accepted Consumer Governance Skill v1 to its intended destination in the topology-neutral routing architecture.

This is characterization only. It does not rewrite Consumer v1, choose R*/B* candidates, create references or define T023 cases/thresholds.

A future decomposition is not semantically equivalent merely because it preserves capability names; all material v1 responsibilities below must remain traceable.

## Status vocabulary

- `MAPPED` — destination is explicit in current design.
- `MAPPED-CONDITIONAL` — semantic is preserved through an early guard plus capability/Core detail loaded only when material.
- `LATER-INSTANCE` — design destination exists, but exact generated wording/reference asset awaits MG1/T024.
- `UNMAPPED` — no safe destination exists; would be a blocking design gap.

## Activation and authority

| v1 semantic family | Destination | Status |
| --- | --- | --- |
| explicit adopting-repository Governance activation | L0 activation metadata + Consumer boundary in L1 routing | `LATER-INSTANCE` |
| reject generic planning/coding/testing/refactoring/release/SDD/Skill-install/source-maintenance | L0 negative metadata + L1 Consumer boundary | `MAPPED` |
| Skill is guidance, not authority | `C-L1-G01` | `MAPPED` |
| installed Core/project authority wins on conflict | `C-L1-G01` + L3 Core | `MAPPED` |
| do not invent strategy/requirements/approval/completion/acceptance | `C-L1-G02` | `MAPPED` |
| Consumer operation independent from canonical source checkout | `C-L1-G03` + D051 distribution boundary | `MAPPED` |
| do not load source maintainer PD/RF/branch/history | `C-L1-G03` | `MAPPED` |

## Progressive routing and context

| v1 semantic family | Destination | Status |
| --- | --- | --- |
| start from installed `GOVERNANCE.md` and routed modules | L1 route -> L3 installed Core | `MAPPED` |
| load only modules needed for current operation | `C-L1-G07` + L2 mapping contract | `MAPPED` |
| read STATE only when current frontier matters | state capability + L5 current evidence | `MAPPED-CONDITIONAL` |
| WORKPLAN only for order/dependency metadata | execution capability + L5 | `MAPPED-CONDITIONAL` |
| disclose exactly active task; no future task preload | `C-L1-G06` + execution capability | `MAPPED` |
| load COEXISTENCE only when ownership/overlap is material | coexistence capability + conditional L2 mapping | `MAPPED-CONDITIONAL` |
| load Skill discovery/audit modules only for the active trust phase | discovery/audit capability IDs + conditional L2 mapping | `MAPPED-CONDITIONAL` |
| reconstruct from repository state, not chat memory as authority | `C-L1-G01` + state capability + L5 | `MAPPED` |

## Deterministic CLI/runtime

| v1 semantic family | Destination | Status |
| --- | --- | --- |
| exact seven-command Consumer v1 deterministic surface | L4 shared deterministic runtime; preserved by D050 fixed functional semantics for later comparisons | `MAPPED` |
| `bootstrap` / `validate` | `consumer.lifecycle.installation` -> L4 | `MAPPED` |
| `state` / `event` | `consumer.lifecycle.state` -> L4 | `MAPPED` |
| `ecosystem` | `consumer.lifecycle.coexistence` -> L4 | `MAPPED` |
| `skill` bounded candidate-vs-approval validation | `consumer.skill-trust.audit` -> L4 | `MAPPED` |
| `archive` | `consumer.lifecycle.mission` -> L4 | `MAPPED` |
| read/check default; mutation flags require authority | `C-L1-G04` + capability-specific L2 mutation precondition + L4 validation | `MAPPED` |
| deterministic output does not create strategy | `C-L1-G02` + L4 boundary | `MAPPED` |

## Installation / validation

| v1 semantic family | Destination | Status |
| --- | --- | --- |
| inspect existing capability/managed surfaces before mutation | installation + coexistence composition | `MAPPED-CONDITIONAL` |
| stop on unresolved managed-file/governance collision | `C-L1-G05` + coexistence capability/L3 | `MAPPED` |
| never silently overwrite Governance/coordination/third-party managed state | `C-L1-G04..G05` + installation/coexistence L2 | `MAPPED` |
| bootstrap existing adopting repository and validate result | installation capability + L4 | `MAPPED` |
| validate installed Consumer instance read-only | installation capability + `C-L1-G04` | `MAPPED` |

## State, execution and mission

| v1 semantic family | Destination | Status |
| --- | --- | --- |
| cold start from STATE + GOVERNANCE and required EXCHANGE delta | state capability -> L3/L5 | `MAPPED` |
| state refresh materializes authoritative facts but creates no decisions | state capability + `C-L1-G02`, `G04` + L4 | `MAPPED` |
| event appends only already-authorized transition | state capability + `C-L1-G02`, `G04` + L4 | `MAPPED` |
| handoff consumes completion/blocker delta only | execution capability + `C-L1-G06` | `MAPPED` |
| exactly one current task; blocker stops later disclosure | execution capability + `C-L1-G05..G06` | `MAPPED` |
| mission initialization uses Human/Strategy authority | mission capability + `C-L1-G02` + L3 | `MAPPED` |
| archive checks first; mutation only when authorized; preserve history | mission capability + `C-L1-G04` + L3/L4 | `MAPPED` |
| no autonomous business requirements/strategic choices | `C-L1-G02` | `MAPPED` |

## Ecosystem coexistence

| v1 semantic family | Destination | Status |
| --- | --- | --- |
| derive `REUSE|ADAPT|COEXIST|MISSING|CONFLICT` from bounded evidence | coexistence capability -> L3 COEXISTENCE + L4 where decidable | `MAPPED` |
| materialize classification only after review/authority | `C-L1-G04` + coexistence L2/L4 | `MAPPED` |
| prefer references/adapters; preserve native SDD/spec/plan/task ownership | coexistence capability -> L2/L3 | `MAPPED` |
| unresolved authority overlap -> `CONFLICT`, do not choose winner | `C-L1-G05` + coexistence capability | `MAPPED` |
| repository remains governable with no SDD/third-party Skills | coexistence capability + Consumer functional contract | `MAPPED` |
| do not replace development methodology or duplicate compatible native specs/tasks | coexistence capability + `C-L1-G05`, `G07` + L3 | `MAPPED-CONDITIONAL` |

## External Skill discovery and audit

| v1 semantic family | Destination | Status |
| --- | --- | --- |
| discovery starts from required capability, not marketplace | `consumer.skill-trust.discovery` -> L2/L3 | `MAPPED` |
| inspect existing project/user Skills and registries before broader discovery | discovery capability -> L2/L3 | `MAPPED` |
| directory/registry is discovery evidence, not approval authority | `C-L1-G01` + discovery/audit capability | `MAPPED` |
| resolve canonical owner/repository/path + immutable artifact identity | discovery -> audit transition; audit L2/L3/L4 | `MAPPED` |
| audit revision/digest/package/dependency/permission/risk/shadowed identity | audit capability -> L3/L4 | `MAPPED` |
| `skill` command validates facts but does not discover/fetch/grant approval | audit capability + `C-L1-G02`, `G08` + L4 | `MAPPED` |
| no active-project marketplace install during discovery | discovery L2 + `C-L1-G09` | `MAPPED` |
| candidate acquisition only in authorized quarantine/review scope | audit/trust effect boundary + `C-L1-G04`, `G09` | `MAPPED` |
| changed/shadowed/unresolved/over-permissioned artifact rejected until re-audited/re-approved | audit capability -> L3/L4 + `C-L1-G01..G02` | `MAPPED` |

## Cross-cutting mutation/safety

| v1 semantic family | Destination | Status |
| --- | --- | --- |
| read-only validation default | `C-L1-G04` | `MAPPED` |
| identified target + authoritative operation required for mutation | `C-L1-G04` | `MAPPED` |
| no silent overwrite | `C-L1-G04..G05` | `MAPPED` |
| no future-task exposure | `C-L1-G06` | `MAPPED` |
| no production/external contact without authority; no secrets | `C-L1-G09` | `MAPPED` |
| model/provider/marketplace/registry/host precedence is not Governance authority | `C-L1-G01` | `MAPPED` |
| Skill must not become sole copy of Governance rules/state | `C-L1-G01`, `G03` + D051 installed Core/state model | `MAPPED` |
| missing deterministic command is reported; do not pretend tool exists | `C-L1-G08` | `MAPPED` |

## Coverage result

No material Consumer v1 semantic family reviewed above is `UNMAPPED`.

The only `LATER-INSTANCE` item is exact future L0 activation/description wording. Its positive/negative semantic boundary is already represented by the catalog and L1 routing contract, but final candidate text must remain a later MG1/T023 concern.

This result means the topology-neutral routing architecture is **semantically complete enough to characterize v1 preservation**, not that any future candidate has yet proven equivalence.

## Future candidate proof obligation

A future Consumer candidate must demonstrate:

1. every `C-L1-G01..G09` guard is explicit or proven early-enforced;
2. every capability semantic family remains reachable;
3. every row above has an actual generated destination;
4. no v1 semantic is silently dropped because its current wording was moved;
5. L3/L4 behaviors remain shared rather than forked;
6. any intentional behavioral change is separately authorized and not mislabeled as topology/refactoring equivalence.

## Next routing-design status

G-A from `docs/CONSUMER-ROUTING-DESIGN-GAP-REVIEW.md` is closed by this traceability baseline.

No additional Consumer routing semantic layer is required before MG1. Remaining Orchestrator-only work is context/index discoverability and maintenance hygiene; empirical/topology/reference selection remains gated.

## Acceptance invariants

1. source blob identity is explicit;
2. no v1 behavior is changed;
3. every material family is mapped or explicitly flagged;
4. no `UNMAPPED` item is hidden;
5. final L0 candidate wording remains deferred;
6. no R*/B* winner is selected;
7. no actual reference files are created;
8. no T023 oracle/corpus/threshold is defined.