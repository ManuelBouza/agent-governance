# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O194  
Canonical-Branch: `develop`  
Current-Work-Unit: T023/MG1-v12 is closed with a valid `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE` result; next Orchestrator work is the requested Codex persistent-coordinator pilot specification before any normative D055 change  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: ChatGPT Orchestrator

## Durable frontier

- D053, D054, D040, D041, D042, D048, D050, D051, D052, D055 and D056 remain controlling. Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`.
- T050 is `ACCEPTED`; review `docs/reviews/T050-R1.md`; integration PR `#258`, merge `b8eae481e65e0aefc690b666e5eed6d01be85ea4`.
- T050 code-health boundary remains active: `evals/skill_activation_topology/harness.py` ratcheted at `212` LOC, extracted modules governed by size/complexity/dependency checks, deterministic AST symbol map available.
- T023 v2-v11 remain closed according to reviews `T023-R1.md` through `T023-R10.md`.
- T052/MG1-v12 controlling specification remains `docs/tasks/T052-mg1-v12-pair-scoped-scheduler-restart.md`.
- V12 convergence review: `docs/reviews/T023-R11.md`.
- V12 evidence/infrastructure integration PR `#266`; merge `2abc33ad954dbca81975b653bc0a607abdd32f8f`.
- Codex persistent-coordinator research memo: `docs/research/CODEX-PERSISTENT-EXECUTOR-COORDINATOR-RESEARCH.md`; research PR `#265`, merge `91f62278e439be8f5eb7e50c3f6aaac9331fa99e`.
- The persistent-coordinator memo is `RESEARCH / NON-CONTROLLING`; D055 has not yet changed.

## MG1-v12 terminal result

MG1-v12 is closed as a **valid experimental result**:

`BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE`.

Submitted Executor identity:

```text
Branch: test/t023-skill-activation-topology-evals-v12
Canonical execution base: 2696378eb7aef2815cca393102d53f6e25367f29
Live runner: 7b79ba6589becea6d71ab95c7c36e2e158225675
Implementation/evidence HEAD: 32fee8e50ee2fb59c6a9fcc147777f0c2b356e10
Terminal HEAD: 3e5bec392d0b8e5804c4efaad74b795b08dc9779
Handoff: handoffs/T023-executor-handoff.json
Evidence: evals/skill_activation_topology/evidence/mg1-v12-codex-windows-gpt-5.6-sol-medium/
```

V12 successfully established the execution method that prior epochs had failed to prove:

- deterministic/code-health/symbol-map gates PASS;
- focused tests PASS: `77`;
- full pytest PASS: `488`;
- provider-free adaptive-scheduler simulation PASS, including full `160`-observation B0/B1 dry run with zero provider/model calls;
- pair-scoped conditional-third behavior PASS;
- provider-free Windows workspace gate PASS;
- unchanged synthetic Skill canary PASS `2/2`;
- accepted live profile: Codex CLI `0.149.0`, native Windows 11, `elevated/read-only`, inherited-ACL workspace, GPT-5.6 Sol / Medium;
- no capacity event and no post-preflight host-surface drift.

V12 issued `72` fresh acceptance prompts and produced `72` valid observations. Two conditional third repetitions were required. No prior-epoch observation entered V12 scoring or futility state.

## Reference-family result

Both single-family reference candidates are terminally non-qualifying under the frozen V12 thresholds.

### B0

- terminal certificate: `FUTILE_QUALIFICATION`;
- one false activation among `11` negative/near-miss cases;
- false activation case: `WM02`;
- `WM02` is the near-miss asking for a maintainer policy for an unrelated Go library;
- host-observed entrypoint: `agent-governance` despite expected entrypoint set being empty;
- best possible final false-activation rate: `1/11 = 0.090909...`;
- frozen maximum: `0.05`.

### B1

- terminal certificate: `FUTILE_QUALIFICATION`;
- one false activation among `11` negative/near-miss cases;
- false activation case: `WM05`;
- `WM05` asks for a linting Skill while explicitly stating Agent Governance is not installed;
- host-observed entrypoint: `agent-governance-router` despite expected entrypoint set being empty;
- best possible final false-activation rate: `1/11 = 0.090909...`;
- frozen maximum: `0.05`.

For both candidates the frozen false-activation denominator is fixed. No future unfinished case can reduce `1/11` to `<=0.05`; qualification is mathematically impossible.

The terminal failed bound is `false_activation_rate`. Other optimistic qualification bounds do not reverse the result.

## D050 consequence

D050 requires at least one qualifying B0/B1 reference before challenger execution.

Therefore:

```text
B0 -> FUTILE_QUALIFICATION
B1 -> FUTILE_QUALIFICATION
F2 -> NOT_SCHEDULED_NO_REFERENCE
G3 -> NOT_SCHEDULED_NO_REFERENCE
selected topology -> none
```

F2/G3 are **not** behaviorally accepted or rejected by V12. Their non-execution is a D050 consequence, not evidence against them.

Do not run challengers outside D050 merely to obtain a result.

## Post-live verifier note

The immutable live runner was `7b79ba6589becea6d71ab95c7c36e2e158225675`.

After live execution the only technical-code change before the reviewed evidence HEAD was in `evals/skill_activation_topology/_harness/provenance.py`, plus evidence persistence. The live runner's generic verification path incorrectly assumed full reference-stage completion even when adaptive futility legitimately produced `BLOCKED_NO_REFERENCE`.

The post-live verifier correction:

- did not change aggregation, scheduling, scoring or futility semantics;
- did not alter raw observations or frozen D052 assets;
- did not issue additional model observations;
- independently recomputes finalized aggregates, both futility certificates, blocked reference state and final selection.

`T023-R11.md` accepts this as Code Review & Verify plumbing, not retrospective experimental redesign/rescoring.

