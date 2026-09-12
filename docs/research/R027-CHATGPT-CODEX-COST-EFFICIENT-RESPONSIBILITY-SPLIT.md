# R027 — ChatGPT + Codex cost-efficient responsibility split

Research-ID: R027  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-12  
Last-Reviewed: 2026-09-12  
Owner: ChatGPT Orchestrator  
Repository-Baseline: `develop@55aa9c7ae0975ebb24b3047bfcba342110b335ab`  
Scope: optimize the ChatGPT Orchestrator + Codex Executor boundary for lower Codex token/credit consumption while moving repository-local work to the surface best suited to perform it  
Question: What responsibility split, context strategy, model/effort/speed policy, delegation rule, and validation loop should Agent Governance use so ChatGPT and Codex complement each other without duplicating work or spending premium Codex compute unnecessarily?  
Evaluation-Refs: D053; D054; D055; D057; D060; D065; D068; D075; D076; R007; R012; R017; R018; current OpenAI documentation and rate card; external empirical studies listed below  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Executive conclusion

The cost-efficient target is **not** “keep implementation in ChatGPT so Codex only verifies.” That minimizes one class of Codex work but forces ChatGPT to perform repository-local engineering and can make Codex reconstruct, execute, diagnose and repair code it did not create.

The stronger division of comparative advantage is:

```text
ChatGPT Orchestrator
  intent / current external research / scope / product semantics
  -> Specification / Design / Plan / acceptance criteria
  -> normative governance Markdown and semantic oracles
  -> final semantic review / integration decision

Codex Executor
  repository-local exploration
  -> implementation / refactor / implementation-coupled tests and tooling
  -> commands / reproduction / diagnosis / repair
  -> smallest-sufficient verification -> broader gates when justified
  -> concise evidence handoff
```

The optimization objective should be **Codex credits and tokens per accepted work unit**, not raw Codex token count in isolation. Moving appropriate implementation work from ChatGPT to Codex can increase the number of tasks Codex performs while still reducing duplicated context, expensive-model usage, retries and total engineering effort.

The current evidence supports several immediate candidate changes, but the exact normal-work model routing and the D068 ownership change require prospective Agent Governance evaluation before normative adoption.

## Current Agent Governance boundary

The current source-maintenance model contains useful separation but places unusually broad implementation ownership on ChatGPT:

- D054 correctly leaves CLI/API/SDK/shell/browser mechanics to the Executor while ChatGPT owns semantic intent, design and risk bounds.
- D055 selects Codex model/effort by work class.
- D060 keeps one Codex coordinator root through an exact work unit, limiting repeated reorientation.
- D065/D075 separate coordinator-direct microactions from materially delegated work.
- D068 currently makes ChatGPT responsible for complete Stage 5 candidate materialization across source code, tests, configs, schemas and scripts; Codex then owns Stage 6 execution, diagnosis, bounded repair and verification.
- D076 prevents Stage 6 from quietly becoming a second implementation stage through substantial ephemeral materialization.

D068 was rational when the dominant concern was eliminating repeated intent-to-implementation translation. R027 finds that the current vendor surface and cost model expose an opposite inefficiency: ChatGPT may create repository-local implementation that Codex must later rediscover and operationally validate anyway.

This is a **boundary optimization question**, not evidence that D068 was invalid for its original circumstances. Frozen scientific candidates, exact-byte experiments, semantic oracles and other cases where authorship itself is part of the experimental/control boundary remain materially different from ordinary source maintenance.

## Official product boundary

Current OpenAI product guidance draws a clear surface distinction:

```text
Chat
  questions / search / brainstorming / lightweight conversational work

ChatGPT Work
  research / multi-source analysis / larger deliverables

Codex
  code / codebases / developer tools / debugging / tests / commands / review
```

OpenAI's Codex prompting guidance says to use Codex when the work involves code, a codebase, or developer tools, and recommends giving it the desired behavior, relevant code or reproduction, constraints and verification target rather than duplicating broad context.

OpenAI's February 2026 Harness Engineering report is stronger: its operating principle is “Humans steer. Agents execute.” In that experiment Codex authored application code, tests, CI, tooling, documentation and evaluation harnesses while humans primarily specified intent, acceptance criteria and feedback loops.

