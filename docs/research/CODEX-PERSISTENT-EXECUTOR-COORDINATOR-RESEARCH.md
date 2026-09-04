# Codex Persistent Executor Coordinator Research

Status: `RESEARCH / NON-CONTROLLING`  
Date: 2026-09-04  
Owner: ChatGPT Orchestrator  
Canonical product: Agent Governance  

## Purpose

Evaluate whether Agent Governance should replace the current default of a fresh Codex session for each new Task Contract/work unit with a controlled model in which a **persistent Codex coordinator thread is retained for one coherent execution dossier/workstream and delegates bounded work to fresh subagents**.

The intended benefit is not merely parallel execution. The main target is to reduce repeated orientation/bootstrap cost while protecting the coordinator's context from exploration, test logs, command output and other disposable implementation detail.

This memo is research only. It does not change D041, D042, D053, D055, the current T023/MG1-v12 execution, Task Contract semantics, branch ownership or acceptance authority.

## Executive conclusion

The pattern is technically viable and is now supported by stable first-class Codex capabilities.

The recommended architecture is **not** one permanent Codex chat for the whole repository. It is:

```text
one persistent Executor coordinator thread per coherent continuity scope/dossier
        |
        +-- fresh bounded explorer subagents
        +-- fresh bounded implementation worker(s)
        +-- fresh bounded verifier/reviewer subagents
        |
        +-- concise summaries + Git/evidence references only
```

The persistent root is an execution cache and coordination surface. It is never Governance authority. Canonical Git state, `AGENTS.md`, the current Orchestrator checkpoint, persisted Task Contracts/reviews and represented branches remain authoritative.

This architecture is a strong fit for Agent Governance because D041 already explicitly permits sub-agents/workers and executor-native orchestration inside D053 stages 5-6. The normative change required for cross-Task-Contract persistence is primarily a prospective refinement of D055's session-selection rule, which currently defaults the first launch of each new Task Contract/work unit to `NEW`.

Adoption should be staged. First validate the pattern in an interactive Codex pilot using stable native subagent and goal features. Only after measured benefit should Agent Governance automate coordinator persistence through Codex App Server or the SDK.

## 1. Current Codex capability

### 1.1 Subagents are first-class and enabled by default

Current OpenAI Codex documentation states that local Codex versions enable subagent workflows by default. Codex can create subagents, send follow-up instructions, wait for them, close them and consolidate their results. In CLI, `/agent` can inspect and switch among agent threads. Applicable `AGENTS.md` or Skill instructions can also request delegation.

The public configuration reference marks `features.multi_agent` as **stable and enabled by default** and exposes the collaboration tools `spawn_agent`, `send_input`, `resume_agent`, `wait_agent` and `close_agent`. The public `[agents]` configuration supports a per-session concurrency cap and default subagent model/reasoning settings.

This is sufficiently mature to support a product pilot without depending on an experimental multi-agent feature.

### 1.2 OpenAI explicitly recommends protecting the main thread

OpenAI's subagent guidance describes two failure modes of large main-thread contexts: context pollution and context degradation. Its recommended division of responsibility maps directly to the proposed Agent Governance topology:

- keep the main agent focused on requirements, decisions and final results;
- delegate exploration, testing and log analysis to specialized subagents;
- return summaries rather than raw intermediate output;
- begin with read-heavy parallel work and be more cautious when multiple agents write code concurrently.

OpenAI also notes that each subagent performs its own model/tool work, so a multi-agent run can consume more total tokens than a comparable single-agent run. Therefore the expected gain is **lower repeated bootstrap and lower coordinator context pollution**, not an automatic reduction in total token consumption.

### 1.3 Persistent long-running work is an intended Codex pattern

OpenAI's long-running-work guidance recommends keeping related multi-step work in the same chat so the agent can use accumulated context to choose the next step and decide when the work is complete. Codex CLI and the IDE support `/goal` for a durable objective in the same session.

This supports maintaining one root thread for a coherent workstream, provided that context hygiene prevents the persistent thread from becoming a transcript archive.

