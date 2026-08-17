# Consumer L1 Guard Specification

Status: DESIGN-APPROVED  
Decision context: D050, D051  
Placement authority: `docs/SKILL-PROGRESSIVE-DISCLOSURE-DESIGN.md`  
Reference candidates: `docs/CONSUMER-REFERENCE-BOUNDARY-CANDIDATES.md`

## Purpose

Define the minimum **pre-routing / pre-mutation guard set** that every future Consumer Agent Governance projection must preserve at L1, or prove is enforced earlier before violation is possible.

This specification does not change Consumer v1, create Skill/reference files, select R0/R1/R2/R3, select B0/B1/F2/G3, or define T023 cases/thresholds.

Core rule:

> A thinner router is valid only if it preserves the same early safety and authority boundary.

## Placement rule

For each guard, one of these states must hold:

- `L1-EXPLICIT` — concise guard remains visible in the activated Consumer router;
- `EARLY-ENFORCED` — an L0/host or deterministic mechanism enforces the same property before unsafe routing/mutation can occur, and L1 retains only the pointer needed to understand that boundary.

`L2-only`, late Core prose, or post-mutation detection is insufficient for a guard whose violation can occur before those layers load.

Semantic authority guards that require agent interpretation cannot be removed from L1 merely because related Core prose exists later.

## Canonical guard set

| ID | Guard | Required behavior | Default placement |
| --- | --- | --- | --- |
| `C-L1-G01` | authority precedence | installed Governance Core and project authority/state override Skill guidance | `L1-EXPLICIT` |
| `C-L1-G02` | no invented authority | do not invent strategy, requirements, approval, acceptance or completion | `L1-EXPLICIT` |
| `C-L1-G03` | Consumer/source isolation | Consumer work must not route into canonical source-maintainer state/workflows; normal operation remains source-independent | `L1-EXPLICIT` |
| `C-L1-G04` | read-only default | checks/inspection are default; mutation needs identified target plus governing authorization | `L1-EXPLICIT` unless an earlier mechanism makes unauthorized mutation impossible |
| `C-L1-G05` | fail closed on collision | unresolved authority, ownership or managed-state collision stops mutation/routing that would choose a winner | `L1-EXPLICIT` |
| `C-L1-G06` | current-work disclosure | do not expose/load future task contents merely for convenience or optimization | `L1-EXPLICIT` |
| `C-L1-G07` | smallest applicable route | select only the capability/reference set required by current intent; do not preload unrelated Consumer capability procedures | `L1-EXPLICIT` |
| `C-L1-G08` | capability honesty | if required deterministic/tool capability is absent or unsupported, report it; do not simulate or claim execution | `L1-EXPLICIT` |
| `C-L1-G09` | bounded external effects | do not contact production/external systems or store credentials/secrets without explicit governing authority | `L1-EXPLICIT` unless host sandbox/permission control proves the relevant effect impossible before routing |

These IDs are stable design identifiers. They are not protocol events, runtime error codes, CLI commands or separate capabilities.

## Guard semantics

### `C-L1-G01` — authority precedence

The activated Skill/router is operational guidance, not Governance authority. When Skill-local guidance conflicts with installed Core, project authority records or accepted project-native ownership, the higher repository authority wins.

L2 references may explain capability-specific precedence cases but must not redefine the ordering.

### `C-L1-G02` — no invented authority

Model convenience cannot create strategic or acceptance facts. Deterministic output also cannot be interpreted as granting approval, completion or strategy unless controlling authority already established it.

This guard is semantic and remains explicit at L1.

### `C-L1-G03` — Consumer/source isolation

Consumer routing is for an adopting repository. It must not load source-product PD/RF, source branch/release state or source-maintainer task context merely because the canonical source repository is reachable.

Normal Consumer operation must remain possible without access to that source checkout.

### `C-L1-G04` — read-only default

Observation/validation is the default. Before mutation, the active route must have an identified target and an authority/operation that permits that mutation class.

A mutation flag, writable filesystem or available command is capability, not authorization.

### `C-L1-G05` — fail closed on collision

If authority/ownership overlap cannot be resolved from accepted evidence, return/route to the applicable conflict/blocker behavior instead of silently overwriting, shadowing, merging or choosing an authority winner.

