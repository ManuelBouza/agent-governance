# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O198  
Canonical-Branch: `develop`  
Current-Work-Unit: T053 is accepted and integrated; T054 adaptive subagent compute routing pilot is authorized after this checkpoint/task branch is integrated  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: fresh T054 calibration root

## Durable frontier

- D039, D041, D042, D053, D054, D055 and D056 remain controlling. Core protocol remains `1.15.0`.
- T050 is `ACCEPTED`; code-health/symbol-map boundary remains active.
- T023/MG1-v12 remains closed as valid `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE`; review `docs/reviews/T023-R11.md`. No MG1-v13 is authorized.
- Adaptive child-compute research: `docs/research/ADAPTIVE-SUBAGENT-COMPUTE-ROUTING-RESEARCH.md`.
- D055 remains unchanged. Root launch guidance and child compute routing remain separate layers.

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

Accepted technical result:

```text
tools/repository_context.py              1117 -> 232 LOC
tests/test_repository_context.py        1540 -> 233 LOC
full pytest                              491 PASS
focused repository-context/code-health    65 PASS
Ruff / format / code-health / symbol map / cycle checks / diff-check PASS
```

All extracted runtime and focused test modules are below `500` LOC; old `1117`/`1540` ratchets are replaced by final `232`/`233` values. No Executor-authored Markdown or Governance Core change occurred.

### T053 coordinator conclusion

Persistent-root coordination is supported for further controlled evaluation:

- original root continued `NEW -> CONTINUE` across the Orchestrator barrier;
- D042/current Git authority passed in both phases;
- one-writer invariant held and branch/worktree incidents were `0`;
- Phase-1 children were not reused;
- retained concise Phase-1 summaries avoided rereading the `915`-line Phase-1 facade, `1536`-line test module, child transcripts and raw logs before fresh Phase-2 exploration;
- final technical quality improved materially.

Observability limit: the host exposed neither an immutable root fingerprint nor attributable root/child token/context metrics. T053 therefore supports a qualitative context-locality/reduced-reread claim, **not a quantitative token/cost/compute-saving claim**.

The merged implementation topic branch `refactor/t053-repository-context-coordinator-pilot` was still present when final review was prepared. It is frozen at the reviewed head and remains a cleanup candidate under `docs/BRANCHING.md`; the current Orchestrator GitHub surface does not expose branch deletion.

## T054 executable identity

Task Contract: `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md`.

T054 is a separate read-only matched-arm calibration. It does not modify product code or persistent-root policy.

Human-visible D055 root launch profile:

```text
Executor: Codex
Session: NEW
Model: GPT-5.6 Sol
Effort: High
Task: T054
Expected evidence branch: test/t054-adaptive-subagent-compute-routing-pilot
```

Rationale: the fresh root coordinates the experiment and supplies the fixed root-equivalent CONTROL baseline; the experimental variable is child compute selection.

### Frozen T054 experiment

After D042 and host capability preflight, use six fresh read-only children in three matched pairs:

```text
P1 deterministic inventory
  CONTROL: inherited root-equivalent Sol/High, fork_turns=none
  ADAPTIVE: GPT-5.6 Luna / Low, fork_turns=none

P2 dependency + symbol mapping
  CONTROL: inherited root-equivalent Sol/High, fork_turns=none
  ADAPTIVE: GPT-5.6 Terra / Medium, fork_turns=none

P3 adversarial independent review
  CONTROL: inherited root-equivalent Sol/High, fork_turns=none
  ADAPTIVE: GPT-5.6 Terra / High, fork_turns=none
```

All children are read-only; maximum concurrently open children is `2`; no child reuse; no `.codex/agents/` catalog. Matched pair task content/tool access must remain equivalent. P1/P2 use deterministic root-computed oracles. P3 uses the frozen temporary fixed-package-name isolation defect outside tracked repository state.

Required evidence:

- capability preflight for model/reasoning/fork/service-tier controls and effective-profile/token observability;
- requested **and effective** child model/reasoning/service-tier where observable;
- `fork_turns`, timestamps/duration, token metrics where exposed;
- first-attempt oracle result for each arm;
- escalation/retry evidence without overwriting original failures;
- final pilot decision exactly one of `QUALIFIED`, `QUALIFIED_QUALITY_OBSERVABILITY_LIMITED`, `NOT_QUALIFIED`, `BLOCKED_CAPABILITY`;
- no quantitative savings claim without effective-profile/usage evidence.

Persist only authorized non-Markdown evidence:

- `handoffs/T054-adaptive-routing-telemetry.json`;
- `handoffs/T054-executor-handoff.json`.

## Next action

1. Integrate this O198/T054 specification branch into `develop` before Executor launch.
2. Human starts a **NEW** Codex root for T054.
3. Show D055: Codex / NEW / GPT-5.6 Sol / High.
4. Send pointer-only transport to current `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md` on canonical `develop`.
5. Executor runs T054 exactly as frozen and returns terminal handoff fields only.
6. Orchestrator converges the evidence from GitHub before any D055, child-routing adapter, or consumer-portability policy change.
7. Do not launch MG1-v13 concurrently.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not treat session memory as authority; do not bypass D042; do not reuse the T053 root for T054; do not mutate tracked product code in T054; do not permit write-capable T054 children; do not leak the P3 oracle into child prompts; do not add a `.codex/agents/` catalog solely for T054; do not silently substitute Sol for a lower-tier ADAPTIVE arm and count it as successful routing; do not infer effective model/effort or tokens when the host does not expose them; do not change D055 or consumer policy before T054 convergence; do not rerun MG1-v12 or launch V13.
