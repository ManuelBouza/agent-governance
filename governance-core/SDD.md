# Native Spec-Driven Development

SDD-Version: 1.0.0

Load this module whenever a governed change is being framed, specified, designed, planned, implemented, technically reviewed, semantically accepted, or when an existing project-native SDD/specification provider may overlap with Governance.

## Purpose

Define Agent Governance's built-in, tool-neutral Spec-Driven Development method. Native SDD applies to source code, Agent Skills, Markdown/text/policy, configuration, schemas, refactors and comparable governed deliverables without requiring OpenSpec, Spec Kit, Kiro or another external SDD product.

Native SDD is a semantic overlay on the existing Governance lifecycle. It does not create a second task queue, a third agent role, a mandatory vendor-style directory tree, or a competing acceptance authority.

## Core posture

Agent Governance uses **spec-anchored, delta-first SDD**:

- accepted specification remains available after implementation and evolves with the product;
- implementation artifacts remain directly maintainable and reviewable;
- brownfield repositories are specified incrementally through real changes rather than full retrospective backfill;
- tests/evals are evidence projections of approved semantics, never independent authority;
- accepted Governance/Human authority remains above task-local specification artifacts;
- external/project-native SDD providers are reused or adapted when adequate instead of duplicated.

General `spec-as-source` regeneration is not the default.

## Single-owner stage model

Every applicable SDD stage has one accountable owner.

| Stage | Accountable owner | Required result |
| --- | --- | --- |
| `1. Explore / Frame` | Strategy/Governance Agent | Problem, intent, evidence, constraints, research needs and scope boundary are understood. |
| `2. Specify` | Strategy/Governance Agent | Durable normative requirements/spec delta state what SHALL change, remain true or be removed. |
| `3. Design` | Strategy/Governance Agent | The controlling solution design, architecture and material quality/security/privacy/reliability/compatibility decisions are defined. |
| `4. Plan & Trace` | Strategy/Governance Agent | Atomic work, dependencies, acceptance, requirement trace and verification obligations are implementation-ready. |
| `5. Implement` | Implementation Agent | Authorized technical implementation is created strictly inside the approved specification/design/plan. |
| `6. Code Review & Verify` | Implementation Agent | The implementation is technically reviewed, required verification is executed, in-authority defects are corrected and evidence is persisted. |
| `7. Converge / Accept / Evolve` | Strategy/Governance Agent | Specification/design/plan, implementation and evidence are compared; the change is accepted/reworked/rejected and accepted current-spec state is evolved. |

The Human Owner remains final authority over scope, risk, release and overrides.

No stage is dual-owned. In particular:

```text
Strategy owns Explore -> Specify -> Design -> Plan & Trace
Implementation owns Implement -> Code Review & Verify
Strategy owns Converge -> Accept -> Evolve
```

Local coding choices are part of implementation only while they remain inside the approved Design. A choice that materially changes architecture, interfaces, state/data flow, security/trust boundaries, compatibility/migration, failure behavior, acceptance meaning or task decomposition is an upstream Design/Plan issue and requires re-entry.

## Proportional SDD profiles

Every governed change receives SDD reasoning coverage. Separate files are created only when they add durable value.

### `COMPACT`

Use for small, low-risk, local changes or when the changed normative artifact itself is the specification carrier. Explore/Specify/Design/Plan/Trace may be represented inside the existing task/decision/review record.

### `STANDARD`

Use for ordinary features, bugs, Skill behavior changes, compatibility work and non-trivial text/protocol/configuration changes. Require an explicit requirement delta, material design, task/verification trace and convergence evidence.

### `ASSURED`

Use for security-sensitive, public-contract/protocol, high-risk, multi-component, migration or compliance-sensitive work. Require stronger explicit specification/trace evidence and applicable independent/conformance assurance.

Profile selection controls artifact/evidence depth, not stage ownership.

## Current specification carrier

For each touched capability, Strategy SHALL identify the accepted **current specification carrier** when one exists.

A carrier MAY be:

- an adequate project-native spec/SDD artifact;
- a dedicated Governance-native capability specification;
- an existing normative artifact whose contents already define accepted behavior, such as an Agent Skill, policy/protocol Markdown, schema, API contract or comparable product artifact.

Do not create a duplicate full specification when an existing artifact already carries the same accepted semantics adequately.

## Change delta

Behavior-bearing changes express the affected requirement delta using:

- `ADDED` — new required behavior/contract;
- `MODIFIED` — existing required behavior whose accepted meaning changes;
- `REMOVED` — previously required behavior that is intentionally withdrawn;
- `PRESERVED` — material behavior/invariants that MUST remain unchanged and be re-proved.

`PRESERVED` is especially important for refactors, fixes, migrations, security hardening and zero-drift work.

A change with no intended behavior delta may contain only `PRESERVED` requirements plus explicitly authorized structural/objective constraints.

## Requirement quality

Material normative requirements SHOULD be independently traceable and SHALL be verifiable at the level appropriate to the product.

Prefer:

- `SHALL` for mandatory behavior;
- one material obligation per requirement where practical;
- explicit subject/system;
- `what` rather than unnecessary coding prescription;
- explicit trigger/state/error conditions when material;
- Given/When/Then scenarios when examples materially reduce ambiguity;
- stable identifiers when independent traceability is useful;
- a declared verification method or acceptance mapping.

Supported verification methods include `test`, `inspection`, `analysis`, `demonstration`, `eval`, or justified combinations.

## Bidirectional traceability

Material work must support both questions:

```text
Why does this implementation/change exist?
Which implementation/evidence satisfies this requirement?
```

