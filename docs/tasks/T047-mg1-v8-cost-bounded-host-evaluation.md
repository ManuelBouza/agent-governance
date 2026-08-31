# T047 — MG1-v8 Cost-Bounded Host Evaluation Revision

## Identity

- Task ID: `T047`
- Status: `ORCHESTRATOR-CONFORMANCE`
- Type: `test/eval method + holdout revision`
- Base branch: `develop`
- Orchestrator branch: `spec/t047-mg1-v8-cost-bounded-host-eval`
- SDD profile: `ASSURED`
- Re-entry stage: `Specify`
- Test-Authorship-Mode: `orchestrator-conformance`
- Affects: `T023`

## Objective

Prospectively restart the T023 activation-topology experiment under a cost-bounded host method that preserves the existing product/routing acceptance semantics while correcting the MG1-v7 host execution-envelope defect and eliminating acceptance calls whose outcome can no longer affect topology selection.

MG1-v8 MUST:

1. prove the intended Codex Skill-body read/use and trace-observability path before any acceptance prompt is sent;
2. remove unrelated default host surfaces that inflated v7 context without contributing to Skill routing;
3. stop a candidate immediately when frozen thresholds make qualification mathematically impossible even under perfect remaining observations;
4. stop a challenger when frozen material-advantage criteria are mathematically impossible even under optimistic remaining observations;
5. retain enough raw evidence to recompute every early-stop certificate;
6. make no candidate presentation, threshold or D050 selection change based on v7 results.

## Evidence motivating re-entry

`docs/reviews/T023-R6.md` closes MG1-v7 as `BLOCKED / HOST EXECUTION ENVELOPE DEFECT`.

The v7 Executor submission produced 171 valid Stage-R repetitions and 11 capacity events. Inspected raw traces show:

- substantial unrelated app/plugin catalog material entering fresh Codex sessions;
- repeated `SKILL.md` read attempts rejected by host execution policy;
- zero host-observed candidate-body activations despite many model self-reports of activation;
- acceptance scoring continuing without a prior canary proving that the required Skill-body read/use path was operational.

V7 remains immutable. Its observations are diagnostic only and MUST NOT enter v8 scoring.

Research: `docs/research/MG1-V7-COST-AND-HOST-EXECUTION-ANALYSIS.md`.

## Preserved authority

V8 preserves unchanged:

- capability source epoch `MG1-2026-08-25-v3`;
- presentation revision `MG1-T023-PRESENTATIONS-v3` and all candidate/reference bytes;
- candidate topology definitions B0, B1, F2 and G3;
- clarification, cross-profile and permission-boundary semantics;
- deterministic/profile/source-independence gates;
- qualification thresholds: precision/recall/F1 >= 0.95, false/wrong/overactivation <= 0.05, overall semantic accuracy >= 0.95;
- mandatory zero cross-profile violations and ambiguous permission broadening;
- D050 B0/B1 reference and F2/G3 material-advantage percentages/tie-breaks;
- `observed_context_bytes` selection meaning;
- case-level paired 2+1 aggregation semantics;
- capacity-aware pause/resume and two non-capacity attempts per scheduled repetition;
- required acceptance model: Codex / native Windows / GPT-5.6 Sol / Medium.

V8 does **not** use v7 metric outcomes to rewrite candidate wording, thresholds or selection rules.

## MODIFIED — fresh v8 acceptance holdout

V8 uses `MG1-T023-CORPUS-v4`, a fresh set of 40 exact prompt strings with the same semantic class counts, expected capability/outcome semantics and fixture-role distribution as v7.

No exact v7 acceptance prompt is reused. No v2/v3/v4/v6/v7 observation may enter v8 score. V5 had no live acceptance observations.

## ADDED — mandatory host-capability preflight

Before any v8 acceptance case, the Executor MUST run a non-scored synthetic local-Skill canary under the exact model/effort and effective host configuration intended for acceptance.

The canary MUST NOT contain any acceptance prompt or candidate presentation/reference content.

### Synthetic Skill

Materialize a neutral disposable local Skill in the same host-discovery layout used by the candidates:

- `.agents/skills/mx-canary/SKILL.md`;
- small deterministic body with a unique nonce-like sentence that cannot be inferred from metadata alone;
- metadata/body wording must be unrelated to Agent Governance, candidate ids, profiles, routing classes or holdout semantics.

