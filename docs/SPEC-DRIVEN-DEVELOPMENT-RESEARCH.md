# Spec-Driven Development Research and Agent Governance Adaptation

Status: RESEARCH COMPLETE — architecture proposal pending Human Owner decision  
Date: 2026-08-23  
Primary research basis: OpenSpec  
Scope: Agent Governance source development and governed consumer projects

## Purpose

Research the current Spec-Driven Development (SDD) landscape and define the strongest tool-neutral adaptation for Agent Governance without installing or depending on OpenSpec, GitHub Spec Kit, Kiro, or another third-party SDD framework.

The Human Owner's target is broader than code generation. The intended method must apply to any governed development unit whose correctness can be specified and verified: application code, Agent Skills, governance/policy artifacts, configuration, schemas, tests/evals, and text/Markdown products.

This research focuses on the semantic method, not the commands or file layout of any one product.

## Executive conclusion

Agent Governance should adopt a **native, spec-anchored, delta-first, tool-neutral SDD model**.

The strongest parts of the current SDD ecosystem are not vendor commands. They are these recurring engineering properties:

1. persist intent before implementation;
2. distinguish **what must be true** from **how it will be built**;
3. represent a change as a small reviewable unit;
4. evolve existing systems through **spec deltas** rather than attempting a one-time complete specification of a brownfield codebase;
5. decompose approved intent into executable work;
6. maintain traceability from requirement to implementation and verification;
7. verify implementation against the specification rather than treating generated output as self-validating;
8. retain the specification/change history in Git so it survives chats, agents and tool changes;
9. allow explicit iteration/re-entry when implementation evidence invalidates an earlier assumption;
10. scale artifact ceremony to the size and risk of the change.

Agent Governance already implements a large part of this lifecycle through the Consumer F0-F6 governance flow, the source-product PD0-PD6 flow, Task Contracts, Decision Records, the quality envelope, persisted handoffs, D052 conformance ownership and remote review. The missing piece is to make **specification itself a first-class durable concern with change deltas, traceability and convergence**, instead of treating SDD only as an optional external/project-native provider.

## Important maturity correction

SDD has strong current traction, but it is not yet a single formal industry standard and there is no reliable evidence that one standard definition is used by a majority of programmers.

Thoughtworks placed **Spec-driven development** in `Assess` in its November 2025 Technology Radar and described it as an *emerging* approach whose definition is still evolving. Thoughtworks' April 2026 Radar also placed both OpenSpec and GitHub Spec Kit in `Assess`. Birgitta Böckeler similarly describes at least three materially different interpretations: `spec-first`, `spec-anchored`, and `spec-as-source`.

This distinction matters for Agent Governance: adoption should be based on the useful engineering invariants of SDD, not on an assumption that a final universal standard already exists.

## 1. OpenSpec — primary research basis

OpenSpec currently provides the most useful model for Agent Governance because it is intentionally lightweight, tool-agnostic and brownfield-first.

### 1.1 Current truth versus proposed change

OpenSpec separates two concepts:

```text
current specs     = what the system is agreed to do now
active change     = what is proposed to change
```

A change groups proposal, delta specification, design and tasks. After successful implementation, the delta is folded into the current specification and the change is archived.

The useful architectural property is not the `openspec/` directory. It is the separation of **steady-state truth** from **proposed delta** and the explicit transition between them.

### 1.2 Delta-first brownfield adoption

OpenSpec's strongest brownfield rule is explicit: do **not** document an existing codebase in full before SDD becomes useful. Specify only the slice that the next real change touches.

The standard delta vocabulary is:

- `ADDED`
- `MODIFIED`
- `REMOVED`

Over time, accepted changes accumulate into a more complete current specification organically.

For Agent Governance this is substantially better than retroactively generating full specifications for the existing Core, Skills, runtime and every future consumer repository. A full one-time backfill would create large speculative documentation with a high probability of becoming stale.

### 1.3 Specification versus design

OpenSpec distinguishes observable behavior from implementation approach:

- specification: behavior, inputs, outputs, requirements, error conditions;
- design: architecture and technical realization.