R027 does **not** copy that experiment wholesale into Agent Governance. Agent Governance deliberately retains stronger governance, provenance and semantic-authority boundaries. The relevant lesson is narrower: repository-local technical materialization is a native Codex strength and should not remain with ChatGPT merely because ChatGPT can produce files.

## Finding 1 — regular Chat is economically useful as the semantic control plane

Current OpenAI Help states that Codex, ChatGPT Work, ChatGPT for Excel and Workspace Agents share the agentic allowance/credit pool where applicable, while regular Chat usage is not included in the Work/Codex credit history.

Therefore moving research, specification, design reasoning and acceptance work into ordinary Chat is not merely a role-quality choice; it also protects the Codex/agentic pool where that accounting applies.

Durable implication:

```text
Do not spend Codex context on work that does not need repository/tool execution.
Do not spend ChatGPT effort on repository-local mechanics Codex can inspect and execute directly.
```

## Finding 2 — the current root AGENTS.md is already over Codex's default instruction budget

At the reviewed `develop` baseline, root `AGENTS.md` is **34,567 bytes**.

Current Codex documentation states that project instruction files are concatenated from repository root toward the working directory and stop at `project_doc_max_bytes`, **32 KiB by default**.

Therefore:

```text
current root AGENTS.md     34,567 bytes
default Codex budget       32,768 bytes
excess                      1,799 bytes (~5.5%)
```

Unless the active Codex profile explicitly raises the limit, the root file alone exceeds the documented default combined instruction budget before a nested override can add more guidance.

This is a concrete efficiency and correctness defect. It creates truncation/omission risk and spends scarce context on instructions before task/code context is loaded.

OpenAI's own Harness Engineering report describes the same failure mode: a large monolithic `AGENTS.md` crowded out task/code context and became stale/hard to verify. Their successful pattern was a short `AGENTS.md` used primarily as a map into structured repository documentation, with progressive disclosure.

### Candidate correction

Do **not** solve this only by raising `project_doc_max_bytes`.

Prefer:

```text
root AGENTS.md
  compact invariants + routing map + authoritative pointers

nested AGENTS.md / AGENTS.override.md
  only scope-specific non-inferable rules

canonical docs
  detailed policy / rationale / runbooks / decisions

CI / executable checks
  mechanically enforceable invariants
```

A project-specific byte/line target should be measured rather than copied as doctrine. OpenAI's approximately-100-line example is useful directional evidence, not a universal threshold.

## Finding 3 — AGENTS.md quality matters more than AGENTS.md volume

The external evidence is intentionally mixed:

- Lulla et al. (2026), 10 repositories / 124 pull requests, found AGENTS.md presence associated with **28.64% lower median runtime** and **16.58% lower output-token consumption**, with comparable task completion behavior.
- Gloaguen et al. (2026), across multiple coding agents/models and both generated/developer-provided context files, found repository context files did **not generally improve task success** and increased inference cost by **over 20%**; they conclude human-written files should contain only minimal requirements.

These findings are not contradictory enough to justify either “always add more instructions” or “remove AGENTS.md.” They support a narrower rule:

> Persist only high-value, non-inferable, stable instructions that prevent expensive rediscovery or unsafe behavior. Use pointers and mechanical enforcement for the rest.

For Agent Governance, this strengthens the case for slimming the root `AGENTS.md` while preserving strict governance invariants.

## Finding 4 — subagents are not a token-saving primitive by default

Current OpenAI Codex documentation explicitly states:

> because each subagent performs its own model and tool work, subagent workflows consume more tokens than comparable single-agent runs.

OpenAI recommends parallel agents first for independent/read-heavy work such as exploration, tests, triage and summarization, while warning that parallel write-heavy workflows can create conflicts and coordination overhead.

The same documentation allows each child to use a different model/reasoning profile and recommends Terra for efficient exploration/read-heavy support and Luna for narrow, repeatable, high-volume work.

Therefore D065/D075 should not interpret “delegatable” as “cheaper when delegated.” The decision needs an explicit **delegation ROI gate**.

Candidate rule:

```text
Delegate only when at least one material benefit justifies duplicated agent context/tool work:

- independent parallelism materially reduces wall-clock time;
- noisy exploration/log/test output would pollute an expensive root context;
- a cheaper specialist can replace expensive root tool work;
- independent review materially improves correctness;
- context isolation is necessary for quality/safety.

Otherwise prefer one agent for serial write-heavy implementation.
```

