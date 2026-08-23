# D053 — Native spec-anchored delta-first development

Status: PROPOSED  
Date: 2026-08-23  
Authority requested: Human Owner / ChatGPT Orchestrator  
Research basis: `docs/SPEC-DRIVEN-DEVELOPMENT-RESEARCH.md`

## Problem

Agent Governance already performs substantial preimplementation framing, research, architecture, task contracting, readiness, verification and review, but specification is not yet a first-class durable development primitive across source maintenance and governed consumer projects.

Current Core coexistence semantics treat project-native SDD as an optional external capability and permit a no-SDD mode. The Human Owner now wants every governed development unit — code, Agent Skill, policy/text artifact, configuration, schema or comparable deliverable — to receive SDD discipline without requiring a third-party SDD product.

The ecosystem does not provide one settled formal SDD standard. OpenSpec, GitHub Spec Kit, Kiro and other current systems differ materially in artifact layout, lifecycle and source-of-truth posture. Copying one tool wholesale would also conflict with Agent Governance's executor neutrality, coexistence model and existing F/PD lifecycles.

The decision therefore must adopt the engineering invariants of SDD while preserving Agent Governance authority, role ownership, progressive context loading and verification independence.

## Decision

Subject to Human Owner acceptance, Agent Governance SHALL adopt a **native, tool-neutral, spec-anchored, delta-first SDD capability** for both:

- maintenance/development of the Agent Governance source product; and
- governed consumer-project development when no adequate project-native SDD provider is already primary.

No OpenSpec, Spec Kit, Kiro or other external SDD framework becomes a required product dependency.

## 1. SDD posture

Agent Governance SHALL use `spec-anchored` SDD as the default posture:

- durable specification remains available after implementation and evolves with the product;
- implementation artifacts remain directly maintainable and reviewable;
- specifications are not treated as nondeterministic code generators whose output automatically supersedes reviewed implementation;
- tests/evals remain evidence rather than authority;
- accepted Governance/Decision constraints remain above task-local specification semantics.

General `spec-as-source` development is not adopted as the default.

## 2. Brownfield delta-first adoption

Agent Governance SHALL NOT require full retrospective specification of an existing source or consumer repository before SDD can be used.

Specification coverage grows through real accepted changes:

```text
current capability/artifact
        + focused proposed delta
        + implementation/verification
        -> accepted updated capability/artifact
```

Only the slice affected by current work is required to become newly specified unless a broader specification is independently justified.

## 3. SDD logical concerns

All governed development SHALL address these seven logical concerns:

1. `Explore / Frame` — establish problem, intent, constraints, evidence and relevant research.
2. `Specify` — define what SHALL change, be true, or remain unchanged.
3. `Design` — define controlling architecture/quality/security/compatibility boundaries and the feasible solution shape.
4. `Plan & Trace` — derive atomic work and map requirements to tasks and verification.
5. `Implement` — realize the approved change.
6. `Verify & Converge` — prove the implementation and specification agree without material omissions or unauthorized additions.
7. `Integrate & Evolve` — accept the result, update current specification state and preserve change history.

These concerns SHALL be mapped onto the existing Consumer F0-F6 and source PD0-PD6 lifecycles. D053 does not create a competing third lifecycle.

## 4. Proportional artifact materialization

SDD coverage is mandatory; separate file creation is not.

Agent Governance SHALL use proportional materialization so small work does not become ceremonial overhead.

### `COMPACT`

For small/low-risk/local work or where the product artifact itself is the specification. SDD concerns may be collapsed into existing Decision/Task Contract/review records.

### `STANDARD`

For ordinary behavior-bearing features, bugs, Skill changes, compatibility work and non-trivial text/protocol changes. Explicit requirement delta, material design, task/verification trace and convergence evidence are required.

### `ASSURED`

For security-sensitive, protocol/public-contract, high-risk, multi-component or compliance-sensitive work. Dedicated specification/trace evidence and stronger assurance are required as appropriate; D052 conformance ownership applies when semantic authority is material.

The selected profile controls artifact/evidence depth, not whether SDD applies.

## 5. Current specification carrier

For each touched capability, Strategy/Orchestrator SHALL identify the accepted **current specification carrier** when one exists.

A current specification carrier MAY be:

- an adequate project-native SDD/spec artifact;
- a dedicated Agent-Governance-native capability specification;
- an existing normative artifact whose contents themselves define the accepted behavior, including an Agent Skill, Governance Core protocol document, policy, schema or other semantically authoritative product artifact.

Agent Governance MUST NOT create a duplicate full specification when an existing artifact already carries the same accepted semantics adequately.

## 6. Proposed change delta

Behavior-bearing changes SHALL express the affected requirement delta using these semantic classes:

- `ADDED`
- `MODIFIED`
- `REMOVED`
- `PRESERVED`

`PRESERVED` records critical behavior/invariants that MUST remain unchanged and be evidenced after the change. It is particularly important for refactors, bug fixes, migrations and security hardening.

A change with no intended behavior/contract delta may use only `PRESERVED` plus structural/objective constraints rather than inventing artificial new behavior.

