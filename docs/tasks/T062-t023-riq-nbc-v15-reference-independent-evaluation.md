# T062 — T023 RIQ-NBC v15 Reference-Independent Evaluation

Status: READY  
Stage-Readiness: READY_FOR_STAGE5  
Executor-Authorization: NOT_AUTHORIZED_PENDING_STAGE5_AND_SEPARATE_HUMAN_LAUNCH  
Owner: ChatGPT Orchestrator (D068 Stages 3–5 and semantic conformance) / Executor (Stage 6 only after separate Human launch)  
Date: 2026-09-08  
Prospective-Scientific-Branch: `test/t023-skill-activation-topology-evals-v15`

## Objective

Materialize and evaluate the T023 v15 RIQ-NBC epoch so B2, F2 and G3 are measured independently under one fixed live cell, while preserving the exact accepted v14-r1 candidate/presentation bytes and replacing only the reference-gated scheduling/selection policy defined by D074.

The experiment must determine whether an absolute-qualified topology can be selected without allowing B2 scientific non-qualification to suppress observation of F2/G3.

## Authority and trace

- `docs/decisions/D050-canonical-capability-source-and-evaluated-skill-topology.md`
- `docs/decisions/D052-specification-owned-conformance-test-authorship.md`
- `docs/decisions/D053-native-spec-driven-development.md`
- `docs/decisions/D054-executor-owned-operation-resolution-and-runbook-recipes.md`
- `docs/decisions/D061-orchestrator-branch-target-write-guard.md`
- `docs/decisions/D062-repository-long-lived-branch-protection-bootstrap.md`
- `docs/decisions/D065-semantic-executor-delegation-obligation.md`
- `docs/decisions/D068-library-first-candidate-materialization-executor-verification-boundary.md`
- `docs/decisions/D074-reference-independent-topology-qualification.md`
- `docs/reviews/T023-R26.md`
- `docs/reviews/T023-R27.md`
- `docs/reviews/T023-R28.md`
- `docs/reviews/T023-R29.md`

D074 is the semantic authority for RIQ-NBC. This Task Contract operationalizes that decision; it does not broaden it.

## Fixed scientific identities

```text
strategy:              RIQ-NBC
evaluation:            MG1-T023-EVALUATION-v15
candidate hashes:      MG1-T023-CANDIDATE-HASHES-v3
capability source:     MG1-2026-09-06-v4
topology metadata:     MG1-T023-TOPOLOGIES-v4
presentation:          MG1-T023-PRESENTATIONS-v5
corpus:                MG1-T023-CORPUS-v9
oracle:                MG1-T023-TOPOLOGY-ORACLE-v15
execution:             MG1-T023-EXECUTION-v15
trial envelope:        MG1-T023-TRIAL-ENVELOPE-v3
candidate freeze:      Freeze E, assigned in Stage 5
holdout/oracle freeze: Freeze F, assigned only after remote Freeze E verification
```

Candidate set is exactly `B2`, `F2`, `G3`. B0/B1 remain historical and unscheduled.

## Scientific branch lineage

Stage 5 MUST use the following lineage:

1. refresh and record the then-current protected `develop` HEAD;
2. revalidate D061 branch targeting and D062 effective ruleset state;
3. create `test/t023-skill-activation-topology-evals-v15` from that exact current `develop` HEAD;
4. verify the branch ref equals that base before the first mutation;
5. use clean historical Stage 5 HEAD `aea43441a424fe18003176cb05b5594b8b561a68` only as an explicit blob/provenance source;
6. never use provider-backed terminal `67884f52912aeb51821d8f7e8ae7753c40b608fc` as an ancestor or import source;
7. do not merge, rebase, cherry-pick or otherwise inherit the historical scientific branch merely to obtain the bytes.

Historical `evidence/**`, historical executor handoffs and provider-backed outputs are forbidden imports.

The v15 branch therefore has a fresh protected-`develop` ancestry plus explicit byte-source provenance, rather than provider-backed execution ancestry.

## Exact candidate/reference provenance

Clean source HEAD:

`aea43441a424fe18003176cb05b5594b8b561a68`