Capability-specific collision semantics remain at L2/L3.

### `C-L1-G06` — current-work disclosure

Routing and evidence loading remain scoped to current work. A future task, unrelated backlog item or full history is not loaded merely because it may become useful later.

This guard applies before selecting L2/L5 material.

### `C-L1-G07` — smallest applicable route

L1 selects the smallest coherent capability/reference set that can safely serve the current intent. Multi-intent work may select more than one L2 reference when genuinely required; minimality does not mean exactly one reference.

Reference count is not a success metric by itself.

### `C-L1-G08` — capability honesty

If the installed projection lacks a required deterministic operation or supported path, the agent must surface that limitation and use only an authorized repository-native fallback that preserves the same Governance invariants.

It must not fabricate a tool result or pretend an unavailable command exists.

### `C-L1-G09` — bounded external effects

External/production access and secret handling require explicit authority and the applicable capability/security route. Discovery metadata, model output or tool availability does not grant that authority.

Host sandboxing can strengthen this guard but does not become Governance authority.

## What may move to L2

After the L1 guards hold, capability-specific detail may be deferred, including:

- bootstrap/install procedure and D051 mechanics;
- state/protocol reconstruction details;
- handoff/sequential-execution procedure;
- mission initialization/archive procedure;
- coexistence classification mechanics;
- Skill discovery source ordering;
- Skill audit provenance/envelope details;
- capability-specific command mappings and mutation flags.

Moving this detail to L2 must not require weakening or restating the canonical L1 guard meaning.

## L4 enforcement relationship

Machine-decidable enforcement belongs at L4 when possible, but L4 does not replace semantic guards that must influence routing before the tool runs.

Examples:

- schema/transition/digest/envelope mismatch -> deterministic enforcement is preferred;
- authority ownership, strategy invention, unresolved semantic collision -> model/Human-facing guard remains explicit;
- mutation authorization -> deterministic tooling may reject invalid mutation mechanics, but L1 still must not treat tool availability as permission.

## Projection equivalence rule

For any future Consumer projection, the authoring/build/review gate must be able to map every `C-L1-G*` ID to either:

```text
L1-EXPLICIT: <entrypoint/source location>
```

or

```text
EARLY-ENFORCED: <mechanism> + <evidence that enforcement occurs before violation>
```

An unmapped guard is a projection defect, not a context optimization.

Generated entrypoints must derive common guard semantics from one canonical authoring source or be deterministically checked for semantic/source identity. Hand-maintained divergent guard copies are not acceptable architecture.

## Relationship to topology and reference candidates

This guard set is fixed input to later comparisons:

- `R0/R1/R2/R3` may change L2 grouping, not guard meaning;
- `B0/B1/F2/G3` may change activation/entrypoint boundaries, not Consumer guard meaning;
- a separate G3 Skill-trust entrypoint, if ever selected, must receive the subset of common guards required before its own routing/effects and may add stronger trust-specific early guards;
- Source Maintainer needs its own L1 specification; this document does not define it.

## D052 / evaluation hooks

Future conformance may test guard preservation through positive, negative, near-miss, mutation, collision, disclosure and missing-capability cases. Exact corpora, holdouts, repeated-trial method and thresholds remain MG1 authority after T022.

A test oracle may reference guard IDs without making this document protocol authority.

## RCAB rule

Guard compression is evaluated on complete load paths and behavior, not L1 byte count alone.

A candidate cannot claim context improvement if it moves a mandatory guard later, increases compensating fan-out, or causes wrong routing/retrieval.

## Acceptance invariants

1. every Consumer projection maps all `C-L1-G01..G09` guards;
2. semantic authority guards remain effective before unsafe routing/mutation;
3. no late L2/L3 rule is the sole protection for an early-risk boundary;
4. L2 may specialize but not contradict common guard semantics;
5. L4 deterministic enforcement is used where appropriate without encoding strategic authority;
6. Consumer/source-maintainer isolation and source independence remain intact;
7. current-work disclosure remains intact;
8. missing tooling is reported honestly;
9. external effects/secrets remain authority-bounded;
10. reference/Skill topology remains an empirical later decision;
11. no T023 corpus/threshold is defined here;
12. RCAB claims require measured load-path evidence.