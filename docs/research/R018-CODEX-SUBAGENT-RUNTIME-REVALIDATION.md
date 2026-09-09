# R018 — Codex Subagent Runtime Revalidation

Research-ID: R018  
Research-State: COMPLETE  
Decision-State: NOT_REQUIRED  
Opened: 2026-09-09  
Last-Reviewed: 2026-09-09  
Owner: ChatGPT Orchestrator  
Scope: fresh official OpenAI/Codex revalidation for D075 and T063 prelaunch; source-product Executor coordination only  
Question: Do current official OpenAI documentation and the current stable Codex runtime support the D075 coordinator-direct gate and the T063 adaptive-worker evaluation design, and what launch-time corrections or constraints are required?  
Evaluation-Refs: D063; D065; D075; R007; R017; T054/T054-R1; T063  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Provenance correction

R017/D075 were integrated before this **fresh external revalidation** was actually performed. Their official-source discussion was based on recently persisted project research and current-looking source references, not on a new independent web/source pass executed immediately before D075 integration.

This R018 closes that provenance gap explicitly. It does not rewrite the historical R017 analysis or pretend that the earlier fresh revalidation occurred before PR `#349`.

Result: the current official evidence supports D075's conclusion. One T063 topology-label correction is required before launch, described below.

## Sources revalidated on 2026-09-09

### Official OpenAI documentation

- OpenAI, **Subagents**: `https://learn.chatgpt.com/docs/agent-configuration/subagents`
- OpenAI, **Codex best practices**: `https://learn.chatgpt.com/guides/best-practices`
- OpenAI, **Model guidance**: `https://developers.openai.com/api/docs/guides/latest-model`
- OpenAI, **Codex releases**: `https://github.com/openai/codex/releases`

### Official OpenAI Codex stable source

Current stable release at review time:

```text
codex-cli 0.153.4
release tag: rust-v0.153.4
released: 2026-09-04
```

Inspected at the exact stable tag:

- `codex-rs/core/src/tools/handlers/multi_agents/spawn.rs`
- `codex-rs/core/src/tools/handlers/multi_agents_spec.rs`
- `codex-rs/core/src/config/mod.rs`
- `codex-rs/features/src/feature_configs.rs`

The release page also shows `0.154.0-alpha.*` pre-releases. They are not treated as the stable T063 measurement baseline.

## Finding 1 — official guidance supports a direct-versus-delegate gate

Current OpenAI Subagents guidance says subagent workflows are particularly useful for complex/highly parallel tasks such as codebase exploration and multi-step feature work. It identifies context pollution/rot as a reason to offload noisy exploration, tests and logs, and recommends read-heavy work as a starting point while warning that parallel write-heavy work can create conflicts and coordination overhead.

It also states that each subagent performs its own model/tool work and therefore consumes more tokens than a comparable single-agent run.

This supports the central D075 proposition:

```text
worker creation has non-zero coordination/context/compute cost
therefore trivial auxiliary work should not automatically spawn a worker
```

## Finding 2 — Codex 0.153.4 runtime guidance is even closer to D075/D065

The stable `rust-v0.153.4` `spawn_agent` tool guidance explicitly tells the root to:

- analyze the overall task and identify the immediate critical-path task versus independent sidecar tasks;
- decide what immediate work should stay local before delegating;
- delegate concrete bounded subtasks that can run independently alongside useful root work;
- keep urgent blocking work local when the next action depends immediately on its result;
- keep tightly coupled or poorly delegable work local;
- avoid duplicating root and delegated work;
- use disjoint write sets for parallel coding work;
- avoid reflexive waiting and continue useful non-overlapping root work while children run.

This is materially consistent with D065's anti-triggers for small/tightly serial/high-coordination-cost work and D075's coordinator-direct gate.

A useful interpretation refinement is that **critical-path coupling** is already covered by D065's serial/coordination anti-triggers. No new D075 decision is required merely to add a sixth numeric dimension.

## Finding 3 — current official model guidance supports the T063 hypotheses, not a global policy

Current OpenAI Subagents documentation states that child model/reasoning can be inherited or selected independently and gives the following task-oriented guidance:

```text
gpt-5.6        -> demanding, ambiguous, multi-step work
gpt-5.6-terra  -> exploration, read-heavy scans, large-file/supporting work
gpt-5.6-luna   -> narrow, clear, repeatable or high-volume work

medium -> balanced default
low    -> straightforward/speed-oriented work
high   -> complex logic, assumptions, edge cases, review/security
```

That directly supports T063's *hypothesis shape*:

```text
P1 -> Luna-class / Medium
P2 -> Terra-class / Medium
P3 -> Terra-class / High
```

It does **not** qualify those mappings for Agent Governance. T054's `NOT_QUALIFIED` result remains controlling historical evidence and T063 must still measure first-attempt quality and exact-child usage before any normative Stage-B routing decision.

