# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O202  
Canonical-Branch: `develop`  
Current-Work-Unit: R008 Codex child-observability research is complete and under T055 evaluation; T055 child observability qualification is specified but not yet executed  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: fresh T055 qualification root after this Markdown branch is integrated

## Durable frontier

- D039, D041, D042, D053, D054, D055, D056 and D057 remain controlling. Core protocol remains `1.15.0`.
- D057 research-to-decision traceability: `docs/decisions/D057-research-decision-traceability.md`.
- Canonical research ledger: `docs/RESEARCH-TRACEABILITY.md`.
- T050 remains `ACCEPTED`; code-health/symbol-map boundary remains active.
- T023/MG1-v12 remains closed as valid `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE`; no MG1-v13 is authorized.
- D055 remains unchanged as the global Human-facing Executor launch-profile policy.
- T054 remains accepted as an execution with frozen pilot outcome `NOT_QUALIFIED`; do not rerun it unchanged.

## R008 — Codex child observability surface

```text
Research: docs/research/CODEX-CHILD-OBSERVABILITY-SURFACE-RESEARCH.md
Research-State: COMPLETE
Decision-State: EVALUATING
Evaluation: docs/tasks/T055-codex-child-observability-qualification.md
Decision-Ref: none
```

R008 refreshed the current Codex surface on 2026-09-05 using public OpenAI documentation and the official `openai/codex` repository.

Characterized identities:

```text
openai/codex current main:
  ddf04ad26789d040f9ef6a96736f76602e35a6cc

latest stable Codex release:
  0.153.4
  release commit: 3d2ee51ca2d5db578f328aa75e20aa22c0197c9a
  published: 2026-09-04
```

### R008 finding

Current Codex App Server / stable Python SDK expose a materially stronger measurement surface than the direct parent-facing collaboration return used by T054.

Supported/relevant current surfaces include:

- child `Thread` records with `parentThreadId`, `modelProvider`, configured/persisted `model`, configured/persisted `reasoningEffort`, source, role/nickname and CLI version;
- `thread/list` over subagent source kinds;
- experimental direct relationship filters `parentThreadId` / `ancestorThreadId`;
- thread start/resume sandbox responses;
- `thread/tokenUsage/updated` with exact `threadId`, `turnId` and token breakdown;
- child turn timestamps/duration;
- public stable Python SDK `TurnResult.usage` for SDK-run turns;
- `model/rerouted` event as an exception/reroute signal.

Important claim boundary:

```text
Thread.model / Thread.reasoningEffort
  = configured/persisted thread profile
  != per-turn provider execution receipt
```

Therefore future telemetry must distinguish:

```text
requested_profile
resolved_thread_profile
reroute_observed
backend_served_profile
```

R008 does not establish an authoritative per-turn provider-served model/reasoning receipt. That stronger field remains unverified unless a live public host exposes one.

The direct parent-facing MultiAgentV2 activity record remains insufficient by itself. The improvement is the separate supported child-thread/App-Server query and usage surface.

## Research dispositions

### R006 — persistent Executor coordinator

```text
Research-State: COMPLETE
Decision-State: DEFERRED
Decision-Ref: none
```

T053 remains positive qualitative context-locality evidence; no global D055 persistence-session change is adopted.

### R007 — adaptive subagent compute routing

```text
Research-State: COMPLETE
Decision-State: DEFERRED
Evaluation: T054 accepted / NOT_QUALIFIED
Decision-Ref: none
```

R008 does **not** reactivate R007. A corrected routing evaluation may be specified only after T055 qualifies the measurement substrate and the Orchestrator persists a new R007 transition.

### R008 — child observability

```text
Research-State: COMPLETE
Decision-State: EVALUATING
Evaluation: T055 planned
Decision-Ref: none
```

The research conclusion is sufficient to authorize a bounded live observability qualification, not a routing pilot or policy change.

## T055 executable identity

Task Contract: `docs/tasks/T055-codex-child-observability-qualification.md`.

