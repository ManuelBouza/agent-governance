# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O171  
Canonical-Branch: `develop`  
Current-Work-Unit: T023 MG1-v2 closed BLOCKED; T042/MG1-v3 independent holdout restart is the current Orchestrator gate, then T023 relaunch  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: ChatGPT Orchestrator

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D040 single current protocol-version authority, D042 freshness, D048 final-publication boundary, D050 topology evaluation, D051 one-product/single-install, D052 conformance ownership, D055 launch profiles and D056 progress-note rules remain controlling.
- Current routed Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`.
- T023 MG1-v2 executed from `develop@c7239ffd5b97d225e85499c25a6afd6d9880cdf9` and ended `BLOCKED` at submitted Executor HEAD `2da17551d42b5a2fc6b37ad952ea835a1a89bcbe`; implementation/evidence anchor `f87b924f1b9481dde68279f24ff4c4c35f51c868`.
- T023-v2 executed all `360/360` Codex/native-Windows/GPT-5.6-Sol/Medium trials. Full deterministic suite `417 passed`; profile isolation `48 passed`; source-independence `8 passed`; Ruff/diff green; frozen MG1-v2 semantic assets unchanged.
- Evidence integration PR `#229`, merge `c070c0bd5924aa283237d3a1995c58579bd0500a`. This integrates harness/tests/raw evidence/handoff only; it does not accept T023 or select a topology.
- T023 review: `docs/reviews/T023-R1.md`, status `BLOCKED / EXPERIMENT CLOSED`.
- Frozen v2 selection produced no qualifying B0/B1 reference. No topology is accepted.
- Two Specify defects are confirmed for future experiments: v2 `loaded_reference_bytes` is candidate-invariant, and v2 ambiguous grading conflates neutral clarification activation with permission broadening.
- MG1-v2 remains immutable and must not be rescored or tuned post hoc.
- T042 is the Orchestrator-owned restart authority: `docs/tasks/T042-mg1-v3-independent-holdout-restart.md`.
- MG1-v3 identities: Oracle `MG1-T023-TOPOLOGY-ORACLE-v3`; Capability-Source-Epoch `MG1-2026-08-25-v3`; Presentation revision `MG1-T023-PRESENTATIONS-v3`; Corpus `MG1-T023-CORPUS-v2`.
- V3 freezes seven exact candidate Skill surfaces and three exact shared references under `evals/skill_activation_topology/presentations-v3/`, materialized only by byte-copy through the current manifest.
- V3 acceptance holdout is 40 new exact prompts; none of the exact strings was executed in v2. Required matrix is `40 x 4 x 3 = 480` scored live trials.
- V3 ambiguous semantics: neutral B0/B1 may activate solely to return `clarify-context`; this alone is not permission broadening. F2/G3 profile-specific peers remain unselected until context is sufficient.
- V3 cross-profile semantics: legitimate boundary-checking entrypoint activation is permitted; a violation requires forbidden capability/profile grant/performance or failure of bounded rejection.
- V3 context selection metric is candidate-sensitive `observed_context_bytes`, derived from unique successful host reads of candidate `SKILL.md` plus candidate references. `loaded_reference_bytes` becomes diagnostic only.
- V3 keeps routing thresholds and D050 material-improvement percentages unchanged; post-result weakening remains forbidden.
- T025 remains independently dependency-eligible but is not the selected critical-path action.

## Process incident

During convergence after the second T023 blocker, the Orchestrator accidentally created `tmp/placeholder` directly on `develop`, commit `6799335c757bfe60dc4401c481cbcf342b5963e3`, then immediately deleted it in commit `5743aaae90c1b967f4da436493ba67ac9d8cced6`.

The net repository content is unchanged by those two commits. They are administrative incident history only, not product/oracle/Executor evidence or acceptance authority. Do not rewrite history to remove them and do not use them as semantic anchors.

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

## T023 v2 closed identity

```text
Task: T023
Status: BLOCKED / EXPERIMENT CLOSED
Review: docs/reviews/T023-R1.md
Submitted Executor HEAD: 2da17551d42b5a2fc6b37ad952ea835a1a89bcbe
Evidence integration PR: #229
Evidence merge: c070c0bd5924aa283237d3a1995c58579bd0500a
Oracle: MG1-T023-TOPOLOGY-ORACLE-v2
Corpus: MG1-T023-CORPUS-v1
Live trials: 360/360
Selected topology: none
```

## T042 / MG1-v3 identity

```text
Task: T042
Status: ORCHESTRATOR-CONFORMANCE / PENDING INTEGRATION
Task Contract: docs/tasks/T042-mg1-v3-independent-holdout-restart.md
Oracle: MG1-T023-TOPOLOGY-ORACLE-v3
Capability source epoch: MG1-2026-08-25-v3
Presentation revision: MG1-T023-PRESENTATIONS-v3
Corpus: MG1-T023-CORPUS-v2
Scored matrix after integration: 480 trials
```

## Next action

1. Review the complete `docs/t042-mg1-v3-restart` diff; it must contain only Orchestrator Markdown and D052 semantic presentation/oracle assets, with no runtime/Core/harness/evidence mutation.
2. Integrate T042/MG1-v3 through an Orchestrator PR into `develop`.
3. Refresh canonical `develop` and confirm all v3 identities at that exact baseline.
4. Show D055 for T023: Codex `NEW`, GPT-5.6 Sol, High.
5. Relaunch T023 from fresh canonical `develop` using only `docs/tasks/T023-unified-skill-profile-activation-evals.md` plus D042 freshness.
6. Executor may mechanically adapt the existing harness to the v3 frozen fields/semantics, but must not edit Orchestrator-owned Markdown, holdout membership/expectations, presentation wording, thresholds or selection meaning.
7. Executor executes the complete 480-trial holdout and v2 cases only as non-scored regression diagnostics if useful.
8. Orchestrator independently reviews evidence and applies the frozen v3 selection rule before any topology acceptance.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not rescore or modify MG1-v2; do not use v2 acceptance cases in the v3 score; do not tune v3 after holdout execution begins; do not allow Executor-authored candidate activation wording; do not change Core/engine/profile behavior to favor a candidate; do not introduce independent products, per-entrypoint versions, portable Skill-to-Skill dependency or multi-install packaging; do not write directly to `main`/`develop`.
