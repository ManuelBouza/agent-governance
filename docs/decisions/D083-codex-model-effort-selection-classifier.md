# D083 — Codex model and effort selection classifier

Status: ACCEPTED  
Date: 2026-09-17  
Authority: Human Owner / ChatGPT Orchestrator  
Research: `docs/research/R032-CODEX-MODEL-EFFORT-SELECTION.md`  
Refines: D055  
Preserves: D039, D041, D053, D054, D057, D060, D063, D065, D068, D075, D077, D080, D081  
Scope: Human-visible Codex Executor root model/reasoning selection only; no child-routing adoption and no change to Task Contract authority

## Problem

D055 already requires the Orchestrator to recommend the lowest-cost/lowest-effort Executor configuration that retains a reasonable quality margin. Its current Codex adapter correctly distinguishes Luna/Low, Terra/Low, Sol/Medium and Sol/High, but `Sol / Medium` remains the center-of-gravity default for ordinary implementation.

That default is safe, but it does not make explicit how the Orchestrator should recognize a task where semantic ambiguity has already been removed, technical branching is low, and deterministic verification makes a lower initial profile proportionate.

Without an explicit classifier, two errors remain possible:

- routine over-provisioning of highly deterministic, strongly verified work;
- unsafe downshifting based merely on apparent task size or token cost.

R032 establishes a conservative classifier that separates authority completeness from technical execution difficulty and treats model capability and reasoning effort as independent axes.

## Decision

D083 SHALL refine D055 with the following pre-launch classifier for the Human-visible Codex Executor root.

### Gate 0 — authority completeness

Before model/effort selection, persisted authority must be complete for the delegated work.

A missing or materially ambiguous requirement, Design, acceptance criterion, semantic oracle, scope boundary, branch authority, permission, or required input is a fail-closed re-entry condition.

```text
missing/ambiguous authority or required input
    -> STOP / Orchestrator re-entry
    -> do not compensate by raising model or reasoning effort
```

Higher model capability is never permission to resolve Orchestrator-owned semantic ambiguity.

### Gate 1 — classify execution determinism

Classify the remaining technical execution as:

```text
HIGH
  technical path is strongly constrained by frozen authority and known mechanics

MEDIUM
  bounded implementation choices remain, but the work is local/coherent

LOW
  a materially non-obvious technical path must be discovered or reconciled
```

Determinism concerns technical execution after specification is complete. It is not a proxy for business importance.

### Gate 2 — classify technical branching

Classify competing implementation/diagnostic paths as:

```text
LOW
  one obvious path or tightly bounded choice

MEDIUM
  several plausible local approaches or causes

HIGH
  multiple interacting hypotheses, non-local causes, architecture/history/security tradeoffs
```

This is solution branching, not Git branch count.

### Gate 3 — classify verification strength

Classify the available verifier/oracle as:

```text
STRONG
  deterministic tests/postconditions directly cover the relevant behavior and failures are attributable

MIXED
  useful automated evidence exists but material interpretation/integration review remains

WEAK
  sparse, flaky, indirect, expensive, environment-dependent, or judgment-heavy verification
```

Strong verification lowers the expected cost of a conservative downshift because insufficiency is exposed quickly and objectively. Weak verification raises the model/effort floor because false success is harder to detect.

### Gate 4 — apply concrete risk modifiers

Raise the floor when the work includes a concrete material modifier such as:

- security or fail-closed bypass risk;
- concurrency/ordering/race behavior;
- difficult portability/environment interaction;
- repository-history reconciliation where represented work could be lost;
- wide cross-subsystem blast radius;
- destructive/irreversible effects with weak observability;
- difficult diagnosis with several surviving root causes.

Task importance alone is not a risk modifier.

## Conservative Codex mapping

Use this as the current adapter mapping unless a Task Contract/evaluation freezes another profile:

| Work shape | Initial model | Effort |
| --- | --- | --- |
| Read-only/repetitive; high determinism; low branching; strong postcondition | GPT-5.6 Luna | Low |
| Narrow tracked mutation; high determinism; low branching; strong deterministic verification; bounded/reversible blast radius | GPT-5.6 Terra | Low |
| Bounded local implementation/refactor; high-to-medium determinism; low/medium branching; strong or mixed verification | GPT-5.6 Terra | Medium |
| Ordinary multi-file implementation/rework; medium branching or mixed verifier; no exceptional risk | GPT-5.6 Sol | Medium |
| High branching, weak verifier, non-local diagnosis, or serious risk modifier | GPT-5.6 Sol | High |
| Concrete evidence that Sol/High is capability-limited on the task | GPT-6 Astra or current stronger supported tier | Low/Medium initially |
| Exceptional long-horizon/bound-testing work with evidence that normal High is insufficient | strongest justified supported model | XHigh/Max/Ultra only when justified |

Luna is not adopted as a general implementation model. For ordinary tracked mutation, Terra remains the conservative economy floor unless a task class is separately qualified lower.

## Model and effort are independent axes

Do not treat provider model/effort combinations as one monotonic ladder.

When an execution is insufficient, classify the limiting factor:

```text
capability / abstraction / task breadth insufficient
    -> raise model class

model class sufficient but search/diagnosis/edge-case depth insufficient
    -> raise reasoning effort

missing authority/context/files/permissions/tooling state
    -> repair the missing input or re-enter; do not raise compute
```

The Orchestrator SHOULD escalate only the deficient axis unless concrete evidence justifies changing both.

## Expected-total-work objective

Optimization targets accepted-result cost, not cheapest first call.

Qualitatively:

```text
expected total work
  = initial execution
  + verification
  + probability of insufficiency * diagnosis/retry/rework/review churn
```

A low-tier retry cascade can cost more than one adequate Sol execution. Conversely, Sol/High on deterministic work with strong oracles can waste allowance without increasing accepted quality.

No fixed numerical retry probability, time budget, token threshold, or cost threshold is introduced.

## Ratcheting rule

D039 evidence-driven tuning remains controlling.

A repeated task class may be downshifted only when representative evidence shows the lower profile preserves the same verification/acceptance quality without material additional review or rework.

Upshift when failures are credibly attributable to model capability or technical reasoning depth rather than missing authority, stale state, broken tooling, unavailable permission, or inadequate specification.

Do not retry indefinitely at an insufficient tier.

## Boundaries

D083 does NOT:

- adopt the failed T063 frozen adaptive child-routing mapping;
- establish Luna/Terra as globally qualified replacements for Sol;
- change D065/D075 delegation semantics;
- change D053/D068 ownership or stage boundaries;
- alter Task Contract authority;
- make vendor model names repository correctness dependencies;
- authorize Astra as a default;
- make higher effort a substitute for missing authority;
- establish fixed token, runtime, cost, or message thresholds.

## T069 prospective application

T069 Stage 6 is a representative candidate for applying this classifier prospectively because its semantic authority is frozen, repair authority is narrow, verification is deterministic and comprehensive, and unexpected semantic conflict is a stop/re-entry condition rather than Executor-owned redesign.

Under this classifier, the initial profile would be:

```text
Model: GPT-5.6 Terra
Effort: Low
```

with escalation to Terra/Medium only for non-trivial in-contract diagnosis. A material semantic/authority conflict returns to the Orchestrator rather than escalating through Sol/High to cross the governance boundary.

This T069 application may occur only after the current T069 launch authority is revalidated.

## Acceptance record

Human acceptance was given explicitly on 2026-09-18 after R032 had been persisted and represented in `docs/RESEARCH-TRACEABILITY.md`.

Acceptance effects:

1. R032 transitions to `Decision-State: DECIDED` with D083 as its decision authority;
2. this decision refines D055 without replacing its minimum-sufficient-compute principle;
3. `docs/EXECUTOR-LAUNCH-PROFILES.md` must reflect this classifier;
4. any active launch frontier must still be revalidated against current Git authority before execution.

## Disposition

```text
Status: ACCEPTED
Research: R032 COMPLETE / DECIDED
Refines: D055
```
