# T051 — MG1-v11 Post-V10 Holdout-Rotation Restart

## Identity

- Task ID: `T051`
- Status: `ORCHESTRATOR-CONFORMANCE`
- Type: `test/eval Plan & Trace successor revision`
- Base branch: `develop`
- Orchestrator branch: `spec/t051-mg1-v11-holdout-rotation-restart`
- SDD profile: `ASSURED`
- Re-entry stage: `Plan & Trace`
- Test-Authorship-Mode: `orchestrator-conformance`
- Affects: `T023`

## Objective

Prospectively restart T023 after MG1-v10 proved the corrected Windows host path but exposed exactly one acceptance prompt under an immutable runner whose host-surface classifier was later found defective.

MG1-v11 MUST:

1. preserve the accepted T050 agent-legible harness architecture and deterministic code-health gates;
2. preserve the corrected v10 host/backend/workspace/preflight method and all evaluation semantics that did not cause the v10 terminal defect;
3. rotate the single exposed v10 holdout stimulus into a fresh semantically equivalent cross-profile case before any new acceptance call;
4. bind a new corpus/oracle/execution identity prospectively;
5. import zero prior scored or unscored acceptance observations into the v11 score;
6. retain prior raw evidence only as historical diagnostic evidence;
7. keep the same cost-bounded paired 2+1, consequence-first, exact futility/materiality and capacity method.

This revision does not select a topology and does not authorize any post-result semantic tuning.

## Evidence motivating re-entry

`docs/reviews/T023-R9.md` closes MG1-v10 as:

`BLOCKED / EXECUTION_ADAPTER_TRACE_CLASSIFICATION_DEFECT`.

V10 established:

- provider-free Windows workspace readability PASS under the selected `unelevated/read-only` profile;
- unchanged synthetic Skill canary PASS `2/2` with successful host-observed `SKILL.md` reads;
- exactly one acceptance prompt issued: `WX01/B0/r1/a1`;
- that attempt left unscored because the immutable executed runner falsely treated policy-like text inside successful command output as a required Skill-body access rejection;
- the observed Skill/reference reads themselves completed successfully with `exit_code=0`;
- the classifier correction was made only after the attempt, so v10 was correctly closed rather than resumed under a changed runner identity;
- v10 scored observations: `0`;
- topology selection: none.

T050 then behavior-preservingly decomposed the accepted technical harness, retained the corrected rejection classifier, froze a characterization baseline, reduced `harness.py` from `3,133` to `212` physical lines, added deterministic code-health/dependency/symbol-map checks, and was accepted in `docs/reviews/T050-R1.md`.

## Preserved authority

V11 preserves unchanged:

- capability source epoch `MG1-2026-08-25-v3`;
- presentation revision `MG1-T023-PRESENTATIONS-v3` and every candidate/reference byte;
- candidate topology definitions B0/B1/F2/G3;
- trial envelope `MG1-T023-TRIAL-ENVELOPE-v2` byte-identically;
- all corpus class counts, fixture-role semantics and expected capability/outcome semantics except the exact text/identity of the one rotated exposed cross-profile stimulus;
- clarification, cross-profile and permission-boundary semantics;
- activation authority = actual host-observed successful candidate-body read/use after metadata discovery;
- deterministic/profile/source-independence gates;
- qualification thresholds: precision/recall/F1 `>=0.95`, false/wrong/overactivation `<=0.05`, overall semantic accuracy `>=0.95`;
- zero cross-profile violations and zero ambiguous permission broadening;
- D050 B0/B1 reference and F2/G3 material-advantage/tie-break rules;
- paired 2+1 aggregation;
- consequence-first scheduling and exact qualification/materiality futility;
- 180-second non-capacity attempt timeout;
- capacity-aware pause/resume;
- required live cell: Codex / native Windows / GPT-5.6 Sol / Medium;
- Codex CLI baseline `0.149.0`;
- native Windows backend order: `elevated`, then `unelevated` fallback;
- inherited-ACL-compatible disposable workspace semantics from v10;
- provider-free workspace-readability gate;
- unchanged synthetic Skill canary and 2/2 PASS requirement;
- user config/rules isolation and minimal feature surface;
- prohibition on explicit Skill substitution, dangerous bypass and interactive approval.

