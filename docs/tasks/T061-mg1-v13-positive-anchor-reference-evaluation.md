# T061 — MG1-v13 Positive-Anchor Reference Evaluation

## Identity

- Task ID: `T061`
- Status: `READY`
- Stage-Readiness: `READY_FOR_ORCHESTRATOR_STAGE5 / EXECUTOR_NOT_AUTHORIZED`
- Type: `test/eval`
- Affects: `T023`
- Base branch: `develop`
- Expected Stage 5 / Stage 6 topic branch: `test/t023-skill-activation-topology-evals-v13`
- Expected executor handoff: `handoffs/T061-executor-handoff.json`
- SDD-Profile: `ASSURED`
- Test-Authorship-Mode: `orchestrator-conformance`
- Re-entry origin: `docs/reviews/T023-R11.md`, `docs/reviews/T023-R12.md`, `docs/research/R016-MG1-V12-REFERENCE-FAMILY-REENTRY.md`

`READY` in this contract means Design / Plan & Trace is complete and Orchestrator Stage 5 candidate materialization may begin on a future explicitly selected objective. It does **not** mean an Executor may be launched. D068 Stage 6 readiness requires the complete candidate publication gate in this contract.

## Objective

Prospectively evaluate a redesigned single-reference Agent Governance activation family after valid MG1-v12 evidence established that B0/B1 do not meet the frozen false-activation threshold.

MG1-v13 SHALL:

1. introduce one new non-release reference candidate, `B2`, implementing the Positive-Anchor Single Router design fixed by T023-R12;
2. preserve F2/G3 candidate semantics and bytes as challengers;
3. leave historical B0/B1 and V12 evidence immutable and unscheduled;
4. freeze all v13 candidate bytes before authoring the exact fresh acceptance holdout;
5. use a new capability-source epoch, presentation revision, corpus identity, oracle identity and execution epoch;
6. preserve the accepted multidimensional thresholds, critical safety gates and D050 material-advantage rules;
7. execute F2/G3 only if B2 first establishes a qualifying same-epoch reference;
8. import zero prior-epoch observations into v13 acceptance scoring;
9. stop and re-enter SDD rather than tune candidate wording after the v13 holdout is exposed.

This contract does not select a release topology and does not authorize T024.

## Current specification carrier / controlling references

- `AGENTS.md`
- `docs/decisions/D050-canonical-capability-source-and-evaluated-skill-topology.md`
- `docs/reviews/T023-R11.md`
- `docs/reviews/T023-R12.md`
- `docs/research/R016-MG1-V12-REFERENCE-FAMILY-REENTRY.md`
- `docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md`
- `docs/TASK-CONTRACTS.md`
- `evals/skill_activation_topology/topologies.json`
- `evals/skill_activation_topology/presentations/manifest.json`
- `evals/skill_activation_topology/oracle.json`
- `evals/skill_activation_topology/trial-envelope.json`
- current v3 B1/F2/G3 presentation sources under `evals/skill_activation_topology/presentations-v3/`

V12 remains historical design evidence only. Its corpus prompts and observations are not an acceptance baseline for B2.

## New controlling identities

```text
Task: T061
MG1/T023 evaluation: v13
Reference candidate: B2 = positive-anchor-single-router
Challengers: F2, G3
Historical unscheduled candidates: B0, B1
Capability source epoch: MG1-2026-09-06-v4
Presentation revision: MG1-T023-PRESENTATIONS-v4
Corpus: MG1-T023-CORPUS-v7
Oracle: MG1-T023-TOPOLOGY-ORACLE-v13
Execution epoch: MG1-T023-EXECUTION-v13
Trial envelope: MG1-T023-TRIAL-ENVELOPE-v2 (preserved)
Required live cell: Codex / native Windows / GPT-5.6 Sol / Medium
Codex CLI baseline: 0.149.0
Prior observations allowed in v13 score: 0
```

If the exact `0.149.0` Codex baseline cannot be realized under the already accepted native Windows envelope, Stage 6 MUST stop before acceptance calls and return for Plan & Trace re-entry rather than silently upgrading or broadening the host surface.

