# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O165  
Canonical-Branch: `develop`  
Current-Work-Unit: T021 accepted/integrated; T022 source-maintainer profile is next executable work  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D040 single current protocol-version authority, D042 freshness, D048 final-publication boundary, D052 conformance ownership, D055 launch profiles and D056 progress-note rules remain controlling.
- Current routed Core protocol remains `1.15.0`.
- T034 through T039 are accepted; T040 sequencing correction is satisfied.
- T038 review: `docs/reviews/T038-R1.md`; T039 review: `docs/reviews/T039-R1.md`.
- T021 is now `ACCEPTED`. Review: `docs/reviews/T021-R2.md`.
- Accepted T021 canonical verification base: `82a5d8741ddea77e2bec6a369dd8fdb17ef9d109`.
- Accepted T021 reconciliation HEAD: `23be0fe5506d30a90511a1063c02a126da8531c1`.
- Accepted T021 implementation HEAD: `1beaa1193b8522c63f1d1a11a36f3b8cb15ee367`.
- Accepted T021 submitted Executor HEAD: `4f55cb41963f173171e637daf6311aaf99312ffc`.
- T021 integration PR: `#221`; integration merge: `e5bdb3c40236bb146343a405d9d56f2a8ee30877`.
- T021-R1 AC-T021-2 is resolved: every direct unsupported `Profile` identity is rejected fail-closed at the engine/profile boundary before Consumer target mutation. Consumer/default behavior and T020 artifact compatibility remain green.
- T021 verification evidence: focused profile `25 passed`, Consumer v1 regression `79 passed`, T020 artifact `4 passed`, full deterministic `382 passed`, Ruff check/format PASS, py_compile PASS, `git diff --check` PASS.
- T022 dependency on T021 is now satisfied. T022 persisted authority is `docs/tasks/T022-source-maintainer-profile-over-legacy-adapters.md`.
- T022 objective is to activate a `source-maintainer` runtime profile over explicit legacy source adapters without creating Consumer installation state or changing source persistence semantics.
- T023 and later unified-refactor work remain gated by their declared dependencies; do not skip T022.
- Historical Orchestrator Markdown successor incidents on represented Executor branches remain non-authoritative and must not be used as Executor evidence. Never rewrite represented history to remove them.

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

## T021 accepted identity

```text
Task: T021
Status: ACCEPTED
Task Contract: docs/tasks/T021-consumer-profile-abstraction-zero-drift.md
Review: docs/reviews/T021-R2.md
Submitted Executor HEAD: 4f55cb41963f173171e637daf6311aaf99312ffc
Integration PR: #221
Integration merge: e5bdb3c40236bb146343a405d9d56f2a8ee30877
```

## T022 next executable identity

```text
Task: T022
Status: NEXT EXECUTABLE WORK
Task Contract: docs/tasks/T022-source-maintainer-profile-over-legacy-adapters.md
Expected branch: feat/t022-source-maintainer-profile
Expected handoff: handoffs/T022-executor-handoff.json
Base: fresh canonical develop after this acceptance/checkpoint integration
```

## Next action

1. Integrate this T021 acceptance/checkpoint branch into `develop` through PR.
2. Refresh canonical `develop` identity.
3. Show D055 profile for T022: Codex `NEW`, GPT-5.6 Sol, Medium; this is standard semantic profile/adaptor implementation with cross-profile isolation requirements.
4. Launch T022 from fresh canonical `develop` using only pointer `docs/tasks/T022-source-maintainer-profile-over-legacy-adapters.md` plus D042 freshness.
5. Executor performs only T022 Implement + Code Review & Verify, persists/pushes terminal handoff/head and returns canonical completion fields.
6. Orchestrator independently reviews T022 remote evidence/diff before acceptance/integration.
7. Do not start T023 or later work before T022 acceptance and the next declared gate is satisfied.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not broaden T022 into Markdown ownership changes, Core protocol semantics, Consumer installation state at source root, a second independently maintained Skill runtime, source persistence convergence, or downstream T023+ scope; do not let Executor edit committed Markdown; do not write directly to `main`/`develop`.
