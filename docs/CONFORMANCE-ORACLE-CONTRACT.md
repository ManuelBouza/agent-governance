# Conformance Oracle Contract

Status: DESIGN-APPROVED  
Controlling decision: `docs/decisions/D052-specification-owned-conformance-test-authorship.md`

## Purpose

Define the reusable authoring contract for **Orchestrator-owned conformance/oracle assets** under D052.

The contract answers four questions without requiring each Skill/governance task to reconstruct the whole testing policy:

1. what semantic material belongs to the Orchestrator-owned oracle;
2. what remains Executor-owned harness/implementation verification;
3. how oracle identity, freeze, revision and defect handling work;
4. how Task Contracts point to the oracle with minimal context.

This document does **not** create test authority above Governance. It operationalizes the D052 rule:

> Test authorship follows semantic authority.

## Authority hierarchy

A conformance oracle is an executable/data projection of approved semantics.

Authority remains:

```text
Human / accepted Governance authority
    -> governance-core/ where applicable
    -> accepted Decision / functional contract / Task Contract
    -> Orchestrator-owned conformance oracle
    -> Executor harness/execution/result evidence
```

If an oracle contradicts its controlling specification, the specification wins and the oracle must be corrected through persisted Orchestrator authority.

Green oracle execution is evidence, not acceptance authority.

## Applicability

Use this contract when a Task Contract selects:

- `Test-Authorship-Mode: orchestrator-conformance`; or
- `Test-Authorship-Mode: mixed` for the Orchestrator-owned semantic surface.

Typical source-product uses include:

- Agent Skill behavior/activation;
- Governance/policy protocol behavior;
- documentation-managed workflows;
- routing/classification semantics;
- security/permission acceptance expectations;
- frozen characterization baselines whose meaning is owned by the Orchestrator.

Ordinary consumer/application implementation remains `executor-implementation` by default and does not require an Orchestrator-authored oracle unless its Task Contract explicitly says otherwise.

## Oracle != harness

The distinction is semantic, not based only on file extension or directory.

### Oracle

Material whose contents define **what result counts as correct**.

Examples:

- required input/case membership;
- expected output/classification/decision;
- deterministic acceptance assertion meaning;
- semantic negative controls;
- accepted threshold or non-regression rule;
- golden fixture contents when those contents are part of the accepted contract;
- accepted security/adversarial expectations;
- frozen characterization behavior;
- deterministic grader logic when the grader itself directly encodes approved expected semantics.

### Harness

Material whose primary purpose is to **execute, transport, isolate, collect or aggregate** the oracle.

Examples:

- pytest/eval runner mechanics;
- environment/session setup;
- provider/host adapters;
- subprocess/tool invocation plumbing;
- trace collection;
- metrics aggregation implementation;
- benchmark/timing plumbing;
- temporary fixture generation mechanics;
- debugging helpers.

Harness work remains Executor-owned unless a separate accepted ownership rule says otherwise.

## Semantic ownership test

When ownership is unclear, ask:

```text
If this value/code changed while implementation stayed identical,
could the accepted meaning of PASS/FAIL change?
```

If **yes**, it is presumptively oracle semantics and requires Orchestrator ownership/authorization.

If **no**, and the change only affects execution mechanics, it is presumptively harness/technical implementation.

This test is a routing heuristic, not a substitute for the controlling Task Contract when that contract explicitly assigns ownership.

## Oracle identity

Every material conformance oracle SHOULD have a stable identity recorded by its Task Contract or prerequisite gate.

Recommended identity fields are:

- `Oracle-ID` — stable scope/task identifier;
- `Oracle-Revision` — explicit revision label or canonical Git commit identity;
- `Controlling-Authority` — Decision/contract/Core/capability references;
- `Test-Authorship-Mode`;
- `Oracle-Assets` — exact committed paths;
- `Semantic-Scope` — concise statement of what acceptance meaning is encoded;
- `Freeze-State` — `DRAFT | FROZEN | SUPERSEDED | RETIRED`;
- `Executor-Mechanical-Corrections` — `none` or explicitly authorized bounded classes.

