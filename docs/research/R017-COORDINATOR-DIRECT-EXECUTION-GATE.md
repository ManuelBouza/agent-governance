# R017 — Coordinator Direct-Execution Gate Research

Research-ID: R017  
Research-State: COMPLETE  
Decision-State: DECIDED  
Opened: 2026-09-09  
Last-Reviewed: 2026-09-09  
Owner: ChatGPT Orchestrator  
Scope: source-product Executor coordinator direct-execution versus bounded-worker delegation; no Governance Core / consumer-protocol change  
Question: When should a Human-visible Executor coordinator act directly, and when must it delegate a bounded unit to a worker before any child compute routing is considered?  
Evaluation-Refs: R012/D065; R007/T054/T054-R1; D063  
Decision-Ref: `docs/decisions/D075-coordinator-direct-execution-gate.md`  
Supersedes: none  
Superseded-By: none

## Executive finding

Agent Governance already has most of the required semantics in D065: material delegation triggers, anti-triggers for small/serial work, root-context protection, independent verification and one-writer safety. The missing abstraction is an **explicit first routing gate** before worker role/model/effort selection:

```text
Does this bounded unit merit a worker?
    no  -> Coordinator direct microaction
    yes -> delegate bounded unit
            -> then select worker role / compute / context / permissions
```

The Human-visible coordinator is therefore not forbidden from execution. It may perform small technical microactions when delegation overhead would exceed the work. The coordinator must, however, avoid becoming the material worker by chaining many individually small actions into a substantive unit that should have been isolated.

This conclusion is a semantic clarification/refinement of D065, not a reversal of D041 process autonomy.

## Repository evidence

### D065 already supplies the semantic foundation

D065 requires delegation for applicable non-trivial Executor work when a material trigger applies and no anti-trigger dominates. Its triggers include read-heavy exploration, noisy evidence, independent verification, parallel bounded scopes, specialized capability and root-context protection. Its anti-triggers explicitly permit root-local work when the slice is small, straightforward, tightly serial, or more expensive to delegate than to perform directly.

That means Agent Governance already rejects both extremes:

- `every command => spawn worker`;
- `coordinator may do everything because delegation is optional`.

What D065 does not make explicit is that this decision occurs **before** adaptive worker compute routing and can produce a legitimate `Coordinator direct` execution target for microactions.

### R007 and T054 are a separate question

R007 established that current Codex can request heterogeneous child model/reasoning profiles and proposed minimum-sufficient compute with escalation. T054 then executed a matched-arm pilot but ended `NOT_QUALIFIED`:

- Luna/Low failed P1 first-attempt exactness;
- P2 was confounded by a shared task/oracle interpretation across both arms;
- P3 gave positive quality evidence for requested Terra/High;
- effective child profile/usage evidence was insufficient in that run.

D063 later qualified a bounded exact-child measurement surface, clearing the observability substrate blocker. The remaining R007 issue is therefore a **corrected successor evaluation**, not authority to adopt a global Luna/Terra/Sol routing table today.

The direct-execution gate and adaptive child compute routing must remain separate normative/evaluation claims.

## Current official OpenAI/Codex evidence

OpenAI's current Subagents documentation describes subagents as useful for complex work with meaningful parallelism, multi-step implementation, codebase exploration, testing, log analysis and other work whose intermediate output would pollute the main thread. It also states that each subagent consumes its own model/tool work and therefore increases token usage relative to comparable single-agent execution.

The same documentation recommends caution with parallel write-heavy flows because coordination and edit conflicts can outweigh the benefits. This supports a cost-aware gate rather than unconditional delegation.

Current Codex also supports built-in `worker` and `explorer` agents plus custom project/user agents. Child model and reasoning may be inherited or overridden, and official guidance maps more demanding tasks toward stronger models while using Terra/Luna-class workers for faster or narrower work. These are adapter capabilities, not provider-neutral correctness semantics.

OpenAI's current model guidance additionally recommends explicitly tuning subagent delegation behavior because a model may otherwise delegate less or more than the workflow intends. This reinforces the need for project instructions to define **when delegation is materially useful**, while leaving exact decomposition mechanics to the Executor.

## Correct semantic boundary

The coordinator should be defined as:

> The Human-visible coordinator retains task authority and may directly execute auxiliary technical microactions of low elaboration needed to coordinate, verify, classify or choose the next action. It must delegate a materially elaborated unit that is reasonably isolatable under D065 rather than becoming the default worker for that unit.

Direct execution is an efficiency optimization for small work, not an escape hatch from delegation.

## Decision dimensions

Do not use a rigid rule such as `more than two commands => worker`. The coordinator should classify the concrete unit using these semantic dimensions:

1. **Step depth** — one/few bounded operations versus a multi-step stateful sequence.
2. **Context volume** — one pointer/result versus multiple files/sources/logs or broad repository orientation.
3. **Reasoning/ambiguity** — deterministic lookup/check versus hypothesis formation, diagnosis, architecture understanding or substantive interpretation.
4. **Mutation/risk** — read-only/reversible bounded action versus material edits, irreversible effects, broad write scope or elevated operational risk.
5. **Root-context pollution** — compact structured evidence versus noisy logs, traces, repetitive output or large intermediate reasoning that would displace task authority/context.

These dimensions are not individually binary. The coordinator applies judgment to the bounded slice. A read-only investigation can still be material; a single low-risk write can still be small.

## Coordinator-direct microactions

Typical conforming examples include:

- `git status` / exact branch or HEAD lookup;
- verify one SHA/ref/commit relationship;
- check existence of one file/path;
- compute or verify one hash;
- run one deterministic narrow command;
- search for one exact string/symbol;
- read one compact handoff/result;
- inspect one worker status/metadata record;
- perform a brief administrative correction to coordinator-local state;
- decide the next action from an already structured result.

The list is illustrative, not exhaustive.

## Material worker units

Delegation should be favored/required under D065 when the bounded unit requires material elaboration, for example:

- multi-file or multi-source exploration;
- architecture/dependency understanding;
- bug diagnosis and hypothesis testing;
- implementation/refactoring;
- non-trivial patch preparation;
- extensive test execution plus interpretation;
- independent review/security/compatibility verification;
- significant log/trace analysis;
- comparison of technical alternatives;
- conflict resolution or stateful multi-step repair;
- any disposable work whose intermediate output would materially pollute the root context.

## Anti-evasion: microaction chaining

The main failure mode of a permissive direct gate is incremental scope creep:

```text
one small check
-> one more file
-> one more hypothesis
-> one small edit
-> one more test
-> coordinator has silently become the worker
```

Therefore the coordinator must re-evaluate the routing gate whenever the work expands beyond the originally bounded microaction. Several locally small actions that collectively form one material unit are classified as the material unit, not as independent exemptions.

## Two-stage routing architecture

The preferred provider-neutral architecture is:

```text
Stage A — execution target
    COORDINATOR_DIRECT
    DELEGATED
    CONTRACT_FIXED

Stage B — only when DELEGATED
    child role
    task class
    compute tier/model
    reasoning effort
    context fork
    permission/sandbox
    tools/skills/MCP
    escalation policy
```

D075 may adopt Stage A now because it clarifies already-accepted D065 semantics and does not depend on disputed model-performance claims.

Stage B adaptive compute mapping remains R007. It requires a corrected successor evaluation before any global mapping is accepted.

## Evaluation consequence

A future R007 successor should not simultaneously treat Stage A as an experimental variable. That would confound delegation-worthiness with child-compute quality.

Instead:

- D075 fixes Stage A semantics;
- T063 uses tasks that are already unambiguously eligible for delegation under D075/D065;
- T063 re-evaluates only the adaptive child execution profile against a root-equivalent control using D063-qualified measurement.

This preserves causal clarity.

## Decision disposition

R017 supports immediate source-product adoption of the direct-execution gate through D075 because:

- it narrows/clarifies existing D065 triggers and anti-triggers rather than introducing an untested model-quality claim;
- it reduces unnecessary worker overhead for trivial actions;
- it adds an anti-evasion rule against coordinator scope creep;
- it preserves Executor-owned concrete decomposition/mechanics under D041;
- it does not select child models, efforts or vendor-specific role graphs.

Adaptive child compute routing remains separately evidence-gated by R007/T063.

## Sources

### Canonical Agent Governance

- `docs/decisions/D065-semantic-executor-delegation-obligation.md`
- `docs/research/CODEX-COORDINATOR-DELEGATION-POLICY-RESEARCH.md` (R012)
- `docs/research/ADAPTIVE-SUBAGENT-COMPUTE-ROUTING-RESEARCH.md` (R007)
- `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md`
- `docs/reviews/T054-R1.md`
- `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md`

### Official OpenAI / Codex, revalidated 2026-09-09

- OpenAI, **Subagents**: `https://learn.chatgpt.com/docs/agent-configuration/subagents`
- OpenAI, **Model guidance**: `https://developers.openai.com/api/docs/guides/latest-model`
- OpenAI, **AGENTS.md project instructions**: `https://learn.chatgpt.com/docs/agent-configuration/agents-md`

Vendor-specific capabilities are volatile adapter facts and must be revalidated before later experimental execution or concrete model mapping.