## Finding 4 — stable 0.153.4 is the preferred T063 measurement baseline

The official Codex release page identifies `0.153.4` as the current stable release at this review time.

D063's qualified read-only child measurement substrate was also established on Codex/App Server `0.153.4`.

Therefore, for T063, exact stable `0.153.4` is the lowest-confound preferred runtime **if the Human later launches T063 and the native host can realize it**.

Do not substitute an `0.154.0-alpha.*` pre-release for the scored run merely because it is newer. A materially different runtime requires D063 capability/schema revalidation before scoring.

This is a research recommendation, not launch authorization. The launch review must still verify the actual executable/App Server version.

## Finding 5 — model/reasoning overrides exist in stable source but remain runtime-configurable

At `rust-v0.153.4`:

- `SpawnAgentArgs` includes `model` and `reasoning_effort`;
- spawn configuration applies requested model/reasoning overrides;
- the completed spawn event derives effective model/reasoning from the child agent configuration snapshot when available;
- Multi-Agent V2 configuration has `expose_spawn_agent_model_overrides`;
- its stable default is `true`;
- the V2 tool schema removes the model/reasoning properties when that exposure flag is disabled.

Therefore the capability is real in the stable source, but **documentation/source support is not enough to assume that every concrete client/account/session exposes the same callable schema**.

T063 is correct to fail closed unless its live native preflight confirms the required profile-selection and D063 receipt surface.

## Finding 6 — permissions reinforce the D063 read-only design

Current OpenAI Subagents documentation states that subagents inherit the parent's current sandbox/permission policy and that live parent runtime permission overrides are reapplied to spawned children. It also documents custom-agent sandbox overrides.

T063 should not weaken D063 by relying only on prompt-level read-only instructions or a custom-agent declaration. The scored run should continue to require the qualified parent/child `:read-only` permission receipts and tracked-mutation verification.

## Finding 7 — T063 should explicitly pin its root profile at launch

Codex `0.153.4` release notes make GPT-6 Astra the bundled default when no model is explicitly configured.

Agent Governance R010 nevertheless remains `COMPLETE / DEFERRED`: Astra availability does not by itself authorize a global D055 migration.

T063 is also a corrected successor to T054, whose CONTROL baseline was `GPT-5.6 Sol / Medium`. Current OpenAI Subagents guidance still recommends GPT-5.6 as the normal starting point for demanding Codex agent work.

Accordingly, the preferred prelaunch hypothesis is:

```text
root / CONTROL baseline: GPT-5.6 Sol / Medium
P1 ADAPTIVE:              GPT-5.6 Luna / Medium
P2 ADAPTIVE:              GPT-5.6 Terra / Medium
P3 ADAPTIVE:              GPT-5.6 Terra / High
```

The root must be explicitly selected rather than relying on the 0.153.4 default. This preserves T054 comparability and avoids introducing Astra as an unplanned second experimental variable.

The exact matrix remains launch-time adapter data and is **not frozen by R018**. T063's explicit Human launch gate still controls.

## Finding 8 — T063 Stage-A label needs one prelaunch correction

D075 defines three mutually exclusive first-stage execution targets:

```text
COORDINATOR_DIRECT
DELEGATED
CONTRACT_FIXED
```

T063's scored CONTROL/ADAPTIVE topology is material to the experiment: the Task Contract requires fresh matched children, fixed arm order, bounded context, read-only permissions and exact receipts.

Therefore the actual Stage-A target for scored T063 probes is:

```text
execution_target = CONTRACT_FIXED
```

At the same time, the selected probe units are deliberately chosen so that, absent the experiment, they independently satisfy D065/D075 material-delegation eligibility:

```text
underlying_delegation_eligibility = DELEGATED
```

This distinction matters. T063 must not claim that D075 dynamically chose ordinary delegation when the experiment itself fixes the topology.

The correction does not change probe semantics, child count, model hypotheses, or acceptance. It only makes the governance classification internally consistent.

## Disposition

Fresh revalidation result:

```text
D075 direct-execution gate: SUPPORTED / NO NORMATIVE CHANGE REQUIRED
D065 relationship:          SUPPORTED
T063 model hypotheses:      SUPPORTED AS HYPOTHESES ONLY
D063 measurement posture:   SUPPORTED / LIVE PREFLIGHT STILL MANDATORY
preferred stable runtime:   Codex 0.153.4
T063 topology label:        PRELAUNCH CORRECTION REQUIRED
T063 launch:                NOT AUTHORIZED BY THIS RESEARCH
R007 global routing policy: NOT DECIDED
```

A separate persisted prelaunch correction should make T063's exact matched-arm topology `CONTRACT_FIXED` while retaining `DELEGATED` as the underlying semantic eligibility of the probe units.

No provider/model call was made by this research.