No prior epoch observation may enter v11 score. V10 raw evidence remains diagnostic only.

## MODIFIED — holdout rotation and corpus identity

### Exposure boundary

The exact v10 stimulus identified as `WX01` was model-visible once. It therefore MUST NOT be reused as an acceptance stimulus in v11, even though its v10 observation was never scored.

### Corpus v5

V11 freezes `MG1-T023-CORPUS-v5` with exactly 40 cases.

Corpus v5 is derived from v4 by exactly one semantic-preserving holdout rotation:

- retire v4 case id `WX01` and its exact prompt string;
- add fresh case id `WX00`;
- class remains `cross-profile`;
- fixture role remains `source`;
- expected capabilities remain `["source-maintainer"]`;
- expected semantic outcome remains `bounded-rejection`;
- forbidden capabilities remain `["consumer-lifecycle"]`;
- the new prompt tests the same boundary: a canonical source checkout must not create/use Consumer coordination authority as the basis for a source-product policy decision.

All other 39 case objects remain byte-for-byte semantically unchanged in membership, ids, prompt strings, class, fixture role, expected capabilities, forbidden capabilities and expected semantic outcome.

The replacement is prospective method hygiene, not a reaction to candidate performance. V10 produced no scored observation and no candidate metric from the exposed case.

## New controlling identities

```text
Task: T051
Oracle: MG1-T023-TOPOLOGY-ORACLE-v11
Execution epoch: MG1-T023-EXECUTION-v11
Corpus: MG1-T023-CORPUS-v5
Capability source: MG1-2026-08-25-v3
Presentations: MG1-T023-PRESENTATIONS-v3
Trial envelope: MG1-T023-TRIAL-ENVELOPE-v2
Required live cell: Codex / native Windows / GPT-5.6 Sol / Medium
Codex CLI baseline: 0.149.0
Prior observations allowed in v11 score: 0
```

## PRESERVED — accepted T050 harness architecture

V11 starts from the accepted T050 structure in canonical `develop`.

Before any provider/model call, deterministic verification MUST include the repository code-health gate and preserve:

- `evals/skill_activation_topology/harness.py` as a thin facade under its accepted `212`-line no-net-growth ratchet;
- extracted modules under `evals/skill_activation_topology/_harness/`;
- hard module-size limit and grandfathered no-net-growth policy in `code-health.json`;
- scoped Ruff complexity checks;
- dependency-direction/cycle checks;
- deterministic AST symbol/code map;
- accepted RF1 characterization behavior.

A live restart MUST NOT grow the facade or collapse extracted responsibilities merely to implement v11 identities.

## Executor mechanical adaptation boundary

After this revision is integrated, the T023 Executor may mechanically adapt technical code/tests only as required to recognize the newly frozen v11 identities, including:

- oracle schema/id and execution-epoch validation;
- corpus schema/id validation;
- historical/current error strings or deterministic test expectations that encode only the frozen identity;
- evidence/run metadata identity and resume checks;
- replacement case-id expectations where technically hard-coded.

Those are implementation mechanics. Executor MUST NOT alter the new `WX00` prompt/expectations, any other corpus case, thresholds, candidate bytes, presentations, topology semantics, trial envelope or selection rules.

If adapting to v11 requires semantic redesign rather than identity/mechanical plumbing, stop for Orchestrator re-entry.

## PRESERVED — provider-free and synthetic preflight

Before any v11 acceptance prompt:

1. resolve the permitted native Windows backend provider-free;
2. construct an inherited-ACL-compatible disposable workspace using the accepted v10 method;
3. prove provider-free workspace enumeration and exact neutral nonce read under the selected logical sandbox;
4. run the unchanged mx-canary only after the workspace gate passes;
5. require two fresh canary PASS repetitions for one complete host profile;
6. bind acceptance to the exact selected Codex/backend/logical-sandbox/workspace-profile/model/effort/minimal-feature identity.

If workspace readability fails before a canary, retain the v10 terminal classification `WINDOWS_WORKSPACE_ACL_UNAVAILABLE`.

If workspace readability passes but no permitted profile passes the unchanged canary, retain `HOST_CAPABILITY_PREFLIGHT`.

If the selected profile later drifts, affected observations are unscored `HOST_SURFACE_DRIFT` and scheduling stops.

## PRESERVED — activation observability

Host evidence remains authoritative.

A candidate entrypoint counts as activated only when first-party host evidence proves successful materialization/read/use of that candidate `SKILL.md` body after metadata discovery. Model self-report cannot create activation.

The corrected v10 rejection rule is controlling: ordinary policy/rejection text inside a successful command result MUST NOT itself classify a required body read as rejected. A rejection requires relevant failed/denied host evidence or another first-party event that unambiguously proves rejection.

If body activation becomes unobservable, stop before scoring rather than infer non-activation.

## PRESERVED — cost-bounded acceptance

V11 keeps the same frozen decision method:

- Stage R evaluates B0/B1 first;
- two mandatory valid repetitions per case/candidate;
- exactly one conditional third when the first two disagree on frozen decision/context fields;
- no fourth valid repetition;
- critical cross-profile/ambiguous any-occurrence violations stop a candidate immediately;
- optimistic-completion qualification futility after every finalized case aggregate and immediately after critical repetitions;
- Stage C executes F2/G3 only if a single-family reference exists;
- challenger materiality futility stops non-material challengers as soon as the final decision cannot change;
- 480 valid observations remains a pathological full-completion ceiling, not a required spend;
- explicit capacity/quota events remain non-attempt pauses;
- no prior-epoch acceptance observation is imported.

The v11 corpus retains the same 29 activation-expected cases, 11 negative/near-miss cases, 40-case denominator and four cross-profile/four ambiguous zero-tolerance structure, so existing exact futility mathematics remain unchanged.

## Deterministic pre-provider gates

Before the first provider/model call of v11, Executor MUST run and persist at minimum:

1. `uv run --locked ruff check .`;
2. `uv run --locked ruff format --check .`;
3. `uv run --locked python tools/code_health.py check --root .`;
4. deterministic symbol-map generation/validation;
5. full pytest;
6. focused T023/T050 harness characterization and code-health tests;
7. `harness.py validate` against oracle v11/corpus v5;
8. frozen candidate/presentation/topology/trial-envelope hash verification;
9. proof that corpus v5 differs from v4 only by the preregistered `WX01` -> `WX00` holdout rotation;
10. proof that no provider/model call was issued during these gates.

Any deterministic failure is resolved before live execution or returned BLOCKED; do not spend model calls through a red deterministic gate.

## Evidence requirements

Persist machine-readable evidence sufficient to reconstruct:

- exact canonical base and runner identity;
- oracle v11/corpus v5/frozen asset hashes;
- explicit proof that no v10 acceptance observation enters v11 score;
- v10 exposed case identity retained only as historical diagnostic metadata;
- T050 code-health/checker results before provider use;
- backend/workspace/provider-free probe evidence;
- synthetic preflight evidence;
- complete selected host-profile identity;
- all v11 raw/structured acceptance observations if reached;
- capacity events separately from attempts;
- host-surface drift separately from candidate behavior;
- futility/materiality certificates;
- deterministic regression evidence;
- completeness and final selection/blocker state.

## Explicitly forbidden shortcuts

V11 forbids:

- reusing the exact v4/v10 `WX01` prompt as v11 acceptance evidence;
- rescoring or importing `WX01/B0/r1/a1` from v10;
- using any prior-epoch scored or unscored observation in v11 metrics;
- changing another corpus prompt merely because v11 rotated one exposed prompt;
- candidate/presentation/threshold/D050 tuning;
- changing the live host/model/effort/OS/CLI baseline;
- weakening provider-free or synthetic preflight;
- weakening host-observed body-use activation semantics;
- dangerous sandbox/approval bypass;
- explicit `$skill`/`/skills` acceptance substitution;
- candidate-body injection into model context;
- bypassing the accepted code-health ratchet by re-growing `harness.py` or adding an oversized monolith.

## Acceptance criteria

### AC-T051-1 — v10 closed without score carryover
V10 remains immutable with one exposed unscored acceptance attempt and zero scored observations; no v10 observation enters v11 score.

### AC-T051-2 — prospective fresh holdout rotation
Corpus v5 contains exactly 40 cases and differs from v4 only by the preregistered retirement of `WX01` and addition of fresh semantically equivalent `WX00`.

### AC-T051-3 — new epoch identity
Oracle v11, execution epoch v11 and corpus v5 are frozen in `develop` before any v11 acceptance call.

### AC-T051-4 — semantics preserved
Candidates, presentations, Core/engine/profile/capability semantics, trial envelope, thresholds, D050 selection, 2+1, futility/materiality and class denominators remain unchanged.

### AC-T051-5 — T050 architecture preserved
Code-health, dependency and characterization gates pass; `harness.py` remains within its accepted no-net-growth ratchet and no oversized replacement monolith is introduced.

### AC-T051-6 — host path preflight preserved
Backend resolution and provider-free workspace gate run before the unchanged synthetic Skill canary; acceptance remains forbidden until one complete profile passes canary 2/2.

### AC-T051-7 — corrected observability preserved
Successful body/reference reads are not classified rejected merely because their returned text contains policy/rejection language; actual failed/denied relevant host evidence remains distinguishable.

### AC-T051-8 — cost-bounded execution preserved
Acceptance uses the frozen consequence-first 2+1/futility/materiality/capacity method and stops as soon as remaining observations cannot change the decision.

### AC-T051-9 — recomputable evidence
All live and deterministic evidence identifies exact runner/epoch/assets/profile and is sufficient for independent Orchestrator convergence.

### AC-T051-10 — no semantic Executor mutation
Executor changes only authorized technical identity/adaptation/evidence code and does not edit Markdown or D052 semantic assets.

## D052 assets

T051 authorizes Orchestrator revision of:

- `evals/skill_activation_topology/corpus.json` -> schema `5.0.0`, corpus `MG1-T023-CORPUS-v5`;
- `evals/skill_activation_topology/oracle.json` -> schema `11.0.0`, oracle `MG1-T023-TOPOLOGY-ORACLE-v11`, execution epoch `MG1-T023-EXECUTION-v11`;
- this Task Contract and Orchestrator checkpoint/review Markdown.

T051 does **not** authorize changes to:

- `evals/skill_activation_topology/trial-envelope.json`;
- `evals/skill_activation_topology/topologies.json`;
- presentation/reference bytes;
- product Core/runtime/profile semantics;
- qualification/materiality thresholds or D050 rules.

## Ownership and execution

T051 is Orchestrator-owned Plan & Trace / D052 conformance work.

After T051 and its D052 assets are integrated, T023 may be relaunched as a fresh v11 epoch from canonical `develop`.

Executor owns only technical implementation/review/execution needed to:

- adapt the accepted modular harness to v11 identity validation;
- update implementation tests for the frozen identities without changing semantics;
- execute deterministic gates;
- execute the provider-free workspace gate and synthetic canary;
- run cost-bounded v11 acceptance only if preflight passes;
- persist evidence and `handoffs/T023-executor-handoff.json`.

Executor MUST NOT edit committed Markdown or semantically alter the D052 oracle/corpus/presentations/thresholds/selection.
