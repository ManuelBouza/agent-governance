# R029-S2 — Lean-Root Responsibility Contract

Status: COMPLETE  
Parent: `R029 — AGENTS.md / Skill Architecture Refactor Research`  
Subtask: `R029-S2 — Lean-root responsibility contract`  
Baseline-Develop: `03043781084ea1b64d9c7e1a4384f08d37685fd4`  
Input: `docs/orchestrator/R029-S1-ROOT-PRESERVATION-MAP.md`  
Decision-State: EVALUATING  
Normative-Effect: none

## Purpose

This artifact defines only the responsibility boundary of a future lean always-loaded root `AGENTS.md`. It does **not** draft that file, decide the final Skill topology, assign detailed Maintainer Skill internals, create Skills, or promote R029 into normative policy.

The contract answers two questions:

1. What must be knowable before any optional Skill/reference routing can occur safely?
2. What current detail can leave the always-loaded root provided that it remains durably reachable through an explicit destination class?

S1 is the preservation authority for this analysis. S2 does not delete or reinterpret any S1 semantic unit.

## Lean-root inclusion test

A responsibility belongs in the future always-loaded root only when at least one of the following is true:

- it establishes repository/product identity before mutation;
- it establishes Human/Orchestrator/Executor authority or write ownership before delegation;
- it is a fail-closed safety or stop/re-entry rule needed before optional routing;
- it establishes canonical durable authority/bootstrap state before deeper context is loaded;
- it prevents source/consumer, host/role, Skill/authority, or persisted/private-state confusion;
- it is the concise trigger necessary to determine which conditional domain/transverse capability must be loaded;
- it constrains the instruction architecture itself so optional routing cannot silently replace authority.

A rule does not qualify for the root merely because it is important. If it can be applied correctly after an already-safe trigger selects domain/reference context, its detailed procedure belongs outside the always-loaded root.

## Always-loaded responsibility contract

The future root has twelve responsibility families. These are responsibilities, not proposed prose sections or final wording.

| ID | Always-loaded responsibility | Why it must exist before routing | S1 coverage |
| --- | --- | --- | --- |
| LR-01 | Repository identity and contamination boundary | Routing cannot safely choose source-maintenance capabilities if repository identity is not established first | S1-001, 002, 003, 005, 044, 056, 067, 073, 074 |
| LR-02 | Authority model and host neutrality | Optional Skills/hosts must never redefine who owns scope, design, mutation or acceptance | S1-006, 023, 028, 030, 031, 042, 043, 052, 064, 069, 072, 073 |
| LR-03 | Write/file ownership boundary | Write authority must be known before any tool, branch or Skill can mutate repository state | S1-021, 022, 024, 025, 026, 036, 068, 069 |
| LR-04 | SDD stage and re-entry safety boundary | Delegation cannot begin safely if stage ownership and stop conditions depend on later routing | S1-007, 008, 010, 012, 013, 014, 015, 020, 026, 029, 047 |
| LR-05 | Semantic-vs-execution boundary and Human gate | Prevents mechanics from becoming semantic authority and prevents accidental Human terminal delegation | S1-032, 033, 036 |
| LR-06 | Durable authority over ephemeral/private context | Optional context must not override canonical durable state | S1-027, 031, 049, 050, 052, 053, 060, 063 |
| LR-07 | Bootstrap and routing anchors | Progressive disclosure needs enough always-loaded navigation to reach authoritative deeper context without carrying it all | S1-004, 027, 037, 040, 053, 057, 059, 062, 070 |
| LR-08 | Repository mutation/branch safety | Mutation safety must constrain all later workflows before writes occur | S1-036, 045, 070, 072 |
| LR-09 | Durable handoff/completion boundary | Completion cannot depend on local-only or chat-only evidence | S1-048, 049, 050, 051, 052 |
| LR-10 | Research/evidence non-authority and freshness triggers | Research or stale facts must not silently become authority before specialized workflows activate | S1-018, 020, 057, 059, 060 |
| LR-11 | Skill independence/coexistence boundary | Skill routing cannot establish the rules that constrain Skill authority itself | S1-005, 061, 062, 063, 064, 073 |
| LR-12 | Instruction architecture/change-discipline guardrail | Root slimming must itself be constrained against duplication, sprawl and mixed unrelated changes | S1-076, 079 |

These twelve families are a responsibility surface, not a commitment to twelve headings or prose blocks. A later design may compress them provided all covered S1 semantics remain reachable and no pre-routing invariant becomes conditional on successful Skill activation.

## Conditional detail destination contract

Current root detail omitted from the future always-loaded surface remains mandatory, but is loaded only after an always-safe root trigger or domain entry point. S2 defines destination classes, not final Skill package topology.

