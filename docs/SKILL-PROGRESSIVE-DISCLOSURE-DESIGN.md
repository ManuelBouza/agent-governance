# Skill Progressive Disclosure Design Envelope

Status: DESIGN-APPROVED  
Decision context: D050, D051, D052  
Catalog: `docs/CAPABILITY-CATALOG.md`  
Baseline: `docs/CONSUMER-SKILL-CAPABILITY-BASELINE.md`

## Purpose

Define topology-neutral information-placement rules for future Agent Governance Skill projections.

This envelope decides **where information belongs**, not how many Skills will exist. It does not select B0/B1/F2/G3, edit Consumer v1, or pre-register T023 corpus/thresholds.

Core rule:

> Put information at the earliest layer that must know it, but no earlier.

Deferred material is safe only when it is not required to make an earlier activation, authority, routing or mutation decision.

## Disclosure layers

```text
L0  host Skill catalog / activation metadata
L1  activated entrypoint router
L2  focused capability reference
L3  installed Governance Core / normative authority
L4  deterministic engine/tooling
L5  current project/source state and evidence
```

Layers are information-placement boundaries, not products or authorities.

## Layer contract

| Layer | Owns | Must avoid |
| --- | --- | --- |
| `L0` | coherent positive intent, strong negative/near-miss boundary, entrypoint/product identity | protocol procedure, Core duplication, Skill-to-Skill correctness dependency |
| `L1` | universal entrypoint safety/authority guards + capability routing | capability-specific procedural bulk, duplicated Core semantics |
| `L2` | selected capability procedure, capability-specific negatives, command/tool mapping, next authority refs | universal safety duplication, topology-specific semantic forks |
| `L3` | normative Governance protocol semantics | generated Skill becoming competing authority |
| `L4` | machine-decidable checks/actions | Human/Strategy judgment encoded as deterministic output |
| `L5` | exact current state/evidence needed by active work | unrelated/future task or history preload |

## L1 mandatory-visibility rule

A rule MUST remain at L0/L1 when it is needed before a safe focused reference/tool can be selected or before risky mutation could occur.

For Consumer projections, likely mandatory L1 invariants include:

- installed repository/Core authority wins over Skill guidance;
- do not invent strategy, requirements, approval or acceptance;
- Consumer operation is source-independent;
- read-only/check behavior is default unless mutation is explicitly authorized;
- fail closed on unresolved authority/managed-state collision;
- do not expose future task contents for convenience;
- route to the smallest applicable capability;
- report missing deterministic capabilities honestly.

A rule may leave L1 only when an earlier host/product boundary or deterministic guard proves the same safety property before violation is possible.

## L2 capability references

Current catalog routes provide candidate focused boundaries:

```text
consumer.lifecycle.installation
consumer.lifecycle.state
consumer.lifecycle.execution
consumer.lifecycle.mission
consumer.lifecycle.coexistence
consumer.skill-trust.discovery/audit
```

These IDs do **not** require one reference file each. Closely coupled routes may share a reference when that produces a clearer/lower-load path.

L2 should contain only selected capability detail: procedure, specific near misses, deterministic command mapping, capability-specific mutation preconditions, missing-capability behavior, and pointers to the smallest relevant Core modules.

## Core/runtime placement

Keep normative protocol detail at L3 and machine-decidable enforcement at L4.

Examples:

- state/protocol -> `PROTOCOL`, `CONTEXT`, `LIFECYCLE` as routed;
- execution -> `HANDOFF`, `EXECUTION`, `EXECUTION-CONTROL` as needed;
- coexistence -> `COEXISTENCE`;
- Skill trust -> `SKILL-DISCOVERY`, `SKILL-SUPPLY-CHAIN`, optional `SECURITY`/`COEXISTENCE`;
- syntax/schema/transitions/order/digest/envelope/bootstrap mechanics -> deterministic engine/tooling.

Skill/reference prose explains when/why to use deterministic tooling; it does not reproduce the algorithm.

## Information-placement test

For each instruction/data item ask:

1. Needed to decide activation? -> `L0`.
2. Needed before safe routing/mutation? -> `L1`.
3. Specific to one selected capability? -> `L2`.
4. Normative protocol authority? -> `L3`.
5. Machine-decidable implementation/check? -> `L4`.
6. Current-instance evidence/state? -> `L5`.

