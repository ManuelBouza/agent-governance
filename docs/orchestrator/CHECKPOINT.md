# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O100  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

D044 + D050 + D051 + `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md` control the prospective Agent Governance product/distribution architecture. D052 prospectively controls specification-owned conformance-test authorship for Skill/governance/documentation-managed semantic work.

D049 controls RCAB snapshot/live semantics. D048 controls normal-task publication timing.

Accepted/integrated implementation baselines remain T018-T020, T030 and T031.

The active executable sequence is unchanged by the D050/D051/D052 architecture/method gates:

```text
T032 R1 rework + acceptance/integration
    -> green canonical deterministic baseline
    -> T021 R1 rework + acceptance/integration
    -> T022
    -> MG1 Skill topology/eval pre-registration + D052 conformance oracle
    -> T023 comparative activation-topology eval
    -> T024 selected topology / D051 packaging
```

T026 remains BLOCKED behind its separate explicit decision gate.

## D050 — evaluated Skill activation topology

D050 separates:

```text
normative authority        = governance-core/
runtime semantics          = shared deterministic engine
authoring/capability unit  = one canonical capability source
distribution unit          = one Agent Governance product/version
activation unit            = one or more generated coherent Skills
```

MG1/T023 must compare at least B0/B1/F2/G3 under pre-registered multidimensional criteria. Portable Agent Governance must not depend on Skill-to-Skill invocation or unapproved multi-agent product architecture.

Multiple generated entrypoints remain one Agent Governance product/distribution and are not independently versioned by default.

PR #140 integrated D050 and the future T023/T024/T028/T029 contract refinements. `OP063` is cleanup-only for `docs/d050-skill-activation-topology`; it has no executable continuation and must not alter T032/T021 sequencing.

## D051 — single-install / self-bootstrap Consumer invariant

Human Owner approval on 2026-08-17 selected D051.

The Consumer release UX is:

```text
install Agent Governance once
        -> bootstrap clean target repository
        -> durable .agent-governance/ + .agent-coordination/
        -> validate / operate without source checkout
```

D051 distinguishes:

- **distribution payload** — reusable Agent-Governance-owned entrypoints/runtime/Core snapshot/templates/assets/schemas/provenance carried by one installed Agent Governance product;
- **project footprint** — durable Governance authority/state materialized by bootstrap inside the governed repository.

The user must not manually install/copy a second Agent Governance Core/runtime/template/schema/Skill support payload after the distribution is installed.

Normal bootstrap from an installed release must not require the Agent Governance source checkout or network retrieval of missing Agent Governance payload files.

D051 does not bundle arbitrary project-native or third-party capabilities. External Skills remain separately discovered/audited/approved; project-native tooling remains governed by coexistence rules.

D051 preserves D050: even if T023 selects multiple generated Agent Governance Skills, they must be projectable by T024 into one product installation unit/bundle on each supported release-target platform.

D051 also preserves the version separation:

```text
distribution update != project-footprint migration
```

T027/MG2 must keep project migration explicit/transactional; updating the installed distribution alone cannot silently mutate `.agent-governance/` / `.agent-coordination/`.

## D052 — specification-owned conformance test authorship

Human Owner approval on 2026-08-17 selected D052.

Core rule:

```text
Test authorship follows semantic authority.
```

D052 defines three modes when ownership is material:

- `orchestrator-conformance` — ChatGPT owns the required acceptance/conformance oracle; executor executes it and may add supplementary technical tests;
- `executor-implementation` — executor owns technical test/eval implementation and execution within ChatGPT-owned acceptance semantics;
- `mixed` — ChatGPT owns the semantic oracle while executor owns implementation/exploratory tests and executes both.

For Skill/governance/policy/documentation-managed semantic products, `orchestrator-conformance` or `mixed` is the expected default when ChatGPT owns the correctness meaning. Ordinary consumer/application implementation remains `executor-implementation` by default.

Orchestrator-owned conformance assets are narrowly limited to executable acceptance projections such as required assertions, positive/negative/near-miss/cross-profile/ambiguous corpora, expected outcomes/classifications, frozen holdouts, semantic negative controls, thresholds represented as data, golden fixtures, security acceptance cases and deterministic grader expectations.

The executor retains implementation, technical harness/adapters, supplementary tests, property/fuzz/exploratory discovery, all required test/eval execution, diagnostics, traces and evidence.

Semantic changes to an Orchestrator-owned oracle require persisted ChatGPT authority. A suspected semantic defect is reported as `ORACLE_DEFECT`-equivalent rather than silently changed. Tests remain evidence, never Governance authority.

