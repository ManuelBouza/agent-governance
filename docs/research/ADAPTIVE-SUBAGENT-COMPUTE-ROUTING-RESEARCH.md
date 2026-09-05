# Adaptive Subagent Compute Routing Research

Status: RESEARCH / PROSPECTIVE  
Date: 2026-09-05  
Scope: source-product Executor orchestration; no current Governance Core change  
Related: D039, D041, D046, D055, T053

## Research question

Can Agent Governance improve Executor efficiency by selecting a subagent's model, reasoning effort and compatible launch-time parameters according to the bounded task assigned to that child, rather than routinely inheriting the coordinator root's compute profile?

The intended objective is **minimum sufficient compute for accepted quality**: preserve or improve technical quality while reducing avoidable token use, latency and cost on read-heavy, repetitive or mechanically bounded child work.

This research does **not** authorize changing T053 Phase 2, D055, Governance Core, or the current Executor launch profile. T053 must first converge under its already-frozen pilot design so that persistent-root continuity remains a clean experimental variable.

## Executive finding

Yes. Current Codex explicitly supports heterogeneous subagent compute profiles.

A spawned Codex child inherits the parent model and reasoning effort when no child-specific values are supplied, but Codex also supports child-specific selection through:

1. explicit values at spawn time;
2. `[agents]` defaults in Codex configuration;
3. custom-agent configuration files with their own model, reasoning, sandbox, MCP and Skill settings.

This means the T053 Phase-1 evidence does not imply that a Sol/High coordinator must pay Sol/High compute for every Explorer, Worker or Verifier. The host can route bounded child work to a lower-cost model/effort where quality evidence permits it.

The preferred Agent Governance direction is therefore **adaptive child execution profiles**, not uniform inheritance.

## What current Codex supports

### Inheritance and explicit overrides

OpenAI's current Subagents documentation states:

- if a subagent has no configured `model` or `model_reasoning_effort`, it inherits the creating agent's model and reasoning effort;
- an explicit spawn selection can choose a different child model and/or reasoning effort;
- `[agents].default_subagent_model` and `[agents].default_subagent_reasoning_effort` can establish defaults;
- custom-agent files can set `model` and `model_reasoning_effort` for a role;
- a model selected without an explicit effort uses that model's default effort.

The documented base resolution order is explicit spawn -> corresponding `[agents]` default -> parent. A selected custom-agent file is then a configuration layer: if that file defines `model` or `model_reasoning_effort`, its defined value wins for that field.

That precedence has an important design consequence: a role file that hard-codes a model can defeat task-by-task dynamic routing. For adaptive routing, static role definitions should normally describe capability/instructions/permissions while leaving model and effort unset unless the role intentionally requires a fixed compute floor.

### Spawn-time controls

The current OpenAI Codex source for Multi-Agent V2 exposes these relevant `spawn_agent` inputs when the active surface enables the corresponding metadata:

- `task_name`;
- `message`;
- `agent_type`;
- `fork_turns`;
- `model`;
- `reasoning_effort`;
- `service_tier`.

`fork_turns` can be `none`, `all`, or a positive number of recent turns. This gives the coordinator a second efficiency lever beyond model selection: a bounded specialist can receive only the conversation history it actually needs rather than cloning the full root history.

The Codex source also shows that availability/exposure of model, reasoning and service-tier overrides is runtime/surface dependent. Agent Governance must therefore treat these controls as adapter capabilities to detect, not as permanently guaranteed syntax.

### Permissions and tools are a separate dimension

OpenAI documents custom agents as configuration layers that may also define `sandbox_mode`, `mcp_servers` and `skills.config`. Omitted settings inherit from the parent, and live parent permission/sandbox choices can be reapplied to children.

Accordingly, an efficient child profile is broader than `model + effort`, but not every dimension is necessarily a direct `spawn_agent` argument. Agent Governance should distinguish:

- **spawn-time compute/context controls** — model, effort, history fork and, when exposed, service tier;
- **role/capability controls** — read/write posture, tools, MCP servers, Skills and standing instructions;
- **governance constraints** — authority, branch/worktree safety, one-writer policy, verification and acceptance.

