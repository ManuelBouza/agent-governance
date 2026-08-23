# D053 — Native spec-anchored delta-first development

Status: ACCEPTED  
Date: 2026-08-23  
Accepted by: Human Owner  
Research basis: `docs/SPEC-DRIVEN-DEVELOPMENT-RESEARCH.md`

## Problem

Agent Governance already performs substantial preimplementation framing, research, architecture, task contracting, readiness, verification and review, but specification is not yet a first-class durable development primitive across source maintenance and governed consumer projects.

Current Core coexistence semantics treat project-native SDD as an optional external capability and permit a no-SDD mode. The Human Owner requires every governed development unit — code, Agent Skill, policy/text artifact, configuration, schema or comparable deliverable — to receive SDD discipline without requiring a third-party SDD product.

The ecosystem does not provide one settled formal SDD standard. OpenSpec, GitHub Spec Kit, Kiro and other current systems differ materially in artifact layout, lifecycle and source-of-truth posture. Copying one tool wholesale would conflict with Agent Governance's executor neutrality, coexistence model and existing F/PD lifecycles.

The first D053 draft distributed responsibility inside individual SDD stages, for example giving Design partly to the Orchestrator and partly to the Executor, and Verify & Converge partly to each. The Human Owner rejected that model. Native Agent Governance SDD has **one accountable owner per stage**. The Executor is not a co-owner of specification, design, planning or semantic convergence; its SDD responsibility is limited to technical implementation and technical review/verification of that implementation.

## Decision

Agent Governance SHALL adopt a **native, tool-neutral, spec-anchored, delta-first SDD capability** for both:

- maintenance/development of the Agent Governance source product; and
- governed consumer-project development when no adequate project-native SDD provider is already primary.

No OpenSpec, Spec Kit, Kiro or other external SDD framework becomes a required product dependency.

Native SDD SHALL use an **exclusive stage ownership** model:

```text
Orchestrator: Explore -> Specify -> Design -> Plan & Trace
Executor:     Implement -> Code Review & Verify
Orchestrator: Converge -> Accept -> Integrate & Evolve
```

No SDD stage has dual Orchestrator/Executor ownership.

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
        + implementation/review
        -> accepted updated capability/artifact