This maps directly to the existing Agent Governance separation between Orchestrator-owned intent/architecture/acceptance and Executor-owned implementation mechanics.

### 1.4 Requirements and scenarios

OpenSpec recommends clear mandatory requirements using `SHALL`/`MUST` and concrete Given/When/Then scenarios that exercise them.

The value is testability and shared interpretation, not the exact Markdown syntax.

### 1.5 Iteration, not waterfall

OpenSpec's newer OPSX model treats artifact dependencies as **enablers, not irreversible gates**. Proposal, specs, design and tasks can be revisited when new information appears.

Agent Governance should preserve its readiness gates but adopt the same realism: if implementation evidence invalidates a requirement assumption or material design boundary, the workflow explicitly re-enters the earliest affected specification/design stage. The correction must be persisted before execution continues; the Executor must not silently reinterpret the spec.

### 1.6 Verification and convergence

OpenSpec's verification workflow checks whether implementation matches the planned artifacts before archive. GitHub Spec Kit's newer `converge` operation expresses a similar idea: after implementation, detect remaining gaps between spec/plan/tasks and the code, then iterate until the work converges.

Agent Governance already has stronger independent acceptance authority than either tool: Executor verification is evidence, while Orchestrator review controls acceptance. SDD should strengthen that review by making **spec-to-implementation convergence** explicit.

### 1.7 Proportionality

OpenSpec explicitly recognizes that some tooling, refactor or docs-only changes do not need a behavioral spec delta, and that a one-line change may not justify full ceremony.

Agent Governance should interpret this as:

> every change traverses the SDD reasoning concerns; not every change needs a separate file for every concern.

That distinction is critical if SDD is to apply to all work without becoming a documentation tax.

## 2. GitHub Spec Kit — useful controls to adopt selectively

GitHub Spec Kit's core path is:

```text
constitution -> specify -> plan -> tasks -> implement
```

Current versions add optional quality operations such as clarification, checklist analysis, cross-artifact analysis and convergence.

Useful ideas for Agent Governance:

- durable project principles constrain every feature;
- `what/why` is separated from implementation planning;
- requirements, plan and tasks are cross-checked before implementation;
- large work is decomposed into smaller independently specified units;
- stable identifiers can anchor traceability;
- post-implementation convergence checks for omissions.

Agent Governance already has equivalents for the constitution layer (`AGENTS.md`, Governance Core, accepted Decision Records), task decomposition and review. It should not reproduce Spec Kit's generated file volume merely to resemble the tool.

Spec Kit also documents both **living-spec** and **flow-forward/history** models. Agent Governance should use a hybrid: current capability specifications are living; change deltas and reviews remain immutable/auditable historical records.

## 3. Kiro — requirements precision and bug/refactor preservation

Kiro's feature-spec workflow typically uses:

```text
requirements -> design -> tasks -> execution
```

It supports requirements-first and design-first variants and uses EARS-style requirements. Kiro's bug specification explicitly records:

- current defective behavior;
- expected behavior;
- behavior that must remain unchanged.

That last category is especially valuable for Agent Governance refactors, security fixes and zero-drift tasks. OpenSpec's three delta operators are therefore extended in the proposed Agent Governance model with a fourth semantic category:

- `PRESERVED` — a critical invariant that must remain true and must be proved by verification.

`PRESERVED` is not a new behavior. It is a first-class non-regression contract.

## 4. Requirements engineering — EARS and NASA lessons

Modern SDD benefits from established requirements-engineering practice rather than inventing requirement syntax from scratch.

### 4.1 EARS

EARS (Easy Approach to Requirements Syntax), originally published by Alistair Mavin and colleagues from Rolls-Royce work, was designed to reduce ambiguity in natural-language requirements through a small set of structured patterns.

Agent Governance does not need to enforce EARS mechanically, but should borrow the useful forms when they increase precision:

```text
The <system> SHALL <response>.
WHEN <trigger>, the <system> SHALL <response>.
WHILE <state>, the <system> SHALL <response>.
IF <undesired condition>, THEN the <system> SHALL <response>.
```

### 4.2 NASA requirement quality