Source candidate manifest:

- path: `evals/skill_activation_topology/candidate-hashes-v14.json`
- Git blob: `f78b587b76ef0c06669b15fa4d0e85b393cab5b0`
- identity: `MG1-T061-CANDIDATE-HASHES-v2`

The v15 `candidate-hashes-v15.json` manifest MUST preserve these nine file bytes exactly:

| Target/source path | Source Git blob | SHA-256 |
| --- | --- | --- |
| `evals/skill_activation_topology/presentations-v5/B2/agent-governance/SKILL.md` | `1558c74a524b399b100b05dd6f1041011b8e1949` | `1edc1070fc0ea65c4fe826c67cf4da89c50456f0bc0cbce61599d1ea200dc3fe` |
| `evals/skill_activation_topology/presentations-v5/F2/consumer-governance/SKILL.md` | `64a16f403713bde80a8ebebcda9e31dbaa8fea53` | `c8410a3f76c7ec2d29d95df178751e996ae8d405170304c136a5d7e4f9a2f204` |
| `evals/skill_activation_topology/presentations-v5/F2/source-maintainer/SKILL.md` | `13f064d186af528557d1e389e271aaa684122eb1` | `b2c04992fd1162afdf2b341103a4054799c2130c627e87601f3d0627cbd0c132` |
| `evals/skill_activation_topology/presentations-v5/G3/consumer-lifecycle/SKILL.md` | `6b0261a2c677f72eb7efd88ad442eeb3b4b15bd8` | `16259bf24f29c4b4786f4d80c1957c1b8c343a720ba6ed16c1426e77ad1e3825` |
| `evals/skill_activation_topology/presentations-v5/G3/source-maintainer/SKILL.md` | `e00edee8b1a1bacbb47b01bad4492f8ddf954628` | `c463a3e8d2ffdfee67ca09feb720ab3f720c16be9e63deec3d1ce60addca0d81` |
| `evals/skill_activation_topology/presentations-v5/G3/external-skill-trust/SKILL.md` | `308ea420ab9740b3c574a87cc436a5ea8b90f0c6` | `3a5cbf42c51a2171c4024d79fcd9f819701602933ff3ba547766650d3847a685` |
| `evals/skill_activation_topology/presentations-v5/shared/consumer-lifecycle.md` | `f3898d0770486e023d50d48e89091be8033fceec` | `bbd42745f1e47c41f4643cf3d456f2f0186bc96d1f2a385768d58b9f98375b10` |
| `evals/skill_activation_topology/presentations-v5/shared/source-maintainer.md` | `68e5bb75bcff20a72638b22514e0a1ba68c6f8ac` | `80a44c1c4cf5a2134d46be38c198d4b55d244f227e012765f5bcd15b627a657d` |
| `evals/skill_activation_topology/presentations-v5/shared/external-skill-trust.md` | `737223e1b61b1c9efc6e10264735355ad1576059` | `a4bc7bd80a6ad7377d873f69a530b0fe4d4f481414c6a3a3eeb58a3be8d70e51` |

No candidate wording change is authorized.

F2/G3/shared files MUST also remain byte-equal to the corresponding `presentations-v3` paths declared by the clean source manifest. B2 has no v3 copy-equivalence requirement beyond its exact source blob/SHA-256 identity.

## Candidate hash manifest v3

Stage 5 MUST create `evals/skill_activation_topology/candidate-hashes-v15.json` with semantic schema version `2.0.0` and at least these exact fields:

```text
schema_version: 2.0.0
identity: MG1-T023-CANDIDATE-HASHES-v3
algorithm: sha256
topology_revision: MG1-T023-TOPOLOGIES-v4
presentation_revision: MG1-T023-PRESENTATIONS-v5
capability_source_epoch: MG1-2026-09-06-v4
source_stage5_head: aea43441a424fe18003176cb05b5594b8b561a68
source_manifest_path: evals/skill_activation_topology/candidate-hashes-v14.json
source_manifest_blob: f78b587b76ef0c06669b15fa4d0e85b393cab5b0
files: <the nine exact path -> SHA-256 mappings above>
source_git_blobs: <the nine exact path -> Git blob mappings above>
copy_equivalence: <the eight exact F2/G3/shared v5 -> v3 mappings from the source manifest>
```

