# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O157  
Canonical-Branch: `develop`  
Current-Work-Unit: T036 accepted; D040 Phase-B D054 routed-Core activation is the next eligible Orchestrator-owned Markdown-only work unit from fresh canonical develop  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D042 freshness, D055 launch profiles and D056 progress-note rules remain controlling.
- T034 and T035 remain `ACCEPTED`; T035 historical oracle baseline remains preserved.
- T037 is `ACCEPTED`; it restored the canonical repository-context/format verification baseline without semantic product/oracle changes.
- T036 Oracle revision `T036-D054-ACTIVATION-TRANSITION-v1` is `ACCEPTED`.
- T036 final independent verification used a fresh isolated native-Windows checkout from canonical base `f72b1eb609fb5636f102fdfd69501bfc61618008` and submitted Executor HEAD `c862da6a09d84d24c6d80b76de892acf06f39cb5`.
- T036 accepted verification evidence: focused oracle `6 passed`; full deterministic suite `355 passed`; Ruff check PASS; Ruff format PASS; `git diff --check` PASS; no review findings; no product/oracle/runtime/protocol drift.
- T036 verification handoff integrated through PR #209 at `456e27207f8975a3d815a16cb607ddc491fe0df3`.
- T036 acceptance is persisted in `docs/reviews/T036-R1.md`.
- D040 Phase-B D054 routed-Core activation is now structurally eligible and is the next work unit.
- Phase-B must restart from fresh current canonical `develop`; the stale pre-T036 branch `feat/d054-core-activation` and any unattached draft blobs/state are non-authoritative and MUST NOT be reused.
- T021/T022 remain paused and MUST NOT auto-resume.

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

Do not duplicate Task Contract semantics or routine command syntax in the transport prompt.

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

## T036 accepted identity

```text
Task: T036
Status: ACCEPTED
Task Contract: docs/tasks/T036-d054-phase-b-oracle-transition.md
Oracle transition: T036-D054-ACTIVATION-TRANSITION-v1
Planning/oracle PR: #204
Integrated planning/oracle anchor: cc4cb59b3979f6260890e94588f3cb071c9b9488
Accepted verification base: f72b1eb609fb5636f102fdfd69501bfc61618008
Submitted Executor HEAD: c862da6a09d84d24c6d80b76de892acf06f39cb5
Handoff: handoffs/T036-executor-handoff.json
Verification PR: #209
Integrated verification: 456e27207f8975a3d815a16cb607ddc491fe0df3
Acceptance review: docs/reviews/T036-R1.md
```

## T037 accepted identity

```text
Task: T037
Status: ACCEPTED
Submitted Executor HEAD: 71885c6c22f993c3eb9f5b2346a16f0e47c1a511
Implementation anchor: 033f4430ee96a9d3e67063630e2b9e0bf52a4615
Handoff: handoffs/T037-executor-handoff.json
Integration PR: #207
Integrated implementation: e078142a7c18b1f87ace09fd6fc717f9b9f50610
Acceptance review: docs/reviews/T037-R1.md
```

## Next action

1. Integrate this T036 acceptance/checkpoint Markdown branch into `develop` through PR.
2. Refresh current canonical `develop` identity after that merge.
3. Restart D040 Phase-B D054 routed-Core activation as Orchestrator-owned Markdown-only work from a NEW fresh topic branch based on that current `develop`.
4. Re-read the current D040/D054 controlling Markdown and the routed Core modules required for the Phase-B change; do not reuse stale pre-T036 draft branch/blob state as authority.
5. Perform the atomic Phase-B Markdown activation under D040 green-baseline rules, review the complete diff, and integrate through PR only if canonical verification remains green.
6. Do not resume T021/T022 automatically.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not reuse stale pre-T036 activation branch/blob state; do not bypass D040 atomic migration/green-baseline constraints; do not duplicate current protocol-version authority outside the canonical Core source; do not resume T021/T022 automatically; do not write directly to `main`/`develop`.
