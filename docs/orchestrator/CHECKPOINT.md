# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O200  
Canonical-Branch: `develop`  
Current-Work-Unit: T053 accepted/integrated; T054 adaptive subagent compute routing pilot specified but not yet executed; D057 research-to-decision traceability is now controlling  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: fresh T054 calibration root

## Durable frontier

- D039, D041, D042, D053, D054, D055, D056 and D057 are controlling. Core protocol remains `1.15.0`.
- D057 research-to-decision traceability: `docs/decisions/D057-research-decision-traceability.md`.
- Canonical research ledger: `docs/RESEARCH-TRACEABILITY.md`.
- Research findings are evidence, not normative authority. `Research-State` and `Decision-State` are independent and only persisted Git transitions change them.
- T050 is `ACCEPTED`; code-health/symbol-map boundary remains active.
- T023/MG1-v12 remains closed as valid `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE`; no MG1-v13 is authorized.
- D055 remains unchanged as global Human-facing Executor launch-profile policy.

## Live research frontier

The complete research history is in `docs/RESEARCH-TRACEABILITY.md`. Only currently operational research is repeated here.

### R006 — persistent Executor coordinator

```text
Research: docs/research/CODEX-PERSISTENT-EXECUTOR-COORDINATOR-RESEARCH.md
Research-State: COMPLETE
Decision-State: EVALUATING
Evaluation: T053 accepted
Decision-Ref: none
```

T053 provides positive qualitative evidence for persistent-root context locality and reduced rereading. It does not establish a quantitative token/cost saving and does not by itself modify D055's session policy.

### R007 — adaptive subagent compute routing

```text
Research: docs/research/ADAPTIVE-SUBAGENT-COMPUTE-ROUTING-RESEARCH.md
Research-State: COMPLETE
Decision-State: EVALUATING
Evaluation: T054 specified, not yet executed
Decision-Ref: none
```

No global child-routing/model/effort policy has been accepted. T054-specific model/effort choices are frozen experimental controls only.

## T053 final state

T053 is **ACCEPTED**.

Authoritative records:

- Task Contract: `docs/tasks/T053-codex-persistent-executor-coordinator-pilot.md`;
- Phase-1 review: `docs/reviews/T053-P1.md`;
- final review: `docs/reviews/T053-R1.md`;
- final handoff: `handoffs/T053-executor-handoff.json`;
- telemetry: `handoffs/T053-pilot-telemetry.json`;
- submitted Executor HEAD: `fc972e0075463f17e820ea41ac1074b3394145b6`;
- implementation PR: `#273`;
- integrated technical commit: `9a7e4de08b7b3bece5883bd33d0a4aa2fa247c97`.

Accepted result:

```text
tools/repository_context.py              1117 -> 232 LOC
tests/test_repository_context.py        1540 -> 233 LOC
full pytest                              491 PASS
focused repository-context/code-health    65 PASS
Ruff / format / code-health / symbol map / cycle checks / diff-check PASS
```

Persistent-root coordination remains an evaluated hypothesis with positive qualitative evidence, not yet a global policy decision.

## T054 executable identity

Task Contract: `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md`.

T054 has **not been launched**. No experimental evidence exists yet.

Frozen Human-visible root profile:

```text
Executor: Codex
Session: NEW
Model: GPT-5.6 Sol
Effort: Medium
Task: T054
Expected evidence branch: test/t054-adaptive-subagent-compute-routing-pilot
```

O198's earlier T054-specific `Sol / High` guidance was superseded before execution. The corrected `Sol / Medium` baseline is canonical.

Rationale: Sol supplies coordinator capability; Medium is the proportionate balanced baseline. High is not justified merely by coordinator role and remains selective for bounded tasks whose complexity/review/security/eval evidence warrants it.

Do not change the root model/effort mid-pilot. If the root cannot coordinate at the frozen profile, stop for Orchestrator re-entry rather than silently escalating and contaminating the comparison.

## Frozen T054 experiment

T054 is a read-only matched-arm calibration. It does not modify product code, persistent-root policy, D055 or global child-routing policy.

After D042 and host capability preflight, use six fresh read-only children in three matched pairs:

```text
P1 deterministic inventory
  CONTROL: inherited root-equivalent GPT-5.6 Sol / Medium, fork_turns=none
  ADAPTIVE: GPT-5.6 Luna / Low, fork_turns=none

P2 dependency + symbol mapping
  CONTROL: inherited root-equivalent GPT-5.6 Sol / Medium, fork_turns=none
  ADAPTIVE: GPT-5.6 Terra / Medium, fork_turns=none

P3 adversarial independent review
  CONTROL: inherited root-equivalent GPT-5.6 Sol / Medium, fork_turns=none
  ADAPTIVE: GPT-5.6 Terra / High, fork_turns=none
```

P3 deliberately allows higher reasoning on a lower model tier; the hypothesis is task-appropriate compute allocation, not monotonic reduction of every parameter.

Safety/experimental envelope:

- one NEW Human-visible Codex root;
- exactly six fresh read-only matched children unless capability-blocked;
- maximum `2` concurrently open children;
- no write-capable child;
- no child reuse;
- no `.codex/agents/` catalog;
- matched task content, repository/fixture input and tool access equivalent;
- `fork_turns=none` for all matched children;
- P1/P2 deterministic root-computed oracles;
- P3 frozen temporary fixed-package-name isolation defect outside tracked repository state;
- preserve all first-attempt failures and any escalation evidence;
- no quantitative savings claim without effective-profile and attributable usage evidence.

Persist only authorized non-Markdown evidence:

- `handoffs/T054-adaptive-routing-telemetry.json`;
- `handoffs/T054-executor-handoff.json`.

Final pilot decision remains exactly one of:

```text
QUALIFIED
QUALIFIED_QUALITY_OBSERVABILITY_LIMITED
NOT_QUALIFIED
BLOCKED_CAPABILITY
```

These are T054 pilot outcomes. After convergence, D057 requires an explicit research-ledger transition and an accepted normative decision before any result is described as global Agent Governance policy.

## Research traceability operating rule

For every future material investigation:

1. persist the research under `docs/research/` with the next `Rxxx` identity and D057 metadata;
2. update `docs/RESEARCH-TRACEABILITY.md` in the same change set;
3. keep `Research-State` separate from `Decision-State`;
4. link Task Contract/eval/review when the hypothesis moves to `EVALUATING`;
5. do not claim `DECIDED` without explicit accepted normative authority and a registry transition;
6. persist `DEFERRED`, `REJECTED` or `SUPERSEDED` with reason/reference;
7. preserve prior research rather than rewriting history to fit later conclusions;
8. revalidate volatile external evidence before decision promotion.

Research that exists only in chat is not durable project evidence and must not control downstream work.

## Next action

1. Human starts a **NEW** Codex root for T054.
2. Show launch profile: Codex / NEW / GPT-5.6 Sol / Medium.
3. Send pointer-only transport to current `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md` on canonical `develop`.
4. Executor runs T054 exactly as frozen and returns terminal handoff fields only.
5. Orchestrator converges T054 evidence from GitHub.
6. During convergence, update R007 in `docs/RESEARCH-TRACEABILITY.md` to the resulting durable disposition. Do not call it `DECIDED` unless a separate accepted normative decision is created.
7. Consider R006 persistence policy disposition at the same evidence boundary; no implicit D055 change.
8. Do not launch MG1-v13 concurrently.

## Next chat minimum load

Load current `develop` identity, `AGENTS.md`, and this checkpoint.

Then:

- if the request concerns research, evidence synthesis, policy adoption or whether something was decided, load D057 plus `docs/RESEARCH-TRACEABILITY.md`;
- if executing/converging T054, load `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md` and the relevant handoff/evidence when it exists;
- load no additional project history unless a concrete conflict requires it.

## Do not

Do not treat research conclusions as normative decisions; do not alter Research/Decision state only in chat; do not use O198's superseded `Sol/High` T054 launch profile; do not treat session memory as authority; do not bypass D042; do not reuse the T053 root for T054; do not mutate tracked product code in T054; do not permit write-capable T054 children; do not leak the P3 oracle into child prompts; do not add a `.codex/agents/` catalog solely for T054; do not silently substitute Sol for a lower-tier ADAPTIVE arm and count it as successful routing; do not infer effective model/effort or tokens when the host does not expose them; do not change D055 or consumer policy before explicit post-evaluation decision convergence; do not rerun MG1-v12 or launch V13.
