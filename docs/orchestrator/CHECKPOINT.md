# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O183  
Canonical-Branch: `develop`  
Current-Work-Unit: T047/MG1-v8 cost-bounded host evaluation is integrated and controlling; T023 is ready for a fresh v8 epoch gated by host-capability preflight  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: ChatGPT Orchestrator

## Durable frontier

- D053, D054, D040, D042, D048, D050, D051, D052, D055 and D056 remain controlling. Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`.
- T023 v2: closed `BLOCKED / EXPERIMENT CLOSED`; review `docs/reviews/T023-R1.md`.
- T023 v3: closed `BLOCKED / EXECUTION-INCOMPLETE`; review `docs/reviews/T023-R2.md`.
- T023 v4: closed `BLOCKED / EXTERNAL CAPACITY`; review `docs/reviews/T023-R3.md`.
- T023 v5: `SUPERSEDED_PRE_EXECUTION`; review `docs/reviews/T023-R4.md`.
- T023 v6: closed `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE`; review `docs/reviews/T023-R5.md`.
- T023 v7: closed `BLOCKED / HOST EXECUTION ENVELOPE DEFECT`; review `docs/reviews/T023-R6.md`.
- V7 submitted Executor HEAD `6e126d0a978a5ab1e306889f1f6333dbc98b21bb`; evidence integration PR `#244`; merge `4b97782effba1ad552c7d4264abfa79eaaba677f`.
- V7 produced 171 valid Stage-R repetitions plus 11 capacity events. Those records are diagnostic only and MUST NOT enter v8 scoring.
- V7 candidate-level zero host-observed activation is not carried forward as a product conclusion because the live host envelope repeatedly rejected candidate-body reads that v7 required for activation evidence.
- T047/MG1-v8 is integrated by PR `#245`, merge `83ed6c3655446962a642867288b38de3e3cd0012`.
- Current oracle: `MG1-T023-TOPOLOGY-ORACLE-v8`; execution epoch: `MG1-T023-EXECUTION-v8`.
- Capability source remains `MG1-2026-08-25-v3`; presentations remain `MG1-T023-PRESENTATIONS-v3`; trial envelope remains `MG1-T023-TRIAL-ENVELOPE-v2`.
- Fresh holdout is `MG1-T023-CORPUS-v4`: 40 new exact strings with unchanged semantic class/fixture distribution.
- Candidate presentation/reference bytes, qualification thresholds, zero-tolerance safety gates, paired 2+1 aggregation, `observed_context_bytes` meaning and D050 selection percentages remain unchanged from v7.

## T047 / MG1-v8 controlling identity

```text
Task: T047
Status: INTEGRATED / CONTROLLING
Task Contract: docs/tasks/T047-mg1-v8-cost-bounded-host-evaluation.md
Research: docs/research/MG1-V7-COST-AND-HOST-EXECUTION-ANALYSIS.md
Prior Review: docs/reviews/T023-R6.md
Integration PR: #245
Integration merge: 83ed6c3655446962a642867288b38de3e3cd0012
Oracle: MG1-T023-TOPOLOGY-ORACLE-v8
Execution epoch: MG1-T023-EXECUTION-v8
Capability source epoch: MG1-2026-08-25-v3
Presentation revision: MG1-T023-PRESENTATIONS-v3
Corpus: MG1-T023-CORPUS-v4
Trial envelope: MG1-T023-TRIAL-ENVELOPE-v2
Full-completion ceiling: 480 valid acceptance repetitions
Normal behavior: exact early termination when a frozen decision becomes irreversible
```

## V8 host-capability gate

- No acceptance prompt may run before a synthetic local-Skill canary passes twice under the exact intended host profile.
- Canary proves metadata discovery, successful `SKILL.md` body read/use, host trace distinction, exact body nonce, structured output, no required-read policy rejection, no unrelated app/plugin catalog payload, and the workspace mutation postcondition.
- Try `read-only` first. Use `workspace-write` only as the preregistered fallback when read-only specifically cannot expose the required body-read/use path, and only with zero unexpected model-caused writes.
- If neither profile passes twice, stop `BLOCKED / HOST_CAPABILITY_PREFLIGHT` with zero acceptance observations.
- The selected profile becomes immutable for the v8 epoch.

## V8 minimal host surface