The manifest MUST NOT self-reference the future Freeze E commit. Freeze E identity is recorded only after that commit exists and is remotely verified.

## Stage 5 materialization sequence

### Candidate Freeze E

Before Freeze E, Stage 5 may materialize only non-holdout scientific inputs and provider-free mechanics required to freeze/verify candidate identity, including:

- exact B2/F2/G3/shared bytes above;
- preserved topology/presentation/capability-source metadata required by the harness;
- `candidate-hashes-v15.json`;
- a provider-free `verify_v15_candidate_integrity.py`;
- provider-free technical scaffolding needed to execute the guard.

Before Freeze E, the v15 corpus/oracle identities `MG1-T023-CORPUS-v9` and `MG1-T023-TOPOLOGY-ORACLE-v15` MUST NOT exist on the v15 branch.

Commit Candidate Freeze E, publish it, then verify from GitHub:

- exact branch/commit identity and ancestry from the fresh protected-`develop` base;
- all nine SHA-256 values;
- all nine source Git blobs/content equivalence against `aea43441...`;
- v5-to-v3 copy equivalence for F2/G3/shared;
- absence of forbidden historical evidence/handoffs/provider-backed outputs;
- absence of v9/v15 holdout identity before Freeze E.

Freeze F is forbidden until this remote verification passes.

### Holdout/oracle Freeze F

Only after remote Freeze E verification, create and commit:

- `evals/skill_activation_topology/corpus.json` with schema `9.0.0` / identity `MG1-T023-CORPUS-v9`;
- `evals/skill_activation_topology/oracle.json` with schema `15.0.0` / oracle `MG1-T023-TOPOLOGY-ORACLE-v15` / execution `MG1-T023-EXECUTION-v15`;
- `evals/skill_activation_topology/trial-envelope.json` with schema `3.0.0` / identity `MG1-T023-TRIAL-ENVELOPE-v3`;
- provider-free `verify_v15_holdout_integrity.py`.

The Freeze E -> Freeze F semantic delta is limited to those holdout/oracle/trial-envelope/holdout-guard assets. Candidate/reference bytes, candidate hashes, presentation metadata, topology metadata and capability-source semantics MUST NOT drift.

Post-Freeze-F harness/mechanics adaptation is permitted during Stage 5 only when it does not change any frozen semantic input.

## Fresh corpus v9 construction

Corpus v9 preserves the validated 70-case geometry:

```text
positive-consumer:                 6
positive-source-maintainer:        6
positive-external-skill-trust:     6
negative:                         10
near-miss:                        30
ambiguous:                         4
cross-profile:                     4
multi-intent:                      4
total:                            70
FAR denominator:                  40
```

Near-miss axes remain balanced at six cases each:

```text
unrelated-source-maintenance
generic-skill-tooling
explicit-non-applicability
incidental-mention
homonym-outside-product
```

Every v15 prompt string MUST be newly authored after Freeze E and MUST have zero exact overlap with all prior exposed T023 acceptance corpora represented in Git, including at minimum:

- v12 corpus at `3e5bec392d0b8e5804c4efaad74b795b08dc9779`;
- v13 corpus at `d0ebe46a68c02c66dcfbb21c3dfaee43fb15c27f`;
- v14/v14-r1 corpus v8 at clean source `aea43441a424fe18003176cb05b5594b8b561a68` (Freeze D lineage `f8cee7c72688f0486211474d2678d018772e2a58`).

The holdout guard MUST load those historical corpora with Git, assert uniqueness of v15 IDs/prompts, assert exact prompt intersection count `0` for every historical corpus, and fail closed if a required historical corpus cannot be resolved.

No v12/v13/v14 observation enters v15 scoring.

## Independent scheduler

The Stage 6 acceptance scheduler is deterministic and non-blocking:

