# D055 — Executor launch session and compute profile

Status: ACCEPTED  
Date: 2026-08-23  
Authority: Human Owner / ChatGPT Orchestrator  
Refines: D041, D043, D046, D054  
Preserves: executor-product neutrality, persisted Task Contract authority, D053 stage ownership

## Problem

Agent Governance already makes launch prompts intentionally small because the persisted Task Contract and repository state carry the authoritative execution semantics. That leaves a separate operational decision implicit: which concrete Executor is active, whether the next handoff should start a fresh host session or continue the existing one, and which model/reasoning setting is proportionate to the technical work.

Leaving those choices implicit creates two avoidable failure modes:

- **under-provisioning** — a difficult technical task is delegated with insufficient model capability or reasoning effort, increasing retries, review churn or incorrect implementation;
- **over-provisioning** — a narrow or mechanically specified task is run with unnecessarily expensive/slow reasoning, wasting usage and context budget without improving acceptance quality.

The Orchestrator already owns the complete specification/Design/Plan boundary under D053. Therefore model effort must be selected for the remaining technical implementation/review difficulty, not used as compensation for missing Governance authority.

## Decision

Before every prompt intended for an Agente de IA Ejecutor, ChatGPT Orchestrator SHALL emit a separate **Executor Launch Profile** for the Human Owner.

The required visible fields are:

```text
Executor: <concrete active executor/host>
Session: NEW | CONTINUE
Model: <concrete currently available model>
Effort: <concrete host-supported reasoning setting>
Rationale: <one concise sentence>
```

The launch profile is Human-facing execution guidance. It is **not part of the Task Contract** and normally is **not copied into the Executor prompt** when the host exposes model/session settings through its UI or configuration.

The actual Executor prompt remains transport only and continues to point to canonical repository/branch state plus the exact persisted Task Contract/review authority.

## Active Executor identity

The Orchestrator MUST know which concrete Executor adapter is active before issuing an executor prompt.

The current source-maintenance checkpoint SHOULD record the active adapter when one is selected, for example:

```text
Active-Executor: Codex
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows
```

If the active Executor is unknown, changed, or materially differs from the checkpoint, the Orchestrator must resolve that identity before recommending model/session settings. It must not silently apply Codex-specific settings to OpenCode, Claude Code, Antigravity or another host.

Concrete product identity remains an adapter concern only. It does not change task semantics, authority, acceptance or branch ownership.

## Session selection

`NEW` is the default for the first launch of a new Task Contract/work unit.

Use `NEW` when any of these applies:

- the task/work unit is different from the one represented by the current Executor chat;
- a cold-start/independence/fresh-context boundary is part of the evidence;
- the Executor product/host or repository checkout changed;
- prior session context is materially stale, contaminated, contradictory or dominated by unrelated work;
- the host cannot reliably reload newly controlling repository instructions;
- continuing would create more context noise than reconstructing from canonical Git state.

Use `CONTINUE` when all material work remains the same Task Contract/represented branch and the existing session is still a clean implementation context. Typical cases are:

- in-task follow-up after a diagnostic result;
- Executor rework after an Orchestrator review that persists the revised authority;
- completion of the same branch/handoff after a bounded blocker is resolved;
- same-task verification or correction where retaining local implementation context reduces redundant reload cost.

An `AGENTS.md` change does not by itself force a new session if D043's conditional reload can safely refresh the active session. If the host cannot establish the new instruction snapshot reliably, choose `NEW`.

Session continuity is never authority. Canonical Git state and persisted contracts still control.

## Model and reasoning selection

The Orchestrator SHALL recommend the **lowest-cost/lowest-effort configuration that retains a reasonable quality margin for the actual technical risk**.

Higher reasoning is not a remedy for incomplete specification, missing Design, ambiguous acceptance or an unauthorized scope decision. Those conditions require Orchestrator re-entry under D053.

### LOW

Use for mechanically bounded work with strong deterministic guidance, such as:

- read-only canonical baseline checks and evidence collection;
- narrow mechanical metadata/config synchronization;
- small local implementation changes whose exact semantics are already frozen;
- repetitive verification/diagnostic operations with obvious postconditions.

LOW should be common where the Orchestrator has removed semantic ambiguity and the Executor mostly needs accurate execution rather than broad search.