This is a refinement of D065's existing anti-trigger (“coordination cost greater than the benefit”), not a rejection of semantic delegation.

## Finding 5 — smaller Codex models create large per-token savings, but only successful-task economics matter

The reviewed Codex credit rate card reports, per 1M tokens:

| Model | Input credits | Cached-input credits | Output credits | Same-token cost vs Sol |
| --- | ---: | ---: | ---: | ---: |
| GPT-5.6 Sol | 125 | 12.5 | 750 | 100% |
| GPT-5.6 Terra | 50 | 5 | 300 | 40% |
| GPT-5.6 Luna | 5 | 0.5 | 30 | 4% |

For the **same token counts**, Terra consumes 60% fewer credits than Sol and Luna consumes 96% fewer credits than Sol.

This does **not** mean every Sol task should be moved down. A cheaper model that needs more turns, more context, or rework may cost more per accepted result. R007/T054/T063 already demonstrate why Agent Governance must not adopt an unqualified global adaptive routing policy from theoretical cost ratios.

### Candidate compute ladder for evaluation

The current D055 guidance makes Sol/Medium the center of gravity for ordinary implementation. R027 recommends evaluating a cheaper default candidate rather than changing it immediately:

```text
Luna / Low
  deterministic status/read/search
  narrow repetitive inspection
  bounded log/result summarization
  simple high-volume read-only child work

Terra / Low
  narrow mechanical edits
  tightly specified config/test synchronization
  simple fixes with strong deterministic checks

Terra / Medium  <-- candidate default to evaluate for normal bounded implementation
  ordinary multi-file source maintenance with complete Spec/Design/Plan
  normal implementation-coupled tests and documentation

Sol / Medium
  escalation for ambiguity, difficult diagnosis, cross-cutting architectural work,
  or failure of the cheaper profile under the same acceptance contract

Sol / High
  selective high-risk/security/concurrency/fail-closed work

XHigh / Max / Ultra
  exceptional only
```

The `Terra / Medium` line is an **R027 hypothesis**, not adopted policy. It requires prospective comparison against the current Sol/Medium baseline using accepted-task quality, credits/tokens, retries and rework.

## Finding 6 — Standard speed should be the default economic mode

Current Codex speed documentation states that for GPT-5.6, Fast mode provides approximately **1.5x speed** while consuming credits at **2.5x the Standard rate**.

For a task whose token behavior is otherwise comparable, Standard therefore uses 40% of the Fast-mode credits (a 60% credit reduction) in exchange for higher latency.

The current Agent Governance launch card records Executor, session, model and effort but not speed. This leaves an economically material control implicit, and OpenAI documents that managed workspaces can start with Fast enabled by default.

Candidate D055 refinement:

```text
Speed: STANDARD   # normal default
Speed: FAST       # only explicit wall-clock-critical exception with rationale
```

This change is low-risk conceptually, but the exact active host/account setting should still be observed rather than assumed.

## Finding 7 — reasoning and verification should escalate progressively

OpenAI documentation states that higher reasoning effort increases response time and token usage. Current model guidance also recommends calibrating tests so small changes do not trigger unnecessarily broad or repeated validation.

Codex prompting guidance for bug fixing recommends re-running the reproduction and then the **smallest relevant test suite**.

Candidate execution ladder:

```text
1. execute the minimum sufficient reasoning profile for the work class
2. reproduce / implement
3. run the smallest relevant deterministic check
4. broaden only when scope, failure, risk, or a required repository gate justifies it
5. escalate model/effort only after concrete uncertainty/failure evidence
6. do not repeat already-passing broad checks after a no-op/non-impacting change
```

Required repository-wide gates still run when policy requires them. The optimization is against unnecessary repetition, not against verification.

## Finding 8 — specialized cheap children can protect an expensive root context

Two external results support a narrow specialization pattern:

- Microsoft Research's Terminus-4B reports up to approximately **30% lower main-agent token usage** for terminal-heavy software-engineering workloads without benchmark performance loss by offloading noisy terminal execution to a small specialized subagent.
- FastContext reports up to approximately **60% lower coding-agent token consumption** and up to 5.5 points better end-to-end resolution by separating repository exploration into a compact specialized explorer that returns focused file/line evidence.

These are not direct Agent Governance qualification results and do not override OpenAI's warning that subagents increase total tokens versus comparable single-agent execution.

The durable implication is narrower:

> If a child is used, make it materially cheaper and sharply specialized, and return compact evidence instead of raw exploration history.

This supports Luna/Terra read-only explorer/test/log roles, not indiscriminate multi-agent parallelism.

## Finding 9 — current minimal transport prompts are already directionally correct

`docs/EXECUTOR-LAUNCH-PROFILES.md` already says the Human-facing launch prompt should point Codex to current Git authority and the persisted Task Contract instead of copying:

- task requirements already in Git;
- implementation instructions;
- commands;
- review/gate excerpts;
- remembered HEADs as authority;
- model/session data already present in the launch card.

R027 retains this design.

The improvement is upstream: make the persisted authority itself compact and delta-oriented, and ensure `AGENTS.md` is a routing map rather than a policy encyclopedia.

## Finding 10 — D068 should become an explicit mode, not the universal normal path

For ordinary source maintenance, R027's preferred candidate lifecycle is:

```text
Stage 1-4 — ChatGPT Orchestrator
  Research / Spec / Design / Plan
  exact acceptance criteria
  semantic oracle when needed
  persisted Task Contract

Stage 5 — Codex Executor
  repository-local exploration
  technical materialization
  implementation-coupled tests/config/tooling
  local verification
  concise represented handoff

Stage 6 — Codex Executor continuation
  diagnosis / bounded repair / required broader verification

Stage 7 — ChatGPT Orchestrator
  semantic acceptance / review / integration decision / governance closeout
```

However Agent Governance also has cases where exact pre-execution candidate bytes are part of the scientific/control boundary. For those, current D068-style Orchestrator materialization can remain correct.

The candidate protocol should therefore distinguish modes explicitly, for example:

```text
EXECUTOR_MATERIALIZED
  normal source-maintenance default candidate

ORCHESTRATOR_FROZEN_CANDIDATE
  exact-byte scientific candidate
  semantic oracle or governance-owned executable fixture
  other explicitly justified control-boundary case
```

There must still be one owner per stage. R027 does not propose dual-owned implementation.

This is the largest proposed boundary change and requires a new decision plus empirical qualification before adoption.

## Finding 11 — Markdown ownership is currently broader than necessary

Current repository policy assigns every committed Markdown file to ChatGPT. That is appropriate for normative governance material, but it also keeps implementation-coupled technical documentation away from the code executor even when Codex changed the corresponding implementation.

OpenAI's current Codex guidance explicitly includes documentation updates as a Codex workflow, and the Harness Engineering report had Codex author code, tests, CI, tooling and documentation.

Candidate ownership refinement for evaluation:

```text
ChatGPT-only normative Markdown
  AGENTS.md
  Spec / Design / Plan
  Task Contracts
  decisions
  research
  reviews
  checkpoints
  governance policy / semantic authority

Codex-eligible technical Markdown
  implementation-coupled README sections
  API/developer documentation
  non-normative runbook changes
  generated/reference technical docs
```

Codex-authored technical Markdown would remain subject to the same task scope, review and acceptance gates. This change is not adopted by R027.

## Target topology

The efficient normal topology is intentionally small:

```text
1 ChatGPT Orchestrator context
  semantic authority + external/current research + acceptance

1 Codex coordinator root per Task/Operational Contract
  repo-local implementation + execution state

0..N bounded children
  only when delegation ROI is positive
  preferably cheaper read-only/noisy-output specialists
```

Avoid creating a second Human-visible Codex root merely for fresh reasoning; D060's existing same-task continuity rule remains sound.

## Context budget policy

The proposed context discipline is:

```text
ChatGPT -> Codex
  branch/work-unit identity
  one persisted authority path
  minimal task-specific pointers/repro only when not already in authority

Codex root context
  active constraints
  relevant file/symbol findings
  current phase
  test outcomes
  unresolved blockers

Exclude by default
  raw logs after distilled result exists
  full file dumps
  repeated policy text
  old failed implementation traces
  copied research prose
  complete child transcripts
```

Compaction can be used for execution hygiene, but Git/persisted authority remains the correctness source.

## Output-budget policy

The current Codex rate card charges output tokens materially more than input tokens for Sol/Terra/Luna. Therefore Executor handoffs should default to compact structured evidence:

```text
status
branch / represented commit
changed paths
verification commands + PASS/FAIL summary
material findings/blockers
remaining uncertainty
```