1. common deterministic/integrity gates;
2. native-Windows host/backend/workspace preflight;
3. synthetic canary 2/2;
4. acceptance measurements in fixed round-robin order `B2 -> F2 -> G3` for each ordered case/repetition;
5. run all r1 cases, then all r2 cases;
6. after r1+r2, schedule r3 only for unstable candidate/case pairs;
7. no r4.

Order is an audit/interleaving rule only. B2 scientific qualification never gates whether F2/G3 are scheduled.

B2 MUST complete its full base measurement and all required r3 observations even if interim metrics show scientific non-qualification. Exact scientific futility may stop only F2 or G3 when the frozen oracle proves that candidate cannot recover to absolute qualification; stopping one candidate does not stop the others.

Global integrity, host/backend, oracle, evidence-validity or budget failure stops the epoch and is never reclassified as B2 scientific non-qualification.

## Observation and provider-call budgets

Per candidate:

```text
70 cases * r1+r2 = 140 base valid acceptance observations
r3 only for unstable pairs
maximum = 210 valid acceptance observations
```

Global acceptance envelope:

```text
base valid observations: 420
maximum valid acceptance observations: 630
max model attempts per scheduled observation: 2
maximum acceptance model/provider attempts: 1260
synthetic canary: 2 valid observations, max 2 attempts each = 4 attempts
absolute Stage 6 provider/model attempt ceiling including canary: 1264
per-attempt timeout: 180 seconds
```

The valid-observation ceiling and provider/model-attempt ceiling are distinct invariants. Retries do not create additional valid observations.

Stage 5 provider/model calls MUST equal exactly `0`.

## Fixed live cell

```text
host: Codex
runtime: native Windows
model: GPT-5.6 Sol
reasoning: Medium
Codex CLI baseline: 0.149.0
```

The inherited behavioral/version preflight remains mandatory. A version or host mismatch is technical invalidity, not a scientific result.

## Absolute qualification gates

Every candidate is scored independently against the same frozen absolute gates:

```text
activation precision >= 0.95
activation recall >= 0.95
activation F1 >= 0.95
false activation rate <= 0.05
wrong-specialist rate <= 0.05
overactivation rate <= 0.05
semantic accuracy >= 0.95
critical cross-profile violations = 0
critical ambiguous permission broadening = 0
deterministic/profile/source/distribution/single-install/integrity gates = PASS
```

Critical gates use any-occurrence semantics. Repeated-trial metrics use the frozen 2+1 majority/median method.

## Selection regimes

### Regime A — B2 qualifies

A split candidate is eligible only if it passes every absolute gate and satisfies:

```text
F1 >= B2 + 0.03
median observed context <= 0.85 * B2
FAR <= B2
wrong-specialist <= B2 + 0.01
overactivation <= B2 + 0.01
```

If no split candidate is materially eligible, B2 is selected.

### Regime B — B2 is validly measured but scientifically does not qualify

B2 is ineligible but non-blocking. F2/G3 remain eligible only if each independently passes every absolute gate and satisfies admissibility dominance:

```text
median observed context <= 0.85 * B2
FAR <= B2
wrong-specialist <= B2 + 0.01
overactivation <= B2 + 0.01
critical violations = 0
all deterministic/non-regression gates = PASS
```

The Regime-A relative F1 `+0.03` requirement does not apply in Regime B; absolute F1 `>= 0.95` still applies.

If no split candidate is eligible, no topology is selected.

### Multiple eligible split candidates

Preserve the already specified deterministic tie-break:

1. higher F1;
2. lower FAR;
3. lower median observed context;
4. fewer entrypoints;
5. exact tie -> F2.

### Invalid B2 measurement

Technical/epoch invalidity is not scientific non-qualification. If B2 is not a valid measurement under the frozen method, fail closed and select no topology.

## D052 semantic conformance ownership

Before Stage 6, Orchestrator-owned provider-free guards MUST fail closed on at least:

### Candidate guard

- v15 identities and exact B2/F2/G3 candidate set;
- nine current SHA-256s equal the v3 manifest;
- nine current bytes equal the explicit `aea43441...` source blobs;
- F2/G3/shared v5-to-v3 copy equivalence;
- correct topology/presentation/capability-source IDs;
- forbidden historical evidence/handoff/provider-backed imports absent.