## 7. Requirement quality

Material normative requirements SHOULD be independently traceable and SHALL be testable/verifiable at the level appropriate to the product.

Preferred requirements discipline:

- use `SHALL` for mandatory behavior;
- keep one material obligation per requirement where practical;
- state the subject/system explicitly;
- separate `what` from unnecessary implementation prescription;
- make triggering/state/error conditions explicit where material;
- use Given/When/Then scenarios when concrete examples materially reduce ambiguity;
- assign a stable identifier when the requirement needs independent durable traceability;
- identify the intended verification method with the requirement or its acceptance mapping.

Supported verification methods include `test`, `inspection`, `analysis`, `demonstration`, `eval`, or justified combinations.

## 8. Bidirectional traceability

Material SDD work SHALL provide traceability sufficient to answer both directions:

```text
Why does this implementation/change exist?
Which implementation/evidence satisfies this requirement?
```

The normal trace is:

```text
Human / mission intent
        -> requirement / spec delta
        -> controlling design constraint
        -> Task Contract / task
        -> implementation artifact
        -> verification evidence
        -> Orchestrator acceptance
```

A separate traceability matrix is required only when complexity/risk makes it materially useful. For ordinary work the mapping MAY be represented inside Task Contracts, handoffs and reviews.

Material implementation with no authorized requirement/scope parent is potential gold-plating/scope drift and MUST be reviewed before acceptance.

## 9. Orchestrator / Executor ownership by SDD concern

The binary role model remains unchanged.

### Human Owner

Owns final material product, scope, risk, release and override decisions.

### ChatGPT Orchestrator

Owns:

- Explore/Frame synthesis and external research conclusions;
- normative requirement/specification semantics and spec deltas;
- strategic architecture, quality/security/compatibility constraints and solution-diagram acceptance;
- Task Contracts, task decomposition, readiness and trace semantics;
- D052-designated conformance/oracle semantics;
- semantic convergence review;
- accepted current-spec evolution and integration/archival records.

### Agente de IA Ejecutor

Owns:

- technical investigation inside approved scope;
- detailed implementation design not reserved as a controlling strategic decision;
- authorized code/config/non-Markdown implementation assets;
- implementation-focused and exploratory tests/evals;
- execution of all required verification, including Orchestrator-owned conformance;
- diagnosis, measurements, evidence and executor handoffs.

The Executor MAY propose a spec/design correction when evidence exposes a defect or ambiguity, but MUST NOT silently redefine normative requirement/expected-result semantics.

## 10. Iteration and re-entry

SDD is not a one-way waterfall.

If new evidence changes a material requirement, design constraint or acceptance meaning, work SHALL re-enter the earliest affected SDD concern.

For normative changes:

```text
Executor discovers mismatch
        -> report gap/conflict
        -> Orchestrator revises/persists authority
        -> downstream plan/oracle updated as needed
        -> Executor resumes from revised authority
```

A material semantic change discovered during implementation MUST NOT be hidden as an implementation detail.

## 11. Verify & Converge gate

Before acceptance, SDD review SHALL establish:

- `completeness` — required behavior/change has implementation and evidence;
- `correctness` — evidence actually proves the specified outcome;
- `coherence` — specification, design, task plan, implementation and verification do not materially contradict;
- `containment` — no material unauthorized behavior/scope was added;
- `persistence` — after integration the accepted current spec carrier and product state agree.

Executor `DONE` remains evidence only. Orchestrator convergence review remains acceptance authority subject to Human Owner authority.

## 12. Integrate & Evolve semantics

After acceptance:

- an accepted delta SHALL be folded into the current specification carrier when a dedicated living spec exists;
- when the changed normative product artifact itself is the specification carrier, that accepted artifact becomes the new current specification state without duplicating its contents elsewhere;
- the change delta, Decision/Task Contract, verification/handoff and review history SHALL remain auditable in Git according to applicable retention/archive policy.

The project therefore combines a living current specification with durable flow-forward change history.

## 13. Artifact-type applicability

SDD applies independent of file type.

### Application/source code

Specify externally/materially observable state/API/error/performance/security behavior and verify it with appropriate deterministic/integration/property evidence.

### Agent Skills

Specify activation, inputs, outputs, authority, required context, failure behavior, side effects/permissions, security boundaries and negative controls. D052 normally selects `orchestrator-conformance` or `mixed` where semantics are Orchestrator-owned.

### Markdown/text/policy

A normative text artifact MAY itself be the current specification carrier. Its delta can specify semantic, structural, reference, audience and preserved-meaning requirements. Verification may be inspection, deterministic static/reference checking and/or agent-facing evaluation.

### Configuration/schema

Specify desired state, compatibility, validation and runtime/failure effects; verify through static and applicable runtime evidence.

### Refactor

Use `PRESERVED` requirements/characterization as the primary semantic contract plus explicitly authorized structural changes. Do not invent fake feature behavior.

## 14. Coexistence with project-native SDD

D026/`governance-core/COEXISTENCE.md` remains controlling for provider overlap.

