# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O167  
Canonical-Branch: `develop`  
Current-Work-Unit: MG1 pre-registration authored; integrate MG1, then launch T023 from the exact post-MG1 canonical baseline  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: ChatGPT Orchestrator

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D040 single current protocol-version authority, D042 freshness, D048 final-publication boundary, D050 topology evaluation, D051 one-product/single-install, D052 conformance ownership, D055 launch profiles and D056 progress-note rules remain controlling.
- Current routed Core protocol remains `1.15.0`.
- T021 is `ACCEPTED`; review `docs/reviews/T021-R2.md`.
- T022 is `ACCEPTED`; review `docs/reviews/T022-R1.md`; submitted Executor HEAD `35ba704c8e2997f414a5f2a79b23c33b821b8016`; integration PR `#223`; merge `361e6700d74d47f5805b9af838c1cfa9519766b2`.
- T022 full deterministic evidence is `405 passed`; Consumer/source-maintainer isolation and no source-root Consumer footprint are accepted.
- MG1 has been authored before T023 comparative results under Oracle revision `MG1-T023-TOPOLOGY-ORACLE-v1` and Capability-Source-Epoch `MG1-2026-08-24-v1`.
- MG1 canonical capability source: `docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md`.
- MG1 gate: `docs/MG1-SKILL-ACTIVATION-PREREGISTRATION.md`.
- MG1 topology identities: `evals/skill_activation_topology/topologies.json`.
- MG1 frozen corpus: `evals/skill_activation_topology/corpus.json`, Corpus-ID `MG1-T023-CORPUS-v1`, 30 cases across positive Consumer/source/external-trust, negative, near-miss, cross-profile, ambiguous and multi-intent classes.
- MG1 selection oracle: `evals/skill_activation_topology/oracle.json`; required B0/B1/F2/G3 candidates, 3 clean-context trials per case/candidate, required Codex/native-Windows/GPT-5.6-Sol/Medium live cell, deterministic load evidence, mandatory invariants, qualifying thresholds and material-improvement rule are frozen.
- Executor may implement runner/adapters/result collection and supplementary diagnostics but must not alter MG1 corpus membership, expected semantic outcomes, topology mapping, thresholds or selection meaning. Suspected semantic oracle defects require upstream Orchestrator re-entry.
- T023 remains blocked until this MG1 branch is integrated. After integration, T023 becomes the next critical-path executable work.
- T025 is dependency-eligible after T022 and may proceed in parallel only if explicitly prioritized; it does not replace the MG1 -> T023 critical path.

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

## MG1 identity

```text
Gate: MG1 — Skill activation topology and eval pre-registration
Status: AUTHORED / PENDING INTEGRATION
Owner: ChatGPT Orchestrator
Gate authority: docs/MG1-SKILL-ACTIVATION-PREREGISTRATION.md
Capability source: docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md
Oracle: evals/skill_activation_topology/oracle.json
Corpus: evals/skill_activation_topology/corpus.json
Topologies: evals/skill_activation_topology/topologies.json
Oracle revision: MG1-T023-TOPOLOGY-ORACLE-v1
Capability source epoch: MG1-2026-08-24-v1
```

## T023 next identity after MG1 integration

```text
Task: T023
Status: BLOCKED UNTIL MG1 MERGE; THEN NEXT EXECUTABLE
Task Contract: docs/tasks/T023-unified-skill-profile-activation-evals.md
Expected branch: test/t023-skill-activation-topology-evals
Expected handoff: handoffs/T023-executor-handoff.json
Test authorship: mixed
Required execution: frozen MG1/D052 experiment; no semantic oracle mutation
```

## Next action

1. Review the complete MG1 branch diff and ensure it changes only Orchestrator-owned Markdown plus D052 conformance assets.
2. Integrate MG1 into `develop` through PR.
3. Refresh canonical `develop` identity and confirm all MG1 assets exist at that exact baseline.
4. Show D055 for T023: Codex `NEW`, GPT-5.6 Sol, Medium; T023 requires standard harness implementation plus a substantial controlled eval matrix, but no semantic redesign.
5. Launch T023 using only pointer `docs/tasks/T023-unified-skill-profile-activation-evals.md` plus D042 freshness.
6. Executor must execute the frozen MG1 oracle exactly, preserve Orchestrator-owned semantic assets, and return `BLOCKED` rather than substitute/redefine the required live cell or thresholds.
7. Orchestrator independently reviews T023 evidence and applies the frozen selection rule before accepting any topology.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not launch T023 before MG1 integration; do not modify MG1 semantic assets after comparative results without explicit Orchestrator restart authority; do not change Core/engine/profile behavior to favor a candidate; do not introduce independent products, per-entrypoint versions, portable Skill-to-Skill dependency or multi-install packaging; do not let Executor edit committed Markdown; do not write directly to `main`/`develop`.
