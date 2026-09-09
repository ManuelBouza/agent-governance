# D075 — Coordinator Direct-Execution Gate

Status: ACCEPTED  
Date: 2026-09-09  
Authority: Human Owner / ChatGPT Orchestrator  
Research: `docs/research/R017-COORDINATOR-DIRECT-EXECUTION-GATE.md` (`R017`)  
Scope: source-product Executor coordinator execution/delegation policy; no Governance Core / consumer-protocol change  
Refines: D041, D060, D065  
Preserves: D055, D058, D063, D068

## Decision

Before an Executor coordinator selects a child role, model, reasoning effort or other worker profile, it SHALL first decide whether the bounded unit of work merits a worker at all.

The provider-neutral execution-target gate is:

```text
bounded unit
    -> COORDINATOR_DIRECT
    -> DELEGATED
    -> CONTRACT_FIXED
```

`COORDINATOR_DIRECT` is valid for auxiliary technical microactions of low elaboration when delegating would cost more coordination/context than resolving the action directly.

`DELEGATED` is required when the bounded unit contains material elaboration and is reasonably isolatable under D065's delegation triggers without a dominating anti-trigger/safety constraint.

`CONTRACT_FIXED` applies when the controlling Task/Operational Contract makes topology material and explicitly fixes another execution topology.

The coordinator is therefore **not execution-incapable**. It must instead avoid becoming the default material worker for a unit that should be isolated in a child.

## Direct-execution purpose

Coordinator-direct execution exists to support coordination, verification, classification and next-action selection with minimal overhead.

Typical examples include:

- one exact `git status`, branch, ref or HEAD lookup;
- verifying one SHA/ancestor relationship;
- checking one file/path/ref exists;
- computing or verifying one hash;
- running one narrow deterministic command;
- searching for one exact symbol/string;
- reading one compact handoff/result;
- checking worker status/metadata;
- making a minimal administrative correction to coordinator-local state;
- deciding the next action from already structured evidence.

This list is illustrative rather than exhaustive. A command does not become coordinator-direct merely because it is one shell line; semantic scope controls.

## Material-work boundary

A unit should be delegated when it materially requires one or more of:

- multiple dependent steps with state that must be carried forward;
- broad/multi-file/multi-source context acquisition;
- substantive interpretation or hypothesis formation;
- architecture/dependency understanding;
- meaningful bug diagnosis;
- implementation/refactoring or a non-trivial patch;
- extensive test/log/trace execution plus interpretation;
- independent correctness/security/compatibility review;
- significant comparison of alternatives;
- specialized tools/context that are better isolated;
- noisy intermediate output whose retention would pollute the coordinator root.

Read-only is not automatically coordinator-direct. A multi-file investigation may be material even when it mutates nothing.

Mutation is not automatically delegated either. A truly minimal, low-risk administrative write may remain coordinator-direct if no other material trigger dominates and the controlling authority permits the effect.

## Decision dimensions

The coordinator evaluates the concrete bounded unit semantically rather than by a rigid command-count threshold. The primary dimensions are:

1. **Step depth** — isolated operation versus multi-step stateful work.
2. **Context volume** — compact pointer/result versus broad files/sources/logs.
3. **Reasoning/ambiguity** — deterministic verification versus substantial diagnosis/interpretation.
4. **Mutation/risk** — bounded reversible/read-only effect versus material writes/privilege/impact.
5. **Root-context pollution** — compact evidence versus noisy intermediate output/reasoning.

These dimensions refine D065's trigger/anti-trigger judgment; they do not replace it with a numeric scoring formula.

## No rigid threshold

Agent Governance SHALL NOT define a universal rule such as:

```text
more than N commands => delegate
writes => delegate
reads => root-local
```

Such rules misclassify both complex read-only exploration and trivial deterministic operations.

The decision is proportional and semantic.

## Anti-evasion: microaction chaining

Coordinator-direct execution MUST NOT be used to avoid delegation by decomposing one material unit into a sequence of nominally tiny steps.

The coordinator SHALL re-evaluate the gate whenever scope grows beyond the original microaction.

```text
small check
-> more context needed
-> hypothesis/implementation/extended validation emerges
=> stop treating the sequence as independent microactions
=> classify the material unit and delegate when D065 requires it
```

Several individually small actions that collectively implement, diagnose or validate one substantive unit are governed as that substantive unit.

## Relationship to D065

D065 remains the controlling semantic delegation obligation.

D075 makes explicit the routing order already implicit in D065:

```text
D075 Stage A:
    Does this bounded unit merit a worker?

D065:
    material trigger + no dominating anti-trigger
    => delegate eligible bounded slice

D041:
    Executor coordinator still owns HOW delegation is performed
```

D075 does not prescribe worker count, vendor role graph, sequencing, parallelism or spawn mechanics.

## Relationship to adaptive child compute routing

Worker compute routing is a second-stage decision and is not adopted by D075.

```text
Stage A — D075/D065
    COORDINATOR_DIRECT | DELEGATED | CONTRACT_FIXED

Stage B — only if DELEGATED
    role / task class / model tier / reasoning / context / permissions / tools / escalation
```

R007 adaptive subagent compute routing remains evidence-gated. T054 ended `NOT_QUALIFIED`; no global Luna/Terra/Sol mapping is currently normative.

A successor evaluation may qualify a future Stage-B mapping using D063's measurement boundary. D075 must not be cited as authority for a concrete child model or effort choice.

## Coordinator accountability

Whether direct work or delegation is used, the Human-visible coordinator retains D065 accountability for:

- controlling Task/Operational Contract authority;
- branch/worktree identity;
- child-result synthesis;
- represented repository state;
- technical Code Review & Verify completion;
- final handoff accuracy;
- stop/re-entry when upstream specification/Design/Plan authority is defective.

Direct execution does not widen authority, and delegation does not transfer lifecycle/governance authority to children.

## Evidence posture

D065's existing delegation receipt remains sufficient. D075 does not require a transcript of every coordinator microaction.

For applicable STANDARD/ASSURED work:

- `delegation_posture: DELEGATED` remains the normal receipt when material slices were delegated;
- `ROOT_LOCAL` remains valid when anti-triggers dominate the complete work unit, with a compact reason;
- `CONTRACT_FIXED` remains valid when topology is authoritative.

A coordinator may perform direct microactions while the overall posture is `DELEGATED`; those auxiliary actions do not need individual ledger entries unless another contract makes them material evidence.

## Applicability

D075 applies prospectively to source-product Executor coordination.

COMPACT/bounded operational work may remain coordinator-direct/root-local when small/serial anti-triggers dominate. STANDARD and ASSURED work continue to apply D065 delegation evaluation before substantial work and before final Code Review & Verify.

A Task Contract may impose a stronger topology when independence, safety, experimentation or reproducibility makes topology material.

## Effective rule

```text
microaction of low elaboration
AND delegation overhead dominates
AND no material trigger/risk requires isolation
=> Coordinator direct is conforming

material elaborated unit
AND reasonably isolatable
AND no dominating anti-trigger/safety constraint
=> delegate bounded worker slice

sequence of microactions grows into material work
=> reclassify; direct-execution exemption does not accumulate

child model/effort routing
=> separate Stage-B policy/evaluation, not decided here
```
