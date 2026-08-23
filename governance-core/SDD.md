# Native Spec-Driven Development

SDD-Version: 1.0.0

Load this module for governed development framing, specification, Design, planning, implementation review, convergence, or SDD-provider overlap.

## Purpose and posture

Agent Governance provides built-in, tool-neutral, **spec-anchored, delta-first SDD** for code, Agent Skills, Markdown/text/policy, configuration, schemas, refactors and comparable deliverables.

Native SDD:
- evolves accepted specification with the product instead of treating implementation as the only durable intent;
- keeps implementation artifacts directly maintainable/reviewable rather than using general `spec-as-source` regeneration;
- grows brownfield specification coverage through real changes, not full retrospective backfill;
- treats tests/evals as evidence projections, never authority;
- reuses/adapts adequate project-native SDD providers instead of duplicating them;
- creates no second task queue, third agent role, mandatory vendor directory tree or competing acceptance authority.

## Single-owner stages

Every applicable stage has one accountable owner.

| Stage | Owner | Result |
| --- | --- | --- |
| `1. Explore / Frame` | Strategy | Problem, intent, evidence, constraints and scope are understood. |
| `2. Specify` | Strategy | Durable normative requirements/spec delta state what SHALL change, remain true or be removed. |
| `3. Design` | Strategy | Controlling solution architecture and material quality/security/privacy/reliability/compatibility decisions are defined. |
| `4. Plan & Trace` | Strategy | Atomic work, dependencies, acceptance, trace and verification obligations are implementation-ready. |
| `5. Implement` | Implementation | Authorized technical implementation is created inside the approved specification/Design/Plan. |
| `6. Code Review & Verify` | Implementation | Implementation is technically reviewed, required verification runs, in-authority defects are corrected and evidence is persisted. |
| `7. Converge / Accept / Evolve` | Strategy | Specification/Design/Plan, implementation and evidence converge; accepted current-spec state is evolved. |

The Human Owner remains final authority over scope, risk, release and overrides.

No stage is dual-owned. Local coding choices belong to Implementation only while they preserve approved Design. A choice that materially changes requirements, architecture/interfaces/state/data flow/trust boundaries, compatibility/migration, failure behavior, acceptance or task decomposition requires Strategy re-entry.

## Proportional profiles

Every governed change receives SDD reasoning coverage; separate files are created only when they add durable value.

- `COMPACT` — small/low-risk/local work or when the changed normative artifact itself is the specification carrier. Existing task/decision/review records may carry the SDD concerns.
- `STANDARD` — ordinary features, bugs, Skill behavior changes, compatibility work and non-trivial text/protocol/config changes. Require explicit delta, material Design, trace and convergence evidence.
- `ASSURED` — security-sensitive, public-contract/protocol, high-risk, multi-component, migration or compliance-sensitive work. Require stronger explicit specification/trace and applicable independent/conformance assurance.

Profile depth never changes stage ownership.

## Current specification carrier

For each touched capability, Strategy SHALL identify the accepted **current specification carrier** when one exists. It MAY be:
- an adequate project-native spec/SDD artifact;
- a dedicated Governance-native specification;
- an existing normative product artifact such as an Agent Skill, protocol/policy Markdown, schema or API contract.

Do not duplicate adequate current truth merely to create a new spec file.

## Requirement delta and quality

Behavior-bearing changes use the applicable classes:
- `ADDED` — new required behavior/contract;
- `MODIFIED` — existing required behavior whose accepted meaning changes;
- `REMOVED` — previously required behavior intentionally withdrawn;
- `PRESERVED` — material behavior/invariants that MUST remain unchanged and be re-proved.

A zero-behavior-delta change may use only `PRESERVED` plus authorized structural/objective constraints.

Material normative requirements SHALL be verifiable at the appropriate product level and SHOULD be independently traceable when useful. Prefer `SHALL`, one material obligation per requirement, an explicit subject, `what` over unnecessary coding prescription, explicit trigger/state/error conditions, stable IDs when needed, and Given/When/Then where examples materially reduce ambiguity.

Supported verification methods: `test`, `inspection`, `analysis`, `demonstration`, `eval`, or justified combinations.

## Bidirectional traceability

Material work must answer both:

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

