# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O199  
Canonical-Branch: `develop`  
Current-Work-Unit: T053 is accepted/integrated; T054 adaptive subagent compute routing pilot is specified but not yet executed, with corrected root baseline `GPT-5.6 Sol / Medium`  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: fresh T054 calibration root

## Durable frontier

- D039, D041, D042, D053, D054, D055 and D056 remain controlling. Core protocol remains `1.15.0`.
- T050 is `ACCEPTED`; code-health/symbol-map boundary remains active.
- T023/MG1-v12 remains closed as valid `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE`; no MG1-v13 is authorized.
- Adaptive child-compute research: `docs/research/ADAPTIVE-SUBAGENT-COMPUTE-ROUTING-RESEARCH.md`.
- D055 remains unchanged as global policy. T054's Human-facing root profile is an experiment-specific launch choice; child routing remains a separate layer.

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

Persistent-root coordination is supported for further controlled evaluation on qualitative context-locality evidence. T053 does not support a quantitative token/cost claim because the host did not expose attributable root/child usage metrics.

## T054 correction status

Task Contract: `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md`.

T054 had **not been launched** when the coordinator-effort question was re-evaluated. Therefore no evidence is invalidated and no experimental run must be discarded.

O198's T054-specific `GPT-5.6 Sol / High` root guidance is superseded before execution.

Corrected frozen root profile:

```text
Executor: Codex
Session: NEW
Model: GPT-5.6 Sol
Effort: Medium
Task: T054
Expected evidence branch: test/t054-adaptive-subagent-compute-routing-pilot
```

Rationale: use Sol for coordinator capability but Medium as the proportionate balanced reasoning baseline. High is not justified merely by the coordinator role; it remains appropriate when a bounded task's complexity, verification burden, edge cases, security risk, or measured eval result warrants it.

Do not change the root model/effort mid-pilot. If the root itself cannot coordinate at the frozen profile, stop for Orchestrator re-entry rather than silently escalating and contaminating the matched comparison.

## Frozen T054 experiment

T054 remains a separate read-only matched-arm calibration. It does not modify product code, persistent-root policy, or D055.

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

## Next action

1. Integrate this O199/T054 correction into `develop` before Executor launch.
2. Human starts a **NEW** Codex root for T054.
3. Show launch profile: Codex / NEW / GPT-5.6 Sol / Medium.
4. Send pointer-only transport to current `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md` on canonical `develop`.
5. Executor runs T054 exactly as frozen and returns terminal handoff fields only.
6. Orchestrator converges evidence from GitHub before any D055, child-routing adapter, or consumer-portability policy change.
7. Do not launch MG1-v13 concurrently.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not use O198's superseded `Sol/High` T054 launch profile; do not treat session memory as authority; do not bypass D042; do not reuse the T053 root for T054; do not mutate tracked product code in T054; do not permit write-capable T054 children; do not leak the P3 oracle into child prompts; do not add a `.codex/agents/` catalog solely for T054; do not silently substitute Sol for a lower-tier ADAPTIVE arm and count it as successful routing; do not infer effective model/effort or tokens when the host does not expose them; do not change D055 or consumer policy before T054 convergence; do not rerun MG1-v12 or launch V13.