These fields may live directly in the Task Contract/gate rather than in a separate manifest when a separate manifest would add no value.

Do not create metadata for its own sake.

## Freeze states

### `DRAFT`

The oracle is still being authored/reviewed and is not eligible to constrain implementation execution.

### `FROZEN`

The oracle is integrated into canonical `develop`, its semantic meaning is approved for the task, and the Executor may execute against it.

A task using pre-authored conformance MUST NOT begin before the required oracle is `FROZEN` and reachable from the Executor's current canonical base.

### `SUPERSEDED`

A later persisted Orchestrator revision replaces the oracle for future execution.

The superseding authority must say whether prior results remain usable, require partial rerun, or are invalidated.

### `RETIRED`

The oracle no longer participates in current acceptance but remains auditable historical evidence.

Retirement must not erase the original accepted request/result history.

## Oracle asset classes

A task may use only the classes it actually needs.

### 1. Case corpus

Structured or code-defined cases whose membership is semantically material.

Possible classes include:

- positive;
- negative;
- near-miss;
- cross-profile;
- ambiguous;
- multi-intent;
- security/adversarial;
- compatibility/coexistence;
- migration/rollback;
- characterization/regression.

Not every task needs every class.

### 2. Expected outcomes

Expected decisions/classifications/state/output properties for required cases.

Expected outcomes should be explicit enough that the Executor does not need to infer semantic acceptance from broad documentation.

### 3. Deterministic acceptance assertions

Machine-decidable invariants selected by the Orchestrator because they directly encode acceptance meaning.

Prefer deterministic assertions over model judgment when the property is mechanically decidable.

### 4. Semantic negative controls

Purposeful mutations/input variants chosen to prove that a verifier rejects or distinguishes materially incorrect states.

Negative controls MUST target the **semantic boundary promised by the criterion**, not merely one convenient corruption mechanism.

Where a criterion covers several materially distinct dimensions, the oracle SHOULD identify representative controls for each relevant dimension.

This requirement incorporates the T020/T032 lesson that a green suite or one negative test does not prove the entire criterion boundary.

### 5. Thresholds / decision rules

Numeric or qualitative victory/non-regression rules that affect acceptance.

Thresholds must be frozen before observed comparative results when post-hoc tuning would bias the decision.

A threshold is never weakened merely because the current implementation fails it.

### 6. Golden fixtures

Fixture contents whose exact semantic state is part of the accepted contract.

Execution-only fixture setup remains harness work.

### 7. Grader expectations

Expected grader behavior/criteria when a grader is required.

Mechanical properties should use deterministic graders. Model-based graders are reserved for genuinely semantic properties that cannot be safely reduced to code.

### 8. Characterization baseline

Observed behavior explicitly accepted/frozen as the baseline for behavior-preserving refactoring.

Characterization captures what must not drift; it does not automatically bless unrelated defects or expand future product semantics.

## Capability-source integration

For Agent Governance Skill/governance work, `docs/CAPABILITY-SOURCE-CONTRACT.md` is the preferred topology-neutral source for capability-level routing semantics.

A conformance oracle MAY reference stable capability IDs such as:

```text
consumer.lifecycle
consumer.skill-trust
source.maintenance
```

This allows cases to bind to intent/profile/risk/context boundaries without copying the full functional contracts into the oracle.

Capability IDs do not replace controlling normative references.

## Minimal-context oracle rule

A D052 task should let the Executor start from:

```text
AGENTS.md / repository bootstrap
    -> exact Task Contract
    -> exact frozen oracle assets
    -> implementation surface
```

rather than requiring broad semantic reconstruction before test design.

Each oracle case/assertion SHOULD point, directly or through its Oracle index, to the smallest controlling authority needed to explain its semantic meaning.

When a conformance failure needs interpretation, load the focused authority for that case rather than preloading every related Decision/Core/Skill document.