```

Only the slice affected by current work is required to become newly specified unless a broader specification is independently justified.

## 3. Single-owner SDD stages

All governed development SHALL address the applicable SDD stages below. Every stage has exactly one accountable role.

| Stage | Single accountable owner | Required result |
| --- | --- | --- |
| `1. Explore / Frame` | ChatGPT Orchestrator | Problem, intent, constraints, evidence, research needs and scope boundary are understood. |
| `2. Specify` | ChatGPT Orchestrator | Durable normative requirements/spec delta state what SHALL change, remain true or be removed. |
| `3. Design` | ChatGPT Orchestrator | The complete controlling solution design, architecture, quality/security/compatibility boundaries and implementation-relevant decisions are defined. |
| `4. Plan & Trace` | ChatGPT Orchestrator | Atomic work, dependencies, acceptance, requirement trace and verification obligations are persisted and implementation-ready. |
| `5. Implement` | Agente de IA Ejecutor | Authorized technical implementation/code is created strictly from the approved specification/design/plan. |
| `6. Code Review & Verify` | Agente de IA Ejecutor | The implementation is technically reviewed against the approved specification/design/plan, required tests/evals/checks are executed, defects within implementation authority are corrected, and evidence is persisted. |
| `7. Converge, Accept & Evolve` | ChatGPT Orchestrator | Specification/design/plan, implementation, review evidence and resulting current-spec state are compared; the change is accepted/reworked/rejected, integrated when accepted, and the living specification/history is evolved. |

The Human Owner remains final authority for material scope, product/risk, release and override decisions.

### 3.1 No dual-stage ownership

A stage SHALL NOT be represented as:

```text
Orchestrator does strategic half
Executor does technical half
```

Instead, the upstream Orchestrator stage must be complete enough to hand off a coherent execution contract. Local coding choices made by the Executor during implementation are implementation decisions, not a second Design authority.

If an Executor-side choice would materially alter approved requirements, architecture, quality/security boundaries, compatibility, acceptance or task decomposition, the Executor SHALL stop the affected work and return the issue to the Orchestrator for re-entry into the appropriate earlier stage.

### 3.2 Executor participation boundary

Within native SDD, the Executor participates only in:

1. technical implementation/code creation; and
2. technical code review/verification of that implementation.

The Executor does not own Explore, Specify, Design, Plan & Trace, semantic convergence, acceptance, current-spec evolution or integration policy.

Executor-native private plans, internal reasoning, sub-agents, coding tools or review tools may be used inside stages 5-6, but they are implementation aids only and do not become competing SDD authority.

### 3.3 Non-code and Orchestrator-owned artifact work

SDD applies even when a change contains no Executor-owned code.

For a Markdown/text/policy/Skill change whose implementation artifact is Orchestrator-owned under repository/project policy, the Orchestrator may materialize that artifact without introducing an Executor merely to satisfy a process diagram. Stages 5-6 are then satisfied through the artifact owner's implementation plus proportionate inspection/eval/conformance under the applicable ownership rules.

The invariant is not "an Executor must touch every change". The invariant is:

> no stage has shared authority, and an Executor is used only for implementation/code and technical review within its artifact ownership boundary.

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

For each touched capability, the Orchestrator SHALL identify the accepted **current specification carrier** when one exists.

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
        -> Orchestrator design
        -> Orchestrator Task Contract / plan
        -> Executor implementation
        -> Executor code review / verification evidence
        -> Orchestrator convergence / acceptance
        -> current-spec evolution / integration
```

A separate traceability matrix is required only when complexity/risk makes it materially useful. For ordinary work the mapping MAY be represented inside Task Contracts, handoffs and reviews.

Material implementation with no authorized requirement/scope parent is potential gold-plating/scope drift and MUST be reviewed before acceptance.

## 9. Role ownership under native SDD

The binary role model remains unchanged, but D053 defines a stricter SDD stage boundary.

### Human Owner

Owns final material product, scope, risk, release and override decisions.

### ChatGPT Orchestrator

Exclusively owns native SDD stages 1-4 and 7:

- Explore/Frame synthesis and external research conclusions;
- normative requirement/specification semantics and spec deltas;
- complete controlling design and architecture;
- quality/security/privacy/reliability/compatibility design constraints;
- task decomposition, readiness and trace semantics;
- D052-designated conformance/oracle semantics;
- semantic convergence review and acceptance decision;
- accepted current-spec evolution and integration/archival records.

### Agente de IA Ejecutor

Exclusively owns native SDD stages 5-6 when Executor-owned technical implementation exists:

- authorized technical implementation/code;
- implementation-focused and exploratory test code within ownership rules;
- technical code review against the approved specification/design/plan;
- execution of all required tests/evals/checks, including Orchestrator-owned conformance;
- correction of implementation defects that do not alter approved semantics/design;
- measurements, diagnostics, verification evidence and executor handoffs.

The Executor MAY report that the specification/design/plan is defective, ambiguous or technically impossible. It MUST NOT repair that defect by silently assuming ownership of an earlier SDD stage.

## 10. Design ownership refinement

Native SDD Design is an Orchestrator responsibility.

The Design stage SHALL define enough implementation-relevant architecture and constraints that the Executor does not need to invent missing design authority. This includes material component boundaries, interfaces, state/data flow, security/trust boundaries, compatibility/migration strategy, failure model and other controlling technical decisions when applicable.

This does **not** require the Orchestrator to prescribe every function name, local variable, loop, library call or equivalent coding detail. Such local choices remain part of implementation as long as they do not materially change the approved design.

