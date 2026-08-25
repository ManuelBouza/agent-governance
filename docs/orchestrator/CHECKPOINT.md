# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O169  
Canonical-Branch: `develop`  
Current-Work-Unit: T023 blocked pre-trial by MG1 presentation-spec defect; T041/MG1-v2 revision is ready for integration, then T023 relaunch  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: ChatGPT Orchestrator

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D040 single current protocol-version authority, D042 freshness, D048 final-publication boundary, D050 topology evaluation, D051 one-product/single-install, D052 conformance ownership, D055 launch profiles and D056 progress-note rules remain controlling.
- Current routed Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`.
- MG1 v1 integrated by PR `#225`; T023 launched from canonical `develop@04c42e0a4b7c3be6fa64b336df93521d07cd5805`.
- T023 submitted blocker HEAD: `b7402bbaea52d7ac4342b848c73bf56a7bb4bbef`; implementation/preflight anchor: `9fc4d5039a4f7d8dfeae45228f9fd47f18ff086e`; handoff `handoffs/T023-executor-handoff.json`.
- T023 status is `BLOCKED / ORACLE_DEFECT`, upstream re-entry stage `Specify`. The branch is exactly two evidence-only commits ahead of its base and is not an integration source.
- The blocker is valid: MG1 v1 specified candidate IDs and capability mappings but omitted exact host-visible B0/B1/F2/G3 Skill metadata/body/reference surfaces and deterministic candidate-specific load inputs.
- T023 executed `0/360` live trials. Full deterministic baseline remained green at `405 passed`; Ruff check/format and `git diff --check` passed; frozen MG1 v1 assets were byte-identical to canonical baseline.
- T041 is the Orchestrator-owned pre-trial correction authority: `docs/tasks/T041-mg1-candidate-presentation-oracle-revision.md`.
- T041/MG1 v2 freezes seven exact experimental candidate `SKILL.md` sources, three exact shared capability references and `evals/skill_activation_topology/presentations/manifest.json` as the lossless projection/load-accounting specification.
- Revised identities: Oracle `MG1-T023-TOPOLOGY-ORACLE-v2`; Capability-Source-Epoch `MG1-2026-08-25-v2`; Presentation revision `MG1-T023-PRESENTATIONS-v2`; Corpus remains `MG1-T023-CORPUS-v1` because membership/expectations are unchanged.
- MG1 v1 thresholds, required live cell, 3-trial method, metric meanings, mandatory non-regression conditions and final selection rule are preserved. This revision occurs before any comparative result and is not post-hoc tuning.
- After T041/MG1-v2 integration, T023 is relaunched from fresh canonical `develop`; the blocked T023 branch must not be merged or used as implementation base.
- T025 remains independently dependency-eligible but is not the current critical-path action.

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
Status: PLANNED / ORCHESTRATOR CONFORMANCE
Re-entry: Specify
Task Contract: docs/tasks/T041-mg1-candidate-presentation-oracle-revision.md
Oracle revision: MG1-T023-TOPOLOGY-ORACLE-v2
Capability source epoch: MG1-2026-08-25-v2
Presentation revision: MG1-T023-PRESENTATIONS-v2
Corpus ID: MG1-T023-CORPUS-v1 (unchanged)
```

## T023 re-entry identity

```text
Task: T023
Status: BLOCKED UNTIL T041/MG1-v2 INTEGRATION; THEN RELAUNCH
Task Contract: docs/tasks/T023-unified-skill-profile-activation-evals.md
Expected branch: test/t023-skill-activation-topology-evals
Expected handoff: handoffs/T023-executor-handoff.json
Previous blocked HEAD: b7402bbaea52d7ac4342b848c73bf56a7bb4bbef
Previous live trials: 0/360
```

## Next action

1. Review the complete T041/MG1-v2 diff; confirm it changes only Orchestrator-owned Markdown and D052 conformance/presentation assets.
2. Integrate T041/MG1-v2 through an Orchestrator PR into `develop`.
3. Refresh canonical `develop` identity and confirm v2 presentation/oracle assets at that exact baseline.
4. Show D055 for T023: Codex `NEW`, GPT-5.6 Sol, High.
5. Relaunch T023 from fresh canonical `develop` using only its Task Contract pointer plus D042 freshness. Do not continue from the blocked branch.
6. Executor mechanically materializes candidates from the frozen manifest, executes all required trials/evidence and preserves v2 semantic assets unchanged.
7. Orchestrator independently reviews and applies the frozen selection rule before acceptance.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not merge the blocked T023 branch; do not alter corpus expectations or thresholds; do not allow Executor-authored candidate activation wording; do not change Core/engine/profile behavior to favor a candidate; do not introduce independent products, per-entrypoint versions, portable Skill-to-Skill dependency or multi-install packaging; do not write directly to `main`/`develop`.
