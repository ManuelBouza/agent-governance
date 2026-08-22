# T023 — Agent Governance Skill Activation Topology Evals

## Identity

- Task ID: `T023`
- Status: `BLOCKED`
- Type: `test/eval`
- Base branch: `develop`
- Expected topic branch: `test/t023-skill-activation-topology-evals`
- Expected executor handoff: `handoffs/T023-executor-handoff.json`
- Assurance-Class: `routing/behavioral-eval + deterministic-isolation + context/distribution evidence`
- Test-Authorship-Mode: `mixed`
- Readiness note: Remains `BLOCKED` until T022 is ACCEPTED and MG1 is integrated into `develop` with the D050 topology corpus, D052 conformance oracle and victory thresholds pre-registered.

## Objective

Compare the D050 Agent Governance Skill activation topologies under a controlled experiment that keeps Governance Core, deterministic engine, profile/capability semantics and functional behavior fixed.

Select the activation/distribution projection that meets the pre-registered multidimensional criteria, or preserve a single-dispatcher/thin-router outcome when split entrypoints do not demonstrate accepted material advantage.

This task decides an **activation topology**, not Governance authority, runtime semantics or the number of independently maintained products.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/decisions/D050-canonical-capability-source-and-evaluated-skill-topology.md`
- `docs/decisions/D051-single-install-self-bootstrap-and-durable-project-footprint.md`
- `docs/decisions/D052-specification-owned-conformance-test-authorship.md`
- `docs/decisions/D046-agent-capability-engineering-and-context-architecture.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- MG1-integrated canonical/experimental Skill routing Markdown and pre-registered D052 conformance assets
- `docs/TESTING-AND-EVALUATION.md`
- `docs/CONTEXT-ARCHITECTURE.md`
- `docs/MAINTAINER-SKILL-CONTRACT.md`
- `docs/GOVERNANCE-SKILL-CONTRACT.md`

## D052 ownership split

MG1/ChatGPT Orchestrator owns the semantic acceptance oracle for this experiment before T023 starts, including at minimum:

- exact candidate topology definitions/identities;
- positive/negative/near-miss/cross-profile/ambiguous/multi-intent corpus membership;
- expected classifications/outcome semantics;
- fixed train/validation or equivalent holdout partition when applicable;
- repeated clean-context trial method;
- applicable metric definitions;
- material-improvement and mandatory non-regression thresholds;
- semantic negative controls;
- deterministic grader/assertion expectations that encode the approved comparison meaning.

Those assets are frozen once T023 begins unless a persisted ChatGPT revision explicitly restarts/redefines the experiment.

The executor owns technical realization and verification execution, including:

- host/model/provider runner/adapters where authorized;
- environment/session isolation;
- trace/result collection;
- metric computation from the frozen oracle/results;
- technical harness plumbing;
- supplementary implementation/exploratory tests and diagnostics that do not redefine the frozen oracle;
- the executor handoff and evidence package.

If the executor finds a suspected semantic defect in the MG1 oracle, it must stop the affected claim and report an `ORACLE_DEFECT`-equivalent blocker with evidence rather than changing expected classifications, thresholds or semantic grader meaning.

## Required topology set

T023 MUST evaluate at least the MG1-frozen forms of:

- **B0 — unified dispatcher baseline**: one top-level Agent Governance dispatcher with `consumer` / `source-maintainer` routing;
- **B1 — thin single router**: one minimal dispatcher with progressive focused references;
- **F2 — generated profile peers**: Consumer Governance + Source Maintainer generated peer Skills;
- **G3 — hybrid challenger**: Consumer lifecycle + Source Maintainer + External Skill Trust generated peer Skills.

For G3, External Skill Trust contains only the already-defined external Skill discovery and supply-chain audit capability surface. It is a challenger topology, not a pre-accepted release architecture.

Any additional candidate requires MG1 authority before T023 starts. Provider-specific/nested-Skill experiments MUST be reported separately and cannot redefine the portable comparison set.

## Authorized scope

