# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O170  
Canonical-Branch: `develop`  
Current-Work-Unit: T041/MG1-v2 integrated; T023 is next executable relaunch from fresh canonical develop  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D040 single current protocol-version authority, D042 freshness, D048 final-publication boundary, D050 topology evaluation, D051 one-product/single-install, D052 conformance ownership, D055 launch profiles and D056 progress-note rules remain controlling.
- Current routed Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`.
- T023 first launch from `develop@04c42e0a4b7c3be6fa64b336df93521d07cd5805` ended `BLOCKED / ORACLE_DEFECT` at submitted HEAD `b7402bbaea52d7ac4342b848c73bf56a7bb4bbef`; implementation/preflight anchor `9fc4d5039a4f7d8dfeae45228f9fd47f18ff086e`.
- The blocked T023 branch contains only structured blocker evidence and handoff, executed `0/360` live trials, and must not be merged or used as implementation base.
- T041 corrected the pre-trial Specify defect by freezing exact host-visible candidate presentation inputs.
- T041/MG1-v2 integration PR: `#227`; merge: `d459217ef961bc6de4ee38358d56d9aceb113ace`.
- Current MG1 identities: Oracle `MG1-T023-TOPOLOGY-ORACLE-v2`; Capability-Source-Epoch `MG1-2026-08-25-v2`; Presentation revision `MG1-T023-PRESENTATIONS-v2`; Corpus `MG1-T023-CORPUS-v1` unchanged.
- Frozen presentation authority includes seven exact candidate `SKILL.md` files, three exact shared capability references and `evals/skill_activation_topology/presentations/manifest.json`.
- Candidate materialization is byte-copy only; Executor may not author or rewrite activation wording.
- `activation_surface_bytes` is reported separately; `loaded_reference_bytes` follows the exact manifest unique-reference UTF-8 byte-sum rule. Neither is an exact token claim.
- All MG1 v1 corpus expectations, required Codex/native-Windows/GPT-5.6-Sol/Medium live cell, 3-trial method, metrics, non-regression conditions, numeric thresholds and selection rule are preserved.
- T023 is now the next critical-path executable work. T025 remains parallel-eligible but is not selected.

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

## T041 / MG1-v2 identity

```text
Task: T041
Status: INTEGRATED / CONTROLLING
Task Contract: docs/tasks/T041-mg1-candidate-presentation-oracle-revision.md
Integration PR: #227
Integration merge: d459217ef961bc6de4ee38358d56d9aceb113ace
Oracle revision: MG1-T023-TOPOLOGY-ORACLE-v2
Capability source epoch: MG1-2026-08-25-v2
Presentation revision: MG1-T023-PRESENTATIONS-v2
Corpus ID: MG1-T023-CORPUS-v1
```

## T023 next executable identity

```text
Task: T023
Status: RELAUNCH FROM FRESH DEVELOP
Task Contract: docs/tasks/T023-unified-skill-profile-activation-evals.md
Expected branch: test/t023-skill-activation-topology-evals
Expected handoff: handoffs/T023-executor-handoff.json
Previous blocked HEAD: b7402bbaea52d7ac4342b848c73bf56a7bb4bbef
Previous live trials: 0/360
Use fresh canonical develop; do not continue from blocked branch history.
```

## Next action

1. Integrate this O170 checkpoint branch into `develop` through PR.
2. Refresh canonical `develop` identity.
3. Show D055 for T023: Codex `NEW`, GPT-5.6 Sol, High.
4. Relaunch T023 from fresh canonical `develop` using only `docs/tasks/T023-unified-skill-profile-activation-evals.md` plus D042 freshness.
5. Executor mechanically materializes candidates from the frozen v2 manifest, executes the required matrix/evidence and preserves all Orchestrator-owned semantic assets unchanged.
6. Orchestrator independently reviews raw evidence and applies the frozen selection rule before accepting any topology.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not merge or continue from the blocked T023 branch; do not alter corpus expectations or thresholds; do not allow Executor-authored candidate activation wording; do not change Core/engine/profile behavior to favor a candidate; do not introduce independent products, per-entrypoint versions, portable Skill-to-Skill dependency or multi-install packaging; do not write directly to `main`/`develop`.