### Holdout guard

- Freeze E is an ancestor of Freeze F/current Stage 5 head;
- corpus/oracle/trial-envelope identities are exact v9/v15/v3;
- 70-case geometry, FAR denominator 40 and five balanced near-miss axes;
- unique case IDs and prompt strings;
- exact prompt overlap `0` against all required prior corpora;
- candidate/provenance assets unchanged from Freeze E;
- Freeze E -> Freeze F semantic path boundary;
- independent B2/F2/G3 scheduling and B2 non-blocking semantics;
- absolute thresholds, both selection regimes and tie-break;
- 420 base / 630 maximum valid observations;
- 1260 acceptance-attempt / 1264 total-including-canary ceilings;
- Stage 5 provider/model calls exactly `0`.

## Stage 6 pre-acceptance gate order

Stage 6 remains forbidden until a separate future Human launch is durably persisted.

If launched, Executor MUST perform provider-free verification first, with zero model/provider calls until all deterministic gates pass:

1. candidate-integrity guard;
2. holdout-integrity guard;
3. `ruff check`;
4. `ruff format --check`;
5. full `pytest`;
6. code-health/symbol-map checks required by repository policy;
7. frozen-input and scheduler characterization tests.

Only then:

8. native-Windows backend/workspace/version preflight;
9. synthetic canary 2/2;
10. full independent B2/F2/G3 acceptance schedule.

Executor evidence/handoff path for T062 is:

`handoffs/T062-executor-handoff.json`

## Acceptance criteria

Stage 5 is complete only when:

- v15 branch is rooted at the then-current protected `develop` according to D061/D062;
- exact source provenance from `aea43441...` is verified;
- Freeze E is published and remotely verified;
- fresh corpus v9/oracle v15/trial-envelope v3 are created only after Freeze E verification;
- Freeze F is published and remotely verified;
- candidate and holdout guards pass in the available provider-free Stage 5 verification surface;
- frozen semantic assets do not drift after their freeze boundaries;
- Stage 5 provider/model calls are exactly `0`;
- a Stage 5 readiness review/checkpoint is integrated on `develop`;
- no Executor has been launched.

Stage 6 acceptance and topology selection require a separate Human-selected launch and terminal Executor evidence; they are not part of Stage 5 authorization.

## Verification and required evidence

Persist/reconstruct from Git:

- exact protected-`develop` base used to create v15;
- D062 ruleset verification receipt/state;
- v15 branch HEADs for Freeze E, Freeze F and reviewed Stage 5 terminal;
- source-head/source-manifest/source-blob provenance;
- exact candidate-hash v3 manifest;
- Freeze E -> Freeze F compare/path boundary;
- corpus geometry and historical-overlap results;
- candidate/holdout guard outputs available in Stage 5;
- explicit provider/model call count `0` for Stage 5;
- later Stage 6 handoff only if separately Human-launched.

Chat-only or local-only evidence is insufficient for acceptance.

## Constraints / out of scope

- Do not tune B2/F2/G3/shared bytes.
- Do not reuse v14 exact prompts.
- Do not import v12/v13/v14 observations into v15 scoring.
- Do not inherit or copy provider-backed evidence from `67884f52...`.
- Do not reuse historical Stage 6 launch gates.
- Do not launch an Executor during Stage 5.
- Do not issue provider/model calls during Stage 5.
- Do not start T024 before accepted T023 topology selection.
- Do not modify or silently close D066 intentional gaps.
- Do not reopen T058.
- Do not rewrite, reset, rebase, clean or force-push historical scientific branches.

## Rollback / fail-closed behavior

Before Freeze E, a defective v15 topic branch may be abandoned without mutating `develop` or historical branches.

After Freeze E or Freeze F is published, do not rewrite the freeze. A materialization or semantic defect requires an explicit successor iteration/branch/epoch with preserved failed evidence.

Any lineage ambiguity, candidate-byte mismatch, historical-corpus resolution failure, holdout leakage, provider call during Stage 5, or frozen-asset drift is a STOP condition.