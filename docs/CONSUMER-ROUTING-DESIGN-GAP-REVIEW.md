# Consumer Routing Design Gap Review

Status: REVIEW / DESIGN READINESS  
Scope: topology-neutral Consumer routing architecture

## Purpose

Review the Orchestrator-only Consumer routing work completed after D050 and identify what is:

- sufficiently specified now;
- intentionally deferred to a later gated experiment/implementation;
- still a real Orchestrator-owned gap that can be closed without the Executor or premature MG1/T023 work.

This review does not modify Consumer v1 or select R*/B* candidates.

## Reviewed design stack

- `docs/CAPABILITY-CATALOG.md`
- `docs/CONSUMER-SKILL-CAPABILITY-BASELINE.md`
- `docs/SKILL-PROGRESSIVE-DISCLOSURE-DESIGN.md`
- `docs/CONSUMER-REFERENCE-BOUNDARY-CANDIDATES.md`
- `docs/CONSUMER-L1-GUARD-SPEC.md`
- `docs/CONSUMER-L1-ROUTING-CONTRACT.md`
- `docs/CONSUMER-L2-PROJECTION-MAPPING-CONTRACT.md`
- D050/D051/D052 controlling decisions/contracts

## Resolved enough for later instantiation

### Stable semantic units

Consumer routing has stable topology-neutral IDs for installation, state, execution, mission, coexistence, Skill discovery and Skill audit. Capability count is explicitly independent from command/reference/Skill count.

### Information placement

The L0-L5 model distinguishes activation metadata, early router/guards, focused capability references, Core authority, deterministic tooling and current evidence/state.

### Early safety boundary

`C-L1-G01..G09` define the minimum early Consumer guards. A future projection must map each guard to `L1-EXPLICIT` or prove `EARLY-ENFORCED` before violation is possible.

### Semantic routing

Intent classification is separated from file layout:

```text
intent/evidence -> capability ID(s)
```

Near misses override keyword similarity, multi-route selection is minimal, and material ambiguity fails closed.

### Projection mapping

Reference selection is a second independent step:

```text
capability ID(s) -> minimal sufficient L2 set
```

Mappings require coverage, de-duplication, evidence-triggered conditional loads and fail-closed handling for missing/invalid assets.

### Downstream authority

L2 cannot become a second Core. L3 remains normative authority; L4 owns machine-decidable behavior; L5 stays current-work scoped.

### Packaging and oracle boundaries

D051 preserves one-install distribution semantics regardless of reference/Skill count. D052 provides future conformance-oracle ownership without making tests authority.

## Intentionally deferred — not current gaps

The following must **not** be resolved now:

- final R0/R1/R2/R3 reference granularity;
- final B0/B1/F2/G3 activation topology;
- actual T023 corpus, holdouts, repetitions, model/host matrix or thresholds;
- final L0 descriptions/trigger wording for compared candidate entrypoints;
- actual L2 reference files and generated Skill projections;
- structured/machine-readable capability or mapping source implementation;
- source-maintainer L1 guard/routing equivalent before T022 establishes the accepted runtime/profile surface;
- provider/host-specific orchestration as portable baseline;
- independent entrypoint versions or manual multi-install packaging.

These belong to MG1/T023/T024 or later explicit gates.

## Evidence gaps that remain expected

These are not design defects but cannot be claimed as proven yet:

- no measured RCAB/task-load improvement from R1/R2/R3 or split Skills;
- no measured routing precision/recall/false-activation improvement;
- no repeated clean-context evidence for candidate routing;
- no proof that generated projections preserve every L1 guard;
- no actual reference-asset currentness/build reproducibility proof;
- no cross-host activation/permission comparison for candidate topologies.

Do not convert design intent into empirical claims before those gates run.

## Current Orchestrator-only gaps

### G-A — Consumer v1 semantic traceability

The current baseline characterizes the v1 Skill structurally, but there is not yet a compact clause-level trace showing where each material existing v1 routing/safety responsibility lands in the new architecture.

Without this trace, a future author could produce a clean-looking L1/L2 decomposition while accidentally omitting a v1 semantic requirement not captured by a headline capability/guard label.

**Disposition:** close now with a Consumer v1 semantic traceability matrix:

```text
current v1 semantic clause
 -> C-L1 guard and/or capability ID
 -> intended L2/L3/L4 destination
 -> preservation status
```

This is characterization, not implementation or topology selection.

### G-B — context-map discoverability

The stable source context map does not yet expose one compact route for the completed Consumer routing-design family. Current checkpoint can name files explicitly, but repeated future design/review should not reconstruct the set manually.

**Disposition:** after traceability is integrated, add one focused `consumer-routing-design` route only if it remains compact enough; do not put these files into cold-start/bootstrap.

### G-C — duplication/currentness audit

The new design documents intentionally overlap at boundaries (guards, routing, mapping). A future change could update one without another.

**Disposition:** keep one owner per concern:

- guard meaning -> `CONSUMER-L1-GUARD-SPEC`;
- intent classification -> `CONSUMER-L1-ROUTING-CONTRACT`;
- capability metadata -> `CAPABILITY-CATALOG`;
- reference mapping invariants -> `CONSUMER-L2-PROJECTION-MAPPING-CONTRACT`;
- candidate reference groupings -> `CONSUMER-REFERENCE-BOUNDARY-CANDIDATES`.

Other documents should point rather than restate when future edits occur. No new meta-schema is justified yet.

## Not recommended now

Do not create:

- another routing abstraction layer;
- one document per capability;
- final reference files just to make the design concrete;
- machine-readable routing JSON merely because the Markdown model exists;
- a source-maintainer mirror before T022;
- synthetic T023 cases/thresholds early;
- a generic orchestrator Skill or Skill-to-Skill protocol.

Those steps would either add context/maintenance surface or pre-empt later evidence.

## Readiness assessment

The topology-neutral Consumer routing design is **architecturally sufficient for later candidate instantiation**, subject to closing G-A semantic traceability.

After G-A, no additional routing architecture should be added without a concrete discovered gap.

The remaining decisive questions are empirical and gated:

```text
Which reference grouping performs best? -> later measured evidence
Which Skill topology performs best?      -> MG1/T023
How is it generated/packaged?            -> T024/D051
```

## Next safe action

Create the Consumer v1 semantic traceability matrix. It must:

1. use the current accepted `governance-skill/SKILL.md` as characterized input;
2. map every material routing/safety/procedure family to existing guard/capability/Core/tool destinations;
3. identify any truly unmapped v1 behavior as a design gap rather than inventing a destination;
4. avoid changing v1 wording/behavior;
5. avoid choosing R*/B* candidates;
6. avoid defining T023 cases/thresholds.

## Acceptance invariants

1. no deferred MG1/T023/T024 question is silently decided here;
2. empirical claims remain unproven until measured;
3. G-A traceability is the only required next routing-design artifact;
4. G-B is routing/index hygiene, not a new semantic layer;
5. G-C preserves single ownership per design concern;
6. no source-maintainer runtime completion is inferred;
7. no Executor action is required;
8. no Consumer v1 behavior is modified.