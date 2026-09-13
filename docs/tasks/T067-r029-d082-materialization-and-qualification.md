# T067 — R029 / D082 Materialization and Post-Materialization Qualification

## Identity

- Task ID: `T067`
- Status: `IN_PROGRESS`
- Type: `refactor`
- SDD profile: `ASSURED`
- Base branch: `develop`
- Base SHA: `758b92cf38af9bc06e4717b1206dafb8e5d82e9e`
- Expected topic branch: `refactor/r029-d082-materialization`
- Expected executor handoff: `handoffs/T067-executor-handoff.json`
- Test-Authorship-Mode: `mixed`
- Owner: `ChatGPT Orchestrator (specification/Design/Plan/acceptance and D068 Stage 5 materialization) / Agente de IA Ejecutor (D068 Stage 6 execution/diagnosis/bounded repair/verification) / Human Owner (final authority)`
- Execution Shape: `MULTI_EXECUTION`
- ChatGPT Effort: `HIGH`

## Objective

Materialize the production instruction/Skill architecture adopted for R029 by D082 and perform its post-materialization qualification without weakening any preserved authority, safety, cold-start, ownership, routing or residual condition.

The accepted target topology is exactly:

```text
lean always-loaded root AGENTS.md
  + one Agent Governance Maintainer top-level domain Skill
       -> Orchestrator internal route
       -> Executor internal route
  + five top-level transverse capabilities
       -> repository-change-control
       -> upstream-version-revalidation
       -> research-evidence-traceability
       -> durable-work-checkpoint
       -> executor-launch-handoff
            -> workspace-isolation internal route/reference
  + host-specific adapters/references only where mechanics differ
  + deterministic scripts/CI/references for mechanical enforcement
```

This task does not reopen R029 topology selection. Any material authority gap, routing ambiguity, topology conflict or contradictory evidence discovered during materialization/qualification is a fail-closed SDD/decision re-entry condition.

T066 is explicitly out of scope and MUST remain untouched.

## Current specification carrier / controlling references

Load only the smallest authoritative set needed for the active unit. Controlling authority is:

- `AGENTS.md`
- `docs/decisions/D082-r029-lean-root-and-transverse-skill-architecture.md`
- `docs/decisions/D068-library-first-candidate-materialization-executor-verification-boundary.md`
- `docs/decisions/D061-orchestrator-branch-target-write-guard.md`
- `docs/decisions/D067-objective-scoped-orchestrator-chat-lifecycle.md`
- `docs/decisions/D080-orchestrator-execution-shape-control.md`
- `docs/orchestrator/R029-S1-ROOT-PRESERVATION-MAP.md`
- `docs/orchestrator/R029-S2-LEAN-ROOT-RESPONSIBILITY-CONTRACT.md`
- `docs/orchestrator/R029-S3-MAINTAINER-DOMAIN-BOUNDARY.md`
- `docs/orchestrator/R029-S4-REPOSITORY-CHANGE-CONTROL-CANDIDATE.md`
- `docs/orchestrator/R029-S5-UPSTREAM-VERSION-REVALIDATION-CANDIDATE.md`
- `docs/orchestrator/R029-S6-RESEARCH-EVIDENCE-TRACEABILITY-CANDIDATE.md`
- `docs/orchestrator/R029-S7-DURABLE-WORK-CHECKPOINT-CANDIDATE.md`
- `docs/orchestrator/R029-S8-EXECUTOR-LAUNCH-HANDOFF-CANDIDATE.md`
- `docs/orchestrator/R029-S9-WORKSPACE-ISOLATION-PLACEMENT.md`
- `docs/orchestrator/R029-S10-CANDIDATE-TOPOLOGY-EVALUATION-PLAN.md`
- `docs/orchestrator/R029-PRE-DECISION-EVALUATION.md`
- `docs/orchestrator/R029-E3-CONVERGENCE.md`
- `docs/MAINTAINER-SKILL-CONTRACT.md`
- `docs/TASK-CONTRACTS.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `maintainer-skill/references/TASK-CONTRACT-V4-TEMPLATE.md`
- `maintainer-skill/references/TASK-CONTRACT-TEMPLATE-USAGE.md`

R029 scientific evidence remains evidence; D082 is the normative architecture authority.

## Requirement / specification delta

### ADDED

- `T067-A1` Materialize a lean always-loaded `AGENTS.md` that preserves all 79 S1 semantic units with `ROOT=39`, `ROOT+ROUTE=20`, `ROUTE=20`, uncovered `0`.
- `T067-A2` Materialize the single top-level Agent Governance Maintainer Skill with internal Orchestrator and Executor routes; source-maintenance authority remains repository/domain policy rather than Skill-local authority.
- `T067-A3` Materialize exactly five top-level transverse Skills with the logical names adopted by D082: `repository-change-control`, `upstream-version-revalidation`, `research-evidence-traceability`, `durable-work-checkpoint`, and `executor-launch-handoff`.
- `T067-A4` Materialize workspace isolation only as an internal route/reference under `executor-launch-handoff`, consuming repository-change-control/repository-local policy for branch/base/integration/retirement semantics; it MUST NOT become a sixth top-level Skill.
- `T067-A5` Materialize deterministic conformance/qualification assets sufficient to verify semantic coverage, topology, activation/anti-trigger boundaries, no-Skill operation and post-materialization burden measurements without depending on model-driven Skill activation.
- `T067-A6` Measure on the materialized candidate: lean-root byte size, initial Skill catalog metadata burden, representative conditional context load, duplicated normative text, and reference-hop depth.
- `T067-A7` Qualify real Maintainer-domain activation/anti-trigger behavior rather than promoting the historical `21/36` Maintainer observation into PASS.
- `T067-A8` Preserve the R029 residual that ChatGPT/Codex empirical parity is `NOT_ESTABLISHED`; no later artifact may relabel the waived `0/36` ChatGPT half as PASS.
- `T067-A9` Reuse the prior 36/36 Codex transverse evidence unless Stage 5 introduces a material change to the scored transverse semantics/descriptions or a later controlling qualification authority explicitly requires fresh provider/model evidence.

### PRESERVED

- `T067-P1` Human Owner, ChatGPT Orchestrator and product-agnostic Executor authority/ownership boundaries remain unchanged except for the already-adopted D068 Stage 5/6/7 source-maintenance refinement.
- `T067-P2` Authority, ownership, safety, fail-closed behavior, durable authority and cold-start correctness remain available before optional Skill activation.
- `T067-P3` Skills remain tooling/routing aids, not governance authority; deterministic tests and bootstrap paths remain valid with Skills absent or disabled.
- `T067-P4` Agent Governance source maintenance and consumer governance remain separate activation domains; consumer-governance MUST NOT activate for source-product maintenance and Maintainer MUST NOT activate merely because an adopting repository uses Agent Governance.
- `T067-P5` Agent Governance-specific D052/D053/D054/D055/D058/D060/D061/D062/D065/D068/D076/D077 semantics remain domain-side and are not generalized into transverse authority.
- `T067-P6` Historical/grandfathered persisted authority keeps its original meaning; this refactor does not silently migrate completed historical tasks/handoffs.
- `T067-P7` Progressive disclosure is preserved and normative duplication is reduced rather than displaced into multiple competing instruction copies.
- `T067-P8` T066 Stage 5 remains `NOT_STARTED` and is not modified, launched, evaluated or combined with T067.

## Controlling Design

### 1. Always-loaded root

`AGENTS.md` remains the pre-routing safety/authority surface and MUST retain the twelve S2 responsibility families:

1. repository identity and contamination boundary;
2. authority model and host neutrality;
3. write/file ownership boundary;
4. SDD stage and stop/re-entry safety boundary;
5. semantic-vs-execution boundary and Human gate;
6. durable authority over ephemeral/private context;
7. bootstrap and routing anchors;
8. repository mutation/branch safety;
9. durable handoff/completion boundary;
10. research/evidence non-authority and freshness triggers;
11. Skill independence/coexistence boundary;
12. instruction architecture/change-discipline guardrail.

A root trigger may route detail outward, but no ROOT/ROOT+ROUTE precondition may become dependent on successful Skill activation.

### 2. Maintainer domain package

The production package remains `maintainer-skill/` and gains `maintainer-skill/SKILL.md`.

Internal role context is represented through narrow references rather than separate top-level role Skills:

- `maintainer-skill/references/orchestrator-route.md`
- `maintainer-skill/references/executor-route.md`

The existing Task Contract references remain part of the package and MUST remain reachable from the Orchestrator route:

- `maintainer-skill/references/TASK-CONTRACT-V4-TEMPLATE.md`
- `maintainer-skill/references/TASK-CONTRACT-TEMPLATE-USAGE.md`

`docs/MAINTAINER-SKILL-CONTRACT.md` and `maintainer-skill/STATUS.md` are revised only as needed to describe the adopted/materialized architecture and release/qualification state. Standing repository policy SHOULD be referenced rather than duplicated into route-local prose.

### 3. Transverse package layout

The existing source-product Skill convention is a top-level `*-skill/` package containing `SKILL.md`. The five D082 logical capability names are therefore materialized as:

- `repository-change-control-skill/SKILL.md` with frontmatter `name: repository-change-control`
- `upstream-version-revalidation-skill/SKILL.md` with frontmatter `name: upstream-version-revalidation`
- `research-evidence-traceability-skill/SKILL.md` with frontmatter `name: research-evidence-traceability`
- `durable-work-checkpoint-skill/SKILL.md` with frontmatter `name: durable-work-checkpoint`
- `executor-launch-handoff-skill/SKILL.md` with frontmatter `name: executor-launch-handoff`

Workspace isolation is represented at:

- `executor-launch-handoff-skill/references/workspace-isolation.md`

No `workspace-isolation/SKILL.md` or equivalent sixth top-level Skill is permitted.

Host-specific mechanics may be added only as narrow `references/` material when a real mechanics difference requires it. Host identity MUST NOT split semantic capabilities or authority.

### 4. Activation/routing contract

Each production `SKILL.md` MUST carry a narrow positive trigger, explicit anti-triggers, a bounded postcondition and an authority boundary consistent with R029 S4-S8. The same semantic intent uses the same transverse capability across ChatGPT/Codex/other compatible hosts by default.

For Agent Governance source work, Maintainer domain context remains the domain entry point and may compose with the minimum required transverse capability. Composition does not create competing authority.

### 5. Qualification assets

Stage 5 MUST publish Orchestrator-owned semantic/conformance assets before Stage 6. The candidate shall include a dedicated deterministic R029 qualification surface under `evals/r029_materialization/` and/or `tests/`, containing at minimum:

- a machine-readable 79-unit preservation ledger mapping each S1 ID to its materialized root/route/reference destination;
- activation/anti-trigger cases for Maintainer domain selection and the five transverse capabilities, including source-maintenance positives, consumer/non-source anti-triggers, generic-tool near misses and cross-capability ambiguity;
- structural assertions for exactly five transverse top-level Skills and subordinate workspace isolation;
- cold-start/no-Skill assertions proving correctness does not require Skill activation;
- burden-measurement inputs/results for root size, initial catalog metadata, representative conditional loads, normative duplication and reference-hop depth;
- a descriptor/semantic equivalence assessment against the frozen R029 transverse evaluation descriptions sufficient to decide whether repeating the historical 36 Codex trials is materially required.

A deterministic measurement helper may be added under `tools/` when needed. If added, it is part of the Stage 5 candidate and MUST NOT be first-pass materialized by the Executor during Stage 6.

### 6. Burden measurement method

Post-materialization qualification records at least:

- `root_bytes`: UTF-8 bytes of materialized `AGENTS.md`; compare against the pre-materialization baseline `34567` bytes without treating size reduction as sufficient for PASS;
- `initial_catalog_bytes`: UTF-8 bytes of the name+description metadata exposed for the Maintainer plus five transverse production Skills; record per-Skill and total burden;
- `representative_conditional_bytes`: for frozen representative task classes, sum the exact root + selected Skill/reference text needed to reach controlling context; record route and loaded paths so results are reproducible;
- `normative_duplication`: identify materially duplicated normative obligations across root/domain/transverse/adapters by stable normalized rule IDs or an equivalent reviewable method; semantic references do not count as duplicated normative ownership;
- `reference_hop_depth`: maximum and representative hop count from root trigger/domain entry to the controlling policy/reference for frozen representative cases.

No numeric optimization threshold is invented by this task where D082/S10 did not adopt one. Qualification requires preservation plus evidence that progressive disclosure is real and does not introduce hidden authority/routing defects.

### 7. Provider/model evidence reuse rule

The historical R029 E2 Codex transverse result (`36/36 PASS`, zero route mismatch, zero authority/safety violations) is regression evidence, not a ceremony requirement.

Before any repeat provider/model run, Stage 5/Stage 7 MUST classify whether the materialized production Skill names/descriptions changed the scored semantic trigger/anti-trigger contract materially relative to the frozen R029 evaluation surface.

- materially equivalent descriptors/semantics -> preserve prior evidence; do not repeat 36 trials solely because files were materialized;
- material semantic/description change affecting routing -> fresh targeted/full provider evidence may be required under explicit authority before qualification can close;
- ChatGPT/Codex parity remains `NOT_ESTABLISHED` regardless unless separately evaluated under new authority.

## Plan & Trace / D080 execution units

| Unit | Scope | Prerequisites | Required durable output | Completion gate | Next-unit condition |
| --- | --- | --- | --- | --- | --- |
| `E1` | Freeze controlling authority, Task Contract, exact D082 design and writable frontier | Bootstrap matches `develop@758b92cf...`, O321, D067/D082/D068/D061/D080 and required R029 evidence | this T067 on verified topic branch `refactor/r029-d082-materialization` | branch exists at intended base; T067 contains complete Design/Plan/Trace and no Stage 5 product mutation has begun | only `E2` may begin |
| `E2` | D068 Stage 5 complete candidate materialization by ChatGPT | E1 complete; branch freshness revalidated before writes | coherent candidate containing lean root, Maintainer package/routes, five transverse packages, subordinate workspace-isolation reference, conformance/qualification assets and updated T067 published-candidate freeze | 79/79 mapping represented; topology mechanically coherent; semantic oracle/assets frozen; burden instrumentation present; descriptor-equivalence disposition recorded; exact candidate HEAD pushed/verified | only `E3` may begin |
| `E3` | D068 Stage 6 execution, diagnosis, bounded repair, Code Review & Verify by Executor | E2 published freeze; Human-visible D055 launch profile selected; exact candidate branch/HEAD/base supplied through thin transport | final remote branch plus `handoffs/T067-executor-handoff.json` and required deterministic/eval/measurement evidence | Executor verifies exact initial candidate, completes technical review/tests/evals/measurements, performs only bounded repairs, satisfies D076 audit, pushes final state; or returns BLOCKED/PARTIAL for re-entry | DONE path permits `E4`; blocker re-enters earliest affected stage |
| `E4` | ChatGPT Stage 7 convergence, post-materialization qualification, acceptance/integration | E3 durable handoff and remote HEAD verified | persisted qualification disposition, accepted/rejected residuals, PR/integration state and successor checkpoint | every D082 materialization condition classified with evidence; Maintainer activation/anti-trigger qualified or explicitly unresolved; burden metrics recorded; parity residual preserved; no authority/topology contradiction; accepted PR may integrate to `develop` | close objective or fail closed into explicit decision/SDD re-entry |

Later units MUST NOT begin if an earlier completion gate is unsatisfied. This is one Human objective split into ordered executions, not four separate objectives.

## Stage ownership and candidate boundary

```text
Stages 1-4  Explore / Specify / Design / Plan & Trace
            -> ChatGPT Orchestrator