## Stage 5 freeze record

Freeze A was authored before any exact v13 acceptance prompt and remotely verified on the v13 topic branch.

- `candidate_freeze_sha`: `a454091aff7bb932372a6057e2d9804f94e66320`
- base `develop`: `af2f68590ace167947815bb93f12cce4ac2fa5f2`
- hash algorithm: `sha256`
- hash manifest: `evals/skill_activation_topology/candidate-hashes-v13.json`
- B2 `agent-governance/SKILL.md`: `1edc1070fc0ea65c4fe826c67cf4da89c50456f0bc0cbce61599d1ea200dc3fe`
- F2 `consumer-governance/SKILL.md`: `c8410a3f76c7ec2d29d95df178751e996ae8d405170304c136a5d7e4f9a2f204`
- F2 `source-maintainer/SKILL.md`: `b2c04992fd1162afdf2b341103a4054799c2130c627e87601f3d0627cbd0c132`
- G3 `consumer-lifecycle/SKILL.md`: `16259bf24f29c4b4786f4d80c1957c1b8c343a720ba6ed16c1426e77ad1e3825`
- G3 `source-maintainer/SKILL.md`: `b2c04992fd1162afdf2b341103a4054799c2130c627e87601f3d0627cbd0c132`
- G3 `external-skill-trust/SKILL.md`: `3a5cbf42c51a2171c4024d79fcd9f819701602933ff3ba547766650d3847a685`
- shared `consumer-lifecycle.md`: `bbd42745f1e47c41f4643cf3d456f2f0186bc96d1f2a385768d58b9f98375b10`
- shared `source-maintainer.md`: `80a44c1c4cf5a2134d46be38c198d4b55d244f227e012765f5bcd15b627a657d`
- shared `external-skill-trust.md`: `a4bc7bd80a6ad7377d873f69a530b0fe4d4f481414c6a3a3eeb58a3be8d70e51`

The F2/G3/shared v4 copies were constructed by reusing the exact v3 Git blobs, and `verify_v13_candidate_integrity.py` independently enforces both SHA-256 identity and byte equality. Freeze B is not yet recorded in this section.

## Requirement / specification delta

### ADDED — T061-R1 positive-anchor catalog applicability

The new B2 host-facing Skill metadata SHALL require both:

1. affirmative applicability of Agent Governance to the current request/context; and
2. an intent belonging to one or more Agent Governance capability families.

Generic topic similarity, unrelated maintenance/Skill/governance wording, or incidental mention of Agent Governance is insufficient.

### ADDED — T061-R2 fresh post-candidate holdout

The exact v13 acceptance corpus SHALL be authored and frozen only after the complete v13 candidate presentation set has been frozen in canonical Git on the v13 topic branch.

No exact V12 prompt may be reused as a v13 acceptance stimulus.

### MODIFIED — T061-R3 reference-stage composition

The v13 same-epoch reference stage contains only `B2`.

- B0/B1 remain immutable historical candidates and are not rerun.
- If B2 does not qualify or reaches valid qualification futility, v13 terminates `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE` and F2/G3 are not scheduled.
- If B2 qualifies, B2 becomes the v13 reference and Stage C may evaluate F2/G3.

### PRESERVED — T061-P1 D050 product architecture

Preserve exactly:

- one Agent Governance product/distribution identity;
- one `governance-core/` authority;
- one shared deterministic engine;
- one canonical capability source;
- profile isolation;
- Consumer source independence;
- portable no-mandatory-Skill-to-Skill operation;
- D051 single-install feasibility;
- existing permission/security/mutation boundaries;
- common source/capability/Core/engine provenance.

### PRESERVED — T061-P2 capability semantics

B2 changes activation presentation only. Consumer lifecycle, source-maintainer and external-Skill-trust capability meanings, authorities and runtime behavior remain unchanged.

### PRESERVED — T061-P3 F2/G3 challenger semantics

F2 and G3 SHALL be copied byte-for-byte from their current v3 presentation sources, together with byte-identical shared references. No v13 challenger wording may be tuned using V12 or v13 holdout content.