The canary prompt explicitly requests use of that synthetic local instruction and returns a minimal structured record containing the body nonce.

### Required canary proof

A host profile passes only when two fresh canary repetitions both prove:

1. local Skill metadata discovery occurred;
2. the `SKILL.md` body was successfully read/used;
3. host trace evidence distinguishes body read/use from metadata discovery;
4. the returned body nonce is correct;
5. structured output validation succeeds;
6. no execution-policy rejection affects the required body-read/use path;
7. no unrelated app/plugin catalog payload is materialized into the model/tool trace;
8. candidate-style workspace isolation and output-file behavior are preserved.

Any external capacity event during canary readiness pauses the canary and does not become an acceptance attempt.

### Least-permissive sandbox selection

Pre-register exactly this selection order:

1. test `read-only` under the minimal effective host surface;
2. if either read-only canary repetition fails specifically because the required body-read/use path is denied by the execution envelope, test `workspace-write` under the same minimal surface inside the OS-temporary disposable workspace;
3. `workspace-write` passes only if both canary repetitions show successful body read/use **and** no unexpected model-caused file mutation; expected harness-owned schema/result/evidence files do not count as model mutation;
4. if neither profile passes, stop T023 `BLOCKED / HOST_CAPABILITY_PREFLIGHT` before any acceptance prompt.

Once a profile passes, freeze its effective host configuration for the entire v8 acceptance epoch. No acceptance observation may use a different sandbox/configuration surface.

## ADDED — minimal effective Codex surface

The acceptance/canary host surface MUST have the following effective state, using version-appropriate Executor-owned adapter syntax resolved under D054:

- user config ignored;
- user/project execpolicy `.rules` ignored for the isolated eval workspace;
- local shell/Skill mechanism retained;
- Apps/connector integrations disabled;
- remote plugin catalog disabled;
- multi-agent collaboration disabled;
- automatic Skill MCP dependency installation disabled;
- PowerShell shell snapshot disabled;
- web search disabled;
- ephemeral session behavior retained;
- no unrelated MCP server, plugin or app may be explicitly added by the harness.

These controls are method identity, not optional performance tuning. If the installed Codex version cannot realize an equivalent effective surface, stop before acceptance rather than silently broadening tools/context.

## PRESERVED — stimulus/workspace/fixture isolation

V7's neutral in-band envelope and workspace rules remain controlling:

- exact corpus prompt, two newlines, exact suffix `Return only the required structured record.`;
- no extra domain-bearing evaluator prose;
- OS-temporary disposable workspace outside/not linked to canonical source checkout;
- forbidden root-substring/path-leak checks;
- exact `fixture_role` materialization only;
- ambiguous/negative/near-miss cases remain neutral.

Trial envelope remains `MG1-T023-TRIAL-ENVELOPE-v2` unless a mechanical schema revision is required solely to record v8 method identity without changing the model-visible suffix or fixture semantics.

## PRESERVED + HARDENED — activation observability

Scored activation remains host-observable candidate-body activation. Model self-report alone cannot score activation.

Before acceptance, canary success MUST prove that the chosen host profile can expose the required read/use evidence.

After acceptance begins, any occurrence of either condition below is `HOST_SURFACE_DRIFT` and immediately pauses/stops new scheduling before the affected observation is scored:

- a required candidate-body read/use is explicitly rejected by host policy after the preflight established that the same class of read/use is permitted;
- unrelated app/plugin catalog content reappears despite the frozen minimal surface.

The affected observation is not a candidate failure and does not consume a semantic acceptance repetition. Resume is permitted only after exact host/profile identity and preflight invariants are restored; previously valid v8 observations remain authoritative.

## MODIFIED — 180-second model-attempt timeout

Each non-capacity model attempt has a 180-second timeout rather than 600 seconds.

A timeout remains a non-capacity model-attempt failure. Two non-capacity failures for the same scheduled repetition block the epoch as before.

Explicit host-surface drift is not allowed to run until timeout merely to accumulate rejected-tool loops; it stops scheduling as soon as the harness can classify it from trace evidence.

## PRESERVED — paired 2+1 aggregation

For every case/candidate pair that is actually required before a candidate becomes terminal:

- two valid repetitions are required;
- exactly one third valid repetition is required when the first two disagree on any frozen trigger field/context;
- no fourth valid repetition is permitted;
- ordinary discrete fields use majority aggregation;
- context uses median aggregation;
- cross-profile and ambiguous mandatory boundaries inspect each valid repetition and remain any-occurrence zero-tolerance.

