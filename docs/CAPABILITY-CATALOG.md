# Agent Governance Capability Catalog

Status: DESIGN-APPROVED  
Model contract: `docs/CAPABILITY-SOURCE-CONTRACT.md`  
Controlling decision: `docs/decisions/D050-canonical-capability-source-and-evaluated-skill-topology.md`

## Purpose

Provide the compact, topology-neutral inventory of **currently accepted Agent Governance capability/routing units**.

Use this catalog to answer routine questions such as:

- which capability owns an intent or operation;
- which profile/role boundary applies;
- what mutation/risk surface is involved;
- which focused authority should be loaded next;
- which capability ID a D052 oracle case should reference.

Use `docs/CAPABILITY-SOURCE-CONTRACT.md` when changing the capability model itself.

This catalog is a routing projection of accepted contracts. It is not Governance Core authority and does not select the final Skill topology.

## Reading rules

```text
capability ID != Skill
sub-capability ID != top-level Skill
operation != capability
profile != Skill
```

The same IDs MUST remain stable across B0/B1/F2/G3 when semantics are unchanged.

The final activation topology remains MG1/T023 authority after T022.

## Compact classification vocabulary

### Profile

- `consumer` — Consumer runtime/profile surface.
- `source-maintainer-target` — intended source-maintainer profile/routing surface; runtime implementation remains sequenced through T022 and is not implied complete by this catalog.

### Effect

- `read` — observation/validation only.
- `project-governance` — creates/updates durable installed Governance footprint or authority-controlled project records.
- `project-state` — derives/updates durable coordination state after authority already exists.
- `quarantine-trust` — reads/acquires candidate material only in review/quarantine scope; not active installation/approval by itself.
- `source-markdown` — Orchestrator-owned source Markdown/design mutation.
- `source-executable` — Task-Contract-authorized non-Markdown source mutation.
- `release` — release/package/migration/branch-publication surface with separate Human/release authority.

### Assurance/judgment

- `deterministic-first` — machine-decidable properties should be checked deterministically; judgment is only for unresolved semantic boundaries.
- `mixed` — deterministic checks plus model/Strategy interpretation are both intrinsic.
- `authority-led` — Human/Strategy/Orchestrator authority is required for the semantic decision; deterministic tooling may validate structure/evidence only.

These labels are routing metadata, not universal risk scores or a replacement for D046 assurance-plane selection.

# Consumer family

Parent: `consumer.lifecycle`  
Profile: `consumer`

The parent remains one semantic family even though focused sub-routes reduce context. Its sub-routes MUST NOT be interpreted as separately installable/versioned Skills.

## `consumer.lifecycle.installation`

**Responsibility:** establish/validate a reusable Consumer Governance installation while preserving D051 single-install/self-bootstrap, source independence and existing project ownership.

**Current operations:**
- bootstrap governance;
- validate installation;
- portability test.

**Primary intent:** initialize or validate Agent Governance in a target project; verify installed-product portability/source independence.

**Near misses / exclusions:**
- source-product maintenance;
- application feature implementation;
- installing an unrelated SDD because none exists;
- requiring a second manually installed Agent Governance support payload.

**Primary actor:** Strategy/Consumer operator; Human input where project authority/overwrite ambiguity exists.

**Effect:** `project-governance` for bootstrap; `read` for validation/portability.

**Assurance/judgment:** `mixed` — layout/version/reference/self-bootstrap rules are deterministic-first; existing ownership/collision interpretation may require Strategy judgment.

**Focused authority:**
- `docs/GOVERNANCE-SKILL-CONTRACT.md`;
- D051 when install/package semantics are material;
- `governance-core/COEXISTENCE.md` only when project-native ownership/collisions are material;
- adapter/Core modules only when the concrete install check routes to them.

**D052 oracle families:** clean bootstrap, overwrite refusal, source independence, single-install/no supplemental payload, adapter portability, project-native ownership preservation.

## `consumer.lifecycle.state`

**Responsibility:** reconstruct and validate effective Governance state/protocol facts without inventing strategy.

**Current operations:**
- cold-start reconstruction;
- validate state;
- validate protocol events;
- refresh checkpoint.

**Primary intent:** determine current frontier/state validity or materialize derived checkpoint state after authoritative records/events already exist.

**Near misses / exclusions:**
- deciding new project strategy;
- rewriting decisions to make STATE consistent;
- loading full history when routed current state is sufficient.

**Primary actor:** Strategy and compatible stateless agents; Implementation may consume routed current-state facts within its disclosed task.

**Effect:** `read` for reconstruction/validation; `project-state` for authorized checkpoint refresh.