Normal trace:

```text
Human / mission intent
        -> requirement / spec delta
        -> Strategy Design
        -> task / Plan & Trace
        -> Implementation
        -> Code Review & Verify evidence
        -> Strategy Converge / Accept
        -> evolved current specification state
```

A separate traceability matrix is required only when complexity/risk makes it materially useful. Ordinary work may keep the mapping in existing task, handoff, EXCHANGE and review records.

Material implementation with no authorized requirement/scope parent is potential scope drift or gold-plating and must be reviewed before acceptance.

## Design boundary

Design is a Strategy responsibility.

Before implementation readiness, Design must be complete enough that the Implementation Agent does not have to invent missing architecture or acceptance semantics. Material component boundaries, interfaces, state/data flow, trust/security boundaries, compatibility/migration strategy, failure model and other controlling technical decisions belong to Strategy when applicable.

Design does not need to prescribe every function name, variable, loop, helper or equivalent local coding choice. Those remain implementation details while they preserve the controlling Design.

`QUALITY.md` supplies the cross-cutting design/quality envelope; `SECURITY.md` and `EXECUTION-CONTROL.md` add their specific authority when applicable.

## Code Review & Verify

Before marking an implementation task `DONE`, the Implementation Agent SHALL technically review the implementation against the approved specification/design/plan and the applicable quality/security constraints already represented there.

The review covers the applicable subset of:

- requirement/spec-delta fidelity, including `PRESERVED` behavior;
- approved design/task-boundary fidelity;
- correctness, edge cases and failure behavior;
- maintainability and unnecessary complexity;
- security/privacy/reliability/compatibility obligations already in scope;
- required deterministic/property/integration/eval/conformance evidence;
- unauthorized scope additions visible in implementation.

The Implementation Agent MAY correct implementation/test defects found by this review when the correction remains inside the approved specification/design/plan.

If review reveals that an upstream requirement, Design, acceptance meaning or Plan is defective/ambiguous/infeasible, the Implementation Agent reports a blocker/re-entry trigger instead of redefining the upstream stage.

Implementation `DONE` is evidence that stages 5-6 completed; it is not product acceptance.

## Converge / Accept / Evolve

Strategy performs the final semantic/governance review after implementation handoff.

Before acceptance, Strategy establishes:

- `completeness` — every required change has implementation and evidence;
- `correctness` — evidence actually proves the specified outcome;
- `coherence` — specification, Design, Plan, implementation and evidence do not materially contradict;
- `containment` — no material unauthorized behavior/scope was introduced;
- `persistence` — accepted current-spec carrier and resulting product state agree after integration.

Strategy accepts, rejects or sends bounded rework. Accepted deltas are folded into the current specification carrier when a dedicated living spec exists; when the normative product artifact itself is the carrier, the accepted artifact becomes the new current state without duplicate specification text.

Historical change/task/evidence/review records remain auditable according to project retention policy.

## Re-entry

SDD is iterative, not a one-way waterfall.

When stages 5-6 expose an upstream defect:

```text
Implementation discovers spec/design/plan conflict
        -> persist/report evidence
        -> STOP affected work
        -> Strategy re-enters earliest affected stage
        -> Strategy persists revised authority
        -> Implementation resumes stages 5-6
```

A material semantic or design change discovered during implementation MUST NOT be hidden as a coding detail.

## Coexistence with project-native SDD

`COEXISTENCE.md` controls provider overlap.

When an adequate project-native SDD/specification provider exists, Strategy classifies it under `REUSE`, `ADAPT`, `COEXIST`, `MISSING` or `CONFLICT` and references its adequate artifacts instead of duplicating them.

Any reused/adapted provider must map to the single-owner Governance stage model. A tool that lets both agents edit the same spec/design/plan does not transfer authority: Strategy remains the owner of stages 1-4 and 7; Implementation may use private tool workflows only inside stages 5-6.

When no adequate external/project-native SDD provider exists, this native module supplies SDD coverage. Absence of an external SDD product is therefore valid and does not justify installing one merely for methodology availability.

## Artifact-type applicability

Native SDD applies independent of file type.

- **Code** — Strategy specifies/designs observable behavior and controlling solution structure; Implementation codes and technically reviews/verifies it; Strategy converges/accepts/evolves.
- **Agent Skills** — Strategy specifies activation, inputs, outputs, authority, context, failure behavior, side effects/permissions, security boundaries and negative controls. Artifact ownership still controls who writes the Skill/package pieces.
- **Markdown/text/policy** — the normative artifact may itself be the current spec carrier. When Strategy owns that artifact, an Implementation Agent is not inserted merely for ceremony.
- **Configuration/schema** — Strategy specifies desired state, validation, compatibility and failure/runtime effects; Implementation handles only authorized technical realization/review.
- **Refactor** — `PRESERVED` requirements/characterization plus authorized structural Design are the primary contract; Implementation changes structure without changing preserved semantics.

## Historical/brownfield rule

Native SDD is prospective and delta-first.

Do not stop normal project work to generate a full historical specification of an existing repository. Do not rewrite accepted historical task/spec/review records merely to attach new SDD labels. Coverage grows when real work touches a capability.

## Core invariants

```text
specification != proof
plan          != proof
Implementation DONE != acceptance
```

- one accountable owner per SDD stage;
- Strategy owns stages 1-4 and 7;
- Implementation owns stages 5-6 only for its authorized technical implementation;
- no external SDD product is required;
- no duplicate source of truth;
- no full brownfield backfill;
- explicit re-entry for material upstream changes;
- Git/project-native durable records remain the authority surface across chats/agents/tools.
