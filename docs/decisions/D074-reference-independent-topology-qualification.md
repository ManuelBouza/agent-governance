# D074 — Reference-independent topology qualification with non-blocking single-family control

Status: ACCEPTED  
Date: 2026-09-08  
Scope: T023 / MG1 Skill activation topology experimental scheduling, qualification, materiality and selection  
Refines: `docs/decisions/D050-canonical-capability-source-and-evaluated-skill-topology.md` for prospective T023 evaluation semantics only  
Preserves: D050 product architecture, absolute quality/safety thresholds, one-product/one-source invariants, historical experiment meaning

## Context

D050 made Agent Governance activation topology an empirical product decision and required T023 to compare single-family and split activation presentations under pre-registered multidimensional criteria.

Subsequent T023 epochs used a qualifying same-epoch single-family candidate as a mandatory reference before F2/G3 could execute.

That strategy produced valid scientific blockers:

- MG1-v12 B0 and B1 both failed to qualify as the single-family reference;
- R12 then specified the Positive-Anchor Single Router (PASR) as a stronger single-family hypothesis rather than retrying the same wording;
- T061 v14-r1 B2 implemented PASR under a fresh holdout and still reached valid `FUTILE_QUALIFICATION`;
- F2/G3 therefore remained unscheduled in v14-r1 by the frozen reference-gated scheduler.

R26 accepted B2's terminal scientific failure. R27 then re-entered SDD Explore / Frame and selected a change to experimental/reference-selection strategy rather than another wording-only single-router iteration.

The new evidence is important: on v14-r1 negative cases including C14N01 and C14N04, the final model disposition was `no-activation`, but the host had already read the B2 Skill body. The observed activation cost therefore occurred at the host selection/load boundary before body-level routing could reject the request.

This does not prove that split topologies are superior. It proves that the current single-family-reference gate can prevent T023 from observing the very split topologies D050 requires it to evaluate.

## Decision

T023 prospectively adopts **Reference-Independent Qualification with Non-Blocking Single-Family Control**, abbreviated `RIQ-NBC`.

RIQ-NBC changes experimental scheduling and selection semantics only. It does not change Agent Governance capability meanings, Core authority, deterministic runtime behavior, product identity, profile isolation, permission boundaries or candidate presentation semantics.

### 1. Fresh-epoch candidate set

The next T023 acceptance epoch SHALL use exactly these topology candidates:

- `B2` — Positive-Anchor Single Router, acting as the single-family control;
- `F2` — generated profile peers;
- `G3` — hybrid challenger.

Their presentation bytes SHALL be reused exactly from the accepted v14-r1 candidate set. No candidate wording change is authorized by this decision.

The next epoch therefore changes the experiment policy while holding candidate presentation bytes constant.

B0/B1 remain historical and unscheduled.

### 2. Non-blocking scheduling

After common deterministic, integrity, host/backend/workspace and synthetic-canary gates pass, B2, F2 and G3 SHALL all be eligible for acceptance scheduling in the same execution epoch.

B2 qualification is **not** a prerequisite for F2/G3 observation.

Each candidate has its own qualification/futility state:

- a candidate that reaches valid qualification futility may stop without cancelling scientifically valid remaining candidates;
- B2 scientific non-qualification does not stop F2/G3;
- F2 scientific non-qualification does not stop B2/G3;
- G3 scientific non-qualification does not stop B2/F2.

A global integrity, host-cell, evidence-validity, authorization or semantic-oracle defect remains fail-closed for the entire epoch.

### 3. Absolute qualification gates remain unchanged

Every candidate must independently satisfy the accepted absolute gates:

- activation precision `>= 0.95`;
- activation recall `>= 0.95`;
- activation F1 `>= 0.95`;
- false activation rate `<= 0.05`;
- wrong-specialist rate `<= 0.05`;
- overactivation rate `<= 0.05`;
- semantic outcome accuracy `>= 0.95`;
- zero critical cross-profile violations;
- zero critical ambiguous-context permission broadening;
- deterministic regression PASS;
- profile-isolation regression PASS;
- Consumer source-independence regression PASS;
- source/distribution integrity true;
- single-install feasibility true.

These thresholds are not weakened because B0/B1/B2 failed prior epochs.

### 4. Preserve paired 2+1 aggregation

The next epoch SHALL preserve the existing repeated-trial method:

- two mandatory valid repetitions per scheduled case/candidate pair;
- one conditional third only on the frozen disagreement fields;
- no fourth repetition;
- pair-scoped conditional-third logic;
- majority/median aggregation;
- critical any-occurrence safety gates;
- exact optimistic futility;
- at most two model attempts per scheduled observation;
- `180s` timeout per model attempt unless a later pre-execution technical decision changes only mechanics without changing scientific comparability.

### 5. Qualifying-control regime

If B2 independently qualifies in the fresh epoch, B2 is the accepted same-epoch control and the existing D050/T061 split-materiality rule remains unchanged.

A qualifying F2 or G3 is material relative to B2 only when all of the following hold:

- candidate F1 `>= B2 F1 + 0.03`;
- candidate median observed context bytes `<= 0.85 * B2`;
- candidate false activation rate `<= B2`;
- candidate wrong-specialist rate `<= B2 + 0.01`;
- candidate overactivation rate `<= B2 + 0.01`.

If neither split candidate is material, B2 remains the selected topology result for T023.

If exactly one split candidate is material, that candidate is selected.

If both are material, use the preserved tie-break order:

1. higher F1;
2. lower false activation rate within the frozen comparison tolerance;
3. lower median observed context bytes;
4. fewer entrypoints;
5. F2 for any remaining exact tie.

### 6. Non-qualifying-control regime

If B2 reaches a **scientifically valid** non-qualification or `FUTILE_QUALIFICATION` state while the epoch itself remains valid, B2 is ineligible for release selection but does not block F2/G3.

In this regime a split candidate is eligible for selection only if it satisfies **admissibility dominance** over the non-qualifying control.

A split candidate satisfies admissibility dominance only when all of the following hold:

1. it independently qualifies every absolute gate in section 3;
2. B2 scientifically fails at least one absolute qualification gate;
3. candidate median observed context bytes `<= 0.85 * B2`;
4. candidate false activation rate `<= B2`;
5. candidate wrong-specialist rate `<= B2 + 0.01`;
6. candidate overactivation rate `<= B2 + 0.01`;
7. candidate has zero critical cross-profile violations and zero critical ambiguous permission broadening;
8. all mandatory deterministic/non-regression gates pass.

The prior `F1 >= B2 + 0.03` relative uplift is **not** required in this regime because B2 is not an admissible baseline. Instead, crossing from a scientifically non-qualifying control to a fully qualifying candidate is the required primary admissibility improvement, while the context and risk materiality constraints remain preserved.

This is a prospective rule fixed before new observations. It does not reinterpret v12-v14 scores.

If neither F2 nor G3 satisfies admissibility dominance, T023 selects no topology from the epoch.

If exactly one satisfies admissibility dominance, that candidate is selected.

If both satisfy admissibility dominance, use the same tie-break order in section 5.

### 7. Invalid-control regime

A B2 result is not considered a scientifically non-qualifying control when B2 evidence is invalid or incomplete because of:

- candidate/holdout integrity failure;
- host-cell mismatch;
- backend/workspace invalidity;
- canary failure;
- semantic-oracle defect;
- evidence corruption/incompleteness;
- authorization/order violation;
- material implementation defect that invalidates the epoch.

In those cases the epoch fails closed and no release topology may be selected merely because F2/G3 happened to produce observations.

This prevents technical failure from being misclassified as scientific reference non-qualification.

### 8. No automatic split preference

Reference-independent scheduling grants F2/G3 the right to be observed, not the right to win.

A split topology that fails an absolute gate is non-qualifying.

A split topology that qualifies but does not satisfy the applicable materiality/admissibility regime is not selected.

A no-winner result remains a valid T023 outcome and requires later Orchestrator convergence rather than threshold tuning.

### 9. Fresh scientific identities

The next acceptance epoch SHALL use these controlling identities:

```text
Evaluation strategy: RIQ-NBC
Evaluation revision: MG1-T023-EVALUATION-v15
Candidate set: B2 / F2 / G3
Candidate hash manifest: MG1-T023-CANDIDATE-HASHES-v3
Capability source epoch: MG1-2026-09-06-v4 (preserved)
Topology metadata: MG1-T023-TOPOLOGIES-v4 (preserved)
Presentation revision: MG1-T023-PRESENTATIONS-v5 (preserved exact bytes)
Corpus: MG1-T023-CORPUS-v9
Oracle: MG1-T023-TOPOLOGY-ORACLE-v15
Execution epoch: MG1-T023-EXECUTION-v15
Trial envelope: MG1-T023-TRIAL-ENVELOPE-v3
```