If an any-occurrence mandatory violation disqualifies a candidate on the first repetition of a pair, no additional repetition for that candidate is required because qualification is already impossible.

## ADDED — deterministic decision-order groups

Within each candidate stage, schedule cases by immutable semantic consequence rather than corpus-file order:

1. **critical boundary group** — all cross-profile cases, then all ambiguous cases;
2. **false-activation group** — all generic negative cases, then all near-miss cases;
3. **activation/semantic group** — positive Consumer, positive source-maintainer, positive external-Skill-trust, then multi-intent cases.

Within each class, order by ascending case id. Candidate order continues to rotate deterministically inside a scheduling wave to avoid fixed candidate-order bias.

The order is frozen before v8 live execution and does not depend on v7 candidate outcomes.

## ADDED — qualification-impossibility futility certificate

After each finalized case aggregate, and immediately after any valid repetition capable of triggering a mandatory any-occurrence gate, the harness MUST recompute whether the candidate can still qualify.

A candidate becomes `FUTILE_QUALIFICATION` when **any** of the following is true:

1. a mandatory zero-tolerance condition has failed;
2. its optimistic best possible final activation precision is below 0.95;
3. its optimistic best possible final activation recall is below 0.95;
4. its optimistic best possible final activation F1 is below 0.95;
5. its best possible final false-activation rate exceeds 0.05;
6. its best possible final wrong-specialist rate exceeds 0.05;
7. its best possible final overactivation rate exceeds 0.05;
8. its best possible final overall semantic accuracy is below 0.95.

### Optimistic-completion rule

For all unscheduled/incomplete cases, assume the completion most favorable to the candidate while preserving the frozen expected sets and metric denominators:

- all remaining expected entrypoints become true positives;
- no additional false positives, wrong specialists, overactivations or semantic errors occur;
- every remaining semantic outcome is correct;
- no remaining safety violation occurs.

If even that optimistic completion cannot pass a threshold, future live calls cannot restore qualification and MUST NOT be scheduled for that candidate.

Persist a machine-recomputable futility certificate containing observed numerators/denominators, remaining optimistic contribution and the exact failed bound.

Do not report unexecuted-case partial metrics as if they were complete acceptance metrics. Report the terminal candidate state plus its futility certificate.

### Immediate exact consequences

The generic optimistic calculation must reproduce at least these consequences for the frozen 40-case class distribution:

- one finalized false activation across the 11 negative/near-miss cases makes `false_activation_rate <= 0.05` impossible;
- three finalized semantic errors make `semantic_outcome_accuracy >= 0.95` impossible;
- any cross-profile or ambiguous mandatory violation immediately disqualifies the candidate.

Hard-coded shortcuts may be tested, but the authoritative decision must come from the generic frozen-denominator calculation.

## MODIFIED — Stage R early termination

Evaluate B0/B1 under the above scheduling/futility method.

- If both become `FUTILE_QUALIFICATION`, T023 stops `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE` immediately; remaining B0/B1 and all F2/G3 calls are forbidden.
- If one becomes futile, stop scheduling that candidate and continue the surviving single-family candidate through all cases/repetitions still required to establish full qualification or its own futility.
- If both survive, complete both and apply the unchanged B0/B1 reference rule.

The previous 160–240 Stage-R range remains the **maximum full-completion range**, not a minimum expenditure.

## ADDED — Stage C materiality-impossibility stopping

Stage C begins only after a fully established single-family reference exists.

For each challenger F2/G3, apply qualification futility as above. In addition, after each finalized aggregate compute whether the challenger can still satisfy the unchanged D050 material-advantage rule under optimistic remaining completion.

A challenger becomes `FUTILE_MATERIALITY` when any required material condition is mathematically impossible even under optimistic completion:

- final F1 cannot reach `reference + 0.03`;
- best possible final false-activation rate cannot be `<= reference`;
- best possible final wrong-specialist or overactivation rate cannot be `<= reference + 0.01`;
- best possible final median observed context cannot be `<= 0.85 * reference median`.

For the context bound, assign every unfinished activation-relevant case an optimistic context value of zero bytes and compute the best possible final median over the frozen activation-relevant case set. If that optimistic median still exceeds the required ratio, materiality is impossible.