**Assurance/judgment:** `deterministic-first` for JSONL/protocol/state derivation; authority ambiguity remains Strategy/Human territory.

**Focused authority:**
- `docs/GOVERNANCE-SKILL-CONTRACT.md`;
- `governance-core/PROTOCOL.md` for event/protocol validity;
- `governance-core/CONTEXT.md` for routed reconstruction/context behavior;
- `governance-core/LIFECYCLE.md` when lifecycle state/gates are material.

**D052 oracle families:** VALID vs STALE/INVALID, monotonic/actor/event/state-transition cases, cold-start without chat history, checkpoint derivation without invented decisions.

## `consumer.lifecycle.execution`

**Responsibility:** preserve delta-only handoff and one-task-at-a-time sequential execution/disclosure semantics.

**Current operations:**
- process handoff;
- validate sequential execution.

**Primary intent:** review/recover the current disclosed task position, validate handoff evidence, dependencies and future-task non-disclosure.

**Near misses / exclusions:**
- disclosing future task contents for convenience;
- treating a handoff as authority to broaden scope;
- continuing after a valid blocker.

**Primary actor:** Strategy for completion/blocker review; Implementation for current sequence/disclosed-task recovery.

**Effect:** normally `read`; any later state mutation follows the applicable authoritative lifecycle/state operation rather than this route inventing it.

**Assurance/judgment:** `mixed` — sequence/dependency/disclosure invariants are deterministic-first; acceptance/blocker semantics may require Strategy review.

**Focused authority:**
- `docs/GOVERNANCE-SKILL-CONTRACT.md`;
- `governance-core/HANDOFF.md`;
- `governance-core/EXECUTION.md`;
- `governance-core/EXECUTION-CONTROL.md` only when the control boundary is material.

**D052 oracle families:** delta-only handoff, exactly one disclosed task, dependency readiness, blocker stops later disclosure, future-task canary/non-read evidence.

## `consumer.lifecycle.mission`

**Responsibility:** create and retire mission-level durable coordination records from authorized Human/Strategy intent.

**Current operations:**
- initialize mission;
- archive completed mission.

**Primary intent:** establish a new governed mission/workplan or archive a terminal mission while preserving history.

**Near misses / exclusions:**
- inventing business requirements;
- silently cancelling unresolved work;
- duplicating project-native specs/plans/tasks already owned by a compatible SDD.

**Primary actor:** Human/Strategy.

**Effect:** `project-governance` + `project-state`.

**Assurance/judgment:** `authority-led` for mission/scope meaning; deterministic-first for structure, references, terminal/archive invariants.

**Focused authority:**
- `docs/GOVERNANCE-SKILL-CONTRACT.md`;
- `governance-core/LIFECYCLE.md`;
- `governance-core/EXECUTION.md` when workplan/task sequencing is material;
- `governance-core/COEXISTENCE.md` when native SDD/spec ownership is present.

**D052 oracle families:** missing-strategy refusal, native spec reference-not-duplication, initialized records/sequence, archive history preservation and unresolved-active-state refusal.

## `consumer.lifecycle.coexistence`

**Responsibility:** detect/classify project-native capability ownership and fail closed on unresolved overlap before Governance duplicates or overwrites behavior.

**Current operation:**
- inspect ecosystem coexistence.

Bootstrap/mission/task flows may call this route conditionally; its existence does not require independent activation packaging.

**Primary intent:** determine whether an existing SDD, Skill, registry, memory/context, permission or branch/workflow capability should be `REUSE`, `ADAPT`, `COEXIST`, `MISSING`, or `CONFLICT`.

**Near misses / exclusions:**
- choosing an authority winner on semantic conflict;
- requiring recognition of a named third-party product;
- scanning unrelated project surfaces.

**Primary actor:** Strategy.

**Effect:** `read` by default; subsequent integration/mutation requires the owning capability/authority.

**Assurance/judgment:** `mixed` — evidence discovery can be deterministic; semantic ownership classification may require Strategy judgment.

**Focused authority:**
- `governance-core/COEXISTENCE.md`;
- `docs/GOVERNANCE-SKILL-CONTRACT.md` only when operation-level constraints are needed.

**D052 oracle families:** REUSE/ADAPT/COEXIST/MISSING/CONFLICT fixtures, managed-file preservation, no-SDD behavior, semantic governance overlap fail-closed.

# External Skill trust family

Parent: `consumer.skill-trust`  
Profile: `consumer`

This family has a materially different provenance/threat/permission envelope from ordinary lifecycle work. D050 permits it to be evaluated separately as the G3 `External Skill Trust` challenger, but this catalog does **not** pre-accept a separate release Skill.

## `consumer.skill-trust.discovery`