When an adequate project-native SDD capability exists, Agent Governance SHALL classify and use it through `REUSE`, `ADAPT`, `COEXIST`, `MISSING` or `CONFLICT` semantics rather than duplicate its artifacts.

The new default changes only the missing-provider case:

```text
adequate project-native SDD exists -> reuse/adapt it
no adequate SDD provider exists    -> Agent Governance native SDD applies
```

OpenSpec, Spec Kit, Kiro and similar systems remain compatibility/research examples, not hard-coded dependencies.

## 15. Source-product mapping

The existing source procedure is refined, not replaced:

```text
PD0 -> Explore / Frame + initial Specify/Design
PD1 -> persisted spec delta / Task Contract / conformance + Plan & Trace
PD2 -> execution readiness
PD3 -> Implement
PD4 -> Verify
PD5 -> Converge / review / persisted re-entry when required
PD6 -> Integrate & Evolve
```

## 16. Consumer lifecycle mapping

The existing Core lifecycle is refined, not replaced:

```text
F0/F1 -> Explore / Frame + Specify
F2    -> controlling Design
F3    -> Agent Governance capability/Skill audit
F4/F5/F6 -> Plan & Trace + readiness/persistence
execution -> Implement
assurance/review -> Verify & Converge
closure/archive -> Integrate & Evolve
```

## 17. No full historical backfill

D053 is prospective and delta-first.

Agent Governance SHALL NOT stop normal roadmap work to generate full historical specs for the entire existing repository. Current-spec coverage SHALL accumulate when capabilities are touched by real work.

Historical Task Contracts and accepted changes MUST NOT be rewritten solely to attach new SDD labels.

## 18. Relationship to D052

D052 remains fully controlling for conformance test authorship.

D053 adds specification and trace structure around that rule:

```text
Orchestrator requirement semantics
        -> applicable D052 conformance oracle
        -> Executor implementation + supplementary verification
        -> Executor evidence
        -> Orchestrator convergence/acceptance
```

Conformance remains subordinate to the specification and is never an independent authority source.

## 19. Implementation boundary

Acceptance of D053 would authorize a follow-up design/implementation program, not direct ad-hoc mutation.

Expected affected governance surfaces include, at minimum:

- `AGENTS.md` role/workflow representation;
- `governance-core/LIFECYCLE.md`;
- `governance-core/QUALITY.md`;
- `governance-core/COEXISTENCE.md`;
- source `docs/DEVELOPMENT-WORKFLOW.md`;
- `docs/TASK-CONTRACTS.md`;
- reusable consumer/source templates and any schemas required for native spec/change/trace materialization;
- deterministic/eval conformance needed to prove the new protocol and cross-artifact invariants;
- package/bootstrap behavior if new durable consumer spec state is materialized.

Those changes MUST be separately scoped under the normal contract-first process. D053 itself does not authorize the Executor to change runtime/Core/package artifacts.

## 20. Evidence and measurement

Agent Governance SHALL NOT claim that SDD inherently reduces defects merely because artifacts exist.

Adoption should measure practical outcomes where feasible, including:

- requirement-to-evidence completeness;
- review-detected spec/implementation drift;
- unauthorized scope/gold-plating findings;
- rework caused by requirement ambiguity;
- context load/RCAB impact;
- stale or duplicated specification findings;
- verification quality/non-regression coverage.

D039 learning-loop semantics may consume that evidence to refine the process later.

## Consequences if accepted

### Gains

- intent becomes durable and cross-agent rather than chat-local;
- brownfield work gains precise change deltas without full backfill;
- existing Task Contracts become part of a complete requirement-to-evidence chain;
- Skill/text/protocol work receives the same SDD discipline as code;
- refactors gain explicit preserved-behavior semantics;
- external SDD tools remain optional and reusable rather than required;
- post-implementation spec drift becomes a named acceptance failure.

### Costs / risks

- additional specification/trace work must be kept proportional;
- poor specs can still be wrong and create false confidence;
- duplicate current-truth artifacts are dangerous and must be avoided;
- spec evolution requires disciplined re-entry rather than silent implementation deviation;
- new consumer footprint/schema behavior may require migration/versioning design.

## Alternatives rejected

### Require OpenSpec directly

Rejected: useful research baseline, but external product/tool coupling is unnecessary and conflicts with Agent Governance portability and single-install philosophy.

### Adopt GitHub Spec Kit/Kiro workflow verbatim

Rejected: stronger ceremony/tool assumptions than needed and duplicates existing Governance lifecycle/artifacts.

### Make spec the sole source and regenerate code

Rejected as general default: nondeterminism and mixed normative/implementation product types make this too strong for Agent Governance.

### Keep SDD optional only

Rejected if D053 is accepted: the Human Owner's intended product is to provide SDD discipline even when no external provider exists.

### Full brownfield spec backfill

Rejected: high cost, likely stale, and contrary to the strongest OpenSpec brownfield lesson.

## Decision request

Human Owner approval is requested for the D053 architecture before Agent Governance changes its Core/source workflow or consumer footprint.
