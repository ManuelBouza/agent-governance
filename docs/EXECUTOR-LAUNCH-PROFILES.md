# Executor Launch Profiles

Status: ACTIVE SOURCE-MAINTAINER GUIDANCE  
Controlling decision: `docs/decisions/D055-executor-launch-session-and-compute-profile.md`  
Coordinator/worktree refinement: `docs/decisions/D058-executor-coordinator-session-and-worktree-hygiene.md`  
Bootstrap authority: `docs/decisions/D042-remote-baseline-freshness-before-contract-load.md`

## Purpose

Provide the compact Human-facing launch metadata that ChatGPT Orchestrator must give before every prompt delegated to an Agente de IA Ejecutor, and normalize the minimal transport prompt used to reach persisted Git authority safely.

This file maps the portable D055 policy onto the currently selected Executor adapter. It does not change Task Contract semantics and does not make any model/product a source dependency.

## Required launch card

Before the prompt itself, ChatGPT presents:

```text
Executor: <active concrete executor>
Session: NEW | CONTINUE
Coordinator-Chat: <deterministic name when the host supports named sessions; otherwise n/a>
Model: <exact recommended model available in that executor>
Effort: <exact recommended reasoning setting>
Rationale: <one concise sentence>
```

For the current Codex adapter, D058 requires:

```text
Coordinator-Chat: AG | <repo> | <work-unit> | root-<n>
```

The first coordinator for a work unit uses `root-1`. Same-work-unit `CONTINUE` keeps the same name. A required fresh root for the same work unit increments the ordinal.

The coordinator name is Human navigation/continuity metadata, not Task Contract authority. The Human applies the exact name through the supported host UI/session naming surface before substantive execution.

The launch card is for the Human to configure/select the Executor session. Do not duplicate it inside the prompt unless the host has no separate model/session control and the setting must be conveyed textually.

## Mandatory remote-freshness bootstrap

D042 applies to **every** Executor launch, including read-only verification, same-task continuation and work on an already existing topic branch.

Before loading repository policy or persisted execution authority, the Executor must:

```text
synchronize canonical GitHub remote
        -> establish/verify safe current local baseline from canonical remote state
        -> load AGENTS.md from that refreshed state
        -> load the exact persisted task/review/gate authority
        -> execute
```

`current` means the current canonical remote state at execution time, not a SHA remembered by ChatGPT, not a stale local `develop`, and not merely the branch currently checked out.

Remote freshness must not discard local or unrepresented work. If a safe current baseline cannot be established, the Executor fails closed according to D042/RB001 rather than reset/clean/overwrite merely to satisfy the launch.

D058 additionally requires the writable workspace selected for a work unit to be exclusive when concurrent writable work exists. The Executor must not solve a workspace collision by discarding another worktree's represented or unrepresented state.

The prompt tells the Executor to synchronize/refresh from GitHub; **the prompt does not prescribe Git commands**. Exact Git/CLI mechanics remain Executor-owned under D054 and the applicable runbook.

## Canonical minimal transport prompt

Unless a persisted authority explicitly requires additional transport metadata, every Executor prompt SHOULD use this shape:

```text
Operate as the Agente de IA Ejecutor for <repository>.

Synchronize with GitHub and establish a safe current local baseline from the canonical remote state before loading repository instructions or execution authority, per D042/RB001. Do not discard unrepresented local work.

Use <canonical/base or represented topic branch as applicable>.

Load current repository instructions, then execute exactly:
<persisted authority path>

Return only the output required by that persisted authority.
```

For a task that must continue on an existing represented topic branch, `Use ...` identifies that branch. The Executor still refreshes canonical remote references first and safely reconciles only as permitted by the persisted authority.

Do **not** add to the prompt:

- task requirements or acceptance criteria already persisted in Git;
- implementation instructions;
- shell/Git/uv/PowerShell commands;
- copied excerpts from the Task Contract/review/gate;
- a remembered HEAD as the source of truth when the persisted authority can resolve current state;
- model/session configuration already shown in the Human-facing launch card.

