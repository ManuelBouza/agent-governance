# Consumer Reference-Boundary Candidates

Status: CHARACTERIZATION / DESIGN INPUT  
Decision context: D050  
Placement rules: `docs/SKILL-PROGRESSIVE-DISCLOSURE-DESIGN.md`  
Baseline: `docs/CONSUMER-SKILL-CAPABILITY-BASELINE.md`

## Purpose

Define topology-neutral **L2 reference-boundary candidates** for the current Consumer capability family.

These candidates are possible internal progressive-disclosure groupings. They are not top-level Skills, do not change Consumer v1, do not select B0/B1/F2/G3, and do not pre-register T023 experimental results.

## Fixed L1 guard envelope

Every candidate assumes the activated Consumer router keeps enough L1 guidance to preserve:

- explicit Agent Governance scope and negative activation boundary;
- repository/installed Core authority over Skill guidance;
- no invented strategy, requirements, approval or acceptance;
- source independence;
- read-only/check default and fail-closed mutation behavior;
- unresolved authority/managed-state collision stop behavior;
- current-task-only disclosure;
- smallest-capability routing and missing-capability honesty.

A candidate cannot appear smaller by moving one of these guards behind a reference that may not load before risk occurs.

## Candidate set

### `R0` — current Skill-local monolith

```text
L1
  lifecycle + coexistence + Skill trust procedure
L2
  none
```

Purpose: structural baseline only.

Advantages:
- no reference selection error;
- all Consumer operational guidance visible after activation.

Risks/costs:
- every activation receives all Skill-local operation families;
- lifecycle and external Skill trust guidance share one body despite different intent/risk envelopes;
- combined state/execution/mission section mixes deterministic-first and authority-led concerns.

### `R1` — coarse four-reference split

```text
L1 Consumer router
  -> installation
  -> state-execution-mission
  -> coexistence
  -> skill-trust
```

Mapping:

| L2 reference | Catalog coverage |
| --- | --- |
| `installation` | `consumer.lifecycle.installation` |
| `state-execution-mission` | state + execution + mission |
| `coexistence` | `consumer.lifecycle.coexistence` |
| `skill-trust` | discovery + audit |

Rationale: separates the strongest context/risk boundaries while keeping highly coupled lifecycle work together.

Primary risk: state/execution/mission may remain too broad and mix authority-led mission work with deterministic-first state work.

### `R2` — lifecycle-focused six-reference split

```text
L1 Consumer router
  -> installation
  -> state
  -> execution
  -> mission
  -> coexistence
  -> skill-trust
```

Mapping is one L2 route for each lifecycle sub-capability, while discovery/audit remain together.

Rationale: mirrors the current capability catalog without turning trust discovery and trust audit into separate files.

Primary risks:
- more reference-selection decisions/fan-out;
- some state/execution/mission tasks may legitimately require multiple references;
- could create micro-routing overhead without reducing actual Core/project-state load.

### `R3` — trust-split seven-reference candidate

```text
L1 Consumer router
  -> installation
  -> state
  -> execution
  -> mission
  -> coexistence
  -> skill-discovery
  -> skill-audit
```

Rationale: discovery and audit have different operational phases and deterministic coverage; audit has the stronger provenance/permission/security envelope.

Primary risk: discovery commonly hands directly into audit, so two references may increase load/fan-out without providing enough independent reuse.

## Boundary evidence matrix

| Boundary | Evidence for separation | Evidence for grouping |
| --- | --- | --- |
| installation vs other lifecycle | bootstrap/overwrite/D051 concerns; unique project initialization mutation | validation/coexistence preflight shares Core/ownership rules |
| state vs execution | state derivation/protocol checks are deterministic-first | execution depends on current state/dependencies/handoff |
| execution vs mission | current-task disclosure and handoff mechanics differ from mission creation/archive authority | mission work uses task ordering/execution records |
| coexistence vs lifecycle | only needed when capability/ownership overlap is material; semantic classification surface | bootstrap/mission may conditionally require it |
| Skill trust vs lifecycle | distinct provenance/threat/permission envelope; candidate quarantine behavior | same Consumer product/profile and common authority/source-independence rules |
| discovery vs audit | different phase; audit has exact artifact/envelope/security checks | discovery frequently flows directly to audit; same trust objective |

This matrix is evidence for **candidate boundaries**, not proof that a boundary should become a file or Skill.

## Command mapping constraint

Reference boundaries must not be generated from CLI count.

Current relationships include:

- installation -> `bootstrap`, `validate`;
- state -> `state`, `event`;
- execution -> no dedicated handoff/sequential command;
- mission -> `archive` plus model/Strategy-guided initialization;
- coexistence -> `ecosystem`;
- discovery -> no dedicated command;
- audit -> `skill` covers bounded deterministic validation only.

Therefore one-command-per-reference would misrepresent capability semantics.

## Core-reference constraint

L2 candidates should route onward rather than duplicate installed Core.

Representative destinations:

- installation -> Consumer contract + conditional D051/COEXISTENCE;
- state -> PROTOCOL/CONTEXT/LIFECYCLE;
- execution -> HANDOFF/EXECUTION/EXECUTION-CONTROL as needed;
- mission -> LIFECYCLE + conditional EXECUTION/COEXISTENCE;
- coexistence -> COEXISTENCE;
- discovery -> SKILL-DISCOVERY;
- audit -> SKILL-SUPPLY-CHAIN + conditional SECURITY/COEXISTENCE.

## Comparison dimensions for later evidence

When a future gate is eligible, R0/R1/R2/R3-like internal groupings may be compared on:

- L1 body size/load;
- L2 reference count actually loaded per task;
- retrieval fan-out/navigation depth;
- duplicate safety/procedure text;
- wrong/missing reference selection;
- multi-intent reference combinations;
- task success and deterministic regression;
- cross-capability contamination;
- total Core/project-state load path.

No threshold or winner is defined here.

## Relationship to D050 topologies

These are **internal reference granularity candidates**, orthogonal to top-level activation topology.

Examples:

- B1 could use R1, R2, R3 or another measured grouping;
- F2 Consumer entrypoint could use the same internal references;
- G3 would remove Skill-trust from the Consumer-lifecycle entrypoint but still needs an internal trust-reference decision;
- B0 may also use focused references beneath a unified dispatcher.

Do not conflate `R*` reference grouping with `B0/B1/F2/G3` Skill topology.

## No-decision boundary

This document does not authorize:

- actual creation/movement of Skill references;
- changing accepted Consumer v1 routing text;
- selecting R1/R2/R3;
- selecting a D050 topology;
- splitting External Skill Trust for release;
- changing Core/runtime/profile semantics;
- T023 corpus/threshold/holdout definition.

## Acceptance invariants

Any future reference grouping must preserve:

1. fixed L1 safety/authority envelope;
2. identical accepted capability semantics;
3. one shared Core/runtime/product authority;
4. Consumer/source-maintainer isolation;
5. D051 one-install packaging;
6. deterministic checks at L4 rather than copied prose;
7. exact current-work disclosure;
8. D052 required/supplementary evidence separation;
9. no command/file-count decomposition rule;
10. MG1/T023 authority over final experimental selection.
