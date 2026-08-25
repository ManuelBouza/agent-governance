# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O172  
Canonical-Branch: `develop`  
Current-Work-Unit: T042/MG1-v3 integrated; T023 is next executable relaunch on the fresh 480-trial holdout  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD, D054 execution-mechanics ownership, D040 single current protocol-version authority, D042 freshness, D048 final-publication boundary, D050 topology evaluation, D051 one-product/single-install, D052 conformance ownership, D055 launch profiles and D056 progress-note rules remain controlling.
- Current routed Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`.
- T023 MG1-v2 is closed `BLOCKED / EXPERIMENT CLOSED`; review `docs/reviews/T023-R1.md`.
- T023-v2 submitted Executor HEAD `2da17551d42b5a2fc6b37ad952ea835a1a89bcbe`; evidence integration PR `#229`; merge `c070c0bd5924aa283237d3a1995c58579bd0500a`.
- V2 executed all `360/360` live trials, full deterministic `417 passed`, profile isolation `48 passed`, source independence `8 passed`, Ruff/diff green, and no frozen semantic drift. No topology was selected.
- MG1-v2 remains immutable and must not be rescored or tuned post hoc.
- T042/MG1-v3 is integrated by PR `#230`, merge `dc5b31b8ab74a3032980a847fff48aaa0c54729e`.
- Current MG1 identities: Oracle `MG1-T023-TOPOLOGY-ORACLE-v3`; Capability-Source-Epoch `MG1-2026-08-25-v3`; Presentation revision `MG1-T023-PRESENTATIONS-v3`; Corpus `MG1-T023-CORPUS-v2`.
- V3 freezes seven exact candidate Skill surfaces and three exact shared references under `evals/skill_activation_topology/presentations-v3/`, materialized only by byte-copy through `evals/skill_activation_topology/presentations/manifest.json`.
- V3 acceptance holdout is 40 new exact prompts; none of the exact strings was executed in v2. Required scored matrix is `40 x 4 x 3 = 480` live trials.
- V3 ambiguous semantics: neutral B0/B1 may activate solely to return `clarify-context`; this alone is not permission broadening. F2/G3 profile-specific peers remain unselected until context is sufficient.
- V3 cross-profile semantics: legitimate boundary-checking entrypoint activation is permitted; a violation requires forbidden capability/profile grant/performance or failure of bounded rejection.
- V3 selection context metric is candidate-sensitive `observed_context_bytes`, derived from unique successful host reads of candidate `SKILL.md` plus candidate references. `loaded_reference_bytes` is diagnostic only.
- V3 retains routing thresholds and D050 material-improvement percentages; post-result weakening remains forbidden.
- Executor may mechanically adapt the existing harness to v3 fields/semantics, but cannot change Orchestrator-owned corpus, presentation wording, thresholds or selection meaning.
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

## T042 / MG1-v3 identity

```text
Task: T042
Status: INTEGRATED / CONTROLLING
Task Contract: docs/tasks/T042-mg1-v3-independent-holdout-restart.md
Integration PR: #230
Integration merge: dc5b31b8ab74a3032980a847fff48aaa0c54729e
Oracle: MG1-T023-TOPOLOGY-ORACLE-v3
Capability source epoch: MG1-2026-08-25-v3
Presentation revision: MG1-T023-PRESENTATIONS-v3
Corpus: MG1-T023-CORPUS-v2
Scored matrix: 480 trials
```

## T023 next executable identity

```text
Task: T023
Status: RELAUNCH FROM FRESH DEVELOP / V3 HOLDOUT
Task Contract: docs/tasks/T023-unified-skill-profile-activation-evals.md
Expected branch: test/t023-skill-activation-topology-evals
Expected handoff: handoffs/T023-executor-handoff.json
Previous v2 submitted HEAD: 2da17551d42b5a2fc6b37ad952ea835a1a89bcbe
Previous v2 result: BLOCKED / closed
Use fresh canonical develop; do not continue from v2 branch history.
```

## Next action

1. Integrate this O172 checkpoint branch into `develop` through PR.
2. Refresh canonical `develop` identity.
3. Show D055 for T023: Codex `NEW`, GPT-5.6 Sol, High.
4. Relaunch T023 from fresh canonical `develop` using only `docs/tasks/T023-unified-skill-profile-activation-evals.md` plus D042 freshness.
5. Executor mechanically adapts the existing harness to v3 frozen fields/semantics, executes all 480 scored trials, may run v2 cases only as non-scored diagnostics, and preserves all Orchestrator-owned semantic assets unchanged.
6. Orchestrator independently reviews raw evidence and applies the frozen v3 selection rule before accepting any topology.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not rescore or modify MG1-v2; do not use v2 acceptance cases in the v3 score; do not tune v3 after holdout execution begins; do not allow Executor-authored candidate activation wording; do not change Core/engine/profile behavior to favor a candidate; do not introduce independent products, per-entrypoint versions, portable Skill-to-Skill dependency or multi-install packaging; do not write directly to `main`/`develop`.
