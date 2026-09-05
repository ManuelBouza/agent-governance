# R012 — Codex Coordinator Delegation Policy Research

Research-ID: R012  
Research-State: COMPLETE  
Decision-State: DEFERRED  
Opened: 2026-09-05  
Last-Reviewed: 2026-09-05  
Owner: ChatGPT Orchestrator  
Scope: source-maintenance Executor coordinator/subagent orchestration policy; no current Governance Core change  
Question: Should Agent Governance leave worker/subagent use entirely to Executor coordinator discretion, or define when delegation is required and how much of worker selection/orchestration should remain Executor-owned?  
Evaluation-Refs: `docs/research/CODEX-PERSISTENT-EXECUTOR-COORDINATOR-RESEARCH.md` (R006); `docs/tasks/T053-codex-persistent-executor-coordinator-pilot.md`; `docs/reviews/T053-R1.md`; `docs/research/ADAPTIVE-SUBAGENT-COMPUTE-ROUTING-RESEARCH.md` (R007); current Codex 0.153.4 and current official OpenAI subagent guidance  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Executive conclusion

Agent Governance should **not** keep the current delegation posture as pure coordinator discretion if the intended operating model is a real coordinator root with bounded workers.

The current D041 wording is permissive: the Executor *may* use workers/subagents. That correctly protects implementation-process autonomy, but it does not require Codex to behave as a coordinator. Current Codex explicitly distinguishes multi-agent modes in which proactive delegation is disabled unless the user or applicable `AGENTS.md`/Skill instructions request delegation. Therefore a Sol/Medium root can remain fully conforming while doing almost all work itself.

The opposite extreme is also undesirable. Agent Governance should **not** normally prescribe an exact worker graph, exact worker count, exact Codex role name, exact model, or step-by-step spawn/wait choreography. That would couple product correctness to one vendor scheduler, increase coordination overhead, and undermine D041/D054 process ownership.

The recommended design is a **semantic delegation obligation**:

```text
Agent Governance decides WHEN delegation is required or strongly preferred,
and defines safety/evidence boundaries.

Executor coordinator decides HOW to decompose eligible work,
how many children to use, which compatible worker/role to select,
and the concrete spawn/wait/close mechanics.
```

Exact topology remains contract-controlled only when topology itself is part of the experiment, safety invariant, independent-review requirement, or acceptance evidence.

This research recommends a prospective D060-style refinement after the currently running T057 has converged. It does not change T057, D041, D055, R007, or current child-routing policy during an active task.

## 1. Why the current permissive rule under-delegates

Current `AGENTS.md` says that inside Executor-owned stages 5-6 the Executor may independently choose direct work, private planning, workers/subagents, Skills and other implementation aids.

That rule establishes permission, not a coordination posture.

OpenAI's current Codex documentation states that local Codex delegates when:

- the user directly requests subagents/delegation/parallel work; or
- applicable `AGENTS.md` or Skill instructions request delegation.

Codex 0.153.4 source makes this distinction explicit through multi-agent mode instructions. The `ExplicitRequestOnly` mode says not to spawn subagents unless the user or applicable `AGENTS.md`/Skill instructions explicitly ask for subagents, delegation, or parallel agent work. The same 0.153.4 surface also contains a `Proactive` mode that encourages delegation when parallel work can save time or improve quality.

Therefore an Agent Governance rule that only says "you may delegate" cannot reliably produce coordinator behavior across modes, models, or versions.

### Consequence

If Agent Governance wants the Human-visible Executor root to be a coordinator rather than simply a powerful single-agent worker, the project must express a positive delegation policy in durable instructions. Raising the root model/effort merely to induce more proactive delegation is the wrong primary control.

## 2. OpenAI guidance supports steering, not rigid orchestration

OpenAI's current Subagents documentation recommends subagents for:

- complex work with meaningful parallelism;
- read-heavy codebase exploration;
- testing and log analysis that would pollute the main context;
- independent specialized analysis;
- bounded parallel work whose results can be summarized back to the main thread.

It also warns that every subagent performs its own model/tool work, so multi-agent runs consume more tokens than comparable single-agent runs. Parallel write-heavy work needs more caution because conflicts and coordination cost can increase.

OpenAI's GPT-5.6 builder guidance states that GPT-5.6 has a strong sense of the appropriate number of subagents and when to spawn them, but multi-agent behavior is highly steerable. Explicit instructions about when to invoke subagents can increase the likelihood that delegation happens only when the additional token expenditure should improve performance.

This supports a policy that defines **delegation triggers and constraints** while leaving the coordinator latitude inside those boundaries.