Do not return raw command transcripts unless the Task Contract requires exact evidence.

## Measurement objective

Raw token minimization is insufficient. The project should measure:

```text
primary
  Codex credits per accepted work unit
  Codex total tokens per accepted work unit
  accepted on first implementation attempt

secondary
  uncached input tokens
  cached input tokens
  output/reasoning tokens
  root vs child usage where observable
  number of model/effort escalations
  rework turns
  verification repetitions
  wall-clock duration

quality guardrails
  acceptance correctness
  regressions
  review defects
  rollback/reopen rate
```

A cheaper model that increases retries is not cheaper. A subagent that reduces root tokens but increases total credits without quality/latency benefit is not an efficiency win.

OpenAI's current usage surfaces can group Work/Codex history by model, reasoning, speed and token class where available; those observations should be used for operational feedback, not as a substitute for prospective controlled evaluation.

## Proposed improvement set

### Priority 0 — correctness and immediate waste removal

1. **Slim root `AGENTS.md` below the default combined Codex instruction budget** and make it a routing map with progressive disclosure. Do not merely increase the cap.
2. **Add `Speed` to the D055 launch card** and make `STANDARD` the normal candidate default; Fast requires an explicit latency rationale.
3. **Add a delegation-ROI rule to D065/D075** so subagents are not spawned merely because work is separable.
4. **Make verification progressive**, starting with the smallest relevant checks and broadening only under explicit risk/gate conditions.

### Priority 1 — boundary and compute qualification

5. **Evaluate `EXECUTOR_MATERIALIZED` as the normal source-maintenance mode**, retaining D068-style `ORCHESTRATOR_FROZEN_CANDIDATE` for exact-byte/control-boundary cases.
6. **Evaluate Terra/Medium as the normal bounded-implementation candidate** against current Sol/Medium, with Luna/Terra specialists for narrow read-heavy work and Sol as escalation.
7. **Evaluate narrower Markdown ownership**, retaining normative governance Markdown with ChatGPT while allowing implementation-coupled technical docs to travel with Codex-owned code changes.

### Priority 2 — operational feedback

8. **Add per-work-unit efficiency evidence** to Executor handoffs: model, effort, speed, child count, tokens/credits when exposed, retries and verification scope.
9. **Review efficiency periodically by accepted work class**, not by global token averages.
10. **Promote repeated workflow knowledge into compact repo-local skills or mechanical checks** instead of repeated prompt prose when the behavior is stable and enforceable.

## Proposed normal routing matrix

This matrix is a research recommendation, not current policy:

| Work | Primary surface | Candidate compute | Reason |
| --- | --- | --- | --- |
| External/current research, requirements, trade-offs | ChatGPT | current Chat reasoning appropriate to risk | avoids Codex agentic pool and does not need repo execution |
| Spec/Design/Plan, acceptance, normative governance | ChatGPT | current Chat reasoning appropriate to risk | semantic authority and policy ownership |
| Repo discovery/call graph/technical localization | Codex | Terra Medium root or Terra/Luna bounded explorer | direct repository access; avoids ChatGPT copying code context |
| Narrow deterministic repo observation | Codex | Luna Low | very low per-token credit rate; bounded outcome |
| Mechanical patch/config/test sync | Codex | Terra Low | cheaper technical execution with deterministic verification |
| Normal bounded implementation | Codex | Terra Medium **candidate for evaluation** | strong cost differential; complete upstream contract should reduce ambiguity |
| Difficult ambiguous implementation/diagnosis | Codex | Sol Medium | escalation where deeper capability can reduce rework |
| Security/concurrency/fail-closed high risk | Codex | Sol High | selective high-reasoning case |
| Noisy logs/tests/parallel read-only analysis | Codex child | Luna/Terra Low/Medium when ROI-positive | protects root context; child returns distilled evidence |
| Write-heavy serial implementation | Codex root | normally single-agent | avoids subagent token/coordination multiplier |
| Final semantic acceptance/integration | ChatGPT | current Chat reasoning appropriate to risk | separates implementation from acceptance authority |

## Expected economic effects

R027 can support exact **rate** comparisons but not a guaranteed project-wide savings percentage before evaluation.

The defensible directional effects are:

- removing over-budget/bloated instruction context reduces mandatory prompt load and truncation risk;
- Standard speed avoids the 2.5x GPT-5.6 Fast credit multiplier when latency is not critical;
- same-token Terra work is 60% cheaper in Codex credits than Sol; Luna is 96% cheaper than Sol;
- fewer unnecessary subagents avoids an officially documented total-token multiplier;
- repo-local implementation by Codex can eliminate ChatGPT-to-Codex implementation reconstruction, but its net Codex-token effect must be measured;
- progressive verification reduces repeated broad test/tool work where no risk/gate requires it.

A project-wide claim such as “R027 saves X%” is **not qualified** by this research.

## Required evaluation before normative adoption

A successor evaluation should compare matched ordinary source-maintenance work under at least:

```text
CONTROL
  current boundary
  ChatGPT Stage 5 materialization
  Codex Sol/Medium verification/repair
  observed current speed

CANDIDATE
  ChatGPT semantic authority through Plan/Task Contract
  Codex Stage 5 materialization + verification
  Terra/Medium + Standard as initial profile
  Sol escalation only on predeclared trigger
  cost-aware child delegation
```

The experiment must keep acceptance criteria and task difficulty matched and score **accepted outcome plus cost**, not token consumption alone.

A separate focused qualification can validate the slim-AGENTS instruction chain and verify that critical invariants remain loaded from representative working directories.

No provider/model execution is authorized by R027 itself.

## Decision questions

R027 leaves the following normative decisions open:

1. Should ordinary source maintenance default to Executor materialization, with Orchestrator materialization reserved for explicit frozen-candidate/semantic-control cases?
2. Should D055 add `Speed: STANDARD|FAST` with Standard as the normal default?
3. Should D065/D075 make positive delegation ROI explicit before spawning children?
4. Should Terra/Medium become the normal bounded implementation profile if prospective evidence meets quality/cost gates?
5. Should all-Markdown ChatGPT ownership narrow to normative governance Markdown, allowing Codex to own implementation-coupled technical documentation?
6. What project-specific root `AGENTS.md` budget preserves every critical invariant while minimizing mandatory context?

Until those questions are decided:

```text
Research-State: COMPLETE
Decision-State: EVALUATING
Current D068/D055/D065/D075 authority: unchanged
Current Markdown ownership: unchanged
New Codex model default: NOT ADOPTED
New Executor materialization default: NOT ADOPTED
No provider/model calls authorized
```

## Sources

### OpenAI — primary/current

- ChatGPT Work and Codex: https://help.openai.com/en/articles/20001275/
- Using Codex with your ChatGPT plan: https://help.openai.com/en/articles/11369540/
- Prompting / Codex workflows: https://learn.chatgpt.com/docs/prompting
- AGENTS.md project instruction discovery: https://learn.chatgpt.com/docs/agent-configuration/agents-md
- Codex subagents: https://learn.chatgpt.com/docs/agent-configuration/subagents
- Codex speed: https://learn.chatgpt.com/docs/agent-configuration/speed
- Codex rate card: https://help.openai.com/es-419/articles/20001106-tarifario-de-codex
- GPT-5.6 Terra model: https://developers.openai.com/api/docs/models/gpt-5.6-terra
- Harness Engineering: https://openai.com/index/harness-engineering/

### External empirical/specialized

- Lulla et al., *On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents*, arXiv:2601.20404: https://arxiv.org/abs/2601.20404
- Gloaguen et al., *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?*, arXiv:2602.11988: https://arxiv.org/abs/2602.11988
- Garg, Nitin, Huang, *Terminus-4B: Can a Smaller Model Replace Frontier LLMs at Agentic Execution Tasks?*, Microsoft Research / arXiv:2605.03195: https://www.microsoft.com/en-us/research/publication/terminus-4b-can-a-smaller-model-replace-frontier-llms-at-agentic-execution-tasks/
- Zhang et al., *FastContext: Training Efficient Repository Explorer for Coding Agents*, arXiv:2606.14066: https://arxiv.org/abs/2606.14066

## Volatility / revalidation note

Model availability, credit rates, Fast-mode multipliers, product usage accounting, Codex instruction limits and subagent behavior are vendor/runtime facts and may change. D077 therefore applies before any later consequential decision based on those facts.

The durable parts of R027 are the architectural principles: eliminate duplicate context/work, put repo-local execution with the code executor, keep semantic authority separate from implementation, delegate only when the delegation benefit exceeds its context/tool overhead, and evaluate cost per accepted outcome rather than token count alone.
