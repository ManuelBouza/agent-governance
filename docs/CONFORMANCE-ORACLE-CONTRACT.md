# Conformance Oracle Contract

Status: DESIGN-APPROVED  
Controlling decision: `docs/decisions/D052-specification-owned-conformance-test-authorship.md`

## Purpose

Define the reusable contract for **Orchestrator-owned conformance/oracle assets** under D052 without requiring each Skill/governance task to reconstruct acceptance semantics from broad testing documentation.

Core rule:

> Test authorship follows semantic authority.

A conformance oracle is an executable/data projection of approved semantics. It is evidence, not Governance authority.

## Authority

```text
Human / accepted Governance authority
    -> governance-core/ where applicable
    -> accepted Decision / functional contract / Task Contract
    -> Orchestrator-owned conformance oracle
    -> Executor harness / execution / evidence
```

If the oracle conflicts with its controlling specification, the specification wins and the oracle must be corrected through persisted Orchestrator authority.

## Applicability

Use this contract when a Task Contract selects:

- `orchestrator-conformance`; or
- `mixed` for the Orchestrator-owned semantic surface.

Typical uses: Agent Skills, Governance/policy protocols, documentation-managed workflows, routing/classification semantics, security acceptance and frozen characterization baselines.

Ordinary consumer/application implementation remains `executor-implementation` by default.

## Oracle vs harness

Ownership is semantic, not based only on file extension/path.

**Oracle** = material whose change can alter what counts as PASS/FAIL while implementation stays identical.

Examples:
- required case membership;
- expected result/classification/decision;
- deterministic acceptance assertion meaning;
- semantic negative controls;
- accepted thresholds/non-regression rules;
- contract-significant golden fixture contents;
- security/adversarial expectations;
- frozen characterization behavior;
- deterministic grader logic when it directly encodes approved expected semantics.

**Harness** = material that executes, isolates, transports, collects or aggregates the oracle.

Examples:
- pytest/eval runner mechanics;
- environment/session setup;
- provider/host adapters;
- tool/subprocess wiring;
- trace collection;
- metrics aggregation implementation;
- benchmark/timing plumbing;
- debugging helpers.

Harness/technical implementation remains Executor-owned unless a separate accepted rule says otherwise.

When ownership is unclear, ask:

```text
Could changing this value/code change accepted PASS/FAIL meaning
without changing the implementation under test?
```

`yes` -> presumptively oracle semantics.  
`no` -> presumptively harness/technical implementation.

The Task Contract overrides this heuristic when it assigns ownership explicitly.

## Oracle identity and lifecycle

Every material oracle SHOULD be identified by its Task Contract or prerequisite gate using only the metadata needed for auditability:

```text
Oracle-ID: <stable-id>
Oracle-Revision: <label or canonical Git identity>
Oracle-Assets:
  - <path>
Oracle-Semantic-Scope: <concise meaning>
Oracle-Freeze-State: DRAFT | FROZEN | SUPERSEDED | RETIRED
Executor-Mechanical-Corrections: none | <bounded classes>
```

Do not create a separate manifest when the Task Contract already carries this information clearly.

Lifecycle:
- `DRAFT` — still authored/reviewed; not eligible for implementation acceptance.
- `FROZEN` — integrated in canonical `develop` and eligible for execution.
- `SUPERSEDED` — replaced by a persisted Orchestrator revision; supersession states whether prior evidence remains usable or must rerun.
- `RETIRED` — no longer current acceptance input but retained as auditable history.

A task requiring pre-authored conformance MUST NOT begin before the required oracle is `FROZEN` and reachable from the Executor's current canonical base.

## Oracle asset classes

Use only the classes a task actually needs.

| Class | Semantic content |
| --- | --- |
| case corpus | required positive/negative/near-miss/cross-profile/ambiguous/multi-intent/security/compatibility/characterization cases |
| expected outcomes | required decisions/classifications/state/output properties |
| deterministic assertions | machine-decidable acceptance invariants |
| semantic negative controls | materially incorrect variants selected to prove the criterion boundary |
| thresholds / decision rules | accepted victory/non-regression rules |
| golden fixtures | exact fixture state when that state itself is contractual |
| grader expectations | accepted deterministic/model-grader meaning |
| characterization baseline | accepted observable behavior frozen before behavior-preserving refactor |

### Negative-control sufficiency

Negative controls MUST exercise the semantic boundary promised by the criterion, not merely one convenient corruption.

If a criterion covers materially distinct dimensions, the oracle SHOULD contain representative controls for those dimensions.

This incorporates the T020/T032 lesson: green tests and one negative case do not prove a multidimensional boundary.

## Capability-source integration

For Agent Governance Skill/governance work, prefer stable capability references from `docs/CAPABILITY-SOURCE-CONTRACT.md`, for example:

```text
consumer.lifecycle
consumer.skill-trust
source.maintenance
```

This reduces duplicated intent/profile/risk prose while preserving the controlling normative references.

Capability IDs are routing metadata, not authority.

## Minimal-context rule

A D052 task should allow the Executor to begin from:

```text
repository bootstrap
    -> exact Task Contract
    -> exact frozen oracle assets
    -> implementation surface
```

rather than first reconstructing the oracle from a broad document graph.

Cases/assertions SHOULD carry the smallest useful authority/capability reference needed to interpret a failure. Load deeper focused authority only when that case actually requires it.

Token/context benefit must be measured from real load paths; it is not assumed merely because an oracle exists.

## Task Contract binding

For `orchestrator-conformance`/`mixed`, the Task Contract or prerequisite gate SHOULD record the Oracle identity block above and map acceptance criteria to exact oracle assets/case families when material.