```text
Orchestrator Design = controlling solution structure and constraints
Executor Implement  = local realization inside that complete design
```

The distinction prevents dual ownership without turning Design into line-by-line coding instructions.

## 11. Code Review & Verify stage

Stage 6 is owned by the Executor and is distinct from Orchestrator acceptance.

The Executor SHALL review the submitted implementation for at least:

- fidelity to the current spec delta and preserved requirements;
- fidelity to the approved design and task boundaries;
- correctness, edge cases and failure behavior;
- maintainability and unnecessary complexity;
- relevant security/privacy/reliability/compatibility concerns already represented by the design/contract;
- required deterministic/property/integration/eval/conformance evidence;
- unauthorized scope additions visible in implementation.

The Executor MAY correct code/test/technical implementation defects found by this review when the correction stays inside the approved specification/design/plan.

If review reveals a specification, design or plan defect, stage 6 reports it as a blocker/re-entry trigger rather than redesigning the work.

Executor `DONE` after stage 6 remains evidence only; it is not product acceptance.

## 12. Converge, Accept & Evolve stage

Stage 7 is owned by the Orchestrator.

Before acceptance, the Orchestrator SHALL establish:

- `completeness` — every required behavior/change has implementation and evidence;
- `correctness` — the submitted review/verification evidence actually proves the specified outcome;
- `coherence` — specification, design, plan, implementation and evidence do not materially contradict;
- `containment` — no material unauthorized behavior/scope was added;
- `persistence` — after integration the accepted current spec carrier and product state agree.

The Orchestrator does not perform a second implementation/code-authoring stage. It reviews the remote implementation/evidence at the semantic and governance boundary, requests rework when necessary, accepts only when convergence is established, and then evolves the current specification state and integration history.

## 13. Iteration and re-entry

SDD is not a one-way waterfall.

If stage 5 or 6 discovers evidence that changes a material requirement, design constraint, acceptance meaning or plan boundary, work SHALL re-enter the earliest affected Orchestrator-owned stage.

```text
Executor discovers upstream defect/conflict
        -> persist/report evidence
        -> STOP affected implementation/review
        -> Orchestrator re-enters Specify, Design or Plan
        -> Orchestrator persists revised authority
        -> Executor resumes Implement / Code Review & Verify
```

A material semantic or design change discovered during implementation MUST NOT be hidden as a coding detail.

## 14. Integrate & Evolve semantics

After acceptance:

- an accepted delta SHALL be folded into the current specification carrier when a dedicated living spec exists;
- when the changed normative product artifact itself is the specification carrier, that accepted artifact becomes the new current specification state without duplicating its contents elsewhere;
- the change delta, Decision/Task Contract, verification/handoff and review history SHALL remain auditable in Git according to applicable retention/archive policy.

The project therefore combines a living current specification with durable flow-forward change history.

## 15. Artifact-type applicability

SDD applies independent of file type, but Executor participation remains bounded by artifact ownership.

### Application/source code

The Orchestrator specifies and designs externally/materially observable state/API/error/performance/security behavior and the controlling solution structure. The Executor implements and performs code review/verification. The Orchestrator then performs convergence/acceptance and spec evolution.

### Agent Skills

The Orchestrator specifies activation, inputs, outputs, authority, required context, failure behavior, side effects/permissions, security boundaries and negative controls, and owns committed Markdown Skill content where repository/project ownership says so. Executor participation is limited to any separately authorized technical code/helpers/tests and their technical review. D052 normally selects `orchestrator-conformance` or `mixed` where semantics are Orchestrator-owned.

### Markdown/text/policy

A normative text artifact MAY itself be the current specification carrier. Its delta can specify semantic, structural, reference, audience and preserved-meaning requirements. Where the Orchestrator owns the artifact, it also materializes the text change; no Executor is introduced solely for SDD ceremony. Verification may be inspection, deterministic static/reference checking and/or agent-facing evaluation under applicable ownership rules.

