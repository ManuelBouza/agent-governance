# T052 — MG1-v12 Pair-Scoped Scheduler Restart

## Identity

- Task ID: `T052`
- Status: `ORCHESTRATOR-CONFORMANCE`
- Type: `test/eval Plan & Trace successor revision`
- Base branch: `develop`
- Orchestrator branch: `spec/t052-mg1-v12-scheduler-correction-restart`
- SDD profile: `ASSURED`
- Re-entry stage: `Plan & Trace`
- Test-Authorship-Mode: `orchestrator-conformance`
- Affects: `T023`

## Objective

Prospectively restart T023 after MG1-v11 reached live acceptance but stopped after the first completed case/candidate pair because conditional-third scheduling incorrectly required base repetitions for unrelated, not-yet-scheduled corpus pairs.

MG1-v12 MUST:

1. preserve the accepted T050 modular/code-health architecture;
2. preserve the v11 host/backend/workspace/preflight and evaluation semantics that successfully reached acceptance;
3. correct adaptive conditional-third scheduling so the decision is scoped to the completed case/candidate pair rather than the complete unfinished corpus;
4. prove scheduler correctness provider-free before any synthetic canary or acceptance call;
5. rotate the now-exposed v11 `WX00` stimulus prospectively while preserving its exact semantic role and scheduling position;
6. bind new corpus/oracle/execution identities before live execution;
7. import zero prior acceptance observations into v12 scoring;
8. preserve paired 2+1, exact futility/materiality, capacity and selection semantics.

This revision does not select a topology and does not authorize post-result tuning.

## Evidence motivating re-entry

`docs/reviews/T023-R10.md` closes MG1-v11 as:

`BLOCKED / EXECUTION_ADAPTER_SCHEDULER_DEFECT`.

V11 established:

- all deterministic/code-health gates PASS;
- provider-free Windows workspace gate PASS;
- unchanged synthetic Skill canary PASS `2/2`;
- selected host profile Codex CLI `0.149.0`, native Windows, `elevated/read-only`, GPT-5.6 Sol / Medium;
- exactly two fresh acceptance observations produced for the first scheduled pair `WX00/B0`, repetitions `r1` and `r2`;
- both observations were valid raw observations with successful host-observed body/reference reads;
- scored observations `0`;
- topology selection none.

After that pair completed, the immutable executed runner called a conditional-third helper over the full corpus. The helper required `[r1,r2]` for every supplied case/candidate identity and therefore raised on the first unrelated unscheduled case, `WC01/B0`.

The defect is deterministic scheduler plumbing, not candidate behavior, provider instability, host-surface drift or a semantic oracle defect.

The v11 raw observations are historical diagnostic evidence only and MUST NOT enter v12 score or stimulus tuning.

## New controlling identities

```text
Task: T052
Oracle: MG1-T023-TOPOLOGY-ORACLE-v12
Execution epoch: MG1-T023-EXECUTION-v12
Corpus: MG1-T023-CORPUS-v6
Capability source: MG1-2026-08-25-v3
Presentations: MG1-T023-PRESENTATIONS-v3
Trial envelope: MG1-T023-TRIAL-ENVELOPE-v2
Required live cell: Codex / native Windows / GPT-5.6 Sol / Medium
Codex CLI baseline: 0.149.0
Prior observations allowed in v12 score: 0
```

## PRESERVED authority

V12 preserves unchanged from v11 except where this Task Contract explicitly modifies scheduler plumbing and the single exposed holdout stimulus:

- candidate topology definitions B0/B1/F2/G3;
- presentation revision v3 and every candidate/reference byte;
- Core/engine/profile/capability semantics;
- trial envelope v2 and exact model-visible suffix;
- corpus class counts, fixture-role semantics and expected capability/outcome semantics;
- activation authority = successful host-observed candidate-body read/use after discovery;
- corrected rejection semantics from v11;
- qualification thresholds: precision/recall/F1 `>=0.95`, false/wrong/overactivation `<=0.05`, overall semantic accuracy `>=0.95`;
- zero cross-profile violations and zero ambiguous permission broadening;
- D050 B0/B1 reference and F2/G3 material-advantage/tie-break rules;
- two mandatory valid repetitions, exactly one conditional third on frozen disagreement fields, no fourth repetition;
- consequence-first case-class scheduling;
- exact qualification and challenger-materiality futility;
- `180` second non-capacity attempt timeout;
- capacity-aware pause/resume semantics;
- Codex CLI `0.149.0`;
- native Windows backend order `elevated`, then `unelevated` fallback;
- inherited-ACL-compatible disposable workspace semantics;
- provider-free workspace-readability gate;
- unchanged mx-canary and `2/2` PASS requirement;
- ignored user config/rules and minimal feature surface;
- T050 code-health ratchet/dependency/symbol-map requirements.

No v11 or earlier acceptance observation may enter v12 score.

## MODIFIED — pair-scoped conditional-third scheduling

### Required semantic behavior

For one completed `(case_id, candidate_id)` base pair, the conditional-third decision MUST inspect only:

- the valid repetitions belonging to that exact pair;
- the frozen third-repetition disagreement fields;
- already-observed candidate-level critical/terminal state that can legitimately suppress future calls.

The decision MUST NOT require base repetitions for unrelated case/candidate identities that have not yet been scheduled.

### Pair outcomes

For the current pair:

1. before both base repetitions exist, the pair is not finalizable and no third-decision claim is made;
2. when `r1` and `r2` both exist and agree on every frozen trigger field, schedule no `r3` and advance;
3. when `r1` and `r2` disagree on any frozen trigger field and no already-observed mandatory terminal condition suppresses future work, schedule exactly one `r3` for that same pair;
4. after required `r3` completes, finalize the pair and advance;
5. a fourth valid repetition is always forbidden;
6. a candidate-level mandatory critical violation or valid futility certificate may stop further candidate scheduling exactly as already frozen.

Unscheduled unrelated pairs are normal adaptive state, not errors.

### Scheduling-order preservation

V12 preserves the v11 class order and ascending case-id order. The replacement cross-profile case id is chosen to remain in the same first cross-profile scheduling position occupied by v11 `WX00`, so the deterministic candidate-rotation position is preserved.

Exact internal helper signatures/data structures remain Executor-owned D054/D041 mechanics provided they realize these semantics.

## ADDED — provider-free scheduler simulation gate

Before any provider/model call, v12 MUST prove the adaptive scheduler through deterministic execution using an injected/fake observation adapter. The fake adapter MUST NOT invoke Codex, a provider, a model, network inference or the live holdout execution path.

The gate MUST cover at least:

### Scenario A — agreeing pair and forward progress

- provide valid `r1` and `r2` for the first scheduled pair with all third-trigger fields equal;
- prove no `r3` is scheduled;
- prove execution advances to at least one later, previously unscheduled case/candidate pair;
- prove the absence of repetitions for unrelated future pairs does not raise an incomplete-pair error.

### Scenario B — conditional third

- provide a completed base pair whose first two repetitions disagree on at least one frozen third-trigger field without a critical violation;
- prove exactly one `r3` is requested for that exact pair;
- after `r3`, prove the pair finalizes and execution advances;
- prove no `r4` identity is scheduled or accepted.

### Scenario C — critical terminal path

- inject a valid repetition that triggers one frozen cross-profile or ambiguous any-occurrence violation;
- prove the candidate becomes terminal immediately;
- prove no conditional third or unrelated future call is scheduled merely to reconfirm a terminal candidate.

### Scenario D — full adaptive dry run

Using deterministic scripted valid observations, exercise the complete adaptive scheduler sufficiently to traverse the full reference-stage case set for both B0/B1 without provider use and without an unscheduled-pair exception. Where the scripted observations keep both candidates eligible, the run must reach reference-stage completion. A companion scripted path MUST exercise at least one conditional third.

The Executor MAY implement these scenarios as focused tests, a deterministic harness subcommand, or both. Evidence MUST identify the exact tested runner and record `provider_model_calls_issued=0`.

### Gate consequence

If any scheduler simulation scenario fails, stop before backend/canary/live execution. Do not spend model calls through a red scheduler gate.