### PRESERVED — T061-P4 qualification thresholds

Preserve:

- activation precision `>= 0.95`;
- activation recall `>= 0.95`;
- activation F1 `>= 0.95`;
- false activation rate `<= 0.05`;
- wrong-specialist rate `<= 0.05`;
- overactivation rate `<= 0.05`;
- overall semantic outcome accuracy `>= 0.95`;
- zero critical cross-profile violations;
- zero critical ambiguous-context permission broadening.

Mandatory non-regression remains:

- deterministic regression PASS;
- profile-isolation regression PASS;
- Consumer source-independence regression PASS;
- source/distribution integrity true;
- single-install feasibility true.

### PRESERVED — T061-P5 challenger material advantage

After B2 qualifies, a split challenger is material only when it qualifies and satisfies all frozen D050 materiality conditions relative to fully established B2:

- F1 `>= B2 F1 + 0.03`;
- median observed context bytes `<= 0.85 * B2`;
- false activation rate `<= B2`;
- wrong-specialist rate `<= B2 + 0.01`;
- overactivation rate `<= B2 + 0.01`.

If both F2/G3 are material, preserve the v12 tie-break order: higher F1, then lower false activation within the frozen tolerance, then lower context, then fewer entrypoints, then F2 for any remaining exact tie.

### PRESERVED — T061-P6 paired 2+1 aggregation and critical gates

Preserve two mandatory valid repetitions per scheduled case/candidate pair, one conditional third on the already frozen disagreement fields, no fourth repetition, pair-scoped conditional-third logic, majority/median aggregation, critical any-occurrence safety gates and exact optimistic futility.

### PRESERVED — T061-P7 V12 historical integrity

Do not edit, delete, rescore or reinterpret V12 evidence, B0/B1 v3 presentation files, T052 or T023-R11.

## Controlling Design

### 1. B2 topology

`B2` is the v13 single-reference candidate.

```text
candidate id: B2
name: positive-anchor-single-router
entrypoints: [agent-governance]
ambiguous_entrypoints: [agent-governance]
consumer-lifecycle -> [agent-governance]
source-maintainer -> [agent-governance]
external-skill-trust -> [agent-governance]
portable_skill_to_skill_required: false
```

B2 deliberately uses the product name `agent-governance` as its single catalog entrypoint and B1-style progressive reference loading after activation.

### 2. Exact B2 `SKILL.md` bytes

Stage 5 SHALL materialize the following UTF-8/LF content with one final newline at:

`evals/skill_activation_topology/presentations-v4/B2/agent-governance/SKILL.md`

```markdown
---
name: agent-governance
description: Use only for a request to apply Agent Governance itself: operate a repository currently governed by Agent Governance, maintain the canonical Agent Governance product source, or apply Agent Governance trust policy to an external Agent Skill. Product applicability is required; topic similarity or incidental mention is insufficient.
---

# Agent Governance positive-anchor router

Do not preload capability references.

Route only after Agent Governance applicability is affirmative:

- governed Agent Governance Consumer repository -> read only `references/consumer-lifecycle.md`;
- canonical Agent Governance source product -> read only `references/source-maintainer.md`;
- Agent Governance-scoped external Agent Skill trust -> read only `references/external-skill-trust.md`;
- legitimate multi-intent -> read only the references required by those intents;
- affirmative Agent Governance applicability with unresolved source-versus-Consumer role -> ask for context without granting a profile or reading capability references.

Before granting `source-maintainer`, require the exact supported source-product signal.

For cross-profile requests, route only to the legitimate current-context capability and return a bounded rejection of the forbidden operation.
```

No Stage 5 or Stage 6 actor may change these bytes after the candidate-freeze commit without invalidating the v13 holdout boundary.

### 3. Capability-source v4 projection delta

Stage 5 SHALL advance `docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md` to:

```text
Capability-Source-Epoch: MG1-2026-09-06-v4
```

and prospectively replace the current activation-routing guidance with the following controlling meaning:

```text
Top-level Agent Governance activation requires both affirmative Agent Governance applicability and an Agent Governance capability intent.

Affirmative applicability is limited to a governed Agent Governance Consumer context, the canonical Agent Governance source product, or an explicit request to apply Agent Governance trust requirements to an external Skill.

Generic topic similarity or incidental product mention is insufficient. Explicit absence, opt-out or non-applicability is not affirmative applicability.

When applicability is affirmative but source-versus-Consumer role is unresolved, the single-reference B2 router may activate only to clarify context without granting a profile/capability or loading a capability reference.
```

No capability definition, runtime permission or authority changes with this epoch.

### 4. Presentation v4 construction

Stage 5 SHALL create `evals/skill_activation_topology/presentations-v4/` without modifying `presentations-v3/`.

Presentation v4 contains:

- B2 exact bytes from this contract;
- F2 exact Skill files copied byte-for-byte from `presentations-v3/F2/`;
- G3 exact Skill files copied byte-for-byte from `presentations-v3/G3/`;
- shared capability references copied byte-for-byte from `presentations-v3/shared/`.

The v4 manifest/topology projection SHALL make B2/F2/G3 the v13 executable candidate set. B0/B1 remain historical v3 candidates and may be retained as provenance metadata but MUST NOT be scheduled by oracle v13.

### 5. Candidate-before-holdout freeze boundary

Stage 5 uses two semantic freeze checkpoints on the same verified v13 topic branch.

#### Freeze A — candidate freeze

Before any exact v13 acceptance prompt is authored, commit and push:

- capability-source v4 routing delta;
- topology/presentation revision v4 metadata;
- B2 exact Skill bytes;
- byte-identical F2/G3/shared v4 projections;
- generic harness changes, if needed, that do not contain exact v13 holdout prompts or expected case objects;
- deterministic candidate-integrity checks.

Record the pushed commit as `candidate_freeze_sha` and persist hashes for every v13 candidate/reference file.

#### Freeze B — holdout/oracle freeze

Only after Freeze A is remotely verified may the Orchestrator author and commit:

- exact corpus v7 prompt objects and expected semantics;
- oracle v13;
- corpus/oracle integrity assertions;
- any corpus-count/scheduling data needed by the harness that does not alter candidate bytes.

From Freeze B onward, any change to a v13 candidate/reference byte invalidates corpus v7 and oracle v13. Re-entry must allocate a new corpus/oracle/execution identity before any acceptance call.

### 6. Fresh corpus v7 design

`MG1-T023-CORPUS-v7` SHALL contain exactly `70` fresh cases, with zero exact V12 prompt reuse:

| Class | Count |
| --- | ---: |
| positive-consumer | 6 |
| positive-source-maintainer | 6 |
| positive-external-skill-trust | 6 |
| negative | 10 |
| near-miss | 30 |
| ambiguous | 4 |
| cross-profile | 4 |
| multi-intent | 4 |
| **Total** | **70** |

The false-activation denominator is therefore exactly `40` (`10` negative + `30` near-miss), giving 2.5 percentage-point empirical resolution around the frozen 5% boundary. This denominator is fixed for balanced measurement coverage, not after observing B2 results.

The 30 near-miss cases SHALL contain exactly six fresh cases in each axis:

1. unrelated source/maintainer work with no Agent Governance applicability;
2. generic Skill recommendation/installation/tooling without Agent Governance trust scope;
3. explicit Agent Governance absence/opt-out/non-applicability;
4. incidental Agent Governance mention without governed intent;
5. governance/source/Skill homonyms outside the Agent Governance product.

The 18 positive cases SHALL include lexical/semantic contrasts against every near-miss axis so improved precision cannot be obtained simply by suppressing relevant Agent Governance vocabulary.

Recommended case-id families are fixed prospectively as:

```text
C13C01..C13C06  positive-consumer
C13S01..C13S06  positive-source-maintainer
C13E01..C13E06  positive-external-skill-trust
C13N01..C13N10  negative
C13M01..C13M30  near-miss
C13A01..C13A04  ambiguous
C13X01..C13X04  cross-profile
C13I01..C13I04  multi-intent
```

