# Consumer L2 Projection Mapping Contract

Status: DESIGN-APPROVED  
Routing: `docs/CONSUMER-L1-ROUTING-CONTRACT.md`  
Guards: `docs/CONSUMER-L1-GUARD-SPEC.md`  
Candidates: `docs/CONSUMER-REFERENCE-BOUNDARY-CANDIDATES.md`

## Purpose

Define topology-neutral rules for mapping already-classified Consumer capability IDs to the L2 reference set of a generated projection.

```text
stable capability ID(s)
 -> projection mapping
 -> minimal L2 reference set
 -> focused L3/L4/L5 load
```

This contract governs mapping correctness, not which R0/R1/R2/R3 or B0/B1/F2/G3 candidate wins. It creates no actual reference files and defines no T023 corpus/threshold.

## Separation invariant

Semantic routing and file mapping are different layers:

```text
intent -> capability ID(s)     = L1 routing semantics
capability ID(s) -> references = projection mapping
```

Changing reference grouping MUST NOT change capability classification, authority, supported behavior or guard meaning.

## Mapping requirements

Every candidate projection must provide a complete mapping for every Consumer capability it exposes.

A mapping entry needs only enough information to answer:

- which stable capability ID(s) it covers;
- which L2 reference asset(s) must load for that ID/set;
- which additional references are conditional rather than always required;
- whether another selected capability already supplies the same reference;
- which L3 Core destinations the L2 reference may route onward to.

Do not create a second editable copy of capability semantics inside mapping metadata.

## Coverage

For the Consumer profile, mapping coverage must account for:

- `consumer.lifecycle.installation`;
- `consumer.lifecycle.state`;
- `consumer.lifecycle.execution`;
- `consumer.lifecycle.mission`;
- `consumer.lifecycle.coexistence`;
- `consumer.skill-trust.discovery`;
- `consumer.skill-trust.audit`.

A topology that intentionally removes a family from one entrypoint must still expose it through the selected Agent Governance distribution if that capability remains supported. G3 is therefore a distribution/topology question, not permission to drop semantics.

## Reference-set construction

Given selected capability IDs:

1. resolve each ID through the active projection mapping;
2. take the union of required L2 references;
3. de-duplicate identical reference assets;
4. add conditional references only when current evidence triggers their condition;
5. preserve any required semantic ordering between operations without treating file order as authority;
6. stop if any selected capability lacks a valid mapping.

The result is the **minimal sufficient L2 set**, not the smallest possible file count.

## Conditional-reference rules

Conditional loads should preserve current-work minimality.

Examples:

- coexistence detail loads when existing ownership/collision is material;
- `SECURITY`-oriented audit detail loads when security/permission envelope is material;
- execution-control detail loads when the control boundary is actually involved;
- state detail may accompany execution only when current-state derivation is needed;
- audit need not load merely because discovery is active.

A candidate must not hide universally required safety behind a conditional L2 load; `C-L1-G*` controls that boundary.

## Composition and de-duplication

`ROUTE_MULTI` may produce shared references. Shared assets load once per current routing episode unless the host requires otherwise.

Reference union must not:

- duplicate the same Core semantics across several L2 files merely to avoid a shared pointer;
- turn a commonly shared guard into hand-maintained divergent text;
- force unrelated capabilities to load together solely because one candidate file happened to combine them;
- split one coherent operation across several references without evidence that the extra fan-out helps.

## Candidate compatibility

The contract permits different internal mappings.

Conceptually:

```text
R1: state + execution + mission may map to one coarse lifecycle reference
R2: state, execution, mission may map to separate references
R3: discovery and audit may map separately
```

All such candidates must produce semantically equivalent downstream behavior for the same capability decision.

Reference candidate identity is experimental metadata, not Governance authority.

## L2 content boundary

A mapped L2 reference may contain:

- capability-specific procedure;
- capability-specific near misses;
- capability-specific mutation preconditions;
- command/tool mapping;
- missing-capability handling;
- pointers to the smallest applicable Core modules.

It must not become a second Core, duplicate the canonical L1 guard set, redefine profile permissions or encode topology-specific behavior forks.

## L3/L4/L5 continuation

Mapping ends at L2 selection.

From there:

- L3 provides normative protocol semantics;
- L4 provides machine-decidable checks/actions;
- L5 provides exact current state/evidence.

A mapping may point onward but must not copy full L3/L4 semantics into L2 merely to reduce navigation depth.

## Failure states

Projection mapping fails closed when:

- a selected capability ID has no mapping;
- the mapping targets a missing reference asset;
- a required reference is conditionally omitted without evidence;
- mapping would cross Consumer/source-maintainer profile boundaries;
- a candidate mapping changes accepted capability meaning;
- a guard required before L2 is available only inside the selected reference.

These are projection defects, not semantic reclassification opportunities.

## D051 packaging constraint

Every selected L2 reference remains part of the same Agent Governance distribution/install unit. Progressive disclosure changes what is loaded, not what the user must separately install.

No R*/B* candidate may require manual acquisition of additional Agent Governance reference/support packages after installation.

## Review identity

A future generated projection should be reviewable through three independent layers:

```text
1. intent -> capability ID(s)
2. capability ID(s) -> L2 reference set
3. L2 -> Core/tool/state behavior
```

This separation allows later evidence to localize routing, mapping and downstream behavior failures without changing the oracle after results.

## RCAB metrics

Later comparison should measure at least:

- number/bytes of L2 references actually loaded for representative tasks;
- duplicate reference/Core content;
- conditional-load precision;
- missing/extra reference selection;
- fan-out/navigation depth;
- complete L0-L5 load path;
- task success and guard preservation.

No threshold is set here.

## Acceptance invariants

1. every supported Consumer capability has valid projection coverage;
2. mapping never changes semantic classification;
3. required references are unioned and de-duplicated;
4. conditional loads require current evidence;
5. missing mappings/assets fail closed;
6. L1 guards stay effective before L2;
7. L2 points to rather than duplicates Core/tool semantics;
8. Consumer/source-maintainer isolation remains intact;
9. D051 one-install semantics remain intact;
10. R*/B* remain experimental choices;
11. D052 may verify mapping equivalence but is not authority;
12. RCAB conclusions require measured full-load evidence.