The last category remains independent of model choice.

## Current OpenAI model guidance

OpenAI's Subagents documentation recommends different model classes for different child work:

- GPT-5.6 / Sol-class capability for demanding, ambiguous, multi-step work requiring planning, tools and validation;
- GPT-5.6 Terra for faster, lower-cost exploration, read-heavy analysis, large-file review and supporting parallel agents;
- GPT-5.6 Luna for narrow, clear, repetitive or high-volume work.

The same documentation recommends reasoning effort proportionally:

- `low` for simple work where speed is primary;
- `medium` as the balanced default;
- `high` for complex logic, assumption checking, edge cases, review or security work;
- `xhigh` / `max` / `ultra` only for especially demanding work on models/surfaces that support them.

OpenAI's GPT-5.6 builder guidance reinforces this direction. It reports that lower reasoning settings can improve price-performance and that smaller models can be especially effective for repeated agentic steps, extraction, code retrieval and other high-throughput workloads. One cited production example reports a code-exploration workload in a multi-agent engineering system using Luna with materially lower inference cost and latency while improving its measured F1.

OpenAI's general agent-building guidance gives the appropriate optimization method: establish quality with a capable baseline and evals first, then replace larger models with smaller ones where the acceptance target remains satisfied. Agent Governance should adopt that evidence-driven direction rather than assuming either the largest or the smallest model is correct a priori.

## External research and specialized guidance

The broader multi-agent literature supports heterogeneous routing rather than uniform model allocation.

### MasRouter — ACL 2025

MasRouter formalizes multi-agent-system routing across collaboration mode, agent role and LLM choice. Its published ACL results report lower overhead through customized routing while retaining or improving benchmark performance, including up to 52.07% overhead reduction against compared methods on HumanEval and 17.21%-28.17% reduction when used as a plug-in router.

The relevant principle for Agent Governance is not its specific learned router. It is that **role allocation and model allocation are coupled optimization decisions**.

### CASTER — 2026 preprint

CASTER targets the waste created by assigning a strong model uniformly to trivial and difficult sub-tasks. It uses context-aware task-difficulty signals to route work dynamically and reports up to 72.4% inference-cost reduction against strong-model baselines while matching success rates in its experiments.

The useful design lesson is progressive, task-difficulty-aware routing rather than a fixed global child model.

### SC-MAS — 2026 preprint

SC-MAS explicitly allocates different LLM backbones to individual agents while also varying collaboration structure. Its reported results show simultaneous accuracy improvements and cost reductions on MMLU and MBPP.

Again, Agent Governance does not need to adopt the research framework itself. The evidence supports the portability of **heterogeneous child models by role/task**.

### Duke Codex Starter Best Practices

Duke's current Codex guidance independently recommends subagents mainly for genuinely parallel/read-heavy work, warns that every child consumes additional tokens, and documents custom agents with task-specific model, reasoning, sandbox and tool configuration. This is consistent with the official OpenAI guidance and with T053's one-writer / bounded-child safety direction.

## Proposed Agent Governance abstraction

Do not make vendor model names normative. Introduce a provider-neutral **Child Execution Profile** selected per bounded child task.

Candidate shape:

```text
Child-Role: <Explorer | Worker | Verifier | specialized capability>
Task-Class: <bounded semantic class>
Compute-Tier: ECONOMY | BALANCED | FRONTIER
Reasoning: LOW | MEDIUM | HIGH | exceptional higher tier
Context-Fork: MINIMAL | RECENT_N | FULL
Capability: READ_ONLY | WRITE
Tool-Surface: <required tools/MCP/skills only>
Latency-Tier: DEFAULT | FAST only when justified/supported
Escalation: <conditions that permit/require promotion>
Expected-Return: <bounded result shape>
```

The active Executor adapter maps that abstract profile to concrete host settings. Model names remain operational mappings, just as D055 currently treats root model names.

### Candidate Codex mapping for a future pilot

This is a hypothesis to evaluate, not yet policy:

| Child task class | Initial Codex mapping | Reasoning | Context bias |
| --- | --- | --- | --- |
| deterministic inventory, grep/search, file/symbol map, repetitive evidence collection | GPT-5.6 Luna | Low | minimal/recent |
| broader code exploration, large-file analysis, documentation research | GPT-5.6 Luna or Terra | Medium | minimal/recent |
| normal bounded implementation or test correction | GPT-5.6 Terra | Medium | recent sufficient context |
| ordinary independent correctness/test review | GPT-5.6 Terra | High | delta + relevant authority |
| ambiguous cross-cutting implementation, subtle concurrency/portability, serious defect rework | GPT-5.6 Sol | High | task-appropriate |
| security/fail-closed review or unresolved multi-cause diagnosis | GPT-5.6 Sol | High, escalate only with evidence | task-appropriate |

The coordinator root may still justify Sol/High for an ASSURED, multi-phase task while most disposable children run below the root's compute level.

## Routing rule: minimum sufficient compute with escalation

A safe routing algorithm should optimize **downward only after quality is established**.

1. Classify the bounded child task by ambiguity, scope, write risk, verification risk and required tool depth.
2. Choose the lowest profile already validated for that class.
3. Keep the child prompt and context bounded; avoid full-history forks when repository authority plus the child task is sufficient.
4. Execute independent deterministic checks where available.
5. Escalate model and/or reasoning when concrete signals show the current profile is insufficient.
6. Never raise compute to compensate for missing Task Contract/Design/Plan authority; re-enter the Orchestrator instead.
7. Do not retry indefinitely at the same insufficient tier.

Candidate escalation signals include:

- unresolved ambiguity with multiple plausible technical interpretations inside otherwise complete authority;
- unexplained deterministic test failures after bounded diagnosis;
- non-local concurrency/order behavior;
- security or fail-closed bypass risk;
- a verifier finding whose root cause spans several subsystems;
- repeated low-tier child failure to produce required evidence;
- confidence/evidence insufficient for the requested independent review.

A child that only performs mechanical search should not inherit Sol/High merely because its parent root is handling a difficult task.

## Context routing is part of compute routing

Token efficiency is not only a model-selection problem.

Codex's `fork_turns` capability allows the root to limit copied conversational history. For fresh specialists, a future adapter should prefer the smallest safe fork:

- `none` when the bounded child message plus inherited repository/session instructions fully describe the job;
- a small recent-turn fork when the immediate technical exchange is material;
- `all` only when the child genuinely requires the root's full conversational trajectory.

This complements T053's existing rule to return concise child conclusions instead of ingesting full transcripts into the root.

## Telemetry required for a future adaptive-routing pilot

T053 Phase 1 exposed a measurement gap: it records child role/purpose/result but not model or reasoning effort. A future routing pilot should add, per child when the host exposes them:

```text
requested_profile
requested_model
requested_reasoning_effort
requested_fork_turns
requested_service_tier
resolved/effective_model
resolved/effective_reasoning_effort
resolved/effective_service_tier
profile_resolution_verified
input_tokens
cached_input_tokens
output_tokens
reasoning_tokens
total_tokens
latency/duration
result_status
verification_result
retry_or_escalation_reason
```

If the host does not expose an effective value, persist `null` plus an explicit availability reason. Do not infer that a requested override actually executed.

For an experiment whose claim is model-routing efficiency, an unverified effective profile cannot support a quantitative savings claim even if the technical task itself succeeds.

## Cost significance

As of this research date, OpenAI's ChatGPT Work/Codex token-based rate card shows a large spread between Sol, Terra and Luna. The exact prices are provider-operational data and must not become policy constants, but the ratio is sufficient to make routing material: a read-heavy child shifted from a frontier tier to a validated economy tier can reduce per-token cost by an order of magnitude or more.

This strengthens the case for routing, but cost alone is not the acceptance objective. The governing metric remains accepted quality adjusted for total compute, latency and rework.

## Interaction with existing Agent Governance decisions

### D041 — Executor process autonomy

