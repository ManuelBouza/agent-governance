# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O182  
Canonical-Branch: `develop`  
Current-Work-Unit: T047/MG1-v8 cost-bounded host evaluation revision is ready for integration; T023 must not relaunch until v8 is canonical  
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
- V7 candidate-level zero host-observed activation is not carried forward as a product conclusion because the live host envelope repeatedly rejected the candidate-body reads that v7 required for activation evidence.
- T047 is the prospective v8 authority: `docs/tasks/T047-mg1-v8-cost-bounded-host-evaluation.md`.
- Research: `docs/research/MG1-V7-COST-AND-HOST-EXECUTION-ANALYSIS.md`.
- Proposed oracle: `MG1-T023-TOPOLOGY-ORACLE-v8`; execution epoch: `MG1-T023-EXECUTION-v8`.
- Capability source remains `MG1-2026-08-25-v3`; presentations remain `MG1-T023-PRESENTATIONS-v3`; trial envelope remains `MG1-T023-TRIAL-ENVELOPE-v2`.
- Fresh holdout: `MG1-T023-CORPUS-v4`, 40 new exact strings with unchanged semantic class/fixture distribution.

## T047 / MG1-v8 method

### Host preflight

- No acceptance prompt may run before a synthetic local-Skill canary passes twice under the exact intended host profile.
- Canary proves metadata discovery, successful `SKILL.md` body read/use, host trace distinction, exact body nonce, structured output, no required-read policy rejection, no unrelated app/plugin catalog payload, and workspace mutation postcondition.
- Try `read-only` first; use `workspace-write` only as a preregistered fallback when read-only specifically cannot expose the required body-read/use path, and only with zero unexpected model-caused writes.
- If neither profile passes twice, stop `BLOCKED / HOST_CAPABILITY_PREFLIGHT` with zero acceptance observations.

### Minimal host surface

Acceptance effective state must ignore user config and execpolicy `.rules`, retain local shell/Skill behavior, and disable Apps/connectors, remote plugin catalog, multi-agent, automatic Skill MCP dependency installation, PowerShell shell snapshot and web search. Sessions remain ephemeral and use OS-temporary isolated workspaces.

### Cost-bounded scheduling

- Paired 2+1 semantics remain unchanged for pairs still required.
- Case order is fixed: cross-profile, ambiguous, negative, near-miss, Consumer positive, source positive, external-Skill positive, multi-intent.
- Any mandatory zero-tolerance failure terminates the candidate immediately.
- After each aggregate, compute optimistic final metric bounds. If qualification remains impossible even assuming perfect unfinished work, mark `FUTILE_QUALIFICATION` and stop that candidate.
- After reference selection, challengers additionally stop when material advantage is impossible under optimistic completion, including an optimistic zero-byte bound for unfinished context medians.
- Unexecuted cases are explicitly `NOT_SCHEDULED_FUTILITY`; they are never fabricated as metric rows.
- Previous 160–240 Stage-R and 320–480 full-run figures are worst-case full-completion ranges/ceilings, not mandatory spend.

### Runtime/cost controls

- Required acceptance cell remains Codex / native Windows / GPT-5.6 Sol / Medium.
- Timeout is 180 seconds per non-capacity model attempt.
- Capacity events remain non-attempt pauses with same-epoch resume.
- Persist token usage when Codex exposes it plus cached tokens, reasoning/output tokens, tool calls, rejected tool calls, unrelated resource counts/bytes, duration and effective host profile.
- Experimental rollout-budget reminders are not part of v8 acceptance.

## T047 / MG1-v8 identity

```text
Task: T047
Status: ORCHESTRATOR-CONFORMANCE / READY_FOR_INTEGRATION
Task Contract: docs/tasks/T047-mg1-v8-cost-bounded-host-evaluation.md
Research: docs/research/MG1-V7-COST-AND-HOST-EXECUTION-ANALYSIS.md
Prior Review: docs/reviews/T023-R6.md
Oracle: MG1-T023-TOPOLOGY-ORACLE-v8
Execution epoch: MG1-T023-EXECUTION-v8
Capability source epoch: MG1-2026-08-25-v3
Presentation revision: MG1-T023-PRESENTATIONS-v3
Corpus: MG1-T023-CORPUS-v4
Trial envelope: MG1-T023-TRIAL-ENVELOPE-v2
Full-completion ceiling: 480 valid acceptance repetitions
Normal behavior: exact early termination when decision becomes irreversible
```

## Next action

1. Validate T047 branch artifacts and complete diff against canonical `develop@4b97782effba1ad552c7d4264abfa79eaaba677f`.
2. Integrate T047/MG1-v8 through PR only if changes are Orchestrator-owned Markdown plus authorized D052 corpus/oracle assets.
3. Refresh canonical `develop` and checkpoint v8 as `INTEGRATED / CONTROLLING`.
4. Only then show D055 and relaunch T023 from fresh canonical `develop`.
5. Executor mechanically implements synthetic preflight, minimal effective host surface, host-surface drift detection, exact futility/materiality scheduling, 180-second attempts and cost telemetry; it MUST NOT alter candidate bytes or semantic selection authority.
6. Orchestrator independently reviews successor evidence and accepts a topology only under the frozen v8 rule.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not rerun v7; do not import v7 or earlier observations into v8 score; do not launch any v8 acceptance prompt before the synthetic canary passes; do not score policy-rejected body reads as candidate non-activation; do not re-enable unrelated Apps/plugin surfaces during acceptance; do not weaken thresholds or zero-tolerance gates; do not change candidate presentation/reference bytes; do not treat missing futility-skipped cases as observations; do not write directly to `main`/`develop`.
