# MG1 — Skill Activation Topology and Eval Pre-registration Gate

Status: `READY_FOR_INTEGRATION`  
Date: 2026-08-25  
Owner: ChatGPT Orchestrator  
Applies to: `T023`  
Test-Authorship-Mode: `mixed`  
Oracle revision: `MG1-T023-TOPOLOGY-ORACLE-v2`  
Capability-Source-Epoch: `MG1-2026-08-25-v2`  
Presentation revision: `MG1-T023-PRESENTATIONS-v2`

## Revision reason

T023 v1 preflight stopped with `ORACLE_DEFECT` at Executor HEAD `b7402bbaea52d7ac4342b848c73bf56a7bb4bbef` because MG1 had not frozen the exact host-visible B0/B1/F2/G3 Skill presentation surfaces. The blocker records `0/360` live trials. No candidate performance was observed before this revision.

This v2 revision corrects that Specify defect only. Corpus membership, expected semantic outcomes, required live cell, repetition method, metric meanings, qualifying thresholds, mandatory non-regression boundaries and final selection rule are unchanged.

## Frozen capability and topology authority

Canonical capability source: `docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md`  
Topology mapping: `evals/skill_activation_topology/topologies.json`  
Presentation manifest: `evals/skill_activation_topology/presentations/manifest.json`  
Acceptance corpus: `evals/skill_activation_topology/corpus.json` (`MG1-T023-CORPUS-v1`)  
Selection oracle: `evals/skill_activation_topology/oracle.json`

Required candidates remain exactly B0, B1, F2 and G3. All remain projections of one Agent Governance product, one Core, one shared deterministic engine and one capability-source epoch. Portable Skill-to-Skill invocation remains forbidden.

## Exact candidate presentations

The D052 oracle now includes exact `SKILL.md` sources for all seven entrypoints:

- B0: `agent-governance`;
- B1: `agent-governance-router`;
- F2: `consumer-governance`, `source-maintainer`;
- G3: `consumer-lifecycle`, `source-maintainer`, `external-skill-trust`.

The exact files live under `evals/skill_activation_topology/presentations/`. Three shared references encode the constant capability semantics: Consumer Lifecycle, Source Maintainer and External Skill Trust.

T023 candidate construction is mechanical byte-copy only according to `presentations/manifest.json`. The Executor may not synthesize, rewrite, shorten, expand or substitute activation wording or progressive references.

## Frozen trial method

Required live cell remains:

- Host: Codex
- Platform: native Windows
- Model: GPT-5.6 Sol
- Effort: Medium

Each of 30 cases is executed 3 times for each of 4 candidates in clean context: 360 scored trials. Candidate order rotates deterministically. Mechanical smoke cases do not enter acceptance scores.

If the required live cell cannot be executed reproducibly, T023 is `BLOCKED`; substitution is forbidden.

## Metrics and deterministic load accounting

The existing routing/semantic metrics remain unchanged: activation precision/recall/F1, false activation, wrong specialist, overactivation, semantic-outcome accuracy, cross-profile violations, ambiguous-context permission broadening, median/p95 loaded-reference bytes, single-install feasibility and source/distribution integrity.

The v2 presentation manifest fixes the previously missing load inputs:

- `activation_surface_bytes` = UTF-8 bytes of activated `SKILL.md` surfaces, reported separately;
- `loaded_reference_bytes` = UTF-8 byte sum of unique exact shared reference files required by the expected capability route, counted once per unique path;
- byte measures are deterministic load-model evidence, not exact token counts.

## Mandatory boundaries and thresholds

All MG1 v1 values remain unchanged. Selected candidates require deterministic/profile/source-independence PASS, one-product/source/install integrity, zero cross-profile violations, zero ambiguous permission broadening and perfect bounded behavior on cross-profile/ambiguous cases.

Qualifying thresholds remain: precision >= 0.95; recall >= 0.95; F1 >= 0.95; false activation <= 0.05; wrong specialist <= 0.05; overactivation <= 0.05; overall semantic-outcome accuracy >= 0.95.

The B0/B1 single-family reference rule, F2/G3 material-advantage rule and tie-break sequence remain byte-for-byte semantically unchanged in `oracle.json`.

## D052 ownership boundary

Frozen Orchestrator-owned semantic assets now include:

- this gate;
- `docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md`;
- `evals/skill_activation_topology/topologies.json`;
- `evals/skill_activation_topology/corpus.json`;
- `evals/skill_activation_topology/oracle.json`;
- `evals/skill_activation_topology/presentations/manifest.json`;
- all seven candidate `SKILL.md` files and three shared references under `evals/skill_activation_topology/presentations/`.

Executor ownership remains technical runner/provider adapters, isolated candidate materialization, trial execution, result collection, metric computation, load instrumentation, package-feasibility plumbing, supplementary diagnostics and ordinary regression tests.

A suspected semantic defect requires another persisted Orchestrator re-entry; the Executor must not mutate these frozen meanings.

## T023 readiness

After this T041/MG1-v2 revision is reviewed and integrated into canonical `develop`, T023 may be relaunched from a fresh baseline. The previous blocked T023 branch is evidence only and must not be merged or used as an implementation base.