### MEDIUM

MEDIUM is the normal default for Agent Governance Executor work and is expected to be the center of gravity.

Use for:

- ordinary multi-file implementation under a complete Task Contract;
- normal refactors with characterization coverage;
- bounded debugging and test correction;
- routine Code Review & Verify over a coherent implementation;
- ordinary branch reconciliation without unusual history/risk conditions.

The majority of normal implementation tasks should not need reasoning above this level merely because they are delegated to an agent.

### HIGH

Use selectively when the technical implementation/review itself contains substantial reasoning risk, for example:

- non-local concurrency or ordering defects;
- security/fail-closed behavior with subtle bypass risk;
- portability/platform interactions with weak observability;
- difficult repository-history reconciliation where represented work must be preserved;
- complex refactors with several interacting invariants;
- hard debugging where multiple plausible root causes survive deterministic narrowing.

HIGH is a minority setting. Its rationale must identify the concrete technical difficulty, not simply state that the task is important.

### XHIGH / MAX / ULTRA or equivalent

Treat the host's highest reasoning/subagent modes as exceptional escalation settings, never as defaults.

Use only when a concrete difficult/long-horizon task has evidence that normal HIGH is insufficient or when the marginal quality benefit materially affects the result. Subagent/Ultra topology remains Executor-internal process under D041 and gains no Governance authority.

## Evidence-driven tuning

D039's learning loop applies to launch-profile tuning.

Repeated task classes may be downshifted when evidence shows a lower model/effort configuration preserves quality, verification success and review convergence. They may be upshifted when failures are credibly attributable to implementation reasoning capacity rather than specification defects, missing evidence, tool/host faults or stale context.

Do not optimize against raw token/latency usage alone; the objective is minimum sufficient compute for accepted quality with low rework.

## Provider-specific mapping

The generic LOW/MEDIUM/HIGH policy is portable. The concrete model mapping belongs to the current Executor adapter and can change without changing Governance semantics.

For the current Codex adapter, `docs/EXECUTOR-LAUNCH-PROFILES.md` carries the current mapping and must be refreshed when OpenAI materially changes available model tiers or reasoning controls.

No model name is a repository correctness dependency.

## Handoff and audit boundary

Model, reasoning level and session choice are normally launch-time operating parameters, not acceptance criteria.

They SHOULD be persisted in a Task Contract or required handoff evidence only when the model/session itself is material to reproducibility, a model-dependent eval, a host-independence experiment, or another explicit acceptance claim.

Otherwise remote review continues to judge the submitted Git state and evidence rather than inferring quality from model identity or reasoning effort.

## Research basis

Current OpenAI guidance supports the proportional-compute direction used by the Codex adapter:

- GPT-5.6 exposes Sol as the frontier tier, Terra as the intelligence/cost-balanced tier and Luna as the efficient high-volume tier; Codex permits model and effort selection: https://openai.com/index/gpt-5-6/
- OpenAI model guidance recommends setting reasoning effort intentionally, using `medium` as a balanced starting point and `low` for latency-sensitive workloads, and comparing one level lower rather than assuming maximum reasoning is optimal: https://developers.openai.com/api/docs/guides/latest-model
- OpenAI documents Codex as a persistent desktop coding workflow and explicitly supports follow-up work in the same chat, which is compatible with same-task `CONTINUE` when canonical authority remains persisted: https://help.openai.com/en/articles/20001275/
- GPT-5.6 reasoning controls and Codex availability remain product/version dependent: https://help.openai.com/en/articles/20001354-gpt-56-in-chatgpt/

These sources inform the current adapter mapping. They do not become Agent Governance authority and do not freeze vendor model names.

## Consequences

- every Executor prompt is accompanied by an explicit session/model/effort recommendation;
- the Human no longer has to infer whether a new Codex chat is required;
- MEDIUM becomes the normal default, LOW is deliberately used for bounded work, and HIGH is reserved for concrete technical complexity;
- the Orchestrator must track the active concrete Executor adapter;
- model/session settings remain outside Task Contract semantics unless materially required;
- host-specific model churn does not require changing Governance Core semantics;
- over-effort and under-effort become observable launch-quality defects that can be tuned through D039 evidence.
