# Agent Governance Capability Catalog

Status: DESIGN-APPROVED  
Model: `docs/CAPABILITY-SOURCE-CONTRACT.md`  
Decision: `docs/decisions/D050-canonical-capability-source-and-evaluated-skill-topology.md`

## Purpose

Compact, topology-neutral inventory of current Agent Governance capability/routing units.

Use it to answer:
- which capability owns an intent/operation;
- which profile/actor/effect boundary applies;
- which focused authority to load next;
- which stable capability ID a D052 oracle case may reference.

Use `docs/CAPABILITY-SOURCE-CONTRACT.md` only when changing the capability model itself.

This catalog is a routing projection of accepted contracts, not Governance Core authority and not a final Skill topology.

```text
capability ID != Skill
sub-capability ID != top-level Skill
operation != capability
profile != Skill
```

IDs remain stable across B0/B1/F2/G3 when semantics are unchanged. Final Skill topology remains MG1/T023 authority after T022.

## Vocabulary

**Profile**
- `consumer` — Consumer runtime/profile surface.
- `source-maintainer-target` — intended source-maintainer surface; this catalog does not imply T022 runtime completion.

**Effect**
- `read` — observation/validation only.
- `project-governance` — durable installed Governance/authority records.
- `project-state` — derived durable coordination state after authority exists.
- `quarantine-trust` — candidate material in review/quarantine scope, not active approval/install.
- `source-markdown` — Orchestrator-owned source design/Markdown mutation.
- `source-executable` — Task-Contract-authorized non-Markdown source mutation.
- `release` — package/migration/branch-publication surface with separate release authority.

**Assurance**
- `deterministic-first` — machine-decidable properties use deterministic verification.
- `mixed` — deterministic checks plus semantic/Strategy interpretation are intrinsic.
- `authority-led` — Human/Strategy/Orchestrator supplies the semantic decision; tooling validates structure/evidence.

These are routing labels, not universal risk scores and not a replacement for D046.

## Reference aliases

| Alias | Path |
| --- | --- |
| `CG` | `docs/GOVERNANCE-SKILL-CONTRACT.md` |
| `MS` | `docs/MAINTAINER-SKILL-CONTRACT.md` |
| `COEX` | `governance-core/COEXISTENCE.md` |
| `CTX` | `governance-core/CONTEXT.md` |
| `LIFE` | `governance-core/LIFECYCLE.md` |
| `PROTO` | `governance-core/PROTOCOL.md` |
| `HANDOFF` | `governance-core/HANDOFF.md` |
| `EXEC` | `governance-core/EXECUTION.md` |
| `EXEC-C` | `governance-core/EXECUTION-CONTROL.md` |
| `DISC` | `governance-core/SKILL-DISCOVERY.md` |
| `SUPPLY` | `governance-core/SKILL-SUPPLY-CHAIN.md` |
| `SEC` | `governance-core/SECURITY.md` |
| `D052C` | `docs/CONFORMANCE-ORACLE-CONTRACT.md` |
| `TEST` | `docs/TESTING-AND-EVALUATION.md` |

# Consumer lifecycle

Parent: `consumer.lifecycle`  
Profile: `consumer`

The following are focused routes inside one semantic family, not independently installable/versioned Skills.

| ID | Current operations | Actor / effect | Assurance | Focused refs |
| --- | --- | --- | --- | --- |
| `consumer.lifecycle.installation` | bootstrap governance; validate installation; portability test | Strategy/Consumer; Human on collision ambiguity / `project-governance` or `read` | `mixed` | `CG`; D051 when packaging matters; `COEX` only on ownership collision |
| `consumer.lifecycle.state` | cold-start reconstruction; validate state; validate protocol events; refresh checkpoint | Strategy/stateless agent; Implementation consumes routed facts / `read`, optional `project-state` refresh | `deterministic-first` | `CG`, `PROTO`, `CTX`, `LIFE` as routed |
| `consumer.lifecycle.execution` | process handoff; validate sequential execution | Strategy review + Implementation current-task recovery / normally `read` | `mixed` | `CG`, `HANDOFF`, `EXEC`, `EXEC-C` when control boundary matters |
| `consumer.lifecycle.mission` | initialize mission; archive completed mission | Human/Strategy / `project-governance` + `project-state` | `authority-led` | `CG`, `LIFE`; `EXEC` for sequencing; `COEX` for native SDD ownership |
| `consumer.lifecycle.coexistence` | inspect ecosystem coexistence | Strategy / `read` | `mixed` | `COEX`; `CG` only for operation constraints |

### Intent boundaries / D052 case families

| ID | Reject / near-miss boundary | Representative oracle families |
| --- | --- | --- |
| `consumer.lifecycle.installation` | source maintenance; app implementation; forced SDD install; second manual AG payload | clean bootstrap, overwrite refusal, source independence, D051 one-install, adapter portability, managed ownership |
| `consumer.lifecycle.state` | inventing strategy; rewriting decisions to fit STATE; unnecessary full-history loading | VALID vs STALE/INVALID, protocol/event validity, cold start without chat, checkpoint derives but does not decide |
| `consumer.lifecycle.execution` | future-task disclosure; handoff broadening scope; continuing after valid blocker | delta-only handoff, exactly-one-task disclosure, dependency readiness, blocker stop, future-task non-read/canary |
| `consumer.lifecycle.mission` | invented business requirements; silent cancellation; duplicate native specs/plans/tasks | missing-strategy refusal, native reference-not-duplication, initialized sequence, archive/history/active-state rules |
| `consumer.lifecycle.coexistence` | choosing authority winner; named-product dependence; unrelated scanning | `REUSE|ADAPT|COEXIST|MISSING|CONFLICT`, managed-file preservation, no-SDD, governance-overlap fail-closed |