If both challengers become non-material/futile, select the frozen single-family reference without remaining challenger calls. If exactly one remains potentially material, stop calls for the other and continue only the viable challenger. If both remain viable, continue both as required by the unchanged tie-break rule.

## ADDED — cost/tool telemetry

Persist per live invocation when exposed by the installed Codex event stream:

- input tokens;
- cached input tokens;
- reasoning tokens;
- output tokens;
- total tokens;
- tool-call count;
- execution-policy rejected-tool-call count;
- unrelated app/plugin resource count/bytes;
- duration;
- capacity status;
- effective sandbox/configuration identity.

If exact token fields are not exposed, record `token_usage_available=false` and retain all available duration/tool/context proxies. Do not invent token estimates and do not substitute a different model/provider solely for telemetry.

The experimental Codex rollout-budget feature is not required for v8 acceptance because its behavior/reminders could change the model-visible execution path. Prompt caching may be observed through cached-token telemetry but is not an acceptance invariant.

## Acceptance model/effort

V8 keeps the required live cell:

- host: Codex;
- platform: native Windows;
- model: GPT-5.6 Sol;
- reasoning effort: Medium.

No Low/Medium effort comparison may use v8 acceptance prompts. A future independent calibration may revise effort prospectively if needed.

## D052 assets

T047 authorizes Orchestrator creation/revision of:

- `evals/skill_activation_topology/corpus.json` -> schema `4.0.0`, corpus `MG1-T023-CORPUS-v4`;
- `evals/skill_activation_topology/oracle.json` -> schema `8.0.0`, oracle `MG1-T023-TOPOLOGY-ORACLE-v8`, execution epoch `MG1-T023-EXECUTION-v8`;
- preregistration/checkpoint/research Markdown.

Candidate presentation/reference bytes and `topologies.json` are not authorized to change.

## Acceptance criteria

### AC-T047-1 — host preflight before acceptance
No v8 acceptance prompt is issued unless two synthetic canary repetitions prove successful local Skill-body read/use and trace observability under the exact frozen acceptance host profile.

### AC-T047-2 — minimal unrelated surface
The selected host profile excludes unrelated Apps/remote-plugin/multi-agent/web-search/MCP-install surfaces and does not load user/project execpolicy rules into the isolated acceptance run.

### AC-T047-3 — no blocked-read scoring
An explicit required Skill-body read rejection or unrelated tool-surface drift after preflight stops the affected acceptance scheduling and cannot be scored as candidate non-activation.

### AC-T047-4 — fresh holdout
All 40 v8 exact prompts are new and preserve the frozen semantic class/fixture distribution and expectations.

### AC-T047-5 — exact decision-preserving futility
Every skipped candidate observation is justified by a recomputable qualification or materiality impossibility certificate using only frozen thresholds, completed v8 evidence and optimistic remaining completion.

### AC-T047-6 — rigor preserved
Candidate bytes, semantic expectations, qualification thresholds, zero-tolerance gates, paired 2+1 aggregation, context meaning and D050 reference/material-advantage percentages remain unchanged.

### AC-T047-7 — cost evidence
The handoff distinguishes model observations, capacity events, host-surface drift, skipped-by-futility work, and available token/tool/duration telemetry; no unexecuted case is represented as a completed metric row.

## Ownership and execution

T047 is Orchestrator-owned Specify/Design/Plan work. After integration, T023 is relaunched from fresh canonical `develop`.

Executor owns only:

- version-specific CLI/config adapter mechanics implementing the frozen effective host surface;
- synthetic canary plumbing;
- mechanical harness implementation of futility/materiality bounds and scheduling;
- live execution/evidence;
- implementation tests and Code Review & Verify;
- handoff JSON.

Executor MUST NOT change the fresh corpus expectations, candidate presentations, thresholds, selection percentages or semantic oracle meaning.

## Stop conditions

Stop/re-enter rather than launch/continue acceptance if:

- the synthetic preflight cannot prove successful body read/use and observability under either permitted sandbox profile;
- effective host configuration cannot exclude the required unrelated surfaces;
- an acceptance session shows required body-read policy rejection or unrelated app/plugin surface drift after preflight;
- any prior-epoch observation enters v8 score;
- a candidate/presentation/reference byte changes;
- any threshold/selection rule is changed in response to v7 or v8 results;
- futility logic cannot produce an exact optimistic-completion certificate;
- an early-stop implementation would require treating missing cases as observed successes/failures rather than explicitly unexecuted.