T055 is a read-only host/App-Server observability qualification. It does not compare CONTROL/ADAPTIVE quality and makes no savings claim.

Human-visible launch profile after this specification branch is integrated:

```text
Executor: Codex
Session: NEW
Model: GPT-5.6 Sol
Effort: Medium
Expected evidence branch: test/t055-codex-child-observability-qualification
```

Rationale: bounded protocol/host qualification requiring reliable version, App Server/SDK, thread-correlation and evidence work. Medium remains the proportionate default.

### T055 live qualification target

T055 creates one disposable App-Server/SDK-managed read-only parent and requires one real multi-agent child:

```text
parent:
  GPT-5.6 Sol / Medium
  read-only

child:
  task: t055_observability_child
  requested model: GPT-5.6 Terra or documented current equivalent
  requested reasoning: Low
  fork_turns: none
  deterministic bounded nonce task
```

The qualification then must correlate that exact child to:

- child thread ID + parent relationship;
- resolved/configured child model/reasoning from supported thread state;
- non-write child sandbox receipt;
- child-attributable `thread/tokenUsage/updated` token breakdown;
- child-attributable duration;
- exact installed Codex/App Server/SDK version provenance;
- reroute signal if observable;
- backend-served profile receipt only if a genuinely stronger public receipt exists.

Internal SQLite/JSONL inspection may be diagnostic only and cannot upgrade a qualification result.

The Executor may use an isolated temporary SDK environment outside the repository if needed, but MUST NOT change repository dependencies or globally upgrade Codex merely to make the task pass.

### T055 frozen decisions

Exactly one:

```text
QUALIFIED_STABLE_SURFACE
QUALIFIED_WITH_EXPERIMENTAL_DISCOVERY
PARTIAL_OBSERVABILITY
BLOCKED_CAPABILITY
```

Passing qualification requires a real spawned child, supported child relationship/profile/sandbox receipts, child-thread/turn-attributable non-estimated token usage, duration and complete version provenance.

Provider-served per-turn model/reasoning identity is not required for T055 qualification, but it must remain explicitly unverified unless a stronger public receipt is actually obtained.

Persist only:

- `handoffs/T055-child-observability-telemetry.json`;
- `handoffs/T055-executor-handoff.json`.

No product code, Markdown, persistent `.codex/agents/` catalog, product dependency, D055, routing policy or Governance Core mutation is authorized.

## Next action

1. Integrate this R008/T055 Markdown specification branch into `develop`.
2. Human starts a **NEW** Codex root for T055.
3. Show D055 launch profile: Codex / NEW / GPT-5.6 Sol / Medium.
4. Send pointer-only transport to current `docs/tasks/T055-codex-child-observability-qualification.md` on canonical `develop`.
5. Executor runs T055 exactly as frozen and returns only terminal handoff fields.
6. Orchestrator converges T055 evidence from GitHub.
7. Under D057, transition R008 from `EVALUATING` to an explicit durable disposition.
8. Only if T055 qualifies the measurement surface may the Orchestrator consider returning R007 to `EVALUATING` and specifying a corrected routing successor. Do not do so implicitly.
9. Do not launch MG1-v13 concurrently.

## Next chat minimum load

Load current `develop` identity, `AGENTS.md`, and this checkpoint.

Then follow `Next action`. Load R008/T055 only as directly referenced by that action. Load T054 review only if exact predecessor limitations are needed.

## Do not

Do not rerun T054 unchanged. Do not claim that configured `Thread.model` / `reasoningEffort` prove the backend-served model for every response. Do not estimate child tokens. Do not use private SQLite/JSONL as a passing telemetry dependency. Do not globally upgrade Codex to make T055 pass. Do not add repository SDK dependencies for T055. Do not change D055, persistence policy, consumer policy or global child-routing policy. Do not reactivate R007 without a persisted D057 transition after T055 convergence. Do not rerun MG1-v12 or launch V13.
