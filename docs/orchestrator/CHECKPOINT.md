# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O168  
Canonical-Branch: `develop`  
Current-Work-Unit: MG1 integrated; T023 activation-topology evaluation is next executable work  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D040 single current protocol-version authority, D042 freshness, D048 final-publication boundary, D050 topology evaluation, D051 one-product/single-install, D052 conformance ownership, D055 launch profiles and D056 progress-note rules remain controlling.
- Current routed Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`. T022 review: `docs/reviews/T022-R1.md`; submitted Executor HEAD `35ba704c8e2997f414a5f2a79b23c33b821b8016`; integration PR `#223`; merge `361e6700d74d47f5805b9af838c1cfa9519766b2`.
- MG1 is integrated in canonical `develop` by PR `#225`, merge `b3e20020daf9d8f1ff475f0f414f31555639abb2`.
- MG1 Oracle revision is `MG1-T023-TOPOLOGY-ORACLE-v1`; Capability-Source-Epoch is `MG1-2026-08-24-v1`; Corpus-ID is `MG1-T023-CORPUS-v1`.
- MG1 capability source: `docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md`.
- MG1 gate: `docs/MG1-SKILL-ACTIVATION-PREREGISTRATION.md`.
- MG1 topology identities: `evals/skill_activation_topology/topologies.json`.
- MG1 frozen corpus: `evals/skill_activation_topology/corpus.json`, 30 cases.
- MG1 selection oracle: `evals/skill_activation_topology/oracle.json`.
- Required T023 candidates are exactly B0/B1/F2/G3. Required acceptance matrix is 30 cases x 4 candidates x 3 clean-context trials = 360 live trials, using the pre-registered Codex/native-Windows/GPT-5.6-Sol/Medium live cell plus deterministic regression/load/provenance/installability evidence.
- MG1 expected semantics, corpus membership, topology mapping, thresholds and selection meaning are frozen. Executor may implement technical runner/adapters/result collection and supplementary diagnostics only; semantic oracle defects require Orchestrator re-entry.
- T023's MG1 and T022 readiness dependencies are now satisfied. T023 is the next critical-path executable work.
- T025 is independently dependency-eligible after T022 but remains parallel optional work; do not substitute it for T023 unless Human reprioritizes.

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

## MG1 accepted gate identity

```text
Gate: MG1 — Skill activation topology and eval pre-registration
Status: INTEGRATED / FROZEN FOR T023
Integration PR: #225
Integration merge: b3e20020daf9d8f1ff475f0f414f31555639abb2
Oracle revision: MG1-T023-TOPOLOGY-ORACLE-v1
Capability source epoch: MG1-2026-08-24-v1
Corpus ID: MG1-T023-CORPUS-v1
```

## T023 next executable identity

```text
Task: T023
Status: NEXT EXECUTABLE WORK
Task Contract: docs/tasks/T023-unified-skill-profile-activation-evals.md
Expected branch: test/t023-skill-activation-topology-evals
Expected handoff: handoffs/T023-executor-handoff.json
Test authorship: mixed
Required execution: frozen MG1/D052 experiment; no semantic oracle mutation
```

## Next action

1. Integrate this O168 checkpoint branch into `develop` through PR.
2. Refresh canonical `develop` identity.
3. Show D055 for T023: Codex `NEW`, GPT-5.6 Sol, High; the work combines technical harness implementation, controlled 360-trial live evaluation, deterministic regressions, provenance/load/installability evidence and strict oracle preservation.
4. Launch T023 from fresh canonical `develop` using only pointer `docs/tasks/T023-unified-skill-profile-activation-evals.md` plus D042 freshness.
5. Executor must execute the frozen MG1 oracle exactly and return `BLOCKED` rather than substitute/redefine the required live cell, corpus, expected outcomes or thresholds.
6. Orchestrator independently reviews raw/structured evidence, recomputes the frozen metrics/selection rule where practical, and accepts exactly one topology outcome only if all mandatory invariants hold.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not modify MG1 semantic assets after comparative results without explicit Orchestrator restart authority; do not change Core/engine/profile behavior to favor a candidate; do not introduce independent products, per-entrypoint versions, portable Skill-to-Skill dependency or multi-install packaging; do not let Executor edit committed Markdown or Orchestrator-owned semantic oracle assets; do not write directly to `main`/`develop`.