Exact prompts remain intentionally unspecified at Design / Plan & Trace so they can be authored only after Freeze A.

### 7. Oracle v13 reference/challenger sequencing

Oracle v13 SHALL use:

```text
candidate_ids = [B2, F2, G3]
reference_stage_candidates = [B2]
challenger_stage_candidates = [F2, G3]
```

Consequence-first class order remains:

```text
cross-profile
ambiguous
negative
near-miss
positive-consumer
positive-source-maintainer
positive-external-skill-trust
multi-intent
```

If B2 reaches a mandatory critical failure or exact qualification futility, stop B2 immediately. If B2 is non-qualifying, the experiment terminates without F2/G3.

### 8. Host/profile and trial mechanics

Preserve the accepted v12 host envelope and trial envelope v2:

- Codex CLI `0.149.0`;
- native Windows 11;
- native backend order `elevated`, then `unelevated` fallback;
- logical sandbox order `read-only`, then `workspace-write` fallback;
- ordinary inherited Windows ACL workspace semantics;
- ignored user config and execpolicy rules;
- no dangerous bypass;
- no interactive approvals;
- apps/connectors/remote plugin catalog/multi-agent disabled;
- web search disabled;
- GPT-5.6 Sol / Medium;
- provider-free workspace gate before canary;
- unchanged synthetic local-Skill canary with `2/2` PASS for the selected complete profile;
- acceptance calls only after deterministic and host-preflight gates pass.

No V12 observation is imported. The same host cell is retained to avoid introducing a host/model change while evaluating the candidate redesign.

## Plan & Trace

### Stage 5 — Orchestrator candidate materialization

On a new explicitly authorized objective:

1. verify current protected `develop` and create/freshen `test/t023-skill-activation-topology-evals-v13` from that exact base;
2. load T061 and the exact Design authority from canonical Git;
3. materialize capability-source epoch v4 and presentation/topology revision v4;
4. materialize B2 exact bytes and byte-identical F2/G3/shared presentation copies;
5. materialize any generic harness/schema/test changes required for B2 and the 70-case shape without authoring exact holdout prompts;
6. add deterministic guards proving v3 historical assets are unchanged and F2/G3/shared v4 bytes equal their v3 sources;
7. commit/push **Freeze A** and record `candidate_freeze_sha` plus candidate hashes in T061 on the topic branch;
8. only after remote verification of Freeze A, author all 70 exact corpus v7 cases under the frozen class/axis/count design;
9. materialize oracle v13 referencing the exact Freeze A candidate hashes and corpus v7 identity;
10. add deterministic corpus/oracle/hash/scheduling/futility integrity checks and any remaining candidate-immutable harness support;
11. commit/push **Freeze B**;
12. review the complete Stage 5 branch diff and prove no candidate/reference byte changed between Freeze A and Freeze B;
13. update T061 on the topic branch to `Stage-Readiness: READY_FOR_STAGE6` only after all required candidate/oracle assets are complete and coherent;
14. publish one coherent final Stage 5 topic-branch checkpoint for Executor verification.

No provider/model call is permitted during Stage 5 materialization.

### Stage 6 — Executor execution / diagnosis / bounded repair / verification

Only after a later Orchestrator launch authorization:

1. synchronize the exact published v13 topic-branch checkpoint and verify its protected-base relationship;
2. run deterministic candidate/corpus/oracle/harness integrity gates and full repository verification;
3. prove provider/model calls issued during deterministic gates equals `0`;
4. resolve the already frozen Codex/native-Windows profile under the v12-compatible preflight sequence;
5. require synthetic canary PASS before acceptance;
6. execute Stage R for B2 using corpus v7 and oracle v13;
7. if B2 is non-qualifying/futile, stop terminally without F2/G3;
8. if B2 qualifies, execute F2/G3 under the same complete host/model/epoch and frozen holdout;
9. preserve capacity/pause-resume semantics, observation uniqueness and evidence integrity;
10. make only bounded technical repairs that do not change candidate/reference bytes, corpus prompts/expected semantics, thresholds, candidate set, selection rules or permission meaning;
11. persist `handoffs/T061-executor-handoff.json`, commit authorized repairs/evidence and push the branch.

