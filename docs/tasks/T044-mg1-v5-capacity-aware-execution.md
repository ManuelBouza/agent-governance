# T044 — MG1-v5 Capacity-Aware Execution Method

## Identity

- Task ID: `T044`
- Status: `PLANNED`
- Type: `orchestrator-conformance`
- Owner: ChatGPT Orchestrator
- Affects: `T023`
- D053 re-entry stage: `Specify`
- New oracle: `MG1-T023-TOPOLOGY-ORACLE-v5`
- New execution epoch: `MG1-T023-EXECUTION-v5`
- Capability source remains: `MG1-2026-08-25-v3`
- Presentation revision remains: `MG1-T023-PRESENTATIONS-v3`
- Corpus remains: `MG1-T023-CORPUS-v2`

## Trigger

MG1-v4 ended `BLOCKED / EXTERNAL CAPACITY` after 31 valid observations. Eight attempts across four logical observations terminated with explicit Codex usage-limit events. No partial score or topology selection was computed.

## Objective

Define a prospective capacity-aware execution protocol that separates external account-capacity events from model-evaluation attempts so the 480-observation acceptance epoch can pause and resume without discarding valid observations or consuming model-attempt budget on provider/account unavailability.

## Preserved semantics

T044 MUST NOT change:

- the 40-case holdout membership or exact prompts;
- candidate identities, topology mapping or candidate presentation wording;
- expected entrypoints, semantic outcomes, capability/permission boundaries;
- routing/context metrics;
- qualifying thresholds;
- D050 material-improvement percentages or tie-breaks;
- Core/runtime/profile behavior;
- required Codex/native-Windows/GPT-5.6-Sol/Medium live cell.

## Capacity-aware protocol

A new v5 acceptance epoch starts from zero scored observations. V2/v3/v4 observations do not enter v5 scoring.

For each of the 480 logical observations:

1. The logical observation retains the v4 maximum of two **model attempts**.
2. Every model attempt uses a fresh Codex thread and disposable workspace, frozen candidate materialization, 600-second timeout, exact required model/effort and exact frozen prompt.
3. A valid structured model response consumes the attempt and, if it is the first valid response, becomes the sole scored result for that logical observation.
4. A timeout, malformed response, provider failure other than an explicitly classified capacity event, or other non-capacity execution failure consumes the current model attempt.
5. An **external capacity event** is recognized only when the Codex/provider trace contains an explicit account/service usage-limit or quota-capacity failure before a valid structured model result is produced.
6. An external capacity event does **not** consume a model attempt. It is persisted separately as diagnostic evidence, the affected logical observation remains pending at the same attempt ordinal, and new live scheduling stops promptly.
7. The v5 epoch may later resume from its persisted evidence root after capacity is available. Previously valid v5 observations remain authoritative and MUST NOT be rerun or replaced; pending observations continue in the deterministic schedule from the preserved state.
8. Resume must verify exact epoch identity, frozen asset hashes, harness identity, host/model/effort, completed logical-observation uniqueness, attempt ordinals and evidence integrity before issuing any new live call.
9. Capacity pauses may occur multiple times. Capacity-event count and elapsed wall-clock time are diagnostics only and do not enter candidate score.
10. If any logical observation exhausts two non-capacity model attempts without a valid result, the v5 epoch is `BLOCKED`; partial scoring/selection remains forbidden.

## Capacity readiness

Before each initial launch or resume, the Executor may perform at most one non-scored provider-capacity probe using a fixed trivial synthetic prompt that contains no holdout prompt or candidate contents. The probe is diagnostic only. A usage-limit response means do not start/resume the acceptance scheduler. A successful probe does not guarantee sufficient remaining capacity and does not enter scoring.

## Evidence requirements

Persist:

- 480 logical-observation identities and completion state;
- every model attempt and its ordinal;
- every capacity event separately from model attempts;
- exact thread/workspace identity per issued live call;
- raw/structured valid trial evidence;
- frozen asset/harness/runtime identity;
- pause/resume audit records;
- complete-epoch recomputability before metrics/selection.

## Acceptance boundary

Only a complete 480-observation v5 epoch may be scored. The frozen MG1 selection rule then applies unchanged. No v4 evidence may be imported as a v5 result.