## 3. Manager/coordinator pattern fit

OpenAI's practical agent-building guidance distinguishes a manager pattern in which one central agent retains workflow control and uses specialized agents as tools. That pattern fits Agent Governance better than decentralized peer handoff because:

- one Human-visible root should retain task/worktree/handoff responsibility;
- Git/Task Contract authority must remain centralized and reconstructable;
- children are disposable implementation contexts;
- final synthesis and represented branch state remain with the coordinator root.

The root should therefore be a **manager/coordinator**, not merely another worker with access to `spawn_agent`.

## 4. Evidence from T053

T053 is the strongest existing project evidence because it explicitly required a coordinator topology.

Its Task Contract required:

- one Human-visible coordinator root;
- fresh Explorer children;
- a Worker child as primary writer;
- a fresh independent Verifier/Reviewer;
- bounded concurrency and one-writer safety;
- concise child result transfer and child closure.

T053 completed successfully. The final review recorded four fresh Phase-2 children, no Phase-1 child reuse, concise child conclusions, zero branch/worktree incidents, and positive qualitative context-locality evidence.

This proves that explicit delegation requirements are executable and compatible with Agent Governance authority boundaries.

It does **not** prove that the exact T053 Explorer/Worker/Verifier sequence should be mandatory for every task. T053 was an ASSURED pilot whose topology was itself an experimental variable.

## 5. T057 is not evidence of normal under-delegation

The currently running T057 should not be used as a normal coordinator benchmark.

T057 intentionally freezes:

- exactly one provider-backed parent;
- exactly one real child;
- one specific child purpose;
- one requested child model/reasoning profile;
- no compensating second provider-backed attempt.

The Human-visible Sol/Medium root is the experiment controller. It must perform version/schema/controller setup, parent lifecycle management, telemetry capture and exact child reattachment logic itself. Spawning additional explorer/verifier workers would introduce extra child activity and could invalidate the experimental design.

Therefore seeing substantial Sol/Medium root activity before the single T057 child is expected. If T057 never creates its exact required child, that would be a T057 failure; otherwise root-heavy controller work is conforming.

## 6. Why exact worker choreography should remain non-normative by default

A general rule such as:

```text
always spawn Explorer -> Worker -> Verifier
always use N children
always use model X for role Y
always wait in sequence Z
```

would create several problems.

### Vendor coupling

Codex built-in/custom roles, model names, spawn parameters and multi-agent modes are adapter surfaces that can change. Agent Governance should not make those names product-correctness semantics.

### Over-delegation

OpenAI explicitly warns that subagents increase total token consumption and that simple/straightforward tasks do not need a new agent.

### Cognitive locality

Tasks touching the same state, same files and serial decisions may be faster and more reliable in one context than after repeated worker orientation.

### Write coordination

Parallel writing creates conflicts and merge/synthesis overhead. D058 already requires workspace isolation across concurrently writable work units; within one work unit the same principle favors narrow writer ownership.

### Existing R007 boundary

R007 has not yet qualified a global adaptive child model/effort mapping. Therefore a new delegation policy should not prematurely hard-code Luna/Terra/Sol mappings as normative worker semantics.

## 7. Recommended semantic delegation gate

A future source-maintenance policy should require the coordinator to evaluate delegation before substantial implementation and again before final technical verification.

### Delegate when at least one material trigger applies

Candidate triggers:

1. **Independent read-heavy exploration** — codebase/API/dependency mapping can run independently and would otherwise consume substantial root context.
2. **Noisy execution** — tests, logs, traces, large command output or repetitive evidence collection can be isolated and summarized.
3. **Independent verification** — correctness/security/test-gap review materially benefits from a fresh reasoning path.
4. **Parallelizable bounded scopes** — two or more non-overlapping subtasks can run concurrently and save meaningful wall time.
5. **Specialized capability** — a narrower toolset/domain/context is materially better suited to a child.
6. **Root-context protection** — delegating disposable reasoning keeps requirements, constraints, decisions and synthesis clearer in the coordinator.

### Keep work in the root when a material anti-trigger applies

Candidate anti-triggers:

1. task is small and straightforward;
2. work is tightly serial and depends on one continuous mental model;
3. delegation would duplicate most orientation/context;
4. child coordination cost likely exceeds work saved;
5. mutable ownership overlaps and isolation would create more risk than benefit;
6. the root is acting as an exact experimental/controller state machine, as in T057;
7. persisted authority explicitly freezes a different topology.

### Coordinator accountability

For non-trivial STANDARD/ASSURED Executor work, the handoff should record a compact delegation decision:

```text
delegation_posture: DELEGATED | ROOT_LOCAL | CONTRACT_FIXED
material_triggers_considered: [...]
children_used: <count>
child_purposes: [...]
root_local_reason: <required when eligible work stayed local>
```

This makes systematic under-delegation observable without requiring private chain-of-thought or a full orchestration transcript.

## 8. Recommended ownership boundary

The prospective policy boundary should be:

### Agent Governance / Orchestrator owns

- whether a task class requires a delegation decision;
- semantic triggers/anti-triggers;
- safety constraints such as one-writer/worktree isolation;
- independent-review requirements when materially required by acceptance;
- bounded child return/evidence expectations;
- any exact topology needed because topology is itself experimental evidence.

### Executor coordinator owns

- concrete task decomposition;
- number of children within configured/safety bounds;
- built-in versus custom compatible child role;
- exact spawn/wait/follow-up/close mechanics;
- whether eligible independent tasks run sequentially or concurrently;
- concrete model/effort mapping only within separately accepted D055/R007 adapter guidance.

This preserves D041/D054 while turning "coordinator" into an actual behavioral role rather than a label.

## 9. Root compute implication

Do not solve under-delegation by automatically moving every coordinator to Ultra or another maximal reasoning mode.

Codex 0.153.4 contains explicit and proactive multi-agent mode semantics, and current OpenAI documentation confirms that project instructions can request delegation. A durable project-level delegation policy can therefore make Sol/Medium behave as a coordinator without making maximal compute the control plane.

Root compute should continue to follow D055 minimum-sufficient-compute logic. Worker compute remains a separate R007 question.

## 10. Proposed prospective policy shape

After T057 convergence, consider a D060-style policy with language equivalent to:

```text
The Human-visible Executor root is the coordinator for non-trivial governed execution.

Before substantial implementation/exploration and before final technical verification,
the coordinator MUST evaluate whether a bounded child should be used under the
accepted delegation triggers.

When a trigger applies and no anti-trigger/safety constraint dominates, the root
MUST delegate at least the eligible bounded slice instead of doing all work locally.

The coordinator retains discretion over concrete decomposition, child count,
compatible worker/role selection and execution mechanics unless the controlling
Task/Operational Contract makes topology itself authoritative.
```

A more prescriptive role graph should remain Task-Contract-specific rather than global.

## 11. Decision disposition

The research conclusion is stable:

```text
Pure optional delegation under D041 is insufficient for a desired coordinator-root architecture.
Exact global worker choreography is too prescriptive.
Recommended direction = semantic delegation obligation + Executor-owned concrete orchestration.
```

Normative adoption is deferred until the currently running T057 converges so that no active Task Contract is affected by a mid-run change in Executor process policy.

Reconsideration condition:

```text
After T057 terminal convergence, decide whether to adopt a D060 delegation-policy refinement
before the next normal non-experimental source-maintenance implementation task.
```

No T057 reroute, extra child, model change or prompt amendment is authorized by R012.

## Authoring incident

During R012 persistence, one Orchestrator file-create call accidentally targeted `develop` directly and created this research path with placeholder content at commit `2a2f34baa5e90724c46555c876aabe68309a8b99` before the intended topic branch was created.

Do not rewrite `develop` history to hide this incident. The corrective content and all further R012 Markdown authoring are performed through `docs/r012-coordinator-delegation-policy` and normal PR integration. The direct placeholder commit has no intended normative meaning.

## Primary sources

### OpenAI / Codex

- OpenAI, **Subagents**: https://learn.chatgpt.com/docs/agent-configuration/subagents
- OpenAI, **The builder's guide to GPT-5.6**: https://openai.com/index/builders-guide-to-gpt-5-6/
- OpenAI, **A practical guide to building agents**: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
- OpenAI Codex 0.153.4 source, `codex-rs/core/src/context/multi_agent_mode_instructions.rs`
- OpenAI Codex 0.153.4 source, `codex-rs/core/templates/collab/experimental_prompt.md`
- OpenAI Codex current source/tests for `spawn_agent` and multi-agent mode behavior

### Agent Governance evidence

- R006: `docs/research/CODEX-PERSISTENT-EXECUTOR-COORDINATOR-RESEARCH.md`
- T053: `docs/tasks/T053-codex-persistent-executor-coordinator-pilot.md`
- T053 final review: `docs/reviews/T053-R1.md`
- R007: `docs/research/ADAPTIVE-SUBAGENT-COMPUTE-ROUTING-RESEARCH.md`
- T057: `docs/tasks/T057-codex-read-only-child-requalification-v2.md` (used only to delimit why current root-heavy behavior is not a normal delegation benchmark)