### 1.4 App Server provides explicit thread lifecycle primitives

Codex App Server exposes the primitives needed for a later programmatic implementation:

```text
thread/start
thread/resume
thread/fork
thread/read
thread/list
thread/name/set
thread/goal/set|get|clear
turn/start
turn/steer
```

A stored `thread.id` can be resumed later. `thread/fork` creates a new thread with copied history. `thread.sessionId` identifies the root of the active session tree. Goals are persisted and expose objective/status plus optional token-budget accounting.

This is materially better suited to a future Agent Governance session manager than parsing CLI transcripts or inventing an external memory layer.

Some App Server pagination/descendant-listing surfaces remain experimental. A first implementation should use only documented stable thread start/resume/read/fork/name/goal behavior that is actually supported by the selected Codex release, and must fail back to Git bootstrap when a runtime thread cannot be recovered.

### 1.5 Custom project agents exist, but should not be the first dependency

Codex supports project-scoped custom agents under `.codex/agents/*.toml`, including role description, developer instructions, model/reasoning overrides, sandbox, MCP and Skill configuration. OpenAI recommends narrow, opinionated agent roles and provides examples such as read-only explorers and reviewers.

However, OpenAI also warns that the custom-agent file shape may evolve as authoring/sharing mature. Agent Governance should therefore pilot the orchestration pattern with built-in `explorer` / `worker` roles and explicit bounded prompts before committing a large project-specific agent catalog.

If custom agents are later added, model names should normally remain adapter guidance rather than product correctness semantics, preserving D055's provider-neutral intent.

## 2. Why a permanent repository-wide chat would be the wrong design

A large context window is capacity, not reliable working memory.

Chroma's Context Rot research evaluated 18 model families and found performance becoming less reliable as input length increased even on controlled tasks. In its conversational LongMemEval experiment, focused prompts containing only relevant material substantially outperformed full histories containing irrelevant material. This supports retrieving/retaining only what the current reasoning step needs rather than accumulating all prior implementation traces.

OpenAI links directly to this context-rot research from its Codex subagent documentation.

Thoughtworks' 2026 “Orchestrator's Tax” field report reaches a compatible operational conclusion: the highest-value property of subagents is often what they keep **out** of the orchestrator's working memory. Pulling full worker transcripts back into the main thread creates a persistent tax on later decisions. The same report highlights duplicated orientation when work is split more finely than the underlying “cognitive locality” permits, overlapping writer risk, and the value of concise worker summaries.

Therefore the correct unit of persistence is a **coherent dossier/workstream**, not the entire Agent Governance repository and not every historical task forever.

## 3. Coding-specific lessons from long-running agent systems

Anthropic's long-running coding research is provider-specific but useful as independent harness evidence.

Their long-running-agent work repeatedly finds that durable external artifacts plus Git history allow fresh agents to recover state efficiently. Their 2026 harness work uses planner/generator/evaluator separation and structured contracts between stages. Their parallel C-compiler experiment shows the limits of indiscriminate parallelism: when many agents hit the same underlying bug, they duplicate work and overwrite one another; parallelism becomes useful again when the harness creates genuinely independent units.

The same C-compiler study recommends keeping test output terse and logging detail to files so model context does not fill with thousands of low-value bytes. That matches T050's agent-legible/code-health direction and the proposed coordinator rule that raw logs belong in evidence files or child contexts, not the root thread.

The general pattern is:

```text
persistent high-level coordination
+ bounded independent workers
+ deterministic verification
+ external durable artifacts
+ concise handoffs
```

This is already close to Agent Governance's Git-authoritative architecture.

## 4. Fit with current Agent Governance authority

### 4.1 D041 already permits internal multi-agent execution

D041 explicitly states that the Executor may choose private/internal planning, sub-agents/workers, Skills, navigation tools, testing/review helpers or other executor-native mechanisms. Internal worker state does not become Task Contract authority or Governance acceptance.

No D041 change is required merely to let Codex spawn subagents.

### 4.2 D053 remains unchanged

