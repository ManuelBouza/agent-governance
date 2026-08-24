# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O159  
Canonical-Branch: `develop`  
Current-Work-Unit: T021-R1 rework explicitly resumed by Human Owner; reconcile represented T021 branch with fresh canonical develop, correct only the accepted review defect, then re-verify  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D042 freshness, D048 final-publication boundary, D055 launch profiles and D056 progress-note rules remain controlling.
- D054 Phase-B is `ACCEPTED`; routed Core protocol is `1.15.0`.
- T034, T035, T036 and T037 remain `ACCEPTED`.
- Human Owner explicitly authorized resumption of T021 on 2026-08-24 after O158 stopped for priority rather than auto-resuming paused T021/T022.
- T021 remains `REWORK_REQUIRED` under `docs/reviews/T021-R1.md`; the unchanged Task Contract is `docs/tasks/T021-consumer-profile-abstraction-zero-drift.md`.
- T021-R1's sole semantic defect is the AC-T021-2 fail-closed bypass: directly constructed unsupported `Profile` identities can reach the engine boundary without authoritative active-profile validation. Rework must preserve AC-T021-1 consumer zero drift and AC-T021-3 T020 artifact compatibility.
- The prior RCAB baseline blocker recorded by the original T021 handoff is no longer active; T037 restored the canonical verification baseline and later T036 fresh verification passed the full native-Windows suite.
- Represented T021 topic branch remains `refactor/t021-consumer-profile-abstraction`. Its previously verified submitted HEAD is `969e2130ca9abb27c6ae5ad830923582f45b8a2f`, with implementation anchor `30bea773560e013811b90366e77735e6f7530e48`.
- Against pre-resume canonical `develop@fbced51621cda93c070326d3b9d7415b3d811dc5`, the represented T021 branch is 2 commits ahead and 195 commits behind with merge-base `53b9c39c1111f4b871ef73b7447510195f672ea2`. Its net task delta remains limited to the original five authorized non-Markdown files.
- T021 history MUST be reconciled with current `develop` without discarding/recreating represented work or force-pushing rewritten history.
- T022 remains `BLOCKED` until T021 is accepted. MG1/T023 and downstream unified-refactor work remain ineligible until their declared dependencies are satisfied.

## Mandatory Executor prompt transport invariant

Every Executor prompt is pointer-only and includes D042 freshness:

```text
Operate as the Agente de IA Ejecutor for <repository>.

Synchronize with GitHub and establish a safe current local baseline from the canonical remote state before loading repository instructions or execution authority, per D042/RB001. Do not discard unrepresented local work.

Use <canonical/base or represented topic branch as applicable>.

Load current repository instructions, then execute exactly:
<persisted authority path>

Return only the output required by that persisted authority.
```

Do not duplicate Task Contract/review semantics or routine command syntax in the transport prompt.

## D055 launch invariant

Before every Executor prompt, show concrete Executor, `NEW|CONTINUE`, exact recommended model, effort and one-line rationale.

Current Codex mapping:

```text
read-only/repetitive observation -> GPT-5.6 Luna / Low
narrow mechanical implementation -> GPT-5.6 Terra / Low
standard AG implementation/rework -> GPT-5.6 Sol / Medium
complex/high-risk technical work  -> GPT-5.6 Sol / High
exceptional long-horizon work     -> GPT-5.6 Sol / highest mode only when justified
```

## T021 active identity

```text
Task: T021
Status: REWORK_REQUIRED / HUMAN-RESUMED
Task Contract: docs/tasks/T021-consumer-profile-abstraction-zero-drift.md
Review authority: docs/reviews/T021-R1.md
Topic branch: refactor/t021-consumer-profile-abstraction
Previously verified submitted HEAD: 969e2130ca9abb27c6ae5ad830923582f45b8a2f
Implementation anchor: 30bea773560e013811b90366e77735e6f7530e48
Prior handoff: handoffs/T021-executor-handoff.json
Current required action: history-preserving reconciliation with fresh develop + T021-R1 correction + complete re-verification
```

## Next action

1. Integrate this Human-authorized T021 resume checkpoint into `develop` through PR.
2. Show D055 profile: Codex `NEW`, GPT-5.6 Sol, Medium, because the task is narrow but the represented branch is materially stale and must be reconciled safely before rework.
3. Launch T021 from current canonical `develop` using only pointer `docs/tasks/T021-consumer-profile-abstraction-zero-drift.md` plus D042 freshness; current repository instructions/checkpoint route the executor to `docs/reviews/T021-R1.md` and the represented branch.
4. Executor preserves represented T021 history, reconciles with current `develop`, applies only T021-R1-authorized correction, runs the complete current verification matrix, persists a terminal handoff, performs the D048 final push, and returns canonical completion fields.
5. Orchestrator independently reviews the submitted remote HEAD, complete diff and evidence before acceptance/integration.
6. Do not start T022, MG1/T023 or later program work before T021 acceptance.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not discard or rewrite represented T021 history; do not absorb unrelated baseline/RCAB work; do not broaden T021 into source-maintainer behavior; do not edit committed Markdown from the Executor; do not start T022 before T021 acceptance; do not write directly to `main`/`develop`.