The effective canary/acceptance surface must ignore user config and execpolicy `.rules`, retain local shell/Skill behavior, and disable Apps/connectors, the remote plugin catalog, multi-agent collaboration, automatic Skill MCP dependency installation, PowerShell shell snapshot and web search. Sessions remain ephemeral and use OS-temporary isolated workspaces. Exact version-specific adapter syntax remains Executor-owned under D054.

After a successful preflight, any required candidate-body read rejection or reappearance of unrelated app/plugin catalog material is `HOST_SURFACE_DRIFT`: do not score the affected observation as candidate behavior and stop new scheduling until exact profile identity is restored.

## V8 cost-bounded scheduling

- Paired 2+1 semantics remain unchanged for case/candidate pairs that are still required.
- Fixed case order: cross-profile, ambiguous, generic negative, near-miss, Consumer positive, source positive, external-Skill positive, multi-intent; ascending case id inside each class.
- Any mandatory zero-tolerance failure terminates the candidate immediately.
- After each finalized aggregate, compute the frozen optimistic final metric bounds. If qualification remains impossible even assuming perfect unfinished work, mark `FUTILE_QUALIFICATION` and stop all remaining calls for that candidate.
- After a reference exists, challengers additionally stop with `FUTILE_MATERIALITY` when even optimistic completion cannot satisfy the unchanged D050 material-advantage conditions, including an optimistic zero-byte bound for unfinished context medians.
- Every early stop requires a machine-recomputable certificate. Unexecuted cases are `NOT_SCHEDULED_FUTILITY` and never become fabricated metric rows.
- The former Stage-R `160–240` and full-run `320–480` figures are full-completion ranges/ceilings, not minimum expenditure.

## Runtime and cost controls

- Required acceptance cell remains Codex / native Windows / GPT-5.6 Sol / Medium.
- Each non-capacity model attempt has a 180-second timeout.
- Explicit usage-limit/quota events remain non-attempt capacity pauses; same-epoch resume preserves valid observations and terminal futility states.
- Persist provider-reported input/cached-input/reasoning/output/total tokens when available, plus tool calls, rejected tool calls, unrelated resource count/bytes, duration and effective host profile.
- If exact token usage is unavailable, record that fact and use available proxies; do not invent estimates.
- Experimental rollout-budget reminders are not part of v8 acceptance.

## T023 next executable identity

```text
Task: T023
Status: READY / FRESH V8 EPOCH
Task Contract: docs/tasks/T023-unified-skill-profile-activation-evals.md
Controlling revision: docs/tasks/T047-mg1-v8-cost-bounded-host-evaluation.md
Expected handoff: handoffs/T023-executor-handoff.json
Required acceptance cell: Codex / native Windows / GPT-5.6 Sol / Medium
Prior v2/v3/v4/v6/v7 observations allowed in v8 score: 0
Prior v5 live observations: 0
Pre-acceptance requirement: two passing synthetic host-capability canary repetitions
```

## Next action

1. Refresh current canonical `develop` before Executor launch.
2. Show D055 for T023: Codex `NEW`, GPT-5.6 Sol, High for technical v8 harness/preflight/futility implementation; the live acceptance observations themselves remain GPT-5.6 Sol / Medium.
3. Relaunch T023 from fresh canonical `develop` using only `docs/tasks/T023-unified-skill-profile-activation-evals.md` plus D042 freshness.
4. Executor mechanically implements v8 synthetic preflight, minimal effective host surface, host-surface drift detection, exact futility/materiality scheduling, 180-second attempts and cost telemetry, then performs Code Review & Verify.
5. Executor MUST stop before any acceptance prompt if the preflight does not pass twice under one permitted host profile.
6. If preflight passes, Executor starts a fresh v8 acceptance epoch and sends only observations still required by the frozen decision logic; it MUST NOT alter candidate bytes, expectations, thresholds or D050 selection semantics.
7. Orchestrator independently reviews the submitted v8 evidence and applies the frozen selection rule.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not rerun v7; do not import v7 or earlier observations into v8 score; do not launch any v8 acceptance prompt before the synthetic canary passes; do not score policy-rejected body reads as candidate non-activation; do not re-enable unrelated Apps/plugin surfaces during acceptance; do not weaken thresholds or zero-tolerance gates; do not change candidate presentation/reference bytes; do not treat futility-skipped cases as observations; do not write directly to `main`/`develop`.
