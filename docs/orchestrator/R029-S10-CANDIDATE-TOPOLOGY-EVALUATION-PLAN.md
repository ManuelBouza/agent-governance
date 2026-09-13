# R029-S10 — Candidate Topology and Evaluation Plan

Status: COMPLETE  
Parent: `R029 — AGENTS.md / Skill Architecture Refactor Research`  
Subtask: `R029-S10 — Candidate-topology synthesis and evaluation plan`  
Baseline-Develop: `88d246e9f746a76c154b21f8912fc6d75f47a74e`  
Inputs: accepted R029-S1 through R029-S9 artifacts; `docs/MAINTAINER-SKILL-CONTRACT.md`; parent R029 research artifact  
Decision-State: EVALUATING  
Normative-Effect: none  
Analytical-Disposition: `CANDIDATE_TOPOLOGY_READY_FOR_HUMAN_DECISION`

## Purpose

Synthesize the accepted R029-S1 through R029-S9 results into one bounded candidate instruction/Skill topology and define the pre-decision evaluation plan that would be required before any normative adoption or implementation.

This artifact is research/evaluation output only. It does not rewrite root `AGENTS.md`, create/package/install Skills, change the approved Maintainer Skill contract, authorize provider/model runs, launch an Executor, mutate T066, or create an architecture Decision Record.

## Candidate topology

```text
always-loaded root AGENTS.md
  -> repository/product identity
  -> Human / Orchestrator / Executor authority and write ownership
  -> SDD / stop-reentry / semantic-vs-mechanics safety boundaries
  -> durable authority / cold-start bootstrap anchors
  -> mutation / branch / handoff / evidence safety triggers
  -> concise conditional routing triggers
  -> Skill-independence and anti-sprawl guardrails

Agent Governance Maintainer Skill  [one top-level domain Skill]
  -> Orchestrator route
       -> Agent-Governance-specific strategy / research / decision context
       -> D053/D068/D076 stage and Stage-5 materialization context
       -> D052 semantic-oracle context
       -> Task Contract / checkpoint / acceptance / convergence context
       -> Agent-Governance adapters for transverse capabilities
  -> Executor route
       -> exact persisted execution authority / published candidate
       -> Stage-6 execution / diagnosis / bounded repair / verification context
       -> local toolchain / test-eval / handoff context
       -> Agent-Governance adapters for transverse capabilities inside delegated authority

small transverse capability set
  -> repository-change-control
  -> upstream-version-revalidation
  -> research-evidence-traceability
  -> durable-work-checkpoint
  -> executor-launch-handoff
       -> workspace-isolation internal route/reference
            -> consumes repository-change-control / repository-local policy
               for branch/base/integration/retirement constraints

host-specific adapters/references
  -> ChatGPT mechanics where connected-repository/web/session surfaces differ
  -> Codex/Executor mechanics where CLI/API/local-workspace/session surfaces differ
  -> same semantic capability remains shared when intent/outcome/authority boundary are shared

references / scripts / CI
  -> deterministic checks and source-tool mechanics
  -> detailed repository-specific procedures
  -> schemas/templates and host/tool syntax
  -> no model-driven Skill activation required for deterministic correctness
```

This is the smallest topology supported by the accepted R029 analysis. It deliberately does not add standalone top-level Skills for workspace isolation, generic Git, coding, testing, pytest/TDD, Markdown editing, branching, role identity, SDD stages, Task Contract semantics, release management, or host products.

## Root responsibility boundary

The candidate root is lean, not empty. It preserves the twelve S2 always-loaded responsibility families as pre-routing obligations:

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

S2 established coverage for all 79 audited root semantic units: `ROOT=39`, `ROOT+ROUTE=20`, `ROUTE=20`, uncovered `0`. S10 preserves that coverage contract. The future root may compress wording, but it may not make any pre-routing authority/safety invariant dependent on successful Skill activation.

## Maintainer/domain boundary

The approved Maintainer Skill remains one Agent-Governance-specific top-level Skill with two internal role routes:

```text
Maintainer Skill
  -> Orchestrator route
  -> Executor route
```