# External Skill trust

Parent: `consumer.skill-trust`  
Profile: `consumer`

This family has a distinct provenance/threat/permission envelope. D050 allows G3 to evaluate it as `External Skill Trust`; separation is **not** pre-accepted for release.

| ID | Current operations | Actor / effect | Assurance | Focused refs |
| --- | --- | --- | --- | --- |
| `consumer.skill-trust.discovery` | discover Skill candidates | Strategy / `read` | `mixed` | `DISC`; `CG` only for operation boundary |
| `consumer.skill-trust.audit` | audit Skill supply chain; exact identity/envelope/shadowing validation | Strategy; Human/project authority for exceptions / `quarantine-trust` | `mixed` | `SUPPLY`; `SEC` when security material; `COEX` for host/name collision |

| ID | Reject / near-miss boundary | Representative oracle families |
| --- | --- | --- |
| `consumer.skill-trust.discovery` | marketplace-first selection; active install during discovery; rankings/badges as approval | capability-first discovery, local/project registry preference, unresolved-provenance rejection, directory-not-authority, no install side effect |
| `consumer.skill-trust.audit` | scanner score as approval; mutable/unresolved identity; changed/shadowed artifact without re-audit | exact source/rev/digest, dependency/permission drift, revocation, runtime shadow mismatch, malicious/overbroad envelope, supplemental-scanner-only |

# Source maintenance

Parent: `source.maintenance`  
Profile: `source-maintainer-target`

Role-aware routes do not create new Governance roles or top-level Skills.

| ID | Responsibility / primary intent | Actor / effect | Assurance | Focused refs |
| --- | --- | --- | --- | --- |
| `source.maintenance.orchestrator` | source strategy, research, architecture, Markdown, Task Contracts, review/acceptance, handoff control, checkpointing | ChatGPT Orchestrator / `source-markdown`; exact D052 oracle assets only when designated | `authority-led` | `AGENTS.md`, current checkpoint/context map, smallest applicable Decision/Core/Task policy |
| `source.maintenance.executor` | authorized non-Markdown implementation/refactor/test from exact Task Contract | Agente de IA Ejecutor / `source-executable` | task-specific; deterministic-first where decidable | `AGENTS.md`, exact Task Contract, handoff policy when material, focused implementation/test/toolchain refs |
| `source.maintenance.testing` | on-demand deterministic/property/eval/security testing without generic testing Skill | Orchestrator for D052 oracle; Executor for harness/tests/execution/evidence / ownership-specific source effects | D046-selected | D052 + `D052C` for oracle; `TEST` for assurance; `tests/` or `evals/` router only when selected |
| `source.maintenance.release` | release/public distribution/migration/branch-promotion readiness | Orchestrator + contracted Executor mechanics; Human final authority / `release` | `mixed` | `docs/RELEASES.md`; `docs/BRANCHING.md` when material; D050/D051 for topology/package; exact release gate |

### Source route boundaries

- `source.maintenance.orchestrator` MUST NOT absorb general Executor non-Markdown implementation merely because it can describe it.
- `source.maintenance.executor` requires a persisted Task Contract and MUST NOT acquire Markdown/strategy/acceptance authority.
- `source.maintenance.testing` is a facet callable from the role-appropriate route; it is not a new agent role or release Skill. Required Orchestrator oracle vs supplementary Executor coverage follows D052/`D052C`.
- `source.maintenance.release` MUST NOT treat feature completion as release authorization, bypass Human risk/release authority, project source-maintainer overlays into Consumer footprint, or independently version generated Skill entrypoints.

# Topology projection eligibility

| Capability family | B0 unified | B1 thin router | F2 profile peers | G3 hybrid challenger |
| --- | --- | --- | --- | --- |
| `consumer.lifecycle` | included | included | Consumer Governance | Consumer Lifecycle |
| `consumer.skill-trust` | included | included | Consumer Governance | External Skill Trust challenger |
| `source.maintenance` | included | included | Source Maintainer | Source Maintainer |

Sub-capabilities remain internal routes unless MG1/T023 later proves another activation boundary.

# Cross-cutting invariants

1. Core/accepted contracts remain above catalog metadata.
2. Deterministic tooling does not invent Human/Strategy decisions.
3. Routing metadata does not broaden profile permissions.
4. Read-only validation is default when mutation is unnecessary.
5. Consumer operation remains source-independent after installation.
6. D051 one-product/single-install identity holds regardless of activation count.
7. Skill discovery/audit never makes a directory/registry/provider approval authority.
8. Source routes do not create new agent roles.
9. D052 oracle assets are executable acceptance projections, not authority.
10. Final Skill topology remains MG1/T023 empirical authority.

# Change discipline

- **Catalog clarification:** Orchestrator Markdown update when routing/reference precision changes without behavior change.
- **Semantic capability change:** update controlling Core/Decision/functional contract first when supported behavior, authority, profile, mutation/risk semantics or accepted outcomes change; then update catalog.
- **Topology change:** follows D050/MG1/T023/T024 and MUST NOT fork catalog semantics.
- **Structured projection:** do not introduce a second editable JSON/YAML capability authority until a separate gate selects one source-of-truth/generation direction.