- Non-Markdown runner/harness/adapters and result evidence needed to execute the already-integrated MG1/D052 experiment.
- Non-Markdown deterministic profile-isolation/routing implementation tests required to verify constant semantics across topology candidates.
- Non-Markdown context/load-path instrumentation or structured traces that measure the MG1-defined metrics without introducing telemetry/network dependencies outside the test harness.
- Temporary/ignored generated Skill/package outputs produced from the MG1-owned canonical experimental definitions.
- Non-Markdown structured topology-selection evidence derived from the frozen MG1 oracle and executed results.
- Supplementary executor-authored diagnostic/edge/adversarial cases that do not change the pre-registered selection rule or required corpus.
- Mechanical harness corrections only when they preserve the frozen semantic oracle and are authorized by the durable task/review flow.
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics.
- Changes to accepted deterministic capability behavior merely to improve one topology.
- Post-hoc modification of the MG1 corpus, expected classifications, variants, host/model matrix, repeated-trial method, metric meaning or victory thresholds after comparative results are observed.
- Executor-authored semantic replacement of any D052 Orchestrator-owned conformance asset.
- Creating independently maintained Governance Skill sources/products.
- Independent per-entrypoint product/version identities.
- Making portable correctness depend on Skill-to-Skill invocation.
- Introducing a manager/multi-agent product architecture.
- Requiring users to manually assemble multiple Agent Governance packages/support files in order to realize a candidate topology.
- Unrelated provider/model routing, production host configuration, permissions, Gentle AI/Caveman integration, or release promotion.
- Direct writes to `develop` or `main`.
- Editing committed `SKILL.md`, profile references or experimental Skill Markdown; those are MG1/ChatGPT-owned.
- T026 or source persistence convergence.

## Experiment invariants

Across B0, B1, F2 and G3, T023 MUST hold constant the accepted:

- Governance Core semantics and identity;
- shared deterministic engine behavior;
- `consumer` and `source-maintainer` profile semantics;
- functional capability set except for presentation/routing partition;
- source-independence requirements;
- Consumer/source permission and mutation boundaries;
- deterministic regression baseline;
- canonical capability/source authority;
- D051 one-product/single-install Consumer distribution constraint;
- D052 frozen conformance-oracle meaning for the comparative experiment.

A topology MAY change which Skill metadata/body/reference is exposed or activated. It MUST NOT gain an artificial advantage by changing the governed behavior being routed or the acceptance oracle used to score it.

## Required corpus classes

The MG1 corpus MUST be persisted before T023 and executed with the repetition/isolation policy pre-registered before T023. It includes at least:

- positive Consumer lifecycle prompts;
- positive state/event/mission/handoff/sequencing prompts;
- positive coexistence prompts;
- positive external Skill discovery/audit prompts;
- positive source-maintainer prompts;
- negative generic coding/SDD/tooling prompts;
- near-miss Governance, Skill-installation and source-maintenance prompts;
- cross-profile cases designed to detect Consumer/source-maintainer contamination;
- ambiguous cases with an expected bounded/insufficient-context behavior;
- multi-intent cases where one or more capabilities may legitimately be needed.

The executor may add exploratory cases for diagnosis, but those additions cannot silently enter the frozen acceptance score or change the pre-registered decision rule.

## Required evidence dimensions

T023 MUST report the MG1-predeclared measures applicable to the harness, including:

1. **Functional non-regression** — task success and deterministic capability outputs remain equivalent where topology should not affect semantics.
2. **Activation quality** — precision, recall, F1 or the accepted equivalent over positive/negative/near-miss cases.
3. **Isolation** — cross-profile contamination and unauthorized context/permission acquisition.
4. **Routing quality** — wrong-specialist selection and failure-to-select rates.
5. **Overactivation** — unnecessary multiple Skill activations per task.
6. **Context/load path** — actual host traces when available or an explicitly labelled deterministic load model; report TMC/RFO/ND/CAR-compatible evidence without calling byte heuristics exact tokens.
7. **Permission/risk exposure** — when host/runtime observability makes comparison meaningful; host-specific guarantees must be labelled as such.
8. **Portability** — results across the MG1-supported host/model matrix, separating portable findings from provider-specific behavior.
9. **Source/distribution integrity** — no duplicate authority/runtime source, source independence preserved, and all candidates remain projections of one product/capability source.
10. **Single-install feasibility** — whether the candidate can reasonably be projected by T024 into one self-contained Agent Governance distribution installation unit on the intended release-target host set, without manual assembly of product-owned support files.

T023 does not implement final platform wrappers; its installability evidence may therefore be architectural/package-feasibility evidence rather than final install execution. Final proof belongs to T024/T029.

## Selection rule

