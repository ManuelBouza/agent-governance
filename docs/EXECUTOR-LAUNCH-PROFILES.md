# Executor Launch Profiles

Status: ACTIVE SOURCE-MAINTAINER GUIDANCE  
Controlling decision: `docs/decisions/D055-executor-launch-session-and-compute-profile.md`  
Coordinator/worktree refinement: `docs/decisions/D058-executor-coordinator-session-and-worktree-hygiene.md`  
Task-scoped coordinator continuity: `docs/decisions/D060-task-scoped-executor-coordinator-continuity.md`  
Bootstrap authority: `docs/decisions/D042-remote-baseline-freshness-before-contract-load.md`

## Purpose

Provide the compact Human-facing launch metadata that ChatGPT Orchestrator must give before every prompt delegated to an Agente de IA Ejecutor, and normalize the minimal transport prompt used to reach persisted Git authority safely.

This file maps the portable D055 policy onto the currently selected Executor adapter. D060 prospectively refines the session-lifetime portion of D055/D058. It does not change Task Contract semantics and does not make any model/product a source dependency.

## Required launch card

Before the prompt itself, ChatGPT presents:

```text
Executor: <active concrete executor>
Session: NEW | CONTINUE
Coordinator-ID: AG | <repo> | <work-unit> | root-<n>
Host-Display-Title: <observed host-generated title when useful, otherwise n/a>
Model: <exact recommended model available in that executor>
Effort: <exact recommended reasoning setting>
Rationale: <one concise sentence>
```

The first coordinator for a work unit uses `root-1`. The same work unit normally keeps that exact governance `Coordinator-ID` for its entire lifecycle. `root-2+` is reserved for explicit same-task failover when the prior root cannot safely continue; it is not a routine fresh-context choice.

`Coordinator-ID` is Human navigation/continuity metadata, not Task Contract authority. If the active host exposes a supported naming/rename control, apply the exact `Coordinator-ID` as the visible session title. If it does not, preserve the host-generated visible title separately as `Host-Display-Title`; a mismatch between the two is not itself a governance failure.

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

## Session rule — D060 task-scoped continuity

Use this decision order:

```text
new Task/Operational Contract work unit?      -> NEW / root-1
same work unit and root safely recoverable?   -> CONTINUE same root
same task after Orchestrator barrier/review?   -> CONTINUE same root
fresh independent technical perspective?      -> keep root; use internal fresh child/context
prior root unavailable/corrupt/unrecoverable?  -> NEW same task / next root ordinal (failover)
context irreparably contaminated?              -> NEW same task / next root ordinal (failover)
new successor Task/Operational Contract?       -> NEW / root-1 for the new work unit
```

A work unit is the exact persisted Task Contract ID/path or Operational Contract ID/path. A review/rework revision that continues the same Task ID remains the same work unit. A successor Task ID is a new work unit even if it shares product area, research lineage or branch ancestry.

Under D060, `CONTINUE` is not merely an optimization for same-task follow-up; it is the normal required coordinator continuity behavior while the original root remains safe and recoverable.

Need for independent review, exploration or noisy test/log analysis does not normally justify a second Human-visible coordinator. Prefer a fresh bounded internal child/subagent or equivalent fresh context while the root remains the task coordinator.

`root-2+` is failover only. The launch rationale must state why the prior root cannot safely continue, and the old/replacement roots must not remain concurrently writable for the same task/worktree.

A newly governing `AGENTS.md` or review change does not by itself require a new root when the active host can safely reload it. D042/D043 freshness/reload still applies on every continuation.

Session continuity never exempts D042 remote freshness. `CONTINUE` preserves useful task context, not stale repository state.

## Root context-hygiene rule

The Human-visible root should remain a compact task ledger.

Prefer retaining:

```text
exact task/authority pointer
current phase/status
branch/worktree identity
relevant accepted constraints
concise child findings
completed actions represented in Git/evidence
unresolved blockers/findings
latest Orchestrator review/gate
next concrete action
```

Avoid retaining unnecessary raw logs, large command output, full file dumps, full child transcripts, abandoned implementation traces and repeated copies of persisted authority.