A persistent Codex root plus subagents remains entirely inside Executor-owned stages:

```text
Implement
Code Review & Verify
```

The root coordinator cannot authoritatively change Specify, Design, Plan & Trace or acceptance. If a child discovers a material upstream defect, the root must still stop/re-enter the Orchestrator rather than redesign the task internally.

### 4.3 D042 remains the anti-staleness boundary

Session persistence must never mean repository-state persistence.

Before the root coordinator starts a new governed work unit, it must perform the same D042 remote-freshness reconciliation required today:

```text
refresh canonical remote
-> establish safe local baseline
-> reload current AGENTS.md
-> reload current checkpoint / exact persisted authority
-> reconcile the retained coordinator summary with Git
-> execute
```

The benefit is that the root retains useful architectural/operational orientation while Git refresh invalidates stale authority.

Internal child spawns are implementation mechanics under D041, not new ChatGPT-to-Executor launches. They should receive a narrow pointer to the already-refreshed authoritative work and the exact bounded subtask. A child that creates or switches a separate worktree/branch must independently establish the required safe Git state for that worktree.

### 4.4 D055 is the policy that needs prospective refinement

Current D055 says `NEW` is the default for the first launch of a new Task Contract/work unit and `CONTINUE` is normally limited to the same represented Task Contract/branch.

That rule correctly optimized for the older topology where the human-visible Executor chat was also the implementation context.

A persistent coordinator design needs two separate lifecycles:

```text
Coordinator root session: may CONTINUE across related Task Contracts inside one continuity scope
Child implementation context: fresh/bounded per delegated work slice
```

The retained root should be allowed to continue across Task Contracts only after a **continuity reconciliation gate** proves that continued context is useful rather than contaminating.

The prospective gate should require at least:

1. same repository and same coherent continuity scope/dossier;
2. root thread is identifiable and recoverable;
3. D042 freshness and current instruction/authority reload succeeds;
4. new work does not require independent/cold-context evidence;
5. retained context is not materially stale, contradictory or dominated by unrelated work;
6. branch/worktree ownership can be established without conflicting writers;
7. the root can restate the new authoritative task pointer and current represented frontier before delegation.

Any failed condition selects a new coordinator root rather than attempting to preserve continuity at all costs.

## 5. Recommended Agent Governance topology

### 5.1 Persistent root coordinator

Maintain one root Codex thread for each explicit **Executor Continuity Scope**. In user-facing language this can correspond to an “expediente”: a chain of closely related Task Contracts that share product area, architecture and operational state.

The root should retain only:

- the current high-level objective;
- authoritative Git pointers, never copied authority as truth;
- accepted architectural constraints that remain relevant;
- represented branch/worktree map;
- short conclusions from completed child work;
- unresolved blockers and current next step;
- final results already represented in Git.

It should not retain raw test output, complete command logs, full file dumps, complete child transcripts, abandoned implementation traces or large copied Task Contract sections.

A short `/goal` can help the coordinator preserve the continuity objective, but the goal is host state only. Git remains authoritative and must be reloaded on every new governed work unit.

### 5.2 Fresh bounded children

Use child threads as disposable reasoning contexts.

Recommended initial functional roles are:

- **Explorer** — read-only code/evidence mapping, documentation or dependency research;
- **Worker** — the single writer for one bounded implementation slice/worktree;
- **Verifier/Reviewer** — independent read-only technical review, test-gap analysis or reproduction;
- **Specialist** — only when a narrow domain materially benefits from a different tool/model profile.

The root decides whether to delegate based on independence and cognitive locality, not because subagents are available.

### 5.3 One writer per mutable worktree

OpenAI recommends caution with write-heavy parallel agents, and independent coding-agent experience shows repository-wide operations and overlapping ownership become structural hazards under parallel writers.

Initial Agent Governance policy should therefore be:

```text
parallel read-heavy children: allowed when useful
parallel writers on same worktree/branch: forbidden
parallel writers on explicitly isolated worktrees/branches: pilot-only and only when file/semantic ownership is non-overlapping
```