**Responsibility:** locate and resolve candidate Skill artifacts from a required capability without installing/trusting them.

**Current operation:**
- discover Skill candidates.

**Primary intent:** find candidate external Skills for an uncovered capability and resolve owner/repository/path/canonical provenance inputs.

**Near misses / exclusions:**
- marketplace-first selection without capability need;
- active-project install commands during discovery;
- treating rankings/badges/registry presence as approval.

**Primary actor:** Strategy.

**Effect:** `read`; optional candidate acquisition only in later authorized quarantine/audit flow.

**Assurance/judgment:** `mixed` — provenance resolution has deterministic checks; relevance/source confidence may require judgment.

**Focused authority:**
- `governance-core/SKILL-DISCOVERY.md`;
- `docs/GOVERNANCE-SKILL-CONTRACT.md` when operation boundary is needed.

**D052 oracle families:** capability-first search, local/project registry preference, unresolved-provenance rejection, directory-not-authority, no active install side effects.

## `consumer.skill-trust.audit`

**Responsibility:** audit exact candidate artifact identity, dependencies, permissions and execution envelope before approval/installation/update.

**Current operation:**
- audit Skill supply chain.

This route also owns exact canonical source/revision/digest, dependency/permission envelope and host-shadowing validation semantics associated with approved Skill artifacts.

**Primary intent:** determine whether a resolved candidate/existing approved Skill artifact remains acceptable under exact provenance and execution-envelope constraints.

**Near misses / exclusions:**
- trusting directory/platform scanner results as approval;
- approving mutable/unresolved identity;
- accepting changed/shadowed artifacts without re-audit;
- executing candidate code merely to inspect it in the active project.

**Primary actor:** Strategy; Human/explicit project authority retains approval/exception authority where required.

**Effect:** `quarantine-trust`; active installation/update is outside audit until exact approval and applicable mutation authority exist.

**Assurance/judgment:** `mixed` — identity/digest/envelope comparisons deterministic-first; risk/approval suitability remains authority/judgment mediated.

**Focused authority:**
- `governance-core/SKILL-SUPPLY-CHAIN.md`;
- `governance-core/SECURITY.md` when security envelope is material;
- `governance-core/COEXISTENCE.md` when host precedence/name collision is material.

**D052 oracle families:** exact identity/digest, dependency/permission drift, revocation/supersession, shadowed runtime artifact mismatch, malicious/overbroad permission cases, supplemental-scanner-not-authority.

# Source-maintenance family

Parent: `source.maintenance`  
Profile: `source-maintainer-target`

The Maintainer contract uses role-aware internal routing. These routes do not create new Governance roles or top-level Skills.

## `source.maintenance.orchestrator`

**Responsibility:** route ChatGPT Orchestrator source-product strategy, research, architecture, Markdown, Task Contracts, review/acceptance, handoff control and checkpointing to the smallest relevant source authority.

**Primary intent:** source-product work whose semantic/write ownership belongs to the Orchestrator.

**Near misses / exclusions:**
- taking over general non-Markdown implementation because it is difficult;
- consumer-project governance;
- loading every source policy for a focused decision.

**Primary actor:** ChatGPT Orchestrator.

**Effect:** `source-markdown`; D052-designated non-Markdown oracle assets only when a governing contract/gate explicitly assigns them.

**Assurance/judgment:** `authority-led` for architecture/acceptance; deterministic verification where a selected property is machine-decidable.

**Focused authority:**
- `AGENTS.md`;
- `docs/orchestrator/CHECKPOINT.md` for current frontier;
- `docs/CONTEXT-MAP.md` for stable routing;
- smallest applicable Decision/Core/Task/operation policy selected by the current concern.

**D052 oracle families:** authored only when a concrete source Task Contract/gate chooses `orchestrator-conformance` or `mixed`; generic lifecycle is governed by D052 + `docs/CONFORMANCE-ORACLE-CONTRACT.md`.

## `source.maintenance.executor`

**Responsibility:** route an authorized Agente de IA Ejecutor to the exact Task Contract, implementation surface, required verification and handoff without exposing a parallel strategy layer.

**Primary intent:** implement/refactor/test authorized non-Markdown source-product work already persisted in a Task Contract.

**Near misses / exclusions:**
- uncontracted source changes;
- Markdown mutation;
- acceptance/strategy redefinition;
- consumer-project feature implementation.

**Primary actor:** Agente de IA Ejecutor.

**Effect:** `source-executable` within exact Task Contract scope.

**Assurance/judgment:** `deterministic-first` for contracted machine-decidable verification plus task-specific assurance planes; semantic acceptance remains Orchestrator/Human authority.

