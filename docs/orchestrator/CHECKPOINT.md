# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O166  
Canonical-Branch: `develop`  
Current-Work-Unit: T022 accepted/integrated; MG1 Skill activation topology/eval pre-registration is next Orchestrator-owned gate before T023  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: ChatGPT Orchestrator

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D040 single current protocol-version authority, D042 freshness, D048 final-publication boundary, D052 conformance ownership, D055 launch profiles and D056 progress-note rules remain controlling.
- Current routed Core protocol remains `1.15.0`.
- T021 is `ACCEPTED`; review `docs/reviews/T021-R2.md`; submitted Executor HEAD `4f55cb41963f173171e637daf6311aaf99312ffc`; integration PR `#221`.
- T022 is `ACCEPTED`; review `docs/reviews/T022-R1.md`.
- Accepted T022 canonical verification base: `7ad68b2774dafc58208737af66f88fb67cec2e53`.
- Accepted T022 implementation HEAD: `a32a906a636e49b9392129d42925c30fef07e027`.
- Accepted T022 submitted Executor HEAD: `35ba704c8e2997f414a5f2a79b23c33b821b8016`.
- T022 integration PR: `#223`; integration merge: `361e6700d74d47f5805b9af838c1cfa9519766b2`.
- T022 verification evidence: focused source-profile/adapter `48 passed`; Consumer/profile/shared-engine/artifact regression `110 passed`; full deterministic `405 passed`; Ruff check/format, py_compile and `git diff --check` PASS; no root `.agent-governance` or `.agent-coordination` exists.
- T022 activates explicit `source-maintainer` routing through exact versioned `agent-governance-source.json`, fail-closed source adapters, live Core/source record routing, Consumer/source isolation and flat `handoffs/*.json` write-path resolution only.
- T023 is still `BLOCKED` by its own readiness condition. T022 acceptance satisfies only one dependency.
- Before T023 can start, MG1 must be integrated into `develop` with D050 topology definitions, D052 conformance corpus/expected outcomes, host/model matrix, repeated clean-context trial method, metric definitions, and material-improvement/non-regression thresholds frozen before comparative results.
- MG1 is ChatGPT Orchestrator-owned Markdown/conformance authority. Executor must not compensate for a missing MG1 by authoring or changing committed Markdown or semantic oracle assets.
- T025 becomes dependency-eligible after T022 acceptance and may proceed in parallel with the MG1/T023 path, but current critical-path next action is MG1 unless Human reprioritizes.

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

## T022 accepted identity

```text
Task: T022
Status: ACCEPTED
Task Contract: docs/tasks/T022-source-maintainer-profile-over-legacy-adapters.md
Review: docs/reviews/T022-R1.md
Submitted Executor HEAD: 35ba704c8e2997f414a5f2a79b23c33b821b8016
Integration PR: #223
Integration merge: 361e6700d74d47f5805b9af838c1cfa9519766b2
```

## MG1 next gate

```text
Gate: MG1 — Skill activation topology and eval pre-registration
Owner: ChatGPT Orchestrator
Dependency satisfied: T022 ACCEPTED
Purpose: freeze T023 candidate topology identities and D052 experiment oracle before comparative results
Required before T023: integrated MG1 authority + corpus + expected outcomes + thresholds + trial/matrix/metric definitions
```

## T023 blocked identity

```text
Task: T023
Status: BLOCKED PENDING MG1
Task Contract: docs/tasks/T023-unified-skill-profile-activation-evals.md
Expected branch: test/t023-skill-activation-topology-evals
Expected handoff: handoffs/T023-executor-handoff.json
Do not launch until MG1 is integrated and independently reviewed for completeness.
```

## Next action

1. Integrate this T022 acceptance/checkpoint branch into `develop` through PR.
2. Refresh canonical `develop` identity.
3. Execute MG1 as Orchestrator-owned Plan & Trace / conformance pre-registration work, using D050, D051, D052, the unified refactor plan, current accepted T021/T022 semantics, and T023's readiness requirements.
4. Persist the smallest complete MG1 authority needed to freeze B0/B1/F2/G3 candidate identities, canonical capability/routing projection source, required corpus and expected classifications, host/model matrix, clean-context repetition method, metrics, installability-feasibility evidence method, and victory/non-regression thresholds.
5. Integrate MG1 through an Orchestrator PR only after remote diff review.
6. Only then show D055 and launch T023. T025 may be scheduled in parallel only if explicitly selected without weakening MG1/T023 sequencing.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not launch T023 before MG1 integration; do not let Executor author or modify committed Markdown or D052 semantic oracle meaning; do not change accepted Core/engine/profile semantics to favor a topology; do not introduce independent Governance products, per-entrypoint version identities, portable Skill-to-Skill dependency, or manual multi-install packaging; do not write directly to `main`/`develop`.