Use a separate matrix only when complexity/risk makes it useful. Untraceable material implementation is potential scope drift/gold-plating and must be reviewed before acceptance.

## Design boundary

Design is Strategy-owned and must be complete enough that Implementation does not invent missing architecture or acceptance semantics. Define material component boundaries, interfaces, state/data flow, trust/security boundaries, compatibility/migration, failure model and other controlling decisions when applicable.

Do not prescribe every function, variable, helper or equivalent local coding choice unless it is materially controlling. `QUALITY.md`, `SECURITY.md` and `EXECUTION-CONTROL.md` supply applicable cross-cutting boundaries.

## Code Review & Verify

Before `DONE`, Implementation SHALL technically review the submitted implementation against the approved specification/Design/Plan for the applicable subset of:
- requirement/spec-delta fidelity, including `PRESERVED` behavior;
- Design/task-boundary fidelity;
- correctness, edge cases and failure behavior;
- maintainability/unnecessary complexity;
- represented security/privacy/reliability/compatibility obligations;
- required deterministic/property/integration/eval/conformance evidence;
- unauthorized scope additions.

Implementation MAY correct implementation/test defects inside approved authority. If review exposes a defective/ambiguous/infeasible upstream requirement, Design, Plan or acceptance meaning, report a blocker/re-entry trigger instead of redefining it.

Implementation `DONE` proves stages 5-6 only; it is not product acceptance.

## Converge / Accept / Evolve

Strategy reviews the implementation and evidence for:
- `completeness` — every required change has implementation/evidence;
- `correctness` — evidence proves the specified outcome;
- `coherence` — specification, Design, Plan, implementation and evidence do not materially contradict;
- `containment` — no material unauthorized behavior/scope was introduced;
- `persistence` — accepted current-spec carrier and product state agree after integration.

Strategy accepts, rejects or sends bounded rework. Accepted deltas are folded into a dedicated living spec when one exists; when the normative product artifact itself is the carrier, that accepted artifact becomes current truth without duplicate specification text. Preserve historical change/task/evidence/review records under project retention policy.

## Re-entry

SDD is iterative, not a one-way waterfall.

```text
Implementation discovers upstream spec/Design/Plan defect
 -> persist/report evidence and STOP affected work
 -> Strategy re-enters earliest affected stage
 -> Strategy persists revised authority
 -> Implementation resumes stages 5-6
```

A material semantic/Design change MUST NOT be hidden as a coding detail.

## Provider coexistence

`COEXISTENCE.md` controls overlap. When an adequate project-native SDD provider exists, Strategy classifies it as `REUSE`, `ADAPT`, `COEXIST`, `MISSING` or `CONFLICT` and references adequate native artifacts instead of duplicating them.

Reused/adapted tools still map to the single-owner stage model. Host-native SDD/planning tools used by Implementation inside stages 5-6 remain private implementation aids and do not gain specification/Design/Plan/acceptance authority.

When no adequate external/project-native provider exists, this module supplies SDD. Absence of an external SDD product is valid and does not justify installing one merely for methodology availability.

## Artifact applicability

- **Code** — Strategy specifies/designs; Implementation implements/reviews/verifies; Strategy converges/accepts/evolves.
- **Agent Skills** — Strategy owns activation/input/output/authority/context/failure/side-effect/security semantics; artifact write ownership still controls materialization.
- **Markdown/text/policy** — the artifact may itself be the current spec carrier. Do not introduce Implementation merely for ceremony when Strategy owns the artifact.
- **Configuration/schema** — Strategy owns desired state/validation/compatibility/failure/runtime semantics; Implementation handles authorized technical realization/review.
- **Refactor** — `PRESERVED` requirements/characterization plus authorized structural Design are the contract; Implementation changes structure without semantic drift.

## Brownfield and core invariants

Do not stop normal work to generate full historical specs or rewrite accepted historical task/spec/review records merely to attach SDD labels. Coverage grows when real work touches a capability.

```text
specification != proof
plan          != proof
Implementation DONE != acceptance
```

- Strategy owns stages 1-4 and 7; Implementation owns stages 5-6 only for authorized technical work.
- no external SDD product is required;
- no duplicate source of truth;
- no full brownfield backfill;
- material upstream changes use explicit re-entry;
- Git/project-native durable records remain the cross-chat/cross-agent authority surface.