MG1 MUST define and persist the exact numeric/qualitative material-improvement and non-regression thresholds before T023 starts.

T023 MUST apply those thresholds without changing them after results are observed.

A topology cannot be selected if it weakens any mandatory deterministic correctness, Governance authority, profile isolation, Consumer source-independence, package boundary, D051 single-install feasibility or required security invariant.

Among candidates satisfying all mandatory invariants, select according to the pre-registered multidimensional criteria. A split topology must demonstrate the predeclared material benefit; multiple Skills are not presumed better merely because they are smaller or more modular.

If no split topology meets the pre-registered advantage criteria, B0 or B1 remains a valid accepted architecture.

## Acceptance criteria

### AC-T023-1 — controlled topology equivalence
All evaluated candidates use the same accepted Core/engine/profile/capability semantics, and deterministic functional regressions are green.

### AC-T023-2 — complete pre-registered routing corpus
The exact MG1/D052 positive, negative, near-miss, cross-profile, ambiguous and multi-intent cases execute under the pre-registered repetition/isolation method with raw/structured evidence retained.

### AC-T023-3 — multidimensional comparison
Activation, routing, overactivation, isolation, context/load-path and D051 installability-feasibility dimensions are reported exactly as pre-registered; applicable portability/permission evidence is separated into portable versus host-specific claims.

### AC-T023-4 — threshold and oracle integrity
The selection uses the MG1 thresholds, expected outcomes and semantic graders frozen before comparative results. No threshold/corpus/classification/oracle mutation is used to force a preferred architecture.

### AC-T023-5 — one-product/source/install invariant
Every candidate remains traceable to one canonical capability source, one Core and one deterministic engine; no second normative or independently maintained runtime source is introduced; the selected candidate remains compatible with D051 one-product/single-install packaging.

### AC-T023-6 — objective topology outcome
Evidence yields exactly one accepted outcome under MG1 rules: B0, B1, F2, G3, or an explicitly pre-authorized additional candidate. If no challenger meets the accepted advantage criteria, the valid result is retention of the qualifying single-dispatcher/thin-router candidate rather than forced fragmentation.

### AC-T023-7 — D052 ownership/evidence boundary
The submitted branch preserves the frozen Orchestrator-owned conformance assets, records any supplementary executor-authored cases separately from the acceptance score, and provides evidence that the required oracle was executed rather than reconstructed or weakened during implementation.

## Verification requirements

- Run the complete MG1/D052 topology corpus with the predeclared repeated clean-context trial method.
- Run deterministic profile-isolation and Consumer/source-maintainer regression tests.
- Run artifact/source-independence regression necessary to prove the candidates did not alter accepted runtime/distribution semantics.
- Persist raw/structured non-Markdown evidence sufficient to recompute the reported routing metrics from the frozen corpus/results.
- Persist candidate identity/provenance sufficient to prove that the evaluated presentation is the MG1-frozen one.
- Persist structured context/load-path measurements or explicitly labelled deterministic load-model evidence.
- Persist the MG1-defined installability/package-feasibility evidence for each candidate where applicable.
- Report per-host/per-model results separately where the matrix has multiple cells; do not collapse provider variance into one opaque score.
- Distinguish required D052 conformance cases from supplementary executor-authored diagnostic/exploratory cases in evidence.
- Map every acceptance criterion to exact evidence type/path in the handoff.

## Stop / escalation conditions

Stop and report `BLOCKED` rather than broadening scope if:

- MG1 is not integrated into current `develop`;
- MG1 lacks pre-registered topology variants, conformance corpus/expected outcomes or victory/non-regression thresholds;
- the executor identifies a suspected semantic `ORACLE_DEFECT` in the frozen MG1/D052 acceptance assets that cannot be resolved mechanically without changing meaning;
- the harness cannot distinguish topology quality from unrelated provider/network instability to the degree required by the predeclared method;
- candidate construction would require executor-authored committed Markdown;
- an apparently winning topology requires changed Core/runtime semantics or broader source-maintainer authorization;
- a proposed solution requires portable Skill-to-Skill invocation or new multi-agent product architecture;
- the only way to realize a candidate on the intended supported host set is multiple manual Agent Governance installations or out-of-band product support files contrary to D051;
- T022/profile isolation is not accepted and stable.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T023-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, follow D048's normal-task publication boundary, commit/push all authorized work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