When supported, safe host-native compaction may be used to reduce context pressure. Compaction is execution state only; Git and persisted authority remain canonical.

D060 defines root lifetime, not the exact worker-delegation policy. R012 separately controls the pending question of when delegation should become semantically mandatory.

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

Research baseline: 2026-08-23; naming/session guidance corrected 2026-09-06  
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

The current Codex desktop surface used by Agent Governance has demonstrated host-generated conversation titles. Do not assume deterministic thread/session rename capability from the presence of a visible title. When a supported naming/rename surface is directly available in the active host version, the Human may align the visible title to the governance `Coordinator-ID`; otherwise the host-generated title remains separate adapter metadata.

Current OpenAI Help documentation describes Codex chat titles in chat-history management, but deterministic naming/rename control is not a correctness dependency of Agent Governance.

Current OpenAI long-running-agent guidance also recommends deliberate compaction and preservation of completed actions, active assumptions, IDs, tool outcomes, unresolved blockers and the next concrete goal. D060 adopts that principle only as context hygiene; vendor compaction is never correctness authority.

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
Coordinator-ID: AG | agent-governance | TNNN | root-1
Host-Display-Title: <host-generated title or n/a>
Model: GPT-5.6 Sol
Effort: Medium
Rationale: first launch of a new bounded implementation task; this governance root remains the coordinator through the complete TNNN lifecycle.
```

### Same-task R1 rework

```text
Executor: Codex
Session: CONTINUE
Coordinator-ID: AG | agent-governance | TNNN | root-1
Host-Display-Title: <same recoverable host conversation title>
Model: GPT-5.6 Sol
Effort: Medium
Rationale: same Task Contract and recoverable coordinator root; reload the persisted review/current authority and continue without discarding useful task context.
```

### Same-task independent review

```text
Human-visible root: CONTINUE Coordinator-ID AG | agent-governance | TNNN | root-1
Freshness need: delegate a bounded fresh Verifier/Reviewer child when supported
Do not open root-2 solely to obtain independent technical reasoning.
```

### Read-only post-integration operation

```text
Executor: Codex
Session: NEW
Coordinator-ID: AG | agent-governance | OPNNN | root-1
Host-Display-Title: <host-generated title or n/a>
Model: GPT-5.6 Luna
Effort: Low
Rationale: this Operational Contract is a new governed work unit with its own coordinator lifecycle.
```

### Same-task root failover

```text
Executor: Codex
Session: NEW
Coordinator-ID: AG | agent-governance | TNNN | root-2
Host-Display-Title: <host-generated title or n/a>
Model: <minimum sufficient current model>
Effort: <minimum sufficient effort>
Rationale: root-1 is no longer recoverable/safe to continue; this is explicit same-task failover, not a fresh-review convenience.
```

### Subtle concurrency/security correction in a new task

```text
Executor: Codex
Session: NEW
Coordinator-ID: AG | agent-governance | TNNN | root-1
Host-Display-Title: <host-generated title or n/a>
Model: GPT-5.6 Sol
Effort: High
Rationale: new Task Contract with non-local ordering/fail-closed risk where extra reasoning materially reduces implementation/review risk.
```

## Re-evaluation

The Orchestrator should periodically re-check official Executor documentation when:

- available model tiers change;
- effort labels/semantics change;
- session/thread naming or compaction surfaces change;
- a new Executor replaces the current adapter;
- repeated AG evidence shows task-scoped continuation is creating material context degradation despite hygiene;
- repeated AG evidence shows the current compute mapping is systematically over- or under-provisioned.

Provider mapping and naming/compaction surface changes are operating-guidance updates, not Governance Core protocol changes.

## Current OpenAI references

- https://openai.com/index/gpt-5-6/
- https://developers.openai.com/api/docs/guides/latest-model
- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5
- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.2
- https://developers.openai.com/codex/use-cases
- https://help.openai.com/en/articles/20001354-gpt-56-in-chatgpt/
- https://help.openai.com/en/articles/20001275/
- https://help.openai.com/en/articles/20001333-how-to-archive-and-delete-codex-chats-in-the-chatgpt-app