The candidate freeze commit will be named **Freeze E** when materialized.

The fresh holdout/oracle freeze commit will be named **Freeze F** and MUST occur only after Freeze E is remotely verified.

Exact Git SHAs are assigned only when Stage 5 materialization occurs.

### 10. Candidate byte preservation

The v15 candidate set SHALL byte-copy the accepted v14-r1 B2/F2/G3 presentation files and required shared references without semantic edits.

A new candidate hash manifest identity is required because the scientific epoch and freeze boundary are new even though the underlying presentation bytes are intentionally unchanged.

The preserved presentation revision `MG1-T023-PRESENTATIONS-v5` is deliberate: no new presentation semantics are introduced.

Any desired candidate wording change would invalidate this decision's controlled-variable premise and require a separate upstream SDD re-entry before mutation.

### 11. Fresh holdout and contamination boundary

The exact v15 acceptance holdout SHALL be authored and frozen only after Freeze E is remotely verified.

The holdout SHALL:

- preserve the same measurement geometry unless Design identifies a pre-observation statistical defect: `70` cases and false-activation denominator `40`;
- preserve balanced near-miss coverage across the existing five axes;
- use fresh exact prompts;
- exclude exact prompt reuse from all prior exposed T023/MG1 acceptance corpora available in canonical Git, including v12, v13 and v14;
- import zero prior-epoch observations into v15 scoring;
- avoid tuning candidate wording because of exposed historical cases;
- close and rotate the epoch if exact holdout content is used to change candidate semantics after freeze.

Prior observations may be used only as historical design evidence.

### 12. Same live-cell comparability

The next Design/Plan SHALL preserve the currently accepted live-cell identity unless a separate pre-observation decision explicitly changes comparability semantics:

```text
Executor adapter: Codex
Host: native Windows
Model: GPT-5.6 Sol
Reasoning effort: Medium
Codex CLI: exactly 0.149.0
```

No newer CLI/model is silently equivalent.

### 13. Provider-call boundary

Explore, Specify, Design, Plan & Trace and D068 Candidate Materialize issue zero provider/model acceptance calls.

A later D068 Stage 6 requires a separate explicit Human selection and persisted launch gate.

Provider-free deterministic verification occurs before backend/workspace preflight and synthetic canary. Acceptance scheduling begins only after the canary passes.

### 14. D052 semantic-oracle ownership

The v15 oracle, corpus semantics, selection/materiality rules, futility semantics and integrity guards that directly encode this decision are Orchestrator-owned semantic conformance assets under D052.

The Stage 6 Executor may execute and technically diagnose them and may make bounded technical repairs only when semantics remain unchanged.

A semantic change requires persisted Orchestrator re-entry.

## D050 refinement relationship

D074 preserves D050's central product decision:

- one Agent Governance product/distribution identity;
- one canonical capability source;
- one Core and deterministic engine;
- activation topology determined empirically;
- F2/G3 are challengers rather than preselected winners;
- selection considers routing quality, context, risk, correctness and source integrity;
- thresholds and victory criteria are pre-registered before results;
- T024 projects only the topology selected by T023.

D074 prospectively refines only the **experimental dependency** that previously required a qualifying single-family reference before challengers could be observed.

Historical v12-v14 reference-gated experiments retain exactly the meaning they had when executed.

## Consequences

### Keep

- B2/F2/G3 bytes unchanged for the next epoch;
- absolute qualification and safety thresholds;
- 2+1 aggregation and exact futility;
- D050 architecture and one-product identity;
- provider/host comparability;
- historical evidence immutability.

### Change

- F2/G3 scheduling is independent of B2 qualification;
- B2 becomes a non-blocking same-epoch control;
- a prospective admissibility-dominance regime exists when B2 is scientifically non-qualifying;
- the next corpus/oracle/execution/trial-envelope identities are new.

### Do not introduce

- automatic preference for split topologies;
- post-hoc threshold weakening;
- historical rescoring;
- reuse of exposed exact prompts as fresh acceptance stimuli;
- candidate wording tuning inside the RIQ-NBC controlled-variable experiment;
- release selection from technically invalid evidence.

## Rollback

D074 is prospective and can be superseded before Stage 5 only through a new explicit Orchestrator decision.

Once the v15 candidate freeze and fresh holdout are exposed, semantic changes require closure of that epoch and a new acceptance identity rather than in-place tuning.