### Configuration/schema

The Orchestrator specifies desired state, compatibility, validation, failure/runtime effects and controlling design. Authorized Executor-owned technical configuration/schema implementation is performed and technically reviewed in stages 5-6; semantic acceptance remains stage 7.

### Refactor

The Orchestrator defines `PRESERVED` requirements/characterization and the authorized structural design. The Executor performs the code refactor and code review/verification without changing the preserved semantics.

## 16. Coexistence with project-native SDD

D026/`governance-core/COEXISTENCE.md` remains controlling for provider overlap.

When an adequate project-native SDD capability exists, Agent Governance SHALL classify and use it through `REUSE`, `ADAPT`, `COEXIST`, `MISSING` or `CONFLICT` semantics rather than duplicate its artifacts.

Any reused/adapted SDD system must still map to a **single accountable owner per Agent Governance stage**. A tool workflow cannot create dual authority between Orchestrator and Executor merely because the tool permits both to edit the same artifact class.

The missing-provider case becomes:

```text
adequate project-native SDD exists -> reuse/adapt under single-owner mapping
no adequate SDD provider exists    -> Agent Governance native SDD applies
```

OpenSpec, Spec Kit, Kiro and similar systems remain compatibility/research examples, not hard-coded dependencies.

## 17. Source-product mapping

The existing source procedure is refined, not replaced:

```text
PD0 -> Orchestrator Explore / Frame + Specify + initial Design
PD1 -> Orchestrator persisted spec/design/Task Contract/conformance + Plan & Trace
PD2 -> Orchestrator readiness handoff; Executor establishes execution baseline only
PD3 -> Executor Implement
PD4 -> Executor Code Review & Verify + handoff/publish evidence
PD5 -> Orchestrator Converge / Accept / re-entry decision
PD6 -> Orchestrator Integrate & Evolve
```

PD2 does not transfer SDD planning/design authority to the Executor. Checkout/bootstrap mechanics remain an execution prerequisite rather than a new planning stage.

## 18. Consumer lifecycle mapping

The existing Core lifecycle is refined, not replaced:

```text
F0/F1       -> Orchestrator Explore / Frame + Specify
F2          -> Orchestrator Design
F3          -> Orchestrator capability/Skill audit
F4/F5/F6    -> Orchestrator Plan & Trace + readiness/persistence
execution   -> Executor Implement when technical implementation is delegated
review      -> Executor Code Review & Verify
acceptance  -> Orchestrator Converge / Accept / Integrate & Evolve
```

For Orchestrator-owned non-code work, the Executor implementation/review stages are not artificially inserted.

## 19. No full historical backfill

D053 is prospective and delta-first.

Agent Governance SHALL NOT stop normal roadmap work to generate full historical specs for the entire existing repository. Current-spec coverage SHALL accumulate when capabilities are touched by real work.

Historical Task Contracts and accepted changes MUST NOT be rewritten solely to attach new SDD labels.

## 20. Relationship to D041 and D052

### D041 executor process autonomy

D041 remains valid inside the Executor's assigned stages, but D053 refines the authority boundary for native SDD.

The Executor may choose internal coding/review tools, sub-agents, private plans and local implementation tactics inside stages 5-6. It may not use those mechanisms to create a competing authoritative specification, design, task plan or acceptance model.

### D052 conformance authorship

D052 remains fully controlling for conformance test authorship.

D053 adds the single-owner stage structure around that rule:

```text
Orchestrator Specify / Design / Plan
        -> applicable Orchestrator-owned D052 oracle
        -> Executor Implement
        -> Executor Code Review & Verify, including oracle execution
        -> Orchestrator Converge / Accept / Evolve
```

Conformance remains subordinate to the specification and is never an independent authority source.

## 21. Implementation boundary

Acceptance of D053 authorizes a follow-up design/implementation program, not direct ad-hoc mutation.