Stage 5     Complete candidate materialization
            -> ChatGPT Orchestrator
Stage 6     Execute / diagnose / bounded repair / verify
            -> Agente de IA Ejecutor
Stage 7     Converge / accept / integrate / evolve
            -> ChatGPT Orchestrator
```

This task is D068-governed. The Executor MUST NOT reconstruct or first-pass materialize the adopted architecture during Stage 6.

## Published candidate freeze

Current E1 state:

```text
candidate_branch: refactor/r029-d082-materialization
candidate_head:   NOT_PUBLISHED_E1
candidate_base:   758b92cf38af9bc06e4717b1206dafb8e5d82e9e
```

E2 MUST replace `NOT_PUBLISHED_E1` with the exact verified Stage 5 candidate HEAD before E3 launch. A different initial candidate HEAD requires Orchestrator re-entry and durable update.

## Authorized Stage 6 scope

After E2 publishes the exact candidate, the Executor may:

- establish the exact candidate/base/branch state;
- execute deterministic tests/evals/measurement tooling already present in the candidate;
- inspect Skill/root/reference topology and perform technical Code Review & Verify;
- diagnose failures inside the approved D082 architecture and this Design;
- make bounded non-Markdown technical repairs that do not change adopted topology, semantic trigger/anti-trigger meaning, authority, acceptance meaning or Orchestrator-owned semantic oracle meaning;
- add supplementary technical verification inside the approved semantics when it does not become substantial first-pass executable material;
- persist `handoffs/T067-executor-handoff.json` and permitted technical evidence.

## Explicit exclusions

The Executor MUST NOT:

- edit committed Markdown;
- rewrite `AGENTS.md`, any `SKILL.md`, Maintainer route Markdown, this Task Contract, D082, R029 evidence or acceptance semantics;
- add/remove/split/merge top-level Skills;
- promote workspace isolation to a top-level Skill;
- alter the 79-unit semantic mapping or weaken an Orchestrator-owned activation/anti-trigger oracle to obtain green results;
- relabel ChatGPT/Codex parity as established;
- decide to rerun or waive provider/model evidence by itself;
- launch or modify T066;
- create a substantial new harness/controller/script/fixture/oracle required for first-pass qualification; D076 requires Stage 5 re-entry instead.

## Invariants / constraints

- Exactly `79/79` S1 semantic units must remain represented; zero delete-without-replacement units.
- Every ROOT/ROOT+ROUTE obligation needed before routing remains in `AGENTS.md`.
- There is exactly one project-owned top-level Maintainer domain Skill with internal Orchestrator/Executor routes.
- There are exactly five D082 transverse top-level Skills, neither fewer nor more.
- `workspace-isolation` is subordinate to `executor-launch-handoff` and depends on repository change-control/local policy for repository semantics.
- Skill activation cannot be a prerequisite for deterministic correctness, bootstrap safety or authority.
- Consumer Governance remains distinct from source-maintenance activation.
- Repository/domain policy outranks generic/transverse defaults and host adapters.
- No host identity creates authority or justifies semantic Skill splitting by itself.
- The canonical writable branch for T067 is `refactor/r029-d082-materialization`; no T067 content mutation may target `develop` or `main` directly.

## D076 executable-materialization boundary

```text
small mechanical execution aid
    -> Stage 6 may create/use it