### Stage 7 — Orchestrator convergence

ChatGPT shall review remote Git state, exact Freeze A/Freeze B ancestry, final candidate hashes, oracle/corpus integrity, Executor handoff, live observations, futility/materiality certificates, final metrics and complete branch diff.

A later T023 review shall record one of:

- qualifying B2 selected because no challenger is materially superior;
- qualifying material F2/G3 topology selected under frozen tie-break rules;
- `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE`;
- another explicit method/host/oracle blocker requiring SDD re-entry.

Only an accepted topology result may unblock T024.

## Trace matrix

| Requirement | Stage 5 projection | Stage 6 evidence | Acceptance |
| --- | --- | --- | --- |
| T061-R1 | B2 exact Skill bytes + capability-source v4 | host-observed activation records | activation metrics + near-miss behavior |
| T061-R2 | Freeze A ancestry + corpus v7 authored after it | hash/preflight evidence | no candidate tuning after holdout exposure |
| T061-R3 | oracle v13 reference set `[B2]` | scheduler/futility evidence | F2/G3 absent unless B2 qualifies |
| T061-P1/P2 | unchanged Core/engine/profile code and semantic refs | deterministic/profile/isolation tests | mandatory non-regression PASS |
| T061-P3 | F2/G3/shared byte-copy guards | candidate hash evidence | challenger bytes unchanged |
| T061-P4 | oracle thresholds | metric certificates | all qualification thresholds preserved |
| T061-P5 | oracle materiality/tie-break rules | challenger certificates | split selection only on frozen material advantage |
| T061-P6 | paired 2+1 scheduler/oracle | provider-free simulation + live schedule | no r4; critical/futility behavior exact |
| T061-P7 | no historical-path mutation | changed-path review | V12/B0/B1 history unchanged |

## Authorized Stage 6 scope

The Executor may technically repair only non-semantic harness/evidence implementation inside the already materialized v13 branch when the repair preserves all frozen Design/Plan semantics. Expected repairable implementation surfaces are:

- `evals/skill_activation_topology/_harness/**/*.py`;
- `evals/skill_activation_topology/harness.py`;
- `evals/skill_activation_topology/finalize_incomplete.py`;
- focused non-semantic deterministic tests for the harness;
- v13 evidence under `evals/skill_activation_topology/evidence/`;
- `handoffs/T061-executor-handoff.json`.

The exact Stage 5 branch diff controls the concrete list at launch. Any required repair outside that boundary requires Orchestrator review before mutation.

## Orchestrator-owned semantic assets — Executor read-only

During Stage 6 the Executor MUST NOT semantically edit:

- `docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md`;
- `docs/tasks/T061-mg1-v13-positive-anchor-reference-evaluation.md`;
- `evals/skill_activation_topology/topologies.json` candidate semantics;
- `evals/skill_activation_topology/presentations/manifest.json` semantic mappings;
- any `presentations-v4/**/SKILL.md` or shared capability reference;
- `evals/skill_activation_topology/corpus.json` prompts/classes/expected semantics;
- `evals/skill_activation_topology/oracle.json` thresholds/selection/scheduling/semantic gates;
- `evals/skill_activation_topology/trial-envelope.json` semantic trial envelope.

A suspected defect in any of these is an `ORACLE_DEFECT` / SDD re-entry condition, not Executor authority to rewrite it.

## Explicit exclusions

Do not:

- rerun or rescore V12;
- modify B0/B1 v3 presentation files or historical evidence;
- reuse any exact V12 prompt as v13 acceptance stimulus;
- change B2 candidate/reference bytes after Freeze A while retaining corpus v7/oracle v13;
- tune F2/G3 using V12 or v13 results;
- relax any threshold or critical safety gate;
- schedule F2/G3 before B2 qualifies;
- start T024;
- modify D066 or close any D066 gap;
- reopen T058;
- perform historical branch cleanup;
- introduce a release topology decision before valid prospective evidence;
- change Core/runtime/capability semantics merely to improve activation metrics.