Expected affected governance surfaces include, at minimum:

- `AGENTS.md` role/workflow representation;
- `governance-core/LIFECYCLE.md`;
- `governance-core/QUALITY.md`;
- `governance-core/COEXISTENCE.md`;
- source `docs/DEVELOPMENT-WORKFLOW.md`;
- `docs/TASK-CONTRACTS.md`;
- D041-aligned Executor autonomy wording where needed to prevent SDD authority ambiguity;
- reusable consumer/source templates and any schemas required for native spec/change/trace materialization;
- deterministic/eval conformance needed to prove the new protocol and cross-artifact invariants;
- package/bootstrap behavior if new durable consumer spec state is materialized.

Those changes MUST be separately scoped under the normal contract-first process. D053 itself does not authorize the Executor to change runtime/Core/package artifacts.

## 22. Evidence and measurement

Agent Governance SHALL NOT claim that SDD inherently reduces defects merely because artifacts exist.

Adoption should measure practical outcomes where feasible, including:

- requirement-to-evidence completeness;
- review-detected spec/implementation drift;
- unauthorized scope/gold-plating findings;
- rework caused by requirement/design ambiguity;
- defects found during Executor code review before Orchestrator acceptance;
- context load/RCAB impact;
- stale or duplicated specification findings;
- verification quality/non-regression coverage.

D039 learning-loop semantics may consume that evidence to refine the process later.

## Consequences

### Gains

- each SDD stage has one accountable owner;
- the Orchestrator owns the entire upstream engineering contract before coding begins;
- the Executor's role is sharply bounded to technical implementation and technical code review/verification;
- intent becomes durable and cross-agent rather than chat-local;
- brownfield work gains precise change deltas without full backfill;
- existing Task Contracts become part of a complete requirement-to-evidence chain;
- Skill/text/protocol work receives the same SDD discipline without forcing an Executor into Orchestrator-owned artifacts;
- refactors gain explicit preserved-behavior semantics;
- external SDD tools remain optional and reusable rather than required;
- post-implementation spec drift becomes a named acceptance failure.

### Costs / risks

- the Orchestrator must produce sufficiently complete Design and Plan stages before code handoff;
- weak upstream design can block or misdirect implementation, so re-entry must remain explicit and cheap;
- additional specification/trace work must be kept proportional;
- poor specs can still be wrong and create false confidence;
- duplicate current-truth artifacts are dangerous and must be avoided;
- spec evolution requires disciplined re-entry rather than silent implementation deviation;
- new consumer footprint/schema behavior may require migration/versioning design.

## Alternatives rejected

### Dual Orchestrator/Executor responsibility inside an SDD stage

Rejected by Human Owner direction. It blurs accountability and allows the execution agent to become a co-author of specification/design/acceptance semantics that should already be complete before implementation.

### Require OpenSpec directly

Rejected: useful research baseline, but external product/tool coupling is unnecessary and conflicts with Agent Governance portability and single-install philosophy.

### Adopt GitHub Spec Kit/Kiro workflow verbatim

Rejected: stronger ceremony/tool assumptions than needed and duplicates existing Governance lifecycle/artifacts.

### Make spec the sole source and regenerate code

Rejected as general default: nondeterminism and mixed normative/implementation product types make this too strong for Agent Governance.

### Keep SDD optional only

Rejected: native SDD is now an accepted Agent Governance capability when no adequate project-native provider is primary.

### Full brownfield spec backfill

Rejected: high cost, likely stale, and contrary to the strongest OpenSpec brownfield lesson.

## Acceptance

The Human Owner approved the revised D053 architecture on 2026-08-23.

The accepted architecture is therefore controlling for subsequent SDD adoption work. Implementation remains subject to the normal branch, Task Contract, D052 conformance, review and integration gates; acceptance of D053 does not itself authorize an Executor to mutate Core/runtime/package artifacts.
