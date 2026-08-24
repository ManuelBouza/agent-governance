# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O164  
Canonical-Branch: `develop`  
Current-Work-Unit: T039 accepted; resume T021-R1 on preserved represented history against fresh canonical develop  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D040 single current protocol-version authority, D042 freshness, D048 final-publication boundary, D052 conformance ownership, D055 launch profiles and D056 progress-note rules remain controlling.
- Current routed Core protocol remains `1.15.0`.
- T034, T035, T036, T037, T038 and T039 are `ACCEPTED`.
- T038 acceptance review: `docs/reviews/T038-R1.md`; submitted Executor HEAD `cb2e7f86fe08ffd80665b4616d71ebad86a425bf`; integration PR `#217`; integration merge `b02b6bf2a5d5b843b2803fb454b0316779a5dae8`.
- T039 acceptance review: `docs/reviews/T039-R1.md`; final verification base `dffc2a2fba34080b111ea9ebe5b975acf81cfca2`; submitted Executor HEAD `38aa7dd4c2db46796f526f47ce0484265e12306c`; integration PR `#219`; integration merge `3ad69a70cc2319c8f4c228c6fcefb8148bee289a`.
- T039 final verification passed focused T034 `3 passed`, full locked pytest `357 passed`, Ruff check/format and `git diff --check`.
- T039 oracle revision `T039-T034-PROTOCOL-HISTORY-TRANSITION-v1` remains controlling: historical T034 `1.14.0` acceptance is proven historically while current artifact identity derives from current Core.
- T040 sequencing correction is satisfied; the T038/T039 convergence chain is complete.
- Orchestrator process incidents on represented T038/T039 branches were explicitly excluded from submitted-head integration and are non-authoritative successor noise. Never use those later Markdown commits as Executor evidence and never rewrite represented history to remove them.
- Human Owner explicitly resumed T021 on 2026-08-24. T021 remains `REWORK_REQUIRED` under `docs/reviews/T021-R1.md` and is now the next eligible work unit.
- T021's sole semantic defect remains AC-T021-2: directly constructed unsupported `Profile` identities can bypass `resolve_profile()` and reach the engine Consumer path unless the authoritative engine/profile boundary validates supported identity fail-closed.
- T021 represented branch is `refactor/t021-consumer-profile-abstraction`. Its prior history-preserving reconciliation anchor is `f078928734be4ed0d272821955ba4d8ccdd7cd53`; prior blocked submitted HEAD is `b2ec49e210a752fa539832e06b48b2bcdc00a8dd`. No T021-R1 correction was committed at that blocked HEAD.
- T021 represented history MUST be preserved. Reconcile current canonical develop containing accepted T038/T039 into the represented branch without discard/recreation/force-push, then apply only the T021-R1-authorized correction and complete current verification.
- T022 remains `BLOCKED` until T021 is accepted. MG1/T023 and later unified-refactor work remain ineligible until their declared dependencies are satisfied.

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

## T039 accepted identity

```text
Task: T039
Status: ACCEPTED
Task Contract: docs/tasks/T039-t034-protocol-history-oracle-transition.md
Review: docs/reviews/T039-R1.md
Submitted Executor HEAD: 38aa7dd4c2db46796f526f47ce0484265e12306c
Integration PR: #219
Integration merge: 3ad69a70cc2319c8f4c228c6fcefb8148bee289a
```

## T021 active identity

```text
Task: T021
Status: REWORK_REQUIRED / HUMAN-RESUMED / NEXT EXECUTABLE WORK
Task Contract: docs/tasks/T021-consumer-profile-abstraction-zero-drift.md
Review authority: docs/reviews/T021-R1.md
Represented branch: refactor/t021-consumer-profile-abstraction
Prior reconciliation HEAD: f078928734be4ed0d272821955ba4d8ccdd7cd53
Prior blocked submitted HEAD: b2ec49e210a752fa539832e06b48b2bcdc00a8dd
Pending semantic correction: AC-T021-2 direct unsupported-Profile fail-closed boundary
Required action: preserve history, reconcile fresh canonical develop, apply only R1 correction, run complete current verification, persist/push terminal handoff/head
```

## Next action

1. Integrate this T039 acceptance/checkpoint branch into `develop` through PR.
2. Refresh canonical `develop` identity.
3. Show D055 profile for T021: Codex `NEW`, GPT-5.6 Sol, Medium; the semantic correction is narrow but represented history must be reconciled safely with the now-restored canonical baseline.
4. Launch T021 from fresh canonical `develop` using only pointer `docs/tasks/T021-consumer-profile-abstraction-zero-drift.md` plus D042 freshness. Current repository instructions/checkpoint route the Executor to `docs/reviews/T021-R1.md` and the represented branch.
5. Executor preserves represented T021 history, reconciles current develop without force-push/recreation, applies only the T021-R1 correction, runs the complete current verification matrix, persists/pushes terminal handoff/head and returns canonical completion fields.
6. Orchestrator independently reviews the submitted remote HEAD, complete diff, history preservation and evidence before acceptance/integration.
7. Do not start T022 or later unified-refactor work before T021 acceptance.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not treat post-submission Orchestrator Markdown successors on represented T038/T039 branches as Executor evidence; do not force-rewrite represented T021 history; do not broaden T021 into source-maintainer behavior, Core semantics or unrelated baseline work; do not let Executor edit committed Markdown; do not start T022 before T021 acceptance; do not write directly to `main`/`develop`.