## MG1 re-entry boundary

MG1 re-enters `Explore / Specify`, not another execution epoch.

V12 is the first recent epoch whose terminal blocker is accepted candidate/topology behavior rather than host/method/adapter failure.

Any future MG1 work must therefore investigate the design problem revealed by near-miss overactivation before authorizing another acceptance run.

Potential research questions include:

- why unified reference descriptions activate on unrelated `maintainer` language (`WM02`);
- why thin-router wording activates on generic `Skill`/linting language when Agent Governance is explicitly absent (`WM05`);
- whether a revised reference-family trigger contract can preserve positive/source/consumer coverage while tightening near-miss precision;
- whether D050's requirement for a qualifying single-family reference still represents the desired product-selection question after this substantive result.

No automatic V13 is authorized.

A candidate/presentation redesign may use closed V12 evidence for root-cause/design research, but a new acceptance epoch must establish a prospective fresh holdout boundary because V12 exposed substantial corpus content.

Do not relax the `0.05` false-activation threshold post hoc.

## Persistent Codex Executor Coordinator research

The user requested investigation and eventual incorporation of a Codex execution topology that retains one coordinator context and delegates bounded work to subagents.

The integrated research memo concludes that the preferred architecture is:

```text
one persistent Codex Executor coordinator root per coherent continuity scope/dossier
        |
        +-- fresh bounded Explorer child
        +-- fresh bounded Worker child
        +-- fresh bounded Verifier/Reviewer child
        +-- optional narrow Specialist child
        |
        +-- concise summaries + Git/evidence references only
```

Key constraints:

- Git remains authoritative; retained chat state is only an execution optimization;
- D042 freshness/reconciliation remains mandatory before each Human-to-Executor governed work unit;
- D041 already permits internal subagents/workers inside Executor-owned stages 5-6;
- D053 stage ownership remains unchanged;
- child agents do not receive Human-facing D055 launch cards; they are private Executor mechanics;
- persist the coordinator root, not the complete child tree as a correctness dependency;
- close disposable children after concise result transfer;
- parallel read-heavy children are preferred initially;
- normally only one writer per mutable worktree/branch;
- thread/session identifiers are runtime metadata, never Governance authority;
- resume failure must degrade to fresh Git bootstrap, never correctness failure.

Current D055 still defaults a first new Task Contract/work unit to `NEW`. The research proposes a future distinction between a persistent Coordinator Root lifecycle and fresh internal Child lifecycle, but no normative change is authorized yet.

## Next work unit — T053 pilot specification

`T053` is currently free and is reserved as the recommended next Task ID for a **Codex Persistent Executor Coordinator Pilot**.

The pilot must be specified by the Orchestrator before launch and should deliberately avoid changing D055 first.

Recommended Phase-1 shape under current rules:

1. one T053 Task Contract with a coherent technical maintenance scope and at least two represented execution phases/checkpoints;
2. first Human-to-Executor T053 launch: Codex `NEW` root, as current D055 requires;
3. root uses native stable Codex subagents for bounded internal work;
4. phase checkpoint returns `PARTIAL`/evidence to Orchestrator;
5. after Orchestrator acceptance of the checkpoint, same T053/same represented branch may use `CONTINUE` under current D055;
6. root must repeat D042 Git/current-authority reconciliation before the continuation;
7. second phase uses fresh bounded child agents rather than reusing child reasoning trees;
8. normally at most three concurrent children during the pilot and at most one write-capable child per mutable worktree;
9. children return concise status/findings/files/verification/Git-evidence/blocker summaries, not full transcripts;
10. close completed children after summary transfer.

The pilot should use the native documented Codex multi-agent/thread surface first. Do **not** build an App Server/SDK session manager or modify consumer Core semantics before measured Phase-1 evidence.

## Pilot telemetry

T053 should record when available:

- coordinator root input/output/reasoning tokens;
- child input/output/reasoning tokens;
- total tokens;
- time to first useful technical action;
- repeated instruction/file reads attributable to bootstrap;
- root context occupancy/compaction events;
- child spawn count and rationale;
- child failures/retries;
- wall-clock completion time;
- review rework and acceptance outcome;
- stale-authority/branch/worktree incidents, which must remain zero.

The optimization objective is lower repeated bootstrap and lower root context pollution at equal-or-better accepted quality, not simply fewer sessions.

Only after a measured T053 pilot should the Orchestrator consider a normative D055 continuity refinement or consumer-project portability.

## Next action

1. Orchestrator creates and integrates `docs/tasks/T053-codex-persistent-executor-coordinator-pilot.md` from current `develop`.
2. T053 must define a useful bounded technical maintenance deliverable, two-phase same-Task continuity, subagent roles, one-writer/worktree safety, concise child-return contract, telemetry and recovery/fallback behavior.
3. Keep D055 unchanged for the pilot: first T053 launch `NEW`; same-task/same-branch accepted follow-up may `CONTINUE`.
4. Do not launch a T053 Executor until its Task Contract and checkpoint authority are integrated.
5. Separately, MG1 remains in Orchestrator Explore/Specify. Do not launch V13 or modify V12 evidence while the pilot is being specified.
6. After T053 evidence is accepted, decide whether to refine D055 and whether the continuity topology should become a portable Agent Governance adapter pattern.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not rerun V12; do not relax V12 thresholds; do not execute F2/G3 outside D050; do not infer challenger quality from non-execution; do not import V12 observations into a future acceptance score; do not create V13 before upstream MG1 design authority; do not treat persistent Codex context as authoritative state; do not change D055 before the pilot; do not require child-thread persistence for correctness; do not allow overlapping writers on one worktree; do not bypass D042 on coordinator continuation; do not write directly to `main`/`develop`.