NASA's Systems Engineering Handbook provides useful discipline independent of any AI tool:

- `shall` denotes a requirement;
- requirements should describe **what**, not unnecessarily prescribe **how**;
- one subject/predicate and atomicity improve reviewability;
- assumptions and constraints should be explicit;
- requirements should be complete and consistent;
- requirements should be uniquely referenceable;
- bidirectional traceability should connect higher-level intent, requirements, design, code and verification;
- the verification method should be considered when the requirement is written.

NASA recognizes verification by test, analysis, inspection and demonstration. Agent Governance should add `eval` as an explicit method for agent-facing/probabilistic behavior while retaining those deterministic methods.

## 5. Industry and research caution — SDD is not proof of quality

Thoughtworks' research is directionally supportive of structured specification, while also warning that SDD definitions are in flux and heavyweight workflows can become tedious or disproportionate for small work.

A 2026 empirical study presented for ESEM's Software Engineering in Practice track examined specification artifacts across 119 open-source repositories and did **not** find evidence that specification use or measured spec quality by itself reduced defects or rework after controlling for task/developer effects. Its interpretation is not the final word on SDD, but it is an important warning against treating SDD artifacts as a quality guarantee.

Agent Governance therefore must preserve this invariant:

```text
specification != proof
plan          != proof
passing one generated suite != acceptance
```

Quality comes from the combination of explicit intent, appropriate design, traceability, proportionate verification, independent review and controlled evolution. This is already aligned with D052: conformance tests are executable projections of approved semantics, not Governance authority.

## 6. Current Agent Governance coverage

Agent Governance is already structurally close to SDD.

### Consumer lifecycle

`governance-core/LIFECYCLE.md` currently provides:

```text
F0 Frame
F1 Viability / research
F2 Engineering Strategy + solution diagram
F3 Skill Capability Audit
F4 Atomic Work Planning
F5 Readiness Review
F6 Persist and Handoff
```

### Source-product lifecycle

`docs/DEVELOPMENT-WORKFLOW.md` currently provides:

```text
PD0 Frame / research
PD1 Persist contract / conformance authority
PD2 Executor checkout + verification plan
PD3 Implement
PD4 Verify + handoff + publish
PD5 Orchestrator review / rework
PD6 Integrate
```

### Existing supporting controls

- `docs/TASK-CONTRACTS.md` already persists objective, scope, exclusions, invariants, acceptance and verification before execution.
- `governance-core/QUALITY.md` already requires proportionate engineering quality and a Primary Solution Diagram when material.
- `governance-core/COEXISTENCE.md` already understands external/project-native SDD systems and prevents duplicate authority.
- D052 already makes conformance authorship follow semantic authority.
- Git and persisted handoffs already provide durable cross-agent/cross-chat continuity.

Therefore Agent Governance should **not add a second parallel lifecycle**. Native SDD should become a semantic overlay and artifact model mapped onto the existing F/PD lifecycle.

## 7. Gaps to close

Despite the strong overlap, five capabilities are not yet first-class:

1. **Current specification carrier** — there is no generic rule identifying the durable artifact that states accepted behavior for a capability.
2. **Explicit spec delta** — Task Contracts express change scope, but there is no standard ADDED/MODIFIED/REMOVED/PRESERVED requirement delta for every behavior-bearing change.
3. **Requirement traceability** — acceptance criteria are strong, but there is no uniform requirement -> design/task -> verification -> implemented-artifact trace model.
4. **Convergence gate** — PD5/F5-style checks exist, but post-implementation spec/implementation drift is not named as a dedicated SDD invariant.
5. **Native no-tool SDD** — current coexistence rules allow `no-SDD` as a valid state. The Human Owner now wants SDD to be an intrinsic Agent Governance development capability even when no external SDD provider is installed.

## 8. Proposed Agent Governance SDD model

### 8.1 Posture: spec-anchored, not spec-as-source

Agent Governance should use **spec-anchored SDD**:

- a durable specification remains available after implementation and evolves with the product;
- code/text/config remains a directly maintained product artifact, not disposable generated output;
- the specification is not allowed to override constitutional Governance or accepted Decision Records;
- discrepancies are blockers to reconcile, not an excuse to blindly regenerate code.