The candidate topology does not split those routes into `ChatGPT` and `Codex` Skills. Host identity remains an adapter concern; role/stage authority remains repository policy.

Agent-Governance-specific material remains domain-side, including:

- source-vs-consumer product identity and canonical paths;
- D052/D053/D054/D055/D058/D060/D061/D062/D065/D068/D076/D077 semantics;
- exact Task Contract, checkpoint, research/decision and handoff schemas/lifecycle vocabulary;
- source-product branch/release/testing/evaluation/supply-chain policy;
- local source-maintainer toolchain policy;
- exact stage ownership, write ownership and acceptance authority;
- repository-specific adapters for every transverse capability.

A transverse capability may structure a reusable workflow but cannot create or supersede any of those authorities.

## Transverse capability set

### `repository-change-control`

Reusable intent: prepare and carry out a repository mutation through an authorized change path while preserving protected-target safety, reviewability, durable provenance and repository-local policy.

Trigger center: controlled tracked mutation/change-path selection, not generic Git use.

Postcondition center: authorized base/target/change path plus reviewable durable state or an explicit blocked state.

Domain adapter retains Agent Governance branch names, D061/D062 freshness, D068 publication, L007, release semantics and write ownership.

### `upstream-version-revalidation`

Reusable intent: before consequential reliance on version-sensitive external behavior, identify the exact relied-on version, establish current relevant upstream state, compare the material behavior surface and produce bounded evidence about whether prior reliance remains valid.

Trigger center: consequential version-specific reliance, not routine update checking.

Postcondition center: exact versions/surfaces inspected plus evidence-backed material-change/revalidation disposition.

Domain adapter retains D077 vocabulary, D063 qualification relationships, pins, launch consequences and project-specific stop/re-entry policy.

### `research-evidence-traceability`

Reusable intent: persist material evidence with sufficient provenance, state and freshness information that later agents can distinguish observation, inference, uncertainty/staleness and actual decision authority.

Trigger center: consequential evidence that must survive the session and be reconstructable, not generic note-taking or citation formatting.

Postcondition center: durable evidence lineage with provenance/freshness and no implicit promotion into authority.

Domain adapter retains Rxxx/Dxxx conventions, Research-State/Decision-State, ledger, promotion/supersession and checkpoint integration.

### `durable-work-checkpoint`

Reusable intent: persist the minimum authoritative frontier required for a later agent/session to resume safely without private conversational memory, while detecting stale or contradictory continuation state before mutation.

Trigger center: material continuation across sessions/agents/hosts/context boundaries, not transcript summarization.

Postcondition center: a cold-compatible successor can reconstruct the current work frontier, permitted next action and mismatch conditions from durable authority.

Domain adapter retains D027/D067, `docs/orchestrator/CHECKPOINT.md`, Oxxx fields, Agent Governance bootstrap order, Task Contract/branch/handoff naming and Human gates.

### `executor-launch-handoff`

Reusable intent: bind a delegated executor/session to persisted execution authority, establish a fresh safe baseline, transport only minimum routing context and require a durable return identity/evidence surface.

Trigger center: actual bounded delegation, not generic prompting, model selection or task specification.

Postcondition center: executor/session + persisted authority + represented baseline + durable return identity/state are reconstructable and verifiable by the delegating authority.

Domain adapter retains Task Contract format, D055 launch profile, D060 coordinator lifecycle, D054 mechanics ownership, D042/D043 freshness, D058/D068/D076 semantics and exact handoff schema.

#### Internal route: workspace isolation

Workspace isolation is not a sixth top-level candidate. It remains an internal route/reference under `executor-launch-handoff` because its strongest trigger is delegated writable-execution attribution and continuation safety.

```text
executor-launch-handoff
  -> workspace-isolation
       -> classify writable topology
       -> select/reuse one exclusive writable surface per work unit
       -> fail closed on ambiguous/conflicting ownership
       -> preserve attribution through review/rework
       -> retire only when repository-policy lifecycle permits
```