Expected token/context savings are hypotheses until measured under RCAB/load-path evidence.

## Task Contract requirements

For `orchestrator-conformance` or `mixed`, the Task Contract/prerequisite gate SHOULD identify:

```text
Test-Authorship-Mode: <mode>
Oracle-ID: <stable-id>
Oracle-Revision: <revision-or-integrated-commit>
Oracle-Assets:
  - <path>
  - <path>
Oracle-Semantic-Scope: <concise meaning>
Oracle-Freeze-State: FROZEN
Executor-Mechanical-Corrections: <none or bounded list>
```

It SHOULD also map each acceptance criterion to the relevant oracle asset/case family when that mapping materially improves auditability.

The Task Contract remains the execution-scope authority; the oracle is its executable acceptance projection.

## File-placement rule

D052 does not require a new universal top-level `conformance/` directory.

Place assets where their execution/evaluation surface is most coherent, for example:

- deterministic acceptance assets under `tests/` when they are naturally part of deterministic testing;
- agent-facing corpora/expected outcomes under `evals/` when they are naturally part of behavioral/routing evaluation;
- task-specific structured data alongside an existing narrow test/eval fixture family when that avoids duplication.

The Task Contract must identify exact Orchestrator-owned paths.

A future layout/schema decision may introduce a dedicated generated/structured oracle representation if evidence shows that it materially improves context, reproducibility or tooling. Until then, do not create a parallel directory tree merely for conceptual purity.

## Machine-readable data rule

Use JSON/JSONL or another deterministic structured form when structure materially improves reproducibility, diffability or automated grading.

A machine-readable oracle asset SHOULD:

- have canonical/stable ordering where order is not semantic;
- distinguish stable case identity from display text;
- represent expected outcomes explicitly;
- avoid embedding unnecessary normative prose;
- identify capability/acceptance references when useful;
- avoid provider-specific fields unless the case is intentionally provider-specific;
- preserve enough identity to distinguish required frozen cases from Executor-added exploratory cases.

This contract does not mandate one universal schema for all assurance planes.

## Required vs supplementary evidence

Executor-added cases remain valuable but must not silently mutate the required acceptance set.

Evidence SHOULD distinguish:

```text
required_orchestrator_oracle
supplementary_executor_tests
```

A supplementary case may later be promoted into the required oracle only through persisted Orchestrator review/revision.

This preserves independent technical exploration while preventing implementation-driven post-hoc redefinition of acceptance.

## Mechanical correction boundary

The Executor may change an Orchestrator-owned asset only when the controlling Task Contract/review explicitly authorizes a mechanical correction class.

Examples that may be mechanical if semantics remain identical:

- import/path repair;
- fixture setup/wiring repair;
- serialization syntax correction;
- runner/API compatibility adaptation;
- environment-specific harness integration.

A correction is **not mechanical** merely because it is small.

The following remain semantic and require persisted Orchestrator authority:

- expected outcome/classification;
- case category;
- required corpus membership;
- threshold;
- negative-control intent;
- security expectation;
- accepted grader meaning;
- frozen characterization meaning.

When unsure, fail closed and report `ORACLE_DEFECT` rather than edit.

## `ORACLE_DEFECT` protocol

If the Executor finds evidence that a frozen oracle is semantically wrong, contradictory or impossible under the controlling authority:

1. do not change the affected semantic asset;
2. identify the exact oracle case/assertion/path;
3. identify the controlling authority believed to conflict;
4. provide the smallest reproducible evidence;
5. report the affected acceptance claim as `ORACLE_DEFECT`-equivalent / blocked;
6. continue only unrelated work that the Task Contract safely permits without relying on the disputed oracle;
7. wait for a persisted Orchestrator revision before rerunning the affected claim.

The Orchestrator then decides whether:

- implementation is wrong;
- oracle is wrong;
- specification is ambiguous/wrong.

That decision must be persisted before semantic execution continues.