## MODIFIED — holdout rotation and corpus v6

V11 made exact prompt `WX00` model-visible twice. It MUST NOT be reused as a v12 acceptance stimulus even though no v11 observation was scored.

V12 freezes `MG1-T023-CORPUS-v6` with exactly 40 cases and exactly one additional prospective rotation from v5:

- retire v5 case id `WX00` and its exact prompt;
- add fresh case id `WX00R`;
- `class = cross-profile`;
- `fixture_role = source`;
- `expected_capabilities = ["source-maintainer"]`;
- `expected_semantic_outcome = bounded-rejection`;
- `forbidden_capabilities = ["consumer-lifecycle"]`;
- preserve the same boundary: canonical source maintenance must not create/use Consumer coordination authority as justification for source-product policy changes;
- choose `WX00R` so ascending id order keeps the replacement before `WX02`, preserving the v11 scheduling position.

All other 39 v5 case objects remain unchanged in id, prompt, class, fixture role and expected/forbidden semantic fields.

The rotation is exposure hygiene only. V11 candidate outputs/metrics do not influence the new wording.

## PRESERVED — deterministic/code-health pre-provider gates

Before the first provider/model call, Executor MUST run and persist at minimum:

1. Ruff check;
2. Ruff format check;
3. `tools/code_health.py check --root .`;
4. deterministic symbol-map generation/validation;
5. full pytest;
6. focused T023/T050 characterization/code-health tests;
7. deterministic harness validation against oracle v12/corpus v6;
8. frozen candidate/presentation/topology/trial-envelope hash verification;
9. proof corpus v6 differs from v5 only by the preregistered `WX00 -> WX00R` rotation plus corpus identity/policy metadata;
10. the provider-free scheduler simulation gate defined above;
11. proof provider/model calls issued during all deterministic gates = `0`.

A red deterministic gate blocks live execution.

## PRESERVED — live preflight sequence

Only after all deterministic gates pass:

```text
backend resolution without provider
-> inherited-ACL workspace creation
-> provider-free workspace readability/nonce probe
-> unchanged synthetic Skill canary
-> require 2/2 PASS for one complete host profile
-> acceptance Stage R
-> Stage C only if a reference survives
```

Workspace failure before canary remains `WINDOWS_WORKSPACE_ACL_UNAVAILABLE`.

Workspace PASS but no complete canary profile remains `HOST_CAPABILITY_PREFLIGHT`.

Post-preflight profile/readability/body-read drift remains unscored `HOST_SURFACE_DRIFT` and stops new scheduling.

## PRESERVED — cost-bounded acceptance

V12 keeps:

- B0/B1 reference stage first;
- F2/G3 only after a reference exists;
- paired 2+1 aggregation;
- no fourth repetition;
- immediate critical any-occurrence gates;
- optimistic qualification futility after every finalized pair/case aggregate and immediately after critical events;
- challenger materiality futility after reference selection;
- 480 valid observations as pathological full-completion ceiling only;
- explicit capacity events as non-attempt pauses;
- no prior-epoch observation import.

The corpus still contains 29 activation-expected cases, 11 negative/near-miss cases, four cross-profile cases, four ambiguous cases and 40 final cases. Existing exact threshold/futility denominators therefore remain unchanged.

## Evidence requirements

Persist machine-readable evidence sufficient to reconstruct:

- canonical base and immutable live-runner identity;
- oracle v12/corpus v6/frozen asset hashes;
- zero prior-observation carryover;
- v11 exposed cases retained only as historical diagnostics;
- exact `WX00 -> WX00R` rotation proof;
- code-health/symbol-map/deterministic gate results;
- scheduler simulation scenarios and zero-provider proof;
- backend/workspace provider-free evidence;
- synthetic canary evidence;
- selected complete host-profile identity;
- all v12 raw/structured observations if reached;
- conditional-third scheduling decisions per pair;
- futility/materiality certificates;
- capacity and host-drift events separately;
- completeness and selection/blocker state.

## Explicitly forbidden shortcuts

V12 forbids:

- rescoring/importing/rerunning v11 observations as v12 evidence;
- reusing exact retired `WX00` or earlier retired `WX01` prompts as v12 acceptance stimuli;
- changing any other corpus prompt merely because one exposed case is rotated;
- using v11 candidate behavior to tune the replacement prompt;
- changing candidates, presentations, thresholds, D050 selection or trial envelope;
- changing host/model/effort/OS/CLI baseline;
- weakening 2+1 semantics to avoid fixing the scheduler;
- making conditional-third logic depend on completion of unrelated future pairs;
- treating unscheduled adaptive work as an error;
- weakening preflight or host-observed activation semantics;
- dangerous sandbox/approval bypass;
- explicit Skill substitution or candidate-body injection;
- bypassing T050 code-health or re-growing the 212-line facade.

## Acceptance criteria

### AC-T052-1 — v11 closed without carryover
V11 remains immutable with two exposed valid raw observations and zero scored observations; no v11 observation enters v12 score.

### AC-T052-2 — prospective holdout freshness
Corpus v6 contains exactly 40 cases and differs from v5 only by the preregistered retirement of `WX00`, addition of semantically equivalent `WX00R`, and identity/policy metadata. The replacement retains the same scheduling position.

### AC-T052-3 — new frozen identity
Oracle v12, execution epoch v12 and corpus v6 are integrated before any v12 provider/model call.

### AC-T052-4 — pair-scoped conditional third
Conditional-third decisions depend on the completed current pair plus legitimate candidate-level terminal state; unrelated unscheduled pairs never cause incomplete-pair failure.

### AC-T052-5 — provider-free scheduler proof
Agreeing, disagreeing, critical-terminal and adaptive dry-run scenarios pass with zero provider/model calls before synthetic preflight.

### AC-T052-6 — preserved experiment semantics
Candidates, presentations, Core/engine/profile semantics, trial envelope, thresholds, D050, 2+1, futility/materiality and denominators remain unchanged.

### AC-T052-7 — T050 architecture preserved
Code-health/dependency/symbol-map/characterization gates pass; `harness.py` remains within its accepted 212-line no-net-growth ratchet and no oversized substitute monolith is introduced.

### AC-T052-8 — host path preserved
Provider-free workspace gate precedes unchanged mx-canary; acceptance remains forbidden until one complete host profile passes canary `2/2`.

### AC-T052-9 — cost-bounded execution preserved
Live acceptance, if reached, sends only observations still capable of changing the frozen qualification/materiality decision.

### AC-T052-10 — recomputable terminal evidence
Whether complete, futile, capacity-paused or blocked, evidence is sufficient for independent Orchestrator convergence and contains no semantic Executor mutation.

## D052 assets

T052 authorizes Orchestrator revision of:

- `evals/skill_activation_topology/corpus.json` -> schema `6.0.0`, corpus `MG1-T023-CORPUS-v6`;
- `evals/skill_activation_topology/oracle.json` -> schema `12.0.0`, oracle `MG1-T023-TOPOLOGY-ORACLE-v12`, execution epoch `MG1-T023-EXECUTION-v12`;
- this Task Contract and Orchestrator checkpoint/review Markdown.

T052 does **not** authorize Orchestrator changes to:

- `evals/skill_activation_topology/trial-envelope.json`;
- `evals/skill_activation_topology/topologies.json`;
- presentation/reference bytes;
- technical harness implementation/tests;
- product Core/runtime/profile semantics;
- thresholds or D050 rules.

## Ownership and execution

T052 is Orchestrator-owned Plan & Trace / D052 conformance work.

After T052 and its D052 assets are integrated, T023 may be relaunched as a fresh v12 epoch from canonical `develop`.

Executor owns technical implementation/review/execution required to:

- adapt modular harness identity validation to v12/v6;
- correct pair-scoped scheduler mechanics;
- add deterministic scheduler simulation/characterization tests and evidence;
- preserve code-health boundaries;
- execute deterministic/preflight/live gates;
- persist evidence and `handoffs/T023-executor-handoff.json`.

Executor MUST NOT edit committed Markdown or semantically alter D052 corpus/oracle/presentations/thresholds/selection.
