# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O158  
Canonical-Branch: `develop`  
Current-Work-Unit: D054 Phase-B routed-Core activation accepted/integrated; next work must be selected from current canonical program authority without auto-resuming paused T021/T022  
Chat-Closure: SAFE_TO_CLOSE  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D042 freshness, D055 launch profiles and D056 progress-note rules remain controlling.
- T034, T035, T036 and T037 are `ACCEPTED`.
- T036 Oracle revision `T036-D054-ACTIVATION-TRANSITION-v1` is accepted and removed the stale future-current-version pin while preserving T035 historical semantics and the exact Consumer CLI v1 command set.
- T036 accepted verification used a fresh isolated native-Windows checkout: focused oracle `6 passed`, full deterministic suite `355 passed`, Ruff check/format PASS and `git diff --check` PASS.
- D040 Phase-B D054 routed-Core activation was restarted from fresh canonical `develop` after T036 acceptance; stale pre-T036 branch/blob state was not reused.
- D054 Phase-B activation branch `feat/d054-phase-b-core-activation` changed only routed Core Markdown and integrated through PR #211 at `37d163975f46b67573ee9ce1ffff6e1745195126`.
- Current routed Core protocol is `1.15.0`.
- Activated module versions: `EXECUTION-CONTROL 1.1.0`, `PROTOCOL 1.4.0`, `CONTEXT 1.4.0`.
- Routed Core now makes Executor-owned adapter mechanics explicit, separates semantic runbooks from Verified Operation Recipes, defines authoritative version-compatible syntax resolution and evidence-gated recipe promotion, routes native `.agent-coordination/runbooks/` persistence, and forbids copying runbook/recipe registries into STATE.
- Human Owner remains the authority for `REQUIRE_HUMAN`, MFA/external approval, material credential/risk decisions and explicit syntax inspection/execution; routine command copy/paste is not a default Human responsibility.
- D054 Phase-B acceptance is persisted in `docs/reviews/D054-PHASE-B-R1.md`.
- The old `feat/d054-core-activation` branch and unattached pre-T036 draft blobs/state remain non-authoritative historical scratch state and MUST NOT be reused.
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

## D054 Phase-B accepted identity

```text
Decision: D054
Status: PHASE-B ACCEPTED / ROUTED CORE ACTIVE
Migration authority: D040
Activation branch: feat/d054-phase-b-core-activation
Activation HEAD: 7ab00e5358ccf021312d3652f428624d6f9b279d
Integration PR: #211
Integrated activation: 37d163975f46b67573ee9ce1ffff6e1745195126
Acceptance review: docs/reviews/D054-PHASE-B-R1.md
Current Protocol-Version: 1.15.0
```

## Next action

1. Integrate this D054 Phase-B acceptance/checkpoint Markdown branch into `develop` through PR.
2. On the next orchestration cycle, refresh current canonical `develop` identity.
3. Read `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md` only as needed to identify the next explicitly authorized, non-paused work unit after D054 Phase-B.
4. Do not infer or auto-resume T021/T022; if the plan offers no clearly eligible work, stop for Human priority rather than inventing scope.
5. If the selected next work is executable, persist the required Task Contract/SDD authority before any Executor launch; if Markdown-only, follow normal Orchestrator branch/PR ownership.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint. Then follow `Next action`; load `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md` only at the selection step above.

## Do not

Do not reuse stale pre-T036 activation branch/blob state; do not duplicate current protocol-version authority outside `governance-core/GOVERNANCE.md`; do not treat a VERIFIED recipe as execution authority; do not make the Human Owner the routine terminal operator; do not resume T021/T022 automatically; do not write directly to `main`/`develop`.
