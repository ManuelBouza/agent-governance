# Consumer L1 Routing Decision Contract

Status: DESIGN-APPROVED  
Guards: `docs/CONSUMER-L1-GUARD-SPEC.md`  
Catalog: `docs/CAPABILITY-CATALOG.md`

## Purpose

Define topology-neutral L1 routing semantics for Consumer Agent Governance.

```text
current intent/evidence
 -> stable capability ID(s)
 -> projection-specific L2 mapping
 -> focused Core/tool/state load
```

Classification must not depend on reference-file count or Skill topology. This contract selects no R0/R1/R2/R3 or B0/B1/F2/G3 candidate and defines no T023 corpus/threshold.

## Inputs

Use only current routing evidence:
- current request;
- already-established Consumer repository/profile context;
- current-work state needed to understand that request;
- capability intent/near-miss boundaries from the catalog;
- active capability-ID -> L2 mapping;
- applicable `C-L1-G*` guards.

Do not preload future tasks, unrelated history, every L2 reference or source-maintainer context just to classify intent.

## Conceptual outcomes

- `ROUTE` — one capability fits.
- `ROUTE_MULTI` — a minimal current-intent set is genuinely required.
- `OUT_OF_SCOPE` — not Consumer Agent Governance work.
- `AMBIGUOUS` — missing evidence matters to materially different routes/effects.
- `CONFLICT` — unresolved accepted authority/ownership collision.
- `MISSING_CAPABILITY` — valid Consumer need but no safe installed path.

These labels are design vocabulary, not protocol events or runtime exit codes.

## Routing sequence

### 1. Consumer boundary

Apply `C-L1-G01..G03` first.

Do not route source maintenance, generic application work, generic planning/testing/refactoring/release, generic SDD operation or generic Skill installation into Consumer capabilities merely because Governance is mentioned.

### 2. Classify action/effect, not keywords

| Current intent | Capability ID |
| --- | --- |
| bootstrap/install validation/portability | `consumer.lifecycle.installation` |
| cold-start/state/protocol/checkpoint derivation | `consumer.lifecycle.state` |
| handoff/readiness/sequential disclosure | `consumer.lifecycle.execution` |
| mission initialization/archive | `consumer.lifecycle.mission` |
| project capability/authority overlap | `consumer.lifecycle.coexistence` |
| locate/resolve external Skill candidate | `consumer.skill-trust.discovery` |
| exact artifact provenance/risk/envelope audit | `consumer.skill-trust.audit` |

A mention of `skill`, `state`, `task`, `install` or `audit` alone is insufficient. Catalog reject/near-miss boundaries override lexical similarity.

### 3. Resolve match cardinality

- zero matches + non-Governance intent -> `OUT_OF_SCOPE`;
- zero matches + valid unsupported Consumer need -> `MISSING_CAPABILITY`;
- insufficient evidence to distinguish safely -> `AMBIGUOUS`;
- one supported match -> `ROUTE`;
- multiple matches -> `ROUTE_MULTI` only when all are required by the current request.

If candidates differ materially in authority, mutation effect or trust/security envelope and evidence does not resolve the choice, do not guess.

## Composition rules

Valid multi-capability compositions may include:

- installation + coexistence when bootstrap/validation encounters existing managed ownership;
- mission + coexistence when native SDD/spec ownership is material;
- state + execution when current-state derivation is required for readiness;
- discovery + audit when the explicit request covers candidate resolution and subsequent artifact audit.

Composition is demand-driven. Do not load adjunct capabilities merely because they may become useful.

## Ambiguity examples

Fail closed rather than preload all candidates for requests such as:

- “update governance” when install mutation, state refresh and source-product update are plausible;
- “validate governance” when installed footprint vs current state is materially unresolved;
- “approve this Skill” when authority approval vs artifact audit is unclear;
- “continue the project” without enough evidence to distinguish state, execution or mission work.

Ask only for the missing discriminator when clarification is required.

## Projection mapping

Semantic classification happens **before** reference mapping:

```text
capability ID set
 -> active projection mapping
 -> de-duplicated minimal L2 reference set
```

R0/R1/R2/R3 may map the same IDs differently. A projection must not change capability meaning to fit its layout, load every reference as a routing substitute, or imply one capability per file.

## Pre-effect gate

Before mutation, external effect or broader evidence load, apply the relevant guards:

- `C-L1-G04` read-only default / mutation authority;
- `C-L1-G05` collision fail-closed;
- `C-L1-G06` current-work disclosure;
- `C-L1-G07` smallest applicable route;
- `C-L1-G08` capability honesty;
- `C-L1-G09` bounded external effects/secrets.

Correct routing does not grant effect permission.

## Missing capability

When a legitimate Consumer operation lacks a required installed command/reference/tool path:

1. identify the missing path honestly;
2. do not fabricate execution;
3. use only an already-authorized repository-native fallback preserving the same Governance invariants;
4. otherwise stop as `MISSING_CAPABILITY`.

Tool availability is not permission; tool absence is not permission to bypass Governance.

## Future review/eval decomposition

A projection should be reviewable as two independent mappings:

```text
intent class -> capability ID(s)
capability ID(s) -> L2 reference set
```

This lets later D052 evidence distinguish semantic misclassification from projection/reference error, guard failure, missing runtime/tooling or downstream Core/state failure. Actual cases, holdouts, repetitions and thresholds remain MG1 authority after T022.

## RCAB

Routing quality is not fewest files. Later evidence should measure wrong/missed routes, unnecessary L2 loads, fan-out/navigation depth and the full L0-L5 load path while preserving guards and task success.

## Acceptance invariants

1. stable capability semantics drive classification;
2. near-miss boundaries override keyword similarity;
3. `ROUTE_MULTI` is minimal/current-intent driven;
4. unresolved material ambiguity fails closed;
5. semantic classification precedes projection mapping;
6. R*/B* layout changes do not redefine capability meaning;
7. effect authorization is separate from routing;
8. applicable L1 guards hold before risk/effect;
9. missing capability is reported, never fabricated;
10. Consumer/source-maintainer isolation remains intact;
11. D052 may verify mappings but is not authority;
12. no T023 corpus/holdout/threshold is defined here.