## Oracle revision after observed results

Changing semantic oracle content after implementation/eval results are observed creates a post-hoc bias risk.

Default rule:

- if the revision changes acceptance meaning, invalidate and rerun all affected evidence against the revised frozen oracle;
- if the revision is proven purely mechanical and semantics are unchanged, prior semantic results may remain usable when the evidence remains reproducible;
- comparative/routing thresholds, corpus membership and expected classifications cannot be altered after results merely to select a preferred outcome;
- any exception requires an explicit persisted rationale.

## Security/adversarial oracle rules

For security-sensitive acceptance:

- deterministic security invariants should have deterministic assertions/negative controls where possible;
- malicious/adversarial cases owned by the Orchestrator should encode the expected containment/rejection semantics, not hidden exploit instructions unnecessary to the acceptance claim;
- dynamic execution remains in disposable isolated environments under Executor control;
- no conformance asset may contain production credentials/secrets;
- external scanner/marketplace/provider scores are supplemental evidence, never the oracle.

## Behavioral/routing oracle rules

For model-mediated routing/activation work:

- use realistic positive and negative prompts;
- include near-boundary cases where false activation is plausible;
- use repeated clean-context trials;
- freeze holdout/validation membership before comparative results when optimization is occurring;
- record expected routing/classification separately from observed result;
- separate portable semantic expectation from host/model-specific measurements;
- do not collapse several provider/model cells into one opaque pass/fail when variance is material.

MG1/T023 will instantiate these rules later. This contract does not define their task-specific corpus or thresholds now.

## Characterization/refactor oracle rules

For behavior-preserving refactors:

- characterize observable behavior before structural mutation;
- distinguish intended public/contract behavior from incidental internal implementation details;
- freeze the accepted characterization baseline before refactor execution;
- do not rewrite the baseline to match the refactor after implementation begins;
- newly discovered baseline defects require explicit Orchestrator decision/revision.

## Oracle completion evidence

A final Executor handoff for a D052 task SHOULD make it possible to verify:

- exact frozen oracle revision executed;
- all required oracle assets/cases executed or exact blockers identified;
- no semantic oracle drift on the implementation branch;
- supplementary Executor cases reported separately;
- relevant results/traces/metrics are reproducible from persisted evidence;
- `ORACLE_DEFECT` events, if any, identify the exact affected semantic claim.

The handoff does not acquire acceptance authority.

## Anti-patterns

Do not:

- create an Orchestrator-owned copy of every unit test;
- move technical harness code to the Orchestrator merely because D052 exists;
- hide semantic expected values inside Executor-owned runner code when they should be frozen oracle data;
- make the Executor infer expected behavior from a large document set when a focused oracle can encode it directly;
- duplicate Governance Core prose inside every case;
- use one trivial negative control to claim a multidimensional invariant is covered;
- change corpus membership/thresholds after seeing results to make an implementation pass;
- treat supplementary Executor tests as part of the required acceptance score without Orchestrator promotion;
- create a new universal oracle directory/schema before a real need exists;
- let model-based graders replace deterministic checks for machine-decidable properties;
- treat the oracle as independent Governance authority.

## Acceptance invariants

This conformance-oracle architecture is valid only while:

1. controlling Governance/specification remains above the oracle;
2. D052 ownership modes remain explicit when material;
3. exact Orchestrator-owned assets are identified before Executor implementation when required;
4. semantic PASS/FAIL meaning cannot be changed unilaterally by the Executor;
5. mechanical corrections are bounded and semantics-preserving;
6. `ORACLE_DEFECT` fails closed on semantic disagreement;
7. Executor supplementary testing remains independent and encouraged;
8. required versus supplementary evidence is distinguishable;
9. oracle revisions after observed results are auditable and trigger rerun when meaning changes;
10. capability IDs/references can reduce context without replacing authority;
11. tests/evals remain executable evidence rather than Governance authority;
12. no T023-specific corpus/threshold is pre-registered before its proper MG1 gate.