substantial new controller/harness/script/fixture-oracle implementation
    -> STOP
    -> ChatGPT Orchestrator Stage 5 re-entry
```

The T067 handoff MUST contain the normal D076 `ephemeral_artifacts` audit, including an explicit empty array when none exist.

## Acceptance criteria

- **AC-T067-1 — Preservation:** all 79 S1 units are traceably represented with `ROOT=39`, `ROOT+ROUTE=20`, `ROUTE=20`, uncovered `0`, and no pre-routing authority/safety obligation depends on Skill activation.
- **AC-T067-2 — Topology:** one Maintainer top-level domain Skill with two internal role routes and exactly five transverse top-level Skills are materialized; workspace isolation is internal to executor-launch-handoff.
- **AC-T067-3 — Activation:** production Maintainer activation/anti-trigger cases demonstrate source-maintenance activation and reject ordinary consumer governance; transverse Skills preserve their S4-S8 positive/negative/near-miss boundaries and authority deferral.
- **AC-T067-4 — Cold start:** cold Orchestrator and authorized cold Executor bootstrap remain reconstructable from canonical Git without prior chat or Skill activation; stale/mismatched authority fails closed.
- **AC-T067-5 — Progressive disclosure:** actual `root_bytes`, `initial_catalog_bytes`, representative conditional context load, normative duplication and reference-hop depth are measured and reviewable; context reduction cannot compensate for semantic loss.
- **AC-T067-6 — Deterministic qualification:** repository-owned deterministic conformance/measurement assets execute without model-driven Skill activation and validate topology/coverage/no-Skill invariants.
- **AC-T067-7 — Residual integrity:** ChatGPT/Codex empirical parity remains explicitly `NOT_ESTABLISHED`; Maintainer historical `21/36` remains unscored history and is replaced only by production-specific qualification evidence, not relabeling.
- **AC-T067-8 — Evidence economy:** the prior 36 Codex transverse trials are not repeated merely because of materialization; rerun occurs only if the production descriptor/semantic equivalence check identifies a material routing change or new controlling authority requires it.
- **AC-T067-9 — Stage boundary:** E2 is complete ChatGPT Stage 5 materialization; E3 is Executor Stage 6 verification/bounded repair only; E4 is ChatGPT Stage 7 acceptance/integration.
- **AC-T067-10 — Isolation:** T066 remains unchanged and not started.

## Verification and trace requirements

Stage 6 evidence MUST include, at minimum:

- deterministic 79-unit preservation/topology checks;
- syntax/structure checks for all production Skill packages and references;
- activation/anti-trigger oracle execution or equivalent deterministic evaluation of the frozen production corpus;
- cold-start/no-Skill structural checks;
- execution of burden measurement tooling with persisted results;
- verification that workspace isolation is not discoverable as a sixth top-level production Skill;
- review of normative duplication and reference-hop outputs for reproducibility;
- descriptor/semantic equivalence result governing whether fresh provider/model trials are required;
- normal repository test/lint/conformance suite affected by these instruction/Skill changes.

Orchestrator-owned semantic conformance assets are the 79-unit mapping, adopted topology assertions, activation/anti-trigger expected classifications and D082 residual expectations. Executor supplementary technical tests may strengthen verification but may not change those semantics.

## Code Review & Verify obligations

Before `DONE`, the Executor MUST review the final implementation anchor against D082 and this Task Contract for:

- requirement/design fidelity and all PRESERVED invariants;
- missing/duplicated authority and incorrect route ownership;
- false-positive/false-negative activation risks represented by the frozen corpus;
- hidden dependency on Skill activation for correctness;
- accidental sixth capability or role/host split;
- stale/incorrect references and unreachable routed policy;
- measurement reproducibility;
- unauthorized scope additions;
- D076 compliance.

Technical findings inside the bounded repair envelope may be corrected and affected verification rerun. Any semantic/topology/authority finding requires upstream re-entry.

## Stop / escalation / SDD re-entry conditions

STOP rather than guess when any of the following occurs:

- candidate/base/branch identity cannot be established safely;
- an S1 semantic unit lacks an unambiguous preserved destination;
- slimming `AGENTS.md` would make authority, ownership, safety, fail-closed behavior or cold-start correctness conditional on Skill activation;
- a transverse trigger cannot be separated from Maintainer/domain authority without hidden policy invention;
- Maintainer/source versus consumer activation remains materially ambiguous after applying the adopted contract;
- workspace isolation appears to require a sixth top-level Skill to work correctly;
- production routing semantics materially contradict the evidence that supported D082;
- the descriptor-equivalence review determines that old 36-trial evidence no longer applies and fresh provider/model evidence is required but not separately authorized/available;
- a semantic oracle appears defective;
- Stage 6 requires substantial missing executable qualification material under D076;
- any repair would change D082 architecture, this Design, acceptance meaning or Orchestrator-owned semantics;
- T066 would need to be touched to complete T067.

Persist available evidence and identify the earliest affected SDD/decision stage before returning control.

## Expected handoff / evidence

Stage 6 MUST persist:

```text
handoffs/T067-executor-handoff.json
```

The handoff must satisfy `docs/EXECUTOR-HANDOFFS.md`, including `sdd_profile`, implementation/review SHA anchors, requirement trace, verification commands/results/runtime, findings, upstream re-entry fields and D076 `ephemeral_artifacts`.

Additional non-Markdown measurement/eval evidence may be persisted under the Stage 5-authorized qualification directories when their schemas/paths are already part of the candidate.

## Terminal return shape

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T067-executor-handoff.json
BRANCH: refactor/r029-d082-materialization
HEAD: <actual remote pushed HEAD>
```

## Human launch gate

```text
launch_state: NOT_AUTHORIZED
```

E1 does not authorize Executor launch. E2 must first publish/freeze the complete candidate and then ChatGPT must present the D055 concrete Executor/session/model/effort launch profile and thin transport to the Human.

## Thin transport invariant

The future Human-visible Executor prompt is transport only. It may identify the canonical repository, session mode/coordinator identity when required, this Task Contract and the exact authorized candidate branch@HEAD. It MUST NOT duplicate the Design, acceptance criteria, test commands, repair rules, evidence schema or stop conditions already persisted here.