D052 does not override D041 process autonomy beyond this material ownership boundary and does not change ICAE assurance-plane selection.

Expected RCAB benefit is not presumed: pre-authored conformance may reduce executor semantic reconstruction/document load, but actual load-path/token benefit must be measured.

### Grandfathering / first application

- T032 R1 remains under its already-launched contract and is not re-scoped.
- T021 R1 remains under its existing contract and is not re-scoped.
- T022 may complete under its already-integrated runtime/profile contract.
- MG1/T023 is the first strong planned D052 application.
- T023 is now `Test-Authorship-Mode: mixed`; MG1 must persist the semantic corpus/expected outcomes/threshold oracle before T023 begins.

## PR #142 / OP065

PR #142 is the Markdown-only D052 policy gate. Its intended scope is:

- `docs/decisions/D052-specification-owned-conformance-test-authorship.md`;
- D016/D019/D046 ownership refinements;
- `AGENTS.md` D052 ownership override;
- `docs/TASK-CONTRACTS.md` test-authorship modes and preimplementation conformance gate;
- `docs/TESTING-AND-EVALUATION.md`;
- `tests/README.md` and `evals/README.md` ownership guidance;
- refined T023 D052 `mixed` contract;
- `docs/operations/OP065-retire-d052-test-authorship-gate.md`;
- this checkpoint.

The gate is prospective and must not modify T032/T021/T022 executable state or authorize T026.

After PR #142 is merged, `OP065` may retire exactly `docs/d052-specification-owned-conformance-tests` and publish its durable receipt to PR #142. OP065 is cleanup-only and has no executable continuation.

Because PR #142 modifies `AGENTS.md`, the next executor launch governed by a post-PR-#142 integrated change must follow D043's conditional current-`AGENTS.md` reload when a running session may still hold the pre-D052 instruction snapshot. This does not retroactively interrupt an already-running T032 invocation.

## PR #141 / OP064

PR #141 is the Markdown-only D051 product gate. Its aggregate intended scope is:

- `docs/decisions/D051-single-install-self-bootstrap-and-durable-project-footprint.md`;
- `docs/GOVERNANCE-SKILL-CONTRACT.md`;
- `docs/GOVERNANCE-SKILL-PACKAGE.md`;
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`;
- refined T023/T024/T027/T029 future Task Contracts;
- `docs/operations/OP064-retire-d051-single-install-gate.md`;
- this checkpoint.

The gate is prospective and must not modify T032/T021/T022 executable state or authorize T026.

After PR #141 is merged, `OP064` may retire exactly `docs/d051-single-install-self-bootstrap` and publish its durable receipt to PR #141. OP064 is cleanup-only and independent of OP063/T032/T021.

## T032 — active R1 rework frontier

Last reviewed/rejected submitted HEAD: `b43b306e56c6b90969c3dd10e23ccf8e00cc8ba5`  
Implementation anchor of that rejected candidate: `26c9b6481ffc458cf773320390a0ae19b0271c52`  
Review authority: `docs/reviews/T032-R1.md`

OP062 Stage A already passed and authorized the T032 R1 continuation. The remaining blocker is complete offline snapshot-integrity binding while preserving D049 snapshot/live separation and a green deterministic baseline.

R1 requires:

- deterministic binding of the complete snapshot epoch-evidence payload without self-reference;
- exact recomputation/validation of derived bootstrap/ratchet state;
- verifiable registry identity from snapshot-carried canonical semantics;
- canonical entry/type/order checks;
- canonical serialization or equivalent identity boundary;
- independent tamper negative controls for metadata/metrics, registry identity and bootstrap/ratchet state;
- historical snapshot + explicit stale + live-current behavior preserved;
- green full deterministic and package/isolation regressions.

Do not change D049/D047 semantics to solve T032.

D052 does not retroactively transfer T032 test authorship; its current executor rework remains governed by T032-R1.

## T021 remains frozen

T021 submitted HEAD `969e2130ca9abb27c6ae5ad830923582f45b8a2f` remains `IN_PROGRESS / REWORK_REQUIRED` under `docs/reviews/T021-R1.md`.

Its blocker remains the unsupported directly constructed `Profile` bypass at the engine boundary.

Do not rework or merge T021 until corrected T032 is accepted/integrated and the canonical deterministic baseline is green.

D050/D051/D052 do not change T021's bounded correction.

## T022 / MG1 / T023 boundaries

T022 remains sequenced after T021 acceptance and still adds the `source-maintainer` profile over the shared engine/current source-maintenance adapters. It may complete under its existing test ownership semantics rather than being retrofitted with D052.

Only after T022 is accepted may MG1 freeze and persist the D050/D051/D052 topology experiment, including:

- exact candidate Skill definitions/identity;
- Orchestrator-owned positive/negative/near-miss/cross-profile/ambiguous/multi-intent corpus;
- expected classifications/outcome semantics;
- semantic negative controls and accepted deterministic grader expectations;
- repeated clean-context method;
- practical host/model matrix;
- activation/routing/overactivation/isolation/context/portability metrics;
- D051 single-install/package-feasibility evidence definition;
- material-improvement and mandatory non-regression thresholds.

Corpus/expected outcomes/thresholds must be fixed before T023 comparative results are observed. T023 executor owns technical runner/adapters, execution, supplementary diagnostics/tests, traces and evidence, not semantic mutation of the frozen oracle.

T023 cannot select a topology that intrinsically requires multiple manual Agent Governance installations or out-of-band product support payload assembly.

## Future packaging/release consequences

- T024 must generate exactly the T023-selected topology as one self-contained Agent Governance installation unit per supported release-target platform and prove clean one-install -> bootstrap -> validate/operate behavior without source checkout.
- T027 must keep distribution update separate from explicit project-footprint migration and preserve one-product update identity across multiple generated entrypoints.
- T028 retires independently maintained product/source assumptions, not necessarily multiple generated entrypoints.
- T029 must verify one distribution/Core/engine/capability identity, D051 clean-install journey, source-maintainer overlay exclusion, explicit migration semantics and Consumer v1 rollback.
- future Skill/governance/documentation-managed conformance work should declare D052 authorship mode instead of assuming all executable tests belong to the executor.

## EGLL

- L003 `task.done_requires_rework`: `CONTROL_PLANNED`.
- L004 `workflow.procedural_nonconformance`: `CONTROL_PLANNED`.
- L005 `workflow.premature_remote_publication`: `CONTROL_INTEGRATED`, not VERIFIED.
- L006 `verification.generated_snapshot_live_coupling`: `CONTROL_PLANNED`; D049 remains sound, but corrected T032 is still required for integration.

D052 is a methodology/ownership response informed by T020/T030/T032 evidence. It does not by itself mark L003 VERIFIED; representative implemented/replay evidence is still required for any systemic-control verification claim.

## Next Action

1. Keep T032 R1 as the primary executable frontier. When the executor returns a corrected completion, read the exact remote branch/handoff and OP062 receipt from GitHub and review against T032-R1.
2. Accept/integrate corrected T032 only if complete snapshot-integrity negative controls and full green regression pass; then perform required cleanup.
3. Resume T021-R1 only after T032 acceptance/integration/cleanup.
4. After T021 acceptance/integration, proceed to T022 under its existing contract.
5. After T022 acceptance, execute MG1 under D050 + D051 + D052 and persist the D052 conformance oracle before T023.
6. Execute T023 as `mixed`: executor runs the frozen oracle plus supplementary technical verification; semantic oracle changes require persisted Orchestrator revision.
7. T024 must implement the exact selected topology and D051 one-install/self-bootstrap package path.
8. OP063, OP064 and OP065 are cleanup-only and may be executed independently when their respective PRs are merged; none authorizes executor Task continuation.
9. Do not launch T026 without its explicit separate gate.

## Next Chat Minimum Load

After normal bootstrap:

- D049, T032, T032-R1, L006 and OP062 while T032 is open;
- T021 + T021-R1 only after T032 acceptance permits rework;
- D048/L005 only when publication timing is material;
- D052 + Task Contracts when test-authorship/oracle ownership is material;
- D044 + D050 + D051 + unified refactor plan when architecture/sequencing beyond T021/T022 is material;
- T023 + D050/D051/D052 details only when preparing MG1 or the topology/package experiment.

## Do Not

Do not accept/merge rejected T032 HEAD `b43b306e...`; weaken snapshot tamper/currentness semantics; change D047 thresholds; resume T021 early; mutate T021 during T032; retroactively transfer T032/T021 test ownership under D052; let an executor silently alter an Orchestrator-owned expected result/classification/threshold/semantic negative control; treat tests as authority; claim token savings without RCAB load-path evidence; push intermediate normal-task progress without D048 authority; interpret D050 as command/file micro-Skill decomposition; require Skill-to-Skill invocation; introduce multi-agent product architecture; independently version generated Skills; require manual supplemental Agent Governance product payload after installation; confuse durable project footprint with a second package; silently migrate governed project footprint on distribution update; run T023 before T022+MG1; launch T026 early; delegate committed Markdown; or write directly to `develop`/`main`.