**Focused authority:**
- `AGENTS.md`;
- exact `docs/tasks/TNNN-*.md`;
- `docs/EXECUTOR-HANDOFFS.md` when handoff/finalization is material;
- only task-specific implementation/test/toolchain references.

**D052 relationship:** execute frozen Orchestrator oracle when designated; supplementary/implementation tests and harness remain Executor-owned. Semantic oracle mutation is prohibited.

## `source.maintenance.testing`

**Responsibility:** provide an on-demand testing/evaluation capability route without creating a generic testing Skill or duplicating test-runner authority.

This is a **facet of source maintenance**, callable from the Orchestrator or Executor route according to D052 ownership; it is not an independent agent role or release Skill.

**Current focused areas:**
- deterministic test maintenance;
- property/state-machine testing;
- Skill/eval maintenance;
- security/supply-chain testing.

**Primary actor:** Orchestrator for semantic conformance/oracle authoring when D052 assigns it; Executor for technical harness, implementation/supplementary tests and all required execution/evidence.

**Effect:** `source-markdown` and exact D052 oracle assets on the Orchestrator side; `source-executable` on the Executor side.

**Assurance/judgment:** selected by D046/`docs/TESTING-AND-EVALUATION.md`; do not use model-mediated verification where deterministic checks suffice.

**Focused authority:**
- D052 + `docs/CONFORMANCE-ORACLE-CONTRACT.md` for semantic oracle work;
- `docs/TESTING-AND-EVALUATION.md` for assurance architecture;
- `tests/README.md` or `evals/README.md` only for the selected execution surface;
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md` only when executable local tooling is material.

## `source.maintenance.release`

**Responsibility:** route release/public-distribution/migration readiness work while preserving Human release authority and source/Consumer separation.

**Primary intent:** prepare or verify an Agent Governance release, package/migration artifact, branch promotion or public distribution readiness.

**Near misses / exclusions:**
- treating ordinary feature completion as release authorization;
- bypassing Human release/risk decisions;
- projecting source-maintainer overlays into Consumer footprint;
- independently versioning generated Skill entrypoints.

**Primary actor:** Orchestrator + authorized Executor mechanics as contracted; Human retains final release/override authority.

**Effect:** `release` plus bounded `source-markdown`/`source-executable` preparation according to ownership.

**Assurance/judgment:** `mixed` — reproducibility/package/provenance gates deterministic-first; release/risk judgment remains Human/Orchestrator authority.

**Focused authority:**
- `docs/RELEASES.md`;
- `docs/BRANCHING.md` when promotion/branch semantics are material;
- D050/D051 when generated topology or one-install packaging is material;
- exact release/migration Task Contract/gate.

# Topology projection eligibility

The catalog does not score candidates. It only records how the same capability IDs may be exposed without semantic forks.

| Capability family | B0 unified dispatcher | B1 thin router | F2 profile peers | G3 hybrid challenger |
| --- | --- | --- | --- | --- |
| `consumer.lifecycle` | included | included | Consumer entrypoint | Consumer Lifecycle entrypoint |
| `consumer.skill-trust` | included | included | Consumer entrypoint | External Skill Trust challenger |
| `source.maintenance` | included | included | Source Maintainer entrypoint | Source Maintainer entrypoint |

Sub-capabilities remain internal routes unless MG1/T023 later provides evidence for a different activation boundary.

# Cross-cutting invariants

Every catalog entry inherits these rules:

1. Governance Core/accepted contracts remain above catalog metadata.
2. Deterministic tooling does not invent Human/Strategy decisions.
3. Profile boundaries are not broadened by routing metadata.
4. Read-only validation is the default where mutation is not required.
5. Consumer operation remains source-independent after install.
6. D051 single-install/one-product identity is preserved regardless of activation count.
7. External Skill discovery/audit does not make a directory/registry/provider an approval authority.
8. Source-maintainer routes do not create additional agent roles.
9. D052 oracle assets remain executable acceptance projections, not authority.
10. Final Skill topology remains an empirical MG1/T023 decision.

# Change discipline

### Routine catalog clarification

Orchestrator-owned Markdown change when it only improves routing/reference precision without changing accepted behavior.

### Semantic capability change

Adding/removing supported behavior, changing authority/mutation/profile/risk semantics, or changing accepted outcomes requires the controlling Core/Decision/functional contract first. Then update this catalog.

### Topology change

Changing which generated Skill exposes a capability follows D050/MG1/T023/T024 authority and MUST NOT fork the capability semantics in this catalog.

### Structured projection

This Markdown catalog is the current human-readable canonical projection. Do not create a second editable JSON/YAML capability authority until a separate gate demonstrates a need and selects one source-of-truth/generation direction.
