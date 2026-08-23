# Executor Launch Profiles

Status: ACTIVE SOURCE-MAINTAINER GUIDANCE  
Controlling decision: `docs/decisions/D055-executor-launch-session-and-compute-profile.md`

## Purpose

Provide the compact Human-facing launch metadata that ChatGPT Orchestrator must give before every prompt delegated to an Agente de IA Ejecutor.

This file maps the portable D055 policy onto the currently selected Executor adapter. It does not change Task Contract semantics and does not make any model/product a source dependency.

## Required launch card

Before the prompt itself, ChatGPT presents:

```text
Executor: <active concrete executor>
Session: NEW | CONTINUE
Model: <exact recommended model available in that executor>
Effort: <exact recommended reasoning setting>
Rationale: <one concise sentence>
```

Then, separately:

```text
PROMPT FOR EXECUTOR
<minimal transport prompt pointing to canonical repository/branch + persisted authority>
```

The launch card is for the Human to configure/select the Executor session. Do not duplicate it inside the prompt unless the host has no separate model/session control and the setting must be conveyed textually.

## Session rule

Use this decision order:

```text
new Task Contract/work unit?                 -> NEW
same Task Contract + same represented branch? -> CONTINUE
cold-start/independence evidence required?    -> NEW
executor/host/checkout changed?               -> NEW
prior context stale/contaminated/unrelated?   -> NEW
same-task rework/follow-up with clean context? -> CONTINUE
```

A newly governing `AGENTS.md` change uses D043 conditional reload when the host can refresh it safely; otherwise use `NEW`.

## Effort rule

```text
LOW     = mechanical/bounded execution with strong deterministic guidance
MEDIUM  = normal AG implementation/review default
HIGH    = substantial technical reasoning risk
XHIGH/MAX/ULTRA = exceptional escalation only
```

Do not raise effort to compensate for an incomplete specification or missing Design/Plan authority. Stop/re-enter instead.

## Current adapter — Codex

Research baseline: 2026-08-23  
Surface: ChatGPT desktop app -> Codex  
Current host: native Windows source-maintenance workstation

OpenAI currently exposes the GPT-5.6 family in Codex with Sol, Terra and Luna tiers and configurable effort. The current Agent Governance recommendation is:

| Work class | Recommended Codex model | Effort | Typical use |
| --- | --- | --- | --- |
| Read-only/repetitive observation | GPT-5.6 Luna | Low | baseline/status/log collection with deterministic postconditions |
| Narrow mechanical implementation | GPT-5.6 Terra | Low | tightly specified local/config/test synchronization with strong tests |
| Standard AG implementation/rework | GPT-5.6 Sol | Medium | default multi-file implementation, ordinary refactor/debug/review |
| Complex/high-risk technical work | GPT-5.6 Sol | High | concurrency, subtle fail-closed/security, hard portability, complex Git/history, difficult diagnosis |
| Exceptional long-horizon work | GPT-5.6 Sol | XHigh/Max only when justified | only after concrete evidence that High is insufficient |

### Conservative fallbacks

- If Luna is unavailable, use Terra Low for read-only/repetitive work.
- If Terra is unavailable, use Sol Low for narrow mechanical work.
- If the exact higher-effort label differs in the Codex UI, use the closest current host-supported equivalent and state that exact label in the launch card.
- `Ultra`/subagent mode is not required by Agent Governance. Use it only when the task genuinely benefits from parallel/long-horizon execution and the added resource use is justified.

## Default bias

For the current source-maintenance workflow, the expected distribution is qualitative, not a quota:

- **MEDIUM / Sol** should be the center of gravity and likely cover more than half of ordinary Executor implementation work;
- **LOW** should be used deliberately for a substantial set of mechanical/read-only tasks instead of paying for unnecessary reasoning;
- **HIGH** should be materially less common and must have a concrete technical rationale;
- the highest modes should be rare exceptions.

Do not force tasks into these percentages. Actual task risk and evidence control.

## Examples

### Fresh normal implementation task

```text
Executor: Codex
Session: NEW
Model: GPT-5.6 Sol
Effort: Medium
Rationale: first launch of a new bounded implementation task; the Task Contract carries the design and normal multi-file technical reasoning remains.
```

### Same-task R1 rework

```text
Executor: Codex
Session: CONTINUE
Model: GPT-5.6 Sol
Effort: Medium
Rationale: same represented Task Contract/branch and the persisted review supplies the revised authority, so retaining implementation context avoids redundant reload cost.
```

### Read-only post-integration baseline

```text
Executor: Codex
Session: NEW
Model: GPT-5.6 Luna
Effort: Low
Rationale: independent read-only verification with deterministic commands/postconditions; no implementation reasoning is required.
```

### Subtle concurrency/security correction

```text
Executor: Codex
Session: NEW
Model: GPT-5.6 Sol
Effort: High
Rationale: the technical work has non-local ordering/fail-closed risk where extra reasoning materially reduces implementation/review risk.
```

## Re-evaluation

The Orchestrator should periodically re-check official Executor documentation when:

- available model tiers change;
- effort labels/semantics change;
- a new Executor replaces the current adapter;
- repeated AG evidence shows the current mapping is systematically over- or under-provisioned.

Provider mapping changes are operating-guidance updates, not Governance Core protocol changes.

## Current OpenAI references

- https://openai.com/index/gpt-5-6/
- https://developers.openai.com/api/docs/guides/latest-model
- https://help.openai.com/en/articles/20001354-gpt-56-in-chatgpt/
- https://help.openai.com/en/articles/20001275/