If several apply, keep one authoritative location and only the smallest necessary early pointer/guard.

## Cross-cutting rule classes

- **Early mandatory guard:** stays L0/L1; e.g. activation boundary, authority ordering, no invented strategy, read-only/fail-closed default, source independence.
- **Deterministically enforced guard:** may be concise at L1/L2 when L4 reliably enforces it before mutation; e.g. exact digest/envelope mismatch.
- **Capability-local rule:** moves to L2; e.g. discovery ordering, archive procedure, coexistence classification detail.
- **Normative Core rule:** full semantics stay L3; Skill layers retain only necessary summary/pointer.

Do not remove the only early safety guard merely to deduplicate prose.

## Shared-source invariant

D050 requires common L0/L1 semantics across generated entrypoints to come from one capability/authoring source or be deterministically validated for equivalence.

Multiple entrypoints MUST NOT create independently editable copies of authority ordering, profile semantics, common safety constraints, deterministic command semantics or distribution identity/version.

## Candidate-topology constraints

- **B0:** broad unified L0/L1 must prove acceptable activation/context/profile isolation.
- **B1:** thin L1 should keep universal safety/routing and defer capability detail to L2 without loading every reference on every task.
- **F2:** Consumer and Source Maintainer may have separate L0/L1 surfaces while sharing Core/runtime/capability authority.
- **G3:** `consumer.skill-trust` may gain its own L0/L1 only if measured benefit justifies extra activation/catalog overhead.

All candidates must preserve the same accepted capability semantics for compared work.

## Consumer v1 baseline relation

Current Consumer v1 is structurally:

```text
one 8.9 KB Skill-local SKILL.md
    -> focused installed Core modules after activation
    -> shared deterministic CLI/runtime
```

The future hypothesis is whether capability-specific Skill-local prose can move from L1 to L2 while preserving behavior. This envelope does not authorize modifying Consumer v1 before the applicable future gate.

## D051 constraint

Focused references are product payload, not supplemental user installs.

Whatever topology wins, one Agent Governance distribution installation contains the selected entrypoint(s), references, shared engine/Core payload and required assets.

Progressive disclosure changes **what is loaded**, not what the user must manually assemble.

## D052 / MG1 hooks

Future conformance may verify:

- L0 positive/negative/near-miss activation;
- correct L1 capability route;
- no unnecessary L2 loads;
- cross-profile/cross-capability contamination;
- mandatory early guard preservation;
- deterministic guard before mutation;
- current-state-only disclosure;
- semantic equivalence across candidate projections.

Actual cases and thresholds remain MG1 authority after T022.

## RCAB measurement

Do not infer savings from file count or LOC.

Later comparisons should measure the complete task load path, including:

- L0 metadata;
- L1 router body;
- L2 references actually loaded;
- L3 Core modules actually loaded;
- L5 state/evidence;
- retrieval fan-out/navigation depth;
- duplicated content across projections;
- task success and wrong/extra routing.

## Anti-patterns

Do not:

- create one reference/Skill per CLI command or source file;
- hide pre-routing safety behind a late reference;
- duplicate Core semantics into every reference;
- require every L2 reference on every activation;
- require Skill-to-Skill invocation for portable correctness;
- hand-maintain divergent common safety text across generated entrypoints;
- confuse reference decomposition with extra user installation steps;
- claim a thinner entrypoint saves context without load-path evidence;
- change capability semantics to make a topology score better.

## Acceptance invariants

1. L0 is sufficient for activation/negative routing.
2. L1 preserves all required pre-routing/pre-mutation guards not enforced earlier.
3. L2 contains selected capability detail and points onward instead of duplicating Core.
4. L3 remains normative authority.
5. L4 owns appropriate machine-decidable enforcement.
6. L5 remains current-work scoped.
7. all generated candidates share one capability/Core/runtime/product authority.
8. Consumer/source-maintainer isolation remains intact.
9. D051 one-install semantics survive decomposition.
10. D052 verifies placement/routing without becoming authority.
11. RCAB evaluates actual load paths.
12. final topology remains MG1/T023 authority.
