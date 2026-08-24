# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O156  
Canonical-Branch: `develop`  
Current-Work-Unit: T037 accepted/integrated; T036 must now be independently re-verified from fresh canonical develop before D040 Phase-B can resume  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D042 freshness, D055 launch profiles and D056 progress-note rules remain controlling.
- T034 and T035 remain `ACCEPTED`; T035 historical oracle baseline remains preserved.
- T036 planning/oracle transition `T036-D054-ACTIVATION-TRANSITION-v1` is integrated through PR #204 at `cc4cb59b3979f6260890e94588f3cb071c9b9488`.
- First T036 independent verification submitted `BLOCKED` at `7919f6050d9d67b3ca27c9d49b9a0f4dd32f6160`; focused oracle passed `6 passed`, with no T036 semantic/runtime drift. Blocking failures were unrelated canonical baseline conditions.
- T037 restored that canonical baseline. Submitted Executor HEAD `71885c6c22f993c3eb9f5b2346a16f0e47c1a511` changed only the deterministic repository-context manifest plus its handoff. Locked Ruff formatting required no file changes.
- T037 verification: repository-context `56 passed`; T035/T036 oracle `6 passed`; full pytest PASS; Ruff check PASS; Ruff format PASS; `git diff --check` PASS; no unresolved review findings.
- T037 implementation integrated through PR #207 at `e078142a7c18b1f87ace09fd6fc717f9b9f50610` and accepted in `docs/reviews/T037-R1.md`.
- T036 is still not accepted. It must be independently re-verified from fresh canonical `develop` after T037 integration; do not reuse the prior blocked handoff as acceptance evidence.
- D040 Phase-B D054 routed-Core activation remains BLOCKED pending T036 acceptance.
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

## T036 current identity

```text
Task: T036
Status: VERIFICATION REQUIRED AFTER T037
Task Contract: docs/tasks/T036-d054-phase-b-oracle-transition.md
Oracle transition: T036-D054-ACTIVATION-TRANSITION-v1
Integrated planning/oracle anchor: cc4cb59b3979f6260890e94588f3cb071c9b9488
Prior blocked verification HEAD: 7919f6050d9d67b3ca27c9d49b9a0f4dd32f6160
Prior handoff: handoffs/T036-executor-handoff.json
Focused oracle from prior run: PASS — 6 passed
Next requirement: fresh independent verification from current canonical develop
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

1. Integrate this T037 acceptance/checkpoint Markdown branch into `develop` through PR.
2. Show D055 launch profile for Codex.
3. Launch a `NEW` T036 independent verification session from then-current canonical `develop`, using only pointer `docs/tasks/T036-d054-phase-b-oracle-transition.md` plus D042 freshness.
4. Executor performs only the T036-authorized independent Code Review & Verify and persists a new pushed handoff/head.
5. ChatGPT reviews that fresh T036 evidence and performs Converge/Accept.
6. Only after T036 acceptance may D040 Phase-B restart from fresh canonical `develop`.
7. Do not resume T021/T022 automatically.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not waive T036 verification; do not modify T035/T036 oracle semantics outside persisted authority; do not activate D054 Core before T036 acceptance; do not reuse stale pre-T036 activation branch state; do not resume T021/T022 automatically; do not write directly to `main`/`develop`.
