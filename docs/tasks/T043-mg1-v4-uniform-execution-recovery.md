# T043 — MG1-v4 Uniform Execution Recovery

## Identity

- Task ID: `T043`
- Status: `ORCHESTRATOR-CONFORMANCE`
- Base branch: `develop`
- Owner: ChatGPT Orchestrator
- Test-Authorship-Mode: `orchestrator-conformance`
- Re-entry stage: `Specify`

## Objective

Restart T023 acceptance execution prospectively after the incomplete MG1-v3 run, without changing candidate semantics, corpus expectations, thresholds, or topology selection meaning.

## Frozen recovery method

The next acceptance execution is a new execution epoch under `MG1-T023-TOPOLOGY-ORACLE-v4`.

- The prior MG1-v3 incomplete run is diagnostic only and contributes zero scored observations to v4.
- The complete 40-case x 4-candidate x 3-repetition matrix is executed anew: exactly 480 logical scored observations.
- Each logical observation starts in a fresh Codex thread and disposable workspace.
- Each logical observation permits at most 2 execution attempts.
- Each attempt uses the same frozen prompt, candidate, repetition, model, effort, host, and candidate materialization.
- Uniform per-attempt timeout: 600 seconds.
- A failed attempt is never scored and must be retained as structured execution-failure evidence.
- The first attempt that returns a valid structured observation becomes the sole scored result for that logical observation.
- If both attempts fail for any logical observation, the acceptance run is `BLOCKED`; no partial metrics or topology selection may be published.
- Retry count and failure class are diagnostic only and must be reported per candidate; they do not replace routing/context metrics.
- No retry may occur after a valid structured observation exists for that logical observation.
- Candidate order rotation and all MG1-v3 clean-context requirements remain unchanged.

## Preserved semantics

Unchanged from MG1-v3:

- candidate identities B0/B1/F2/G3;
- `MG1-2026-08-25-v3` capability-source epoch;
- `MG1-T023-PRESENTATIONS-v3` exact presentation surfaces;
- `MG1-T023-CORPUS-v2` 40-case holdout and expected outcomes;
- clarification/cross-profile grading semantics;
- qualifying thresholds;
- D050 material-improvement percentages and tie-breaks;
- one-product/Core/engine/profile/isolation requirements;
- Codex/native-Windows/GPT-5.6-Sol/Medium required live cell.

## Executor boundary

The Executor may mechanically adapt harness/recovery plumbing and execute v4. It must not edit committed Markdown or any Orchestrator-owned semantic asset except through already integrated authority. It must preserve all failed-attempt evidence, verify exactly 480 scored logical observations before scoring, and stop fail-closed if the recovery method cannot be applied uniformly.

## Acceptance

T043 is complete when the v4 oracle identity/recovery method is integrated into `develop` before any v4 live attempt. T023 may then relaunch in a NEW Executor session from fresh canonical `develop`.
