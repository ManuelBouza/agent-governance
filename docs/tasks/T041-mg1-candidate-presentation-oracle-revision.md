# T041 — MG1 Candidate Presentation Oracle Revision

## Identity

- Task ID: `T041`
- Status: `PLANNED`
- Type: `orchestrator-conformance`
- Base branch: `develop`
- Owner: ChatGPT Orchestrator
- Affected task: `T023`
- Re-entry stage: `Specify`
- Oracle revision: `MG1-T023-TOPOLOGY-ORACLE-v2`
- Capability-Source-Epoch: `MG1-2026-08-25-v2`

## Trigger

T023 preflight at Executor HEAD `b7402bbaea52d7ac4342b848c73bf56a7bb4bbef` stopped with `ORACLE_DEFECT` before any live comparative trial. MG1 v1 defined candidate identities and capability mappings but not the exact host-visible Skill metadata/body/reference surfaces or deterministic load-accounting inputs. Executor construction of those surfaces would redefine the experiment's independent variable.

No comparative result exists: `0/360` live trials were executed. This revision therefore occurs before observation of candidate performance and does not tune thresholds or outcomes post hoc.

## Objective

Freeze exact B0/B1/F2/G3 activation presentations and deterministic load inputs so T023 can execute the existing corpus and selection rule without Executor-authored semantic wording.

## Requirements

1. Preserve T023 corpus membership, expected outcomes, live cell, repetition count, metrics, thresholds and selection rule.
2. Persist exact `SKILL.md` source for all seven candidate entrypoints: B0=1, B1=1, F2=2, G3=3.
3. Persist exact shared references for `consumer-lifecycle`, `source-maintainer` and `external-skill-trust`.
4. Persist a deterministic manifest mapping candidate entrypoints to exact Skill source, capability families, references and ordered load plan.
5. Define `loaded_reference_bytes` as UTF-8 byte sum of unique manifest-listed reference files loaded for the expected route. Record `SKILL.md` bytes separately as `activation_surface_bytes`.
6. Candidate construction is mechanical byte-copy only; no wording synthesis or semantic substitution.
7. Preserve one Core, one engine, one capability-source epoch, one product identity and no portable Skill-to-Skill invocation.
8. Revise MG1 presentation/oracle identity to v2 while preserving v1 blocker evidence historically.

## Frozen presentation layout

`evals/skill_activation_topology/presentations/` contains shared references, seven exact candidate `SKILL.md` files and `manifest.json` as the lossless projection specification.

B0 is the fuller unified dispatcher. B1 is the thin unified router. F2 splits by runtime profile while retaining external trust inside Consumer Governance. G3 additionally separates External Skill Trust. All use the same underlying capability semantics.

## Acceptance criteria

- Every candidate entrypoint has one exact persisted `SKILL.md`.
- Every capability route has an exact reference set and byte-accounting rule.
- v1 blocker evidence proves zero comparative trials occurred before revision.
- Corpus expectations and numeric selection thresholds remain unchanged.
- T023 can relaunch without Executor semantic authorship of candidate presentations.

## Exclusions

No runtime, Core, T022 semantics, Consumer package behavior, T023 results, corpus expectation or accepted threshold changes are authorized. The blocked T023 branch is evidence only and is not an integration source.