| Destination class | Responsibility | S1 units whose detailed procedure belongs here |
| --- | --- | --- |
| DR-01 Agent Governance SDD/source-maintenance domain | D053 profiles/deltas, D068 publication/Stage 6/7 procedure, D076 classification/evidence, refactoring/protocol-change procedure | S1-009, 011, 016, 017, 029, 045, 046, 048, 076, 077, 078 |
| DR-02 Agent Governance execution/handoff domain | provisional recipe state, launch-profile adapter detail, coordinator metadata, Task Contract/handoff lifecycle/templates | S1-035, 038, 039, 051 |
| DR-03 Agent Governance checkpoint/research adapters | exact checkpoint lifecycle/schema and `Rxxx`/Decision-state/ledger/supersession conventions | S1-054, 055, 058 |
| DR-04 Agent Governance branching/release domain | release/hotfix conventions and repository-specific branch naming/promotion detail | S1-071 |
| DR-05 Testing/evaluation/supply-chain domain | verification architecture, fixtures, graders/thresholds, external Skill discovery/supply-chain procedure | S1-075 |
| DR-06 Deterministic tool/reference layer | execution-adapter recipes, workspace hygiene mechanics, source toolchain commands/configuration/CI | S1-034, 041, 065, 066 |
| DR-07 Transverse candidate: upstream/version revalidation | operational workflow behind version-sensitive comparison/freshness trigger, subject to later S5 disposition | S1-018; S1-059 when version-sensitive |
| DR-08 Transverse candidate: durable work checkpoint | generic cold-start/durable-frontier workflow behind repository bootstrap trigger, subject to later S7 disposition | S1-027, 053 |
| DR-09 Transverse candidate: executor launch/handoff | reusable launch/session preparation workflow behind launch trigger, subject to later S8 disposition | S1-037; reusable portion of S1-051 only if later proven separable from Agent Governance authority |
| DR-10 Transverse candidate: repository change control/workspace isolation | reusable repository-change/collision-prevention workflow, with workspace placement explicitly deferred to S9 | S1-040, 070 |
| DR-11 Transverse candidate: research evidence traceability | reusable persist/provenance/freshness workflow, subject to later S6 disposition | S1-057; S1-059 when evidence/fact-freshness rather than version-specific |

A root-trigger S1 unit may appear in both a root family and a destination class because the root preserves the concise trigger while the routed destination preserves conditional operational detail. This is progressive disclosure, not duplicate normative ownership.

## S1 coverage ledger

Every S1 unit is accounted for by one of three S2 treatments:

- `ROOT` — semantic obligation remains directly represented in the always-loaded responsibility surface;
- `ROOT+ROUTE` — concise trigger/invariant stays always loaded and conditional operational detail is routed;
- `ROUTE` — detailed material is reachable through a domain/reference class after a safe root trigger.

| Treatment | S1 IDs |
| --- | --- |
| `ROOT` | 001, 002, 003, 005, 006, 008, 012, 013, 014, 020, 022, 023, 024, 025, 026, 028, 030, 031, 033, 036, 042, 043, 044, 047, 049, 050, 052, 056, 060, 061, 063, 064, 067, 068, 069, 072, 073, 074, 079 |
| `ROOT+ROUTE` | 004, 007, 010, 015, 018, 021, 027, 029, 032, 037, 040, 045, 048, 051, 053, 057, 059, 062, 070, 076 |
| `ROUTE` | 009, 011, 016, 017, 019, 034, 035, 038, 039, 041, 046, 054, 055, 058, 065, 066, 071, 075, 077, 078 |

Coverage count: `ROOT=39`, `ROOT+ROUTE=20`, `ROUTE=20`, total `79`, uncovered `0`.

## Important boundary decisions deferred by S2

S2 intentionally does not decide:

- exact final wording, ordering, length or headings of a lean `AGENTS.md`;
- exact Maintainer Skill internal route structure;
- whether each transverse candidate becomes a top-level Skill, an internal route/reference, or is rejected;
- whether workspace isolation is standalone or a repository-change-control sub-route (`S1-040`, later S9);
- whether volatile-fact refresh routes through research-evidence traceability, version revalidation, or a dispatch between them (`S1-059`, later S5/S6/S10);
- packaging, trigger descriptions, host adapters or implementation mechanics for any Skill.

## Completion assessment

S2 completion gate is satisfied:

- every proposed always-loaded responsibility is justified by pre-routing identity, authority, safety, bootstrap, trigger or instruction-architecture necessity;
- all 79 S1 semantic units remain covered;
- all detail proposed outside the always-loaded root has an explicit reachable destination class;
- no root wording was drafted;
- no Skill topology was adopted;
- no normative decision or implementation occurred.

R029-S2 is complete analytically and awaits Human review/acceptance before R029-S3 may be selected.