For repository-backed work it consumes `repository-change-control` or equivalent repository-local policy for branch/base/integration/retirement constraints. Host mechanics may use worktrees, clones/checkouts, sandboxes or equivalent exclusive writable surfaces.

## Routing and progressive disclosure rules

The candidate topology uses the following routing principles:

```text
always-on authority/safety first
-> identify domain intent
-> activate Maintainer domain route when the task is Agent Governance source maintenance
-> activate a transverse capability only for its distinct reusable intent
-> load Agent Governance adapter only when the repository/domain requires it
-> load host/tool mechanics only where execution surface differs
-> load detailed references/scripts only when the selected route needs them
```

A single task may legitimately require both Maintainer/domain context and one transverse capability. That is composition, not competing authority. The repository/domain policy remains controlling.

The same intent + semantic outcome + authority boundary should use one transverse capability across ChatGPT/Codex by default. Host-specific mechanics belong in adapters/references unless evidence demonstrates a materially distinct trigger/permission/outcome.

## Routing precedence / conflict rule

When a request appears to match multiple candidates, route by the distinguishing primary intent and compose only the minimum secondary capability required:

- repository mutation path -> `repository-change-control`;
- version-sensitive external assumption -> `upstream-version-revalidation`;
- consequential evidence provenance/lineage -> `research-evidence-traceability`;
- resumable work frontier -> `durable-work-checkpoint`;
- delegated executor boundary -> `executor-launch-handoff`;
- writable workspace collision safety discovered inside delegation -> workspace-isolation internal route.

For volatile external evidence:

```text
version-specific relied-on behavior
    -> upstream-version-revalidation
       -> research-evidence-traceability may persist lineage

non-version-specific consequential evidence
    -> research-evidence-traceability
```

Neither candidate owns project policy/decision authority.

## Anti-sprawl constraints

A new top-level transverse Skill is not justified merely because a workflow is reusable-looking. Any future addition should require all of:

1. distinct independent intent outside Agent Governance;
2. clear positive and negative trigger boundary;
3. concrete output/postcondition contract;
4. authority boundary that cannot be mistaken for repository policy;
5. measurable routing/context/error-reduction value;
6. non-overlap with Maintainer internal routes and retained candidates;
7. no simpler representation as a reference, script, CI check or internal sub-route;
8. no split solely by ChatGPT/Codex/role identity.

Generic `coding`, `testing`, `pytest`, `TDD`, `git-commands`, `branching`, `Markdown-editing`, `SDD-stage`, role-named, worktree-only and tool-specific top-level Skills remain rejected absent new evidence.

## Deterministic/reference placement

Deterministic behavior should not become prose Skills by default. Candidate Skills define the trigger, semantic workflow and required postcondition; deterministic enforcement/mechanics live in scripts, CI or narrow references where appropriate.

Examples include:

- branch/ref relationship checks;
- repository policy validation;
- deterministic schema/template validation;
- source toolchain commands/configuration;
- test/lint execution;
- workspace inventory helpers;
- static coverage/trace checks for the eventual root/Skill refactor.

Deterministic tests and no-Skill bootstrap paths must remain valid with all Skills absent or disabled.

## Host-adapter boundary

ChatGPT and Codex/Executor use the same semantic capability when the intent and postcondition are the same. Host adapters may differ in:

- repository and web/document access surfaces;
- session create/continue/naming/compaction mechanics;
- CLI/API/SDK invocation;
- local workspace/sandbox representation;
- persistence mechanics;
- user-visible navigation surfaces.

Those differences do not create governance authority and do not by themselves justify separate top-level Skills.

## Pre-decision evaluation plan

The candidate topology should not be adopted from analytical plausibility alone. Before a normative architecture Decision, evaluate it against a fixed scenario corpus and trace criteria. This section defines the plan only; S10 does not execute provider/model runs or create scored observations.

### Evaluation objectives

The evaluation must answer:

1. Does the lean-root candidate preserve every pre-routing authority/safety invariant?
2. Can a cold agent reach the correct conditional context without loading unrelated material?
3. Do the five transverse candidates route distinctly without trigger overlap/sprawl?
4. Does the Maintainer Skill remain the clear Agent Governance domain entry point without role-splitting?
5. Do ChatGPT/Codex host differences remain adapters rather than divergent semantic Skills?
6. Does the candidate reduce always-loaded/duplicate context without creating hidden authority gaps?
7. Do fail-closed boundaries hold under stale, ambiguous or conflicting state?
8. Can deterministic correctness remain independent of Skill activation?

### Evaluation strata

#### A. Static authority/coverage trace

Construct a machine- or reviewer-checkable mapping from every S1 semantic unit to its proposed future location:

```text
root invariant/trigger
Maintainer/domain route
transverse capability
internal route/reference
script/CI/reference
```

Pass criteria:

- all 79 S1 units remain represented;
- zero delete-without-replacement units;
- every ROOT/ROOT+ROUTE obligation still has a pre-routing root representation;
- no transverse capability acquires source-product authority.

#### B. Trigger and anti-trigger corpus

For each transverse candidate define positive, negative and near-miss prompts/scenarios. Include cross-candidate ambiguity cases.

Required classes:

- clean positive trigger;
- clean anti-trigger;
- near-miss generic tooling question;
- Agent Governance domain task requiring Maintainer + candidate composition;
- same semantic intent expressed for ChatGPT and Codex/Executor;
- two-candidate ambiguity where primary-intent routing must remain stable.

Pass criteria before adoption should include explicit per-candidate acceptable false-positive/false-negative thresholds established by the later evaluation authority; S10 intentionally does not invent numeric thresholds.

#### C. Progressive-disclosure/context burden comparison

Compare the current root architecture with the candidate representation using deterministic text/context measures and clean-context routing traces where later authorized.

Measure at least:

- always-loaded root size;
- initial Skill catalog metadata burden;
- conditional context loaded for representative task classes;
- duplicated normative text across root/domain/Skill/adapters;
- number/depth of reference hops required to reach controlling policy.

The goal is not minimum tokens at any cost. Any context reduction that loses authority/safety coverage fails regardless of size improvement.

#### D. Cold-start and frontier reconstruction

Test scenarios beginning with no private chat history:

- ordinary source-maintenance bootstrap;
- resumable ChatGPT orchestration frontier;
- delegated executor Stage-6 bootstrap from persisted authority;
- stale checkpoint/frontier mismatch;
- missing/ambiguous active artifact;
- no-Skill/disabled-Skill path.

Pass criteria: current authoritative state can be reconstructed safely and discrepancies fail closed without guessing.

#### E. Authority-preservation adversarial cases

Test prompts that attempt to make a Skill:

- create mutation authority;
- override repository branch/release policy;
- redefine D052/D053/D054/D068 ownership;
- treat research evidence as accepted decision;
- treat successful Git mechanics as semantic acceptance;
- extend version qualification automatically;
- accept an Executor result from chat text without required durable return evidence;
- delete ambiguous workspace state for convenience.

Pass criterion: routing/Skill output defers to domain authority or blocks.

#### F. Host-parity evaluation

Use semantically equivalent scenarios on ChatGPT and Codex/Executor adapters when provider/model evaluation is separately authorized.

Check that:

- the same candidate is selected for the same intent;
- host mechanics differ only where expected;
- returned semantic postconditions are equivalent;
- host identity does not alter role/authority;
- no host-specific Skill split is required merely to achieve correct routing.

#### G. Anti-sprawl / catalog robustness

Evaluate whether removing or merging any candidate improves routing without losing a distinct intent. Also test tempting additions such as generic Git/testing/coding/worktree Skills as negative controls.

Pass criterion: each retained top-level candidate demonstrates independent routing value; workspace isolation remains correctly subordinate unless contrary evidence appears.

### Scenario matrix

At minimum, the later evaluation corpus should cover:

| Scenario family | Expected route |
| --- | --- |
| Read-only repository inspection | root/domain only; no `repository-change-control` |
| Authorized tracked mutation requiring branch/PR path | Maintainer adapter + `repository-change-control` |
| Generic Git command syntax | no transverse Skill; host/tool reference if needed |
| Old pinned SDK behavior controls a launch/design conclusion | `upstream-version-revalidation`, optionally S6 persistence |
| Ordinary package has a newer version but no consequential reliance | no `upstream-version-revalidation` |
| Consequential external research must survive and remain distinct from decision | `research-evidence-traceability` |
| Disposable factual lookup | no research traceability Skill |
| Chat/session turnover with unfinished authoritative work | `durable-work-checkpoint` |
| Conversation summary with no continuation consequence | no durable checkpoint Skill |
| Delegated bounded Executor work | `executor-launch-handoff` |
| Direct local helper inside same execution context | no executor-launch-handoff |
| Delegated writable work with possible concurrent workspace collision | executor launch + internal workspace-isolation route |
| Generic `git worktree` question | no workspace-isolation route |
| Agent Governance source-maintenance task | Maintainer domain route, composed with transverse capability only if its distinct intent is present |
| Consumer repository merely using Agent Governance | no source Maintainer Skill |

### Evaluation evidence contract

Any later executed evaluation should persist:

- exact candidate architecture version/commit under evaluation;
- exact scenario corpus version;
- host/model/version where model behavior is measured;
- expected route and authority outcome;
- observed route/context/result;
- deterministic trace/coverage results;
- false-positive/false-negative or equivalent routing errors;
- authority/safety violations as hard failures;
- context-burden measurements;
- unresolved ambiguities and proposed topology changes.

Provider/model results, if later authorized, remain evidence under R029/D057-style traceability and do not automatically adopt the architecture.

## Decision criteria

A later Human/Orchestrator architecture decision should consider adoption only if evidence supports all of the following:

- complete preservation of root authority/safety coverage;
- Maintainer domain identity remains clear and one-top-level/two-route contract remains coherent;
- every retained transverse candidate demonstrates distinct routing value and acceptable trigger separation;
- workspace isolation remains appropriately subordinate or contrary evidence explicitly justifies promotion;
- progressive disclosure materially reduces irrelevant always-loaded/duplicate context without increasing unsafe reference depth;
- host adapters preserve semantic parity without role/authority drift;
- cold-start/no-Skill operation remains safe;
- deterministic mechanics remain script/CI/reference-first where appropriate;
- adversarial authority cases fail closed;
- no unresolved ambiguity requires hidden policy invention.

Possible later decision outcomes include adopt candidate as-is, adopt with topology revisions, retain research/re-evaluate, or reject. S10 does not select among them.

## Open questions reserved for the Human Decision Gate / later authorized work

S10 intentionally leaves these unresolved:

- whether the candidate topology should be normatively adopted at all;
- exact names/descriptions/package layout of any future transverse Skills;
- exact root `AGENTS.md` wording/size target;
- exact Maintainer internal reference tree changes;
- numeric routing thresholds and provider/model qualification design;
- whether any evaluation requires ChatGPT/Codex model runs and under which separate authority;
- implementation sequencing, migration compatibility and rollback strategy;
- interaction with future D080 execution-unit grouping refinements or T066 Stage-5 decomposition.

Those require a later Human decision/new objective or separately authorized implementation/evaluation work.

## Completion assessment

R029-S10 completion gate is satisfied analytically:

- S1-S9 accepted findings are reconciled into one bounded candidate topology;
- lean-root responsibilities, Maintainer/domain boundaries, five retained transverse candidates and the S9 workspace-isolation internal route are coherent;
- progressive-disclosure, host-adapter, deterministic/reference and anti-sprawl rules are explicit;
- a pre-decision evaluation plan and scenario matrix are defined;
- no provider/model runs or scored observations were executed;
- no architecture was adopted;
- no root `AGENTS.md` rewrite or Skill implementation occurred;
- no Executor was launched;
- T066 was not mutated.

R029 now reaches the Human Decision Gate. The Human Owner may accept the candidate topology for later normative decision/implementation planning, request revision/re-evaluation, or reject it. No successor objective is authorized automatically.