## Acceptance criteria

- **AC-T061-1:** Freeze A exists remotely and fixes capability-source v4, presentation v4, B2 exact bytes and byte-identical F2/G3/shared challenger assets before any exact corpus v7 prompt is authored.
- **AC-T061-2:** Freeze B contains exactly 70 fresh cases with the frozen class counts; no exact V12 acceptance prompt is reused.
- **AC-T061-3:** the negative/near-miss denominator is exactly 40 with exactly six cases in each required near-miss axis.
- **AC-T061-4:** B2/F2/G3 candidate/reference hashes are unchanged between Freeze A and Freeze B and through live acceptance.
- **AC-T061-5:** oracle v13 preserves all frozen qualification, critical safety, paired 2+1, futility, materiality and tie-break semantics except the authorized B2-only reference-stage composition.
- **AC-T061-6:** deterministic regression, profile isolation, Consumer source independence, source/distribution integrity and single-install feasibility all pass.
- **AC-T061-7:** host profile preflight passes under the frozen Codex 0.149.0/native-Windows/GPT-5.6-Sol/Medium envelope before any acceptance call.
- **AC-T061-8:** if B2 is non-qualifying/futile, zero F2/G3 acceptance observations are issued.
- **AC-T061-9:** if B2 qualifies, F2/G3 execute only under the same v13 corpus/oracle/host/model epoch and are selected only by frozen D050 materiality/tie-break rules.
- **AC-T061-10:** zero prior-epoch observation enters v13 scoring.
- **AC-T061-11:** Stage 6 makes no semantic changes to Orchestrator-owned candidate/corpus/oracle assets.
- **AC-T061-12:** final evidence is sufficient for independent Orchestrator recomputation of qualification/futility, reference state, challenger materiality and terminal selection.

## Minimum verification and evidence

Before the first acceptance call, Stage 6 MUST persist evidence for at least:

- Ruff check;
- Ruff format check;
- code-health check;
- deterministic symbol-map / code-health gates applicable to the current harness;
- focused harness tests;
- full pytest;
- candidate/topology/presentation hash verification;
- Freeze A -> Freeze B candidate immutability proof;
- corpus v7 count/class/near-miss-axis uniqueness and freshness checks;
- oracle v13/corpus/presentation/trial-envelope identity checks;
- provider-free pair-scoped scheduler simulation for agree/disagree/critical/full-reference paths;
- provider/model calls during deterministic gates = `0`;
- workspace/backend/profile evidence;
- synthetic Skill canary evidence;
- all raw v13 model attempts/observations;
- finalized case aggregates and exact metric/futility/materiality certificates;
- final selection record;
- `git diff --check` and changed-path review;
- exact final branch HEAD and handoff path.

## Stop / escalation / SDD re-entry conditions

Stop before live acceptance and report the earliest affected SDD stage if:

- candidate/reference bytes cannot be frozen before holdout authoring;
- F2/G3/shared v4 copies differ from their v3 sources;
- exact V12 prompts are discovered in corpus v7;
- the 70-case/40-negative-near-miss design cannot be realized without changing the preregistered sampling rationale;
- B2 activation semantics require changing Core/runtime/capability authority;
- Codex `0.149.0` cannot realize the frozen host envelope;
- any deterministic/preflight gate fails;
- any semantic oracle/corpus/candidate defect is suspected;
- a repair would require changing B2/F2/G3/reference bytes, expected semantics, thresholds, scheduling, materiality or safety meaning after Freeze B;
- host/model/candidate/holdout identity drifts during the epoch;
- evidence cannot independently reconstruct the terminal result.

After Freeze B, a material candidate/corpus/oracle semantic correction requires a new prospective identity set; do not patch-and-continue the same acceptance epoch.

## Expected handoff

Persist:

`handoffs/T061-executor-handoff.json`

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T061-executor-handoff.json
BRANCH: test/t023-skill-activation-topology-evals-v13
HEAD: <pushed-head>
```
