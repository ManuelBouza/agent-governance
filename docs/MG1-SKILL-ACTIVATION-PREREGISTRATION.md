# MG1 — Skill Activation Topology and Eval Pre-registration Gate

Status: `READY_FOR_INTEGRATION`  
Date: 2026-08-27  
Owner: ChatGPT Orchestrator  
Applies to: `T023`  
Test-Authorship-Mode: `mixed`  
Oracle revision: `MG1-T023-TOPOLOGY-ORACLE-v5`  
Execution epoch: `MG1-T023-EXECUTION-v5`  
Capability-Source-Epoch: `MG1-2026-08-25-v3`  
Presentation revision: `MG1-T023-PRESENTATIONS-v3`  
Corpus: `MG1-T023-CORPUS-v2`

## Restart boundary

MG1-v2 is closed `BLOCKED`; MG1-v3 is closed `EXECUTION-INCOMPLETE`; MG1-v4 is closed `EXTERNAL CAPACITY`. V4 completed 31 valid logical observations before the configured Codex account reached its usage limit; review: `docs/reviews/T023-R3.md`.

No v2/v3/v4 observation may enter the v5 acceptance score. Candidate semantics, holdout membership/expectations, thresholds and topology-selection meaning remain unchanged.

V5 is a prospective execution-method revision under `docs/tasks/T044-mg1-v5-capacity-aware-execution.md`.

## Frozen authority

- Capability source: `docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md`
- Candidate mapping: `evals/skill_activation_topology/topologies.json`
- Exact presentation manifest: `evals/skill_activation_topology/presentations/manifest.json`
- Candidate presentation sources: `evals/skill_activation_topology/presentations-v3/`
- Acceptance holdout: `evals/skill_activation_topology/corpus.json`
- Selection/execution oracle: `evals/skill_activation_topology/oracle.json`

Required candidates remain B0, B1, F2 and G3. All remain projections of one Agent Governance product, one Core, one shared engine and one capability-source epoch. Portable Skill-to-Skill invocation remains forbidden.

## Capacity-aware v5 execution

Required live cell remains Codex / native Windows / GPT-5.6 Sol / Medium. The v5 acceptance epoch starts from zero and requires 40 x 4 x 3 = **480 logical scored observations**.

Each logical observation permits at most two **model attempts**, each using a fresh Codex thread/disposable workspace, frozen inputs and a 600-second timeout. A timeout, malformed response or non-capacity provider failure consumes an attempt. The first valid structured response is the sole scored result. Two failed non-capacity model attempts block the epoch and partial scoring is forbidden.

An explicit provider/account `usage-limit` or quota-capacity event before a valid model result is an **external capacity event**, not a model attempt. It is retained as diagnostic evidence, leaves the logical observation pending at the same attempt ordinal and stops new scheduling promptly.

The same v5 epoch may resume after capacity becomes available. Previously valid v5 observations remain authoritative and MUST NOT be rerun or replaced. Resume must verify exact epoch/frozen hashes/harness/runtime identities, completed-observation uniqueness, attempt ordinals and evidence integrity before issuing new live calls.

Before launch/resume the Executor may issue at most one non-scored fixed synthetic capacity probe containing no holdout prompt or candidate contents. A usage-limit response prevents scheduling; a successful probe is diagnostic only.

Capacity events, pause count and elapsed wall-clock time never enter candidate scoring.

## Semantic and selection invariants

Clarification, cross-profile, context-byte accounting, mandatory non-regression conditions, routing thresholds and D050 selection percentages remain exactly those frozen before v5. `observed_context_bytes` remains the selection context metric. No threshold, expected outcome, presentation or topology-selection rule may be changed based on prior or v5 results.

## Ownership boundary

The frozen semantic assets are Orchestrator-owned under D052. Executor owns harness/provider mechanics, capacity detection, pause/resume persistence, trial isolation, byte-copy materialization, trace extraction, metric computation, evidence and ordinary technical tests.