The Task Contract remains execution-scope authority. The oracle is its executable acceptance projection.

## File placement and data format

D052 does **not** require a universal top-level `conformance/` directory.

Use the existing coherent surface:
- deterministic conformance assets under `tests/` when appropriate;
- agent-facing/routing corpora and expected outcomes under `evals/` when appropriate;
- narrow task-specific structured fixture locations when that avoids duplication.

The Task Contract identifies exact Orchestrator-owned paths.

Use JSON/JSONL or another deterministic format when structure materially improves reproducibility/diffability. Structured oracle data SHOULD:
- keep stable case IDs;
- represent expected outcomes explicitly;
- use canonical ordering where order is not semantic;
- avoid unnecessary copied normative prose;
- distinguish required frozen cases from Executor-added exploratory cases;
- separate portable semantics from provider-specific fields.

No universal oracle schema is mandated across all assurance planes.

## Required vs supplementary tests

Executor-added tests remain encouraged but MUST NOT silently change the required acceptance set.

Evidence distinguishes:

```text
required_orchestrator_oracle
supplementary_executor_tests
```

A supplementary case enters the required oracle only through persisted Orchestrator review/revision.

## Mechanical correction boundary

The Executor may edit an Orchestrator-owned asset only when durable authority explicitly permits a bounded **mechanical** correction whose semantic meaning is unchanged.

Potentially mechanical:
- import/path repair;
- fixture setup/wiring repair;
- serialization syntax correction;
- runner/API compatibility adaptation;
- environment-specific harness integration.

Semantic and therefore Orchestrator-owned:
- expected result/classification;
- case category;
- required corpus membership;
- threshold;
- negative-control intent;
- security expectation;
- grader meaning;
- frozen characterization meaning.

A change is not mechanical merely because it is small.

When uncertain, fail closed and report `ORACLE_DEFECT` rather than edit.

## `ORACLE_DEFECT`

When a frozen oracle appears semantically wrong or contradictory:

1. do not change the disputed semantic asset;
2. identify exact case/assertion/path;
3. identify the controlling authority believed to conflict;
4. provide the smallest reproducible evidence;
5. block the affected acceptance claim as `ORACLE_DEFECT`-equivalent;
6. continue only unrelated work safely independent of that claim;
7. wait for a persisted Orchestrator revision before rerunning it.

The Orchestrator determines whether the defect is in implementation, oracle or specification and persists any semantic correction.

## Revision after observed results

Changing semantic oracle content after implementation/eval results are visible creates post-hoc bias risk.

Default:
- semantic change -> affected evidence is invalidated and rerun against the new frozen oracle;
- proven mechanical change -> prior semantic evidence may remain usable if reproducible;
- corpus membership, expected classifications and thresholds MUST NOT change merely to select a preferred comparative result;
- exceptions require explicit persisted rationale.

## Assurance-specific rules

### Behavioral/routing
- realistic positives and negatives;
- near-boundary false-activation cases;
- repeated clean-context trials;
- frozen holdout/validation membership when optimization/comparison occurs;
- expected classification stored separately from observed result;
- portable semantic expectations separated from host/model-specific measurements.

MG1/T023 will instantiate these later; this contract does not define their task-specific corpus/thresholds now.

### Security/adversarial
- deterministic security invariants use deterministic assertions/negative controls where possible;
- expected containment/rejection semantics belong in the oracle;
- dynamic execution remains isolated under Executor control;
- no production credentials/secrets in oracle assets;
- external scanner/marketplace/provider scores remain supplemental evidence.

### Refactor characterization
- characterize observable behavior before structural mutation;
- freeze intended contract behavior, not arbitrary internal implementation detail;
- do not rewrite the baseline after refactor work starts;
- discovered baseline defects require persisted Orchestrator decision/revision.

## Completion evidence

A D052 Executor handoff SHOULD prove:
- exact frozen oracle revision executed;
- all required cases/assets executed or exact blockers identified;
- no semantic oracle drift on the implementation branch;
- supplementary Executor tests reported separately;
- persisted evidence can reproduce relevant results/metrics;
- any `ORACLE_DEFECT` identifies the affected semantic claim.

The handoff remains evidence, not acceptance authority.

## Anti-patterns

Do not:
- make the Orchestrator own every unit test;
- move ordinary harness/debug code to the Orchestrator;
- hide semantic expected values inside Executor-owned runner code;
- require broad-document reconstruction when a focused frozen oracle can encode the acceptance boundary;
- duplicate Core prose inside every case;
- use one trivial negative control for a multidimensional invariant;
- change required cases/thresholds after seeing results to force PASS;
- mix supplementary Executor cases into the required score without Orchestrator promotion;
- create a universal oracle directory/schema before evidence requires it;
- replace deterministic checks with model graders for machine-decidable properties;
- treat the oracle as Governance authority.

## Acceptance invariants

1. controlling specification remains above the oracle;
2. D052 ownership mode is explicit when material;
3. required Orchestrator assets are frozen before implementation when required;
4. semantic PASS/FAIL meaning cannot be changed unilaterally by the Executor;
5. mechanical corrections remain bounded and semantics-preserving;
6. `ORACLE_DEFECT` fails closed;
7. supplementary Executor testing remains independent and encouraged;
8. required vs supplementary evidence is distinguishable;
9. semantic oracle revisions after observed results are auditable and rerun affected evidence;
10. capability references may reduce context without replacing authority;
11. tests/evals remain evidence, never Governance authority;
12. no T023-specific corpus/threshold is pre-registered before MG1.