`spec-as-source` is rejected as the general default because Agent Governance contains security-sensitive protocol logic, normative Markdown, tests, packaging and manually reviewed implementation whose correctness cannot safely be delegated to nondeterministic regeneration from natural language alone.

### 8.2 Brownfield posture: delta-first

Do not backfill a complete specification of Agent Governance or every consumer repository.

For each future change:

1. identify the capability/artifact being changed;
2. identify its current specification carrier, if one already exists;
3. create only the delta needed for this change;
4. after acceptance, fold the accepted delta into the current spec carrier or designate the changed normative artifact itself as the updated carrier;
5. preserve the change/review evidence in Git.

Coverage grows from real work.

### 8.3 Logical SDD stages

Agent Governance should define seven logical SDD concerns:

| SDD concern | Question | Primary owner |
| --- | --- | --- |
| Explore / Frame | What problem/result and evidence are we dealing with? | Orchestrator |
| Specify | What SHALL be true, change, or remain unchanged? | Orchestrator |
| Design | What strategic architecture/quality boundaries govern the solution? | Orchestrator for controlling design; Executor for detailed implementation design |
| Plan & Trace | What atomic work proves each requirement and dependency? | Orchestrator |
| Implement | How is the approved change realized technically? | Executor |
| Verify & Converge | Does the delivered artifact satisfy every requirement without extra unintended behavior? | Executor executes/evidences; Orchestrator judges semantic convergence |
| Integrate & Evolve | Is the accepted delta folded into current truth and history preserved? | Orchestrator |

The Human Owner remains final authority for material scope, product/risk and release decisions.

These are **not seven new workflow gates**. They map onto the existing F0-F6 and PD0-PD6 processes.

### 8.4 Mapping to existing Consumer lifecycle

```text
Explore / Frame     -> F0 + F1
Specify             -> F0/F1 durable requirement definition, completed before readiness
Design              -> F2
Capability audit    -> F3 (Agent Governance-specific additional gate)
Plan & Trace        -> F4 + F5 + F6
Implement           -> existing Execution controls
Verify & Converge   -> Assurance + task DONE evidence + Strategy review/re-entry when required
Integrate & Evolve  -> accepted project state/spec update + archival/history controls
```

### 8.5 Mapping to source-product lifecycle

```text
Explore / Frame     -> PD0
Specify             -> PD0/PD1 + Decision/Task Contract/spec delta
Design              -> PD0/PD1 architecture + applicable conformance gate
Plan & Trace        -> PD1/PD2
Implement           -> PD3
Verify & Converge   -> PD4 + PD5
Integrate & Evolve  -> PD6 + accepted spec/change-history update
```

## 9. Artifact model: semantic completeness without file explosion

Every SDD concern is mandatory to consider. Separate artifacts are materialized only when they add durable value.

### 9.1 Current specification carrier

A capability's accepted specification can be carried by:

1. an existing project-native SDD/spec artifact;
2. a dedicated Agent-Governance-native capability spec;
3. an already normative product artifact whose contents *are* the behavior contract, such as an Agent Skill, Governance Core protocol Markdown, schema or policy artifact.

This prevents duplicate truth. A Skill does not need a second document that merely copies the entire Skill's semantics.

### 9.2 Change specification

A behavior-bearing change records the affected requirements with:

- `ADDED`
- `MODIFIED`
- `REMOVED`
- `PRESERVED`

`PRESERVED` identifies non-regression behavior that is material to acceptance, especially for bug fixes, refactors, security hardening and migrations.

### 9.3 Design carrier

Material architecture/design constraints may live in an existing Decision Record, architecture document, Task Contract design section or dedicated design artifact. Detailed file/class/algorithm choices remain with the Executor unless strategically controlling.

### 9.4 Plan carrier

Existing Governance Task Contracts, task records and WORKPLAN remain the normal execution-planning layer. SDD should strengthen them with requirement references rather than create a redundant parallel task system.

### 9.5 Trace carrier