Child orchestration remains Executor-internal implementation process. Agent Governance should not prescribe a provider-specific spawn syntax as correctness semantics.

A future policy may nevertheless define **material efficiency/observability constraints** such as minimum-sufficient compute, bounded context, one-writer safety, escalation rules and requested/effective-profile telemetry. The concrete Codex mapping remains an adapter implementation.

### D055 — root launch profile

D055 currently governs the Human-facing Executor root launch: Executor, NEW/CONTINUE session, model and effort. It already requires the lowest-cost/lowest-effort configuration that retains a reasonable quality margin.

The natural future refinement is to separate two layers:

```text
Human-visible Root Launch Profile
        -> Executor / session / root model / root effort

Executor-internal Child Execution Profile
        -> role / task class / model tier / reasoning / context / capability / escalation
```

This preserves D055's Human-facing purpose while extending the same proportional-compute principle inside a persistent coordinator.

### D039 — evidence-driven tuning

D039 should control promotion/demotion of task-class mappings. A cheaper child profile becomes preferred only after repeated evidence shows that it preserves acceptance quality and does not create offsetting rework.

## T053 boundary

Do **not** retrofit this routing model into T053 Phase 2.

T053 was deliberately frozen to test persistent-root continuity while keeping D055 unchanged. Its Task Contract also explicitly says not to add a project `.codex/agents/` catalog solely for the pilot. Changing child compute policy now would introduce a second experimental variable and weaken causal interpretation of the Phase-1/Phase-2 continuity evidence.

T053 Phase 2 should therefore continue exactly under O196. After final T053 convergence, the Orchestrator can use both:

- T053 evidence about persistent-root/subagent topology; and
- this research about task-adaptive child compute routing

to decide whether to specify a separate follow-up pilot and prospective D055/adaptor refinement.

## Recommended next design after T053

If T053 converges with adequate evidence for persistent-root coordination, specify a separate controlled pilot for **Adaptive Child Compute Routing**.

That pilot should compare at least:

- inherited/root-equivalent child profiles versus task-adaptive profiles;
- quality/verification/rework;
- time to useful result;
- child token/context use when exposed;
- total cost or normalized usage when measurable;
- escalation frequency;
- whether lower-tier children increase root workload or verifier findings.

The pilot should freeze task classes and acceptance before execution, use a deterministic or independently reviewed technical workload, and avoid changing persistent-root policy simultaneously.

Only after that evidence should Agent Governance revise D055 or portable consumer guidance.

## Sources

### Official OpenAI / Codex

- OpenAI, **Subagents**: https://learn.chatgpt.com/es-419/docs/agent-configuration/subagents
- OpenAI, **Configuration reference**: https://learn.chatgpt.com/es-419/docs/config-file/config-reference
- OpenAI, **Example configuration**: https://learn.chatgpt.com/es-419/docs/config-file/config-sample
- OpenAI, **The builder's guide to GPT-5.6**: https://openai.com/index/builders-guide-to-gpt-5-6/
- OpenAI, **A practical guide to building agents**: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
- OpenAI, **ChatGPT Work and Codex token-based rate card**: https://help.openai.com/en/articles/20001415
- OpenAI Codex source, `multi_agents_spec.rs`: https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_spec.rs
- OpenAI Codex source/tests, `multi_agents_spec_tests.rs`: https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_spec_tests.rs

### Specialized / research

- Yue et al., **MasRouter: Learning to Route LLMs for Multi-Agent Systems**, ACL 2025: https://aclanthology.org/2025.acl-long.757/
- Liu et al., **CASTER: Breaking the Cost-Performance Barrier in Multi-Agent Orchestration via Context-Aware Strategy for Task Efficient Routing**, 2026: https://arxiv.org/abs/2601.19793
- Zhao et al., **SC-MAS: Constructing Cost-Efficient Multi-Agent Systems with Edge-Level Heterogeneous Collaboration**, 2026: https://arxiv.org/abs/2601.09434
- Duke University, **Codex Starter Best Practices — Subagents**: https://codex-best-practices-d67bea.pages.oit.duke.edu/best-practices/subagents.html