The root remains responsible for the final represented branch and Executor handoff.

### 5.4 Summary-return contract

A child should normally return only:

```text
status
concise findings/result
files/symbols affected
verification performed
Git/evidence references when applicable
blocker or follow-up needed
```

The root should not request full transcripts for routine status checks. Detailed logs belong in files/evidence or remain in the child thread.

This is both a token-control mechanism and a context-quality mechanism.

## 6. Session persistence implementation options

### Phase 1 — native interactive Codex pilot

Use the supported interactive Codex surface first:

- one named root chat for one continuity scope;
- `/goal` for the high-level continuity objective;
- native subagents requested by the root;
- `/agent` only when human inspection of a child is needed;
- built-in agent roles initially;
- no new Agent Governance runtime code;
- no dependency on experimental Multi-Agent V2-specific configuration keys.

The public stable configuration surface should be preferred over undocumented/internal V2 knobs. A recent Codex GitHub issue notes differing concurrency semantics between public `[agents]` configuration and an explicit V2-specific setting, reinforcing the need to stay on the documented interface until it is clarified.

### Phase 2 — project-scoped agent profiles, if the pilot proves value

Add a minimal `.codex/agents/` catalog only for roles that repeatedly demonstrate value. Keep the catalog small and role-oriented.

Do not hard-code expensive models merely because an agent has a particular name. Let D055/current adapter guidance choose minimum sufficient compute, with read-only explorer work biased toward lower-cost tiers and difficult verifier/worker tasks escalated only when justified.

### Phase 3 — App Server session manager

If manual root persistence is valuable but operationally awkward, build a small local Executor adapter around Codex App Server.

A local registry can map:

```text
(repository, continuity_scope) -> root threadId
```

The adapter can then:

1. `thread/read` or `thread/resume` the root;
2. set a human-readable thread name;
3. refresh Git/current authority;
4. update the root goal to the current continuity objective;
5. start the next turn;
6. use native subagents during the turn;
7. persist only operational session metadata locally;
8. fall back to `thread/start` + Git bootstrap if resume fails.

Thread IDs should normally remain local/runtime metadata, not committed product authority. Losing the registry must degrade only performance, never correctness: a fresh root can reconstruct the frontier from Git.

## 7. Known Codex operational risks

Current Codex issue reports show why the root-only persistence model should be conservative.

Recent reports include subagent JSONL history causing disk growth, resumed roots being unable to resume prior subagents in some Multi-Agent V2 versions, completed threads failing resume/fork on some platforms, and long goal sessions hitting subagent-thread limits when completed children remain open.

These are issue reports, not normative product guarantees, and some have been closed/fixed. They nevertheless support four design choices:

- persist the **root**, not the entire child tree as a correctness dependency;
- close completed children after their result has been summarized;
- keep Git/evidence as recovery state;
- treat thread persistence as an optimization that can fail safely.

## 8. Context and concurrency controls for the pilot

Do not maximize concurrency by default.

A reasonable first pilot is one root plus at most **three concurrently open child threads**, normally with only one write-capable child. This is a pilot control, not a universal product constant. It is intentionally below the large examples in vendor documentation because Agent Governance work often has shared architecture and branch state.

The root should prefer delegation when at least one of these is true:

- the work is independently verifiable/read-heavy;
- a child can keep substantial noisy exploration out of the root;
- a specialist can operate with a materially narrower context/toolset;
- independent review benefits from not inheriting the worker's reasoning path;
- parallel execution materially reduces wall time without overlapping ownership.

Keep work in the root when tasks require the same mental model, touch the same files/state, depend serially on one another or would force several children to repeat the same orientation.

## 9. Cost model and telemetry

The pilot should test the actual hypothesis instead of assuming that multi-agent means cheaper.

Measure per governed work unit:

| Measure | Why it matters |
| --- | --- |
| Root input/output/reasoning tokens | Detect coordinator-context growth |
| Child input/output/reasoning tokens | Quantify delegation amplification |
| Total tokens | Compare true spend against fresh-session baseline |
| Time to first useful technical action | Measure bootstrap savings |
| Repeated instruction/file reads | Measure duplicate orientation |
| Root context occupancy before/after | Detect context accumulation |
| Number and reason for child spawns | Detect over-delegation |
| Child failures/retries | Detect coordination overhead |
| Compaction events | Detect root pressure |
| Review rework / acceptance outcome | Prevent optimizing cost at quality expense |
| Wall-clock completion time | Quantify useful parallelism |

The optimization objective should be:

```text
minimum sufficient total compute
+ lower repeated bootstrap
+ lower root context pollution
+ equal-or-better accepted quality
```

not simply “fewest sessions”.

## 10. Proposed pilot acceptance criteria

A prospective Agent Governance pilot should compare several related work units using the persistent coordinator pattern against recent fresh-session behavior.

Adopt/refine the pattern only if evidence shows:

- lower repeated bootstrap/orientation effort;
- no stale-authority or branch-safety incidents;
- root context remains compact enough to improve rather than degrade reasoning;
- no increase in semantic rework attributable to delegated context loss;
- total token cost remains acceptable relative to quality/time benefit;
- D042 reconciliation reliably invalidates stale chat assumptions;
- loss of root/child runtime state can be recovered from Git without authority loss.

If persistence reduces bootstrap but the root accumulates enough noise to increase rework, the correct response is a smaller continuity scope or deliberate root renewal, not unlimited compaction of an eternal chat.

## 11. Recommended prospective governance change

After the currently running T023/MG1-v12 work is converged, create a dedicated source-maintenance pilot rather than changing D055 immediately during an active Executor run.

The pilot should prospectively refine D055 along these lines:

```text
Human-visible Executor continuity has two levels:

1. Coordinator Root
   - NEW when a continuity scope starts or reconciliation fails.
   - CONTINUE across related Task Contracts only when the continuity gate passes.

2. Internal Child
   - fresh bounded subagent context by default;
   - no Human D055 launch card for each internal spawn;
   - remains private Executor process under D041.
```

D042 remains mandatory for every Human-to-Executor governed work-unit launch/continuation. Child spawning does not create a second Governance lifecycle.

No Governance Core protocol change is required for the initial source-product pilot. If the pattern later proves portable and materially useful for consumers using persistent coding agents, portability can be considered separately.

## 12. Recommendation

Proceed with a controlled pilot.

The strongest version of the proposal is:

> Maintain one clean Codex coordinator root per coherent Agent Governance execution dossier, rehydrate authority from Git before every governed work unit, and delegate disposable implementation/research/review work to fresh bounded subagents that return concise evidence references rather than transcripts.

This architecture uses Codex's current stable multi-agent and goal capabilities while preserving the central Agent Governance invariant that **Git is durable authority and chat is replaceable execution state**.

The likely improvement is meaningful: repeated architecture/orientation context can stay warm in the root while expensive noisy reasoning is isolated in children. But the value must be measured because multi-agent execution can spend more tokens overall, and an overgrown persistent root recreates the exact context problem the design is meant to solve.

## Primary sources

### OpenAI / Codex

- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/long-running-work
- https://learn.chatgpt.com/docs/app-server
- https://learn.chatgpt.com/docs/config-file/config-reference
- https://learn.chatgpt.com/docs/codex-sdk
- https://developers.openai.com/blog/codex-as-a-platform
- https://developers.openai.com/blog/automating-repetitive-work-at-openai-with-codex

### Context / coding-agent research

- https://www.trychroma.com/research/context-rot
- https://martinfowler.com/articles/orchestrator-tax.html
- https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- https://www.anthropic.com/engineering/harness-design-long-running-apps
- https://www.anthropic.com/engineering/building-c-compiler
- https://www.anthropic.com/engineering/multi-agent-research-system

### Codex issue evidence used only as operational risk signals

- https://github.com/openai/codex/issues/30779
- https://github.com/openai/codex/issues/33002
- https://github.com/openai/codex/issues/32035
- https://github.com/openai/codex/issues/20908
- https://github.com/openai/codex/issues/40211