For ordinary changes, requirement-to-task-to-verification mapping can be embedded in the Task Contract/handoff/review. A separate traceability matrix is required only when complexity, safety, compliance or cross-task scope makes it materially useful.

## 10. Proportional SDD profiles

A universal method needs proportional artifact depth.

### COMPACT

Use for small, low-risk, local changes or products whose normative artifact itself is the specification.

All seven SDD concerns still apply, but proposal/spec/design/trace may collapse into the existing Decision/Task Contract/change review. No fake extra files are created merely to satisfy ceremony.

### STANDARD

Use for ordinary features, bugs, Skill behavior changes, compatibility changes and non-trivial documentation/protocol work.

Require explicit requirement delta, material design, task/verification trace and convergence evidence.

### ASSURED

Use for security-sensitive, protocol/public-compatibility, high-risk, multi-component or compliance-sensitive work.

Require stronger explicit specification/trace artifacts, security/quality design where applicable, D052 conformance ownership when semantic authority warrants it, and stronger independent verification.

Profile selection controls artifact/evidence depth, **not whether SDD applies**.

## 11. Requirement style

A durable normative requirement should, where practical:

- have a stable identifier when it needs independent traceability;
- state one material obligation;
- use `SHALL` for mandatory behavior;
- distinguish goals/recommendations from requirements;
- avoid unnecessary implementation prescription;
- state relevant precondition/trigger/error state explicitly;
- include concrete Given/When/Then examples when examples materially reduce ambiguity;
- identify a verification method: `test`, `inspection`, `analysis`, `demonstration`, `eval`, or a justified combination.

Scenarios are not mandatory decoration. They are required when they clarify observable behavior or boundary conditions.

## 12. Bidirectional traceability and anti-gold-plating

For material requirements, the normal trace becomes:

```text
Human/mission intent
      -> requirement / spec delta
      -> controlling design constraint
      -> Task Contract / work item
      -> implementation artifact
      -> verification evidence
      -> Orchestrator acceptance
```

Review should work in both directions:

- every approved requirement has implementation/evidence;
- every material implementation behavior/change has an authorized requirement/scope parent.

Untraceable extra behavior is potential scope drift or gold-plating and must be reviewed rather than silently accepted.

## 13. Convergence and specification drift

Before acceptance, the change must be checked for:

- **completeness** — every required behavior/change is implemented and evidenced;
- **correctness** — the evidence actually proves the intended requirement;
- **coherence** — spec, design, tasks, implementation and verification do not contradict;
- **containment** — no material unauthorized behavior/scope is introduced;
- **persistence** — accepted current spec carrier and historical change evidence will agree after integration.

If implementation discovery changes the intended behavior, the Executor must not silently edit normative requirements or an Orchestrator-owned oracle. It reports the gap/conflict; Orchestrator re-enters the earliest affected SDD stage, persists the revision, and only then resumes execution.

## 14. Applying SDD beyond application code

### Code

Specify observable API/state/error/performance/security behavior; design the architecture; implement; verify with appropriate automated/deterministic/integration/property evidence.

### Agent Skill

Specify activation boundaries, inputs, outputs, authority, required context, failure behavior, side effects/permissions, security constraints and negative controls. D052 normally makes semantic conformance `orchestrator-conformance` or `mixed`.

### Markdown/text/policy

The text artifact may itself be the current specification carrier. The change delta defines semantic/structural/reference requirements and preserved meaning; verification may use inspection, deterministic reference checks and/or agent-facing evals. SDD does not require executable application code.

### Configuration/schema

Specify desired state, compatibility and failure behavior; verify statically and, when material, by runtime/integration demonstration.

### Refactor

The primary specification is often a `PRESERVED` behavior set plus explicitly allowed structural changes. Characterization/conformance proves zero drift. No fictional new user feature is needed.

## 15. Coexistence with external/project-native SDD

The Human Owner is not adopting OpenSpec, Spec Kit or Kiro as a product dependency.

Native Agent Governance SDD becomes the fallback methodology when no adequate project-native SDD provider exists. When a repository already has an SDD/spec system:

- classify it under existing `REUSE / ADAPT / COEXIST / CONFLICT` rules;
- map its artifacts to Agent Governance SDD concerns;
- reference rather than duplicate adequate current specs/design/tasks;
- add only missing Governance authority, trace, acceptance or assurance metadata;
- stop on conflicting write/authority ownership.

Therefore Agent Governance can guarantee SDD coverage without forcing one tool or one file layout on every project.

## 16. Brownfield rollout for Agent Governance itself

Do **not** pause the roadmap to retro-specify the whole repository.

Adoption should be prospective and incremental:

1. accept the native SDD architecture;
2. update Governance/Core/source workflow semantics and reusable templates/contracts;
3. add any required deterministic conformance for the new protocol;
4. on each subsequent real change, create/update only the specs for the capability touched;
5. let canonical spec coverage accumulate through accepted work;
6. measure whether the new artifacts improve traceability/review/context rather than assuming success from artifact count.

The existing T021/T022 work should not be silently rewritten merely to retrofit labels unless the Human Owner explicitly decides to re-contract them.

## 17. Recommended architecture decision

The research supports D053 with these core decisions:

- native SDD is part of Agent Governance, not an external required tool;
- posture is `spec-anchored`, not general `spec-as-source`;
- adoption is brownfield `delta-first`;
- SDD is mandatory as logical coverage but proportional in artifact materialization;
- current-spec carrier and proposed-change delta are distinct;
- delta vocabulary is `ADDED / MODIFIED / REMOVED / PRESERVED`;
- requirements are testable/traceable and verification method is decided with the requirement;
- Orchestrator owns intent, normative specification, controlling design, task/trace semantics and acceptance;
- Executor owns detailed technical design, implementation, supplementary technical verification and evidence;
- semantic conformance continues to follow D052;
- post-implementation convergence is explicit;
- accepted deltas fold into current truth while historical change evidence remains in Git;
- existing SDD providers are reused/adapted rather than duplicated;
- full brownfield spec backfill is rejected.

## Sources

Primary:

- OpenSpec, Core Concepts: https://openspec.dev/docs/overview
- OpenSpec, OPSX Workflow: https://openspec.dev/docs/opsx
- OpenSpec, Existing Projects: https://openspec.dev/docs/existing-projects
- OpenSpec, Writing Good Specs: https://openspec.dev/docs/writing-specs
- OpenSpec, Reviewing a Change: https://openspec.dev/docs/reviewing-changes
- OpenSpec, Team Workflow: https://openspec.dev/docs/team-workflow

Comparative SDD:

- GitHub Spec Kit documentation: https://github.github.com/spec-kit/
- GitHub Spec Kit Agentic SDD reference: https://github.com/github/spec-kit/blob/main/docs/reference/agentic-sdd.md
- GitHub Spec Kit evolving specs: https://github.com/github/spec-kit/blob/main/docs/guides/evolving-specs.md
- Kiro Feature Specs: https://kiro.dev/docs/specs/feature-specs/
- Kiro Analyze Requirements: https://kiro.dev/docs/specs/analyze-requirements/

Requirements/verification:

- Mavin et al., Easy Approach to Requirements Syntax (EARS), IEEE RE 2009, DOI 10.1109/RE.2009.9
- NASA Systems Engineering Handbook, Appendix C/D: https://www.nasa.gov/reference/system-engineering-handbook-appendix/
- NASA Requirements Management: https://www.nasa.gov/reference/6-2-requirements-management/
- NASA Product Verification: https://www.nasa.gov/reference/5-3-product-verification/

Industry/research posture:

- Birgitta Böckeler, Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl: https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
- Thoughtworks Technology Radar, Spec-driven development, Nov 2025
- Thoughtworks Technology Radar, OpenSpec, Apr 2026: https://www.thoughtworks.com/en-us/radar/tools/openspec
- Thoughtworks, Spec-driven development: Unpacking one of 2025's key new AI-assisted engineering practices
- Brenn Hill, Does Spec-Driven Development Reduce Defects? ESEM SEIP 2026 / SSRN 6515898

## Research disposition

Research is complete enough to select the architecture. The next step is Human Owner review of D053. No external SDD tool installation and no executable/core protocol mutation is authorized by this research record alone.