A SHA may appear in a prompt only when the persisted authority makes that exact identity materially necessary for safe reconciliation or verification. It must never replace the required fresh remote synchronization.

## Session rule

Use this decision order:

```text
new Task Contract/work unit?                  -> NEW
same Task Contract + same represented branch? -> CONTINUE
cold-start/independence evidence required?     -> NEW
executor/host/checkout changed?                -> NEW
prior context stale/contaminated/unrelated?    -> NEW
same-task rework/follow-up with clean context? -> CONTINUE
```

Under D058, `CONTINUE` additionally requires the same coordinator chat identity. If multiple chats could plausibly represent the work unit and the correct one cannot be identified, use `NEW` with the next root ordinal rather than guessing.

A newly governing `AGENTS.md` change uses D043 conditional reload when the host can refresh it safely; otherwise use `NEW`.

Session continuity never exempts D042 remote freshness. `CONTINUE` preserves useful conversation context, not stale repository state.

## Worktree rule

For writable work on a repository that may host parallel coordinators:

```text
one writable work unit -> one exclusive worktree -> one topic branch
```

Two writable coordinators must not share the same worktree or branch. Before mutation, establish that the selected workspace is attributable to the current work unit and not owned by another active coordinator.

Post-integration worktree retirement and primary-checkout convergence follow `docs/EXECUTOR-SESSION-WORKTREE-HYGIENE.md` and the existing branch-cleanup policy.

## Effort rule

```text
LOW     = mechanical/bounded execution with strong deterministic guidance
MEDIUM  = normal AG implementation/review default
HIGH    = substantial technical reasoning risk
XHIGH/MAX/ULTRA = exceptional escalation only
```

Do not raise effort to compensate for an incomplete specification or missing Design/Plan authority. Stop/re-enter instead.

## Current adapter — Codex

Research baseline: 2026-08-23; naming surface revalidated 2026-09-05  
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

Codex currently supports explicit thread/session naming. R011 records the inspected current source surface; exact naming UI/commands remain vendor-specific and may change.

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
Coordinator-Chat: AG | agent-governance | TNNN | root-1
Model: GPT-5.6 Sol
Effort: Medium
Rationale: first launch of a new bounded implementation task; the Task Contract carries the design and normal multi-file technical reasoning remains.
```

### Same-task R1 rework

```text
Executor: Codex
Session: CONTINUE
Coordinator-Chat: AG | agent-governance | TNNN | root-1
Model: GPT-5.6 Sol
Effort: Medium
Rationale: same represented Task Contract/branch and coordinator chat; the persisted review supplies the revised authority, so retaining implementation context avoids redundant reload cost.
```

### Read-only post-integration baseline

```text
Executor: Codex
Session: NEW
Coordinator-Chat: AG | agent-governance | OPNNN | root-1
Model: GPT-5.6 Luna
Effort: Low
Rationale: independent read-only verification with deterministic commands/postconditions; no implementation reasoning is required.
```

### Subtle concurrency/security correction

```text
Executor: Codex
Session: NEW
Coordinator-Chat: AG | agent-governance | TNNN | root-1
Model: GPT-5.6 Sol
Effort: High
Rationale: the technical work has non-local ordering/fail-closed risk where extra reasoning materially reduces implementation/review risk.
```

## Re-evaluation

The Orchestrator should periodically re-check official Executor documentation when:

- available model tiers change;
- effort labels/semantics change;
- session/thread naming surfaces change;
- a new Executor replaces the current adapter;
- repeated AG evidence shows the current mapping is systematically over- or under-provisioned.

Provider mapping and naming-surface changes are operating-guidance updates, not Governance Core protocol changes.

## Current OpenAI references

- https://openai.com/index/gpt-5-6/
- https://developers.openai.com/api/docs/guides/latest-model
- https://help.openai.com/en/articles/20001354-gpt-56-in-chatgpt/
- https://help.openai.com/en/articles/20001275/
